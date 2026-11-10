# LECT12 conversion review

Reviewed draft, November 9, 2026. 5 canonical Djot decks produce editable ODP
and LibreOffice-derived PDF. 101 explicit `@replaceme` slides retain difficult conversions.
Those slides need reconstruction before classroom use.

## November 10 agenda wording

Use brief deck and activity labels under Chapter 11: Gene Trees, Gene Tree Handout Activity,
and Evolutionary Time. Include Group Quiz 4 on the
December 1 agenda and correct its schedule date; next week's Quiz 5 remains conditional.
A retains 54 authored / 17 hidden / 37 PDF pages; its agenda is PDF 2. Rebuilt ODP/PDF, passed
strict native lint, and inspected the agenda and changed logistics. The wording correction passes
213 documentation/guidance checks. Evidence: `_temp/genetics_agendas_09_15/`. Existing weather/registration
capacity advisories remain. The wording correction is verified separately in
`_temp/genetics_agenda_voice/`. The content/date mismatch below remains a scheduling task.

## Outputs and counts

Editable sources are in this directory. Generated artifacts use the same stem under
`output/odp/` and `output/pdf/` at the repository root. The accompanying
[LECT12_SOURCE_MAP.md](LECT12_SOURCE_MAP.md) maps all original content slides and additions.

| Deck | Authored ODP | Hidden | PDF pages | Replacements |
| --- | --- | --- | --- | --- |
| lect12a-2026_announcements | 54 | 17 | 37 | 0 |
| lect12b-gene_trees | 77 | 0 | 77 | 39 |
| lect12c-more_gene_trees | 56 | 0 | 56 | 43 |
| lect12d-gene_tree_activity | 32 | 0 | 32 | 18 |
| lect12e-evol_time | 19 | 0 | 19 | 1 |

Total: 238 authored, 17 hidden, 221 PDF pages.
Content decks preserve 171 original slides and add 13 opening/closing slides.
Sibling Djot includes keep long source files below the repository size limit without splitting slides.
Original THE END slides and following appendices retain their order; repeated closing bookends
close appendices where necessary. Existing definition slides serve the introduced vocabulary.

## Inputs and source order

There was no existing Djot in these target folders. Source ODP files were imported with the
repository tools; limited temporary import adapters are described below. All 18 original ODP
SHA-256 hashes across this conversion match the pre-import inventory. Original PDFs were retained.
Raw announcement Djot imports are intermediate evidence under `_temp/lect12_13_1x/`;
their unused extracted artwork was removed, while the import reports remain.

- `lect12a-2025_announcements 2.odp`: 60 authored; hidden 2-3, 5-6, 12-13, 15, 17, 27-31, 39-42, 45-46, 52-53, 58-59; source animation elements none.
- `lect12a-2025_announcements.odp`: 60 authored; hidden 2-3, 5-6, 12-13, 15, 17, 27-31, 39-42, 45-46, 52-53, 58-59; source animation elements none.
- `lect12b-gene_trees.odp`: 74 authored; hidden none; source animation elements none.
- `lect12c-more_gene_trees.odp`: 52 authored; hidden none; source animation elements 26.
- `lect12d-gene_tree_activity.odp`: 29 authored; hidden none; source animation elements none.
- `lect12e-evol_time.odp`: 16 authored; hidden none; source animation elements none.

Source section order, `lect12b-gene_trees`: 3 Why do we want to study molecular evolution? -> 6 Gene Trees -> 18 Reading a Gene Tree -> 25 Constructing a Gene Tree from Sequences -> 28 Gene Tree Methods -> 38 Simple Example of Gene Tree by Distance Method -> 39 UPGMA Simple Example Part 1: Create Distance Matrix -> 54 UPGMA Simple Example Part 2: Create Gene Tree -> 65 17.22 From Gene Tree to Distance Matrix -> 74 THE END.

Source section order, `lect12c-more_gene_trees`: 2 Full Example -> 28 Hartl Question 17.27 -> 41 THE END -> 42 Former Textbook Example of Gene Tree by Distance Method.

Source section order, `lect12d-gene_tree_activity`: 6 Gene Tree Handout -> 29 THE END.

Source section order, `lect12e-evol_time`: 3 Molecular Clocks and Evolutionary Time -> 10 Homologous Genes -> 16 THE END.

## Dates, announcements, and conversion findings

