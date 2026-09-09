# Pipeline architecture

This repository owns a native-object presentation pipeline with extended-Djot as its sole authored
deck source. Repository-owned Python parses `.djot` directly and never calls a browser or a
rendered-slide converter.

## Component map

```text
ONE-TIME EXISTING-PRESENTATION IMPORT

trusted ODP -> bounded ODF archive/XML/manifest facts
  -> odp_reader raw facts -> SlidePlan geometry -> djot_emitter
  -> staged Djot validation and reachable local assets -> non-overwriting publication

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
  -> slide_lib.layout_engine compiles one immutable CompilationResult
  -> slide_lib.odp_export writes native page layouts and editable ODF objects
  -> LibreOffice PDF from that native ODP

genetics/xlect99-template_2023.otp
  -> slide_lib.presentation_theme
  -> shared 16:10 geometry, title, gradient, and outline semantics
  -> native ODP export
```

## Current direct-adapter architecture

The completed [native ODP layout migration](archive/native_odp_layout_migration.md) established
the direct native ODP construction path:

```text
semantic Deck + PresentationTheme.template_path
  -> compile_layout_deck(Deck, PresentationTheme) -> CompilationResult(LayoutDeck, diagnostics)
  -> write_odp(LayoutDeck, PresentationTheme, Path) -> editable ODP -> LibreOffice PDF
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

ODP export derives package-only OFL-compliant renamed copies of those six validated font bytes as
face-specific `Fonts/` resources and maps each editable run to its stable ODF face declaration.
The renamed family avoids a host same-name collision while the document remains ordinary editable
ODF text; ODP remains the sole input to LibreOffice PDF conversion.

The theme's ordinary outline policy is 1.30em line spacing, serialized in the OTP as
`fo:line-height="130%"`. `ParagraphProperties` holds the resolved list text-start and hanging
indents. For every wrapped line, compilation records a safe advance equal to the greater of nominal
1.30em and that line's maximum mixed-face ascent plus descent. ODP projects this physical plan fact
unchanged; the exporter does not measure text, select leading, or derive list geometry.

The pipeline has direct-import modules with no compatibility facade: `layout_model.py` owns
immutable physical facts, `layout_engine.py` owns allocation and preflight for the twelve
LibreOffice-backed layouts plus the project-owned `multiple-choice` and `gallery` layouts,
`odp_export.py` owns ODF document/frame/package projection and `odp_text.py` owns ODF editable
text, lists, links, and tables. `PresentationTheme.template_path` is the sole template authority.

The PDF path is intentionally downstream of editable ODP. Rendering a final ODP-derived PDF for
visual QA is separate from the production object-conversion chain and never supplies slide content.

## One-to-one capacity recovery

`layout_engine` emits exactly one physical `LayoutSlide` for each source slide. It measures every
rendered text path with committed font profiles, uses quarter-point candidates, and records a
structured source-location/layout/slot diagnostic when representable content needs a size below its
readable floor. The render plan remains format-neutral; an immutable `CompilationResult` carries the
diagnostics beside it through ODP export and the normal terminal summary.

The native ODP serializer receives only point sizes at or above the shared 1 pt serializer-safe minimum.
Content that cannot fit even at that bound raises one source-located physical-capacity error before
an artifact is published. Generated ODP remains the sole production input to LibreOffice PDF
conversion.

`deck_tools.py capacity PATH` compiles selected Djot sources without writing presentation artifacts
or invoking LibreOffice, then reports the same source-located capacity diagnostics grouped by cause.

## Ownership boundaries

| Owner | Responsibility | Artifact |
| --- | --- | --- |
| `deck_tools.py` | Sole user-facing application entry point | Build, capacity, import, lint, and visibility commands |
| `slide_lib/cli.py` | Argument parsing and direct operation dispatch | Format-neutral command routing |
| `slide_lib/importers/odp_to_djot.py` | Direct ODP orchestration and staged non-overwriting publication | Djot source, assets, and provenance |
| `slide_lib/importers/odp_reader.py` | Bounded native ODP extraction | Raw runs, tables, images, notes, geometry, visibility, and page evidence |
| `slide_lib/importers/source_model.py` | Raw imported-presentation facts | Reader-to-planner/emitter records |
| `slide_lib/importers/slide_plan.py` | Positioned-fact validation and geometry-first semantic planning | Normalized regions and `SlidePlan` |
| `slide_lib/importers/topology.py` | Shared ordinary-layout topology matching | Registry-derived layout candidate |
| `slide_lib/importers/djot_emitter.py` | Escaping and atomic component-to-Djot projection | Source-located Djot components |
| `slide_lib/importers/import_report.py` | Lossless normalized-region and note diagnostics | JSON-ready migration evidence |
| `slide_lib/djot_parser.py` | Extended-Djot framing, slots, actions, and block assembly | Typed slide model |
| `slide_lib/djot_grammar.py` | Exact directive and action spellings derived from the layout registry | Shared Djot contract |
| `slide_lib/djot_lint.py` | Strict-tool invocation and source-only Djot semantics | Source diagnostics |
| `slide_lib/layout_registry.py` | Names, slots, topology, and LibreOffice classifier policies | `LayoutContract` |
| `slide_lib/layout_measurement.py` | Font-backed capacity, flow, and title measurement | Resolved physical facts |
| `slide_lib/layout_builders.py` | Format-neutral native object construction | `LayoutSlide` objects |
| `slide_lib/layout_engine.py` | Public one-to-one compilation orchestration | Immutable `CompilationResult` |
| `slide_lib/presentation_theme.py` | Validated, format-neutral reading of the authoritative OTP | 16:10 page, gradient, title, and outline values |
| `slide_lib/odp_export.py` | ODF document structure, layouts, frames, notes, images, and package orchestration | Editable ODP structure |
| `slide_lib/odp_text.py` | Editable ODF paragraphs, spans, links, native lists, tables, and text styles | ODF text and table objects |
| `slide_lib/odp_animation.py` | Source-ordered ODF/SMIL timing trees | Native reveal timing |
| `slide_lib/odf_package.py` | Bounded ODF package validation and atomic publication | Validated ODP package |
| `slide_lib/libreoffice.py` | Process preflight and PDF conversion | ODP-derived PDF |
| `slide_lib/native_export.py` | Deck discovery, export stages, notes, and paths | Ordered deck and artifact paths |
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
permission. Adaptive vertical image flow starts ordinary text at 28 pt and records a fit below the
20 pt body floor before uniformly scaling every image. These routes do not use slide-specific
geometry exceptions.

A tightly coupled diagram and its distributed labels project as native text and genuine source
images in one standard source-order flow. Dense fields use a visible redesign diagnostic while the
import report retains every label's raw runs, safe link, source order, and normalized bounds.
Unsupported vector members are recorded for review rather than photographed. Ambiguous or
overlapping legacy geometry collapses into one standard native panel with a review reason, making
the loss of spatial semantics visible for redesign.

Publication retains only assets reachable from the parsed Djot deck below that deck's local
`assets/` directory. Missing, unsafe, or symlinked references fail staging; unreachable generated
files are pruned before non-overwriting publication. A private same-parent staging directory writes
assets first, atomically renames the asset directory, then commits the Djot file as the marker of a
complete import. A failed commit uses bounded rollback of only the staged publication.

Only actual ODP table metadata may become an editable native table. Header status and intentional
blank cells remain source-derived. Merged or spanned table cells require review before publication;
a diagram that merely resembles a grid stays native review content. Ambiguous table-bearing
geometry isolates every table in its own exact native grid cell; other ambiguous components use the
documented source-order normalization rather than inventing a legacy layout match.

## Authoring contract

[DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md) is the single normative authoring reference. It owns
legal layouts and slots, root content, supported blocks, component images, tables, and reveal
spellings. `layout_registry` remains the implementation authority for the catalog, while
`layout_engine` compiles its contracts into a `CompilationResult` and `odp_export` writes native
LibreOffice page-layout references and editable frames.

The compiler keeps each built-in identity distinct from its editable frames. LibreOffice's ODF
importer uses classifier-only `title`, `subtitle`, `outline`, `object`, and `graphic` tokens with
placeholder ordering and position to select a built-in layout. The mapping follows LibreOffice's
[`AutoLayout` enum](https://github.com/LibreOffice/core/blob/master/include/xmloff/autolayout.hxx),
[ODF importer](https://github.com/LibreOffice/core/blob/master/xmloff/source/draw/ximpstyl.cxx),
and installed `layoutlist.xml` definitions.

At the physical-object boundary, `title-slide` uses the theme's master title and outline frames,
and `section` uses its master outline frame with centered, middle-aligned text. `title-only` keeps
its native title placeholder and places following root-body objects as ordinary editable objects in
the free body region. [DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md) owns the author-facing rules.

Folder `pdf` and `all` builds stage their generated ODPs, preflight the closed desktop once, and
run direct headless `soffice` conversions one ODP at a time in source order. Each command has
`--norestore`, the Impress PDF filter, and an output directory; it must create its expected PDF.
The converter waits two seconds between files. Only after the complete staged result set succeeds
does publication replace final PDFs.

## Verification lanes

| Lane | Establishes |
| --- | --- |
| Fast Python tests | Parser, layout validation, native object construction, and source diagnostics |
| Native semantic E2E | ODP text, lists, links, component images, template master, counts, and no full-slide image |
| ODP-derived PDF review | Final-page containment and visual teaching clarity |
| Strict Jotdown gate | Raw-Djot syntax before project slide semantics |
| Importer acceptance | Source conversion, full-corpus build, provenance, and visual comparisons |
| Native all-format acceptance | Eight sequential editable ODP and LibreOffice-derived PDF exports with matching counts |
| M5 permanent structural tests | Bounded ODF/SMIL timing structure and parser attachment rules |
| LibreOffice ODP round trip and PDF | Native layout retention, editable ODP objects, and final PDF state |
| Attended Impress check | Click-by-click reveal playback |

### Advisory visual review

LibreOffice converts the generated editable ODP to the PDF used for every generated-slide visual
review. Standalone review supplies that generated PDF page and the
[visual rubric](SLIDE_VISUAL_REVIEW_RUBRIC.md), then records five scores, a broad total band, and a
qualitative concern with its visible teaching reason. Migration review supplies the corresponding
original PDF page alongside the LibreOffice-generated PDF page and records `improved`, `roughly
equivalent`, or `materially worse` with the most important functional visual-equivalence reason.
This on-demand evidence directs presentation improvements and remains separate from build gating.

No one lane proves the complete product. Fast tests cannot prove LibreOffice conversion, and a
rendered page cannot prove editability. The E2E build verifies native ODP output, an ODP open/save
round trip, and ODP-to-PDF conversion.
It removes artifacts after success and retains diagnostic outputs after failure. Exact rendered-ink
percentages, source-line inventories, and per-run retained screenshots are not permanent acceptance
requirements.
The strict Jotdown gate is a one-time/source-acceptance check, not a replacement for permanent
offline parser tests. Importer conversion, a full-corpus build, visual comparisons, and native
all-format output are likewise one-time acceptance evidence. The native gate passed through strict
lint for 8 decks/336 visible slides/185 image occurrences, `build_slides.sh genetics`, the Djot
native-layout E2E, and ODP/PDF exports with editable text/direct images and the Lecture 02e native
table retained. Permanent pytest remains offline, fast, and
deterministic.
M5 permanent tests passed separately from its native ODP/PDF evidence. The headless evidence
passed; attended Impress playback remains open because macOS permissions blocked slideshow control.
See [wp_a1_animation_fidelity.md](active_plans/reports/wp_a1_animation_fidelity.md).

## Durable source boundary

After one-time import, each deck has one selected canonical source form and local assets. ODP and
PDF are reproducible products. Imported ODP evidence does not become a second authored source.

See [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md), [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md), and
[USAGE.md](USAGE.md) for the corresponding requirement, rationale, and authoring contract.
