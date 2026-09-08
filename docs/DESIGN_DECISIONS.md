# Design decisions

<!-- VENDORED HEADER: START -->
Record each durable decision about how this code and repository are shaped, once it is settled, with
the reasoning a later reader needs. Guidance Neil Voss states belongs in
[HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md), dated history in `docs/CHANGELOG.md`, open discussion in
`docs/active_plans/decisions/`. [PROPAGATED HEADER - ENTRIES BELOW ARE YOURS]
<!-- VENDORED HEADER: END -->

## Native presentation design

### Strict Djot compatibility governs the successor language

**Decision.** The successor language is an extended Djot language. It inherits every construct
supported by the pinned Djot syntax revision. Every source it accepts must be valid strict Djot and
pass every applicable Djot parser, formatter, editor rule, and linter in the project's pinned
compatibility suite before the repository's extension linter evaluates its slide semantics.

**Why.** Djot's linear, local, hard-wrap-friendly grammar is the selected authoring foundation. A
compatibility gate prevents convenience slide syntax from silently turning the language into a Djot
fork with an incompatible parser.

**Consequence.** Pin the exact Djot syntax revision and all compatibility tools before
implementation. The extension linter adds source-located layout, slot, and animation diagnostics;
it never excuses a Djot failure. Djot has no advertised official standalone linter, so a concrete
parser/formatter/editor-rule/linter inventory is required before any claim that source "passes all
Djot linters." Extended-Djot presentation source uses the upstream `.djot` suffix, so standard
Djot tooling continues to recognize it. This decision adds no language-accepting parser or renderer:
the experimental source-only linter cannot accept a source until its pinned native Djot gate passes.

**Initial suite member.** Jotdown 0.10.0, installed with its CLI, is the pinned native parser. It
runs before the source-only extension linter and accepts every imported genetics source. It is the
suite's native parser-validation lane; a clean parse is a meaningful raw-Djot lint result. It does
not provide formatting, editor-rule, or slide-semantic diagnostics, so those remaining suite lanes
still need explicit selection.

**Owner.** [djot_slide_extension_exploration.md](active_plans/decisions/djot_slide_extension_exploration.md)
and a future approved language guide.

### Djot is the sole authored deck source

**Decision.** Accept `.djot` as the only authored presentation source and parse it with the
repository-owned Djot modules.

**Why.** One source language keeps authoring, validation, import output, and native export aligned
without maintaining a second parser or compatibility vocabulary.

**Consequence.** `native_export` admits only `.djot`; ODP and PPTX import always emits Djot. The
runtime has no alternate source-language parser, suffix dispatch table, or target-selection flag.

**Owner.** `slide_lib/native_export.py`, `slide_lib/djot_parser.py`, and [PIPELINE.md](PIPELINE.md).

### Djot requirements inform the implemented grammar

**Decision.** The implemented Djot slide language makes recurring teaching structures directly
authorable: title; title and subtitle; ordinary body; nested bulleted and numbered lists; equal and
unequal panels; image/text on either side; three or four regions; image with caption; gallery;
quote or callout; and reusable named teaching layouts. The layout vocabulary must include every
default LibreOffice layout plus the custom `multiple-choice` layout. It must also support simple
Markdown images with predictable named-region placement and both inline and display equations through
LaTeX-compatible or similarly capable hand-writable syntax. It must support simple on-advance
teaching reveals: make an authored item appear or present an outline one bullet at a time.

**Why.** These lecture structures require portable spatial semantics. They define the implemented
grammar's required authoring surface and preserve room for
native-output capabilities that still need an explicit owner.

**Consequence.** The language survey uses those structures and equation support as literal source
examples. The Djot extension grammar preserves ordinary nested Djot content, avoids routine
HTML-comment or container scaffolding when possible, and map text, lists, practical equations, and
images to typed editable native slide objects. Reveal semantics remain bounded to authored
appearance order; motion paths, timing tracks, and complex choreography are outside this
requirement. Equation support must not require a scientific-publishing workflow. The 2026-09-05
exploration status is superseded by the 2026-09-06 implemented Djot parser, grammar, linter, and
native export path; native math and M5 timing still require their own acceptance evidence.

**Owner.** `slide_lib/djot_grammar.py`, `slide_lib/djot_parser.py`,
[PIPELINE.md](PIPELINE.md), and [LECTURE_LAYOUT_SURVEY.md](LECTURE_LAYOUT_SURVEY.md).

