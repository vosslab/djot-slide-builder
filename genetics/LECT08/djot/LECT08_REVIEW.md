# Lecture 08 conversion review

Converted and reviewed again October 26, 2026. Originals remain unchanged one directory above.
The six Djot sources use existing layouts. This second pass applies the updated prose-preservation
policy and adds missing instructional bookends from the existing lecture content.
Content covers use the October 27, 2026 lecture date and Chapter 8, verified
against the [BPW Genetics index](https://biologyproblems.org/genetics/).

## Checklist acceptance pass

Completed October 26, 2026 against [the reusable checklist](../../../docs/SLIDE_CONVERSION_CHECKLIST.md).
This is completed conversion review with documented replacement drafts, not classroom readiness.
No existing prose, scientific claims, source sequence, or visibility was changed in this pass.
Every original B-F slide remains one-to-one with its converted slide. No source slides were split.
Retaining `@replaceme` is preferred over splitting. Any split requires human approval.
Four additional source slides now explicitly carry `@replaceme`: B2/B40, C6, and F5.
The final inventory is 264 authored / 250 visible / 14 hidden / 109 replacement slides.

### Audit results and decisions

- The durable [slide map](LECT08_SLIDE_MAP.md) accounts for every original B-F slide,
  inserted objectives/dividers/takeaways, final authored/PDF numbering, and hidden status.
  A retains the maintained 2026 LECT07 Djot inventory and its 13 hidden slides.
- Original PDFs and ODPs are in `genetics/LECT08/`; reports and component assets remain in
  `genetics/LECT08/djot/assets/<source deck stem>/`. The previous all-page source comparison
  remains applicable: this pass changes only four replacement markers, not content or geometry.
- BPW's Genetics index reconfirms Chapter 8: Gene Mapping. The published Fall 2026 Genetics
  schedule, drawn from the instructor's linked spreadsheet, reconfirms October 27, Gene Distances,
  and November 3 Quiz 3 / assignments 07-08:
  [BPW index](https://biologyproblems.org/genetics/) and
  [course schedule](https://vosslab.github.io/syllabus/fall_2026/genetics/SCHEDULE/).
- Earlier terminology is covered in LECT04-07; B defines linked genes and cis/trans, C introduces
  mapping, recombination frequency, parental types, and map units, and D/F apply those terms.
  Existing definitions are retained. An optional additional definitions slide was not needed.
- Fresh podcast preview safely stopped because the newest episode lacks a unique playable-project
  URL. No source was overwritten. The instructor's explicit one-week choice of episode 37 remains;
  episode 38 is the newer special episode. Both saved video and game URLs return HTTP 200.
  The saved thumbnail, three-line caption, and position directly after the channel slide match.
  Evergreen/private link references and administrative visibility remain unchanged; authenticated
  Discord access and live QR scanning were not tested.
- The aligned image-area audit uses temporary copies containing only source-mapped slides, so
  inserted slides cannot shift comparisons. It examined 147 source-artwork records. Native-table
  reconstructions and SVG replacements require manual matching rather than matching image hashes.
  Twenty-four previously unmarked source-slide pairs were inspected at larger size. E8/E10-16/
  E21-23 and D2/D4 retain editable/native equivalents; C16 and F2/F26 retain matching replacements.
  B29/B32, C15, F6/F8/F36 retain readable source relationships despite measured area reductions.
  C6 and F5 fail label readability and now remain explicitly marked. See source-number findings.
- B2/B40 require 15.75/14.5 pt. A four-panel trial did not solve the fit, so both now retain
  replacement markers. Retain these drafts rather than splitting; no source prose was shortened.
- Remaining unmarked capacity diagnostics: A6's caption 15.25 pt (visually checked, no clipping);
  C5 body 18.25 pt; D5 and F11 body 19.75 pt; E11 table/text 19.75 pt. Body values exceed HG's
  usually acceptable 17 pt threshold. All mixed-readability failures remain marked.
- Source C15's title says "2% cross-over frequency" while its figure says 1% recombination.
  This source wording is retained; instructor clarification is needed before changing the science.
- Final strict Jotdown/semantic lint passes. Capacity inspection reports 56 concerns, handled
  above or by the source-specific replacement findings. All six final ODP/PDF decks rebuild.
  The 75 existing cover tests pass. Authored/visible/hidden counts are checked against both formats.
- Evidence: `_temp/lect08_checklist/` contains image audit JSON, source inventory, paired image
  comparisons, lint/capacity/build logs, and cover-test results. Earlier all-page contact sheets,
  mixed-flow trials, table checks, and reveal evidence are in `_temp/lect08_second_pass/`.
  Output files are `output/odp/<Djot stem>.odp` and `output/pdf/<Djot stem>.pdf` for all six decks.
- Attended Impress click playback remains untested. F27-29 retain native appear targets;
  other unresolved source reveal/overlay slides remain marked. No new tests, compiler changes,
  layouts, or permanent podcast exceptions were introduced.

### Source animation inventory

- `lect08b-chap8-linked_genes.odp`: 41 authored; animation containers on source slides 35.
- `lect08c-gene_mapping.odp`: 46 authored; animation containers on source slides 17, 20, 45.
- `lect08d-3_point_testcross_voss.odp`: 44 authored; animation containers on source slides none.
- `lect08e-linked_gene_chi_square.odp`: 25 authored; animation containers on source slides none.
- `lect08f-3_point_testcross_textbook.odp`: 54 authored; animation containers on source slides 20, 27, 28, 29, 53.

### Completed task list

Checkboxes record performed checks; unresolved results and unperformed interactive checks are
explicitly recorded above and in the source-number findings. No check implies zero warnings.

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

- [x] Import each source with the repository importer documented in [USAGE.md](USAGE.md).
  Save the generated Djot, component assets, and import report; list their paths in the review.
  For an existing conversion, locate these artifacts instead of overwriting reviewed source.
- [x] Build a source-to-Djot slide map. Account for every source slide, its relative order,
  and hidden status; verify one-to-one correspondence through existing content and list added
  slides separately so counts reconcile. Record human approval for any source-slide splitting.
- [x] Update each cover's course, lecture number, date, and topic. Check the rendered cover
  against the cover requirements in the pedagogical guide.
- [x] Verify each cover's chapter number against the relevant BPW course index linked from
  [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md). Do not infer it from the lecture number;
  announcements have no chapter.
- [x] Locate the learning objectives in each content deck. If absent, add content-derived
  objectives on slide 2; record the resulting slide number.
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
- [x] For sequential text/image content split across panels, try the existing one-panel mixed
  flow and compare the render. Keep the grouping with readable labels and correct reading order;
  record unresolved fit failures rather than adding a special layout.
- [x] Run the [image-area audit](USAGE.md#audit-image-shrinkage) for matching source/conversion
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

### Build and hand off

- [x] Run `source source_me.sh && python3 deck_tools.py lint --require-native
  --native-executable "$(command -v jotdown)" LECTURE_DIR` as one command.
  Save its result and resolve parser/semantic errors.
- [x] Run `source source_me.sh && python3 deck_tools.py capacity LECTURE_DIR`.
  Inspect each diagnostic and record a repair or slide-specific unresolved finding.
- [x] Run `source source_me.sh && python3 deck_tools.py build LECTURE_DIR --format all`
  outside the sandbox. Confirm an editable ODP and ODP-derived PDF exist for every deck.
- [x] Inspect every visible PDF page against the source using
  [the visual review rubric](SLIDE_VISUAL_REVIEW_RUBRIC.md) as assessment guidance. Inspect dense
  text, small diagram labels, tables, and repaired slides at readable size; record problems and
  repairs, then rerender and recheck subsequent edits. Routine conversion review does not require
  per-slide numerical scores; the separate scored review is advisory and runs on demand.
- [x] Reconcile final ODP authored counts and PDF visible counts with the slide map, hidden flags,
  and added slides. Count remaining replacement markers per deck and list their source numbers.
- [x] Finish the lecture review report with output paths, validation results, repaired slides,
  unresolved slides, and unperformed checks. Distinguish reviewed draft completion from
  classroom readiness when replacement slides remain.
- [x] Add a concise conversion/review entry to [CHANGELOG.md](CHANGELOG.md), naming the lecture
  and resulting artifacts; report the review and output paths to the instructor.


## Source selection

- B-F come from the corresponding original ODPs, retaining all 210 slides and
  the one hidden C slide. Per-slide import evidence is under `assets/<deck>/import_report.json`.
- A reuses the maintained LECT07 2026 Djot announcements and its local assets,
  following HG rather than converting the obsolete 2025 announcements.
- A now has the October 27 linked-genes/mapping agenda and the explicitly selected
  `modify-an-animal` icebreaker from `icebreakers.yaml`, with its inherited Week 6 label removed.
  The 2026 schedule confirms Quiz 3 and Weeks 07-08 homework on November 3. Their existing red
  status colors are correct; the stale note saying no assessment was due next week is corrected.
- StVC episode 37, published October 22, replaces episode 36: updated video, thumbnail, and
  playable Bad Cell Day link, with the required three-line caption directly after the YouTube
  channel slide. The instructor explicitly selected 37 because 38 is a special episode.
  This is a one-week choice, not a permanent change to the refresh script.
- Evergreen announcements, private link references, the 13 hidden administrative slides,
  and the hidden C source note remain intact.

## Second-pass changes

- Add learning objectives on slide 2 and penultimate key takeaways to B-F, using each deck's
  own content and the pedagogical slide style guide. Add four missing opening dividers and
  Summary dividers to E/F. Existing summary/reference material remains before the takeaways.
- All 210 original science slides remain in their original relative sequence. 205 original
  slide blocks are unchanged; four E slides are source-faithful reconstructions and the E cover
  gains the required parenthesized chi-square notation. A per-slide
  word-token comparison retains 99.93% of prior native prose, excluding added bookends,
  image alt text, and importer-generated reconstruction placeholders. This comparison against
  the first-pass Djot is a preservation check, not proof that flagged source content is complete.
- Reconstruct original E8 and E10 as editable tables, transposed into phenotype rows for
  readable headers. Preserve all labels, 900 totals, question marks, ratios, and counts.
  E10 retains the original "Genes Unlinked" annotation below its table.
- Restore E9's chromosome-location/ratio associations with two native nested-list groups.
  Restore E22's scaled-data table and original concluding sentence with native table/text flow.
  These four source slides no longer need replacement markers. E19/E24 remain marked because
  their distribution-table highlights and surrounding source details are still unresolved.
- Evaluate all four stacked mixed-content candidates. Three still fail shared readability
  bounds; E22's larger-area candidate still lacked table labels until reconstructed. Do not
  clear diagram/spatial/reveal markers merely because one-panel placement increases area.
- The current policy/checklist comes from `docs/HUMAN_GUIDANCE.md` and the historical
  `docs/ANNOUNCEMENT_REVIEW_2026_10_20.md`; the reusable conversion checklist now supplies the actionable announcement tasks.

## Verification

- Strict Jotdown parsing and semantic lint pass for all six sources.
- All six covers pass the existing HG cover checker.
- Repository builds produce six editable ODPs and six LibreOffice-derived PDFs.
  LibreOffice runs outside the sandbox.
- ODP slide counts and PDF visible-page counts match Djot: 264 authored,
  250 visible, 14 hidden. The original content PDFs provide 209 source pages; 16 inserted
  bookend/divider slides account for the current 225 visible B-F pages.
- Original/generated B-F contact sheets were compared for all visible pages;
  repaired pages were rendered again. Original source C2 remains hidden as current slide C4, retaining its internal note.
- Eight previously reconstructed chi-square tables retain the source numeric values and blank cells.
  Three additional native tables and the ratio-list reconstruction restore four more source slides.
  The calculation-table headers use stacked equation fractions; each total has a separate final row.
- F27-29 source XML identifies the answer paragraphs as on-click appear targets.
  Existing three-panel layouts now carry corresponding native appear reveals.
  Their ODP timing metadata was checked; attended Impress playback was not performed.
- One-time checks, build logs, preservation mapping, candidate measurements, and final WebP
  contact sheets are in `_temp/lect08_second_pass/`. All 250 final visible pages received a
  contact-sheet check; changed bookends, announcements, and tables were inspected at larger size.
  The 75 existing cover checks pass, and the playable-project URL returns HTTP 200.
  Existing refresh/lint/capacity/build scripts were reused; no permanent tests or compiler/script
  changes were added.

## Remaining limitations

Replacement markers denote representation failures, not requests to rewrite content.
Source table highlights, column masks, connected chromosome diagrams, and unsupported
animations remain visibly flagged. The 109 flagged drafts are not ready for classroom use.
Some retain only partial native content; use their original ODP and import evidence
when reconstructing them. No whole-slide screenshots replace editable slide content.

Original source C6 and image-heavy F5 retain smaller figures than their originals. Dense text slides
retain their authored wording and can require smaller type (notably the repeated Mendel-principles
pages). The E10 table/text flow renders at 19.75 pt; the three-line StVC caption renders at
15.25 pt and retains an existing caption-floor warning. Capacity warnings remain
in the build log; unresolved low-capacity diagram slides retain their replacement marks.

## Deck inventory

| Deck | Authored | Visible | Replacement marks |
| --- | --- | --- | --- |
| [lect08a-2026_announcements.djot](lect08a-2026_announcements.djot) | 38 | 25 | 0 |
| [lect08b-chap8-linked_genes.djot](lect08b-chap8-linked_genes.djot) | 44 | 44 | 21 |
| [lect08c-gene_mapping.djot](lect08c-gene_mapping.djot) | 49 | 48 | 20 |
| [lect08d-3_point_testcross_voss.djot](lect08d-3_point_testcross_voss.djot) | 47 | 47 | 32 |
| [lect08e-linked_gene_chi_square.djot](lect08e-linked_gene_chi_square.djot) | 28 | 28 | 2 |
| [lect08f-3_point_testcross_textbook.djot](lect08f-3_point_testcross_textbook.djot) | 58 | 58 | 34 |

## LECT08B findings

| Source slide | Comparison | Finding |
| --- | --- | --- |
| 1 | improved | Standard title layout; same topic, canonical chapter and current lecture metadata. |
| 2 | materially worse; flagged | Dense original list renders at 15.75 pt. Four-panel trial remains below readable size; retain @replaceme and all prose until a readable same-slide reconstruction is available. |
| 3 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 4 | materially worse; flagged | Positioned labels and their diagram relationships need reconstruction. |
| 5 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 6 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 7 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 8 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 9 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 10 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 11 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 12 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 13 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 14 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 15 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 16 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 17 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 18 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 19 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 20 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 21 | materially worse; flagged | Source grid lost its row/column relationships. |
| 22 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 23 | materially worse; flagged | Source grid lost its row/column relationships. |
| 24 | materially worse; flagged | Positioned labels and their diagram relationships need reconstruction. |
| 25 | materially worse; flagged | Source grid lost its row/column relationships. |
| 26 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 27 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 28 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 29 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 30 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 31 | materially worse; flagged | Positioned labels and their diagram relationships need reconstruction. |
| 32 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 33 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 34 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 35 | materially worse; flagged | Positioned labels and their diagram relationships need reconstruction. |
| 36 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 37 | materially worse; flagged | Positioned labels and their diagram relationships need reconstruction. |
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
| 17 | materially worse; flagged | Positioned labels and their diagram relationships need reconstruction. |
| 18 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 19 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 20 | materially worse; flagged | Source reveal/mask sequence is unresolved; static PDF is insufficient. |
| 21 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 22 | materially worse; flagged | Positioned labels and their diagram relationships need reconstruction. |
| 23 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 24 | materially worse; flagged | Positioned labels and their diagram relationships need reconstruction. |
| 25 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 26 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
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
| 37 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 38 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 39 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 40 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 41 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 42 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 43 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 44 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 45 | materially worse; flagged | Source reveal/mask sequence is unresolved; static PDF is insufficient. |
| 46 | roughly equivalent | Existing theend layout preserves the authored closer and native star. |

## LECT08D findings

| Source slide | Comparison | Finding |
| --- | --- | --- |
| 1 | improved | Standard title layout; same topic, canonical chapter and current lecture metadata. |
| 2 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 3 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 4 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 5 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 6 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 7 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 8 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 9 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 10 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 11 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 12 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 13 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 14 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 15 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 16 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 17 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 18 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 19 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 20 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 21 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 22 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
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
| 13 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 14 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 15 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 16 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
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
| 31 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 32 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 33 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 34 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 35 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 36 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 37 | materially worse; flagged | Column mask is missing; the censored gene remains visible. |
| 38 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 39 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 40 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 41 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 42 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 43 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 44 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 45 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 46 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 47 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 48 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 49 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 50 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 51 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 52 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 53 | materially worse; flagged | Source reveal/mask sequence is unresolved; static PDF is insufficient. |
| 54 | roughly equivalent | Existing theend layout preserves the authored closer and native star. |
