## 2026-09-28

### Additions and New Features

- Converted eight Genetics Lecture 05 ODP decks into canonical Djot and local assets, preserving
  all 325 source slides. Added a conversion review and documented the supplied Lecture 04 edits.

### Fixes and Maintenance

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
