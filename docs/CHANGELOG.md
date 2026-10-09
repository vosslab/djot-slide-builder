## 2026-10-08

### Additions and New Features

- Expand the business-plan lecture from 41 to 57 slides with 23 PDF crops from 13 submissions:
  logos, paragraphs, a pathway, milestones, and document-design comparisons. Retain all eight
  native tables and the instructor's question-led voice. Split D into six included section files.
  Record source pages, crop coordinates, and hashes in the asset manifest and sample review.
- Add ordered Djot chapter includes with theme inheritance, source-local diagnostics, local path
  validation, circular-include detection, and master-only folder discovery. Native lint validates
  each included file. Document the [include contract](DJOT_SLIDE_SYNTAX.md#chapter-files-and-includes).
- Expand Biotechnology Talking Points Set 4 from 125 to 248 slides using the annual 2021-2026
  material and exact 2026 numbering. Split the lecture into Chapters 12-16 plus opening and summary
  files, controlled by the existing master filename. Add a topic/source guide for all 33 topics.
  Retain all 121 original source-slide records, all 90 image references, and the instructor's
  question-led style. Complete Set 4 before the requested business-plan visual revision.

- Convert Biotechnology Lecture 06 to four native Djot decks with local assets, editable ODP,
  and PDF output: announcements, individual project, Talking Points Set 4, and business plans.
- Modernize the 41-slide business-plan deck using all 31 sample executive summaries from
  2015-2021. Add concrete mechanism, evidence, customer, competition, cost, and milestone guidance.
  Record sample evidence and source coverage in the
  [Lecture 06 review](../biotech/LECT06/djot/LECT06_REVIEW.md).

### Fixes and Maintenance

- Emphasize all 36 dates on the six Lecture 05C Theranos timeline slides with bold, underlined
  text, matching genetics definition terms while retaining event wording and slide order.

- Combine Biotechnology Lecture 04 Talking Points Set 3 through one include master in chapter
  order. Remove three intermediate closers, keeping one final THE END and six hidden answers.
  Folder builds now select one combined talking-points deck plus announcements and project decks.

- Give all 33 Biotechnology Lecture 06C topics numbered subsection dividers. Retain five major
  chapter dividers at boundaries verified in the 2026 source deck under `old/`; convert 12 internal
  legacy sections to ordinary content slides. Preserve source notes and figures, and update the
  topic guide and review page references for the 281-slide deck.

- Resolve nine factual Set 4 review markers using primary sources. Correct LibertyLink/Clearfield
  examples and the bee study's experimental doses and sample denominators; date the mosquito
  research, salmon business history, and cattle review records. Replace factual placeholders with
  worked comparisons and native tables. Retain all 248 slides, 121 source IDs, and 90 image references.
- Correct the Set 4 guide's stale business-plan status and record the final source checks and
  remaining instructor judgments in the Lecture 06 review.
- Place the 16S profiling figures under topic 2, distinguish OTUs from ASVs, and place minimal
  genomes and synthetic chloroplasts under their 2026 topics. Keep Brainbow in Chapter 15 as
  the 2026 deck does. Repair a narrow fermentation-table label found in rendered review.

- Refresh October 8 announcements and project guidance against the local Fall 2026 syllabus.
  Retain archived slides, the submission format, and the original rubric.
- Restore pyruvate and photosynthesis labels in self-contained SVGs, repair image comparisons,
  and preserve six native question/answer reveals. Correct bounded scientific claims with sources.
- Repair clipped answer text, captions, and the video heading found during PDF inspection.
- Rotate September 29-30 history into `CHANGELOG-2026-09d.md`, retaining the two newest dates.

### Decisions and Failures

- After factual follow-through, keep three science review markers (two instructor opinions and
  one source graphic) and the hidden talking-marks placeholder for instructor review. Separate
  historical examples and sample proposals from verified current facts.

### Developer Tests and Notes

- Theranos timeline emphasis: strict native lint passes (37 slides, 25 images); ODP/PDF builds
  succeed. Inspect Poppler renders of all six timeline slides for emphasis, wrapping, and clipping.

- Lecture 04 combined Set 3: native folder lint selects three masters (457 slides, 709 images).
  The single talking-points ODP builds with 389 slides; verify exact chapter concatenation, six
  hidden answers, one final closer, and unchanged content apart from three removed closers.
  All 89 Markdown-link checks and `git diff --check` pass.

- Lecture 06C divider cleanup: strict native lint passes (281 slides, 90 images); ODP/PDF builds
  and artifact counts pass. Source comparison retains all 248 prior slides in order. Visually
  check all 50 added or affected divider/content pages; all 89 Markdown-link tests pass.
  LibreOffice's sandboxed PDF export exits -6; the permitted build outside the sandbox succeeds.

- Business-plan visual revision: strict folder lint passes for four masters, 395 slides, and
  141 image references. D capacity and ODP/PDF builds pass; rendered review checks all 57 pages
  and corrects caption overflow and crop boundaries. Verify 57 notes pages, eight native tables,
  preserved prior teaching coverage, and unchanged A/B/C sources and source PDFs.
  Markdown-link checks pass all 89 cases; `git diff --check` passes.
- Chapter assembly has 101 passing focused parser/lint/export/terminal tests. A semantic
  before/after comparison confirms that splitting preserves content, notes, order, and assets.
- Expanded Lecture 06 folder lint passes: four master decks, 379 slides, 111 image references.
  Set 4 capacity and ODP/PDF build pass. Inspect the expanded sequence and final changed pages;
  verify 248 ODP/PDF pages, 235 notes pages, seven answer reveals, 16 native tables, and two SVGs.
- A fresh full suite reports 2,554 passed and 18 pre-existing failures in source-text encoding,
  older test hygiene, developer-script hygiene, and documentation format/size. Reproduce and undo
  only the suite's 22 unrelated automatic formatting changes; retain a local evidence copy.
  No full-suite pass is claimed. The earlier conversion-only results below remain historical.

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
