# Plan: Close native fidelity gaps

Status: implemented on 2026-09-15. The optional strict-Jotdown acceptance lane remains pending
because the pinned executable is not installed in this checkout.

## Context

The `big-image` layout now gives focal images most of the slide while retaining an editable caption.
Three remaining gaps prevent Djot decks from matching the useful structure of the original lecture
slides:

- Authored text cannot yet select a semantic font color, even though physical text runs already
  carry a resolved foreground color.
- Djot cannot author arrows or outline boxes over an image, and the importer cannot preserve those
  supported shapes as source.
- Native tables use a dark body fill and can clip text because the builder discards measured row
  heights.

These gaps are narrower than a general drawing or styling system. The target remains one canonical
Djot source, one authored slide per output slide, editable native ODP objects, preserved image aspect
ratios, and font glyphs throughout the final presentation and PDF.

## Objectives

- Add a small semantic text-color mapping through Djot's existing attribute language.
- Add native editable arrows and transparent outline rectangles over one contained image.
- Repair native table colors and make serialized row and column geometry agree with measurement.
- Preserve supported text colors and image overlays during bounded legacy import.
- Validate the result in generated ODP and LibreOffice-derived PDF without rasterizing text or
  annotation shapes.

## Design philosophy

Apply **Fix the design, not the symptom**, **Use the scientific method**, and **Perfect is the enemy
of good** from [REPO_STYLE.md](../../REPO_STYLE.md). Use one semantic fact from source through the
format-neutral model and into native ODF. Keep each vocabulary closed and justified by an actual
lecture slide.

The first implementation supports named text-color roles, one-ended arrows, and unfilled rectangle
outlines. It repairs the current table model before considering author-controlled column widths or
new table syntax.

Evidence strategy for uncertain methods:

- Compare representative original slides with current output before settling color scope and
  overlay source syntax.
- Use a temporary LibreOffice-native ODF probe to choose arrow-marker, transparent-fill, and table
  row-height forms that survive an ODP open/save round trip.
- Add content-aware table columns only when the repaired equal-column version still causes avoidable
  wrapping on representative tables.

## Scope

- Inventory the actual text colors, arrows, outlines, and table shapes needed by the current
  Genetics corpus.
- Define semantic text colors through one-line Djot attributes and, when required by the corpus,
  strict-Djot inline spans.
- Add an optional, image-scoped overlay surface with normalized geometry for arrows and outlines.
- Extend the semantic and physical models only with facts required by those two shape types.
- Emit arrows, outlines, tables, and colored text as editable native ODF objects.
- Preserve the supported subset during ODP import and Djot emission.
- Migrate affected Genetics sources and verify all 15 decks through the normal build path.
- Update syntax, architecture, decisions, human guidance, and changelog documentation as contracts
  become settled.

## Non-goals

- Build a general vector drawing language.
- Add arbitrary paths, freeform polygons, rotation, motion paths, timing tracks, or animation
  choreography.
- Add arbitrary hexadecimal colors, per-object style bags, or author-controlled font files.
- Add author-facing table widths, cell fills, merged-cell syntax, or spreadsheet behavior without a
  demonstrated source slide that needs them.
- Reproduce legacy slides by pixel comparison or by flattening text and shapes into images.
- Split one authored slide into multiple output slides to make a table fit.
- Replace the repository XML stack beyond the bounded readers and probes touched by this work.

## Current state summary

