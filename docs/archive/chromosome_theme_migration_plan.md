# Plan: chromosome theme migration

## Context

Chromosome drawings had drifted between sections of genetics LECT12 and across active course material despite the established v2 rod/open-X language and chromosome drawing tools. The approved migration starts with LECT12 and then applies the same family deliberately across every active course, while keeping each diagram's biological state and teaching purpose intact.

## Objectives

- Give chromosome schematics a recognizable shared v2 family across all active course roots.
- Preserve source biology, native teaching prose, reveal order, and empirical evidence.
- Leave a hash-bound, reproducible record of every retain, migration, source layout repair, and contextual native review.

## Design philosophy

Use the repository's teaching-first and KISS principles: shared geometry should remove visual drift, while source-specific recipes preserve counts, ancestry, loci, poses, and evidence. Do not flatten every biological image into the same silhouette merely to make it look uniform.

## Scope

- Inventory every live image placement in Genetics, Biotechnology, Biostatistics, and evergreen material, including hidden and non-keyword images.
- Use v2 rounded rods, replicated sisters, hollow purple centromeres, and source-derived colors for migratable chromosome schematics.
- Extend the shared SVG helper only for source-required curved, ring, and terminal forms.
- Preserve empirical photos, measured maps, gene tracks, plots, organisms, logos, and sources whose content is not a condensed chromosome body.
- Repair native slide composition only where an artwork migration left required labels, bars, or readable placement missing; retain every slide, word, reveal, and biological association.
- Export and review affected ODP/PDF pages through the serialized native coordinator.

## Non-goals

- Do not correct pre-existing scientific disagreements between source artwork and native prose.
- Do not introduce a theme engine, new configuration layer, or BPQ runtime dependency.
- Do not redraw empirical image data as generic chromosomes or split slides to resolve density.
- Do not claim classroom projection, Zoom delivery, GUI edit/reopen, or a full-suite result that was not run.

## Current state summary

Status: COMPLETE, 2026-11-15. M1 inventory, M2 shared geometry, M3 LECT12, M4 all remaining active courses, and M5 independent integration acceptance passed.

## Architecture boundaries and ownership

### Mapping (milestones -> components)

| Milestone | Component | Review boundary |
| --- | --- | --- |
| M1 | live-source inventory and placement ledger | Every placement classified; baseline/current hashes retained |
| M2 | `svg_tools/chromosomes.py` and focused tests | Shared geometry preserves source facts and renders correctly |
| M3 | LECT12 B-E recipes, Djot layouts, native receipts | Source science, quality, and actual contextual pages |
| M4 | remaining active-course recipes and source layouts | Promotion hashes, retained-source rationale, contextual pages |
| M5 | current ledger, native receipts, independent integration | All live source, output, and review bindings agree |

### File scope

| File or directory | Intended change | Canonical source, for generated output |
| --- | --- | --- |
| `svg_tools/chromosomes.py` | Shared curved/ring/terminal chromosome parts | Typed helper implementation and focused tests |
| `tests/test_svg_chromosome_paths.py` | Geometry and source-projection coverage | Shared helper contract |
| `genetics/*/djot/` recipes and assets | Course-specific source-faithful figures | Production recipes plus sibling authored inputs |
| `docs/active_plans/reports/` | Live inventory and placement evidence | Current source parser and SHA-256 reconciliation |
| `_temp/chromosome_migration/` | Review and native evidence only | Not a runtime dependency |

## Milestone plan

| M | Title | Summary | Goal |
| --- | --- | --- | --- |
| M1 | Inventory | Classify every live placement | No unresolved classification |
| M2 | Shared family | Add required path and terminal primitives | One consistent, source-faithful body language |
| M3 | LECT12 | Migrate B-E before later courses | Accepted source and contextual native output |
| M4 | Remaining courses | Promote reviewed figures and required layout repairs | Every active-course chromosome decision resolved |
| M5 | Integration | Reconcile source, recipe, native, and review evidence | Deliver a verified migration record |

### M1 inventory

