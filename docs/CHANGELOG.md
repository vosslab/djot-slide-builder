## 2026-10-26

### Additions and New Features

- Document mixed text/image sequences as one-panel compositions, using LECT07B slide 24 as
  the reference. Prefer the existing vertical-flow import path before caption-based panel
  grouping; preserve comparative and spatial layouts plus unrelated replacement reasons.
- Check mixed-flow import readability before publishing and add `@replaceme` with a split
  recommendation to generated source/import reports when bounds cannot be met.
- Convert Genetics LECT08B-F to native Djot with source assets and import provenance;
  retain all 210 content slides, their sequence, and the hidden LECT08C slide.
- Reuse the canonical 2026 announcements for LECT08A, updating lecture metadata and
  date-relative assessment/homework colors from the instructor's schedule spreadsheet.
  Preserve announcement prose, including the previous agenda and podcast selection.

### Fixes and Maintenance

- Update HUMAN_GUIDANCE conversion policy to preserve approximately 98% of existing prose,
  permit minor grammar/clarity improvements, and require managers to add missing objectives
  and summaries from lecture content using the pedagogical slide style guide. Replace the
  conflicting prohibition on instructional additions with source-grounded positive guidance.
- Optimize shared mixed text/image panels by occupied bounding-box area at half-point font
  precision, with independent aspect-preserving image sizes and theme-derived reduction bounds.
  Mark unreadable arrangements as replacement previews and recommend splitting through build
  diagnostics and speaker notes; preserve authored sources and existing layouts.
- Use existing title, panel, section, and closing layouts without rewriting teaching prose.
  Reconstruct eight incremental chi-square tables as editable native tables, preserve their
  source values and blanks, and restore three source answer reveals and allele superscripts.
- Compare original and generated content-deck PDF pages; retain explicit replacement markers
  for unresolved diagram geometry, table overlays, source masks, and animations. Record
  slide-specific findings in genetics/LECT08/djot/LECT08_REVIEW.md.

### Developer Tests and Notes

- Pass 1,299 repository tests after the mixed-flow converter change. Re-plan original LECT07B-D
  evidence and render five import examples: B24/B34/C12/C27 now use one panel without clearing
  unrelated review reasons. Check a six-image mixed panel (192 candidate vertices per font).
- Pass all 1,273 repository tests and 400 temporary exhaustive allocation comparisons; render
  seven ODP/PDF specimens including LECT07B slides 24/25, starvation, tall, and multi-image cases.
  Warm slide-25 compilation measures about 13 ms versus 2 ms for the previous rule. Test scope
  is `pytest tests`; unrestricted discovery also enters unrelated OTHER_REPOS projects.
- Plan shared mixed-content scaling with independent image sizes, half-point font
  candidates, measured area comparisons, and an explicit readability-policy investigation
  in docs/active_plans/active/mixed_content_scaling.md; no compiler behavior changed.
- Specify replacement marking with a recommendation to split when mixed-content readability
  constraints cannot be met, following instructor guidance.
- Run strict native Djot lint and the six HG cover checks; export editable ODP and
  LibreOffice-derived PDF outside the sandbox. Preserve original ODP/PDF inputs.
- Restore missing local MathJax dependencies with the existing lockfile; use a writable npm
  cache after the default cache rejects writes. No dependency manifest or compiler change.

## 2026-10-21

### Fixes and Maintenance

- Add one graduate-student regression tutorial reminder slide from the supplied
  Tutorial_Outline Markdown/PDF: four scenario/model-comparison bullets, an editable
  coffee-and-exam SVG, and the outline's spreadsheet URL as a single-line citation.

- Refine the eight tutorial SVGs with fried-chicken and broccoli hospital signs, small
  Baby Butter Ball trophies on Fried Foods 1-2, and a shared bacterial jar emblem.
  Preserve all statistical marks and labels. Validate SVG XML/IDs, native slide lint,
  and the rebuilt ODP/PDF; visually inspect all eight illustrations at slide size.

- Label the StVC caption links `Watch the Video:` and `Play the Game:` across existing
  slides and the refresher, retaining the title and two links on three separate lines.

- Revise all StVC slides and the refresher to put a shorter title, video URL, and playable
  project URL on three lines inside the big-image caption box; reserve citations for one line.
  Use the full series name and episode number, retaining the episode subtitle but dropping
  the repeated YouTube SEO series suffix.

