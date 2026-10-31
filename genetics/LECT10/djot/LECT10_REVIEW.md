# Lecture 10 conversion review

Reviewed conversion draft, October 31, 2026. Replacement markers are intentional unresolved
conversion or source-content findings; these decks are not yet classroom-ready replacements.
Original ODP/PDF files remain unchanged in the lecture directory.

## Canonical decks

| Djot | Authored | Visible PDF | Hidden | Replacement markers |
| --- | --- | --- | --- | --- |
| [lect10a-2026_announcements.djot](lect10a-2026_announcements.djot) | 43 | 29 | 14 | 0 |
| [lect10b-karyotypes.djot](lect10b-karyotypes.djot) | 52 | 52 | 0 | 20 |
| [lect10c-chromo_nomenclature.djot](lect10c-chromo_nomenclature.djot) | 22 | 22 | 0 | 10 |
| [lect10d-chromo_aneuploid.djot](lect10d-chromo_aneuploid.djot) | 58 | 58 | 0 | 19 |

The [LECT10_SOURCE_MAP.md](LECT10_SOURCE_MAP.md) accounts for every source content slide,
all additions, the PDF page correspondence, and announcement include ownership.
Import evidence and extracted components are in `assets/<content-deck>/import_report.json`.

## Input inventory

| Original ODP | Authored | Source-hidden slides | Source animation slides | Source PDF pages |
| --- | --- | --- | --- | --- |
| `lect10a-2025_announcements.odp` | 62 | [2, 4, 5, 11, 12, 14, 16, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 38, 39, 40, 41, 43, 44, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61] | none | 25 |
| `lect10b-karyotypes.odp` | 50 | none | [8, 16] | 50 |
| `lect10c-chromo_nomenclature.odp` | 19 | none | none | 19 |
| `lect10d-chromo_aneuploid.odp` | 55 | none | [10, 39, 40] | 55 |

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

## Weekly announcements

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

## Repairs and review findings

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

Source-content decisions still needed: Karyotypes source 12 repeats the questionable
"euchromatin is visible only after chromosome condensation" wording; source 46's HPV statistics
and historical vaccine language were not modernized. Aneuploidy source 15's absolute survival
claim conflicts with source 11, and source 38 labels monosomic/trisomic zygotes as n - 1/n + 1.
Retain the wording for an instructor decision and mark the directly identified contradictions.
Medical percentages, screening recommendations, incidence data, and historical narratives were
preserved from the source, not fact-checked or updated as clinical guidance.

## Unresolved source slides

For each row, compare the source and diagnostic render; restore the missing geometry, labels,
mask, or instructional emphasis in native Djot or a bounded figure. Keep the marker until that
specific repair has a successful source/render comparison. Source-content contradictions require
the instructor's decision before rewriting. No slide split is proposed or performed.

