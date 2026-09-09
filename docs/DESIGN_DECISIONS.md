# Design decisions

<!-- VENDORED HEADER: START -->
Record each durable decision about how this code and repository are shaped, once it is settled, with
the reasoning a later reader needs. Guidance Neil Voss states belongs in
[HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md), dated history in `docs/CHANGELOG.md`, open discussion in
`docs/active_plans/decisions/`. [PROPAGATED HEADER - ENTRIES BELOW ARE YOURS]
<!-- VENDORED HEADER: END -->

## Native presentation design

### Bundled font profiles are the measurement authority

**Decision.** Every font face the presentation pipeline emits is a versioned repository asset with
an immutable family/style key, repository-relative path, SHA-256 digest, and face index. Theme
loading verifies each asset and its intrinsic metrics before layout work begins; it never accepts an
operating-system font substitution.

**Why.** A readable-floor calculation is only meaningful when its glyph metrics are reproducible.
Host fonts and silent LibreOffice substitution turn the same Djot deck into different geometry on
different machines.

**Consequence.** OpenDyslexic regular, bold, italic, and bold italic and PT Sans Narrow regular and
bold are bundled under their SIL OFL licenses. PT Sans Narrow has no upstream italic face, so an
italic URL run fails at face selection rather than becoming synthesized or substituted. Inline code
continues to use OpenDyslexic; a future code family requires its own licensed profile before it can
be emitted or measured.

**Owner.** `slide_lib/presentation_theme.py` and `assets/fonts/PROVENANCE.md`.

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

**Decision.** Compile all sixteen LibreOffice layout-grid patterns, `gallery`, and
`multiple-choice` in `slide_lib/layout_engine.py`, the sole 18-layout compiler, into one immutable
format-neutral `LayoutDeck`. Native ODP and optional PPTX adapters consume `LayoutDeck` only and
serialize it independently.

**Why.** Editable output needs predictable native text, list, image, and shape regions. The
LibreOffice grid provides a useful visual catalog, but applying it after conversion does not create
the required objects. Keeping geometry inside a python-pptx renderer also prevents a native ODP
adapter from sharing the same placement and fit decisions.

**Consequence.** Every canonical slide selects one named layout and supplies its declared slots.
`slide_lib/layout_engine.py` exposes only `compile_layout_deck`, `registered_layout_names`, and
`layout_contract`; it delegates geometry, capacity checks, presentation roles, reading order, and
pagination to cohesive private helpers. Ownership flows from `layout_primitives.py` through
`layout_content.py` to `layout_model.py`: primitives own neutral records including `LayoutContract`,
content owns immutable editable-content records, and the model composes the complete physical plan.
In import direction, `layout_content` imports `layout_primitives`, and `layout_model` imports both;
`native_model` remains independent source-semantic authority and is imported only by the
compiler-side translation modules. `layout_registry.py` is declarative catalog data;
`layout_measurement.py` owns pure measurement/preflight/pagination/local-heading work; and
`layout_builders.py` turns resolved facts into planned objects without recomputing them. Typography
uses points in the shared plan.
Output adapters contain no layout allocation, fit-selection, or layout-registry logic, and source
styling does not determine output geometry.

**Owner.** `slide_lib/layout_primitives.py`, `slide_lib/layout_content.py`,
`slide_lib/layout_model.py`, `slide_lib/layout_engine.py`, its private helpers, and `docs/USAGE.md`.

### Layout topology has canonical identity

**Decision.** Model a semantic `PlaceholderKind` and member kind for every occupied presentation
member. Key each ODF presentation-page layout with a canonical `PresentationPageLayoutKey` containing
the declared layout identity, canvas, ordered member IDs, kinds, roles, and geometry, plus a separate
LibreOffice `AutoLayout` classifier signature for each standard layout. The key excludes authored
content.

**Why.** Layout identity is structural. A title text change must not create a different page layout,
while a placeholder-geometry change must not silently reuse one. XML layout names are opaque,
document-local serialization details and cannot serve as the identity. LibreOffice's ODF importer
infers some layouts from classifier-only `object` or `graphic` tokens even though the editable slide
members remain outline frames, so frame roles cannot double as the classifier.

