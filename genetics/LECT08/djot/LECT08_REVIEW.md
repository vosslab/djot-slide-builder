# Lecture 08 conversion review

## Active LECT08F: BPW worked example

The active deck is `lect08f-three_point_testcross_bpw.djot`: 49 visible slides, 12 static SVG
components, and three shared six-step recaps. The textbook predecessor remains preserved
byte-for-byte as `.djot.retired` beside its assets. Original ODP/PDF evidence remains unchanged.

### Generated classroom example

The original bank question `ae3b_1ad2` (25%, 9%, 33%; 1,400 offspring) has been superseded by
this larger-gap classroom example. The new instance is generated locally with the same BPW
`gene_map_class_lib.GeneMappingClass(3)` implementation, not fetched from the published bank.
Neither BPW checkout was changed. The exact counts are fixed in the Djot/SVG source, so ordinary
builds do not require BPW or regenerate the data.

Generator directory:
`~/nsh/PROBLEMS/biology-problems/problems/inheritance-problems/gene_mapping/`.
Configure gene letters `cdh`, order `dch`, parental classes `c++` / `+dh`, total 1,000,
and pairwise values 30, 20, 40 in map-index order. Derive interference (1,6) with
`calculate_interference_from_three_distances(20,30,40)`, then call the existing group-count,
genotype-pair, and genotype-count methods. Reciprocal counts were split by the generator.
The separate `gene_map_solver_lib.gene_map_solver` confirms [20,30,40], (1,6), and hcd.

| Original C-D-H label | Count |
| --- | --- |
| cdh | 29 |
| cd+ | 120 |
| c+h | 75 |
| c++ | 260 |
| +dh | 290 |
| +d+ | 75 |
| ++h | 130 |
| +++ | 21 |
| Total | 1,000 |

| Pair | Recombinant counts | Sum | Fraction | Percent |
| --- | --- | --- | --- | --- |
| CD | 29 + 120 + 130 + 21 | 300 | 0.30 | 30 |
| CH | 29 + 75 + 75 + 21 | 200 | 0.20 | 20 |
| DH | 120 + 75 + 75 + 130 | 400 | 0.40 | 40 |

Adjacent intervals are 30 cM and 20 cM. Double-recombinant classes cdh (29) and +++ (21)
total 50, or 5%. Thus 40 + 2*5 = 50 cM. The 50 cM interval sum does not mean 50%
recombination: observed D-H recombination is 40%. This is the instructor-accepted example
following the discussion of that distinction. The brief 25/15/34 candidate was not adopted.
Answer fields use 30, 20, 40, and dch/hcd, matching the generator's pairwise convention.

### Visual sequence

- Keep all 21 full progeny tables through the final calculation, with equal gene columns,
  merged Total, fixed row order, original green parental references, lime other P rows,
  and a gray covered column. All sums/divisions/percentages use the new data.
- Slide 3: fly emoji and testcross context without revealing phase or gene order.
- Slides 12-13: initial matching question/answer. With H covered, cd+ projects to recombinant
  cd, while c+h projects to parental c+.
- Slide 22: repeat the matching answer for C-H. c+h projects to recombinant ch; cd+ matches
  parental c+. Slide 31 repeats it for D-H: cd+ projects to recombinant d+, while cdh matches
  parental dh. The latter is the same class revisited in the double-recombinant explanation.
- Slides 38-41: remove the full progeny table. Compare 30/20/40% bars, reveal the endpoints
  and middle gene, then ask why the map intervals sum to 50 cM while D-H gives 40%.
  CD and CH segments use red and blue; the endpoint D-H line uses purple.
- Slide 43: trace one double-recombinant chromatid across two exchanges, showing how its
  outer +/+ combination is restored. Only the two participating nonsister chromatids are
  shown; the reciprocal path is faint. The path is schematic, not a distance scale.
- Slide 44: compare original and double-recombinant allele combinations in D-C-H order.
  The middle allele differs while outer combinations match.
- Slide 45: the 29 and 21 offspring are R for CD and CH, P for DH. Show that 50 offspring
  contribute 100 adjacent-interval counts, are already included in those interval counts,
  and account for the 10-point correction. Keep 5% and the correction in the main content.
