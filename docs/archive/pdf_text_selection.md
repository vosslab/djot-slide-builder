# PDF text selection repair

Archived 2026-11-05 as implementation, review, or design history. Original status and
checklists below describe that snapshot; current verification tasks are tracked in
[ROADMAP.md](../ROADMAP.md) and [TODO.md](../TODO.md).

The instructor reported that decorative frames prevented copying text from 09D objectives,
definitions, section, closing, and reference slides. The earlier cover fix applied only to
title-slide decoration. This revision applies that background-master boundary to all theme shapes.

## Cause and repair

- Native macOS PDFKit selection between two points returned an object marker for headings
  inside the old foreground frames. Plain slides and the previously repaired cover worked.
- Moving decoration to a derived master restores the requested heading text. Fonts are unchanged.
- Section/subsection and THE END outlines now have no fill. Page styles retain their colors.
- Bookend/definition bands, reference borders, the closing star, and citation backing bands
  live on background masters. Native slide text and real figures remain on their slides.
- Masters preserve course chrome where appropriate; dark layouts omit it. Explicit stacking
  accounts for unnumbered course-master objects so the upper frame remains visible.

## Regression test

[test_odp_export.py](../../tests/test_odp_export.py) extends the existing cover regression
to seven layouts and two themes: 14 fast cases, without LibreOffice. It requires background
ownership for theme decoration, native slide text, no fill on outline frames, and decoration
stacking above the course background. A failure requires fixing that export boundary.

```bash
source source_me.sh && python3 -m pytest tests/test_odp_export.py -k decoration_is_master_owned -q
```

The focused suite passes 115 cases. The two existing real cover PDF/ODP round-trip tests pass.
Pyflakes and whitespace checks pass. The full unrelated test suite was not run.

## Export acceptance

Rebuild all 12 Lecture 09/10 ODP/PDF pairs. All Djot inputs remain unchanged. Existing Lecture 09
exports retain their text and visible inventories; Lecture 10 had no prior output baseline here.
The 12 PDF inventories match their sources, totaling 403 visible pages.

Use macOS PDFKit's point-selection API for 125 selections, including every affected 09D layout,
its definition/body text, reference footer, and both THE END lines. Requested text is returned
without decorative object markers. 09D's 22 selected lines match exactly. Existing Lecture 10
replacement-marked layouts can select additional nearby warning text; their layout findings remain.

Review 46 representative framed pages, including the affected 09D pages, and compare the full-size
objectives slide with its preceding render. Keep the original frame appearance and proportions.
Scratch probes, baselines, selection results, test/build logs, and quality-90 WebPs are in
`_temp/pdf_text_selection/`.

Point-selection checks exercise PDFKit's native text-selection behavior. They do not constitute
clipboard or attended Preview mouse testing, and other PDF viewers remain untested. Extraction
alone is not the copy/paste acceptance check. Existing Lecture 09 table and Lecture 10 draft-layout
warnings remain outside this renderer repair.
