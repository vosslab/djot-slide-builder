# Plan: Restore original-deck fidelity in the Djot slide compiler

## Context

The native ODP layout migration (commits `59c3a99`, `b76635c`, 2026-09-08) achieved its stated
goal: Djot compiles once into a `LayoutDeck` and `odp_export.py` writes ODF 1.3 directly, so
slides land on LibreOffice's official `AutoLayout` identities. That part works and stays.

**2026-09-09 conversion correction.** The private-profile/batch LibreOffice lifecycle added failure
states and a recovery prompt, so it is retired as failed complexity. The durable method is one
desktop preflight followed by direct sequential `soffice --headless --norestore --convert-to`
commands, a two-second settling interval, expected-PDF verification, and complete-set staging
before publication. Quality and DPI are defaults, not acceptance gates.

It arrived with five regressions. Four were reported by the human; the fifth was measured while
planning. Crucially, the original `.odp` decks and their original `.pdf` renderings are still on
disk in `genetics/` (untracked, 60 MB), which makes every one of these measurable against ground
truth rather than argued about.

**The page-count regression is proven to be a compiler problem.** That is a narrower claim than
"the importer is fine," and the difference matters. Page counts show the compiler invents pages;
they say nothing about whether the generated Djot is a faithful semantic translation of the
original. Import is semantic planning and normalization, not transcription, and regression 4 below
is exactly an import semantic error. So this plan treats the generated Djot as *provisional*: where
layout identity, content grouping, or other migration semantics are in question, compare against
the original ODP and either correct the importer or mechanically migrate the Djot once a systematic
import error is demonstrated.

Page-count evidence uses visible pages. The raw original ODP packages contain 378 physical pages,
including 42 hidden pages; their 336 visible pages match both the original PDF pages and the 336
Djot slide markers. Hidden pages are retained evidence about the historical packages, not authored
output targets for this compiler.



| Deck | Original visible ODP/PDF pages | Djot slides | Current build pages |
| --- | --- | --- | --- |
| `lect01b-genetic_disorders` | 23 | 23 | 72 |
| `lect02b-genes_dogma` | 49 | 49 | 90 |
| `lect02c-genome_sizes` | 59 | 59 | 97 |

The importer preserved slide *count* exactly. Every extra page is created by the compiler at build
time: in `lect01b` the emitted ODP contains 23 pages named `slide-N-p0` -- matching the source --
plus 49 `-p1`, `-p2`, ... continuations. Count fidelity is not semantic fidelity, which regression
4 demonstrates.

**Why the compiler thinks content does not fit.** `presentation_theme.py:572` constructs the
theme with `title_floor_size_pt=30.0` and `body_floor_size_pt=24.0` as bare literals. They are
not read from the master and not derived from any deck. The actual body sizes the author used in
the original decks are mostly *below* that floor -- in `lect02b`, 22.2 pt appears 21 times, 18 pt
14 times, 21 pt 11 times, 20 pt 11 times, 13.2 pt 10 times, 12 pt 10 times, with further mass at
13-16 pt. Content the author set at 18 pt is forced to 24 pt, no longer fits, and is split. The
invented floor is the regression.

The floor concept itself is correct and stays. `docs/HUMAN_GUIDANCE.md` is explicit: "Use
shrink-on-overflow for native presentation frames only after build preflight proves the text
remains above a readable floor; LibreOffice's unbounded manual shrink is not the floor owner."
This repository owns the floor. What is wrong is only its *value* -- 24 pt was chosen as a literal,
not measured, and it exceeds what the author actually published.

The five regressions:

1. **Slide count is not 1:1.** Measured above. The human's requirement is absolute: one source
   slide is one Djot slide is one output slide.

2. **Titles and section headers are not centered.** `layout_measurement.paragraph_properties`
   (line 272) hardcodes `HorizontalAlignment.START` on every paragraph, and
   `layout_builders._frame_text` (line 850) hardcodes `VerticalAlignment.TOP` on every frame.
   Meanwhile `presentation_theme.py:543` reads the master, *validates* that its title style
   declares `fo:text-align="center"`, then discards the fact. The explicit `START` overrides the
   inherited master style, so every title renders left-aligned and top-anchored. Rendered pages 1,
   3, and 6 of `lect01b` confirm it. Outline slides look right because body text is genuinely
   start-aligned.

3. **Images are stretched.** `odp_export._frame_attributes` (line 183) writes `item.rectangle` --
   the *allocation* box -- as `draw:frame` geometry, and `draw:image` fills its frame. The
   aspect-correct `placement.displayed_rectangle` computed by `layout_builders._picture_object` is
   discarded. In `output/odp/lect02b-genes_dogma.odp` every body image frame is
   `25.375cm x 14.700cm` (aspect 1.726) regardless of source, while sources are `850x850` (1.00),
   `1036x1056` (0.98), `1402x1056` (1.33). A square figure is stretched about 73% horizontally.
   `pptx_export.py:288` reads `displayed_rectangle` and is correct, which is why only the ODP and
   its derived PDF show the defect.

4. **Section slides were flattened into `title-only`.** The human authors section dividers as a
   distinct kind of slide and reserves `title-only` for a title with content below that no other
   layout fits. The importer has no section concept: `djot_emitter.py:897` maps any slide with a
   heading and no components to `title-slide` when first and `title-only` otherwise. All 63
   `title-only` slides in the corpus are section dividers -- provably, because the `title-only`
   contract declares no slots and no root body, so a `title-only` slide carrying content could not
   compile. The registry already holds the right layout, unused: `centered-text` maps to
   LibreOffice `AutoLayout.ONLY_TEXT`, Impress's section-divider identity.

   A provenance note that changes how this is framed: the layout *names* in
   `docs/HUMAN_GUIDANCE.md` were written by agents, not by the human. He authored the requirements
   recorded there, not the vocabulary. So `centered-text` was never a name he chose, and moving to
   `section` is **not** a rename request against a human-defined identifier -- it is naming the
   semantic concept he actually has, which the project had labelled after its LibreOffice
   AutoLayout instead. Treat every layout identifier in that file the same way: evidence of a
   project decision, not of a human naming decision. Cite that file's requirements, not its
   identifiers, as human authority.

   **The vocabulary's source of truth**, as the human states it: the LibreOffice Impress layouts,
   given author-facing semantic names where useful, plus explicitly documented project extensions.
   He supplied the authoritative list -- Impress's twelve layout-panel entries:

   | # | Impress name | AutoLayout | Registry contract |
   | --- | --- | --- | --- |
   | 1 | Blank slide | `NONE` | `blank` |
   | 2 | Title Slide | `TITLE` | `title-slide` |
   | 3 | Title, Content | `TITLE_CONTENT` | `one-panel` |
   | 4 | Title and 2 Content | `TITLE_2CONTENT` | `two-panels` |
   | 5 | Title only | `TITLE_ONLY` | `title-only` |
   | 6 | Centered text | `ONLY_TEXT` | `centered-text` -> `section` |
   | 7 | Title, 2 Content and Content | `TITLE_2CONTENT_CONTENT` | `two-plus-one-panels` |
   | 8 | Title, Content and 2 Content | `TITLE_CONTENT_2CONTENT` | `one-plus-two-panels` |
   | 9 | Title, 2 Content over Content | `TITLE_2CONTENT_OVER_CONTENT` | `two-over-one-panels` |
   | 10 | Title, Content over Content | `TITLE_CONTENT_OVER_CONTENT` | `stacked-panels` |
   | 11 | Title, 4 Content | `TITLE_4CONTENT` | `four-panels` |
   | 12 | Title, 6 Content | `TITLE_6CONTENT` | `six-panels` |

   Two consequences, both of which correct earlier drafts of this plan.

   First, the registry carries **16** LibreOffice-backed contracts, not 12. The extra four --
   `vertical-panel`, `vertical-title-two-panels`, `vertical-text-panel`,
   `two-panels-vertical-clipart` -- use `VERTICAL_*` AutoLayouts, which are Asian-language layouts
   available only when CJK support is enabled and are absent from the twelve-entry layout panel.
   An earlier draft proposed removing them, and a later draft reversed that on the strength of
   their appearing by name in `docs/HUMAN_GUIDANCE.md`. That reversal was wrong: those names are
   agent-authored. The human's own list settles it, and removal is back on the table with real
   authority behind it.

   Second, Impress's "Centered text" has **no title box at all** -- just one body box, not
   preconfigured for bullets, with text centered and governed by the Subtitle style. That is a
   sharper definition than "a section divider," and it is exactly the shape a section slide wants.
   It also means a `section` slide has no title placeholder: its `#` heading supplies the centered
   text itself. The current `_centered_text_slide` already puts title and subtitle into one
   `OUTLINE` member, so the implementation matches; the syntax specification must say so plainly
   rather than implying a title placeholder exists.

   Renaming `centered-text` to `section` therefore gives an author-facing semantic name to a
   layout the project had labelled after its AutoLayout -- the stated vocabulary rule working as
   intended, not an exception to it.

5. **Slide-number and footer chrome appears in the bottom corner.** The human does not want it.
   There are two independent sources. First, `layout_engine._with_page_number` (lines 290-315)
   draws an 18 pt muted numeral at `LogicalRectangle(1190, 762, 62, 22)` on every continuation
   page. Second, `odp_export._add_page_style` (line 102) sets `background-objects-visible="true"`
   but never sets the three display flags, so each page inherits the master's
   `display-footer="true"` and `display-date-time="true"`. The master already sets
   `display-page-number="false"`, so the footer and date-time placeholders are what still render.

6. **The code is larger than the capability warrants.** `slide_lib/` is 12,618 lines. The dominant
   avoidable mass is the continuation and grid-decomposition machinery that exists only to paper
   over regression 1, plus 86 `raise ValueError` invariant checks across `layout_primitives.py`,
   `layout_model.py`, and `layout_content.py` guarding a model with a single producer.

A Graphify pass over the 1,437-node graph added three structural facts:

- **Layout is driven by catching exceptions in retry loops.** Six of nine `except ValueError`
  handlers in `slide_lib/` are search oracles, not error reporting: five in `layout_engine.py`
  (all continuation and decomposition) and one in `layout_builders._with_fitting_title` (line 155),
  which rebuilds an entire slide once per quarter-point title size from 36 pt down to 30 pt -- 25
  full compiles per slide -- keeping whichever attempt does not raise. Under continuation this
  nested inside a binary search over content units, which is where the reported 0.69-second cold
  compile came from. `docs/PYTHON_STYLE.md` is explicit that try/except should be rare and at most
  two lines.
- **`layout_engine` exposes two pure pass-throughs.** `layout_contract` (22 call sites) and
  `registered_layout_names` (6) forward verbatim to `layout_registry`; only `compile_layout_deck`
  (13) does work. Those wrappers are the sole reason `slide_lib/importers/` imports the compiler.
- **`layout_validation.py` is legitimate.** Its 498 lines prove every supported source block has a
  native destination. That is source validation, not model self-checking, and stays untouched.

On the human's direct question -- "is that why the repo got so big?" -- no. The native ODF writers
total 1,216 lines (`odp_export` 549, `odp_text` 390, `odf_package` 208, `odp_animation` 69), under
10% of `slide_lib`, and writing ODF directly is what made the official LibreOffice layouts
reachable at all. Native ODP stays. The size lives in the continuation engine and its supporting
invariants, which this plan removes.

## Objectives

- Compile exactly one output page per source slide, for every deck, with no manual Djot repair.
- Derive the compiler's type-size floors from the original decks rather than from invented
  literals, so content the author already published continues to fit.
- Give section dividers a `section` layout on LibreOffice's `ONLY_TEXT` AutoLayout and move the 63
  misfiled `title-only` slides onto it.
- Give `title-only` the content-below-title capability the human described, so both of his named
  layouts do the job he names them for.
- Center title-slide and section text on both axes, matching the authoritative
  `genetics/xlect99-template_2023.otp` master.
- Display every image at its intrinsic aspect ratio in ODP and the LibreOffice-derived PDF.
- Remove continuation, decomposition, exception-driven layout search, and pass-through boundaries
  so the architecture matches what the tool actually does.