- Slide 46: answer fields alongside the 30:20 proportional map, explicitly distinguishing
  the 50 cM map length from 50% recombination.

Keep base hues and HSL saturation stable while varying lightness. The canonical fill values
are in `docs/COLOR_PALETTE.md`; repeat them in tables and SVG allele tiles. Colored pair labels
connect the pale fills to map lines without relying on background color alone.

### Sources informing the diagrams

These are conceptual references, not imported textbook figures. Source history stays here,
not in Djot notes or comments.

- `~/nsh/MARKDOWN_BOOKS/inheritance_genetics/Essential_Genetics_and_Genomics-2020.md`, chapter 4,
  the comparison of observed recombination with map distance (lines 3778-3802), and double
  recombinants contributing to both adjacent intervals (lines 3886-3944).
- `~/nsh/MARKDOWN_BOOKS/genetics/Genetics_Analysis_of_Genes_and_Genomes-2019.md`, section 5.3
  (lines 2166-2173): arbitrary table order versus solved chromosome order, parental comparison,
  and inclusion of double recombinants in both interval counts.
- `~/nsh/MARKDOWN_BOOKS/inheritance_genetics/Genetics_A_Conceptual_Approach-Pierce-2012.md`,
  section 7.3: paired allele comparisons clarify the effect of double recombination.
- `~/nsh/MARKDOWN_BOOKS/genetics_history/The_Gene_An_Intimate_History-2017.md`, Sturtevant account
  (lines 978-984), considered for the evidence-to-linear-map narrative; no history detour added.
- SVG skill local references: `A_Handbook_of_Biological_Illustration-1988.md`, "Clarity" and
  "Emphasis and Comparison"; `Mastering_SVG-2018.md`, "viewBox and viewport in SVG". Apply
  simple comparison geometry, minimal detail, and fixed coordinate systems.

### Validation

Strict native Jotdown/structural lint passes: 49 slides, 12 images. The typography audit has
no findings. The only capacity advisories remain the unchanged shared roadmaps at 19.75 pt
versus the 20 pt advisory floor (slides 6, 20, 29). This revision changes content and assets,
not renderer code or source syntax.

The generator's independent solver and a separate pair-projection calculation confirm every
recombinant set and percentage. One-time checks cover counts in all progeny tables, progress
reveal timing, original-parent and P/R colors, covered columns, three matching answers, and the
absence of the full progeny table after calculations. Both solved map assets use the 30:20
ratio. All SVGs validate and are embedded verbatim in the ODP; source fills preserve each base
color's hue and saturation within RGB rounding. Reviewed the actual exported PDF, including
all matching reminders, pair calculations, and the ending's mechanism and count explanation.

Evidence: `_temp/bpw_larger_gap_example.json`, `_temp/bpw_example_source_evidence.txt`,
`_temp/bpw_example_authored_map.txt`, `_temp/bpw_gap_audit.json`, `_temp/bpw_gap_review/`,
and canonical output ODP/PDF. Temporary helpers are authoring aids only. Djot and SVG files
remain the canonical inputs. Earlier review findings below are historical.

## Typography audit follow-up

October 26 follow-up to the conversion review below:

| Warning | Before source edits | After source edits | After final-paragraph exemption |
| --- | --- | --- | --- |
| Title wrap | 53 | 0 | 0 |
| Runt | 62 | 54 | 39 |
| URL too wide | 3 | 3 | 3 |
| Total | 118 | 57 | 42 |

Shortened 53 content titles, preserving the mapping questions, allele combinations, color spans,
and scientific meaning. Shortened four generated key-takeaway bullets in C, D, and F. Original
body prose, URLs, slide sequence, hidden states, and all 48 replacement markers remain unchanged.
Fifteen remaining final-paragraph runts at the maximum body font size are now exempt by instructor
request; this is an audit policy change, not a visual repair.

All six decks pass strict native Djot lint and rebuild to diagnostic ODP/PDF. All 170 content
titles are present on one line in the fresh LibreOffice PDFs. The remaining 39 runts and three
URLs need individual review; the URLs exceed their regions even at 12 pt.

