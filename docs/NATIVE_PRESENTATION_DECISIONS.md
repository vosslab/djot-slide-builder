# Native presentation decisions

Part of [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md).

### Model checks protect authoring and native-adapter boundaries

**Decision.** Keep validation where malformed Djot-derived data could reach an ODP adapter with an
invalid placeholder topology, animation order, or picture placement. Keep measurement caches
private implementation details. Pictures use the sole `CONTAIN` policy.

**Why.** The builder constructs ordinary model records consistently, so duplicate construction
checks add little protection. Adapter boundaries have distinct native ODF requirements: a page
layout defines its member topology, animation needs one contiguous click order, and an image frame
must remain in its allocated region without source cropping.

**Consequence.** `MeasurementStatistics` and its cache-hit assertion are retired. The physical
model continues to reject invalid topology, reveal, and contained-picture data before export while
leaving normal compiler output unchanged.

**Owner.** `slide_lib/layout_model.py`, `slide_lib/layout_content.py`, and
`slide_lib/layout_measurement.py`.

### Visible URL typography and wrapping belong to the backend

**Decision.** Literal URL links use the condensed font at the paragraph size minus 2 pt.
Measurement and native export use the same lossless fragmentation routine, preferring address
separators when an address exceeds the available width. Every linked fragment retains the full
destination. Long separator-free components still use grapheme-safe splitting when necessary.

**Why.** Users want to inspect destinations before clicking. Separate measurement and emission
algorithms produced inconsistent breaks; replacing URLs with descriptive labels hid the problem.
Source authors should supply intact addresses and layout context, not font names or manual breaks.

**Owner.** `slide_lib/layout_measurement.py`, `slide_lib/layout_object_builders.py`,
`slide_lib/presentation_theme.py`, and `slide_lib/odp_text.py`.

### Bundled font profiles are the measurement authority

**Decision.** Every font face the presentation pipeline emits is a versioned repository asset with
an immutable family/style key, repository-relative path, SHA-256 digest, and face index. Theme
loading verifies each asset and its intrinsic metrics before layout work begins. Missing glyphs
within a valid face may use rendering-backend substitution; Djot never names fallback fonts.

**Why.** A readable-floor calculation is only meaningful when its glyph metrics are reproducible.
Host fonts and silent LibreOffice substitution turn the same Djot deck into different geometry on
different machines. Atkinson Hyperlegible Next replaces OpenDyslexic because the OpenDyslexic
metrics produced distracting line spacing in ordinary lecture text.

**Consequence.** Atkinson Hyperlegible Next, Atkinson Hyperlegible Mono, and IBM Plex Sans
Condensed each have bundled regular, bold, italic, and bold italic faces under SIL OFL licenses.
Ordinary text, inline code, and literal URLs select these roles in the backend. Supporting math
fonts and missing-glyph substitutions also belong to the backend, not to authored Djot overrides.

**Owner.** `slide_lib/presentation_theme.py` and `assets/fonts/PROVENANCE.md`.

### Generated ODPs embed the measured bundled faces

**Decision.** Every generated ODP contains unchanged copies of the validated repository font
files as `Fonts/` members. Each family, weight, and style has a stable ODF face name and
`svg:font-face-uri`; emitted semantic styles use the original public family.

**Why.** Embedding supplies the measured fonts as portable dependencies. Renamed families were
visible in LibreOffice's font selector and prevented ordinary editing with familiar installed
families. Original bytes preserve the public identity, outlines, and metrics together. This
supersedes the earlier collision-avoidance policy; host handling of same-named fonts remains
LibreOffice's responsibility and rendered export still requires validation.

**Consequence.** Theme validation reads every face's OS/2 embedding permission and reports a
restrictive face before export. Source assets and embedded bytes remain hash-verified and unchanged.
The package also contains the applicable OFL notice files. The small package-size cost
is accepted for deterministic editable decks.