### Component images and dollar-delimited mathematics have fixed surfaces

**Decision.** The implemented language's component-image form is `![alt](path)`. Its official
mathematics forms are `$inline$` and `$$display$$`. These surfaces are unavailable for future slide,
layout, region, gallery, reveal, or styling syntax.

**Why.** The image form already has native Djot meaning.
The dollar forms are the instructor's preferred hand-writable mathematics surface and can be mapped
by a repository-owned MathJax-compatible adapter. Reserving all three prevents slide syntax from
colliding with ordinary teaching content.

**Consequence.** This reserves ordinary component images only, not extra image modifiers for
backgrounds, sizing, position, or filters. The implemented grammar owns slide starts and named slots;
`%%`, generic overlay geometry outside `multiple-choice`, and native math rendering remain open.

**Owner.** [djot_slide_extension_exploration.md](active_plans/decisions/djot_slide_extension_exploration.md)
and the future approved language guide.

### Multiple-choice is an implemented bounded layout

**Decision.** `multiple-choice` is an official layout in the implemented language catalog.
It requires exactly one `@question` slot and one `@answer` slot. The question contains the prompt
and its ordinary choice list; the answer contains one or two short, flat paragraphs in a fixed
bottom-right popup region. It carries implicit reveal intent only.

**Why.** Multiple-choice questions have a short, revealable answer. Implicit intent removes redundant
animation spelling while keeping open-ended questions out of a layout that would misstate their
teaching structure.

**Consequence.** The parser, linter, exporter, and native builder own its `@question` and `@answer`
contract. The answer occupies an editable popup region; OOXML timing and Impress first-advance
playback remain M5 acceptance questions. No generally available overlay slot follows from this
bounded layout.

**Owner.** [djot_slide_extension_exploration.md](active_plans/decisions/djot_slide_extension_exploration.md)
and a future approved language guide.

### Static linter enforces the implemented source contract

**Decision.** Provide a fast, source-only linter with pyflakes-level enforcement for the implemented
Djot language.

**Why.** The author needs immediate, source-located feedback for structural mistakes without a
browser, LibreOffice, or a rendered deck.

**Consequence.** It runs after the required strict-Djot compatibility suite, then validates slide
declarations, selected layouts, permitted titles and subtitles, slot contracts, animation attachment,
and special-layout rules. It does not establish geometry, overflow, native animation export, or
visual quality; those remain renderer and acceptance checks. Permanent parser and linter tests keep
short inputs inline, as required by the pytest policy.

**Owner.** `slide_lib/djot_lint.py`, `slide_lib/djot_parser.py`, and their deterministic tests.

### Standard Djot content covers tables and sequences

**Decision.** The implemented language accepts Djot tables and inline verbatim for native rendering
where their selected layout has an editable destination. Fenced code and `$inline$` or
`$$display$$` mathematics remain parse-valid/reserved source forms until dedicated native owners
exist.

**Why.** The Lecture 02 survey shows all four forms in normal teaching content. They are ordinary
content needs, not evidence for a custom biological notation or another slide-extension marker.

**Consequence.** Inline verbatim renders as editable fixed-width text. A validated table renders
only in a layout with a native table destination. Fenced code and mathematics receive
source-located native-export rejections until their owners are implemented. The language does not
introduce custom table, DNA-sequence, or math delimiters.

**Owner.** [djot_slide_extension_exploration.md](active_plans/decisions/djot_slide_extension_exploration.md)
and [lect02_genetics_syntax_gap_survey.md](active_plans/decisions/lect02_genetics_syntax_gap_survey.md).

### ASCII character references project Unicode

**Decision.** Permit the documented ASCII token `&prime;` in ordinary Djot text and map it to the
Unicode code point U+2032 PRIME only in the native-output pipeline after strict Djot validation.

**Why.** The author can keep source ASCII-only where typing literal Unicode is inconvenient without
abandoning Djot compatibility or accepting inaccurate curly quotes for biological prime labels.

**Consequence.** The literal ASCII token remains valid Djot source until the project projection maps
it. This is a small project-owned vocabulary, not an HTML-entity parser; add each mapping explicitly.
Never transform raw or verbatim content, whose literal spelling is part of its meaning. The strict
Djot gate and extension linter test the ASCII source separately from native-output projection.

**Owner.** [djot_slide_extension_exploration.md](active_plans/decisions/djot_slide_extension_exploration.md)
and a future approved language guide.

### Native layout registry owns geometry

