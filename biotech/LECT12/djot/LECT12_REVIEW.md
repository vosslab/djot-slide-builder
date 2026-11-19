# BIOL 480 lecture 12 review

Teaching date: Thursday, November 19, 2026. The current Fall 2026 BIOL 480
schedule, Projects page, and Talking Points page set the dates, requirements,
and 60-second speaking limit.

## 12A announcements

- Rolled forward the instructor's [11A deck](../../LECT11/djot/lect11a-2026_biotech_announcements.djot).
  Compared the November 2025 Lecture 12A PDF, whose breakout asked about project choice.
  That product discussion now appears in 12B.
- The Week 12 announcement deck has the Nov 19 Company Vision Report and Homework 6.
  Nov 26 is Thanksgiving break. Dec 3 has Group Project Discussion, BioTech News #2,
  and Homework 7. The news preparation slide is visible.
- The Nov 19 NWS Chicago forecast immediately precedes the icebreaker.
- Students choose a cyborg upgrade and share how they would use it aloud or in
  the Zoom chat. The Fall 2026 announcement sources and the previous-year 12A
  breakout were checked for repeats.
- Used Stump the Vibe Coder #39, Red Dead Cell Counter. Its feed description contains
  two project links, so the automatic refresh refused to choose. The link explicitly
  labeled Project was verified against the playlist. On Nov 18, fetched the revised
  Western-clothing thumbnail from YouTube and verified it on PDF page 9 and in the ODP.
- Used Veridian Dynamics #11, Good / Bad, from the local episode transcript and
  existing course logo. The talking-mark screenshot, completed signup reminder,
  dormant club announcement, and unconfirmed evaluations remain hidden.
- Replaced the Biotechnology instructor-contact copy with the
  [shared evergreen group](../../../evergreen/instructor_contact.djot). All eight Fall
  2026 Biotechnology announcement decks now include the same Office Hours slide.
  Early decks retain their dated Discord signup slides and visibility. Verified PDF
  contact order, identical Office Hours renders, and distinct office-hours and classroom
  Zoom destinations. The shared Ways to Contact slide still reports a 19.5 pt advisory
  against the 20 pt floor.

## 12B group project

- Rolled forward the [11B guide](../../LECT11/djot/lect11b-2026_group_project.djot).
  Compared the 2025 12B guide in LECT11/old and followed the Nov 19 stage in the
  [group project progression](../../GROUP_PROJECT_PROGRESSION.md).
- Product choice and one Company Vision Report due Nov 19 lead the guide. The form
  stays on Blackboard. The project discussion connects the choice to the biological mechanism,
  market, competition, group contributions, and a concrete milestone.
- Show the two presentation rubric images from the instructor's Fall 2026 Group Project
  ODP. They carry the group scoring, including three points for timing. The complete
  seven-part business-plan rubric follows. Presentations are Dec 10 and the business
  plan is due Dec 17.
  Prerecording/upload, peer evaluation, and final logistics stay hidden for this week.

### Refresh the presentation rubric

Update the two rubric images in the instructor's ODP. The refresh copies the PNG bytes in
slide order from the two pages captioned **Presentation Rubric**. Run from the repository root:

```bash
source source_me.sh && python3 biotech/LECT12/djot/refresh_presentation_rubric.py \
  "$HOME/Documents/teaching/CLASS/biol_480-biotech/2026-BioTech-2fall/LECTURES-2026/lect11b-2026_group_project.odp"
```

Build the editable ODP, then export the classroom PDF at the rubric images' native
resolution. The standard PDF build downsamples images to 100 ppi. Run the LibreOffice
command outside the sandbox.

```bash
source source_me.sh
python3 deck_tools.py build --format odp biotech/LECT12/djot/lect12b-2026_group_project.djot
mkdir -p output/pdf
soffice_bin="$(python3 -c 'from slide_lib.libreoffice import require_soffice; print(require_soffice())')"
"$soffice_bin" --headless --norestore --convert-to \
  'pdf:impress_pdf_Export:{"UseLosslessCompression":{"type":"boolean","value":"true"},"ReduceImageResolution":{"type":"boolean","value":"false"},"ExportHiddenSlides":{"type":"boolean","value":"false"},"ExportNotes":{"type":"boolean","value":"false"},"ExportNotesPages":{"type":"boolean","value":"false"},"ExportOnlyNotesPages":{"type":"boolean","value":"false"},"SelectPdfVersion":{"type":"long","value":"3"}}' \
  --outdir output/pdf output/odp/lect12b-2026_group_project.odp
```