**Owner.** `slide_lib/presentation_theme.py`, `slide_lib/odp_export.py`, and `slide_lib/odp_text.py`.

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
repository-owned Djot modules. Per-slide `hidden: true` metadata preserves optional content in
source; omission or `hidden: false` makes it visible. Metadata precedes content and slots.

**Why.** One source language keeps authoring, validation, import output, and native export aligned
without maintaining a second parser or compatibility vocabulary.

**Consequence.** `native_export` admits only `.djot`; ODP import emits Djot. The
runtime has no alternate source-language parser, suffix dispatch table, or target-selection flag.
Import retains hidden slides and assets; lint and capacity inspection validate them, compilation
retains each as a native hidden ODP page style, and LibreOffice omits hidden pages from PDF and
classroom playback. An all-hidden source can be imported and linted but cannot produce a classroom deck.
This is one boolean on the semantic slide, not a generic metadata or export-mode framework.

**Owner.** `slide_lib/native_export.py`, `slide_lib/djot_parser.py`, and [PIPELINE.md](PIPELINE.md).

### Djot requirements inform the implemented grammar

**Decision.** The implemented Djot slide language makes recurring teaching structures directly
authorable: title; title and subtitle; ordinary body; nested bulleted and numbered lists; equal and
unequal panels; image/text on either side; three or four regions; image with caption; gallery;
quote or callout; and reusable named teaching layouts. The layout vocabulary must include every
default LibreOffice layout plus the custom `multiple-choice` layout. It must also support simple
Markdown images with predictable named-region placement and standalone equations through
LaTeX-compatible or similarly capable hand-writable syntax. It must support simple on-advance
teaching reveals: make an authored item appear or present an outline one bullet at a time.

**Why.** These lecture structures require portable spatial semantics. They define the implemented
grammar's required authoring surface and preserve room for
native-output capabilities that still need an explicit owner.

**Consequence.** The language survey uses those structures and equation support as literal source
examples. The Djot extension grammar preserves ordinary nested Djot content, avoids routine
HTML-comment or container scaffolding when possible, and map text, lists, practical equations, and
images to typed native slide objects. Equations use measured SVG artwork. Reveal semantics remain bounded to authored
appearance order; motion paths, timing tracks, and complex choreography are outside this
requirement. Equation support must not require a scientific-publishing workflow. The 2026-09-05
exploration status is superseded by the 2026-09-06 implemented Djot parser, grammar, linter, and
native export path. The 2026-10-20 MathJax-to-SVG implementation supplies equation rendering; see [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md).

**Owner.** `slide_lib/djot_grammar.py`, `slide_lib/djot_parser.py`,
[PIPELINE.md](PIPELINE.md), and [LECTURE_LAYOUT_SURVEY.md](LECTURE_LAYOUT_SURVEY.md).

### Component images and dollar-delimited mathematics have fixed surfaces

**Decision.** The implemented language's component-image form is `![alt](path)`. Its official
mathematics forms are `$equation$` for equation-only paragraphs, list items, or table cells and
`$$display$$` for display blocks. Mixed prose/math is unsupported. These surfaces are unavailable for future slide,
layout, region, gallery, reveal, or styling syntax.

**Why.** The image form already has native Djot meaning.
The dollar forms are the instructor's preferred hand-writable mathematics surface and can be mapped
by a repository-owned MathJax-compatible adapter. Reserving all three prevents slide syntax from
colliding with ordinary teaching content.

