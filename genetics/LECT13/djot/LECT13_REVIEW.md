# LECT13 conversion review

Reviewed draft, November 9, 2026. 4 canonical Djot decks produce editable ODP
and LibreOffice-derived PDF. 70 explicit `@replaceme` slides retain difficult conversions.
Those slides need reconstruction before classroom use.

## November 10 agenda wording

Use short Chapter 9 labels from the original agenda and deck titles: Inversions, Translocations,
and Meiosis Translocations. Mark the Quiz 5
opening and agenda item conditional on the class vote; correct the past Quiz 4 date to December 1.
A retains 55 authored / 18 hidden / 37 PDF pages; its agenda is PDF 3. Rebuilt ODP/PDF, passed
strict native lint, and inspected the agenda and changed logistics. The wording correction passes
213 documentation/guidance checks. Evidence: `_temp/genetics_agendas_09_15/`. Existing weather/registration
capacity advisories remain. The wording correction is verified separately in
`_temp/genetics_agenda_voice/`. The content/date mismatch below remains a scheduling task.

## Outputs and counts

Editable sources are in this directory. Generated artifacts use the same stem under
`output/odp/` and `output/pdf/` at the repository root. The accompanying
[LECT13_SOURCE_MAP.md](LECT13_SOURCE_MAP.md) maps all original content slides and additions.

| Deck | Authored ODP | Hidden | PDF pages | Replacements |
| --- | --- | --- | --- | --- |
| lect13a-2026_announcements | 55 | 18 | 37 | 0 |
| lect13b-chromo_alter_3-inversion | 48 | 0 | 48 | 11 |
| lect13c-chromo_alter_4-translocation | 31 | 0 | 31 | 14 |
| lect13d-meiosis_translocation | 62 | 0 | 62 | 45 |

Total: 196 authored, 18 hidden, 178 PDF pages.
Content decks preserve 132 original slides and add 9 opening/closing slides.
Sibling Djot includes keep long source files below the repository size limit without splitting slides.
Original THE END slides and following appendices retain their order; repeated closing bookends
close appendices where necessary. Existing definition slides serve the introduced vocabulary.

## Inputs and source order

There was no existing Djot in these target folders. Source ODP files were imported with the
repository tools; limited temporary import adapters are described below. All 18 original ODP
SHA-256 hashes across this conversion match the pre-import inventory. Original PDFs were retained.
Raw announcement Djot imports are intermediate evidence under `_temp/lect12_13_1x/`;
their unused extracted artwork was removed, while the import reports remain.

- `lect13a-2025_announcements.odp`: 59 authored; hidden 4-5, 11-12, 14, 16, 29, 35, 38-41, 44-45, 51-52, 58; source animation elements none.
- `lect13b-chromo_alter_3-inversion.odp`: 45 authored; hidden none; source animation elements 8.
- `lect13c-chromo_alter_4-translocation.odp`: 28 authored; hidden none; source animation elements 10, 19, 25, 27.
- `lect13d-meiosis_translocation.odp`: 59 authored; hidden none; source animation elements 43.

Source section order, `lect13b-chromo_alter_3-inversion`: 3 Inversions -> 9 Paracentric Inversion -> 13 Pericentric Inversion -> 32 Position-effect Variegation (PEV) -> 35 The Sparrow with Four Sexes -> 45 THE END.

Source section order, `lect13c-chromo_alter_4-translocation`: 3 Translocations -> 28 THE END.

Source section order, `lect13d-meiosis_translocation`: 6 Separation of Translocated Chromosomes During Cell Division -> 26 Spindle Binding during Cell Division -> 31 Determine the Possible Gametes -> 51 Robertsonian Translocations -> 59 THE END.

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

The canonical announcement deck is `lect13a-2026_announcements.djot`, dated December 8.
The cooking icebreaker comes from `evergreen/icebreakers.yaml`; Group Quiz 5 remains visible.
Quiz 5/homework 11/12 are red for this week and the cumulative final is next week's emphasis.
The old hidden midterm overview/deadlines were replaced by the current final-exam overview,
shared exam guidance, and December 15 homework deadline. That exam group is now visible.
Registration switches from visible in Lecture 12 to hidden after its December 1 window.
Other first-week, evaluation, club, and weather groups remain hidden. The source map records
the complete current visibility inventory.

Inversion B8 loses the additional drawn chromosome example; its animation warning remains.
The scanned book problems largely survive as images, but B25/B28-31 lose crossover arrows
or emphasis boxes. The sparrow B40-41 text was verified before clearing color-only flags.
Translocation C8's annotated Philadelphia-chromosome figure becomes tiny; C13-18 lose drawn
links and boxes. C20/C22 retain complete colored problem text and their flags were cleared.
The multiple-choice examples preserve their options and answers; flagged answer reveals
remain unresolved. They were not rewritten into a new question format.

