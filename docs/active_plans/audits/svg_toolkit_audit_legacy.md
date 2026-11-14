# SVG toolkit legacy review

## Finding

- **Low — unreferenced CairoSVG dependency.** `pip_requirements.txt:8` installs `cairosvg` for local SVG drawing recipes, but a repository-wide case-insensitive search found no live Python import or command invoking it. The only code reference is the archived, reference-only `docs/archive/genetics_gene_tree_svg/reference_only/cd/draw_trials.py.txt:4`; its README identifies it as historical. Every installation therefore carries a dependency with no current consumer. Remove the requirement if replaying that archived reference is not a supported installation workflow. The archive itself can remain intact.

## Areas checked

- `/opt/homebrew/bin/python3.12 -B -m pyflakes svg_tools` completed with no findings.
- Searched toolkit modules and SVG tests for TODO, FIXME, skip/xfail markers, compatibility markers, and commented-out executable blocks; no actionable residue found.
- The new curve, plotting, icon, XML, and font dependencies have live source consumers. The MathJax and xmldom requirements are explicitly mandated by repository guidance.
- The existing chromosome and gene-track APIs have an explicit preservation policy in `docs/active_plans/active/svg_toolkit_plan.md:125` and real consumers including `svg_tools/chromosome_examples.py:32` and `:220`; their compatibility paths should stay.
- Inspected shared placement, text bounds, and curve helpers and their callers; no duplicate helper justified removal on the evidence reviewed.

## Limits

This is a static legacy and dependency review, not a runtime or visual validation. No tests were run; no permanent test is proposed for removing an unused dependency. External users and unpublished scripts cannot be searched, so the CairoSVG recommendation is conditional on the archive not being a supported workflow.