- Update all 12 StVC announcement slides with video and playable GitHub Pages links in
  `@citation`. Update the refresher to extract the project URL from the episode description
  and reject missing or ambiguous destinations instead of linking a repository. Trim the
  repeated series suffix from captions so episode titles fit above both links.

- Expand each tutorial recall slide to four short story and comparison cues, retaining
  guide links without adding discussion questions or calculation instructions.

- Simplify all eight tutorial overview slides to brief scenario and testing summaries with
  guide links; remove authored questions, numeric details, procedures, and result guidance.

- Tone down the outdoor icebreaker's colors to emphasize prompts; replace the instructor
  answer with cross country, hiking with his spouse, and looking at Fall leaves.

- Add preferred-palette color to the biostats outdoor icebreaker prompts and examples;
  record the general preference for more colorful icebreaker slides.

- Replace the four remaining stacked-panel YouTube channel slides in Biotechnology
  LECT04-LECT07 with the shared big-image format; resolve the outdated HG layout guidance.

- Color both current-week and next-week homework rows dark red, including their dates;
  update the durable homework color guidance accordingly.

- Update the biostats YouTube channel slide to `big-image` with a visible channel URL;
  remove the hidden playlist link and ad hoc URL color from the copied older layout.

- Remove the one-time biostatistics announcement request from human guidance; keep its
  implementation history in this changelog.

### Additions and New Features

- Add eight editable schematic SVG illustrations for the Fried Foods and Microbes tutorials,
  pairing the story imagery with each test comparison. Alternate image/text sides.
- Add layout-independent `@citation` for small condensed article references and clickable URLs
  in the bottom margin. Preserve normal layout space; use ordinary two-panel tutorial slides.
- Verify citation rendering and clickable links across all 19 layouts in ODP/PDF, plus
  parser/layout regression checks and visual review of the eight illustrated tutorial slides.

- Add a Tutorial Overviews section with eight source-based slides for Fried Foods 1-3
  and Microbes 1-5, including visible clickable Google Docs links. Read current guide exports;
  distinguish benchmark means, two-sample means, variances, and five-group ANOVA.

- Add Course Information and Group Project section-heading slides to Biostatistics Lecture 08A.

- Add an outdoor-activity icebreaker after the biostats agenda, with example answers,
  instructor examples, and Busse Woods as a local connection to the ANOVA discussion.
- Record the durable preference for concrete examples that help students start sharing.

- Add an undergraduate group-project introduction to Biostatistics Lecture 08A: tutorial
  purpose, team composition, shared contributions, proposal, peer testing, and final deadline.
  Use the course project scaffold for workflow and the current syllabus for dates.

- Add "In Two Weeks: Nov 4" to Biostatistics Lecture 08A after the next-week slide,
  covering the in-person meeting, Quiz 2, topics, assignments, and group formation.

- Create green-themed Biostatistics Lecture 08A announcements for October 21: shared HG
  contact slides, current podcast, syllabus links, variance comparisons/ANOVA agenda,
  tutorial deadlines, quiz dates, and graduate/group milestones.
- Use the instructor-updated biostats schedule source instead of the stale generated site;
  retain asynchronous weeks, target-release wording, and tutorial-specific cutoff instructions.
- Validate all 17 slides with strict native Djot lint and build editable ODP and classroom PDF.

## 2026-10-20

### Fixes and Maintenance

- Align strict lint with the existing ordered prose/list/image/table renderer. Accept supported
  content around a single table while preserving table shape and layout-specific restrictions.
  Fix LECT07D's line-132 lint rejection without changing lecture content or rendering geometry.
  Verify strict native lint for all 62 slides and 120 focused parser, lint, and layout tests.

### Additions and New Features

- Add an explicit YouTube slide generator using yt-dlp titles and thumbnails, ordinary
  `big-image` fragments, local PNG assets, and full visible clickable watch URLs.
- Restyle LECT07B's Numberphile video using its thumbnail and add Chi-squared Test before
  LECT07D's closing slide. Keep the Numberphile prompts and source provenance in notes.
- Verify generator/layout/include tests, both ODP/PDF builds, rendered video slides, and
  full-URL PDF hyperlinks. LECT07B retains 51 authored slides; LECT07D grows from 61 to 62.
  Initial strict lint passed for LECT07B and the new video fragment but exposed LECT07D's
  pre-existing prose/table rejection at line 132; the validation fix above resolves it.

