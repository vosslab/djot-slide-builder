# Lecture 09 Review

## November 3 next-week lookahead and seasonal rules

Add a dated Next Week slide at PDF 3, immediately after the agenda, using the current local
Genetics schedule for class events and work due. Use assessment overview, hidden Exam, Quiz,
then Weekly Assignments. Keep three main sections and conditional seasonal groups. Shared
signup/profile reminders now state September 21 in fall and February 14 in spring. Counts:
55 authored / 39 visible / 16 hidden. Build ODP/PDF outside the sandbox; strict native
lint passes. Verify lookahead placement, assessment order, visibility, and PDF text. Inspect the
new lookahead slide. Existing weather caption advisories remain. Evidence is in
`_temp/announcement_hierarchy/`; earlier counts/page numbers below are historical.

## Cross-deck announcement inventory

Reviewed all 16 `lect##a` Djot files: 14 unique weekly announcement decks, the duplicated Biotech
03A source, and the older Genetics 01A course introduction. Missing recurring items are omissions,
not evidence that the instructor wanted a different template. This is a source/inventory review,
not a visual rebuild of every older deck. Current Genetics 08A-10A hierarchy changes are covered
below. Full per-slide inventory: `_temp/announcement_hierarchy/all_decks.json`.

### Gaps in other weekly decks

Missing items often reflect forgotten material, but seasonal absence is appropriate. Lack of
weather in older snapshots does not warrant adding today's forecast. Textbook placement and
historical Exam/Quiz order vary; neither is a correctness finding. Use the preferred current
assessment sequence (overview, Exam, Quiz, Assignments) going forward.

| Decks | Items worth checking or carrying forward |
| --- | --- |
| Genetics 03A | Graduation was visible after its first-two-weeks window and is now hidden. Older hidden seasonal text contains stale dates. |
| Genetics 04A | All icebreakers hidden; Student Profile reminders still visible after September 21. |
| Genetics 05A | No icebreaker; first-week profile material remains visible after September 21. |
| Genetics 06A | No icebreaker. |
| Genetics 07A | No registration group despite October 20 falling in its display window. |
| Genetics 08A | No registration group despite October 27 falling in its display window. No historical weather snapshot; do not invent one. |
| Biotech 03A (both copies) | First-week profile reminder correctly visible before September 21; seasonal groups correctly hidden in September. Hierarchy can be aligned when reused. |
| Biotech 04A | Student Profile remains visible after September 21. Seasonal groups need carrying forward if this deck is used as a later starter. |
| Biotech 05A/06A | No visible Discord server reminder, only hidden completed signup. Completed signup/profile visibility is appropriate. |
| Biotech 07A | No icebreaker; October 15 registration remains hidden and course-promotion slides are placeholders. |
| Biostatistics 08A | No contact-method overview; October 21 registration is absent. Preserve tutorial, graduate, and project-specific content. |

Genetics 01A is an older course introduction, not a weekly template. Missing evaluation slides
in midsemester decks and missing graduation slides after the first two weeks are not display
failures. Hidden reusable groups are useful, but do not show every seasonal group every week.

### Retain the course-specific exceptions

- Biotechnology ends with Veridian Dynamics, then THE END. Do not replace or relocate that
  special ending while completing the common announcement structure.
- Graduating Students appears only in the first two weeks. It is not missing from later decks.
  The visible Genetics 03A copy carried a September 2025 deadline; hide it instead of promoting
  stale dates. Rebuilt 03A and confirmed graduation is absent from PDF text; strict lint passes.
  That old deck reports existing layout capacity issues on authored slides 19/66 and small-text
  advisories on 23/26/40/43; those surfaces were not edited. The older Genetics 01A introductory
  copy remains unchanged.
- First-week signup/profile assignments remain hidden after their deadlines in current decks.
- Old Zoom/preassigned-group quiz setup differs from the current in-class/self-formed groups.
  Reuse only after updating that procedure, not by copying the old slides unchanged.