**Consequence.** The compiler makes occupied topology and LibreOffice inference explicit before
either adapter runs. The ODP adapter deduplicates page layouts only by this key, assigns arbitrary
stable ODP names, writes classifier placeholders to `styles.xml`, and writes actual occupied member
roles to `content.xml`. The sixteen standard contracts map one-to-one to the current LibreOffice
catalog; `gallery` and `multiple-choice` remain repository layouts without a claimed built-in
`AutoLayout` identity. Authored text, media, notes, and decorations remain members of a planned
slide rather than inputs to page-layout identity. LibreOffice saves a completely empty blank page
with its title-slide layout reference; preserve the empty page instead of inserting hidden content
to coerce the saved label.

**Owner.** `slide_lib/layout_primitives.py`, `slide_lib/layout_registry.py`,
`slide_lib/layout_model.py`, `slide_lib/odp_export.py`, and
`tests/e2e/e2e_djot_native_layouts.py`.

### Djot uses visible layout and slot directives

**Decision.** Use extended Djot's visible `=== layout: <name>` declaration and named `@<slot>`
directives. Do not use `<!-- _cell: <slot> -->` as layout syntax.

**Why.** The survey shows that comment structure is precise but costly to hand-write. The desired
source must remain legible in a GitHub Markdown view without routine HTML or comment scaffolding.

**Consequence.** Do not add or migrate `_cell` parsing, imports, decks, preview behavior, or tests.
The layout registry supplies the allowed visible layout and slot vocabulary.

**Owner.** [presentation_language_choices.md](active_plans/decisions/presentation_language_choices.md).

### ODP-derived PDF is the only PDF path

**Decision.** Generate editable ODP directly from the format-neutral layout plan and authoritative
OTP, then have LibreOffice create PDF from that ODP. Publish optional PPTX independently from the
same compiled plan.

**Why.** One ordered ODP-to-PDF pathway makes the distributed PDF represent the editable classroom
artifact. The former blank-layout PPTX intermediate caused LibreOffice to import generated text as
custom OOXML rectangle shapes rather than layout-owned presentation frames; replacing its master and
styles afterward could not restore discarded layout identity.

**Consequence.** ODP and PDF builds never create or read PPTX. `--format all` builds ODP and PPTX as
sibling artifacts, then exports PDF from ODP. The ODP writer emits native page-layout references and
title, subtitle, outline, and object presentation frames. PDF review rendering remains evidence only
and never becomes slide content.

**Owner.** `slide_lib/odp_export.py`, `slide_lib/native_export.py`, `build_slides.sh`, and
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

**Owner.** `slide_lib/importers/djot_emitter.py`, `slide_lib/layout_engine.py`,
`slide_lib/odp_export.py`, `slide_lib/pptx_export.py`, and their tests.

### The default theme normalizes lecture structure

**Decision.** Use `genetics/xlect99-template_2023.otp` as the sole master-slide theme authority.
Load its 16:10 page ratio, native top gradient, presentation-frame geometry, typography, and
outline-level bullet geometry into a format-neutral theme model. Standard titles begin at 36 pt and
ordinary body/list text begins at 28 pt. Direct ODP inherits the template's native styles; optional
PPTX mirrors the same model.

**Why.** The legacy lecture decks establish useful common visual rules, but reproducing their
individual quirks would weaken the consistent authoring system. Explicit presentation semantics let
PPTX, ODP, and PDF share the same intended structure.

**Consequence.** The repository retains a stable 1280x800 logical layout canvas, and every accepted
template must have a 16:10 page ratio; its physical centimeter or inch dimensions may vary. The target
ODP contains the template's real master page, with its background outside the planned slide-object
stream, rather than a repeated per-slide background. Authored decorations remain planned objects with normal
reading and z order. Wrapped list lines align with their paragraph text, not with the bullet, and
nested levels have distinct bullet and text positions. Title-only, title-slide, and centered question
layouts retain vertical centering where their teaching role calls for it. Typography remains
point-valued and never passes through the logical-geometry conversion. Build preflight enforces a
30 pt title floor and 24 pt ordinary-text floor before native shrink-on-overflow protects against
small font-metric differences. CSS and browser rendering are not part of the build.

