# SVG repair backlog

This is the canonical inventory of LLM-drawn SVGs removed from teaching decks because the
replacement lost teaching detail or failed visual review. Keep the drawings at their existing
paths as repair starting points. Record the replacement, source comparison, and reason here.

Initial scope: Genetics LECT10, reviewed November 10, 2026. Eleven drawings have been dropped,
including the four chromosome-shape drawings restored to textbook rasters in the final queue pass.
Slide numbers below refer to the current Djot decks on that date. Original slide numbers identify
the instructor's ODP/PDF under `genetics/LECT10/`.

## Dropped drawings

### Chromosome addresses

| Drawing | Former use | Reason for removal | Repair target |
| --- | --- | --- | --- |
| [chromosome_arm_landmarks.drawn.svg](../genetics/LECT10/djot/assets/visual_renewal/chromosome_arm_landmarks.drawn.svg) | 10C5 and C8, chromosome arms and landmarks | An unbanded schematic replaced banded teaching figures. "Landmarks, not a band map" acknowledged the missing information instead of supplying it. | Preserve visible bands, centromere, arm proportions, and numbered regions/bands needed for the lesson. |
| [cftr_address.drawn.svg](../genetics/LECT10/djot/assets/visual_renewal/cftr_address.drawn.svg) | 10C16, CFTR address answer | The hierarchy diagram lacked the actual chromosome bands needed to explain region 3, band 1, subband 2. | Show 7q31.2 on a banded chromosome with a legible region/band/subband enlargement. |

Current replacements, relative to `genetics/LECT10/djot/`:

- C5: `assets/lect10c-chromo_nomenclature/image_002.png` and `image_003.png`;
  original C2, chromosomes 1-3 and 21-22.
- C8: `assets/lect10c-chromo_nomenclature/image_007.png`;
  original C4, banded chromosomes 11-14.
- C16-17: `assets/lect10c-chromo_nomenclature/image_012.png`;
  original CFTR chromosome-7 band-location figure, alongside the editable answer table on C16.

### Nondisjunction sequence

| Drawing | Former use | Reason for removal | Repair target |
| --- | --- | --- | --- |
| [nondisjunction_1.drawn.svg](../genetics/LECT10/djot/assets/visual_renewal/nondisjunction_1.drawn.svg) | 10D21, meiosis I | The simplified lineage omitted detail from the original progressive comparison of meiosis I and II errors. | Retain both error pathways and the original stage-by-stage teaching relationships. |
| [nondisjunction_2.drawn.svg](../genetics/LECT10/djot/assets/visual_renewal/nondisjunction_2.drawn.svg) | 10D22, meiosis II | The simplified lineage omitted detail from the original progressive comparison. | Distinguish homolog separation from sister-chromatid separation and carry both pathways forward coherently. |
| [nondisjunction_products.drawn.svg](../genetics/LECT10/djot/assets/visual_renewal/nondisjunction_products.drawn.svg) | 10D23, gamete products | The replacement rendered blank in LibreOffice during the earlier review, breaking the sequence. | Render reliably and show all eight gametes across the two pathways, with readable chromosome counts. |

Current replacements, relative to `genetics/LECT10/djot/`:

- D21: `assets/lect10_repaired_figures/nondisjunction_meiosis_i.svg`, original D35.
- D22: `assets/lect10_repaired_figures/nondisjunction_meiosis_ii.svg`, original D36.
- D23: `assets/lect10_repaired_figures/nondisjunction_gametes.svg`, original D37.

These ordinary SVG replacements package the original artwork and reconstructed labels.
Their SVG extension does not identify them as the rejected LLM drawings. The blank-rendering
failure above records the removal decision; it has not been retested in this inventory pass.

### Prenatal sampling

