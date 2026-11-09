# Native table styles progress

Tracks the approved [native table styles plan](native_table_styles_plan.md).
Current evidence and limits are in the dated
[2026-11-09 results](native_table_styles_results.md).

## Status

| Task | Status | Result |
| --- | --- | --- |
| M1: Corpus baseline | Spec and quality accepted | Baseline: 421 physical course tables and 96 source-table repair records. Final census: 424, including three restored tables. |
| M2a: Native implementation experiment | Spec and quality accepted | Actual LibreOffice text/fill/border editing, resize, save, close, and reopen verified through Java UNO; PDF appearance inspected. |
| M2b: Style model and authoring | Spec and quality accepted | Validated registry, direct semantic-cell formatting, local overrides, and native style sharing; final core 238 checks passed. |
| M2c: Measurement | Spec and quality accepted | Resolved formatting and cell geometry feed measurement; shared wrapping correction passed 480 checks. |
| M2d: Native serialization and sharing | Spec and quality accepted | Concrete native fills, borders, padding, alignment, spans, and document-scoped style interning preserve independent cell identities. |
| M2e: Visual family, guide, and demo | Spec and quality accepted | Maintained 14-page/179-cell demo, authoring guide, and four WebP captures accepted; 842 focused checks passed. |
| M3a: Import repair | Spec and quality accepted | Secure YAML/XML handling, exact preview suppression, source properties, and drawing-fill precedence verified against fresh native LibreOffice output. |
| M3b: Corpus adoption | Spec and quality accepted | All 424 physical teaching tables reconciled; all three corpus groups accepted, including fresh LECT12 A-deck correction review. |
| M4: Final verification | Complete; integration accepted | Physical sources, source/artifact hashes, semantics, render evidence, 53 normal course pairs, and base-suite result reconciled. The independent [integration review](reports/native_table_styles_integration_review_2026-11-09.md) accepted M4 and D18 SPEC/QUALITY with no open requirement gaps or architectural drift. |

The final source census finds 369 Genetics, 53 Biotechnology, and two Biostatistics
tables. The disjoint owner sets contain 263 + 59 + 102 = 424 tables across 74 files;
53 teaching sources changed (35 + 4 + 14). The maintained 14-table demo is separate.
All 58 handoff source hashes match current bytes. The 96 repaired original tables
preserve 1,769 anchors, 316 blanks, 27 covered positions, and 191 script runs.

Exactly 59 repaired target markers were cleared and 37 retain separate non-table
blockers. This is a verified target-scope delta, not a new repository-wide marker
count. Sixteen Biotechnology tables have fallback render evidence because two
LECT10 canonical consumer roots remain blocked by inherited source structure.
Their native tables are verified; their original whole-slide contexts remain limited.

## Decisions

- **D4-D7 - Core contract and physical cells:** Use `CellOverrides`, `Border`, and
  `CellFormatting`; semantic cells own formatting directly. Load the validated registry
  once per measurement session and cache resolved tables. Choose one winner for
  each shared edge and write it to both cells; merged borders use uniform native
  components. Do not rely on native border precedence to choose the winner.
- **D8 - ODF style sharing:** Intern equivalent table-cell, paragraph, text, and
  dimension styles within one document; preserve independent object identities.
- **D9 - Import facts:** Preserve cells, blanks, spans, widths, scripts, and inherited
  formatting. Suppress exact-frame previews only when the native table is emitted.
  Never infer a header from the first body row; preserve explicit white fills.
- **D10 - Measurement:** Retain conservative full-size script measurement unless
  rendered evidence demonstrates a failure.
- **D11 - Header comparison:** Center comparison-table headers.
- **D12 - Neutral fills:** Omit `draw:fill="none"` when no fill is intended; retain
  explicitly authored white rather than adding a blanket neutral reset.
- **D13 - Example hygiene:** Exclude only `examples/**` lecture-cover hygiene checks.
  All other native source gates remain active. Spec and quality accepted.
- **D14 - Source highlights:** Preserve cell-aligned source highlights through native
  fills and borders; retain separate tree/arrow blockers.
