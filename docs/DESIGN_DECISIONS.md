# Design decisions

### Homework practice in Lecture 10

**Decision.** Keep Lecture 10 focused on chromosome disorders. Use saved Topic 09 examples for
band order, simple karyotype notation, and polyploid counts; add chromosome-shape matching from
the homework term set. Present questions before worked answers. Leave deletion mapping and
translocation segregation for Lecture 11, as the instructor clarified.

**Why.** Students need to connect chromosome pictures and notation with the homework. Replacing
repeated explanation creates room for practice without removing the disease and research stories.

**Consequence.** Store fixed question records locally; normal builds need no generator checkout.
Distinguish schematic band labels from real cytobands, and explain the homework's notation where
it differs from the convention used in class. Teach nondisjunction before testing. Keep detailed
reference material and discussion links, and distinguish a segregation model from live-birth risk.
Repair original figure labels and preserve image proportions. Image-bearing source SVGs remain
ignored; they do not use the reviewed-original-drawing suffix or new tracking exceptions.

**Owner.** [LECT10_REVIEW.md](../genetics/LECT10/djot/LECT10_REVIEW.md) and
[LECT10_SOURCE_MAP.md](../genetics/LECT10/djot/LECT10_SOURCE_MAP.md).

### Manual weather story snapshots

**Decision.** Capture the NWS Chicago page's initially displayed PNG and its complete description
in one `big-image` slide immediately before the icebreaker. Preview by default; save explicitly.
Use the description as native caption text. Put attribution, retrieval date, and source URL in
the separate `@citation` footer, as requested by the instructor.

**Why.** The forecasters choose a useful conversation starter. A local snapshot preserves that
choice for the lecture and keeps normal builds offline. The story's image filename can change.

**Consequence.** Store immutable, content-addressed PNGs beside each selected deck and replace
one managed weather slide. Validate the active story, official HTTPS URLs, image, and every
insertion point before writing. Long captions may grow down into the unused lower margin,
with image geometry fixed and citation clearance preserved. Keep existing font fitting and
accept roughly 15 pt for this use. Tab selection and historical forecast lookup are outside v1.
Downloaded text stays literal Djot; URL admission and redirect validation apply ASVS 2.2.1/1.2.2.
Native caption text sits in a wrapping text frame; its rounded panel is master decoration.
Text directly inside the rectangle ran off-page in LibreOffice despite measured wrapping.

**Owner.** [refresh_weather.py](../tools/refresh_weather.py),
[layout_specialty_builders.py](../slide_lib/layout_specialty_builders.py), and [USAGE.md](USAGE.md).

### Twin spots lead 09C

**Decision.** Restore the linked-gene crossover to body-cell crossover to twin-spot sequence.
Show the original chromosome and fly figures immediately after the introduction. Explain patch
growth before naming loss of heterozygosity; keep cancer and research as extensions. Move the
short repair explanation near the end and use plain language throughout.

**Why.** Starting with repair changed the instructor's story and could make a natural, uncommon
event sound as though it required laboratory damage. DNA breaks can arise naturally, and repair
can lead to an exchange. A DNA break and the exchange that can follow are different steps.

**Consequence.** Retain the 13 existing slides, every figure, all five researched additions, both segregation
outcomes, and the two-copy distinction. Replace acronym-led headings with concrete descriptions.
Keep detailed repair qualifications in teaching notes and the source ledger. Update current page
ownership; earlier section/research verification remains a dated snapshot.
Add four conceptual dividers at the instructor's request, bringing 09C to 17 pages. Mark the
twin-spot mechanism, genotype change, cell-growth experiment, and repair explanation without
reordering or rewriting the existing slides. Add the approved simple twin-spot prediction and
worked answer after the fly illustration, bringing 09C to 19 pages. Specify the exchange and
chromosome-separation pattern; keep optional harder extensions in the research report.

**Owner.** [lect09c-mitotic_crossover.djot](../genetics/LECT09/djot/lect09c-mitotic_crossover.djot)
and [LECT09C_RESEARCH.md](../genetics/LECT09/djot/LECT09C_RESEARCH.md).

### Conceptual dividers in Lecture 09

**Decision.** Add section and subsection slides at changes in the teaching task, using roughly
one divider per ten slides as a pacing guide. Use the existing section and subsection
layouts in the Genetics course hue.

**Why.** Long worked examples need visible transitions between identifying evidence, calculating,
and interpreting results. A useful boundary matters more than exact spacing.

**Consequence.** Add 14 dividers across 09B-H, retaining 09D's existing two. Preserve every
existing slide, its order, figures, colors, notes, equations, and fixed problem data. Update current
page maps and exports; dated review reports retain their earlier page numbers. No new layout,
automatic insertion, or permanent slide-count test is needed.

**Owner.** Lecture 09 sources and
[LECT09_SECTIONS_REVIEW.md](../genetics/LECT09/djot/LECT09_SECTIONS_REVIEW.md).

### Distinguish drawings from SVG image wrappers

**Decision.** Use `.drawn.svg` for reviewed, image-free drawings and allow that suffix in Git.
Keep ordinary `.svg` files ignored by default, with exact-file exceptions for reviewed original
generator captures. Reject `image` and `feImage` elements, including nested ones, in `.drawn.svg`.

**Why.** Folder wildcards admit future imported artwork, while long lists of drawing names
obscure the distinction. Repaired labels or an SVG wrapper do not establish rights to its image.

**Consequence.** Rename 31 reviewed drawings without changing their bytes, update current
references and the two-gene table builder, and retain 15 explicit generator-capture exceptions.
Stop tracking other image-bearing SVGs while preserving local files. Existing validation uses
the same restrictive XML parser (ASVS 1.5.1); the new structural check enforces the declared
format at the shared validation boundary (ASVS 2.2.1). If it fails, use an ordinary ignored SVG
and review image provenance before allowing it. Structure does not establish ownership.
Earlier vector assets and Git history are outside this migration.

**Owner.** [.gitignore](../.gitignore), [svg_images.py](../slide_lib/svg_images.py),
and [SVG_DIAGRAMS.md](SVG_DIAGRAMS.md).

### Current ordered-ascus artwork in 09H

**Decision.** Recapture the generator's updated ascus drawings for the five existing teaching
figures. Add a definitions slide after the objectives for spore/ascospore, ascus, FDS, and SDS.

**Why.** The updated spore shapes, shading, and ascus outline should match the homework.
Defining the sac as well as its spores gives the segregation terms a clear starting point.

**Consequence.** Keep all six fixed patterns and counts, the static question/answer sequence,
and every calculation. Center naturally scaled artwork in the existing rows and measure the
four pair brackets against the new spore bounds. Terms use the existing blue FDS/orange SDS
colors. Record the current working-tree source/function hashes separately from the original
numeric-problem revision. The deck grows from 27 to 28 slides; later pages shift by one.

**Owner.** Lecture 09H and
[ordered_problem_data.json](../genetics/LECT09/djot/assets/lect09c-tetrad_worked_examples_bpw/ordered_problem_data.json).

### Pairwise focus and parental reference in 09G

**Decision.** Add static gray covers over the unused gene in each pair's question/answer
table. Keep Set 6 outlined in PD gold, emphasize its 702 contribution in the native summaries,
and show a complete page of the instructor-edited handout beside the activity instructions.

**Why.** Students need to focus on two loci while retaining the homework table's appearance.
Set 6 contains only the original parental genotypes, so it stays PD for every pair; frequency
does not determine classification. A page preview connects the activity to the actual handout.

**Consequence.** Retain the original embedded table bytes, all counts, earlier classifications,
and an uncovered final reference. Use measured allele-cell bounds for covers. The source
handout remains unchanged; page 2 previews its three-gene problems without cropping or stretching.
Change the shared roadmap reminder to focus on one pair, updating F's two uses as well.
Use the existing one-plus-two-panel layout for G11-15, G20-24, and G29-33: explanations occupy
the top-right slot, and native distance tables share a table group in the bottom-right slot.
Move each linkage conclusion below its left-hand count summary to keep the right-hand sums
readable; show those sums as separate paragraphs so bullet indentation cannot force a wrap
into the table below. Frame G39's unchanged handout capture with an unfilled gray SVG rectangle;
keep this reviewed image-bearing wrapper distinct from `.drawn.svg` assets.

**Owner.** Lecture 09G, the local unordered roadmap, and
[three_gene_homework_sources.json](../genetics/LECT09/djot/assets/lect09c-tetrad_worked_examples_bpw/three_gene_homework_sources.json).

### Consistent tetrad classes across E/F/G

**Decision.** Use a static question/large-answer pair in E and preserve existing question/answer
sequences in F/G. Match class colors across terms, figures, tables, formulas, and substituted counts.

**Why.** Small labels and black substitutions obscure connections students need for homework.
Imported per-glyph coordinates also produced poor spacing after font substitution.

**Consequence.** Reuse the generator's ascus geometry beside the original chromosome mechanisms;
retain the A/B-to-plus key. Normalize imported labels to natural text shaping. Enlarge table
class labels without altering genotype data, cumulative answers, arithmetic, or map results.
Restore original bitmap proportions. Use ordinary layouts for already-taught recaps and the
later unlinked TT slide, preserving reference treatment for additional material.
No shared layout or equation renderer changes.