| Drawing | Former use | Reason for removal | Repair target |
| --- | --- | --- | --- |
| [amniocentesis.drawn.svg](../genetics/LECT10/djot/assets/lect10_repaired_figures/amniocentesis.drawn.svg) | 10D54 | The instructor rejected the replacement drawing as an inadequate substitute for the original labeled figure. A particular anatomical error was not established in that review. | Match the original anatomy, needle destination, sample processing, labels, and test-workflow relationships clearly enough for teaching. |
| [chorionic_villus_sampling.drawn.svg](../genetics/LECT10/djot/assets/lect10_repaired_figures/chorionic_villus_sampling.drawn.svg) | 10D55 | The instructor rejected the replacement drawing as an inadequate substitute for the original labeled figure. A particular anatomical error was not established in that review. | Match the original placental sampling routes, anatomy, labels, and downstream workflow clearly enough for teaching. |

Current replacements, relative to `genetics/LECT10/djot/`:

- D54: `assets/lect10d-chromo_aneuploid/amniocentesis_original_labeled.png`, original D28.
- D55: `assets/lect10d-chromo_aneuploid/chorionic_villus_sampling_original_labeled.png`, original D29.

These are 3x raster captures of the complete original figures, including overlaid labels and
credits. The separately imported textbook JPEGs omit those labels.

### Chromosome shapes

The November 10 side-by-side review found clearer teaching relationships in the textbook
figures. The final queue pass restores those original raster figures on B33-36, retaining the
editable titles and existing matching exercise. B32 is the Chromosome Shapes subsection card.

| Drawing | Former use | Repair target |
| --- | --- | --- |
| [centromere_positions.drawn.svg](../genetics/LECT10/djot/assets/visual_renewal/centromere_positions.drawn.svg) | 10B33, Based on Centromere Location | Make replicated chromosome structure, centromeric constriction, arm proportions, and p/q labels as clear as the textbook overview. |
| [metacentric_movement.drawn.svg](../genetics/LECT10/djot/assets/visual_renewal/metacentric_movement.drawn.svg) | 10B34, Metacentric | Show sister-chromatid connection, meaningful spindle attachment, and the V-shaped anaphase configuration distinctly. |
| [submetacentric_movement.drawn.svg](../genetics/LECT10/djot/assets/visual_renewal/submetacentric_movement.drawn.svg) | 10B35, Submetacentric | Preserve unequal arms, short-arm visibility, meaningful spindle attachment, and the J-shaped anaphase distinction. |
| [acrocentric_movement.drawn.svg](../genetics/LECT10/djot/assets/visual_renewal/acrocentric_movement.drawn.svg) | 10B36, Acrocentric | Preserve the very short arm and centromere-led movement while keeping the I-shaped configuration distinct from the other examples. |

Current replacements, relative to `genetics/LECT10/djot/`:

- B33: `assets/lect10b-karyotypes/image_022.png`, original B33.
- B34: `assets/lect10b-karyotypes/image_023.png`, original B34.
- B35: `assets/lect10b-karyotypes/image_024.png`, original B35.
- B36: `assets/lect10b-karyotypes/image_025.png`, original B36.

All four files match the embedded original ODP images byte-for-byte. The rejected SVGs remain
at their listed paths as repair starting points. Restoration evidence:
`_temp/lect10b_shape_restore/`.

The comparison found clearer teaching relationships in the textbook rasters despite their lower
resolution. Temporary side-by-side evidence: `_temp/lect10b_shape_comparison/compare-33.webp`
through `compare-36.webp`. Original B33-36 in `genetics/LECT10/lect10b-karyotypes.odp` and `.pdf`
are the durable comparison baseline.

## Repair and reuse

- Add an entry when a drawing is dropped after a teaching or rendering review. Record its exact
  path, affected deck/title, replacement, reason, and source baseline. Use current deck references
  to distinguish a completed removal from a recommendation.
- Compare a repaired drawing with the original at presentation size. Preserve the biological
  relationships and labels needed to answer the slide's question.
- Build through LibreOffice and inspect the exported PDF. Confirm complete rendering, readable
  labels, useful scale, and the original teaching sequence. Record that evidence before marking
  an entry restored to use.
- Retain the rejection history when a repaired asset returns to a deck; record the repaired
  revision and review date in the same entry.

See [slide-specs/SVG_DIAGRAMS.md](slide-specs/SVG_DIAGRAMS.md) for the asset contract and
[LECT10_REVIEW.md](../genetics/LECT10/djot/LECT10_REVIEW.md) for the dated restoration reviews.