## Design philosophy

The governing principle is **the original decks are evidence, not a composition target.**
`docs/HUMAN_GUIDANCE.md` settles the authority question: "An existing ODP is imported once; Djot
and its local assets then become authoritative," and "Simplification is the overall goal. Present
the same instructional content through an existing Djot layout whenever possible instead of
preserving the original slide composition." So this plan does not chase the originals' geometry.

What the originals *are* good for is measurement. They rendered correctly in LibreOffice for a
year, so they empirically bound what type sizes are readable and what content volume fits on one
page. Every fitting number in this plan comes from measuring them rather than from a threshold
invented here. This is "use the scientific method" from `docs/REPO_STYLE.md`: the evidence is on
disk, so no constant needs to be guessed.

The trade-off accepted: **the compiler stops choosing pagination and starts owning a measured
floor.** The floor stays -- guidance requires this repository, not LibreOffice's unbounded manual
shrink, to own it -- but its value is set from the corpus instead of from a literal. Splitting is a
compiler decision masquerading as an authoring decision, and it violates the human's first
requirement, so it goes.

**Robustness governs what replaces it.** Guidance is explicit: "Make the software robust: imperfect
inputs, data, state, or behavior should preserve useful operation through context-appropriate
graceful recovery whenever possible." A slide that cannot fit at the preferred floor and can fit at
the shared serializer-valid recovery minimum produces one slide at that reduced size. The compiler
records a diagnostic naming the slide and the size it needed, and **the deck still builds**. One
awkward slide does not cost the instructor the other ninety.

The shared recovery minimum is at least 1 pt, so every recovered value can be serialized by every
supported native exporter. Content that cannot physically fit at that minimum produces a
source-located physical-capacity error. That error identifies an input that no usable native slide
can represent, rather than concealing an invalid size in an otherwise successful build.

This recovery stays deliberately narrow: it covers one named condition -- content the compiler can
represent but not at the preferred size -- and it stays visible through the diagnostic. It is not a
license for generic "recover somehow" behavior elsewhere. A source construct the compiler genuinely
cannot represent still stops at the `layout_validation.py` boundary, because masking a semantic
error is the opposite of robustness.

That is not the "silent fallback" guidance warns against, and the distinction matters. A fallback
hides a problem; this reports it loudly through the capacity diagnostic and the build summary while
still delivering a usable deck. It also preserves 1:1 exactly -- one slide in, one slide out,
always. The failure mode being removed is the whole-build abort, not the reporting. Sub-floor type
is a visible, recorded compromise on one page, which is strictly better than either splitting the
slide or refusing to build the lecture.

Rejected alternative: keep continuation but cap it at one extra page. This preserves the whole
machinery for a behavior the human has ruled out, and leaves the invented floor -- the actual
cause -- in place. It treats the symptom and forfeits the simplification.

**Visual review principle.** Review generated ODP-derived PDFs as classroom slides on their own
merits, and compare original and generated PDFs for functional visual equivalence. LibreOffice
creates every PDF used in either review, including calibration and final artifacts. The original is
guidance, not a geometry target; a cleaner standardized Djot layout is an acceptable improvement.

This is a review principle, not an acceptance gate. Nothing blocks on it. The originals were
sometimes assembled quickly and diverge from any layout for no particular reason, and a large image
or oversized text often just filled empty space rather than signalling importance -- intent a
compiler cannot recover and should not try to. So: where the original arrangement carries real
meaning, that is useful evidence; where it is arbitrary, inconsistent, or unnecessarily custom, the
standard Djot layout wins and the new slide may simply be better than the old one. Guidance says
the same -- "Use one consistent, rule-based Djot theme rather than preserving slide-specific
quirks," and "Prefer simple teaching layouts instead of copying arbitrary legacy ODP geometry."

The gates in this plan are therefore objective and checkable: page-count parity, image aspect
within 1% of source, section identity, title centering, no chrome, tests pass. Visual judgment
never adjudicates any of those. It is applied separately, through a rubric, to the things
automation cannot measure -- awkward empty space, lost prominence, visual imbalance, or a layout
that technically passes and plainly looks bad.

**The rubric has two distinct modes.** Standalone visual quality judges the generated PDF as a
classroom artifact on its own merits. Migration comparison judges the original and generated PDFs
together for functional visual equivalence: useful hierarchy, grouping, emphasis, balance, and
instructional character carry forward while cleaner standardized composition is welcome. An ugly
original against a much cleaner generated slide is an improvement even though they look different.
An original whose figure was deliberately enlarged because it mattered, against a generated slide
where that figure is small in a sea of whitespace, is the regression worth catching.

**Robust assessment comes from several partly independent signals agreeing, not from one number.**
Visual quality is part of this product, and many of its failure modes resist deterministic
encoding, so the measurement earns real weight. The chain:

1. **Deterministic tests first.** One source slide to one output slide; images preserve aspect;
   the intended AutoLayout is present; titles and sections carry the specified alignment; no
   unwanted chrome; the build succeeds. These are facts, they are ordinary tests, and no vision
   model adjudicates them.
2. **Standalone visual quality.** The evaluator sees only the generated page and scores each
   dimension. The goal is a good teaching slide, not a slide resembling the old one.
3. **Migration comparison.** In a separate context, the evaluator sees the original and generated
   pages and answers whether useful visual or instructional information was lost -- `improved`,
   `roughly equivalent`, or `materially worse`, with a reason. This catches what standalone
   scoring cannot know, such as a biologically important figure becoming inconspicuous.
4. **Calibration.** Repeat a representative sample to establish repeatability, and try a second
   vision model to check whether the rubric communicates this project's standard or merely elicits
   one model's taste.
5. **Corpus statistics and outliers**, surfaced as a report the human can read whenever he wants.

**No milestone waits on him.** Guidance is explicit that every implementation milestone must
complete without his participation, so every gate in this plan is closed by a test, a build, or an
agent review. The visual lane produces a report and flags a tail; it never blocks. If he is asleep,
the manager and subagents still have a complete path to the end of the plan.

**Criterion-level results outrank the total.** A slide scoring well overall with Image
presentation at 1 needs attention that a good total would hide.

**The dimensions are broad; the anchors are precise.** The vagueness belongs in *what* is being
judged, and the precision in *what good and bad look like*. Five gestalt dimensions, each 0-4, a
fixed 20-point total:

| Dimension | Question |
| --- | --- |
| Readability | Can the slide be comfortably read and understood in a classroom? |
| Visual organization | Does the arrangement make the slide easy to follow? |
| Emphasis and hierarchy | Does attention go naturally to the important material? |
| Use of space | Does the content feel appropriately sized, balanced, and placed? |
| Overall effectiveness | Does this work as a teaching slide? |

The five universal dimensions give every slide the same fixed 20-point assessment. Short positive
4, 2, and 0 scoring examples show what the anchors mean in practice, while 3 and 1 interpolate
between them. A section divider, dense outline, and image-heavy slide each earn scores on all five
dimensions. Standalone visual quality assesses the generated slide as a classroom artifact;
migration comparison uses the same dimensions as lenses for functional visual equivalence. Three
independent passes and one different vision model calibrate how this shared instrument behaves on
the corpus.

Image quality, crowding, whitespace, type size, and alignment are considered *inside* those
judgments when relevant, rather than each demanding its own score. The things that genuinely need
exactness -- aspect distortion, page counts, centering, chrome -- are deterministic tests already,
and the vision model covers only what those cannot.

The anchors stay holistic to match: "Visual organization = 4" means clear, coherent organization
supporting immediate comprehension -- not a panel count, a whitespace percentage, or an alignment
rule. Each dimension includes short positive 4, 2, and 0 scoring prototypes; 3 and 1 interpolate
between those anchors. A single project-visual-guidance section summarizes the applicable
requirements and links to `docs/HUMAN_GUIDANCE.md`, which remains authoritative. This avoids brittle
per-dimension line citations while keeping the rubric grounded in this project's standard.

`docs/SLIDE_VISUAL_REVIEW_RUBRIC.md` owns the durable definition of visual quality for this
project. This section states the plan's stance; the rubric is the authority, and it is a permanent
pipeline lane rather than migration scaffolding.

Second philosophy, "fix the design, not the symptom," applied to invariants: the layout model has
one producer (`layout_builders.py`). Checks that restate what the builder constructs by
construction are deleted; checks that catch genuine authoring or adapter mistakes stay.

Evidence strategy for uncertain methods: three questions are settled by measurement against the
originals, each with a stated procedure below -- the correct type floors (WP-A3), the correct
`title-only` identity (WP-E3), and whether master-derived geometry beats the current hardcoded
rectangles (WP-C2). No milestone depends on a number invented for this migration.

## Scope

- Delete continuation and grid-decomposition compilation so `compile_layout_deck` emits one
  `LayoutSlide` per source slide.
- Derive `body_floor_size_pt` and `title_floor_size_pt` from measured original-deck evidence and
  remove the hardcoded literals at `presentation_theme.py:572`.
- Add a minimal immutable `CompilationResult` that carries the `LayoutDeck` render plan and
  structured capacity diagnostics through one compilation and normal build reporting.
- Add classification, aggregation, and a `capacity` command around those diagnostics, used by the
  manager during this plan to drive fixes to completion.
- Replace the exception-driven title-fitting retry loop with direct measurement.
- Delete `layout_engine.layout_contract` and `registered_layout_names`, pointing their 28 call
  sites at `layout_registry` and decoupling `slide_lib/importers/` from the compiler.
- Rename the unused `centered-text` contract to `section`, emit it from the importer for
  content-free heading slides, and migrate the 63 `title-only` markers in `genetics/djot/`.
- Give `title-only` a content region matching whatever identity the original decks show it needs.
- Center title-slide and section text horizontally and vertically from validated master facts.
- Write `placement.displayed_rectangle` as ODP picture frame geometry.
- Remove the four `VERTICAL_*` CJK layouts, which are outside Impress's twelve-layout catalog.
- Remove the records and enums left unreachable, and thin the single-producer invariants.
- Supersede the three recorded design decisions that mandate the removed behavior, and amend the
  fourth that fixes the floor values.
- Add fast pytest coverage for centering, picture geometry, and page parity; add E2E coverage
  comparing built output against the original decks.
- Update `docs/CHANGELOG.md`, `docs/DESIGN_DECISIONS.md`, `docs/HUMAN_GUIDANCE.md`, and the
  architecture docs.

## Non-goals

- Keep the importer architecture after source admission: format-neutral raw facts, spatial
  normalization, region planning, topology matching, and the geometry model in `slide_lib/importers/`.
  WP-I1 replaces the temporary-PPTX admission path with one bounded native ODP reader and preserves
  those planning and publication boundaries. This is a stability boundary, not a claim of
  correctness: the page counts show slide-count preservation only, and regression 4 is an evidenced
  semantic mapping defect. Evidenced semantic defects like direct page evidence and layout identity
  stay in scope; the existing planner and emitter retain their focused roles.
- Keep native ODP export. Direct ODF is what made the official LibreOffice layouts
  reachable.
- Leave the Djot parser, the theme reader, and the font-metrics subsystem as they are.
- Keep `slide_lib/layout_validation.py` intact.
- Keep outline, two-panel, and multiple-choice slides exactly as they render today. The human reports these render
  correctly; leave their geometry alone.
- Keep `blank`, `six-panels`, and `gallery` registered even though no current source uses them.
  `blank` and `six-panels` are two of Impress's twelve, and `gallery` is a documented project
  extension. Unused is not unwanted.
- Keep capacity classification and aggregation in the `capacity` command. Normal builds expose the
  minimal structured recovery diagnostics from their single compilation; guidance keeps the linter
  source-only and fast, with geometry, overflow, native animation export, and visual quality as
  separate validation lanes.
- Leave `genetics/djot/*.djot` prose, headings, lists, and images untouched. The only permitted source
  change is mechanical: rewriting the 63 `=== layout: title-only` markers to `=== layout: section`.
- Do not treat generated Djot as the human's authoring backlog. These files were produced from
  working decks; capacity work keeps manual Djot edits at zero. A source-located recovery remains
  visible when evidence supports retained editable authored density or a bounded direct-import
  semantic limitation; repeated compiler constraints and hidden or unreadable output remain defects.