**Owner.** `genetics/xlect99-template_2023.otp`, `slide_lib/presentation_theme.py`,
`slide_lib/layout_engine.py`, `slide_lib/odp_export.py`, `slide_lib/pptx_export.py`, and their
native-export tests.

### Font metrics are versioned theme inputs, not host behavior

**Decision.** Treat every face used for layout capacity as a committed, hash-verified OFL asset with
recorded provenance. `PresentationTheme` exposes immutable profiles for exact family, weight, and
italic states; all measurement resolves styled runs against those profiles. OpenDyslexic is the
ordinary-text family. PT Sans Narrow is permitted only for displayed literal URLs and only in the
face states actually committed to the repository; it has no fabricated italic fallback.

**Why.** A system-installed font, a silent substitution, or an average-glyph estimate makes line
wrapping machine-dependent. That would allow the same deck to pass capacity on one host and shrink
or overflow on another, undermining the point-size and frame contracts.

**Consequence.** The format-neutral measurement owner uses Pillow `getlength()` over resolved
styled runs with token-aware line breaking, OTP list text-start and hanging-indent geometry, and
ascent/descent line boxes that cover mixed-face lines. Its cache key includes face hashes and every
measurement input. Missing assets, hash mismatches, unsupported styles, and profile drift fail
before publication; neither adapters nor LibreOffice may select a substitute. The rejected `0.25em`
heuristic and generic 10-percent list-width cap cannot decide fit. Permanent offline asset/profile
tests and V2 runtime-drift evidence enforce this contract before WP-L2 accepts capacity.

**Owner.** WP-T2 of the native ODP layout migration; `slide_lib/presentation_theme.py`, the
format-neutral measurement owner, committed font assets/provenance, and their focused tests.

### ODP packages retain template authority

**Decision.** Seed direct ODP from the authoritative OTP, retain its masters, `styles.xml`, and
reachable resources, replace `content.xml`, and reconcile the manifest under strict package rules.
Local automatic styles parent the shipped `Default-*` presentation styles. The ODP adapter owns
deterministic media identities.

**Why.** The template defines theme-level master visuals and presentation defaults, while each build
must publish only a self-consistent set of content and assets. Deterministic media names prevent
caller paths and insertion order from leaking into a document identity.

**Consequence.** Publication rejects duplicate or unsafe member names, missing manifest entries,
missing referenced members, unmanifested reachable non-directory members, and unreachable generated
media. Root and required directory manifest entries are explicit exceptions; retained resources
reachable through masters or styles remain valid even without a slide-object reference. Fast tests
inspect XML/package invariants only. Serialized headless LibreOffice preservation is a separate E2E
and review gate.

**Owner.** `slide_lib/odf_package.py`, `slide_lib/odp_export.py`, `slide_lib/odp_text.py`,
`tests/test_odp_export.py`, and `tests/e2e/e2e_djot_native_layouts.py`.

### Native acceptance uses evidence tiers

**Decision.** Keep deterministic, offline behavior contracts in permanent pytest. Keep one
source-built native-layout runner under `tests/e2e/` for the real PPTX/ODP/PDF and LibreOffice
round-trip boundary. Treat full-corpus builds, production-deck inspection, visual comparisons, and
rebuild inventories as one-time acceptance evidence that may be removed after the decision they
support. Retain ignored diagnostic artifacts only when the durable E2E fails.

**Why.** The external application boundary needs periodic real evidence, but snapshot-specific
source lines, exact rendered-ink percentages, screenshot inventories, and permanent proof bundles
do not provide stable behavior contracts. Keeping them would turn a completed rebuild into a
fragile maintenance obligation.