Evidence: `_temp/lect08_audit_before.json` and `_temp/lect08_audit_cleanup/` (source snapshots,
after-edit and after-policy audits, diagnostic ODP/PDF, and title verification).
[Representative preview](../../../output/pdf/lect08_audit_cleanup_preview.pdf) includes two pages
per deck. Canonical lecture outputs and the older full-review PDF have not been replaced;
the conversion review below describes that earlier render and is superseded here for typography.

## Final checklist review

Reviewed October 26, 2026 after the shared sizing, course subsection color, image-relative cover,
and labeled-image changes. All 250 visible pages were inspected in 34 diagnostic contact sheets;
original B-F pages were paired through the source map. A uses the maintained 2026 announcement
inventory, not the obsolete 2025 announcement deck. All 14 hidden states remain unchanged.

**Replacement markers: 99 before this pass, 48 after (51 cleared).** This is a reviewed conversion
with specific unresolved drafts, not a claim that all slides are classroom ready.

| Deck | Authored | Visible | Hidden | Replacement markers |
| --- | --- | --- | --- | --- |
| lect08a-2026_announcements.djot | 38 | 25 | 13 | 0 |
| lect08b-chap8-linked_genes.djot | 44 | 44 | 0 | 12 |
| lect08c-gene_mapping.djot | 49 | 48 | 1 | 5 |
| lect08d-3_point_testcross_voss.djot | 47 | 47 | 0 | 17 |
| lect08e-linked_gene_chi_square.djot | 28 | 28 | 0 | 2 |
| lect08f-3_point_testcross_textbook.djot | 58 | 58 | 0 | 12 |

Totals: 264 authored / 250 visible / 14 hidden / 48 replacements. Every original B-F source slide
still maps one-to-one to its conversion. No source slide was split, reordered, or newly hidden.

### Source inventory

Original content decks in `genetics/LECT08/`:

| Source ODP stem | Authored | Hidden source slides | Source animation slides |
| --- | --- | --- | --- |
| lect08b-chap8-linked_genes | 41 | none | 35 |
| lect08c-gene_mapping | 46 | 2 | 17, 20, 45 |
| lect08d-3_point_testcross_voss | 44 | none | none |
| lect08e-linked_gene_chi_square | 25 | none | none |
| lect08f-3_point_testcross_textbook | 54 | none | 20, 27, 28, 29, 53 |

