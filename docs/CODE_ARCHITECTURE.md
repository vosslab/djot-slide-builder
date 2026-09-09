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
- [../slide_lib/layout_registry.py](../slide_lib/layout_registry.py),
  [../slide_lib/layout_measurement.py](../slide_lib/layout_measurement.py), and
  [../slide_lib/layout_builders.py](../slide_lib/layout_builders.py) own declarative layout
  contracts, distinct LibreOffice classifier signatures, font-backed capacity, and format-neutral
  physical object construction. [../slide_lib/multiple_choice_layout.py](../slide_lib/multiple_choice_layout.py)
  isolates the context, stem, choice, and answer measurement policy for the adaptive teaching layout.
  [../slide_lib/layout_engine.py](../slide_lib/layout_engine.py) is their public compiler boundary.
- [../slide_lib/presentation_theme.py](../slide_lib/presentation_theme.py) validates and reads the
  format-neutral theme from `genetics/xlect99-template_2023.otp`.
  [../slide_lib/odp_export.py](../slide_lib/odp_export.py) writes native ODF page layouts and
  presentation frames, while [../slide_lib/odp_text.py](../slide_lib/odp_text.py) owns editable
  paragraphs, styled spans, links, lists, and tables. Standard-layout inference tokens remain
  separate from occupied editable frame roles.
  [../slide_lib/pptx_export.py](../slide_lib/pptx_export.py) independently projects the same compiled
  plan to optional PPTX.
- [../slide_lib/layout_validation.py](../slide_lib/layout_validation.py) is the semantic gate
  between typed authored blocks and a layout: it rejects unsupported or unplaceable source with
  its canonical source location before native objects are constructed.
- [../slide_lib/editable_text.py](../slide_lib/editable_text.py) projects supported text into
  renderer-neutral editable paragraphs and source-owned reveal ranges.
  [../slide_lib/pptx_animation.py](../slide_lib/pptx_animation.py) then writes the bounded
  per-slide OOXML timing tree for supported on-click reveals; LibreOffice remains the separate
  conversion boundary rather than an animation writer.
- [../slide_lib/odf_package.py](../slide_lib/odf_package.py) validates bounded ODF ZIP packages and
  publishes them atomically. [../slide_lib/libreoffice.py](../slide_lib/libreoffice.py) preflights
  and drives headless ODP-to-PDF conversion.
- [../slide_lib/importers/](../slide_lib/importers/) imports trusted ODP or PPTX decks. The
  readers retain raw source facts, planners validate and normalize geometry before selecting
  semantic layouts, and the emitter publishes validated Djot plus local assets.
- [../slide_lib/importers/slide_plan.py](../slide_lib/importers/slide_plan.py) owns the
  deterministic, geometry-first `SlidePlan`; it uses
  [../slide_lib/importers/visual_relations.py](../slide_lib/importers/visual_relations.py) only for
  conservative visual-relation evidence. The emitter normalizes difficult spatial compositions into
  standard native source-order panels and records review reasons; it never renders source layout as
  substitute content.
- [../slide_lib/importers/import_report.py](../slide_lib/importers/import_report.py) retains raw
  text runs, safe links, source order, normalized geometry, and presenter-note text when migration
  limitations need later reconstruction.
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
  -> slide_lib.layout_engine and the format-neutral OTP theme
  -> native editable ODP -> LibreOffice PDF
  -> optional sibling editable PPTX
```

The one-time import path is separate:

```text
trusted ODP or PPTX
  -> slide_lib.importers reader
  -> source_model records and geometry-first SlidePlan
  -> djot_emitter
  -> validated .djot source and local assets
```

The detailed ownership and conversion boundary are documented in [PIPELINE.md](PIPELINE.md).
Imported source figures remain ordinary image assets, while surrounding text and structure become
native Djot. Unsupported relationships remain visible in source or diagnostics rather than becoming
full-slide or composite raster fallbacks.

## Testing and verification

- [../tests/](../tests/) contains the permanent fast pytest suite for CLI routing, parser and
  grammar behavior, layouts, native export, import boundaries, and repository hygiene.
- [../tests/e2e/e2e_djot_native_layouts.py](../tests/e2e/e2e_djot_native_layouts.py) is a
  non-browser native export acceptance runner and is intentionally outside normal pytest
  collection. It removes successful proof artifacts and retains failed-run diagnostics under
  `output/`.
- Run the fast suite with `source source_me.sh && python3 -m pytest tests/`.
- Run source validation through `source source_me.sh && python3 deck_tools.py lint PATH`.
  Strict-Djot validation and real LibreOffice output remain separate acceptance lanes; see
  [PIPELINE.md](PIPELINE.md) and [E2E_TESTS.md](E2E_TESTS.md).

## Extension points

- Add a supported presentation layout to
  [../slide_lib/layout_registry.py](../slide_lib/layout_registry.py), then implement its physical
  allocation in the compiler-side layout modules before either adapter projects it.
- Add a typed source construct in [../slide_lib/native_model.py](../slide_lib/native_model.py),
  its parser support, and a native layout owner before accepting it in authored source.
- Add trusted-import extraction or planning behavior under
  [../slide_lib/importers/](../slide_lib/importers/) without moving normalized-region ownership out
  of `slide_plan.py` or output syntax out of `djot_emitter.py`.
- Add permanent behavior-focused coverage under [../tests/](../tests/); reserve complete native
  application runs for [../tests/e2e/](../tests/e2e/).

## Known gaps

- Verify attended LibreOffice Impress click playback before claiming final reveal playback support;
  [ROADMAP.md](ROADMAP.md) tracks that acceptance task.
- Decide whether presenter notes need authored Djot syntax before promoting their losslessly
  retained import-report text into rebuilt native note objects.
