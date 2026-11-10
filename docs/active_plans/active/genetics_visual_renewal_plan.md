# Plan: Renew genetics illustrations with original SVG artwork

## Context

Status: reviewed creative direction in execution on 2026-11-09. The reassessment hold is
released for the bounded original-art batch under existing implementation authorization. Guide,
construction helpers and ABO/bottleneck artwork are accepted. The eight-page contextual proof
passes independent review, and the four drawings plus six reviewed source-line removals are
integrated. Canonical ABO/drift full-root exports and final batch checks pass. The next four
drawings (chromosome complements, folded hemoglobin, CCR5 and corn) and their ten-page
original-voice proof are accepted; art-only integration, canonical full-root exports and fresh
final checks are complete. Remaining art families and whole-course delivery stay open. The
[progress ledger](../reports/genetics_visual_renewal_progress.md) owns current status and
[workstream index](../workstreams/genetics_visual_workstreams.md) owns dispatchable next tasks.
All delegated agents use `gpt-6-astra`, as explicitly requested.

The latest overall goal covers original high-quality SVG replacements across all production
lecture slides while preserving voice and content without lesson redesign. This Genetics plan
remains the current workstream; `remaining_lecture_art_survey` surveys Biotechnology,
Biostatistics and shared lecture art. Finishing Genetics alone will not complete that goal.

The intended result is ambitious, original scientific artwork throughout Genetics. Existing
rasters establish scientific facts, course examples and teaching purpose; they are visual
references, not templates to trace or reproduce pixel for pixel. Artists can change composition,
perspective, form and visual explanation while preserving the instructional substance.

The latest instructor clarification makes drawing/clipart replacement for rasterized images
the task. Preserve slide voice, titles, native prose, examples, layouts and sequence. Source
checks establish only what is needed to draw accurately; global scientific correction and
prose revision are outside this work. Focus on consequential drawing and delivery issues.
Prioritize potential visual improvement balanced against creation difficulty: achievable
high-impact replacements before complex work, regardless of `@replaceme` status.

The existing effort includes useful original art. Earlier implementation also expanded into
native-content migration, followed by scope cleanup and a serializer refactor. The instructor
clarified that the pixel-equivalence evidence raised concern, not that all artwork was poor.
That evidence belongs to maintenance; it does not establish or constrain creative success. The [reassessment](../reports/genetics_illustration_reassessment.md)
separates useful work from artwork to refine or redesign. M1's 1,782 image uses across 82 roots
and 1,226 unique asset paths remain accounted for; these are inventory counts, not art quotas.

## Objectives

- Create recognizable, expressive, scientifically useful original SVG illustrations that improve
  how students see organisms, objects, apparatus and biological relationships.
- Establish a coherent visual language through representative equipment, organism and scientific
  diagram examples before dispatching hundreds of drawings.
- Develop a small, useful construction toolkit from demonstrated drawing needs and book-informed
  experiments, including geometric volume where it improves recognition or explanation.
- Preserve course objectives, examples, facts, data, question states and staged disclosure while
  allowing new artistic compositions and visual explanations.
- Integrate finished artwork with minimal source changes and inspect actual ODP/PDF delivery.

## Design philosophy

Apply **Dream big**, **Use the scientific method** and **Keep it simple (KISS)** from
[REPO_STYLE.md](../../REPO_STYLE.md). Creative ambition belongs in the artwork; software remains
small and understandable. A modest implementation can support an excellent illustration.

Investigate drawing references and simulated 3D construction before choosing toolkit features.
Use boxes, cylinders, spheres, ellipses, cut forms, organic paths, shading or flat diagrams where
they help the specific subject. Consistency means related visual decisions, not forcing every
figure through one technique. Two illustrative alternatives are useful when an artistic choice
is uncertain; they are not a required exercise for every asset.

The existing `text()`, `line()` and `write_svg()` helpers are a maintenance foundation. Limiting
the toolkit to those three functions was a manager choice, not the user's requirement. Shared
construction functions must earn their place in real artwork; keep one-off geometry local.

## Scope

- Renew suitable clipart, organisms, apparatus, molecular/chromosome structures, mechanisms,
  schematic gels, pedigrees and supported scientific figures across the five active groups.
- Evaluate existing candidates visually: keep strong work, refine promising work and redesign
  weak constructions or compositions instead of treating every valid SVG as finished.
- Develop a provisional illustrated guide covering palette and semantic color, linework,
  lighting/depth, proportions/detail, labels and reusable parts from successful examples.
- Replace the graphic portion of mixed figures while retaining their existing data, prose,
  calculations and reveal requirements; retain a complete source composite when separation would
  require an independent content migration.
- Preserve original assets, empirical images, photographs, identities and source evidence.
- Integrate artwork through the necessary image references, preserving native prose, alt text,
  titles, examples, layouts and sequence; retain useful existing native tables/styles as resources.