- Complete six independent equation-pipeline audit passes. Reconcile stale math contracts
  in decision records, document module ownership, clarify the mixed-math diagnostic, and
  apply local comment/separator style. Leave proposed test changes for human review.

- Remove mixed prose/SVG equation flow and its token positioning, baseline, and wrapping
  code. Keep whole equation blocks, equation-only bullets/cells, and intact native prose
  paragraphs. Reject mixed authoring with a source location; revise LECT07C accordingly.
- Apply the permanent-test checklist to equation coverage: retain authoring/export
  contracts and remove fragment geometry and table-sizing assertions. Keep real-render
  verification as one-time evidence.

- Document equation-only list items with `\displaystyle` and the explicit distinction
  between native Djot scripts and LaTeX math. Remove a stale unsupported-math statement.

- Render standalone LaTeX equations with local MathJax and STIX2 outlined SVG.
  Share block sizing, table placement, and reveals with the slide compiler.
  Add locked Node dependencies and two offline layout/export tests.
- Migrate selected LECT07C binomial formulas and inline calculations to Djot math, retaining
  all 38 slides, original assets, and the existing slide 8 review marker. Verify native
  Djot parsing, 149 focused tests, and LibreOffice ODP/PDF rendering.

- Remove redundant `(continued)` from the two LECT07D slide titles to reduce wrapping.

- Repair LECT07C recovered equation spacing using font-independent vector outlines from
  the original PDF: 19 formula assets and two composite figures. Preserve original equation
  content; record source crops in `formula_sources.json` beside the assets.

- Start `icebreakers.yaml` with six prompts recovered from past announcements and the requested
  pets question. Add the pets Breakout Room Chat after the Genetics LECT07A agenda.

- Add lecture-date selection to the StVC refresher, excluding future publications and
  non-announcement course-introduction decks. Validate all thumbnails before source writes.
- Populate past Genetics/biotech announcements with their date-appropriate StVC episodes
  and remove unused agenda icebreaker entries.

- Audit 12 Genetics/biotech announcement sources against recent shared-slide guidance:
  anonymous-message layout, YouTube links/captions, grade colors, homework tables,
  and assessment date formatting/status colors. Preserve slide counts, order, hidden
  status. Reconcile 2026 Genetics assessment dates with the syllabus as authorized.
- Remove obsolete 2025 announcement source decks and generated outputs as requested;
  retain assets. Preserve course-specific output copies to avoid same-name export collisions.

- Restore preferred-palette blue/magenta emphasis to LECT07A Graded vs Total
  Percentage, matching the title, labels, and key distinction without rewriting text.

- Hide Reviewing Old Quiz Questions with the LECT07A Exam section until final-exam
  preparation is timely; retain it in the editable deck.

- Label homework table rows with zero-padded Week numbers while retaining the
  Assignment column heading.

- Rename LECT07A homework pages to Homework Due Dates and complete Part 2 deadlines
  through Assignment 13 using the published Fall 2026 Genetics syllabus.

- Match homework date-status colors to exam schedules: gray past due, red next week,
  black later. Apply to both cells of LECT07A homework rows.

- Reformat LECT07A homework as assignment/date tables with padded dates; retain hidden
  Part 1 and visible Part 2 slides and remove redundant deadline/schedule prose.

- Use the instructor-cleaned biotech LECT07 anonymous-message slide in Genetics LECT07A,
  preserving its text-left/image-right layout, wording, form URL, and image.

- Restore consecutive factorial rows 3-13 on LECT07B slide 13 (17.5 pt).
- Size standard slide titles independently of body density, preserving full-size short titles.

- Label build capacity warnings with authored slide numbers and titles.
- Improve LECT07B readability with a shorter representative factorial table and separate
  pea-pod setup/outcome panels. Split the later LECT07D hypothesis summary into critical-value
  and p-value slides with instructor approval, retaining its wording.

- Correct the numeric-table sign character class to remove the regular-expression
  FutureWarning while preserving signed-number alignment.

- Vertically center ordinary text on titleless one-panel slides while preserving
  horizontal alignment and standard body size. Leave mixed media layouts intact.

- Promote LECT07B slide 7's answer to the title, leaving the original explanation
  in the body to improve the use of space.

- Use preferred purple `#A719DB` consistently for LECT07D significance-level labels,
  replacing the overly dark imported purples.

- Reorder colors across all four LECT07D seven-step slides to increase hue separation
  between consecutive steps; retain matching colors for the step 4 and 5 references.