| Area | Existing support | Observed gap |
| --- | --- | --- |
| Text color | [layout_content.py](../../../slide_lib/layout_content.py) stores a resolved foreground on every `RunStyle`; [odp_text.py](../../../slide_lib/odp_text.py) writes it as native ODF text color. | [djot_blocks.py](../../../slide_lib/djot_blocks.py) parses one-line attributes, but [layout_validation.py](../../../slide_lib/layout_validation.py) rejects every attributed block because no presentation mapping exists. Inline nodes do not yet carry attributes. |
| Image geometry | The physical picture model stores both allocation and aspect-preserving displayed rectangles. | Source has no small overlay record tied to the displayed image rectangle. |
| Native shapes | [layout_content.py](../../../slide_lib/layout_content.py) and [odp_export.py](../../../slide_lib/odp_export.py) support rectangles, rounded rectangles, lines, and stars. | Shape fills are always solid, lines have no arrow marker, and line geometry assumes a top-left to bottom-right direction. |
| Overlay import | The importer already extracts positioned visual facts and identifies some image/text overlay relationships. | It does not emit an authored arrow or outline contract. `blue overlay` remains a deferred action in [djot_grammar.py](../../../slide_lib/djot_grammar.py). |
| Tables | Djot tables remain native `draw:frame` plus `table:table` content with explicit physical column widths and row heights. | `TABLE_BODY` falls back to the dark foreground color as its background. The measurement pass computes content-dependent row heights, while `table_object()` serializes equal-height rows. |

The Genetics source currently contains 21 table blocks, including a headerless 8-by-4 restriction
site table, repeated short 2- and 3-column blood/HLA tables, and dense 9-by-4 assay tables. These are
the acceptance corpus; a synthetic exhaustive matrix would add little value.

## Architecture boundaries and ownership

Source syntax and native semantics stay separate from physical geometry and ODF serialization.
Import support maps only objects that the source and exporter can preserve.

### Mapping (milestones / workstreams -> components / patches)

| Milestone / Workstream | Component | Review boundary |
| --- | --- | --- |
| M1 / WS-E | Corpus evidence and native ODF reference probes | One report settles the smallest required vocabularies and ODF forms before implementation. |
| M2 / WS-T | [layout_measurement.py](../../../slide_lib/layout_measurement.py), [layout_object_builders.py](../../../slide_lib/layout_object_builders.py), and [odp_text.py](../../../slide_lib/odp_text.py) | One table patch owns palette, row sizing, and any evidence-triggered column allocation. |
| M3 / WS-C | [djot_blocks.py](../../../slide_lib/djot_blocks.py), [djot_inline.py](../../../slide_lib/djot_inline.py), [native_model.py](../../../slide_lib/native_model.py), and text projection | One color patch owns source scope, semantic roles, diagnostics, and run projection. |
| M4 / WS-O | Djot grammar, semantic overlay records, physical line/shape geometry, layout compilation, and ODF shape export | One overlay contract precedes native serialization and import support. |
| M5 / WS-I | [slide_lib/importers/](../../../slide_lib/importers), Genetics Djot sources, full build, and documentation | Import and corpus changes consume settled contracts; validation reviews the integrated artifacts. |

Shared production fixtures remain owned by their implementing work package. Temporary comparison
files live under `/private/tmp` or an ignored `output_*` directory and stay out of Git.

## Milestone plan

| M | Title | Summary | Goal |
| --- | --- | --- | --- |
| M1 | Settle bounded contracts | Inventory real source needs and test native ODF behavior. | Approve the smallest syntax, model, and serialization forms needed for implementation. |
| M2 | Repair tables | Correct body styling and unify measurement with serialized geometry. | Produce readable native tables with no silently clipped cells. |
| M3 | Add semantic text colors | Map a closed source vocabulary into resolved native text runs. | Restore meaningful font colors without a generic style system. |
| M4 | Add native image overlays | Author, compile, and serialize arrows and outlines over contained images. | Preserve editable annotations at the correct visual coordinates. |
| M5 | Preserve and integrate | Extend bounded import, migrate affected sources, and validate all Genetics decks. | Close the three fidelity gaps through the normal user-visible build path. |

### Milestone: M1 settle bounded contracts

- Depends on: none.
- Deliverables: `docs/active_plans/reports/native_fidelity_baseline.md` and a recorded decision for
  each conditional implementation choice.
- Workstreams: WS-E with WP-E1 and WP-E2.
- Entry criteria: current original ODP/PDF evidence and canonical Djot sources are available.
- Exit criteria: each planned color role and overlay type has real corpus evidence; ODF arrow,
  no-fill outline, and table row-height forms survive the selected LibreOffice round trip.
- Parallel-plan ready: yes. WP-E1 and WP-E2 use separate read-only evidence and temporary files.

### Milestone: M2 repair tables

