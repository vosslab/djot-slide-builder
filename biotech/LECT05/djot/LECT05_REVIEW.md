# Biotechnology Lecture 05 conversion

Lecture 05 uses three canonical Djot sources. Announcements and project guidance build on the
editable Lecture 04 material; the legacy Lecture 05 decks supply the Theranos teaching sequence
and the project slides to restore. The current lecture date is Oct 1, 2026.

| Deck | Djot source | Authored | Hidden | Classroom PDF |
| --- | --- | ---: | ---: | ---: |
| Announcements | [lect05a-2026_biotech_announcements.djot](lect05a-2026_biotech_announcements.djot) | 38 | 18 | 20 |
| Individual project | [lect05b-individual_project.djot](lect05b-individual_project.djot) | 52 | 20 | 32 |
| Theranos | [lect05c-theranos.djot](lect05c-theranos.djot) | 37 | 1 | 36 |
| **Total** | | **127** | **39** | **88** |

## Source and visibility choices

- Use the native Lecture 04 sources for stable announcements, project guidance, and local images.
- Use the copied 2026 files and the prior Lecture 05 visibility as evidence of the instructor's
  teaching sequence. The copied Set #3 protein decks remain reference inputs in the lecture root.
- Hide Discord signup and Student Profile, both completed Sept 21. The archived slides explicitly
  say the assignments are complete. Keep Discord in the current contact and homework-help slides.
- Restore feedback, One Great Idea, executive-summary, AI, milestones, pitch, and video guidance
  from the archived project material. Keep historical schedules and previous assignments hidden.
- Use the current Fall 2026 course schedule for Oct 1 feedback, Oct 8 selection, Oct 22 executive
  summary and pitch, and Oct 29 follow-up. Blackboard supplies assignment-specific links and
  deadlines; the slides do not invent a new Homework 3 or Theranos-form deadline.
- Replace the old points screenshot with the published 88-point project breakdown. Rewrite the
  milestones-form screenshots as editable questions. No student grade screenshot is included.
- Mark the hidden talking-marks image placeholder with `@replaceme`. Its editable ODP page has
  a large red warning until the instructor replaces and reviews that image.
- Import the Theranos portraits and resource images as components, with native text around them.
  The original 31-slide import evidence remains in
  [import_report.json](assets/lect05c-theranos/import_report.json); its counts describe the import,
  before timeline splitting, objectives, discussion, summary, and the film-slide visibility edit.
- Vary image/text sides in the announcement panels and alternate the three Veridian project
  examples if restored. The twelve consecutive Theranos character slides already alternate.
- The distinct announcement filename preserves the Genetics Lecture 05 output in the shared
  generated-output folder. No original lecture ODP/PDF is overwritten.

## Calendar and factual sources

Current project dates and points come from the published
[Fall 2026 schedule](https://vosslab.github.io/syllabus/fall_2026/biotech/SCHEDULE/) and
[project requirements](https://vosslab.github.io/syllabus/fall_2026/biotech/PROJECTS/), checked
against the local syllabus sources during conversion.

The historical Holmes and Balwani sentencing wording follows the
[Department of Justice case record](https://www.justice.gov/usao-ndca/us-v-elizabeth-holmes-et-al).
These are dated sentencing events, not claims about current release dates. The assay slide uses
the [FDA clearance record](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K143236)
for the specific HSV-1 test. The television slide uses
[Hulu's series page](https://press.hulu.com/shows/the-dropout/) and describes the 2022 series in
the past tense. The legacy film-development announcement remains hidden.

## Validation and visual review

Strict native Jotdown validation and repository semantic lint pass for all three sources, 127
slides, and 46 image references. Capacity inspection reports no concerns, including hidden slides.
The public folder build writes three editable ODPs and three ODP-derived PDFs.

Every ODP has the authored page count and exactly matches the source's hidden flags in order.
PDF page counts match the visible-slide counts. PDF text checks confirm that completed assignment
slides and instructor-only archive notes are absent; Discord remains a contact channel.

All 88 classroom pages were rendered for visual inspection. Review fixes include readable project
dates on the red section surfaces, editable project tables and form questions, split Theranos
timelines, and a full-width trial-podcast URL. The eight initial import-review flags are resolved
through native poll color emphasis, timeline splits, portrait/resource panel review, and a native
THE END closer. Image panels retain the source's component images and proportions.

The image-side variation pass rebuilds the decks and visually checks the three changed pages.
All 127 slides retain their content, notes, and visibility. Consecutive two-panel image/text
slides alternate in both the authored sequence and the visible classroom sequence.

Generated files are under `output/odp/` and `output/pdf/`. Contact sheets, page renders, source
inventory, and the visibility receipt are under `output/biotech_lect05_review/`. These are local
review artifacts. Rebuild with `./build_slides.sh biotech/LECT05/`.

To show or hide a slide, change its `hidden: true` line immediately after `=== layout:`. Hidden
slides remain editable in ODP and are omitted from the classroom PDF. See
[DJOT_SLIDE_SYNTAX.md](../../../docs/DJOT_SLIDE_SYNTAX.md#hidden-slides).
