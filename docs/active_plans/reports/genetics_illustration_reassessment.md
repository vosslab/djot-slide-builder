# Genetics illustration reassessment

Status: reviewed direction in execution, 2026-11-09. The manager releases the reassessment
hold for the bounded original-art batch under existing implementation authorization. Contextual
review, bounded canonical integration, canonical ABO/drift full-root exports and final batch
checks are complete. The chromosome/folded-hemoglobin/CCR5/corn drawings and their ten-page
original-voice proof are accepted; art-only integration, canonical four-root exports and fresh
full-suite verification are complete. Broader creative renewal remains open. This report supports
[genetics_visual_renewal_plan.md](../active/genetics_visual_renewal_plan.md); the existing
[progress ledger](genetics_visual_renewal_progress.md) and
[workstream index](../workstreams/genetics_visual_workstreams.md) own execution status and tasks.

## What the clarification changes

The goal remains ambitious original SVG artwork throughout Genetics. The instructor clarified
that the pixel-equivalence evidence raised concern, not that the existing artwork was uniformly
poor. Keep useful existing art. Source images establish facts, teaching purpose and course
examples; artists can change viewpoint, composition, form and visual explanation.

The instructor's latest clarification prioritizes drawing and clipart replacements for
rasterized images. Preserve slide voice, titles, native prose, alt text, examples, layouts and
sequence. Scientific source checks support the drawing; they do not open a global science
audit or prose-revision project. Resolve important drawing issues without bikeshedding.

Pixel comparisons were valid evidence that serializer refactoring preserved existing drawings.
Archive replay equality similarly proves preservation. Neither is an art-quality requirement or
proof of creative renewal. The three `svg_tools/drawing.py` helpers are useful maintenance work;
limiting the requested construction toolkit to them was a manager decision, incorrectly presented
as user direction in D7. The plan and ledger now correct that attribution.

Earlier broad implementation also included independent native/table/lesson changes. Five cleanup
handoffs and the narrowed specification review establish that the scope reconciliation and
preservation work is complete. That review explicitly leaves the art/construction-toolkit
objective open. Existing accepted M2 integration remains useful; its table edit/reopen exercise
is not a new delivery task. Gene-tree work remains archived and deferred.

## What the artwork shows

A read-only audit rendered and inspected six actual source/current pairs. Its detailed evidence
is local at `_temp/svg_creative_reassessment/FINDINGS.md`, with `01_apparatus_pair.png` through
`06_bottleneck_pair.png` and exact source mappings in `render_pairs.py`. This sample supports
specific decisions, not a verdict on every candidate.

| Example | Observed result | Proposed action |
| --- | --- | --- |
| Electrophoresis apparatus | Coherent chamber planes, wells and polarity improve recognition and reading. | Keep; selectively refine rim, gel thickness and near/far edge hierarchy. |
| Pea anatomy | Recognizable legume form and flower cutaway explain reproductive structures. | Keep/refine organic overlaps and the pollination bag; retain characteristic flower anatomy. |
| Nucleotide | Better labels, bond hierarchy and component color; source-like topology is appropriate. | Refine spacing/background emphasis while retaining ribose chemistry and stereochemical cues. |
| ABO glycans | Small symbolic differences are separated from the larger chemical chains; row/column organization forces remapping. | Align large symbols and chains by antigen and emphasize the terminal difference. |
| Chromosome complements | Smoother contours preserve parts but add little explanation of the two groups. | Establish the source relationship before labels/recomposition; do not invent banding or a chromocenter from the filename. |
| Bottleneck | Open bins/funnel weaken the bottle metaphor; an equal-color bead grid appears deliberately arranged. | Construct a recognizable bottle, narrow neck and receiving vessel; preserve stages and the five-blue/one-white result. |

The earlier plan's completion criteria emphasized source preservation, parsing and export checks.
Those checks remain necessary but did not explicitly require visible gains in recognition,
comparison or explanation. Likewise, preserving "geometry" did not distinguish scientific
topology from incidental contour. The revised plan makes that distinction and carries good work
forward rather than imposing a blanket redraw.

