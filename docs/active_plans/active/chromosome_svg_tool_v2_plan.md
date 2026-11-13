# Plan: Stabilize chromosome bands, centromere labels, and sister shape

## Context

The user rejects the v1 sister silhouette and requests meaningful cytogenetic bands and a
larger labelable centromere marker. This supersedes v1 visual acceptance for that silhouette.
Preserve the v1 specimen and reviews as historical evidence. The task is a bounded tool repair;
course substitutions require a separate source-level review.

Status: DONE for the library and standalone v2 artifact, 2026-11-12. Fresh corrected
specification, independent quality, and integration reviews PASS. The broader lecture-art
goal remains ACTIVE; no course substitutions or user/classroom acceptance are implied.
This is a stabilization plan at the rendering-contract level. It identifies local failures,
bounded experiments, and their acceptance criteria, rather than prescribing a broad refactor.
The user has authorized continuation through internal review and implementation; another human
permission cycle is not a dependency.

## Objectives

- Show source-authored variable-width named bands with usable address geometry and provenance.
- Make the centromere a readable label target while retaining the underlying constriction.
- Replace the default tapered sister shape with thick rounded chromatids forming an open X.
- Preserve old rod APIs, segment ancestry through rearrangements, and separate exon/intron tracks.

## Design philosophy

Apply **Keep it simple (KISS)** from REPO_STYLE.md: extend immutable values and the existing
renderer only where these three requests need information or geometry it currently lacks.
Use small rendered comparisons to settle the shape before committing an interface. A generic
layout engine, biological simulator, or stock-art trace would add work without satisfying the
actual teaching need. Keep scientific map identity separate from decorative texture.

## Scope

- Diagnose and repair the three observed output limitations with recorded one-variable proofs.
- Establish explicit interval, marker, portrait-orientation, and attachment-anchor contracts.
- Produce a new v2 example, source-backed chromosome-7 map and nested 7q31.2 enlargement.
- Verify useful small and large actual displays, compatibility, scientific meaning, and fonts.

## Non-goals

- Add a GUI, CLI, dependency, schema system, theme engine, genomic database, or runtime download.
- Implement inversion, meiosis, crossing over, or a comprehensive chromosome catalog.
- Modify Biotechnology, LECT11, teaching decks, historical specimens, or historical review seals.
- Treat the schematic 17q41.3 teaching exercise as an actual chromosome-17 band map.

## Historical baseline

On 2026-11-12 the planner reran the two focused modules: **10 passed in 0.04s** using direct
Python 3.12, `--noconftest -p no:cacheprovider`. This is focused regression evidence only.
The current source hash supplied by the manager is
`fc78b4cd52a1f55abe1ecf215250ac510cd4c9fd8626ea90d2aa192d27114df4`.
The baseline failures were visual/informational, not a failing test suite:

- `_BANDS` contains five sparse decorative patterns, with no named intervals or address anchors.
- Sister paths taper over long distances and shrink labels close to the attachment.
- The small collar offers little usable labeling area; the return tuple exposes only x boundaries.

The frozen Segment model and deletion/tail-exchange operations already retain surviving objects,
lengths, colors, and decorative band identity. `gene_tracks.py` provides separate DNA anatomy.
Current `chromosome_svg` and `render_chromosome` return fragment, width, and x boundaries.

Reference report: `_temp/chromosome_svg_tool_v2/references/REPORT.md`; all four source images
were personally viewed by the manager. BioNinja and Shutterstock best support substantial rounded
arms, open negative space, and a broad central oval. Construct original contours. The fourth
reference contains two replicated homologs, four chromatids, not one four-color chromosome.

