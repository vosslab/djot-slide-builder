# Plan: Three chromosome animations for Genetics

## Goal and context

Create three standalone animated WebPs using the chromosome API. Use C66 Robertsonian fusion for
the third clip. Its key visual is the difference between the large chromosome that remains and the
small short-arm product that is usually lost. C55 remains deferred.

## Design philosophy

Keep colors tied to chromosome material as it moves. Pause at each important change so students
can trace the pieces and read the result.

## Scope

| Slide | Animation | Steps |
| --- | --- | --- |
| C01 | Insertional translocation | Mark the cuts around **EF** and between **L** and **M**. Move **EF** from the blue donor into the green recipient. Hold on **ABCDGH** and **JKLEFMNO**, with white zigzags marking the new joins. |
| C22 | Single crossover | Bring the two inner nonsister chromatids together between the marked loci. Exchange their tips and ease the arms apart while each sister pair stays joined at its centromere. Hold on parental **ab** and **++** and recombinant **a+** and **+b**. |
| C66 | Robertsonian fusion | Start with the blue and red acrocentric chromosomes from C66. Mark the breakpoints near their centromeres. Rotate one long arm so the long arms meet at their cut ends. Show the fused chromosome with one active centromere and hold long enough to see the separate short-arm product. Then fade that product while explaining that it is usually lost. |

Use a fixed 1200 by 720 transparent canvas, explicit Atkinson Hyperlegible Next and Mono fonts,
and short step captions. Target 6 to 9 seconds per loop with a two-second final hold.

## File scope

| Path | Change |
| --- | --- |
| `prototype/make_chromosome_animations.py` | Generate all three clips from chromosome models. Base C66 on the existing LECT13D fusion recipe. |
| `prototype/make_chromosome_engine_mini2.py` | Share C01's model and cut definitions and C22's crossover pose. Preserve the static SVGs byte for byte. |
| `prototype/assets/chromosome_animations/` | Keep the generated `c01_insertional_translocation.webp`, `c22_single_crossover.webp`, and `c66_robertsonian_fusion.webp` with the prototype assets. |

## Milestones

| M | Title | Summary | Goal |
| --- | --- | --- | --- |
| 1 | Render the steps | Use the existing topology operations and renderer. Check the final gene orders in C01 and C22. Verify that C66 conserves the input material before the fade and that the fused chromosome retains two centromere sites with one active. | Make each operation traceable without adding a public animation API. |
| 2 | Export and review | Rasterize SVG frames with `rsvg-convert` and encode with Pillow. Decode each WebP to verify frame timing, alpha, and loops, then watch all three in headless Playwright Chromium on light and dark backgrounds. Run focused chromosome tests and compare regenerated static SVGs with their originals. | Deliver three reproducible clips with readable labels and clear results. |

```bash
source source_me.sh && python3 prototype/make_chromosome_animations.py
```

*Plan created with `vosslab-skills:modest-plan-drafter`.*
