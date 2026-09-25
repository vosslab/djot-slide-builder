## 2026-09-25

### Fixes and Maintenance

- Corrected the 2026-09-24 heading so commit_changelog.py recognizes its entries.

## 2026-09-24

### Additions and New Features

- Expanded Biotechnology 04C from the full instructor deck plus the complete 30-topic synthesis to
  386 slides. Rebuilt both animated quiz sets as visible question-and-answer flipbooks, retained all
  six hidden source answer slides and the instructor's original closer, and added at least one local
  image to every slide. The expanded notes retain useful explanation while dense pages use shorter
  phrases.
- Extended the dedicated `theend` layout to accept one optional component image while preserving
  its framed, editable two-line closer.
- Added the explicit `theend` layout for final slides, with source validation for one exact
  `# THE END` heading; migrated canonical deck closers to the named layout.
- Preserved `hidden: true` slides as native hidden ODP pages; the PDF/classroom view continues to
  omit them, while capacity inspection includes their authored content.
- Stored hidden state in native ODF drawing-page styles and explicitly disabled hidden-slide PDF
  export so LibreOffice keeps archived pages out of classroom PDFs.
- Restored all 42 archived Lecture 04B project slides after the eight current Fall 2026 slides as
  hidden, editable pages (50 physical pages total), removing a legacy screenshot that exposed a
  student filename.
- Organized Biotechnology by lecture: Djot sources and local assets now live under each
  `biotech/LECT##/djot/`, while original decks, PDFs, and course source files live under the
  corresponding `old/` folder.
- Added Lecture 04A announcements, a current-schedule Lecture 04B project overview, and a synthesized
  Lecture 04C protein deck combining the 2025 instructor ODP with 2022-2026 student-presentation
  sources.
- Added `biotech/LECT04/djot/LECT04_REVIEW.md` with migration counts and the visual-review boundary.

### Fixes and Maintenance

- Corrected Lecture 04A's copied Lecture 03 heading, date, agenda, set number, and weekly talking
  marks reference for Sept 24, 2026.
- Updated the file-structure and usage guides with the lecture-organized Biotechnology corpus and
  its lecture-folder build command.
- Normalized the moved Lecture 03B Djot typography and example icons to ASCII, following the
  presentation-source authoring guidance.
- Removed the imported Lecture 04A gradebook screenshot containing student IDs and scores from the
  canonical Djot deck and its local assets.
- Replaced Lecture 04B's stale 2024-25 project dates with the published Fall 2026 project sequence.
- Expanded Lecture 04C to 220 slides covering all 30 Fall 2026 protein topics, with at least seven
  slides per topic and expanded answer coverage; protein gels has an additional staining page.
- Added 16 reviewed figures extracted from the Fall 2026 student PDF, recorded their page provenance,
  and adapted the professor ODP's proteomics/metabolomics flipbook as two sequential
  question-and-answer pairs.
- Kept presenter names and identities out of the canonical deck; the incomplete student
  presentations remain archived as source material.
- Corrected the carried-over figure descriptions and replaced an unrelated image with a Western
  blot example; removed a low-quality IRES figure.
- Replaced two misassigned ELISA figures on the instructor's central-dogma slide with the relevant
  omics-flow diagram, and replaced unreadable entity codes with DNA/RNA/protein process labels.
- Replaced the Lecture 04C proteomics/metabolomics click-reveal list with two question-and-answer
  flipbook pairs and rebuilt the 220-page editable ODP.
- Converted the instructor's two seven-question click-reveal sequences into adjacent question and
  answer slides, and the antibody-recognition reveal into an adjacent prompt and explanation. The six
  original hidden answer pages remain hidden in ODP, while the visible sequences appear in the PDF.
- Advanced the Lecture 04A Veridian Dynamics announcement to Video #4, "Diversity Good for Us,"
  using the numbered movie filenames as the source of truth and keeping the original image unchanged.
- Removed the outdated LibreOffice closed-desktop preflight. Headless conversions keep the tested
  sequential command shape and can run while the desktop application is open.
- Restored the original full-size talking marks page and its explanatory points, plus the separate
  Grading and Assessment divider. The prior spreadsheet screenshot stays out for instructor paste-in.
- Restored Lecture 04A's specialty `THE END` closer with two giant centered editable lines and its
  native vector star.
- Regenerated all three Lecture 04 ODP/PDF pairs through direct, source-ordered headless LibreOffice
  conversion. The 04B PDF contains its eight Fall 2026 pages, while the editable ODP retains the 42
  archived pages with native hidden status.
- Strict native Djot validation passed all three sources and 454 physical slides (406 visible, 48
  hidden). Capacity inspection reports no concerns for 04A or 04C; the seven below-floor paragraphs
  belong to hidden archived 04B pages. Representative visible pages were rendered and visually
  reviewed after the final edits; the six hidden 04C quiz answers were confirmed in the editable ODP
  and omitted from the PDF.

## 2026-09-21

### Additions and New Features

- Added regenerated high-resolution HTML-table figures for the Lecture 04G Punnett-square
  progression and Lecture 04I seven-gene worksheet sequence, with local HTML provenance and a
  reusable rendering helper.

- Converted the nine Genetics Lecture 04 ODP decks to canonical Djot sources with adjacent native
  image assets: announcements, Mendel history, the first two principles, cross experiments,
  segregation, Punnett squares, independent assortment, independent-assortment problems, and the
  multiple-cross problem.
- Added `genetics/LECT04/djot/LECT04_REVIEW.md` and extended the Genetics Djot inventory with Lecture 04
  provenance, source counts, hidden-slide counts, and delivery evidence.
- Reorganized the Genetics corpus by lecture: canonical sources and assets now live under each
  `genetics/LECT##/djot/`, while original ODP/PDF/ODS evidence lives under the matching `old/`
  folder. The existing recursive builder can now target one lecture directly.
- Replaced the Genetics announcement recording visuals and informational-slide blocks in Lectures
  02A, 03A, and 04A with the polished Biotechnology pattern, using the shared recording, Zoom,
  YouTube, Discord, and office-hours visuals while retaining each deck's course-specific content.
- Reworked Genetics Lecture 04B's "Character and Trait" quiz into a two-over-one-panels layout,
  keeping the character and trait columns above the question and answer choices.
- Re-lettered the canonical Lecture 04 sequence from D--K to B--I and applied the same names to
  the adjacent original evidence, asset directories, import reports, review inventory, and builds.
- Repaired the six Lecture 04C terminology quiz stems so each complete question is a paragraph;
  the answer-choice lists now contain only the A--G choices and receive the intended layout space.
- Restored the original Lecture 04C principle-emphasis sequence: paired factors is emphasized on
  its lead-in lists, dominance is emphasized on its lead-in lists, and the other principles are gray.
- Recast the Lecture 04C visible page 23 open-ended principles prompt as a `subsection` question
  prompt instead of a chapter `section` divider.
- Reworked the Lecture 04C visible page 27 blending-hypothesis slide as `stacked-panels`, giving
  its flower diagram a dedicated lower panel instead of allowing mixed-flow text sizing to collapse
  the image.
- Reworked visible Lecture 04C pages 32--34 as `two-panels`, separating allele definitions on the
  left from the genotype examples and dominance sequence on the right.
- Drafted `docs/active_plans/active/djot_deck_includes_plan.md` for reusable Djot deck includes,
  including source-local asset provenance, dependency-aware folder discovery, and a shared
  announcement pilot.

### Fixes and Maintenance

- Increased the Lecture 04G and 04I HTML-table rasterization from 144 DPI to 200 DPI while
  retaining lossless PNG output; regenerated table figures are now about 3333 x 1667 pixels,
  avoiding oversized source assets while preserving clear projected text.
