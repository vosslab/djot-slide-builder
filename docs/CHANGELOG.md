## 2026-10-06

### Additions and New Features

- Import original GDI metafiles as SVG instead of preferring raster previews. Retain glyph text,
  table rules, and fills; surface conversion failures or absent live text for review.
- Replace Lecture 06D slides 13, 56, and 57 raster figure references with vector SVG exports.
  Preserve existing layouts and unresolved replacement markers.

- Add direct self-contained SVG sizing and ODP embedding, plus `image-comparison` with two
  diagrams above measured native captions. Document authoring in [SVG_DIAGRAMS.md](SVG_DIAGRAMS.md).
- Preserve definition-term bold and underline through import and export, with optional color.
- Repair 42 Lecture 06 replacement slides using original artwork, positioned labels, native
  captions, and editable tables. Retain 22 unresolved markers and the visible exam section.

- Convert Genetics Lecture 06 into five custom Djot decks with local component assets and
  source-slide notes. Preserve all 167 science slides in their original order.
- Restore visible midterm exam guidance; update announcements for October 6, assignments 4-5,
  Quiz 2, and the October 13 in-person exam covering Chapters 1-4.

### Fixes and Maintenance

- Preserve inherited frame/paragraph/span formatting, italic runs, explicit normal/none and color
  resets, and uppercase/lowercase source transformations. Retain otherwise unsupported source RGB
  colors in validated inline Djot spans, with existing review warnings instead of discarded hues.
- Restore confirmed emphasis losses in Lecture 06C, D, and E, including chromomeres, no consensus,
  parental phenotypes, sex-lethal/Sxl, and all-caps exceptions. Require LLM review to check formatting
  as well as wording. A focused import-to-native-export test covers combined styles and resets.

- Record reviewed `@replaceme` markers as acceptable conversion outcomes. Acceptance does not
  require eliminating every marker or forcing a reconstruction that loses teaching intent.

- Clarify that deterministic ODP import produces a draft requiring LLM evaluation against source
  slides and animation evidence before acceptance. Keep canonical Djot builds deterministic;
  document that the import CLI does not yet enforce this workflow automatically.

- Preserve source on-click text appearances through import planning. Recognize a question with
  one revealed answer using the existing multiple-choice layout; flag unsupported animation
  actions, targets, timing, and unmapped text reveals for review with `@replaceme`.
- Restore Lecture 06D slide 36's answer popup. Allow a single standalone question in the existing
  layout and measure answers in bold. Split slide 36's answer into two native paragraphs for fit.

- Correct observed LibreOffice SVG direction flags on Latin-only figures and remove its exact
  unused SVG DTD declaration before validation. Actual PDF inspection verified the genotype table.

- Use current ZipGrade wording and meeting time. Remove the obsolete blanket assignment deadline
  and unverified reopening claim. Recover native question/answer layouts and allele superscripts.
- Mark 64 slides needing diagram, relationship, color, or composition reconstruction with
  `@replaceme`; retain their source references and reconstruction evidence.

### Decisions and Failures

- LibreOffice image import requires desktop process access. Original 06D slides 58-60 exceed the
  native table-grid import contract; import question frames from a temporary copy and retain
  explicit replacement markers. Leave original presentations unchanged.

### Developer Tests and Notes

- Metafile vector work: 48 focused tests pass; live SVM conversion/import, strict Djot lint,
  byte-exact SVG packaging, and rendered PDF checks pass. EMF/WMF live acceptance remains untested.

- Track image-area regression using Lecture 06D slide 9: image coverage fell from 47.19% to
  12.13% of the slide. Add a non-blocking import audit and `image-audit` command after scope
  clarification; leave layouts and trimming unchanged. See
  [image_area_regression_followup.md](active_plans/image_area_regression_followup.md).
- Track vector-preserving GDI conversion and the current preference for raster previews in
  [metafile_vector_followup.md](active_plans/metafile_vector_followup.md).

- SVG/definition work: 143 focused tests pass; direct SVG payloads, aspect ratios, native caption
  geometry, and inherited/reset emphasis are covered. Full repository checks with cleanup disabled
  report 2328 passes and 44 existing hygiene failures; see the Lecture 06 review for categories.

