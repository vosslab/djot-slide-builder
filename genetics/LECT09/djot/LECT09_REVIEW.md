# Lecture 09 Review

## 09C story and plain language

09C still has 13 slides. Restore the instructor's linked-gene crossover to body-cell crossover
to twin-spot story; move both original illustrations to C5-6, patch growth to C7, and the short
repair explanation to C11. Keep the genotype change, cancer, and research examples at C8-10.
Natural DNA breaks and experimentally induced damage are distinct; repair is a route to an
exchange, not the opening reason for teaching it. Use concrete headings and explain terms after
their examples. See [LECT09C_RESEARCH.md](LECT09C_RESEARCH.md) for current sequence and sources.

## Current conceptual section breaks

Add 14 section/subsection dividers across B-H; D keeps its existing two. Current counts are
B50, C13, D17, E34, F25, G43, and H31: 213 slides, including 24 dividers. C-H total 163.
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
They now total 163 with the conceptual dividers; each has its own cover, objectives, takeaways,
and ending. The two mixed masters are preserved with a pre_split.djot.retired suffix.
Earlier full introduction/activity retirements and all original ODP/PDF inputs remain intact.

The ordered and unordered roadmaps live beside the Lecture 09 masters and use local includes.
Their reuse within this lecture does not qualify them as evergreen content. The preserved
pre-split master retains its historical include path.

| Deck | Topic | Slides | Source |
| --- | --- | --- | --- |
| 09C | Mitotic Crossover | 13 | [lect09c-mitotic_crossover.djot](lect09c-mitotic_crossover.djot) |
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

## Pre-Split Records (Historical)

### Current Tetrad Replacement

The active 09C is [lect09c-tetrad_worked_examples_bpw.pre_split.djot.retired](lect09c-tetrad_worked_examples_bpw.pre_split.djot.retired):
90 visible slides, five included teaching chapters, six uses of the shared unordered roadmap,
two uses of the ordered roadmap, seventeen SVG assets, and no authored or automatically added
replacement watermarks. The instructor
approved fixed examples and then requested an additional unlinked two-gene problem and
small conceptual bridges into the equations in his teaching voice. He then requested an ordered
gene-centromere problem and confirmed that the unordered centromere extension is unnecessary.

| Active Deck | Authored / Visible | Replacement Markers |
| --- | --- | --- |
| Announcements | 43 / 29 | 0 |
| Crossover interference | 23 / 23 | 9 |
| Tetrad introduction (09B) | 62 / 62 | 17 |
| BPW tetrad worked examples (09C) | 90 / 90 | 0 |

The former activity Djot is preserved as
[lect09c-tetrads_2_activity_format.djot.retired](lect09c-tetrads_2_activity_format.djot.retired).
The complete introduction conversion is also preserved as
[lect09b-tetrads_1_introduction.djot.retired](lect09b-tetrads_1_introduction.djot.retired).
Original ODP/PDF inputs and old assets remain untouched. Folder discovery selects four master
decks, excludes the retired files, and folds the five teaching chapter files into 09C.

#### Fixed Examples and Answers

Exact unordered counts, generator calls, seeds, genotype multisets, class labels, and the source
revision are recorded in [problem_data.json](assets/lect09c-tetrad_worked_examples_bpw/problem_data.json).
The ordered example is recorded separately in
[ordered_problem_data.json](assets/lect09c-tetrad_worked_examples_bpw/ordered_problem_data.json).
The BPW generator checkout is read only. Ordinary slide builds use the saved Djot/SVG source.

| Problem / Pair | Total Tetrads | PD | NPD | TT | Result |
| --- | --- | --- | --- | --- | --- |
| Two genes A-B; parents ++ / ab | 1,000 | 650 | 10 | 340 | Linked; 20 cM; observed RF 18% |
| Two genes D-E; parents ++ / de | 1,000 | 402 | 398 | 200 | Unlinked; observed RF 49.8% |
| Three genes A-B; parents a++ / +bc | 1,200 | 995 | 7 | 198 | 10 cM |
| Three genes A-C; same cross | 1,200 | 905 | 13 | 282 | 15 cM |
| Three genes B-C; same cross | 1,200 | 704 | 16 | 480 | 24 cM |

The three-gene answer is B-A-C or C-A-B. Its adjacent map intervals are 10 and 15 cM, summing
to 25 cM. The separate B-C estimate remains 24 cM; the deck explicitly distinguishes these
values. The unlinked example stops at the linkage conclusion, without applying the linked-gene
map correction. The given cross defines parental combinations, including for rare tetrad sets.

#### Teaching and Visual Review

- Start with definitions and a linked two-gene problem; then contrast an unlinked cross before
  introducing three genes. Repeat one canonical six-step rainbow roadmap six times with black
  titles and matching colored step references. Preserve gene-color and class-color meanings.
- Present large labeled asci, then use SVG two-gene/ordered classification tables and native
  three-gene tables. Keep the compact ordered summation/substitution tables native.
  During each three-gene pair,
  display only the selected pair and keep all set numbers/counts stable. Add a matching reminder
  for every pair. Reveal classifications, sums, substitutions, fractions, and results in successive
  slides; update the native results table after each completed pair.
- Close with middle-gene reasoning, a proportional interval map, a full-genotype classification
  reference, the formula reference, handout instructions, and takeaways. Retain all three old
  Google Slides links as visible references with year labels. The existing handout is unchanged.
- Reuse the approved `genemap_art.asci` artwork. Preserve geometry and genotype multiplicities;
  enlarge labels and draw their white halos behind separate live foreground text because
  LibreOffice does not reliably honor `paint-order`. Review actual exported SVG labels and colors.
- Use compact SVG two-gene tables with larger allele labels and one-line totals. Use separate
  fixed panels for three-gene explanations and results so they do not
  overlap. The initial 67-page sequence was visually reviewed, including equation states and links.
- In 09B remove the old analysis divider and five numeric-example states (source 28-32 and 51).
  Retain the conceptual and ordered-tetrad sequence. Correct the RF/map distinction, complete
  count normalization, identify class proportions in the derivation, and express its final
  proportion-to-cM conversion explicitly. Review all seven revised mathematical slides.

