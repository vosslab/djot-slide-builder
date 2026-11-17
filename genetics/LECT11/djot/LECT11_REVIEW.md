# Lecture 11 refresh review

The November 14, 2026 refresh replaces B-D with new teaching sequences; the historical
conversion counts, markers, and one-to-one mappings below do not describe those decks now.
The November 17 announcements have the corrected agenda and dates. The November 17
11B restoration below supersedes the November 14 conceptual rewrite for that deck. F (formerly E) retains its original
content and its unresolved source-5/Djot-7 substitution figure, including the replacement
marker and detached labels. See [GENETICS_GENE_TREE_REFRESH_REPORT.md](../../../docs/GENETICS_GENE_TREE_REFRESH_REPORT.md)
for current sources, accepted reviews, and preserved-deck limitations. Current A/B/C/D/E/F
PDF page counts are 36/30/59/38/65/19; A retains 57 authored ODP slides including hidden slides.

## November 17 classroom updates

- Refresh and show the November 17 NWS Chicago five-day outlook (PDF 3).
- Add *The Animal Kingdom* to the agenda (PDF 2).
- Replace the short movie announcement with the plot, ratings, details, review, and poster
  imported from `movie-slide-maker/the_animal_kingdom_2023.odp`. Text remains editable.
  The former PDF 26 is now PDF 27 because the weather slide is visible.
- Confirm that LECT08 used the exact animal-modification icebreaker; retain the question
  pending the instructor's choice of a replacement.
- Rebuild A only, pass strict native Djot lint, and visually inspect the agenda, weather,
  and movie PDF pages. Movie body text fits at 16.75 pt, below the preferred 20 pt floor;
  preserve the supplied movie wording. No attended Impress playback check.

## November 17 evergreen audit

- Read every included shared/course fragment, including hidden exam, quiz, first-week,
  evaluation, and club groups. Compare office hours and assessments with the current
  instructor-information and Genetics grading syllabus pages; verify the textbook destination.
- Refresh StVC to regular Episode 39, published November 12, using the current playlist feed
  and thumbnail. Skip Special Episode 38. Episode 39 supplies no project URL, so retain only
  its verified video link. The refresh helper refuses that missing project link; update the
  lecture source directly without changing shared tooling.
- Align LECT11 assessment overview, interruption recovery, quiz counts/timing, and optional
  group scoring with the current syllabus. Use lecture-local copies of the three affected
  fragments to keep other lectures and shared evergreen sources untouched.
- Registrar confirms Spring 2027 registration began October 30, with all listed student
  groups eligible by November 13. Retain the accurate start date and current course listings
  supplied November 5 and preserved in `evergreen/UPCOMING_COURSES_SOURCES.md`.
- Preserve the recorded Quiz 4 move to December 1 despite the older public schedule showing
  November 17. Keep first-week signup, exam/quiz guidance, evaluations, and club hidden.
  No public current evaluation window was verified; do not claim evaluations are open.
- Strict native lint and the LECT11A ODP/PDF build pass (56 authored / 35 visible).
  Visually inspect the nineteen visible evergreen/informational pages. Existing small-font
  advisories remain; no attended Impress playback or authenticated portal check.
- Sources: https://vosslab.github.io/syllabus/fall_2026/shared/INSTRUCTOR_INFORMATION/
  and https://vosslab.github.io/syllabus/fall_2026/genetics/ASSIGNMENTS_AND_GRADING/
  and https://www.roosevelt.edu/current-students/academics/register-classes

## Historical conversion review

Historical review: this bundle became LECT11 on November 14, 2026. Original lecture
numbers, dates, slide numbers, and results below describe the earlier conversion.

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
[LECT11_SOURCE_MAP.md](LECT11_SOURCE_MAP.md) maps all original content slides and additions.

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

## November 17 StVC selection correction

Use Episode 36, *Bad Cell Day - Two Drugs, One Keyboard*, at the instructor's request
for variety; Episode 39 is not ready for this announcement. Save Episode 36's own
thumbnail, video link, and published Bad Cell Day project link. This explicit selection
overrides the latest-regular-episode rule and the Episode 39 audit entry above.
Rebuild only LECT11A and visually inspect PDF 8.

