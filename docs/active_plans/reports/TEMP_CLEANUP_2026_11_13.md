# Temporary evidence cleanup

2026-11-13. The user directed that the final illustration report live in `docs/` and old
temporary evidence be removed. Completed scratch evidence was removed after its conclusions
were preserved in [the durable report](../../ILLUSTRATION_RENEWAL_REPORT.md); historical
receipts and provenance manifests were not rerun or resealed.

| Owner | Task | Status |
| --- | --- | --- |
| cleanup_report_spec | Durable report specification review | PASS before deletion |
| temp_cleanup_quality | Cleanup quality review | Finding: stray bracket in chromosome plan; corrected |
| cleanup_markdown_fix | Correct stray bracket | Done; exact one-byte correction verified |
| cleanup_final_integration | Fresh quality re-review and integration review | PASS |
| root | Inventory, deletion and five focused product-source hash checks | Done; 811 direct entries removed; hashes match before and after deletion |

The initial inventory contained 813 direct entries, 44,890 files and symlinks, 4,353,047,504
logical bytes and 4,452,634,624 allocated bytes. After cleanup, two direct entries remained,
containing 1,598 files and symlinks, 323,253,195 logical bytes and 326,701,056 allocated bytes.
The differences are 4,029,794,309 logical bytes and 4,125,933,568 allocated bytes. Allocated
bytes are filesystem block estimates, not measured free-space gains; directories are excluded
from byte totals. Symlinks were counted as entries, not followed or included in byte totals.

The retained entries are `_temp/biotech_lect11` and `_temp/biotech_lect11_scope_exclusion`,
both excluded Biotechnology work. No other top-level entry had a descendant modified since the
task start at 2026-11-13 12:34 UTC. Each candidate was checked again immediately before deletion;
symlinks were unlinked and directories removed without following symlinks. `_temp/` remains.

Current closeout links point to the durable report; removed historical proof links now name
their former scratch paths. A workspace Markdown scan outside excluded trees found zero missing
active links to `_temp/`; all five local links in the durable report resolve. The manager checked
five focused product-source hashes against their pre-task values and found them unchanged.
An independent pre/post fingerprint of the excluded trees and a full product-tree comparison
were not captured. No LibreOffice export, render, or test suite was run for this cleanup.

Final integration review inspected the durable report, the corrected chromosome plan, current
report references with `grep -R -n 'ILLUSTRATION_RENEWAL_REPORT.md' docs/active_plans`, and
the top-level inventory with `ls -la _temp`. The report is self-contained, current status links
resolve to it, and removed review evidence is labeled as historical scratch rather than linked.
Only the two protected trees remain in `_temp/`, with no cleanup script there. This review did
not re-audit artwork or deleted proofs, run Git, or repeat the product hash checks.
