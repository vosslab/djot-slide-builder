# Code architecture

## Overview

This repository turns extended-Djot lecture decks into editable PPTX, ODP, and PDF
presentations. The authored source is a `.djot` deck; generated presentations are products of that
source. Trusted ODP and PPTX files enter only through the one-time import workflow.

## Major components

- [../deck_tools.py](../deck_tools.py) is the user-facing application entry point. It exposes build,
  import, lint, and ODP visibility commands.
- [../slide_lib/cli.py](../slide_lib/cli.py) parses command arguments and dispatches each operation
  without making format-specific decisions at the entry point.
- [../slide_lib/djot_parser.py](../slide_lib/djot_parser.py),
  [../slide_lib/djot_blocks.py](../slide_lib/djot_blocks.py), and
  [../slide_lib/djot_inline.py](../slide_lib/djot_inline.py) parse extended-Djot into the typed
  records in [../slide_lib/native_model.py](../slide_lib/native_model.py).
- [../slide_lib/djot_grammar.py](../slide_lib/djot_grammar.py) derives directive and action
  spellings from the layout registry. [../slide_lib/djot_lint.py](../slide_lib/djot_lint.py)
  performs source-only validation and can invoke a pinned strict-Djot tool.
- [../slide_lib/native_export.py](../slide_lib/native_export.py) discovers decks, drives export,
  and selects output paths. [../slide_lib/terminal_output.py](../slide_lib/terminal_output.py)
  presents build progress and expected failures in the terminal.
- [../slide_lib/layouts.py](../slide_lib/layouts.py) owns the native layout registry, capacity
  preflight, and editable PPTX object construction. It uses `python-pptx`, Pillow, and the text and
  animation helpers beside it.
- [../slide_lib/layout_validation.py](../slide_lib/layout_validation.py) is the semantic gate between
  typed authored blocks and a layout: it rejects unsupported or unplaceable source with its
  canonical source location before native objects are constructed.
- [../slide_lib/editable_text.py](../slide_lib/editable_text.py) projects supported text into
  renderer-neutral editable paragraphs and source-owned reveal ranges.
  [../slide_lib/pptx_animation.py](../slide_lib/pptx_animation.py) then writes the bounded
  per-slide OOXML timing tree for supported on-click reveals; LibreOffice remains the separate
  conversion boundary rather than an animation writer.
- [../slide_lib/libreoffice.py](../slide_lib/libreoffice.py) preflights and drives the headless
  LibreOffice conversion from editable PPTX to ODP and from ODP to PDF.
- [../slide_lib/importers/](../slide_lib/importers/) imports trusted ODP or PPTX decks. The
  intended boundary is that readers retain source facts, planners select geometry-backed semantic
  layouts, and the emitter publishes validated Djot plus local assets. At present,
  [../slide_lib/importers/pptx_reader.py](../slide_lib/importers/pptx_reader.py) also constructs
  positioned-content region records for the planner; [ROADMAP.md](ROADMAP.md) tracks moving that
  projection into `slide_plan.py`.
- [../slide_lib/importers/slide_plan.py](../slide_lib/importers/slide_plan.py) owns the
  deterministic, geometry-first `SlidePlan`; it uses
  [../slide_lib/importers/visual_relations.py](../slide_lib/importers/visual_relations.py) only for
  conservative, bounded exceptional visual relations. When a coupled visual cannot remain as
  separate editable objects, [../slide_lib/importers/source_region_render.py](../slide_lib/importers/source_region_render.py)
  validates the request and renders a bounded, non-full-slide PNG region.
- [../build_slides.sh](../build_slides.sh) is a thin convenience wrapper that builds every Djot
  deck below one supplied folder.

## Data flow

The normal build path is:

```text
.djot source
  -> deck_tools.py build
  -> slide_lib.cli and slide_lib.terminal_output
  -> slide_lib.native_export
  -> slide_lib.djot_parser and slide_lib.native_model
  -> slide_lib.layouts
  -> editable PPTX
  -> LibreOffice ODP
  -> LibreOffice PDF
```

The one-time import path is separate:

```text
trusted ODP or PPTX
  -> slide_lib.importers reader
  -> source_model records and geometry-first SlidePlan
  -> djot_emitter
  -> validated .djot source and local assets
```

The detailed ownership and conversion boundary are documented in
[PIPELINE.md](PIPELINE.md). In particular, imported source regions may become bounded component
images when the importer cannot retain a tightly coupled visual as separate editable objects; the
pipeline does not use a full-slide raster fallback.

## Testing and verification

- [../tests/](../tests/) contains the permanent fast pytest suite for CLI routing, parser and
  grammar behavior, layouts, native export, import boundaries, and repository hygiene.
- [../tests/e2e/e2e_djot_native_layouts.py](../tests/e2e/e2e_djot_native_layouts.py) is a
  non-browser native export acceptance runner and is intentionally outside normal pytest
  collection.
- Run the fast suite with `source source_me.sh && python3 -m pytest tests/`.
- Run source validation through `source source_me.sh && python3 deck_tools.py lint PATH`.
  Strict-Djot validation and real LibreOffice output remain separate acceptance lanes; see
  [PIPELINE.md](PIPELINE.md) and [E2E_TESTS.md](E2E_TESTS.md).

## Extension points

- Add a supported presentation layout in [../slide_lib/layouts.py](../slide_lib/layouts.py), then
  let the registry update the accepted Djot layout and slot contract.
- Add a typed source construct in [../slide_lib/native_model.py](../slide_lib/native_model.py),
  its parser support, and a native layout owner before accepting it in authored source.
- Add trusted-import extraction or planning behavior under
  [../slide_lib/importers/](../slide_lib/importers/) toward the intended reader-to-planner-to-
  emitter boundary; do not treat the current `pptx_reader.py` region projection as settled
  ownership.
- Add permanent behavior-focused coverage under [../tests/](../tests/); reserve complete native
  application runs for [../tests/e2e/](../tests/e2e/).

## Known gaps

- Verify attended LibreOffice Impress click playback before claiming final reveal playback support;
  [ROADMAP.md](ROADMAP.md) tracks that acceptance task.
- Verify whether imported presenter notes need a non-Djot preservation design before adding a new
  authoring or export contract.
- Move positioned-content region projection from `pptx_reader.py` into `slide_plan.py` before
  claiming that the raw-reader-to-geometry-planner ownership boundary is fully restored; see
  [ROADMAP.md](ROADMAP.md).