**Consequence.** The archived WP-V2 proposal for a retained acceptance directory, a dedicated
acceptance report, and fixed 144-DPI geometry thresholds is superseded. Migration acceptance rests
on the fixture-free 18-layout E2E, its LibreOffice `ODP -> FODP -> ODP` preservation check,
ODP-derived PDF validation, the completed one-time 99-page production build, and the permanent
offline suite. A future concrete rendering defect may add a focused temporary probe without
changing the permanent test contract.

**Owner.** [PYTEST_STYLE.md](PYTEST_STYLE.md), [E2E_TESTS.md](E2E_TESTS.md),
`tests/e2e/e2e_djot_native_layouts.py`, and [PIPELINE.md](PIPELINE.md).

### Vertical root-body layouts use one author-visible block

**Decision.** `vertical-text-panel` and `vertical-panel` accept exactly one root body
block after the level-one title: a paragraph, list, or component image.

**Why.** The one authored block maps directly to one native vertical text frame or contained image
region without inventing a repository-specific Markdown wrapper language.

**Consequence.** Native geometry uses the fixed 94-unit vertical title, 24-unit spacer, and
1042-unit body tracks. The two vertical-title layouts place the title strip on the right, matching
LibreOffice. `vertical-title-two-panels` stacks a vertical text member over a normal content member;
`two-panels-vertical-clipart` retains its approved source name but supplies LibreOffice's two
side-by-side vertical-content members through `left` and `right` slots.

**Owner.** `slide_lib/layout_engine.py` and its contract tests.

### Readers extract facts and the emitter renders Djot

**Decision.** ODP and PPTX readers return raw source facts. Geometry planning assigns semantic
regions, and one Djot emitter owns escaping and output syntax.

**Why.** A reader that pre-renders output syntax can double-escape text and makes the input format
own details of the authored language.

**Consequence.** `source_model.py` carries raw runs, links, images, tables, notes, and review facts;
`slide_plan.py` owns geometry; `djot_emitter.py` renders supported source facts exactly once and
`import_report.py` preserves imported note and normalized-region content without inventing Djot
syntax.

**Implementation status.** Complete. `pptx_reader.py` returns raw positioned facts;
`slide_plan.py` validates and normalizes their geometry; `djot_emitter.py` owns Djot projection; and
`import_report.py` retains canonical text, safe links, geometry, source order, and presenter notes.
Promoting report-only notes into rebuilt native note objects remains a separate language decision.

**Owner.** [PIPELINE.md](PIPELINE.md).

### The registry defines Djot layout and slot contracts

**Decision.** `slide_lib.layout_engine.registered_layout_names()` and
`slide_lib.layout_engine.layout_contract()` are the authoritative public layout catalog for canonical
short names and named Djot slots. The engine delegates declarative values to the private
`layout_registry.py` catalog; the grammar derives legal vocabulary through the public API and
provides no aliases.

**Why.** Source validation and native geometry must describe the same layouts. Derived vocabulary
keeps a later layout change local to the layout owner rather than creating parallel spelling tables.

**Consequence.** The canonical names are `one-panel`, `two-panels`, `one-plus-two-panels`,
`two-plus-one-panels`, `stacked-panels`, `two-over-one-panels`, `four-panels`, `six-panels`,
`vertical-panel`, `vertical-title-two-panels`, `vertical-text-panel`, and
`two-panels-vertical-clipart`; `blank`, `title-only`, `title-slide`, `centered-text`, and `gallery`
remain. The asymmetric layouts use named slots rather than source position.

**Owner.** `slide_lib/layout_engine.py`, `slide_lib/layout_registry.py`, and
`slide_lib/djot_grammar.py`.

### Djot normalizes headings and cells before geometry

**Decision.** Djot parses global H1/H2 headings separately from named `Cell` content. All H2 lines
on a `title-slide` form one subtitle region, and cells bind by declared slot name rather than source
order.

**Why.** A normalized IR lets both source front ends share geometry while preserving imported
title-slide subtitles and allowing authors to order named regions for readability.

**Consequence.** Layouts validate title/subtitle permission and named-cell completeness. Missing,
duplicate, unknown, and unnamed cells fail source-located. Multiple H2 lines are preserved rather
than collapsed into a single source line.