- Rework Genetics LECT07C against all 38 original pages: remove duplicated Punnett
  squares, restore lethal-TT crosses and missing equations, and give calculation groups
  dedicated panel space. Preserve source wording and sequence.
- Recognize extensionless SVM formula previews by their validated header in the existing
  ODP importer. Extend its conversion regression test to cover ObjectReplacements members.

- Split Genetics LECT07D original slides 3 and 4 into four slides: hypotheses and
  probability, calculation terms, critical-value decisions, and p-value decisions.
  Preserve the instructor's voice while applying approved scientific corrections to
  the p-value definition, non-rejection language, and decision comparisons.
  Apply the same approved terminology corrections to editable worked examples and
  repeated summaries throughout LECT07D.

- Convert the scanned Mendel quotation on Genetics LECT07D slide 50 to editable,
  condensed bullet points at the instructor's request; retain the original image and
  transcription in source assets and presenter notes.

- Document the instructor's full preferred hex palette locally and link it from human
  guidance, including the instructor-developed QTI color-wheel API for additional palettes
  and independence from LibreOffice's named colors.

- Apply the instructor's matching-set template palette to all four seven-step chi-square
  slides, with step references matching their action colors and wording preserved.

- Clear instructor-approved chi-square terminology and decision-slide flags, including
  repeated copies, and standardize all six null-hypothesis labels to editable H subscript 0.

- Record root `_temp/` as the canonical temporary directory and ignore its artifacts.

- Let titleless one-panel slides use the normal top content margin and a taller body;
  document omission of the root heading instead of adding another layout type.

- Review all 61 LECT07 replacement flags against original and rebuilt PDF pages; clear
  eight confirmed-complete slides. Restore the homework two-panel layout and missing
  original schedule sentence; restore crossed-out treatment of the incorrect B9 calculation.

- Switch Genetics LECT07A YouTube channel slide to big-image, preserving caption and URL.

- Right-align numeric table cells and distinguish total rows with bold text and a pale
  course-color fill in the shared native table renderer.

### Additions and New Features

- Keep public YouTube and other public course links in tracked sources; only private
  Discord and Zoom URLs use local configuration.
- Implement ignored local YAML course URLs with explicit Djot references, safe loading,
  validation, and focused tests. Populate existing Discord and Zoom URLs from slide sources;
  replace Blackboard link placeholders while retaining evergreen Discord slides and QR images.

- Add a universal Djot slide 1 pytest check across standalone decks and resolved includes.
  Accept omitted chapters, combined chapter/topic lines, and separate chapter lines.
  Require announcement topic exactly "Announcements" with no chapter.

- Add `refresh_podcast.py`: preview or explicitly refresh the latest published Stump the Vibe
  Coder episode across selected announcement decks. Save its thumbnail locally and insert or
  replace a `big-image` slide after the YouTube channel slide. Apply Episode 36 to Genetics 07A.
- Convert Genetics Lecture 07 into five canonical Djot decks: current announcements, probability
  review, two progeny-probability decks, and chi-square. Preserve original source evidence and
  hidden slides; add learning objectives and closing summaries.
- Update canonical 2026 announcements for October 20 using the instructor's schedule spreadsheet.
  Record Quiz 3 and Assignments 7-8 on November 3; hide completed midterm-preparation slides.

### Fixes and Maintenance

- Clarify the standardization boundary in HG: visual consistency is authorized; content
  decisions remain with the instructor, including corrections and teaching sequence.

- Revise all five Genetics LECT07 decks against their original sources using the existing
  importer. Remove unrequested teaching additions and rewrites; restore source sequence,
  images, and notes while retaining approved announcement and formatting changes. Record
  remaining representation gaps with @replaceme and supersede the old LECT07 review report.

- Put the mandatory outside-sandbox LibreOffice rule first in AGENTS.md, explicitly covering
  indirect metafile conversion during ODP imports and conversion tests.

- Restore the missing n, n!, ln(n!) tables beside both LECT07B factorial explanations,
  preserving the original 0-9 then 0-16 progression and original definition wording.

- Add spaces around multiplication signs in both LECT07B factorial expansions.

- Record the instructor's prohibition on adding slide content during conversion, including
  invented learning objectives, summaries, prompts, explanations, and slogans.

- Correct LECT07B birth-probability questions to the multiple-choice answer-reveal layout;
  highlight the changed condition, restore source wording in the independence explanation,
  and separate the seven-child alternatives from the assumption.

