# Chromosome engine Mini2 execution ledger

The ten figures, deck, and native exports passed initial acceptance against the approved
[chromosome_engine_mini2_plan.md](../chromosome_engine_mini2_plan.md).

## Current revision

| Figure | Requirement | Specification review |
| --- | --- | --- |
| C01 | Leave one telomere-cap length of visible chromosome body between the centromere collar and the nearest gene card on each side in the shared renderer. | `c01_gap_review` |
| C16 | Use horizontal sister caps. | `c16_tips_review` identified the issue, `c16_cap_correction` corrected it, and `c16_cap_rereview` verified both edges of all 28 caps are horizontal and all 42 glyph instances are present. |
| C22 | Lengthen chromosomes by 15.1%. | `c22_length_review` |
| C25 | Lengthen chromosomes by 20%. | `c25_length_review` |
| C28 | Use Atkinson Hyperlegible Next with a sans-serif fallback. | `c28_font_review` |
| C31 | Flank bands with gray and use deep purple for the G bands. | `c31_bands_review` |
| C55 | Space loci at equal arc-length intervals and draw a new smooth loop. | `c55_spacing_review` |
| C61 | Restore the original lavender and plum. | `c61_palette_review` |
| C63 | Slim the centromere collars and expose more of the arms. | `c63_proportion_review` |

`mini2_revision_visual_quality` accepted the native PNGs for C01, C22, C25, C28, C31, C55, C61,
and C63. `c16_cap_visual_quality` accepted the final native page 2 and its cap close-up.
C23 is a source question only. Its source is slide 40 of the original LECT08B.

The base pytest suite passed 9,920 tests in 24.98 seconds (`revisions/pytest.log`). Strict Djot
lint passed all 83 slides across Mini2 and the full review. The full review's 73-slide ODP and
PDF were rebuilt and verified with the C22 and C31 revisions. `mini2_revision_integration`
accepted the revision after confirming that all ten regenerated SVGs matched the canonical
assets, both ODPs embedded the canonical C22, C23, and C31 SVGs byte for byte, the export
hashes matched, and the C23 source was correct.

Seven other reviewed pages matched pixel for pixel after the C16 re-export. A later C28 revision
brought the sisters together under each collar and retained both exchange points. The revised
collar footprints cover the chromatid outlines through both centromeres. The exported page 6
render and all 12 Atkinson allele labels were verified.

C31 now has 25 aligned bands on 444-unit chromatids, with one gray for unstained regions and
a stain-colored label for each view. The shared renderer combines consecutive same-color strokes
while preserving each region's identity and anchors. C31's `c31.svg` uses one opaque lossless
band-color image per chromatid to remove separate band paint operations in the PDF. Both decks
embed that SVG. The base suite passed 9,919 tests (`c31-bands/pytest-final.log`).

C55's blue path now follows the original lecture's omega-shaped loop. Five guides connect all
matching loci, including A and E on the flanks. Both paths measure 1,130 SVG units and retain
equal corresponding distances between loci. The exported page 8 and 42 focused tests passed.