- Biotech talking marks, news presentations, and evaluation-linked business-plan time are
  course-specific; do not substitute Genetics quiz rules or final-exam extra-time wording.
- Older hidden registration/evaluation slides contain stale years, dates, and course placeholders.
  Refresh them before showing; use the corrected shared registration course group for upcoming
  lectures.

## November 3 three-section hierarchy

Use Informational Slides, Course Content, and General Announcements as the three main sections.
Title, agenda, weather when present, and icebreaker precede them. Move Course Content before
the textbook, remove the redundant Textbooks divider, and use subsection dividers for grading,
Quiz/Exam, Quiz, Exam, Weekly Assignments, registration, evaluations, and club. Quiz precedes
the hidden Exam group. Preserve evaluation visibility and add the hidden club group at the end.
Counts: 54 authored / 38 visible / 16 hidden. Build ODP/PDF sequentially outside the sandbox and pass strict
native lint. Verify the three major sections and exported order; visually inspect representative
dividers. Existing weather caption advisories remain. Evidence: `_temp/announcement_hierarchy/`.
Earlier page numbers below are historical.

## November 3 clarified announcement order

Preserve the original opening; only registration needed moving out of logistics: weather PDF 3-4, icebreaker PDF 5, YouTube/podcast PDF 6-8,
then course logistics at PDF 9-30, and registration/upcoming courses at PDF 31-37.
Evaluations remain hidden before THE END. Content, counts, and visibility are unchanged.
Rebuild ODP/PDF, pass strict native lint, and verify exported page order from PDF text in
`_temp/announcement_order/`. Earlier page numbers below are historical.

## November 3 upcoming courses

Expanded the shared registration group with a spring/summer 2027 summary and individual slides
for BCHM 355/455 lecture, BCHM 356/456 lab, tentative BIOL 301 teaching assignment, and
BIOL 383/483 Biology and Ethics in Film. Use the instructor's updated lecture/lab details
and recurring summer format; omit historical enrollment counts, links, and exact session dates.
The deck has 52 authored / 38 visible / 14 hidden. New course slides are PDF 23-27.
Rebuilt ODP/PDF outside the sandbox and passed strict native lint. Reviewed the five new slides
in 09A; the same shared source supplies 10A. Earlier counts and page numbers below are historical.
Review artifacts are in `_temp/upcoming_courses/`.

## Weather story reminder

Added the November 1 NWS Chicago Five Day Outlook at PDF 3, immediately before the icebreaker,
using the existing refresh tool. The original PNG, full native caption, and separate dated NWS
citation are saved locally; builds do not fetch a new story. Refresh before teaching with
`source source_me.sh && python3 launchers/refresh_weather.py genetics/LECT09 --write`.

09A now has 46 authored / 32 visible / 14 hidden slides. Registration moves to PDF 20-21;
the earlier registration-only review below retains its previous page numbers. All 31 previous
PDF pages retain their text, and removing the weather block restores the previous source exactly.
Rebuilt ODP/PDF, inspected the weather page, and verified the PNG proportions and clickable NWS
link. Strict native lint passes. Keep the accepted 15.25 pt caption capacity advisory; typography
findings remain limited to the unchanged office-hours runt, now PDF 9. Evidence is in
`_temp/weather_announcements/`. Impress playback was not checked.

## Spring registration evergreen

Added the shared `evergreen/spring_registration.djot` group on November 1: PDF 19 is
the divider and PDF 20 keeps the original biotech reminder, with the Registrar and instructor's
Course Finder links. The weekly include is visible; show this seasonal evergreen roughly
October 15 through December 1. At that stage, 09A had 45 authored / 31 visible / 14 hidden slides.
Removing the single new include reproduces the entire previous master exactly.

Rebuilt ODP/PDF outside the sandbox and visually inspected both new pages. Strict native lint
and capacity checks pass; the new pages have no typography findings. The unchanged contact slide
at PDF 8 retains its office-hours runt advisory. Both links are clickable in the PDF. Evidence is
in `_temp/spring_registration/`. Impress playback was not checked.