- Applied cumulative light-gray choice depletion to the six Lecture 04C terminology quizzes:
  choices already used as answers are gray on later slides while the current and unused choices
  remain dark.
- Increased Lecture 04C's active-principle cue to high-contrast red for both the principle and its
  definition, while retaining gray for the inactive principles across the repeated overview slides.
- Reworked the Lecture 04B Mendel-history slide 21 as a side-by-side teaching slide so the
  true-breeding hybrid figure receives a full image region instead of collapsing to an inline
  postage-stamp image above the explanatory text.
- Added authored line breaks to the Lecture 04A Blackboard Homework list so each assignment's
  complete due-date phrase stays together instead of stranding the day on a third visual line.
- Fixed the Genetics 04A Syllabus Links slide by using bare Djot URLs for same-text hyperlinks;
  underscores in the long `ASSIGNMENTS_AND_GRADING` link had been interpreted as emphasis and
  caused part of the URL to render in a different type style.
- Replaced the Shutterstock-watermarked recording card in Genetics announcement decks 02A, 03A,
  and 04A with a clean local recording visual. The Biotechnology reference asset contained the
  same watermark, so the replacement is an original local card rather than another copied stock
  image.
- Manually reviewed the relettered 04G--04I decks: 04G now uses a readable progressive and
  highlighted Punnett-square series, 04H uses a lower-weight question prompt, and 04I restores
  the lost worksheet tables plus the two closing group-work tables.

- Reworked Genetics Lecture 04A as the 2026 announcement deck, combining current Lecture 03
  guidance with recurring Lecture 04 material from the 2025 announcement source. Current Fall 2026
  schedule dates, assignment and quiz information, course links, office hours, and non-obsolete
  contact guidance now replace stale course details.
- Polished Biotechnology Lecture 03A using the same announcement treatment: current assignment and
  talking-point language, current course links and office hours, clearer contact guidance, corrected
  image-number collisions that placed Genetics/biochemistry screenshots on Biotechnology slides,
  and text-only fallbacks where no course-appropriate source image was available.
- Retained source-hidden slides in the canonical Djot files and kept original ODP/PDF files as
  visual evidence rather than making them alternate authoring sources.

### Developer Tests and Notes

- Strict native Jotdown validation accepted the nine Genetics Lecture 04 sources and the revised
  Biotechnology Lecture 03A source. Native `--format all` builds produced matching editable ODP
  and PDF page counts: 289 visible Lecture 04 pages and 17 Biotechnology Lecture 03A pages.
- The native build required the repository's LibreOffice preflight to access `ps`; the successful
  build was rerun with the required execution approval. The compiler still reports inherited dense
  slide capacity warnings, so this evidence does not claim a full visual review or attended Impress
  click-through.
- Verified the reorganized command `./build_slides.sh genetics/LECT04/` against all nine Lecture 04
  Djot decks; it selected no original files and produced matching ODP/PDF page counts.

## 2026-09-17

### Additions and New Features

- Converted Biotechnology Lecture 03A, 03B, and 03C ODP sources to canonical Djot with adjacent
  local source-image assets. The imports retain all 198 source slides, including the 31 hidden
  announcement and project slides.
- Merged the 2026 current-course and 2025 Lecture 03 announcement sources into the 2026 03A deck.
  The deck uses the 2026 course context, the recurring Lecture 03 agenda and reminders, and the
  September 17, 2026 presentation date.
- Rebuilt 03C as a classroom deck organized by chapter. Each of the 25 talking points has a section
  page, questions copied from the canonical single-topic template, and two short source-grounded
  answer slides. The 105-slide source replaces the 117-slide legacy compilation without publishing
  unverified student answers or names.

### Fixes and Maintenance

- Recorded the instructor's source-authority boundary for the Biotechnology Lecture 03C merge in
  `docs/HUMAN_GUIDANCE.md` and `docs/DESIGN_DECISIONS.md`.
- Corrected the 03A and 03B title pages to use the Biotechnology Lecture 03 title-slide structure,
  with their proper letter suffixes and September 17, 2026 date.
- Updated 03A Week 3 work and 03B project milestones from the published Fall 2026 Biotechnology
  schedule. Replaced historical 2024/2025 dates and unsupported midnight cutoffs with the current
  schedule's Sept 17, Sept 24, Oct 1, Oct 8, Oct 22, and Oct 29 milestones.
- Rebuilt the 03A remote-participation and office-hours slides as two-panel layouts. Replaced
  external legacy links and obsolete Zoom credentials with published Fall 2026 course links and
  current office-hour information.
- Rebuilt all Lecture 03B section dividers with an explicit topic heading and current-date subtitle,
  eliminating the legacy, independently placed deadline text and red-on-red date treatment.
- Formatted the Lecture 03B project-sequence date column as fixed-width `Mon DD` labels so its
  current Fall 2026 milestones align clearly.
- Added a roadmap item for a reusable centered-left two-panel layout without changing the standard
  top-aligned comparison layout.
- Added a roadmap item for a lower-weight subsection divider so chapter and numbered topic
  transitions can carry distinct visual hierarchy.
- Implemented the reusable `subsection` native centered-text layout with a burgundy transition
  surface, and applied it to all numbered Lecture 03C talking points while preserving bright-red
  chapter dividers.
- Completed a topic-by-topic Lecture 03C provenance check. It distinguishes cross-year coverage
  corroboration from factual certification and identifies the expanded-answer topics that require
  independent review before classroom use.
- Restored the source-provided Bozeman Science `What Is CRISPR?` YouTube reminder slide after the
  Native CRISPR answer sequence.
- Normalized the edited Lecture 03C Djot source to ASCII-only text, retaining project-supported
  escapes and entities for rendered Unicode where needed.
- Added automatic native-link projection for bare HTTP(S) URLs in Djot source, so course URLs no
  longer need redundant Markdown link wrappers.
- Expanded Lecture 03C from three to four slides per talking point and added selected relevant
  legacy-ODP and Fall 2025-PPTX visual assets to answer pages. The old ODP is retained only as a
  partial historical source, while the Fall 2025 PPTX corroborates complete topic coverage.

### Developer Tests and Notes

- Strict Jotdown 0.10.0 validation and semantic Djot lint accepted all three Biotechnology Lecture
  03 sources. The revised 03C passed its native build with an 80-page editable ODP and matching
  LibreOffice-derived PDF; every question and answer slide meets the 20 pt capacity floor.
- Completed a standalone LLM visual review of all 130 generated Biotechnology Lecture 03 PDF pages.
  The per-page scores and follow-up calls are recorded in
  `docs/active_plans/reports/biotech_lecture_03_slide_review.md`.

## 2026-09-15

### Behavior or Interface Changes

- Changed the ordinary slide-text default from OpenDyslexic to the bundled Atkinson Hyperlegible
  Next 2.001 regular, bold, italic, and bold italic faces. Updated deterministic measurement, the
  native OTP defaults, package-only font embedding, provenance, and inline-code rendering while
  retaining PT Sans Narrow for displayed literal URLs.
- Added restrained native shape treatments for the standard lecture cover, section divider, and
  closer. Sections now use a solid dark transition surface with exactly centered text in a rounded
  frame. An exact `THE END` section renders as two giant centered lines with a vector star inside
  the D.
- Added the `big-image` layout with one focal image and a separate full-width editable caption.
  Converted the recording reminder, YouTube, and Discord signup examples in both announcement decks.
- Restored the multiple-choice answer popup as a native rounded light-gray rectangle with a dark-red
  outline and editable dark-red text. Converted the two HLA question-and-answer examples to that layout.