- Record the required stacked fractions and binomial coefficients; withdraw the earlier
  LECT07 review instruction to use slash fractions and C(n,k). Native math rendering remains
  unimplemented, despite parser support for dollar-delimited expressions.

- Restore the visible public YouTube channel URL on Genetics LECT05-07 channel slides;
  retain automatic condensed URL formatting and clickable destinations. Shorten the
  explanatory sentence to fit on one line.

- Apply mandatory condensed, smaller URL typography to visible URL labels even when their
  clickable destinations differ; prevent code styling from overriding the URL font. Keep
  layout measurement and exported text styling consistent.

- Preserve explicit hyperlink destinations when the visible label is itself a URL; prevent
  nested automatic links from overriding password-bearing meeting targets.
  Validate local course links with 154 focused tests and PDF hyperlink inspection.

- Record course-link and evergreen Discord guidance: include actual URLs in student slides,
  retain the opening server slide after signup deadlines, and distinguish assignment reminders.
  Record untracked root YAML imports as a proposed storage approach.

- Restore the title-card fill as a pale, desaturated course-color tint on the master-owned background,
  preserving separate
  native cover text. Record the instructor's preference for filled cards over an outline-only design.

- Simplify Genetics LECT07's assessment schedule to fixed item/date lines with abbreviated months.
  Preserve dates and status colors; move the long link and explanatory material to notes.

- Move cover decoration to a dedicated course-derived master; leave metadata as native slide text.
  Explicit stacking indices did not resolve the reported PDF text-selection problem.
- Normalize announcement covers across courses, add a title slide before Biotechnology Set 3's
  teaching content, and separate Set 4's chapter metadata from its talking-points note.

- Restore separate title, chapter, instructor, and date lines on all five Genetics LECT07 covers.
  Export explicit native stacking indices so the unfilled gray title border stays behind text.
  Consolidate the global cover requirements in a dedicated Human Guidance slide 1 section.
  Verify BPW chapter mapping: probability review/progeny decks use Chapter 4, chi-square uses
  Chapter 7, and announcements span both. Add editable parenthesized chi-squared to the title.

- Apply assessment-date colors to Genetics 07A: completed quizzes and midterm in light gray,
  future assessments in black. Record dark red for next-week assessments; none apply this week.
- Restore editable math, factorial and Pascal tables, the surviving-mice distribution, multinomial
  examples, and chi-square calculations. Reduce image placements from 48 to 13 after review.
- Rebuild step-by-step chi-square completion with stable native tables. Correct legacy rounding
  of expected counts, p-value interpretation, seed/pod terminology, and flattened exponents.
- Accept valid embedded ODF document-directory references with manifest-declared, present
  `content.xml` members. Preserve rejection of missing content and unsafe paths.

### Decisions and Failures

- Initial import encountered formula-directory references incorrectly treated as missing files;
  repair the package reader. Sandboxed metafile extraction also failed; manually rebuild the
  affected teaching mathematics as editable Djot rather than relying on missing previews.
- Keep explicit replacement markers for the source animation and stacked integral equations that
  cannot be faithfully represented in Djot. Treat the old activity URL as an editorial update,
  not a replacement-marker condition; retain it in notes and use the included worksheet.
  Preserve detailed provenance and review boundaries in
  [LECT07_REVIEW.md](../genetics/LECT07/djot/LECT07_REVIEW.md).

### Developer Tests and Notes

- Cover/source regression checks: 132 passed, including all 61 standalone Djot decks.
  Two focused external LibreOffice tests pass for PDF cover text extraction and master ownership
  after resaving, one per course theme. Rebuild all five LECT07 ODP/PDF pairs and visually review
  the announcement cover, chi-square cover, and simplified assessment schedule.
- The broader native-layout E2E runner exposes unrelated stale layout-uniqueness and big-image
  occupancy assumptions. Leave that runner unchanged; focused cover acceptance is reported
  separately. The instructor confirms PDF text selection works.
- Podcast refresh: four focused tests pass; repeated refresh produces no source diff. Preview
  accepts both Genetics and Biotechnology lecture folders. Lecture 07A passes strict lint and
  capacity checks; rebuilt ODP/PDF and the podcast slide's layout and hyperlink were verified.
  The addition brings Lecture 07 to 203 authored slides, 189 visible pages, and 14 images.
- Strict native/semantic lint passes for five sources, 202 slides, and 13 image placements.
  Capacity inspection reports no concerns. External LibreOffice builds all five ODP/PDF pairs.