## Non-goals

- Convert standalone tables, prose, formulas, alignments, calculations or worksheets to native Djot.
- Reorganize lessons, change datasets or undertake unrelated teaching-sequence redesign.
- Renew gene-tree/phylogeny content, including LECT12 teaching, great-ape trees and the M2 rotation
  pilot; retain the archive and future BPQ SVG export entry in [TODO.md](../../TODO.md).
- Trace source contours or require identical pixels, coordinates, layouts or decorative geometry.
- Build a general 3D engine, framework, configurable art platform or copied normalizer port.
- Discard excluded working code, original assets or useful experimental evidence.

## Current state summary

M1 coverage and source maps remain useful. Historical M2 evidence includes electrophoresis,
peas, cis/trans and deletion drawings; historical native-table work is not a new assignment.
Five source-group cleanup handoffs are complete. The narrowed specification review accepts
source reconciliation and archival preservation, not the creative-art/toolkit objective.
Gene-tree work is archived and excluded from this delivery.

The latest historical maintenance baseline is `5322 passed, 2 warnings in 28.66s` for
`source ./source_me.sh && pytest tests/`, with zero final-run mutations, all 118 Genetics Djot
files ASCII and all 376 inspected source SVGs parsing. This validates that checked state; it does
not accept the artwork or future edits. XML-safe normalization and the three serializer helpers
are retained. The small `project()`, `cuboid()` and `cylinder()` construction additions now
have accepted specification and quality reviews; their use is demonstrated in apparatus art.

The six-pair creative audit supports retaining/refining apparatus and pea work, refining the
nucleotide, and redesigning ABO comparison, bottleneck imagery and the Drosophila chromosome-complement comparison.
The equipment-construction experiment demonstrates useful cuboids and projected cylinders;
the organism trial favors organic anatomy for a large figure and compact forms for repeated
comparisons, while the crossover trial favors a flat three-stage explanation. A combined scratch
deck exports to seven ODP/PDF pages. Fresh review accepts these prototype examples: no clipping,
label or export defect was found, and the three-stage ancestry is coherent. One rear fly leg is
occluded, so the organism is suitable for phenotype illustration rather than six-leg counting.
The reviewed examples now support the accepted, explicitly provisional
[GENETICS_ILLUSTRATION_GUIDE.md](../../slide-specs/GENETICS_ILLUSTRATION_GUIDE.md). ABO and
bottleneck refinements pass standalone specification and quality reviews. Their eight-page
contextual ODP/PDF proof passes independent review and the bounded canonical integration is
complete. Canonical ABO/drift full-root exports and final batch checks pass; remaining
art families and whole-course exports stay open.
Chromosome context supports the accepted XX/XY redraw. Folded hemoglobin, CCR5 and corn also
pass artwork and contextual review. The authoritative ten-page proof is
`_temp/svg_family_renewal/export/exact_source/contextual_proof.{djot,odp,pdf}`.
The three CCR5 native-prose qualifications in the other scratch variant are cancelled after
the instructor's clarification and must not enter canonical sources. Current integration is
two existing SVG replacements, two new SVGs and exactly two image-URL substitutions;
the ledger records its completion and later export/check evidence separately.

Six yeast drawings and one mouse-selection comparison have passed independent art/context
review, canonical integration and full-root export review. Seven image URLs changed with native
content, layouts and markers preserved; the inherited mouse placement remains tiny. The DNA
polarity pure-text image is now an independently reviewed editable SVG quote card, with one URL
changed and the original PNG retained. Canonical quote and pedigree exports and the final
post-integration suite are complete; the ledger records their evidence and display limits. Defer complex inversion work until tractable higher-payoff work.

## Architecture boundaries and ownership

### Mapping (milestones -> components)

| Milestone | Component | Review boundary |
| --- | --- | --- |
| M1-M2 | Inventory and historical pilots | Preserve evidence without carrying old acceptance forward. |
| M3 | Reference research and representative art | Demonstrated improvements in equipment, organism and diagram. |
| M4 | Provisional visual language and useful parts | Consistency across the examples; code justified by actual use. |
| M5 | Focused art batches | Original visual explanation plus preserved science and teaching purpose. |
| M6 | Course integration and delivery | Changed consumers rendered, inspected and checked. |

### File scope

