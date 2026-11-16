# Chromosome theme migration report

Scratch evidence was preserved on November 16, 2026; see the
[rescue index](../prototype/temp_cleanup/README.md). Historical `_temp/` paths below identify
the original locations, retained inside the source archive. Archived acceptance records the
original validation; it does not imply that generated output files are still present.

Status: COMPLETE, 2026-11-15. Source promotions, contextual native gates, focused checks, live
reconciliation, and independent integration acceptance pass. The
[archived plan](archive/chromosome_theme_migration_plan.md) records the approved delivery;
the [live progress ledger](active_plans/reports/chromosome_theme_migration_progress.md) records
current gates. This report records dated results, not a new drawing policy.

## Scope and result

The baseline covers all 110 current roots in Genetics, Biotechnology, Biostatistics and
evergreen: 2,895 image uses and 1,699 distinct assets, including hidden placements and images
without chromosome keywords. Every use has a family decision; zero classifications remain
unresolved. The current parsed source has 2,849 direct image nodes and 1,704 distinct assets.
[Inventory JSON](active_plans/reports/chromosome_theme_inventory.json), the
[baseline placement CSV](active_plans/reports/chromosome_theme_placements.csv), and the
[current placement CSV](active_plans/reports/chromosome_theme_current_placements.csv) retain
both sides without pretending that a grouped composition is a one-to-one replacement. The
LECT13D grouping receipt expands the 54 final direct nodes back to its 100 preserved source
component occurrences; restored source-native bars are separately recorded. Archival originals
remain intact. Asset/file counts do not establish native acceptance.
External biology-problems code is a read-only model reference, with no runtime
dependency or migration claim.