- Reader/export regression checks: 43 passed, including the embedded-document reference repair.
  Parser checks: 70 passed. Final package inspection confirms matching page/visibility counts and
  identical native table geometry across chi-square steps. Rendered decks and revised math/table
  pages reviewed; no attended click-playback claim.

## 2026-10-15

### Additions and New Features

- Split Lecture 07B's four major project sections into included chapter files, retaining intro,
  AI policy, milestones, and peer evaluation in the main source. Add between-slide include blocks
  with a single section-wide hidden flag; preserve existing visibility and physical diagnostics.
  Name chapters `lect07b1-three_ideas.djot` through `lect07b4-executive_summary.djot` in order.

- Support standard Djot highlighting, insert/delete, subscript, superscript, and braced bold/italic
  as editable ODP text styles retained in PDF. Keep standalone highlighted paragraphs as content.
- Rebuild Lecture 07A with the agenda's Shark Talk presentation highlight.

### Fixes and Maintenance

- Audit runtime, pytest, E2E, and release gates against robustness/KISS guidance. Remove font
  hash/provenance build requirements, fixed template typography/overflow checks, quarter-point
  cache restrictions, and input ZIP ordering restrictions. Measure actual usable fonts and read
  template sizes/spacing. Keep structural/content safety and atomic output publication checks.
- Remove 20 policy/redundant pytest modules plus the historical E2E page-count gate and obsolete
  helper/snapshot tests. Document retained gates and actionable failure responses in
  [GATE_AUDIT.md](GATE_AUDIT.md); use temporary checks for the audit's compatibility evidence.
- Record human guidance on graceful recovery, aggressive KISS, demonstrated compatibility needs,
  actionable gate failures, and the permanent-test checklist in the repository guidance.
- Resolve the 19 reported hygiene failures: normalize remaining symbols in nine archived lecture
  text files; use the bounded XML reader in tests; correct test annotations, a path literal, and
  the genetics rendering helper's indentation, executable mode, and development dependency.
- Split oversized design decisions into native-presentation and source-pipeline references, and
  move quantitative teaching and delivery guidance into a linked companion. Preserve all sections.
- Remove license-text validation from slide-build gates. Copy available notices into output;
  preserve upstream license bytes by excluding them from automatic text cleanup.
- Repair five corrupted punctuation sequences in Lecture 07B using ASCII hyphens, straight
  quotes around "pretend", and the apostrophe in "don't". Verify the entire source is ASCII.
- Report invalid UTF-8 at its actual source line and character column, with a marked excerpt
  and save-as-UTF-8 guidance, instead of a misleading line 1 and raw byte offset.
- Detect bare HTTP(S) URLs with Djot-escaped scheme colons as editable hyperlinks, matching
  plain URL behavior. Preserve trailing punctuation and document that escaping is optional.
- Rebuild Lecture 07A announcements with the anonymous-message URL linked and styled.

### Developer Tests and Notes

- Gate audit validation: 1,078 remaining checks pass with no warnings (previously 2,622).
  Lecture 07A builds to ODP/PDF using external LibreOffice; rendered agenda retains its layout,
  italics, and highlight. Temporary compatibility checks pass for changed font metadata, template
  spacing/overflow metadata, non-quarter sizes, and repacked ZIP ordering/compression.
- Full test suite after hygiene and license-gate repairs: 2,622 passed, with three existing
  source-size advisories. Lecture 07A editable ODP builds successfully. Regression coverage verifies
  that absent and changed license notices do not block font metadata or license packaging.
- Encoding diagnostics: 75 parser/lint checks pass, including multibyte text, long input, and
  LF/CRLF/CR line endings. The actual Lecture 07B file now reports line 122, column 19.
- Formatting validation: 119 parser/layout/ODP tests pass; strict native lint and external
  LibreOffice exports pass for Lecture 07A and a one-slide formatting review. Visually checked
  the agenda highlight and every requested inline format in rendered PDFs.
- Expanded checks: 579 pass, with three existing failures (two oversized documentation files
  and missing return annotations in `tests/test_odp_reader.py`), confirmed against HEAD.
- A sandboxed LibreOffice attempt crashed with status -6. External export succeeded; use that
  path directly for subsequent macOS PDF builds.

- Parser, layout, and ODP export checks: 118 passed, including plain and escaped URL schemes.
- Sandboxed LibreOffice export exited with status -6; the build outside the sandbox succeeded.

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
