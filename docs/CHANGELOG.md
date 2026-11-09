## 2026-11-09

### Additions and New Features

- Add seven short curated teaching-purpose decks and a visual authoring index in
  [../exemplars/README.md](../exemplars/README.md). Preserve course context in
  lightly polished copies, keep verified original artwork in deck-owned local folders, and document
  source headings, teaching rationale, alternatives, adaptations, and historical logistics.
  Link the collection from the root README and authoring overview; retain the canonical table-style
  demonstration. Independent rendered review and integration are tracked separately.

- Add themed native table presets, whole-cell and table formatting overrides, measured padding,
  selective borders, and coordinated question/answer column sizing. Publish
  [slide-specs/TABLE_AUTHORING_GUIDE.md](slide-specs/TABLE_AUTHORING_GUIDE.md) and the maintained
  [../exemplars/table_styles.djot](../exemplars/table_styles.djot) demonstration for editable ODP
  and ODP-derived PDF output. Reconcile 424 physical teaching tables (421 existing plus three
  restored), separately from the 14-table demo; preserve all 96 repaired source tables and clear
  59 target markers while retaining 37 non-table blockers. Record native edit/save/reopen,
  rendered comparison, source/hash evidence, and verification limits in the dated
  [native table results](archive/native_table_styles_results.md). Verify 53 normal course ODP/PDF pairs plus the separate 14-page demo; retain 16
  table-only fallback contexts in two blocked consumers. Final integration review is pending.
  Raw ODP import now preserves every supplied valid source column proportion,
  including equal and near-equal widths; curated course tables and accepted outputs
  were unchanged. All 93 changed raw snippets preserve source facts, cell lines,
  scripts, and spans, with maximum ratio error 1.039e-6. Two regressions, 50 importer
  checks, and six selected security/typing/style gates pass. The final base suite
  reports 4,380 passed, three failed, two warnings, and 109 errors in 24.86s; the
  failures and setup errors trace to inherited Biotechnology LECT10 parse conflicts,
  and no new table-code tests failed.

- Consolidate authoritative slide guidance into `docs/slide-specs/COLOR_GUIDE.md`, `VOICE_GUIDE.md`, and
  `PEDAGOGY_GUIDE.md`. Preserve recorded preferences and useful teaching examples, distinguish
  instructor instructions from observed habits and inherited recommendations, and adapt the BPQ
  material to slide teaching. Keep the older style guide as a layout/typography overview, remove
  the superseded methods guide, and link authoring and review docs directly to the specifications.
- Convert Genetics LECT12, LECT13, and LECT1X into 17 canonical Djot decks with local assets,
  per-folder source maps, and conversion reviews. Preserve all 642 original content slides
  and their hidden status; add 45 opening/closing slides. Build 796 editable ODP slides and
  760 visible PDF pages, retaining 307 explicit `@replaceme` slides for difficult conversions.
- Convert Genetics LECT11 into five canonical Djot decks with local assets, source maps,
  and a completed conversion review. Retain all 253 original B-E content slides and their
  hidden status; add objectives and closing summaries. Build 320 editable ODP slides and
  302 visible PDF pages, retaining 62 explicit `@replaceme` slides for difficult conversions.

### Fixes and Maintenance

- Keep seven exemplar gallery WebPs and reuse the existing table screenshot; delete the other
  61 slide previews. Publish the compact gallery and link all 68 authored slides to their Djot
  source definitions instead of individual preview files.
- Archive seven completed root-level planning and review documents and seven completed exemplar
  review reports from `docs/active_plans/` in `docs/archive/`; update inbound and relative links.
- Move the announcement guide, authoring overview, visual rubric, Djot syntax, and SVG diagram
  contract into `docs/slide-specs/`, naming the overview `AUTHORING_GUIDE.md`. Add a short README
  index and update inbound and relative links, including course reviews and archived plans.
  Keep vendored palette/contrast references at their managed paths; retain no compatibility files.
- Review all 460 current replacement-marked slides against rendered diagnostics and mapped
  source pages. Recommend the existing native-table import path as the largest bounded repair
  target: 96 affected slides, compared with 69 artwork-composition candidates. Record the
  per-slide findings in [replaceme_impact_review_2026-11-09.md](archive/replaceme_impact_review_2026-11-09.md).
  Clarify that a composed figure has one artwork image and associated labels that may extend
  outside it; slide titles, captions, and explanatory prose remain native.
- Extend that review with a source-table feature census: 61 of the 96 slides use selective
  borders, 40 have colored cells, nine have horizontal merges, and none has vertical merges.
  Identify selective cell borders as the strongest new table feature; fills, horizontal spans,
  column proportions, and shared column sizing already exist.
- Split former Genetics LECT1X into LECT14 (allele frequencies and Hardy-Weinberg) and
  LECT15 (evolution, selection, drift, and inbreeding), with four B-E decks in each.
  Renumber covers and move original inputs, local assets, includes, and review/source maps
  together. Rebuild 362 authored slides and 361 PDF pages; retain all 136 replacement markers.
  Keep the existing December 8 cover date because the schedule assigns no Lecture 14/15 dates.
- Prepare December 1/8 announcements from the latest current-year deck and matching prior-year
  sources, with current quiz/homework/final dates and shared groups. Retain LECT1X's eight
  separate population-genetics variants and document the supplied folders' schedule mismatch.
- Compare every visible original content page with diagnostic renders. Mark missing tree,
  chromosome, table, and mask relationships; restore basic superscripts and readable colored
  definitions. Record temporary import fallbacks and unresolved work in each lecture review.
- Prepare 2026 Lecture 11 announcements from the latest current-year material and matching
  prior-year lecture, using shared groups and current assessment dates. Record the schedule's
  content/date mismatch and keep the early weather snapshot hidden. Describe this usual
  two-source starting point briefly in the announcement guide and human guidance.