**Owner.** Lecture 09 E/F/G sources, local figures, `tools/render_tetrad_tables.py`, and
[LECT09EFG_REVIEW.md](../genetics/LECT09/djot/LECT09EFG_REVIEW.md).

### Undistorted 09D mating and asci

**Decision.** Preserve 09D's original prose across the approved meiosis split, add two section
dividers, and show one enlarged mating stage per slide using the original bitmap proportions.

**Why.** Imported figure matrices stretched the artwork horizontally; cumulative figures made
the later states too small. Homework-matched asci connect the vocabulary to the upcoming problems.

**Consequence.** Reuse original image bytes, reposition live labels, and retain all unique stages
across D9-11. Reuse an actual three-gene homework ascus on D6/D14, preserving all loci and
explaining symbols, schematic colors, and unordered positions. Keep figure provenance local.
The deck has 17 pages; ordinary builds use saved SVGs without importing the generator.

**Owner.** `genetics/LECT09/djot/lect09d-yeast_unordered_tetrads.djot`, its figures,
and `assets/lect09_tetrad_concepts/lect09d_figure_sources.json`.

### Research-backed 09C mitotic crossover

**Decision.** Add five steps connecting DNA repair to LOH, clonal patches, an RB1 second hit,
and twin-spot experiments. Retain both original fly illustrations and keep the deck at twelve pages.

**Why.** LOH links the existing allele/phenotype examples to a cellular mechanism and gives
students useful applications. Primary papers support each addition; technical pathway catalogs
would add detail without helping this short conceptual introduction.

**Consequence.** Clarify repair timing and the context-dependent frequency of crossovers.
Use three original, static SVG diagrams with large allele labels, preserve both segregation
outcomes in the retained figure, and keep prose/tables/DOI citations native. Scope the SVG
ignore exception to these authored source assets. Save the evidence and scientific assumptions
in the lecture-local research report and ledger.

**Owner.** `genetics/LECT09/djot/lect09c-mitotic_crossover.djot`, its adjacent mitotic-crossover
assets, and [LECT09C_RESEARCH.md](../genetics/LECT09/djot/LECT09C_RESEARCH.md).

### Homework-matched 09B interference

**Decision.** Use two frozen numeric-bank items as 09B's worked examples, with native
homework-shaped tables and a locally included five-step roadmap.

**Why.** Students need to recognize their homework and understand each equation's quantities,
including the difference between a fractional expectation, observed count, coincidence, and interference.

**Consequence.** Save each bank item/HTML/data/hashes; build offline from authored Djot. Remove
the three old reference problems at the instructor's request. Contrast 20% and 75% interference,
including the distinction between coincidence and interference. Keep outside-pair recombination
distinct from adjacent-interval sums and preserve the corrected chromatin explanations.
Lecture-only chapter/roadmap files belong beside the master; no new dependency folder or
problem-to-slide framework is required.

**Owner.** `genetics/LECT09/djot/lect09b-crossover_interference.djot`, its worked chapters,
`interference_steps.djot`, saved data, and the Lecture 09 source map/review.


### Genetics 09 Tetrad Topic Sequence

**Decision.** Keep 09B interference and use six independent C-H masters: mitotic crossover,
yeast/asci, crossover classes and map distance, two-gene mapping, three-gene mapping, and
ordered tetrads/centromeres. Retire both mixed masters as pre-split source records.

**Why.** The introduction and worked master repeated classifications, unordered derivation,
and ordered-tetrad explanations. One home for each explanation keeps the small teaching
steps while making each topic easier to teach and locate for homework.

**Consequence.** 09E owns the count-based bridge from recombinant spores to DCO = 4NPD,
SCO = TT - 2NPD, and the corrected numerator. Preserve NCO and the mean-crossover identity
as normalized references. 09F and 09G apply the method without repeating its full derivation.
Keep all fixed datasets and results; the 10/15/24 cM estimates retain their pairwise meaning
while adjacent intervals sum to 25 cM. Ordered tetrads use a distinct four-step roadmap and
the 150 SDS/500 asci example, last in the sequence.

Reuse the actual homework table in 09G: all three genes stay visible in four spore boxes,
with A-B/A-C/B-C columns filled cumulatively. Four fixed SVG states share a quality-90,
3x capture of the original generated table and live class labels. Show it large during
classification; use native classified-count summaries for arithmetic. Two-gene and ordered
asci retain their approved art. Save the generator HTML and provenance; ordinary builds are
offline and do not import BPW or invoke Chromium. The existing two-gene utility is unchanged.

Recover nine figure regions from the original lecture PDF, keeping positioned labels and
leaders as SVG text/paths around source bitmap artwork. Use whitespace-free xlink data URIs,
quality-90 WebP, and a simple figure clip for LibreOffice. Keep asset directories stable,
original presentations unchanged, and all previous-slide actions in the source map.

Keep the ordered/unordered roadmaps in `genetics/LECT09/djot/` and use local includes.
Their repetition within one lecture does not make them evergreen content.

**Owner.** The C-H masters under `genetics/LECT09/djot/`, their included chapters,
the lecture-local ordered/unordered roadmaps, and `LECT09_SOURCE_MAP.md`.

## Genetics 09/10 conversion (2026-10-31)

- Keep both existing Lecture 09 B filenames and identities distinct. Use the maintained 2026
  announcement master for both weeks; the mislabeled 09 copy and 2025 10 announcements remain
  historical evidence. Keep one source slide per content slide, with additions recorded in maps.
- Expand source table merges only in temporary ODP copies for the current importer, then author
  native Djot spans. Keep unresolved visual relationships explicitly marked for replacement.
- Each equation-adjacent prose fragment owns its native ODP list. Start that fragment's list at
  level zero while retaining the original measured paragraph indentation; a parent list cannot
  span independent text frames.

<!-- VENDORED HEADER: START -->
Record each durable decision about how this code and repository are shaped, once it is settled, with
the reasoning a later reader needs. Guidance Neil Voss states belongs in
[HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md), dated history in `docs/CHANGELOG.md`, open discussion in
`docs/active_plans/decisions/`. [PROPAGATED HEADER - ENTRIES BELOW ARE YOURS]
<!-- VENDORED HEADER: END -->


- Table headers use black text and a course-accent tint with HSL lightness at least
  80%, preserving hue and saturation. Explicit native cell drawing fills prevent
  inherited template opacity from altering the palette.

- Native tables use 12 logical units of horizontal padding and 4 vertically. Header
  paragraphs default to centered; all cells use middle vertical alignment. Explicit
  text-align remains authoritative. Shared measurement includes the full cell padding.

### Advisory typography audit

`deck_tools.py audit` checks final compiled text-frame geometry using the same styled-token
wrapping routine as sizing. It reports source locations and predicted lines as JSON without
changing prose or failing on typography warnings. Pytest protects detection and shared
measurement behavior, not lecture-specific counts. Math, explicit breaks, and embedded figure
text require separate review; compiler predictions do not establish LibreOffice rendering.
Font advances retain fractional pixel sizes: integer rounding creates discontinuous widths
and incorrect wrapping near a line boundary. Ordinary hyphens and en dashes are break
opportunities; nonbreaking hyphens remain intact. Exact native line breaking for URLs that
still exceed the region at their 12 pt floor is not modeled.

### Labeled image assets

Static diagram masks and highlights are retained inside the bounded source figure. Existing
vector table images stay vector with live visible labels; do not expose text originally hidden
under an opaque mask. Associated marks may extend the figure viewport, but slide titles and
surrounding prose stay native. Source ODP animation targets distinguish static masks from reveals.
Marker removal depends on restored content/behavior and sound rendering; attended playback is
reported separately when native target/order and static evidence already verify the conversion.

LECT08's reviewed labeled figures use one embedded quality-90 WebP and live SVG text at
source-derived coordinates. The WebP includes the selected artwork and reviewed diagram marks;
marks are rasterized, labels remain editable in the SVG. Titles/captions and surrounding prose
remain native. Crop to the image group, not the slide, and inspect actual LibreOffice output.
This is an explicit asset repair, not automatic importer grouping. Multi-image overlaps,
native tables, and unresolved masks retain their own repair paths. Static fidelity does not
clear an interaction warning. Inventory: `genetics/LECT08/djot/assets/labeled_figures.json`.

### Image-owned click-to-remove covers

**Decision.** A `cover` immediately follows one initially visible image in the same region,
using normalized image-relative bounds and an explicit `disappear` action. Covers are opaque
white native rectangles; they are projected after image layout and take no flow space.

**Why.** LECT08B source 6 needs to hide the Punnett-square answers until a click. Slide-coordinate
rectangles lose alignment when layouts move or scale their image. This source copy retains the
rectangle but lacks animation; the instructor supplies the click intent explicitly.

