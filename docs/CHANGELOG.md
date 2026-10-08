## 2026-10-08

### Additions and New Features

- Convert Biotechnology Lecture 06 to four native Djot decks with local assets, editable ODP,
  and PDF output: announcements, individual project, Talking Points Set 4, and business plans.
- Modernize the 41-slide business-plan deck using all 31 sample executive summaries from
  2015-2021. Add concrete mechanism, evidence, customer, competition, cost, and milestone guidance.
  Record sample evidence and source coverage in the
  [Lecture 06 review](../biotech/LECT06/djot/LECT06_REVIEW.md).

### Fixes and Maintenance

- Refresh October 8 announcements and project guidance against the local Fall 2026 syllabus.
  Retain archived slides, the submission format, and the original rubric.
- Restore pyruvate and photosynthesis labels in self-contained SVGs, repair image comparisons,
  and preserve six native question/answer reveals. Correct bounded scientific claims with sources.
- Repair clipped answer text, captions, and the video heading found during PDF inspection.
- Rotate September 29-30 history into `CHANGELOG-2026-09d.md`, retaining the two newest dates.

### Decisions and Failures

- Keep 12 science review markers and the hidden talking-marks placeholder for instructor review.
  Separate historical examples and sample proposals from verified current facts.

### Developer Tests and Notes

- Strict native Djot lint passes for 256 slides and 111 image references; capacity reports no
  concerns. Build four ODP/PDF pairs and inspect all 218 visible pages plus enlarged repair checks.
- This content conversion does not change the slide engine or claim a fresh full-suite pass.
- Native artifact counts, hidden flags, notes, six reveal objects, and two SVG payloads pass.
  Markdown-link checks report 80 passes and four failures in pre-existing documentation links
  to older untracked files; all newly added Lecture 06 links pass.

## 2026-10-06

### Additions and New Features

- Import original GDI metafiles as SVG instead of preferring raster previews. Retain glyph text,
  table rules, and fills; surface conversion failures or absent live text for review.
- Replace Lecture 06D slides 13, 56, and 57 raster figure references with vector SVG exports.
  Preserve existing layouts and unresolved replacement markers.

- Add direct self-contained SVG sizing and ODP embedding, plus `image-comparison` with two
  diagrams above measured native captions. Document authoring in [SVG_DIAGRAMS.md](SVG_DIAGRAMS.md).
- Preserve definition-term bold and underline through import and export, with optional color.
- Repair 42 Lecture 06 replacement slides using original artwork, positioned labels, native
  captions, and editable tables. Retain 22 unresolved markers and the visible exam section.

- Convert Genetics Lecture 06 into five custom Djot decks with local component assets and
  source-slide notes. Preserve all 167 science slides in their original order.
- Restore visible midterm exam guidance; update announcements for October 6, assignments 4-5,
  Quiz 2, and the October 13 in-person exam covering Chapters 1-4.

### Fixes and Maintenance

- Preserve inherited frame/paragraph/span formatting, italic runs, explicit normal/none and color
  resets, and uppercase/lowercase source transformations. Retain otherwise unsupported source RGB
  colors in validated inline Djot spans, with existing review warnings instead of discarded hues.
- Restore confirmed emphasis losses in Lecture 06C, D, and E, including chromomeres, no consensus,
  parental phenotypes, sex-lethal/Sxl, and all-caps exceptions. Require LLM review to check formatting
  as well as wording. A focused import-to-native-export test covers combined styles and resets.

- Record reviewed `@replaceme` markers as acceptable conversion outcomes. Acceptance does not
  require eliminating every marker or forcing a reconstruction that loses teaching intent.

- Clarify that deterministic ODP import produces a draft requiring LLM evaluation against source
  slides and animation evidence before acceptance. Keep canonical Djot builds deterministic;
  document that the import CLI does not yet enforce this workflow automatically.

- Preserve source on-click text appearances through import planning. Recognize a question with
  one revealed answer using the existing multiple-choice layout; flag unsupported animation
  actions, targets, timing, and unmapped text reveals for review with `@replaceme`.
- Restore Lecture 06D slide 36's answer popup. Allow a single standalone question in the existing
  layout and measure answers in bold. Split slide 36's answer into two native paragraphs for fit.

- Correct observed LibreOffice SVG direction flags on Latin-only figures and remove its exact
  unused SVG DTD declaration before validation. Actual PDF inspection verified the genotype table.

- Use current ZipGrade wording and meeting time. Remove the obsolete blanket assignment deadline
  and unverified reopening claim. Recover native question/answer layouts and allele superscripts.
- Mark 64 slides needing diagram, relationship, color, or composition reconstruction with
  `@replaceme`; retain their source references and reconstruction evidence.

### Decisions and Failures

- LibreOffice image import requires desktop process access. Original 06D slides 58-60 exceed the
  native table-grid import contract; import question frames from a temporary copy and retain
  explicit replacement markers. Leave original presentations unchanged.

### Developer Tests and Notes

- Metafile vector work: 48 focused tests pass; live SVM conversion/import, strict Djot lint,
  byte-exact SVG packaging, and rendered PDF checks pass. EMF/WMF live acceptance remains untested.

- Track image-area regression using Lecture 06D slide 9: image coverage fell from 47.19% to
  12.13% of the slide. Add a non-blocking import audit and `image-audit` command after scope
  clarification; leave layouts and trimming unchanged. See
  [image_area_regression_followup.md](active_plans/image_area_regression_followup.md).
- Track vector-preserving GDI conversion and the current preference for raster previews in
  [metafile_vector_followup.md](active_plans/metafile_vector_followup.md).

- SVG/definition work: 143 focused tests pass; direct SVG payloads, aspect ratios, native caption
  geometry, and inherited/reset emphasis are covered. Full repository checks with cleanup disabled
  report 2328 passes and 44 existing hygiene failures; see the Lecture 06 review for categories.

- Strict Jotdown/semantic lint passes for five decks, 203 slides, and 115 image references.
  Capacity inspection reports no concerns. Build editable ODP and PDF, inspect contact sheets,
  and verify page counts, replacement warnings, source order, and visible exam guidance.
  All 80 Markdown-link checks pass.
