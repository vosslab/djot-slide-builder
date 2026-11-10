# INH-M2: Pea phenotype and cross sequence

Saved workstream evidence for [genetics_visual_renewal_plan.md](../active/genetics_visual_renewal_plan.md).
Source owner: `/root/classify_inheritance`.
Local source: `_temp/genetics_visual_renewal/inheritance/M2_PEA_BRIEF.md`. This is a saved snapshot;
see [genetics_visual_renewal_progress.md](genetics_visual_renewal_progress.md)
for current authorization, dependencies and acceptance status. Scratch paths remain local.
Non-ASCII source characters use numeric HTML character references.

Status: ready for implementation. D1 authorizes correction of the 04C dominance sentence.
Owner: one implementer owns physical `genetics/LECT04/djot/lect04c-two_principles.djot`
and `genetics/LECT04/djot/lect04d-cross_experiments.djot`. Other concepts in these files
must be coordinated through that owner. Every root consumer is the same named deck.

## Intended inference

Pea flower phenotype can mask a recessive allele; true-breeding parents produce uniform F1
hybrids, and the white phenotype returns among F2 offspring. Preserve recognizable pea
banner, wings, keel, calyx/stem rather than generic radial flowers.

## Exact artwork and states

- 04C `Dominance`, `assets/lect04c-two_principles/image_006.png`: nine flowers in a
  population, with source labels WW/Ww/ww. Preserve each genotype/phenotype association.
  Purple is not proven dominant merely by being more frequent. Adjacent sentence says it is
  'likely dominant' because more common; parent manager was notified. Use the F1 evidence
  to support the dominance explanation under the user-approved D1 correction; document the change.
- 04D `True Breeding`, `image_001.png`: AA purple crossed with AA purple; P/F1/F2 remain
  purple and AA. Portrait right panel beside native explanation.
- 04D `Hybrid Plants`, `image_002.png`: AA purple x aa white -> Aa purple F1; F1 cross ->
  purple AA or Aa and white aa F2. This is an existing overview preceding the experiment
  sequence; preserve its location and role, do not replace the subsequent staged experiment
  with a single overview.
- 04D unheaded experiment, source lines 79/100/127 (see CSV for exact inventory line):
  `image_003.jpg` shows P only; `image_004.jpg` adds F1; `image_005.jpg` adds F2. Keep
  separate static authored states with the same visual anchor. P: true-breeding purple x
  white. F1: all plants purple. F1 self- or cross-pollination. F2: **705 purple-flowered
  plants, 224 white-flowered plants**, observed counts, not exact 3:1 data.
- 04D `Hybrid Cross Terminology`, `image_006.png`: full P/F1/F2 recap in right panel.
  Prefer a tall compact recap for this actual half-width slot; pilot full-width geometry
  should be recomposed before reuse here.
- 04D `Reciprocal Crosses`, `image_007.png`: native cross rows, not SVG prose. Preserve
  WW female x ww male -> Ww and ww female x WW male -> Ww.
- 04D `Testcross`, `image_009.png`: purple unknown PP or Pp x white pp; two predicted
  Punnett outcomes all purple Pp or 1:1 purple Pp:white pp. Keep this P notation even though
  earlier slides use A/a and W/w. The sheep example `image_008.png` is a separate organism
  trial, owned by the same physical source implementer.

## Construction and acceptance

Use authored starting geometry in
`_temp/svg_migration_research/experiments/assets/flowers_botanical.drawn.svg` and
`pea_cross.drawn.svg`. Create distinct `*.drawn.svg` states adjacent to the owning deck's
assets; use semantic groups, live short labels, title/description and self-contained vectors.
Main questions, observations and count statements remain native Djot. Full-width experiment
states are appropriate; side-panel recap needs portrait composition. Preserve source hidden
flags, question states and later answers. Remove broken imported loose-label arrangements
only after their text is represented in the replacement.

Check AA/aa/Aa and PP/Pp/pp outcomes separately; count nine source population flowers;
verify all 705/224 occurrences; prove P-only state contains neither F1 nor F2 and F1 state
contains no F2 count/result. Compare exported pages and adjacent pages through the normal
pipeline, with manager-serialized unsandboxed LibreOffice. Inspect actual smallest slot,
not just standalone SVG. No claim about attended playback follows from static PDF checks.

Scientific/art references: original assets and physical sources above;
`_temp/svg_migration_research/experiments/FINDINGS.md` records inspected botanical sources
and pilot export evidence. PlantNET Pisum and Kew Fabaceae links there support simplified
pea morphology. The original source owns all numerical values and reveal states.

## Other consumers to coordinate

04E `image_001.png`, 04F `image_001.png`, and 05H `image_001.jpg`-`image_003.jpg` repeat
Mendel's cross as separate physical assets; their owning implementers can reuse the accepted
art while preserving each local stage. 05H `image_004.png`-`image_006.png` instead teach
Bateson/Punnett white x white, F1 purple, F2 382 purple/269 white (9:7); they must not inherit
Mendel's 705/224 or 3:1 labels. No inventory consumer outside LECT04-07 shares the exact
physical sources or asset paths.