- Changed the Genetics theme band and transition color from purple to blue, preserving purple as the
  stated Biochemistry course color. Section text is white for accessible contrast.
- Centered primary titles across the standard title-bearing layouts while retaining top placement
  where the layout uses a top title band.
- Added deck-level `color-theme` metadata with the course values `genetics`, `biostatistics`,
  `biochemistry`, and `biotechnology`. The selected theme now controls the native top band, links,
  table headers, cover accents, sections, and closers; all Genetics sources declare blue explicitly.
- Added a closed semantic text-color vocabulary for attributed blocks, list items, and inline Djot
  spans. Restored the original red, orange, green, and purple parental-haplotype grouping on HLA
  offspring slides 33 through 36 as editable font-backed text.
- Added image-relative `arrow` and `outline` records to `big-image`. They map through the displayed
  aspect-preserving image rectangle and export as editable native ODF lines, arrow markers, and
  transparent rectangles; object-level appearance reveals work on either shape.

### Fixes and Maintenance

- Repaired native tables so light body cells, content-aware column widths, and measured row heights
  reach ODF serialization from one shared measurement result. The eight-row restriction-site table
  now retains every row and its bottom border without truncation.
- Extended bounded ODP import to retain recognized text colors and native image annotations. The
  importer resolves properties through admitted ODF styles and emits overlays only when both
  endpoints belong unambiguously to one image; other legacy drawings remain explicit review items.
- Normalized genetics title-slide metadata to a subject/topic line that accepts an optional
  colon-delimited subtopic, followed by separate chapter, instructor, and date lines. Removed the
  Lecture 03 slash separators, joined older split subject/subtopic lines, and standardized cover
  titles as `Lecture ##<letter>` with two-digit lecture numbers.
- Recorded the title-slide line-boundary and Atkinson Hyperlegible Next typography guidance and
  design decisions.
- Added a format-neutral page-surface fact and native ODF projection for solid page colors, hidden
  master decorations, rounded rectangles, and five-point stars. Authored lettering remains editable
  font glyphs throughout ODP export and LibreOffice PDF conversion.
- Reserved a visible bottom margin for ordinary slide content and removed the obsolete quiz-named
  18 pt floor; multiple-choice questions now use the normal body-text floor.
- Replaced `defusedxml` with a narrowly configured `lxml` parser that rejects DTDs and disables
  entity resolution and network access. Removed one source emoji that forced a Type 3 PDF font.

### Developer Tests and Notes

- The full pytest suite passed (1,991 tests), and structural lint accepted all 15 genetics sources
  with 611 authored slides and 335 images. The pinned native Jotdown executable was unavailable, so
  its separate source-acceptance lane was not run.
- The current full Genetics build produced 15 editable ODPs with 585 visible pages. Package
  inspection found all four renamed Atkinson faces in every ODP and no OpenDyslexic reference.
  A one-time semantic audit found six focal-image slides, 102 sections, 15 native closers, and the
  two native HLA answer popups. Existing capacity diagnostics remain visible for dense inherited slides.
- A temporary four-theme build verified that every authored course name writes its selected native
  band and accent colors. All four readable accents pass the documented 5.5:1 white-background target.
- The normal Genetics build produced all 15 editable ODPs and LibreOffice-derived PDFs with 585
  matching visible pages. Every PDF font was embedded and no Type 3 font appeared. Native package
  inspection confirmed font-backed color spans, editable tables, an arrow marker, and a no-fill
  outline; temporary rendered review confirmed alignment and absence of table clipping.

## 2026-09-14

### Additions and New Features

- Converted Lecture 03's seven current ODP decks to canonical Djot and local source-image assets:
  275 authored slides, including 26 hidden announcement slides and 249 visible slides. Used the
  2026 announcements and retained the original teaching sequence and visible slide counts.
- Added per-slide `hidden: true` / `hidden: false` metadata before content. ODP import now retains
  hidden slides and their assets; lint checks all source slides while ODP/PDF builds omit hidden
  slides. Restored Lecture 03's 26 hidden slides without changing the 40 edited visible slides.

### Fixes and Maintenance

- Recorded the announcements workflow: copy the current year's previous lecture announcements,
  then merge in the target lecture's announcements from the previous year:
  `LECT(N) 2026 + LECT(N+1) 2025 -> LECT(N+1) 2026`.
- Clarified which announcement content follows the year, which follows the lecture/week, and
  which dates and reminders must be updated for both in `docs/HUMAN_GUIDANCE.md`.
- Recorded the plain-language planning criteria in `docs/HUMAN_GUIDANCE.md`: prefer familiar words
  and direct sentences, and use technical terms only when they improve precision or clarity.
- Repaired content omitted by legacy drawing and SVM import using existing Djot layouts: blood-test
  results, HLA combinations and answers, STR evidence, genotype tables, ABO SNP outcomes, sequencing
  steps, genome-chart labels, and review-challenge cues. Improved figure/text placement and shortened
  table labels after rendered inspection. Updated lecture covers and the Lecture 03 agenda.
- Recorded the requested KISS priority and conversion details in the human guidance and
  `genetics/djot/LECT03_REVIEW.md`. Content repairs use the existing layouts; the hidden-slide feature
  adds one semantic boolean and filters classroom compilation without adding an export mode.

### Developer Tests and Notes

- Strict native Djot lint and ODP/PDF exports passed for all seven decks. Verified 249 visible slides,
  249 native ODP pages, and 249 PDF pages; inspected rendered contact sheets and repaired problem
  slides against the original PDFs. Dense inherited content still produces capacity warnings;
  historical links and facts were retained, and attended reveal playback was not tested.
- The hidden-slide feature passed the full pytest suite (1,921 tests), covering metadata errors,
  hide/show output, hidden-asset validation, and import preservation. Strict lint accepts the
  restored 66-slide announcements source.

## 2026-09-09

### Additions and New Features

- WP-E3: `title-only` now accepts a leading H1 followed by ordinary editable root text, lists,
  component images, or one table in the blank region below its native Title Only placeholder.  It
  retains `AUTOLAYOUT_TITLE_ONLY`, one title placeholder, and the established START/TOP title.
- Embedded OFL-compliant uniquely renamed copies of the six hash-validated bundled font faces in
  every generated ODP with stable face-specific ODF declarations and editable-run mappings. The
  exporter validates OS/2 editable-embedding permission before publication; the unique package
  families prevent a host same-name substitute from replacing the measured repository asset. The
  package now includes the applicable OFL notices and freezes derivative font timestamps.
- WP-S1: Added `docs/DJOT_SLIDE_SYNTAX.md` as the compact authoritative Djot presentation-surface
  reference. It defines the 14-layout catalog, slots, title and section semantics, supported
  teaching syntax, reveal behavior, and native-destination boundaries.

### Behavior or Interface Changes

- Final eight-deck delivery is ODP-first: `./build_slides.sh genetics` now publishes exactly eight
  editable ODP files and eight LibreOffice-derived PDFs. The completed 50.6-second build preserved
  the 31/23/43/49/59/43/62/26 visible-page counts (336 total).

### Fixes and Maintenance

- WP-D1/D4: Consolidated active Djot authoring guidance in `DJOT_SLIDE_SYNTAX.md`. Operational
  documents now link to that reference while retaining their command, pipeline, corpus, and status
  roles; dated decisions now distinguish retired PPTX/OOXML paths from the active ODP/ODF boundary.
  Architecture references now describe master-backed heading layouts, title-only body objects,
  capacity inspection, and staged sequential LibreOffice PDF conversion.
- WP-C1/C2: Section dividers now use the authoritative native master outline rectangle while
  retaining centered text and middle vertical alignment.