## Representative experiments

Equipment evidence is complete at `_temp/svg_construction_primitives/findings.md`. A newly
composed cutaway gel chamber and a construction sheet were rendered at 1200 and 320 pixels.
An assembled cutaway and exploded alternative were compared; the assembled view was chosen for
the direct well-to-positive-pole relationship. Cuboids supply coherent chamber/gel faces, and
projected cylinders/tapers construct electrode terminals and pipette parts. An ellipsoid exists
on the sheet; its usefulness for organisms is not established by equipment alone.

The experiment applies Robertson's *How to Draw* passages on boxes/XYZ planes, ellipse axes,
volume planning and cuts, plus *A Handbook of Biological Illustration* on clarity, selective
emphasis, upper-left light and line hierarchy. *Mastering SVG* supports viewBox scaling. Exact
local reference paths and passages are in the findings. These books informed drawing choices;
they do not prescribe the experimental palette, projection coefficients or a universal style.

Organism experiments at `_temp/svg_visual_language/organism/` compare compact form-based and
organic Drosophila. `REVIEW.md` favors organic anatomy for a large illustration and compact forms
for repeated phenotype comparisons. Silhouette, eyes, wing pair and abdomen remain useful at
320 pixels; tiny facets/bristles need not carry the meaning. The organic drawing uses curved
masses and overlap without importing a general shared organism constructor.

Diagram experiments at `_temp/svg_visual_language/diagram/NOTES.md` favor a flat three-stage
crossover composition. It shows the starting four chromatids, the inner nonsister exchange and
two unchanged/two recombinant products. Flat ancestry colors, dots and allele labels carry the
meaning; equipment-like shading would add little. Shared ink, restrained line hierarchy and
purposeful color connect these examples without a universal projection or palette.

The combined `_temp/svg_visual_language/export/visual_language_proof.odp` and `.pdf` each have
seven pages matching the Djot source, with zero hidden pages. `evidence.json` records embedded
SVG hashes, text and rendered pages. Fresh review accepts all seven actual PDF pages without
clipping, label or export defects; the three-stage crossover ancestry is coherent. Equipment and
organic fly are strong prototypes to keep. One rear fly leg is occluded, so the fly is suitable
for organism/phenotype illustration rather than a six-leg-counting diagram. Detailed findings
are at `_temp/svg_visual_language/VISUAL_REVIEW.md`. This accepts prototype examples, not final
course integration or an authoritative style guide.

## Reviewed direction

The accepted provisional
[GENETICS_ILLUSTRATION_GUIDE.md](../../slide-specs/GENETICS_ILLUSTRATION_GUIDE.md) preserves
successful equipment, organism and diagram examples as three durable SVGs before broad dispatch. Cover palette and semantic color, linework,
lighting/depth, proportions/detail, label hierarchy and reusable parts. Start from the existing
color guidance and useful current art. Share qualities that improve reading; allow apparatus
planes, organic anatomy and flat molecular/topological diagrams to use different techniques.

The accepted small toolkit adds `project()`, `cuboid()` and `cylinder()` to the existing writer.
Cuboids and projected cylinders have real equipment uses; a shared rounded-form API is not justified merely because the organism uses curved masses.
Keep subject-specific assembly, scientific meaning and label placement with the drawing. There
is no demonstrated need for a 3D engine, scene framework or universal style API.

The first focused batch has accepted ABO/bottleneck artwork and canonical delivery, with
chromosome identity/context investigation complete. Three remaining-family surveys now support
bounded assignments through the five active groups; selective refinements to strong examples
remain lower-priority tasks. The first batch demonstrates the reviewed guide.
Preserve scientific facts, examples and reveals while allowing fresh visual explanations. Use
minimal course integration and inspect real ODP/PDF pages; standalone previews cannot prove fit.

## Accepted bounded work

