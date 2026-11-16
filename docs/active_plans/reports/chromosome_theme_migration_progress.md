# Chromosome migration progress

Status: COMPLETE, 2026-11-15. The
[archived plan](../../archive/chromosome_theme_migration_plan.md) and independent integration
receipt close the migration.
Dated outcomes and authoring continuity are in the
[migration report](../../CHROMOSOME_THEME_MIGRATION_REPORT.md).

## Reconciled source coverage

Fresh native root discovery, ordered source loading and typed image parsing confirm
**110 root decks**, **2,849 current direct image nodes**, **1,704 current assets**,
zero missing image files and zero parse errors. The baseline remains 110 roots / 2,895 uses /
1,699 assets. All uses have family decisions; no unresolved classification remains.

The baseline CSV preserves every original occurrence and hash. The separate
`chromosome_theme_current_placements.csv` is authoritative for live source nodes. This is
necessary because LECT13D now groups source strips: its 54 final direct nodes expand through
`lect13d_grouping_reconciliation.json` to the original 100 component occurrences, while
source-native chromosome bars are restored separately. The mapping is semantic, not positional;
no source component is claimed deleted. The `native_receipt` column supplies deck receipt
provenance; its presence does not imply visual acceptance of every unchanged placement.

| Course | Placements | Current distinct assets |
| --- | ---: | ---: |
| genetics | 1,718 | 1,228 |
| biotech | 1,110 | 463 |
| biostats | 15 | 15 |
| evergreen | 6 | 6 |

## Milestone gates

| Gate | Current evidence | Remaining work |
| --- | --- | --- |
| M1 inventory | All live uses classified; baseline and current bytes reconciled | Refresh after final source edits |
| M2 shared renderer | Fresh scientific specification and separate quality PASS; shared path and source-known marker helpers in production | Complete |
| M3 LECT12 B/C/D/E | Scientific/quality PASS; actual current native 48/69/112/37 pages; corrected B/C/D receipt and E receipt below | Complete; retained for final integration traceability |
| M4 remaining courses | Production promotions and 22 accepted masters / 177 changed actual PDF pages | Complete; retained for final integration traceability |
| M5 delivery | Actual source/output SHA authority retained in native receipts; accepted changed pages viewed | Complete: focused checks, final reconciliation, and independent integration PASS |

M1-M5 are complete. No staged figure, recipe file count or contact sheet was treated as a native gate.

## Current native authority

- `_temp/chromosome_migration/native_m4/combined_acceptance.json`: 26 current accepted masters,
  1,377 visible / 1,379 expanded pages, 234 changed PDF pages, and 255 changed placements.
  M3 contributes 4 masters / 57 pages / 64 placements; M4 contributes 22 masters / 177 pages
  / 191 reviewed 360-pixel frames across early courses, LECT06 B/C/D/E, LECT08 B/C/F,
  LECT09 C/D/E/H, LECT10 B/D and LECT13 B/C/D. Independent `review_*/` receipts bind actual
  output hashes; source hashes must still match.
- `_temp/chromosome_migration/native_repaired/verification.json`: current corrected
  LECT12 B/C/D outputs, superseding corresponding older native_bc/native_de counts.
- `_temp/chromosome_migration/native_de/verification.json`: current LECT12 E output.

The native coordinator alone invokes LibreOffice, serialized outside the sandbox using repository
scripts. Receipts record native text objects and exact source SVG bytes embedded in ODP;
there was no GUI selection test. All changed accepted pages were inspected at classroom size.
Inherited capacity/REPLACE ME warnings at unchanged placements remain documented in receipts.

## Open source and native gates

- LECT06 B/C: final35 production figures now pass scientific and quality review and actual B/C
  native acceptance now covers 25 changed pages / 26 frames (including shared LECT08 C12).
  Current
  production hashes/recipes are in `_temp/chromosome_migration/lect06/production_all35.json`;
  `native_combined36.json` adds shared LECT08 C12, and `final_changed_placements.json` records
  42 current uses. D/E uses remain accepted at unchanged bytes.
  Do not reuse original pre-namespace B hashes. The immutable final9 package remains evidence.
- LECT13D: all 40 v3 figures and ten source-faithful composites are promoted with scientific and
  separate quality PASS. Actual contextual review passes 45 changed pages / 54 frames. Grouped
  source components are reconciled as associations, not missing uses. No slide splits.
- Root: independent integration PASS at
  `_temp/chromosome_migration/reviews/final_integration/REPORT.md`.

## Scientific retains and source fidelity

Use `centromere_after=None` when the source has no centromere locus, neck or marker.
Preserve source-established necks such as PAR and known source units: D013 3R is approximately
110 cM and 27.9 Mbp. Ornamental poses may use standard rods; biological loops/pairing remain.

Retain empirical photographs, cytogenetic band maps, biological molecular gene tracks,
quantitative tables/plots and brand identity. D006's full original panel is unchanged evidence,
not a redraw. C MyoD and empirical X distributions remain evidence. The E opsin figure has
shared whole-X context plus unchanged molecular array groups. Original institutional logos
and transparent placeholders remain retained. LECT02 EMF organism/count table remains evidence.

LECT12B's pre-existing depicted-count/native-word mismatches and the meiosis mini/enlarged
color disagreement are source-fidelity observations, separate from scientific correction.
No correction is inferred from migration acceptance. LECT02 Beadle/Tatum test-tube and
replica-plating charts lack chromosome bodies; LECT06 corn life-cycle/gametogenesis/oogenesis
figures show nuclei/dots rather than explicit condensed chromosome bodies. These remain exact
retains under source scientific review.

Three ignored private inputs (two PNGs and one normal SVG containing exact WebP) replace public
JSON/Python raster payload literals. Relative canonical recipes regenerate 40 LECT13 B/C and
LECT08 outputs with identical artwork bytes. Exact original raster/package/output hashes and
clean production scan evidence: `_temp/protected_raster_inputs/HANDOFF.md` and sibling manifests.
Include private sibling inputs when copying local recipes; public source alone cannot recreate
the protected pixels.

## Evidence links and limits

- [Baseline placement CSV](chromosome_theme_placements.csv),
  [current placement CSV](chromosome_theme_current_placements.csv),
  [LECT12 subset](chromosome_theme_lect12_placements.csv),
  [inventory JSON](chromosome_theme_inventory.json).
- Baseline survey and staged review paths remain in the inventory; intermediate PASS reports
  are limited to their exact source/output hashes and are superseded by current native receipts.
- Reconciliation used direct Python 3.12 and asserts for root count, physical files, equal ordered
  per-source use counts and exact SHA-256. Scratch evidence:
  `_temp/chromosome_migration/closeout_docs/reconciliation.json`.

No full suite, unchanged whole-deck visual audit or GUI selection test is claimed by this ledger.
The final shared focused run and independent integration acceptance pass. CSV/JSON ledgers are
evidence data; their volume is not a production source-module size exception.
