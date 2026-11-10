# LECT08&#8211;09 M1 evidence

Saved workstream evidence for [genetics_visual_renewal_plan.md](../active/genetics_visual_renewal_plan.md).
Source owner: `/root/classify_linkage`.
Local source: `_temp/genetics_visual_renewal/linkage/EVIDENCE.md`. This is a saved snapshot;
see [genetics_visual_renewal_progress.md](genetics_visual_renewal_progress.md)
for current authorization, dependencies and acceptance status. Scratch paths remain local.
Non-ASCII source characters use numeric HTML character references.

Completed 2026-11-09 in assigned `_temp/genetics_visual_renewal/linkage/` only. Canonical content
was read only by this worker. Other workers may be changing canonical files concurrently.

## Coverage

The original parser inventory was filtered by root deck LECT08 or LECT09, retaining all original
fields. The CSV adds original_disposition, reason, concept_id, asset_id, heading, layout, slot,
physical_use_id and outside_consumers. Original disposition was unreviewed; the disposition
column now records the contextual decision.

| Measure | Count |
| --- | --- |
| Expanded original image uses | 181 |
| Distinct physical source/line uses | 175 |
| Distinct asset paths | 155 |
| Distinct asset hashes | 153 |
| Physical Djot source files | 21 |
| Root consumers | 14 |
| Hidden image uses in this filtered inventory | 0 |
| Concept IDs (including retained subgroups) | 34 |
| Original SVG redesign uses | 63 |
| Native-content repair uses | 46 |
| Already suitable uses | 49 |
| Retain with reason uses | 22 |
| Source clarification needed uses | 1 |

These are original-use counts, not promised new asset counts. The broader course has hidden
slides; this subset happens to have zero hidden image uses. No original row was discarded.

## Visual and context review performed

All 155 unique paths were rendered/read with Pillow or CairoSVG, then inspected in eight contact
sheets `contact_1.jpg` through `contact_8.jpg`. Original filename-to-preview mapping is assets.txt;
individual previews are `renders/001.png` through `renders/155.png`. This includes bitmap-containing
SVG wrappers, original vectors, photos, shared assets and repeated teaching sequences.

Enlargements inspected explicitly: 013 cis/trans; 016/017 X-linked source prose; 036 crossover
frequency; 042 six-locus chromosome model; 043 fly traits/map; 080 chi-square table; 099 mapping
functions; 102 mitotic exchange; 122 six crossover histories; 140 Neurospora cycle/micrograph;
154 random-order tree; 155 ws/ws+ ordered-spore example. Contact sheets contain all native-table
question/answer/mask states, not just one representative table.

Read physical source contexts including native prose, questions, notes, layouts, predictions,
reveals, and references. The complete snapshots are sources_context.txt and baseline_sources.json.
USE_ANCHORS.md and classification.csv provide each image use's local heading and slot. The saved
baseline protects those anchors from concurrent implementation edits. LECT08B prediction/answer,
LECT08C/D static table masks, LECT09E NPD question versus answer, and LECT09G/H cumulative
classification states have explicit preservation instructions in BRIEFS.md.

Read the approved plan, experiment FINDINGS.md, slide README/color/voice/pedagogy guidance,
SVG_DIAGRAMS.md, repository AGENTS/rules, and SVG creator skill's task-selection/project workflow.
Existing generator provenance was checked from `problem_data.json`, `ordered_problem_data.json`,
`lect09e-tetrad_visuals/figure_sources.json`, `lect09_tetrad_concepts/figure_sources.json`, and
LECT08/09 review notes. This supports retaining suitable original-generator captures rather than
misclassifying every embedded bitmap as imported textbook artwork.

## Verified checks and exact commands

From repository root, using the required Python environment:

```bash
source source_me.sh && python3 _temp/genetics_visual_renewal/linkage/classify.py
source source_me.sh && python3 _temp/genetics_visual_renewal/linkage/verify_science.py
```

Both passed. classify.py checks exact 181-row coverage, preservation of every original field
except the intentionally updated disposition, complete nonempty decisions, and one preview file
for every asset. It writes classification.csv, USE_ANCHORS.md, DUPLICATES.md and summary.json.

verify_science.py independently calculates the native-table recombinant sets, w/m and b/vg
counts, crossover denominator, chi-square source value, all saved unordered pair classifications,
ordered-spore pair/allele totals and FDS/SDS counts, and six possible random orders. It checks
source examples, not any future replacement geometry. It exposed one real rounding discrepancy:
LECT08D AB is 499/2100 &#215;100 =23.7619%; source says23.7. The final calculation's image use067 is
marked source clarification needed. Preserve the source value pending instructor direction;
the table's eight rows and other pairs remain unambiguous.

## Trial and ownership requirements for implementation

No new artwork or native source repair was made in M1. BRIEFS.md specifies bounded trials for
four-chromatid crossover connectivity, mitotic segregation, tetrad DCO alternatives, ordered
meiosis, recognizable fly trait comparisons and theoretical mapping curves. Dense scientific
illustrations were not retained simply because they are difficult. The mapping curve is
identified as theoretical, with source model assumptions; verify equations before plotting.

Shared source physical owners must be assigned separately. DUPLICATES.md lists every global
inventory consumer sharing each reused hash; classification.csv marks consumers outside this
batch. L02 cis/trans is already assigned to M2 by the manager, including 08C's duplicate raster.
Subsequent M3 ownership must wait until M2 releases those same physical files.

## Verification limits

No LibreOffice invocation, fresh lecture export, Impress playback, source edit/save/reopen,
base pytest run, external research verification, or new visual-family trial was performed here.
The original images and source context were reviewed directly; this report does not claim
lecture-scale layout acceptance or independent implementation/specification review. Future
exports must be scheduled centrally and run outside the sandbox through repository scripts.
Actual retained micrographs/photos and generator captures are identified explicitly in briefs;
no scientific image was replaced or source asset deleted.