## Current state summary

Build path (`native_export.py:128`): parse `.djot` -> compile once to immutable `CompilationResult`
(a `LayoutDeck` render plan plus structured diagnostics) -> `odp_export.write_odp` -> LibreOffice
converts ODP to PDF. Native output no longer uses a PPTX-to-ODP bridge. Legacy ODP import currently
uses ODP-to-temporary-PPTX normalization; WP-I1 replaces that temporary conversion with the bounded
native ODP reader before WP-D3 retires the PPTX surface.

Layout stack, 3,687 lines: `layout_builders.py` 954, `layout_measurement.py` 629,
`layout_primitives.py` 499, `layout_validation.py` 498, `layout_model.py` 367,
`layout_engine.py` 315, `layout_content.py` 254, `layout_registry.py` 171.

Registry declares 18 contracts. Sources use 10: `one-panel` 158, `two-panels` 70, `title-only` 63
(all content-free section dividers, migrating to `section`), `multiple-choice` 15, `title-slide` 8,
`two-over-one-panels` 7, `stacked-panels` 5, `one-plus-two-panels` 5, `two-plus-one-panels` 3,
`four-panels` 2.

Of the 18 contracts, 14 stay: Impress's twelve, plus the `multiple-choice` question-and-answer
layout and the `gallery` project extension. `centered-text` is renamed to `section`, keeping its
`ONLY_TEXT` identity. The four `VERTICAL_*` CJK layouts are removed as outside the catalog. Layouts
no current source uses but that belong to the twelve stay registered.

Recorded decisions this plan changes, all in `docs/DESIGN_DECISIONS.md`:

| Decision | Line | Action |
| --- | --- | --- |
| Continuation is a fit-gated physical-layout decision | 620 | Superseded -- the compiler no longer paginates |
| Context handoff is explicit | 654 | Superseded -- no continuation means no handoff pages |
| Generic grid overflow decomposes to a one-panel physical topology | 700 | Superseded -- a grid that does not fit fails source-locally |
| Layout capacity is a shared, font-metric-backed compiler result | 728 | Amended -- the compiler keeps capacity ownership; the recorded "30 pt / 24 pt ordinary floors" become corpus-derived values, and pagination and grid decomposition leave its scope |

Ground-truth assets available for measurement: `genetics/*.odp` (the original decks) and
`genetics/*.pdf` (their original renderings), for all eight lectures, untracked but on disk.


## Architecture boundaries and ownership

### Mapping (milestones / workstreams -> components / patches)

| Milestone / Workstream | Component | Review boundary |
| --- | --- | --- |
| M1 / WS-B picture geometry and chrome | `odp_export.py` only | Frame aspect matches source intrinsic aspect; no page number, footer, or date renders |
| M2 / WS-A one-to-one compilation | `layout_engine.py`, `_with_fitting_title` in `layout_builders.py`, continuation helpers in `layout_measurement.py`, continuation records in `layout_model.py`, continuation enums in `layout_primitives.py`, `paginate` in `native_model.py` and `djot_parser.py` | Exactly one page per source slide; no layout decision made by catching an exception |
| M3 / WS-A fitting evidence | new `capacity_report.py`, floors in `presentation_theme.py`, shared constraints in `layout_measurement.py` and `layout_builders.py` | Page parity against the original visible ODP/PDF pages for all eight decks, zero manual Djot edits |
| M4 / WS-V visual review rubric | new `docs/SLIDE_VISUAL_REVIEW_RUBRIC.md` | Visual quality has a written, calibrated definition |
| M5 / WS-S catalog and syntax specification | settled 14-layout catalog; new `docs/DJOT_SLIDE_SYNTAX.md` | Every layout has a stated purpose, not just a slot table |
| M6 / WS-E layout identities | bounded native ODP reader, `layout_registry.py`, `importers/djot_emitter.py:897`, `genetics/djot/*.djot` layout markers | Section identity comes from retained source page evidence; `title-only` can hold content |
| M6 / WS-C template fidelity | `layout_builders._heading_slide`, `_section_slide`, `_frame_text`; `layout_measurement.paragraph_properties`; `presentation_theme` consumption | Rendered title-slide and section pages centered on both axes |
| M7 / WS-D simplification harvest | `layout_primitives.py`, `layout_model.py`, `layout_content.py`, PPTX modules/dependency/tests, `docs/DESIGN_DECISIONS.md` | Named architectural concepts and the PPTX surface retired; no visible rendering change |

WS-A and WS-C both touch `layout_measurement.py` and `layout_builders.py`, so they sit in
different milestones and never run concurrently. WS-B touches one file no other workstream opens.

## Milestone plan

| M | Title | Summary | Goal |
| --- | --- | --- | --- |
| M1 | ODP output defects | Aspect-correct picture frames; remove page-number, footer, and date chrome | Images undistorted, corners clean |
| M2 | One-to-one compilation | Remove continuation and decomposition; measured title fitting; decouple the importer | Exactly one page per source slide |
| M3 | Fitting evidence | Diagnose capacity, ground the type floors in the corpus, and resolve repeated compiler constraints | Every deck builds at original visible ODP/PDF page count with zero unexplained sub-floor slides and no manual Djot edits |
| M4 | Visual review rubric | Derive `docs/SLIDE_VISUAL_REVIEW_RUBRIC.md` from guidance and calibrate it | A trusted way to judge whether slides look right |
| M5 | Syntax specification | `docs/DJOT_SLIDE_SYNTAX.md` defining the authored surface and every layout's purpose | A contract to implement against |
| M6 | Layout identity and fidelity | Add `section`, complete `title-only`, center from master facts | Both layouts work; titles and sections match the .otp |
| M7 | Simplification harvest | Delete what earlier milestones made unreachable | Named architectural concepts gone, no visible rendering change |

M4 depends on nothing and may start at any point, including first and in parallel with M1. It is
its own milestone because deriving five universal criteria from guidance, writing positive scoring
examples and anchors, defining the two review modes, and calibrating repeatability is a substantial
piece of work with a distinct owner and a distinct kind of evidence -- and because the rest of the
plan is judged with it.

Seven tightly scoped milestones rather than three broad ones, deliberately. M1 through M3 were one
milestone in an earlier draft, and M4 and M5 were another; both were split because each half has
its own failure mode -- an ODP serialization bug, a compiler restructuring, an empirical constant,
a rubric derivation, a syntax contract -- and a regression is far easier to isolate when each lands
alone. Smaller milestones also make progress visible and stop one oversized milestone from hiding
several unresolved design decisions. M1 is the fastest visible win and depends on nothing; M4
likewise depends on nothing and may run first or alongside.

**Every milestone completes without human participation.** Each exit criterion is closed by a test,
a build, or an agent review; none waits on the human reading a report, answering a question, or
inspecting a slide. Each patch ends with the changelog updated and the working tree ready for his
review, which he picks up whenever he chooses.

### Milestone: M1 ODP output defects

- Depends on: none
- Deliverables: ODP picture frames carry `displayed_rectangle`; no page number, footer, or date
  renders.
- Workstreams: WS-B
- Entry criteria: `source source_me.sh && pytest tests/` passes on `main` at `b76635c`.
- Exit criteria: every ODP image frame aspect is within 1% of its source intrinsic aspect; no
  built page shows chrome in any corner; `pytest tests/` passes.
- Parallel-plan ready: yes -- WP-B1 and WP-B2 touch different functions in one file.

### Milestone: M2 one-to-one compilation

- Depends on: none (independent of M1; ordered after it only because M1 is quick)
- Deliverables: one compile produces immutable `CompilationResult` containing a `LayoutDeck` render
  plan and structured normal-build diagnostics; the plan emits one page per source slide; the
  14-layout catalog removes unused vertical-flow geometry before the final title solver; title size
  is solved by measurement; the importer package no longer imports the compiler.
- Workstreams: WS-A, with the early catalog patch from WS-S; packages WP-A5, WP-A1, WP-D5, WP-A4
- Entry criteria: M1 committed, or M1 explicitly deferred.
- Exit criteria: no code path can append a second page for one source slide; slide identities carry
  no `-pM` suffix; no `except ValueError` remains in `layout_engine.py` or `layout_builders.py`;
  no module under `slide_lib/importers/` imports `slide_lib.layout_engine`; `pytest tests/` passes.
  Decks are **not** expected to build cleanly yet -- the floors are still wrong, which M3 fixes.
- Parallel-plan ready: no -- WP-A1 establishes the one-to-one core, WP-D5 removes the only remaining
  title-solver geometry mismatch, and WP-A4 completes the direct solver against the final catalog.

### Milestone: M3 fitting evidence

- Depends on: M2
- Deliverables: the `capacity` diagnostic; corpus-derived type floors replacing the literals at
  `presentation_theme.py:572`; repeated compiler capacity constraints resolved and explained
  residual diagnostics retained visibly.
- Workstreams: WS-A, packages WP-A2, WP-A3, WP-A6
- Entry criteria: M2 exit criteria met.
- Exit criteria: for all eight decks the emitted `<draw:page` count equals both the source
  `=== layout:` count and the original visible ODP/PDF page count, with zero unexplained sub-floor
  slides and zero manual Djot edits. A sub-floor diagnostic may remain when corpus evidence shows
  retained editable authored content cannot meet the readable floor in its named native layout, or
  a bounded direct-import semantic limitation is recorded with review evidence. Each recovery is
  source-located and visible in normal builds and `capacity`. A repeated compiler constraint, hidden
  content loss, clipping, unreported unreadability, or a floor-safe source that renders incorrectly
  remains a WP-A6 defect. `pytest tests/` passes.
- Parallel-plan ready: no -- WP-A3 depends on WP-A2's output and WP-A6 on WP-A3's floor.

### Milestone: M4 visual review rubric

- Depends on: nothing -- may run first, or in parallel with M1 through M3
- Deliverables: `docs/SLIDE_VISUAL_REVIEW_RUBRIC.md` -- five gestalt dimensions with centralized
  `docs/HUMAN_GUIDANCE.md` provenance, holistic 0-4 anchors and 4/2/0 prototypes, a fixed 20-point
  total; calibration evidence; registration as a verification lane in `docs/PIPELINE.md`.
- Workstreams: WS-V
- Entry criteria: none.
- Exit criteria: the five dimensions are Readability, Visual organization, Emphasis and hierarchy,
  Use of space, and Overall effectiveness; centralized guidance provenance and written 0-4 anchors
  define their use, supported by short 4/2/0 prototypes; every slide is scored on all five, so the
  total is a fixed 20 with no applicability rules or N/A bookkeeping; calibration characterizes
  repeatability across three independent runs and one alternate vision model; an attention threshold
  is derived from that evidence rather than assumed; `docs/PIPELINE.md` lists the lane and its two
  review modes.
- Parallel-plan ready: no -- one document, one owner, and calibration depends on it.

### Milestone: M5 syntax specification

- Depends on: WP-A1, accepted WP-D5, and WP-E1; a final semantic-accuracy review follows M3.
- Deliverables: `docs/DJOT_SLIDE_SYNTAX.md`,
  defining the authored grammar and, for each of the 14 catalog layouts, what it is *for* -- so an
  author and the importer choose the same way.
- Workstreams: WS-S
- Entry criteria: WP-A1 provides the one-to-one core, WP-D5 establishes the final 14-layout catalog,
  and WP-E1 supplies the legal `section` name.
- Exit criteria: covers slide framing, headings, slots, every layout name with its purpose and
  slots, which layouts accept root content, images, lists, tables, reveals, and reserved or
  unsupported syntax; the `section` versus `title-only` distinction is explicit; every statement
  matches `djot_grammar.py` and `layout_registry.py` or an entry in `docs/DESIGN_DECISIONS.md`; a
  final reviewer checks semantic accuracy after M3.
- Parallel-plan ready: yes -- WP-S1 starts after its catalog and `section` prerequisites, while M3
  completes the independent capacity lane; the final review joins their settled facts.

### Milestone: M6 layout identity and fidelity

