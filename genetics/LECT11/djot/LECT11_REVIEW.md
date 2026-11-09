# Lecture 11 conversion review

Reviewed draft, November 9, 2026. Five canonical Djot masters produce editable ODP and
LibreOffice-derived PDF. Difficult conversions retain 62 explicit `@replaceme` slides;
this draft is not classroom-ready wherever those watermarks appear.

## Outputs and counts

Sources are in this directory; generated decks are under `output/odp/` and `output/pdf/`
at the repository root. [LECT11_SOURCE_MAP.md](LECT11_SOURCE_MAP.md) maps every original
content slide, hidden status, source PDF page, and final page.

| Deck | Authored ODP | Hidden | PDF pages | Replacement slides |
| --- | --- | --- | --- | --- |
| lect11a-2026_announcements | 55 | 17 | 38 | 0 |
| lect11b-polyploidy | 49 | 1 | 48 | 13 |
| lect11c-sex_dosage | 67 | 0 | 67 | 26 |
| lect11d-chromo_alter_1-deletions | 112 | 0 | 112 | 20 |
| lect11e-chromo_alter_2-duplications | 37 | 0 | 37 | 3 |

Total: 320 authored slides, 18 hidden slides, 302 PDF pages. B-E retain all 253 original
content slides in order and add 12 opening/closing slides. C and D use sibling topic includes
to keep editable source files below the repository size limit. No slides were split.
The original D95 THE END and subsequent book-problem appendix remain in their original order;
a repeated summary and a final THE END close the appendix.

## Inputs and announcements

All six supplied ODP files were imported with `deck_tools.py import`. There was no existing
LECT11 Djot. Original ODP/PDF files were not edited. The deletion-guide ODT/PDF is a handout,
not a slide deck, and remains unchanged. The original announcement imports are intermediate
evidence in `_temp/lect11/*_imported.djot`; their unused extracted images were removed.
All six original import reports remain under `assets/<source-stem>/import_report.json`.

Starting inputs:

- `lect09a-2026_announcements.odp`: 52 authored; hidden: 25, 26, 27, 28, 29, 30, 36, 37, 38, 47, 48, 49, 50, 51; animation/reveal elements: none.
- `lect11a-2025_announcements.odp`: 62 authored; hidden: 4, 5, 11, 12, 14, 16, 26, 27, 28, 29, 30, 38, 39, 40, 41, 43, 44, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61; animation/reveal elements: none.
- `lect11b-polyploidy.odp`: 46 authored; hidden: 2; animation/reveal elements: 12.
- `lect11c-sex_dosage.odp`: 65 authored; hidden: none; animation/reveal elements: 4, 31, 41, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62.
- `lect11d-chromo_alter_1-deletions.odp`: 108 authored; hidden: none; animation/reveal elements: 9.
- `lect11e-chromo_alter_2-duplications.odp`: 34 authored; hidden: none; animation/reveal elements: none.

For 2026 announcements, use the most recent current-year deck for course information and
formatting, and the matching prior-year deck for useful week-specific material. The supplied
current-year file is still Lecture 09; the repository's reviewed Lecture 10A Djot is newer and
supplies current shared groups. The prior-year Lecture 11A supplies the Group Quiz 4 cue and
chromosome topics. The instructor-cleaned Biotechnology Lecture 10A is the shared formatting
example described in the announcement guide; no Biotechnology sources were edited here.