- Replaced the private-profile, one-process LibreOffice batch experiment with the established
  simple method: one desktop-process preflight, then direct sequential `soffice --headless
  --norestore --convert-to` commands with the Impress PDF filter, output directory, expected-PDF
  verification, and a two-second settling interval. Folder PDF builds still stage and verify the
  complete set before publication, preserving existing final PDFs if conversion fails. The retired
  profile, process-group, timeout-cleanup, and GUI-orchestration complexity caused recovery prompts
  without solving a demonstrated problem; quality and DPI remain defaults rather than gates.
- WP-D3: Retired the direct PPTX exporter, OOXML animation writer, PPTX importer, temporary
  conversion path, `python-pptx` dependency, and their dedicated tests. Native ODP is now the sole
  editable build artifact; `all` writes ODP and its LibreOffice-derived PDF, and legacy PPTX is
  saved as ODP in LibreOffice before bounded import.
- WP-D3: Restored four compact format-neutral planner checks using direct source-model facts;
  the ODP pairing boundary remains covered without rebuilding PPTX fixtures.
- WP-D2: Removed measurement-cache counters and retired the unreachable cover/stretch picture-fit
  variants. The retained model checks name the native ODP adapter boundary they protect: declared
  placeholder topology, contiguous reveal activation, and contained image placement.

- Multiple-choice questions now use one adaptive choice-and-popup geometry whether or not they
  include an image, reserving the answer reveal outside every visible choice.
- WP-E2: Direct ODP import now recognizes a section only from immutable positive source evidence:
  a declared layout identity with one `subtitle` placeholder, one populated subtitle text frame,
  and no other meaningful object. The 63 matching genetics source markers now use `section`;
  ordinary heading-only slides retain their existing semantic layout.
- WP-A6: Title slides now use the authoritative native master title and outline frames, restoring
  readable subtitle metadata while retaining title/subtitle placeholders. Standard layouts preserve
  the largest readable title before reporting a genuinely constrained named body slot. Title
  measurement keeps the repository-owned font facts and an 8-logical-pixel serializer margin while
  LibreOffice font determinism is resolved; body/list measurement and standard slot geometry are unchanged.
- Recorded the KISS and positive-prompting guidance: use the smallest coherent design that solves
  demonstrated needs, and phrase desired actions directly for small language models.
- WP-E1: Renamed the authored `centered-text` layout to `section` while retaining LibreOffice
  `AUTOLAYOUT_ONLY_TEXT` and its outline placeholder semantics. The centered one-frame builder now
  carries the `section` identity; `title-only` remains the separate `AUTOLAYOUT_TITLE_ONLY` layout.
- WP-A3: Set named corpus-derived typography recovery floors to 22 pt for titles and 20 pt for
  body text while retaining the 36 pt / 28 pt classroom defaults. The visible original-deck facts
  fixture records the migration baseline. The first selected-floor scan recorded 105 explicit
  residuals (82 paragraph/list, 10 title, 8 local-heading, 4 mixed-flow, 1 table) for WP-A6.
- Patch 3 (WP-A2): Added `deck_tools.py capacity <source>` for compile-only, deterministic
  capacity inspection. It aggregates explicit title, paragraph/list, table, mixed-flow,
  local-heading, and geometry/slot-constraint causes across a selected corpus, continues after
  source-located physical-capacity boundaries, and returns a nonzero result whenever a concern is
  present. Fixed title frames now measure their title and subtitle regions, while the project-owned
  `multiple-choice` layout evaluates its adaptive answer geometries before recording only the final
  capacity result. Normal builds retain their one-compilation recovery reporting; capacity inspection
  writes no presentation artifacts and invokes no LibreOffice conversion.
- Patch 2b (WP-A1, WP-A4): The compiler now emits exactly one `LayoutSlide` per authored Djot
  slide, with stable `slide-N` identities. Removed continuation, grid decomposition, context
  handoff, pagination fields, generated page chrome, and their serializer/accessibility paths.
  Representable over-capacity content now remains on its authored slide at a measured sub-floor
  quarter-point size and returns a source-located capacity diagnostic shown by normal builds.
  Title fitting now measures body capacity before construction and selects one deterministic title
  size instead of using exceptions as a layout-search oracle.
- Patch 3b (WP-A1, WP-A4): Compilation now returns an immutable result that pairs the render-only
  `LayoutDeck` with structured source-location/layout/slot capacity diagnostics. Normal builds
  propagate that single result to their summaries rather than recompiling completed decks. Capacity
  recovery uses a shared 1 pt serializer-safe minimum and raises a source-located physical-capacity
  error below that bound. Public PDF builds pass their generated ODP to LibreOffice directly.
- Patch 3c (WP-A4): Direct title fitting now uses the exact proportional mixed text/image allocation
  consumed by final construction. Vertical CJK layouts were retired before the final title solver,
  leaving one horizontal text-flow geometry for preflight and native output.
- WP-D5: Removed the unused CJK-only vertical layout contracts from Djot grammar, validation,
  measurement, and ODP/PPTX adapters. The supported catalog now contains the twelve standard
  Impress layout-panel identities plus the project-owned `multiple-choice` and `gallery` layouts.
- WP-A5: Collapsed the `layout_engine` catalog pass-throughs. `layout_registry` now directly owns
  public layout-name and contract lookup for Djot validation, import topology, and their tests,
  leaving the compiler's public boundary as `compile_layout_deck` only.
- M1: Native ODP picture frames now serialize the compiler-resolved displayed rectangle, preserving
  contained-image proportions instead of stretching every image to its allocated slot. Drawing-page
  styles now suppress the master page-number, footer, and date-time chrome while retaining the
  visible gradient background and background objects.
- WP-I1: Replaced the ODP migration bridge with direct native ODP extraction into typed source facts.
  Import admission now uses bounded archive/XML/manifest/media checks,
  source-page evidence, reviewable unsupported objects, and private same-parent staging. Publication
  prunes unreachable media, atomically renames assets, then uses the Djot file as its commit marker;
  bounded rollback preserves non-overwriting behavior. Local media requires both package and manifest
  membership; decoded raster bytes must match their published extension.

- Final artifact audit accepted 336 editable pages and 185 picture frames (maximum aspect error
  0.0068%) with suppressed chrome. The PDFs identify Impress as creator and LibreOffice 26.2.5.2 as
  producer; bounded direct import and both ODP/LibreOffice E2E gates passed.

### Removals and Deprecations

- M7 removed the canonical-SVG/diagram subsystem and its tests. The remaining importer uses simple
  same-parent staging, atomic asset rename, and a Djot commit marker; one durable rollback behavior
  test remains. The publication implementation fell from 521 to 245 lines and its tests from 327 to
  136 lines.
- The final six-pass audit removed the unneeded descriptor-level ODP input snapshot, two unused ODP
  reader helpers, and six mechanism-focused tests. Bounded package, XML, manifest, media, link, and
  page-evidence validation remains at the direct-reader boundary. The audit also corrected the
  roadmap and import-failure recovery documentation.

### Developer Tests and Notes

- One-time closeout evidence: 63 `title-only` markers changed to `section` with no other genetics
  Djot source diff; capacity reported 99 explicit accepted diagnostics (94 paragraph/list, 4
  mixed-flow, 1 table), all source-located; strict Jotdown 0.10.0 lint passed 8 sources, 336 slides,
  and 185 images; the post-audit fast suite passed 1,908 tests in 5.17 seconds.
- Six independent closeout review passes found no blocker or high-severity issue. The affected real
  23-slide direct import, original-deck parity E2E, and LibreOffice native-layout roundtrip passed
  after the accepted KISS fixes.