**Consequence.** This reserves ordinary component images only, not extra image modifiers for
backgrounds, sizing, position, or filters. The implemented grammar owns slide starts and named slots;
`%%` and generic overlay geometry outside `multiple-choice` remain open. MathJax renders whole
equation SVGs under the constraints in [DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md#equations).

**Owner.** [djot_slide_extension_exploration.md](active_plans/decisions/djot_slide_extension_exploration.md)
and [DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md).

### Multiple-choice is an implemented bounded layout

**Decision.** `multiple-choice` is an official layout in the implemented language catalog.
It requires exactly one `@question` slot and one `@answer` slot. The question contains the prompt
and its ordinary choice list; the answer contains one or two short, flat paragraphs in a bounded
popup region selected from measured question geometry. It carries implicit reveal intent only.

**Why.** Multiple-choice questions have a short, revealable answer. Implicit intent removes redundant
animation spelling while keeping open-ended questions out of a layout that would misstate their
teaching structure.

**Consequence.** The parser, linter, exporter, and native builder own its `@question` and `@answer`
contract. The answer occupies an editable popup region; ODF/SMIL timing and Impress first-advance
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

### Native content keeps bounded styling and drawing semantics

**Decision.** Accept Djot tables, inline verbatim, and a closed `{color=name}` vocabulary. On
`big-image`, accept only one-ended arrows and transparent rectangle outlines expressed as percentages
of its single aspect-preserving displayed image. Fenced code and mathematics stay reserved until
dedicated native owners exist.

**Why.** The lecture corpus needs meaningful mixed-run colors, readable tables, and editable image
annotations. It does not justify arbitrary hexadecimal styling, page coordinates, or a general
drawing language.

**Consequence.** Text remains font-backed ODF spans. Tables use measured native rows and columns with
light body cells. Image annotations become native `draw:line` or no-fill `draw:rect` objects and may
reuse object reveal intent. Import preserves recognized colors and image-owned annotations, while
ambiguous drawings, fenced code, and mathematics receive source-located review.

**Owner.** `djot_inline.py`, `layout_object_builders.py`, `odp_export.py`, and `importers/odp_reader.py`.

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

### Historical (2026-09-08): native layout registry owned 18 layouts

**Status.** Superseded by the 2026-09-09 ODP-only 14-layout catalog used at that time. This entry
preserves the earlier registry rationale and its former optional-PPTX boundary.

**Decision.** Compile all sixteen LibreOffice layout-grid patterns, `gallery`, and
`multiple-choice` in `slide_lib/layout_engine.py`, the sole 18-layout compiler, into one immutable
format-neutral `LayoutDeck` plus a separate immutable `CompilationResult` carrying capacity
diagnostics. Native ODP and optional PPTX adapters consume `LayoutDeck` only and serialize it
independently.

**Why.** Editable output needs predictable native text, list, image, and shape regions. The
LibreOffice grid provides a useful visual catalog, but applying it after conversion does not create
the required objects. Keeping geometry inside a python-pptx renderer also prevents a native ODP
adapter from sharing the same placement and fit decisions.

**Consequence.** Every canonical slide selects one named layout and supplies its declared slots.
`slide_lib/layout_engine.py` exposes only `compile_layout_deck`; it delegates geometry, capacity
checks, presentation roles, and reading order to cohesive private helpers. The public
registry owns layout catalog lookup directly. Ownership flows from `layout_primitives.py` through
`layout_content.py` to `layout_model.py`: primitives own neutral records including `LayoutContract`,
content owns immutable editable-content records, and the model composes the complete physical plan.
In import direction, `layout_content` imports `layout_primitives`, and `layout_model` imports both;
`native_model` remains independent source-semantic authority and is imported only by the
compiler-side translation modules. `layout_registry.py` is declarative catalog data;
`layout_measurement.py` owns pure measurement/preflight/local-heading work; and
`layout_builders.py` turns resolved facts into planned objects without recomputing them. Typography
uses points in the shared plan.
Output adapters contain no layout allocation, fit-selection, or layout-registry logic, and source
styling does not determine output geometry.

**Owner.** `slide_lib/layout_primitives.py`, `slide_lib/layout_content.py`,
`slide_lib/layout_model.py`, `slide_lib/layout_engine.py`, its private helpers, and `docs/USAGE.md`.

### Historical (2026-09-08): layout topology used 16 standard identities

**Status.** Superseded by the current twelve standard LibreOffice identities plus two custom
layouts. This entry preserves the earlier topology rationale.

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
Author image/text variation with the existing `two-panels` slots, alternating the image side on
consecutive slides. Explicit `@left` and `@right` placement makes that choice reviewable in Djot
and preserves it when slides are reordered or hidden.

**Owner.** [presentation_language_choices.md](active_plans/decisions/presentation_language_choices.md).

### Historical (2026-09-08): ODP-derived PDF used sibling PPTX output

**Status.** Superseded by the current ODP-only build boundary. This entry preserves why PDF must
derive from ODP rather than an intermediate presentation format.

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

### Advisory visual review uses functional PDF comparison

**Decision.** Review generated classroom pages from the PDF LibreOffice creates from the editable
ODP. Use the five universal dimensions in
[SLIDE_VISUAL_REVIEW_RUBRIC.md](SLIDE_VISUAL_REVIEW_RUBRIC.md) for standalone quality and as
comparison lenses for an original PDF paired with its corresponding generated PDF. Record migration
as `improved`, `roughly equivalent`, or `materially worse` with the most important visible teaching
reason.

**Why.** The PDF reflects the native editable ODP that instructors receive. Functional comparison
preserves meaningful hierarchy, grouping, emphasis, balance, and instructional character while
allowing simpler standard layouts instead of treating legacy coordinates as a visual target.

**Consequence.** WP-S4 calibrated the standalone workflow on 20 opaque pages with three independent
primary-model passes and one alternate-model pass. It supports broad advisory bands, an explicit
concern with a visible reason, and follow-up for a total of 14 or below, a dimension of 2 or below,
or a material concern. One-point total differences remain contextual. The five dimensions are
correlated complementary lenses, not independent measurements. A small disposable paired
original/generated PDF check will calibrate migration-category repeatability. Visual review remains
on demand and advisory; deterministic checks retain ownership of measurable output properties.

**Owner.** [SLIDE_VISUAL_REVIEW_RUBRIC.md](SLIDE_VISUAL_REVIEW_RUBRIC.md),
[PIPELINE.md](PIPELINE.md), and rendered-review evidence recorded with the affected migration.

### Historical (2026-09-09): private-profile batch experiment

**Decision.** Run batch conversions with `--headless --norestore` and one private
`UserInstallation` profile after confirming that the main desktop application is closed.

**Why.** A private profile keeps automated conversion separate from desktop crash-recovery state
and prevents the build from reopening user-facing recovery prompts.

**Consequence.** Each conversion owns a short-lived private profile and temporary converted
artifacts. `--headless` supplies non-visual batch mode. A timed-out invocation stops and reaps
only its private POSIX process group before profile cleanup. If that bounded cleanup cannot reap
its direct child, the private profile remains at the named diagnostic path for recovery.

**Status.** Superseded by the direct sequential method recorded at the top of this document. The
private profile triggered recovery prompts and added lifecycle machinery without a demonstrated
benefit.

**Owner.** `slide_lib/libreoffice.py` and all LibreOffice conversion callers.

### Historical (2026-09-09): one-process PDF batch

**Decision.** A folder `pdf` or `all` build writes every editable ODP, converts the ordered ODP set
through one headless LibreOffice process, verifies every staged PDF, and then publishes the PDFs.

**Status.** Superseded by staging the complete set around direct sequential conversions. The staged
publication safety remains; the one-process batch does not.

**Why.** A fresh process per ODP follows the demonstrated local method and has fewer hidden
cross-file lifecycle assumptions.

**Consequence.** A failed conversion leaves final PDF destinations unchanged; each final PDF uses
one atomic replacement after staging. A filesystem publication failure can leave an earlier PDF
published, and rerunning the folder build completes that recoverable set. Direct one-deck export
uses the same batch boundary with one input.

**Owner.** `slide_lib/libreoffice.py`, `slide_lib/native_export.py`, and
`slide_lib/terminal_output.py`.

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
rather than replace it. Embedded GDI figures use their package-local raster preview, or convert
individually through LibreOffice to PNG. Import never substitutes a full-slide render; temporary
full-slide renders support QA only. Surrounding text remains native and editable.

**Owner.** `slide_lib/importers/djot_emitter.py`, `slide_lib/layout_engine.py`,
`slide_lib/odp_export.py`, and their tests.

### The default theme normalizes lecture structure

**Decision.** Use `genetics/xlect99-template_2023.otp` as the sole master-slide theme authority.
Load its 16:10 page ratio, native top gradient, presentation-frame geometry, typography, and
outline-level bullet geometry into a format-neutral theme model. Standard primary titles are
centered and begin at 36 pt; ordinary body/list text begins at 28 pt. Direct ODP inherits the template's native styles.

**Why.** The legacy lecture decks establish useful common visual rules, but reproducing their
individual quirks would weaken the consistent authoring system. Explicit presentation semantics let
ODP and its LibreOffice-derived PDF share the same intended structure.

**Consequence.** The repository retains a stable 1280x800 logical layout canvas, and every accepted
template must have a 16:10 page ratio; its physical centimeter or inch dimensions may vary. The target
ODP contains the template's real master page, with its background outside the planned slide-object
stream, rather than a repeated per-slide background. Authored decorations remain planned objects with normal
reading and z order. Wrapped list lines align with their paragraph text, not with the bullet, and
nested levels have distinct bullet and text positions. Body content and local headings retain their
reading alignment; title-slide and section text retain vertical centering where their role calls for it. Typography remains
point-valued and never passes through the logical-geometry conversion. Build preflight enforces a
30 pt title floor and 24 pt ordinary-text floor before native shrink-on-overflow protects against
small font-metric differences. CSS and browser rendering are not part of the build.

**Owner.** `genetics/xlect99-template_2023.otp`, `slide_lib/presentation_theme.py`,
`slide_lib/layout_engine.py`, `slide_lib/odp_export.py`, and their native-export tests.

### Font metrics are versioned theme inputs, not host behavior

**Decision.** Treat every face used for layout capacity as a committed, hash-verified OFL asset with
recorded provenance. `PresentationTheme` exposes immutable profiles for exact family, weight, and
italic states; all measurement resolves styled runs against those profiles. Atkinson Hyperlegible
Next is the ordinary-text family, Atkinson Hyperlegible Mono supplies inline code, and IBM Plex
Sans Condensed supplies displayed literal URLs. All three include real regular/bold/italic faces.

**Why.** A system-installed base font or an average-glyph estimate makes line
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
Local automatic styles parent the shipped `Default-*` presentation styles. Scoped `lxml` parsing
rejects DTDs while disabling entity resolution and network access. The ODP adapter owns
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

### Historical (2026-09-08): native acceptance used the 18-layout evidence set

**Status.** Superseded by the later 14-layout ODP/ODF evidence boundary. This entry preserves
the rationale for separating permanent tests from one-time acceptance evidence.

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

### CJK vertical layouts stay outside the catalog

**Decision.** Support the twelve standard LibreOffice Impress layout-panel identities and the
project-owned `multiple-choice`, `gallery`, and `big-image` extensions. Remove the four CJK-only
vertical AutoLayouts from the Djot grammar, layout registry, measurement path, and native adapters.

**Why.** The CJK-only identities are absent from the standard layout panel and no genetics source
or importer output uses them. A single horizontal text-flow model gives title preflight and native
output one physical contract.

**Consequence.** The supported catalog contains fifteen layouts. Text frames use horizontal
writing only, and the ODP adapter serializes no vertical-writing metadata.

**Owner.** `slide_lib/layout_registry.py`, `slide_lib/layout_measurement.py`,
`slide_lib/layout_builders.py`, and `slide_lib/odp_export.py`.

### Historical (2026-09-08): readers extracted ODP and PPTX facts

**Status.** Superseded by the current direct bounded-ODP reader. This entry preserves the
reader-to-planner-to-emitter separation rationale.

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

**Decision.** `slide_lib.layout_registry.names()` and
`slide_lib.layout_registry.contract_for()` are the authoritative public layout catalog for canonical
short names and named Djot slots. The compiler exposes only compilation; the grammar and import
tools derive layout vocabulary directly from the registry and provide no aliases.

**Why.** Source validation, import topology selection, and native geometry must describe the same
layouts. The former compiler pass-throughs forwarded verbatim to the registry and made importers
depend on compilation only for catalog data. Direct registry access preserves one declarative owner
and removes that false dependency.

**Consequence.** The canonical standard names are `blank`, `title-only`, `title-slide`,
`one-panel`, `section`, `two-panels`, `one-plus-two-panels`, `two-plus-one-panels`,
`stacked-panels`, `two-over-one-panels`, `four-panels`, and `six-panels`. Project-owned
`multiple-choice`, `gallery`, and `big-image` remain explicit extensions. `section` is the authored
semantic name for LibreOffice Centered Text (`AUTOLAYOUT_ONLY_TEXT`), whose single outline member carries
the centered title and subtitle lines. The asymmetric layouts use named slots rather than source
position.

**Owner.** `slide_lib/layout_registry.py`, `slide_lib/djot_grammar.py`, and the direct registry
clients; `slide_lib/layout_engine.py` owns compilation only.

### Title Only keeps one native title placeholder and ordinary body objects

**Decision.** `title-only` accepts one leading H1 and optional root teaching body.  Its H1 uses
LibreOffice's sole `TITLE_ONLY` title placeholder; following text, lists, component images, and a
sole table use the blank region below as ordinary editable objects.

**Why.** A native Title Only page has one title member, not an outline member.  Reusing the common
body-flow measurement and containment path preserves editable instructional content without
inventing a second placeholder or a separate free-positioning system.

**Consequence.** Heading-only title-only slides retain their existing START/TOP native geometry.
Body objects retain source order and capacity diagnostics while `AUTOLAYOUT_TITLE_ONLY` remains
the page-layout identity.

**Owner.** `slide_lib.layout_registry`, `slide_lib.layout_validation`, and
`slide_lib.layout_builders`.

### Direct ODP section identity uses positive page evidence

**Decision.** The direct ODP importer emits `section` only when its immutable page evidence records
a declared source layout identity, exactly one declared `subtitle` placeholder, exactly one
populated `subtitle` text placeholder, and one meaningful content object. Missing evidence or any
other recorded identity follows the ordinary geometry-based emission path.

**Why.** The original genetics corpus has 63 pages with this complete signature across `AL2T32`
and `AL3T32`. Their source geometry varies, so layout identity and sole-content evidence express
the durable semantic intent without treating legacy coordinates as an authored layout target.

**Consequence.** Direct ODP conversion can emit the centered `section` semantic layout without
guessing from generic heading-only content. The committed Djot migration marks those 63 evidenced
pages as `section`; other authored title-only slides remain distinct.

**Owner.** `slide_lib.importers.source_model.SourcePageEvidence` and
`slide_lib.importers.djot_emitter`.

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

**Consequence.** The visible question owns the full question region. A question first fits at the
ordinary 20 pt body floor; on true-fit failure, the compiler separates leading context labels,
context prose, the teaching stem, and choices, then adapts the editable choice split and column
widths using that same floor. The answer is sized against its selected column and placed in
reserved space below the shorter column, so its revealed final state does not hide a choice. Its
native rounded popup uses a light-gray fill with dark-red outline and text. The intent becomes a
bounded ODF/SMIL animation request only when M5 builds it. Package semantics and the
automated reveal-state harness are the acceptance evidence.

**Owner.** `slide_lib/multiple_choice_layout.py`, `slide_lib/layout_builders.py`,
`slide_lib/djot_parser.py`, and
[wp_a1_animation_fidelity.md](active_plans/reports/wp_a1_animation_fidelity.md).

### Historical (2026-09-08): animation used OOXML and Impress evidence

**Status.** Superseded by the current ODF/SMIL reveal path. This entry preserves the
format-neutral reveal-intent rationale.

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
disappearing. The unused target-text `blue overlay` experiment was retired.

**Owner.** `slide_lib/odp_animation.py`, `slide_lib/pptx_animation.py`, [PIPELINE.md](PIPELINE.md), and
[wp_a1_animation_fidelity.md](active_plans/reports/wp_a1_animation_fidelity.md).