- **D15 - Drawing-fill precedence:** For absent/solid fill, prefer native drawing color
  over stale paragraph background; explicit no-fill remains unfilled. Fresh actual
  LibreOffice source-page output proves the white case. Spec and quality accepted.
- **D16 - Scoped contrast:** Audit all 59 LECT12 tables, including announcements:
  932 actual text/fill pairs meet 5.5:1 after 41 scoped cell corrections in 12 groups.
  Preserve instructional hues; keep the repository-wide contrast audit intact.
  Final raster spot checks and spec/quality review accepted.
- **D17 - Shared wrapping:** Use the same tokenizer for measured text and native
  projection, preserving script boundaries and hyphen wrapping. The 480-check
  correction pass and independent spec/quality review accepted.
- **D18 - Raw-import widths:** Preserve every supplied valid source column
  proportion, including equal and near-equal widths. Unknown widths still use
  automatic layout. Curated course choices remain unchanged. The 93-of-96 snippet
  correction, ratio error, and checks are recorded in
  `_temp/table_styles/width_preservation/REPORT.md`.

### Historical decisions

- **D1 - Practical ODP authority:** LibreOffice 26.2.7.3, build
  `08dfbf04dcac895fc3a8d30dbf5a00de1b9dda5e`, is the compatibility authority.
  The baseline retained two native tables and all 53 cells through ODP -> FODP -> ODP
  and matched PDFs. Separate actual UNO editing proves text/fill/border edits,
  resize, save/reopen, and neighbor independence; no GUI interaction claim.
- **D2 - Production demonstration:** Maintain `examples/table_styles.djot`; normal
  outputs are `output/odp/table_styles.odp` and `output/pdf/table_styles.pdf`.
- **D3 - Authoring and backend:** Keep authoring simple; backend complexity serves
  accurate native output. SVG tables remain outside scope.

## Completion

Implementation and M4 verification are complete. The independent AI
[integration review](reports/native_table_styles_integration_review_2026-11-09.md)
accepted the combined result on 2026-11-09; saved evidence identifies event
`amsg_01a1c251-e003-7c43-99b1-2b65b11d7bbb`. This records no human review, merge
approval, or release authorization.

The complete base suite still has three inherited Biotechnology LECT10 failures
and 109 cascading setup errors. Sixteen tables have fallback-only context evidence,
and 37 target slides retain unrelated non-table blockers. Fresh GUI/classroom checks
were not performed.

## Verification record

- Independent physical census: 424 unique source/line keys, disjoint owner scopes,
  exact modified-file counts, unique 96 source ODP/page repair keys, matching handoff
  source hashes. Evidence: `_temp/table_styles/final_verification/reconciliation.json`.
- Remaining corpus: 263 tables/3,957 anchors, 240 reviewed pages, 247 tables in original
  contexts plus 16 fallback tables, and one supplementary overlay-omitted proof.
- LECT12: 59 tables, 56 preview references removed, 44 native selection rectangles,
  932 contrast pairs, final normal A/B/C 187 authored/17 hidden/170 PDF pages.
- Other repairs: 102 tables, 34 preview references removed, 39 exact source repairs,
  13 normal pairs, 618 authored/17 hidden/601 PDF pages.
- Remaining normal batch: 37 pairs, 247 tables, 1,953 authored/198 hidden/1,755 PDF
  pages. Combined disjoint course delivery: 53 pairs, 408 tables, 2,758 authored/
  232 hidden/2,526 PDF pages. All current artifact hashes match the final handoffs;
  independent ODP ZIP and `pdfinfo` counts agree. Adding the separate 14-page demo
  gives 54 pairs, 422 native tables, 2,772 authored slides, and 2,540 PDF pages.
- Focused implementation, importer, security, typing, source, demo, and documentation
  checks passed as recorded in component reports. Overlapping runs are not summed.
- Final base suite: **3 failed, 4,380 passed, 2 warnings, 109 errors in 24.86s**.
  The three failures trace to existing Biotechnology LECT10 parse-conflict roots;
  the 109 setup errors cascade from those inherited conflicts. No new table-code
  tests failed.
  Warnings are an upstream anyio pytest deprecation and the advisory 916-line
  `tests/test_layout_engine.py`. The complete suite does not pass.