**Owner.** `slide_lib/native_model.py`, `slide_lib/djot_parser.py`, and
`slide_lib/layout_engine.py`.

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
`slide_lib/layout_engine.py`.

### Multiple-choice carries reveal intent, not timing proof

**Decision.** `multiple-choice` requires `question` and `answer` cells. The question contains a
visible choice list; the answer is one or two short editable flat paragraphs with implicit
object-appear reveal intent and no explicit action directive.

**Why.** The layout communicates the instructional structure without making the author repeat a
redundant answer action or turning a popup into a general overlay system.

**Consequence.** The answer is placed in the fixed popup region and rejects explicit `<=` or `=>`
actions. The intent becomes a bounded OOXML animation request only when M5 builds it. Package
semantics and the automated reveal-state harness are the acceptance evidence.

**Owner.** `slide_lib/layout_engine.py`, `slide_lib/djot_parser.py`, and
[wp_a1_animation_fidelity.md](active_plans/reports/wp_a1_animation_fidelity.md).

### Animation uses OOXML and Impress evidence

**Decision.** Keep bounded `appear` and `fade`, `object` and `paragraphs`, `on-click` reveal intent in
the format-neutral model. Build it as native ODF/SMIL in `slide_lib/odp_animation.py` and as OOXML in
`slide_lib/pptx_animation.py`. LibreOffice Impress and ODP are the editing and playback contract;
PPTX is an independent interchange artifact.

**Why.** The former OOXML-only implementation made ODP reveal fidelity depend on LibreOffice import
and allowed timing to disappear from generated ODP. Independent native writers preserve one authored
intent without making either output format the parent of the other.

**Consequence.** Each adapter owns only its serialization and targets stable object identities from
the shared layout plan. Runtime XML templates and PowerPoint-authored decks are not contracts. Fast
tests cover structural semantics with inline inputs, while native ODP package validation, headless
LibreOffice round trips, PDF/render metrics, and the automated reveal-state interpreter are the final
acceptance evidence. Unsupported reveal intent fails with its source location instead of
disappearing. `blue overlay` remains deferred.

**Owner.** `slide_lib/odp_animation.py`, `slide_lib/pptx_animation.py`, [PIPELINE.md](PIPELINE.md), and
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
source-order panel with a review reason. A table-bearing fallback isolates each table in its own
native cell. Difficult slides retain their instructional text and genuine images through an
existing registered layout; when dense labels cannot remain useful on-slide, the import report
retains their lossless text/link/geometry facts beside a visible redesign diagnostic. Ordinary
source pictures remain independent image assets; unsupported vectors stay explicit in diagnostics.
No rendered source slide or composite region is an import product.

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
`slide_lib/importers/djot_emitter.py`, and `slide_lib/layout_engine.py`.

### Ordinary layouts preflight optional titles and local headings

**Decision.** Ordinary panel layouts accept zero or one global H1, and each ordinary cell accepts
at most one local H2. Preflight title, heading, table, image, and text capacity before creating
native shapes.

**Why.** Imported slides sometimes have an absent global title or a component-local heading. The
same source allocation must remain readable whether the title is present or absent.

**Consequence.** A titleless layout receives its full content region. Local headings and ordinary
body/list text retain the shared point-valued readability contract: ordinary text starts at 28 pt
and build preflight rejects any fit below 24 pt before native objects are created. An unsupported
combination or unreadable allocation reports the relevant source location and leaves no partial
shapes.

**Owner.** `slide_lib/layout_engine.py` and [PIPELINE.md](PIPELINE.md).

### Continuation is a fit-gated physical-layout decision

**Decision.** Begin every logical source slide as one panel. If and only if it cannot meet its
point-size floor, `layout_engine` may paginate when the source permits it; otherwise it raises a
source-located error before serialization. It selects the latest fitting mixed partition without
splitting a paragraph, root-list subtree, table-row group, or atomic object.

**Why.** Adapter-specific overflow handling caused the prior system to lose physical-layout meaning.
A compiler-owned continuation plan makes readable expansion deterministic and keeps ODP and PPTX
equivalent without a format-specific rescue path.