Shared rods, replicated sisters and authored curved chromatids use the v2 geometry in
[chromosomes.py](../svg_tools/chromosomes.py). Source-known centromere positions, loci, ancestry,
counts, replication, loops, pairing and reciprocal products remain authoritative. See
[SVG_VISUAL_STYLE.md](SVG_VISUAL_STYLE.md#chromosome-family-authority) and
[GENETICS_ILLUSTRATION_GUIDE.md](slide-specs/GENETICS_ILLUSTRATION_GUIDE.md#chromosome-language)
for the canonical scientific and visual rules.

## Accepted evidence

LECT12 B/C/D/E scientific and quality reviews pass. Actual current native outputs have
48/69/112/37 visible PDF pages respectively. Corrected B/C/D authority is
`_temp/chromosome_migration/native_repaired/verification.json`; E authority is
`_temp/chromosome_migration/native_de/verification.json`. These receipts bind source and
ODP/PDF SHA-256, embedded source SVG bytes, page counts and editable native text objects.
All accepted current artifact hashes were rechecked during documentation closeout.
Actual changed placements were viewed; inherited density warnings elsewhere remain.

The current native receipt accepts 26 masters: M3 contributes 4 masters, 57 changed PDF pages,
and 64 changed placements; M4 contributes 22 masters, 177 changed PDF pages, and 191 reviewed
360-pixel frames. In total, it binds 234 changed pages and 255 changed placements across 1,377
visible / 1,379 expanded pages.
The current authority is `_temp/chromosome_migration/native_m4/combined_acceptance.json`, with
group `*_progress.json` and independent `review_*/` receipts. Acceptance is conditional on
matching current source and output hashes. Earlier intermediate HANDOFF counts and rejected
exports are superseded by these receipts. Native exports were serialized by the native
coordinator through repository scripts outside the macOS sandbox.

Completed final gates:

- LECT06 B/C: all final35 figures are installed with scientific and quality PASS, including
  vector26's sealed namespace correction and nine mixed figures (seven corrected panels plus
  mitosis and meiosis). `_temp/chromosome_migration/lect06/production_all35.json` binds current
  hashes and recipes; `native_combined36.json` adds shared LECT08 C12. The final35 has 42 live
  uses. Actual B/C native acceptance covers 25 changed pages and 26 frames; D/E acceptance
  stands at unchanged bytes.
- LECT13D: all 40 v3 source figures and ten source-faithful composite canvases pass scientific
  and quality review, are promoted, and pass actual native acceptance across 45 changed pages
  and 54 frames. Grouped strips and restored source-native chromosome bars remain associated
  with their original outcomes. Every word, reveal and slide count is preserved; no split slides.
- Root integration: final focused checks, live source/hash reconciliation, and independent
  acceptance pass. The acceptance receipt is
  `_temp/chromosome_migration/reviews/final_integration/REPORT.md`.

## Deliberate retains and existing discrepancies

Empirical photographs, measured cytogenetic bands/maps, molecular DNA and gene tracks,
quantitative plots and institutional identity retain their distinct representations. LECT02
Beadle/Tatum test-tube/replica-plating charts and LECT06 corn life cycle, gametogenesis and
oogenesis nuclei/dots have no explicit condensed chromosome body and remain exact retains.
LECT06 retain rationale and exact original hashes are in `assortment_terra/HANDOFF.md` and
`retained_assets.json` under `_temp/chromosome_migration/lect06/`; all 63 retained bytes match.
The LECT12D
source006 full empirical panel is retained unchanged, including its original low resolution,
bands and constrictions; it is not a newly reconstructed chromosome. LECT02's quantitative EMF
organism/count table remains an evidence retain. Transparent source placeholders remain blank.

LECT12B's original visible chromosome counts and native words sometimes disagree. Source
fidelity preserves both and records the mismatch; this is not scientific correction. The
meiosis mini/enlarged color inconsistency is likewise recorded separately. Inherited source
prose and unchanged deck capacity warnings outside changed placements remain separate work.

Three protected raster inputs now live as ignored local files: two MIME-correct PNGs and one
normal SVG wrapper preserving its exact WebP image. Public JSON/Python contains no raster
payload literals. Canonical recipe paths are relative and portable. All 24 LECT13 B/C outputs
and all 16 LECT08 outputs regenerated with identical reviewed artwork bytes (40/40). Details
and exact raster/package/output hashes are in `_temp/protected_raster_inputs/HANDOFF.md` and
its manifests. Include these private inputs when copying the local regeneration package.

## Regeneration and continued authoring

Run from the repository root with `PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B`.
Production recipes and their sibling authored inputs are the regeneration sources; `_temp/`
proofs are evidence, not runtime dependencies. Current recipe commands include:

```bash
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B genetics/LECT12/djot/make_polyploidy_chromosomes.py
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B genetics/LECT12/djot/lect12c_chromosome_recipes.py
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B genetics/LECT12/djot/render_lect12d_chromosomes.py
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B genetics/LECT12/djot/render_lect12e_chromosomes.py
```

Other production entry points include the LECT06 `make_chromosome_*.py` scripts, LECT08
`chromosome_recipes/*_recipe.py`, LECT10 `regenerate_lect10b.py` and `lect10_count_recipe.py`,
and LECT13 `lect13bc_chromosome_recipes.py`, `lect13b_loop_chromosome_recipes.py` and
`lect13d_chromosome_recipes.py`. For example:

```bash
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B genetics/LECT08/djot/chromosome_recipes/b31_recipe.py
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B genetics/LECT10/djot/regenerate_lect10b.py
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B genetics/LECT13/djot/lect13bc_chromosome_recipes.py
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B genetics/LECT13/djot/lect13b_loop_chromosome_recipes.py
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B genetics/LECT13/djot/lect13d_chromosome_recipes.py
```

LECT09's nine canonical `make_*.py` entry points are listed in
`_temp/chromosome_migration/lect0910/lect09_promotion.json`. Their sibling templates and JSON
are production inputs. Additional recipes are recorded by each promoted
source package and the inventory `current_recipe` column. Preserve sibling private raster inputs and
source maps. Use `chromosome_part()`/`render_chromosome_layout()` for straight forms,
`chromosome_path_part()` for authored paths and `centromere_part()` only at a source-known
terminal locus. Finish SVGs with `drawing.write_svg()` so normal SVG/xlink namespaces survive XML
composition and native import. Check regenerated bytes and view the actual placement after
any meaningful change. Native builds use `deck_tools.py build <master.djot> --format all`
through unsandboxed execution, as required by repository instructions.

## Verification limits

The migration is complete. Native receipts prove inspected changed placements,
source/output bytes and ODP text objects; they do not establish a whole-deck biology audit or
GUI selection test. The final shared focused lane passed 22 tests, including the source-projection
and native namespace checks. No full base suite is claimed. High-volume CSV/JSON
ledgers are evidence data, not production source modules subject to source-file size limits.