Meiosis D7-25 loses the colored vector chromosome drawings completely. D27-28 loses label
associations; D33-34 loses gamete/chromosome products. D37-50 loses chromosome geometry,
pairing, and product grouping; D53-55 loses fusion/karyotype annotations or readable size.
These are substantial reconstruction tasks. Their retained prose and extracted media are
available beneath explicit replacement watermarks.

Two importer limitations were handled with temporary adapters: B25's multiple caption
paragraphs fell back to existing ordinary panels, and D's mixed flows with more than six
component images were grouped into existing panels. Image counts were asserted unchanged;
the affected geometry/reveal markers remain. Production importer code was not changed.

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

### lect13b-chromo_alter_3-inversion

Cleared after paired/rendered verification: source 40-41.

- Source 8 -> Djot 10: source reveal/animation not preserved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 12 -> Djot 14: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 14 -> Djot 16: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 21 -> Djot 23: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 22 -> Djot 24: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 25 -> Djot 27: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 28 -> Djot 30: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 29 -> Djot 31: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 30 -> Djot 32: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 31 -> Djot 33: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 34 -> Djot 36: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.

### lect13c-chromo_alter_4-translocation

Cleared after paired/rendered verification: source 20, 22.

- Source 6 -> Djot 8: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 7 -> Djot 9: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 8 -> Djot 10: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 10 -> Djot 12: source reveal/animation not preserved; rework the native layout/figure and compare with the original.
- Source 13 -> Djot 15: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 14 -> Djot 16: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 15 -> Djot 17: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 16 -> Djot 18: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 17 -> Djot 19: figure or notation remains too small or loses source emphasis; rework the native layout/figure and compare with the original.
- Source 18 -> Djot 20: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 19 -> Djot 21: source reveal/animation not preserved; rework the native layout/figure and compare with the original.
- Source 21 -> Djot 23: figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 25 -> Djot 27: source reveal/animation not preserved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 27 -> Djot 29: source reveal/animation not preserved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.

### lect13d-meiosis_translocation

- Source 4 -> Djot 6: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 7 -> Djot 9: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 8 -> Djot 10: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 9 -> Djot 11: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 10 -> Djot 12: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 11 -> Djot 13: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 12 -> Djot 14: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 13 -> Djot 15: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 14 -> Djot 16: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 15 -> Djot 17: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 16 -> Djot 18: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 17 -> Djot 19: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 18 -> Djot 20: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 19 -> Djot 21: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 20 -> Djot 22: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 21 -> Djot 23: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 22 -> Djot 24: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 23 -> Djot 25: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 24 -> Djot 26: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 25 -> Djot 27: colored vector chromosomes absent; reconstruct the chromosome arrangement with live labels.
- Source 27 -> Djot 29: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 28 -> Djot 30: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 29 -> Djot 31: figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 30 -> Djot 32: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 32 -> Djot 34: figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 33 -> Djot 35: chromosome products, grouping, or labels missing/detached; reconstruct the chromosome and gamete figures.
- Source 34 -> Djot 36: chromosome products, grouping, or labels missing/detached; reconstruct the chromosome and gamete figures.
- Source 37 -> Djot 39: chromosome products, grouping, or labels missing/detached; reconstruct the chromosome and gamete figures.
- Source 38 -> Djot 40: chromosome products, grouping, or labels missing/detached; reconstruct the chromosome and gamete figures.
- Source 39 -> Djot 41: chromosome products, grouping, or labels missing/detached; reconstruct the chromosome and gamete figures.
- Source 40 -> Djot 42: chromosome products, grouping, or labels missing/detached; reconstruct the chromosome and gamete figures.
- Source 41 -> Djot 43: chromosome products, grouping, or labels missing/detached; reconstruct the chromosome and gamete figures.
- Source 42 -> Djot 44: chromosome products, grouping, or labels missing/detached; reconstruct the chromosome and gamete figures.
- Source 43 -> Djot 45: chromosome products, grouping, or labels missing/detached; reconstruct the chromosome and gamete figures.
- Source 44 -> Djot 46: chromosome products, grouping, or labels missing/detached; reconstruct the chromosome and gamete figures.
- Source 45 -> Djot 47: chromosome products, grouping, or labels missing/detached; reconstruct the chromosome and gamete figures.
- Source 46 -> Djot 48: chromosome products, grouping, or labels missing/detached; reconstruct the chromosome and gamete figures.
- Source 47 -> Djot 49: chromosome products, grouping, or labels missing/detached; reconstruct the chromosome and gamete figures.
- Source 48 -> Djot 50: chromosome products, grouping, or labels missing/detached; reconstruct the chromosome and gamete figures.
- Source 49 -> Djot 51: chromosome products, grouping, or labels missing/detached; reconstruct the chromosome and gamete figures.
- Source 50 -> Djot 52: chromosome products, grouping, or labels missing/detached; reconstruct the chromosome and gamete figures.
- Source 53 -> Djot 55: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 54 -> Djot 56: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 55 -> Djot 57: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 58 -> Djot 60: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.