**Consequence.** The ordered fallback reduces ordinary text only to 24 pt, then partitions whole
paragraphs, root-list subtrees, table-row groups, and atomic objects. Only a root-list subtree that
cannot itself fit may recursively partition between descendant list-item subtrees; a too-tall leaf
fails source-locally. The format-neutral plan holds an ordered `ContinuationContext` ancestor trail,
the `INLINE_STATIC`, `HANDOFF_STATIC`, or `METADATA_ONLY` display mode, and physical
`ContinuationKind.NORMAL`, `AUTHORED`, or `CONTEXT_HANDOFF`. When a trail and new authored
descendant fit together, the compiler uses `INLINE_STATIC`. Otherwise it creates one deterministic
static context-handoff page immediately before the detached descendant; if the trail itself cannot
fit, it retains metadata-only context on the descendant. The descendant stays at its original level
and must fit. Context uses no abbreviation, clipping, subfloor, or text-specific branch, is never
authored or revealable, and existing `continuation_context` marks visible repeats. Every authored
unit occurs exactly once. Ordinary repeated H1 behavior remains independent of the ancestor trail.
Continuations retain the same topology and title behavior, use stable `source_id-pN` identities with
contiguous indexes, reset local reveals per physical page, repeat qualified notes, and number
physical pages. The adapters receive only this plan, preserve its count and order, and serialize
nonvisual trails into matching accessibility descriptions and generated continuation notes.

**Owner.** `slide_lib/layout_engine.py`, `slide_lib/layout_model.py`, `slide_lib/odp_export.py`, and
`slide_lib/pptx_export.py`.

### Context handoff is explicit

**Decision.** Model detached continuation ancestry as an ordered, format-neutral
`ContinuationContext`. Select `INLINE_STATIC` when the required ancestor trail and its new authored
descendant fit one physical page. Otherwise emit one immediately preceding static
`CONTEXT_HANDOFF` page using `HANDOFF_STATIC`; use `METADATA_ONLY` only when the trail itself cannot
fit. The descendant remains at its original level and must fit or fail source-locally.

**Why.** A requirement that every physical continuation page visibly contain both ancestry and new
content fails for legitimate deep-list splits. Dropping context makes the detached descendant
ambiguous, while shrinking, clipping, or abbreviating it would violate the readability and content
contracts. An explicit physical handoff preserves meaning without making a renderer choose a hidden
rescue behavior.

**Consequence.** `layout_model` represents the three display modes and `NORMAL`, `AUTHORED`, and
`CONTEXT_HANDOFF` physical kinds. `layout_engine` emits static context with no reveal targets and
keeps authored units and reveal targets exactly once. Existing `continuation_context` continues to
mark visible static repeats. ODP and PPTX project a nonvisual trail into equivalent accessibility
descriptions and generated continuation notes. WP-L2 proves inline, handoff, metadata-only, and
leaf-error behavior from inline test inputs; WP-O1/P1 prove projection parity; WP-V2 verifies `lect02a` line
293, Student Profile at line 470, and the full deck without an attended step.

**Owner.** WP-L2, WP-O1, WP-P1, and WP-V2 in the archived
[native ODP layout migration](archive/native_odp_layout_migration.md).

### Physical plans own safe line advance and list geometry

**Decision.** Ordinary theme text has nominal 1.30em line spacing, matching the OTP outline
`fo:line-height="130%"`. The compiler resolves list start and hanging indents into
`ParagraphProperties`, and records an exact safe advance for each wrapped line as the greater of
that nominal spacing and the mixed-face ascent-plus-descent required by the resolved runs.

**Why.** Measuring with one spacing rule while serializing another can make an apparently fitting
deck wrap, shrink, or overflow in either adapter. Adapter-local list or leading choices would also
recreate the original format-dependent layout behavior.