- Depends on: accepted WP-S1
- Deliverables: one bounded native ODP reader supplies typed source facts and immutable page
  evidence directly to the existing planning and emission path; a `section` layout on `ONLY_TEXT`
  with the corpus migrated from that evidence; `title-only` able to carry content below its title;
  title-slide and section centered on both axes.
- Workstreams: WS-E after prerequisite WP-E1, then WS-C
- Entry criteria: accepted WP-S1 defines the `section` versus `title-only` semantics this milestone
  implements; M5's final semantic-accuracy review follows M3 in parallel with its later work.
- Exit criteria: every `=== layout:` marker in `genetics/djot/` reflects its direct native-ODP
  page evidence; a `title-only` slide with body content compiles; rendered `lect01b` pages
  1, 3, 6 show centered titles; outline pages 5 and 17 of `lect02b` are unchanged from their M3
  state; `pytest tests/` passes.
- Parallel-plan ready: no -- WS-E renames the contract WS-C then centers, and WS-C is one coherent
  typography change across two files WS-A also edits. Concurrent dispatch invites conflicting
  edits to `layout_registry.py` and `layout_measurement.paragraph_properties`.

### Milestone: M7 simplification harvest

- Depends on: M6
- Deliverables: unreachable continuation records and enums deleted; single-producer invariants
  thinned; superseded design decisions rewritten; duplicated language material trimmed into the
  M5 specification; the maintained PPTX output/import/temporary-conversion surface retired.
- Workstreams: WS-D
- Entry criteria: M6 exit criteria met.
- Exit criteria: the named concepts are absent from `slide_lib/` -- continuation, decomposition,
  grid-stream packing, exception-driven layout search, `layout_engine` pass-throughs,
  `MeasurementStatistics`, and the maintained PPTX modules; `pyflakes` clean; `pytest tests/`
  passes; `deck_tools build` supports `all`, `odp`, and `pdf`, with `all` emitting editable ODP and
  its LibreOffice-derived PDF; `deck_tools import` accepts bounded ODP; all eight decks render
  equivalently to their M6 output. M6 is the last milestone that intentionally changes what a slide
  looks like -- it settles section identity, `title-only`, centering, and master-derived geometry --
  so M5, not M3, is the baseline M6 must preserve.
- Parallel-plan ready: yes

## Workstream breakdown

### Workstream: WS-A one-to-one compilation

- Goal: One physical page per source slide, with type sizes grounded in the original decks so no
  slide needs rewriting.
- Owner: `expert_coder`
- Work packages: WP-A5, WP-A1, WP-A4, WP-A2, WP-A3, WP-A6 (in that order)
- Needs: nothing
- Provides: one immutable `CompilationResult` whose `LayoutDeck` render plan has the source slide
  count and whose diagnostics make any recovery visible.
- Review boundary, when modifying the repository: `reviewer` confirms no code path can append a
  second page for one source slide; content that fits at the shared serializer-valid minimum yields
  a usable slide plus a recorded diagnostic; content below that physical capacity produces a
  source-located error; source structures outside the compiler's model continue through the
  existing `layout_validation.py` boundary; and direct measurement makes every layout decision.

### Workstream: WS-B picture geometry and chrome

- Goal: ODP picture frames use the aspect-correct rectangle the compiler already computes, and no
  page number, footer, or date renders.
- Owner: `coder`
- Work packages: WP-B1, WP-B2
- Needs: nothing
- Provides: undistorted images and clean corners in ODP and LibreOffice-derived PDF.
- Review boundary, when modifying the repository: `reviewer` confirms text, table, and shape frame
  geometry is untouched and only picture frames changed.

### Workstream: WS-V visual review rubric

- Goal: Derive a rubric from stated guidance, calibrate it, and run it as the standing
  visual-quality lane.
- Owner: `planner`, with `reviewer` for WP-S4 and `image_evaluator` for WP-S3
- Work packages: WP-S2, WP-S4, WP-S3
- Needs: nothing for WP-S2 and WP-S4; WP-S3 needs whichever milestone's output it reviews.
- Provides: the pipeline's permanent visual-quality lane and the corpus assessment report.
- Review boundary, when modifying the repository: documentation and reports only; `reviewer`
  confirms the centralized project-visual-guidance section accurately summarizes and links to
  `docs/HUMAN_GUIDANCE.md`, and confirms the rubric has both review modes and universal dimensions.

### Workstream: WS-S syntax specification

- Goal: Document the settled 14-layout catalog as the authoring contract WS-E and WS-C implement
  against.
- Owner: `planner` for WP-S1; `maintainer` completes WP-D5 immediately after WP-A1.
- Work packages: WP-S1, after WP-A1, WP-D5, and WP-E1
- Needs: completed WP-A1 and WP-D5 plus the legal `section` name from WP-E1. WP-D5 runs before
  final title-solver work because its four unused CJK vertical contracts are the only remaining
  title-solver geometry mismatch. The resulting 14-layout catalog lets WP-A4 solve the layouts that
  remain, without adding vertical-flow machinery that the supported catalog does not use. A final
  reviewer checks the published specification for semantic accuracy after M3.
- Provides: the definition of `section` versus `title-only` that WP-E2's importer rule must
  satisfy.
- Review boundary, when modifying the repository: documentation only; `reviewer` checks every claim
  against `djot_grammar.py`, `layout_registry.py`, and `docs/DESIGN_DECISIONS.md`.

### Workstream: WS-E layout identities

- Goal: Make `section` and `title-only` each do the job the human names it for.
- Owner: `coder`
- Work packages: WP-E1, WP-I1, WP-E2, WP-E3
- Needs: WP-A1 for WP-E1 and the downstream layout changes. WP-I1 establishes the independent,
  format-neutral source boundary; WP-E2 joins WP-E1, WP-I1, and WP-S1.
- Provides: a `section` contract for WS-C to center, and a usable `title-only`.
- Review boundary, when modifying the repository: `reviewer` confirms direct ODP page evidence
  supports every migrated marker, every migrated source page was content-free, and the marker-only
  corpus change preserves its authored content.

### Workstream: WS-C template fidelity

- Goal: Drive title-slide and section typography and geometry from validated master facts.
- Owner: `expert_coder`
- Work packages: WP-C1, WP-C2
- Needs: WP-A1, WP-E1
- Provides: centered title-slide and section slides.
- Review boundary, when modifying the repository: outline pages must not change -- that part is
  objective. `image_evaluator` also compares title and section pages against the original PDFs and
  reports concerns under the visual review principle, without blocking.

### Workstream: WS-D simplification harvest

- Goal: Delete what M1 and M2 made unreachable, without changing rendered output.
- Owner: `maintainer`
- Work packages: WP-D1, WP-D4, WP-D2, WP-D3
- Needs: WP-A1, WP-A4, WP-C1, WP-I1, WP-E1, WP-E2, WP-E3
- Provides: a smaller layout stack and documentation that matches it.
- Review boundary, when modifying the repository: rendered pages must read the same as M6 output;
  a visible change is a defect, not an improvement.

## Work packages

### Work package: WP-A5 collapse the layout_engine pass-throughs

- Owner: `coder`
- Touch points: `layout_engine.py` -- delete `layout_contract` and `registered_layout_names`;
  update 28 call sites across `djot_lint.py`, `djot_grammar.py`, `djot_parser.py`,
  `pptx_export.py`, `importers/slide_plan.py`, `importers/topology.py`,
  `importers/native_normalization.py`, `importers/djot_emitter.py`, and affected tests to call
  `slide_lib.layout_registry` directly.
- Depends on: none
- Acceptance criteria: `layout_engine.py` exposes only `compile_layout_deck`; no module under
  `slide_lib/importers/` imports `slide_lib.layout_engine`; `pyflakes` clean.
- Evidence or review, when useful: this is an architectural change, not merely a tidy-up -- it
  narrows a documented public boundary, so record it in `docs/DESIGN_DECISIONS.md` alongside the
  entry that established that boundary. The justification is current dependency evidence: both
  names forward verbatim to `layout_registry`, and they are the only reason the importer package
  depends on the compiler at all. Re-run `graphify map-repo` and confirm the importer communities
  no longer connect to Layout Engine and Pagination.
- Obvious follow-ons: mechanically it is import redirection, so land it first to shrink every later
  review.

### Work package: WP-A1 delete continuation and decomposition compilation

- Owner: `expert_coder`
- Touch points: `layout_engine.py` (delete `_PageCandidate`, `_continuations`, `_decompose_grid`,
  `_context_handoff_pages`, `_context_entries`, `_continuation_source`, `_with_page_number`, and
  the split branch of `_compile_source_pages`); `layout_measurement.py` (delete
  `continuation_units`, `grid_stream_units`, `descendant_list_units`, `list_leaf_paths`,
  `path_fragment`, `mark_context_paragraphs`, `inline_context`, `GridStreamUnit`,
  `ContinuationUnit`); `layout_model.py` (delete `ContinuationContext`,
  `ContinuationContextEntry`, `DecompositionOrigin`, `_validate_continuation_context`, the
  `continuation_kind` / `continuation_context` fields on `LayoutSlide`, `source_parent_id` /
  `continuation_index` on `SlideIdentity`, and the lineage half of `_validate_slide_identities`);
  `layout_primitives.py` (delete `ContinuationPolicy`, `ContinuationKind`,
  `ContinuationContextDisplay`, the `continuation_policy` field, and the `REPEATED_CONTEXT` and
  `GENERATED_CHROME` members of `LayoutObjectOrigin`); `layout_registry.py` (drop `continuation=`
  and `decompose=`); `native_model.py` and `djot_parser.py` (drop `paginate`);
  `layout_builders.py` (delete `compile_grid_stream_page`, `_compile_grid_stream_page_at_theme`,
  `_grid_stream_cell`, `_grid_stream_cell_height`); new `capacity_report.py`, `native_export.py`,
  and `terminal_output.py` for the immutable result and its normal-build reporting.
- Depends on: WP-A5
- Acceptance criteria: `compile_layout_deck` produces one immutable `CompilationResult` per
  requested deck and compiles it once; its `LayoutDeck` remains the render plan and has no loop that
  can append more than one `LayoutSlide` per source slide; slide identities are `slide-N` with no
  `-pM` suffix; normal builds present the result's structured capacity diagnostics without a second
  compilation. A slide that fits at the shared serializer-valid minimum of at least 1 pt compiles
  to one slide at a reduced size and records `path:line`, layout, slot, required size, and preferred
  floor. Content that cannot fit at the serializer-valid minimum raises a source-located
  physical-capacity error. `pyflakes` is clean.
- `CompilationResult` is immutable and travels through export and terminal reporting. The compiler
  collects representable-recovery diagnostics in that result, so every build reports the same
  compilation it exports. The existing validation boundary continues to identify source structures
  outside the compiler's model.
- Evidence or review, when useful: `reviewer` audits the diff to confirm every removed continuation
  path produces either a usable serializer-valid slide with a recorded diagnostic or a
  source-located capacity or validation result, so no authored content disappears without a trace.
- Obvious follow-ons: update `tests/test_layout_engine.py` and `tests/test_layout_model.py` to
  drop continuation cases.

### Work package: WP-A4 replace exception-driven title fitting with measurement

- Owner: `expert_coder`
- Touch points: `layout_builders.py` `_with_fitting_title` (142-159) and `_standard_slide` (133);
  `layout_measurement.py` for the direct-solve helper.
- Depends on: WP-A1
- Acceptance criteria: no `try` / `except ValueError` remains in `layout_builders.py`; the title
  size is computed by measuring required title height against required body height and solving for
  the largest quarter-point size leaving the body above its floor, then built once.
- Evidence or review, when useful: capture the selected title size per slide before and after and
  diff the lists as **one-time replacement evidence**. An exact match is the expected result and
  the quickest way to show the solver is right; a difference is investigated rather than
  automatically rejected, since the old retry loop is being removed partly because its design was
  poor and reproducing its output exactly is not the goal. The durable contract is behavioral:
  the compiler selects the largest fitting title size, deterministically, for the same input. The
  permanent test asserts that property, not a captured list of sizes. Compile-time change is
  informational.
