# Plan: Migrate the chromosome review deck to the shared API

## Context

The [chromosome_review.djot](../../../prototype/chromosome_review.djot) prototype contains 73
pages, with 68 distinct figure IDs and 71 figure placements. Seven figures already use the shared
chromosome topology and renderer, and the second mini deck provides reviewed replacements for
seven more. The remaining 53 schematic IDs need source-backed recipes. C04 is the original
karyotype photograph. The existing [chromosome_review_sources.md](../../../prototype/chromosome_review_sources.md)
and [chromosome_samples.csv](../../../prototype/chromosome_samples.csv) record source provenance.

## Objectives

- Deliver the existing 73-page prototype with API-backed chromosome schematics, all 71 figure
  placements, editable slide text, and the original empirical evidence.
- Regenerate the review from its canonical recipe and verify the figures in the native ODP and
  PDF deliverables.

## Design philosophy

Follow **Keep it simple (KISS)** in [REPO_STYLE.md](../../REPO_STYLE.md). Use source topology to
describe material and its changes, use the shared renderer for bodies, and keep figure poses and
composition in the recipes. Extend the shared painter only where faithful source geometry needs
an API capability. Follow the chromosome conventions in [SVG_VISUAL_STYLE.md](../../SVG_VISUAL_STYLE.md).

## Scope

- Retain the API figures C18, C20, C22, C23, C29, C31, and C66.
- Promote the reviewed Mini2 figures C01, C16, C25, C28, C55, C61, and C63. Derive both C55 views
  and all three C63 views from their respective shared models. Preserve C25's native twin-spot
  explanation.
- Migrate the 53 remaining schematic IDs. Share C03/C36 and C13/C21 artwork while keeping their
  individual native captions and source records. Derive Barr bodies from the corresponding
  active X models.
- Preserve C04 and the empirical images in mixed figures. Preserve C49's separate Mb and cM
  extents, C51's unequal spacing and distinct V/VI intervals, and C52's equal slots and deletion
  membership.
- Keep the cover, closing page, figure order, native captions and other editable text, existing
  notes, and provenance. Declare Atkinson Hyperlegible Next on ordinary authored SVG text.
  Preserve approved roles for Atkinson Hyperlegible Mono and IBM Plex Sans Condensed as specified
  in [HUMAN_SLIDE_GUIDANCE.md](../../HUMAN_SLIDE_GUIDANCE.md). Use `.drawn.svg` for vector recipes
  and `.image.svg` for SVGs with embedded images.

## Non-goals

- Confine artwork and deck changes to the review prototype. Preserve original lecture sources
  and assets byte for byte.
- Limit renderer changes to capabilities needed by the review figures and use the existing
  prototype generator as the normal rebuild entry point.

## Current state summary

The approved baseline passed strict native Djot lint and 62 focused tests. The existing
[chromosome_review_verification.json](../../../prototype/chromosome_review_verification.json)
records earlier checks. The fresh review covers the final exports produced by this migration.

## Architecture boundaries and ownership

### Mapping (milestones -> components)

| Milestone | Component | Review boundary |
| --- | --- | --- |
| M1 | Shared topology and renderer | Check C48 closure and conservation and C57's two poses and belt before releasing the contract. |
| M2 | Mini2 promotion and reuse | Verify the reviewed artwork and the native text and composition in the full deck. |
| M3 | Forms, division, recombination, movement, ploidy, and dosage | Verify source biology, empirical image retention, and figure legibility. |
| M4 | Structural changes, maps, inversions, and translocations | Verify intervals, copy and centromere identity, and segregation outcomes. |
| M5 | Generator, deck, artifacts, and evidence | Independently review the canonical rebuild and its native exports. |

### File scope

| Path | Responsibility |
| --- | --- |
| `svg_tools/chromosomes.py`, `svg_tools/chromosome_surface.py`, and the existing topology modules | Provide shared painting and source-material behavior for authored paths, C48 ring closure, and C57 sister poses. Preserve existing callers. |
| [CHROMOSOME_ENGINE.md](../../CHROMOSOME_ENGINE.md) and focused chromosome tests | Record and exercise any new shared contracts needed by the recipes. |
| `prototype/` recipe modules and [make_chromosome_review.py](../../../prototype/make_chromosome_review.py) | Generate the review schematics. Import the approved Mini2 models where needed. Write all generated review artwork under `prototype/`. |
| `prototype/assets/` and `prototype/chromosome_assets/` | Store generated figures and retained source-image components, addressed through the canonical recipes. |
| `prototype/chromosome_review*.djot` and [chromosome_replacements.csv](../../../prototype/chromosome_replacements.csv) | Reference canonical assets and record replacement provenance. Keep the original source map as provenance. |
| `output/odp/chromosome_review.odp` and `output/pdf/chromosome_review.pdf` | Native deliverables built from the canonical Djot entry point. |
| [chromosome_review_api_migration.md](../workstreams/chromosome_review_api_migration.md), verification JSON, and [CHANGELOG.md](../../CHANGELOG.md) | Record acceptance evidence and the delivered changes. Keep scratch previews and render receipts under `_temp/`. |

## Milestone plan