- The advisory visual review covered 336 standalone pages and 336 original/generated pairs: 48
  improved, 272 roughly equivalent, and 16 materially worse only at explicit native reconstruction
  placeholders. Those source-migration limitations remain accepted because the plan forbids
  source/image edits and the diagram abstraction was removed. Graphify rebuilt 1,497 nodes, 3,288
  edges, and 66 communities; `slide_lib/` is 12,532 lines.

## 2026-09-08

### Additions and New Features

- Completed the native ODP layout migration. Djot now compiles once into an immutable physical
  `LayoutDeck`; `odp_export.py` writes ODF 1.3 page layouts, presentation frames, editable text,
  hierarchical lists, tables, images, links, notes, and ODF/SMIL reveals, while `pptx_export.py`
  writes an independent optional sibling artifact. PDF remains derived from native ODP.
- Added bounded OpenDocument package validation and atomic publication in `odf_package.py`, plus a
  dedicated `odp_animation.py` timing owner. All 18 registered layouts receive native page-layout
  definitions and declared slides reference the compiler-selected definition.
- Added explicit LibreOffice `AutoLayout` classifier signatures to the format-neutral plan. Native
  ODP now exposes all 16 distinct built-in identities; LibreOffice preserves the 15 nonblank
  identities through open/save while normalizing the empty blank page's reference to its title-slide
  definition without adding content. Occupied editable frame roles remain independent and unchanged.
- Completed and independently accepted WP-L2, the format-neutral layout compiler. It compiles all
  18 layouts without output-format imports, uses committed exact font metrics (including
  quarter-point sizes), and applies 36 pt / 28 pt defaults with 30 pt / 24 pt floors. Its 171
  focused tests cover recursive inline/handoff/metadata continuation context, grapheme-safe explicit
  breaks, table and unsupported-fact parity, and grid-stream co-packing with immutable provenance.
  The complete `lect02a` source deterministically compiles to 99 physical pages; the approximately
  0.69-second cold compile is informational only. This completes compiler authority, not WP-O1/P1
  adapter work or the migration's native ODP/LibreOffice acceptance gates.

- Bundled hash-verified OpenDyslexic and PT Sans Narrow font faces with SIL OFL provenance and
  immutable style selection. Theme loading now exposes real intrinsic face metrics and refuses
  missing, tampered, or unavailable styles instead of using a system-font substitution.

- Added an execution-ready native ODP layout migration plan. It defines a shared format-neutral
  physical layout model, direct ODF 1.3 and sibling PPTX adapters, native ODF/SMIL reveals, explicit
  owners, dependency-ready work packages, and autonomous XML-contract, headless-preservation,
  PDF/render, and reveal-state acceptance gates.
- Made `genetics/xlect99-template_2023.otp` the authoritative master-slide theme. Added a validated
  format-neutral reader for its 16:10 page, top gradient, centered title typography, and nine native
  outline levels, plus ODP and PPTX adapters over that shared model.
- Recorded the target ODP-first artifact graph for the approved migration: the future direct ODP
  writer will create editable content from the shared layout plan, and PDF will derive from that
  ODP while PPTX remains an independent interchange artifact. The current build still uses the
  PPTX-to-ODP bridge until WP-I1 removes it; this entry is a plan/decision record, not completion
  evidence.
- Kept layout authoring on a stable 1280x800 logical canvas. The 16:10 ratio is mandatory while the
  template's physical centimeter or inch dimensions are not an authoring constraint.

### Fixes and Maintenance

- Fixed the first public `./build_slides.sh genetics` run after the native ODP migration. The
  compiler now recovers from the 17 masked corpus-capacity failures: dense multiple-choice
  questions separate context, stem, and choices, then adapt the editable choice split and column
  widths down to an 18 pt quiz-specific floor; the sized answer popup uses reserved space beneath
  the shorter column instead of covering final-state choices. One-descendant list overflow uses the
  existing static context handoff, and redundant repeated H1 context yields only when a readable
  authored leaf needs the full body. Ordinary body content retains its 24 pt floor, source order and
  slot provenance remain intact.
- Rotated the September 1, 5, and 6 entries into `CHANGELOG-2026-09a.md` after the active changelog
  crossed its documented 800-line threshold.
- Removed the superseded PPTX-to-ODP bridge, theme splice, legacy layout facade, and their
  implementation-pinning tests. Renamed the permanent compiler modules from leading-underscore
  scratch names to `layout_registry.py`, `layout_measurement.py`, and `layout_builders.py`.
- Removed the committed binary ODP fixture tree and its one-time fixture readers. Permanent tests
  now create inputs inline under `tmp_path`; the whole-system E2E builds source-owned specimens and
  verifies native layout and reveal identities through the documented LibreOffice
  `ODP -> FODP -> ODP` preservation path.
- Ran the requested six-pass pre-merge audit and removed seven implementation-proof pytest cases,
  orphan PPTX reveal wrappers, and stale test-tier wording. Retained only the fast behavioral
  layout, package, text, animation, and export contracts that satisfy `PYTEST_STYLE.md`.
- Resolved the audit's remaining architecture findings. `odp_text.py` now owns ODF paragraphs,
  spans, links, lists, tables, and text styles. The evidence-tier decision supersedes WP-V2's
  snapshot-specific 144-DPI thresholds and retained proof bundle while preserving the fixture-free
  LibreOffice E2E and one-time production-deck evidence.
- Completed the importer recovery boundary. `pptx_reader.py` now returns raw positioned facts and
  `slide_plan.py` alone validates normalized geometry. Native fallbacks follow retained source stack
  order, isolate tables in valid grid cells, and keep lossless normalized-region text, safe links,
  bounds, and presenter notes in `import_report.json` for later reconstruction.
- Forced a deletion-aware Graphify rebuild after the module rename sweep; stale underscore-module
  nodes and their duplicate-ID warnings are gone from the current architecture graph.
- Corrected the vertical catalog to match current Impress: vertical titles occupy the right strip,
  `vertical-title-two-panels` stacks its content regions, and `two-panels-vertical-clipart` retains
  its approved name but now accepts `left` and `right` side-by-side vertical-content slots.
- Bound one primary authored object to every content-slot presentation member, including native
  graphic frames for image-only and gallery regions. Reapplying a layout can no longer add an empty
  member over a picture or table that merely shared its geometry.
- Replaced the multiple-choice answer's ODF custom shape with a styled native `draw:frame` object
  target. The fixture-free E2E now requires every generated page to occupy its declared layout
  topology exactly once and verifies that LibreOffice preserves the answer frame, reveal identity,
  editable text, and all default-layout presentation classes.
- Corrected shared-plan projection defects that hid ordinary paragraphs, hard-broke normal prose in
  the middle of words, collapsed separate reveal blocks onto one shape, discarded hierarchical list
  structure, lost cascade target IDs during LibreOffice save, and treated line decorations as an
  invalid PowerPoint auto-shape.
- Normalized the two bundled OFL license text files and updated their recorded provenance hashes.
- Corrected the native ODP layout evidence so its pruned XML comparator is described as a
  deterministic structural fixture, while the complete `lect02a` slide 3 deck supplies the real
  `ODP -> FODP -> ODP` LibreOffice preservation proof. Layout identifiers are now documented as
  document-local names validated through their resolved placeholder topology.
- Extended the XML-only native-layout transition contract with the captured compatible alternate
  topology. It retains the One Box title and primary outline exactly once, permits only one empty
  secondary outline, and rejects duplicate or malformed slot mappings without a LibreOffice or
  human interaction dependency.