## November 17 icebreaker correction

Replace the repeated LECT08 animal-modification prompt with "Which animal would make
the worst roommate, and why?" Use the native prompt layout and face-to-face Icebreaker title.
Check available Genetics LECT01-10 Djot sources, including hidden alternatives, for matching
wording and premise. No animal-roommate prompt appears in those sources; LECT02 has no
announcement Djot in this checkout. Earlier available questions concern outdoor activities,
popular culture, pets, animal modification, robot chores, and food classification.
The new whole-semester non-repetition rule and REPLACEME fallback are recorded in human
guidance, the announcement guide, and the reusable prompt catalog.

## November 17 agenda chapter grouping

Group Gene Trees, Gene Tree Group Activity, and Evolutionary Time under Chapter 11,
as requested. Match LECT10's blue chapter label and nested topic bullets.
Keep Movie Night and homework as separate agenda items.

## November 17 next-class lookahead

Title the lookahead Next Class: December 1, 2026. Retain the November 24 Thanksgiving
break reminder and December 1 class/Group Quiz 4 reminder. Remove December 8 and 15
items from this slide; their dedicated schedule/due-date slides retain those dates.

## Original ODP agenda comparison

Use the instructor's `genetics/**/lect??a*.odp` files as agenda references; ARTIFACTS
was a reference to another repository. Read every matching ODP's agenda text and list
nesting, and visually inspect existing LECT10/LECT11 2025 PDF page 2.

- LECT03 2026 authored slide 2 groups activities/topics under Chapter 1 and Chapter 2.
- LECT08 2025 authored slide 4 and LECT10 2025 authored slide 3 use chapter parent
  bullets with short nested topic labels; LECT10 includes Chapter 8 and Chapter 9.
- LECT11 2025 authored slide 3 groups chromosome topics under Chapter 9; its alternative
  movie agenda on authored slide 4 groups GATTACA and runtime under Feature Film.
  Only the movie agenda appears in its saved PDF, on page 2.
- LECT12/13 2025 similarly group chromosome topics by chapter. Other 2026 agendas
  sometimes use flat topic lists or a named unit instead of a chapter number.
- Current LECT11 matches the chapter/topic hierarchy and concise labels. Its explicit
  No Quiz and homework reminders add logistics compared with the older agendas, which
  usually end with Closing Remarks. Current LECT11's movie title is on one line; the
  old movie agenda uses a separate parent heading and indented movie/runtime details.

No further agenda changes are made by this comparison.

## November 17 office-hours hierarchy

Apply the requested humanizer pass and the instructor's explicit format,
"Wed 2:30-3:30pm". Put Wednesday and Thursday schedules first in bold office-hours
green; place appointment, room, and a labeled clickable Zoom link below. Keep the
existing note illustration. Use a LECT11-local instructor-contact fragment so other
lectures remain unchanged. Preserve actual meeting times and destinations.

## November 17 agenda logistics correction

Remove the homework reminder from the agenda; retain "Today: No Quiz" because the quiz
moved from the earlier schedule. Homework dates remain on their dedicated slides.

## November 17 syllabus URL review

The exported ODP and PDF already use IBM Plex Sans Condensed for literal syllabus
URLs, starting 2 pt below ordinary text and shrinking long addresses independently.
Correct the source grouping: each label and its URL are now one bullet with an explicit
line break, rather than eight equal-level bullets. Keep all four complete addresses.
Rebuild LECT11A, pass strict native lint, inspect PDF 15, and inspect PDF font spans
and hyperlink targets: four intact URLs use IBMPlexSansCond at 26, 25.5, 19.5, and
26 pt, with four clickable link annotations. Additional intended URL formatting is
pending instructor clarification; do not claim that an unspecified rule was verified.

## November 17 URL size and lookahead outline

The instructor clarified that syllabus labels should be flat text and URLs should be
bullets. Update that source and reduce automatic URL sizing from a 2 pt reduction to
80% of surrounding text, retaining condensed type, independent fitting, and the 12 pt
floor. The shared helper affects future builds; rebuild only LECT11 for this task.