If the ODP rubric is redesigned as native slide shapes or text, use a slide export for that layout.

## 12C talking points

The [Set 7 topic guide](SET7_TOPIC_GUIDE.md) has PDF page ranges for all 41 topics,
a short list of pages to pull up in class, and links to the data behind the figures.
The Fall 2026 shared student deck holds presenter assignments and individual talks.

### Drawn SVG canvas audit

All 40 Set 7 `.drawn.svg` figures were cropped to their painted content with a small
clearance for labels, strokes, and arrowheads. The audit found 12 opaque canvas fills in
two batches of evidence figures:

- `set7_human_outcomes/` used a pale blue `#f8fbfd` rectangle behind all five figures
  (`bci_speed`, `cell_to_person`, `claim_ladder`, `kidney_waitlist`, and
  `organex_timeline`).
- `set7_reproduction_evidence/` used a pale gray `#f8fafb` rectangle behind all seven
  figures (`art_infants_2010_2021`, `cell_sources`, `consent_map`, `evidence_compare`,
  `mei_public_record`, `screen_compare`, and `somatic_compare`). The public-record
  timeline rounded the corners of that same canvas fill.

Both batches explicitly painted these backdrops in their SVG source. The other 28 drawings
already had transparent canvases. The crop and background removal preserved all editable
foreground elements. All 40 images were verified in the rebuilt 406-page PDF. The three
drawing recipes in this lecture use the
[shared normalizer](../../../docs/slide-specs/SVG_DIAGRAMS.md#normalize-a-drawn-svg)
when regenerating their assets.

## November 19 classroom edition

- Expanded the 303-slide draft to 400 slides, then added six bonus slides after Topic 23.
  The 406-page PDF has 102 figure slides, including
  county maps, primary-source micrographs, photos, experimental diagrams, and time series.
  Archival portraits and case photographs now illustrate 38 previously text-only slides.
  All 41 numbered topics open with the Fall 2026 discussion questions.
- Checked source credits on the new photos and charts. The deck includes 315 source
  footers. Each external target in a source footer appears as a link on the same PDF page.
- Checked all 406 PDF pages for selectable text and page bounds, compared the page order
  with the topic map, and matched every source image to the bytes embedded in the ODP.
  Reviewed the PDF contact sheets for the revised charts and all 38 new photo slides.
- Strict Djot lint and the Set 7 capacity check passed. The classroom deck has no
  capacity advisories. A separate check of the original 15.25 pt Genetics caption
  confirms the new 15 pt advisory floor. Short captions still use 22 pt.
- The focused parser, link, slide-lint and layout checks passed all 207 tests. The isolated
  full-suite run passed 10,211 tests. Three pre-existing checks still fail: type annotations
  and script entry-point conventions in the original Set 7 drawing recipe, and a missing
  test-file link in the chromosome SVG plan.
- The earlier 303-slide draft had 22 figures and 254 citation footers.
  Its review files are in `_temp/set7_revision/`. Review files for the 400-slide
  edition are in `_temp/set7_expansion/` and `_temp/set7_people/`. The six bonus
  pages and their editable table were checked in `_temp/set7_bonus/`.

## Artifact verification

| Deck | Authored slides | Hidden | Classroom PDF pages |
| --- | ---: | ---: | ---: |
| 12A Announcements | 47 | 7 | 40 |
| 12B Group Project Guide | 41 | 6 | 35 |
| 12C Bioethics in Biotechnology | 406 | 0 | 406 |

- Strict Jotdown and repository slide lint passed for all three masters.
- LibreOffice exported all three PDFs from the editable ODP artifacts. Reviewed contact
  sheets for all visible pages and inspected the source figures at larger size.
- ODP package checks passed. The PDFs matched ODP visibility, all visible PDF pages
  contained selectable text, and no extracted words exceeded the page bounds.
  Checked the announcement media link targets and the PDF order of all 41 Set #7 topics.
- The November 18 build reported capacity advisories in inherited announcement/project material
  and four talking-point setup slides. The two presentation rubric SVGs stay sharp at PDF zoom.
- In the November 18 review, the focused suite passed 241 tests. The base suite passed
  10,278 tests and reported four ASCII failures in
  existing Set #7 text exports. The base suite auto-normalized six historical/current
  text snapshots. Verified that the shared fixers explained the changes and restored
  all six source files to their original bytes.
- Live Impress playback and Blackboard access were not tested. Build logs, visual
  checks, and the machine-readable receipt are in `_temp/biotech_lect12/`.
