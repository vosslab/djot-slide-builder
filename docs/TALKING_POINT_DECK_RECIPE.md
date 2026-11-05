# Talking-point deck recipe

Use this recipe to build the next Biotechnology talking-point sets from annual student
presentations and expanded instructor material. The result is an editable Djot study deck,
an editable ODP, and a reviewed classroom PDF. It supports live discussion and later study;
complete explanations belong on visible slides when students need them afterward.

The working examples are Set #4 in
[SET4_TOPIC_GUIDE.md](../biotech/LECT06/djot/SET4_TOPIC_GUIDE.md) and Set #5 in
[SET5_TOPIC_GUIDE.md](../biotech/LECT10/djot/SET5_TOPIC_GUIDE.md). Use their organization and
review method. Their dates, topic counts, page counts, and scientific claims are examples,
not defaults for the next set.

Follow the stages in order:

1. [Establish input authority](#establish-input-authority) and
   [inventory the sources](#inventory-before-writing).
2. [Organize the files](#organize-the-work) and [build the topic map](#build-the-topic-map).
3. [Compose each topic](#compose-each-topic), [handle figures](#handle-figures-deliberately),
   and [author native Djot](#author-native-djot).
4. [Validate and build](#validate-and-build), then [review the export](#review-the-actual-render).
5. [Close out the set](#close-out-the-set) with outputs, maps, and an honest review receipt.

## Start with the outcome

A finished set has:

- Every current assigned topic, in the instructor's exact numbered order.
- Useful teaching content from the expanded instructor deck and all available annual sources.
- Current questions, explanations, mechanisms, examples, and relevant figures.
- Chapter sections and numbered topic subsections, with content easy to edit in small files.
- Local figure assets with separate provenance, without tracking copyrighted images.
- A topic/source map, an input inventory, and a completed conversion/review receipt.
- Successful source validation, ODP/PDF export, and visual review of the actual PDF.
- Explicit unresolved items and unperformed checks, rather than an unsupported readiness claim.

There is no target slide count. A compact outline is not a substitute for the requested expanded
study deck. Conversely, repeated generic prose or unrelated illustrations do not improve coverage.

### Choose the correct workflow

For an ordinary conversion, preserve source slides and their relative sequence. Follow
[SLIDE_CONVERSION_CHECKLIST.md](SLIDE_CONVERSION_CHECKLIST.md), including the existing rules
for source-slide splitting and preservation of instructor prose.

For an explicitly requested annual-source merge, the current topic list governs the new
organization. Preserve useful instructor material while adding researched explanations for
topics absent from the older deck. Record the existing authorization and the merge method in
the review report. Account for the original content through a source map; do not claim that
the expanded result is a one-to-one conversion.

Set #4 and Set #5 used the second workflow. Permission for those merges does not silently
turn every future conversion into a redesign. Apply the current request and recorded guidance
without creating another feedback gate for work already authorized.

## Read the working references

Read these before authoring, with the instructor's current request taking precedence:

- [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md): teaching voice, study slides, topic hierarchy,
  preservation, figures, visibility, and the recorded Set #4/Set #5 direction.
- [DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md): actual supported syntax and layouts.
- [PEDAGOGICAL_SLIDE_STYLE_GUIDE.md](PEDAGOGICAL_SLIDE_STYLE_GUIDE.md): teaching structure.
- [SLIDE_CONVERSION_CHECKLIST.md](SLIDE_CONVERSION_CHECKLIST.md): conversion accounting.
- [SLIDE_VISUAL_REVIEW_RUBRIC.md](SLIDE_VISUAL_REVIEW_RUBRIC.md): rendered review criteria.
- [USAGE.md](USAGE.md): supported commands.
- [PYTEST_STYLE.md](PYTEST_STYLE.md): permanent tests versus implementation proof.

Use the guides together: concise presentation slides and complete study explanations serve
different purposes. Do not hide the study explanation exclusively in speaker notes.

## Establish input authority

Each source answers a different question:

| Input | Use it for | Do not assume |
| --- | --- | --- |
| Current instructor topic list | Exact numbers, labels, coverage, order | Older deck numbering still applies |
| Current schedule | Lecture date, assigned set, upcoming work | Last year's week or date is current |
| Expanded instructor ODP | Mechanisms, examples, wording, emphasis, useful figures | It covers every current topic |
| Current annual student deck | Current prompts, topic coverage, candidate visuals | Answers or clinical claims are verified |
| Earlier annual student decks | Missing explanations, questions, examples, useful figures | The newest file contains their best material |
| Source PDFs | Appearance, grouping, emphasis, readable figure identity | PDF page number equals authored slide number |
| Text exports | Searchable leads and question extraction | Reading order, formatting, or diagrams survived |
| Prior reviewed Djot set | Structure, layout patterns, successful workflow | Its scientific content belongs in the new set |

For Fall 2026 Biotechnology, the schedule source used for Set #5 was
`~/nsh/syllabus/site_docs/fall_2026/biotech/SCHEDULE.md`. Locate the current semester's
equivalent rather than copying that path or its dates indefinitely. Topic-list files may be
under the lecture root or `old/`; locate the actual instructor-supplied file.

Keep lecture number, talking-point set number, and textbook chapter number distinct. Set #4
was taught in LECT06; Set #5 was taught in LECT10 and covered Chapters 17-19.

When the request also includes announcements or project guidelines, use
[ANNOUNCEMENT_DECK_GUIDE.md](ANNOUNCEMENT_DECK_GUIDE.md) and the current syllabus for those
companion decks. Keep weekly dates, project-phase changes, media selection, and private
`{{course_url:key}}` substitutions separate from the reusable science chapters.

### Understand the source files

Annual sources often have long names such as
`Fall_2026_Talking_Points_Set_5-Medicinal_BioTech.odp`. Expect ODP, PPTX, matching PDFs,
and plain-text exports, with inconsistent naming and storage across years.

An annual presentation can contain topic prompts, student answers, screenshots, embedded
figures, empty submissions, presenter names, assignment directions, hidden pages, and animations.
Its apparent length is not a measure of useful instructor coverage.

ODP and PPTX are ZIP packages. Read-only package inspection can recover text, embedded media,
relationships, notes, visibility, and animation leads without starting LibreOffice:

- ODP uses `content.xml`, `styles.xml`, and commonly `Pictures/` assets.
- PPTX uses `ppt/presentation.xml`, slide XML, relationship files, and `ppt/media/`.
- Resolve PPTX presentation relationships for actual slide order. Sorting `slide1.xml`,
  `slide2.xml`, and so on is not reliable after slides have been rearranged.
- Resolve images from their owning slide's relationships. A media filename alone does not
  establish which picture was displayed on a slide.
- Resolve ODP hidden state through page styles; checking a single page attribute is insufficient.
- Preserve paragraph boundaries and slide identifiers during extraction. Flattened text can
  mix labels, body text, and presenter notes.

Use extracted text to find candidates, then look at the source page and actual image. Text
extraction cannot establish figure identity, colored emphasis, masks, or reveal behavior.

## Inventory before writing

Search the lecture folder, its `old/` directory, and the earlier relevant lecture folders.
Survey all available annual sources before deciding that a topic has no useful existing content.
Do not ask the instructor to choose between sources before completing this survey.

Save a source inventory in the lecture review report:

| Field | Record |
| --- | --- |
| Source identity | Repository-relative path, year, format, role |
| Source size | Authored slide count and visible count |
| Hidden material | Authored slide numbers and reason when understood |
| Reveals | Slides with animation elements, targets/order when applicable |
| Visual reference | Existing or newly exported PDF and its visibility behavior |
| Extraction | Location of temporary text/media inventory |
| Coverage | Topics or instructor source ranges represented |

Useful discovery and visibility commands, from the repository root:

```bash
rg --files biotech/LECT10 | rg '\.(odp|pptx|pdf|txt|djot)$'
source source_me.sh && python3 deck_tools.py visibility \
  biotech/LECT10/lect10c-set_5_TP-chap17-19_material.odp
pdfinfo biotech/LECT10/lect10c-set_5_TP-chap17-19_material.pdf
```

These are Set #5 examples; substitute the next lecture's real paths.

Original PDFs may include hidden slides even when the new classroom export excludes them.
Verify this rather than subtracting hidden counts blindly. Keep authored slide number,
source PDF page, and final PDF page as separate fields.

For a sync-related disappearance, recheck existence and the current inventory. Do not reset
the working tree or invent replacement material from an error message.

## Organize the work

Keep canonical Djot inside its lecture's `djot/` directory. Follow the existing lecture
layout; new collections of original material normally belong in its `old/` directory.
Set #5's originals were already at the lecture root. That is input history, not a reason
to move the originals during every new deck build.

Example layout for a future set:

```text
biotech/LECT12/
  old/                              original inputs, when organized here
  2026_topic_list.txt                instructor's current numbered list
  djot/
    lect12c-set_6_topic_material.djot master manifest
    set6_opening.djot
    set6_chapter_20.djot
    set6_chapter_21.djot             or a manifest of cohesive topic ranges
    set6_summary.djot
    SET6_TOPIC_GUIDE.md
    LECT12_REVIEW.md
    assets/
      set6_chapter_20/
        PROVENANCE.md
        mechanism_source.png        local ignored artwork
        mechanism_detail.png        local ignored derived crop
_temp/
  biotech_lect12/                    extraction, diagnostics, renders, receipts
output/
  odp/                              generated editable products
  pdf/                              generated classroom products
```

This tree illustrates naming and ownership, not a new lecture assignment or chapter mapping.

Keep permanent documentation outside `docs/active_plans/`. Keep temporary scripts and review
renders under root `_temp/`. Do not depend on a previous session's temporary scripts as
installed tools: they may contain fixed paths, old counts, or mutation steps that undo repairs.

Reuse shared slides through `evergreen/` or `biotech/evergreen/`. Keep set-specific science
and dated snapshots with their lecture. Do not recreate a top-level `biotech/djot/` collection.

Use `git mv` for tracked moves. Staging, checkout/restore, and commits remain outside the
slide-authoring task unless separately authorized. Deleting obsolete generated drafts does not
require keeping a second retired copy; preserve necessary original evidence and provenance.

### Divide files cohesively

Use one small master manifest and chapter files. Split a large chapter by related topic
ranges before it approaches the source-size advisory. Keep each topic's divider, questions,
explanation, and figure views together. Do not split a file mechanically every fixed number
of lines or add wrappers to satisfy a test.

The source limit is below 1,000 physical lines, with an advisory at 900. Leave room for
later improvements. Set #5's gene-therapy chapter used a nested manifest and topic ranges
01-04, 05-08, and 09-12.

```djot
color-theme: biotechnology

include: set6_opening.djot
include: set6_chapter_20.djot
include: set6_chapter_21.djot
include: set6_summary.djot
```

Build the master for one combined deck. Folder commands select masters and omit their
included files as separate decks. Do not duplicate the same slide content in the master.
Use the existing include syntax and containment rules; ordinary chapter paths stay within
the master directory. Use `repo:` includes for shared evergreen content.

## Build the topic map

Before drafting, make a row for every assigned topic:

| Field | Purpose |
| --- | --- |
| Number and current label | Prevent omissions and silent renumbering |
| Chapter and editable file | Establish curriculum boundaries and ownership |
| Current questions | Preserve what students are expected to explain |
| Instructor source slides | Preserve expanded mechanisms and examples |
| Annual source candidates | Record useful questions, explanations, and visuals by year/page |
| Missing coverage | Identify researched additions needed |
| Figure identity | Connect the actual asset to its scientific role |
| Final PDF pages | Add after the final build |

Use the current list literally for mapping even when the student-facing topic title is
expanded for clarity. Confirm chapter boundaries from the current source outline. Do not
infer them from a filename, topic count, or convenient equal-sized partition.

Account for every instructor slide: retained, regrouped, reconstructed, superseded, or excluded,
with a reason. Account for title/closing replacements and hidden legacy material too.
Annual student sources need a useful-content survey, not automatic reproduction of every page.

Update the final page ranges after the last insertion or deletion. A source-to-topic map
cannot use a stale PDF page number as permanent identity.

## Compose each topic

A useful topic sequence is:

1. A numbered `subsection` divider.
2. The current questions in clear, complete form.
3. An overview answering the central question.
4. Mechanism, comparison, experiment, or worked interpretation.
5. Useful instructor examples and figures, including enlarged views when needed.
6. A limitation, misconception, or evidence question where the material calls for it.

This is a teaching pattern, not a fixed slide quota. A short topic may need less; a mechanism
with several useful source figures may need substantially more.

Start each major chapter with `section`. Repeat the current topic number in supporting
titles or meaningful captions so students can navigate. Do not add visible slide-number
footers. Use Title Case for slide titles while keeping Markdown documentation headings in
sentence case.

Preserve the instructor's useful explanations, examples, humor, opinions, deliberate emphasis,
and scientific distinctions. Make new explanation direct and concrete. Do not invent a personal
opinion or phrase it as something Dr. Voss said.

Retain complete questions and enough visible explanation for study. Avoid generic paragraphs
that could fit any topic. Prefer a mechanism, an explicit comparison, an assay, a prediction,
or an interpretation tied to the assigned question.

Use speaker notes for delivery cues. Keep source filenames, source-slide numbers, repair history,
selection metadata, and verification logs in the review/topic guide or provenance files.
Older decks may contain source references in notes; that is not the current authoring policy.

### Verify scientific additions

Student slides supply leads, not authority. Check substantive additions and corrections against
primary papers, official scientific institutions, or the relevant regulator. Search when a claim
is uncertain, specialized, or may have changed. Keep a bounded source trail for each addition.

Pay special attention to:

- Approval versus trial participation, and the jurisdiction/date of an approval.
- Preclinical, early clinical, and established clinical results.
- Mechanism diagrams versus evidence of treatment benefit.
- Cell identity, assay readout, clinical outcome, and safety as different claims.
- Historical examples versus current treatment protocols.
- Absolute statements, performance percentages, and broad safety claims.
- Similar words that name different mechanisms or disease roles.

Open the actual cited page or paper. Confirm title, authors, year, and the claim it supports.
A plausible DOI or a paper on a neighboring subject is not enough. Set #5 review caught two
citations pointing to the wrong papers.

When the inputs conflict, preserve the evidence and state the bounded distinction. Do not
silently present a disputed or unverified claim as settled instructor content.

## Handle figures deliberately

### Extract and identify

Use original embedded assets where possible. A whole student slide is usually a poor figure:
it can carry a name, unsupported assertions, tiny text, and an unrelated slide design.
Crop the actual scientific diagram or reconstruct suitable prose/tables as native content.

For every selected image:

1. View it independently.
2. Locate its source slide and inspect that page.
3. Verify what it depicts, including labels, orientation, and scientific role.
4. Check that the explanation actually refers to that image.
5. Give the copied asset a meaningful name after identification.

Set #5 exposed misleading asset selections: water droplets under CRISPR, a grocery aisle under
CAR design, a steroid-signaling diagram called an Ames test, and a historical ADA-SCID web capture
called an expression cassette. A filename, nearby extraction index, or matching color is not proof.

Avoid repeating a generic stem-cell diagram under genome quality, release criteria, and clinical
outcomes. Prefer a relevant figure or an editable comparison/workflow. A useful text-only page
is preferable to an irrelevant decorative image.

### Preserve useful detail

Keep diagrams proportional. Preserve arrows, labels, scale bars, legends, controls, and meaningful
grouping. Trim empty borders only after inspecting what the crop removes. Save derived crops
separately and record the source and crop bounds.

Keep titles, surrounding explanation, and representable tables native. For a complex labeled
figure, use the existing artwork-plus-live-label approach described in the conversion checklist;
do not rasterize the entire slide to avoid a layout problem.

Add an enlarged figure view when the mixed text/figure page makes labels too small. Keep its
caption connected to the current topic. A large source image can still be unreadable if its
meaningful diagram occupies only a small area inside it.

Retain an inaccurate historical diagram only for a deliberate critique, with the correction
visible beside it or in its caption. Otherwise replace or omit it. Do not use a wrong diagram
as a silent illustration of the corrected explanation.

### Keep assets local

Copyrighted images stay local and ignored. Track the authored Djot and text provenance where
repository policy allows; do not stage image binaries to make a checker pass.

```bash
git check-ignore -v -- biotech/LECT10/djot/assets/set5_stem_cells/stem_division_crop.png
git ls-files -- biotech/LECT10/djot/assets
```

The first command verifies the ignore rule for a real asset. Inspect the second command's
output for accidentally tracked media. Neither command stages anything.

Djot lint checks local existence and safe paths, including ignored/untracked assets.
Markdown checking applies to `.md` documentation and has its own link policy. It does not
validate Djot image syntax. Do not add copyrighted images to Git or weaken vendored checks
to compensate for using the wrong checker.

Write `PROVENANCE.md` beside each coherent asset group. Record source/year, source-slide
number, original embedded member when useful, actual figure identity, external source if
verified, derived filenames/crops, and relevant limitations. Use portable paths, not a
machine-specific `/Volumes/...` or home-directory path.

### Compare figure size

The supported one-to-one audit is:

```bash
source source_me.sh && python3 deck_tools.py image-audit \
  SOURCE.odp CONVERTED.djot --loss-threshold 30
```

Replace the uppercase placeholders. It compares identical artwork's displayed share of a
slide and reports relative area loss; the default threshold is 30 percent. It requires
matching authored slide count and order. It is a diagnostic, not proof of label readability.

For a reorganized expansion, do not run that command against unmatched decks. Use the source
map and a temporary comparison that matches assets across the compiled expanded deck.
Compare each source use with its mapped destination; for several views, identify which one
preserves the required readable detail.

Byte-identical images can be matched by content hash. Crops, composites, reconstructed text,
and transformed figures require manual correspondence. Record those cases explicitly.
Do not call a missing match a successful preservation check. Set #5 used a temporary cross-deck
comparison plus manual review, not a new permanent audit command.

## Author native Djot

Follow [DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md), not Markdown habits:

- Strong text is `*term*`, not `**term**`. Double asterisks appeared literally in an early PDF.
- Keep source ASCII where possible. Use supported character references such as `&alpha;`,
  `&beta;`, and `&prime;`; verify the rendered glyph and scientific meaning.
- Do not write HTML entities into plain-text notes expecting a renderer to interpret them.
  Use plain words or punctuation there when appropriate.
- Use semantic font roles; the backend selects installed font families.
- Preserve deliberate colored terms, bold, italics, underline, and ALL CAPS.
- Keep complete visible URLs and actual clickable destinations. Put long scientific references
  in `@citation`, outside the body paragraph.
- Prefer one relevant source paragraph per citation footer. Multiple paragraphs caused a fit
  failure in Set #5 even after excessive shrinking; put additional sources in the topic guide.
- Use native tables for comparisons. Inspect headers, column widths, values, totals, and wrapping.
- Keep table-header text black on light course-colored fills. A dark total row needs explicit
  light text; Set #5 used `[*Total*]{color=#FFFFFF}`.

A topic starts with this structure:

```djot
=== layout: subsection

# Topic 1: A Specific Mechanism

=== layout: one-panel

# 1. Questions: How Does It Work?

@body

- What enters the system, what changes, and what can you measure?
- Which comparison would distinguish the two proposed explanations?
```

Use the existing layouts before considering a new one. A difficult original conversion may
retain `@replaceme` and a precise review finding. Removing every marker is not a requirement
and clearing a marker without checking the repaired render is not a repair.

### Assemble the bookends

Each standalone content deck needs:

1. Cover with lecture letter, subject, chapter information, instructor, and teaching date.
2. Specific learning objectives using `bookend`.
3. Optional definitions of new terms actually needed in the lecture.
4. Chapter sections and ordered topics.
5. Summary/reference material and final key takeaways using `bookend`.
6. A separate `theend` slide.

Preserve existing useful bookends. Keep decorative frames behind native selectable text.
Verify the combined master, since included chapter files may intentionally omit standalone covers.

## Use the right tools

Run from the repository root. Use the required Python 3.12 bootstrap:

```bash
source source_me.sh && python3 --version
```

Keep `PYTHONDONTWRITEBYTECODE=1` and the repository environment. Do not use `py_compile`
or `compileall` as syntax checks; they explicitly write bytecode despite that environment
setting. Use the source lint or an in-memory check when necessary.

Commands that can invoke LibreOffice must run outside the sandbox on this Mac. This includes
imports, PDF builds, conversions, and conversion tests. An ODP import may invoke LibreOffice
indirectly for embedded metafiles; it is not guaranteed to be a ZIP-only operation.
Serialize LibreOffice jobs. Parallelize read-only source survey or separate authoring instead.

The supported roles are:

| Tool | Job |
| --- | --- |
| `rg --files`, `rg -n` | Locate inputs and search extracted text |
| `zipfile`, XML readers | Read-only package inventory/extraction of trusted local inputs |
| `deck_tools.py visibility` | Resolve authored ODP visibility |
| `deck_tools.py import` | Convert a trusted ODP to Djot/assets/report |
| `deck_tools.py lint` | Validate extended Djot, includes, links, assets |
| `deck_tools.py capacity` | Estimate text/table fitting concerns |
| `deck_tools.py audit` | Report title wrapping, runts, and URL concerns as JSON |
| `deck_tools.py image-audit` | Compare matching one-to-one source/conversion image area |
| `deck_tools.py build` | Export editable ODP and ODP-derived PDF |
| `pdfinfo`, `pdftotext` | Inspect PDF count and selectable text |
| `pdftoppm` | Render PDF pages for visual review |
| Pillow or existing image tools | Inspect assets, make documented crops/contact sheets |

### Import selectively

The importer accepts trusted ODP, not PPTX. Save PPTX as ODP using LibreOffice outside the
sandbox when an actual import is needed. Read-only PPTX inventory does not require conversion.
Do not turn every annual deck into a canonical imported lecture.

Use a new temporary destination for an initial instructor import:

```bash
mkdir -p _temp/biotech_lect12
source source_me.sh && python3 deck_tools.py import \
  biotech/LECT12/old/instructor_material.odp \
  --output _temp/biotech_lect12/instructor_import.djot
```

These example inputs must be replaced with existing paths. The importer refuses existing
output Djot or asset directories. Locate existing reviewed import artifacts before trying
again; do not overwrite the canonical lecture with a fresh mechanical import.

Inspect the generated source, reachable assets, and `import_report.json`. Review markers
and diagnostics identify candidates for repair; slides without warnings still need review.
Preserve useful importer output and original figure assets when assembling the authorized merge.

## Validate and build

Run source checks before invoking LibreOffice:

```bash
source source_me.sh && python3 deck_tools.py lint --require-native \
  --native-executable "$(command -v jotdown)" biotech/LECT10/djot
source source_me.sh && python3 deck_tools.py capacity biotech/LECT10/djot
source source_me.sh && python3 deck_tools.py audit \
  biotech/LECT10/djot/lect10c-set_5_medicinal_biotechnology.djot
```

Use the next lecture's paths. Strict lint visits included files too. Resolve parsing, semantic,
missing-asset, and link errors. Lint success says nothing about an image's scientific identity.

Inspect capacity and typography findings rather than editing prose automatically. Ordinary body
text above 17 pt is generally acceptable under current instructor guidance; below 17 pt needs
layout review, and a 17 pt table can be acceptable. Keep complete URLs independently sized under
the backend's URL rules. Inspect awkward word breaks even when a table technically fits.

Prefer better grouping, wider columns, meaningful short labels, or an enlarged figure view
over unreadable shrinking. Preserve instructor prose unless the requested merge/revision authorizes
the change. Shorten newly generated long titles when useful, then check the actual render.

Build the selected master outside the sandbox:

```bash
source source_me.sh && python3 deck_tools.py build --format all \
  biotech/LECT10/djot/lect10c-set_5_medicinal_biotechnology.djot
```

Or build all eligible decks in one lecture with `./build_slides.sh biotech/LECT10`.
Outputs use the master source stem under `output/odp/` and `output/pdf/`.
The generated ODP is editable, but lasting repairs belong in canonical Djot so the next build
retains them. Document any deliberate output-only instructor update.

## Review the actual render

Use the ODP-derived PDF, not only a source preview or compiled estimate.

```bash
mkdir -p _temp/biotech_lect10/review
pdfinfo output/pdf/lect10c-set_5_medicinal_biotechnology.pdf
pdftotext -layout output/pdf/lect10c-set_5_medicinal_biotechnology.pdf \
  _temp/biotech_lect10/review/science.txt
pdftoppm -scale-to 1600 -png \
  output/pdf/lect10c-set_5_medicinal_biotechnology.pdf \
  _temp/biotech_lect10/review/page
```

Review every visible page, using manageable contact sheets to find problems and individual
pages at readable size for dense text, diagrams, tables, and repairs. A contact sheet alone
cannot certify small labels. Send only a few sheets per image-inspection call so output
truncation does not hide unreviewed pages.

For each topic, verify:

- Correct number, chapter, questions, and intended order.
- Complete explanation and retained meaningful instructor content.
- Actual figure identity and its connection to the explanation.
- Readable labels, intact diagrams, preserved emphasis, and no stretching.
- No student names, whole-slide student screenshots, or unsupported performance claims.
- No literal Markdown markers, clipped text, overlapping citations, or broken table words.
- Complete visible/clickable URLs and citations supporting the adjacent claim.

For each deck, verify:

- Cover/date, learning objectives, optional definitions, summary, and separate THE END.
- Source/Djot/ODP authored counts and final visible PDF count reconcile through the map.
- Hidden slides remain in editable ODP and stay out of the classroom PDF.
- Hidden reference material is also inspected, using a separate review export when needed.
- Native text remains selectable, including bookends, tables, and the closer.
- Original reveal targets/order are preserved where required; static PDF review is distinguished
  from attended Impress click/video playback.

Routine review uses the visual rubric's criteria without requiring a numerical score per page.
Record concrete defects and their repairs. After a repair, rebuild and recheck the affected pages.
If page insertion shifts numbers, refresh the map and review-sheet labels before further work.

## Keep checks proportionate

Use the existing permanent checks that apply:

```bash
source source_me.sh && pytest \
  tests/test_djot_links.py tests/test_djot_audit.py tests/test_slide_one.py \
  tests/test_ascii_compliance.py tests/test_markdown_links.py \
  tests/test_source_file_line_limit.py tests/test_guidance_doc_format.py -q
```

Source discovery policies differ between checkers. Ensure newly authored files are actually
covered; directly lint the new master and inspect the new documentation rather than relying
on a green inventory that omitted them.

Keep deck-specific count reconciliation, asset-hash comparisons, source inventories, crop
checks, and PDF text probes as one-time verification under `_temp/`. Do not add a permanent
test asserting this year's topic count, exact page count, or chapter filename list merely to
prove the rebuild. Retain durable Djot syntax/guideline protection even if exact assertions
look fragile. Apply the permanent-test checklist before promoting any new test.

If a vendored test fails, inspect the content or code it checks. Do not weaken the test to
hide the failure. A missing local copyrighted asset should be restored locally, not tracked.

## Coordinate without collisions

For a large set, independent chapter authoring and source surveys can run in parallel.
Use a fresh agent per independent task, as required by repository guidance.

Give each author:

- Exact topic numbers, current questions, chapter boundaries, and owned files/asset directory.
- Instructor source ranges and annual extraction locations.
- The visible-study-explanation requirement and instructor voice/preservation rules.
- Instructions to inspect actual figures, verify additions, and write separate provenance.
- Supported layouts and required Python environment.
- A self-contained handoff containing checks run, coverage, assets, and unresolved findings.
- Notice that others are editing the repository: preserve their work and stay within ownership.

One integrator owns the master manifest, topic map, final titles/cross-references, combined build,
and final review report. Serialize LibreOffice builds/imports through that owner. Independent
reviewers can inspect disjoint PDF ranges or audit figure identity without editing sources.

Treat handoffs as evidence to integrate, not final acceptance. Set #5 needed a combined review
to catch incorrect figures, Markdown emphasis, citation identity, generic repeated artwork,
and table contrast after chapter-level checks passed.

## Close out the set

Save a short `SETN_TOPIC_GUIDE.md` with the final topic-to-chapter/page map and scientific
reading links. Save a lecture review report with:

- Input inventory, current topic/schedule authority, and authorized merge scope.
- Original-slide coverage, additions/exclusions, hidden material, and source PDF correspondence.
- Asset/provenance locations and significant reconstruction/crop decisions.
- Scientific corrections and verified source identities.
- Final source/ODP/PDF paths and authored/hidden/visible counts.
- Validation results, rendered review coverage, remaining markers/advisories, and limitations.
- A copied conversion checklist with honest `N/A` explanations for merge-specific differences.

Update [CHANGELOG.md](CHANGELOG.md). Record new human-stated preferences in
[HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md), and actual settled design decisions in
[DESIGN_DECISIONS.md](DESIGN_DECISIONS.md). Do not turn a one-off repair into a general policy
without evidence.

Remove obsolete authored drafts after their useful content has been integrated. Keep original
source evidence and useful review receipts. Do not leave an alternative draft where folder builds
will export it as another canonical deck.

Hand off concrete ODP/PDF paths and the topic guide. State what was tested and reviewed.
Do not claim a full pytest run, attended Impress playback, working external uploads, or verified
clinical currency unless those checks were actually performed. Finish authorized work using
available evidence; do not leave completion dependent on a feedback question.

## Worked example: Set #5

The November 5, 2026 build combined six annual sources (2021-2026), a 62-slide expanded
instructor ODP, and the instructor's exact 37-topic list. The annual inputs had 40, 44, 74,
74, 100, and 136 authored slides respectively; the 2025 source was PPTX.

The final science master had 235 visible pages organized into gene therapy, genome editing,
stem cells/cloning, and cancer biotechnology. This count is a historical receipt, not a quota.
The next set's topic list and useful material determine its length.

Use these concrete examples:

- [SET5_TOPIC_GUIDE.md](../biotech/LECT10/djot/SET5_TOPIC_GUIDE.md): final page map, instructor
  correspondence, annual-source coverage, and scientific references.
- [LECT10_REVIEW.md](../biotech/LECT10/djot/LECT10_REVIEW.md): source inventory, repaired figures,
  visibility decisions, conversion checklist, and validation limits.
- [lect10c-set_5_medicinal_biotechnology.djot](../biotech/LECT10/djot/lect10c-set_5_medicinal_biotechnology.djot):
  small combined master.
- [set5_gene_therapy.djot](../biotech/LECT10/djot/set5_gene_therapy.djot):
  cohesive nested chapter manifest.
- [PROVENANCE.md](../biotech/LECT10/djot/assets/set5_stem_cells/PROVENANCE.md):
  local artwork provenance and derived-crop documentation.

The durable lessons are to survey first, map topics before drafting, preserve the instructor's
useful material, inspect figure identity, verify citations, keep explanations visible, and
review the final export. None of the successful command exits replaced that editorial work.