**Decision.** Implement all sixteen LibreOffice layout-grid patterns and `gallery` as distinct
native builders in `slide_lib/layouts.py`.

**Why.** Editable output needs predictable native text, list, image, and shape regions. The
LibreOffice grid provides a useful visual catalog, but applying it after conversion would not create
the required objects.

**Consequence.** Every canonical slide selects one named layout and supplies its declared slots.
`native_export` imports the registry one way; source styling does not determine output geometry.

**Owner.** `slide_lib/layouts.py` and `docs/USAGE.md`.

### Djot uses visible layout and slot directives

**Decision.** Use extended Djot's visible `=== layout: <name>` declaration and named `@<slot>`
directives. Do not use `<!-- _cell: <slot> -->` as layout syntax.

**Why.** The survey shows that comment structure is precise but costly to hand-write. The desired
source must remain legible in a GitHub Markdown view without routine HTML or comment scaffolding.

**Consequence.** Do not add or migrate `_cell` parsing, imports, decks, preview behavior, or tests.
The layout registry supplies the allowed visible layout and slot vocabulary.

**Owner.** [presentation_language_choices.md](active_plans/decisions/presentation_language_choices.md).

### ODP-derived PDF is the only PDF path

**Decision.** Generate PPTX first, convert it to editable ODP, then have LibreOffice create PDF from
that ODP.

**Why.** One ordered pathway avoids a second PDF implementation and makes the distributed PDF
represent the editable classroom artifact.

**Consequence.** `build_slides.sh` retains the PPTX, ODP, and ODP-derived PDF artifacts. PDF review
rendering remains evidence only and never becomes slide content.

**Owner.** `slide_lib/native_export.py`, `build_slides.sh`, and
`tests/e2e/e2e_djot_native_layouts.py`.

### LibreOffice conversion uses its established profile

**Decision.** Run batch conversions with `--headless --norestore` and LibreOffice's established
user profile after confirming that the main desktop application is closed.

**Why.** A brand-new `-env:UserInstallation` directory forces first-profile initialization for
each conversion and produces a macOS task-policy diagnostic. LibreOffice already owns normal and
safe-mode profile behavior.

**Consequence.** Temporary directories contain converted artifacts only. `--safe-mode` is available
for explicit profile repair rather than routine isolation, and `--headless` already supplies the
non-visual batch mode. ODP-to-PDF conversion uses `impress_pdf_Export`, 70 percent JPEG quality,
150 DPI image reduction, and `SelectPdfVersion=3` for PDF/A-3b. The 150 DPI limit replaces the
unsupported 100 DPI value with the next documented resolution.

**Owner.** `slide_lib/libreoffice.py` and all LibreOffice conversion callers.

### One application CLI owns user workflows

**Decision.** `deck_tools.py` is the sole user-facing application CLI. `slide_lib/` owns reusable
behavior, and `slide_lib/cli.py` dispatches build, import, lint, and visibility operations directly.

**Why.** The repository supports build, import, lint, and visibility workflows. One entry point
makes those capabilities visible without format-specific wrappers.

**Consequence.** The former `tools/*.py` package-import wrappers have no compatibility layer.
`build_slides.sh` remains only as the folder-build convenience around `deck_tools.py build`.

**Owner.** `deck_tools.py` and `slide_lib/cli.py`.

### One terminal owner presents every build

**Decision.** Route folder builds and destination-named single-deck commands through one Rich
terminal interface. Keep `build_slides.sh` as a bootstrap wrapper and keep artifact generation free
of permanent per-stage logging.

**Why.** One presentation owner can show transient current work while leaving a concise,
consistent, redirect-safe result for every command.

**Consequence.** `deck_tools.py build` accepts a file or folder in one Python process. Folder
discovery recursively selects sorted Djot decks only, successful LibreOffice output stays captured,
and expected failures receive a concise stderr panel. Unexpected defects retain their traceback.

**Owner.** `slide_lib/terminal_output.py`, `slide_lib/native_export.py`, and `build_slides.sh`.

### Native objects replace slide rasterization

**Decision.** Native text, lists, shapes, component images, links, and notes are the only normal
output objects.

**Why.** A full-slide image loses editability, searchability, accessibility, and durable layout
ownership.

**Consequence.** Source features without an explicit native mapping remain visibly incomplete or
fail with an actionable source diagnostic. Existing layouts should retain the same instructional
text and genuine content images even when their arrangement changes; diagnostics accompany content
rather than replace it. Import never substitutes a full-slide or composite render. Temporary visual
renders may support QA but never enter canonical Djot or output.