The current-year Lecture 11A Djot is the newest shared course-information and formatting
source. The matching prior-year announcement deck supplies useful week-specific cues. This is
the ordinary two-source workflow in [the announcement guide](../../../docs/slide-specs/ANNOUNCEMENT_DECK_GUIDE.md).
The instructor-cleaned Biotechnology Lecture 10A remains the guide's formatting example;
no Biotechnology files were edited. The earlier Lecture 09 current-year starter is superseded.

Dates were checked against `/Users/vosslab/nsh/syllabus/site_docs/fall_2026/genetics/SCHEDULE.md`,
generated from the [course spreadsheet](https://docs.google.com/spreadsheets/d/1XLZcg8PnW4GyMxFctAKCTvzN9qImIb5S3bK6hyeDz0Q/edit).
The local schedule was read; the underlying spreadsheet was not separately refreshed.
The [published schedule](https://vosslab.github.io/syllabus/fall_2026/genetics/SCHEDULE/)
is the student-facing link used in the slides.

**Content/date mismatch:** the schedule places gene trees/population genetics on November 17,
chromosome abnormalities on December 1, and population genetics on December 8. The supplied
LECT12 folder contains gene trees and LECT13 contains chromosome rearrangements. Their supplied
content and order are retained; covers use their 2026 lecture dates and the calendar controls
assessment deadlines. No rescheduling was inferred.

Quiz 5 and homework 11/12 are due December 8; the cumulative final and homework 13 are due
December 15. Assessment colors and next-week wording follow those dates. Quiz guidance is
visible through one include setting because Quiz 5 is next week/this week. First-week signup,
profile, and assignment groups remain hidden and Discord information remains in the shared
course-information group. Evaluations and club groups remain hidden; current evaluation
availability dates were not established. Refresh those dates before showing that group.

The podcast helper preview (`--by-lecture-date`) selected regular StVC episode 37 as of the
November 9 conversion, excluding special 38. The saved Bad Cell Day title, thumbnail, video,
and game agree with the reviewed current-year source. The video oEmbed and game returned HTTP
200 during the preceding LECT11 conversion; browser playback/gameplay were not tested.
Future episodes published before the December lecture dates need a teaching-time refresh.
The inherited November 9 NWS weather snapshot remains hidden; it is not a December forecast.
Refresh weather on the day before class. YouTube/anonymous-message/Discord/Zoom slides use
the shared groups, local artwork, and existing private course-link references.

The canonical announcement deck is `lect12a-2026_announcements.djot`, dated December 1.
The popular-culture icebreaker comes from `evergreen/icebreakers.yaml`. The November 10 calendar
follow-up adds Group Quiz 4 on December 1. The December 8 quiz/homework lookahead is visible;
Quiz 5 is conditional on the class vote.
Exam guidance remains hidden, registration remains visible through its documented December 1
window, and early homework dates remain hidden. The complete updated visibility inventory is
in the source map. The duplicate `lect12a-2025_announcements 2.odp` has exactly the same ZIP
members and member bytes as the normally named source; it was imported once. Both originals
remain unchanged.

Gene-tree branches and their positioned labels are the largest conversion failures. B42-53
lose aligned sequence columns/highlights; B55-64 lose progressive tree geometry; B67-72
lose table/diagonal-arrow relationships. C3 and C5-24 duplicate bitmap/native matrices or
lose merge highlights. C26 retains an animation warning; C38-39 lose tree geometry. C45-52
lose static masks and expose the full later tree. The D activity retains the original
year-labeled group-sheet URLs; its matrix outlines and selected merge cells need repair.
No 2026 group-sheet copies were invented, and historical spreadsheet access was not tested.

E3's imported three-bullet divider is now a native Molecular Clocks and Evolutionary Time
section. E2/E4 retain their complete bitmap/prose content despite frame/bounds warnings;
those flags were cleared after comparison. E5's substitution diagram remains tiny with
detached labels and retains its marker. B23/B33/B35's colored text and complete figures were
verified before clearing their color-only flags. No new special layout was added.

The ordinary importer could not express C39's seven mixed components as an exact grid.
A temporary adapter grouped the non-table components into one ordinary panel beside the
native table. The source image count was asserted unchanged and C39 remains marked.

Covers/objectives/summaries and ordinary teaching prose remain selectable native text.
Original scanned problem and textbook text within bitmap figures remains raster content.
Chapter assignments were checked against the [BPW genetics index](https://biologyproblems.org/genetics/):
gene trees 11, chromosome disorders 9, population genetics 10. Cover chapter numbers follow those topics.

## Visual review and replacement tasks

All 641 visible original content slides across the three folders were compared against
watermark-free diagnostic ODP-derived PDFs in 45 paired sheets under
`_temp/lect12_13_1x/review/`. Original pages are on the left and diagnostic pages on the right.
Hidden source slides were checked through source text/XML, not a visible source PDF page.
Final announcement pages and all added covers/bookends were inspected in `final_review/`.
Selected dense tables, equations, colored dividers, and repaired notation were inspected at
readable size. Contact sheets do not certify every small label at classroom viewing distance.

Numbers below are original ODP numbers; the source map gives final Djot/PDF positions.
Keep the original assets and ODP as references. Each task ends by rendering and comparing
the native repair before clearing its marker. Do not split content slides as a default repair.

### lect12b-gene_trees

Cleared after paired/rendered verification: source 23, 33, 35.

- Source 10 -> Djot 12: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 11 -> Djot 13: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 12 -> Djot 14: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 13 -> Djot 15: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 14 -> Djot 16: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 15 -> Djot 17: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 16 -> Djot 18: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 19 -> Djot 21: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 20 -> Djot 22: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 24 -> Djot 26: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 27 -> Djot 29: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 42 -> Djot 44: aligned sequence columns, dot notation, or highlighted differences lost; restore a monospace alignment and matching highlights.
- Source 43 -> Djot 45: aligned sequence columns, dot notation, or highlighted differences lost; restore a monospace alignment and matching highlights.
- Source 44 -> Djot 46: aligned sequence columns, dot notation, or highlighted differences lost; restore a monospace alignment and matching highlights.
- Source 45 -> Djot 47: aligned sequence columns, dot notation, or highlighted differences lost; restore a monospace alignment and matching highlights.
- Source 46 -> Djot 48: aligned sequence columns, dot notation, or highlighted differences lost; restore a monospace alignment and matching highlights.
- Source 47 -> Djot 49: aligned sequence columns, dot notation, or highlighted differences lost; restore a monospace alignment and matching highlights.
- Source 48 -> Djot 50: aligned sequence columns, dot notation, or highlighted differences lost; restore a monospace alignment and matching highlights.
- Source 49 -> Djot 51: aligned sequence columns, dot notation, or highlighted differences lost; restore a monospace alignment and matching highlights.
- Source 50 -> Djot 52: aligned sequence columns, dot notation, or highlighted differences lost; restore a monospace alignment and matching highlights.
- Source 51 -> Djot 53: aligned sequence columns, dot notation, or highlighted differences lost; restore a monospace alignment and matching highlights.
- Source 52 -> Djot 54: aligned sequence columns, dot notation, or highlighted differences lost; restore a monospace alignment and matching highlights.
- Source 53 -> Djot 55: aligned sequence columns, dot notation, or highlighted differences lost; restore a monospace alignment and matching highlights.
- Source 55 -> Djot 57: matrix-to-tree branch geometry or merge highlights lost; rebuild the progressive tree and matrix emphasis.
- Source 56 -> Djot 58: matrix-to-tree branch geometry or merge highlights lost; rebuild the progressive tree and matrix emphasis.
- Source 57 -> Djot 59: matrix-to-tree branch geometry or merge highlights lost; rebuild the progressive tree and matrix emphasis.
- Source 58 -> Djot 60: matrix-to-tree branch geometry or merge highlights lost; rebuild the progressive tree and matrix emphasis.
- Source 59 -> Djot 61: matrix-to-tree branch geometry or merge highlights lost; rebuild the progressive tree and matrix emphasis.
- Source 60 -> Djot 62: matrix-to-tree branch geometry or merge highlights lost; rebuild the progressive tree and matrix emphasis.
- Source 61 -> Djot 63: matrix-to-tree branch geometry or merge highlights lost; rebuild the progressive tree and matrix emphasis.
- Source 62 -> Djot 64: matrix-to-tree branch geometry or merge highlights lost; rebuild the progressive tree and matrix emphasis.
- Source 63 -> Djot 65: matrix-to-tree branch geometry or merge highlights lost; rebuild the progressive tree and matrix emphasis.
- Source 64 -> Djot 66: matrix-to-tree branch geometry or merge highlights lost; rebuild the progressive tree and matrix emphasis.
- Source 67 -> Djot 69: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 68 -> Djot 70: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 69 -> Djot 71: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 70 -> Djot 72: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 71 -> Djot 73: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 72 -> Djot 74: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.

### lect12c-more_gene_trees

- Source 3 -> Djot 4: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 5 -> Djot 6: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 6 -> Djot 7: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 7 -> Djot 8: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 8 -> Djot 9: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 9 -> Djot 10: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 10 -> Djot 11: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 11 -> Djot 12: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 12 -> Djot 13: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 13 -> Djot 14: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 14 -> Djot 15: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 15 -> Djot 16: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 16 -> Djot 17: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 17 -> Djot 18: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 18 -> Djot 19: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 19 -> Djot 20: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 20 -> Djot 21: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 21 -> Djot 22: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 22 -> Djot 23: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 23 -> Djot 24: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 24 -> Djot 25: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 26 -> Djot 27: source reveal/animation not preserved; source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 29 -> Djot 30: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 30 -> Djot 31: figure or notation remains too small or loses source emphasis; rework the native layout/figure and compare with the original.
- Source 31 -> Djot 32: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 32 -> Djot 33: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 33 -> Djot 34: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 34 -> Djot 35: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 35 -> Djot 36: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 36 -> Djot 37: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 37 -> Djot 38: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 38 -> Djot 39: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 39 -> Djot 40: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 40 -> Djot 41: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 44 -> Djot 46: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 45 -> Djot 47: static white masks lost, exposing the completed tree before its teaching step; restore source masks and paint order.
- Source 46 -> Djot 48: static white masks lost, exposing the completed tree before its teaching step; restore source masks and paint order.
- Source 47 -> Djot 49: static white masks lost, exposing the completed tree before its teaching step; restore source masks and paint order.
- Source 48 -> Djot 50: static white masks lost, exposing the completed tree before its teaching step; restore source masks and paint order.
- Source 49 -> Djot 51: static white masks lost, exposing the completed tree before its teaching step; restore source masks and paint order.
- Source 50 -> Djot 52: static white masks lost, exposing the completed tree before its teaching step; restore source masks and paint order.
- Source 51 -> Djot 53: static white masks lost, exposing the completed tree before its teaching step; restore source masks and paint order.
- Source 52 -> Djot 54: static white masks lost, exposing the completed tree before its teaching step; restore source masks and paint order.

### lect12d-gene_tree_activity

- Source 3 -> Djot 5: figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 8 -> Djot 10: pair/merge outlines or matrix highlights missing; restore the specific highlighted cells and progressive emphasis.
- Source 9 -> Djot 11: pair/merge outlines or matrix highlights missing; restore the specific highlighted cells and progressive emphasis.
- Source 10 -> Djot 12: pair/merge outlines or matrix highlights missing; restore the specific highlighted cells and progressive emphasis.
- Source 12 -> Djot 14: pair/merge outlines or matrix highlights missing; restore the specific highlighted cells and progressive emphasis.
- Source 13 -> Djot 15: pair/merge outlines or matrix highlights missing; restore the specific highlighted cells and progressive emphasis.
- Source 14 -> Djot 16: pair/merge outlines or matrix highlights missing; restore the specific highlighted cells and progressive emphasis.
- Source 16 -> Djot 18: pair/merge outlines or matrix highlights missing; restore the specific highlighted cells and progressive emphasis.
- Source 17 -> Djot 19: pair/merge outlines or matrix highlights missing; restore the specific highlighted cells and progressive emphasis.
- Source 18 -> Djot 20: pair/merge outlines or matrix highlights missing; restore the specific highlighted cells and progressive emphasis.
- Source 20 -> Djot 22: pair/merge outlines or matrix highlights missing; restore the specific highlighted cells and progressive emphasis.
- Source 21 -> Djot 23: pair/merge outlines or matrix highlights missing; restore the specific highlighted cells and progressive emphasis.
- Source 22 -> Djot 24: pair/merge outlines or matrix highlights missing; restore the specific highlighted cells and progressive emphasis.
- Source 24 -> Djot 26: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 25 -> Djot 27: pair/merge outlines or matrix highlights missing; restore the specific highlighted cells and progressive emphasis.
- Source 26 -> Djot 28: pair/merge outlines or matrix highlights missing; restore the specific highlighted cells and progressive emphasis.
- Source 27 -> Djot 29: pair/merge outlines or matrix highlights missing; restore the specific highlighted cells and progressive emphasis.
- Source 28 -> Djot 30: pair/merge outlines or matrix highlights missing; restore the specific highlighted cells and progressive emphasis.

### lect12e-evol_time

Cleared after paired/rendered verification: source 2, 4.

- Source 5 -> Djot 7: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.

## Capacity and typography

Capacity diagnostics are advisory; every mixed-readability failure has an explicit marker.
Other small-font advisories remain where recorded below. Source wording was retained.
The source image-area audit is stored in each import report; flagged shrinkage was visually
compared using the source map, and unresolved figure size/relationships remain marked.

| Deck / Djot | Slot | Cause | Required / floor pt | Review outcome |
| --- | --- | --- | --- | --- |
| lect12a-2026_announcements / 4 | caption | paragraph/list | 15.25 / 18.0 | Below-floor advisory retained; inspect at teaching distance. |
| lect12a-2026_announcements / 43 | left | paragraph/list | 19.75 / 20.0 | Below-floor advisory retained; inspect at teaching distance. |
| lect12a-2026_announcements / 43 | bottom-right | paragraph/list | 18.5 / 20.0 | Below-floor advisory retained; inspect at teaching distance. |
| lect12a-2026_announcements / 44 | body | paragraph/list | 19.75 / 20.0 | Below-floor advisory retained; inspect at teaching distance. |
| lect12b-gene_trees / 9 | right | paragraph/list | 19.0 / 20.0 | Below-floor advisory retained; inspect at teaching distance. |
| lect12b-gene_trees / 10 | right | paragraph/list | 18.75 / 20.0 | Below-floor advisory retained; inspect at teaching distance. |
| lect12b-gene_trees / 13 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect12b-gene_trees / 14 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect12b-gene_trees / 15 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect12b-gene_trees / 16 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect12b-gene_trees / 17 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect12b-gene_trees / 18 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect12b-gene_trees / 21 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect12b-gene_trees / 22 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect12b-gene_trees / 25 | top-right | paragraph/list | 14.5 / 20.0 | Below-floor advisory retained; inspect at teaching distance. |
| lect12b-gene_trees / 26 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect12b-gene_trees / 35 | right | paragraph/list | 17.5 / 20.0 | Below-floor advisory retained; inspect at teaching distance. |
| lect12c-more_gene_trees / 11 | top-right | table | 16.5 / 20.0 | Retain replacement marker. |
| lect12c-more_gene_trees / 12 | top-right | table | 16.5 / 20.0 | Retain replacement marker. |
| lect12c-more_gene_trees / 27 | left | paragraph/list | 19.75 / 20.0 | Retain replacement marker. |
| lect12c-more_gene_trees / 40 | right | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect12c-more_gene_trees / 47 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect12c-more_gene_trees / 48 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect12c-more_gene_trees / 49 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect12c-more_gene_trees / 50 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect12c-more_gene_trees / 51 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect12c-more_gene_trees / 52 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect12c-more_gene_trees / 53 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect12c-more_gene_trees / 54 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect12d-gene_tree_activity / 5 | body | paragraph/list | 18.0 / 20.0 | Retain replacement marker. |
| lect12e-evol_time / 7 | body | mixed-readability | 14.0 / 20.0 | Retain replacement marker. |

Typography audit summary: {'runt': 5, 'title-wrap': 2}. Skipped coverage: {'special-layout-titles': 11, 'hidden-slides': 17, 'math-or-explicit-break-paragraphs': 12}.
Existing wrapped titles were retained; possible shorter wording below is a review suggestion only.
No instructor-authored title was shortened solely to silence an audit warning.

| Deck / Djot | Finding | Review or possible shorter title |
| --- | --- | --- |
| lect12a-2026_announcements / 10 | runt in left, paragraph 4 | Existing wording retained; advisory line fit. |
| lect12b-gene_trees / 31 | runt in left, paragraph 4 | Existing wording retained; advisory line fit. |
| lect12b-gene_trees / 32 | runt in left, paragraph 2 | Existing wording retained; advisory line fit. |
| lect12c-more_gene_trees / 8 | Title wraps | Use the Lower Matrix |
| lect12c-more_gene_trees / 22 | runt in left-1, paragraph 1 | Existing wording retained; advisory line fit. |
| lect12c-more_gene_trees / 23 | runt in left-1, paragraph 1 | Existing wording retained; advisory line fit. |
| lect12e-evol_time / 6 | Title wraps | Substitution Rates in Mammalian Genes |

## Validation and limits

- Strict native Djot lint passed for all 17 expanded masters; final per-folder logs are
  `_temp/lect12_13_1x/lect*_final_lint.log`. All-format builds produced editable ODP and real
  LibreOffice PDFs outside the sandbox. Capacity and typography commands ran for all folders.
- `final_artifacts.json` records authored/hidden/page/marker counts and selectable text totals.
  Every hidden flag matches the authored source; every visible replacement slide has its PDF
  watermark. Source-slide order and original hidden flags reconcile with the source map.
- Base suite: 4,043 passed, 3 failed, 87 errors. The failures/errors come from existing
  Biotechnology LECT10 working-tree conflicts/malformed section content and a duplicate left
  slot in `set5_cancer.djot:503`. Those pre-existing edits were not changed. This is not a
  clean full-suite result. Log: `_temp/lect12_13_1x/pytest.log`.
- Attended Impress click playback, classroom/Zoom testing, remote historical spreadsheet
  access, and independent scientific fact-checks were not performed. Static PDF review
  does not certify animation behavior. Source reveals remain marked where not preserved.
- Extracted media/import reports and generated ODP/PDF are ignored by Git. They are present
  in this checkout; a source-only Git handoff does not contain all teaching media.

## Conversion checklist

Copied from the repository conversion checklist. Checked review items can retain documented
replacement outcomes. N/A and unperformed checks are annotated explicitly.

### Inventory the inputs

- [x] List every source ODP and existing Djot deck in the review report; identify the version
  being converted and the canonical announcement deck before copying or importing anything.
- [x] Record each source deck's authored slide count, hidden slide numbers, section order,
  and slides with animations or answer reveals.
- [x] Generate or locate a source PDF for visual comparison. Map source slide numbers to
  visible PDF pages, explicitly accounting for hidden slides.
- [x] Record the lecture date and the schedule/spreadsheet used for weekly updates, including
  its path or URL. Identify the instructor-cleaned announcement deck used as a format example.

### Initial conversion and assembly

- [x] Follow the instructor-edited announcement formatting: put very long URLs in `@citation`,
  keeping their complete clickable destinations.
- [x] Show the quiz-guidance group if a quiz is this week or next week; hide it otherwise.
  Control the included group's visibility with one `hidden` setting.
- [x] Reference course-wide evergreen groups for recurring opening slides and quiz/exam guidance.
  Keep the agenda, selected icebreaker/podcast, assessment colors, and dated deadlines weekly.
- [x] Retain first-week assignments and future course-evaluation slides as hidden reusable
  groups. Verify their inventory survives the weekly update; refresh dates before showing them.

- [x] Keep source filenames, source slide numbers, and conversion provenance out of Djot files,
  including `@notes` and comments. Use separate import reports, slide maps, or review files for
  traceability; reserve `@notes` for presentation note cards used while lecturing. Exclude selection history,
  publication metadata, refresh commands, repair details, and verification logs from Djot files.

- [x] Import each source with the repository importer documented in [USAGE.md](../../../docs/USAGE.md).
  Save the generated Djot, component assets, and import report; list their paths in the review.
  For an existing conversion, locate these artifacts instead of overwriting reviewed source.
- [x] Build a source-to-Djot slide map. Account for every source slide, its relative order,
  and hidden status; verify one-to-one correspondence through existing content and list added
  slides separately so counts reconcile. Record human approval for any source-slide splitting.
- [x] Update each cover's course, lecture number, date, and topic. Check the rendered cover
  against the cover requirements in the pedagogical guide.
- [x] Verify each cover's chapter number against the relevant BPW course index linked from
  [HUMAN_GUIDANCE.md](../../../docs/HUMAN_GUIDANCE.md). Do not infer it from the lecture number;
  announcements have no chapter.
- [x] Locate the learning objectives in each content deck. If absent, add content-derived
  objectives on slide 2; record the resulting slide number.
- [x] Inspect generated objectives for runts. Shorten generated wording to one line where practical;
  otherwise avoid a single-word final line and aim for a final line at least one-third of the text
  width. Recheck the render. Preserve instructor-authored wording unless edits are authorized.
- [x] Run `python3 deck_tools.py audit <djot-file-or-folder>` using the repository Python
  environment. The audit exempts final-paragraph runts at maximum body size.
  Review title-wrap and runt findings against the rendered slides; record skipped
  coverage and unresolved warnings. Findings are advisory, not automatic wording changes.
- [x] Verify condensed URLs remain intact after independent sizing down to 12 pt. Review
  `url-too-wide` audit warnings; preserve complete displayed addresses and clickable destinations.
- [x] Compare important terminology with previous lectures and locate existing definitions.
  If useful, add a definitions slide near the beginning for important terms new to the lecture
  sequence. Keep definitions concise and limited to terms used in the lecture; list the added
  slide in the slide map.
- [x] Locate the closing summary in each content deck. If absent, add content-derived
  takeaways immediately before THE END; verify the closing slide order in the PDF.
- [x] Check section boundaries against the existing lecture outline. Insert missing dividers
  only to label existing topic boundaries, without reorganizing the teaching sequence;
  list any inserted dividers in the slide map.

### Recurring lecture announcement updates

Use [../../../docs/slide-specs/ANNOUNCEMENT_DECK_GUIDE.md](../../../docs/slide-specs/ANNOUNCEMENT_DECK_GUIDE.md) for the announcement order,
section hierarchy, seasonal groups, and signup/profile deadlines.

- [x] Replace the copied agenda with this lecture's topics and activities; compare each agenda
  item with the content decks and current course schedule.
- [x] Check every assessment and assignment date against the schedule/spreadsheet. Update
  relative wording, deadline/status colors, and expired assignment entries for the lecture date.
- [x] Compare announcement visibility with this week's plan. Record every changed hidden flag;
  confirm evergreen Discord information remains even when its signup assignment expires.
- [x] Select the week's icebreaker explicitly from `evergreen/icebreakers.yaml` or an instructor selection.
  Copy its prompt/examples and remove any stale week/date label; record the selected catalog key.
- [x] Preview the StVC refresh with
  `source source_me.sh && python3 -m slide_lib.refresh_podcast DECK.djot`.
  Inspect the selected episode before applying `--write`.
- [ ] November 9 episode selected; refresh nearer the future lecture date. Confirm the latest published regular StVC episode available on the lecture date, excluding
  specials, and use it as the default. Record its number; if another episode is more appropriate,
  select it and document why.
- [x] Snapshot identity/links checked; browser playback untested. Verify the saved StVC episode number/title, video URL, thumbnail, and playable game/tool
  URL all refer to the selected episode. Open both links and inspect the downloaded image.
- [x] Inspect the rendered StVC slide: confirm three caption lines, visible clickable video
  and game/tool URLs, and placement immediately after the YouTube channel slide.
- [x] Check the YouTube channel, anonymous-message, Discord, and applicable Zoom slides.
  Verify their images/QR codes and visible clickable URLs; keep private course URLs in
  `course_links.local.yaml` through `{{course_url:key}}` references.

### Repair individual slides

- [ ] Visible pages compared; hidden content checked as text/XML only. Compare every source slide with its rendered conversion, including slides without importer
  warnings. Record missing text, labels, objects, emphasis, and changed reading order by slide.
- [x] Inspect the content underneath existing replacement watermarks using separate diagnostic
  copies. Reassess the actual failure rather than inheriting an old import warning. Keep diagnostic
  copies clearly labeled; removing a watermark for inspection does not clear the canonical marker.
- [x] Copy colored text and emphasis faithfully from the source: match colors, colored spans,
  bold, underline, and cross-references in the Djot and rendered PDF. Do not flatten colored text
  during conversion. Check repeated procedure slides against the same canonical colored version.
- [ ] N/A: no new three-point testcross problem. Before a new three-point testcross problem, repeat the matching colored roadmap: the
  pairwise-distance checklist for full mapping, or the DCO checklist for quick gene-order exercises.
  Keep the two methods' step numbering distinct. Use the fixed [COLOR_PALETTE.md](../../../docs/COLOR_PALETTE.md)
  colors in rainbow order, with matching colored step cross-references.
- [x] Remove textbook figure-number artifacts from titles, captions, citations, and editable
  diagram labels. Keep meaningful explanatory captions and all diagram content.
- [x] Wrapped titles retained; shorter wording proposed above for review. Inspect every rendered title for single-line fit, following the preference in
  [HUMAN_GUIDANCE.md](../../../docs/HUMAN_GUIDANCE.md). Flag wrapping titles and record proposed shorter
  wording for review; permission to rewrite titles remains separate from checking their length.
- [x] For textbook diagrams assembled from artwork and positioned labels, compare label placement,
  arrows, and diagram relationships with the source. Record whether a labeled image reconstruction
  is a suitable repair; retain the replacement marker until the rendered result is verified.
- [ ] N/A: no new labeled-image reconstruction. Where suitable, use one quality-90 WebP inside SVG with live overlapping labels. Keep titles,
  captions, surrounding prose, and native tables outside the asset. Verify the LibreOffice render
  and review any source reveals separately; a static figure does not certify animation fidelity.
- [x] Preserve source vector figures as vectors with live labels. Restore static diagram highlights
  and masks within their figure, and preserve paint order so hidden answers do not reappear above
  opaque masks. Verify both masked and unmasked regions against the source.
- [x] Check each figure's identity against the source render, including orientation and cropping;
  a plausible diagram or matching subject is insufficient evidence that it is the right asset.
- [x] Static-mask losses retained as replacement tasks; no new click masks authored. Distinguish static masks from actual reveal targets using the source ODP. Use an image-relative
  native cover for an explicitly intended click-to-remove image mask; check bounds against the final
  displayed image. Test native targets/order and record unperformed click playback separately.
- [x] Confirm local headings and all other content share region sizing, and subsection backgrounds
  follow the course accent. Do not compensate for allocation defects by rewriting source prose.
- [x] For sequential text/image content split across panels, try the existing one-panel mixed
  flow and compare the render. Keep the grouping with readable labels and correct reading order;
  record unresolved fit failures rather than adding a special layout.
- [x] Inspect images for excess borders and composite panels. Trim empty margins and cut,
  split, or crop images where this improves their fit and associations with nearby text.
  Use derived assets or cropped views so the original remains recoverable. Compare against
  the source to preserve labels, arrows, scale bars, legends, and meaningful spacing; update
  overlapping label coordinates when cropping labeled images. Image splitting is authorized;
  splitting slides still requires human approval.
- [x] Run the [image-area audit](../../../docs/USAGE.md#audit-image-shrinkage) for matching source/conversion
  slides. Inspect flagged shrinkage and record the chosen repair or retained review reason;
  after slide insertions, use the source map rather than assuming page numbers still align.
- [x] Compare every table's headers, values, totals, blank calculation cells, and progressive
  steps with the source. Rebuild representable tables as native tables and inspect their PDF.
- [x] Inspect rendered equations and genetic notation against the source: fractions, chi-square,
  allele superscripts, generation subscripts, and H~0~. Correct misplaced or baseline characters.
- [ ] Static states/source animation inventory checked; attended playback unperformed. Compare source animation targets/order with the converted reveals. Inspect final PDF states
  and test click playback in Impress for affected slides, or explicitly record playback as untested.
- [x] For each unresolved slide, add or retain `@replaceme` and record its source number, specific
  missing feature, and next action. When readable sizing cannot fit, retain the source slide with
  `@replaceme`, the preferred outcome over splitting. Do not make splitting the default repair;
  any split requires human approval.
- [x] Before clearing any replacement marker, compare the repaired render with the original and
  verify the previously missing content or behavior; record the evidence in the review report.

### Build and hand off

- [x] Run `source source_me.sh && python3 deck_tools.py lint --require-native
  --native-executable "$(command -v jotdown)" LECTURE_DIR` as one command.
  Save its result and resolve parser/semantic errors.
- [x] Run `source source_me.sh && python3 deck_tools.py capacity LECTURE_DIR`.
  Inspect each diagnostic and record a repair or slide-specific unresolved finding.
- [x] Run `source source_me.sh && python3 deck_tools.py build LECTURE_DIR --format all`
  outside the sandbox. Confirm an editable ODP and ODP-derived PDF exist for every deck.
- [x] Inspect every visible PDF page against the source using
  [the visual review rubric](../../../docs/slide-specs/SLIDE_VISUAL_REVIEW_RUBRIC.md) as assessment guidance. Inspect dense
  text, small diagram labels, tables, and repaired slides at readable size; record problems and
  repairs, then rerender and recheck subsequent edits. Routine conversion review does not require
  per-slide numerical scores; the separate scored review is advisory and runs on demand.
- [x] Reconcile final ODP authored counts and PDF visible counts with the slide map, hidden flags,
  and added slides. Count remaining replacement markers per deck and list their source numbers.
- [x] Finish the lecture review report with output paths, validation results, repaired slides,
  unresolved slides, and unperformed checks. Distinguish reviewed draft completion from
  classroom readiness when replacement slides remain.
- [x] Add a concise conversion/review entry to [CHANGELOG.md](../../../docs/CHANGELOG.md), naming the lecture
  and resulting artifacts; report the review and output paths to the instructor.