- Depends on: WP-E1 for representative tables and WP-E2 for row-height behavior.
- Deliverables: corrected native palette, one authoritative row-sizing calculation, and conditional
  content-aware column allocation.
- Workstreams: WS-T with WP-T1 followed by WP-T2 when its trigger is met.
- Entry criteria: M1 table specimens and native row-height decision are recorded.
- Exit criteria: all corpus tables use readable body colors and no cell is silently clipped.
- Parallel-plan ready: no. WP-T2 evaluates WP-T1 output and touches the same measurement path.

### Milestone: M3 add semantic text colors

- Depends on: WP-E1 for required roles and source scope.
- Deliverables: source grammar, semantic role mapping, run projection, diagnostics, and focused
  stable tests.
- Workstreams: WS-C with WP-C1 followed by WP-C2.
- Entry criteria: M1 identifies block-level and mixed-run color examples.
- Exit criteria: approved color attributes compile to native editable ODF text runs and unsupported
  names fail at their source location.
- Parallel-plan ready: no. Projection depends on the source and semantic contract.

### Milestone: M4 add native image overlays

- Depends on: WP-E1 for overlay examples and WP-E2 for native ODF shape forms.
- Deliverables: source grammar, semantic geometry, displayed-image coordinate mapping, ODF export,
  and reveal reuse where the original slide uses an appearance build.
- Workstreams: WS-O with WP-O1, WP-O2, and WP-O3 in dependency order.
- Entry criteria: M1 settles the syntax and native form.
- Exit criteria: an arrow and an outline remain editable, aligned to the image, and correctly
  layered after ODP generation and LibreOffice open/save.
- Parallel-plan ready: no. The physical model and serializer depend on the approved source model.

### Milestone: M5 preserve and integrate

- Depends on: WP-T1, the WP-T2 decision, WP-C2, and WP-O3.
- Deliverables: bounded import preservation, migrated source slides, complete ODP/PDF rebuild,
  acceptance report, and closed documentation.
- Workstreams: WS-I with WP-I1, WP-I2, and WP-I3.
- Entry criteria: all three production contracts pass their focused gates.
- Exit criteria: every affected source uses the new contracts, the full build passes, and visual and
  semantic audits record no unresolved fidelity regression in scope.
- Parallel-plan ready: no. Import mapping consumes the final contracts, source migration consumes
  importer output, and full validation consumes the migrated corpus.

## Workstream breakdown

### Workstream: WS-E evidence and contracts

- Goal: turn visible gaps into a small set of source and native requirements.
- Owner: architecture owner.
- Work packages: WP-E1 and WP-E2.
- Needs: original editable decks, canonical Djot sources, generated ODP/PDF output, and LibreOffice.
- Provides: approved vocabularies, specimens, and ODF serialization choices.
- Review boundary, when modifying the repository: one evidence report; no production code.

### Workstream: WS-T native tables

- Goal: make existing Djot tables readable and fully visible as native ODF tables.
- Owner: table implementation owner.
- Work packages: WP-T1 and conditional WP-T2.
- Needs: M1 specimens and native row-height evidence.
- Provides: measured column widths, measured row heights, cell content, and semantic table styles to
  the existing ODF serializer.
- Review boundary, when modifying the repository: one table-focused patch and focused contract tests.

### Workstream: WS-C semantic text colors

- Goal: preserve the small set of meaningful lecture text colors.
- Owner: source-language implementation owner.
- Work packages: WP-C1 and WP-C2.
- Needs: M1 color-role inventory and strict-Djot validation.
- Provides: named semantic color facts resolved to physical run colors.
- Review boundary, when modifying the repository: one grammar/model patch followed by one projection
  and importer patch if review separation helps.

### Workstream: WS-O image overlays

- Goal: retain editable arrows and outlines over focal images.
- Owner: native-shape implementation owner.
- Work packages: WP-O1, WP-O2, and WP-O3.
- Needs: M1 syntax and ODF decisions plus the existing displayed image rectangle.
- Provides: validated normalized overlay facts and native ODF shapes.
- Review boundary, when modifying the repository: source/model contract first, then native export.