- Strict Jotdown/semantic lint passes for five decks, 203 slides, and 115 image references.
  Capacity inspection reports no concerns. Build editable ODP and PDF, inspect contact sheets,
  and verify page counts, replacement warnings, source order, and visible exam guidance.
  All 80 Markdown-link checks pass.

## 2026-09-30

### Additions and New Features

- Add slide-level `@replaceme` metadata with a large editable red "REPLACE ME" watermark in ODP
  and PDF. Preserve original content and keep the warning visible on red and dark slide surfaces.
- Automatically mark newly imported slides with review reasons. Mark Biotechnology Lecture 05's
  hidden talking-marks image placeholder for instructor replacement.
- Convert Biotechnology Lecture 05 to three canonical Djot decks: announcements, individual
  project, and Theranos. Adapt the editable Lecture 04 sources and import the Theranos portraits
  and resource images; retain hidden material for later instructor show/hide changes.
- Update the visible decks to Oct 1, 2026 using the Fall 2026 course schedule. Restore the
  project-selection, executive-summary, and pitch guidance used in the prior Lecture 05.

### Behavior or Interface Changes

- Vary the image side in Biotechnology Lecture 05's two-panel slides. Alternate consecutive
  image/text slides using explicit `@left` and `@right` slots; record this as an authoring rule.
- Hide the completed Discord signup and Student Profile assignments after Sept 21. Retain
  Discord as a contact channel and keep the completed assignment slides editable in ODP.
- Use a distinct Biotechnology announcement filename so the shared output folder preserves
  the Genetics Lecture 05 announcements. Keep copied Set #3 decks as reference inputs.

### Fixes and Maintenance

- Split dense Theranos timelines and course links, restore readable project tables, and update
  obsolete trial and television-resource wording. Archive the old film-development announcement.
- Use current project dates and the published 88-point individual-project breakdown; replace
  the legacy point screenshot and keep student grade screenshots out of the classroom decks.
- Repair the Lecture 04 review's stale Proteomics source link. Rotate the Sept 28 and Sept 25
  entries into CHANGELOG-2026-09c.md to keep the two most recent day blocks active.

### Developer Tests and Notes

- Verify image-side variation with strict native lint, capacity inspection, and 81 Markdown-link
  checks. Rebuild the classroom decks and inspect the three changed pages. Confirm all 127 source
  slides preserve content, notes, and visibility, and consecutive image/text slides alternate.
- Verify the replacement marker with 122 focused parser/layout/import/export/lint tests and
  194 Pyflakes/Markdown-link checks. Build and visually inspect all 18 layouts with the warning;
  verify that hidden markers stay in ODP and out of PDF. Rebuild Lecture 05 announcements.
- The full pytest lane reports 2,373 passes and 16 existing hygiene failures in legacy text,
  old test/developer files, and oversized documentation. Restore its automatic normalization of
  initially clean source assets, including hash-pinned font licenses, before rendering acceptance.
- Validate all three Biotechnology Lecture 05 sources with strict native Jotdown lint and
  capacity inspection. Build three editable ODPs and three PDFs; verify exact hidden-page
  retention and 88 visible classroom pages. Render all classroom pages for visual review.
- The initial restricted LibreOffice PDF invocation exited with status -6. The unchanged folder
  build succeeds with desktop process access; no product-code workaround is required.
- Markdown link validation caught the stale Lecture 04 Proteomics path; repair it and rerun
  successfully. Keep the one-time source, visibility, and render checks in the ignored lane.

## 2026-09-29

### Additions and New Features

- Add deck-scoped `table-group` sizing: the compiler pools column needs across explicitly
  related tables before laying out slides, so later answer text informs earlier question widths.
  Replace 05D v2's four manual width lists with the `overlap-cross` group. Preserve independent
  automatic tables and optional manual proportions; reject conflicting modes or column counts.
  Verify adaptation to later edits, isolation across tables/builds, 126 focused tests, lint,
  capacity, and all four rendered PDF pages.
- Add optional table `column-widths` proportions with source validation and native measurement.
  Apply 1:3:3 widths to the 05D v2 overlap question, answer, double-count explanation, and callback.
  Verify all four PDF pages, lint/capacity, and 121 focused parser/layout/export tests.
- Add the `reference` one-panel layout with an unfilled light gray border behind editable
  text and an automatic "For reference - not covered in class." footer outside the body area.
  Apply it to the three 05D v2 study slides. Validate with 65 focused parser/layout/export tests,
  deck lint and capacity checks, and visual review of all three exported PDF pages.