- Obvious follow-ons: `MeasurementStatistics` (`layout_measurement.py:56`) exists to prove
  measurement reuse to a test asserting a caching implementation detail; retire both in WP-D2.

### Work package: WP-A2 enrich capacity reporting

- Owner: `coder`
- Touch points: new `slide_lib/capacity_report.py`; `cli.py` (a `capacity` subcommand);
  `terminal_output.py` for formatting.
- Depends on: WP-A1
- Acceptance criteria: `djot-slides capacity genetics/djot` consumes the structured diagnostics
  from one compilation per deck, classifies and aggregates them by cause, and prints one line per
  overflowing slide giving `path:line`, layout, slot, the point size that would be required, and
  the current floor. It continues across the corpus, exits non-zero when any capacity concern is
  present, and exits zero when none are present.
- Evidence or review, when useful: this is a diagnostic that drives WP-A3 and WP-A6 to completion
  inside this plan. It is not a work order handed to the human.
- Obvious follow-ons: document in `docs/USAGE.md`; reference from `docs/TROUBLESHOOTING.md`.

### Work package: WP-A3 derive the type floors from the original decks

- Owner: `reviewer`
- Touch points: measurement only, then a single constant change in `presentation_theme.py:572`.
- Depends on: WP-A2
- Acceptance criteria: the effective body and title font sizes actually used across all eight
  original `genetics/*.odp` decks are extracted and summarized (distribution, minimum, and the
  minimum excluding decorative or footnote runs); `body_floor_size_pt` and `title_floor_size_pt`
  are set to values that admit the sizes the author already published; the literals at
  `presentation_theme.py:572` are replaced by named constants carrying a comment citing that
  measurement.
- Evidence or review, when useful: the rule is **not** "adopt the smallest size the originals
  used." That a slide once carried 12 pt text proves 12 pt existed, not that 12 pt should become
  this theme's minimum; guidance treats the old decks as visual guidance rather than formatting
  authority, and sets 36 pt / 28 pt defaults precisely because readability is a design goal. The
  rule is: use the corpus to establish the range of typography needed to carry these decks'
  instructional density, then **choose the highest practical floor that serves normal teaching
  density.** Preliminary sampling shows `lect02b` using 22.2 pt, 21 pt, 20 pt, and 18 pt heavily
  with a tail at 12-16 pt, so the answer is below 24 and likely well above 12. Record the
  distribution and the chosen value in the changelog.
- Also produce `tests/original_deck_facts.json`: per deck, physical, hidden, and visible original
  page counts; visible-page layout identities; and the body font-size distribution. Small,
  committed, and diffable, it is the durable form of the evidence this milestone measures. The
  permanent E2E parity check reads the visible count rather than the untracked originals.
- Ordering matters: search from the bulk of the corpus rather than the last stubborn slide. One
  pathological page would then set the global readability floor for all eight decks. Characterize
  the systematic causes first -- WP-A2 groups overflows by cause, and wasted slot space or
  over-generous block spacing belong in WP-A6 as compiler fixes rather than being absorbed by a
  lower floor. Set the floor from the bulk of the corpus, then let WP-A6 close the remainder. If a
  few slides still resist, that is a WP-A6 finding, not a reason to drop the floor further.
- Obvious follow-ons: record in `docs/DESIGN_DECISIONS.md` that floors are corpus-derived, stating
  this rule so a future change re-derives the value rather than picking a number.

### Work package: WP-A6 resolve residual capacity constraints

- Owner: `expert_coder`
- Touch points: determined by the diagnostic -- expected candidates are
  `layout_measurement.select_size`, `slot_rectangles`, `_content_area`, and the inter-block
  spacing constants in `layout_builders.py`.
- Depends on: WP-A3
- Acceptance criteria: all eight decks build with zero unexplained sub-floor slides and zero
  manual Djot edits. For each diagnostic class, the owner consults the original ODP and
  LibreOffice-PDF evidence, then resolves each repeated compiler constraint that prevents a
  reasonable one-slide representation. An explained, source-located diagnostic remains when
  retained editable authored content cannot meet the readable floor in its named native layout or a
  bounded direct-import semantic limitation has review evidence. Normal builds and `capacity`
  display every retained recovery.
- Evidence or review, when useful: the goal is a compiler that represents this content on one
  native editable slide, not one that reproduces original geometry. Fix shared constraints such as a
  floor that is too high, a slot rectangle that wastes space, excessive inter-block spacing, or a
  title band that consumes needed room. Keep an explained diagnostic only with evidence that
  distinguishes physical authored density or a bounded direct-import semantic limitation from a
  repeated compiler constraint. Hidden content loss, clipping, unreported unreadability, and an
  incorrect rendering of floor-safe content remain defects.
- The current 97 recovered slides are one-time implementation evidence for this classification, not
  an acceptance target or a permanent test count. Their reports and paired LibreOffice-PDF review
  evidence support the retained diagnostic classes without encoding a fixed corpus total.
- Obvious follow-ons: any per-slide finding goes in the changelog under
  `### Decisions and Failures` with the original-PDF page cited, for the human to read whenever he
  chooses. Nothing waits on him reading it.

### Work package: WP-B1 write aspect-correct picture frames

- Owner: `coder`
- Touch points: `odp_export.py` -- `_frame_attributes` (183) and its callers.
- Depends on: none
- Acceptance criteria: for `PictureContent`, frame `svg:x`, `svg:y`, `svg:width`, `svg:height`
  derive from `content.placement.displayed_rectangle`; every other content type still derives from
  `item.rectangle`; `pptx_export._write_picture` is the reference and is not modified.
- Evidence or review, when useful: rebuild `lect02b-genes_dogma.odp` and confirm image frame
  aspects match `magick identify` on each source (1.00, 0.98, 1.33) rather than the uniform 1.726
  seen today; spot-check the same figures in `genetics/lect02b-genes_dogma.pdf`.
- Obvious follow-ons: cover the placeholder-bound case -- when `_occupy_primary_slot` promotes a
  picture to a `GRAPHIC` member, the frame must still carry the displayed rectangle.

### Work package: WP-B2 remove slide-number and footer chrome

- Owner: `coder`
- Touch points: `odp_export._add_page_style` (line 102) -- add
  `presentation:display-page-number="false"`, `display-footer="false"`, and
  `display-date-time="false"` to the drawing-page properties; `layout_engine._with_page_number`
  is deleted by WP-A1.
- Depends on: none
- Acceptance criteria: no built deck renders a page number, footer, or date in any corner; the
  master's own `page-number`, `footer`, and `date-time` placeholder frames are suppressed on every
  emitted page; slide content and the top gradient band are unaffected.
- Evidence or review, when useful: this enforces guidance already on record -- "Do not show slide
  numbers; they encourage the audience to track remaining time and watch the clock instead of the
  presenter." The current build violates it from two directions: our own chrome object, and the
  master's footer and date-time placeholders inherited because the exported drawing-page style sets
  `background-objects-visible="true"` without disabling them. Confirm by rendering the bottom strip
  of several pages at high DPI.
- Obvious follow-ons: none -- the master already sets `display-page-number="false"`, so only footer
  and date-time were leaking.

### Work package: WP-S2 write the slide visual review rubric

- Owner: `planner`
- Touch points: new `docs/SLIDE_VISUAL_REVIEW_RUBRIC.md`.
- Depends on: none
- Acceptance criteria: this document is the project's durable definition of visual quality -- what
  "looks right" means here -- and the plan's Design philosophy defers to it rather than restating
  it. A short project-visual-guidance section summarizes the applicable requirements and links once
  to `docs/HUMAN_GUIDANCE.md`, the authoritative source. Five broad dimensions -- Readability,
  Visual organization, Emphasis and hierarchy, Use of space, and Overall effectiveness -- each use
  0-4 holistic anchors and concise positive 4, 2, and 0 scoring prototypes; 3 and 1 interpolate.
  Every slide is scored on all five, so the total is a fixed 20 with no applicability or N/A
  machinery.
- The rubric directs standalone review to the generated ODP-derived PDF produced by LibreOffice and
  asks for scores plus a `no concern`, `minor concern`, or `material concern` call with a visible
  teaching reason. Migration comparison receives original and generated PDFs, both rendered by
  LibreOffice, and uses the same five dimensions as lenses for `improved`, `roughly equivalent`, or
  `materially worse`, with the most important visible teaching reason. It records a direct
  functional-equivalence classification rather than subtracting two totals.
- Deterministic verification owns page count, aspect ratio, layout identity, centering, chrome,
  full-slide raster checks, and other mechanically measurable properties. Image quality, crowding,
  type size, and alignment inform the relevant universal dimension when visually meaningful.
- Obvious follow-ons: this is a **permanent** repository document and a standing part of the
  pipeline, not migration scaffolding. It becomes the visual-quality validation lane that
  `docs/HUMAN_GUIDANCE.md` already names alongside geometry, overflow, and animation export. Add it
  to `docs/PIPELINE.md` under "Verification lanes" with its inputs and its two review modes; record
  it in `docs/DESIGN_DECISIONS.md` as the owner of visual-quality judgment; reference it from
  `docs/DEVELOPMENT.md` so it runs on future imports and on changes that move layout geometry.
  Permanent does not mean gating: it stays advisory, run on demand rather than on every build.

### Work package: WP-S4 calibrate the evaluator

- Owner: `reviewer`
- Touch points: none -- measurement only; results recorded in a calibration section of
  `docs/SLIDE_VISUAL_REVIEW_RUBRIC.md`.
- Depends on: WP-S2
- Acceptance criteria: score a representative sample of roughly 20 generated ODP-derived PDF pages
  produced by LibreOffice -- spanning section, title, outline, image-heavy, and dense slides -- in
  three independent passes, then once with a **different vision model**. Each pass receives the
  rubric and only the opaque standalone review bundle, so it works without prior scores, source
  categories, or original pages. Record the spread per dimension and per slide. The rubric records
  what the measurements show and what follows: the precision the scores support and the advisory
  attention threshold. The package characterizes the measurement; disagreement sharpens anchors or
  supports broader score bands.
- Evidence or review, when useful: repetition measures the stability of the scoring instrument. A
  second model measures whether the rubric communicates this project's visual standard across a
  model change. Calibration records whether dimensions collapse or correlate in practice and
  whether one-point total differences exceed repeatability.
- Obvious follow-ons: set the attention threshold from this evidence rather than assuming ~80%.
  Whatever the number, it selects slides for review; it never fails a build.

### Work package: WP-S3 run the independent visual review

- Owner: `image_evaluator`
- Touch points: none -- review only, over PDFs rendered from ODP by LibreOffice.
- Depends on: WP-S2, and whichever milestone's output is under review
- Acceptance criteria: two named passes over the corpus, answering different questions.
  **Standalone visual quality** is the primary measurement of the final product: the evaluator sees
  only the generated ODP-derived PDF page and scores the five dimensions. **Migration comparison**
  receives the original PDF and its generated ODP-derived PDF, each rendered by LibreOffice, and
  returns `improved`, `roughly equivalent`, or `materially worse` with a reason. It uses the pair as
  evidence for a direct functional-equivalence classification, rather than a subtraction of two
  20-point totals. The standalone pass judges the generated deck as a classroom artifact on its own
  merits. The rubric and `docs/PIPELINE.md` use these two names because they are different
  judgments. Findings record `no concern`, `minor concern`, or `material concern` with one short
  visible-teaching explanation.
- Evidence or review, when useful: reviewers use deterministic verification results for page count,
  image aspect, section identity, chrome, and centering. They use the rubric to assess visible
  quality and functional visual equivalence. Cleaner standard layouts, changed coordinates,
  different wrapping, and simplification can support an improved comparison classification.
- The corpus report is the deliverable, not a list of scores. It states, for the generated corpus:
  the distribution of each dimension and of the 20-point total; the comparative judgments and their
  reasons; and every outlier. It surfaces for review each slide judged
  `materially worse`, each slide below the calibrated attention threshold, and each slide with a
  materially weak individual dimension even when its total looks fine. A deck clustered at 17-19/20
  is far stronger evidence than one averaging the same because half score 20 and several score 12,
  and the report must make that visible.