### Workstream: WS-I import and integration

- Goal: apply the new contracts to real sources and prove the full native delivery path.
- Owner: integration owner.
- Work packages: WP-I1, WP-I2, and WP-I3.
- Needs: all production contracts and representative original decks.
- Provides: migrated Djot, rebuilt artifacts, acceptance evidence, and closed documentation.
- Review boundary, when modifying the repository: importer, corpus, and validation/docs remain
  separately reviewable patches.

## Work packages

### Work package: WP-E1 inventory fidelity specimens

- Owner: architecture owner.
- Touch points: original lecture ODP/PDF pairs, Genetics Djot, current ODP/PDF output, and
  `docs/active_plans/reports/native_fidelity_baseline.md`.
- Depends on: none.
- Acceptance criteria:
  - Record every distinct semantic text-color use as block-wide, existing emphasized/link content,
    or a plain mixed-run span.
  - Record each needed image overlay as arrow or outline, static or revealed, with its owning image.
  - Select representative short, dense numeric, and long-text tables from the 21-table corpus.
  - Remove a proposed role or object type when no actual slide needs it.
- Evidence or review, when useful: side-by-side original and generated page images plus native source
  object inspection. Pixel equivalence is not a criterion.
- Obvious follow-ons: provide the exact source examples to WP-T1, WP-C1, and WP-O1.

### Work package: WP-E2 probe native ODF behavior

- Owner: native ODF evidence owner.
- Touch points: temporary ODPs in `/private/tmp`, LibreOffice open/save, and the M1 report.
- Depends on: none.
- Acceptance criteria:
  - Identify the smallest ODF form for a one-ended arrow that LibreOffice retains as an editable
    native object.
  - Confirm that an unfilled rectangle retains its stroke and transparent interior.
  - Compare exact row heights with LibreOffice optimal-row-height behavior on wrapped cell text.
  - Parse probe packages with narrowly configured `lxml`: DTD loading off, entity resolution off,
    and network access off.
- Evidence or review, when useful: before/after package XML and one rendered reference page.
- Obvious follow-ons: choose `draw:line` plus a native marker when it survives; otherwise choose the
  simplest LibreOffice-native arrow shape that remains editable. Choose exact measured row heights
  unless optimal height is demonstrably stable through the normal build and open/save path.

### Work package: WP-T1 unify table styling and row sizing

- Owner: table implementation owner.
- Touch points: [layout_measurement.py](../../../slide_lib/layout_measurement.py),
  [layout_object_builders.py](../../../slide_lib/layout_object_builders.py),
  [layout_content.py](../../../slide_lib/layout_content.py), [odp_text.py](../../../slide_lib/odp_text.py),
  and focused table tests.
- Depends on: WP-E1 and WP-E2.
- Acceptance criteria:
  - Resolve table-body fill to a light surface with dark text; retain theme accent headers with white
    text and a readable semantic border.
  - Use one row-measurement helper for font-size selection and final `TableContent.row_heights`.
  - Serialize every row at or above its measured content need at the selected font size.
  - Keep tables as native editable ODF tables.
  - Report a source-located table capacity concern when the content cannot fit; never conceal it by
    clipping or by splitting the slide.
- Evidence or review, when useful: focused unit tests for palette semantics and the row-height
  invariant; temporary renders for representative tables.
- Obvious follow-ons: run the WP-T2 comparison using WP-T1 output.

### Work package: WP-T2 decide and implement column allocation

- Owner: table implementation owner.
- Touch points: table measurement and object construction only.
- Depends on: WP-T1.
- Acceptance criteria:
  - Compare equal-width columns on the short, numeric, and long-text specimens.
  - Keep equal widths when the repaired tables wrap and fit well.
  - When equal widths cause avoidable wrapping or a lower selected font size, allocate each column a
    measured minimum for its widest unbreakable token and a measured preferred width for its
    single-line content, then distribute available width between those bounds.
  - Keep the total column width equal to the table frame width and keep every cell's measurement
    width identical to its serialized column width.
- Evidence or review, when useful: temporary comparison renders. Add one permanent behavioral test
  only if the content-aware allocator is implemented: a wider-content column receives more room
  while total width is preserved.