The guide's specification and quality reviews accept the provisional guidance and all three
examples. They support coherent line hierarchy, restrained detail, semantic color and techniques
suited to each subject. The fly remains unsuitable for counting all six legs. The guide is a
working reference, not final course integration or an immutable style policy. Reviews remain
local at `_temp/genetics_illustration_guide/SPEC_REVIEW.md` and `QUALITY_REVIEW.md`.

Both construction reviews accept the fixed projection and small cuboid/cylinder toolkit, with
two focused tests passing and existing recipe compatibility checked. The apparatus demonstrates
connected volumes and readable wells, pipette and polarity. The cylinder uses a sampled surface
for upright schematic components; shallow, wide tapers need fresh tangency work, and zero-radius
cone tips are unsupported. Recipes retain responsibility for occlusion, cutaways, draw order and
scientific labels. No general scene framework or organism constructor was added. Evidence is
local at `_temp/svg_creative_refinements/construction/{SPEC_REVIEW,QUALITY_REVIEW}.md`.

ABO specification and quality reviews accept the paired horizontal rows: each O/A/B symbolic
chain sits beside its chemical equivalent, with aligned scaffolds exposing the terminal sugar
difference. The source Fuc-Gal-GlcNAc-Gal chain, alpha-1,2 and beta-1,3 backbone links, and A/B
alpha-1,3 additions to the first Gal remain intact. Shape, position and live labels supplement
source-specific colors. Full linkage notation is readable at the larger preview size; small
previews establish the scaffold and square/circle distinction, not every chemical label.

All three bottleneck stages pass specification and quality reviews. Upright/tilted bottles,
narrow necks and a receiving vessel restore the metaphor, with irregular bead positions and
restrained depth. The first stage contains only the starting population; stage 2 adds exactly
two falling blue beads; stage 3 adds five blue and one white survivor with no yellow. Repeated
groups retain cumulative reveal identity. Starting masses are explicitly schematic; their
15 blue, 12 white and 3 yellow beads do not claim measured frequencies. A falling bead slightly
overlaps the receiver rim, judged optional polish rather than a teaching defect. Local reviews
are in `_temp/svg_creative_refinements/{abo,bottleneck}/{SPEC_REVIEW,QUALITY_REVIEW}.md`.

The eight-page contextual ODP/PDF proof includes ABO authored slides 8-10 and drift authored
slides 10-14, covering the four drawings and their neighbors. The export owner reports clear
labels, preserved native text and reveal states, and no final clipping or replacement overlays.
The scratch drift placement removes three review markers and three references to `image_002.svg`:
its only painted content is a fully transparent 1243 x 236 PNG, verified pixel by pixel. Keeping
that invisible second image shrank stage 3 and triggered a readability overlay. The asset itself
is retained; only the reviewed references/markers are removed at integration. Export evidence is
local at `_temp/svg_creative_refinements/export/REVIEW.md` and `evidence.json`. Fresh independent
`INTEGRATION_REVIEW.md` accepts all eight pages for this bounded integration: source/ODP/PDF
counts agree, all five SVG payloads match, 28 native paragraphs are preserved, and rendered
previews reproduce the exact PDF. Stage 3 is about 14% smaller but remains readable for the
existing page-by-page reveal; stationary animation was not tested. This contextual proof does
not establish whole-course delivery.

Canonical integration now replaces the four SVGs with the exact accepted bytes and removes
only the three review markers and three invisible-image references from drift authored slides
11-13. ABO Djot is unchanged. Source counts remain 44 ABO and 35 drift slides; other assets
and original rasters remain unchanged, with prior versions backed up. ASCII/XML, full-source
parse/compile, structural lint and scoped diff checks pass. The local integration receipt is
`_temp/svg_creative_refinements/integration/HANDOFF.md`, with hashes in `evidence.json` and the
exact six-line delta in `source.diff`. Canonical ABO/drift ODP/PDF rebuilds now pass; the
[genetics_visual_renewal_progress.md](genetics_visual_renewal_progress.md) records final batch
evidence and unrelated capacity advisories.

## Chromosome source findings

