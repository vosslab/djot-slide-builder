# SVG toolkit code audit

Six independent passes completed against the current source and supplied implementation evidence. Each pass reported findings; none reported a blocker or high-severity finding. This is a current-source audit, not a Git diff or an independent rerun of historical acceptance.

## Open findings

1. **Medium: process-wide XML namespace mutation.** [svg_import.py:123](../../../svg_tools/svg_import.py#L123) registers XLink on each import, changing ElementTree serialization for unrelated callers and overriding their prefix. The style reviewer reproduced this change. Handle the prefix locally at serialization without mutating the global registry; reconcile the implementation report's historical statement when fixed. The source remains unchanged in this low-risk cleanup.
2. **Medium: gallery caller state leaks.** [build_gallery.py:46](../../../svg_tools/examples/build_gallery.py#L46) changes the working directory and [line 56](../../../svg_tools/examples/build_gallery.py#L56) replaces the curve example's `__file__`, without restoration even on failure. A Python caller can subsequently resolve relative paths or write outputs in an unexpected location. Avoid changing these values or restore both in `finally`, with an explicit output destination if needed. The source remains unchanged.

## Resolved findings and decisions

The missing renderer font setup (medium) is documented, distinguishing bundled measurement files from installed fonts. Brittle artwork tests (medium) were pruned to public invariants. Membrane coverage retains input-dependent anchors and bounds and invalid-gap validation; serialized markup inspection was removed, so appearance, leaflets and rendered gaps depend on temporary or native visual review.

Low findings resolved include plan font wording, optional librsvg prerequisites, toolkit architecture and file map, the new changelog category, unused CairoSVG requirement, function separators and font-layout comments, and the global `Path.is_file` monkeypatch in the root test. Changelog-wide rotation predates this audit and remains outside its boundary. Details and limitations are in the [test](../reports/svg_toolkit_audit_test_fixes.md), [documentation](../reports/svg_toolkit_audit_docs_fixes.md), and [comment](../reports/svg_toolkit_audit_comment_fixes.md) fix reports.

The test reviewer recommended removing or moving several checks. The coordinator retained same-input two-export plot determinism for the explicit D4 contract and an actual date/hash regression (repeated output, not a golden baseline); adapter equality for legacy preservation; binding contacts as a scientific invariant; a real Matplotlib asset as a supported production input and permitted genuine file fixture; and the existing chr7 source map for the earlier chromosome-tool boundary and supplied cytoband data contract. The original classifications remain in the [test pass](svg_toolkit_audit_test.md). No permanent test was proposed or added.

## Pass outcomes

- [Plan](svg_toolkit_audit_plan.md): one low font wording finding.
- [Test](svg_toolkit_audit_test.md): one medium artwork brittleness finding and low test-maintenance findings, with the retained disagreements above.
- [Style and ownership](svg_toolkit_audit_style.md): two open medium shared-state findings.
- [Documentation](svg_toolkit_audit_docs.md): one medium font setup and three low documentation findings.
- [Legacy](svg_toolkit_audit_legacy.md): one low unused dependency finding.
- [Comments](svg_toolkit_audit_comment.md): two low separator and explanatory-comment findings.

## Evidence and scope

After creating the parent of the root-local basetemp, the current focused lane ran:

```sh
PYTHONPATH="$PWD:$PWD/tests" MPLCONFIGDIR="$PWD/_temp/mplconfig" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest --basetemp="$PWD/_temp/svg_toolkit_audit/closeout/pytest" tests/test_svg_*.py tests/test_djot_includes.py -q
```

Result: **107 passed in 1.78s**. An initial run before creating the parent directory had 81 passes and 26 setup errors; the rerun above corrected that setup error. Current SHA-256 checks matched all 99 durable artifacts against their manifests: 41 regeneration outputs, 42 native artifacts, and 16 trial artifacts. No regeneration or native conversion was performed in this audit.

The comment cleanup compared executable ASTs across 34 files before and after and found them identical. The documentation fix report records local relative-link, bundled font-face, `rsvg-convert` version, requirements parsing and CairoSVG consumer checks. Installation instructions were not exercised on a clean machine. The focused lane is not the full suite; no fresh native or interactive Impress review, projector or Zoom test was performed. Historical visual acceptance is preserved in the [implementation report](../../SVG_TOOLKIT_IMPLEMENTATION_REPORT.md).

## Changed files

The fix reports identify `tests/test_svg_organelles.py`, `tests/test_svg_membranes.py`, `tests/test_svg_proteins.py`, `tests/test_svg_phenotypes.py`, `tests/test_djot_includes.py`, `docs/INSTALL.md`, `docs/CODE_ARCHITECTURE.md`, `docs/FILE_STRUCTURE.md`, `docs/CHANGELOG.md`, `docs/active_plans/active/svg_toolkit_plan.md`, and `pip_requirements.txt`. Comment cleanup touched toolkit `parts.py`, `text.py`, `svg_import.py`, `icons.py`, `plots.py`, and `phenotypes.py`, plus examples `allele_frequencies.py`, `annotations.py`, `array_comparison.py`, `build_gallery.py`, `cells.py`, `gene_features.py`, `genome_composition.py`, `icons.py`, `organelles.py`, `phenotypes.py`, `placement.py`, `plots.py`, `seed_cross.py`, `signaling.py`, `styled_text.py`, `svg_composition.py`, `text_labels.py`, and `yeast_mating.py`. This closeout also added this report, moved the six pass reports here, updated the test-fix report and appended an audit link to the implementation report. These lists follow the fix reports and task boundary; no Git diff was used.