B6's click-to-remove cover follows explicit instructor intent; its original ODP retains the
rectangle but has no source animation entry. Native reveal verification is recorded separately.
Previous schedule evidence is the [Fall 2026 Genetics schedule](https://vosslab.github.io/syllabus/fall_2026/genetics/SCHEDULE/),
with Chapter 8 from the [BPW Genetics index](https://biologyproblems.org/genetics/).
These external facts were not refreshed in this pass.

### Repairs and marker decisions

- Restore 52 static diagram groups: C27-39, D5-22, F13-16/F31/F33-35/F37-49. Single-image
  figures preserve source masks and highlights in one quality-90 WebP background with live SVG
  labels. Existing vector tables stay vector with live visible text and source overlays.
  Six of these retain markers for mixed figure/calculation sizing: C31/C35/C39 and D10/D16/D22.
- Preserve paint order: hidden vector-table text stays beneath the opaque column mask. Include
  the full extents of associated masks and diagram marks, and exclude overlapping title lines.
  Titles, surrounding explanations, legends, and D/C calculation text remain native Djot.
- B25's predictions/results become a native table. C18's existing map resolves a stale warning.
- Clear B6/C20/C45 after static and native reveal-target/order verification. B6 also has the
  existing LibreOffice save-roundtrip evidence. Actual attended click playback remains untested.
  B35, C17, and F53 still lose source interaction behavior and remain marked.
- B36 used a different meiosis illustration; restore the correct source artwork. Its labels remain
  native, and its marker stays because label/product alignment still needs work.
- Demote remaining figure-number headings to native captions. Preserve instructor title wording;
  wrapping scientific titles remain a recorded presentation concern, not authority to rewrite them.
- Shorten only the five generated objective slides for line balance. Preserve instructor prose,
  data, equations, phenotype labels, existing tables, teaching sequence, and course color roles.
- B13 retains its existing two-over-one composition and mixed-readability warning. B2/B40 retain
  the dense incremental Mendel checklists. No sizing safeguards were weakened to reduce markers.

### Verification and artifacts

- Strict native Jotdown/semantic lint passes all six decks. All six native ODPs and ODP-derived
  PDFs rebuild. ODP page counts, visible PDF counts, hidden states, and explicit/physical marker
  counts reconcile. There are no additional automatic replacement watermarks.
- Capacity inspection reports 27 concerns: 15 mixed-readability, 11 text-sizing, and one mixed-flow.
  Mixed-readability failures remain marked; existing minor text-sizing findings are documented.
- The 52 remaining wrapping content titles are recorded in `_temp/lect08_full_review/title_wraps.json`.
  Retitling instructor prose remains a separate decision; all five generated objective slides now
  render with one line per bullet.
- 184 focused parser, SVG, metafile, layout, capacity, native-export, image-cover, and ODP tests pass.
  Static repairs introduce no new renderer options, layouts, or dependencies.
- [Full source/render review PDF](../../../output/pdf/lect08_full_review.pdf) includes every visible
  page. Diagnostic inspection views omit watermarks and label unresolved pages explicitly.
- Current slides: `output/odp/<deck stem>.odp` and `output/pdf/<deck stem>.pdf` for all six decks.
  Source-number mapping: [LECT08_SLIDE_MAP.md](LECT08_SLIDE_MAP.md).
- Asset provenance/bounds: `assets/static_figure_repairs.json` and `assets/labeled_figures.json`.
  Evidence, all-page contact sheets, capacity/build/test logs, and final inventory:
  `_temp/lect08_full_review/`. Original ODP/PDF inputs remain unchanged in `genetics/LECT08/`.
- This is a conversion/layout review, not a new weekly announcement refresh. Reuse the earlier
  October 27 schedule/chapter/episode selection evidence; no podcast, external URLs, authenticated
  course links, QR scanning, or assessment dates were refreshed in this pass.
- Source C15 still says 2% cross-over frequency while its figure reports 1% recombination. Preserve
  this source discrepancy for instructor clarification rather than changing the science.

### Remaining source slides

- LECT08B: 2, 7, 9, 13, 15, 16, 17, 18, 30, 35, 36, 40.
- LECT08C: 6, 17, 31, 35, 39.
- LECT08D: 10, 16, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37.
- LECT08E: 19, 24.
- LECT08F: 5, 18, 19, 20, 21, 22, 23, 24, 25, 50, 51, 53.

The tables below retain the specific missing feature or sizing finding for each unresolved slide.
Announcements retain 13 hidden authored slides; C retains its original hidden source slide 2.

## Completed checklist

The checklist below is copied from the current shared checklist. Checked items record performed
checks or reuse of the existing inventory/import evidence; they do not imply zero unresolved slides.
Recurring weekly-update tasks are N/A for this same-lecture conversion review. For the animation
item, target/order and static checks were performed; attended playback is explicitly unperformed.

## Inventory the inputs

- [x] List every source ODP and existing Djot deck in the review report; identify the version
  being converted and the canonical announcement deck before copying or importing anything.
- [x] Record each source deck's authored slide count, hidden slide numbers, section order,
  and slides with animations or answer reveals.
- [x] Generate or locate a source PDF for visual comparison. Map source slide numbers to
  visible PDF pages, explicitly accounting for hidden slides.
- [x] Record the lecture date and the schedule/spreadsheet used for weekly updates, including
  its path or URL. Identify the instructor-cleaned announcement deck used as a format example.

## Initial conversion and assembly

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
- [x] Compare important terminology with previous lectures and locate existing definitions.
  If useful, add a definitions slide near the beginning for important terms new to the lecture
  sequence. Keep definitions concise and limited to terms used in the lecture; list the added
  slide in the slide map.
- [x] Locate the closing summary in each content deck. If absent, add content-derived
  takeaways immediately before THE END; verify the closing slide order in the PDF.
- [x] Check section boundaries against the existing lecture outline. Insert missing dividers
  only to label existing topic boundaries, without reorganizing the teaching sequence;
  list any inserted dividers in the slide map.

## Recurring lecture announcement updates

N/A for this pass: previously reviewed selections and dates were retained.


- N/A: Replace the copied agenda with this lecture's topics and activities; compare each agenda
  item with the content decks and current course schedule.
- N/A: Check every assessment and assignment date against the schedule/spreadsheet. Update
  relative wording, deadline/status colors, and expired assignment entries for the lecture date.
- N/A: Compare announcement visibility with this week's plan. Record every changed hidden flag;
  confirm evergreen Discord information remains even when its signup assignment expires.
- N/A: Select the week's icebreaker explicitly from `icebreakers.yaml` or an instructor selection.
  Copy its prompt/examples and remove any stale week/date label; record the selected catalog key.
- N/A: Preview the StVC refresh with
  `source source_me.sh && python3 tools/refresh_podcast.py DECK.djot`.
  Inspect the selected episode before applying `--write`.
- N/A: Confirm the latest published StVC episode available on the lecture date and use it as the
  default selection. Record the selected episode number; if another episode is more appropriate,
  select it and document why.
- N/A: Verify the saved StVC episode number/title, video URL, thumbnail, and playable game/tool
  URL all refer to the selected episode. Open both links and inspect the downloaded image.
- N/A: Inspect the rendered StVC slide: confirm three caption lines, visible clickable video
  and game/tool URLs, and placement immediately after the YouTube channel slide.
- N/A: Check the YouTube channel, anonymous-message, Discord, and applicable Zoom slides.
  Verify their images/QR codes and visible clickable URLs; keep private course URLs in
  `course_links.local.yaml` through `{{course_url:key}}` references.

## Repair individual slides

- [x] Compare every source slide with its rendered conversion, including slides without importer
  warnings. Record missing text, labels, objects, emphasis, and changed reading order by slide.
- [x] Inspect the content underneath existing replacement watermarks using separate diagnostic
  copies. Reassess the actual failure rather than inheriting an old import warning. Keep diagnostic
  copies clearly labeled; removing a watermark for inspection does not clear the canonical marker.
- [x] Check that slide titles are actual headings, not promoted figure-number captions. Keep
  figure references with their diagrams.
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
- [x] Compare source animation targets/order with the converted reveals. Inspect final PDF states
  and test click playback in Impress for affected slides, or explicitly record playback as untested.
- [x] For each unresolved slide, add or retain `@replaceme` and record its source number, specific
  missing feature, and next action. When readable sizing cannot fit, retain the source slide with
  `@replaceme`, the preferred outcome over splitting. Do not make splitting the default repair;
  any split requires human approval.
- [x] Before clearing any replacement marker, compare the repaired render with the original and
  verify the previously missing content or behavior; record the evidence in the review report.

## Build and hand off

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

## LECT08B findings

| Source slide | Comparison | Finding |
| --- | --- | --- |
| 1 | improved | Standard title layout; same topic, canonical chapter and current lecture metadata. |
| 2 | roughly equivalent content; readability flagged | Instructor confirms an incremental checklist with accumulating exceptions, mostly equivalent to source. Converted text measures 15.75 pt; retain @replaceme pending readable reconstruction and reveal verification. Shorter exception prose is an option for review. |
| 3 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 4 | repaired; marker cleared | Single-image WebP/SVG restores positioned labels and diagram relationships. Static source comparison and native capacity/build pass; replacement marker removed. |
| 5 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 6 | native reveal repaired; marker cleared | Static source comparison, native on-click target/order, and relevant exporter tests verify the intended reveal. Attended Impress playback remains untested; this alone is not a missing conversion feature. |
| 7 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 8 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 9 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 10 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 11 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 12 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 13 | sizing repaired; capacity flagged | Shared font-size/width optimization selects 20 pt definitions with larger trimmed diagram views. Original prose and associations survive; the conservative image-reduction diagnostic remains, so retain the replacement marker. See sizing review PDF. |
| 14 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 15 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 16 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 17 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 18 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 19 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 20 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 21 | repaired; marker cleared | Single-image WebP/SVG restores positioned labels and diagram relationships. Static source comparison and native capacity/build pass; replacement marker removed. |
| 22 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 23 | repaired; marker cleared | Single-image WebP/SVG restores positioned labels and diagram relationships. Static source comparison and native capacity/build pass; replacement marker removed. |
| 24 | repaired; marker cleared | Single-image WebP/SVG restores positioned labels and diagram relationships. Static source comparison and native capacity/build pass; replacement marker removed. |
| 25 | repaired; marker cleared | Native table restores predicted ratios 1:1:1:1 and 1:1:0:0 against results 965/944/206/185; original conclusion retained. |
| 26 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 27 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 28 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 29 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 30 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 31 | repaired; marker cleared | Single-image WebP/SVG restores positioned labels and diagram relationships. Static source comparison and native capacity/build pass; replacement marker removed. |
| 32 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 33 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 34 | repaired; marker cleared | Single-image WebP/SVG restores positioned labels and diagram relationships. Static source comparison and native capacity/build pass; replacement marker removed. |
| 35 | static repaired; interaction pending | Single-image WebP/SVG restores positioned labels and diagram relationships. Retain @replaceme for interaction verification. |
| 36 | artwork corrected; flagged | Earlier conversion used a different meiosis image. Correct horizontal source artwork restored; native product labels still need closer spatial alignment, so retain @replaceme. |
| 37 | repaired; marker cleared | Single-image WebP/SVG restores positioned labels and diagram relationships. Static source comparison and native capacity/build pass; replacement marker removed. |
| 38 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 39 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 40 | materially worse; flagged | Dense summary list renders at 14.5 pt. Four-panel trial remains below readable size; retain @replaceme and the source exceptions until a readable same-slide reconstruction is available. |
| 41 | roughly equivalent | Existing theend layout preserves the authored closer and native star. |

## LECT08C findings

| Source slide | Comparison | Finding |
| --- | --- | --- |
| 1 | improved | Standard title layout; same topic, canonical chapter and current lecture metadata. |
| 2 | hidden; structural review | Original internal note and hidden status retained; no source PDF page. |
| 3 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 4 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 5 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 6 | materially worse; flagged | Image audit reports 53-56% area loss for text-heavy fragments. Two-panel trial is worse; retain original four-panel draft and retain @replaceme; try editable text/table reconstruction within the original slide. |
| 7 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 8 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 9 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 10 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 11 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 12 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 13 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 14 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 15 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 16 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 17 | static repaired; interaction pending | Single-image WebP/SVG restores positioned labels and diagram relationships. Retain @replaceme for interaction verification. |
| 18 | roughly equivalent; marker cleared | The chromosome map and equation are already present; fresh source/render comparison resolves the old geometry warning. |
| 19 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 20 | native reveal repaired; marker cleared | Static source comparison, native on-click target/order, and relevant exporter tests verify the intended reveal. Attended Impress playback remains untested; this alone is not a missing conversion feature. |
| 21 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 22 | repaired; marker cleared | Single-image WebP/SVG restores positioned labels and diagram relationships. Static source comparison and native capacity/build pass; replacement marker removed. |
| 23 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 24 | repaired; marker cleared | Single-image WebP/SVG restores positioned labels and diagram relationships. Static source comparison and native capacity/build pass; replacement marker removed. |
| 25 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 26 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 27 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 28 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 29 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 30 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 31 | static repaired; capacity flagged | Single-image SVG restores source static highlights/masks and overlapping labels. Native calculation text still triggers mixed-readability; retain @replaceme. |
| 32 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 33 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 34 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 35 | static repaired; capacity flagged | Single-image SVG restores source static highlights/masks and overlapping labels. Native calculation text still triggers mixed-readability; retain @replaceme. |
| 36 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 37 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 38 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 39 | static repaired; capacity flagged | Single-image SVG restores source static highlights/masks and overlapping labels. Native calculation text still triggers mixed-readability; retain @replaceme. |
| 40 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 41 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 42 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 43 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 44 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 45 | native reveal repaired; marker cleared | Static source comparison, native on-click target/order, and relevant exporter tests verify the intended reveal. Attended Impress playback remains untested; this alone is not a missing conversion feature. |
| 46 | roughly equivalent | Existing theend layout preserves the authored closer and native star. |

## LECT08D findings

| Source slide | Comparison | Finding |
| --- | --- | --- |
| 1 | improved | Standard title layout; same topic, canonical chapter and current lecture metadata. |
| 2 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 3 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 4 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 5 | repaired; marker cleared | Source vector table, visible cell text, highlights, and opaque column mask restored. Source/render comparison verifies the repair; no source animation is present. |
| 6 | repaired; marker cleared | Source vector table, visible cell text, highlights, and opaque column mask restored. Source/render comparison verifies the repair; no source animation is present. |
| 7 | repaired; marker cleared | Source vector table, visible cell text, highlights, and opaque column mask restored. Source/render comparison verifies the repair; no source animation is present. |
| 8 | repaired; marker cleared | Source vector table, visible cell text, highlights, and opaque column mask restored. Source/render comparison verifies the repair; no source animation is present. |
| 9 | repaired; marker cleared | Source vector table, visible cell text, highlights, and opaque column mask restored. Source/render comparison verifies the repair; no source animation is present. |
| 10 | static repaired; capacity flagged | Source vector table, visible cell text, highlights, and opaque column mask restored. Native calculation text still triggers mixed-readability; retain @replaceme. |
| 11 | repaired; marker cleared | Source vector table, visible cell text, highlights, and opaque column mask restored. Source/render comparison verifies the repair; no source animation is present. |
| 12 | repaired; marker cleared | Source vector table, visible cell text, highlights, and opaque column mask restored. Source/render comparison verifies the repair; no source animation is present. |
| 13 | repaired; marker cleared | Source vector table, visible cell text, highlights, and opaque column mask restored. Source/render comparison verifies the repair; no source animation is present. |
| 14 | repaired; marker cleared | Source vector table, visible cell text, highlights, and opaque column mask restored. Source/render comparison verifies the repair; no source animation is present. |
| 15 | repaired; marker cleared | Source vector table, visible cell text, highlights, and opaque column mask restored. Source/render comparison verifies the repair; no source animation is present. |
| 16 | static repaired; capacity flagged | Source vector table, visible cell text, highlights, and opaque column mask restored. Native calculation text still triggers mixed-readability; retain @replaceme. |
| 17 | repaired; marker cleared | Source vector table, visible cell text, highlights, and opaque column mask restored. Source/render comparison verifies the repair; no source animation is present. |
| 18 | repaired; marker cleared | Source vector table, visible cell text, highlights, and opaque column mask restored. Source/render comparison verifies the repair; no source animation is present. |
| 19 | repaired; marker cleared | Source vector table, visible cell text, highlights, and opaque column mask restored. Source/render comparison verifies the repair; no source animation is present. |
| 20 | repaired; marker cleared | Source vector table, visible cell text, highlights, and opaque column mask restored. Source/render comparison verifies the repair; no source animation is present. |
| 21 | repaired; marker cleared | Source vector table, visible cell text, highlights, and opaque column mask restored. Source/render comparison verifies the repair; no source animation is present. |
| 22 | static repaired; capacity flagged | Source vector table, visible cell text, highlights, and opaque column mask restored. Native calculation text still triggers mixed-readability; retain @replaceme. |
| 23 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 24 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 25 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 26 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 27 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 28 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 29 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 30 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 31 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 32 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 33 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 34 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 35 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 36 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 37 | materially worse; flagged | Source grid lost its row/column relationships. |
| 38 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 39 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 40 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 41 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 42 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 43 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 44 | roughly equivalent | Existing theend layout preserves the authored closer and native star. |

## LECT08E findings

| Source slide | Comparison | Finding |
| --- | --- | --- |
| 1 | improved | Standard title layout; same topic, canonical chapter and current lecture metadata. |
| 2 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 3 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 4 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 5 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 6 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 7 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 8 | improved; second pass | Native phenotype-row table restores original labels, question marks, ratios, and counts. |
| 9 | improved; second pass | Native nested lists restore chromosome-location/ratio associations. |
| 10 | improved; second pass | Native phenotype-row table restores counts and the Genes Unlinked annotation. |
| 11 | improved | Editable native table preserves source numbers, blanks, incremental completion and total. |
| 12 | improved | Editable native table preserves source numbers, blanks, incremental completion and total. |
| 13 | improved | Editable native table preserves source numbers, blanks, incremental completion and total. |
| 14 | improved | Editable native table preserves source numbers, blanks, incremental completion and total. |
| 15 | improved | Editable native table preserves source numbers, blanks, incremental completion and total. |
| 16 | improved | Editable native table preserves source numbers, blanks, incremental completion and total. |
| 17 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 18 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 19 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 20 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 21 | improved | Editable native table preserves source numbers, blanks, incremental completion and total. |
| 22 | improved; second pass | Native scaled-data table restores source labels, blank calculation cells, and original sentence. |
| 23 | improved | Editable native table preserves source numbers, blanks, incremental completion and total. |
| 24 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 25 | roughly equivalent | Existing theend layout preserves the authored closer and native star. |

## LECT08F findings

| Source slide | Comparison | Finding |
| --- | --- | --- |
| 1 | improved | Standard title layout; same topic, canonical chapter and current lecture metadata. |
| 2 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 3 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 4 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 5 | materially worse; flagged | Image audit reports 54.61% area loss; chromosome labels and result counts are too small. Retain @replaceme until the diagram and explanation can remain readable together on the original slide. |
| 6 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 7 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 8 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 9 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 10 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 11 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 12 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 13 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 14 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 15 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 16 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 17 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 18 | materially worse; flagged | Source grid lost its row/column relationships. |
| 19 | materially worse; flagged | Source grid lost its row/column relationships. |
| 20 | materially worse; flagged | Source reveal/mask sequence is unresolved; static PDF is insufficient. |
| 21 | materially worse; flagged | Source grid lost its row/column relationships. |
| 22 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 23 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 24 | materially worse; flagged | Source grid lost its row/column relationships. |
| 25 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 26 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 27 | roughly equivalent | Existing two-over-one layout; source answer restored as an on-click appear reveal. |
| 28 | roughly equivalent | Existing two-over-one layout; source answer restored as an on-click appear reveal. |
| 29 | roughly equivalent | Existing two-over-one layout; source answer restored as an on-click appear reveal. |
| 30 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 31 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 32 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 33 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 34 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 35 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 36 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 37 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 38 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 39 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 40 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 41 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 42 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 43 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 44 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 45 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 46 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 47 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 48 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 49 | repaired; marker cleared | Single-image SVG restores source static highlights/masks and overlapping labels. Source/render comparison verifies the repair; no source animation is present. |
| 50 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 51 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 52 | repaired; marker cleared | Single-image WebP/SVG restores positioned labels and diagram relationships. Static source comparison and native capacity/build pass; replacement marker removed. |
| 53 | static repaired; interaction pending | Single-image WebP/SVG restores positioned labels and diagram relationships. Retain @replaceme for interaction verification. |
| 54 | roughly equivalent | Existing theend layout preserves the authored closer and native star. |


## Colored procedure recaps

The original LECT08D ODP slide 3 and original PDF page 3 show black procedure text.
The new canonical six-step roadmap uses the fixed palette in rainbow order:
red, dark orange, dark yellow, green, blue, purple. Step 2 references match dark orange.
The separate DCO roadmap uses red, green, blue, purple to keep its four phases distinct.

The original F ODP slide 9 has essentially the same six-step wording as D, with a red
heading and black steps; its quick DCO procedure is a separate four-step method.
Both shared roadmap titles are now black to emphasize the colored steps.

LECT08D uses four six-step recaps: before the worked problem, at the A-C and B-C
pair transitions, and before the group activity. LECT08F uses six: before the main
example, before each of three quick gene-order exercises, before genotype summaries,
and before map-distance calculations. The separate quick DCO recaps remain available.
All occurrences use shared includes, and the source maps reflect the added positions.
The six-step body fits at 19.75 pt; existing unrelated reconstruction and capacity
warnings remain in the source decks.

## Negative deviations and chi-square notation

Negative deviations now use mathematical minus signs and align at the right edge with
positive values. Numeric alignment also recognizes legacy en-dash negatives. Replace
legacy Symbol-font chi characters, and use math-rendered chi-square sum labels to keep
them visibly distinct from Latin X. Rebuilt LECT08E and inspected PDF page 16; all 67
layout-engine tests pass, including ASCII, Unicode minus, and entity-encoded negatives.

The first shared six-step roadmap now appears in LECT08C immediately before Pandora
Plant Inheritance: roadmap PDF page 26, Pandora page 27. Subsequent D/F recaps use
the same canonical source and colors.

### Middle-gene framing

Slide 39 now presents all three possible middle genes and their equivalent reversed orders.
The D-H result prompts the choice before slide 40 reveals C. The deck remains 49 slides;
11 SVGs are referenced, with the earlier endpoint SVG retained as an unused source asset.