**Owner.** `slide_lib/importers/djot_emitter.py`, `slide_lib/layouts.py`,
`slide_lib/native_export.py`, and their tests.

### The default theme normalizes lecture structure

**Decision.** Apply one native, rule-based lecture theme to standard Djot layouts: a shallow
blue-to-white top gradient, horizontally centered standard titles, consistent content margins, and
native hierarchical list paragraphs with theme-owned bullet positions, text tab stops, and hanging
indents at every supported outline level.

**Why.** The legacy lecture decks establish useful common visual rules, but reproducing their
individual quirks would weaken the consistent authoring system. Explicit presentation semantics let
PPTX, ODP, and PDF share the same intended structure.

**Consequence.** Wrapped list lines align with their paragraph text, not with the bullet. Nested
levels have distinct positions and alternating bullet forms. Title-only, title-slide, and centered
question layouts retain vertical centering where their teaching role calls for it. Exporters may
translate these native semantics, but no slide-specific pixel matching overrides the theme.

**Owner.** `slide_lib/pptx_theme.py`, `slide_lib/layouts.py`, and their native-export tests.

### Vertical root-body layouts use one author-visible block

**Decision.** `vertical-text-panel` and `vertical-panel` accept exactly one root body
block after the level-one title: a paragraph, list, or component image.

**Why.** The one authored block maps directly to one native vertical text frame or contained image
region without inventing a repository-specific Markdown wrapper language.

**Consequence.** Preview and native geometry share the fixed 94px title, 24px spacer, and 1042px
body tracks. `vertical-title-two-panels` uses 94px, 24px, 500px, 42px, and 500px tracks with
explicit child placement.

**Owner.** `slide_lib/layouts.py` and its contract tests.

### Readers extract facts and the emitter renders Djot

**Decision.** ODP and PPTX readers return raw source facts. Geometry planning assigns semantic
regions, and one Djot emitter owns escaping and output syntax.

**Why.** A reader that pre-renders output syntax can double-escape text and makes the input format
own details of the authored language.

**Consequence.** `source_model.py` carries raw runs, links, images, tables, notes, and review facts;
`slide_plan.py` owns geometry; `djot_emitter.py` renders supported source facts exactly once and
preserves imported note content without inventing Djot syntax.

**Implementation status.** The six-pass Djot-first audit found this boundary incomplete:
`pptx_reader.py` still constructs planner region records, and `djot_emitter.py` records note
omissions instead of preserving the note content. Both require design-level follow-up.

**Owner.** [PIPELINE.md](PIPELINE.md).

### The registry defines Djot layout and slot contracts

**Decision.** `slide_lib.layouts.LAYOUTS` is the authoritative catalog for canonical short layout
names and named Djot slots. The grammar derives its legal vocabulary from that registry and provides
no aliases.

**Why.** Source validation and native geometry must describe the same layouts. Derived vocabulary
keeps a later layout change local to the layout owner rather than creating parallel spelling tables.

**Consequence.** The canonical names are `one-panel`, `two-panels`, `one-plus-two-panels`,
`two-plus-one-panels`, `stacked-panels`, `two-over-one-panels`, `four-panels`, `six-panels`,
`vertical-panel`, `vertical-title-two-panels`, `vertical-text-panel`, and
`two-panels-vertical-clipart`; `blank`, `title-only`, `title-slide`, `centered-text`, and `gallery`
remain. The asymmetric layouts use named slots rather than source position.

**Owner.** `slide_lib/layouts.py` and `slide_lib/djot_grammar.py`.

### Djot normalizes headings and cells before geometry

**Decision.** Djot parses global H1/H2 headings separately from named `Cell` content. All H2 lines
on a `title-slide` form one subtitle region, and cells bind by declared slot name rather than source
order.

**Why.** A normalized IR lets both source front ends share geometry while preserving imported
title-slide subtitles and allowing authors to order named regions for readability.

**Consequence.** Layouts validate title/subtitle permission and named-cell completeness. Missing,
duplicate, unknown, and unnamed cells fail source-located. Multiple H2 lines are preserved rather
than collapsed into a single source line.

**Owner.** `slide_lib/native_model.py`, `slide_lib/djot_parser.py`, and `slide_lib/layouts.py`.

### Supported Djot constructs fail explicitly at the native boundary