- Ran the requested six-pass code audit over the native Djot theme, legacy importer normalization,
  screenshot-fallback removal, tests, documentation, dead code, and comments.
- Removed permanent tests that pinned tunable theme coordinates, exact gradient colors, the dense
  label threshold, and one geometry-specific diagnostic phrase. Retained semantic native bullet,
  gradient, and centered-title coverage.
- Removed unused import-planning return state and unused vector fields. Replaced the obsolete root
  migration plan with a concise retired marker because repository file discovery still includes the
  tracked path while Git operations remain outside this work.
- Corrected current changelog wording that described the superseded bounded-raster implementation as
  live behavior, and clarified the canonical theme and simplification behavior for newcomers.
- Replaced residual `CSS px` terminology with format-neutral logical units; CSS and browser
  rendering are not part of the presentation theme pipeline.

### Decisions and Failures

- The post-migration compiler and focused `lect02a` acceptance both passed while the user-facing
  eight-deck build still crashed on its first deck. A source-by-source preflight exposed 16 more
  failures hidden behind that first exception. Full public-command acceptance is required for this
  recovery; a passing representative deck is not corpus acceptance.
- The six-pass review found that the archived migration checked WP-V2 complete without retaining all
  proposed acceptance machinery and that planned `odp_text.py` ownership remained folded into
  `odp_export.py`. The resolution restores the text boundary and narrows acceptance to durable
  behavioral, E2E, and explicitly one-time evidence instead of implementing snapshot-specific
  metrics solely to satisfy an archived plan.
- LibreOffice 26.2.6.3 normalizes the custom `multiple-choice` answer's `object` presentation class
  during `ODP -> FODP -> ODP`, even for the fixture-proven native frame form. The generated ODP
  still declares and occupies the exact custom topology; preservation acceptance therefore requires
  the answer's native frame, editable text, and reveal target rather than claiming LibreOffice keeps
  that custom class. Default LibreOffice layout classes remain exact.
- Approved the executable list-continuation and leading contract for the native layout migration.
  Ordinary outline text uses the OTP's 130 percent (1.30em) nominal line spacing; the compiler
  carries an exact per-wrapped-line safe advance of `max(nominal, mixed-face ascent+descent)` plus
  resolved list start/hanging indents in the physical plan, and both adapters serialize those facts
  unchanged. Overflow reduces only to 24 pt before ordinary atomic partitioning; only an oversized
  root-list subtree may recursively split between descendant subtrees. Repeated ancestry is explicit
  static `continuation_context`, and a too-tall leaf fails at its source location. WP-L2/T1/T2/O1/
  P1/V2 now have plan, projection, and LibreOffice parity gates; this records required work and does
  not claim it is implemented.
- Added the architect-approved context-handoff continuation addendum. The physical plan carries an
  ordered `ContinuationContext`, display mode (`INLINE_STATIC`, `HANDOFF_STATIC`, or
  `METADATA_ONLY`), and physical kind (`NORMAL`, `AUTHORED`, or `CONTEXT_HANDOFF`). A trail and new
  descendant share a page only when they fit; otherwise one static handoff page immediately precedes
  the detached descendant, with metadata-only context when the trail itself cannot fit. The
  descendant retains its level and must fit or fail source-locally. ODP/PPTX project nonvisual trails
  into equivalent accessibility descriptions and generated continuation notes. WP-L2/O1/P1/V2 own
  scripted fixture, cross-adapter, `lect02a` line 293, Student Profile line 470, and full-deck gates;
  this is a target contract, not completion evidence.
- Approved `DECOMPOSE_TO_ONE_PANEL` as the only overflow transition for eligible generic grids:
  `two-panels`, `one-plus-two-panels`, `two-plus-one-panels`, `stacked-panels`,
  `two-over-one-panels`, `four-panels`, and `six-panels`. Only a failed true-fit preflight with
  `paginate: true` may gather all nonempty slots in reading order and route them through the shared
  one-panel splitter; fitting grids remain unchanged. Resulting pages retain one-panel topology,
  repeat H1/context/qualified notes but not slot labels, use canonical image/table placement,
  preserve origin provenance and deterministic identities, and place every content unit and reveal
  once. Semantic layouts are excluded, while `paginate: false` and excluded or unsplittable input
  fail at the source location. The migration acceptance gate now includes `lect02a` line 362 and
  full-deck public-CLI success plus ODP/PPTX physical-page parity.
- Approved compiler-owned continuation policy for the native migration. A source slide begins as one
  panel; only true-fit failure with `paginate: true` may create same-topology physical pages, using
  the latest-fitting mixed partition while preserving paragraph, root-list-subtree, table-row-group,
  and atomic boundaries. Continuations repeat the H1 and active H2 without stranded headings, use
  deterministic `source_id-pN` identities, reset reveals per page, repeat qualified notes, and use
  physical page numbers. `paginate: false` and unsplittable atomic content fail at their source
  location before serialization. The acceptance gate requires `lect02a` line 112 to produce two or
  more pages at 24 pt or above with matching ODP/PPTX count and continuation order.
- Decomposed the approved layout compiler before WP-L2: `layout_engine.py` is specified as an at-most
  350-physical-line public API exposing only compilation and layout lookup; declarative contracts
  live in `layout_registry.py`, pure fit/pagination work in `layout_measurement.py`, and plan
  construction in `layout_builders.py`. The model ownership layers are
  `layout_primitives -> layout_content -> layout_model`, while `native_model` remains independent
  source-semantic input to the compiler. The exact import DAG, physical-line budgets, private-helper
  isolation, import-graph test, and no-module-at-or-over-1,000-lines gate are part of the migration
  plan; this is a design record, not an implementation-completion claim.
- Refined the approved native ODP architecture: `layout_engine.py` is the sole 18-layout compiler;
  adapters consume `LayoutDeck` only; canonical layout topology now includes semantic placeholder
  member kinds and geometry while excluding authored content; and ODP XML names are treated as opaque
  document-local serialization details. Direct ODP retains template masters, styles, and resources,
  replaces `content.xml`, reconciles the manifest under strict reachability rules, parents local
  styles to shipped `Default-*`, and assigns deterministic adapter-owned media identities. Fast
  package/XML tests remain separate from serialized headless LibreOffice E2E preservation evidence.
- Diagnosed the generated layout failure on slide 3 of `lect02a-2025_announcements`. The blank-layout
  PPTX intermediate becomes imported `ooxml-rect` custom shapes in ODP, so applying One Box creates
  new empty placeholders instead of reusing the authored content; replacing the master and styles
  cannot restore layout identity that the intermediate never supplied.
- Replaced the planned PPTX-parent architecture with direct native ODP and optional sibling PPTX
  adapters over one format-neutral layout plan. The theme contract now starts standard titles at
  36 pt with a 30 pt build floor, and ordinary body/list text at 28 pt with a 24 pt build floor;
  the compiler rejects below-floor fits before serialization, while native shrink-on-overflow is
  only a font-metric safety net.
- Approved WP-T2 as a hard precondition for compiler capacity acceptance: committed, hash-verified
  OFL font assets and provenance define immutable theme face profiles; Pillow measures styled runs
  with token-aware line breaks, actual OTP list text-start/hanging indents, and mixed-face line
  boxes. Missing, changed, unresolved, or substituted faces fail before publication; cache keys
  include font identity and measurement inputs. OpenDyslexic serves ordinary text, while PT Sans
  Narrow is limited to its committed applicable URL faces with no invented italic fallback. The
  rejected `0.25em` heuristic and generic 10-percent width cap cannot determine fit. Offline asset
  tests and V2 runtime-drift evidence are required before this becomes completion evidence.