**Consequence.** Shared cover extraction validates ownership and actions for lint and compilation.
Native export uses LibreOffice's `ooo-exit-disappear` visibility-to-hidden effect, confirmed against
its [effect definitions](https://github.com/LibreOffice/core/blob/master/sd/xml/effects.xml).
The importer does not infer animation from static rectangles. PDFs retain the initial cover;
state-render checks and native save roundtrips remain separate from attended click playback.

**Owner.** `slide_lib/image_covers.py`, `slide_lib/layout_object_builders.py`, and
`slide_lib/odp_animation.py`; syntax in [DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md).

### One allocator per content region

**Decision.** Jointly measure local headings, paragraphs, lists, tables, and images in their
source order. Use the shared selector for competing content, scoring each text block by font
size and each image by displayed width, in logical-pixel units. Preserve the existing text
floor and image-reduction checks; optimize readable text candidates during marked recovery too.

**Why.** Reserving the largest fitting local heading before sizing its image bypassed the
shared optimizer on LECT08B source 13. Individual text-box areas also rewarded extra height.

**Consequence.** Native text styling and object projection remain type-specific. Their space
allocation is shared; separate eager-heading and paragraph/table-flow sizing paths are removed.

**Owner.** `slide_lib/layout_builders.py` and `slide_lib/layout_measurement.py`.

### Subsections inherit the course palette

**Decision.** Use a dedicated subsection role for transition-card backgrounds and frames.
Resolve it as a darker shade of the course accent used by section cards.

**Why.** Subsections previously reused the fixed burgundy answer role, separating them from
their course palette. A darker shade distinguishes hierarchy and retains readable white text.

**Consequence.** All courses inherit this behavior through the shared exporter. Answer colors
retain their existing role; no per-deck color configuration is needed.

**Owner.** `slide_lib/layout_specialty_builders.py` and `slide_lib/odp_export.py`.

### Mixed vertical import sequences precede caption topology

**Decision.** Recognize an ordinary, vertically separated, horizontally aligned sequence of
text and pictures before caption pairing assigns multi-panel topology. Reuse the existing
source-flow slot and emitter: an image, its following sentence, and a second image can all
occupy one `@body`. The converter checks mixed-flow readability through the shared compiler
before publication and adds a source `@replaceme` plus report split recommendation when needed.

**Why.** Caption pairing previously preempted the existing vertical-flow recognition in
LECT07B slide 24. It grouped the PNG and sentence into one component and assigned the SVG a
second equal-height panel. The apparent object count dictated panel count, reducing prominence.
The shared area optimizer can allocate those objects together without manual geometry.

**Boundary.** Keep side-by-side comparisons, image-owned annotations, tables, and spatial
diagram reconstruction on their existing paths. Improved flow does not clear animation,
unsupported-media, missing-object, or spatial-reconstruction review reasons. Rendered review
is still required; no lecture-specific rule, new layout, or source prose rewrite is introduced.

### Mixed text and image area optimization

**Decision.** For a panel containing ordinary text and images, measure font candidates at
half-point intervals from the theme's ordinary size to its body floor. Maximize the sum of
measured full-width text-box area and actual displayed image areas. Scale images independently,
preserve their aspect ratios and source order, and favor larger fonts on exact area ties.
At each font, enumerate bounded allocation vertices: a convex image-area objective needs at
most one image between its bounds. The supported six-image limit bounds the search to at most
192 vertices per font candidate; surveyed lecture panels currently contain at most four images.

**Bounds.** Each image may occupy up to its full-panel contain size. Its minimum linear size is
that size multiplied by the theme's body-floor/ordinary-font ratio (currently 20/28). This
reuses the existing reduction budget rather than adding an unrelated percentage. Comparing
with contain size, rather than panel width alone, accommodates tall figures. This is a
geometric guardrail, not evidence that embedded labels are readable; original artwork still
requires visual review. Bounding-box area also includes whitespace within images and text.

**Failure.** If no bounded allocation fits, retain a serializer-safe half-point review preview,
add the existing REPLACE ME watermark, and report that the source requires `@replaceme` with
a recommendation to split into separate slides or panels. Include the recommendation in
speaker notes. Do not rewrite Djot during compilation or automatically split teaching content.
If even review geometry is impossible, fail with a source-located replacement/split diagnostic.

**Evidence.** LECT07B slide 24's one-panel trial selects 20 pt and approximately full-width
images; slide 25 selects 23.5 pt and a full-width question image. The doubled-text starvation
case is now marked for replacement. A tall-image specimen remains accepted; crowded three-
and four-image examples require splitting. Focused regression tests cover independent scaling,
aspect/order/fit preservation, determinism, and replacement reporting without changing source.
Temporary exhaustive comparisons verified 400 bounded allocation cases. On the local host,
warm slide-25 compilation measured about 13 ms versus 2 ms for the previous selection rule.

### Prose and table validation

**Decision.** Accept paragraphs, lists, and component images alongside one table in an ordinary
body or panel, matching the existing ordered-flow renderer. Keep rectangular-table validation,
one table per region, and layout-specific content restrictions.

**Why.** The old table-only lint restriction rejected successfully rendered LECT07D slides.

**Consequence.** Strict lint accepts supported mixed content without changing slide sources or
rendering geometry. Unsupported block combinations still produce source-located errors.

**Owner.** [layout_validation.py](../slide_lib/layout_validation.py) and
[DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md).

### Explicit YouTube slide generation

**Decision.** Generate ordinary `big-image` Djot fragments with yt-dlp metadata and a locally
validated PNG thumbnail. Include sibling fragments from lecture sources using existing syntax.
Show the full canonical watch URL as both the editable label and clickable destination.

**Why.** The StVC layout already provides the requested composition. Explicit generation keeps
network access outside ordinary builds and leaves the existing renderer unchanged.

**Consequence.** Regenerating replaces the selected fragment and thumbnail. Keep fragments beside
their master decks because included images resolve relative to the master directory.

**Owner.** [make_youtube_slide.py](../tools/make_youtube_slide.py) and [USAGE.md](USAGE.md).

### MathJax equations occupy complete blocks

**Decision.** Render LaTeX equations with local MathJax 4, STIX2 font data, and the mhchem
font extension. Batch distinct expressions per compilation. Use self-contained SVG paths
and measure complete equation boxes before selecting slide geometry.

**Why.** Djot is the editable source, and the existing SVG/ODP pipeline already preserves
vector equations. Native equation editing and a DOCX/OMML intermediate are unnecessary.
Positioning SVG between independently positioned prose fragments requires matching
LibreOffice's text layout and adds unnecessary fragility.

**Consequence.** Support standalone equations and equation-only list items or table cells.
Reject mixed prose/math with a source location. Keep native Djot formatting for simple
notation; do not classify LaTeX automatically. Prose stays in intact native paragraphs,
and the compiler stacks paragraph and equation boxes. Math table frames use the measured row sum so
Impress row expansion cannot move text away from equations. Generated SVGs live under
`_temp/math/`; original TeX is retained in equation descriptions. Definitions are
expression-local, and invalid TeX fails with a source location. Rendering uses no network.
This supersedes both the mixed inline fragment implementation and older documentation
requiring editable native equation objects. Representative rendering checks are one-time
evidence; permanent tests protect supported authoring and export contracts.

**Owner.** `slide_lib/math_render.py`, `slide_lib/math_layout.py`, and
[DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md).

### Decorative frames belong to masters

**Decision.** Put all theme-owned decorations on derived background masters; retain slide text
on the slide. Use no fill for section/subsection and THE END outlines. Preserve the pale cover
card and thin colored teaching bands. Citation backing bands also belong to the theme.

**Why.** Foreground borders can intercept PDF text selection even with no fill. macOS PDFKit's
point selection returned a graphic-object marker instead of the heading; moving decoration to
the background master restores the text. Extraction alone did not detect this failure.

**Consequence.** Share masters by decoration geometry and course-background visibility; retain
the dark page surfaces and keep decorations above the course background within their master.
An offline parametrized pytest covers eight layouts and two themes, including image captions.
Real PDF point-selection and visual checks verify exports; a failed ownership/fill assertion
requires repairing that boundary.

**Owner.** [odp_export.py](../slide_lib/odp_export.py) and [test_odp_export.py](../tests/test_odp_export.py).

### Embedded ODF document references

**Decision.** Accept a reference to an embedded-document directory when the manifest declares
that directory and its `content.xml`, and the content member exists in the validated archive.

**Why.** Native LibreOffice formula objects use directory references without an explicit ZIP
directory entry. Treating them as ordinary file references prevented Lecture 07 import.

**Consequence.** Existing path, XML, archive, and missing-file checks remain in force.
Formula interpretation remains an importer or authoring responsibility.

**Owner.** [odf_package.py](../slide_lib/odf_package.py).

### Includes between slides

**Decision.** Support `=== include: chapter.djot` blocks with optional `hidden: true`.
An include's hidden flag applies to all descendant slides; otherwise slide visibility is retained.

**Why.** Authors need to keep introductory and miscellaneous slides in the main deck while
controlling a whole project section with one flag. Bare include text in notes stays literal.

**Consequence.** Existing manifests still work. Physical source locations, chapter order,
theme inheritance, shared image paths, and folder discovery remain intact.

### Gates protect useful operation

**Decision.** Remove historical byte/provenance requirements, fixed template styling checks,
arbitrary repository budgets, and redundant or policy-only tests. Keep checks with concrete
content-preservation, execution, or safe-publication consequences.

**Why.** The human requires robust recovery and the smallest coherent design, with tests and
blocking gates justified by actual needs.

**Consequence.** [GATE_AUDIT.md](GATE_AUDIT.md) lists the removals, retained checks, and failure
actions. It supersedes earlier byte-pinning and permanent migration-baseline decisions.

**Owner.** [GATE_AUDIT.md](GATE_AUDIT.md).

### License notices do not gate rendering

**Decision.** Keep font-binary validation for reproducible measurement, but treat license notices
as optional packaging metadata during builds. Copy readable notices without checking their hash.

**Why.** License text and whitespace do not affect rendered slides and must not block teaching work.

**Consequence.** Preserve upstream licenses verbatim by excluding them from automatic ASCII and
whitespace cleanup. Missing or unreadable notices are omitted from the output package.

**Owner.** [presentation_theme.py](../slide_lib/presentation_theme.py).

### Encoding error locations

**Decision.** Decode source bytes as a whole and report invalid UTF-8 with a physical line,
character column, and bounded excerpt. Normalize LF, CRLF, and CR consistently.

**Why.** Editor coordinates let authors repair corruption without translating byte offsets.

**Consequence.** Invalid files still fail before parsing; no replacement text is silently saved.

**Owner.** [djot_sources.py](../slide_lib/djot_sources.py).

### Standard inline text formatting

**Decision.** Resolve Djot highlight, insert/delete, and sub/superscript spans into editable run
styles; braced emphasis uses the same model as ordinary emphasis.

**Why.** Standard author markup must survive through native ODP and its derived PDF.

**Consequence.** Insert/delete show underline/strikethrough, not tracked revisions. Highlight uses
pale yellow. Scripts use native ODF text positioning at 70% size; layout measurement conservatively
reserves the full-size text width. Existing color and underline attribute spans remain supported.

**Owner.** [DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md) and
[djot_inline.py](../slide_lib/djot_inline.py).

### Bare URLs with escaped colons

**Decision.** Recognize both plain HTTP(S) schemes and Djot-escaped scheme colons as native hyperlinks.
Normalize the escaped colon in the destination while consuming the full source spelling.

**Why.** This preserves automatic link styling for imported slides without requiring redundant labels.

### Theranos timeline date emphasis

**Decision.** Timeline date labels use the existing bold, underlined definition-term markup.

**Why.** Matching the genetics definition slides makes dates easy to locate within each event.

**Consequence.** All 36 dates across six timeline slides gain native editable emphasis.
Event wording and slide order stay intact.

**Owner.** [lect05c-theranos.djot](../biotech/LECT05/djot/lect05c-theranos.djot).

### Lecture 04 combined talking points

**Decision.** One Set 3 master includes the four existing chapter files in C/D/E/F order,
with a single final closer. Folder discovery builds the master as one deck.

**Why.** The instructor wants one ODP while retaining separately editable chapter sources.

**Consequence.** The combined deck retains six hidden answer slides and all teaching content;
only three intermediate closers are removed. Announcements and project slides stay separate.

**Owner.** [lect04c-talking_points_set_3.djot](../biotech/LECT04/djot/lect04c-talking_points_set_3.djot).

### Lecture 06C divider hierarchy

**Decision.** Each of the 33 Set 4 topics begins with a `subsection` divider; chapter starts
use `section`. Internal legacy section slides become `title-only` content slides.

**Why.** Consistent layout semantics distinguish chapter changes from numbered talking points.
The 2026 deck under `old/` confirms chapter starts before topics 1, 14, 22, 24, and 31.

**Consequence.** The combined deck has 281 slides, retaining existing teaching content and notes.
Brainbow stays in Chapter 15; the Summary remains a major closing transition.

**Owner.** [SET4_TOPIC_GUIDE.md](../biotech/LECT06/djot/SET4_TOPIC_GUIDE.md).

- **Decision.** Lecture 06D uses source PDF crops as writing/design examples, with native prompts,
  tables, quotations, and annotations. Six included section files produce one combined deck.
  **Why.** Actual student examples make the guidance concrete while keeping instruction editable;
  page/crop/hash provenance distinguishes historical proposal claims from verified results.

- **Decision.** Large lectures may use ordered, include-only Djot masters with separately edited
  chapter files, one shared image base, and physical chapter diagnostics.
  **Why.** Authors can edit a chapter without maintaining duplicate slide content or changing
  the combined build command. [The include contract](DJOT_SLIDE_SYNTAX.md#chapter-files-and-includes)
  defines ordering, theme inheritance, local paths, and folder discovery.

- **Decision.** Set 4 retains all 121 original source-slide records and 90 image references,
  regrouped under the 33 topics in `biotech/LECT06/old/2026_topic_list.txt`.
  **Why.** The 2026 topic list controls numbering; the annual decks expand explanations and
  discussion without silently replacing the instructor's original examples or opinions.

- Biotechnology Lecture 06 uses four canonical Djot decks. Keep the science deck as C and
  name business-plan guidance D to distinguish the two legacy C filenames. Use historical
  executive summaries as writing case studies, with current syllabus/Blackboard requirements
  authoritative for assignments. Sample claims are not validated scientific results.

- Resolve imported text formatting through frame, paragraph, and span context, retaining explicit
  normal/none resets. Preserve italic runs and source uppercase/lowercase transformations without
  changing the case of unrelated scientific symbols. Inline Djot colors may use validated six-digit
  RGB values when a source color has no semantic alias; retain the source-color review warning so
  LLM evaluation can assess contrast and diagram relationships instead of silently guessing a hue.

- A reviewed `@replaceme` is a valid conversion outcome. Acceptance does not require zero markers;
  it requires faithful converted slides or explicit replacement markers with source provenance and
  a clear reason. Do not force a weak reconstruction merely to reduce the marker count.

- Deterministic ODP import produces a draft, not an accepted teaching deck. Require LLM evaluation
  of source evidence and rendered draft slides before accepting the Djot conversion; repair and
  render again, or retain `@replaceme` where teaching intent cannot be preserved. Keep subsequent
  builds from the reviewed canonical Djot deterministic. This is a workflow requirement, not an
  implemented automatic LLM gate in the import CLI.

- Carry text appearance evidence from source ODP into import planning. Reuse the existing answer
  popup for a two-text question with one on-click answer labeled "Answer"; keep other unmatched
  reveals and unsupported animation actions reviewable. This is bounded recognition, not a
  general animation engine. A single standalone question uses the existing full-width layout.

## Explicit THE END layout (2026-09-24)

**Decision.** Author final closers with the dedicated `theend` layout and one exact `# THE END`
heading. Keep ordinary section dividers governed by their declared `section` layout.

**Why.** A layout's visual behavior should come from its named source contract. Inferring a special
closer from heading text makes ordinary section syntax carry hidden layout behavior.

**Consequence.** The `theend` layout validates the exact closer source and compiles to editable text,
a native vector star, and the established framed theme surface. Its ODP page uses LibreOffice's
Centered Text classifier.

**Owner.** `slide_lib/layout_registry.py`, `slide_lib/layout_validation.py`,
`slide_lib/layout_specialty_builders.py`, and `docs/DJOT_SLIDE_SYNTAX.md`.

## Current operational boundary

### Preserve metafile vectors during import

**Decision.** Export original metafiles through the existing component ODG wrapper to SVG instead
of selecting raster previews. Reuse static SVG validation and native SVG packaging. Report failed
conversion or missing live text for review.

**Why.** Native vectors retain editable labels and sharp diagrams at presentation scale.

**Evidence.** The genotype table retains 56 text elements and 34 paths with no bitmap images.
Actual PDF review exposed spurious RTL flags on Latin runs; a narrow correction restores positions
while preserving genuine RTL text. Details:
[metafile_vector_followup.md](active_plans/metafile_vector_followup.md).

### Image-area review without layout changes

**Decision.** Compare original image-frame area with compiled displayed area, both normalized to
slide size. Store non-blocking import warnings and provide an explicit audit command. Match exact
artwork bytes per slide; flag uncertain correspondence for manual review.

**Why.** Readable text can still displace a teaching image. Capacity checks alone miss that loss.

**Consequence.** The initial adjustable warning threshold is 30% relative area loss. Margin analysis
is advisory, and the audit neither trims artwork nor introduces layouts. Details and limitations:
[image_area_regression_followup.md](active_plans/image_area_regression_followup.md).

### SVG figures and definition emphasis

**Decision.** Package labeled diagrams as self-contained SVG components, with native Djot prose
outside the figure. A measured `image-comparison` layout reserves one shared caption row beneath
two diagrams. Preserve bold and underline through ODF import, Djot spans, and native text export.

**Why.** Labels must remain positioned with their artwork while explanations retain native text
editing and readable sizing. Definition terms need the visual hierarchy of the original slides.

**Consequence.** SVG labels are editable in the SVG source; the figure is one Impress object.
Keep replacement markers for unresolved relationships. Existing four-panel layouts are unchanged.

**Owner.** [SVG_DIAGRAMS.md](SVG_DIAGRAMS.md), `slide_lib/svg_images.py`,
`slide_lib/comparison_layout.py`, and `slide_lib/importers/odf_text.py`.

### Lecture 06 conversion boundary

**Decision.** Keep the four science decks in original slide order. Keep source-slide traceability
in separate slide maps or review files; reserve Djot `@notes` for instructor notes, following
[HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md).
Mark unsupported teaching relationships with `@replaceme`; restore the exam announcements
from legacy material and update calendar/policy details from the current local syllabus.

**Why.** A source-order list cannot preserve a positioned diagram or staged Punnett-square
explanation. A visible replacement marker makes that loss explicit for instructor repair.

**Consequence.** The original ODP remains the reconstruction reference. Three unsupported
06D table compositions use an import-only staging copy; their final sources retain warnings.

**Owner.** [LECT06_REVIEW.md](../genetics/LECT06/djot/LECT06_REVIEW.md).

### Explicit slide replacement marker

**Decision.** Accept one exact `@replaceme` line as slide metadata before content. Compile it
as an editable foreground warning with large red text and white backing for every layout.
New ODP imports emit the marker whenever the slide has review reasons.

**Why.** Import compromises and unfinished slides need an obvious human-review cue in the
source and rendered artifacts. A foreground object works across images and red section surfaces.

**Consequence.** Existing content, notes, visibility, and reveals remain intact. Removing the
marker clears the watermark on rebuild. Validation and capacity still inspect the marked slide.
Code examples and note text cannot enable it; detailed import reasons stay in the import report.

**Owner.** [DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md#slides-needing-replacement),
`slide_lib/djot_parser.py`, `slide_lib/layout_engine.py`, `slide_lib/layout_specialty_builders.py`,
and `slide_lib/importers/djot_emitter.py`.

### Lecture 05D teaching revision

**Decision.** Keep Lecture 05D v2 as a separate Djot deck. Use native text and tables for its
textbook-derived questions, manual question-answer slide sequences, and notes on every slide.

**Why.** The instructor requested a reviewable alternative preserving the hard opener,
addition-rule misconception, and callbacks while improving readability and participation.

**Consequence.** The original remains available; folder builds include both versions. V2 ends on
its requested summary and resolves the opening problem before introducing conditional inheritance.

**Owner.** [LECT05D_V2_REVIEW.md](../genetics/LECT05/djot/LECT05D_V2_REVIEW.md) and
[lect05d-v2-probability_concepts.djot](../genetics/LECT05/djot/lect05d-v2-probability_concepts.djot).

### Authored instructor notes

**Decision.** Every layout accepts one optional `@notes` region. It ends at the next named slot,
slide directive, or EOF. Store each plain-text line in the existing native speaker-note model,
preserve internal blank lines, and decode complete character references once.

**Why.** Instructor reminders belong to the slide but have no visible layout destination. The
existing ODP writer already owns native notes, so the language needs no new layout or model.

**Consequence.** Required visible slots remain required. Notes survive in the editable ODP and
are excluded from ordinary PDF export through explicit LibreOffice filter settings. Formatting
and action-like text stay literal. Existing import reports continue to retain imported notes;
automatic note emission during ODP import is outside this authoring change.

**Owner.** `slide_lib/djot_parser.py`, `slide_lib/odp_export.py`, `slide_lib/libreoffice.py`, and
[DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md#instructor-notes).

### Wide legacy table teaching figures

**Decision.** For imported legacy tables that need progressive highlighting or are too wide for a
readable native table, author the states as local HTML tables and render them once as lossless
200-DPI component PNGs. Use those figures in an explicit `one-panel` or `big-image` slide while
keeping the ordinary presentation build independent of HTML, CSS, and browser tooling.

**Why.** The Lecture 04G Punnett-square sequence and Lecture 04I seven-gene worksheet were
instructional table figures, not ordinary prose tables. Compressing them into six-panel or mixed
text flow layouts made the teaching sequence unreadable, while one large figure per step preserves
the progressive construction and phenotype cues.

**Consequence.** The generated HTML provenance and PNG figures live beside their canonical Djot
sources under the lecture asset folders. `devel/render_genetics_lect04_tables.py` can regenerate
the figures, but normal ODP/PDF builds consume only the checked-in PNG component images.

**Owner.** `devel/render_genetics_lect04_tables.py` and the Lecture 04 Djot asset directories.

### Recurring recording visual

**Decision.** Use one clean, locally authored recording card for recurring Genetics announcement
slides. Do not copy a stock-image watermark from a reference deck into a classroom asset.

**Why.** The Biotechnology reference's recording image was itself the Shutterstock-watermarked
asset that had been propagated into Genetics 02A, 03A, and 04A. A simple original card preserves
the recording cue without reproducing an unlicensed or distracting mark.

**Consequence.** The shared visual is rendered from `devel/recording-card.svg` into each lecture's
local `recording_biotech.png`; each announcement deck remains self-contained for the ordinary
Djot build.

**Owner.** `devel/recording-card.svg` and the Genetics announcement asset directories.

### Lecture-organized Genetics source tree

**Decision.** Organize the Genetics corpus by lecture. Each `genetics/LECT##/` directory contains
`djot/` for canonical Djot sources and adjacent imported assets, plus `old/` for original ODP/PDF/ODS
evidence. The shared master theme remains at `genetics/xlect99-template_2023.otp`, and the existing
recursive folder build command is the lecture selector.

**Why.** The lecture is the useful unit for authoring, review, source comparison, and classroom
delivery. Keeping original evidence beside its corresponding canonical source makes provenance
clear without requiring the build command to know about two top-level corpora.

**Consequence.** `./build_slides.sh genetics/LECT04/` builds only Lecture 04, while
`./build_slides.sh genetics/` still builds the complete Genetics corpus. Folder discovery continues
to select `.djot` files recursively and ignores the `old/` evidence because it contains no Djot
sources.

**Owner.** `genetics/`, `build_slides.sh`, and `slide_lib/native_export.py`.

### Lecture-organized Biotechnology source tree

**Decision.** Organize Biotechnology by lecture using the Genetics directory pattern. Each
`biotech/LECT##/` contains canonical Djot and its local assets in `djot/`, and original ODP, PDF,
and teaching-source evidence in `old/`.

**Why.** The lecture is the working unit for source review, authoring, and building. Keeping source
material beside the corresponding lecture makes the Biotechnology corpus follow the established
Genetics workflow.

**Consequence.** `./build_slides.sh biotech/LECT04/` selects Lecture 04, and `./build_slides.sh
biotech/` selects the complete Biotechnology corpus. Djot references remain local to each
lecture's `djot/` directory.

**Owner.** `biotech/` and `build_slides.sh`.

### Biotechnology protein Set #3 chapter decks

**Decision.** Keep all 146 pages from the instructor's Set #3 ODP across the chapter decks, including
its six hidden quiz answers. Convert the instructor's two on-click quiz sets and antibody-recognition
reveal into sequential visible question-and-answer slides, while retaining the six source answer
pages as hidden ODP slides.
Add all 30 protein topics as expanded study notes, with at least four slides per topic. Treat 04C
as a study resource, so presentation guidance about the instructor doing the talking does not fully
apply. Keep the text scannable while retaining explanations that help students study. Give every
slide at least one relevant local image and use several when they help explain the material. Let
source coverage and content determine the slide count; set no target or ceiling. Keep student names
and presenter identities out of canonical slides. Split the material into 04C Chapter 9: Proteomics,
04D Chapter 10: Recombinant Proteins, 04E Structural Biology (the added chapter outside the book),
and 04F Chapter 11: Protein Engineering. Keep each instructor chapter with its corresponding study
topics and retain the six hidden quiz answers in 04C. Give each standalone deck a relevant cover and
the dedicated `theend` closer.

**Why.** The instructor deck has good content but is incomplete, and the current student
presentations are incomplete too. Combining them preserves the instructor material while extending
coverage to all 30 protein topics; student figures add relevant visuals.

**Consequence.** The 30 topics are assigned by chapter: 1-13 in 04C, 14-20 in 04D, 21-24 in the
added 04E structural-biology deck, and 25-30 in 04F. The decks contain 214, 81, 31, and 66 slides,
respectively (392 total, including six hidden quiz-answer pages in 04C). All 146 instructor source
pages remain represented across 04C, 04D, and 04F. The hidden answer pages stay in the editable ODP
and are omitted from the classroom PDF. Instructor and student figures remain local with source-page
provenance; original source files remain under `biotech/LECT04/old/`.

**Owner.** `biotech/LECT04/djot/` and `biotech/LECT04/old/`.

### Biotechnology announcement workflow

**Decision.** Build a new lecture's announcements from the current-year preceding lecture and the
matching next lecture from the previous year. Use current course, instructor, and schedule sources
for policies, dates, links, contact information, office hours, and assignment or exam timing. Use
the prior-year matching lecture for recurring topics, agendas, readings, homework, activities, and
review questions. Use the numbered Veridian Dynamics filenames for the episode number and title,
while keeping its announcement image unchanged. Show talking marks as a big-image slide and leave
their spreadsheet out for instructor paste-in.

**Why.** The merge keeps current details accurate while carrying forward useful weekly material.
The instructor supplies the talking-marks spreadsheet directly in the editable ODP.

**Consequence.** The 2026 Biotechnology Lecture 04A deck uses Video #4, "Diversity Good for Us," and
retains the original Veridian image. Its talking-marks page is a large image, with no spreadsheet
embedded in the canonical Djot.

**Owner.** `biotech/LECT04/djot/lect04a-2026_announcements.djot` and the course sources in
`biotech/LECT04/old/`.

### Biotechnology Lecture 04B project archive

**Decision.** Keep all 42 archived individual-project slides after the eight current Fall 2026
slides in the Djot source and emit the archived pages as native hidden ODP slides.

**Why.** The complete project archive remains editable while only the current assignment appears in
classroom playback.

**Consequence.** The ODP contains 50 physical slides, 42 hidden; the classroom PDF contains the
eight visible Fall 2026 slides.

**Owner.** `biotech/LECT04/djot/lect04b-individual_project.djot` and its source material in
`biotech/LECT04/old/`.

### Genetics Lecture 04B character and trait quiz

**Decision.** Put the character and trait lists in two upper panels, then place the question and
answer choices together in a lower panel.

**Why.** Students need to compare the paired terms while reading the quiz prompt and choices.

**Consequence.** The slide uses a two-over-one panel composition rather than a text-only quiz layout.

**Owner.** `genetics/LECT04/djot/lect04b-mendel_history.djot`.

### Genetics Lecture 04C principle sequence

**Decision.** Highlight the principle being introduced next and gray the other principles on the
repeated overview slides. Use a lower-weight `subsection` slide for the open-ended principle prompt,
and keep allele definitions and genotype examples in left and right panels.

**Why.** The repeated highlights show the lesson's progression, while the prompt and paired
definitions/examples need distinct hierarchy and regions.

**Consequence.** The source sequence uses the existing `subsection` and `two-panels` layouts.

**Owner.** `genetics/LECT04/djot/lect04c-two_principles.djot`.

### Biotechnology Lecture 03 source merge

**Decision.** The canonical Biotechnology Lecture 03C Djot deck has a section slide, a canonical
student-question slide, and two short answer slides for each of the 25 current talking points.
Chapter dividers retain the curriculum sequence. Historical instructor and student sources
establish coverage, but student claims and identities are not published.

**Why.** The historical source collection is incomplete and includes unreliable student answers;
no individual instructor or student deck is authoritative. Together, the sources corroborate
coverage but do not certify factual claims.

**Consequence.** The merged Djot deck is the sole editable source for Lecture 03C. It provides a
105-slide classroom-ready 25-topic sequence without presenting unverified student work as course
content. The old ODP supplies relevant historical figures only; the Fall 2025 PPTX corroborates
complete topic coverage and supplies selected newer visuals.

**Owner.** `biotech/LECT03/djot/lect03c-talking_points_set_2.djot`.

### Lecture 03B section-divider hierarchy

**Decision.** Lecture 03B section dividers use `#` for the topic and `##` for its current Fall
2026 date or deadline.

**Why.** The legacy deck separated deadline text into an independently positioned visual object,
which produced visibly awkward spacing after conversion.

**Consequence.** Each generated divider has an intentional centered heading/subtitle hierarchy,
with no red-on-red dates or legacy midnight cutoff fragments.

**Owner.** `biotech/LECT03/djot/lect03b-individual_project.djot`.

### Chapter and topic divider hierarchy

**Decision.** `section` remains the bright course-color chapter divider; `subsection` is a
lower-weight burgundy divider for numbered topics within that chapter.

**Why.** A shared transition treatment flattened the teaching hierarchy between chapters and their
individual talking points.

**Consequence.** Both remain native editable Centered Text layouts, but their color contrast makes
the chapter/topic relationship immediately visible.

**Owner.** `slide_lib.layout_registry.py` and
`biotech/LECT03/djot/lect03c-talking_points_set_2.djot`.

The native-ODP decision below supersedes earlier decisions that describe a maintained PPTX reader,
writer, animation adapter, temporary conversion, or sibling artifact. Current operation builds one
editable ODP from Djot and asks LibreOffice to make every classroom and review PDF from that ODP.
The desktop GUI may remain open during headless conversion. Import reads bounded ODP; a legacy PPTX
is first saved as ODP in LibreOffice. The active catalog has twelve LibreOffice layouts plus the
project-owned `multiple-choice`, `gallery`, and `big-image` layouts, and native reveals use ODF/SMIL.
Earlier references remain dated design history.

### Sequential LibreOffice PDF conversion

**Decision.** Resolve `soffice` and invoke it once per generated ODP in source order with direct
`subprocess.run` arguments: `--headless`, `--norestore`, `--convert-to`, the Impress PDF filter,
`--outdir`, and the ODP path. The desktop GUI may remain open during conversion. Wait two seconds
between successful conversions and require each expected PDF before continuing. `native_export`
stages the complete PDF set and publishes only after every conversion succeeds.

**Why.** This is the established author workflow in `~/nsh/junk-drawer/makePDFSlides.sh`. The
private-profile, one-process batch, process-group, and timeout-cleanup experiment added failure
states and triggered a LibreOffice recovery prompt without solving a demonstrated classroom need.

**Consequence.** Numeric quality and DPI are export defaults, not gates. The build does not control
the desktop GUI and does not require it to close. No AppleScript, private `UserInstallation`,
`Popen`, process killing, or conversion timeout policy belongs in the build path.

**Owner.** `slide_lib/libreoffice.py` and `slide_lib/native_export.py`.

### Explicit podcast announcement refresh

**Decision.** `refresh_podcast.py` reads the public playlist Atom feed on demand, selects the
newest publication date in its recent entries, and inserts or replaces one marked `big-image`
slide after the selected deck's unique YouTube channel slide. Preview is the default; `--write`
saves the editable caption and local thumbnail.

**Why.** One reusable command supports multiple lectures while keeping ordinary builds
reproducible and old lectures tied to the episode originally selected.

**Consequence.** No API credentials or build-time network lookup are needed. The feed is a
recent-entry view, not a complete playlist history. Preserve the managed marker in speaker notes;
missing or ambiguous anchors require a source edit. Full-size thumbnails fall back to standard
thumbnails only when YouTube returns HTTP 404.

**Owner.** `refresh_podcast.py` and `docs/USAGE.md`.

## Related decision records

- [NATIVE_PRESENTATION_DECISIONS.md](NATIVE_PRESENTATION_DECISIONS.md) records native model,
  typography, layout, and export decisions.
- [SOURCE_PIPELINE_DECISIONS.md](SOURCE_PIPELINE_DECISIONS.md) records import, source,
  table, and capacity decisions.

## Local course URL resolution

Resolve explicit `{{course_url:key}}` references at the parser boundary using the resolved
course theme and ignored root YAML for private Discord and Zoom URLs. Public URLs, including
YouTube, remain in tracked sources. Preserve line numbers and native hyperlink parsing.
Load only when a reference exists; fail on missing keys rather than silently displaying a
Blackboard placeholder. Shared office hours and Biotechnology course Zoom are separate keys,
initially populated from the same meeting URL in the original Biotechnology ODPs. Existing
QR artwork is preserved. No source rewriting or network lookup occurs during builds.

## Mandatory URL typography

Recognize visible URL text independently of its destination. Use the condensed face and
start two points below surrounding text, with an independent 12 pt floor. Shared measurement
first fits the remaining line width; if that cannot fit at the floor, move the intact URL to
a new line and fit the full text width. Store the chosen size on the resolved run so ODP output
uses exactly the measured size. Keep complete display text and link destinations, including
URL labels inside explicit links and code spans. Human-readable link labels keep their ordinary
typography. The audit reports addresses still wider than the region at 12 pt; LibreOffice may
wrap these exceptional addresses. Ordinary paragraph sizing retains its own readability floor.

### Recovered LECT07C formula outlines

**Decision.** Use outlined SVG crops from the original PDF for recovered LECT07C formulas
with font-dependent spacing errors. Keep source slide and crop coordinates in
`genetics/LECT07/djot/assets/source_fidelity/lect07c/formula_sources.json`.

**Why.** The metafile-derived SVG text used substituted font metrics during PDF export,
shifting binomial entries and overlapping multiplication dots with parentheses.

**Consequence.** Figures remain sharp vectors with original spacing. Formula glyphs are
paths, not editable or copyable equation text; this does not implement LaTeX rendering.
Slide 18 uses the identical clean equation on source slide 19; slide 33 clips the separate
YUCK callout from the figure because the slide already contains that native text.

**Owner.** The LECT07C source-fidelity SVG assets and their `formula_sources.json` manifest.

### Biostatistics announcement source

**Decision.** Start the biostats announcement series at `biostats/LECT08/djot/` for
October 21, 2026, using the existing `biostatistics` green theme and shared HG layouts.
Use the freshly updated syllabus schedule source for topics, meeting format, quiz dates,
assignment dates, and graduate/group milestones. Keep tutorial cutoff times unspecified.

**Why.** The generated syllabus site still has the earlier generic schedule. The new source
provides the actual alternating in-person/asynchronous plan. Biostats has no exams.
Shared Discord and office-hours URLs remain in ignored course-link configuration.

### Tutorial art and citation footer

**Decision.** Use original schematic SVGs with flat fills, consistent outlines, and live labels
for the eight biostats tutorial reminders. Hospitals identify Fried Foods; soil-sample containers
identify Microbes. Comparison marks communicate means or variability without plotting results.
SVG assets remain canonical beside the Djot deck and are embedded as vector images in ODP.

**Layout.** The layout-independent `@citation` region uses the bottom margin without
resizing normal content slots. Citation text starts at 14 pt in the condensed font, with
the standard 2 pt reduction for visible URLs. Citations remain editable and clickable in
ODP/PDF. Dark surfaces receive a white footer backing; the reference-only label moves
slightly upward when a citation is present. The tutorial sources use ordinary `two-panels`.

**Drawing references.** The SVG creator skill's local-only corpus supplied Robertson,
*How to Draw*, "Drawing boxes in perspective" (construction and line hierarchy), and
*Mastering SVG*, "viewBox and viewport in SVG" (stable coordinate system and scaling).
Source paths under the skill's `references/local-only/` are
`object_construction/How_to_Draw_Drawing_and_Sketching_Objects_and_Environments_from_Your_Imagination-2013.md`
and `svg_authoring/Mastering_SVG-2018.md`. Front elevations and simplified containers serve
as illustrative memory cues, not drawings of actual buildings or measured specimens.
### Tutorial illustration identity refinements

The hospital food signs, two small trophies, and repeated bacterial jar emblem are
story reminders. The microbial emblem is identical across years and does not encode
community composition. Existing mean dots, spread brackets, labels, and geometry remain
unchanged. Editable SVGs in `biostats/LECT08/djot/assets/tutorial_overviews/` remain the
source images embedded in the Djot two-panel slides and exported through ODP/PDF.

Construction references revisited in the SVG skill's `references/local-only/` corpus:
Robertson's `object_construction/How_to_Draw_Drawing_and_Sketching_Objects_and_Environments_from_Your_Imagination-2013.md`,
"Drawing boxes in perspective" (outline hierarchy), and
`svg_authoring/Mastering_SVG-2018.md`, "viewBox and viewport in SVG" (stable coordinates).
The additions use simple silhouettes and matching strokes within the existing viewBox.

## Final-paragraph runt exemption

The Djot audit suppresses runt findings for the last displayed paragraph of a native text
frame when its selected size reaches the theme's ordinary body-size ceiling. Use the theme
ceiling, not compiled typography `start_size_pt`, which currently equals the selected size.
Count suppressed runts separately; retain title-wrap and URL-width warnings. This changes
advisory reporting only, not text, font selection, or rendering.

### Podcast slide identification

**Decision.** Identify managed podcast slides by their existing thumbnail path under
`assets/stump_the_vibe_coder/`; emit no administrative notes or comments in Djot.

**Why.** The instructor reserves `@notes` for presentation note cards used while lecturing.

**Consequence.** Refresh replaces the previous episode using its asset path, including decks
whose old metadata notes have been removed. Duplicate managed slides still stop refresh.

**Owner.** `tools/refresh_podcast.py` and [USAGE.md](USAGE.md).

### Announcement groups and visibility

**Decision.** Keep Genetics quiz and exam guidance, first-week assignments, course evaluations,
and constant course-information slides in `genetics/evergreen/`. Weekly masters use explicit
`repo:` includes and one visibility flag per group. Shared assets use the same `repo:` prefix.

**Why.** The instructor wants quiz guidance shown this week or next week when a quiz is due,
and early assignments and future evaluation slides preserved for reuse. Existing mixed
includes already support the required visibility behavior.

**Consequence.** Preserve the edited quiz wording and surrounding announcement slides.
Retain early assignments and evaluations hidden, and replace obsolete evaluation deadlines
with a published-deadline reminder. Future weekly decks reference these groups. Keep weekly
content and dated exam details in the master. Ordinary local includes retain their existing
containment boundary; explicit repository includes and images stay inside the Git checkout.
Podcast refresh recognizes include boundaries, preserving the shared channel and course slides.
Prior-week announcement copies are temporary starters for the new weekly A source. Once that
source uses the shared groups, remove unused starter copies and their extracted assets from
the new lecture folder; they are not additional lecture material.

**Owner.** [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md), [DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md),
and `genetics/LECT08/djot/lect08a-2026_announcements.djot`.

### Shared evergreen slides

**Decision.** Keep slides shared across courses in root-level `evergreen/`, starting with
spring registration and the YouTube channel. Keep course-specific reusable groups in the
course's own evergreen folder. Use the existing `repo:` includes and inherit the master's theme.

**Why.** Common announcements need one source that any course can include without copying text.

**Consequence.** Shared assets move with their owning group. Weekly podcast episodes and weather
snapshots remain with the lecture; this organization does not change their refresh tools.

**Owner.** [../evergreen/README.md](../evergreen/README.md) and
[../genetics/evergreen/README.md](../genetics/evergreen/README.md).

### Builds without Git

**Decision.** Use the Git root when available and fall back to the current working directory
when Git is missing or fails. Apply this to the launcher, environment setup, native build root,
and shared slide/image resolution.

**Why.** A copied project folder must build without `.git` metadata.

**Consequence.** Run Git-free builds from the top-level project folder. The existing traversal
and symlink-containment checks use that folder as their boundary.

**Owner.** `build_slides.sh`, `source_me.sh`, `slide_lib/djot_sources.py`, and
[USAGE.md](USAGE.md).

### Bookend and definitions layouts

**Decision.** Share one `bookend` layout for learning objectives and key takeaways. Use its
ordinary one-panel geometry with an editable, thin angular course-colored frame. Give
`definitions` the same frame geometry and course accent color with automatic bold/underline on
leading terms. Keep `reference` gray with its later-study footer. Use the existing course accent for the long bands and its pale tint for the opposite corner
accents. Pair shapes with exact half-turn symmetry and diagonal gaps. Native editable polygons
keep the 8-pixel bands outside the standard content area.

**Why.** Objectives and takeaways bookend the lecture with equal prominence. Definitions need
consistent term emphasis; live teaching anchors need a distinct identity from later-study material.

**Consequence.** Authors select the semantic layout instead of repeating visual formatting.
Plain `Term: explanation` entries and existing leading bold terms are normalized before measurement.
Nested examples keep their authored formatting. Initial adoption covers LECT08B-F objectives and
takeaways plus LECT08B's linkage definitions, preserving their wording and sequence.

**Owner.** `slide_lib/teaching_layouts.py`, `slide_lib/layout_specialty_builders.py`, and
[DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md).

### Automatic runt balancing

**Decision.** Use the same runt criterion for advisory detection and automatic text balancing.
For a wrapped paragraph with a short final line, move whole words from the preceding line until
the tail is acceptable, without changing font size or adding a line. Retain run styles and links.

**Why.** The instructor prefers automatic layout handling and accepts more words on the next line.
Manual wording edits should not be required for a renderer-controlled line break.

**Consequence.** Sizing and final text projection share measured balanced lines. The ODP receives
soft line breaks only when balancing changes a paragraph. The audit measures those emitted breaks
and still reports unresolved runts. Explicit author breaks, URLs, and math keep their existing
handling. Leave an unfixable tail unchanged rather than overflowing or creating a new short line.
Source Djot wording remains unchanged. The final-paragraph audit exemption still applies.

**Owner.** `slide_lib/typography.py`, `slide_lib/layout_measurement.py`,
`slide_lib/layout_object_builders.py`, and `slide_lib/djot_audit.py`.

### Three-point procedure recaps

**Decision.** Store the pairwise-distance and quick DCO procedure slides as separate canonical
Djot files under `genetics/evergreen/`. Repeat the appropriate include before a new problem.
Use the fixed [COLOR_PALETTE.md](COLOR_PALETTE.md) colors in rainbow order, including matching
colors on internal step references. The six-step procedure uses red/orange/yellow/green/blue/purple;
the four-step procedure uses red/green/blue/purple.

**Why.** The instructor wants a recurring colored roadmap. Full mapping and quick middle-gene
inference use different numbered methods; separate sources keep their instructions consistent.

**Consequence.** LECT08D includes the six-step procedure before its worked problem and activity.
The replacement BPW LECT08F includes it before its worked problem and at gene-pair transitions.
The original textbook F deck is retired; its separate DCO roadmap remains available for future use.

**Owner.** `genetics/evergreen/three_point_testcross_steps.djot`,
`genetics/evergreen/three_point_gene_order_steps.djot`, and
[SLIDE_CONVERSION_CHECKLIST.md](SLIDE_CONVERSION_CHECKLIST.md).

Procedure recap titles use explicit black text, leaving the fixed rainbow colors on
the steps. Six-step recaps also mark gene-pair changes and returns to summary/distance
work, alongside repeats before new practice problems.

### Native cell backgrounds

**Decision.** Use a whole-cell `[content]{background-color=#RRGGBB}` wrapper with the CSS
property name. Authored `TableCell` records retain inlines and an optional hex background;
physical cells carry the explicit fill into ODP `fo:background-color` cell styles.

**Why.** Worked examples need editable parental/recombinant shading and blank covered columns.
This extends the existing native table pipeline instead of adding picture overlays or CSS parsing.

**Consequence.** Explicit fills override theme/total defaults without changing text color or
geometry. Measurement and math/text traversal use the typed cell's inlines. Unattributed cells
keep their previous behavior. Partial-cell and non-table backgrounds are source errors.

**Owner.** `slide_lib/native_model.py`, `slide_lib/djot_blocks.py`,
`slide_lib/layout_object_builders.py`, `slide_lib/odp_text.py`, and `docs/DJOT_SLIDE_SYNTAX.md`.

### BPW replacement for LECT08F

**Decision.** Replace the active textbook deck with a fixed, authored example (now 43 slides with phase dividers) from
BPW question `ae3b_1ad2`. Keep the original Djot as `.djot.retired` beside its assets and retain
original ODP/PDF evidence. Folder discovery selects only the replacement `.djot`.

**Why.** The instructor teaches the pairwise method used by BPW and LECT08C/D.

**Consequence.** Each gene pair has six states: select/cover, classify, sum prompt, sum reveal,
divide, and multiply. A native results table accumulates completed calculations. Original BPW
answers remain 25, 9, 33 and dch/hcd; the map separately shows adjacent intervals totaling 34 cM.
No BPW repository changes or permanent conversion generator are required.

**Owner.** `genetics/LECT08/djot/lect08f-three_point_testcross_bpw.djot` and its lecture review/map.

### Merged and aligned table cells

**Decision.** Extend whole-cell wrappers with HTML-named `colspan` and CSS-named `text-align`.
The semantic cell retains a positive horizontal span and optional left/center/right alignment.
Grid validation counts logical columns, measurement uses the combined spanned width, and the
existing ODP writer emits merged cells plus native covered positions. Explicit text alignment
wins over numeric auto-alignment. Existing unspanned cells keep their original behavior.

**Why.** The BPW example needs equal gene columns, a Total label spanning all three genes,
and centered class labels separated from right-aligned counts.

**Consequence.** Spanned rows omit covered source cells. Automatic/grouped sizing accounts for
spanned text without allocating the full label width to the first gene column. The BPW tables
use repeated explicit `1,1,1,2,1.5` proportions; backgrounds are stronger green/purple tints with
a gray covered column. Eight section/subsection dividers separate the lesson's teaching phases.

**Owner.** `slide_lib/native_model.py`, `slide_lib/djot_blocks.py`,
`slide_lib/layout_measurement.py`, `slide_lib/layout_object_builders.py`, and table syntax docs.

### Persistent parental references

**Decision.** In the BPW worked example, only the two original parental progeny rows retain green
backgrounds throughout all pairwise states. Other pairwise P rows use lime; recombinant rows use the fixed color assigned to their
gene pair (CD red, CH blue, DH purple). The unused gene column stays gray even where it intersects a reference row.

**Why.** Covering a gene changes the displayed projection, not the identity of the original parents.
Students need stable reference rows when deciding how to classify the remaining offspring.

**Consequence.** Known parental P labels and counts persist through pair-selection prompts.
Classification slides compare c++ / +dh to their two-gene projections in the same order, using
three short bullets in the main work panel. A compact slide-wide citation-footer legend explains
row colors, P/R labels, and pair colors without taking comparison space or causing the former awkward wrap.

**Owner.** `genetics/LECT08/djot/lect08f-three_point_testcross_bpw.djot`.

### Gene-pair color continuity

**Decision.** Use CD red, CH blue, and DH purple from the fixed palette, with hue-matched lighter
fills in progeny and summary tables. Reserve green for original parental rows and lime for other
pairwise parental rows. The exact base/fill values are recorded in `docs/COLOR_PALETTE.md`.

**Why.** The instructor wants all classified rows colored and each recombinant sum visibly linked
to its own pair's results, while preserving stable parental reference rows.

**Consequence.** Summary pair labels establish the mapping; result cells reveal in the same color
as their source recombinant rows. Final percentages and the corresponding adjacent map intervals
use the pair's base color. Step colors and the gray covered-column mask keep their existing roles.

**Owner.** `genetics/LECT08/djot/lect08f-three_point_testcross_bpw.djot` and the color palette doc.

### BPW visuals follow the reasoning

**Decision.** Keep the full progeny table and each arithmetic reveal through the three pairwise
calculations. Add two matched question/answer slides at the first C-D classification: cd+ (120)
projects to recombinant cd; c+h (75) projects to parental c+. Use stable green original-parent
references and the same covered-H geometry in both states.

After all three results are known, replace the progeny table with a shared-scale recombination
bar chart and large endpoint, middle-gene, and proportional interval-map views. Separate the
50 cM interval sum from the 40% observed D-H recombination. Compare parental and double-recombinant
alleles in solved D-C-H order, then use a small native table to show that the same fifty offspring
are R for CD and CH but P for DH. State that these offspring are already included in both interval
counts. Preserve the original C-D-H genotype labels in the count table and identify both orders.

**Why.** The working table provides continuity during classification; afterward it competes with
the spatial reasoning. The two side-step examples explain the classification rule, while the
double-recombinant comparison connects the count correction to allele combinations.

**Implementation.** Twelve static SVG components use explicit labels and the fixed pair palette;
titles, explanatory text, and tables remain native Djot. The setup uses a native fly emoji and
lists heterozygous loci separately without revealing phase or gene order. Existing layouts and
export behavior suffice. The active deck has 49 visible slides, including three shared roadmaps.

**Owner.** `genetics/LECT08/djot/lect08f-three_point_testcross_bpw.djot`, its local SVG assets,
and its review/slide map. Book references and validation evidence stay in the review document.

**Follow-up.** Repeat the matching answer for CH and DH, keeping the covered-gene geometry and
original-parent references. Replace the small-gap bank instance with a locally generated example:
CD 30%, CH 20%, DH 40%, 1,000 offspring, and 50 double recombinants. Set up the 50 cM / 40%
mismatch before tracing two exchanges and comparing/counting the resulting offspring. A 50 cM
interval sum is not a claim of 50% recombination. Preserve semantic hue and saturation across
line/text colors and pale fills, adjusting lightness only. The generator and independent solver
are used during authoring; normal builds consume fixed Djot and SVG sources.

## StVC print showcase (2026-10-28)

**Decision.** Give the evergreen podcast approximately 53% of usable Letter-page height
and the four games 47%. Lead with the title, a 2.22-inch YouTube QR, the existing
StVC 36 "Bad Cell Day" host thumbnail, a personal invitation, and the Wednesday
livestream invitation. The thumbnail shows the hosts together; restore Dr. Voss' small
portrait beside the dominant headline to reinforce his personal invitation. Use the
human's "Check out Dr. Voss' podcast!" and "Watch us build them and see what happens!"
copy, framing the show as people experimenting together. Preserve Atkinson Hyperlegible
Next and mixed-case surrounding text.

**Podcast grouping.** Arrange the invitation and title with a secondary portrait at right,
then a full-width description. A thin teal rule introduces the livestream invitation,
schedule, and scan instructions at left, with the 160-point QR at right. Reduce the
episode thumbnail to 160 by 90 points beneath that invitation. Independent review of
two new upper-page layouts prefers these horizontal groups over a text column beside
a separate image rail. Keep the section boundary and lower game artwork unchanged;
render comparison confirms the entire game section is pixel-identical to the approved
version. These alternatives and QR checks are in `_temp/stvc-grouping/`.

**Games.** Use a compact two-by-two showcase with thin colored rules and white backgrounds.
Each advertisement has a solid-filled light-mode vector wordmark above a source-derived
action scene, a clean game QR beside the scene, and 10.5-point promotional copy beneath.
The scenes show a maze pursuit, plaque blasting, a cooperative climb, and a steroid moving
toward a porous nucleus. Recolor wordmark text for white paper and remove text outlines
and duplicate shadow layers; retain recognizable typography, helix, bow, and brand hues.

**Why.** The user superseded the initial game-heavy design with an evergreen podcast focus.
Independent designers explored a magazine-cover composition and a two-thumbnail editorial
composition. Both initially compressed game artwork too far. Independent visual reviewers
selected the refined single-thumbnail composition with larger scenes and clearer game
copy. One thumbnail limits image coverage while visibly representing the show. The page
remains predominantly white, with no filled game-card backgrounds. Actual printer ink
consumption was not measured.

**QR contract.** Use 160 points (2.22 inches) for the main YouTube code and 76 points
(about 1.06 inches) for each game. Preserve high error correction and four-module quiet
zones from `qrcode2.py`. Retain the central YouTube icon only; game codes have no embedded
logos or cleared center patches. Steroid Quest retains QR mask 0.
All five destinations decode in 200- and 300-dpi renders, including an independent check;
physical printer/phone scanning has not been performed.

**Colors.** Teal `#00775F` identifies Ms Taq Man; Light orange `#935D00`, Plaque Attack;
Sky blue `#076DAD`, Bad Cell Day; and Magenta `#C80085`, Steroid Quest. These fixed palette
colors keep QR modules dark on white while retaining game branding in the illustrations.

**Destinations.** The main QR opens `https://www.youtube.com/@VossLab/streams` for the
live invitation. Past episodes retain a clickable StVC playlist link in the PDF. The
channel handle was verified against the playlist owner's channel. The local recording
schedule is labeled Central based on the Chicago teaching context.

**Artifacts.** `output/pdf/build_stvc_flyer.py` builds the PDF and WebP from saved assets.
`output/pdf/stvc-flyer-assets/scenes/` contains editable SVGs and vector PDF derivatives;
`output/pdf/render_stvc_scenes.py` regenerates those derivatives using Chromium outside
the macOS sandbox. `output/pdf/render_stvc_wordmarks.py` renders the editable wordmarks
the same way. The saved host thumbnail is `output/pdf/stvc-flyer-assets/episode-hosts.jpg`,
copied from the existing `0zhh6g-DJFs` episode image. This supersedes the more cartoonish
`_9HjPmVv_MU` thumbnail at the human's request. Final alternatives and print-review
evidence are in `_temp/stvc-next/`; earlier explorations remain in `_temp/stvc-concepts/`.
