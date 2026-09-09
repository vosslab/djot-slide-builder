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

The reader returns raw positioned facts. `slide_plan.py` validates and normalizes their geometry at
one trusted boundary before semantic planning.

CURRENT REPEATABLE BUILD

canonical extended-Djot source
  -> deck_tools.py application CLI
  -> slide_lib.cli
  -> slide_lib.terminal_output for builds
  -> slide_lib.native_export
  -> slide_lib.djot_parser
  -> typed native slide-object model
  -> slide_lib.layout_engine compiles one immutable LayoutDeck
  -> slide_lib.odp_export writes native page layouts and editable ODF objects
  -> LibreOffice PDF from that native ODP
  -> slide_lib.pptx_export writes an optional sibling editable PPTX

genetics/xlect99-template_2023.otp
  -> slide_lib.presentation_theme
  -> shared 16:10 geometry, title, gradient, and outline semantics
  -> both direct output adapters
```

## Current direct-adapter architecture

The completed [native ODP layout migration](archive/native_odp_layout_migration.md) removed
the PPTX-to-ODP construction bridge:

```text
semantic Deck + PresentationTheme.template_path
  -> compile_layout_deck(Deck, PresentationTheme) -> LayoutDeck
  -> write_odp(LayoutDeck, PresentationTheme, Path) -> editable ODP -> LibreOffice PDF
  -> write_pptx(LayoutDeck, PresentationTheme, Path) -> optional editable PPTX