| M | Title | Summary | Goal |
| --- | --- | --- | --- |
| 1 | Prove challenging poses | Confirm C48 closure and C57 sister placement using the shared engine. | Publish stable renderer calls before dependent recipes. |
| 2 | Promote Mini2 artwork | Integrate seven accepted figures into the full-size layout. | Retain the reviewed biology in every full-deck view. |
| 3 | Migrate forms and division | Rebuild the remaining target IDs across C02-C46. | Preserve cell stages, chromosome identity, and dosage comparisons. |
| 4 | Migrate structural changes | Rebuild the remaining target IDs across C47-C68. | Preserve topology, measured evidence, and product identity. |
| 5 | Integrate and verify | Regenerate, lint, test, export, and inspect the complete deck. | Deliver a reproducible, independently reviewed 73-page ODP and PDF. |

- **M1.** Begin with C48 and C57 source comparisons. Render the C48 excised circle through
  `render_ring()` and the shared closed painter, verify a closed seam and conservation between
  starting and product material, and preserve the shortened linear product. For C57, render
  the deep bend as independently authored sisters with one common centromere belt anchored to
  both. Use `render_path()` for faithful authored geometry. Exit after both proofs and the
  renderer contract pass review. Parallel-plan ready: no. The figures establish shared APIs.
- **M2.** Begin with the reviewed Mini2 sources. Exit after the seven promotions pass full-slide
  comparison, including C25 native prose, C55 overview and loop, and C63 overview and two
  detail views. Parallel-plan ready: yes. The accepted models already exist.
- **M3.** Begin after the shared renderer contract is ready. Exit after the C02-C46 targets pass
  comparison to source order, stage, biological counts and identities, and figure-layout review.
  Parallel-plan ready: yes. Figure families have independent sources and recipe files.
- **M4.** Begin after the shared renderer contract is ready. Exit after the C47-C68 targets
  pass source and quality review. Verify C49 coordinates and units, C51 exact endpoints and
  unequal spacings, and C52 equal slots and gene membership. Check ancestry, independent
  copy identity, centromere placement, and gamete products where applicable. Parallel-plan
  ready: yes. Evidence maps, inversions, and translocation families can be checked independently.
- **M5.** Begin when the figure workstreams have passed review. Integrate into the canonical
  entry point, check both reproducible regenerations, and run native lint, tests and exports.
  Exit when all 71 rendered figure pages, the cover and closing page, and native artifact
  structure pass review. Parallel-plan ready: yes. Fresh reviewers can examine different page
  ranges of the same final PDF after the exports are fixed.

## Test and verification strategy

- Compare with the source inventory for 68 distinct IDs, 71 figure placements, 73 pages, and
  the preserved reference and lecture corpus. Use source and asset hashes for original images.
  Compare the coordinates and membership of empirical maps directly to authoritative data.
- Check meaningful model invariants, including source interval conservation, allele order,
  independent copy IDs, centromere and sister assignments, observed counts, and gamete
  combinations. Use focused tests for shared contracts. Keep figure-specific acceptance in
  scratch checks and the execution ledger.
- Run two scratch regenerations through the canonical review generator and compare output
  SHA-256 hashes with one another and the delivered SVGs. Validate SVG IDs, references,
  applicable fonts, and generated inventory hashes. Fix mismatches at the recipe or source.
- Run pyflakes on changed Python, strict native Djot lint, the focused chromosome tests, and
  `source source_me.sh && python3 -m pytest tests/`. Investigate failures before closeout.
- Build through the repository script outside the sandbox using `soffice --headless --norestore
  --convert-to`. Compare
  each ODP figure placement to the intended SVG or original image hash. Verify ODP native text,
  captions, notes, and PDF text selection. Check for fit and capacity diagnostics.
- Inspect all 71 figure pages in the final rendered PDF using fresh specification and visual
  quality reviewers. Use close-ups where joins, small labels, bands, or reference endpoints
  need them. Include the cover and closing page in the final document check. Repair any issue
  in source and rerun affected checks and render reviews on the rebuilt artifacts.
- Record final export sizes, hashes, page counts, image hashes, review coverage, and test results
  in the execution ledger and the verification record.

## Risk register

| Risk | Trigger | Response and owner |
| --- | --- | --- |
| Deep poses obscure sister paths or invent caps on a circle | C48 seam, C57 overlap, or a displaced belt | Engine owner checks geometric anchors and real renders before recipe integration. |
| Styling alters biological evidence | Bounds, intervals, labeled products, or image hashes drift | Recipe owner corrects model or composition against the source before fresh review. |
| An accepted SVG fails in LibreOffice | Blank pane, raster mismatch, clipping, or unreadable type in ODP/PDF | Integration owner corrects SVG or Djot source, rebuilds, and sends the affected pages for fresh review. |

## Documentation close-out requirements

Record pass counts, reviewer decisions, final sizes and hashes, and any observed limits in
[chromosome_review_api_migration.md](../workstreams/chromosome_review_api_migration.md). Add the
delivered behavior to [CHANGELOG.md](../../CHANGELOG.md). Keep the existing prototype source
records available for subsequent instructor review.
