# Original-deck fidelity tracker

This tracker records verified execution status for
[abundant-painting-bird.md](abundant-painting-bird.md). That plan remains the
authoritative scope, design, and acceptance source.

## Current evidence

- Final `./build_slides.sh genetics` completed in 50.6 seconds: eight editable ODP files and eight
  LibreOffice-derived PDFs with 31/23/43/49/59/43/62/26 visible pages (336 total).
- Artifact audit accepted 336 editable pages, 185 picture frames, maximum aspect error 0.0068%, and
  suppressed chrome. PDFs report Impress as creator and LibreOffice 26.2.5.2 as producer; bounded
  direct import, original-deck parity, and native ODP/LibreOffice roundtrip E2E checks passed.
- Capacity reports 99 explicit accepted source-located diagnostics (94 paragraph/list, 4 mixed-flow,
  1 table); it is evidence, not a target count. The 63 `title-only` to `section` changes are the
  only genetics Djot source changes.
- The advisory visual report covers 336 standalone pages and 336 original/generated pairs: 48
  improved, 272 roughly equivalent, and 16 materially worse at pre-existing explicit native
  reconstruction placeholders. Those findings are accepted source-migration limitations because the
  plan forbids source/image edits and the rejected diagram abstraction is absent.
- M7 review passed: no continuation, decomposition, grid stream, exception-driven layout search,
  layout-engine pass-through, `MeasurementStatistics`, or maintained PPTX surface remains. The
  canonical-SVG/diagram subsystem is removed. `slide_lib/` is 12,532 lines.
- The post-audit fast suite passed 1,908 tests in 5.17 seconds. One-time build, artifact, capacity,
  visual, and E2E checks remain implementation evidence rather than permanent pytest tests.

Graphify rebuilt 1,497 nodes, 3,288 edges, and 66 communities after the cleanup.

## Milestones

| Milestone | Status | Dependency / next condition |
| --- | --- | --- |
| M1 ODP output defects | Accepted | Final ODP and LibreOffice-PDF audit confirms page parity, aspect preservation, and no chrome. |
| M2 One-to-one compilation | Accepted | WP-A1, WP-A4, and WP-D5 are accepted. |
| M3 Fitting evidence | Accepted | 336-page parity and 99 explained, source-located diagnostics are accepted evidence. |
| M4 Visual review rubric | Accepted | Standalone and paired advisory review completed; material findings are accepted limitations. |
| M5 Syntax specification | Accepted | WP-E1 and WP-S1 are accepted. |
| M6 Layout identity and fidelity | Accepted | Final LibreOffice PDF and visual verification completed. |
| M7 Simplification harvest | Accepted | Retired concepts, PPTX surface, and diagram abstraction are absent. |

## Work packages

| Package | Status | Depends on |
| --- | --- | --- |
| WP-A5 | Accepted | None |
| WP-A1 | Accepted | WP-A5 |
| WP-A4 | Accepted | WP-A1 and accepted WP-D5 |
| WP-A2 | Accepted | WP-A1 |
| WP-A3 | Accepted | WP-A2 |
| WP-A6 | Accepted | WP-A3 |
| WP-B1 | Accepted | None |
| WP-B2 | Accepted | None |
| WP-S2 | Accepted | None |
| WP-S4 | Accepted | WP-S2 |
| WP-S3 | Accepted | Final LibreOffice PDF and paired visual verification completed. |
| WP-D5 | Accepted | WP-A1 |
| WP-S1 | Accepted | WP-A1, WP-D5, and WP-E1 |
| WP-E1 | Accepted | WP-A1 |
| WP-I1 | Accepted | Bounded native ODP reader and immutable page-evidence boundary. |
| WP-E2 | Accepted | WP-E1, WP-I1, and WP-S1 |
| WP-E3 | Accepted | WP-E2 and WP-S1 |
| WP-C1 | Accepted | WP-A1 and WP-E1 |
| WP-C2 | Accepted | WP-C1 |
| WP-D1 | Accepted | WP-A1 and WP-A3 |
| WP-D4 | Accepted | WP-S1, WP-E3, and WP-C1 |
| WP-D2 | Accepted | WP-A1 and WP-A4 |
| WP-D3 | Accepted | ODP-only code, documentation, and tests. |
