# Slide conversion checklist

This checklist governs conversion of existing lectures, not pedagogical redesign. Follow
[HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md) when preserving existing content and sequence.
Adding missing learning objectives, a closing summary, and an optional definitions slide for
terms used in the lecture is explicitly authorized. Other substantive instructional changes
require separate authorization.

Any slide splitting requires human approval. Keep existing content slides one-to-one with their
source slides; authorized opening and closing additions may shift numbering.

Managers must complete this checklist for each conversion and subsequent conversion review.
Copy it into the lecture's review report. Check successful routine items without extra evidence.
Record findings and evidence for failures, repairs, unresolved conversions, and significant
decisions; mark inapplicable items `N/A` with a reason. Identify affected source decks and slide
numbers. A checked review item may retain a documented `@replaceme`.

For initial conversion, complete all sections. For recurring lecture updates, refresh the
announcements and repeat the affected inventory, repair, build, and handoff checks; reuse the
existing slide map and import artifacts.

For content policy, consult [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md). For slide construction,
consult [the pedagogical guide](PEDAGOGICAL_SLIDE_STYLE_GUIDE.md) and
[Djot syntax](DJOT_SLIDE_SYNTAX.md). Commands below run from the repository root; replace
`LECTURE_DIR`, `SOURCE.odp`, and `DECK.djot` with actual paths. Run commands that can launch
LibreOffice outside the sandbox on this Mac, including imports and builds.

## Inventory the inputs

- [ ] List every source ODP and existing Djot deck in the review report; identify the version
  being converted and the canonical announcement deck before copying or importing anything.
- [ ] Record each source deck's authored slide count, hidden slide numbers, section order,
  and slides with animations or answer reveals.
- [ ] Generate or locate a source PDF for visual comparison. Map source slide numbers to
  visible PDF pages, explicitly accounting for hidden slides.
- [ ] Record the lecture date and the schedule/spreadsheet used for weekly updates, including
  its path or URL. Identify the instructor-cleaned announcement deck used as a format example.

## Initial conversion and assembly

- [ ] Import each source with the repository importer documented in [USAGE.md](USAGE.md).
  Save the generated Djot, component assets, and import report; list their paths in the review.
  For an existing conversion, locate these artifacts instead of overwriting reviewed source.
- [ ] Build a source-to-Djot slide map. Account for every source slide, its relative order,
  and hidden status; verify one-to-one correspondence through existing content and list added
  slides separately so counts reconcile. Record human approval for any source-slide splitting.
- [ ] Update each cover's course, lecture number, date, and topic. Check the rendered cover
  against the cover requirements in the pedagogical guide.
- [ ] Verify each cover's chapter number against the relevant BPW course index linked from
  [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md). Do not infer it from the lecture number;
  announcements have no chapter.
- [ ] Locate the learning objectives in each content deck. If absent, add content-derived
  objectives on slide 2; record the resulting slide number.
- [ ] Compare important terminology with previous lectures and locate existing definitions.
  If useful, add a definitions slide near the beginning for important terms new to the lecture
  sequence. Keep definitions concise and limited to terms used in the lecture; list the added
  slide in the slide map.
- [ ] Locate the closing summary in each content deck. If absent, add content-derived
  takeaways immediately before THE END; verify the closing slide order in the PDF.
- [ ] Check section boundaries against the existing lecture outline. Insert missing dividers
  only to label existing topic boundaries, without reorganizing the teaching sequence;
  list any inserted dividers in the slide map.

## Recurring lecture announcement updates

- [ ] Replace the copied agenda with this lecture's topics and activities; compare each agenda
  item with the content decks and current course schedule.
- [ ] Check every assessment and assignment date against the schedule/spreadsheet. Update
  relative wording, deadline/status colors, and expired assignment entries for the lecture date.
- [ ] Compare announcement visibility with this week's plan. Record every changed hidden flag;
  confirm evergreen Discord information remains even when its signup assignment expires.
- [ ] Select the week's icebreaker explicitly from `icebreakers.yaml` or an instructor selection.
  Copy its prompt/examples and remove any stale week/date label; record the selected catalog key.
