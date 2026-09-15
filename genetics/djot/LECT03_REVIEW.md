# Lecture 03 conversion

The seven Lecture 03 decks were imported from `genetics/LECT03/` on 2026-09-14 for the
September 15 lecture. The 2026 announcements are the current source; the 2025 announcements copy
was not imported. Djot and its adjacent assets now own subsequent authoring.
There are 275 authored slides: 249 visible and 26 marked `hidden: true`. Normal exports contain
the 249 visible slides. The page references below refer to visible classroom pages.

| Source | Visible slides | Classroom outputs |
| --- | ---: | --- |
| [lect03a-2026_announcements.djot](lect03a-2026_announcements.djot) | 40 | `output/{odp,pdf}/lect03a-2026_announcements.*` |
| [lect03b-blood_hla_typing.djot](lect03b-blood_hla_typing.djot) | 44 | `output/{odp,pdf}/lect03b-blood_hla_typing.*` |
| [lect03c-fingerprinting.djot](lect03c-fingerprinting.djot) | 51 | `output/{odp,pdf}/lect03c-fingerprinting.*` |
| [lect03d-genotyping_1.djot](lect03d-genotyping_1.djot) | 51 | `output/{odp,pdf}/lect03d-genotyping_1.*` |
| [lect03e-genotyping_2.djot](lect03e-genotyping_2.djot) | 28 | `output/{odp,pdf}/lect03e-genotyping_2.*` |
| [lect03f-whole_genome_analysis.djot](lect03f-whole_genome_analysis.djot) | 24 | `output/{odp,pdf}/lect03f-whole_genome_analysis.*` |
| [lect03g-chap2_challenges.djot](lect03g-chap2_challenges.djot) | 11 | `output/{odp,pdf}/lect03g-chap2_challenges.*` |
| Total | 249 | Seven editable ODPs and seven PDFs |

## Content repairs

Content repairs use the current slide layouts, native
text, tables, ordinary component images, and bounded answer reveals. Source order and visible slide
counts are preserved. All 26 hidden announcement slides now appear in their original Djot positions
with `hidden: true`, their component images, and their notes in the import report. The 40 edited
visible announcement slide blocks were preserved exactly when the hidden slides were restored.

To include a hidden slide in the classroom deck, remove its `hidden: true` line or change it to
`hidden: false`, then rebuild. See
[DJOT_SLIDE_SYNTAX.md](../../docs/DJOT_SLIDE_SYNTAX.md#hidden-slides).

- Covers use the existing title-slide layout and September 15, 2026 date. The announcement cover
  now says Lecture 3A, and its agenda lists the Lecture 03 topics.
- 03b pages 10-18: editable reaction tables replace lost blood-test drawings; clumping patterns and
  answers are restored. Pages 24-30 use a progressive HLA inheritance table in place of the seven
  drawing-only slides that imported as blank. Pages 33-38 restore comparison cues and answers.
- 03c page 17: an editable STR evidence table restores the data hidden by missing drawing text.
  Pages 23, 31, 35-37, 46, and 49 use explicit comparison cues or answers for lost highlighting.
- 03d pages 5-6 and 03f pages 22-23: editable genotype tables and links replace unsupported SVM
  image instances. The source's historical costs remain explicitly labeled 2020.
- 03d pages 28-29 and 31-34 put long ancestry captions beside their figures. 03f pages 6-8
  restore sequencing steps and sequence text; page 13 restores the genome-composition legend.
- 03e page 26: an editable table carries the original common ABO SNP decision-tree outcomes.
- 03g pages 4-10: the original gel image accompanies short sequential comparison instructions and
  the final answer, replacing drawing masks, arrows, and duplicated question-image placements.
- Single-figure slides with explanatory text use the existing two-panel layout to keep the figure
  visible alongside its explanation.

## Review boundary

Import reports record extraction evidence, so their initial layouts and warnings do not
describe the manually repaired source. Legacy arrows, masks, decorative shapes, and exact diagram
geometry are not reproduced. The recovered teaching relationships are expressed directly in Djot.
The announcement report was refreshed to include all 66 source slides and their visibility.
The rebuilt announcement ODP and PDF still have 40 pages, and every PDF page's extracted text
matches the version before hidden slides were restored. Full pytest passed with 1,921 tests.

Some inherited announcement prose, quotations, tables, and reference screenshots remain dense.
Compiler capacity warnings identify text below its usual 20 pt floor; a successful build does not
mean every slide meets that readability target. This conversion preserves historical claims,
prices, references, and older breakout-room links; it is not a factual or link-currency update.

Strict Djot lint, ODP/PDF slide counts, and rendered checks are the acceptance evidence for this
conversion. Native answer reveals have not received an attended Impress click-through. Generated
contact sheets and the final build diagnostics live in `output/lect03_review/`.

Rebuild one deck with the existing command:

```bash
source source_me.sh && python3 deck_tools.py build \
  genetics/djot/lect03b-blood_hla_typing.djot --format all
```