- Obvious follow-ons: give final table geometry to WP-I3 capacity and visual checks.

### Work package: WP-C1 define semantic color scope

- Owner: source-language implementation owner.
- Touch points: [djot_blocks.py](../../../slide_lib/djot_blocks.py),
  [djot_inline.py](../../../slide_lib/djot_inline.py), [native_model.py](../../../slide_lib/native_model.py),
  and [DJOT_SLIDE_SYNTAX.md](../../DJOT_SLIDE_SYNTAX.md).
- Depends on: WP-E1.
- Acceptance criteria:
  - Reuse `{color=<role>}` on the next block or list item for block-wide color.
  - Use a strict-Djot inline span with the same attribute only when WP-E1 finds a needed plain
    mixed-run example that cannot attach to existing emphasis, strong, or link content.
  - Start with the corpus-supported subset of `accent`, `warning`, and `muted`; remove unused roles.
  - Resolve `accent` through the selected deck color theme and keep `warning` and `muted` readable
    against their actual slide backgrounds.
  - Reject duplicates, unknown roles, and unsupported element scopes at the source location.
- Evidence or review, when useful: pinned strict-Djot validation of every accepted source form and
  focused parser behavior tests.
- Obvious follow-ons: pass semantic roles, rather than raw color strings, to WP-C2.

### Work package: WP-C2 project and preserve text colors

- Owner: text projection owner.
- Touch points: native-to-layout text projection, presentation theme resolution, ODF text export,
  relevant importer text-run mapping, and focused tests.
- Depends on: WP-C1.
- Acceptance criteria:
  - Resolve each accepted semantic role once before constructing `RunStyle`.
  - Preserve strong, emphasis, links, inline code, and line breaks inside a colored span.
  - Emit normal editable ODF text spans with explicit foreground colors.
  - Map recognized legacy run colors to semantic roles during bounded import; report an unrecognized
    meaningful color for review instead of writing arbitrary hexadecimal source values.
- Evidence or review, when useful: permanent tests for nested style composition and source-located
  invalid-role errors; temporary ODP/PDF package and font inspection.
- Obvious follow-ons: migrate the WP-E1 color specimens in WP-I2.

### Work package: WP-O1 define image-overlay source and semantic model

- Owner: source-language and model owner.
- Touch points: Djot grammar/parser, layout registry, native semantic model, syntax guide, and focused
  parser tests.
- Depends on: WP-E1 and WP-E2.
- Acceptance criteria:
  - Allow optional overlay records directly after the single component image in `@image`.
  - Accept only `arrow` and `outline` records in the first version.
  - Express arrow endpoints and outline bounds as percentages of the displayed image rectangle.
  - Default shapes to the deck accent; add an optional named role only when WP-E1 proves a second
    color is needed.
  - Retain source location, reveal intent, and enough description to preserve accessible meaning.
  - Reject missing images, multiple images, out-of-bounds geometry, unsupported shape names, and
    malformed records at their source locations.
- Evidence or review, when useful: compare a dedicated `@overlay` slot with the deferred target-text
  `<= blue overlay` form. Use the dedicated geometry records when arrows or outlines point to image
  regions without a unique text target. A candidate record surface for the strict-Djot experiment is:

  ```djot
  @overlay

  arrow: 18 30 62 30
  outline: 42 35 18 12
  ```

- Obvious follow-ons: remove or redefine the deferred `blue overlay` action so only one overlay
  contract remains documented.

### Work package: WP-O2 add physical overlay geometry

- Owner: layout implementation owner.
- Touch points: physical content/primitives, image layout builders, overlay layout builder, object
  layering, and focused geometry tests.
- Depends on: WP-O1.
- Acceptance criteria:
  - Transform normalized coordinates through the picture's `displayed_rectangle`, including
    letterboxing created by aspect-preserving contain placement.
  - Represent explicit line endpoints so arrows can point left, right, up, or down.
  - Represent an outline with no fill and a native stroke.
  - Layer the image first, overlays next, and caption or ordinary reading-order text according to the
    selected layout contract.
  - Reuse the existing object-level appearance reveal for an authored revealed overlay.
