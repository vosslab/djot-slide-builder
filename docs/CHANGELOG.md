## 2026-09-29

### Additions and New Features

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