- Review paired original/diagnostic renders, restore the colored GMO comparison columns,
  clear verified color-only deletion-walkthrough flags, and retain markers for missing
  diagram geometry, labels, source reveals, or readable fit. Preserve the original ODP/PDF.

### Developer Tests and Notes

- Slide-specification relocation: 1,384 Markdown link, ASCII, and whitespace checks pass.
  Verify all five old paths are absent, fenced examples are unchanged, and all six local heading
  links in the specification folder resolve. Full suite and slide exports are not repeated for
  the documentation-only move.
- Remove the superseded teaching-methods pointer and record the pre-production preference for
  direct contract/caller updates over compatibility scaffolding. All 143 Markdown link checks
  pass after cleanup; `git diff --check` is clean.
- Slide-specification documentation checks: 1,386 link, ASCII, and whitespace checks pass.
  Direct review confirms the five consolidated documents are ASCII and their 11 local heading
  links resolve; a five-slide temporary formatting example passes project Djot lint. Base suite:
  4,237 passed, 3 failed, 109 setup errors, all failures/errors tracing to existing Biotechnology
  LECT10 parse problems in unchanged sources. No fresh slide exports or classroom validation.
- Replacement-impact review reconciles all 460 physical markers and per-slide findings, with
  no reviewed source/code drift after the sync warning. Documentation checks: 801 passed,
  2 failed on missing links in the separate question pedagogy/voice guides. No production
  behavior changes; the full base suite and attended playback are not rerun for this review.
- LECT14/15 native lint and all-format LibreOffice builds pass. All 353 non-cover PDF pages
  retain identical teaching text, and original input/media hashes and hidden flags reconcile.
  Reviewed the eight updated covers and sampled minor differences in text rendering. Base suite:
  4,051 passed, 3 failed, 87 errors in the pre-existing Biotechnology LECT10 edits.
- LECT12/13/1X strict native lint and all-format LibreOffice builds pass; authored/hidden/PDF
  counts and replacement watermarks reconcile. Base suite: 4,043 passed, 3 failed, 87 errors
  from the existing Biotechnology LECT10 conflicts. All original ODP hashes remain unchanged.
  Attended playback and classroom validation remain unperformed.
- Strict native lint and all-format LibreOffice builds pass for LECT11; source/ODP/PDF
  counts and replacement watermarks reconcile. Base suite: 4,041 passed, 3 failed,
  87 errors in existing Biotechnology LECT10 working-tree edits, which remain untouched.
  Attended Impress playback and classroom validation were not performed.

## 2026-11-05

### Additions and New Features

- Add `docs/TALKING_POINT_DECK_RECIPE.md` for recurring Biotechnology talking-point builds:
  input authority and inventory, annual-source merging, topic maps, cohesive chapter files,
  local copyrighted assets, scientific verification, supported tools, rendered review, and handoff.
  Link it from usage, the conversion checklist, and the documentation map; restore the supported
  image-area audit instructions and replace the checklist's obsolete podcast launcher command.
  Verify 1,010 focused documentation checks, direct recipe link/ASCII/size checks, and shell
  syntax for all nine command examples; independent documentation review finds no material issues.

### Fixes and Maintenance

- Center subsection titles and replace the short underline with matching full-width top/bottom
  stripes, preserving the theme's bilateral symmetry and distinct chapter-frame treatment.
  Update the existing transition regression to check centered titles and mirrored stripe geometry.
  Rebuild Biotechnology 10A/10C and Genetics 09A/10A, inspect both course hues, reconcile
  unchanged PDF counts, and pass 1,312 focused checks.

- Restore the contact slide's original four colored options and nested response details,
  including the purple anonymous-form prompt. Remove the retired Gmail warning and make
  the email address an italic clickable mailto link; retain native hanging bullet indents.
  Balance the options in two panels, rebuild, and inspect PDF page 12. Verify hyperlink/italic
  and native hanging-list geometry; native lint and 1,201 focused checks pass.

- Restore Biotechnology's three-slide classroom Zoom group: course link/headphones, display
  name during class, and name before joining. Keep the shared fragment course-specific,
  document the guide exception, and refresh name-changing steps against official Zoom help.
  Rebuild 10A (44 authored / 8 hidden / 36 PDF), inspect all three restored pages, verify the
  resolved class hyperlink, and pass native lint and 1,201 focused checks.

- Enrich the Set5 science deck with fourteen student-source figures across gene therapy,
  genome editing, stem cells, and cancer. Preserve the instructional prose and native workflows;
  replace three repeated/less-specific figures and add nine dedicated diagram pages. Update
  topic page maps for the 244-page deck and retain image provenance/local copyright exclusions.
  Reject misleading diagrams during review; replace the delivery backdrop and aptamer mismatch
  with actual LNP/SELEX figures. Inspect all sixteen changed PDF pages, reconcile ODP/PDF counts,
  verify original prose and ignored assets, and pass native lint plus 1,201 focused checks.

- Add a Veridian Dynamics subsection before the Lecture 10A Machines slide. Distinguish
  subsections with smaller left-aligned titles and a short underline; retain centered framed
  section dividers. Extend the existing transition regression to protect shape and alignment.
  Rebuild Biotechnology 10A/10C and Genetics 09A/10A; inspect Veridian, chapter/topic divider
  examples, and pass 1,311 focused checks. Biotechnology 10A now has 33 visible pages.

- Give all four shared course-detail slides nested bullet hierarchy and colored topic emphasis.
  Pair BCHM 355/455 with the instructor-supplied LibreTexts textbook cover; retain course
  content and listing details, cite the image, and keep its binary local and ignored. Rebuild
  all three consumers, inspect twelve revised detail pages, and pass native lint and 1,197 checks.