The comparison is source-supported as XX on the left and XY on the right, with eight chromosomes
in each complement: four large bent autosomes, two dots and two sex chromosomes. It does not
show two chromocenters, deletion stages, synapsis or banding. The current
`polytene_chromocenters.drawn.svg` name/title misidentifies this reference image. Its accepted
replacement is now `chromosome_complements.drawn.svg`; the previous asset remains preserved.

In the original `genetics/LECT11/lect11d-chromo_alter_1-deletions.odp`, physical slide 22,
"Drosophila chromosomes", contains imported `image_013.png` and `image_014.png`. Embedded
bytes match the imported images by SHA-256. The first directly labels X, Y, 2, 3 and 4; the
second is the unlabeled complement pair. On physical slides 23-24, `image_015.png` has an
explicitly labeled inset in the same arrangement: chromosome 2 at left, 3 at right, dot
chromosome 4 centrally, X rod and hooked Y below. Its separate large banded specimen carries
the chromocenter/polytene labels. Original slide 21 introduces polytene deletion mapping and
slide 25 proceeds into that mapping, explaining the complement reference's teaching position.

The original `genetics/LECT11/lect11c-sex_dosage.odp` directly identifies normal XX female and
XY male complements on slide 3 and gives `2,2,3,3,4,4,X,X` for the female on slide 47. Slide 4
states that Y does not determine maleness; new captions must not imply that it does. These
printed labels and statements are direct observations. Applying them to the matching unlabeled
silhouettes in `image_014.png` is the supported interpretation, not a label printed in that image.

A future drawing can align equal XX/XY columns, keep shared autosomes quiet, and emphasize
the two differing sex-chromosome pairs through placement and shape as well as color. Use
"Drosophila chromosome complements" and a schematic/not-to-scale qualifier. Preserve each
complement's chromosome count; derive optional 2/3/4/X/Y group labels from the inset rather than
inventing lengths, homolog-specific identities or band maps. The image's original creator,
external provenance, caption, physical scale and cell-cycle phase remain unknown. The local
source investigation and byte mappings are retained at
`_temp/svg_creative_refinements/chromosome_context/FINDINGS.md` and `source_evidence.json`.
It inspected historical source PDF pages, without a new export or canonical edit.

## Remaining-family survey findings

Three read-only surveys on 2026-11-09 compare current source art, authored SVGs and earlier
drafts. Their nominations and scientific boundaries are durable in the linked group briefs;
source images and empirical evidence remain retained. The exact survey order is:

| Survey | Ranked nominations and visible gain | Current state / durable detail |
| --- | --- | --- |
| Foundations/inheritance | 1. Hemoglobin: folded subunits instead of beads. 2. Corn: recognizable reproductive anatomy and closed cycle. 3. Four-stage meiosis: readable cell/spindle anatomy with source-traced ancestry. | Hemoglobin/corn artwork and exact-source context accepted; integration complete. [genetics_visual_foundations.md](../workstreams/genetics_visual_foundations.md), [genetics_visual_inheritance.md](../workstreams/genetics_visual_inheritance.md). |
| Linkage/variation | 1. Six-slot yeast family: budding/mating/ascus silhouettes and fused-cell continuity. 2. Inversions: physical four-track loops, centromeres and reciprocal outcomes. 3. Morgan: recognizable normal/vestigial flies in two active cross assets. | Future bounded tasks; existing straight-row inversion and disk-cell yeast trials are not ready to promote. [genetics_visual_linkage.md](../workstreams/genetics_visual_linkage.md), [genetics_visual_variation.md](../workstreams/genetics_visual_variation.md). |
| Population/shared | 1. Mouse selection: five coat tones, shared ancestor and selection-pressure/outcome comparison. 2. CCR5: recognizable virus/receptor interaction in three source states. First-cousin paths are lower-priority integration, not a third art nomination. | CCR5 artwork and exact-source context accepted; integration complete; mouse unassigned. Keep recognized Office Hours art. [genetics_visual_population.md](../workstreams/genetics_visual_population.md). |