Lecture date: November 17, 2026, from
`/Users/vosslab/nsh/syllabus/site_docs/fall_2026/genetics/SCHEDULE.md`, itself generated from
the [course spreadsheet](https://docs.google.com/spreadsheets/d/1XLZcg8PnW4GyMxFctAKCTvzN9qImIb5S3bK6hyeDz0Q/edit).
The [published schedule](https://vosslab.github.io/syllabus/fall_2026/genetics/SCHEDULE/)
provides the student-facing citation. The local schedule was read; the underlying spreadsheet
was not separately refreshed.

**Schedule mismatch:** that schedule assigns gene trees/population genetics and Movie Night to
November 17, and these chromosome topics to December 1. The supplied LECT11 content and prior-year
agenda control the converted teaching content; the calendar controls quiz/homework deadlines.
No course rescheduling was inferred. Covers use Lecture 11's November 17 date. Review this
content/date correspondence before teaching. No translocation-meiosis deck was supplied, so
none was invented; D retains its original conditional reference to that homework.

Quiz 4 and assignments 09/10 are due November 17; Quiz 4/homework are red for the current week.
Past assessments remain gray and future ones black. The November 24 lookahead states no class
and the December 1 return. Quiz guidance is visible through its single include setting; exam,
first-week assignments, evaluation, and club groups remain hidden. Registration remains visible.
The historical exam-corrections reminder has no verified 2026 deadline and was not promoted.

Selected icebreaker: `modify-an-animal` in `evergreen/icebreakers.yaml`.
Podcast preview with `--by-lecture-date` selected regular episode 37, excluding special 38.
The saved Bad Cell Day title, thumbnail, video, and game agree. YouTube oEmbed and the game
returned HTTP 200; browser playback/gameplay were not tested. The November 9 NWS snapshot
was refreshed with the repository helper and kept hidden because it is too early for the
November 17 lecture. Refresh weather November 16-17 before showing it.

## Repairs and visual findings

All 252 visible original content slides were compared with watermark-free diagnostic renders
in `_temp/lect11/review/`. Final announcement pages and added bookends were inspected in
`_temp/lect11/final_review/`. Contact sheets establish overall content, ordering, and visual
relationships; they do not certify every small label's classroom readability.

- Covers, objectives, section framing, and closing summaries use editable native text.
  Chapter 9 was checked against the [BPW course index](https://biologyproblems.org/genetics/).
  No extra vocabulary slide was needed: definitions already appear near the relevant material.
- B20's colored GMO answers were restored to two columns with the complete legend in a citation.
  The final render preserves all ten choices and their emphasis. Its original question title
  still wraps, as it did in the source; no unapproved title rewrite was made.
- B31-32's figure-number-only titles now read Hybridization Between Species. Bitmap figure
  numbers remain baked into some original textbook images; those image pixels were not edited.
- D44-89 preserve the four-gene/six-gene problems, intermediate gene orders, gray deemphasis,
  purple active deletions, and colored verification steps. Color-only importer markers were
  cleared after paired comparison. D12, D18, D22, D24, D93, and D101 also preserve the visible
  content despite conservative import flags. Source animations were not cleared on that basis.
- C13 and C23-25 retain the complete visible source image/problem content; their non-content
  frame/bounds warnings were cleared. The missing-label implementation message on C29 was
  removed from student-facing content; its replacement marker remains.
- E30's table retains its complete visible contents; its unsupported-frame warning was cleared.
  Decorative unsupported shapes on original closing slides were replaced by native THE END
  layouts, after checking that no teaching content was missing.
- B27/B37 and E26 received additional markers for materially reduced figure/text readability.
  D91 received a marker for the still-small dense challenge prompt. Source prose was retained.
- Image-area shrinkage was audited by the importer before additions. The original per-image
  values remain in the import reports. The source map accounts for later numbering shifts.
  Many image-only figures remain usable despite a numeric area warning; tiny isolated artwork,
  missing connectors, and detached labels retain replacement markers. No special layouts were added.

Conversion preserves original scientific claims rather than treating them as newly verified.
Examples needing separate content review include B's dated GMO salmon availability and C10's
claim that the fly dosage-compensation complex is on the Y. These were not silently corrected.

## Unresolved conversions

Numbers below are original source ODP slides. The source map gives final Djot/PDF numbers.
Retained source text and assets are editable under the watermark; original ODP/PDF remains the
reference for missing relationships. Replacement is an accepted conversion outcome.

### lect11b-polyploidy

- Source 8 -> Djot 10: readable fit unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 12 -> Djot 14: source reveal/animation not preserved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 23 -> Djot 25: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 27 -> Djot 29: figure/text readability reduced in conversion. Rework the native layout/figure and compare with the original before clearing.
- Source 30 -> Djot 32: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 31 -> Djot 33: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 32 -> Djot 34: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 33 -> Djot 35: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 34 -> Djot 36: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 36 -> Djot 38: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 37 -> Djot 39: figure/text readability reduced in conversion. Rework the native layout/figure and compare with the original before clearing.
- Source 38 -> Djot 40: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 43 -> Djot 45: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.

### lect11c-sex_dosage

- Source 4 -> Djot 5: source reveal/animation not preserved; readable fit unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 5 -> Djot 6: readable fit unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 6 -> Djot 7: readable fit unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 17 -> Djot 18: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 28 -> Djot 29: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 29 -> Djot 30: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 41 -> Djot 42: source reveal/animation not preserved. Rework the native layout/figure and compare with the original before clearing.
- Source 44 -> Djot 45: figure/text readability reduced in conversion. Rework the native layout/figure and compare with the original before clearing.
- Source 45 -> Djot 46: readable fit unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 46 -> Djot 47: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 47 -> Djot 48: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 49 -> Djot 50: source reveal/animation not preserved; readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 50 -> Djot 51: source reveal/animation not preserved; readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 51 -> Djot 52: source reveal/animation not preserved; readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 52 -> Djot 53: source reveal/animation not preserved; readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 53 -> Djot 54: source reveal/animation not preserved; readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 54 -> Djot 55: source reveal/animation not preserved; readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 55 -> Djot 56: source reveal/animation not preserved; readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 56 -> Djot 57: source reveal/animation not preserved; readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 57 -> Djot 58: source reveal/animation not preserved; readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 58 -> Djot 59: source reveal/animation not preserved; readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 59 -> Djot 60: source reveal/animation not preserved; readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 60 -> Djot 61: source reveal/animation not preserved; readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 61 -> Djot 62: source reveal/animation not preserved; readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 62 -> Djot 63: source reveal/animation not preserved; readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 64 -> Djot 65: diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.

### lect11d-chromo_alter_1-deletions

- Source 14 -> Djot 15: readable fit unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 19 -> Djot 20: diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 29 -> Djot 30: diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 30 -> Djot 31: diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 31 -> Djot 32: diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 32 -> Djot 33: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 33 -> Djot 34: diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 34 -> Djot 35: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 35 -> Djot 36: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 36 -> Djot 37: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 37 -> Djot 38: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 38 -> Djot 39: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 39 -> Djot 40: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 40 -> Djot 41: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 41 -> Djot 42: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 91 -> Djot 92: figure/text readability reduced in conversion. Rework the native layout/figure and compare with the original before clearing.
- Source 92 -> Djot 93: readable fit unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 94 -> Djot 95: readable fit unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 99 -> Djot 101: readable fit unresolved; diagram geometry, labels, or source grouping unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 108 -> Djot 110: readable fit unresolved. Rework the native layout/figure and compare with the original before clearing.

### lect11e-chromo_alter_2-duplications

- Source 14 -> Djot 16: readable fit unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 20 -> Djot 22: readable fit unresolved. Rework the native layout/figure and compare with the original before clearing.
- Source 26 -> Djot 28: figure/text readability reduced in conversion. Rework the native layout/figure and compare with the original before clearing.

## Validation and limits

- Strict native lint passed for all five expanded masters: 320 slides, 165 image occurrences.
- Scoped Markdown-link, cover-contract, ASCII, line-limit, and whitespace checks pass for the
  changed guidance and new LECT11 files. No permanent tests or application code were added.
- All-format builds passed outside the sandbox. Verified native ODP authored/hidden counts
  against parsed Djot, reconciled every PDF page count, and checked visible replacement text
  for every marked slide. Exported PDFs retain selectable text on the covers and teaching prose.
- Capacity and typography audits ran. Source-located evidence is in
  `_temp/lect11/final_capacity.log` and `_temp/lect11/final_audit.json`.
  Mixed-readability failures all have explicit Djot markers. Other below-20-pt capacity
  advisories remain, including small reference text; no claim of uniform classroom readability.
- The base suite ran: 4,041 passed, 3 failed, 87 errors. All failures/errors point to existing
  Biotechnology Lecture 10 working-tree edits: malformed section/subsection content and a
  duplicate left slot in `set5_cancer.djot:503`. Those files were already modified at session
  start and were not changed here. This is not a clean full-suite result.
- No attended Impress click playback, classroom/Zoom test, or independent scientific fact-check
  was performed. Original animation/reveal limitations remain explicit replacement reasons.
- Local extracted images, import reports, and ODP/PDF are ignored by Git. They remain available
  in this checkout; a source-only Git handoff does not include all teaching media.

## Remaining audit findings

Typography audit: 3 runts, 6 wrapped titles, 1 long-URL warning. The long FDA URL
on marked B45 remains complete and clickable but exceeds its text region at 12 pt.
The marker retains this unresolved fit; no shortened address was substituted.
Skipped typography coverage: 18 hidden slides, 11 special-layout titles, 2 math/explicit-break
paragraphs, and 1 final-paragraph runt exemption.

| Deck | Djot slide | Typography finding |
| --- | --- | --- |
| lect11a-2026_announcements | 11 | runt |
| lect11b-polyploidy | 21 | title-wrap |
| lect11b-polyploidy | 22 | title-wrap |
| lect11b-polyploidy | 45 | url-too-wide |
| lect11b-polyploidy | 45 | runt |
| lect11c-sex_dosage | 6 | title-wrap |
| lect11c-sex_dosage | 45 | title-wrap |
| lect11c-sex_dosage | 64 | title-wrap |
| lect11d-chromo_alter_1-deletions | 9 | title-wrap |
| lect11e-chromo_alter_2-duplications | 20 | runt |

All capacity diagnostics follow; rows retain the source slot and measured size rather than
suggesting unapproved prose changes or slide splits. Mixed-readability rows retain explicit
replacement markers. Small source/reference text can remain below the advisory 20 pt floor.

| Deck | Djot slide | Slot | Concern | Required pt |
| --- | --- | --- | --- | --- |
| lect11a-2026_announcements | 5 | caption | paragraph/list | 15.25 |
| lect11a-2026_announcements | 44 | left | paragraph/list | 19.75 |
| lect11a-2026_announcements | 44 | bottom-right | paragraph/list | 18.5 |
| lect11a-2026_announcements | 45 | body | paragraph/list | 19.75 |
| lect11b-polyploidy | 10 | body | mixed-readability | 20.0 |
| lect11b-polyploidy | 12 | right | paragraph/list | 17.0 |
| lect11b-polyploidy | 25 | body | mixed-readability | 12.0 |
| lect11b-polyploidy | 32 | body | mixed-readability | 15.0 |
| lect11b-polyploidy | 33 | body | mixed-readability | 20.0 |
| lect11b-polyploidy | 34 | body | mixed-readability | 20.0 |
| lect11b-polyploidy | 35 | body | mixed-readability | 14.5 |
| lect11b-polyploidy | 36 | body | mixed-readability | 12.5 |
| lect11b-polyploidy | 38 | body | mixed-readability | 12.0 |
| lect11b-polyploidy | 40 | body | mixed-readability | 16.0 |
| lect11b-polyploidy | 43 | body | paragraph/list | 18.5 |
| lect11b-polyploidy | 45 | body | mixed-readability | 9.5 |
| lect11c-sex_dosage | 6 | body | mixed-readability | 20.0 |
| lect11c-sex_dosage | 7 | left | paragraph/list | 15.5 |
| lect11c-sex_dosage | 12 | left | paragraph/list | 17.0 |
| lect11c-sex_dosage | 18 | body | mixed-readability | 15.5 |
| lect11c-sex_dosage | 29 | body | mixed-readability | 15.0 |
| lect11c-sex_dosage | 34 | right | paragraph/list | 14.75 |
| lect11c-sex_dosage | 36 | right | paragraph/list | 15.5 |
| lect11c-sex_dosage | 39 | body | paragraph/list | 18.0 |
| lect11c-sex_dosage | 46 | right | paragraph/list | 18.0 |
| lect11c-sex_dosage | 47 | body | paragraph/list | 7.25 |
| lect11c-sex_dosage | 48 | left | paragraph/list | 14.0 |
| lect11c-sex_dosage | 48 | right | mixed-readability | 20.0 |
| lect11c-sex_dosage | 51 | body | paragraph/list | 18.5 |
| lect11c-sex_dosage | 52 | body | paragraph/list | 17.25 |
| lect11c-sex_dosage | 56 | body | paragraph/list | 16.25 |
| lect11c-sex_dosage | 57 | body | paragraph/list | 18.5 |
| lect11c-sex_dosage | 58 | body | paragraph/list | 17.25 |
| lect11c-sex_dosage | 59 | body | paragraph/list | 18.5 |
| lect11c-sex_dosage | 60 | body | paragraph/list | 17.25 |
| lect11c-sex_dosage | 62 | body | paragraph/list | 17.25 |
| lect11d-chromo_alter_1-deletions | 15 | body | mixed-readability | 20.0 |
| lect11d-chromo_alter_1-deletions | 33 | body | mixed-readability | 20.0 |
| lect11d-chromo_alter_1-deletions | 35 | body | mixed-readability | 20.0 |
| lect11d-chromo_alter_1-deletions | 36 | body | mixed-readability | 20.0 |
| lect11d-chromo_alter_1-deletions | 37 | body | mixed-readability | 20.0 |
| lect11d-chromo_alter_1-deletions | 38 | body | mixed-readability | 20.0 |
| lect11d-chromo_alter_1-deletions | 39 | body | mixed-readability | 20.0 |
| lect11d-chromo_alter_1-deletions | 40 | body | mixed-readability | 20.0 |
| lect11d-chromo_alter_1-deletions | 41 | body | mixed-readability | 20.0 |
| lect11d-chromo_alter_1-deletions | 42 | body | mixed-readability | 20.0 |
| lect11d-chromo_alter_1-deletions | 67 | body | paragraph/list | 18.5 |
| lect11d-chromo_alter_1-deletions | 92 | body | paragraph/list | 18.5 |
| lect11d-chromo_alter_1-deletions | 93 | body | paragraph/list | 10.25 |
| lect11d-chromo_alter_1-deletions | 94 | body | paragraph/list | 17.0 |
| lect11d-chromo_alter_1-deletions | 95 | body | paragraph/list | 9.75 |
| lect11d-chromo_alter_1-deletions | 101 | body | mixed-readability | 20.0 |
| lect11d-chromo_alter_1-deletions | 110 | body | mixed-readability | 20.0 |
| lect11e-chromo_alter_2-duplications | 16 | body | mixed-readability | 20.0 |
| lect11e-chromo_alter_2-duplications | 20 | left | paragraph/list | 19.0 |
| lect11e-chromo_alter_2-duplications | 22 | body | mixed-readability | 20.0 |
| lect11e-chromo_alter_2-duplications | 27 | left | paragraph/list | 19.0 |
| lect11e-chromo_alter_2-duplications | 28 | top-left | paragraph/list | 14.5 |
| lect11e-chromo_alter_2-duplications | 33 | left | paragraph/list | 19.75 |
| lect11e-chromo_alter_2-duplications | 35 | left | paragraph/list | 18.0 |

The global whitespace/conflict check also reports pre-existing conflict markers in the same
Biotechnology Lecture 10 edits. The changed announcement guidance and new LECT11 sources
are checked separately; those unrelated conflicts were preserved.

## Conversion checklist

The checklist below is copied from the repository conversion guide. Checked items mean the
check was performed; unresolved outcomes are recorded above. N/A and unperformed items are
annotated rather than implied successful.

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

Use [ANNOUNCEMENT_DECK_GUIDE.md](../../../docs/ANNOUNCEMENT_DECK_GUIDE.md) for the announcement order,
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
- [x] Confirm the latest published regular StVC episode available on the lecture date, excluding
  specials, and use it as the default. Record its number; if another episode is more appropriate,
  select it and document why.
- [x] Verify the saved StVC episode number/title, video URL, thumbnail, and playable game/tool
  URL all refer to the selected episode. Open both links and inspect the downloaded image.
- [x] Inspect the rendered StVC slide: confirm three caption lines, visible clickable video
  and game/tool URLs, and placement immediately after the YouTube channel slide.
- [x] Check the YouTube channel, anonymous-message, Discord, and applicable Zoom slides.
  Verify their images/QR codes and visible clickable URLs; keep private course URLs in
  `course_links.local.yaml` through `{{course_url:key}}` references.

### Repair individual slides

- [x] Compare every source slide with its rendered conversion, including slides without importer
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
- [x] Existing wrapped titles retained and audited; no unapproved rewrites. Inspect every rendered title for single-line fit, following the preference in
  [HUMAN_GUIDANCE.md](../../../docs/HUMAN_GUIDANCE.md). Flag wrapping titles and record proposed shorter
  wording for review; permission to rewrite titles remains separate from checking their length.
- [x] For textbook diagrams assembled from artwork and positioned labels, compare label placement,
  arrows, and diagram relationships with the source. Record whether a labeled image reconstruction
  is a suitable repair; retain the replacement marker until the rendered result is verified.
- [ ] N/A: no new labeled-image reconstruction attempted. Where suitable, use one quality-90 WebP inside SVG with live overlapping labels. Keep titles,
  captions, surrounding prose, and native tables outside the asset. Verify the LibreOffice render
  and review any source reveals separately; a static figure does not certify animation fidelity.
- [x] Preserve source vector figures as vectors with live labels. Restore static diagram highlights
  and masks within their figure, and preserve paint order so hidden answers do not reappear above
  opaque masks. Verify both masked and unmasked regions against the source.
- [x] Check each figure's identity against the source render, including orientation and cropping;
  a plausible diagram or matching subject is insufficient evidence that it is the right asset.
- [ ] N/A: no new native mask conversion attempted. Distinguish static masks from actual reveal targets using the source ODP. Use an image-relative
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
- [ ] Playback unperformed; affected slides retain markers. Compare source animation targets/order with the converted reveals. Inspect final PDF states
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
  [the visual review rubric](../../../docs/SLIDE_VISUAL_REVIEW_RUBRIC.md) as assessment guidance. Inspect dense
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