- Apply the instructor-supplied Course Finder listings to shared upcoming-course slides:
  correct the lecture start to 2 p.m., add lab meeting details, exact Spring/Summer session
  dates, section numbers, CRNs, and credits. Preserve the expanded teaching descriptions.
  Rebuild Genetics 09A/10A and Biotechnology 10A, inspect fifteen course pages, verify all six
  CRNs in each PDF, and pass strict native lint and 1,196 focused checks.

- Correct the Company Vision Report (Form) deadline to November 19: submitting the form is
  selecting the group project, not a separate December 3 milestone. Update announcements,
  the group timeline, form slide, takeaways, and source guidance; rebuild both affected decks.

- Restore Lecture 10B's original ODP wording, color, hierarchy, forms, rubrics, and instructor
  humor; use the syllabus for current dates. Focus today's 13 visible pages on group formation
  and the vision form, with a December 10 / 50-point presentation preview. Keep 26 future and
  reference pages hidden in the editable 39-slide deck; document source correspondence and
  visibility controls in `biotech/LECT10/djot/GROUP_PROJECT_REVIEW.md`. Rebuild ODP/PDF, inspect
  all 13 classroom pages, validate native syntax and visibility counts, and pass 1,202 focused checks.
- Repair 122 conflict-marker hunks in 18 synchronized worktree files, preserving completed
  lecture/documentation/podcast work and unaffected content. Keep original conflict inputs and
  per-file receipts under `_temp/group_project_restore/`; leave Git staging unchanged.


- Restore substance to the shared individual upcoming-course pages: biochemistry mechanisms
  and molecular-visualization assignments, experimental lab work and analysis, BIOL 301 topics
  and lecture/lab/discussion format, and the film course's screenings, discussion, writing,
  hot takes, and podcast. Keep current logistics and the tentative BIOL 301 teaching assignment.
  Record instructor/catalog sources and preserve descriptions during future announcement updates.
  Rebuild Genetics 09A/10A and Biotechnology 10A; inspect all fifteen affected summary/detail
  pages and reconcile source/ODP/PDF visibility counts. Strict native lint and 1,184 checks pass.

- Skip marked StVC special episodes before selecting the latest regular publication; replace
  Lecture 10A's #38 special with #37 and the playable Bad Cell Day link. Permit the official
  thumbnail CDN through the existing HTTPS host restriction, normalize generic episode titles,
  and cover regular-episode selection and thumbnail-origin validation with focused regressions.
  Rebuild ODP/PDF, inspect the episode slide, verify the game destination responds, and pass
  1,227 focused checks.

- Remove Veridian Dynamics from Lecture 10A's agenda: it closes announcements, not the lecture.
  Use the newly available #9 Machines transcript to give the logo slide its characteristic
  tagline and "we hope" punchline; document transcript use for future announcement updates.
  Rebuild editable ODP/PDF, inspect both changed pages, and verify 899 focused checks and native lint.

- Build November 5 Biotechnology Lecture 10 as canonical Djot, editable ODP, and PDF: 32 visible
  announcement pages, 13 group-guidance pages plus 26 hidden future/reference pages, and 235 science
  pages. Follow the successful Set #4 merge across the six annual student sources and expanded
  instructor ODP, with the instructor's exact 37-topic 2026 list controlling chapter/topic order.
- Update the group transition, current milestone dates and 91-point breakdown; retain detailed
  presentation/business-plan requirements and instructor voice. Confirm Veridian #9, Machines,
  from the local video library. Refresh weather/podcast material and verify registration dates.
- Review rendered pages and source correspondence: enlarge source diagrams, restore omitted
  material, repair figure identities and Djot emphasis, remove student-page screenshots and unrelated
  stock images, verify scientific citations, and retain copyrighted media as ignored local assets.
  Add the topic/source guide, asset provenance, conversion checklist, and validation limitations.
  Verify 1,182 focused checks and source/ODP/PDF visibility counts; review the rendered decks
  and correct total-row contrast in both group-project tables.

- Fix ASCII compliance in the 2025/2026 Biotechnology Lecture 10 talking points: use apostrophes
  for nucleotide primes, spell out beta, and remove decorative emoji while preserving heading text.

- Move the icebreaker catalog and recording-reminder graphic into `evergreen/`, using `git mv`
  for tracked files. Keep the graphic's local ODG/PNG companions ignored; update catalog references
  and document the shared content inventory. Preserve catalog wording and repository-relative provenance.
  Focused checks: 767 passed; two ASCII failures concern Biotechnology Lecture 10
  talking-point text files. Verify moved catalog/SVG bytes and ignored companion status directly.

- Complete the responsibility split beyond the line-limit advisory: separate emitted topology,
  ODP geometry/page extraction, figure/multiple-choice recognition, fitting policy, and table
  measurement. Original emitter/reader/planner/text-measurement modules are now 445/136/242/498
  lines, with direct imports and no compatibility facades.
- Apply the permanent-test checklist to affected repository-owned tests: remove three redundant
  internal-only test functions (four parametrized cases), retain Djot syntax/guideline checks,
  source-content preservation, and import-safety regressions. Add no permanent refactor tests.
  Full suite: 3977 passed, no warnings. One-time physical-plan comparisons match for two real
  decks; remove the temporary comparison input and migration script after verification.

- Archive 15 completed or superseded planning, design-research, and implementation-review
  documents with `git mv`. Remove the redundant native-layout-contract redirect, repair relative
  links and inbound references, and mark snapshots as historical. Retain two active Biotechnology
  Lecture 03 reports; keep their unresolved tasks and deferred image investigation in TODO.

