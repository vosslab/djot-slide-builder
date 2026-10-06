# Genetics Lecture 06 conversion

Lecture date: October 6, 2026. Five canonical Djot decks preserve the lecture split.
The four science decks retain one output slide per original source slide, in source order.
Original ODP/PDF files remain reference inputs.

Formatting follow-up (October 6): compare source styles with the canonical text, including LLM
rewrites. Restore C10's underlined chromomeres; D39/D40's bold, underlined no consensus; D52's
italic parental phenotypes; E12's italic sex-lethal/Sxl; and D4/E27's colored all-caps exceptions.
Retain existing layouts and replacement markers. Rebuild C/D/E and inspect representative PDF
pages. This targeted pass is not a complete formatting audit of the lecture.

| Deck | Slides | Replacement markers |
| --- | ---: | ---: |
| [lect06a-2026_announcements.djot](lect06a-2026_announcements.djot) | 36 | 0 |
| [lect06b-intro_cells.djot](lect06b-intro_cells.djot) | 24 | 0 |
| [lect06c-meiosis.djot](lect06c-meiosis.djot) | 53 | 4 |
| [lect06d-x_linked_genes_1.djot](lect06d-x_linked_genes_1.djot) | 62 | 6 |
| [lect06e-x_linked_genes_2.djot](lect06e-x_linked_genes_2.djot) | 28 | 12 |

## Current announcements

- Quiz 2 and assignments 4-5: October 6. Assignment 6: October 13.
- Midterm: October 13, in person during class, Chapters 1-4.
- Restore the Exam divider, exam rules, paper-aid guidance, quiz-review instructions, and
  midterm assignment preparation. All six pages (21-26) are visible in ODP and PDF.
- Use the current ZipGrade bubble-form policy and 1:30-4:25 p.m. class meeting.
- Preserve exam-specific paper-aid and short-answer guidance from the legacy lecture.
- Omit the old unverified claim that assignments have reopened and the obsolete October 15
  blanket deadline. Blackboard remains authoritative for availability and submission times.
- Reuse the editable Lecture 05 announcement content and copy its referenced images locally;
  restore the exam section from the original 2025 Lecture 06 announcements.
- The Fall 2026 local syllabus schedule, course details, syllabus.yml, and shared face-to-face
  exam policy supply dates, coverage, points, meeting time, and ZipGrade instructions.

## Replacement workflow

22 science slides retain `@replaceme`, reduced from 64. These are explicitly incomplete conversions, not
classroom-ready reconstructions. The large warning remains visible in both export formats.
Speaker notes identify the original deck, slide number, and reason. Original component images
remain separate assets; unsupported diagrams are never replaced with whole-slide screenshots.

- Rebuild diagram labels, arrows, color associations, covered/revealed regions, and spatial
  relationships from the original source before removing the marker.
- Dense diagrams use a focal component image and a short reconstruction caption. Imported
  labels and other reconstruction evidence remain in notes and the original ODP.
- Resolve simple title/end layouts and multiple-choice question/answer blocks with native layouts.
- Preserve allele superscripts and powers where the importer flattened them.
- Lecture 06D slides 58-60 cannot pass the importer as originally composed: nine components
  including a table have no exact native grid. A temporary import-only ODP retains their question
  frames. Each final slide is marked, with original source text in its notes. The original ODP
  supplies the authoritative table and reveal geometry.
- Lecture 06D import_report.json names that staging ODP. Its report describes the staged import;
  it is not proof that slides 58-60 preserve the original composition.
- Other import reports describe the initial imports, before native layout repairs. Final markers
  and notes in the Djot sources govern replacement status.

## Validation and outputs

### SVG and typography repairs

- B: slides 7, 9-11, 13-15, 20-22.
- C: slides 4, 7, 13, 16-20, 23-24, 27, 31, 33-35, 40-41, 44, 47.
- D: slides 11-12, 17, 19-22, 24, 33, 38.
- E: slides 13-14, 17.

These 42 repairs use original component artwork with SVG labels/leaders or native text/table
reconstruction. B10-11 use two SVGs and two native captions. C33 retains one larger SVG because
its shared stage labels explain both chromosome arrangements. Source PDF coordinates corroborate
the original ODP composition; transparent artwork retains its masks. These are not page screenshots.
Definition terms on C8 and other definition slides have bold/underline emphasis and selective color.
See [SVG_DIAGRAMS.md](../../../docs/SVG_DIAGRAMS.md) for the authoring contract.

Remaining markers identify the following explicit follow-up work:

| Deck | Slides | Outstanding review |
| --- | --- | --- |
| C | 14, 37, 48, 52 | Composite explanations, semantic color, or distributed diagram labels |
| D | 50, 56-60 | Inheritance problem composition, source tables, and staged answer relationships |
| E | 4-5, 9-11, 15-16, 21-25 | Staged examples, chromosome-set relationships, labels, and dense source composition |

Markers remain the authority for unfinished slides. Original import reports are historical and
do not describe the repaired final assets. Historical replacement reasons remain in source notes,
followed by the SVG repair record where applicable.

### Verification results

- 143 focused parser, importer, layout, ODP, and SVG/definition contract tests pass.
- New module Pyflakes checks and `git diff --check` pass.
- The repository suite, with automatic cleanup disabled, reports 2328 passed and 44 failures.
  Failures concern existing legacy-text ASCII/whitespace, font-license whitespace, an existing
  ODP-reader test's typing/security checks, a Lecture 04 development script, and the already
  oversized design/style documents. This is not a clean repository-wide test run.
- Final package/PDF checks verify all 203 pages, 22 warning pages, source order/provenance,
  current announcements, and visible exam pages 21-26. Rendered repairs were visually reviewed.
- All 46 referenced SVG assets match their packaged ODP bytes; checkpoint labels and native
  captions remain extractable PDF text. The SVG receipt is in
  `output/lect06_svg_review/svg_acceptance.json`. All 81 documentation link checks pass.
- Metafile follow-up: D13, D56, and D57 now use original SVM-to-SVG figures, including live text.
  The genotype table contains 56 text elements and 34 vector paths with no bitmap images. Actual
  PDF review verified the correction for spurious Latin RTL flags. The 22 markers remain unchanged.
  The focused metafile/import/export suite passes 48 tests; see
  [metafile_vector_followup.md](../../../docs/active_plans/metafile_vector_followup.md).
- Interactive slide-show playback was not tested; these repairs target static compositions.

Strict native Jotdown lint and semantic lint pass for 5 sources, 203 slides, and 115 visible-content
image references. Capacity inspection reports no concerns. All science slides retain source
numbers in notes; all authored slides are visible.

Build with `./build_slides.sh genetics/LECT06/`. Editable decks are in `output/odp/` and
classroom PDFs in `output/pdf/`. Review contact sheets and the generated acceptance receipt are
in `output/genetics_lect06_review/`. The review covers source/output page counts, warning presence,
exam visibility, current announcement text, and rendered page inspection. Interactive click
playback has not been tested; native multiple-choice answer reveals are retained.
