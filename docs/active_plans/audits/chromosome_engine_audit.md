# Chromosome engine code audit

November 18, 2026. All six independent review passes completed on the working sources for
C18, C20, C29 and C66. The engine supports general operations on linear chromosome material.
For example, a paracentric inversion in one sister can reverse two loci while preserving both
chromatid lengths, the source of each interval and the shared active centromere.

## Findings

1. **Medium, open for strongly bent sister pairs.** The automatic pair translates both bodies
   along the normal at the centromere. The separation between centerlines on the arms can
   approach zero as the tangent rotates. A 280-unit U-shaped pose at width 12 had 14.4 units
   between centers at the belt, but less than 0.06 units between sampled arm centerlines.
   This can hide one chromatid. The guide now advises separate poses for deep bends.
   Independent sister poses with a common belt would be a useful next extension when a figure
   needs that geometry. [Renderer](../../../svg_tools/chromosomes.py)
2. **Medium, fixed for balanced rearrangements.** A sister pair of length 123.4 with an
   inversion from 12% to 17% in one sister carried the same centromere at 82%. The two
   projections calculated 101.188 and 101.18800000000002. Exact equality rejected the pair.
   The renderer now allows the same two units of floating-point rounding used for material
   cuts, and still matches the source and site identifiers exactly. The example renders with
   the two loci reversed in one sister. Removing the interval still rejects the unequal pair.
   [Topology](../../../svg_tools/chromosome_topology.py) and [renderer](../../../svg_tools/chromosomes.py)
3. **Low, figure regeneration.** The four selected compositions ran with reads of SVG and XML
   files denied. C18 and C66 also have batch entrypoints that rebuild template-based siblings.
   The C20 batch reads a JSON file containing the wide panel's structured data and the
   portrait sibling's SVG. The wide panel function consumes only its structured record.
   C66 now accepts an output directory directly so its isolated build needs no prior batch
   initialization. C20 now resolves its files from the checkout root. The old local C18 and
   C29 template artworks are unused by the selected branches. Earlier source evidence and
   unrelated siblings were preserved. [C18](../../../genetics/LECT06/djot/make_chromosome_xlinked.py),
   [C20](../../../genetics/LECT08/djot/chromosome_recipes/cis_recipe.py),
   [C29](../../../genetics/LECT09/djot/make_centromere.py) and
   [C66](../../../genetics/LECT13/djot/lect13d_chromosome_recipes.py)
4. **Low, test maintenance and wording.** Sister tests now check that the belt paints over the
   bodies and callouts paint over the belt, independently of the number of outer SVG groups.
   A redundant direct-child path assertion was removed. The changelog now describes source
   genes and copy-specific centromere activity accurately.
   [Renderer tests](../../../tests/test_chromosome_render.py) and [changelog](../../CHANGELOG.md)

## Review decisions

| Pass | Disposition |
| --- | --- |
| Plan | Clarified the one-active-site-per-sister limit in the plan. Retained the authorized native deck check and C31 paragraph-break fix. The target figures were judged for biology and legibility. Hash checks protect unselected artwork and identify which SVG actually reached the slide. |
| Test | Trimmed incidental XML structure assertions. Retained the five suggested temporary cases because they exercise demonstrated crashes or paint defects at curved junctions, crowded labels and rounded region boundaries. No new permanent tests proposed. |
| Style | No independent findings. The topology model is standard-library Python, numeric poses feed one spline implementation, and both renderer entrypoints reuse the BPQ painter. |
| Docs | No independent findings. Added the curved-pair limitation found in the coordinator's unfamiliar-pose probe. |
| Legacy | Confirmed the remaining active template readers serve other figures. Documented the unused local templates and checked selected compositions separately from the lecture batches. |
| Comment | Corrected the changelog wording on gene ownership. |

## Verification

The focused topology, spline and render suite passed all 37 checks. Temporary probes also
exercised the balanced inversion, an unequal deletion, and all four composition branches with
source artwork reads denied. All four regenerated SVGs matched the published prototype assets.
The standalone [four-slide deck](../../../prototype/chromosome_engine_mini.djot) embeds those
assets in C18, C20, C29, C66 order. Each ODP page contains the matching SVG and native caption,
and all four exported PDF pages were inspected.

The full `source source_me.sh && pytest tests/` run passed 9,523 tests. The two
line-count advisories were for `svg_tools/chromosomes.py` and `docs/HUMAN_GUIDANCE.md`,
both at 938 lines. Scoped pyflakes passed.

The initial model handles open linear material. Its cut, reverse, copy and join operations
express deletions, duplications, inversions and exchanges. It has no ring closure or general
branched topology. The [authoring guide](../../CHROMOSOME_ENGINE.md) gives runnable examples
for ordinary chromatids, homologs, sister pairs and a terminal exchange.