- Deliverables: baseline/current asset and placement ledgers.
- Exit criteria: 110 roots and every live placement classified, including retains.
- Parallel-plan ready: yes; discovery and visual classification have independent evidence.

### M2 shared family

- Deliverables: `chromosome_path_part()` for authored bends/rings and `centromere_part()` for source-known terminal loci; focused geometry checks.
- Exit criteria: straight, bent, ring, replicated, and terminal forms preserve known source facts.
- Parallel-plan ready: yes; source migration waits on the shared contract.

### M3 LECT12

- Deliverables: source-faithful B-E recipes/assets and reviewed contextual outputs.
- Exit criteria: source science, separate quality, and native reviews pass. **Complete.**
- Parallel-plan ready: no; it is the prerequisite release for broad migration.

### M4 remaining courses

- Deliverables: promoted active-course assets, retain rationale, necessary native composition repairs, and contextual receipts.
- Exit criteria: all reviewed production source bindings and affected pages pass. **Complete.**
- Parallel-plan ready: yes; course families are independent after shared-contract acceptance.

### M5 integration

- Deliverables: final focused tests, live reconciliation, independent integration review, and durable report.
- Exit criteria: current sources, recipes, native outputs, and receipts agree with no unresolved migration classification or staged placeholder.
- Parallel-plan ready: no; it depends on every prior gate.

## Test and verification strategy

Use direct Python 3.12 with `PYTHONPATH="$PWD"` for SVG work. Focused SVG checks use `PYTHONPATH="$PWD:$PWD/tests" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest` with the selected test paths. Native exports run only through `deck_tools.py` outside the sandbox and are inspected at full-page and figure-frame size. Source, scientific, quality, and integration reviews are ordered independent gates; a contact sheet or recipe count never closes a native gate.

## Migration and compatibility policy

Known centromeres, loci, ancestry boundaries, copy number, paired/replicated state, ring shape, and reciprocal products come from the source. Use `centromere_after=None` where no source locus exists; `centromere_part()` is only for a source-known terminal locus. Recipe code composes source-specific structures with `chromosome_part()`/`render_chromosome_layout()` for straight forms and `chromosome_path_part()` for authored paths. Originals remain archived; normal SVG wrappers may retain protected raster evidence byte-for-byte when it is part of the lesson.

## Risk register

| Risk | Impact | Trigger | Owner | Mitigation |
| --- | --- | --- | --- | --- |
| Generic redraw invents biology | Incorrect lesson | Unsupported neck/locus/ancestry | Source reviewer | Preserve source facts; mark unknown loci `None` |
| Dense migration loses association | Misleading answer/reveal | Detached labels or missing native bars | Course owner | Recompose the affected existing slide, then inspect native output |
| Raster evidence is rewritten | Lost empirical meaning | Photo/map treated as schematic | Source reviewer | Retain original pixels and record rationale |
| Export changes layout | Unreadable slide | PDF differs from source compile | Native coordinator | Serialized actual ODP/PDF review and receipt hashes |
| Ledger confuses grouped composition with loss | False coverage claim | Several strips become one canvas | Integration owner | Keep baseline separate and record semantic component mappings |

## Rollout and release checklist

- [x] M1 inventory and classifications
- [x] M2 shared geometry and focused reviews
- [x] M3 LECT12 source and contextual-native acceptance
- [x] M4 remaining-course final native gates
- [x] M5 final focused checks, reconciliation, and independent integration acceptance

## Documentation close-out requirements

- Archived plan / progress tracker: baseline and current counts remain separately recorded for grouped LECT13D composites.
- `docs/CHANGELOG.md` entry: final migration is recorded below; historical archives remain unchanged.
- Archive / closure notes: this plan moved here after all native and integration receipts passed.
- Temporary verification closeout: `_temp/chromosome_migration/` remains evidence, never the canonical recipe source.

## Open questions and decisions needed

- None. Future slide revisions should follow the continuing authoring guidance and rerun the
  focused source/native checks for their changed placement.
