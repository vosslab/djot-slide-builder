# Lecture 07 conversion

The five Djot decks are the canonical authoring sources. Original ODP/PDF files and the ODS
worksheet remain one directory above as source evidence. Generated delivery files live in
`output/odp/` and `output/pdf/` at the repository root.

## Inventory

| Deck | Authored | Visible | Hidden | Image placements |
| --- | ---: | ---: | ---: | ---: |
| `lect07a-2026_announcements.djot` | 36 | 25 | 11 | 7 |
| `lect07a2-genetic_probability.djot` | 11 | 11 | 0 | 2 |
| `lect07b-prob_of_progeny.djot` | 55 | 55 | 0 | 1 |
| `lect07c-prob_of_progeny_2.djot` | 41 | 41 | 0 | 2 |
| `lect07d-chi_square.djot` | 60 | 57 | 3 | 2 |
| Total | 203 | 189 | 14 | 14 |

Import reports retain the initial extraction findings and original source slide indices.
They are provenance records, not descriptions of the manually repaired decks. Added objectives,
summaries, and split reference tables change final slide indices.

## Teaching repairs

- Add podcast Episode 36 after the YouTube channel slide using `refresh_podcast.py`. Its
  locally saved thumbnail, full title, and visible clickable episode link use `big-image`.
  The explicit refresh command can update other lecture announcement decks.
- Use the 2026 announcements supplied as `lect06a-2026_announcements 2.odp`, updated for
  Lecture 7 on October 20. The calendar calls this Week 8 because the midterm occupied Week 7.
  Check the [schedule spreadsheet](https://docs.google.com/spreadsheets/d/1XLZcg8PnW4GyMxFctAKCTvzN9qImIb5S3bK6hyeDz0Q/edit),
  verified October 20, 2026. Quiz 3 and Assignments 7-8 are due November 3. Hide completed
  midterm preparation while preserving the reference slides.
- Keep source-hidden pages, worked-example order, and repeated summary references.
- Replace screenshots of questions, formulas, factorials, and Pascal coefficients with editable
  text and tables. Retain genuine figures, the handwritten genetic cross, the video still,
  announcement artwork, and one full chi-square distribution-table reference.
- Restore superscripts and explicit multiplication, distinguish a specified birth order from
  all arrangements, and define `C(n,k)` before using it. Use parenthesized slash fractions
  consistently in calculations; text, superscripts, and subscripts remain editable ODP glyphs.
- Restore the five-survivor mouse calculation, three-category arrangements, and exact dihybrid
  calculation. Correct the pea exercise to seed color: yellow dominance does not describe pod color.
- Rebuild the chi-square example as a stable six-column, five-row native table. Source slides
  6-13 correspond to authored slides 7-14: observed counts, expected counts, deviations,
  squares, fractional contributions, decimal contributions, sum, and degrees of freedom.
  Keep the total row present from the beginning. Shared `table-group` column widths preserve
  alignment across the sequence and closing reference.
- Restore the fruit-fly example and seven Mendel answer tables as editable calculations.
  Keep expected counts unrounded. This corrects the legacy worksheet's rounded expectations:
  flower color gives chi-square 0.391 and p 0.532; flower position gives 0.350 and p 0.554.
- Define p as the right-tail probability under the null. Use "fail to reject" rather than
  claiming the null is proved. Retain the historical discussion as a discussion, not evidence
  of deliberate falsification.

## Remaining representation limits

Three explicit `@replaceme` markers remain:

- Genetic probability, authored slide 3: the source animation on the video still is not
  represented. The imported image is static; this conversion does not claim video playback.
- Chi-square, authored slides 18-19: the source's stacked integral equations do not have a faithful
  native Djot math destination. Preserve their StarMath expressions in notes and leave the editable
  explanatory drafts under the watermark.

The Fall 2024 activity URL is retained in notes; the visible slide directs groups to the included
worksheet. An outdated URL is an editorial update, not a reason for `@replaceme`.
Older hidden activity links remain as historical references. The importer does not recreate
legacy click timing automatically; progressive worked examples use separate editable slides.

## Verification

- Strict Jotdown and semantic lint: five sources, 203 authored slides, 14 image placements.
- Capacity inspection: no reported concerns after splitting long Pascal reference tables.
- Native ODP/PDF builds: all five decks, with hidden pages excluded from PDF.
- Render review covers each deck and the final revised math/table pages. Historical low-resolution
  source figures retain their original quality; no whole-slide screenshot replacements were added.
- Reader/export regression checks: 43 passed, including valid embedded formula directories and
  rejection of a declared directory without its content.
- Parser checks: 70 passed. Final ODP/PDF inspection confirms all page and hidden-page counts,
  three visible replacement markers, ASCII sources, and identical table frame, column, and row
  geometry across chi-square steps 7-14. One-time numeric checks confirm the mouse distribution,
  three-category arrangement count, and exact dihybrid probability.

This is content conversion and rendered-export evidence, not attended Impress animation testing.

The subsequent podcast addition passes four helper tests, strict source lint and capacity checks.
Lecture 07A's rebuilt ODP/PDF has 36 authored and 25 visible pages. Page 5 was visually reviewed,
and its native ODP hyperlink points to the selected episode. A two-course preview verifies the
same helper selects Genetics and Biotechnology announcement files without modifying the latter.
