# Pipeline architecture

This repository owns a native-object presentation pipeline with extended-Djot as its sole authored
deck source. Repository-owned Python parses `.djot` directly and never calls a browser or a
rendered-slide converter.

## Component map

```text
ONE-TIME EXISTING-PRESENTATION IMPORT

trusted ODP -> LibreOffice temporary PPTX -> pptx_reader raw facts
  -> SlidePlan geometry -> djot_emitter -> extended-Djot + validated local assets

The imported presentation supplies structured text, list, table, image, and geometry facts only.
Ordinary source images remain assets. Difficult spatial compositions normalize into standard native
source-order layouts with review reasons; no source slide or composite region is rendered and
inserted as substitute content.

Audit status: this is the intended ownership flow, but the current reader still constructs planner
region records for positioned content. Moving that projection into `slide_plan.py` remains open.

REPEATABLE BUILD

canonical extended-Djot source
  -> deck_tools.py application CLI
  -> slide_lib.cli
  -> slide_lib.terminal_output for builds
  -> slide_lib.native_export
  -> slide_lib.djot_parser
  -> typed native slide-object model
  -> slide_lib.layouts using the format-neutral OTP theme
  -> python-pptx editable PPTX interchange artifact
  -> background-free native PPTX intermediate
  -> LibreOffice content ODP
  -> authoritative OTP master and styles applied to editable ODP
  -> LibreOffice PDF from that themed ODP

genetics/xlect99-template_2023.otp
  -> slide_lib.presentation_theme
  -> shared 16:10 geometry, title, gradient, and outline semantics
  -> slide_lib.pptx_theme adapter and slide_lib.odp_theme master application
```

The PDF path is intentionally downstream of editable ODP. Rendering a final ODP-derived PDF for
visual QA is separate from the production object-conversion chain and never supplies slide content.

## Ownership boundaries

| Owner | Responsibility | Artifact |
| --- | --- | --- |
| `deck_tools.py` | Sole user-facing application entry point | Build, import, lint, and visibility commands |
| `slide_lib/cli.py` | Argument parsing and direct operation dispatch | Format-neutral command routing |
| `slide_lib/importers/odp_to_djot.py` | ODP visibility and normalization | Djot source and assets |
| `slide_lib/importers/odp_reader.py` | Validated ODP metadata and temporary PPTX conversion | Imported PPTX path and visibility |
| `slide_lib/importers/pptx_reader.py` | Validated PPTX extraction without output syntax | `SlideData`, runs, tables, images, and geometry |
| `slide_lib/importers/source_model.py` | Raw imported-presentation facts | Reader-to-planner/emitter records |
| `slide_lib/importers/pptx_to_djot.py` | Staged import orchestration and atomic publication | Djot source, assets, and provenance |
| `slide_lib/importers/slide_plan.py` | Geometry-first semantic planning | `SlidePlan` |
| `slide_lib/importers/topology.py` | Shared ordinary-layout topology matching | Registry-derived layout candidate |
| `slide_lib/importers/djot_emitter.py` | Escaping and atomic component-to-Djot projection | Source-located Djot components |
| `slide_lib/djot_parser.py` | Extended-Djot framing, slots, actions, and block assembly | Typed slide model |
| `slide_lib/djot_grammar.py` | Exact directive and action spellings derived from the layout registry | Shared Djot contract |
| `slide_lib/djot_lint.py` | Strict-tool invocation and source-only Djot semantics | Source diagnostics |
| `slide_lib/layouts.py` | Registry and 1280x800 logical geometry for every supported layout | Editable native objects |
| `slide_lib/presentation_theme.py` | Validated, format-neutral reading of the authoritative OTP | 16:10 page, gradient, title, and outline values |
| `slide_lib/pptx_theme.py` | Optional PPTX projection of the shared theme | Gradient, bullets, tabs, and hanging indents |
| `slide_lib/odp_theme.py` | ODP package retargeting to the authoritative template master | Editable themed ODP |
| `slide_lib/libreoffice.py` | Process preflight, conversion, and PDF filter | PPTX, ODP, and PDF conversions |
| `slide_lib/native_export.py` | Deck discovery, export stages, notes, pagination, and paths | Ordered deck and artifact paths |
| `slide_lib/terminal_output.py` | Transient progress, summaries, and expected failures | One concise Rich interface |
| `build_slides.sh` | Environment bootstrap for the folder command | One Python batch process |

