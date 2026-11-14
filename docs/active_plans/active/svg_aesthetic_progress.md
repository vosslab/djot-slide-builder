# SVG aesthetic upgrade progress

This ledger records current evidence for
[svg_aesthetic_plan.md](svg_aesthetic_plan.md). The visual contract is
[SVG_VISUAL_STYLE.md](../../SVG_VISUAL_STYLE.md). Status changes require an owner's result
and observable evidence; an assignment or promising render is not completion.

## Milestone ledger

Status snapshot: 2026-11-14. All 14 milestones are DONE, with implementation evidence and independent reviews recorded below.

| Milestone | Accountable owner | Status | Evidence or next completion check |
| --- | --- | --- | --- |
| M1 Guide and baseline | `aesthetic_direction` | DONE | Guide, baseline, protected hashes, ASCII and relative-link checks passed; see [M1 handoff checks](#m1-handoff-checks). |
| M2 Shared-state fixes | `aesthetic_state`; `aesthetic_namespace_fix` | DONE | [Foundation quality](../reports/svg_aesthetic_foundation_quality.md) and [code re-review](../reports/svg_aesthetic_code_respec.md) pass state and namespace corrections. |
| M3 Stroke/tone mechanics | `aesthetic_foundation`; `aesthetic_stroke_cap` | DONE | [Code re-review](../reports/svg_aesthetic_code_respec.md) and [standalone art review](../reports/svg_aesthetic_final_art_quality.md) pass the cap and contained tone planes. |
| M4 Cells/nuclei | `aesthetic_cells` | DONE | [Standalone art review](../reports/svg_aesthetic_final_art_quality.md) passes cells and nuclei at full and reduced size. |
| M5 Organelles | `aesthetic_organelle_fix` | DONE | [Organelle correction](../reports/svg_aesthetic_organelle_fix.md), [code re-review](../reports/svg_aesthetic_code_respec.md), and [standalone art review](../reports/svg_aesthetic_final_art_quality.md) pass the corrected anatomy. |
| M6 Membranes | `aesthetic_signaling` | DONE | [Code re-review](../reports/svg_aesthetic_code_respec.md) and [standalone art review](../reports/svg_aesthetic_final_art_quality.md) pass membrane and insertion checks. |
| M7 Proteins/ligands | `aesthetic_signaling`; `aesthetic_anchor_fix` | DONE | [Code re-review](../reports/svg_aesthetic_code_respec.md) and [standalone art review](../reports/svg_aesthetic_final_art_quality.md) pass corrected anchors and tone planes. |
| M8 Binding | `aesthetic_binding_phenotypes` | DONE | [Standalone art review](../reports/svg_aesthetic_final_art_quality.md) passes contact topology. |
| M9 Chromosomes/gene tracks | `aesthetic_genetics` | DONE | [Standalone art review](../reports/svg_aesthetic_final_art_quality.md) passes identity, bands and tracks. |
| M10 Phenotypes | `aesthetic_binding_phenotypes` | DONE | [Standalone art review](../reports/svg_aesthetic_final_art_quality.md) passes silhouettes, classes and ratios. |
| M11 Diagrams/text/icons | `aesthetic_diagrams` | DONE | [Foundation quality](../reports/svg_aesthetic_foundation_quality.md) and [standalone art review](../reports/svg_aesthetic_final_art_quality.md) pass. |
| M12 Plots | `aesthetic_plots` | DONE | [Foundation quality](../reports/svg_aesthetic_foundation_quality.md) and [standalone art review](../reports/svg_aesthetic_final_art_quality.md) pass. |
| M13 Complete regeneration | `aesthetic_composition` | DONE | [Composition](../reports/svg_aesthetic_composition.md) records 48 outputs, 26 SVGs and seven protected originals; [standalone art review](../reports/svg_aesthetic_final_art_quality.md) passes all 26. |
| M14 Verification/closeout | `aesthetic_native_build` | DONE | [Native rebuild](../reports/svg_aesthetic_native.md) records 32 pages; [native specification](../reports/svg_aesthetic_native_spec.md), [native quality](../reports/svg_aesthetic_native_quality.md), and [integration](../reports/svg_aesthetic_integration.md) pass; [scoped cleanup](../reports/svg_aesthetic_cleanup.md) is complete. |

## Before snapshot

The baseline was captured before aesthetic regeneration. Its 51 scratch copies under
`_temp/svg_aesthetic/baseline/` were removed at closeout; protected hashes and durable
before/after comparisons remain. The manifest records category, path, bytes, hash, and copy.

| Category | Count |
| --- | --- |
| Gallery WebPs, including index | 18 |
| Gallery SVGs | 17 |
| Chromosome v2 SVG | 1 |
| Active toolkit pilot SVGs | 6 |
| Trial SVGs | 2 |
| Protected originals | 7 |

Visual baseline inspected: the full gallery index, organelle composition, and binding
composition. Main opportunities: heavy cell contours, anatomy compressed into small interior
marks, flat body masses, and rigid antibody strokes. Existing meaningful color mappings and
scientific contact relationships are retained. These observations motivate work; they do not
constitute an after-change acceptance.

## Protected source hashes

The following original sources are outside the aesthetic replacement set. Their hashes were
verified again after cleanup in the [integration review](../reports/svg_aesthetic_integration.md).

- `genetics/LECT03/djot/assets/lect03f-whole_genome_analysis/human_genome_composition.plot.svg`
  SHA-256: `2059903ad86b5aade0249c7ab7d84f6029de0d5f9de52368265bb0d6fc7d6b52`.

- `genetics/LECT11/djot/assets/lect11d-chromo_alter_1-deletions/array_comparison_workflow.drawn.svg`
  SHA-256: `b739fac24f49ab7009298acf2a6dbbffd44dfdfef45ab7559a038c1582663f64`.

- `genetics/LECT09/djot/assets/lect09d-yeast_unordered_tetrads/yeast_mating.drawn.svg`
  SHA-256: `bebcfacff1292dcdcf9db63a6774bcf4cebbe95a1922dfce6873dc18d17fb05a`.

- `genetics/LECT09/djot/assets/lect09d-yeast_unordered_tetrads/yeast_diploid.drawn.svg`
  SHA-256: `a4c48c8f2d75c8d41af3abe53ca878acd44ab4e0dda474ae646dd95f7ca0567f`.

- `genetics/LECT04/djot/assets/lect04g-indep_assort/dihybrid_seed_phenotypes.drawn.svg`
  SHA-256: `3de072b6d7cc350dc8daf5a397eb52a96fc10276744f55abb3748b449eed0986`.

- `biotech/LECT04/djot/assets/lect04c-talking_points_set_3/western_detection_detail.drawn.svg`
  SHA-256: `a7cc2655e78ca5c3590675360acffe7cfdd8e50a6ff2889748d23c4bdcc09204`.

- `genetics/LECT02/djot/assets/lect02d-dna_structure_overview/b_dna_helix.drawn.svg`
  SHA-256: `5559e48a7ccab780408bb402d8585c134667a10cce47e785d38a8c9b2cc037ba`.

## Current decisions and limits

- Shared outline default is `min(0.02 * min(width, height), 3.0)`; the 3-unit cap is a
  accepted after standalone quality review. Internal anatomy starts at 0.01.
- Use base plus one or two contained tone planes; preserve caller-supplied hue identities.
- The original LECT02 B-DNA is preserved; no quantitative pitch claim is introduced.
- The local namespace correction passed foundation quality and code re-review.
- Servier remains a style reference only. Its current official CC BY 4.0 guidance and historical
  local Bioicons CC BY 3.0 records are documented in the guide; no external geometry is reused.
- Fresh native proofs cover 32 pages; native specification, quality and integration pass. Array and
  compact Western placements retain small labels; Western pages 5 and 7 have 18.5 pt warnings
  against the 20 pt floor. Interactive Impress, live Zoom, the full 351-slide rebuild and the
  full base suite were not checked.
- Protected Biotechnology work and shared cache directories remain outside cleanup scope.

## M1 handoff checks

Verified 2026-11-14 using `/opt/homebrew/bin/python3.12 -B` with `PYTHONPATH="$PWD"`:

- All three owned Markdown documents encode as ASCII.
- All 8 relative Markdown links resolve from their containing document.
- All 51 snapshot SHA-256 values match the manifest and their then-current source files.
- Manifest counts match 18 gallery WebPs, 17 gallery SVGs, 1 chromosome, 6 toolkit pilots,
  2 trials, and 7 protected originals.
- No production source, protected original, or existing native proof was edited by this owner.

The guide, plan, and ledger are handed to the manager. Subsequent implementation and review
owners supply their own current evidence before milestone status advances.