| Deck | Source | Djot | Import reason / review evidence |
| --- | --- | --- | --- |
| `lect10b-karyotypes` | 3 | 4 | unsupported source object draw:custom-shape requires reconstruction |
| `lect10b-karyotypes` | 5 | 6 | normalized sole material interior overlay label into native source-order content; unrecognized source text color #563a84 requires review; unsupported source object draw:custom-shape requires reconstruction |
| `lect10b-karyotypes` | 6 | 7 | dense text requires post-conversion polish; mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized distributed pictorial annotations into native source-order content; regular text lattice requires border and span reconstruction; unrecognized source text color #e97200 requires review; unsupported source object draw:custom-shape requires reconstruction; unsupported source object draw:line requires reconstruction |
| `lect10b-karyotypes` | 7 | 8 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized distributed pictorial annotations into native source-order content; unrecognized source text color #563a84 requires review; unsupported source object draw:custom-shape requires reconstruction; unsupported source object draw:line requires reconstruction |
| `lect10b-karyotypes` | 8 | 9 | normalized single connected materially coupled visual graph into native source-order content; source text animation is not preserved by the selected layout |
| `lect10b-karyotypes` | 9 | 10 | source object crosses physical page bounds; unsupported source object draw:custom-shape requires reconstruction |
| `lect10b-karyotypes` | 10 | 11 | unrecognized source text color #666666 requires review; unrecognized source text color #b2b2b2 requires review |
| `lect10b-karyotypes` | 11 | 12 | source object crosses physical page bounds; unsupported source object draw:custom-shape requires reconstruction |
| `lect10b-karyotypes` | 12 | 13 | Manual visual/content review: inspect the finding below before classroom use. |
| `lect10b-karyotypes` | 13 | 14 | source object crosses physical page bounds; unsupported source object draw:custom-shape requires reconstruction |
| `lect10b-karyotypes` | 16 | 17 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized overlapping legacy components into one native source-order panel; normalized single connected materially coupled visual graph into native source-order content; source text animation is not preserved by the selected layout |
| `lect10b-karyotypes` | 17 | 18 | unrecognized source text color #512480 requires review; unrecognized source text color #579835 requires review; unrecognized source text color #c38312 requires review |
| `lect10b-karyotypes` | 18 | 19 | source object crosses physical page bounds; unsupported source object draw:custom-shape requires reconstruction |
| `lect10b-karyotypes` | 24 | 25 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized overlapping legacy components into one native source-order panel |
| `lect10b-karyotypes` | 26 | 27 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized distributed pictorial annotations into native source-order content; unrecognized source text color #563a84 requires review; unsupported source object draw:custom-shape requires reconstruction; unsupported source object draw:line requires reconstruction |
| `lect10b-karyotypes` | 29 | 30 | metafile SVG has no live text; review bitmap content or glyph outlines; unsupported source object draw:frame requires reconstruction |
| `lect10b-karyotypes` | 30 | 31 | metafile SVG has no live text; review bitmap content or glyph outlines; unsupported source object draw:frame requires reconstruction |
| `lect10b-karyotypes` | 37 | 38 | unsupported source object draw:custom-shape requires reconstruction |
| `lect10b-karyotypes` | 38 | 39 | source object crosses physical page bounds |
| `lect10b-karyotypes` | 41 | 42 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized distributed pictorial annotations into native source-order content; source object crosses physical page bounds |
| `lect10c-chromo_nomenclature` | 2 | 4 | native annotations could not be assigned to exactly one image |
| `lect10c-chromo_nomenclature` | 3 | 5 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized overlapping legacy components into one native source-order panel; unsupported source object draw:custom-shape requires reconstruction |
| `lect10c-chromo_nomenclature` | 4 | 6 | Manual visual/content review: inspect the finding below before classroom use. |
| `lect10c-chromo_nomenclature` | 5 | 7 | source object crosses physical page bounds; unsupported source object draw:custom-shape requires reconstruction |
| `lect10c-chromo_nomenclature` | 6 | 8 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized overlapping legacy components into one native source-order panel; source object crosses physical page bounds; unsupported source object draw:custom-shape requires reconstruction |
| `lect10c-chromo_nomenclature` | 7 | 9 | normalized single connected materially coupled visual graph into native source-order content; source object crosses physical page bounds; unsupported source object draw:custom-shape requires reconstruction |
| `lect10c-chromo_nomenclature` | 9 | 11 | normalized single connected materially coupled visual graph into native source-order content |
| `lect10c-chromo_nomenclature` | 10 | 12 | unsupported source object draw:custom-shape requires reconstruction |
| `lect10c-chromo_nomenclature` | 15 | 17 | normalized ambiguous topology bounds [NormalizedBounds(left=0.049999999999999996, top=0.23394285714285717, right=0.9499642857142857, bottom=0.870857142857143), NormalizedBounds(left=0.33999999999999997, top=0.8533142857142857, right=0.64, bottom=0.9466285714285715)] into one native source-order panel |
| `lect10c-chromo_nomenclature` | 16 | 18 | normalized ambiguous topology bounds [NormalizedBounds(left=0.049999999999999996, top=0.23394285714285717, right=0.9499642857142857, bottom=0.870857142857143), NormalizedBounds(left=0.3400357142857143, top=0.8533714285714286, right=0.6400357142857144, bottom=0.9466857142857142)] into one native source-order panel |
| `lect10d-chromo_aneuploid` | 9 | 11 | Manual visual/content review: inspect the finding below before classroom use. |
| `lect10d-chromo_aneuploid` | 10 | 12 | source animation for id1 requires review; source animation for id2 requires review; unsupported source object draw:custom-shape requires reconstruction |
| `lect10d-chromo_aneuploid` | 14 | 16 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels |
| `lect10d-chromo_aneuploid` | 15 | 17 | Manual visual/content review: inspect the finding below before classroom use. |
| `lect10d-chromo_aneuploid` | 19 | 21 | unrecognized source text color #00a933 requires review |
| `lect10d-chromo_aneuploid` | 27 | 29 | unrecognized source text color #168253 requires review |
| `lect10d-chromo_aneuploid` | 28 | 30 | 15 positioned labels require native redesign; dense text requires post-conversion polish; normalized distributed pictorial annotations into native source-order content; regular text lattice requires border and span reconstruction; unsupported source object draw:line requires reconstruction |
| `lect10d-chromo_aneuploid` | 29 | 31 | dense text requires post-conversion polish; mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized distributed pictorial annotations into native source-order content; regular text lattice requires border and span reconstruction; unsupported source object draw:line requires reconstruction |
| `lect10d-chromo_aneuploid` | 32 | 34 | dense text requires post-conversion polish; unrecognized source text color #168253 requires review; unrecognized source text color #b47804 requires review; unrecognized source text color #f10d0c requires review |
| `lect10d-chromo_aneuploid` | 35 | 37 | normalized distributed pictorial annotations into native source-order content; unsupported source object draw:line requires reconstruction |
| `lect10d-chromo_aneuploid` | 36 | 38 | mixed text/images cannot fit readability bounds in body; split this slide into separate slides or panels; normalized distributed pictorial annotations into native source-order content; unsupported source object draw:line requires reconstruction |
| `lect10d-chromo_aneuploid` | 37 | 39 | 16 positioned labels require native redesign; dense text requires post-conversion polish; normalized distributed pictorial annotations into native source-order content; regular text lattice requires border and span reconstruction; unsupported source object draw:line requires reconstruction |
| `lect10d-chromo_aneuploid` | 38 | 40 | Manual visual/content review: inspect the finding below before classroom use. |
| `lect10d-chromo_aneuploid` | 40 | 42 | normalized overlapping legacy components into one native source-order panel; source text animation is not preserved by the selected layout |
| `lect10d-chromo_aneuploid` | 42 | 44 | unrecognized source text color #00a933 requires review |
| `lect10d-chromo_aneuploid` | 43 | 45 | normalized overlapping legacy components into one native source-order panel; unrecognized source text color #cc00cc requires review |
| `lect10d-chromo_aneuploid` | 44 | 46 | unsupported source object draw:frame requires reconstruction |
| `lect10d-chromo_aneuploid` | 48 | 50 | unsupported source object draw:custom-shape requires reconstruction |
| `lect10d-chromo_aneuploid` | 50 | 52 | normalized single connected materially coupled visual graph into native source-order content |