`deck_tools.py` delegates command parsing to `slide_lib.cli`, which invokes reusable operations
directly. Build presentation stays in `terminal_output`, while `native_export` invokes the Djot
parser and imports the layout and LibreOffice owners. Lower-level owners do not import the
CLI or terminal interface. This one-way boundary keeps presentation, parsing, geometry, conversion,
and artifact orchestration separate.

## Existing-presentation import contract

Import normalization retains text, lists, genuine images, tables, and geometry before selecting a
target layout. `SlidePlan` is the geometry handoff: it carries a selected title, editable slot
candidates, true source-table metadata, and positive relation evidence used for native grouping.
The importer assigns a component as a complete unit and uses no deck-, slide-, or text-specific
exceptions.

Ordinary source prose and pictures project to editable Djot blocks. Direct source style, placeholder
role, actual top/group z-path, signed rotation, and normalized geometry provide the evidence for
bounded coupled relations. A visible degenerate connector retains a narrow normalized footprint
rather than being silently lost. Ordinary layout selection runs through the shared registry-topology
matcher first; special relations are positive, bounded classifications rather than exceptions.

A narrow coarse-body and picture-inset pair remains two direct editable objects in `two-panels`,
using exact source provenance and one explicit permission. Caption pairing is a single shared
positive relation grouped before topology and reuses the existing `two-plus-one` and footer
permission. Adaptive vertical image flow reserves text at 28 through 14 logical units, then uniformly
scales every image. These routes do not use slide-specific geometry exceptions.

A tightly coupled diagram and its distributed labels project as native text and genuine source
images in one standard source-order flow. Unsupported vector members are recorded for review rather
than photographed. Ambiguous or overlapping legacy geometry collapses into one standard native
panel with a review reason, making the loss of spatial semantics visible for redesign.

Publication also retains only assets reachable from the parsed Djot deck below that deck's local
`assets/` directory. Missing, unsafe, or symlinked references fail staging, and unreachable generated
files are pruned before the atomic publication step.

Only actual PPTX table metadata may become an editable native table. Header status and intentional
blank cells remain source-derived. Merged or spanned table cells require review before publication;
a diagram that merely resembles a grid stays native review content. Ambiguous component geometry
uses the documented source-order normalization rather than inventing a legacy layout match.

## Native layout contract

`slide_lib.layouts` has one distinct builder for each LibreOffice layout-grid entry:

- `blank`
- `title-only`
- `title-slide`
- `one-panel`
- `centered-text`
- `two-panels`
- `one-plus-two-panels`
- `two-plus-one-panels`
- `stacked-panels`
- `two-over-one-panels`
- `four-panels`
- `six-panels`
- `vertical-panel`
- `vertical-title-two-panels`
- `vertical-text-panel`
- `two-panels-vertical-clipart`
- `gallery`
- `multiple-choice`

The first sixteen names are the LibreOffice grid catalog. `gallery` is a repository layout for a
contained image row. LibreOffice is not asked to apply the grid: Python creates the text boxes,
lists, images, shapes, and vertical text direction directly through `python-pptx`.

Every standard slide receives the native lecture theme defined by
`genetics/xlect99-template_2023.otp`: a shallow gradient band across the top, centered standard
titles, and consistent content insets. The repository maps its 16:10 page to a stable 1280x800
logical canvas; the template's physical page size is not an authoring contract. Each Djot list item
becomes its own presentation paragraph. Nine outline levels define separate bullet positions, text
tab stops, and hanging indents so wrapped lines align with the text. ODP pages reference the actual
template master, PDF is exported from that ODP, and PPTX mirrors the same values as an interchange
adapter. No browser or CSS runtime participates in this theme path.