- Evidence or review, when useful: permanent tests for displayed-image coordinate mapping and
  direction-preserving endpoints. Keep placement screenshots temporary.
- Obvious follow-ons: provide fully resolved physical objects to WP-O3.

### Work package: WP-O3 serialize native arrows and outlines

- Owner: native ODF implementation owner.
- Touch points: [odp_export.py](../../../slide_lib/odp_export.py), ODF style/marker definitions,
  accessibility metadata, and focused export tests.
- Depends on: WP-O2 and the WP-E2 ODF decision.
- Acceptance criteria:
  - Emit each arrow and outline as the selected editable native ODF object.
  - Emit no-fill outlines without covering the image below.
  - Preserve stroke color, arrow direction, z-order, source identity, and object-level reveal intent.
  - Retain the same editable object type after LibreOffice open/save.
- Evidence or review, when useful: one structural contract test per stable native object behavior;
  temporary open/save and render evidence for LibreOffice behavior.
- Obvious follow-ons: expose the settled object subset to bounded import in WP-I1.

### Work package: WP-I1 preserve supported legacy facts

- Owner: importer implementation owner.
- Touch points: [slide_lib/importers/](../../../slide_lib/importers), Djot emission, review diagnostics,
  and focused importer tests.
- Depends on: WP-C2 and WP-O3.
- Acceptance criteria:
  - Map a supported source arrow or unfilled rectangle to normalized coordinates only when it belongs
    unambiguously to one component image.
  - Map recognized text-run colors to the approved semantic roles.
  - Preserve static versus revealed overlay intent when source evidence is explicit.
  - Route unsupported shapes, ambiguous image ownership, or unknown meaningful colors to the existing
    review path with source object evidence.
- Evidence or review, when useful: compact importer tests using inline temporary package facts;
  one-time import comparison against the WP-E1 originals.
- Obvious follow-ons: emit source for affected slides and hand it to WP-I2 for human-readable review.

### Work package: WP-I2 migrate affected Genetics sources

- Owner: corpus migration owner.
- Touch points: affected files under the lecture-organized `genetics/LECT##/djot/` directories and
  their existing local component images.
- Depends on: WP-T1, the WP-T2 decision, WP-C2, and WP-I1.
- Acceptance criteria:
  - Apply semantic colors only where the original use carries teaching meaning.
  - Restore the surveyed arrows and outlines with native overlay records.
  - Keep every source slide one-to-one with its output slide and preserve every image's aspect ratio.
  - Keep source concise and avoid per-slide geometry outside the dedicated overlay records.
- Evidence or review, when useful: source review plus representative original/generated page pairs.
- Obvious follow-ons: run the full acceptance path in WP-I3.

### Work package: WP-I3 validate and close

- Owner: integration and review owner.
- Touch points: tests, normal Genetics build, ODP/PDF artifacts, capacity report, acceptance report,
  and repository documentation.
- Depends on: WP-I2.
- Acceptance criteria:
  - Run focused tests during each patch and the full permanent pytest suite once after integration.
  - Lint all 15 Genetics sources and build all 15 through the user-visible ODP/PDF path.
  - Inspect ODP packages for native text spans, native tables, native arrows, and native outlines.
  - Confirm that all font characters remain glyphs and that annotation stars/arrows/outlines remain
    vector objects; the PDF font audit reports no Type 3 glyphs.
  - Review representative table, color, and overlay pages against the originals for meaning,
    legibility, alignment, and absence of clipping.
  - Run capacity inspection and resolve every new table diagnostic or record a source-specific
    correction action.
- Evidence or review, when useful: an independent read-only review of the completed diff and visual
  acceptance report before closure.
- Obvious follow-ons: archive this plan after all closure checks pass.

## Acceptance criteria and gates

- Per-patch gate: focused stable tests pass, source diagnostics identify invalid input at the author
  location, and `git diff --check` reports no whitespace errors. Failure returns the patch to its
  owner with the failing contract and smallest reproducer.