- Refresh README, architecture, file layout, setup, usage, related-project guidance, and agent
  pointers from current code. Audit roadmap, TODO, development, troubleshooting, formats, and
  historical gate guidance; document module refresh commands after launcher removal. Retain
  the existing release-history boundary rather than label unreleased work as a published release.
- Recapture the README's Disease vs. Disorder illustration from current Lecture 01 PDF page 4.
  Replace the PNG with a quality-90 WebP and inspect the final image. The PDF build succeeds;
  existing capacity advisories elsewhere in that lecture remain outside this documentation edit.

- Replace the machine-specific handout provenance path with its filename and course context;
  retain source/export hashes and page metadata. No runtime loader consumes this provenance field.

- Split long importer and layout modules by responsibility: isolate source regions and tables,
  ODP media and table extraction, emitted component flow, mixed-content measurement, and
  source-fact validation. Update direct callers to the owning modules without compatibility
  re-exports. Preserve existing algorithms and test contracts. Full pytest: 3901 passed,
  no warnings; all four original modules are below the 900-line advisory band.
- Exclude deleted Git paths before file-content discovery filters run, preventing collection
  crashes after an unstaged documentation move. Verify the missing-path case directly.
- Remove bytecode caches produced during explicit syntax compilation. Use in-memory compilation
  and the bootstrapped pytest environment for syntax checks.

- Remove the three obsolete `biotech/djot/` Lecture 03 source copies and their obsolete
  assets and import reports. Remove the intermediate `old/djot_assets/` folder at the
  instructor's request rather than retaining another legacy copy. Update old source references.
  Verify all remaining Biotechnology Djot directories are lecture-local; 280 focused
  Djot-link, cover, Markdown-link, and guidance-format checks pass.

- Restore source compliance and test contracts: validate Djot assets locally without tracking
  copyrighted media, use ASCII character references, move reusable refresh/generation commands
  into `slide_lib`, and remove obsolete retired source copies after historical notes are repaired.

- Synchronized shared style guides, tests, and repository support files from the starter template.

## 2026-11-04

### Updates

- Recover the Stump the Vibe Coder flyer from the October 29, 2026, 11:42:22 Time Machine
  backup using `tmutil restore`. Restore `_temp/stvc-flyer/`, the
  `_temp/stvc-next/current-flyer.png` review image, and the final PDF, WebP, builder, assets,
  and three companion regeneration scripts in `output/pdf/`. All 63 restored files match
  the backup byte-for-byte; visually inspect the recovered final WebP. Do not rebuild.

## 2026-11-03

### Updates

- Require `@xmldom/xmldom >=0.9.12` through a root npm override so vulnerable versions are
  excluded from future resolution, not merely absent from today's lockfile. Preserve upstream
  metadata, regenerate the lockfile, and document/test the security minimum. Verify npm audit,
  resolved dependency tree, focused tests, and real MathJax rendering.

- Investigate the Dependabot xmldom alerts: remote main still locks MathJax 4.0.0 and xmldom
  0.9.8, while the existing uncommitted lockfile resolves MathJax 4.1.3 and patched xmldom
  0.9.12. Git history identifies commit `5865733` on November 1 reverting the previously
  corrected lockfile (MathJax 4.1.3/xmldom 0.9.12 back to 4.0.0/0.9.8) during unrelated
  announcement work; the manifest remained correct. No repository script writes the old range.
  Local npm audit reports zero vulnerabilities. Require `@mathjax/src >=4.1.3` in
  agent guidance, installation policy, and HG; add one focused manifest/lockfile regression
  test because agents repeatedly restored `^4.0.0`. Validate math-layout tests and real local
  equation rendering: four focused tests and real fraction/Greek/chemistry renders pass.
  The corrected lockfile must reach GitHub before remote alerts can clear.

- Add `docs/ANNOUNCEMENT_DECK_GUIDE.md` as the practical `lect##a` preparation guide: opening,
  three main sections, flexible textbook placement, assessment order, signup/profile deadlines,
  seasonal announcements, course-specific exceptions, and weekly checks. Keep HG as the human
  guidance record and link the guide from HG, usage, conversion checklist, and evergreen READMEs.
  Check local Markdown links and diff whitespace; no deck content or build changes.

- Add a dated Next Week slide immediately after the agenda in Genetics 08A-10A, using the
  current syllabus schedule for the following week's class events, quizzes, and homework.
  Use assessment overview, Exam, Quiz, then Weekly Assignments; preserve hidden Exam groups.
  Set shared Discord signup/Student Profile deadlines to September 21 in fall and February 14
  in spring. Record that textbook placement and past Exam/Quiz order are flexible, missing
  items may be forgotten, and general announcements normally show one relevant seasonal topic.
  Revise the cross-deck audit to distinguish actual omissions from acceptable seasonal absence.
  Keep club hidden and preserve the Biotech ending. Rebuild 08A-10A and verify lookahead content,
  assessment order, and hidden groups; strict native lint passes.

- Clarify the cross-deck audit: missing recurring items are omissions; Biotechnology retains
  its Veridian Dynamics ending before THE END. Graduating Students is shown only during the
  first two weeks. Hide the mistakenly visible Genetics 03A graduation slide, preserving its
  original text and layout, and document the remaining inventory gaps in the Lecture 09 review.
  Strict lint and ODP/PDF build pass; PDF text confirms graduation is absent. The older 03A
  build reports capacity failures on authored slides 19/66 and small-text advisories on
  23/26/40/43; this visibility-only edit leaves those layouts unchanged.