**Decision.** Retain typed representations for supported Djot blocks, attributes, and reveal intent;
raise source-located errors for valid Djot constructs that have no editable native mapping.

**Why.** Silent loss would make source look accepted while omitting teaching content. A narrow,
explicit subset can expand safely when a native owner and acceptance evidence exist.

**Consequence.** One-line attributes precede their element, standalone image paragraphs become
components, and mixed image paragraphs are unsupported. Inline verbatim and validated tables with a
native table destination render as editable objects. Fenced code, `$inline$`, `$$display$$`, quote
blocks, attributes, and unsupported inline forms receive source-located native-export rejections
until their native owners exist.

**Owner.** `slide_lib/djot_blocks.py`, `slide_lib/djot_inline.py`, `slide_lib/djot_parser.py`, and
`slide_lib/layouts.py`.

### Multiple-choice carries reveal intent, not timing proof

**Decision.** `multiple-choice` requires `question` and `answer` cells. The question contains a
visible choice list; the answer is one or two short editable flat paragraphs with implicit
object-appear reveal intent and no explicit action directive.

**Why.** The layout communicates the instructional structure without making the author repeat a
redundant answer action or turning a popup into a general overlay system.

**Consequence.** The answer is placed in the fixed popup region and rejects explicit `<=` or `=>`
actions. The intent becomes a bounded OOXML animation request only when M5 builds it; attended
Impress playback remains the final visual acceptance evidence.

**Owner.** `slide_lib/layouts.py`, `slide_lib/djot_parser.py`, and
[wp_a1_animation_fidelity.md](active_plans/reports/wp_a1_animation_fidelity.md).

### Animation uses OOXML and Impress evidence

**Decision.** Build the bounded `appear` and `fade`, `object` and `paragraphs`, `on-click` animation
surface as OOXML in `slide_lib/pptx_animation.py`. LibreOffice Impress and ODP are the editing and
playback contract; PPTX is the native-builder and interchange artifact.

**Why.** Python provides stronger practical PPTX construction support, while the instructor uses
LibreOffice rather than Microsoft products. Official OOXML semantics plus observed LibreOffice
importer/exporter and Impress behavior provide a stable, replaceable boundary without external deck
templates.

**Consequence.** M5 implementation is complete. `pptx_animation.py` is the sole timing-tree owner
and builds OOXML directly; runtime XML templates and PowerPoint-authored decks are not contracts.
The permanent offline tests cover structural semantics. One-time headless PPTX-to-ODP/package and
PDF final-state evidence passed. Attended Impress playback remains the only open visual gate because
macOS denied Screen Recording and Accessibility before slideshow clicks could be observed. `blue
overlay` remains deferred.

**Owner.** `slide_lib/pptx_animation.py`, [PIPELINE.md](PIPELINE.md), and
[wp_a1_animation_fidelity.md](active_plans/reports/wp_a1_animation_fidelity.md).

## Canonical source design

### Geometry-first import plans preserve editable intent

**Decision.** Normalize trusted ODP/PPTX content into `SlidePlan` before emitting extended-Djot. The
plan carries source geometry, title evidence, independent editable components, true table metadata,
and positive visual-relation evidence used only to choose a native standard layout.

**Why.** Existing teaching slides mix ordinary semantic content with diagrams whose labels depend on
their original arrangement. Geometry-first planning can identify those relationships without making
the old rendering authoritative. A difficult slide is useful redesign evidence.

**Consequence.** The importer chooses titles from bounded upper-lane geometry and assigns native
components atomically. Ambiguous or overlapping legacy geometry normalizes into one standard
source-order panel with a review reason. Difficult slides retain their instructional text and
genuine images through an existing registered layout; review diagnostics do not replace source
content. Ordinary source pictures remain independent image assets; unsupported vectors stay
explicit in diagnostics. No rendered source slide or composite region is an import product.

**Owner.** `slide_lib/importers/slide_plan.py`, `slide_lib/importers/djot_emitter.py`,
`slide_lib/importers/pptx_to_djot.py`, and [PIPELINE.md](PIPELINE.md).

### Source table metadata controls native tables

**Decision.** Emit an editable native table only from actual source table metadata. Preserve its
source-derived header status and intentional blanks; send merged or spanned cells to review before
publication.

**Why.** A visual grid does not establish table semantics. Retaining genuine source structure keeps
native tables editable without misclassifying diagram labels as rows and columns.