- Obvious follow-ons: flagged slides are written to the report with both renderings saved beside
  it, so the human can inspect a short tail plus a random sample whenever he wants and judge
  whether the automated review is directing attention correctly. That inspection is optional and
  asynchronous -- **it gates nothing**, and the milestone closes on the report existing, not on
  anyone reading it. Findings inform the next patch. Keep the corpus report as a baseline for later
  runs of this standing lane.

### Work package: WP-S1 write the Djot slide syntax specification

- Owner: `planner`
- Touch points: new `docs/DJOT_SLIDE_SYNTAX.md`.
- Depends on: WP-A1, WP-D5, WP-E1
- Acceptance criteria: the document defines the authored surface -- `=== layout: <name>` slide
  framing, `@<slot>` slot selection, `#` title and `##` subtitle rules, `![alt](path)` images,
  `$inline$` and `$$display$$` math, `<=` and `=>` reveal directives, tables, inline verbatim and
  fenced code, and the ASCII character-reference projection -- plus reserved and unsupported
  syntax. For each catalog layout it gives the slot names, the LibreOffice AutoLayout identity,
  whether root content is accepted, and **a sentence on when an author should choose it**.
- Evidence or review, when useful: the semantic half is the point, not the grammar table. A table
  of names, slots, and AutoLayouts would not have prevented the importer from filing every
  heading-only slide as `title-only`. Worked examples of the distinction the human drew:
  `section` is a divider carrying one prominent centered heading and little or no other content;
  `title-only` is a title at the top with otherwise flexible content below, for material that does
  not fit another named teaching layout. Every layout gets that treatment.
- The document opens by stating the vocabulary rule: the catalog is Impress's twelve layouts, given
  author-facing semantic names where useful, plus explicitly documented project extensions. Each is
  listed with both its official LibreOffice name and its AutoLayout constant, so a reader can tell
  at a glance which layouts are Impress and which this repository added, and can look up the
  LibreOffice documentation for any of them.
- Two entries need their distinction spelled out, because conflating them caused regression 4:
  `section` is this project's semantic name for LibreOffice **Centered text** -- one centered body
  box governed by the Subtitle style, **no title placeholder**, not preconfigured for bullets --
  used for a divider carrying one prominent heading. `title-only` is LibreOffice **Title only** --
  a title box with the rest of the slide deliberately blank, which LibreOffice documents as one of
  the two layouts meant for freely positioned content outside the AutoLayout boxes -- used when no
  other named layout fits the content below. State that a `#` heading in `section` becomes the
  centered text itself rather than a title placeholder.
- Final semantic review follows M3. A reviewer confirms that any capacity-related wording remains
  accurate after the fitting evidence settles, without reopening the documented 14-layout catalog or
  `section`/`title-only` semantics.
- Obvious follow-ons: the semantic descriptions are authoritative for the **importer as well as the
  author**. `layout_registry.py` defines the legal vocabulary and `importers/slide_plan.py`
  performs semantic planning before emission; this document is the human-readable counterpart both
  answer to, so a person choosing a layout by hand and the emitter choosing one from source
  evidence reach the same decision. WP-E2's rule and WP-E3's `title-only` behavior are checked
  against it. Trimming the now-duplicated prose out of `FILE_FORMATS.md`, `USAGE.md`,
  `PIPELINE.md`, and `genetics/djot/README.md` happens later in WP-D4.

### Work package: WP-E1 introduce the section layout

- Owner: `coder`
- Touch points: `layout_registry.py` -- rename `centered-text` to `section`, keeping
  `LibreOfficeAutoLayout.ONLY_TEXT` and its `OUTLINE` member; `layout_builders.py` -- rename
  `_centered_text_slide` to `_section_slide` and update the branch in `_heading_slide`;
  `djot_grammar.py` if it enumerates names.
- Depends on: WP-A1
- Acceptance criteria: `=== layout: section` compiles to a slide whose declared AutoLayout is
  `ONLY_TEXT`; `title-only` still exists and still maps to `TITLE_ONLY`; no `centered-text` name
  remains in `slide_lib/`.
- Evidence or review, when useful: none needed -- a rename plus a grammar addition.
- Obvious follow-ons: describe `section` versus `title-only` in `docs/FILE_FORMATS.md` and
  `docs/LECTURE_LAYOUT_SURVEY.md`.

### Work package: WP-I1 read native ODP sources

- Owner: `expert_coder`
- Touch points: `odf_package.py`, `importers/odp_reader.py`, `importers/odp_to_djot.py`,
  `importers/source_model.py`, focused ODP importer tests, and import documentation.
- Depends on: none -- this is the format-neutral source-admission boundary.
- Acceptance criteria: one bounded native ODP reader admits a validated package and extracts typed
  text, lists, links, tables, geometry, order, package-local media, presenter notes, visibility,
  and page evidence directly into the existing format-neutral raw model. Immutable page evidence,
  keyed by source index, records the source layout identity including explicit absence, declared
  placeholder roles, populated roles, and meaningful-content count. The existing planning and
  emission layers receive those facts unchanged in responsibility. `odp_to_djot.py` retains staging
  Djot validation, reachable-media pruning, atomic publication, the JSON report, and conversion
  summary while it orchestrates the direct reader.
- The reader resolves physical page dimensions at the ODF boundary and normalizes geometry once at
  the existing geometry boundary. It records an explicit review reason for a partially visible frame
  and raises a source-located error for a frame with no visible intersection. It validates package
  members, manifest references, XML, local media, and links before extracting or publishing facts.
- Evidence or review, when useful: focused fixtures prove page visibility, layout identity,
  placeholder roles, text/list/link/table/media/note extraction, geometry, and atomic publication.
  A disposable corpus import records 378 physical, 42 hidden, and 336 visible source pages plus
  page-evidence facts. The direct-import report and its generated LibreOffice PDF pair supply the
  standing migration-comparison evidence.
- Obvious follow-ons: WP-E2 consumes the immutable page-evidence record; WP-D3 retires the
  temporary-PPTX modules and dependency after this reader and its migration evidence are accepted.

### Work package: WP-E2 emit and migrate section slides

- Owner: `expert_coder`
- Touch points: `importers/odp_reader.py`, `importers/odp_to_djot.py`,
  `importers/source_model.py`, `importers/slide_plan.py`, `importers/djot_emitter.py:897`, and
  `genetics/djot/*.djot` layout markers.
- Depends on: WP-E1, WP-I1, WP-S1
- Acceptance criteria: section identity uses WP-I1's immutable positive page-evidence record.
  Select `section` where evidence records exactly one declared `subtitle` placeholder, exactly one
  populated `subtitle` text frame, and no other meaningful content object. Source layout identity
  supplies input evidence and an absent identity remains explicit rather than inferred. Re-importing
  a legacy ODP yields the evidenced layout. In `genetics/djot/`, the 63 confirmed markers become
  `section`; the corpus source diff is confined to `=== layout:` lines.
- Evidence or review, when useful: `reviewer` samples direct-import reports and their corresponding
  original ODP facts, confirms the page-evidence rule and near misses, and confirms no heading,
  list, image, or prose line changed.
- Obvious follow-ons: report the resulting layout distribution; if the originals show a mix rather
  than 63 uniform sections, that is a finding worth recording, not a problem.

### Work package: WP-E3 give title-only its content region

- Owner: `expert_coder`
- Touch points: `layout_registry.py` -- set `allows_root_body=True` on the `title-only` contract;
  `layout_builders.py` -- route a `title-only` slide carrying body blocks through the content path
  instead of `_heading_slide`.
- Depends on: WP-E2, WP-S1
- Acceptance criteria: `title-only` keeps its `LibreOfficeAutoLayout.TITLE_ONLY` identity and its
  single title placeholder; body content beneath the title is emitted as ordinary native objects
  outside any content placeholder; a `title-only` slide with only a heading still compiles.
- Evidence or review, when useful: settled by documentation, not by experiment. LibreOffice defines
  Title Only as a title box with the rest of the slide blank, and identifies Blank and Title Only
  as precisely the layouts intended for ordinary text boxes and other freely positioned content
  outside the AutoLayout boxes. That is the human's escape hatch exactly as he described it --
  "when other layouts do not fit the content below" -- so `TITLE_ONLY` plus free native objects is
  the officially correct shape, not a workaround. Do not convert it to `TITLE_CONTENT`; that would
  trade a semantic layout identity for storage convenience and contradict the source. Native
  editable frames and LibreOffice placeholder identity are already separate concepts in this
  codebase, so body content does not require a content-placeholder identity.
- Obvious follow-ons: after WP-E2 the corpus may retain some `title-only` uses; confirm those still
  render correctly rather than assuming the count is zero.

### Work package: WP-C1 center title-slide and section typography

- Owner: `expert_coder`
- Touch points: `layout_measurement.paragraph_properties` (272) -- take alignment as a parameter
  defaulting to `START` so outline callers are unchanged; `layout_builders._frame_text` (850) --
  take vertical alignment as a parameter defaulting to `TOP`; `_heading_slide` -- pass `CENTER` and
  `MIDDLE` for `title-slide` and `section` only.
- Depends on: WP-A1, WP-E1
- Acceptance criteria: `title-slide` and `section` produce paragraphs with
  `HorizontalAlignment.CENTER` and frames with `VerticalAlignment.MIDDLE`; `title-only`,
  `one-panel`, `two-panels`, and every grid layout produce `START` and `TOP` exactly as before.
- Evidence or review, when useful: `image_evaluator` compares rendered `lect01b` pages 1, 3, 6
  against the same pages of `genetics/lect01b-genetic_disorders.pdf`, and confirms pages 5 and 17
  of `lect02b` are unchanged from their M3 state.
- Obvious follow-ons: `_section_slide` and the centered branch of `_heading_slide` now do the same
  work; fold them into one path.

### Work package: WP-C2 source title geometry from the master theme

- Owner: `expert_coder`
- Touch points: `layout_builders._heading_slide` -- replace the hardcoded
  `LogicalRectangle(110, 180, 1060, 250)` and `(110, 445, 1060, 125)` with rectangles derived from
  `theme.title_frame`; add cm-to-logical-pixel conversion using `theme.emu_per_logical_pixel`.
- Depends on: WP-C1
- Acceptance criteria: `theme.title_frame` has at least one consumer -- today it is read,
  validated at `presentation_theme.py:543`, and never used; title geometry for `title-slide` and
  `section` derives from the master.
- Evidence or review, when useful: scope is deliberately limited to `title-slide` and `section`,
  the two layouts the human reports as wrong. `one-panel` and the grid layouts keep their current
  geometry, which he reports as good. Extend master-derived geometry to `one-panel` only if a
  later comparison against the original PDFs shows an actual mismatch; that is a separate change,
  not part of this one.
- Obvious follow-ons: `_unoccupied_classifier_rectangle` carries the same literals for the layouts
  in scope and should move to the same source of truth.

### Work package: WP-D5 remove the CJK vertical layouts

- Owner: `maintainer`
- Touch points: `layout_registry.py`; the `vertical_title`, `vertical_slots`, and vertical
  `TextDirection` handling in `layout_builders.py` and `layout_primitives.py`; `djot_grammar.py`;
  `docs/DESIGN_DECISIONS.md` entry "Vertical root-body layouts use one author-visible block";
  `docs/HUMAN_GUIDANCE.md` catalog bullets; affected tests.
- Depends on: WP-A1
- Ordering: runs immediately after WP-A1's one-to-one core and before WP-A4's final title solver
  and M3 fitting acceptance. The four unused CJK vertical contracts are the sole remaining
  title-solver geometry mismatch; their removal establishes the supported 14-layout catalog before
  the solver is finalized.
- Acceptance criteria: `vertical-panel`, `vertical-text-panel`, `vertical-title-two-panels`, and
  `two-panels-vertical-clipart` are gone along with the vertical text-direction machinery they
  alone required; the remaining catalog is exactly Impress's twelve plus `multiple-choice` and
  `gallery`; no source or importer references a removed name; all eight decks build unchanged.