- Add a textbook-inspired independence vote and Punnett-square answer to Lecture 05D v2:
  three aa offspring do not change the next offspring's probability for known Aa x Aa parents.
  Connect this to the conditioning warmup; the deck now has 45 slides and six MC checkpoints.
- Add deck-specific slide-2 objectives and final takeaways to Lectures 05B, C, E, F, G, and H,
  with instructor notes. Retain their existing review figures and replace THE END with a summary.
- Improve Lecture 05D v2 with illustrative pollen counts before normalization and a conditional
  probability vote plus answer: exclude aa, then count two Aa routes among three remaining.
  The revised deck has 43 slides and five multiple-choice checkpoints.
- Add a separate 41-slide Lecture 05D v2 with objectives, a final summary, and instructor notes.
  Preserve the opening challenge and addition-rule trap; replace textbook screenshots with
  editable questions, crosses, weighted Punnett squares, rule callbacks, and four MC checkpoints.
- Resolve the opening unequal-pollen problem as AA:Aa:aa = 1:3:2 and correct the family example's
  reversed conditional probability under explicit inheritance assumptions.

- Add optional `@notes` regions to every Djot slide layout. Plain instructor text ends at the next
  named slot or slide directive and exports through the existing native ODP speaker-note model.

### Behavior or Interface Changes

- Preserve semantic font roles in the backend: Atkinson Hyperlegible Next for ordinary text,
  Atkinson Hyperlegible Mono for inline code, and IBM Plex Sans Condensed for literal URLs.
  Replace PT Sans Narrow with IBM; bundle and hash-pin four real styles for each new family.
  Keep missing-glyph substitutions backend-owned and student-facing font advice unchanged.
- Preserve note line breaks and blank lines, decode character references once, and keep notes out
  of visible slide content. Explicitly exclude notes and notes pages from normal PDF export.
- Document notes syntax, examples, instructor guidance, and the native-notes design decision.

### Fixes and Maintenance

- Record the teaching value of visually distinct textbook problem statements. Preserve that
  cue when converting screenshots to editable text; leave the reusable layout design open.

- Rebuild Lecture 05D v2 as a 44-slide connected narrative, down from 58. Keep the four-allele
  cross through addition and multiplication, restore parent-to-gamete branching graphics, enlarge
  repeated Punnett squares, and explicitly return to solve the opening F2 pollen problem.
  Shorten conditional probability to one family story with a branching diagram; retain reverse
  conditioning and Bayes as study references. Add purpose/transition notes on the revised flow
  and preserve the prior source, ODP, and PDF under output/lect05d_before_narrative/.

- Add an Addition Rule section and convert the existing multiplication opener to a Multiplication
  Rule section in Lecture 05D v2. Add lighter subsection dividers for the pollen application,
  family example, and condition checks, with instructor notes. The deck now has 58 slides.

- Share URL fragmentation between measurement and export, preferring address separators over
  arbitrary letter splits. Measure and emit literal URLs 2 pt smaller in the condensed role.
  Put Lecture 05 destinations on separate lines and verify the rendered announcement/resource pages.

- Restore visible destination URLs beside link descriptions in Lecture 05 announcements and
  epistasis resources. Document visible URLs as the slide-authoring preference for destination
  inspection; use the existing backend-owned IBM Plex Sans Condensed role without font overrides.

- Embed original, hash-verified font bytes and public font families in generated ODPs instead
  of renamed Djot-prefixed derivatives. Preserve editable text, all styles, and bundled licenses;
  remove obsolete derivative hashes and test exact payload and public-name preservation.

- Restore direct condition-then-formula wording and Specific/General labels on Lecture 05D v2
  probability rule cards and summary references. Retain both multiplication orders and clarify
  that general rules also cover the special cases.

- Restore the 05D v2 opening problem's mutant-pollen context, prior-week F1-to-F2 connection,
  and explicit tasks to complete the Punnett square and predict the F2 genotype ratio.
  Carry generation labels into the callback, solved prediction, and study reference.
- Expand 05D v2's bare Addition opener with the blue union Venn diagram and a concrete
  counting prompt about outcomes shared by both events. Preserve the later overlap discovery;
  rebuild and visually check the revised slide, with passing lint and capacity checks.
