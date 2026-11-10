# LECT12 M1 evidence and limits

Saved workstream evidence for [genetics_visual_renewal_plan.md](../active/genetics_visual_renewal_plan.md).
Source owner: `/root/classify_phylogenetics`.
Local source: `_temp/genetics_visual_renewal/phylogenetics/EVIDENCE.md`. This is a saved snapshot;
see [genetics_visual_renewal_progress.md](genetics_visual_renewal_progress.md)
for current authorization, dependencies and acceptance status. Scratch paths remain local.
Non-ASCII source characters use numeric HTML character references.

Date: 2026-11-09. Reviewer scope: all original `root_deck` paths containing `/LECT12/` in
`_temp/svg_migration_research/experiments/image_inventory.csv`. Canonical sources were read only.

## Coverage

106/106 original uses classified; 60/60 unique asset paths visually reviewed; one hidden use
(the historical NWS weather panel). All original columns remain in order; former disposition
is preserved separately as `inventory_disposition`. A row-order comparison asserts equality
of every original field except the intentionally updated disposition. No inferred missing-
geometry items were added to the original inventory.

| Disposition | Uses |
| --- | ---: |
| original SVG redesign | 34 |
| native-content repair | 52 |
| retain with reason | 15 |
| source clarification needed | 5 |

No `already suitable` row is used: existing suitable primate SVGs need surrounding native
layout repair, and native-table captures need actual table reconstruction. This does not mean
those SVG internals are defective. See each reason instead of treating file format as the task.

`coverage.json` stores the assertions/counts. `write_handoff.py` reproduces classification from
the manually reviewed asset decisions; it is a scratch reporting helper, not production code.
Every reviewed asset's current SHA-256 matched its original inventory hash at final check.

## What was inspected

- All 60 assets rendered or opened through Pillow/librsvg, indexed by `asset_index.txt`.
- `contact_1.jpg` through `contact_5.jpg`: five contact sheets, 12 assets each, white backing
  and stable IDs. All five were visually inspected in this task.
- Enlargements separately inspected for IDs11,13,21,28,29,31,32,34,38,42,45,52,53,54,55,57,60.
  White-background enlargements confirm IDs42 and54 contain no visible artwork. SVG inspection
  confirms42 contains an empty clipped group and54 a transparent embedded PNG.
- Enclosing physical-source slide text read for every use, including all shared included sources.
  `image_contexts.txt` preserves enclosing LECT12 slide blocks and original root slide/line IDs.
  Repeated figure uses were read with their distinct prose and question/answer stages.
- Original PDF pages rendered under `renders/original_*`. Original C44,45,48 and E5 were
  visually inspected for source matrix/sequence arrangement, masking, and exact annotation
  targets. This proves original C45 only shows Hu/Ba, whereas imported current Djot shows the
  complete tree. C48 shows three separate pairs. Original E5 positions the missing Adh labels.
- Original C PDF p8-15 and25-26 text extracted live to verify matrix and arithmetic conflicts
  predate conversion. The initial raster matrix was read enlarged through asset36/contact4.
- Original `LECT12_REVIEW.md` and `LECT12_SOURCE_MAP.md` consulted for conversion losses and
  source order. Existing review says C has26 source animation elements; this review does not
  certify their playback.

No LibreOffice command was launched. Standalone SVG renders are classification evidence;
they are not proof of the eventual presentation/export quality. Existing PDFs were read via
PyMuPDF only.

## Consequential decisions, isolated from ready tasks