C63 uses whole-chromosome DNA length estimates of 41.8 Mb for X, 40.9 Mb for Y, and 60.8 Mb
for chromosome 2. The exchange breakpoints and loci remain schematic. X is Dark orange Dark,
Y is Navy Extra dark, and 2 is Lime green Light. The six gamete pairs carry 12 labeled
centromeres and share a 10 Mb scale bar. [Hoskins et al., Fig. 1](https://doi.org/10.1186/gb-2002-3-12-research0085)

The `c63-drosophila/` checks verified page 10 visually and confirmed native ODP captions,
canonical SVG embedding, and selectable PDF captions across Mini2. The base suite passed
9,919 tests.

C01 uses five extra-light gene-card fills. The enlarged chromosomes give L a full card
beside the insertion, with body color before the splice. Both rows start with 485 + 390
units and conserve 875 units across their products. The source interval check also runs
for the C61 and C63 exchanges. The `c01-clearance/` checks verified all eight C01
chromatids, the exported page 1, and the SVG embedded in the ODP. The base suite passed
9,921 tests.

C22 uses straight terminal runs on two mirrored crossover curves and one centromere
collar per sister pair. All four middle-panel chromatids still measure 313 units along
their paths. The `c22-tips/` checks verified both edges of each cap, the Mini2 and full
review exports, and pixel-identical C25 artwork. The base suite passed 9,921 tests.

| Current export | SHA-256 |
| --- | --- |
| `output/odp/chromosome_engine_mini2.odp` | `7645ae4240bc6c3e8497568da59fe45300019e85cf14a3ecb9f7858c64e81328` |
| `output/pdf/chromosome_engine_mini2.pdf` | `e451c2b362b859a7690ac75cc83afdfe75b1838a5c3db873803b527b33bbf977` |

## Historical figure acceptance

Each owner produced a recipe fragment and rendered preview in
`_temp/chromosome_engine_mini2/`. At initial acceptance, all ten approved previews matched
the canonical SVGs byte for byte. The C16 and C31 entries below record the initial proofs.

| Figure | Owner | Initial proof | Specification reviewer | Quality reviewer |
| --- | --- | --- | --- | --- |
| C01 | `c01` | `c01.svg` | `c01_spec` | `c01_quality` |
| C16 | `c16` | `c16.svg` | `c16_spec` | `c16_quality` |
| C22 | `c22` | `c22.svg` | `c22_spec` | `c22_quality` |
| C23 | `c23` | `c23.svg` | `c23_rereview` | `c23_quality_final` |
| C25 | `c25` | `c25.svg` | `c25_spec` | `c25_quality` |
| C28 | `c28` | `c28.svg` | `c28_spec` | `c28_quality` |
| C31 | `c31` | `c31.svg` | `c31_spec` | `c31_quality` |
| C55 | `c55` | `c55.svg` | `c55_spec` | `c55_quality` |
| C61 | `c61` | `c61.svg` | `c61_spec` | `c61_quality` |
| C63 | `c63` | `c63.svg` | `c63_spec` | `c63_quality` |

C01's reproducibility check asserted both product orders. C23's final reviews accepted the
corrected bridge. C28 used the original lecture raster
`genetics/LECT09/djot/assets/lect09b-tetrads_1_introduction/image_019.png` for the poses and depth.

The revised C16 passed `c16_curve_spec` and `c16_curve_quality`. Its 42 reused chromosome glyph
instances show 84 gently curved sister bodies. The mirrored paths restore the source's visual
profile with an exact 10:1 end-to-waist centerline spacing ratio and one common belt per pair.
The SVG hash for that revision begins `8a40837ce40860f1`.

The revised C31 passed `c31_reference_spec` and `c31_reference_quality`. A fully colored reference
at left points to three separate stains with three arrows. The four aligned sister pairs share
15 irregular intervals each. The shortened native caption fits the slide without a capacity warning.
The SVG hash for that revision begins `735f8139b10a04f0`.

## Historical integration and checks

| Check | Acceptance evidence |
| --- | --- |
| Renderer | `mini2_renderer_spec` and `mini2_renderer_quality` accepted keyword-only `texture=True`. The focused regression confirmed that disabling texture preserves sheen. Pyflakes and 58 focused chromosome tests passed. |
| Djot deck | `mini2_deck_spec` accepted ten ID-ordered slides with one figure and a native caption each, including the initial caption correction. Eight Djot lint tests passed. |
| Canonical recipe at initial acceptance | `mini2_integrator` assembled `prototype/make_chromosome_engine_mini2.py`. All ten initial SVGs matched their reviewed proofs and two scratch runs byte for byte. The log records SVG IDs, references, and accessibility labels. |
| Strict native Djot lint | One source, ten slides, and ten images passed. |
| Final base test suite | `source source_me.sh && python3 -m pytest tests/` passed all 9,919 tests in 25.05 seconds. |
| Final native builds | Mini2 (10 slides) and the full chromosome review (73 slides) exported to ODP and PDF without capacity warnings. |
| Final Mini2 native artifacts | `mini2-native-check.log` verifies all ten ID-ordered native ODP captions, ten byte-identical embedded SVGs with SVG MIME entries, and selectable PDF captions. |
| Rendered PDF | At initial acceptance, the manager and independent reviewer `mini2_integration_review` accepted all ten pages, including C23's sheen, C55's locus matches and overpass, and C63's six combinations. C55's overpass outline is faint at high zoom. Final C16 and C31 review is recorded above. |
| Final fonts | All 236 SVG text elements directly declare Atkinson Hyperlegible Next. Their 155 spans inherit it. The ten-page Mini2 PDF uses Atkinson Hyperlegible Next and IBM Plex Sans Condensed. |

The evidence is in `_temp/chromosome_engine_mini2/`, including `integration-verification.log`,
`integration-djot-lint.log`, `mini2-pytest-final.log`, and `mini2-native-check.log`.

## Prototype cleanup

C13 and C21 share their existing artwork. The two review decks share the C22, C23, and C31
SVGs. Cleanup removed 19 superseded prototype files (16 SVGs, two stale exports, and one old
recipe), totaling 95,479,962 logical bytes. The original course artwork used as a source
remains in place.

## Historical export hashes

| Artifact | SHA-256 |
| --- | --- |
| `output/odp/chromosome_engine_mini2.odp` | `337ed18be4ce1b91e1f0f95942c86636dc8c10ad6dccd92b2a080df4173302ae` |
| `output/pdf/chromosome_engine_mini2.pdf` | `34d48f62d79f0d8ab41ef85e43e184b8ee224fef578c950dff35ab77fc195513` |