The manager's LECT10 source inspection establishes the need for p/q orientation, numbered
regions, variable-width bands, and a nested chromosome-7/region-3/band-1/subband-2 explanation.
Scientific authority: [UCSC cytoBand schema](https://genome.ucsc.edu/cgi-bin/hgTables?db=hg38&hgta_group=map&hgta_track=cytoBand&hgta_table=cytoBand&hgta_doSchema=describe+table+schema),
[UCSC hg38 band table](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/cytoBand.txt.gz),
[MedlinePlus gene location](https://medlineplus.gov/genetics/understanding/howgeneswork/genelocation/),
and [NHGRI centromere](https://www.genome.gov/genetics-glossary/Centromere).
UCSC positions are approximate Giemsa-band intervals, with zero-based starts; preserve the
source's half-open interval convention. CFTR maps to 7q31.2; band numbers increase outward
from the centromere. Do not infer a gene's precise base-pair position from its band address.

Source evidence is now retained in `_temp/chromosome_svg_tool_v2/band_source/REPORT.md`
and `provenance.json`: 44 chr7 rows cover 0, 159345973); q31.2 is
[115000000, 117700000), gneg. The centromeric p11.1/q11.1 boundary is 60100000.
The q3 union spans [107800000, 159345973), and q31 spans [107800000, 127500000).
The exact subset SHA-256 is
`657eddbe2a159b4a99a4caaa5a9ccf462bb18a12047984266924385a21851609`.
Use these retained rows, including q31.31/q31.32/q31.33, rather than inventing map coordinates.
The existing scratch worker's original shape concepts in
`_temp/chromosome_svg_tool_v2/concepts/` supply E1 evidence without a production API commitment.

Decision V2-SHAPE: root personally viewed `concept-800.webp` and `concept-400.webp` and approved
the original shape direction for implementation. The closed smooth arm paths retain substantial
width, form a recognizable upright open X, and meet beneath a broad readable `cen` oval with a
true underlying neck. `concepts/REPORT.md` and `build_concept.py` are geometry evidence only;
integrate the construction into one shared production core, not a second long-lived renderer.
The approved concept uses 70-unit distal arms, a 114-by-62 oval and a 32-unit live label; these
are demonstrated proportions, not hard-coded universal size requirements. Both corrected proofs
use actual embedded Atkinson Hyperlegible Next Regular. Prototype bands are schematic only.

## Hypotheses

- Long linear taper causes the disliked silhouette; rounded near-constant-width arms with only
  a short central constriction will recover the reference-like open X.
- An overlaid oval with reserved label space will make centromeres labelable without representing
  the biological constriction itself as a swollen chromosome segment.
- Explicit intervals retained with source segments will support true band identity and nested
  highlighting without a generalized genomic model.

## Diagnostic phase

Record each result and proof hash in the task ledger before promoting its change.

| Experiment | Hypothesis | Change | Metric | Result | Keep/Revert |
| --- | --- | --- | --- | --- | --- |
| E1 | Long taper causes rejection | Rounded continuous open-X sisters in shared renderer | Thick arms, local neck, upright labels and unequal p/q spans | DONE; final shape at 452 x 724 and both galleries viewed by root and fresh reviewers | Keep |
| E2 | Collar lacks label area | Broad generic labelable oval; explicit marker bounds | Live cen text and external attachment fit complete envelope | DONE; generic label retained; real-map marker confined to collar after P2 correction | Keep |
| E3 | Decorative stripes discard addresses | Exact 44-row chr7 hg38 adapter and identity-linked anchors | Actual stains, original intervals and shared q/q3/q31/q31.2/CFTR zoom | DONE; all 44 paint spans visible, including both acen intervals | Keep |

The architecture_review.md (`_temp/chromosome_svg_tool_v2/architecture_review.md`; scratch evidence removed 2026-11-13)
approved the explicit construction and satisfied the separate algorithm-proposal gate.
The first quality review found P2 map-marker occlusion. The bounded recipe correction uses
`marker_size=(24, 112)` without internal text and an exterior Centromere callout. It leaves
2.4044 drawing units of stroke-inclusive clearance on each side inside the source-free collar.
The generic large labelable marker remains. Core, source data, grouping and zoom were unchanged.

## Completed review sequence

Architecture approval, E1/E2/E3 implementation, final production proofs, corrected fresh
specification review, different quality review, and integration review are complete. Root
personally viewed all five final frozen proofs. Current authority:

- spec_review_v2.md (`_temp/chromosome_svg_tool_v2/spec_review_v2.md`; scratch evidence removed 2026-11-13): PASS.
- quality_review_v2.md (`_temp/chromosome_svg_tool_v2/quality_review_v2.md`; scratch evidence removed 2026-11-13): PASS.
- integration_review.md (`_temp/chromosome_svg_tool_v2/integration_review.md`; scratch evidence removed 2026-11-13): PASS.

Earlier reviews remain historical evidence; their pending follow-on language does not override
these completed gates. The user has not personally approved the final v2 shape.

## Compatibility contract

The implemented contract follows
architecture_review.md (`_temp/chromosome_svg_tool_v2/architecture_review.md`; scratch evidence removed 2026-11-13).
One immutable `Segment` represents each source row; `Segment` and `Chromosome` stay unchanged.
No nested `Band` model was implemented. Frozen `Cytoband(chromosome, start, end, stain, segment)`
retains source coordinates and the original Segment reference; its address is `segment.label`.
`read_cytobands(path)` returns `(Chromosome, tuple[Cytoband, ...])`. It validates a complete,
contiguous, zero-based intact source map, supported stains, p-before-q order, and adjacent p/q
acen rows. The exact 44-row hg38 chr7 TSV has adjacent provenance JSON. No runtime download.

`render_chromosome_layout(name, chromosome, *, length=None, thickness=62,
orientation="horizontal", bands=True, sisters=False, junctions=(), allele_labels=False,
labels=True, marker_size=None, marker_label=None)` returns frozen `ChromosomeLayout`:
`svg`, `width`, `height`, `boundaries`, `segments`, `centromere`, and `marker_bounds`.
Each frozen `SegmentAnchor` holds the original `segment`, `sister`, `start`, `end`, and `bounds`.
Coordinates are final page coordinates; segment bounds are conservative annotation bounds.
The complete longitudinal/transverse envelope includes the marker but excludes outline stroke.
Portrait puts p above q and keeps text upright. `marker_size` is `(along_axis, across_axis)`;
`marker_label` is optional live text, with approximate fitting and actual-font review required.
Marker bounds provide exterior edge-midpoint attachments. Marker/gap/cap space is schematic,
not genomic length. Marker settings require a centromere and must fit the envelope.

Both old horizontal tuple APIs keep their meanings and single-rod compatibility through one
shared renderer. `sisters=True` in both old and new entries now produces rounded continuous
open-X sisters. The local constriction remains beneath the broad generic label target.
Separate DNA/exon/intron behavior is unchanged. Deletion and tail exchange retain original
Segment identity; source address/stain/coordinates do not become destination identities.
Source maps disable decorative texture and dense internal labels with `bands=False, labels=False`.
All supported stain conventions and generic color mode remain documented in
[README.md](../../../svg_tools/README.md#chromosome-drawing-tool).

The same original segments drive the map, q/q3/q31/q31.2 groups and five-band CFTR zoom;
separated rearranged runs stay separate. Positions are approximate cytoband intervals, not
precise CFTR molecular coordinates. There is no actual chromosome-17 q41.3 map claim.
The recipe main writes v2 only. Old functions remain callable using today's renderer; they
cannot reproduce the historical rejected shape. Saved v1 art and review seals remain unchanged.

## Files to modify

| File | Purpose and source of truth |
| --- | --- |
| `svg_tools/chromosomes.py` | Source adapter, shared geometry, frozen layout anchors, marker, validation and compatibility |
| `tests/test_svg_chromosomes.py` | A few lasting regression checks for new biological/geometry contracts |
| `svg_tools/chromosome_examples.py` | New v2 recipe, retaining old recipe and historical output |
| `svg_tools/data/chr7_hg38_cytobands.tsv` | Exact fixed 44-row subset; adjacent provenance JSON records source and hash |
| `docs/slide-specs/illustration_examples/chromosome_tool_v2.drawn.svg` | New output generated by v2 recipe; never overwrite v1 |
| `docs/slide-specs/GENETICS_ILLUSTRATION_GUIDE.md` and `svg_tools/README.md` | Verified API, meaning, size limits and new specimen link |
| `docs/CHANGELOG.md` | Concise v2 behavior and actual validation after acceptance |
| This plan and `_temp/chromosome_svg_tool_v2/TASK_LEDGER.md` | Decisions, experiments and closure evidence |
| `_temp/chromosome_svg_tool_v2/` | Scratch proofs, WebP renders, font evidence, reviews and hashes |
| `docs/SVG_REPAIR_BACKLOG.md` | Append v1 sister rejection now; keep historical evidence |

Existing `gene_tracks.py`, its tests, `drawing.py`, old galleries, old plans/review seals, and
course assets are read-only compatibility references. Review callers with targeted searches
before editing the shared renderer. Python follows repository tabs, annotations and absolute
module imports. The original planning assignment wrote only the new plan, ledger, and backlog entry.
Metadata closure owns exactly seven existing files, with one preimage each; see
closure.md (`_temp/chromosome_svg_tool_v2/closure.md`; scratch evidence removed 2026-11-13).

## Verification

Permanent coverage earns its place through plausible data loss or user-visible regression:
interval order/overlap/range rejection; stain ordering and real-address bounds; retained ancestry
and mirrored sister maps after deletion/tail exchange; marker envelope and attachment coordinates;
portrait text orientation; old tuple/allele/escaping and DNA regression. Use compact fixtures,
not path snapshots, exhaustive matrices, or a new framework.

Run direct Python 3.12 with `-B`, and focused pytest with `--noconftest -p no:cacheprovider`.
This task explicitly prohibits Git, including bootstrap and indirect conftest invocations;
do not run `source_me.sh`. Inspect command imports before execution. Every LibreOffice-capable
command must use the repository wrapper outside the sandbox. Native proof is optional; claim
native compatibility only when that actual route was checked.

Temporary proof must establish:

- XML validity, unique/resolved IDs, live selectable text and escaped labels, and finite geometry.
- Rounded portrait sisters at an actual small panel and large presentation size chosen and
  recorded before review; a tiny overview is not evidence of readable component labels.
- Prominent center label and an exterior annotation with no overlap or clipping, including strokes
  in document margins. Mark the broad oval as a diagrammatic label target over a constriction.
- Source-backed chr7 with p/q, variable-width stained bands, nested q3/q31/q31.2 highlighting and
  enlargement, with visible CFTR address. Use the same interval objects to drive map and zoom.
- Decorative and source-backed examples are visibly captioned and distinguishable in metadata.
- A plain single rod, old allele case, deletion and exchange at a common scale, and unchanged DNA
  behavior. Do not independently normalize products to conceal shortened length.
- Small/large WebP proofs use `PANGOCAIRO_BACKEND=fc`. Verify actual embedded Atkinson Hyperlegible Next font programs
  against installed fonts, not merely SVG font-family text; the default rsvg route substituted
  Helvetica in earlier evidence. Record renderer, font evidence and source/proof hashes.

Blocking failure response: repair the responsible contract or geometry and rerun the affected
checks. A repeated algorithmic failure triggers the separate redesign described above. Do not
declare acceptance from numerical bounds alone or reuse v1 review approval for the new shape.

## Risk register

| Risk | Impact | Trigger | Owner | Mitigation |
| --- | --- | --- | --- | --- |
| Marker mistaken for swollen biology | Misleading anatomy | Oval hides underlying constriction | Renderer/spec reviewer | Preserve constriction and state diagram convention |
| Source identity lost after exchange | False band address | Labels reassigned by output slot | Core owner | Retain immutable source bands and test ancestry |
| Portrait breaks caller coordinates | Misplaced annotations | Reusing x-only tuple for y | Architect/core owner | New explicit point result; preserve old wrappers |
| Labels still tiny | Requested fix not met | Only enlarged crop is legible | Specimen/quality reviewer | Review actual panel sizes; reserve space or exterior labels |
| Plan drifts into broad redesign | Delayed repair | Generic paths/schema/catalog emerge | Architect | Reject expansion; isolate proven local changes |

## Documentation close-out requirements

Record exact approved API and evidence in this plan, including experiment results. Publish v2
usage and specimen links only after fresh review. Record actual tests, sizes, font verification,
and native-export scope. Keep the backlog's v1 rejection and all historical evidence intact.
The ledger owns execution status; do not reseal v1 metadata. Source-based map provenance remains
with the recipe/data and generated SVG. No course-art restoration is implied by tool acceptance.

Construction references read for this plan: SVG skill local-only
`scientific_illustration/A_Handbook_of_Biological_Illustration-1988.md`, lines 276-285
(clarity and emphasis without misleading exaggeration), and
`svg_authoring/Mastering_SVG-2018.md`, lines 635-655 (viewport versus coordinate system).

## Final evidence and limits

Integration reran 11 focused tests (0.07s) and pyflakes clean; root independently recorded
11 passes (0.06s). All five README blocks execute; all 16 scoped links resolve and both usage
docs are ASCII. The README named-map example uses `(18, 100)` and has 4.5725 units clearance.
The rendered diagnostic verifies 51 embedded Atkinson Hyperlegible Next Regular glyph outlines
and advances. Actual reviewed proofs: galleries 1600 x 1000 and 1200 x 750; shape 452 x 724;
map 530 x 724; zoom 538 x 724. These are demonstrated sizes, not universal minima.

Current core SHA-256: `f5468f12a4388c2cd3be5bda924487b2a1ecbcafed961288b3492485e16f37cf`.
Recipe: `5209008305c31166888521cc8a0bc622e8fa44687fce61373f979f0ed6d7bc82`.
Canonical SVG: `1a469d4b4e10ab91315d232440b01a696199f6cde4ef22e65cae5fd0c63a0925`.
Current 19-member manifest: `6dc50ce2eccdc3a5b555156187de92314943e5eed5bb207da7f67c19d840a55d`.
Historical 15-member seals remain unchanged, with exact old recipe/SVG preimages and the
previously authorized unused-parameter transition retained. No historical map was resealed.

Internal ASVS mapping records existing validation (2.2.1/2.2.3), documentation (2.1.1),
XML encoding (1.2.1/1.1.2), and restrictive writer (1.5.1), checked in specification review.
This adds no compliance framework, certification claim, or code-comment change.

Task-specific authorization permits direct Python 3.12 -B without source_me.sh or Git and
scoped edits beyond the general README-first-paragraph rule. Earlier metadata authorizations
and historical exceptions remain in force. Metadata closure performs bounded hash and text
checks only. No new production tests, render, full suite, LibreOffice/native export, classroom,
Zoom or print acceptance is claimed. No course Djot changed for this revision. Broader lecture
art remains ACTIVE; Biotechnology LECT11 is excluded and owned by another manager.
