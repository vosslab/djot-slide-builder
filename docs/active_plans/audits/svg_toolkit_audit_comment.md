# SVG toolkit independent comment review

Scope: current toolkit modules, examples and SVG tests identified in the audit brief, with targeted inspection of text measurement and source comments. No Git history was available, so legacy status of files already present cannot be established from this pass. Findings below cite toolkit files identified as new in the audit boundary.

## Findings

- **Low — required function separators are inconsistent in new toolkit files.** `svg_tools/icons.py:20`, `:27`, and `:33`, `svg_tools/phenotypes.py:27` and `:50`, and `svg_tools/text.py:115`, `:122`, `:134`, `:174`, and `:181` are examples without the equals-sign separator required by `docs/PYTHON_STYLE.md:231`. Numerous new example entry points, such as `svg_tools/examples/allele_frequencies.py:18` and `:35`, also omit it. This makes the new files inconsistent with the explicitly required navigation convention. Add the existing `#============================================` separator above affected module-level functions, applying the rule consistently across the new toolkit files. No behavior change or permanent test is needed.
- **Low — nontrivial text-layout heuristics lack intent at the calculation.** `svg_tools/text.py:39-47` measures at a fixed 1024-unit font size and adds two different fallback margins; `svg_tools/parts.py:70-80` repeats related allowances across runs, while `svg_tools/text.py:115-119` doubles the missing-glyph allowance for wrapping. The public docstrings disclose that fallback bounds are conservative but do not explain the shared scale or why the width allowance differs between measurement and wrapping. These values influence clipping and line breaks, so an editor cannot confidently adjust them without reconstructing the rationale. Add concise intent comments describing the fixed-size scaling and why wrapping includes both sides of the fallback allowance, if that is the intended rationale; verify the rationale before documenting it. No new permanent test is proposed for comments.

## No findings and limits

- The inspected public operations generally have short purpose docstrings, and the XML boundary comments explain their intent. Names and control flow in the inspected paths were understandable.
- A token scan of the designated new modules, examples, and SVG tests found no non-ASCII comment tokens. A text search of these files found no milestone, workstream, TODO, FIXME, or hack tags in permanent comments; the example reference to a temporary gallery is descriptive.
- Automated scans were leads rather than proof of every comment's accuracy. This focused review did not independently validate rendering, correctness, all documentation, or the recorded release checks. Existing unchanged legacy style is not reported as a finding.