#### Conceptual Equation Bridges

Pages 11-18 add eight small steps before the first map calculation; page 19 revises the
formula introduction, and page 22 reinforces the observed-RF versus map-distance distinction.
The added sequence asks students to count recombinant spores in the existing asci, shows
why the RF denominator starts at 4N, and explains how crossovers can be hidden in PD and TT.

The double-crossover table shows the expected PD:TT:NPD shares of 1:2:1. It explicitly applies
only to double-crossover tetrads. The model assumes random chromatid participation and rare
triple or higher crossovers. From DCO = 4NPD and SCO = TT - 2NPD, students see how half the
singles plus the doubles yields half TT plus 3NPD. The next slide explains dividing by N
and multiplying by 100. All class quantities remain counts throughout this bridge.

The three is explicitly identified as a correction weight; an NPD tetrad still has four
recombinant spores. Visible explanations support student review; speaker notes provide
short prompts and teaching connections. Existing genotype drawings, datasets, calculated
answers, the handout, and the introduction are unchanged by this revision.

The derivation was checked against the instructor's existing 09B derivation and
[MIT 7.03 Lecture 9](https://web.mit.edu/7.03/documents/Lecture_9.pdf), pages 2-3.
Review evidence for this addition is in `_temp/tetrad_bridge/`.

#### Ordered Tetrads and Centromeres

09B retains its ordered-tetrad section on pages 47-59: four meiotic products, eight spores
after mitosis, first- and second-division segregation, and gene-centromere mapping. Its five
existing marked diagram conversions on pages 51-55 remain documented draft material.

The new fifth chapter, [lect09h1-ordered_centromere.djot](lect09h1-ordered_centromere.djot),
adds a worked ordered problem on 09C pages 65-78, with a closing formula reference on page 83.
It uses `get_asci_counts(15)` from the instructor's ordered-centromere generator, random seed
309 and `PYTHONHASHSEED=0`. The extra hash seed records the source's set-iteration assignment
of SDS count bins. Ordinary builds use saved Djot/SVG assets and require no generator run.

| Set | Eight-Spores Pattern | Asci | Class |
| --- | --- | --- | --- |
| 1 | ++++aaaa | 188 | FDS |
| 2 | ++aa++aa | 39 | SDS |
| 3 | ++aaaa++ | 44 | SDS |
| 4 | aa++++aa | 30 | SDS |
| 5 | aa++aa++ | 37 | SDS |
| 6 | aaaa++++ | 162 | FDS |

FDS totals 350; SDS totals 150; all asci total 500. The SDS frequency is 30%, and the
single-crossover estimate is half of that, 15 cM from gene A to its centromere. The new
sequence explains why eight spores represent four mitotic pairs, classifies ordered allele
blocks before revealing the answer, sums the SDS rows, and traces centromere origin through
the four meiotic products. Two of those products have recombinant gene-centromere combinations.
This visibly explains the half-weight; no additional factor of eight is used in the denominator.

Use the separate four-step ordered roadmap twice; keep the six-step unordered roadmap and
all previous problems. FDS/SDS remain separate from PD/NPD/TT. The ordered figures preserve
all eight spore positions, distinguish allele symbols from observed pigment, and show an
explicitly schematic genetic map. The asci now reuse the source generator's original artwork,
as described below. The single-crossover model is stated in the visible formula
slides. Pattern rules and the half-weight were checked against
[Furman's ordered-ascus lab guide](https://facweb.furman.edu/~lthompson/bgy30/30sorda.htm).
Construction references: the biological illustration handbook's Clarity section and
Mastering SVG's viewBox section, via the local SVG skill corpus.

The unordered zero-tetratype/centromere extension remains retired by instructor direction;
it is not an outstanding coverage requirement. Existing handout and generator code are unchanged.

#### SVG Two-Gene Working Tables

The three-row linked and unlinked tables now contain complete tetrad drawings in their spore
column. Four reusable SVGs supply question/classified states on pages 7, 9, 10, 20, 21, 26,
28, and 29. Counts, set order, parental combinations, and genotype multisets are unchanged.
The figures retain live SVG text and consistent geometry; slide headings, prompts, and
equations remain native Djot. Allele labels are enlarged to remain readable within each ascus.
The 21 three-gene working tables and two compact ordered working tables remain native.

Rebuild these figures with [render_tetrad_tables.py](../../../tools/render_tetrad_tables.py)
and the saved unordered problem data. The utility checks counts and given-parent
classification, verifies each reused drawing's genotypes, and renders all states before
writing outputs. It uses no BPW import or new dependency. Normal deck builds use the saved SVGs.

Compatibility check: installed python-docx 1.2.0 accepts PNG in a table-cell run, but raw SVG
raises `UnrecognizedImageError`. LibreOffice Writer supports inline graphics and SVG import;
this differs from the Impress exporter used here. In the local Impress probe, a control with
a standalone SVG exported; adding an inline SVG frame to a native table-cell paragraph made
the modified ODP fail to load. This is evidence about that export route, not a claim that all
LibreOffice applications lack SVG support. The whole-table SVG route exports successfully.
DOCX still requires a raster fallback; these figure tables do not have native Impress cells.
See [python-docx's SVG issue](https://github.com/python-openxml/python-docx/issues/659),
[Writer anchoring](https://help.libreoffice.org/latest/en-US/text/swriter/guide/anchor_object.html),
and [LibreOffice's SVG importer](https://docs.libreoffice.org/svgio.html).

#### Verification and Limits

- Strict native lint passes for the final Lecture 09 source tree. It resolves four master decks;
  the included chapters are not standalone covers.
- Independently classify each set against the given parents and sum with rational arithmetic.
  The separate BPW three-gene solver confirms all three distances and the reversible gene order.
  Check all 29 working tables, all six shared-roadmap uses, and the closing classification matrix.
- Twelve include tests and three tracked Lecture 09 cover tests pass. Direct cover-contract
  checks also pass for the new 09C master and revised 09B. Content checks are one-time evidence;
  no permanent tests or reusable generator utility are added.
- The new deck's typography audit has no findings. Its 27 capacity advisories concern 21 working
  tables at 18-18.5 pt and six short prompts at 18.25-19 pt; final PDF review confirms readable
  values, intact genotypes, and no overlapping objects. These are advisory sizes, not lost content.
- The preceding conceptual revision passed strict native lint and the same 15 focused tests. All 29
  working tables and four linked-pair calculations retained their verified answers. Its 75-page
  ODP/PDF counts agree; new pages 11-18 and revised pages 19 and 22 were visually inspected,
  including full-size checks of the double-crossover shares and coefficient derivation.
  The other 65 pages retain identical extracted text. All new bridge slides fit without
  capacity advisories, and its typography audit had no findings. Those checks,
  renders, and arithmetic evidence are saved in `_temp/tetrad_bridge/`.
- 09B retains its earlier conversion issues: 17 authored replacement markers, with three long
  title warnings and two runt warnings in retained content. The source map gives their current
  positions. This introduction remains a reviewed conversion draft.
- Both current decks have matching ODP and PDF page counts (62 and 90), with selectable cover
  metadata. The new worked sequence uses slide advances rather than click-dependent reveals.
  Existing 09B animation playback and physical classroom projection remain untested.
- The ordered addition passes strict native lint and all 15 focused include/cover tests.
  Independently check run-length classification, the four identical mitotic pairs, all four
  new working tables, and the 150/500 half-weight calculation; compare the generator's answer
  formatter. The 29 earlier unordered tables retain their verified values. Both ordered
  roadmaps are identical; five new SVGs parse and preserve the saved pattern order and
  centromere-origin combinations. All 19 added or revised pages were visually reviewed,
  including full-size checks of the data, pattern-table footer, and half-weight diagram.
  The final typography audit has no findings and the 27 capacity advisories are unchanged;
  none concerns the ordered addition. Seventy-one previous pages retain identical extracted
  text; the four changed previous pages expand objectives/takeaways or clarify unordered
  headings. Checks and quality-90 WebP review images are in `_temp/tetrad_ordered/`.

Outputs: `output/odp/lect09c-tetrad_worked_examples_bpw.odp`,
`output/pdf/lect09c-tetrad_worked_examples_bpw.pdf`, and the matching 09B outputs.

The preceding two-gene SVG-table revision passed strict native lint and 17 focused tests, including the renderer's
given-parent/reveal/data-fidelity checks. All four SVG states (12 distinct drawn rows, eight
slide uses) match the saved counts and genotype multisets. The remaining 21 native unordered
tables and four native ordered tables retain their verified data: 33 working-table instances
in total. All eight changed PDF pages were visually reviewed, with page 7 inspected at full
size; the other 82 pages retain identical extracted text. Both output formats retain 90 pages.
The typography audit has no findings and the 27 earlier three-gene capacity advisories remain;
the new figure tables add no recovery markers. Evidence is in `_temp/tetrad_table_svg/`.
Initial review evidence: `_temp/tetrad_bpw/final_review/`, `source_checks.json`, `artifact_checks.json`,
`capacity_detail.json`, native-lint/audit/build logs, and the focused pytest logs.

#### Original Ordered-Ascus Artwork

Pages 66-68 and 70-71 now reuse the exact `generate_html_for_pattern` output from the current
ordered-centromere generator, using `bptools.default_color_wheel(2)`: brown + spores and blue
a spores inside shaded green asci. The source generator already has local artwork edits;
the provenance record includes its source hash as well as the repository revision.
[ordered_generator_art.html](assets/lect09c-tetrad_worked_examples_bpw/ordered_generator_art.html)
preserves the exact six generated HTML/CSS fragments. Capture each at three times CSS size,
check all eight DOM allele labels against the saved pattern, and embed quality-90 WebP
captures in self-contained SVGs. These are artwork captures rather than vector redrawings.

SVG set numbers, counts, class reveals, run-length labels, and mitotic-pair brackets remain
live text/geometry around the original art. The question and classified tables share the
same drawings, counts, dimensions, and set order. The two compact ordered tables, all equations,
roadmaps, and teaching steps remain native and unchanged. Ordinary builds require neither
Chromium nor the BPW checkout. The existing two-gene table utility has its original scope.

The final 90-page ODP/PDF exports agree. All five revised pages were visually inspected,
including the classified table at full size; the other 85 pages retain identical extracted
text. Check all six original DOM patterns and all 18 overview/question/classified figure
rows against the saved sequences and counts, including embedded-image identity. Source
equations and chapter headings are unchanged. All 17 SVGs pass the static component checks.
Strict native lint and 17 focused tests pass; the typography audit has no findings. The 27
existing three-gene capacity advisories are unchanged. Evidence and quality-90 WebP review
images are in `_temp/tetrad_generator_art/`. Classroom projection remains untested.

Checklist actions from the initial conversion remain recorded below. The authorized replacement
supersedes its original one-to-one requirement for worked examples. Equations, tables, colors,
row stability, all visible pages, chapter discovery, retired-source preservation, and outputs
were checked for this revision. Attended playback and classroom projection are unperformed.

### Initial Conversion Record (Historical)

The following inventory, page numbers, replacement findings, and test results describe the
initial conversion before the BPW replacement. Use the current source map for active page numbers.


Reviewed conversion draft, October 31, 2026. Replacement markers are intentional unresolved
conversion or source-content findings; these decks are not yet classroom-ready replacements.
Original ODP/PDF files remain unchanged in the lecture directory.

### Canonical decks

| Djot | Authored | Visible PDF | Hidden | Replacement markers |
| --- | --- | --- | --- | --- |
| [lect09a-2026_announcements.djot](lect09a-2026_announcements.djot) | 43 | 29 | 14 | 0 |
| [lect09b-crossover_interference.djot](lect09b-crossover_interference.djot) | 23 | 23 | 0 | 9 |
| [lect09b-tetrads_1_introduction.djot.retired](lect09b-tetrads_1_introduction.djot.retired) | 68 | 68 | 0 | 22 |
| [lect09c-tetrads_2_activity_format.djot](lect09c-tetrads_2_activity_format.djot.retired) | 53 | 53 | 0 | 24 |

The [LECT09_SOURCE_MAP.md](LECT09_SOURCE_MAP.md) accounts for every source content slide,
all additions, the PDF page correspondence, and announcement include ownership.
Import evidence and extracted components are in `assets/<content-deck>/import_report.json`.

### Input inventory

| Original ODP | Authored | Source-hidden slides | Source animation slides | Source PDF pages |
| --- | --- | --- | --- | --- |
| `lect08a-2026_announcements.odp` | 47 | [23, 24, 25, 26, 27, 28, 34, 35, 36, 42, 43, 44, 45, 46] | none | 33 |
| `lect09b-crossover_interference.odp` | 20 | none | [2, 17] | 20 |
| `lect09b-tetrads_1_introduction.odp` | 66 | none | [51] | 66 |
| `lect09c-tetrads_2_activity_format.odp` | 50 | none | [12, 15, 17] | 50 |

The maintained `genetics/LECT08/djot/lect08a-2026_announcements.djot` is the canonical
announcement model, following the cleaned Biotechnology announcements through the shared evergreen
content. LECT09's original A file is a copy of Lecture 08; LECT10's original A is from 2025.
These are inventory/comparison evidence, not current weekly masters. All content ODPs are authoritative;
the Karyotypes source PDF still says Chapter 6 while the ODP's opening divider says Chapter 9.
Content source PDF pages correspond directly to source slide numbers. Announcement source PDFs
omit the listed hidden slides; their page order is the ascending visible source-slide sequence.

The source outline/order is retained in the source map and import reports. Dividers label the
existing topic boundaries; only an opening divider is added where absent. Both Lecture 09 B
filenames and their original B identities remain distinct; neither is overwritten or renumbered.

### Weekly announcements

Lecture dates: November 3 (09) and November 10 (10), 2026. Dates and assignments were checked
against `/Users/vosslab/nsh/syllabus/site_docs/fall_2026/genetics/SCHEDULE.md`, generated from
[the schedule spreadsheet](https://docs.google.com/spreadsheets/d/1XLZcg8PnW4GyMxFctAKCTvzN9qImIb5S3bK6hyeDz0Q/edit).
Both weeks show quiz guidance: Quiz 3 is Nov 03 and Quiz 4 is Nov 17. Quiz/exam and homework
status colors are relative to the corresponding lecture date. The shared quiz guidance now says "In class and Blackboard" and asks students to form
groups in class, replacing obsolete Zoom/breakout instructions. Opening information and quiz/exam
policies use `repo:genetics/evergreen/` includes. Expired assignments, evaluation slides, and exam
review stay hidden; the evergreen Discord slide remains visible. Private course links retain
`{{course_url:key}}` references. Icebreaker catalog choices: 09 `cooking`; 10 `popular-culture`.

The podcast preview failed because the newest feed publication, special Episode 38, has no
GitHub Pages tool URL. Episode 39 also has no playable link. Retain Episode 37, the latest
feed publication with a confirmed playable project, with a descriptive Bad Cell Day caption.
Both video and game responded HTTP 200. This selection is current as of conversion, not a
prediction of publications before these future lecture dates. The saved thumbnail was inspected.

### Repairs and review findings

- Covers use native selectable text, current dates, and the canonical course chapters:
  Chapter 8 for mapping/tetrads and Chapter 9 for chromosome disorders, verified against the
  [BPW Genetics index](https://biologyproblems.org/genetics/).
- Add source-grounded learning objectives on slide 2 and Key Takeaways immediately before
  THE END in every content deck. Preserve existing summary dividers and teaching sequence.
  New jargon is defined within the source's early instructional slides; no extra glossary is added.
- Preserve colored spans, bold, italics, underline, scientific names, and chromosome addresses.
  Normalize ASCII source with character references and straight quotes. Remove editable textbook
  figure identifiers; identifiers baked into raster artwork remain a documented limitation.
- The import of tetrad introduction failed on merged cells. A temporary ODP copy expanded only
  its table merge attributes; original content and inputs stay unchanged. Restore four-spore
  header merges and total rows in native Djot tables, remove duplicate SVG table previews,
  and retain markers for lost source cell emphasis, overlays, and table fit issues.
- Transcribe the tetrad derivation equations to editable Djot LaTeX, including the activity
  deck's `/total` denominator. Retain the source distinction between proportions and counts;
  do not silently add normalization or change the source's mathematics. Compare the typeset
  fractions and derivation order with the originals.
- Rebuild the interference chromosome figures from one quality-90 WebP artwork inside SVG,
  with live gene/frequency labels and arrows. Keep the surrounding questions native.
  Source 2 retains its marker because its original reveal was not fully reproduced.
- Use existing two-panel layouts for intact interference data images and native explanations.
  Reposition the three PD/NPD/TT diagrams alongside their definitions. Keep unresolved
  masks, lost labels, missing highlights, shrinking tables, and source answer-reveal differences
  explicitly marked, even when the output looks plausible.
- Restore native multiple-choice answer popups for the Karyotypes answer slides. Original
  question-only slides remain question-only; no answer is invented. Nondisjunction source 39
  already imports as multiple-choice. Click playback in Impress was not performed.
- Use footer citations for long single URLs. Two-link reading slides use full-width panels
  because a two-line citation cannot fit the fixed footer. Preserve full clickable URLs.
- A rendering defect blocked equation slides containing nested prose bullets. The shared
  ODP fragment exporter now starts each independent paragraph list locally, retaining its
  measured indentation. The existing math test now covers that regression; 40 focused tests pass.

The instructor clarified that Genetics has met face to face since 2025 and uses handouts.
Add a current handout activity instruction slide; retain all three prior-year Google Slides links
as visible outside-class references with their year labels. No 2026 URL is invented.

Source-content decisions still needed: interference source 6 contains `11.648.5` and says
48.5% interference means "no interference". Source 11's euchromatin definition and source 12's
interpretation of suppressed recombination also need instructor review. Those slides remain marked.
The source's map-distance rounding and older activity examples are preserved.

### Unresolved source slides

For each row, compare the source and diagnostic render; restore the missing geometry, labels,
mask, or instructional emphasis in native Djot or a bounded figure. Keep the marker until that
specific repair has a successful source/render comparison. Source-content contradictions require
the instructor's decision before rewriting. No slide split is proposed or performed.

| Deck | Source | Djot | Import reason / review evidence |
| --- | --- | --- | --- |
| `lect09b-crossover_interference` | 2 | 4 | native annotations could not be assigned to exactly one image; normalized ambiguous topology bounds [NormalizedBounds(left=0.3886071428571429, top=0.06291428571428571, right=0.6288928571428571, bottom=0.1572), NormalizedBounds(left=0.39139285714285715, top=0.18834285714285715, right=0.4502857142857143, bottom=0.23794285714285715), NormalizedBounds(left=0.5628214285714286, top=0.18942857142857142, right=0.6407857142857143, bottom=0.238), NormalizedBounds(left=0.0, top=0.2513714285714286, right=1.0, bottom=0.5355428571428571), NormalizedBounds(left=0.030000000000000002, top=0.7085714285714286, right=0.9700000000000001, bottom=0.8914285714285715)] into one native source-order panel; normalized distributed pictorial annotations into native source-order content; regular text lattice requires border and span reconstruction; source animation for id1 requires review; unsupported source object draw:line requires reconstruction |
| `lect09b-crossover_interference` | 4 | 6 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized single connected materially coupled visual graph into native source-order content; unrecognized source text color #0000cc requires review |
| `lect09b-crossover_interference` | 6 | 8 | Manual visual/content review: inspect the finding below before classroom use. |
| `lect09b-crossover_interference` | 11 | 13 | Manual visual/content review: inspect the finding below before classroom use. |
| `lect09b-crossover_interference` | 12 | 14 | Manual visual/content review: inspect the finding below before classroom use. |
| `lect09b-crossover_interference` | 14 | 16 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; native annotations could not be assigned to exactly one image; normalized ambiguous topology bounds [NormalizedBounds(left=0.3886071428571429, top=0.024857142857142855, right=0.6288928571428571, bottom=0.11914285714285713), NormalizedBounds(left=0.39139285714285715, top=0.15028571428571427, right=0.4502857142857143, bottom=0.19988571428571428), NormalizedBounds(left=0.5628214285714286, top=0.1513142857142857, right=0.6407857142857143, bottom=0.1998857142857143), NormalizedBounds(left=0.0, top=0.21325714285714287, right=1.0, bottom=0.8730285714285715), NormalizedBounds(left=0.381, top=0.5131428571428572, right=0.9797142857142856, bottom=1.0)] into one native source-order panel; normalized distributed pictorial annotations into native source-order content; regular text lattice requires border and span reconstruction; source object crosses physical page bounds; unsupported source object draw:line requires reconstruction |
| `lect09b-crossover_interference` | 15 | 17 | dense text requires post-conversion polish; mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; native annotations could not be assigned to exactly one image; normalized ambiguous topology bounds [NormalizedBounds(left=0.3886071428571429, top=0.024857142857142855, right=0.6288928571428571, bottom=0.11914285714285713), NormalizedBounds(left=0.39139285714285715, top=0.15028571428571427, right=0.4502857142857143, bottom=0.19988571428571428), NormalizedBounds(left=0.5628214285714286, top=0.1513142857142857, right=0.6407857142857143, bottom=0.1998857142857143), NormalizedBounds(left=0.0, top=0.21325714285714287, right=1.0, bottom=0.8730285714285715), NormalizedBounds(left=0.381, top=0.5131428571428572, right=0.9797142857142856, bottom=0.8626285714285715)] into one native source-order panel; normalized distributed pictorial annotations into native source-order content; regular text lattice requires border and span reconstruction; unsupported source object draw:line requires reconstruction |
| `lect09b-crossover_interference` | 17 | 19 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized distributed pictorial annotations into native source-order content; source animation for id2 requires review; source animation for id3 requires review; source animation for id4 requires review; source animation for id5 requires review; source animation for id6 requires review; source animation for id7 requires review; source animation for id8 requires review; source animation for id9 requires review |
| `lect09b-crossover_interference` | 18 | 20 | dense text requires post-conversion polish; mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized distributed pictorial annotations into native source-order content |
| `lect09b-tetrads_1_introduction` | 12 | 13 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized distributed pictorial annotations into native source-order content; regular text lattice requires border and span reconstruction; unsupported source object draw:custom-shape requires reconstruction; unsupported source object draw:line requires reconstruction |
| `lect09b-tetrads_1_introduction` | 13 | 14 | 13 positioned labels require native redesign; dense text requires post-conversion polish; normalized distributed pictorial annotations into native source-order content; regular text lattice requires border and span reconstruction; unsupported source object draw:custom-shape requires reconstruction; unsupported source object draw:line requires reconstruction |
| `lect09b-tetrads_1_introduction` | 14 | 15 | 16 positioned labels require native redesign; dense text requires post-conversion polish; normalized distributed pictorial annotations into native source-order content; regular text lattice requires border and span reconstruction; unsupported source object draw:custom-shape requires reconstruction; unsupported source object draw:line requires reconstruction |
| `lect09b-tetrads_1_introduction` | 17 | 18 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized ambiguous topology bounds [NormalizedBounds(left=0.7277857142857144, top=0.14657142857142857, right=0.8777857142857144, bottom=0.39325714285714286), NormalizedBounds(left=0.018142857142857145, top=0.20674285714285714, right=0.7166428571428571, bottom=0.9666285714285714), NormalizedBounds(left=0.7277857142857144, top=0.4108571428571429, right=0.8777857142857144, bottom=0.6575428571428572), NormalizedBounds(left=0.7277857142857144, top=0.6713142857142856, right=0.8777857142857144, bottom=0.9179999999999999)] into one native source-order panel; unrecognized source text color #00a933 requires review; unrecognized source text color #a1467e requires review; unrecognized source text color #b47804 requires review |
| `lect09b-tetrads_1_introduction` | 20 | 21 | dense text requires post-conversion polish; mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized ambiguous topology bounds [NormalizedBounds(left=0.03257142857142858, top=0.016000000000000004, right=0.9685714285714285, bottom=0.7528571428571429), NormalizedBounds(left=0.02242857142857143, top=0.768, right=0.42635714285714293, bottom=0.9579428571428571), NormalizedBounds(left=0.4895714285714286, top=0.7733142857142857, right=0.9944642857142857, bottom=0.9724571428571428)] into one native source-order panel; normalized distributed pictorial annotations into native source-order content; regular text lattice requires border and span reconstruction; unrecognized source text color #00a933 requires review; unrecognized source text color #b47804 requires review; unsupported source object draw:custom-shape requires reconstruction |
| `lect09b-tetrads_1_introduction` | 27 | 28 | normalized sole material interior overlay label into native source-order content; unsupported source object draw:custom-shape requires reconstruction |
| `lect09b-tetrads_1_introduction` | 29 | 30 | normalized overlapping legacy components into a table-safe native grid; unrecognized source text color #00a933 requires review; unrecognized source text color #8d1d75 requires review; unrecognized source text color #b47804 requires review |
| `lect09b-tetrads_1_introduction` | 30 | 31 | normalized overlapping legacy components into a table-safe native grid; unrecognized source text color #00a933 requires review; unrecognized source text color #a1467e requires review; unrecognized source text color #b47804 requires review; unsupported source object draw:custom-shape requires reconstruction |
| `lect09b-tetrads_1_introduction` | 32 | 33 | normalized overlapping legacy components into a table-safe native grid; unrecognized source text color #00a933 requires review; unrecognized source text color #a1467e requires review; unrecognized source text color #b47804 requires review |
| `lect09b-tetrads_1_introduction` | 35 | 36 | normalized overlapping legacy components into one native source-order panel; source object crosses physical page bounds; unrecognized source text color #00a933 requires review; unrecognized source text color #a1467e requires review; unrecognized source text color #b47804 requires review |
| `lect09b-tetrads_1_introduction` | 38 | 39 | source object crosses physical page bounds |
| `lect09b-tetrads_1_introduction` | 39 | 40 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized ambiguous topology bounds [NormalizedBounds(left=0.026607142857142857, top=0.039999999999999994, right=0.9800357142857145, bottom=0.09948571428571427), NormalizedBounds(left=0.02721428571428572, top=0.09331428571428572, right=0.9706428571428571, bottom=0.9714857142857144), NormalizedBounds(left=0.8850000000000001, top=0.34622857142857144, right=0.9750000000000001, bottom=0.4513714285714286), NormalizedBounds(left=0.8850000000000001, top=0.5970285714285715, right=0.9750000000000001, bottom=0.9341714285714285)] into one native source-order panel; normalized distributed pictorial annotations into native source-order content; regular text lattice requires border and span reconstruction; unrecognized source text color #a1467e requires review |
| `lect09b-tetrads_1_introduction` | 40 | 41 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized ambiguous topology bounds [NormalizedBounds(left=0.026607142857142857, top=0.039999999999999994, right=0.9800357142857145, bottom=0.09948571428571427), NormalizedBounds(left=0.02721428571428572, top=0.08188571428571428, right=0.9706428571428571, bottom=1.0), NormalizedBounds(left=0.8850000000000001, top=0.34622857142857144, right=0.9750000000000001, bottom=0.5445714285714286), NormalizedBounds(left=0.8850000000000001, top=0.5917714285714286, right=0.9750000000000001, bottom=1.0)] into one native source-order panel; normalized distributed pictorial annotations into native source-order content; regular text lattice requires border and span reconstruction; source object crosses physical page bounds; unrecognized source text color #a1467e requires review |
| `lect09b-tetrads_1_introduction` | 41 | 42 | unrecognized source text color #009933 requires review; unrecognized source text color #00a933 requires review; unrecognized source text color #8d1d75 requires review; unrecognized source text color #996600 requires review; unrecognized source text color #b47804 requires review |
| `lect09b-tetrads_1_introduction` | 42 | 43 | mixed text/images cannot fit readability bounds in bottom; split this slide into separate slides or panels; normalized distributed pictorial annotations into native source-order content; regular text lattice requires border and span reconstruction; source object crosses physical page bounds |
| `lect09b-tetrads_1_introduction` | 48 | 49 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized single connected materially coupled visual graph into native source-order content |
| `lect09b-tetrads_1_introduction` | 51 | 52 | normalized overlapping legacy components into a table-safe native grid; source animation for id1 requires review; source animation for id2 requires review; source animation for id3 requires review; unrecognized source text color #00a933 requires review; unrecognized source text color #990099 requires review; unrecognized source text color #a1467e requires review; unrecognized source text color #b47804 requires review |
| `lect09b-tetrads_1_introduction` | 56 | 57 | normalized single connected materially coupled visual graph into native source-order content |
| `lect09b-tetrads_1_introduction` | 57 | 58 | source object crosses physical page bounds |
| `lect09b-tetrads_1_introduction` | 58 | 59 | source object crosses physical page bounds |
| `lect09b-tetrads_1_introduction` | 59 | 60 | source object crosses physical page bounds |
| `lect09b-tetrads_1_introduction` | 60 | 61 | source object crosses physical page bounds |
| `lect09c-tetrads_2_activity_format` | 5 | 6 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized ambiguous topology bounds [NormalizedBounds(left=0.7277857142857144, top=0.14657142857142857, right=0.8777857142857144, bottom=0.39325714285714286), NormalizedBounds(left=0.018142857142857145, top=0.20674285714285714, right=0.7166428571428571, bottom=0.9666285714285714), NormalizedBounds(left=0.7277857142857144, top=0.4108571428571429, right=0.8777857142857144, bottom=0.6575428571428572), NormalizedBounds(left=0.7277857142857144, top=0.6713142857142856, right=0.8777857142857144, bottom=0.9179999999999999)] into one native source-order panel; unrecognized source text color #00a933 requires review; unrecognized source text color #a1467e requires review; unrecognized source text color #b47804 requires review |
| `lect09c-tetrads_2_activity_format` | 6 | 7 | mixed text/images cannot fit readability bounds in bottom; split this slide into separate slides or panels; normalized distributed pictorial annotations into native source-order content; regular text lattice requires border and span reconstruction; source object crosses physical page bounds |
| `lect09c-tetrads_2_activity_format` | 7 | 8 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized single connected materially coupled visual graph into native source-order content |
| `lect09c-tetrads_2_activity_format` | 11 | 12 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized overlapping legacy components into one native source-order panel; normalized single connected materially coupled visual graph into native source-order content |
| `lect09c-tetrads_2_activity_format` | 12 | 13 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized overlapping legacy components into one native source-order panel; normalized single connected materially coupled visual graph into native source-order content; source animation for id1 requires review; unrecognized source text color #b47804 requires review; unrecognized source text color #ff0066 requires review |
| `lect09c-tetrads_2_activity_format` | 13 | 14 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized overlapping legacy components into one native source-order panel; normalized single connected materially coupled visual graph into native source-order content; unrecognized source text color #b47804 requires review; unrecognized source text color #ff0066 requires review |
| `lect09c-tetrads_2_activity_format` | 14 | 15 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized overlapping legacy components into one native source-order panel; normalized single connected materially coupled visual graph into native source-order content; unrecognized source text color #00a933 requires review; unrecognized source text color #b47804 requires review; unrecognized source text color #ff0066 requires review; unrecognized source text color #ff4000 requires review |
| `lect09c-tetrads_2_activity_format` | 15 | 16 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized overlapping legacy components into one native source-order panel; normalized single connected materially coupled visual graph into native source-order content; source animation for id2 requires review; unrecognized source text color #b47804 requires review |
| `lect09c-tetrads_2_activity_format` | 16 | 17 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized overlapping legacy components into one native source-order panel; normalized single connected materially coupled visual graph into native source-order content; unrecognized source text color #073d7c requires review; unrecognized source text color #159d27 requires review; unrecognized source text color #8e306b requires review; unrecognized source text color #a46509 requires review; unrecognized source text color #fc2707 requires review |
| `lect09c-tetrads_2_activity_format` | 17 | 18 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized overlapping legacy components into one native source-order panel; normalized single connected materially coupled visual graph into native source-order content; source animation for id3 requires review; unrecognized source text color #b47804 requires review |
| `lect09c-tetrads_2_activity_format` | 18 | 19 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized overlapping legacy components into one native source-order panel; normalized single connected materially coupled visual graph into native source-order content; unrecognized source text color #ff5429 requires review |
| `lect09c-tetrads_2_activity_format` | 19 | 20 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized overlapping legacy components into one native source-order panel; normalized single connected materially coupled visual graph into native source-order content; unrecognized source text color #8d1d75 requires review; unrecognized source text color #ed4c05 requires review |
| `lect09c-tetrads_2_activity_format` | 29 | 30 | unsupported source object draw:custom-shape requires reconstruction |
| `lect09c-tetrads_2_activity_format` | 30 | 31 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized single connected materially coupled visual graph into native source-order content; source object crosses physical page bounds; unrecognized source text color #00a933 requires review; unrecognized source text color #a1467e requires review; unrecognized source text color #b47804 requires review; unsupported source object draw:custom-shape requires reconstruction |
| `lect09c-tetrads_2_activity_format` | 31 | 32 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized single connected materially coupled visual graph into native source-order content; source object crosses physical page bounds; unrecognized source text color #00a933 requires review; unrecognized source text color #a1467e requires review; unrecognized source text color #b47804 requires review; unsupported source object draw:custom-shape requires reconstruction |
| `lect09c-tetrads_2_activity_format` | 32 | 33 | dense text requires post-conversion polish; mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized single connected materially coupled visual graph into native source-order content; unrecognized source text color #00a933 requires review; unrecognized source text color #a1467e requires review; unrecognized source text color #b47804 requires review; unsupported source object draw:custom-shape requires reconstruction |
| `lect09c-tetrads_2_activity_format` | 34 | 35 | unsupported source object draw:custom-shape requires reconstruction |
| `lect09c-tetrads_2_activity_format` | 35 | 36 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized single connected materially coupled visual graph into native source-order content; unrecognized source text color #00a933 requires review; unrecognized source text color #a1467e requires review; unrecognized source text color #b47804 requires review; unsupported source object draw:custom-shape requires reconstruction |
| `lect09c-tetrads_2_activity_format` | 36 | 37 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized single connected materially coupled visual graph into native source-order content; unrecognized source text color #00a933 requires review; unrecognized source text color #a1467e requires review; unrecognized source text color #b47804 requires review; unsupported source object draw:custom-shape requires reconstruction |
| `lect09c-tetrads_2_activity_format` | 37 | 38 | dense text requires post-conversion polish; mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized single connected materially coupled visual graph into native source-order content; unrecognized source text color #00a933 requires review; unrecognized source text color #a1467e requires review; unrecognized source text color #b47804 requires review; unsupported source object draw:custom-shape requires reconstruction |
| `lect09c-tetrads_2_activity_format` | 39 | 40 | unsupported source object draw:custom-shape requires reconstruction |
| `lect09c-tetrads_2_activity_format` | 40 | 41 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized single connected materially coupled visual graph into native source-order content; unrecognized source text color #00a933 requires review; unrecognized source text color #a1467e requires review; unrecognized source text color #b47804 requires review; unsupported source object draw:custom-shape requires reconstruction |
| `lect09c-tetrads_2_activity_format` | 41 | 42 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized single connected materially coupled visual graph into native source-order content; unrecognized source text color #00a933 requires review; unrecognized source text color #a1467e requires review; unrecognized source text color #b47804 requires review; unsupported source object draw:custom-shape requires reconstruction |
| `lect09c-tetrads_2_activity_format` | 42 | 43 | dense text requires post-conversion polish; mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized single connected materially coupled visual graph into native source-order content; unrecognized source text color #00a933 requires review; unrecognized source text color #a1467e requires review; unrecognized source text color #b47804 requires review; unsupported source object draw:custom-shape requires reconstruction |

### Validation and artifacts

- Strict native lint: all eight sources pass, 362 authored slides across the eight decks (see per-deck counts above; 28 announcement slides are hidden in total).
- Focused renderer tests: 40 passed in `test_math_layout.py`, `test_odp_export.py`, and
  `test_native_export.py`; LibreOffice calls in those tests are mocked. All eight new covers pass
  their focused cover checks. The broader run has 123 passes and one existing failure: the
  unchanged evergreen `three_point_gene_order_steps.djot` fragment is treated as a standalone
  cover by `test_slide_one.py`. No unrelated cover or test source was changed.
- Capacity and typography reports, source inventories, mapped image-area audits, and build logs
  are in `_temp/lect09_10/`. Audit findings are advisory; source wording is preserved for long
  titles and remaining runts. Source text in artwork and table cells is outside typography-audit coverage.
- Every content source page was paired with its converted page for visual inspection. Diagnostic
  ODP/PDF copies in `_temp/lect09_10/diagnostic/` remove only review watermarks for inspection;
  they do not clear canonical markers. Contact sheets are `*_compare_*.webp`. Final edited
  equations, tables, bookends, popups, activity instructions, and citations receive separate previews.
- Image-area audit uses the source map to omit added slides before matching. Edited/composite
  artwork is manually compared. Serious shrinkage remains marked; labels in raster artwork
  remain raster. Some source GDI figures still need label reconstruction.
- Outputs: `output/odp/<deck-stem>.odp` and `output/pdf/<deck-stem>.pdf`, derived through the
  repository LibreOffice path outside the sandbox. See the count reconciliation above.
- Unperformed checks: Impress click playback; physical classroom readability testing; historical
  Google Slides access requiring a student account. A full clinical/scientific fact check is outside
  conversion scope. Replacement markers distinguish the reviewed draft from classroom readiness.

### Final check results

Typography audit: {'runt': 3, 'title-wrap': 7}. No `url-too-wide` warnings remain.

Capacity summary: 40 concerns (mixed-readability=29, paragraph/list=11). Warnings remain documented; no automatic slide splitting is accepted.

- `lect09b-crossover_interference_image_audit`: shrinkage source slides [4, 17, 18]; changed/vector artwork requiring manual matching [2, 14, 15].
- `lect09b-tetrads_1_introduction_image_audit`: shrinkage source slides [12, 13, 14, 15, 19, 20, 27, 31, 37, 39, 40, 42, 48, 58, 59, 61, 63]; changed/vector artwork requiring manual matching [29, 30, 32, 35, 43, 44, 45, 46, 50, 51].
- `lect09c-tetrads_2_activity_format_image_audit`: shrinkage source slides [4, 6, 7, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 24]; changed/vector artwork requiring manual matching [8, 11, 12, 13, 14, 15, 16, 17, 18, 19, 27, 29, 30, 31, 32, 34, 35, 36, 37, 39, 40, 41, 42, 43].

Final outputs reconcile to the authored/visible/hidden counts in the deck table. Covers
contain selectable PDF text. Review preview: `_temp/lect09_10/final_preview.pdf` and
`final_preview_map.json`; the final quiz wording is rechecked in the rebuilt announcement PDFs.

### Conversion checklist

Checked items include documented unresolved findings; they do not certify marker-free output.
N/A: new three-point-testcross roadmaps (these are tetrad/interference and chromosome decks),
Zoom (Genetics has no course Zoom meeting), extra glossary additions, new reveals on static figures,
and clearing every marker. The source's five-step unordered-tetrad procedure is preserved twice;
it is distinct from the LECT08 six-step three-point-testcross roadmap. No new roadmap colors are invented.

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

- [x] Replace the copied agenda with this lecture's topics and activities; compare each agenda
  item with the content decks and current course schedule.
- [x] Check every assessment and assignment date against the schedule/spreadsheet. Update
  relative wording, deadline/status colors, and expired assignment entries for the lecture date.
- [x] Compare announcement visibility with this week's plan. Record every changed hidden flag;
  confirm evergreen Discord information remains even when its signup assignment expires.
- [x] Select the week's icebreaker explicitly from `icebreakers.yaml` or an instructor selection.
  Copy its prompt/examples and remove any stale week/date label; record the selected catalog key.
- [x] Preview the StVC refresh with
  `source source_me.sh && python3 tools/refresh_podcast.py DECK.djot`.
  Inspect the selected episode before applying `--write`.
- [x] Confirm the latest published StVC episode available on the lecture date and use it as the
  default selection. Record the selected episode number; if another episode is more appropriate,
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
- [x] Before a new three-point testcross problem, repeat the matching colored roadmap: the
  pairwise-distance checklist for full mapping, or the DCO checklist for quick gene-order exercises.
  Keep the two methods' step numbering distinct. Use the fixed [COLOR_PALETTE.md](../../../docs/COLOR_PALETTE.md)
  colors in rainbow order, with matching colored step cross-references.
- [x] Remove textbook figure-number artifacts from titles, captions, citations, and editable
  diagram labels. Keep meaningful explanatory captions and all diagram content.
- [x] Inspect every rendered title for single-line fit, following the preference in
  [HUMAN_GUIDANCE.md](../../../docs/HUMAN_GUIDANCE.md). Flag wrapping titles and record proposed shorter
  wording for review; permission to rewrite titles remains separate from checking their length.
- [x] For textbook diagrams assembled from artwork and positioned labels, compare label placement,
  arrows, and diagram relationships with the source. Record whether a labeled image reconstruction
  is a suitable repair; retain the replacement marker until the rendered result is verified.
- [x] Where suitable, use one quality-90 WebP inside SVG with live overlapping labels. Keep titles,
  captions, surrounding prose, and native tables outside the asset. Verify the LibreOffice render
  and review any source reveals separately; a static figure does not certify animation fidelity.
- [x] Preserve source vector figures as vectors with live labels. Restore static diagram highlights
  and masks within their figure, and preserve paint order so hidden answers do not reappear above
  opaque masks. Verify both masked and unmasked regions against the source.
- [x] Check each figure's identity against the source render, including orientation and cropping;
  a plausible diagram or matching subject is insufficient evidence that it is the right asset.
- [x] Distinguish static masks from actual reveal targets using the source ODP. Use an image-relative
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
- [ ] Compare source animation targets/order with the converted reveals. Inspect final PDF states
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
