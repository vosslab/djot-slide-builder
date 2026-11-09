# Native table styles results - 2026-11-09

This dated report records the implementation and corpus evidence for the
[approved plan](native_table_styles_plan.md). The
[progress ledger](native_table_styles_progress.md) owns current completion status.
The independent [integration review](../active_plans/reports/native_table_styles_integration_review_2026-11-09.md)
accepted M4 and D18 SPEC/QUALITY on 2026-11-09; saved event evidence is recorded in
`_temp/table_styles/final_verification/integration_review_evidence.json`.

## Delivery

The maintained authoring references are the
[table authoring guide](../slide-specs/TABLE_AUTHORING_GUIDE.md), exact
[Djot table syntax](../slide-specs/DJOT_SLIDE_SYNTAX.md), and
[production demonstration source](../../exemplars/table_styles.djot).
The normal demo outputs are `output/odp/table_styles.odp` and
`output/pdf/table_styles.pdf`. Generated output files remain ignored production
artifacts; the source and four guide WebP captures are maintained.

Ordinary tables use themed defaults. Seven named treatments support comparison,
working data, testcrosses, Punnett squares, and upper/lower matrices. Local whole-cell
formatting provides fills, four borders, padding, alignment, and horizontal spans.
Measurement and native export use the same resolved formatting and geometry.
Equivalent native styles are shared within a document while table cells retain
independent identities. Inline scientific notation and intentional blanks remain.

## Physical corpus reconciliation

The final census reads physical Djot table blocks once, including hidden slides
and included source files. It does not multiply tables by their consumer decks.

| Scope | Final tables | Physical files with tables | Modified files | Anchor cells |
| --- | --- | --- | --- | --- |
| Remaining authored corpus | 263 | 56 | 35 | 3,957 |
| Genetics LECT12 | 59 | 4 | 4 | 1,151 |
| Genetics LECT06/08/14/15 | 102 | 14 | 14 | 2,502 |
| Teaching corpus total | 424 | 74 | 53 | 7,610 |
| Production demo, separate | 14 | 1 | 1 | 179 |

The three owner sets have no overlapping physical sources. The independent census
finds 369 Genetics, 53 Biotechnology, and two Biostatistics tables: the 421-table
baseline plus three restored Punnett tables. All 424 physical source/line keys are
unique. The demo's 14 tables are excluded from those totals.

The 96 original source-table repair records also have unique ODP/page keys.
They preserve 1,769 anchors, 316 intentional blanks, 27 covered positions, and
191 scientific script runs. These source-repair counts are a subset of the final
teaching tables and are not added to 424. Exactly 59 target markers were cleared;
37 target slides retain documented non-table blockers. This is a verified repair
scope delta, not a refreshed repository-wide replacement-marker census.

All 58 source hashes in the three final handoffs match current bytes. The modified
teaching-source sets reconcile as 35 + 4 + 14 = 53. The remaining-corpus adoption
removed 192 redundant gene-cell `text-align=center` attributes; meaningful authored
alignment, fills, text colors, spans, order, scripts, and groups were preserved.

Source-read-only census and exact per-file hashes:
`_temp/table_styles/final_verification/reconcile.py` and `reconciliation.json`.
The census leaves the original M1 baseline intact.

## Source and render evidence

**Remaining authored corpus:** all 263 tables, with 3,957 anchors, pass native
text/order/span checks. All 240 diagnostic PDF pages were visually inspected.
The mapping covers 247 tables in 224 original-context pages and 16 tables in
fallback contexts. One supplementary overlay-omitted PDF proves a native table
otherwise obscured by an inherited replacement overlay. Eight targeted enlarged
cases supplement the contact sheets. Both specification and quality review accepted.

The 16 fallback tables belong to two Biotechnology LECT10 consumer roots blocked
by inherited source structure. Their table appearance is verified; their original
whole-slide contexts are not. The existing replacement overlay and title artifacts
remain recorded in `_temp/table_styles/corpus_remaining/REPORT.md`.