## Announcement starter cleanup

The copied `lect08a-2026_announcements.odp` and PDF were starters for 09A, not Lecture 09
content. Removed those unused copies and `assets/lect08a-2026_announcements/`; no current
Djot source references that extraction. The current weekly source uses the shared evergreen
slides. Recovery copies and hashes are in `_temp/lect09_starter_cleanup/`. The original
input inventory below is historical and does not require retaining these starter files here.
All eight Lecture 09 masters compile after cleanup. Slide sources and existing PDF/ODP
exports are byte-identical, so no export rebuild was needed.

## 09G table sizing and handout frame

Use the existing one-plus-two-panel layout on G11-15, G20-24, and G29-33. The bottom-right
distance table has its own slot and a shared table group, keeping its position, column widths,
row heights, and text size constant throughout all three pairwise calculations. Keep each
linkage conclusion below the left-hand count summary so the sums remain readable above the
distance table. All wording, data, equations, colors, and cumulative answers are preserved.

G39 shows the same complete handout capture inside a thin, unfilled gray page outline.
The SVG embeds the original WebP bytes at their natural proportions. It is explicitly reviewed
as an image-bearing handout wrapper rather than labeled as an image-free drawing.

Strict native lint, capacity, and typography checks are clean. Source/ODP/PDF retain 43 pages.
All 15 tables have identical compiled geometry, font size, and exported ODP frames. Every
PDF page retains its words and numbers; all 16 changed pages were visually inspected. The
three class sums use separate paragraphs to avoid bullet-induced wrapping. Evidence is in
`_temp/09g_layout/`. No renderer changes, new dependencies, or permanent tests are needed.
The existing table-sizing and decoration regressions pass in 17 focused cases. Physical
projection, Impress playback, and the full unrelated test suite were not checked.

## 09C story and plain language

09C now has 19 slides, including the prediction problem and answer on C8-9. Retain the instructor's linked-gene
crossover to body-cell crossover to twin-spot story. Both original illustrations are at C6-7,
patch growth at C10, and the short repair explanation at C17. The genotype change, cancer,
and research examples are at C12, C13,
and C15. Additional dividers are C5, C11, C14, and C16.
Breaks can arise during ordinary cell activity; a lab treatment is not required. Repair can lead
to an exchange. Use concrete headings and explain terms after
their examples. See [LECT09C_RESEARCH.md](LECT09C_RESEARCH.md) for current sequence and sources.
The research report identifies Brooker's simple twin-spot prediction exercise. The original
yellow/singed version is now in the teaching deck, with a separate native answer table.
Specify one exchange between the centromere and both genes after copying, recombinant
chromatids in opposite daughters, and two X chromosomes retained per daughter. The answer
connects each genotype to its patch and explains why neither a new mutation nor chromosome
loss is needed. All 17 preceding slides and figures remain intact and in order.
Source/ODP/PDF agree on 19 visible pages; strict lint, capacity, and typography checks are clean.
The new pages and their transition were visually inspected, the genotypes match a chromatid
model, and eight native PDFKit selections pass including both answer rows. Other Lecture 09 sources and
artwork remain byte-identical. Evidence is in `_temp/09c_twin_spot_problem/`. Classroom playback
and the full unrelated test suite were not checked.

## Current conceptual section breaks

Add 14 section/subsection dividers across B-H; D keeps its existing two. Current counts are
B50, C19, D17, E34, F25, G43, and H31: 219 slides, including 28 dividers. C-H total 169.
The four extra 09C dividers respond to its frequent topic changes.
That divider-only revision preserved the teaching slides and their order. Current page numbers are in
[LECT09_SOURCE_MAP.md](LECT09_SOURCE_MAP.md); the dated revision accounts below retain their
earlier inventories. See [LECT09_SECTIONS_REVIEW.md](LECT09_SECTIONS_REVIEW.md) for the new breaks
and verification.

## 09H current artwork and opening terms