```

Before `compile_layout_deck` accepts capacity, the approved WP-T2 font-metric contract resolves
every styled run to a committed, hash-verified OFL face profile. It measures Pillow `getlength()`
token-aware line breaks with OTP list text-start/hanging indents and mixed-face ascent/descent line
boxes. OpenDyslexic profiles serve ordinary text; PT Sans Narrow is available only for the shipped
face states used by displayed literal URLs, never as a fabricated italic fallback. Missing,
hash-mismatched, unresolved, or substituted faces fail before publication. Font/hash/style and all
measurement inputs participate in the cache key, so host substitution or a stale result cannot
silently alter capacity. The obsolete `0.25em` heuristic and generic 10-percent width cap are not
part of this pipeline.

The theme's ordinary outline policy is 1.30em line spacing, serialized in the OTP as
`fo:line-height="130%"`. `ParagraphProperties` holds the resolved list text-start and hanging
indents. For every wrapped line, compilation records a safe advance equal to the greater of nominal
1.30em and that line's maximum mixed-face ascent plus descent. ODP and PPTX project this physical
plan fact unchanged; neither adapter measures text, selects leading, or derives list geometry.

The pipeline has direct-import modules with no compatibility facade: `layout_model.py` owns
immutable physical facts, `layout_engine.py` owns all 18-layout allocation/pagination/preflight,
`odp_export.py` owns ODF document/frame/package projection, `odp_text.py` owns ODF editable text,
lists, links, and tables, and `pptx_export.py` owns PPTX projection.
`PresentationTheme.template_path` is the sole template authority. ODP and PDF builds do not create
or read PPTX.

The PDF path is intentionally downstream of editable ODP. Rendering a final ODP-derived PDF for
visual QA is separate from the production object-conversion chain and never supplies slide content.

## Continuation policy

`layout_engine` owns continuation before either adapter receives a `LayoutDeck`. A logical source
slide is initially one panel. Only a real fit failure may expand it when `paginate: true`; a
`paginate: false` source instead fails at its source location before output publication. The
fallback order is: reduce ordinary text only to 24 pt; partition whole paragraphs, root-list
subtrees, table-row groups, and atomic objects; then, only for a root-list subtree that alone cannot
fit, recursively partition between descendant list-item subtrees. When a detached leaf needs the
full 24 pt body, its static context handoff precedes a titleless authored page; a leaf that still
cannot fit fails at its source location.

The compiler measures committed font profiles at exact requested point sizes (including
quarter-point values) and carries the result in the physical plan; it does not use a host-font
fallback. Explicit line breaks remain grapheme-safe. It uses the shared 36 pt / 28 pt defaults
and 30 pt / 24 pt floors. At the title floor, a title remains one atomic semantic unit rather than
being fragmented to satisfy a local fit. The complete `lect02a` source expands deterministically to
99 physical pages and builds through both sibling adapters; its native ODP also survives a
LibreOffice open/save round trip before PDF export.

The physical model carries an ordered `ContinuationContext` ancestor trail and the explicit display
modes `INLINE_STATIC`, `HANDOFF_STATIC`, and `METADATA_ONLY`; each physical slide has continuation
kind `NORMAL`, `AUTHORED`, or `CONTEXT_HANDOFF`. The compiler puts the minimum ancestor trail with
the new authored descendant only when that combined page fits (`INLINE_STATIC`). If it does not fit,
the compiler puts one deterministic static `CONTEXT_HANDOFF` page immediately before the detached
descendant (`HANDOFF_STATIC`). If that trail cannot fit, the descendant carries
`METADATA_ONLY` context. The descendant retains its original list level and must fit, or the
compiler raises the source-local error. This policy uses no abbreviation, clipping, or ordinary-body
subfloor. Existing `continuation_context` marks visible static repeats; context is never an authored
unit or a reveal target. Ordinary continuations repeat H1 when it fits; the H1 yields only after a
static handoff when the authored leaf needs the full body.

Every authored unit and reveal target occurs exactly once. Context-handoff pages are static with no
reveal targets; authored continuations have only local reveal targets. Physical pages retain the
same topology and the H1 recovery described above, use deterministic `source_id-pN` identities and
contiguous indexes, repeat qualified notes, and use physical page numbering. For nonvisual trails,
both output adapters serialize the ordered context into an accessibility description and a generated
continuation note. ODP and PPTX serialize that one plan and must therefore agree on physical-page
count, order, continuation kind, context mode, safe line advances, list indents, notes, and
accessibility meaning.

For a true-fit failure of an eligible generic grid, the compiler instead uses
`DECOMPOSE_TO_ONE_PANEL`. The eligible layouts are `two-panels`, `one-plus-two-panels`,
`two-plus-one-panels`, `stacked-panels`, `two-over-one-panels`, `four-panels`, and `six-panels`.
Only `paginate: true` permits this transition. A fitting grid is unchanged; a failing eligible grid
contributes all nonempty slots in canonical reading order to the same one-panel splitter used by
ordinary continuation. Every output page is a one-panel physical topology, applies the same
H1/context/notes recovery but does not repeat source slot labels, places images and tables through
the canonical one-panel rules, and retains source-grid and source-slot provenance. Content and
reveals occur once across the resulting pages, with deterministic physical identities. Semantic
layouts (including title, centered-text,
vertical, gallery, and multiple-choice layouts) do not decompose. `multiple-choice` instead uses its
full question region and, on true-fit failure, separates context, stem, and choices into measured
editable regions. The choice split and column widths adapt down to an 18 pt quiz-specific floor; a
sized answer popup uses space reserved beneath the shorter column and overlays only after its reveal.
Other semantic-layout failures, `paginate: false`, and unsplittable atomic units fail at the
originating source location before either adapter serializes.

## Ownership boundaries

| Owner | Responsibility | Artifact |
| --- | --- | --- |
| `deck_tools.py` | Sole user-facing application entry point | Build, import, lint, and visibility commands |
| `slide_lib/cli.py` | Argument parsing and direct operation dispatch | Format-neutral command routing |
| `slide_lib/importers/odp_to_djot.py` | ODP visibility and normalization | Djot source and assets |
| `slide_lib/importers/odp_reader.py` | Validated ODP metadata and temporary PPTX conversion | Imported PPTX path and visibility |
| `slide_lib/importers/pptx_reader.py` | Validated PPTX extraction without planning or output syntax | Raw runs, tables, images, and positioned facts |
| `slide_lib/importers/source_model.py` | Raw imported-presentation facts | Reader-to-planner/emitter records |
| `slide_lib/importers/pptx_to_djot.py` | Staged import orchestration and atomic publication | Djot source, assets, and provenance |
| `slide_lib/importers/slide_plan.py` | Positioned-fact validation and geometry-first semantic planning | Normalized regions and `SlidePlan` |
| `slide_lib/importers/topology.py` | Shared ordinary-layout topology matching | Registry-derived layout candidate |
| `slide_lib/importers/djot_emitter.py` | Escaping and atomic component-to-Djot projection | Source-located Djot components |
| `slide_lib/importers/import_report.py` | Lossless normalized-region and note diagnostics | JSON-ready migration evidence |
| `slide_lib/djot_parser.py` | Extended-Djot framing, slots, actions, and block assembly | Typed slide model |
| `slide_lib/djot_grammar.py` | Exact directive and action spellings derived from the layout registry | Shared Djot contract |
| `slide_lib/djot_lint.py` | Strict-tool invocation and source-only Djot semantics | Source diagnostics |
| `slide_lib/layout_registry.py` | Names, slots, topology, and LibreOffice classifier policies | `LayoutContract` |
| `slide_lib/layout_measurement.py` | Font-backed capacity, flow, and continuation measurement | Resolved physical facts |
| `slide_lib/layout_builders.py` | Format-neutral native object construction | `LayoutSlide` objects |
| `slide_lib/layout_engine.py` | Public compilation and continuation orchestration | Immutable `LayoutDeck` |
| `slide_lib/presentation_theme.py` | Validated, format-neutral reading of the authoritative OTP | 16:10 page, gradient, title, and outline values |
| `slide_lib/odp_export.py` | ODF document structure, layouts, frames, notes, images, and package orchestration | Editable ODP structure |
| `slide_lib/odp_text.py` | Editable ODF paragraphs, spans, links, native lists, tables, and text styles | ODF text and table objects |
| `slide_lib/odp_animation.py` | Source-ordered ODF/SMIL timing trees | Native reveal timing |
| `slide_lib/odf_package.py` | Bounded ODF package validation and atomic publication | Validated ODP package |
| `slide_lib/pptx_export.py` | Optional direct OOXML projection of the shared plan and theme | Editable PPTX |
| `slide_lib/libreoffice.py` | Process preflight and PDF conversion | ODP-derived PDF |
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
permission. Adaptive vertical image flow starts ordinary text at 28 pt and rejects a fit below the
24 pt build floor before uniformly scaling every image. These routes do not use slide-specific
geometry exceptions.

A tightly coupled diagram and its distributed labels project as native text and genuine source
images in one standard source-order flow. Dense fields use a visible redesign diagnostic while the
import report retains every label's raw runs, safe link, source order, and normalized bounds.
Unsupported vector members are recorded for review rather than photographed. Ambiguous or
overlapping legacy geometry collapses into one standard native panel with a review reason, making
the loss of spatial semantics visible for redesign.

Publication also retains only assets reachable from the parsed Djot deck below that deck's local
`assets/` directory. Missing, unsafe, or symlinked references fail staging, and unreachable generated
files are pruned before the atomic publication step.

Only actual PPTX table metadata may become an editable native table. Header status and intentional
blank cells remain source-derived. Merged or spanned table cells require review before publication;
a diagram that merely resembles a grid stays native review content. Ambiguous table-bearing
geometry isolates every table in its own exact native grid cell; other ambiguous components use the
documented source-order normalization rather than inventing a legacy layout match.

## Current native layout contract

`slide_lib.layout_registry` declares one contract for each supported layout:

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

The first sixteen names are the LibreOffice grid catalog. `gallery` and `multiple-choice` are
repository teaching layouts. `layout_engine` compiles all 18 into `LayoutDeck`; `odp_export` writes
native LibreOffice page-layout references and presentation frames, while `pptx_export` projects the
same plan independently.

| Djot layout | LibreOffice built-in identity |
| --- | --- |
| `blank` | `AUTOLAYOUT_NONE` |
| `title-only` | `AUTOLAYOUT_TITLE_ONLY` |
| `title-slide` | `AUTOLAYOUT_TITLE` |
| `one-panel` | `AUTOLAYOUT_TITLE_CONTENT` |
| `centered-text` | `AUTOLAYOUT_ONLY_TEXT` |
| `two-panels` | `AUTOLAYOUT_TITLE_2CONTENT` |
| `one-plus-two-panels` | `AUTOLAYOUT_TITLE_CONTENT_2CONTENT` |
| `two-plus-one-panels` | `AUTOLAYOUT_TITLE_2CONTENT_CONTENT` |
| `stacked-panels` | `AUTOLAYOUT_TITLE_CONTENT_OVER_CONTENT` |
| `two-over-one-panels` | `AUTOLAYOUT_TITLE_2CONTENT_OVER_CONTENT` |
| `four-panels` | `AUTOLAYOUT_TITLE_4CONTENT` |
| `six-panels` | `AUTOLAYOUT_TITLE_6CONTENT` |
| `vertical-panel` | `AUTOLAYOUT_VTITLE_VCONTENT` |
| `vertical-title-two-panels` | `AUTOLAYOUT_VTITLE_VCONTENT_OVER_VCONTENT` |
| `vertical-text-panel` | `AUTOLAYOUT_TITLE_VCONTENT` |
| `two-panels-vertical-clipart` | `AUTOLAYOUT_TITLE_2VTEXT` |

The compiler carries each built-in identity separately from the editable frames that occupy the
slide. This is required because LibreOffice's ODF importer uses classifier-only `object`, `graphic`,
`vertical_title`, and `vertical_outline` tokens plus placeholder ordering and horizontal position.
Those tokens select the built-in layout; they do not retype authored outline frames. The mapping
follows LibreOffice's
[`AutoLayout` enum](https://github.com/LibreOffice/core/blob/master/include/xmloff/autolayout.hxx),
[ODF importer](https://github.com/LibreOffice/core/blob/master/xmloff/source/draw/ximpstyl.cxx),
and current installed `layoutlist.xml` definitions.

Generated ODP exposes all sixteen signatures. LibreOffice retains the fifteen nonblank identities
through `ODP -> FODP -> ODP`; it normalizes a completely empty blank page's saved layout reference
to its title-slide definition while keeping the page empty. The E2E records that application
behavior instead of adding hidden content to force a blank-layout label.

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
`top-left`, `bottom-left`, and `right`; `vertical-title-two-panels` uses `text` over `chart`; and
`two-panels-vertical-clipart` uses side-by-side `left` and `right` vertical members. `gallery`
accepts a slide title and two through six component images. An ordinary panel may also contain up
to six genuine images in a native row or source-order flow. Layout validation reports unsupported
or overflowing source rather than emitting a raster fallback.

Ordinary panel layouts accept zero or one global H1. Each ordinary cell may also carry one local H2
followed by native text, images, or one source-derived table. A validated table renders only in a
layout region with a native table destination. Before any shape is created, the layout preflight
gives a local heading its required height, starts ordinary body/list text at 28 pt, and rejects a
fit below the 24 pt body floor. Standard titles start at 36 pt and reject a fit below 30 pt. Native
shrink-on-overflow is only a font-metric safety net after that preflight. A title, heading, table,
or body that cannot fit reports its source location before a partial slide can exist.

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
The native adapters and headless LibreOffice round trip preserve that timing intent, but attended Impress
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
| LibreOffice ODP round trip and PDF | Native layout retention, editable ODP objects, and final PDF state |
| Attended Impress check | Click-by-click reveal playback |

No one lane proves the complete product. Fast tests cannot prove LibreOffice conversion, and a
rendered page cannot prove editability. The E2E build verifies sibling PPTX/ODP output, an ODP
open/save round trip, and ODP-to-PDF conversion.
It removes artifacts after success and retains diagnostic outputs after failure. Exact rendered-ink
percentages, source-line inventories, and per-run retained screenshots are not permanent acceptance
requirements.
The strict Jotdown gate is a one-time/source-acceptance check, not a replacement for permanent
offline parser tests. Importer conversion, a full-corpus build, visual comparisons, and native
all-format output are likewise one-time acceptance evidence. The native gate passed through strict
lint for 8 decks/336 visible slides/185 image occurrences, `build_slides.sh genetics`, the Djot
native-layout E2E, and eight sequential matching PPTX/ODP/PDF exports with editable text/direct
images and the Lecture 02e native table retained. Permanent pytest remains offline, fast, and
deterministic.
M5 permanent tests passed separately from its native ODP/PDF evidence. The headless evidence
passed; attended Impress playback remains open because macOS permissions blocked slideshow control.
See [wp_a1_animation_fidelity.md](active_plans/reports/wp_a1_animation_fidelity.md).

## Durable source boundary

After one-time import, each deck has one selected canonical source form and local assets. PPTX, ODP,
and PDF are reproducible products. Imported ODP or PPTX evidence does not become a second authored
source.

See [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md), [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md), and
[USAGE.md](USAGE.md) for the corresponding requirement, rationale, and authoring contract.
