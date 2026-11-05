## 2026-11-05

<<<<<<< Updated upstream
### Fixes and Maintenance

=======
### Additions and New Features

- Add `docs/TALKING_POINT_DECK_RECIPE.md` for recurring Biotechnology talking-point builds:
  input authority and inventory, annual-source merging, topic maps, cohesive chapter files,
  local copyrighted assets, scientific verification, supported tools, rendered review, and handoff.
  Link it from usage, the conversion checklist, and the documentation map; restore the supported
  image-area audit instructions and replace the checklist's obsolete podcast launcher command.
  Verify 1,010 focused documentation checks, direct recipe link/ASCII/size checks, and shell
  syntax for all nine command examples; independent documentation review finds no material issues.

### Fixes and Maintenance

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
  announcement pages, 23 group-guidance pages plus 16 hidden rubric/reference pages, and 235 science
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

>>>>>>> Stashed changes
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
