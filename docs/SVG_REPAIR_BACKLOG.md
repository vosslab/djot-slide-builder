# SVG repair backlog

This is the canonical report of new SVG content deemed unusable and removed from teaching
decks. The eleven rejected drawings remain at their existing paths as review evidence;
their presence does not mean they are approved for teaching or publication.

Updated November 11, 2026: the instructor's classroom rejection supersedes earlier manager
and artwork-review acceptance, including the prenatal drawings. The fetus looks like a monster
to the instructor: its appearance and recognizability make the drawings unusable. The instructor
also considers them too close to the source artwork and raises a copyright concern. This records
human judgment, not a finding of anatomical pathology or copyright infringement. The original
fallbacks preserve lecture continuity; they are not new original book illustrations or a claim
of publication rights. Human-figure drawing is excluded from the current work.
Prenatal status is **DEFERRED**: convincing human anatomy is beyond the reliable drawing ability
demonstrated here. Preserve the fallback rather than force another weak replacement.

Initial scope: Genetics LECT10, reviewed November 10, 2026. Eleven drawings have been dropped,
including the four chromosome-shape drawings restored to textbook rasters in the final queue pass.
Slide numbers below refer to the current Djot decks on that date. Original slide numbers identify
the instructor's ODP/PDF under `genetics/LECT10/`. Later lecture edits can shift those numbers.
Current work and priorities are recorded in
[genetics_visual_renewal_progress.md](active_plans/reports/genetics_visual_renewal_progress.md).

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

These fallback SVGs package original raster artwork and reconstructed labels. They are neither
the rejected LLM drawings nor completed pure-vector deliverables. The blank-rendering
failure above records the removal decision; it has not been retested in this inventory pass.

### Prenatal sampling

| Drawing | Former use | Reason for removal | Repair target |
| --- | --- | --- | --- |
| [amniocentesis.drawn.svg](../genetics/LECT10/djot/assets/lect10_repaired_figures/amniocentesis.drawn.svg) | 10D54 | The instructor finds the fetus monster-like and unusable. The drawing also looks too close to the source artwork, raising a copyright concern. This supersedes earlier review acceptance. | Deferred: human-figure drawing is excluded from current work. Any future independent composition must clearly explain the needle destination, sample processing, and test workflow. |
| [chorionic_villus_sampling.drawn.svg](../genetics/LECT10/djot/assets/lect10_repaired_figures/chorionic_villus_sampling.drawn.svg) | 10D55 | The instructor finds the fetus monster-like and unusable. The drawing also looks too close to the source artwork, raising a copyright concern. This supersedes earlier review acceptance. | Deferred: human-figure drawing is excluded from current work. Any future independent composition must clearly explain placental sampling routes and downstream workflow. |

Current replacements, relative to `genetics/LECT10/djot/`:

- D54: `assets/lect10d-chromo_aneuploid/amniocentesis_original_labeled.png`, original D28.
- D55: `assets/lect10d-chromo_aneuploid/chorionic_villus_sampling_original_labeled.png`, original D29.

These are 3x raster captures of the complete original figures, including overlaid labels and
credits. The separately imported textbook JPEGs omit those labels. On November 11, the current
70-slide deck places Amniocentesis on D55 and CVS on D56, between the D54 testing table and
D57 PUBS. The rejected SVGs remain source evidence only; no new prenatal drawing is assigned.
The attempted PNG-to-WebP fallback conversion was fully rolled back: source preimage and index
restored, as recorded in `_temp/undo_prenatal_raster_conversion/HANDOFF.md`. A fresh fallback
deck build is lecture maintenance evidence only, not SVG completion.

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

- B33: `assets/lect10b-karyotypes/centromere_positions.drawn.svg`, new original drawing accepted
  November 11 through artist/manager review at 900 pixels. Original B33 `image_022.png` is retained.
- B34: `assets/lect10b-karyotypes/metacentric_movement.drawn.svg`, new original drawing
  accepted November 11 through artist/manager review at 900 pixels. Original B34
  `image_023.png` is retained.
- B35: `assets/lect10b-karyotypes/submetacentric_movement.drawn.svg`, new original drawing
  accepted November 11 through artist/manager review at 900 pixels. Original B35
  `image_024.png` is retained.
- B36: `assets/lect10b-karyotypes/acrocentric_movement.drawn.svg`, new original drawing
  accepted November 11 through artist/manager review at 900 pixels. Original B36
  `image_025.png` is retained.

The four retained source rasters match the embedded original ODP images byte-for-byte. The
rejected SVGs remain at their listed paths as evidence. Historical raster restoration evidence:
`_temp/lect10b_shape_restore/`.

The new B33 drawing is a separate asset, not a revision of the withdrawn SVG. Its continuous
sister contours, paired centromeric joins, contrasting arm proportions and nine exact live labels
passed artist and manager review. One URL substitution preserves every other Djot byte;
XML/ASCII/pure-vector checks passed. Evidence: `_temp/centromere_overview_original_svg/`.
This source integration follows the current master plan; existing ODP/PDF outputs update during
the normal course build.