- Evidence or review, when useful: these use `VERTICAL_*` AutoLayouts, which Impress exposes only
  with Asian-language support enabled and which are absent from the twelve-entry layout panel the
  human identified as the catalog. Confirm no `genetics/djot/` source and no importer path emits
  one before deleting. Note for the reviewer: this reverses an intermediate draft of this plan that
  kept them; that draft cited layout names in `docs/HUMAN_GUIDANCE.md` which turned out to be
  agent-authored rather than human decisions.
- Obvious follow-ons: update `docs/LECTURE_LAYOUT_SURVEY.md` and `docs/FILE_FORMATS.md`; the
  removed CJK support also simplifies `_frame_text` and the `TextDirection` enum.

### Work package: WP-D1 supersede the recorded decisions

- Owner: `maintainer`
- Touch points: `docs/DESIGN_DECISIONS.md` -- the four entries named in Current state summary.
- Depends on: WP-A1, WP-A3
- Acceptance criteria: the three superseded entries are rewritten to record the new decision with
  its reasoning and consequence rather than deleted, since a reader needs to know the old behavior
  existed and why it went; "Layout capacity" is amended so its floor values cite the corpus
  measurement and its scope no longer claims pagination or grid decomposition; no entry still
  describes `ContinuationContext`, `CONTEXT_HANDOFF`, or `DECOMPOSE_TO_ONE_PANEL` as current.
- Evidence or review, when useful: `reviewer` greps `docs/` for the removed type names and
  confirms no doc still presents them as implemented behavior.
- Obvious follow-ons: `docs/PIPELINE.md` and `docs/CODE_ARCHITECTURE.md` describe the same
  behavior and need the same pass.

### Work package: WP-D4 consolidate documentation into the syntax specification

- Owner: `maintainer`
- Touch points: trim the language material now duplicated by `docs/DJOT_SLIDE_SYNTAX.md` out of
  `docs/FILE_FORMATS.md`, `docs/USAGE.md` ("Authoring boundaries"), `docs/PIPELINE.md`
  ("Extended-Djot language boundary", and delete "Continuation policy" outright), and
  `genetics/djot/README.md`, so each links to the specification instead of restating it.
- Depends on: WP-S1, WP-E3, WP-C1
- Acceptance criteria: `docs/DJOT_SLIDE_SYNTAX.md` is the single reference; the other documents
  link to it rather than duplicating it; no document still presents `paginate` or continuation
  syntax as current; the specification is updated to reflect anything WP-E2, WP-E3, or WP-C1
  settled after M2.
- Evidence or review, when useful: the language was spread across `FILE_FORMATS.md`, `USAGE.md`,
  `PIPELINE.md`, `COOKBOOK.md`, `LECTURE_LAYOUT_SURVEY.md`, `genetics/djot/README.md`, and about a
  dozen `DESIGN_DECISIONS.md` entries. M2 created the single home; this closes the duplicates.
- Obvious follow-ons: link it from `README.md`; `docs/ROADMAP.md` and `docs/TODO.md` also carry
  stale `=== layout:` examples worth a pass.

### Work package: WP-D2 thin single-producer invariants

- Owner: `maintainer`
- Touch points: `layout_primitives.py` (30 `raise ValueError`), `layout_model.py` (41),
  `layout_content.py` (15).
- Depends on: WP-A1, WP-A4
- Acceptance criteria: `MeasurementStatistics` and the test asserting cache-hit counts are
  retired; every retained check carries one comment naming the authoring or adapter mistake it
  catches; checks that only restate what `layout_builders.py` constructs by construction are
  deleted; the `LayoutSlide` topology cross-check, the reveal activation-order check, and the
  `PicturePlacement` fit rules are explicitly retained as adapter contracts; rendered output is
  unchanged on all eight decks.
- Evidence or review, when useful: `reviewer` verifies no deleted check was the only thing between
  a malformed `.djot` and a corrupt ODP.
- Obvious follow-ons: once WP-D3 lands, `PicturePlacement` retains only `CONTAIN`, so drop
  `COVER` and `STRETCH` with it.

### Work package: WP-D3 remove the PPTX sibling

- Owner: `maintainer`
- Touch points: retire `pptx_export.py`, `pptx_animation.py`, `importers/pptx_reader.py`,
  `importers/pptx_to_djot.py`, temporary-PPTX conversion in `odp_reader.py`, the PPTX-only tests,
  direct-PPTX CLI dispatch, and `python-pptx`; update `native_export.py`, `cli.py`,
  `build_slides.sh`, requirements, import/output tests, and user documentation.
- Depends on: WP-B1, WP-I1, and WP-E2. WP-I1 and WP-E2 have accepted their direct-import and
  page-evidence gates before retirement begins.
- Acceptance criteria: `deck_tools build` supports `all`, `odp`, and `pdf`; `all` emits editable
  ODP and its LibreOffice-derived PDF. `deck_tools import` accepts bounded ODP only. A person with
  a legacy PPTX saves it as ODP with LibreOffice, then invokes `deck_tools import` on that ODP.
  Production and test modules use the native ODP reader and native ODP output path, with no
  temporary conversion or `python-pptx` import/reference. `pytest tests/` and `pyflakes` pass; all
  eight decks produce editable ODP and LibreOffice-derived PDF with unchanged rendering.
- Evidence or review, when useful: the reasoning and outcome go in `docs/DESIGN_DECISIONS.md`,
  superseding the entries that describe PPTX as a maintained sibling artifact. See Resolved
  decisions for why this version succeeds without it.
- Obvious follow-ons: `VERSION` and `pyproject.toml` bump per the CalVer rules in
  `docs/REPO_STYLE.md`.

## Acceptance criteria and gates

- Per-patch gate: `source source_me.sh && pytest tests/` passes; `pyflakes` clean via
  `tests/test_pyflakes_code_lint.py`; `docs/CHANGELOG.md` updated under the correct dated
  subsection.
- Integration gate: `./build_slides.sh genetics` compiles once per requested deck and completes for
  all eight decks with zero unexplained sub-floor slides and zero manual Djot edits. For each deck,
  the emitted `<draw:page` count equals both the source slide count and the original visible
  ODP/PDF page count; every ODP picture frame aspect is within 1% of its source intrinsic aspect;
  every produced PDF derives from its native ODP through LibreOffice. An explained recovery is
  source-located and visible in normal builds and `capacity` when evidence supports retained
  editable authored density in its named native layout or a bounded direct-import semantic
  limitation with review evidence. Repeated compiler constraints, hidden content loss, clipping,
  unreported unreadability, and incorrect rendering of floor-safe content fail this gate.
- Architectural gate for M7: the named concepts are absent from `slide_lib/` -- continuation,
  decomposition, grid-stream packing, exception-driven layout search, `layout_engine`
  pass-throughs, `MeasurementStatistics` -- and absent from `docs/` as descriptions of current
  behavior. Line reduction is recorded as supporting evidence, not as the success criterion; a
  smaller file count does not by itself show the design improved.
- Independent review, advisory: `image_evaluator` applies the rubric's standalone mode to generated
  ODP-derived LibreOffice PDFs and its migration-comparison mode to original and generated
  LibreOffice PDFs. Deterministic verification establishes page parity, centering, aspect, identity,
  and chrome; visual review reports visible teaching concerns and functional-equivalence findings
  for the human to weigh.

## Test and verification strategy

Before writing any test, the owner reads `docs/PYTEST_STYLE.md`, `tests/TESTS_README.md`, and
`docs/E2E_TESTS.md` and checks each proposed test against them, rather than assuming the shapes
below comply. Two rules bear directly on this plan: `tests/conftest.py` sets
`collect_ignore = ["e2e", "playwright"]`, so the corpus checks stay out of the fast lane by
construction; and the fixture policy wants inline inputs under `tmp_path`, which is why the cases
below build their own decks rather than reading committed samples. Repo-local exclusions belong in
`REPO_HYGIENE_FILTERS` in `tests/conftest.py`, currently empty.

Fast pytest under `tests/`, per `docs/PYTEST_STYLE.md` -- inline inputs, `tmp_path` only, well
under one second, asserting behavior rather than constants:

- Compile a two-slide inline deck and assert the `LayoutDeck` has exactly two slides.
- Compile an inline deck whose slide fits below the preferred floor but at the shared
  serializer-valid minimum, and assert that it yields one slide with a source-located diagnostic.
  Compile content that exceeds physical capacity at that minimum and assert its source-located
  capacity error. These cases establish usable graceful recovery and an explicit physical boundary.
- Compile the same inline deck twice and assert the selected title size is identical, and that it
  is the largest size leaving the body above its floor. This is the durable title-fitting contract
  -- a behavioral property, not a captured list of per-slide sizes.
- Compile an inline `title-slide` and an inline `section`; assert each title paragraph alignment is
  `CENTER` and each frame vertical alignment is `MIDDLE`. Compile an inline `title-only` and an
  inline `one-panel`; assert `START` / `TOP`.
- Compile an inline `section` and assert its declared AutoLayout is `ONLY_TEXT`.
- Compile an inline `title-only` carrying a paragraph and assert the content is placed below the
  title rather than rejected.
- Build a `PictureContent` whose source aspect differs from its allocation and assert the emitted
  `draw:frame` width-to-height ratio matches the source ratio, not the allocation ratio.

Non-browser E2E under `tests/e2e/`, per `docs/E2E_TESTS.md`, named `e2e_*.py`:

- Extend `tests/e2e/e2e_djot_native_layouts.py` to build each committed deck and assert page-count
  parity and image aspect across the real corpus. These touch the filesystem and invoke
  LibreOffice, so they stay outside the pytest fast lane.

**The originals become a committed facts file rather than a permanent test dependency.** The
60 MB of untracked `genetics/*.odp` are the evidence base for the floor, the importer semantics,
and migration comparison -- and a permanent runner that silently skips once they move would turn
"test skipped" into permanent loss of the source of truth. So WP-A3 extracts what later work
actually needs into a small committed JSON: per deck, physical, hidden, and visible page counts,
visible-page layout identities, and the body font-size distribution. That file is
repository-appropriate, diffable, survives the originals, and is what the permanent E2E parity
check reads. It is deliberately a compact set of structural facts serving demonstrated needs --
future importer regressions and visible-page parity -- not an attempt to preserve every property of
every legacy slide.

The originals stay useful while they exist, for visual comparison and for any question the facts
file does not answer, and nothing permanent depends on them.

Equivalence method for M7: **not byte-reproducible.** A byte gate would be both wrong and flaky --
`odf_package.py:200` calls `zipfile.writestr` with a string member name, which stamps the current
local time into every entry, so two identical builds already differ on disk. M7 is a structural
cleanup, so what must hold is that it changed nothing a viewer would notice. The checkable part is
objective: same page count, same images at the same aspects, no new failures, tests pass. Beyond
that, `image_evaluator` renders before and after and reports anything that looks materially
different, applying the visual review principle from Design philosophy. Shifted wrapping, changed
coordinates, and different object dimensions are expected and are not defects.

Two separate questions, deliberately evaluated apart, because conflating them is what produced the
section/`title-only` error:

- **Did we translate the slide into the right Djot?** Compare the `.djot` against the original
  `.odp` for layout identity and content grouping. Owned by the WS-E migration work.
- **Does the compiler render that Djot appropriately?** Compare the generated ODP-derived
  LibreOffice PDF against the `.djot` intent and, for vibe, against the original LibreOffice PDF.
  Owned by WS-A, WS-B, and WS-C.

Manual visual confirmation: render LibreOffice-produced PDFs for `lect01b` pages 1, 3, 5, 6 and
`lect02b` pages 17 and 21 at 60 DPI at each milestone and compare against the same original PDF
pages.
Page 5 of `lect01b` and page 17 of `lect02b` are the outline controls that must not change.

## Risk register