That revision brought 09H to 28 slides, with definitions at H3 and five refreshed generator-based figures.
Keep all six patterns/counts and the 15 cM result. At that revision, C-H totaled 153 pages.
See [LECT09H_REVIEW.md](LECT09H_REVIEW.md) for the artwork, page changes, and checks.

## 09E/F/G color and readability

That revision brought 09E to 30 pages, including a separate static classification question/answer pair.
09F/09G then retained 24/42 pages. Use large class answers, colored definition terms and equations,
homework-shaped ascus outcomes, and repaired SVG lettering. Keep the unlinked TT mechanisms
later in the deck as taught material; remove misleading reference footers from covered recaps.
All fixed data and calculations are preserved. At that revision, C-H totaled 153 pages.
See [LECT09EFG_REVIEW.md](LECT09EFG_REVIEW.md) for page changes, figure/data contracts, and checks.

## 09D meiosis and figure revision

The instructor approved a two-slide split of Products of Meiosis, one or two section dividers,
undistorted yeast figures, and generator-style ascus artwork. The deck grows from 14 to 17
visible slides: dividers at D4/D12, split teaching content at D5-6. All original bullet prose,
cover metadata, photographs, life-cycle figures, and bookends remain.

The imported mating bitmaps had unequal x/y scales (about 1.20 horizontal stretch).
Rebuild D9-11 with the same embedded artwork bytes, equal scaling, and live labels; focus
on one large stage per slide. Earlier states remain on preceding slides. Two short native
sentences distinguish cell fusion, separate haploid nuclei, and formation of a diploid nucleus.

D6/D14 use set 3 of the fixed three-gene example: ++c, +bc, a++, ab+. Reuse the generator's
actual sac, four spores, allele colors, and labels, adding ascus/ascospore callouts. The key
distinguishes mutant/wild-type symbols and schematic colors from observed pigmentation;
spore positions do not encode meiotic order. Provenance, dimensions, and hashes are in
[lect09d_figure_sources.json](assets/lect09_tetrad_concepts/lect09d_figure_sources.json).

- [x] Confirm every original bullet survives the split and all other lecture sources are unchanged.
- [x] Check original art bytes, exact SVG/ODP proportions, PDF within 0.3% export precision,
  and the four-spore genotype multiset. The inherited 20% horizontal stretch is removed.
- [x] Pass strict native lint, the existing cover test, and the typography/capacity audits.
- [x] Export only 09D through the repository CLI outside the sandbox. Source/ODP/PDF agree at 17 pages.
- [x] Inspect all 17 final pages, including full-size mating and ascus figures. No replacement markers remain.
- [x] Refresh page ownership, catalog, human guidance, decisions, and changelog.

Evidence: `_temp/yeast_update/` contains the baseline, checks, export logs, inventory, and
quality-90 review WebPs. Physical projection/pacing and Impress playback are untested.
No build-engine or generator code changes, new dependencies, or permanent tests are added.

## 09C mitotic crossover expansion

Add five researched teaching steps, bringing 09C from seven to twelve visible slides:
DNA-repair templates, LOH without chromosome loss, clonal patches, an RB1 second-hit example,
and twin spots as a research tool. The source ledger, primary-paper links, figure assumptions,
and rationale are in [LECT09C_RESEARCH.md](LECT09C_RESEARCH.md).

Retain both original twin-spot pages. Clarify repair before the next mitosis, remove the
unsupported universal frequency ceiling, and update objectives/takeaways. Three original
static SVGs keep the new diagrams editable; native DOI citations are visible and clickable.

Strict lint, the existing 09C cover check, SVG checks, both possible segregation outcomes,
and unchanged-other-source checks pass. Source/ODP/PDF agree at twelve pages; all exported
pages are visually reviewed. No replacement markers, capacity concerns, or typography
findings remain. Physical projection/pacing and Impress playback are untested.

The 09B and tetrad records below describe their earlier updates. C-H totaled 153 visible
slides after the 09C-E and 09H updates; the original reorganization had 143.


## 09B two generated examples

