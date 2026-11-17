# Genetics gene tree refresh

November 17 update: 11B contains interpretation with an early vocabulary slide (30 pages), preserving the
Khan Academy rotation figures, annotated trees, and branch-distance questions.
New 11C contains construction methods, the restored three-rhino introduction, and
the colored four-sequence UPGMA example (59 pages). Former C/D/E are now D/E/F (38/64/19 pages). See
[the current source map](../genetics/LECT11/djot/LECT11_SOURCE_MAP.md).
The November 14 evidence below describes the earlier deck organization.

Completed November 14, 2026. The revised Lecture 11 A-D sources and exported ODP and PDF
files are ready for teaching. Fresh specification, quality, and integration reviews pass; the
preserved E and chromosome decks retain the limitations listed below.

## Schedule and scope

The former 2025 Lecture 12 gene-tree bundle is now Lecture 11 on November 17, 2026. The former
Lecture 11 chromosome bundle is now Lecture 12 on December 1. Lecture 11A selects *The Animal
Kingdom* (2023), states no November 17 quiz and homework 9 and 10 due, and identifies the
November 24 break, December 1 Quiz 4, December 8 Quiz 5 and homework 11 and 12, and December 15 final. Lecture 12A
covers the December 1 chromosome agenda and Quiz 4. Weekly announcements stay with their
calendar weeks.

B introduces reading trees and a new four-gene example; C guides a new five-gene weighted UPGMA
example; D walks through all answers for the existing six-gene worksheet. Students predict before
answers, with no rigid timing requirement. E is preserved apart from numbering and date.
Chromosome content is preserved apart from numbering and references. Slides were refreshed; the
worksheet was not changed or replaced. The methods comparison is intentionally brief.

## Sources and outputs

Each output stem below has an editable `.odp` in `output/odp/` and a `.pdf` in `output/pdf/`.
All ten decks were exported with LibreOffice outside the sandbox. Current sources and historical
source maps are linked from the two reviews.

| Deck | Canonical master | Local ODP and PDF paths |
| --- | --- | --- |
| 11A | [lect11a-2026_announcements.djot](../genetics/LECT11/djot/lect11a-2026_announcements.djot) | `output/odp/lect11a-2026_announcements.odp`, `output/pdf/lect11a-2026_announcements.pdf` |
| 11B | [lect11b-interpreting_gene_trees.djot](../genetics/LECT11/djot/lect11b-interpreting_gene_trees.djot) | `output/odp/lect11b-interpreting_gene_trees.odp`, `output/pdf/lect11b-interpreting_gene_trees.pdf` |
| 11C | [lect11c-building_gene_trees.djot](../genetics/LECT11/djot/lect11c-building_gene_trees.djot) | `output/odp/lect11c-building_gene_trees.odp`, `output/pdf/lect11c-building_gene_trees.pdf` |
| 11D | [lect11d-upgma_weighted_averages.djot](../genetics/LECT11/djot/lect11d-upgma_weighted_averages.djot) | `output/odp/lect11d-upgma_weighted_averages.odp`, `output/pdf/lect11d-upgma_weighted_averages.pdf` |
| 11E | [lect11e-upgma_group_activity.djot](../genetics/LECT11/djot/lect11e-upgma_group_activity.djot) | `output/odp/lect11e-upgma_group_activity.odp`, `output/pdf/lect11e-upgma_group_activity.pdf` |
| 11F | [lect11f-molecular_clocks.djot](../genetics/LECT11/djot/lect11f-molecular_clocks.djot) | `output/odp/lect11f-molecular_clocks.odp`, `output/pdf/lect11f-molecular_clocks.pdf` |
| 12A | [lect12a-2026_announcements.djot](../genetics/LECT12/djot/lect12a-2026_announcements.djot) | `output/odp/lect12a-2026_announcements.odp`, `output/pdf/lect12a-2026_announcements.pdf` |
| 12B | [lect12b-polyploidy.djot](../genetics/LECT12/djot/lect12b-polyploidy.djot) | `output/odp/lect12b-polyploidy.odp`, `output/pdf/lect12b-polyploidy.pdf` |
| 12C | [lect12c-sex_dosage.djot](../genetics/LECT12/djot/lect12c-sex_dosage.djot) | `output/odp/lect12c-sex_dosage.odp`, `output/pdf/lect12c-sex_dosage.pdf` |
| 12D | [lect12d-chromo_alter_1-deletions.djot](../genetics/LECT12/djot/lect12d-chromo_alter_1-deletions.djot) | `output/odp/lect12d-chromo_alter_1-deletions.odp`, `output/pdf/lect12d-chromo_alter_1-deletions.pdf` |
| 12E | [lect12e-chromo_alter_2-duplications.djot](../genetics/LECT12/djot/lect12e-chromo_alter_2-duplications.djot) | `output/odp/lect12e-chromo_alter_2-duplications.odp`, `output/pdf/lect12e-chromo_alter_2-duplications.pdf` |

The generated [gene_tree_four_steps.djot](../genetics/LECT11/djot/gene_tree_four_steps.djot),
[gene_tree_five_steps.djot](../genetics/LECT11/djot/gene_tree_five_steps.djot), and
[gene_tree_six_steps.djot](../genetics/LECT11/djot/gene_tree_six_steps.djot) step fragments supply native matrices
and SVG trees. Regenerate them and their assets from the repository root with:

```sh
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B genetics/LECT11/djot/gene_tree_recipes.py
```