## Capacity and typography

Capacity diagnostics are advisory; every mixed-readability failure has an explicit marker.
Other small-font advisories remain where recorded below. Source wording was retained.
The source image-area audit is stored in each import report; flagged shrinkage was visually
compared using the source map, and unresolved figure size/relationships remain marked.

| Deck / Djot | Slot | Cause | Required / floor pt | Review outcome |
| --- | --- | --- | --- | --- |
| lect13a-2026_announcements / 5 | caption | paragraph/list | 15.25 / 18.0 | Below-floor advisory retained; inspect at teaching distance. |
| lect13a-2026_announcements / 44 | left | paragraph/list | 19.75 / 20.0 | Below-floor advisory retained; inspect at teaching distance. |
| lect13a-2026_announcements / 44 | bottom-right | paragraph/list | 18.5 / 20.0 | Below-floor advisory retained; inspect at teaching distance. |
| lect13a-2026_announcements / 45 | body | paragraph/list | 19.75 / 20.0 | Below-floor advisory retained; inspect at teaching distance. |
| lect13b-chromo_alter_3-inversion / 24 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect13c-chromo_alter_4-translocation / 10 | body | mixed-readability | 19.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 6 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 29 | body | mixed-readability | 15.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 30 | left | paragraph/list | 17.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 30 | right | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 32 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 34 | left | paragraph/list | 17.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 34 | top-right | paragraph/list | 13.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 35 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 36 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 39 | body | mixed-readability | 8.5 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 40 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 41 | top-left | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 41 | bottom-right | mixed-readability | 10.5 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 42 | top-left | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 42 | bottom-right | mixed-readability | 9.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 43 | left | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 43 | right | mixed-readability | 16.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 45 | body | paragraph/list | 15.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 46 | body | paragraph/list | 9.75 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 47 | body | paragraph/list | 9.25 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 48 | body | mixed-readability | 15.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 49 | body | mixed-readability | 7.5 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 50 | body | mixed-readability | 7.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 51 | body | paragraph/list | 10.25 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 52 | body | paragraph/list | 14.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 55 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect13d-meiosis_translocation / 60 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |

Typography audit summary: {'runt': 2, 'title-wrap': 11}. Skipped coverage: {'special-layout-titles': 8, 'hidden-slides': 18, 'math-or-explicit-break-paragraphs': 2, 'final-paragraph-runts-at-max-size': 4}.
Existing wrapped titles were retained; possible shorter wording below is a review suggestion only.
No instructor-authored title was shortened solely to silence an audit warning.

| Deck / Djot | Finding | Review or possible shorter title |
| --- | --- | --- |
| lect13a-2026_announcements / 11 | runt in left, paragraph 4 | Existing wording retained; advisory line fit. |
| lect13b-chromo_alter_3-inversion / 7 | Title wraps | Inversions from Ectopic Recombination |
| lect13b-chromo_alter_3-inversion / 8 | Title wraps | Pairing with an Inversion |
| lect13b-chromo_alter_3-inversion / 9 | Title wraps | No Crossing Over in the Inversion Loop |
| lect13b-chromo_alter_3-inversion / 32 | runt in body-1, paragraph 2 | Existing wording retained; advisory line fit. |
| lect13d-meiosis_translocation / 13 | Title wraps | Form Sister Chromatids |
| lect13d-meiosis_translocation / 29 | Title wraps | Translocation Segregation Patterns |
| lect13d-meiosis_translocation / 30 | Title wraps | Translocation Segregation Patterns |
| lect13d-meiosis_translocation / 31 | Title wraps | Translocation Segregation Patterns |
| lect13d-meiosis_translocation / 32 | Title wraps | Translocation Segregation Patterns |
| lect13d-meiosis_translocation / 35 | Title wraps | Two Gametes per Pattern |
| lect13d-meiosis_translocation / 36 | Title wraps | Two Gametes per Pattern |
| lect13d-meiosis_translocation / 55 | Title wraps | Fusion Origin of Human Chromosome 2 |

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