The instructor requested removal of the reference problems and a second generated example.
[lect09b-crossover_interference.djot](lect09b-crossover_interference.djot) then had 46 visible pages:
the original F-W-P homework example, unchanged mapping/chromatin context, and an A-J-E practice
example. The previous reference section and all Lz/Su/Gl, A-C-B, and F-G-H questions/answers
are absent from the active deck. The earlier [plan](../../../docs/archive/lect09b_homework_interference.md)
records the superseded 44-page version; the source map records the explicit removals.

### Homework presentation and teaching steps

- Keep the first generated item unchanged: F-W-P, 1,800 offspring, 54 observed doubles,
  67.5 expected, 80% coincidence, and 20% interference. Its visible equation bridges remain.
- Use numeric-bank item 11 from the same interference generator for the second example:
  A/E/J table columns, A-J-E order, 7,000 offspring, parents a+j/+e+, and doubles a++/+ej.
  The observed sum is 47 + 23 = 70. Adjacent probabilities 0.16 and 0.25 predict 280 doubles.
  Coincidence is 70/280 = 25%; interference is 75%, or 3/4. This contrast reinforces that
  coincidence and interference are different answers.
- Save the exact generated question, original HTML, hashes, traits, counts, map, and answer in
  [interference_second_problem_data.json](assets/lect09b-crossover_interference/interference_second_problem_data.json),
  [interference_second_problem.html](assets/lect09b-crossover_interference/interference_second_problem.html), and
  [interference_second_bank_item.txt](assets/lect09b-crossover_interference/interference_second_bank_item.txt).
  The recorded generator revision is the checkout at capture; no historical seed is inferred.
- Preserve all three genes and the original phenotype column, row order, allele colors, counts,
  and totals in eight native table states: five first-example and three second-example uses.
  Keep four local roadmap repetitions. The new comparison uses three columns so its headings
  remain readable. The separate DCO comparison explicitly uses physical A-J-E order.
- Ask for a solution before revealing the parents, doubles, expected count, coincidence, and
  interference on successive slides. Close by comparing the 20% and 75% examples.
  Correct numeric-answer units and outside-pair labels in teaching text, preserving original HTML.

### Verification and limits

- [x] Independently derive both examples from all eight genotype counts using exact fractions;
  verify parental/DCO identities, middle-gene changes, adjacent probabilities, expected counts,
  coincidence, interference, and agreement with the original generated numeric answers.
- [x] Verify every native table phenotype, genotype, count, allele fill, total, and row order.
  Check frozen-item hashes, four roadmap uses, and eight-master discovery.
- [x] Confirm the first example, earlier concept/context content, takeaways, all other lecture
  sources, and existing frozen data are unchanged. Confirm all reference problems are removed.
- [x] Pass strict native lint and 13 focused include/09B cover tests (87 deselected).
  The advisory typography audit has zero findings. Eight readable table advisories remain,
  all at 19 pt, above the instructor's 17 pt review threshold.
- [x] Export only 09B through the repository CLI with LibreOffice outside the sandbox.
  Djot, ODP, and PDF agree at 46 pages, with no authored/rendered replacement markers.
- [x] Inspect the new practice sequence, full-size homework table, comparison table, and closing
  pages. Review the final exported deck; cover text remains selectable and metadata unchanged.
- [x] Update the current page map/catalog, guidance, decisions, and changelog. Original source
  presentations and prior frozen reference data remain historical evidence.

All support files are local to Lecture 09. Builds use saved Djot/data without the BPW checkout
or a browser. Review artifacts and one-time checks are in `_temp/interference_second/`.
Physical projection/pacing and Impress click playback remain untested; answers use separate slides.

The tetrad review below describes the earlier reorganization, when 09B was untouched.
Its old 09B hash statements and initial-conversion findings are historical. The 09B update left other decks unchanged; the later 09C addition is recorded above.

## Six Topic Decks

