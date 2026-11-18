# Plan: Build the second chromosome engine review deck

## Goal and context

Create a ten-slide prototype for reviewing chromosome engine figures in native ODP and PDF. Use
the first [chromosome_engine_mini.djot](../../prototype/chromosome_engine_mini.djot) deck as the
layout precedent, with one figure and a native caption on each slide.

## Design philosophy

Use the existing chromosome topology and painter to make the changes in chromosome structure and
inheritance visible at slide size. Add one renderer option where C31 needs separate control of
texture and sheen.

## Scope

- **C01** starts with `ABCDEFGH` and `JKLMNO`. Show moving `EF` in one row, yielding `ABCDGH`
  and `JKLEFMNO`, and exchanging `GH` and `NO` in the other, yielding `ABCDEFNO` and `JKLMGH`.
  Assert both product orders and show zigzags at the joins.
- **C16** shows genomes A, B, and D across groups 1-7. Draw two homologs per genome and group,
  each as two independently drawn, gently curved cubic sister paths mirrored like the source,
  with a common centromere belt. Reuse one visual glyph and named palette hue for all
  chromosomes in each numbered group.
- **C22** replicates `ab` and `++` and shows one exchange between nonsister chromatids between
  the loci. Show products `ab`, `a+`, `+b`, and `++`, with two visible zigzags.
- **C23** cuts the same two nonsisters at approximately 24% and 76% and exchanges the middle
  segment containing the centromere. Meiosis I sorts by centromere and meiosis II separates
  sisters. Show two solid parental products and two reciprocal products with three color runs
  each. Keep the sheen visible.
- **C25** starts with `aB` and `Ab` and shows a proximal crossover. Show the two alternatives
  for daughter pairs: `aB`/`Ab` in both daughters, or `aB`/`aB` and `Ab`/`Ab`.
- **C28** uses the original lecture raster for the four independent brown and ochre poses and
  their depth (`genetics/LECT09/djot/assets/lect09b-tetrads_1_introduction/image_019.png`). Show the
  inner pair crossing first and the outer pair later. Keep the circular ascus with `Ab` twice and
  `aB` twice.
- **C31** uses replicated sisters and the same uneven intervals across four aligned pairs. The
  fully colored reference at left overlays the regions highlighted by three separate stains.
  Three explicit arrows lead to the G-, R-, and C-banding views. Keep purple on light gray for G,
  complementary yellow on dark gray for R, and teal on light gray at the centromere for C.
  Thread a keyword-only `texture=True` through `render` and the existing painter so this figure
  can set `texture=False` and retain sheen.
- **C55** compares `ABCDE` and `ADCBE` beside a larger pairing loop. Reverse `BCD`, connect
  matched loci with guides, and keep the centromeres outside the inversion.
- **C61** exchanges the tips of chromosomes 9 and 22 on a common scale. Use wide before and
  after columns and larger chromosome bodies. Label derivative 22 explicitly.
- **C63** shows six distinct pairs with space for `rb+`, `dp+`, and `dp`. Draw Adjacent-1 as
  1+2 and 3+4, Adjacent-2 as 1+3 and 2+4, and Alternate as 1+4 and 2+3. Use 1 for derivative X,
  2 for normal 2, 3 for normal Y, and 4 for derivative 2.
- Declare Atkinson Hyperlegible Next directly on each SVG text element and let its spans
  inherit the font.

## File scope

| File or directory | Intended change | Canonical source, for generated output |
| --- | --- | --- |
| `prototype/chromosome_engine_mini2.djot` | Ten slides in ID order with native captions | |
| `prototype/make_chromosome_engine_mini2.py` | One recipe for the ten figures | |
| `prototype/assets/chromosome_engine_mini2/*.svg` | Ten generated figures, with an opaque band-color strip in `c31.svg` | `prototype/make_chromosome_engine_mini2.py` |
| `svg_tools/chromosomes.py` and `tests/test_chromosome_render.py` | Renderer option and focused regression check | |
| [CHANGELOG.md](../CHANGELOG.md) | Record the second prototype and renderer option | |
| [chromosome_engine_mini2.md](workstreams/chromosome_engine_mini2.md) | Execution ledger and evidence | |

## Milestones

| M | Title | Summary | Goal |
| --- | --- | --- | --- |
| 1 | Draw and review | Produce ten source recipes and previews. Verify biological specifications before reviewing legibility and layout. | Each figure passes both reviews. |
| 2 | Integrate | Assemble the recipe and Djot deck, generate all ten SVGs, and review the combined result independently. | The normal entry points reproduce the figures and the ordered deck. |
| 3 | Verify and export | Run pyflakes, Djot lint, chromosome tests, and the base pytest suite. Build ODP and PDF outside the sandbox. | Inspect all ten PDF pages and verify the ODP embeds ten SVGs and native captions. |

*Plan created with `vosslab-skills:modest-plan-drafter`.*