| File or directory | Intended change | Canonical source or evidence |
| --- | --- | --- |
| `docs/active_plans/active/genetics_visual_renewal_plan.md`, existing ledger and workstream briefs | Correct authority, record progress and dispatch next work. | Current instructor direction and linked evidence. |
| `docs/active_plans/reports/genetics_illustration_reassessment.md` | One durable account of divergence, findings and reviewed direction. | Six-pair audit and representative experiments. |
| `_temp/svg_creative_reassessment/`, `_temp/svg_construction_primitives/` and related style trials | Source comparisons, trial SVGs, generators and preview/export evidence. | Local scratch evidence; canonical changes require the bounded batch integration outcome. |
| [GENETICS_ILLUSTRATION_GUIDE.md](../../slide-specs/GENETICS_ILLUSTRATION_GUIDE.md) | Accepted provisional visual language with three durable examples. | M3 examples and existing color/pedagogy guidance; remains provisional. |
| `svg_tools/drawing.py` and existing SVG tooling | Add only demonstrated useful construction operations after experiments. | Small standard-library code; retain existing serializer behavior. |
| `genetics/` and specifically owned shared assets/sources | Finished editable SVG and minimal references/labels/layout integration after release. | SVG or its simple authoring script; original raster remains evidence. |
| Normal build output directories | Fresh ODP/PDF for changed and restored consumers. | Canonical Djot and final SVG bytes. |
| Existing focused tests, if shared logic changes | Protect important construction/serialization behavior with plausible regression risk. | No permanent per-artwork or pixel-style tests. |

One owner edits each physical source or shared part; a shared asset lists its consumers. Keep SVG
self-contained with editable geometry, live short labels and title/description. Impress embeds
it as an image; the SVG remains the editable artwork source. Dependencies and runtime configuration
have no planned changes. Existing classifications remain intact; no classification churn is needed
for this bounded execution.

## Milestone plan

| M | Title | Summary | Goal |
| --- | --- | --- | --- |
| M1 | Preserve inventory | Keep original uses and current exclusions accounted for. | Reliable source context. |
| M2 | Retain historical evidence | Preserve useful pilots, cleanup and archived work. | Reuse value without false acceptance. |
| M3 | Investigate and demonstrate | Read relevant drawing references and make representative art experiments. | Show a stronger creative direction. |
| M4 | Establish a visual language | Derive an illustrated guide and useful construction parts from the examples. | Coherent artwork before scale. |
| M5 | Renew focused art batches | Refine or redesign candidates with source-grounded artistic freedom. | Substantial original art across Genetics. |
| M6 | Integrate and deliver | Place final drawings, export consumers and inspect actual slides. | Reliable classroom artifacts. |

### Milestone: Preserve inventory and historical evidence

- Covers M1 and M2; depends on existing inventory, source maps, pilots and preservation archives.
- Entry criteria: existing evidence is available; these historical milestones are not restarted.
- Deliverables: retained classification links, archive receipt and accurate maintenance status in
  the ledger. Preserve explicitly authorized D1 corrections; do not expand correction scope.
- Exit criteria: completed cleanup is distinguishable from creative acceptance and future work.
- Parallel-plan ready: no new inventory campaign is needed.

### Milestone: Investigate and demonstrate

- M3 investigation and representative review are complete; results inform the bounded batch.
- Entry criteria: equipment, organism and diagram examples have explicit teaching purposes and
  source facts. Inspect the relevant local drawing books before selecting construction methods.
- Deliverables: source/current/proposed views, editable trial art and rendered previews for each
  representative family; brief findings recorded in the existing ledger/reassessment.
  Compare a second composition only where it resolves a real uncertainty.
- Exit criteria: examples visibly improve recognition, hierarchy or explanation; reviewers can
  identify the improvement and any remaining defect. Facts, labels and question states survive.
  A disappointing trial is revised or replaced, not promoted because it parses.
- Parallel-plan ready: yes; equipment, organism and diagram trials have separate scratch ownership.

### Milestone: Establish a visual language

- M4 depends on reviewed M3 examples; broad drawing dispatch waits for this shared reference.
- Entry criteria: representative art offers successful choices to reuse and limitations to avoid.
- Deliverables: `GENETICS_ILLUSTRATION_GUIDE.md`, explicitly provisional, with example images and
  concise choices for semantic color/palette, line weights, depth/light, organic and geometric
  proportions, detail at slide size, labels and reusable parts. Reuse the existing palette and
  teaching color relationships. Implement only construction helpers demonstrated useful in M3.
- Exit criteria: equipment, organism and diagram look related while retaining their appropriate
  techniques; a new artist can apply the guide to one focused batch. The toolkit constructs
  recognizable forms, not merely SVG strings. Keep limitations explicit and adjust the guide
  when the next examples reveal a better choice.
- Parallel-plan ready: limited; one visual-language owner consolidates examples, and one toolkit
  owner implements demonstrated parts after that comparison.

### Milestone: Renew focused art batches

- M5 follows the accepted M4 guide/toolkit; the reassessment hold is released for this bounded batch.
- Entry criteria: each batch has an owner, source contexts, a useful teaching objective and the
  provisional guide; assignments live in the existing workstream index.