The approved reorganization replaces the overlapping 62-slide introduction and 90-slide worked
deck with six independently buildable C-H decks. Lecture 09B remains crossover interference.
The six decks originally contained 143 visible slides, then 153 after the 09C-E and 09H updates.
They now total 167 with the conceptual dividers; each has its own cover, objectives, takeaways,
and ending. The two mixed masters were removed after their replacements were accepted.
Earlier full introduction/activity retirements and all original ODP/PDF inputs remain intact.

The ordered and unordered roadmaps live beside the Lecture 09 masters and use local includes.
Their reuse within this lecture does not qualify them as evergreen content. The preserved
pre-split master retains its historical include path.

| Deck | Topic | Slides | Source |
| --- | --- | --- | --- |
| 09C | Mitotic Crossover | 17 | [lect09c-mitotic_crossover.djot](lect09c-mitotic_crossover.djot) |
| 09D | Yeast and Unordered Tetrads | 17 | [lect09d-yeast_unordered_tetrads.djot](lect09d-yeast_unordered_tetrads.djot) |
| 09E | Crossovers and Tetrad Mapping | 34 | [lect09e-tetrad_classes_map_distance.djot](lect09e-tetrad_classes_map_distance.djot) |
| 09F | Two-Gene Tetrad Mapping | 25 | [lect09f-two_gene_tetrad_mapping.djot](lect09f-two_gene_tetrad_mapping.djot) |
| 09G | Three-Gene Tetrad Mapping | 43 | [lect09g-three_gene_tetrad_mapping.djot](lect09g-three_gene_tetrad_mapping.djot) |
| 09H | Ordered Tetrads and Centromeres | 31 | [lect09h-ordered_tetrads_centromeres.djot](lect09h-ordered_tetrads_centromeres.djot) |

### Teaching Ownership and Coverage

- 09C keeps the twin-spot illustrations and adds repair, LOH, mosaics, cancer, and research applications.
- 09D owns yeast mating, haploid/diploid stages, the ascus, and four meiotic products.
- 09E owns observed PD/NPD/TT versus NCO/SCO/DCO histories, independent assortment,
  linkage expectations, recombinant-spore counting, and the unordered distance derivation.
  Keep the newer small count-based steps. The original NCO estimate and mean-crossover
  identity are retained as reference using counts, including the normalization by N.
- 09F applies the method to the existing linked and unlinked two-gene datasets. It uses
  a short formula reminder rather than repeating the derivation.
- 09G retains each pair's classification, linkage decision, arithmetic, distance, and the
  middle-gene reasoning. Handout instructions, all prior-year links, and both videos remain.
- 09H comes last. It connects Neurospora meiosis/mitosis and centromere segregation to the
  existing FDS/SDS problem and half-weight. The distinct probability tree and ws/ws+ example
  remain as labeled reference material. The random-ordering assumption is stated explicitly.

Every one of the previous 152 visible slides has an action and a destination in
[LECT09_SOURCE_MAP.md](LECT09_SOURCE_MAP.md). Repeated section headings and mixed-deck
bookends are superseded; duplicate derivations/diagram builds are merged, with unique
content retained. Repeated roadmaps and applying the same method to three pairs are
intentional teaching practice. Earlier prose, meaningful emphasis, and all worked answers
are preserved while captions and transitions reflect their new context.

### Homework Table Presentation

The former 09C pages 37-43 and their A-C/B-C counterparts no longer show stripped-down
genotype strings. Classification uses the actual table generated by
`tetradlib.make_progeny_html_table`: four separate spore boxes, all A/B/C loci visible,
three pair-classification columns, and the original counts. The exact generator HTML,
source hash, row data, capture geometry, and state meanings are recorded in
[three_gene_homework_sources.json](assets/lect09c-tetrad_worked_examples_bpw/three_gene_homework_sources.json).

Four SVG figures share one high-resolution, quality-90 table capture. Class labels remain
live SVG text. States show no answers, A-B completed, A-B/A-C completed, and all pairs completed.
Six question/answer slide uses preserve the original Set 4, Set 3, and Set 1 matching questions.
The completed table also serves as the closing reference. Count order and table geometry
stay fixed; neither alleles nor earlier classifications disappear when the selected pair changes.