- Apply the instructor's final three-section announcement hierarchy to Genetics 08A-10A:
  Informational Slides, Course Content, General Announcements; opening title/agenda/weather/
  icebreaker precede sections. Move Course Content before textbook, remove redundant Textbooks
  divider, use subsections for grading/assessments/assignments and general groups, move Quiz
  before Exam, and add a hidden shared Natural Science Club group. Preserve conditional
  visibility and substantive content. Update guidance, decisions, source maps, and reviews.
  Strict native lint and all three ODP/PDF builds pass; verify section inventory and exported
  order, inspect representative dividers. Existing weather-caption advisories remain.
- Audit all 16 lect##a Djot files (14 unique weekly announcement decks, one duplicate copy,
  and one older course introduction). Record missing groups, visibility/order gaps, stale
  seasonal content, and reusable material in the Lecture 09 review. Leave older audited decks
  unchanged beyond the explicitly documented 08A shared-fragment updates. Inventory evidence:
  `_temp/announcement_hierarchy/all_decks.json`.

- Restore the established 09A/10A opening: weather, icebreaker, then YouTube/podcast.
  The instructor clarified that only spring registration needed moving out of course logistics.
  Keep registration/upcoming courses and evaluations at the end. Correct the standing guidance
  and current source maps; rebuild both ODP/PDF pairs and verify exported order.

- Apply the instructor's clarified announcement order in 09A/10A: weather, YouTube/podcast,
  icebreaker, course logistics, then registration/upcoming courses and evaluations before THE END.
  Restore YouTube/podcast to the opening and retain registration at the end; preserve all slide
  content and visibility. Correct ordering guidance/source maps, rebuild ODP/PDF, pass strict
  native lint, and verify the exported opening and closing page order. A concurrent LibreOffice
  export failed to create the 10A PDF; rebuilding 10A alone succeeded.

- Move general announcement groups to the end of Genetics 09A/10A, after course information,
  assessments, and assignments: YouTube/podcast, spring registration/upcoming courses, then
  evaluations before THE END. Preserve the hidden evaluation group and all slide content.
  Keep weather immediately before the icebreaker. Record the instructor's ordering guidance,
  update current source maps/reviews, rebuild ODP/PDF, and verify exported page order.

- Expand shared spring registration with a 2027 course summary and individual slides for
  BCHM 355/455 lecture, BCHM 356/456 lab, tentative BIOL 301 teaching assignment, and summer
  BIOL 383/483 Biology and Ethics in Film. Apply the instructor's updated lecture/lab details,
  carry recurring summer information forward, and omit stale enrollment/session details.
  Keep course codes in the body and shorter titles after visual review found title/body overlap
  on long course titles. Update guidance, shared-group documentation, source maps, and reviews.
  Rebuild 09A/10A ODP/PDF and pass strict native lint; inspect all five new 09A slides and compare
  their text with 10A. Existing weather-caption capacity advisories remain. Evidence is in
  `_temp/upcoming_courses/`.

- Refresh Genetics 09A with both current NWS Chicago stories, "Rain Timing Today" and
  "Four Day Outlook", before the icebreaker. Preserve complete captions and November 3
  citations. Update the manual refresh tool to capture all published tabs and replace the
  saved group on subsequent refreshes; retain validation before writes and immutable images.
  Update guidance, workflow documentation, and the 09A source map. Pass eight focused tests
  and strict native lint; rebuild ODP/PDF and visually inspect PDF 3-4. The deck now has
  47 authored / 33 visible / 14 hidden slides. Caption capacity advisories remain at
  11.25 pt (rain timing) and 15.25 pt (outlook); neither caption clips in the rendered PDF.
  Review images are in `_temp/lect09_weather/`.

### Fixes and Maintenance

- Synchronized shared style guides, tests, and repository support files from the starter template.
- Synchronized shared style guides, tests, and repository support files from the starter template.
## 2026-11-01

### Fixes

- Allow folder builds without Git metadata or a Git executable by falling back to CWD in the
  shell launcher, environment setup, native build root, and shared slide/image resolution.
  Reuse one Python Git-root resolver, preserve include/image containment, add focused Git/CWD
  regression coverage, and document running unpacked projects from their top-level folder.
  Pass 138 focused tests, Python lint, and shell syntax checks. Run the exact Lecture 09 folder
  command in an isolated copy without Git metadata: all eight ODP/PDF pairs build successfully.
  Evidence is in `_temp/no_git_build/`.

- Create root-level `evergreen/` for slides shared across courses. Move spring registration,
  the YouTube channel, and its unchanged image there; update 08A, 09A, 10A, refresh-tool test
  examples, and authoring/source-map documentation. Preserve all wording, layouts, colors,
  visibility, and dated lecture snapshots; retain course-specific groups in `genetics/evergreen/`.
  Pass 24 focused tests and strict native lint; rebuild all three ODP/PDF pairs and inspect the
  shared slides. Normalized compiled plans are unchanged, and both groups also compile with the
  Biotechnology theme. Preserve newly appearing sync-conflict copies, updating only their old
  include paths. Evidence is in `_temp/shared_evergreen/`.

- Add the November 1 NWS Chicago weather story to 09A and 10A as a reminder to refresh before
  teaching. Use the existing refresh tool, `big-image`, the complete caption, and a separate
  dated citation. Rebuild/review both ODP/PDF pairs: each has 46 authored / 32 visible / 14 hidden
  slides, with weather at PDF 3 and registration at 20-21. Preserve all 31 previous PDF pages'
  text and the graphic's aspect ratio. Strict native lint passes; retain the accepted 15.25 pt
  caption advisory. No tool or layout changes.

- Add the shared evergreen spring-registration group to Genetics 09A and 10A. Reuse the
  original biotech registration/advising wording, keep the Registrar and instructor-provided
  Course Finder links, and record the approximate October 15-December 1 display window.
  Each weekly master controls the two-slide group with one hidden flag. Rebuild both ODP/PDF
  pairs, inspect PDF 19-20, verify the original masters are otherwise unchanged and both links
  are clickable, and update source maps/reviews. Each deck has 45 authored / 31 visible / 14 hidden
  slides. Strict native lint and capacity pass; no new typography findings.