Each Djot slide begins with exact `=== layout: <name>` and uses exact `@<slot>` directives. The
layout registry is the authority for legal layout and slot names, including asymmetric slots:
`one-plus-two-panels` uses `left`, `top-right`, and `bottom-right`; `two-plus-one-panels` uses
`top-left`, `bottom-left`, and `right`; `two-panels-vertical-clipart` uses `top-left`,
`bottom-left`, and `right-clipart`. `gallery` accepts a slide title and two through six component
images. An ordinary panel may also contain up to six genuine images in a native row or source-order
flow. Layout validation reports unsupported or overflowing source rather than emitting a raster
fallback.

Ordinary panel layouts accept zero or one global H1. Each ordinary cell may also carry one local H2
followed by native text, images, or one source-derived table. A validated table renders only in a
layout region with a native table destination. Before any shape is created, the layout preflight
gives a local heading its required height and fits body text from 28 down to 14 logical units. A
title, heading, table, or body that cannot fit reports its source location before a partial slide
can exist.

## Extended-Djot language boundary

The Djot front end accepts exact whole-line layout and slot directives, global `#` titles and `##`
subtitles where their layout permits them, `<= appear`, `=> appear`, and `=> cascade appear`.
Several H2 lines on a title slide remain one subtitle region; they are not separate title objects.
Pre-element one-line Djot attributes attach to the next element. `![alt](path)` is a component image
only when it is a complete paragraph; mixed text-and-image paragraphs receive a source-located
unsupported-subset diagnostic. Inline verbatim and validated tables with a native table destination
render as editable objects. Fenced code, display math, quote blocks, and inline math remain
source-located native-export rejections until their native owners exist; `$inline$` and
`$$display$$` remain reserved mathematics forms after strict-Djot validation.

`multiple-choice` requires exactly `@question` and `@answer`. The question includes a visible choice
list; the answer is one or two short editable flat paragraphs with implicit object-appear intent.
The native builder and headless LibreOffice bridge preserve that timing intent, but attended Impress
first-advance observation remains open. `<= blue overlay` is recognized and rejected as not yet
supported. Attributes and other valid Djot constructs without an editable native mapping also fail
source-located rather than disappearing.

## Verification lanes

| Lane | Establishes |
| --- | --- |
| Fast Python tests | Parser, layout validation, native object construction, and source diagnostics |
| Native semantic E2E | PPTX/ODP text, lists, links, component images, template master, counts, and no full-slide image |
| ODP-derived PDF review | Final-page containment and visual teaching clarity |
| Strict Jotdown gate | Raw-Djot syntax before project slide semantics |
| Importer acceptance | Source conversion, full-corpus build, provenance, and visual comparisons |
| Native all-format acceptance | Eight sequential editable PPTX, ODP, and PDF exports with matching counts |
| M5 permanent structural tests | Bounded OOXML timing structure and parser attachment rules |
| LibreOffice bridge and PDF | One-time timing package semantics, editable ODP objects, and final PDF state |
| Attended Impress check | Click-by-click reveal playback |

No one lane proves the complete product. Fast tests cannot prove LibreOffice conversion, and a
rendered page cannot prove editability. The E2E build verifies the ordered PPTX-to-ODP-to-PDF path.
The strict Jotdown gate is a one-time/source-acceptance check, not a replacement for permanent
offline parser tests. Importer conversion, a full-corpus build, visual comparisons, and native
all-format output are likewise one-time acceptance evidence. The native gate passed through strict
lint for 8 decks/336 visible slides/185 image occurrences, `build_slides.sh genetics`, the Djot
native-layout E2E, and eight sequential matching PPTX/ODP/PDF exports with editable text/direct
images and the Lecture 02e native table retained. Permanent pytest remains offline, fast, and
deterministic.
M5 permanent tests passed separately from its one-time bridge/PDF evidence. The bridge/PDF evidence
passed; attended Impress playback remains open because macOS permissions blocked slideshow control.
See [wp_a1_animation_fidelity.md](active_plans/reports/wp_a1_animation_fidelity.md).

## Durable source boundary

After one-time import, each deck has one selected canonical source form and local assets. PPTX, ODP,
and PDF are reproducible products. Imported ODP or PPTX evidence does not become a second authored
source.

See [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md), [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md), and
[USAGE.md](USAGE.md) for the corresponding requirement, rationale, and authoring contract.
