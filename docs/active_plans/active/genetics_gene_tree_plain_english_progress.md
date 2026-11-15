# Genetics gene tree polish

## Outcome

Polish worksheet sets B, C, and D for international biology students. Keep the instructor's voice,
biology, and worksheet math intact. Clarify wording in plain English.

## Required design

- Keep the matrix with calculation questions and the tree with path questions.
- Make the tree and prompt composition larger and easier to read.
- On merge answers, show the newly formed merge.
- Highlight only the lower triangle.
- Match the established end layout.

## Work and owners

| Work | Owner | Status |
| --- | --- | --- |
| Update generator, generated fragments and trees, and relevant tests | `/root/polish_generator` | Complete |
| Polish B/C/D masters and `VOICE_GUIDE.md` | `/root/polish_slide_voice` | Complete |
| Fresh specification review | Serialized milestone | PASS: [source review](../reports/genetics_gene_tree_plain_english_spec.md) |
| Rebuild three ODP/PDF files and render every page | Serialized milestone | Complete: [build evidence](../reports/genetics_gene_tree_plain_english_build.md) |
| Fresh quality review | Serialized milestone | PASS: [rendered review](../reports/genetics_gene_tree_plain_english_quality.md), [C correction](../reports/genetics_gene_tree_plain_english_summary_fix.md) |
| Fresh integration review | Serialized milestone | PASS: [integration report](../reports/genetics_gene_tree_plain_english_integration.md) |
| Write durable report and close out | Serialized milestone | Complete: [refresh report](../../GENETICS_GENE_TREE_REFRESH_REPORT.md) |

Complete the two implementation tracks before starting the serialized review and rebuild milestones.
Record evidence and any remaining issues here as work proceeds; do not mark a milestone done without its
review artifact or other direct evidence.

## Scope limits

Known inherited E and chromosome defects are outside this polish scope; keep them visible in the report.
No live classroom verification is planned, so do not claim classroom validation.