- Strict-Djot gate: every new authored form passes the pinned strict-Djot validation lane before the
  presentation parser applies its meaning. Failure revises the source spelling; it does not waive
  Djot compatibility. When the pinned executable is unavailable, record the lane as pending rather
  than claiming acceptance.
- Table gate: body cells use a light readable fill and every serialized row has enough measured
  height for its cell content. Failure compares measurement width, padding, and serialized geometry;
  it does not add a clipping tolerance.
- Overlay gate: native arrows and outlines keep their positions relative to the displayed image
  after ODP generation and LibreOffice open/save. Failure first checks image-coordinate mapping,
  then switches to the alternative native ODF form selected by WP-E2 if LibreOffice changed the
  object.
- Font gate: every authored character remains native text in ODP and a real font glyph in PDF.
  Failure identifies the exact source character and rendering stage, then replaces only a truly
  decorative symbol with a native shape or adds the required embeddable font glyph.
- Integration gate: all 15 Genetics decks lint and build through `./build_slides.sh genetics` with
  matching source/output page counts. Failure fixes the responsible source or production contract
  before publication.
- Independent review gate: a reviewer checks editability, source simplicity, failure diagnostics,
  and visual evidence. A finding blocks closure only when it identifies a current requirement,
  known failure mode, or stable contract.

## Test and verification strategy

Permanent pytest protects only behavior intended to remain stable:

- Semantic color roles compose with existing inline styles and reject invalid source at its
  location.
- Overlay coordinates map through the displayed image rectangle and preserve arrow direction.
- ODF export uses native arrow/outline objects with correct fill and marker semantics.
- Table body/header palette semantics remain readable and measured row height reaches serialization.
- A content-aware width test exists only when WP-T2 adopts that algorithm.

Temporary and one-time checks supply implementation evidence without expanding the permanent suite:

- Original/generated page comparisons for the representative corpus.
- LibreOffice-native ODF experiments and open/save inspection.
- Full 21-table render review and all-theme color sampling.
- ODP package object counts, full Genetics rebuild, capacity scan, PDF font audit, and page renders.

Run Python commands only through the repository environment:

```bash
source source_me.sh && python3 -m pytest tests/
source source_me.sh && python3 deck_tools.py lint genetics
source source_me.sh && python3 deck_tools.py capacity genetics
./build_slides.sh genetics
git diff --check
```

Use the actual CLI spellings present when implementation begins. Do not create a test solely to pin
a command spelling that the product does not promise.

## Migration and compatibility policy

- Djot remains the sole canonical source after one-time import.
- New color and overlay records must remain valid strict Djot before extension semantics apply.
- Imported arbitrary colors and drawing objects remain review items until they match the closed
  supported vocabulary.
- Existing decks without color or overlay attributes retain their current appearance.
- Existing Djot table source remains unchanged unless a specific table needs an editorial correction
  after the geometry repair.
- The pre-production codebase replaces obsolete deferred-overlay behavior directly; it carries no
  compatibility alias for an unshipped syntax.

## Risk register

| Risk | Impact | Trigger | Owner | Mitigation |
| --- | --- | --- | --- | --- |
| The color surface grows into arbitrary styling. | Authors gain inconsistent deck-local palettes and extra syntax. | A patch accepts raw hexadecimal values or unused roles. | Source-language owner | Keep only corpus-backed semantic roles and resolve them through the deck theme. |
| Inline color syntax conflicts with strict Djot. | Canonical source fails its required compatibility lane. | The pinned validator rejects the proposed span. | Architecture owner | Use an accepted Djot inline element with attributes, or limit the first version to block/existing-inline scope and record the uncovered slide. |
| Overlays drift when an image is letterboxed. | Arrows and outlines point at the wrong content. | Geometry is based on the slot allocation rather than the displayed image. | Layout owner | Transform percentages through `PicturePlacement.displayed_rectangle` and test non-matching aspect ratios. |
| LibreOffice rewrites arrow markers or row heights. | Native objects move or change after normal editing. | WP-E2 or integration open/save changes object semantics. | Native ODF owner | Select the simplest preserved native form from the reference probe and serialize that form consistently. |
| Table width logic becomes a layout optimizer. | Complexity grows while real tables remain difficult to reason about. | WP-T2 adds scoring, author knobs, or corpus-specific cases. | Table owner | Keep equal widths when adequate; otherwise use the one minimum/preferred allocator and report true capacity failures. |
| Visual tests become brittle. | Routine typography tuning breaks unrelated permanent tests. | Tests assert pixels, exact coordinates, or full-corpus snapshots. | Review owner | Keep visual comparisons temporary and retain only semantic or behavioral contracts in pytest. |
| Import scope exceeds the supported output model. | Import creates source that the builder cannot faithfully emit. | An importer patch accepts extra shape types or arbitrary colors. | Importer owner | Admit only the settled color roles, arrow, and outline contracts; route everything else to review. |