- Add slide 3, "Probability speak," to 05D v2 before the opening section and challenge.
  Define event, P notation, general event labels, OR, AND, given, mutually exclusive, and
  independent. Use allele-based descriptions instead of B/C aliases in the worked cross.
  The deck now has 54 slides; lint/capacity and visual checks of five changed pages pass.
- Italicize visible allele and genotype symbols throughout 05D v2, including numbered alleles,
  Punnett squares, inheritance probabilities, and study references. Preserve rule colors and
  upright answer labels; check representative exported slides and deck lint/capacity.
- Visibly label the three longer 05D v2 study slides as for reference and not covered in class.
  Record this convention in the pedagogy guide; rebuild and visually check all three pages.
- Add colorful seedling and blossom emoji to five plant-example slides in Lecture 05D v2.
  Keep font selection backend-owned. Rebuild ODP/PDF and visually check all five changed pages;
  emoji render in color without clipping or new wrapping issues.
- Add a closing Summary section to 05D v2 with standalone Addition Rules and Multiplication
  Rules references, each collecting the earlier special and general forms with conditions.
  Keep the three study explanations and final takeaways before THE END. Document selective
  repetition of key slides for emphasis and easy homework lookup; the deck now has 53 slides.
- Restore visual event-set explanations in 05D v2 using four original SVG Venn diagrams:
  union, intersection, disjoint events, and double-counted overlap. Use them on the OR/AND
  comparison and three rule cards; retain the Punnett-square examples and 50-slide sequence.
  Embed 2400-pixel PNG exports because the current image measurement path cannot read SVG.
  Keep editable SVG sources beside those exports; no backend changes.
- Keep 05D v2 probabilities in fractions, removing percentage choices and callbacks. Expand
  compressed wording and add three labeled study-reference slides covering rule choice, the
  pollen calculation, and conditioning. The deck now has 50 slides, with summary and THE END
  still last. Document separate live-teaching and later-study needs in the pedagogy guide.
- Restore a separate THE END after each Lecture 05B-H summary. Add opening section headings
  to 05D v2 and 05F; give the original 05D objectives, an opening section heading, and a
  penultimate summary. Document the preferred content-deck sequence, including optional early
  vocabulary definitions. The revised 05D v2 now has 47 slides.
- Rewrite Lecture 05D v2's opening challenge as a complete, self-contained question with its
  assumptions visible. Clarify that full problem statements are an exception to the guide's
  preference for short slide phrases; keep hints and teaching commentary in notes.
- Use blue for addition/OR and orange for multiplication/AND across Lecture 05's authored
  rule labels, equations, worked steps, and summaries. Keep both general and special forms
  consistent, separate unrelated highlights, and retain biological figure colors.
- Make course title slides serve orientation: lecture identifier, subject, chapter, instructor,
  and teaching date. Replace the Lecture 05D v2 tagline with Chapter 5 and its teaching date;
  correct the other Lecture 05 covers' old chapter labels to Chapter 5.
- Give the shared title metadata frame no fill and preserve its stacking order below both
  editable text boxes, including after a LibreOffice save.
- Extend the pedagogical guide with plain-language guidance and an early-definition rule:
  check prior decks, define essential new jargon visibly in the first few slides, and retain
  technical terms when they improve precision. Add vocabulary checks to the slide checklist.
- Check plant-cross terminology against the local 2001 and 2012 genetics textbooks. Simplify
  Lecture 05D v2 slides 22-24 to Ovules/Successful pollen and remove the anatomy sidebar.
- Remove the recording-card SVG's Arial/Helvetica declarations in favor of the ordinary font.
- Label the Lecture 05D plant example with ovules/pollen, clarifying the egg/sperm alleles inside
  those structures. Keep animal egg/sperm labels in the family example.
- Clean Lecture 05D v2 wrapping with shorter labels and wider, shallower family cross tables.
  Keep the 41-slide sequence, readable font sizes, and Unicode fractions; add no nonbreaking spaces.
- Render Lecture 05D v2 fractions as Unicode glyphs using numeric character references in Djot,
  including halves, quarters, thirds, and sixths in slide content and speaker notes.
- Exclude `tests/_temp/` from Git and normal pytest collection. Retain only note-boundary and
  native-export behavior tests; use temporary checks for broader implementation evidence.
- Synchronized shared style guides, tests, and repository support files from the starter template.