**LECT12:** 57 source repairs preserve 1,121 anchors and 219 blanks; the two
announcement tables bring the final total to 59. Exact same-frame identity checks
justify removing 56 preview references; four genuine textbook-tree PNG references
remain. Forty-four source rectangles are restored as native fills/perimeter borders.
All 150 unmodified source blocks remain byte-identical. Thirty-eight markers
were cleared and 19 retained for sequence workspaces, tree geometry, and symmetry
arrows. Final source/native pages and the refreshed A-deck passed specification
and quality review.

All 932 actual LECT12 text/fill pairs, including 30 announcement pairs, meet the
5.5:1 house target. Forty-one scoped cell corrections across 12 color groups retain
instructional hue and role. Four PDF raster spot checks verify the final gray,
brown, magenta, and announcement combinations. Evidence lives under
`_temp/table_styles/corpus_lect12/contrast/`; the repository-wide contrast audit
was not overwritten.

**LECT06/08/14/15:** 99 existing tables plus three restored tables produce 102.
All 39 source-table repairs preserve 648 anchors, 97 blanks, 27 covered positions,
and 191 script runs. Thirty-four preview references covering 32 unique assets
match original same-frame media. All 63 unflagged table cell blocks remain
byte-identical. Twenty-one markers were cleared and 18 retained. Source/native
comparisons, 81 diagnostic pages, enlarged sequences, canonical artifacts, and
independent specification and quality review passed. Five retained shared-flow
image-floor concerns are documented in the handoff; native table text remains at
least 20pt.

Detailed source mapping, marker reasons, preview identities, selected-cell geometry,
review pages, normal output paths, and hashes remain in each corpus handoff:

- `_temp/table_styles/corpus_remaining/manifest.json` and `REPORT.md`.
- `_temp/table_styles/corpus_lect12/manifest.json`, `summary.json`, and `REPORT.md`.
- `_temp/table_styles/corpus_other_repairs/repair_manifest.json`,
  `source_hashes.json`, and `HANDOFF.md`.

## Practical native behavior

Installed LibreOffice 26.2.7.3, build
`08dfbf04dcac895fc3a8d30dbf5a00de1b9dda5e`, is the practical compatibility authority.
The baseline two-table/53-cell round trip preserved native tables and spans and
matched rendered PDFs. The implementation experiment separately edited cell text,
fill, and a side border, resized the table, saved, closed, reopened, and checked
native properties through actual Java UNO calls in the ordinary application
profile. Rendered exports verify the edited appearance and unchanged neighbor.
This establishes application editing through UNO; mouse/keyboard GUI interaction
and Table Design sidebar behavior were not tested. Longer replacement text can
require ordinary manual resizing; LibreOffice may rebalance row heights.

The final fill-precedence experiment used the actual original LECT12B page 67.
A fresh installed-LibreOffice export proves white cell appearance despite a stale
black paragraph background. The importer now prefers the drawing fill color for
absent/solid fill, honors explicit no-fill, and retains paragraph fallback only
when no drawing color exists. The six affected source tables emit all 66 white
cells correctly, including the 18 formerly black fallback cells; actual black
source diagonals remain black. All 96 raw facts and 462 explicit solid fills retain
their source identity. Evidence: `_temp/table_styles/fill_precedence/REPORT.md`.

### Raw-import column widths

When raw source proportions are present and valid, the importer always preserves
them, including equal and near-equal widths. Unknown widths still use automatic
layout. This raw-import behavior leaves the curated course corpus and accepted
authoring choices unchanged, so no course rebuild was needed. Regenerating the 96
raw snippets added `column-widths` to 93; three snippets were unchanged. Source
facts, cell lines, scripts, and spans remain unchanged, and maximum normalized
ratio error is `1.039e-6`. Two equal/near-equal regressions and compiled width ratios
pass; the focused importer suite reports 50 passed, and all six selected security,
indentation, and typing gates pass. Full evidence and commands:
`_temp/table_styles/width_preservation/REPORT.md`.

## Normal artifacts