The fixed input is [gene_tree_example_data.json](../genetics/LECT11/djot/gene_tree_example_data.json).
The former disconnected B and C include files were removed after comparison with their archived
originals. Original presentations, PDFs, worksheet artwork, and other input media remain preserved.
The [migration manifest](active_plans/reports/genetics_lecture_11_12_renumber.json) records 323
paths and before/after SHA-256 values. The current and historical maps are in
[LECT11_SOURCE_MAP.md](../genetics/LECT11/djot/LECT11_SOURCE_MAP.md) and
[LECT12_SOURCE_MAP.md](../genetics/LECT12/djot/LECT12_SOURCE_MAP.md); inherited conversion
limitations are in [LECT11_REVIEW.md](../genetics/LECT11/djot/LECT11_REVIEW.md) and
[LECT12_REVIEW.md](../genetics/LECT12/djot/LECT12_REVIEW.md).

## Mathematics and provenance

Four- and five-gene distances are illustrative, not observations or years. BPQ catalog topologies
inspired their fixed arrangements; BPQ code was not changed and the selected values were not
randomly generated by BPQ. The six-gene input reproduces all 15 pairs in the existing worksheet
matrix. UPGMA averages all original cross-cluster pairs, weights unequal clusters by membership,
sets node height to half the merge distance, and subtracts child height to obtain branch length.
The four-gene tree reproduces its input distances; the non-ultrametric five- and six-gene inputs
produce fitted trees that need not reproduce every raw pair. Equal root-to-tip lengths reflect the
model's clock assumption.

[genetics_gene_tree_math.md](active_plans/reports/genetics_gene_tree_math.md) preserves every input
pair, matrix stage, merge, branch, example calculation, BPQ provenance, and verification result.
The independent exact-fraction calculation and SciPy average linkage agree on all 12 merges.
The general BPQ SVG export remains a separate deferred item in [TODO.md](TODO.md).

## Plain-English and visual polish (current B/C/D)

The subsequent B/C/D polish uses simpler English for international biology students while retaining the instructor's voice and the worksheet mathematics. Questions show the matrix or tree needed to work, merge answers show the new join and highlight a real lower-triangle cell, and the endings follow a consistent layout. The preference for simple English without fancy idioms is recorded in the [voice guide](slide-specs/VOICE_GUIDE.md).

Current B/C/D PDFs contain 36/34/32 pages and ODPs contain 9/13/15 native tables. The [integration review](active_plans/reports/genetics_gene_tree_plain_english_integration.md) records final hashes, matching embedded trees, the preserved original worksheet evidence, decision D1, checks and limits. [Specification](active_plans/reports/genetics_gene_tree_plain_english_spec.md), [build](active_plans/reports/genetics_gene_tree_plain_english_build.md), [rendered quality](active_plans/reports/genetics_gene_tree_plain_english_quality.md), and [final C summary correction](active_plans/reports/genetics_gene_tree_plain_english_summary_fix.md) document the work. All 102 current B/C/D pages were visually reviewed, including the accepted correction to C32.

## Earlier refresh verification and limits

The counts and build evidence below describe the earlier refresh before the B/C/D polish; current B/C/D counts and hashes are above.

- Fresh [specification](active_plans/reports/genetics_gene_tree_spec_review.md),
  [C delta](active_plans/reports/genetics_gene_tree_spec_delta.md),
  [A and B quality](active_plans/reports/genetics_gene_tree_quality_ab.md),
  [C and D quality](active_plans/reports/genetics_gene_tree_quality_cd.md),
  [final C quality](active_plans/reports/genetics_gene_tree_quality_c_final.md), and
  [integration](active_plans/reports/genetics_gene_tree_integration.md) reviews pass. The initial
  C finding is historical and was fixed and independently reviewed again. The initial sequencing
  and B-D layout and input issues are resolved. The integration correction links the retired C
  exemplar to its archived original source, preserving its historical identity.
- All 173 then-current 11A-D and 12A PDF pages were individually viewed. Preserved E and chromosome
  decks were sampled, not fully visually reviewed. Five compact overviews are retained:
  [lect11a.webp](slide-specs/illustration_examples/gene_tree_lecture/lect11a.webp),
  [lect11b.webp](slide-specs/illustration_examples/gene_tree_lecture/lect11b.webp),
  [lect11c.webp](slide-specs/illustration_examples/gene_tree_lecture/lect11c.webp),
  [lect11d.webp](slide-specs/illustration_examples/gene_tree_lecture/lect11d.webp), and
  [lect12a.webp](slide-specs/illustration_examples/gene_tree_lecture/lect12a.webp).
- The earlier B/C/D PDFs had 36/34/32 visible pages. Their ODPs had 7/12/11 native tables,
  112/264/288 cells, and 7/5/6 SVG files. The 15 generated example SVGs match their embedded
  ODP copies. B-D have no replacement markers or capacity warnings. C questions retain the
  matrix or tree needed for the calculation. D includes all 15 original pairs, five joins,
  four reduced matrices and all ten branches; the original worksheet PDF remains unchanged and
  no replacement worksheet was generated.
- Strict native lint passed 10 masters, 498 slides, and 208 image references; 46 focused tests
  passed. These expanded authored slide counts are distinct from visible PDF page counts and
  source word counts. The math report records all 12 independently checked joins, SciPy agreement,
  and equal root-to-tip paths. [Build evidence](active_plans/reports/genetics_gene_tree_build_evidence.md)
  records commands, native inventory and historical hashes.
- Migration records 323 paths; all 286 recorded original media files match their original hashes.
  E and chromosome content was preserved apart from renumbering and references.
- E retains one authored `@replaceme`, producing three PDF overlay instances and an inherited
  mixed figure with detached labels. Chromosome 12C page 5 has a large inherited `REPLACE ME`
  overlay obscuring content. These preserve-only decks are not all visually reviewed or established
  as classroom-ready. Some inherited announcement evergreen font advisories remain.
- Interactive Impress, live Zoom, classroom use, and the full base suite including Git-dependent
  hygiene were not checked.