### Developer Tests and Notes

- Summary-reference pass: 05D v2 passes strict native lint and capacity checks at 53 slides.
  Rebuilt ODP/PDF and visually reviewed the new Summary heading and both rule references;
  shortened the independence sentence to remove a one-word wrap.
- Venn follow-up: all four SVGs parse with unique IDs and resolved clip references. Rebuilt
  05D v2 and visually checked slides 5, 8, 14, and 19 in the PDF. Native lint and capacity
  checks pass: 50 slides, five image placements. Retain the existing 100-dpi PDF export setting.
- Study-reference pass: 05D v2 passes strict native lint and capacity checks. Rebuilt ODP/PDF,
  reviewed all nine changed or added teaching/reference pages, and checked equation wrapping.
  The source has 50 slides, 50 note sections, and no percentage symbols; ODP has 50 pages.
- Deck-sequence follow-up: rebuilt all Lecture 05 ODP/PDF decks; verified title, objectives,
  opening section, penultimate summary, final THE END, and matching exported page counts in
  all eight B-H sources (including both versions of D). Reviewed 32 rendered bookend slides.
  Strict native lint passes for 388 slides. The original D capacity warning remains at line 403;
  no new capacity warnings were introduced.
- Opening-question follow-up: strict native lint and capacity inspection pass for 05D v2.
  Rebuilt its ODP/PDF and visually checked slide 3; the complete question fits cleanly in a
  single panel, with no added slides.
- Rule-color pass: rebuilt all nine Lecture 05 ODP/PDF decks and visually reviewed 73 changed
  slides across seven sources. Strict native lint passes; no new capacity concerns. Existing
  palette text shades have white-background contrast ratios of 7.41:1 (blue) and 5.14:1 (orange).
  The original 05D crowding warning remains, now at line 379; 05D v2 still has 45 slides.
- Title-frame follow-up: 42 layout/export tests pass. Rebuilt all nine Lecture 05 ODP/PDF
  decks and visually reviewed their covers; verified no fill and frame-before-text order in
  every ODP and after a LibreOffice save of 05D v2. Strict native lint passes for all 376 slides.
  Capacity inspection retains one existing warning in the original 05D source at line 371;
  the other eight decks, including 05D v2, have none.
- Lecture 05D v2's 45-slide follow-up passes strict native lint and capacity inspection.
  Rebuilt ODP/PDF, verified 45 nonempty note sections, and visually checked both added slides.
- All seven revised Lecture 05 sources pass strict native Djot lint and capacity inspection
  (308 slides total). Rebuilt their ODP/PDF files and verified objective/summary positions and
  speaker notes; reviewed the 12 new opening/closing slides and four revised 05D teaching slides.
- Reviewed every changed `slide_lib` line. All 196 functional tests pass, including theme,
  layout, parser, import/export, capacity, and LibreOffice boundary tests. A temporary check
  confirms matching measurement/export font selection across 16 nested styling combinations.
- Built a four-page typography specimen through LibreOffice; its PDF embeds all 12 intended
  faces and preserves linked monospace text. Rebuilt Lecture 05D v2, passed strict native lint
  and capacity checks, and reviewed all 41 rendered pages. Missing Unicode glyphs still use
  backend substitutions; the deck does not specify fallback fonts.
- Broader hygiene checks: 460 pass; two existing failures remain (the oversized
  `docs/DESIGN_DECISIONS.md` and undeclared `weasyprint` in the Lecture 04 table helper).
- Lecture 05D v2 passes strict native lint and capacity inspection. Built and visually reviewed
  all 41 PDF pages; ODP contains 41 slides and 41 nonempty speaker-note sections. Confirmed the
  original source is unchanged. Recorded the sequence and checked calculations in LECT05D_V2_REVIEW.md.

- Focused parser, layout, native-export, and LibreOffice tests pass. Strict Djot lint accepts the
  17-layout notes sample. A one-time LibreOffice ODP round trip preserves its authored notes;
  extracted PDF text includes visible content and excludes instructor notes.
- Broader checks found existing indentation errors in `devel/render_genetics_lect04_tables.py`,
  missing return annotations in `tests/test_odp_reader.py`, and a stale Lecture 04 review link.
  The existing full-layout E2E stops at its distinct AutoLayout identity assertion; the focused
  note round-trip check completes independently.