## Rollout and release checklist

- [x] Publish the M1 corpus and native ODF evidence report.
- [x] Approve the exact text-color roles and scopes.
- [x] Approve the exact overlay record spelling and native ODF forms.
- [x] Land and review the table repair before assessing column allocation.
- [x] Land and review semantic text colors.
- [x] Land and review native image overlays.
- [x] Extend bounded import for the settled subset.
- [x] Migrate the affected Genetics sources; the survey found no legacy arrow or outline that met
  the one-image ownership contract, so those ambiguous drawings remain review evidence.
- [x] Pass focused tests and the full permanent suite.
- [x] Lint, inspect capacity, and build all 15 Genetics decks.
- [x] Complete LibreOffice PDF generation, native-object inspection, and font audit.
- [x] Complete representative visual review and record the legacy-arrow ownership finding.
- [x] Update durable documentation.
- [ ] Run the optional pinned strict-Jotdown lane when its executable is installed, then archive
  this plan.

## Documentation close-out requirements

- Active plan / progress tracker: update this file's status and checklist after each completed patch.
- Syntax: update [DJOT_SLIDE_SYNTAX.md](../../DJOT_SLIDE_SYNTAX.md) only after color and overlay
  grammar pass their M1 decisions and implementation gates.
- Architecture: update [CODE_ARCHITECTURE.md](../../CODE_ARCHITECTURE.md) and
  [FILE_STRUCTURE.md](../../FILE_STRUCTURE.md) only where responsibilities or files actually change.
- Human guidance: retain the stated priorities in [HUMAN_GUIDANCE.md](../../HUMAN_GUIDANCE.md).
- Design decisions: add settled color, overlay, and table contracts to
  [DESIGN_DECISIONS.md](../../DESIGN_DECISIONS.md) during close-out, respecting its source-file line
  limit through the repository's normal rotation or consolidation process.
- `docs/CHANGELOG.md` entry: record each shipped behavior and its real verification evidence.
- Acceptance report: record representative source pages, generated pages, native object evidence,
  remaining capacity diagnostics, and any attended check still pending.
- Archive / closure notes: move the completed plan to `docs/archive/` with `git mv` after all gates
  pass and no implementation task remains.

## Patch plan and reporting format

- Patch 1 - M1 evidence: report corpus specimens and selected native ODF forms.
- Patch 2 - WP-T1/WP-T2: repair table palette and sizing; include the conditional width decision.
- Patch 3 - WP-C1/WP-C2: add semantic font colors and bounded import preservation.
- Patch 4 - WP-O1/WP-O2: add overlay source/model and physical displayed-image geometry.
- Patch 5 - WP-O3/WP-I1: add native ODF serialization and bounded overlay import.
- Patch 6 - WP-I2: migrate affected Genetics source slides.
- Patch 7 - WP-I3: integrate, validate, document, and close.

Each patch report states the work-package IDs, files changed, user-visible outcome, focused evidence,
temporary evidence removed, permanent tests added or deliberately omitted, and remaining risks.

## Open questions and decisions needed

- Settled: plain attributed spans are required for mixed-color HLA haplotypes.
- Settled: dedicated image-relative geometry records replace the deferred target-text action.
- Settled: compiler-measured exact table row heights are serialized; optimal-height rewriting is
  disabled.
- Non-blocking follow-up: consider another overlay shape, author color role, or table control only
  after a real slide remains unrepresentable following this plan.