Chromosome-complement art and its exact-source context are also accepted; source findings above
remain the contract. Guide/helpers/ABO/bottleneck acceptance is unchanged. These surveys do not reclassify
the CSVs, authorize native-table redesign or establish whole-course completion.

| Local evidence directory under `_temp/svg_family_renewal/` | Survey coverage and limits |
| --- | --- |
| `survey_foundations_inheritance/` | `REPORT.md`, `counts.json`, `sheet_sources.json`; five historical foundations and five inheritance sheets plus fresh `flies.webp`, `cycles.webp`, `phenotypes.webp`, `foundations_remaining.webp`, `meiosis.webp`. Combined 357 candidate uses/265 original paths; 82 referenced authored SVGs/97 physical uses; 183 original candidate paths still referenced/265 current uses. Different denominators, not subtraction or required redraws. |
| `survey_linkage_variation/` | `REPORT.md`, `candidate_inventory.csv`, `visual_manifest.json`; seven visually inspected sheets, 55 displayed items including repeated comparisons. Original accounting is 295 candidate uses/198 concept-asset pairs, including excluded M2 candidates. Other variation families were not all freshly reviewed in detail; absent original references do not prove acceptance. |
| `survey_population_shared/` | `REPORT.md`, `reviewed_manifest.json`, `current_consumers.json`; nine visually inspected contact sheets/73 items and two scratch sheets/eight drafts. Current consumer indices were parsed without exporting; recompute after integration. Preserve P25/P34 evidence holds and mixed source composites. |

The surveys report standalone visual selection only. They ran no LibreOffice, full suite,
canonical integration, final ODP/PDF review, native edit/reopen, playback or learner review.
Scientific completeness, ancestry, lecture-size fit and changed/adjacent-page acceptance remain
task-specific requirements. Local evidence is ignored; these retained findings and linked exact
source contracts preserve the actionable decisions without promising scratch availability.

## Four-family contextual acceptance

The independent `_temp/svg_family_renewal/export/INTEGRATION_REVIEW.md` accepts chromosome
complements, folded hemoglobin, CCR5 and corn plus all ten original-voice contextual pages.
Its authoritative proof is `export/exact_source/contextual_proof.{djot,odp,pdf}` under that
same family-renewal directory: 10 source/ODP/PDF pages, 18 preserved native paragraphs and
12 exact embedded payloads. All native paragraphs remain selectable in PDF. Corn also passes
independent artwork-quality review; a minor readable arrow/label contact is accepted.
The [progress ledger](genetics_visual_renewal_progress.md) links the exact canonical consumers.

The three CCR5 native-prose qualifications trialed outside `exact_source/` are cancelled after
the instructor's clarification. They were never canonical and must remain historical scratch
evidence. The original voice is retained; the drawing's own R5 HIV-1 scope remains readable.
Canonical integration preserves alt text too: two existing SVG overwrites, two new SVGs and
exactly two image-URL substitutions. Integration is complete, with exact candidate hashes and
unchanged native source bytes apart from those URLs; the receipt is
`_temp/svg_family_renewal/integration/HANDOFF.md`. Canonical four-root exports and fresh final
checks pass; the final delivery receipt is in the progress ledger. This does not reopen the prior
accepted batch or establish whole-course completion.

## Evidence limits

The latest historical base suite passed `5322` tests with `2` warnings in `28.66s`, zero
mutations across 1,143 hashed files, 118 ASCII Genetics Djots and 376 parseable source SVGs.
Evidence is local at `_temp/genetics_visual_renewal/final_verification/reassessment_closeout/`
(`pytest.log`, `pytest.status`, `postchecks.json`). This predates the current accepted guide,
helpers and art batch. The later final batch run passes 5324 tests with 2 warnings in 28.23s,
exit 0, before this documentation-only receipt; exact evidence and scope are recorded in
[genetics_visual_renewal_progress.md](genetics_visual_renewal_progress.md). The guide/toolkit,
standalone/contextual reviews, bounded canonical integration and ABO/drift exports are complete;
remaining art families and final course exports are unfinished. No attended playback, student
outcome or instructor acceptance is claimed by this reassessment.