The full table needs space. Classification slides show it large; the following 15 native
working tables summarize classified sets or class totals for sums, linkage, and equations.
This prevents the homework table from shrinking into unreadable print beside calculations.
The cumulative native distance table still updates at each pair result. All figures are
saved inputs; normal slide builds invoke neither BPW nor Chromium. The existing two-gene
SVG utility retains its original scope and CLI.

### Diagram Repairs

Nine original figure regions restore the three yeast-mating states, independent-assortment
labels, the six crossover cases, a labeled centromere, and the ordered segregation mechanism.
Their source pages, crop coordinates, and live text counts are in
[figure_sources.json](assets/lect09_tetrad_concepts/figure_sources.json).
Native labels, leaders, and arrows remain SVG text/paths around original bitmap artwork.
The image data is encoded as quality-90 WebP with explicit xlink references and one simple
figure clip for LibreOffice. This repairs the initial export's missing embedded images;
whole-slide rasterization is not used. One clipped source heading is reconstructed as live text.
The twin-spot comparison keeps its three phenotype panels and labels, moves the biological
caption to native Djot, and removes the baked textbook figure identifier.

Retained marker-bearing source slides are repaired or superseded by the corresponding
clean figure/definition/explanation; all six new decks have zero replacement markers.
The unused original source assets and all source presentations remain recoverable.
Construction references are the SVG skill corpus's biological illustration Clarity section
and Mastering SVG's viewBox section; source biology comes from the original lecture figures
and the previously verified problem records.

### Verification

- [x] Reconcile all 152 previous slides and all 143 current visible slides with the source map.
  Both retired mixed masters are byte-identical to their pre-split snapshots; announcements
  and interference sources are byte-identical to the starting versions.
- [x] Run strict native lint: eight master decks, 209 authored slides including the unchanged
  announcement inventory, and 78 image uses. Included chapters are not standalone decks.
- [x] Pass 21 focused renderer/include/cover tests. Check all six new covers directly;
  retain native, extractable title metadata and the existing Chapter 8/date values.
- [x] Independently classify each dataset using the supplied parents and exact rational
  arithmetic. Preserve 20 cM and 18% RF for the linked example, 49.8% RF for the unlinked
  example, the 10/15/24 cM estimates and reversible B-A-C order, and the 15 cM centromere result.
- [x] Verify the complete homework table, all 72 classification cells across four SVG states,
  six large question/answer uses, and 15 native three-gene count summaries. Check all 31
  saved SVGs for static embedded resources, valid dimensions, and unique IDs.
- [x] Inspect every visible PDF page in 26 quality-90 contact sheets, with full-size checks
  of dense tables, fractions, and repaired figures. Recheck corrected image embedding,
  the native twin-spot caption, the complete segregation headings, and visible-gene prompts.
  Each new ODP/PDF pair agrees with its source count; no new deck has a replacement marker.
- [x] Preserve gene/class colors and the shared rainbow roadmaps: five unordered and two
  ordered uses. Check progressive classifications and cumulative pair distances.
- [x] Finish with no typography findings in C-H. The only new-deck capacity advisory is
  the former 09D page 4 at 19.25 pt; the later approved split removes this advisory.
  The former three-gene small-table advisories are eliminated. Existing A/B typography and
  replacement findings remain outside this reorganization.
- [x] Update documentation, current page ownership, historical source links, and the changelog.
  Preserve original presentations, the handout, and all prior-year/video URLs.

Evidence is in `_temp/tetrad_topics/`: `source_checks.json`, `output_inventory.json`, strict
lint/audit/test/build logs, original-diagram comparisons, and final WebP review images.
C-H use slide advances for question/answer states. Live classroom projection and pacing,
and the unchanged interference deck's click playback, remain untested. No build-engine or
problem-generator changes, new dependencies, or additional permanent tests are introduced.