1. **Five-taxon worked lesson:** original C4 &#8220;Another Example&#8221; gives ac21,ad31,ce39,de43;
   original C8 &#8220;Find smallest value&#8221; and subsequent repeated native tables give20,30,35,40.
   Original C10 even contains asymmetric AD31/DA30, while the equation uses30. Original
   C10-12 explicitly use `(20+30)/2=25`, `(30+34)/2=32`, `(23+21)/2=22`, so later native
   inputs have stronger support from the source's own calculations than the single opening
   raster. This discrepancy is not an import artifact.

   Original C15 &#8220;Merge &#8216;(a,b)&#8217; and &#8216;e&#8217;&#8221; prints `25+35=30` for averaging a two-species cluster
   with one species, also omitting the division symbol. Giving each of the three species
   equal weight gives `(20+30+35)/3=28.333...`, and the analogous d value is104/3. Final
   intercluster distance becomes31.5 and root height15.75, instead of33/16.5 in original
   C25/26. `five_taxa_check.json` records independent all-cross-pair calculations.

   Recommendation sent to manager: keep the repeatedly worked native input dataset; correct
   the stray opening matrix and asymmetric cell; obtain instructor direction on correcting
   subsequent arithmetic/tree for UPGMA versus explicitly describing the existing equal-
   cluster procedure. Classification remains source clarification pending that answer.

2. **Dense UPGMA overview:** B image021 and image023 start from matching A-G inputs but
   disagree on reduced values and final heights18.2 versus17.0. Image023 supports direct
   size-weighted checks. Do not mix the two diagrams into one &#8220;faithful&#8221; sequence.

3. **Neighbor-joining label:** B image024's selected AB7 is not the raw distance minimum
   (BC5 and CD5 exist), although NJ's adjusted criterion can choose it. Preserve numbers;
   research/resolve `Min(Dij)` meaning before redrawing the arrow or method explanation.

4. **C textbook appendix method name:** headings say Neighbor Joining while the illustrated
   half-distance hierarchy uses averaging and equal terminal heights. Preserve the actual
   source calculation/reveals while manager resolves the label. This need not block restoring
   missing masks or native tables.

5. **Homology wording:** source definitions tie orthology/paralogy too strongly to retained/
   changed function. Geometry can preserve the duplication/speciation examples while the
   manager separately handles the biological wording decision.

These are bounded source questions; they do not block B rotation/topology, D native matrices,
allele-sorting trial, parsimony, and E conceptual diagram trials.

## Ownership and companions

`shared_sources.json` lists every original-inventory consumer of shared physical sources:
`evergreen/youtube_channel.djot`, `genetics/evergreen/course_information.djot`, and
`evergreen/spring_registration.djot`. B/C split fragments are included by their respective
master roots. The same allele-sorting image and hemoglobin alignment appear as separate
physical asset copies across B/C/E: coordinate content contracts, and let each physical file
have one owner. All edits for the six B/C fragments, D/E files and shared sources need explicit
manager assignment; multiple concept IDs do not grant multiple simultaneous source editors.

Ready M3 packages by physical owner:

- B part01: topology/vocabulary; primate layout and two redraws; hemoglobin alignment;
  parsimony; Bayesian scratch trial; selection scratch trial. Coordinate around M2 rotation
  owner. Hold only disputed overview/NJ-label concepts for source decisions.
- B part02: native prompt/metric tree exercise and connected missing rhino tree geometry.
- C part01: allele-sorting trial and missing Hartl tree; hold five-taxon arithmetic changes.
- C part02: native21-distance matrix/math plus eight staged tree states, preserving original
  masks. Coordinate with manager on method naming.
- D: six native matrix states, staged tree companion, original calculation and highlight order.
- E: shared alignment; allele-sorting reuse; empirical Adh annotation repair; homology trees;
  subfunctionalization scratch trial. Retain rate-plot evidence with source-data limits.

For durable dispatch, copy `classification.csv`, `BRIEFS.md`, `EVIDENCE.md`, `asset_index.txt`,
`coverage.json`, `shared_sources.json`, `five_taxa_check.json`; retain links to `image_contexts.txt`,
contact sheets and `renders/` as visual evidence. The reports are sufficient for ownership and
scope, while visual implementers still require canonical assets and original PDFs. No fresh
implementer should rely on contact sheets alone for exact text/data transcription.

## Unperformed checks and risks

No canonical replacements, actual new lecture exports, full test suite, attended Impress
playback, native-table edit/reopen, or classroom acceptance occurred in M1. Complex-family
trials are mandatory next tasks specified in the briefs, not completed drawings. External
plot datasets and historical Google Sheet access were not researched. The preserved empirical
figures therefore remain evidential rasters, with no invented values. Memory search returned
no relevant lines and did not inform classifications.