**Consequence.** Inferred lattices remain diagrams or review cases. A merged or spanned source table
fails source-located rather than receiving an invented table projection. Native table rendering
therefore has a bounded, extensible input contract for future span support.

**Owner.** `slide_lib/importers/slide_plan.py`,
`slide_lib/importers/djot_emitter.py`, and `slide_lib/layouts.py`.

### Ordinary layouts preflight optional titles and local headings

**Decision.** Ordinary panel layouts accept zero or one global H1, and each ordinary cell accepts
at most one local H2. Preflight title, heading, table, image, and text capacity before creating
native shapes.

**Why.** Imported slides sometimes have an absent global title or a component-local heading. The
same source allocation must remain readable whether the title is present or absent.

**Consequence.** A titleless layout receives its full content region. Local H2 allocation adapts
from 28 down to 14 CSS px before body placement. An unsupported combination or unreadable allocation
reports the relevant source location and leaves no partial shapes.

**Owner.** `slide_lib/layout_validation.py`, `slide_lib/layouts.py`, and [PIPELINE.md](PIPELINE.md).

### Imported evidence keeps relations adaptable

**Decision.** Preserve direct source evidence for shape style, placeholder role, actual top/group
z-paths, and signed rotation beside normalized geometry. Route through the shared registry-topology
matcher before special relations; do not duplicate layout geometry in individual import relations.

**Why.** Style and ordering distinguish explanatory callouts and labels from ordinary prose, while a
single topology authority lets the importer gain layouts without changing each relation classifier.

**Consequence.** The importer may retain a visible degenerate connector through a bounded normalized
footprint and may recognize only positive, bounded relation classes. A narrow coarse-body and
picture-inset pair stays as direct editable objects in `two-panels`, with exact provenance and one
explicit permission. Caption pairing is one shared positive relation, grouped before topology and
reusing the existing `two-plus-one` and footer permission. Adaptive vertical image flow reserves text
at 28 through 14 CSS px, then scales every image uniformly. Visual relations retain source
membership only long enough to normalize it into standard native components; no private render or
geometry exception is a routing mechanism. Ambiguous arrangements become a native source-order
panel with review evidence.
Geometry, heading relations, topology, and Djot emission symbols are imported from their owning
modules. Slide planning and conversion consume those owners directly and do not re-export
compatibility facades.

**Owner.** `slide_lib/importers/geometry.py`, `slide_lib/importers/topology.py`,
`slide_lib/importers/visual_relations.py`, and `slide_lib/importers/slide_plan.py`.

### Imported assets follow source reachability

**Decision.** Publish only generated assets reachable from the parsed Djot deck and keep them below
that deck's local `assets/` directory.

**Why.** Reachability makes a regenerated deck self-contained and prevents stale extracted files from
becoming unreviewed source dependencies.

**Consequence.** Missing, unsafe, or symlinked asset references stop publication. The staged importer
prunes unreachable files before its atomic publication step. Published assets are genuine imported
content rather than rendered reconstructions of source layout.

**Owner.** `slide_lib/importers/pptx_to_djot.py`.

### Djot is the editable source

**Decision.** Import an existing ODP or PPTX once, then make the generated Djot and local assets the sole
editable source.

**Why.** One canonical state prevents Djot, PPTX, and ODP from silently diverging.

**Consequence.** Generated artifacts are reproducible. Imported ODP and temporary normalization PPTX
remain migration evidence, not future editing surfaces.

**Owner.** `deck_tools.py`, `slide_lib/importers/odp_to_djot.py`,
`slide_lib/importers/pptx_to_djot.py`, and [USAGE.md](USAGE.md).

### Structured import replaces OCR

**Decision.** Extract imported ODP/PPTX text, lists, notes, and component images as document objects.

**Why.** The source decks are authored structured documents; OCR is lower fidelity and discards
available semantics.

**Consequence.** Whole-slide source images are conversion failures. OCR is reserved only for text
that genuinely exists within a component image.

**Owner.** `slide_lib/importers/odp_reader.py` and `slide_lib/importers/pptx_reader.py`.

### Local reference projects remain outside runtime

**Decision.** Keep every `OTHER_REPOS/` clone outside the production runtime and dependency graph.

**Why.** Prior art can inform bounded implementation choices without importing incompatible syntax,
workflows, licenses, or renderer assumptions.

**Consequence.** The repository adapts verified ideas into local Python. The inventory records the
specific evidence and limitations for each clone.

**Owner.** `docs/OTHER_REPOS/` and `docs/USAGE.md`.