- Restore the tetraploidy mechanism in 10D after the polyploid definitions. Compare normal
  division with retention of both daughter complements, reconnect 46,XY to 92,XXYY, and
  distinguish whole-set doubling from ordinary DNA replication. Keep all 62 existing slides
  and the homework examples; update the source map and review for the added slide. Rebuild
  the 63-page ODP/PDF, inspect D8-10, pass clean lint/capacity/typography checks and 18 PDFKit
  point selections, and verify all previous page text and other Lecture 10 decks are unchanged.

## 2026-10-31

### Additions

- Apply the approved Lecture 10 review while retaining its disease focus; reserve deletion
  mapping and translocation segregation for Lecture 11. Add saved Topic 09 practice with worked
  answers, repair labeled karyotype/nondisjunction/testing figures, correct chromosome-count and
  clinical-claim errors, and move nondisjunction before testing. Preserve the HeLa, Brainbow,
  chromosome-2, and disease/discussion stories. Update current source maps and distinguish the
  earlier conversion reports as historical snapshots. Rebuild four ODP/PDF pairs; B52/C24/D62
  have no replacement markers or capacity/title-wrap warnings. Verify 18 native tables, four
  bank keys, and 74 PDFKit point selections; leave the announcement source and generators unchanged.

- Review Lecture 10 against the 18 Topic 09 chromosome-disorder tasks and their generated
  homework banks. Recommend specific practice replacements and identify missing structural-change
  instruction, source-content corrections, and bank issues. Rebuild all four PDFs and review
  132 content pages; preserve the teaching sources and generators. Save findings in the Lecture
  10 review and question samples/hashes under `_temp/lect10_homework_review/`.

- Remove the unused Lecture 08 announcement starter ODP/PDF and extracted assets from
  `genetics/LECT09/`. Keep a verified recovery copy under `_temp/lect09_starter_cleanup/`.
  Record that prior-week A decks supplied in a new lecture folder are temporary starters.
  All eight Lecture 09 masters still compile; slide sources and PDF/ODP exports are unchanged.

- Add the approved twin-spot prediction to 09C as a question and separate worked answer on
  slides 8-9. Follow the starting yellow/singed alleles through one specified crossover and
  chromosome-separation pattern into two patch phenotypes. Keep all 17 existing slides and
  artwork, use native editable text/table content, and update the 19-page map and research notes.
  Rebuild/review ODP/PDF, pass strict lint with clean capacity/typography checks, confirm the
  answer with a chromatid model, and pass eight PDFKit selections including both answer rows.

- Move the weather slide's NWS credit, retrieval date, and complete source URL into `@citation`.
  Keep the full forecast in `@caption` and reserve the existing citation footer. Update the
  generator, caption/citation tests, and documentation. Pass 79 focused tests and the real PDF
  export regression; rebuild/review the sample and verify all four caption/citation selections.
  The caption fits at 15.25 pt with the accepted 18 pt advisory; all 29 existing pages are preserved.

- Add a manual NWS Chicago weather-story refresh tool with preview/`--write`, an immutable
  original PNG, complete native forecast caption, visible source/date, and one replaceable
  slide before the icebreaker. Validate downloads and every insertion point before saving.
  Give long `big-image` captions extra room downward, preserving image geometry and citation
  clearance. Keep caption text in a native frame and its rounded panel on the master to fix
  real LibreOffice wrapping/clipping and preserve selection. Add focused offline tests and
  a real caption-export regression, and document the near-lecture workflow. Verify a live
  story on a disposable 09A copy: 30 visible pages, 29 existing pages' text preserved,
  original PNG bytes/proportions intact, and four PDFKit caption selections passing.
  Pass 132 focused tests and one real LibreOffice caption regression. The sample caption
  is readable at 15.75 pt; retain its accepted 18 pt capacity advisory. Real lecture sources
  are unchanged by this implementation; the forecast is saved only in the demonstration.

- Add four section/subsection dividers to 09C, marking the twin-spot mechanism, genotype
  change, cell-growth experiments, and repair explanation. Preserve all 13 existing slides
  and artwork; update the 17-page map, catalog, and research report. Review the instructor's
  local textbooks for twin-spot homework, identify Brooker's linked-marker exercise, and
  draft a small-step fly example with an answer key and source qualifications. Rebuild/review
  ODP/PDF, verify content preservation, and check divider text selection.

- Select the robot-chores icebreaker for Genetics 09A: "What everyday task would you
  permanently hand over to a robot?" Include concrete examples, add it to the reusable
  collection, and rebuild/review the announcement deck's ODP and PDF.

- Restore 09C's original story: linked-gene crossing over, the same kind of exchange in a
  body cell, twin spots, and patch growth. Move the short DNA-repair explanation after the
  examples; explain that breaks can arise naturally during ordinary cell activity. Keep all
  13 slides and figures, the five researched additions, both segregation outcomes, and the
  cancer/research connections. Use concrete headings and plainer prose; refresh notes and sources.
  Rebuild ODP/PDF, inspect all pages, verify unchanged artwork and other decks, and pass
  strict lint with clean capacity and typography reports.

- Add 14 conceptual section/subsection dividers across Lecture 09B-H, bringing 09B from
  two to six dividers and 46 to 50 slides. Separate expected doubles, interference, map meaning,
  tetrad classes, crossover correction, and worked mapping stages. Retain 09D's two existing
  breaks. Preserve all teaching slides, data, artwork, and question/answer sequences; refresh
  current page ownership, catalog, and the section review. Rebuild/review six decks, pass
  strict lint and clean typography audits, verify all 199 prior slides and 152 asset/data files,
  and retain only the eight existing 09B table-capacity advisories. All new titles fit one line.