## Validation and artifacts

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

## Final check results

Typography audit: {'runt': 3, 'title-wrap': 4}. No `url-too-wide` warnings remain.

Capacity summary: 20 concerns (mixed-readability=10, paragraph/list=10). Warnings remain documented; no automatic slide splitting is accepted.

- `lect10b-karyotypes_image_audit`: shrinkage source slides [5, 6, 7, 8, 16, 24, 25, 26, 39, 41]; changed/vector artwork requiring manual matching [29, 30].
- `lect10c-chromo_nomenclature_image_audit`: shrinkage source slides [2, 3, 4, 6, 8, 9, 10, 13]; changed/vector artwork requiring manual matching none.
- `lect10d-chromo_aneuploid_image_audit`: shrinkage source slides [3, 14, 28, 29, 31, 35, 36, 37, 48, 52]; changed/vector artwork requiring manual matching none.

Final outputs reconcile to the authored/visible/hidden counts in the deck table. Covers
contain selectable PDF text. Review preview: `_temp/lect09_10/final_preview.pdf` and
`final_preview_map.json`; the final quiz wording is rechecked in the rebuilt announcement PDFs.

## Conversion checklist

Checked items include documented unresolved findings; they do not certify marker-free output.
N/A: new three-point-testcross roadmaps (these are tetrad/interference and chromosome decks),
Zoom (Genetics has no course Zoom meeting), extra glossary additions, new reveals on static figures,
and clearing every marker. The source's five-step unordered-tetrad procedure is preserved twice;
it is distinct from the LECT08 six-step three-point-testcross roadmap. No new roadmap colors are invented.

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

## Recurring lecture announcement updates

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

## Repair individual slides

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
