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

## 2026-09-28

### Additions and New Features

- Converted eight Genetics Lecture 05 ODP decks into canonical Djot and local assets, preserving
  all 325 source slides. Added a conversion review and documented the supplied Lecture 04 edits.

### Fixes and Maintenance

- Restore Lecture 05F superscript allele letters in ABO and C-locus genotypes, plus
  F1/F2 and P1/P2 generation subscripts in headings, prose, and native tables.

- Deep-review Genetics Lecture 05H and improve 60 of its 87 slides. Restore missing pea, squash,
  and Labrador squares; replace tiny summary images with native grouping tables; clarify pathway
  blocks, F2 versus testcross weights, and the cat example's gene labels.
- Preserve the staged questions and answers, shorten prose and resource links, correct the
  normalized flower-count ratio, and replace an unsupported discovery-date claim with the model.

- Render Lecture 05D allele indices as subscripts using numeric character references in
  text labels, crosses, and Punnett tables, preserving the existing color emphasis.

- Audit the remaining Lecture 05 sources for missing text colors. Restore band clues in B,
  probability-rule and worked-example colors in D/E/G, genotype labels and choices in F,
  and experiment/answer emphasis in H using supported readable palette colors.

- Restore Lecture 05C source color emphasis for inheritance choices, autosomal answer headings,
  recessive labels, and male/female terms using the native semantic palette.

- Correct Lecture 05 announcement colors, missing anonymous-message image, readable link labels,
  and grade-percentage wording. Update assessments and homework from the supplied schedule sheet.
- Decode named and numeric character references in native text after inline parsing, keeping
  verbatim text literal and preventing decoded characters from becoming markup.
- Preserve embedded GDI figures during ODP import: select supplied raster alternatives and
  automatically convert preview-less SVM/EMF/WMF components to PNG through sequential LibreOffice.
- Record the instructor's automatic GDI-to-image guidance and the component-image design decision.
- Keep restored GDI figures in mixed table slides by grouping consecutive images or editable
  text flows into one cell when five components cannot occupy a native grid.
- Updated copied Lecture 05 covers and agenda, standardized explicit covers/dividers/closers, and
  reconstructed four missing teaching diagrams as editable crosses, tables, and donor results.
- Admit unsupported flat ODP polylines as recorded review objects instead of rejecting a valid
  zero-width vertical mark; finite bounds and negative-dimension rejection remain enforced.
- Recorded the instructor's guidance about checking LibreOffice usage after a crash.
- Rotated older changelog day blocks into CHANGELOG-2026-09b.md, retaining the two newest dates.

### Developer Tests and Notes

- Lecture 05F passes strict native validation and capacity checks with 52 slides. Rebuilt ODP/PDF
  and visually checked all 14 changed pages for raised allele letters and lowered generation indices.

- Lecture 05H passes strict native validation and has no capacity warnings. All 87 source and
  generated pages received contact-sheet review, with larger checks of restored teaching objects.
  Independently verified ten Punnett squares, three phenotype totals, eight paired F2/testcross
  groupings, and both nine-pattern overview tables. Rebuilt the 87-page ODP/PDF and recorded
  per-slide advisory scores and remaining compact textbook labels in LECT05H_REVIEW.md.

- Lecture 05D subscript correction passes strict native validation (31 slides); rebuilt ODP/PDF
  and visually verified colored allele labels and Punnett-table genotypes.

- Remaining Lecture 05 color audit passes strict native validation across all eight decks /
  325 slides. Rebuilt eight ODP/PDF pairs and reviewed all 35 changed pages; capacity inspection
  retains only the documented dense Huntington example in D.

- Lecture 05C passes strict native validation (49 slides); rebuilt ODP/PDF and visually checked
  representative recessive, sex-linked, multiple-choice, and autosomal-answer slides.

- Announcement corrections pass 158 parser/lint checks and strict native Djot validation.
  Rebuilt the 35-page ODP/PDF and visually reviewed the nine affected pages; capacity inspection
  reports no concerns in the announcement deck, and exported text has no literal entity remnants.
- Automatic GDI preservation passes complete trial imports of all eight Lecture 05 decks
  (325 slides), including 42 raster alternatives and five preview-less SVM conversions. The
  converted components were visually checked for clipping; 141 importer/geometry/lint checks pass.
- Strict native Djot lint passes eight decks / 325 slides / 206 image references. Focused importer
  tests pass (22 tests); combined importer and Python lint checks pass 132 tests. Eight ODPs and
  eight PDFs have matching source page counts. Final rendered inspection and the two remaining
  capacity concerns are recorded in the Lecture 05 review.

## 2026-09-25

### Additions and New Features

- Split the 386-slide Biotechnology Set #3 protein deck into chapter decks 04C-04F, with individual
  covers and THE END closers; all instructor material, all 30 topics, and six hidden quiz answers
  remain included.

### Fixes and Maintenance

- Renamed the 04D-04F Djot sources and exports to retain the `talking_points_set_3` hierarchy and
  updated their review links.
- Corrected the 2026-09-24 heading so commit_changelog.py recognizes its entries.
- Curated Human Guidance to direct slide advice, consolidated settled choices in Design Decisions,
  and updated the LibreOffice GUI and headless conversion decision.