- Rejected `pyuno` as the current automation harness after reproducible host failures: external
  Python 3.12 segfaults during LibreOffice `pyuno` import or initialization (exit 139), and the
  bundled LibreOffice Python launcher is killed (exit 137). Completion instead relies on the desired
  ODP XML contract, captured minimal fixtures, deterministic package-XML transitions and
  reveal-state interpretation, headless LibreOffice open/save preservation, and PDF/render metrics;
  UNO is an optional future diagnostic only after its runtime is repaired.
- Identified an implementation tracking gap: the authoritative OTP and approved minimal ODP fixtures
  are hidden by broad `*.ot?` and `*.od?` ignore rules and are absent from `HEAD`. The integration
  work owns narrow allowlists; this documentation update does not use force-add or index workarounds.
- Simplification retains the same instructional text and genuine content images through an existing
  Djot layout whenever possible; a review diagnostic accompanies content instead of replacing it.
- The audit found three importer defects: dense positioned-label normalization dropped recoverable
  text, a table-bearing fallback could choose an invalid mixed one-panel layout, and normalization
  received geometry-ordered components. The focused recovery boundary above resolves all three
  without restoring raster substitution or adding a speculative layout mechanism.

### Developer Tests and Notes

- The final permanent offline suite passed all 1,993 tests. The source-built 18-layout E2E passed
  sibling PPTX/native ODP creation, all native ODF page-layout references, hierarchical lists,
  source-ordered reveal targets, LibreOffice ODP open/save preservation, and ODP-derived PDF.
- The final public all-format build of `lect02a-2025_announcements.djot` produced 99-page sibling
  presentations and PDF. Before and after a LibreOffice open/save, physical slide 3 retained exactly
  one native title frame, one native outline frame, and a resolved native page-layout reference.
- A disposable whole-import probe created an overlapping editable table/prose PPTX with a presenter
  note. The public importer emitted a validated two-panel Djot source, preserved the note in its
  report, published atomically, and left no temporary script or artifact behind.
- Theme, native-export, importer, and hygiene verification passed 757 focused tests. The full
  permanent offline suite passed 1,682 tests, and strict native Jotdown validation retained 8 Djot
  sources, 336 slides, and 185 genuine image references.
- The native-layout E2E passed through editable PPTX, OTP-master ODP, and ODP-derived PDF with
  distinct native list levels. The full Genetics build produced 24 artifacts; all 336 slides had
  matching counts, every ODP used the exact template styles and master, every PPTX was 16:10, and no
  PPTX contained a full-slide picture substitution.
- Cropped ODP-derived PDF checks, rather than whole-slide screenshots, confirmed the shallow
  gradient, centered title, level-specific bullet forms, and wrapped-line hanging alignment.
- The first full-suite cleanup run stopped during collection because the deleted tracked migration
  plan remained in repository file discovery. Git operations were out of scope, so the path was
  restored as a concise retired marker; the corrected full suite then passed.

## 2026-09-07

### Additions and New Features

- Added `deck_tools.py` as the sole format-neutral application CLI for build, import, Djot lint,
  and ODP visibility workflows.
- Renamed the reusable application package from `marp_lib/` to `slide_lib/` so its ownership covers
  both Marp and Djot without implying a Marp-only pipeline.
- Added the geometry-first legacy-import architecture: semantic ODP/PPTX normalization now produces
  `LegacySlidePlan` records for atomic editable components, true source tables, and bounded coupled
  spatial regions.
- Added the bounded native OOXML animation backend: object APPEAR/FADE and top-level outline
  paragraph APPEAR reveals are emitted through one programmatic timing-tree owner without widening
  Djot's authoring syntax.
- Added `source_model.py` and `pptx_reader.py` so imported-presentation readers retain raw runs,
  links, images, notes, and first-class `TableBlock` facts.
- Added `pptx_theme.py` as the native lecture-theme owner: every standard slide receives a shallow
  blue-to-white top band, centered title, and nine explicit list levels with bullet positions, text
  tab stops, and hanging indents.
- Added native source-order normalization for ambiguous legacy geometry and visible redesign
  diagnostics for dense positioned-label fields that do not map cleanly to standard slide language.
- Defined the intended `pptx_reader` -> `slide_plan` -> `djot_emitter` ownership boundary.
- Added newcomer-facing `CODE_ARCHITECTURE.md`, `FILE_STRUCTURE.md`, `FILE_FORMATS.md`,
  `DEVELOPMENT.md`, `COOKBOOK.md`, `TROUBLESHOOTING.md`, and `RELATED_PROJECTS.md` guides, plus
  differentiated `NEWS.md` and `RELEASE_HISTORY.md` v26.09 release views from `VERSION` and the
  current changelog.
- Added a static, text-only rendered slide page to the README as an output-proof example.

### Behavior or Interface Changes

- `build_slides.sh genetics` and folder-valued `deck_tools.py build` commands now recursively find
  only `.djot` sources, so imported ODP files and ordinary Markdown are never treated as decks.
- Made `deck_tools.py build` dispatch `.md` and `.djot` sources through the same command, and made
  Djot the concise default target for trusted ODP/PPTX imports.
- Changed `build_slides.sh` into a thin folder-build convenience around `deck_tools.py build`.
- An intermediate ODP/PPTX import path used bounded Poppler renders for difficult regions. The
  same-day native-only redesign removed that path before acceptance; current imports normalize
  difficult slides through standard Djot layouts.
- Ordinary panel layouts now describe optional global titles and one local H2 per cell, with
  source-located capacity preflight before native shapes are created. Source tables remain editable
  only when the source provides actual table metadata; merged or spanned cells require review.
- Legacy source records now retain direct style, placeholder, z-order, rotation, and connector
  evidence. A shared registry-topology matcher and bounded positive relation classes preserve
  coupled visual teaching structures while retaining ordinary source content as editable objects.
- Top/group z-paths now retain actual source order. Reusable coarse-body/picture-inset, caption,
  and adaptive vertical-image relations preserve native objects through topology-first routing;
  they use exact provenance and narrow permissions rather than global or crop exceptions.
- Imported Djot assets now publish only when reachable from the parsed deck in its local asset tree;
  unsafe, missing, and symlinked references fail staged publication.
- Made `.djot` the sole authored deck source. `deck_tools.py import` always emits Djot from trusted
  ODP or PPTX input and no longer accepts `-t` / `--to`.
- Imported text and hyperlinks now remain raw reader facts until the emitter renders Djot, and
  source tables retain rows, cells, headers, blanks, and exact shape binding.
- Adjacent nested Djot lists now retain their semantic hierarchy without requiring a blank line.
- `two-over-one-panels` now allocates its footer from actual content need while preserving the
  readable minimum for both upper panels.
- Ordinary native panels now retain up to six legitimate component images without requiring a
  composite representation.

### Fixes and Maintenance

- Refreshed install and usage guidance for Python 3.12 environment activation, Homebrew tools, a
  validated pinned Jotdown 0.10.0 Cargo install route, and native import/export workflows.
- Corrected current acceptance documentation to name the one retained Djot native-layout E2E after
  the duplicate runners were removed.
- Removed claims that authored Djot or the current native E2E preserves presenter notes. Import
  readers retain raw note lines, but generated Djot currently records their omission pending a
  non-Djot preservation design.
- Corrected stale documentation that still treated the selected Djot grammar as unnamed, qualified
  the README's unobserved reveal claim, and documented non-obvious DNA run normalization.
- Pruned redundant serialization assertions while retaining the observed LibreOffice-prime and
  split-run DNA regressions. Reviewed all six test functions added or materially rewritten for the
  Djot-first fork; retained their current-boundary or known-regression coverage and consolidated the
  table round trip to two semantic assertions.