LECT12's three normal ODP/PDF pairs contain 187 authored slides, 17 hidden slides,
170 PDF pages, 59 native tables, and 1,151 native cells. Eight resolved visible
pages are pixel-identical to reviewed compact exports; 31 match geometry/text
with at most one RGB-channel quantum of rounding. The hidden announcement table
was inspected in a forced-visible review export.

The other-repair set's 13 normal pairs contain 618 authored slides, 17 hidden
slides, 601 PDF pages, and 102 native tables. All 39 repaired native tables and
marker positions match their final manifests. Hashes and paths are recorded in
`corpus_lect12/artifact_proof.json` and
`corpus_other_repairs/normal_artifacts.json` under `_temp/table_styles/`.

The remaining batch completed 37 normal pairs containing 247 tables, 1,953 authored
slides, 198 hidden slides, and 1,755 PDF pages. Its source/ODP visibility and native
table counts agree; PDF counts equal visible authored slides. It skipped exactly
the two known Biotechnology LECT10 roots containing the 16 fallback tables.

The independent final reconciliation checks all current ODP/PDF SHA-256 hashes
against the three handoffs, reads native table/page counts directly from each ODP
ZIP, and obtains PDF counts with `pdfinfo`. The 37 + 13 + 3 course-root sets are
disjoint: **53 normal course pairs, 408 native tables, 2,758 authored slides,
232 hidden slides, and 2,526 PDF pages**. The missing 16 production-table contexts
are exactly the documented blocked-root cases; all 424 tables still have accepted
source and diagnostic review evidence.

Adding the separate production demo yields **54 pairs, 422 native tables,
2,772 authored slides, and 2,540 PDF pages**, with the same 232 hidden slides.
Exact root-specific paths and current artifact hashes are in
`_temp/table_styles/final_verification/reconciliation.json`. The remaining batch's
commands and proof are in
`_temp/table_styles/corpus_remaining/normal_builds/REPORT.md`. Normal artifacts
were checked structurally and by page count; the batch did not repeat the accepted
diagnostic visual review for every normal PDF.

The separate maintained demo contains 14 pages, 14 tables, 179 native cells, and
178 native paragraphs plus one vector equation. All canonical pages and four
quality-90 guide WebPs were inspected. Genetics, Biotechnology, and Biostatistics
variants preserve instructional colors; pages 1, 5, and 14 were inspected in both
additional themes. The complete theme variants were rendered. Specification and
quality review accepted the source, guide, captures, and normal outputs.

## Verification and limits

Focused core verification passed 238 checks. The wrapping correction passed 480
checks, including regression coverage for scientific script/hyphen projection.
Importer, typing, security, source, and documentation checks are recorded in the
component reports; the demo/source/document pass contains 842 checks. These checks
overlap and are not summed into one suite result.

The final base command was:

```bash
source source_me.sh && pytest tests/
```

`_temp/table_styles/base_suite_final.log` reports exactly **3 failed, 4,380 passed,
2 warnings, 109 errors in 24.86 seconds**. The three failures trace to existing
Biotechnology LECT10 parse-conflict roots; the 109 setup errors cascade from those
inherited conflicts. No new table-code tests failed. The two warnings are an upstream
anyio pytest deprecation and an advisory that
`tests/test_layout_engine.py` has 916 lines. Neither warning is a test failure.
The complete base suite does not pass.

Repeat the read-only final census from the repository root:

```bash
source source_me.sh && python3 _temp/table_styles/final_verification/reconcile.py
```

Component reports retain exact reproduction commands. Normal builds use
`source source_me.sh && python3 deck_tools.py build --format all <source.djot>`;
every command that can invoke LibreOffice runs outside the sandbox through the
repository helpers. This reconciliation performed no LibreOffice calls.

The independent AI integration review accepted the combined implementation with no
open requirement gaps or architectural drift. This records neither human review,
merge approval, nor release authorization. Original context verification remains
limited for the 16 fallback tables; 37 repaired target slides retain unrelated
non-table markers. Fresh GUI/classroom checks and learner outcomes were not tested.