- Refresh 09H's five generator-based ordered-ascus figures with the instructor's updated
  artwork. Preserve image proportions, align pair brackets to current spore bounds, and
  keep all fixed patterns/counts and the 15 cM solution. Add colored opening definitions
  for spore/ascospore, ascus, FDS, and SDS; update the 28-page inventory and artwork provenance.
  Rebuild ODP/PDF and inspect the definitions, figures, and retained teaching sequence.

- Refine 09G's pairwise tables with static unused-gene covers and a persistent gold outline
  for Set 6, the 702-tetrad parental reference. Highlight its contribution across all three
  PD sums and add a full-page preview from the instructor-edited handout. Preserve data,
  cumulative classifications, results, and 42-slide inventory. Update the shared pair-focus
  reminder and rebuild F/G; inspect the export and verify masks, proportions, and classifications.

- Revise 09E/F/G for homework-matched class colors and readable answers. Split E6 into
  static question/answer slides, enlarge labels, color definition terms and all formulas/
  substitutions, and replace old yellow asci beside retained crossover mechanisms.
  Repair per-letter SVG positioning and inherited image stretch; enlarge F/G table answers.
  Keep unlinked TT later as taught material; remove incorrect not-covered footers from covered recaps.
  Preserve all fixed data, arithmetic, and gene-order results; rebuild/review 30/24/42 pages
  and verify colors, artwork, equations, labels, existing tests, and clean audits.

- Revise 09D from 14 to 17 slides: split Products of Meiosis with all original prose intact,
  add two topic dividers, and reuse a genuine homework ascus on two concept slides.
  Repair the imported horizontal stretch in all three mating figures, preserve the original
  artwork bytes and labels, and enlarge each stage. Explain cell/nuclear fusion and the
  homework allele symbols. Rebuild ODP/PDF, review every page, and verify image proportions,
  genotype identity, source preservation, strict lint, the cover test, and clean audits.

- Expand 09C from seven to twelve slides with five primary-research-backed additions:
  repair templates, loss of heterozygosity, clonal patches, an RB1 second hit, and twin-spot
  experiments. Add three original SVG diagrams, DOI citations, and a source/assumption ledger.
  Keep the original fly examples, clarify repair timing and frequency, and update bookends,
  page ownership, and the course catalog. Validate SVGs and segregation outcomes, pass strict
  lint and the existing cover test, and inspect all twelve exported pages; no capacity or
  typography findings remain. Preserve other lecture sources.

- Replace 09B's three reference problems with a second fixed generated homework example.
  Keep F-W-P at 20% interference; add A-J-E practice with 7,000 offspring, 70 observed
  versus 280 expected doubles, 25% coincidence, and 75% interference. Preserve the homework
  table/colors and reveal the solution in small steps. The deck now has 46 pages, eight
  native table states, four local roadmaps, and a closing comparison of the two examples.
  Verify both answers and table data, 13 focused tests, strict lint, and the exported pages;
  update the source map and explicitly record the instructor-requested removals.

- Implement the homework-matched Lecture 09B interference plan: 44 visible slides, one fixed
  F/P/W bank problem, five native homework-table states, and a local five-step roadmap.
  Explain the probability/count/expectation/coincidence/interference bridges and preserve all
  three older datasets as reference problems. Save original bank HTML/item/data/provenance.
  Correct source arithmetic, outside-pair labels, and chromatin interpretations; enlarge the
  retained context figures. All 23 preceding slides have recorded dispositions.
  Verify all four datasets, strict lint, 13 focused tests, zero typography findings, and
  matching ODP/PDF counts. Visually review all 44 pages; eight 19/19.5 pt table advisories
  are readable. Keep other decks and original presentations unchanged.

- Plan a homework-matched Lecture 09B interference sequence using one fixed F/P/W numeric
  bank example: 54 observed versus 67.5 expected doubles, giving 20% interference. Keep
  lecture-only support files local, preserve older examples as references, and specify
  equation bridges, source-error repairs, coverage, and export checks before implementation.

- Reorganize Lecture 09 into six focused C-H topic decks, retaining 09B interference.
  Consolidate the unordered derivation, keep all fixed worked examples and calculations,
  teach ordered tetrads last, and map all 152 previous slides to their new owners.
  Repair retained yeast/crossover/centromere diagrams using original figure regions and
  positioned labels. Replace the three-gene genotype-string tables with the actual homework
  table, all three genes visible, plus readable native summaries for calculations.
  Preserve both mixed masters as pre-split retired sources and update the guide and review.

- Reuse the ordered-centromere generator's original shaded eight-spore drawings on five
  LECT09C slides. Save its exact HTML/CSS, embed high-resolution captures in SVG figures,
  and keep set numbers, counts, mitotic-pair brackets, and FDS/SDS reveals as live SVG labels.
  Preserve the six fixed patterns, 500 asci, teaching steps, and 15 cM result.

- Add a whole-table SVG renderer for the fixed two-gene tetrad examples. Reuse existing ascus
  artwork with larger allele labels, preserve live SVG counts/classifications, and replace
  eight text-only working-table instances with four reusable question/classified figures.
  Keep slide prose/equations and the denser three-gene and ordered tables native.

- Add a fixed BPW ordered-tetrad problem to LECT09C: six eight-spore patterns, 500 asci,
  150 SDS asci, and a 15 cM gene-centromere estimate. Add ordered-spore and centromere-origin
  diagrams, a distinct four-step roadmap, progressive native tables/equations, and a closing
  reference. Explain four meiotic products/eight spores and the half-weight. Keep 09B's
  ordered-tetrad introduction and all existing worked problems.