- Made missing animation-writer reveal intent fail loudly and corrected source/native-renderability
  documentation.
- Synchronized shared style guides, tests, and repository support files from the starter template.
- Fixed imported text and links being escaped before the output boundary; the Djot emitter now
  escapes raw characters exactly once and encodes link-target delimiters only while rendering.
- Fixed the PPTX reader inventing spaces between adjacent alphanumeric runs; formatting-only run
  boundaries now preserve the source characters exactly.
- Fixed imported source tables so supported tables emit as parseable Djot pipe tables rather than
  flattened text, including literal pipes, links, blank cells, and DNA prime projection.
- Renamed imported-deck planning modules and `LegacySlidePlan` to package-scoped Djot-first names,
  and renamed the private animation-writer attachment to `_slide_animation_writer`.
- Refreshed the README newcomer route and `INSTALL.md` / `USAGE.md` workflows; updated
  `ROADMAP.md` and `TODO.md` to describe current open boundaries.
- Recorded the 350-character GitHub About limit and the publication boundary: image-bearing slide
  PNGs remain unpublished pending copyright assessment, while text-only slide pages may publish.

### Removals and Deprecations

- Removed the nine `tools/*.py` package-import wrappers without compatibility aliases; this
  pre-production repository has no external callers for the obsolete paths.
- Removed three tracked Python bytecode caches that still embedded the former `marp_lib` name.
- Removed dead importer wrappers, enums, and re-exports instead of retaining compatibility facades.
- Removed duplicate and brittle tests that did not meet the permanent pytest contract.
- Removed the Marp parser, ODP/PPTX-to-Marp routes, target-format switch, suffix-dispatch table,
  parser/importer tests, Markdown decks, deck asset tree, CSS theme, dedicated documentation, and
  `markdown-it-py` / `PyYAML` dependencies.
- Removed Marp-only title-size state, the duplicate PPTX extraction implementation, the obsolete
  native-layout E2E, `tools/`, and completed rename-plan archives instead of retaining compatibility
  shims in this pre-production fork.
- Removed the `source_region` raster subsystem completely: implementation, importer hooks, crop and
  protected-render state, dedicated tests, generated composite references, and stale corpus assets.

### Decisions and Failures

- Exact full-slide rasterization remains outside the importer contract. Ambiguous geometry and
  source-table spans stop for review so a later native owner can extend the model deliberately.
- Exact legacy appearance is not an import contract. Difficult slides normalize to the shared Djot
  theme or expose a visible native limitation; genuine source figures remain ordinary image assets.
- Final acceptance passed 1,660 permanent tests, strict Djot validation for 8 decks/336 slides/185
  image references, the native-layout E2E, and the full 8-deck/24-artifact PPTX/ODP/PDF build.
- `multiple-choice` answers allow one or two short flat paragraphs and carry implicit reveal intent;
  M5 is reopened around a bounded OOXML builder with LibreOffice Impress as the playback authority.
- Corrected the animation architecture: PPTX is the Python-friendly native-builder and interchange
  artifact, while LibreOffice Impress/ODP is the editing and playback contract. The builder will use
  official OOXML and programmatic timing construction in `pptx_animation.py`, with no runtime XML
  templates or Microsoft compatibility gate.
- M5 implementation and its permanent structural/parser tests are complete. One-time LibreOffice
  bridge and ODP-derived PDF checks passed. The sole remaining M5/M7 evidence is attended Impress
  click playback; macOS denied Screen Recording and Accessibility before slideshow control, so no
  playback conclusion is claimed.
- Made the fork Djot-first while holding the implemented Djot grammar and layout behavior fixed.
  Historical changelog and language-decision records retain their provenance; they are not runtime
  compatibility promises.
- For this non-PyPI application, `VERSION` supplies the date-block release identity; a root
  `pyproject.toml` is not required solely as a release-document cross-check.
- Used the pre-production state to replace the extraction boundary directly rather than preserving
  old output-shaped records or aliases.
- The six-pass Djot-first audit found two open design issues: `pptx_reader.py` still constructs
  planner region records, and generated Djot records presenter-note omissions rather than preserving
  the content. These findings remain open rather than being hidden behind compatibility shims or an
  invented Djot note syntax.

### Developer Tests and Notes

- After the Djot-first removal, the permanent offline suite passed 1,634 tests. The final one-time
  name checks found zero Marp references in `slide_lib/` and `tests/`, and no Python bytecode-cache
  directories remained.
- The exact `./build_slides.sh genetics` workflow found only the eight recursive Djot sources and
  produced 24 PPTX, ODP, and PDF files. Strict eight-deck lint and the Djot native-layout E2E passed.
- A fresh 62-slide Lecture 02e ODP import passed strict Jotdown validation and native parsing. Its
  source table parsed back as one native table, and split-run DNA sequences retained prime marks
  and restriction-enzyme cut markers.
- The permanent offline suite passed 1,869 tests, including CLI routing, import boundaries,
  pyflakes, typing, security, support-directory, root-script-budget, shebang, and link checks.
- One-time migration evidence passed for public help and eight-deck lint, representative Marp and
  Djot ODP builds through the same CLI, both native-layout PPTX-to-ODP-to-PDF E2Es, and the retained
  folder-build wrapper. The first sandboxed ODP attempt lacked `ps` access; the same command passed
  with the established LibreOffice preflight permission.
- The one-time eight-deck legacy-corpus acceptance and reproducibility gates passed: 378 source
  slides yielded 336 visible and 42 hidden slides, 167 reachable assets, 72 bounded source regions,
  96 review slides, and 186 image occurrences. References resolved only to files with no missing or
  extra assets, symlinks, or exact-full regions; an independent private regeneration reproduced the
  Djot, report, and asset corpus.
- One-time native acceptance passed: strict lint covered 8 decks, 336 visible slides, and 186 image
  occurrences; `build_slides.sh genetics`, both explicit native E2Es, and sequential `--format all`
  exports passed. Every deck retained matching PPTX, ODP, and PDF counts, editable text/direct images,
  and Lecture 02e retained its native table.
- Before the CLI-boundary migration, the permanence-audited suite contained 1,914 tests, including
  all hygiene checks. The two native PPTX-to-ODP-to-PDF E2Es also passed as one-time evidence. M5
  animation acceptance remains unclaimed only pending attended Impress playback.
- The permanence audit removed static CSS, tunable geometry and catalog assertions, redundant broad
  importer and topology proofs, and the duplicate native E2E. Focused behavior and safety tests
  remain, alongside two explicit native-chain runners for one-time acceptance.
- Converted backend tests to direct native-model construction or Djot fixtures. Retired tests whose
  only subject was Marp parsing, front-matter discovery, old class modifiers, or duplicate E2E
  migration proof; added permanent `.md` rejection, imported-table round-trip, and raw-run
  character-preservation tests.
- Removed the permanent CLI assertion for the retired `--to` flag because it was one-time migration
  proof rather than a current behavior boundary.
- Updated human guidance from the superseded front end to Djot for canonical source, build flow,
  layout slots, `md2pptx` borrowing, raw-markup avoidance, component-image wording, and normal local
  tooling. Removed obsolete guidance for the old parser, compatibility baseline, class-size option,
  theme workflow, survey work, and pre-selection naming decision.
- Recorded the instructor's test-triage and bytecode-cache guidance. An explicit `py_compile`
  diagnostic created two `__pycache__` directories despite `PYTHONDONTWRITEBYTECODE`; both were
  removed, and subsequent Python verification used `source source_me.sh` without explicit bytecode
  compilation.
- The final documentation refresh ran the current permanent offline suite: 1,689 passed.