- Deliverables: refined strong candidates and newly composed weak candidates, original SVG sources,
  a source-to-drawing map and brief actual-size visual comparisons. Start with ABO, bottleneck and
  Drosophila chromosome-complement weaknesses, then expand to coherent families across the five active groups.
- Exit criteria: each finished drawing communicates its intended object or relationship, preserves
  science and course examples, fits the common visual language and is readable at its intended
  size. Retained sources have concrete scientific or scope reasons; broad "too difficult" deferral
  does not substitute for trying a viable art method.
- Parallel-plan ready: yes after M4; batch by art family with disjoint physical edit ownership.

### Milestone: Integrate and deliver

- M6 depends on reviewed M5 artwork and its consumer map; batches may reach it incrementally.
- Entry criteria: final drawing bytes and relevant source states are frozen for each export.
- Deliverables: minimal Djot integration, fresh ODP/PDF for changed consumers and restored roots
  with obsolete outputs, changed/adjacent page review, exact final checks and remaining dispositions.
- Exit criteria: actual slide rendering preserves legibility, facts and reveals; original assets
  remain available; final base pytest passes after edits with mutations inspected; Djot stays
  ASCII and SVG stays XML-valid. Resolve a failed placement by improving composition or necessary
  local layout, then rebuild affected consumers.
- Parallel-plan ready: yes for independent inspection; one owner serializes LibreOffice exports.

## Test and verification strategy

Judge art through source/current/proposed comparisons and actual-size rendered use. Ask whether
students can recognize the object, follow the mechanism, compare the relevant difference and find
labels without visual searching. Assess silhouette and anatomy, purposeful composition, clear
linework, useful depth, consistent color meaning and a level of detail that survives projection.
A cleaner contour alone is insufficient when the original weakness is poor explanation.

Preserve scientific invariants rather than pictorial accidents: identities, bonds, scientifically meaningful or data-defined chromosome/band counts, actual
relationships, numerical values and staged answers. Illustrative wells, bead placements, vein
marks and similar schematic details can change when they do not encode the lesson's evidence. Schematic positions can
change; empirical data cannot be invented. Unknown plot inputs or unresolved source contradictions
hold that drawing for evidence. Count slides to detect accidental losses, not to impose an art
quality target. Preserve the lesson sequence and meaningful reveals; any additional slide split
must follow existing authorization, not an arbitrary matching-count rule.

Inspect actual changed and adjacent ODP/PDF pages, including every consumer of a shared change.
Run LibreOffice-capable commands outside the sandbox through repository scripts. Rendered exports,
attended playback and learner/instructor acceptance are separate evidence. A standalone preview
is not a classroom-output check. Historical native-table edit/reopen proof need not be repeated.

Run `source ./source_me.sh && pytest tests/` after final implementation edits. Inspect any automatic
ASCII/whitespace changes and rerun after fixes. SVG uses XML-supported entities or numeric references;
Djot permits HTML character references. Use small focused checks for new nontrivial shared logic.
Keep one-time art checks under `_temp/`; do not add permanent tests for compositions or subjective
style. No new approval machinery, exhaustive visual matrix or art-score threshold is required.

## Risk register

| Risk | Impact | Trigger | Owner | Mitigation |
| --- | --- | --- | --- | --- |
| Preservation replaces creativity again | Accurate but weak art reaches delivery. | Reviews cite XML/counts without a visible learning or recognition gain. | Art lead | Recompose weak cases and compare at intended size. |
| Style fixed before examples | Hundreds of inconsistent or awkward drawings. | Guide rules lack successful equipment/organism/diagram examples. | Visual-language owner | Keep guide provisional; resolve representative examples before bulk dispatch. |
| Toolkit expands without payoff | Software consumes the art effort. | New abstraction lacks a real drawing use. | Toolkit owner | Keep geometry local; share only demonstrated parts. |
| Artistic freedom changes science | A prettier drawing teaches the wrong thing. | Lost data-defined counts, identities, labels or premature answer cues. | Drawing owner/reviewer | Repair against source facts and neighboring reveal states before integration. |
| Dense source placement fails | Useful standalone art becomes unreadable. | Actual export clips or shrinks a key feature. | Export owner | Adjust composition/minimal layout and rebuild; retain source if unresolved. |

## Documentation close-out requirements

Use the existing ledger and workstream index for results, current next tasks and acceptance limits.
The reassessment is the single durable account of this redirect; detailed experiments stay in
`_temp/`. At delivery, update the existing changelog, final consumer evidence and retained/deferred
reasons. Preserve historical reports without relabeling their acceptance as current creative
approval. The provisional illustration guide becomes a working reference only through reviewed
examples; its accepted creation is complete, while course delivery remains a separate result.
