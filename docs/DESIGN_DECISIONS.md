<!-- VENDORED HEADER: START -->
Record each durable decision about how this code and repository are shaped, once it is settled, with
the reasoning a later reader needs. Guidance Neil Voss states belongs in
[HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md), dated history in `docs/CHANGELOG.md`, open discussion in
`docs/active_plans/decisions/`. [PROPAGATED HEADER - ENTRIES BELOW ARE YOURS]
<!-- VENDORED HEADER: END -->

# Design decisions

### Explicit native stacking order

Export each object's compiled stacking order as `draw:z-index` as well as ordering XML siblings.
LibreOffice presentation placeholders must retain their intended position above cover decorations;
sibling order alone does not explicitly encode that relationship for the consumer.

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

**Decision.** Keep the four science decks in original slide order with source-slide notes.
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
