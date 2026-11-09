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

- Native table padding comes from the selected named style and can be overridden per cell.
  The `standard` style uses 4 pt vertical and 9 pt horizontal padding; header paragraphs default
  to centered and cells use middle vertical alignment. Explicit alignment remains authoritative.
  Shared measurement includes actual padding, borders, bold text, spans, and equation placement.

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
`slide_lib/odp_animation.py`; syntax in [slide-specs/DJOT_SLIDE_SYNTAX.md](slide-specs/DJOT_SLIDE_SYNTAX.md).

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
[slide-specs/DJOT_SLIDE_SYNTAX.md](slide-specs/DJOT_SLIDE_SYNTAX.md).

### Explicit YouTube slide generation

**Decision.** Generate ordinary `big-image` Djot fragments with yt-dlp metadata and a locally
validated PNG thumbnail. Include sibling fragments from lecture sources using existing syntax.
Show the full canonical watch URL as both the editable label and clickable destination.

**Why.** The StVC layout already provides the requested composition. Explicit generation keeps
network access outside ordinary builds and leaves the existing renderer unchanged.

**Consequence.** Regenerating replaces the selected fragment and thumbnail. Keep fragments beside
their master decks because included images resolve relative to the master directory.

**Owner.** `slide_lib/make_youtube_slide.py` and [USAGE.md](USAGE.md).

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
[slide-specs/DJOT_SLIDE_SYNTAX.md](slide-specs/DJOT_SLIDE_SYNTAX.md).

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

**Owner.** [slide-specs/DJOT_SLIDE_SYNTAX.md](slide-specs/DJOT_SLIDE_SYNTAX.md) and
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
  the combined build command. [The include contract](slide-specs/DJOT_SLIDE_SYNTAX.md#chapter-files-and-includes)
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
`slide_lib/layout_specialty_builders.py`, and [slide-specs/DJOT_SLIDE_SYNTAX.md](slide-specs/DJOT_SLIDE_SYNTAX.md).

## Current operational boundary

### Preserve metafile vectors during import

**Decision.** Export original metafiles through the existing component ODG wrapper to SVG instead
of selecting raster previews. Reuse static SVG validation and native SVG packaging. Report failed
conversion or missing live text for review.

**Why.** Native vectors retain editable labels and sharp diagrams at presentation scale.

**Evidence.** The genotype table retains 56 text elements and 34 paths with no bitmap images.
Actual PDF review exposed spurious RTL flags on Latin runs; a narrow correction restores positions
while preserving genuine RTL text. Details:
[metafile_vector_followup.md](archive/metafile_vector_followup.md).

### Image-area review without layout changes

**Decision.** Compare original image-frame area with compiled displayed area, both normalized to
slide size. Store non-blocking import warnings and provide an explicit audit command. Match exact
artwork bytes per slide; flag uncertain correspondence for manual review.

**Why.** Readable text can still displace a teaching image. Capacity checks alone miss that loss.

**Consequence.** The initial adjustable warning threshold is 30% relative area loss. Margin analysis
is advisory, and the audit neither trims artwork nor introduces layouts. Details and limitations:
[image_area_regression_followup.md](archive/image_area_regression_followup.md).

### SVG figures and definition emphasis

**Decision.** Package labeled diagrams as self-contained SVG components, with native Djot prose
outside the figure. A measured `image-comparison` layout reserves one shared caption row beneath
two diagrams. Preserve bold and underline through ODF import, Djot spans, and native text export.

**Why.** Labels must remain positioned with their artwork while explanations retain native text
editing and readable sizing. Definition terms need the visual hierarchy of the original slides.

**Consequence.** SVG labels are editable in the SVG source; the figure is one Impress object.
Keep replacement markers for unresolved relationships. Existing four-panel layouts are unchanged.

**Owner.** [slide-specs/SVG_DIAGRAMS.md](slide-specs/SVG_DIAGRAMS.md), `slide_lib/svg_images.py`,
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

assignments through September 21 in fall or February 14 in spring. General Announcements usually
has one active seasonal topic; preserve graduation/registration/evaluation windows, hide the club,
and allow relevant one-off campus announcements.

### Dedicated announcement preparation guide

**Decision.** Keep the assembled `lect##a` structure, seasonal display rules, course exceptions,
and weekly preparation steps in [slide-specs/ANNOUNCEMENT_DECK_GUIDE.md](slide-specs/ANNOUNCEMENT_DECK_GUIDE.md).
Link it from HG, usage, the conversion checklist, and evergreen READMEs. HG remains the record
of human-stated preferences; the guide is the practical starting point for announcement work.

**Why.** The growing workflow was scattered across HG and decision history. A focused guide
is easier to find and apply without reading unrelated teaching guidance. Refresh the guide
when the instructor changes an announcement preference.