The separate new B34 drawing restores a clear sister join, paired outward spindle
attachments and two centromere-led V-shaped daughters within one anaphase cell.
Artist and manager accepted the direct 900-pixel preview. XML/ASCII/pure-vector checks
and one-URL inverse-byte proof passed; evidence is `_temp/metacentric_movement_original_svg/`.
B35 now has a separate original J-shaped movement drawing, accepted at 900 pixels with
XML/ASCII/pure-vector and one-URL inverse-byte checks. Evidence:
`_temp/submetacentric_movement_original_svg/`. B36 now has a separate original I-shaped
movement drawing with visible short lower tips; the same artist/manager, structural and
inverse-byte checks pass. Evidence: `_temp/acrocentric_movement_original_svg/`.
All four withdrawn SVGs remain rejection evidence.
Normal course builds refresh B34's ODP/PDF; this receipt establishes source integration.

The comparison found clearer teaching relationships in the textbook rasters despite their lower
resolution. Temporary side-by-side evidence: `_temp/lect10b_shape_comparison/compare-33.webp`
through `compare-36.webp`. Original B33-36 in `genetics/LECT10/lect10b-karyotypes.odp` and `.pdf`
are the durable comparison baseline.

## Repair and reuse

- Pure-vector delivery requires editable SVG geometry without `<image>` elements or embedded
  bitmaps. Keep original rasters as fallback/reference and use quality-90 WebP for review previews.
- Defer or skip work beyond reliable drawing ability with a brief reason. Human-figure drawing
  remains excluded; the listed repair targets do not require a forced replacement.
- Add an entry when a drawing is dropped after a teaching or rendering review. Record its exact
  path, affected deck/title, replacement, reason, and source baseline. Use current deck references
  to distinguish a completed removal from a recommendation.
- Compare a repaired drawing with the original at presentation size. Preserve the biological
  relationships and labels needed to answer the slide's question. Compose original artwork
  from those concepts; the original figure's contours and arrangement are not a template.
- Follow the current [master plan](active_plans/active/genetics_visual_renewal_plan.md): inspect
  one intended-size preview and perform a targeted consumer check when a concrete compatibility,
  clipping, reveal or frame concern requires it. Record exactly what was checked; normal full-deck
  builds and classroom acceptance remain separate from source integration.
- Retain the rejection history when a repaired asset returns to a deck; record the repaired
  revision and review date in the same entry.

See [slide-specs/SVG_DIAGRAMS.md](slide-specs/SVG_DIAGRAMS.md) for the asset contract and
[LECT10_REVIEW.md](../genetics/LECT10/djot/LECT10_REVIEW.md) for the dated restoration reviews.

## Tool specimen rejection: November 12, 2026

The instructor rejects the thin, tapered sister silhouette in the v1
[chromosome_tool.drawn.svg](slide-specs/illustration_examples/chromosome_tool.drawn.svg).
This supersedes earlier visual acceptance for that silhouette only. Preserve the v1 specimen
and its reviews as historical evidence. The repair target is two thick, rounded chromatids
forming an open X with clear space between the arms; the
[v2 stabilization plan](active_plans/active/chromosome_svg_tool_v2_plan.md) owns this repair.
This entry does not reject the tool's separate DNA track or authorize course-art substitutions.

Repair update, November 12, 2026: the new manager-reviewed
[chromosome_tool_v2.drawn.svg](slide-specs/illustration_examples/chromosome_tool_v2.drawn.svg)
uses rounded continuous open-X sisters, a broad labelable generic centromere marker, and
source-backed named chr7 bands. Corrected specification, independent quality and integration
reviews PASS; root viewed all five final proofs. This closes the standalone tool repair only.
The original v1 rejection above remains; the user has not personally approved the final v2
shape. No withdrawn LECT10 course art is restored. See
[closure.md](../_temp/chromosome_svg_tool_v2/closure.md).

### Subsequent v2 rejection: shared visual theme, November 12, 2026

The instructor then rejected the current
[chromosome_tool_v2.drawn.svg](slide-specs/illustration_examples/chromosome_tool_v2.drawn.svg):
"I can appreciate that you tried to accommodate my requests ... but they don't look like they
share a common theme anymore". The preceding standalone closure and review passes do not
establish acceptance of this v2 artwork. Keep the public specimen as the current repair
baseline; no course fallback or course-art substitution changes here.

A bounded [theme-revision concept](../_temp/chromosome_theme_revision/PLAN.md) uses the same
source-backed chromosome in single/sister views, common per-chromatid proportions and hollow
centromere collars, and a linked flat-ended internal crop. Root personally viewed and approved
that concept direction; production implementation and fresh review remain pending. This is not
instructor or classroom acceptance. Preserve both earlier rejection entries.
