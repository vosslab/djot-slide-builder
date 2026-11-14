# Array toolkit pilot: figure quality review

**PASS** for fidelity to the existing array workflow figure at the supplied 500 x 235 pixel panel preview. This is a figure review; native slide placement and export remain for M25.

Reviewed the recipe `svg_tools/examples/array_comparison.py`, current toolkit SVG, existing `array_comparison_workflow.drawn.svg`, and the LECT11D slide context. At 500 x 235, `_temp/svg_toolkit/array_pilot/toolkit.webp` and `original.webp` show the same composition, colors, proportions and readable labels. The smallest array captions are small at this size but remain legible in the preview and match the original. The new downward arrowheads are somewhat longer; their direction and associations remain clear. Both CGH lines still converge on the combined array; separate reference and test arrays remain on the SNP side. The adjacent original measured copy-number trace is still referenced in the slide.

The new SVG has all 11 substantive labels from the existing figure, three arrays and 36 spots (12 per array). Both method names and the indirect/direct comparison labels are retained. The recipe's generated `reproduced.svg` is byte-identical to the current toolkit SVG. The consumer contains exactly one toolkit URL; replacing it with the old URL restores every byte of the captured pre-pilot consumer snapshot. This compares to that captured snapshot, not an independently reconstructed initial project state.

Current SHA-256 evidence:

- Recipe: `c28881036a3fef52550380bae659e1b0fbadf276f5173fd5d34a026191a4516e`
- Toolkit SVG: `6d4bee7bba591e82c7a8142610894ddce493ad93e710bb4c93e42414ae4c596a`
- Existing SVG: `b739fac24f49ab7009298acf2a6dbbffd44dfdfef45ab7559a038c1582663f64`
- Current consumer: `ee4606b5aaa1c4ec1469e8e5d488baae6af8734bac07aaa57fcbf37192711c01`
- Captured pre-pilot consumer: `5873a4608fbe846fd38636be00044cbbab5e5206c7acf8017ec084e5fd9db4bd`
- Toolkit and original preview WebPs: `fe67517656383b93c5e7b2e286377272ac738192d0e75cf9b6872fc60d5959fa`, `a9227f150cb847f44d3927c85043c4841595421344c4610bf381372da544f0a0`.

Limit: this review checks fidelity to the existing schematic, not independent experimental validation of the biology, and does not assess a LibreOffice-rendered slide or presentation display.