- [ ] Preview the StVC refresh with
  `source source_me.sh && python3 tools/refresh_podcast.py DECK.djot`.
  Inspect the selected episode before applying `--write`.
- [ ] Confirm the latest published StVC episode available on the lecture date and use it as the
  default selection. Record the selected episode number; if another episode is more appropriate,
  select it and document why.
- [ ] Verify the saved StVC episode number/title, video URL, thumbnail, and playable game/tool
  URL all refer to the selected episode. Open both links and inspect the downloaded image.
- [ ] Inspect the rendered StVC slide: confirm three caption lines, visible clickable video
  and game/tool URLs, and placement immediately after the YouTube channel slide.
- [ ] Check the YouTube channel, anonymous-message, Discord, and applicable Zoom slides.
  Verify their images/QR codes and visible clickable URLs; keep private course URLs in
  `course_links.local.yaml` through `{{course_url:key}}` references.

## Repair individual slides

- [ ] Compare every source slide with its rendered conversion, including slides without importer
  warnings. Record missing text, labels, objects, emphasis, and changed reading order by slide.
- [ ] For sequential text/image content split across panels, try the existing one-panel mixed
  flow and compare the render. Keep the grouping with readable labels and correct reading order;
  record unresolved fit failures rather than adding a special layout.
- [ ] Run the [image-area audit](USAGE.md#audit-image-shrinkage) for matching source/conversion
  slides. Inspect flagged shrinkage and record the chosen repair or retained review reason;
  after slide insertions, use the source map rather than assuming page numbers still align.
- [ ] Compare every table's headers, values, totals, blank calculation cells, and progressive
  steps with the source. Rebuild representable tables as native tables and inspect their PDF.
- [ ] Inspect rendered equations and genetic notation against the source: fractions, chi-square,
  allele superscripts, generation subscripts, and H~0~. Correct misplaced or baseline characters.
- [ ] Compare source animation targets/order with the converted reveals. Inspect final PDF states
  and test click playback in Impress for affected slides, or explicitly record playback as untested.
- [ ] For each unresolved slide, add or retain `@replaceme` and record its source number, specific
  missing feature, and next action. When readable sizing cannot fit, retain the source slide with
  `@replaceme`, the preferred outcome over splitting. Do not make splitting the default repair;
  any split requires human approval.
- [ ] Before clearing any replacement marker, compare the repaired render with the original and
  verify the previously missing content or behavior; record the evidence in the review report.

## Build and hand off

- [ ] Run `source source_me.sh && python3 deck_tools.py lint --require-native
  --native-executable "$(command -v jotdown)" LECTURE_DIR` as one command.
  Save its result and resolve parser/semantic errors.
- [ ] Run `source source_me.sh && python3 deck_tools.py capacity LECTURE_DIR`.
  Inspect each diagnostic and record a repair or slide-specific unresolved finding.
- [ ] Run `source source_me.sh && python3 deck_tools.py build LECTURE_DIR --format all`
  outside the sandbox. Confirm an editable ODP and ODP-derived PDF exist for every deck.
- [ ] Inspect every visible PDF page against the source using
  [the visual review rubric](SLIDE_VISUAL_REVIEW_RUBRIC.md) as assessment guidance. Inspect dense
  text, small diagram labels, tables, and repaired slides at readable size; record problems and
  repairs, then rerender and recheck subsequent edits. Routine conversion review does not require
  per-slide numerical scores; the separate scored review is advisory and runs on demand.
- [ ] Reconcile final ODP authored counts and PDF visible counts with the slide map, hidden flags,
  and added slides. Count remaining replacement markers per deck and list their source numbers.
- [ ] Finish the lecture review report with output paths, validation results, repaired slides,
  unresolved slides, and unperformed checks. Distinguish reviewed draft completion from
  classroom readiness when replacement slides remain.
- [ ] Add a concise conversion/review entry to [CHANGELOG.md](CHANGELOG.md), naming the lecture
  and resulting artifacts; report the review and output paths to the instructor.