| Risk | Impact | Trigger | Owner | Mitigation |
| --- | --- | --- | --- | --- |
| Lowering the type floor makes some slides genuinely unreadable | Medium | WP-A3 sets the floor too low | `reviewer` | WP-A3 derives the floor from the corpus distribution and normal teaching density, not from the hardest slide; residual failures go to WP-A6 as compiler fixes rather than pushing the floor down further; `image_evaluator` spot-checks the smallest-type slides |
| Residual capacity reflects a repeated compiler constraint or hides unusable output | High -- this is the outcome the plan exists to avoid | A diagnostic class repeats without explanation, or content is lost, clipped, unreadable without reporting, or incorrect despite fitting the floor | `expert_coder` | WP-A6 resolves the shared constraint. Retained editable authored density and bounded direct-import semantic limitations keep source-located, review-backed diagnostics visible in normal builds and `capacity` |
| Decks carry capacity diagnostics between M2 and M3 | Low | M2 lands and M3 is active | manager | Graceful degradation keeps every deck building when content fits at the shared serializer-valid minimum: recovery appears in the normal build summary. M3 resolves repeated compiler constraints and retains only explained, source-located recoveries |
| Master-derived title geometry looks worse than the current rectangles | Low | WP-C2 review | `image_evaluator` | WP-C2 is scoped to `title-slide` and `section` only; `one-panel` and grid layouts are explicitly out of scope |
| The corpus migration rewrites more than the layout marker | Medium | WP-E2 uses a loose pattern | `expert_coder` | Acceptance confines the diff to `=== layout:` lines, verified with `git diff --stat` |
| The rubric score hardens from an assessment signal into an acceptance gate | Medium | A threshold starts blocking patches, or a low score is treated as a defect without a reason attached | `planner` | The rubric is a permanent calibrated measurement, but every gate in this plan is deterministic; scores and the qualitative call select slides for attention and never fail a build |
| The measured title solver picks different sizes than the retry loop | Medium | WP-A4 rewrite | `expert_coder` | Acceptance requires an empty per-slide selected-size diff across all eight decks |
| Invariant thinning silently permits a corrupt ODP | Medium | WP-D2 over-deletes | `reviewer` | Every retained check carries a justifying comment; topology, reveal-order, and picture-fit checks are named non-removable; `layout_validation.py` is out of scope |
| Direct ODP reading loses source semantics before section planning | High | WP-I1 lacks typed page evidence or corpus-import facts | `expert_coder` | WP-I1 retains typed content, geometry, media, notes, visibility, and immutable page evidence at the native boundary; its direct-import evidence gate completes before WP-E2 migrates markers |
| Original decks are moved or deleted, removing the ground truth | Medium | The untracked `genetics/*.odp` disappear | manager | WP-A3 extracts physical, hidden, and visible page counts, visible-page layout identities, and font-size distributions into committed `tests/original_deck_facts.json`, so the permanent parity check and future importer work keep their baseline once the 60 MB of originals are gone |

## Rollout and release checklist

- [x] Original-deck baselines (page counts, body font-size distributions) recorded in
      `docs/CHANGELOG.md`
- [x] M3 integration gate met: all eight decks build at original visible ODP/PDF page count, zero
      unexplained sub-floor slides, zero manual Djot edits, and visible source-located recovery
      evidence where retained diagnostics remain
- [x] No `=== layout: title-only` marker remains in `genetics/djot/`
- [x] A `title-only` slide with body content compiles
- [x] WP-I1 direct-import gate records typed native ODP facts and 378 physical / 42 hidden / 336
      visible source pages before marker migration
- [x] No page number, footer, or date renders on any built page
- [x] Visual review against original and generated LibreOffice PDFs recorded by `image_evaluator`
      as advisory notes
- [x] `docs/DJOT_SLIDE_SYNTAX.md` published, covering every layout's purpose as well as its grammar
- [x] `docs/SLIDE_VISUAL_REVIEW_RUBRIC.md` published, calibrated, and registered as a verification
      lane in `docs/PIPELINE.md`
- [x] M7 architectural gate met: named concepts absent from `slide_lib/` and from `docs/`
- [x] `deck_tools build all` emits editable ODP and LibreOffice-derived PDF; `deck_tools import`
      accepts bounded ODP
- [x] `slide_lib/` line count recorded as supporting evidence
- [x] `graphify map-repo` re-run so the architecture graph drops the deleted nodes
- [x] `VERSION` bumped to 26.09.1; this non-PyPI application has no `pyproject.toml` to bump, as
      documented in `docs/CHANGELOG.md`
- [x] `docs/CHANGELOG.md` updated and the working tree left ready for the human's review

## Documentation close-out requirements

- Active plan / progress tracker: create
  `docs/active_plans/active/original_deck_fidelity.md` from this plan; `git mv` to
  `docs/archive/` at closure.
- `docs/CHANGELOG.md`: one entry per milestone under the correct dated subsections --
  `### Behavior or Interface Changes` for the 1:1 rule, corpus-derived floors, and the `section`
  layout; `### Fixes and Maintenance` for centering and image aspect; `### Removals and
  Deprecations` for the continuation machinery; `### Decisions and
  Failures` for the floor measurement, the `title-only` identity, and PPTX removal.
- `docs/DESIGN_DECISIONS.md`: new entries for "one source slide is one output page" (Owner:
  `slide_lib/layout_engine.py`), "type floors are corpus-derived, not invented" (Owner:
  `slide_lib/presentation_theme.py`), the `section` layout on `ONLY_TEXT` (Owner:
  `slide_lib/layout_registry.py`), the bounded native ODP import boundary, the settled
  `title-only` identity, and PPTX removal. Plus
  the WP-D1 rewrite of the three superseded entries and the "Layout capacity" amendment.
- `docs/HUMAN_GUIDANCE.md`: update the two catalog bullets from `centered-text` to `section`, and
  add the human's stated distinction between `section` and `title-only`. Note in the changelog that
  the layout identifiers in that file are agent-authored project vocabulary rather than human
  naming decisions, so future work cites its requirements rather than its identifiers. Everything
  else in that file this plan leaves alone.
- New `docs/DJOT_SLIDE_SYNTAX.md` per WP-S1 in M5, with `FILE_FORMATS.md`, `USAGE.md`,
  `PIPELINE.md`, and `genetics/djot/README.md` trimmed to link to it in WP-D4.
  `docs/PIPELINE.md` also loses its "Continuation policy" section outright.
- `docs/HUMAN_GUIDANCE.md`: the human's four requirements in his own words -- 1:1 slides, centered
  title and section layouts, never stretching images, and the section versus `title-only`
  distinction ("I use new section layout quite often and title-only mostly for when other layouts
  do not fit the content below").
- `docs/CODE_ARCHITECTURE.md` and `docs/FILE_STRUCTURE.md`: refresh after M7, which is where the
  module deletions land.
- `docs/PIPELINE.md`: register `docs/SLIDE_VISUAL_REVIEW_RUBRIC.md` under "Verification lanes" as
  the standing visual-quality lane, with LibreOffice-rendered ODP-derived PDF inputs, its two review
  modes, and the attention threshold WP-S4 derives.
- `docs/DEVELOPMENT.md`: state when the visual-review lane is run -- on future ODP imports and on
  any change that moves layout geometry.
- `docs/USAGE.md`: document the normal-build capacity summary, the `capacity` subcommand, native
  ODP import, and `all` as editable ODP plus LibreOffice-derived PDF.
- Archive: `docs/active_plans/active/native_odp_layout_migration.md` describes the continuation
  behavior this plan removes; `git mv` to `docs/archive/` at closure.

## Patch plan and reporting format

- Patch 1 (WP-B1 + WP-B2): ODP picture frame geometry and chrome removal. Depends on nothing and
  is the fastest visible improvement. Closes M1.
- Patch 2a (WP-A5): collapse the `layout_engine` pass-throughs.
- Patch 2b (WP-A1 -> WP-D5 -> WP-A4): one-to-one compilation, then the CJK catalog removal, then
  immutable compilation results with normal-build capacity reporting and measured title fitting.
  WP-D5 runs between the one-to-one core and the final solver because the unused vertical contracts
  are the remaining solver geometry mismatch; the resulting 14-layout catalog avoids vertical-flow
  implementation that no supported layout needs. Closes M2. Decks keep building through
  serializer-valid recovery, while a source-located error identifies content beyond physical capacity
  until Patch 3 resolves repeated constraints and retains only evidence-backed diagnostics.
- Patch 3 (WP-A2 + WP-A3 + WP-A6): capacity diagnostic, corpus-derived floors, and resolution of
  repeated capacity constraints with visible evidence-backed residual diagnostics. Closes M3.
- Patch 4a (WP-S2 + WP-S4): the visual review rubric, derived from guidance and calibrated.
  Depends on nothing and may land at any point, including first. Closes M4.
- Patch 4b (WP-E1 + WP-S1): establish the legal `section` name, then publish the settled 14-layout
  catalog. Its final semantic-accuracy review follows M3. Documentation provides the contract the
  next patches implement against. Closes M5 after that review.
- Patch 5a (WP-I1 + WP-E2 + WP-E3): bounded native ODP import with page evidence,
  evidence-based corpus migration, and the `title-only` capability. WP-I1 may complete
  independently; WP-E2 begins after WP-E1, WP-I1, and WP-S1 provide the settled section contract.
- Patch 5b (WP-C1 + WP-C2): title-slide and section centering and master-derived geometry.
  Closes M6.
- Patch 6 (WP-D1 + WP-D4 + WP-D2 + WP-D3): superseded decisions, documentation consolidation,
  invariant thinning, and complete PPTX-surface retirement.
- Patch 7: version bump and plan archival. Closes M7.

WP-S3 runs the visual review against Patches 1, 3, 5a, and 5b as each lands.

Each patch reports: files touched, `pytest tests/` result, per-deck page counts against the original
visible ODP/PDF count, and for Patches 1, 3, 5a, and 5b LibreOffice-rendered before-and-after PDFs
compared against the original PDFs.

## Resolved decisions

Every scope question this plan raised is settled here. No milestone waits on an answer.

**PPTX is retired in WP-D3 after WP-I1 and WP-E2.** In scope, owned by `maintainer`. Native output
already writes ODF directly with stdlib `xml.etree`; legacy ODP import still normalizes through a
temporary PPTX until WP-I1 supplies the bounded direct reader and WP-E2 consumes its page evidence.
The accepted end state has one native migration boundary and one editable output: legacy ODP enters
the bounded native reader, Djot compiles to editable ODP, and LibreOffice derives the PDF. WP-D3
retires the maintained OOXML serializer, animation writer, direct importer, temporary conversion,
dependency, and PPTX-only tests after those direct-import gates pass. A collaborator with a legacy
PPTX saves it as ODP with LibreOffice, then invokes `deck_tools import` on that ODP. Success condition:
`deck_tools build` supports `all`, `odp`, and `pdf`, with `all` emitting ODP plus its
LibreOffice-derived PDF; `deck_tools import` accepts bounded ODP; native production and test code
contains no PPTX or `python-pptx` references; and all eight decks produce editable ODP and
LibreOffice-derived PDF.

**The `docs/HUMAN_GUIDANCE.md` provenance pass is in scope**, folded into WP-D1, owned by
`maintainer`. The layout identifiers in that file are agent-authored while its requirements are the
human's, and this plan already found one place where that conflation produced a wrong decision.
Leaving it half-corrected invites the same mistake. WP-D1 marks each layout-vocabulary bullet as
project vocabulary and leaves the requirement bullets in his voice untouched. Success condition:
a reader can tell which bullets are his words and which are project naming, and
`docs/DESIGN_DECISIONS.md` records the distinction.

**Evidence versus infrastructure is settled**, so this plan does not recreate the overengineering
it removes. Permanent: `docs/DJOT_SLIDE_SYNTAX.md`, `docs/SLIDE_VISUAL_REVIEW_RUBRIC.md` and its
pipeline lane, the fast pytest cases, and the corpus-derived floor constants. One-time evidence,
recorded in the changelog and then complete: the full-corpus page-parity comparison, the source
font-size distribution inventory, the rubric's calibration runs, the WP-A4 title-size diff, and the
migration scorecards. The E2E parity runner stays permanent because WP-A3 gives it a committed
input -- `tests/original_deck_facts.json` -- so it tests a real, durable contract instead of
skipping once the untracked originals move. That file is the durable form of the evidence, and
`docs/PYTEST_STYLE.md` governs its use: the fast lane keeps inline `tmp_path` inputs, and the
corpus check lives in `tests/e2e/`.