Outline the next class by topics, quiz, and homework. Keep the Thanksgiving reminder,
Chromosome Abnormalities Part 2, Group Quiz 4, and no homework due December 1. Dedicated
homework slides show November 17 and December 8 deadlines; do not bring those later
deadlines back into the lookahead. Original LECT08 2025's no-class notice mentions an
assignment; the announcement guide also calls for work due at the next meeting.

Verification: strict native lint, pyflakes, and the full base suite pass (9,285 tests).
The export test now checks the shared URL-size policy with float tolerance instead of
assuming the retired 2 pt reduction. Rebuild LECT11A and visually inspect PDF 5 and 15.
Syllabus URLs render in condensed type at 22/22/19.5/22 pt with four clickable targets.
Existing capacity advisories remain on weather, contacts, movie, and course-promotion
slides; no live Impress playback check.

## November 17 anonymous-message bullets

Use three bullets for the original anonymous-message wording, matching the textbook
slide's text/image structure. Retain the form image and full citation URL.

## November 17 quiz-schedule color correction

Make Quiz 4: Dec 01 dark red (#990000): it is at the next class meeting after the
Thanksgiving break. Next-class timing determines the color, not the next calendar week.

## November 17 illness-policy source emphasis

Compare the original LECT11 2025 ODP authored slide 26 and PDF page 18. Restore
its #C9211E emphasis on "If you are sick, let me know. I will provide an extension."
Keep the four original bullets and wording. LECT10 2025 authored slide 25 confirms
the same emphasis. Limit the repair to the LECT11-local assessment fragment.

## November 17 movie character and content advisory

Render the restored `movie-slide-maker/the_animal_kingdom_2023.odp` using the repo's
LibreOffice exporter. Its single visible movie page has a highlighted bold IMDb 6.7,
13k votes, and a green Metacritic 69 mark. It contains no Rotten Tomatoes row.
Restore the IMDb highlight with native Djot highlighting and retain the source plot,
review, metadata, and poster. Add tomato/trophy and popcorn marks with live verified
RT scores, 83% critics / 76% audience, from https://www.rottentomatoes.com/m/the_animal_kingdom
(retrieved November 17). The older LECT10 snapshot has audience 75%; use today's value
for this added row. Highlight color follows the native Djot highlight treatment rather
than an exact new gold-color style; the source header is red and the course header blue.

Add a second movie slide immediately afterward with all five categories/severities from
the instructor-supplied IMDb Parents Guide excerpt and concise content examples.
Omit transient vote counts. Keep the advisory native/editable; do not insert a screenshot.

Movie delivery verification: strict native lint and 341 documentation checks pass.
Build yields 57 authored / 36 visible slides. Visually inspect overview PDF 27 and
advisory PDF 28 against the rendered source. Rating marks and IMDb highlighting are
visible; text remains native. Preserve the original poster/plot/review. The overview
fits at 15.75 pt and the advisory's details at 17 pt, below the preferred 20 pt floor;
no clipping is visible. No live Impress playback check.

## November 17 upcoming-course colors

Update the shared spring-registration fragment's four promotion slides and summary
with the requested course identities: Biochemistry Lecture #6B638F, Biochemistry Lab
#C9211E, Cellular and Molecular Biology #24578F, and Biology and Ethics in Film #45405C.
Apply color to titles, summary course names, semester labels, and selected teaching
labels; keep ordinary prose dark and BIOL 301's tentative assignment red. Existing
course-palette colors supply the shades; the darker biochemistry shade identifies film.
Rebuild only LECT11; other consumers receive the shared change on their next build.

Course-color verification: strict native lint and 341 documentation checks pass.
Rebuild LECT11A and visually inspect PDF 31-35 (summary plus four course slides);
colors, tentative warning, and course content remain legible with no clipping.

## November 17 content-advisory table

Replace the five content-rating bullets with a native two-column Content/Rating table.
Preserve all categories, severity colors, and the adjacent content examples and citation.

## November 17 original 11B content recovery

The instructor rejected the loss of original illustrations and the flat replacement trees.
Recover 35 original conceptual slides (original 2-37 except duplicate 27), with native
text, original embedded figures, and reviewed layouts. Current 11B has 61 visible pages.

- Restore Darwin's notebook, evolutionary examples/finches, the illustrated gene-tree
  overview, primate trees, three question/answer pairs, and the original annotated
  branch-point/MRCA/polytomy diagrams.
- Restore the Khan Academy equivalent-tree figure (original 21 -> current PDF 22),
  the hand-annotated rotation figure (original 22 -> current 23), and the four equivalent
  drawings (original 23 -> current 24). Retain the original citation.
- Restore the hemoglobin alignment, illustrated distance matrix/UPGMA/neighbor-joining
  pages, colored parsimony example, and likelihood/Bayesian methods material.
- Replace the new p/q/r concept tree with the original scaled four-sequence tree and
  native questions/explicit branch-sum answers (PDF 26-27).
- Keep the checked four-sequence UPGMA worked example (PDF 45-59); the original
  rhinoceros walkthrough is not reintroduced. Preserve every matrix value, height,
  question/answer step, and branch geometry in this retained example.
- Color only 11B's tree copies: a/c clade purple #A719DB, b/d teal #00775F, connecting
  root branches dark purple #45405C. Keep labels bold and branches slightly heavier.
  Use the local `lect11c_four_steps.djot` fragment so C/D and the shared recipe stay intact.
- Recover embedded image components at original pixel dimensions as quality-90 WebP;
  keep text/choices/citations native, rather than inserting full-slide screenshots.

Verification: strict native lint passes. A geometry comparison confirms all four tree
SVG copies preserve coordinates, paths, text, heights, and distances; only paint and
weight change. All 61 exported PDF pages are visually inspected as contact sheets,
with the restored figures visible and no clipping. Only original-slide 7/current 8
and character-methods/current 35 retain sub-20 pt capacity advisories. High-resolution
review targets PDF 22-24, 26-27, 37, and 57. Live Impress playback remains untested.
Original sources are `genetics/LECT11/lect11b-gene_trees.odp` and its saved PDF.

Final recovery checks: pyflakes and 344 focused checks pass. The local four-sequence
fragment matches its checked predecessor exactly after normalizing only asset paths.
An ODP/PDF text comparison caught a stale LibreOffice export of PDF 27; export the
final ODP from a fresh temporary filename and replace the final PDF. Confirm the final
PDF contains the explicit 3.2 + 3.1 + 2.4 + 8.7 = 17.4 branch sum. Reinspect the final
PDF 27; both delivered artifacts now match. Temporary evidence is in
`_temp/lect11b_recovery_final/` and `_temp/lect11b_*`.

## November 17: stable 11C and 11D matrix sizes

The repeated distance matrices now use fixed 22 pt cell text. Answer borders keep
the grid thickness of 0.5 pt, preventing highlighted cells from changing row heights.
The recipe and five/six-sequence fragments agree; 11B was not regenerated.
Both ODP/PDF pairs were rebuilt. Exact ODP frame positions, dimensions, row heights,
and column widths match across every repeated matrix shape in each deck (27 matrices
total), and matching shapes also have the same dimensions across C and D.
Rendered question/answer/new-distance sequences and final matrices were inspected;
11D initial prompts remain above 20 pt with no build capacity advisories.
Strict native lint and four table-layout tests pass. Evidence and geometry assertions:
`_temp/lect11cd_table_review/`. Live Impress playback was not checked.

## November 17: StVC episode 39 now ready

Instructor requested switching from episode 36 to the updated episode 39. The live
YouTube playlist feed identifies `Iyz6WX2r8Rg` as Red Dead Cell Counter - Count the
Red Dots. Its explicit Project line points to `https://vosslab.github.io/red-dead-cell-counter/`;
the secondary Plaque Attack link is not the featured destination. The normal refresh
helper rejects the two Pages links, so select the requested episode and explicit
Project line using its existing slide/thumbnail helpers. Save the current 1280 x 720
thumbnail as WebP and label the destination Try the Tool.

Final check: the first thumbnail download returned an old video frame; a timestamped
request retrieved the new COUNT THE RED DOTS artwork. Replace the local WebP and rebuild.
Strict native lint passes (57 authored slides); PDF remains 36 pages, episode on page 8.
The final rendered slide, video hyperlink, primary tool URL, and updated artwork were
checked. The caption fits at 17 pt (below the preferred 18 pt); no clipping observed.
Live Impress playback was not checked. Evidence: `_temp/lect11a_stvc39/`.

## November 17: split interpretation from construction

11B now focuses on interpreting gene trees (29 slides). Move the sequence alignment,
methods overview, distance-matrix definitions, and colored four-sequence UPGMA example
into new 11C, Building a Tree by UPGMA (36 slides). Keep the original instructional
slide blocks in order, and give each deck its own objectives, takeaways, and ending.
Old C/D/E become D/E/F (34/32/19 slides); their content differs only in cover letters.
The local four-sequence fragment is now `lect11c_four_steps.djot` and uses fixed 22 pt
matrix text with 0.5 pt answer borders, matching the five-/six-sequence table fix.
Assets retain their source names. Original source ODPs/PDFs remain unchanged.
Old generated output names were moved to `_temp/lect11_split_before/` to prevent
teaching from stale, ambiguously numbered decks. All five current decks were rebuilt.
Instruction-block preservation and cover-only renumbering assertions pass; strict
native lint passes for 150 slides. Existing Evolutionary Time source-5/Djot-7 figure
limitation remains in F. Live Impress playback was not checked.

Final split verification: 341 documentation/link checks pass. The complete B/C PDF
contact sheets were visually inspected, and all five cover letters/page counts were
checked. Matrix geometry assertions pass across C/D/E. Temporary rendered evidence:
`_temp/lect11_split_review/`.

## November 17: restore the three-rhino introduction in 11C

The original 11B source retains the rhino example (original PDF 38-64). It was absent
from the restored current deck. Add a 17-slide editable walkthrough to 11C at PDF
19-35, before the four-sequence example. Preserve the original northern-white,
southern-white, and black-rhino teaching example, alignment-to-dots progression,
pairwise counts 4/12/8, symmetric matrix, first join at height 2, averaged cluster
distance 10, final root height 5, and branch lengths 2/2/3/5. Alignments and highlighted
positions use editable SVG text; matrices, questions, explanations, and titles stay
native. Tree branches retain purple/teal cues. 11C now has 53 PDF pages.

Correct one internal source typo: the southern-white full sequence has C at position
23 in the original, whereas its dotted version has a match there. Use S at position
23 to match the original dotted version and 4/12/8 matrix. The unchanged full sequence
would give 5/12/7. Assertions check all three 30-letter sequences and every pair count.
These are preserved example fragments; their provenance as empirical rhino sequences
has not been independently verified. Explain that the fitted white-to-black distance
is 10, whereas its two inputs are 12 and 8.

Strict native lint passes (53 slides). The rebuilt 17-slide sequence and detailed
alignment/matrix and final-tree pages were visually inspected. No new capacity warning;
the prior character-methods slide retains its 17.5 pt advisory. Evidence:
`_temp/lect11c_rhino_review/` and `_temp/restore_rhino.py`. Live playback untested.

## November 17: printable activity handout recovered

Recover the original `lect11c-gene_tree_handout.pdf` and ODG from the 2019 SCH
Activities archive. Copy the PDF byte-for-byte to `output/pdf/lect11e-gene_tree_handout.pdf`
and the editable ODG to `genetics/LECT11/lect11e-gene_tree_handout.odg`. Check all
15 upper-triangle distances against `six_gene_worksheet` in the current JSON: exact
match. Visually inspect its one US Letter page: blank update matrices and a large
tree drawing space. The alternate `_2` worksheet has different numbers and is not
selected. Print portrait, single-sided, one page per sheet. No physical print test.
Evidence: `_temp/lect11_handout_review/`.

## November 17: 11B language and vocabulary review

Remove inflated claims (crucial/complexities/underpins/intricate/essential tools/insights)
and explain the comparisons directly. For example, replace the generic importance
claims with shared inherited traits, changes over generations, and the finch-beak
example. Replace Unraveling Gene Trees with What Does a Gene Tree Show? and state
that gene trees estimate relationships among gene sequences. Preserve the original
figures, questions, answer values, rotation sequence, and branching examples.

Add Tree Terms at PDF 9, before interpretation exercises: tip, branch, node/branch
point, root/rooted tree, ancestor, descendant, clade, and expanded MRCA. Keep objectives
in familiar words. Define polytomy as three or more descendant branches, and define
pairwise distance at its exercise. Clarify the gorilla/bonobo question as the age of
their most recent common ancestor. UPGMA stays in 11C. The original scaled-tree image
also contained an embedded UPGMA question; frame its unchanged image below that heading
using `scaled_tree_interpretation.svg`. Original image bytes and all branch numbers
remain unchanged. 11B now has 30 pages. Rebuild ODP/PDF, inspect the full PDF and the
terms slide, and check no clipping or capacity warnings. Live playback untested.
Evidence: `_temp/lect11b_language_review/`; pre-edit source is in `_temp/`.

## November 17: subsection dividers for tree construction

Add six subsection slides to 11C, four to 11D, and four to 11E, bringing their PDF
counts to 59/38/36. Also use subsection styling for the existing rhino tree-building
divider. New headings mark method families, matrix setup, first joins, repeated
updates, cluster weighting, remaining joins, and finished-tree checks. Insert only
between complete teaching sequences; preserve questions with their answer reveals.

All prior teaching-slide blocks remain identical and in order. Update the existing
recipe so five/six-sequence regenerated fragments exactly match the authored sources.
Strict native lint passes for 133 slides; pyflakes passes. Rebuild all three ODP/PDF
pairs and visually review every added/restyled divider. Verify repeated matrix
widths/heights and row/column geometry within each table family and available width.
The rhino full-width and two-panel table layouts intentionally use different widths.
The pre-existing character-methods 17.5 pt advisory remains; no new capacity warnings.
Evidence: `_temp/lect11_subsections_review/` and `_temp/lect11_subsections_before/`.
The printable six-gene handout remains unchanged. Live playback untested.

## November 17: second handout is the extension, with its own answers

Instructor clarified that the original second handout keeps early finishers busy.
Earlier treatment as an alternate worksheet is superseded. Preserve both original
student PDFs and combine them into `output/pdf/lect11e-gene_tree_handouts.pdf`:
page 1 class problem, page 2 extension. Separate extension PDF and editable ODG
copies are also saved under the current 11E stem. The original class PDF had disappeared
from output between builds; recopy it unchanged before assembling the two-page bundle.

The preserved 2025 original activity ODP/PDF has 29 slides and contains only the
class matrix answers. A text/matrix inventory of the 2020-2025 activity ODP copies
found no second-matrix candidates. These checks do not establish absence from every
historic or merged deck. Add the full extension walkthrough to current 11E rather
than attributing newly calculated answers to an unverified old answer key.

Add the original second matrix to `six_gene_extension` in the example JSON, checking
all 15 distances against both printed halves of the original PDF. Reuse the recipe
with distinct extension assets and table groups. The verified joins/distances are
ac/4, df/6, ace/8, bdf/10, abcdef/12; heights are 2/3/4/5/6. Retain exact fractions
32/3 and 38/3 in intermediate matrices. All updated distances weight original genes
equally. Final branch lengths: ac -> a/c = 2; df -> d/f = 3; ace -> ac/e = 2/4;
bdf -> b/df = 5/2; root -> ace/bdf = 2/1. Root-to-tip distance is 6.

The original class teaching content is unchanged. Extension section starts PDF 35,
answers PDF 38-62; 11E now has 64 pages. Native lint and pyflakes pass; rebuild the
ODP/PDF with no capacity advisories. Visually inspect all extension pages and both
printable handouts. Evidence: `_temp/lect11_extension_review/` and
`_temp/lect11_extension_before/`. No live playback or physical print test.

## November 17: consolidate all native 11A reds

Instructor requested one red, #D40000, including next-class reminders and the icebreaker.
Use explicit colors throughout 11A's source tree, including hidden slides. Localize the
shared contact-options, spring-registration, and course-evaluation fragments so this
lecture's consolidation does not recolor other decks. Change only their red attributes.
Every native red style in the rebuilt ODP is now #D40000 (no #990000, #C9211E, or #7B1E2B).
Original icebreaker typography is preserved: Atkinson Hyperlegible Next Bold, 38.75 pt,
matching the pre-change ODP style. The prompt's color wrapper changes only its foreground.

Rebuild the ODP/PDF and export once from a fresh filename to rule out stale formatting.
A PDF text-extraction check misleadingly reported bold glyphs as black; visual inspection
shows the bold question is correctly red. This was an extraction issue, not an export
defect. Native red audit is authoritative for exact values; inspect rendered examples
for appearance. Evidence: `_temp/lect11a_red_review/`. No live Impress playback test.

## November 17: Tree Terms use the standard emphasis palette

Replace muted #355269 with palette Blue #003FFF and #55215B with palette Purple
#A719DB on Tree Terms (PDF 9). Apply the same replacements to the existing matching
branch-point and MRCA references, preserving their associations. Wording, typography,
slide order, and artwork stay unchanged. Rebuild ODP/PDF and visually check PDF 9.
Strict native lint passes; 30 slides remain. No live Impress playback test.

## November 17: saturate the existing primate tree

Instructor clarified that the current tree needs more saturation. Reuse the original
editable SVG recovered as `_temp/assets/lect11b_original_import/image_008.svg`.
Replace its 52 brown fill/stroke attributes, rgb(80,32,12), with palette Blue #003FFF.
All path data, text, font attributes, positions, time labels, and topology are identical
to the original vector source. Set the root viewport to the existing bitmap's 1126 x 757
proportions so the slide keeps its familiar aspect ratio. Keep the gray time axis.
Reference the saturated SVG on all seven uses of this tree (PDF 12-18); the other
primate figures remain unchanged. Original bitmap is preserved. Native lint passes;
rebuild ODP/PDF and inspect the full tree and a question slide. Live playback untested.

## November 17: distinct deck titles and filenames

Rename the canonical masters and generated outputs to match their teaching roles:
- 11B Interpreting Gene Trees: `lect11b-interpreting_gene_trees`.
- 11C Building Gene Trees: Three- and Four-Sequence Examples: `lect11c-building_gene_trees`.
- 11D UPGMA: Five Sequences and Weighted Averages: `lect11d-upgma_weighted_averages`.
- 11E UPGMA Practice: Class and Extension Problems: `lect11e-upgma_group_activity`.
- 11F Molecular Clocks and Evolutionary Time: `lect11f-molecular_clocks`.

Only the cover titles change within the decks; all teaching blocks and included fragments
remain unchanged. Update Markdown links to canonical sources and generated outputs;
original archived ODP/PDF and asset names remain intact. Move superseded generated
filenames into `_temp/lect11_names_before/` to avoid stale duplicates. Handout filenames
remain unchanged. Rebuild all five ODP/PDF pairs, verify cover titles and page counts
30/59/38/64/19, and visually inspect the covers. Native lint passes for 210 slides.
The prior 11C character-methods font advisory and 11F figure marker remain.
Evidence: `_temp/lect11_names_review/`. Live Impress playback untested.

## November 17: color-code the five joins in 11E

Use the documented five-stage rainbow selection: Red #D40000, Dark yellow #6C6C00,
Teal #00775F, Navy #0067CC, Pink #CC0066. Numbered colored Join headings repeat across
each merge's question, answer, and distance updates. Match selected matrix cells and
new cluster labels to each join. Newly created tree branches, their height labels,
and joined tip labels receive the join color; previous branches retain their colors.
Color final node labels in the branch-length summary. Keep ordinary prose neutral.
Add Follow the Join Colors at PDF 7; the extension restarts the same color sequence.
11E now has 65 pages; the extension begins PDF 36, answers PDF 39-63.

The existing recipe owns this behavior for the two six-gene examples. Regenerating
four/five examples with before/after recipe versions gives byte-identical Djot and
SVG output; those canonical artifacts were not regenerated or rebuilt. The two
six-gene histories, all numeric values, SVG path geometry, and text positions match
before/after. Before an answer reveal, the matrix does not highlight the selected
cell. All 30 native tables preserve exact widths/heights and row/column dimensions
against the pre-change export. No new capacity advisories. Native lint and pyflakes
pass. Visually review all changed teaching pages and both completed trees after the
ODP/PDF rebuild. Print handouts remain unchanged. Evidence and assertions:
`_temp/lect11e_stage_colors_review/`, `_temp/check_lect11e_stage_colors.py`.
Live Impress playback untested.

## 11F teaching expansion, November 17

Rebuilt the former 19-page evolutionary-time sequence as 49 bite-size teaching slides.
The central message is that sequence differences need a calibrated rate to become a time
estimate. Four sections follow gene choice, sequence change, calibration, and interpretation.
All nine substantive original figures remain, including a repaired Adh map; the former
replacement marker is resolved. Added 41 speaking notes, early definitions, paired questions
and answers, a two-lineage diagram, a numerical calibration and dating example, and a formula
reference. Corrected the inherited ortholog/paralog definitions and mutation/rate claims.
The beta-globin numbers are explicitly historical teaching assumptions.

See [LECT11H_TEACHING_GUIDE.md](LECT11H_TEACHING_GUIDE.md) for the teaching route, cognitive
walkthrough, scientific corrections, sources, and evidence limits. Strict native lint and
343 focused checks passed. All 49 pages were rendered and reviewed, arithmetic recomputed,
source-image bytes preserved, new diagram contrast measured, and no out-of-page words found.
No student study or attended playback was performed. This supersedes the earlier 11F
figure-placeholder limitation.

## 11A Episode 39 thumbnail refresh, November 17

Downloaded the updated 1280 x 720 YouTube thumbnail for `Iyz6WX2r8Rg` using a
cache-busting request. The revised image gives the hosts Western clothing and hats.
Replaced the local WebP and rebuilt the 11A ODP/PDF; the episode title and links remain.

## 11B primate question/answer pairs and orange tree, November 17

Former PDF slides 13-18 are now three paired questions with native on-click answer reveals,
on current slides 13-15. Kept the two-column layout because the standard multiple-choice
layout limits its top figure to 30 percent of content height. The existing diagram frame
is exactly unchanged on all three questions (12.228125 x 8.220862 cm). Each answer includes
a short explanation. The PDF shows the complete answers for studying. Total deck: 27 pages.

Replaced all 52 saturated-blue tree paint attributes with palette dark orange #B74300
(5.50:1 against white). SVG geometry, labels, time scale, and positions are unchanged.
The introductory tree uses the same orange asset. Strict native lint passes; exported
question pages were visually inspected, and all three reveal objects are present in ODP.
Live click-through in Impress was not tested.

## Second deck split, November 17

Split former 11C at "From Distances to a Tree": current 11C covers sequences and methods
(18 pages), and current 11D contains the complete three-rhino and four-sequence construction
examples (45 pages). Former 11D becomes 11E (38 pages). Split former 11E into current
11F class activity (37 pages) and 11G extension activity (35 pages); each has its own
objectives, procedure, five-color key, complete answers, summary, and end. Former 11F
becomes 11H (49 pages). The molecular-clock teaching guide is now LECT11H_TEACHING_GUIDE.md.

All moved teaching pages were compared against the pre-split exports. Matrices, tree
figures, source assets, and handouts retain their geometry or byte hashes. The H source
is identical to the prior F source except its cover letter; its new export reflects
pre-existing ASCII arrow/multiplication/approximation spellings already in the source.
Current links and source map are updated. Old generated filenames were backed up under
_temp/lect11_second_split_before and removed from the output folders. Original archived
lecture-root sources and printable handout filenames remain unchanged.

Strict native lint passes for all six decks (222 slides). 343 focused link/guidance
checks pass. Covers, summaries, and split boundaries were visually reviewed; all moved
teaching text and table/image-frame geometry were checked. The existing 17.5 pt advisory
on Character-Based Methods remains in C. No attended Impress playback was performed.