- Add eight small conceptual steps before LECT09C's first map calculation: count recombinant
  spores, estimate hidden double crossovers, derive the NPD weight, and explain normalization
  and cM. Reuse existing asci and keep the explanation visible in the student PDF.

- Replace Genetics LECT09C's old activity examples with fixed BPW linked and unlinked two-gene
  problems followed by a three-gene mapping problem. Add labeled ascus SVGs, native progressive
  tables, a shared colored roadmap, classification reminders, reference slides, and current
  handout instructions. Preserve the retired activity source, original presentations, and handout.

- Convert Genetics Lectures 09 and 10 to eight canonical Djot decks with component assets,
  current 2026 announcements, learning objectives, takeaways, and source maps/review reports.
  Retain original ODP/PDF inputs and explicit replacement markers for unresolved diagrams,
  masks, label placement, reveal behavior, and source-content contradictions.
- Add current in-class tetrad handout instructions; retain prior-year Google Slides links as
  visible outside-class references. Record the instructor's face-to-face/handout guidance and
  replace obsolete Zoom group-quiz wording in the shared Genetics quiz guidance.

### Fixes

- Keep 09G's distance tables fixed across slides 11-15, 20-24, and 29-33 using existing
  bottom-right panels and shared column sizing. Preserve the native tables, class colors,
  counts, equations, and cumulative answers; place the three linkage conclusions below
  their count summaries. Add an unfilled gray page outline to slide 39's full handout preview,
  preserving its original image bytes and proportions. Rebuild ODP/PDF, verify identical
  table geometry and unchanged teaching content, and inspect all 16 changed pages.

- Apply the cover's background-master fix to bookend, definitions, reference, section,
  subsection, and THE END decoration. Remove redundant fills from transition/end outlines,
  retain course backgrounds and editable slide text, and move citation backing bands into
  the theme. Extend the fast cover regression across all seven framed layouts and two themes.
  Reproduce the original macOS PDF point-selection failure and verify corrected text selection.
  Pass 115 focused tests, two real cover round-trip tests, and 125 PDFKit selections; rebuild
  all 12 Lecture 09/10 deck pairs and visually review 46 framed pages. Preserve slide sources
  and the existing Lecture 10 draft-layout findings.

- Separate reviewed image-free drawings with a `.drawn.svg` suffix and reject nested image
  elements during shared SVG validation. Rename 31 drawings without changing artwork bytes;
  update references and table-builder outputs. Keep ordinary SVGs ignored and retain only
  15 explicit original-generator capture exceptions. Stop tracking 38 other image-bearing SVGs
  while keeping them locally. Verify ignore behavior, references, byte preservation, and focused
  tests; leave exported slides and earlier Git history intact.

- Move the ordered/unordered tetrad roadmaps from Genetics evergreen into Lecture 09 and
  update all seven active includes. Reserve evergreen for content used across courses or
  more than one week; preserve the retired master as historical source evidence. Verify
  all 143 slides are unchanged and strict native lint passes for the eight Lecture 09 masters.

- Verify the six new Lecture 09 decks (7/14/29/24/42/27 slides): 143 reviewed PDF pages,
  matching ODP counts, zero repair markers, 21 passing focused tests, and no new-deck
  typography findings. Keep the 19.25 pt yeast context slide; replace the old three-gene
  table sizing warnings with large homework tables and readable count summaries.

- Rotate older day blocks into `CHANGELOG-2026-10a.md` and `CHANGELOG-2026-10b.md`, keeping
  the two newest days active. Verify every entry and date block is preserved exactly.

- Remove the superseded 390-tetrad worked sequence from LECT09B. Clarify observed recombination
  versus corrected map distance, distinguish class proportions from counts, and show complete
  normalization in the count-based formulas. Preserve the conceptual and ordered-tetrad content.

- Preserve nested prose bullet indentation when exporting equation-adjacent paragraphs as
  independent ODP frames. Extend the existing math export regression test; 40 focused tests pass.
- Restore native tetrad tables and editable LaTeX derivations after expanding merged cells in
  a temporary import copy. Reconstruct two interference figures with original artwork and live
  SVG labels; move long reading URLs to citations or full-width panels. Imports and exports use
  the external LibreOffice path; no original presentation is overwritten.

## 2026-10-28

### Additions

- Create a standalone US Letter Stump the Vibe Coder office-door flyer in `output/pdf/`.
  The final composition gives the evergreen podcast about 53% of usable page height,
  led by the title, a host episode thumbnail, AI LLM description, Wednesday evening
  livestream invitation, and 2.22-inch YouTube QR. Use Atkinson Hyperlegible Next.
- Recompose the four games as compact white advertisements with vector action scenes,
  solid-filled light-mode wordmarks, readable promotional hooks, and clean colored
  1.06-inch QR codes. Remove center logos from game codes. Compare independent cover
  and two-thumbnail concepts, then select a refined single-thumbnail composition after
  independent visual review. All five QR destinations decode at 200 and 300 dpi;
  physical print scanning remains untested. Final review artifacts are in `_temp/stvc-next/`.
- Restore Dr. Voss' portrait and personal invitation in the podcast section, using the
  human's wording to emphasize people experimenting together and inviting viewers to join
  live. Retain the dominant podcast headline and existing podcast/game proportions.
- Replace the cartoonish episode thumbnail with the more photographic StVC 36 Bad Cell
  Day hosts and enlarge the main QR to use available space beside the portrait.
- Regroup the podcast into title/invitation, description, and livestream sections after
  comparing two upper-page compositions. Independent review prefers the horizontal
  grouping; reduce the thumbnail to 160 by 90 points and move the 2.22-inch QR alongside
  the livestream invitation. Preserve the game section pixel-for-pixel; all five QR
  destinations decode at 200 and 300 dpi after recomposition.