**Consequence.** WP-T1 exposes the nominal OTP policy; WP-T2 supplies only verified font metrics;
WP-L2 carries resolved indents and safe advances in immutable physical plan records; WP-O1 and WP-P1
serialize those values identically without remeasurement. Offline plan/package/projection tests and
WP-V2 LibreOffice round-trip/render parity tests reject a changed leading, indent, continuation
context, or list hierarchy. This is a target contract, not an implementation-completion claim.

**Owner.** WP-T1, WP-T2, WP-L2, WP-O1, WP-P1, and WP-V2 in the native ODP layout migration.

### Generic grid overflow decomposes to a one-panel physical topology

**Decision.** `layout_engine` applies the named `DECOMPOSE_TO_ONE_PANEL` compiler policy only when
an eligible generic grid fails true-fit preflight and `paginate: true`. Eligible grids are
`two-panels`, `one-plus-two-panels`, `two-plus-one-panels`, `stacked-panels`,
`two-over-one-panels`, `four-panels`, and `six-panels`. A fitting grid remains exactly the authored
grid. On an eligible failure, the compiler gathers the entire nonempty slot set in canonical reading
order and passes that one ordered stream through the same one-panel splitter used for ordinary
continuations.

**Why.** Repeating a failed grid topology merely spreads undersized or stranded cells across pages.
Treating each slot as an independent continuation loses the source's reading order and allows
adapter-specific emergency layouts. One canonical decomposition makes overflow readable while
preserving one semantic source and one cross-adapter physical plan.

**Consequence.** Every resulting physical page has the native one-panel topology. The global H1,
active context heading, and qualified notes repeat; source slot labels do not. Images and tables use
the canonical one-panel placement rules, every source content unit and reveal appears exactly once,
and each page records immutable origin provenance for the source grid and contributing slots.
Deterministic identities and continuation indexes use the existing physical-page scheme. Semantic
layouts with their own meaning--including title, centered-text, vertical, gallery, and
multiple-choice layouts--are excluded rather than silently decomposed. `paginate: false`, an
ineligible layout, or an atomic unit that cannot fit raises a source-located error before
serialization.

**Owner.** `slide_lib/layout_engine.py`, `slide_lib/layout_model.py`,
`slide_lib/odp_export.py`, and `slide_lib/pptx_export.py`.

### Layout capacity is a shared, font-metric-backed compiler result

**Decision.** The implemented layout compiler, rather than either output adapter, owns capacity,
pagination, grid decomposition, and title-floor resolution. It measures hash-verified theme faces
at exact requested sizes, including fractional point values, and keeps cache/session identity in the
measurement inputs. Explicit line breaks are grapheme-safe. A title that reaches its shared 30 pt
floor remains one atomic title; it is not rewritten into leaf fragments to make a page fit.

**Why.** The original drift arose when each artifact path could treat text boxes and fit behavior as
format-local details. A fractional-size or grapheme boundary must not turn the same source into a
different plan on a later run. Fragmenting a title to satisfy one local constraint would weaken the
source's semantic structure and recreate adapter-specific fallback behavior.

**Consequence.** WP-L2 is accepted with 171 focused tests and a deterministic 99-page `lect02a`
compile. The compiler uses 36 pt / 28 pt defaults with 30 pt / 24 pt floors, retains atomic leaf
failure for content that truly cannot fit, and supports recursive inline, handoff, and metadata-only
continuation context. Eligible overflowing grids co-pack their canonical source stream into
one-panel pages with immutable provenance; unsupported facts and tables retain recursive parity.
ODP and PPTX remain responsible only for projecting this completed `LayoutDeck`, so WP-O1 and WP-P1
must validate adapter parity rather than remeasure or repaginate it.

**Owner.** `slide_lib/layout_engine.py`, `layout_measurement.py`, `layout_builders.py`; WP-O1,
WP-P1, and WP-V2 consume and verify the plan.

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
reusing the existing `two-plus-one` and footer permission. Adaptive vertical image flow starts text
at 28 pt and rejects a fit below its 24 pt floor before scaling every image uniformly. Visual
relations retain source membership only long enough to normalize it into standard native components;
no private render or geometry exception is a routing mechanism. Ambiguous arrangements become a
native source-order panel with review evidence.
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
