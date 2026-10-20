# Gate audit

The October 15, 2026 human guidance supersedes earlier requirements for the checks removed here.
Useful operation, simple recovery, and meaningful output contracts determine what remains.
This audit covers the collected pytest modules, both E2E runners, source/lint/build entry points,
theme/font loading, measurement/layout validation, package/image import and export, and release
preconditions. It does not claim full support for every Djot or OpenDocument feature.

## Removed blockers

| Area | Removed requirement | Result |
| --- | --- | --- |
| Font loading | Recorded SHA-256 must match the font file | Read actual font metrics and verify usability |
| Font provenance | Manifest version, record inventory, upstream URLs, revisions and hashes | Provenance is reference data, not a rendering prerequisite |
| License notices | Exact hash, existence, readability | Copy available notices; omit unavailable ones |
| Template typography | Exactly 36/28 pt, centered title, prescribed font metadata | Read sizes from template; generated runs select bundled fonts |
| Template overflow | Template must explicitly declare shrink-only flags | Generated frame properties already specify overflow behavior |
| Template line spacing | Exactly 130% on every outline style | Read the actual outline spacing; use ordinary default if unavailable |
| Measurement cache | Every size must be a quarter-point multiple | Cache the actual finite positive size |
| Input ZIP ordering | Mimetype must be first and uncompressed | Read members by name; retain content/type validation |
| Archived lecture baseline | Permanent fixed migration page counts | Lecture content and slide counts can evolve |

The default template remains unchanged. Reading a modified template's sizes and spacing is
different from forcing all future templates to reproduce current styling.

## Removed test modules

These permanent modules imposed incidental structure, arbitrary limits, or duplicated behavior
already exercised through parsing/export. Coding and documentation conventions remain guidance.

- `test_bandit_security.py`: broad static findings repeatedly rejected literal test XML and paths;
  retain behavioral tests of the actual XML and file-access boundaries instead.
- `test_bash_script_line_limit.py`, `test_source_file_line_limit.py`, `test_root_script_budget.py`,
  `test_checkout_disk_budget.py`: arbitrary file, inventory, or checkout size limits.
- `test_function_typing.py`, `test_import_dot.py`, `test_import_star.py`, `test_indentation.py`,
  `test_init_files.py`, `test_support_dirs_not_imported.py`: coding-structure policy gates.
- `test_guidance_doc_format.py`, `test_readme_first_paragraph.py`, `test_markdown_links.py`:
  repository-wide prose structure and link-format gates; review edited documentation directly.
- `test_pytest_hygiene.py`, `test_test_naming_conventions.py`, `test_vendored_headers.py`:
  tests of test organization and propagated boilerplate.
- `test_whitespace.py`: formatting gate that also rewrote upstream licenses during a test run.
- `test_cli.py`, `test_djot_grammar.py`: dispatch and regex-unit checks duplicated by source,
  lint, terminal, and build behavior tests.
- `e2e_original_deck_parity.py`: one-time historical migration evidence, not a permanent contract.

Also removed template-default snapshots, font-hash snapshots, helper delegation assertions,
and diagnostic-constructor checks. The existing ODP export tests still verify usable embedded
fonts and editable text. No new permanent tests were added for this audit.

Several removed modules were propagated files. Do not restore these gates merely because a
template update supplies them again; review the demonstrated need under the human guidance.

## Retained checks and responses

| Check family | Why it remains | Failure action |
| --- | --- | --- |
| Parser, includes and semantic lint | Preserve content, physical source locations, notes, and requested layout meaning | Fix the reported source line; unsupported constructs must not silently disappear |
| Layout model, measurement and capacity | Finite geometry and representable text are needed to produce usable slides | Shrink and report capacity where possible; fix an explicitly unrepresentable source block |
| Import planning, component geometry and image-area audit | Keep figures, labels, tables and teaching relationships | Preserve review markers/diagnostics; repair the flagged source or conversion |
| SVG and metafile handling | Static self-contained figures must retain readable labels and dimensions | Repair/convert the component; preserve review evidence rather than discard it |
| XML/ZIP/path validation | Prevent entity expansion, traversal, unusable references and uncontrolled input expansion | Identify and repair/re-export the offending package; preserve existing destinations |
| Font usability and embedding mode | Measurement and editable output need readable faces with usable metrics | Replace the unreadable/incompatible font; byte/version changes alone are accepted |
| ODP export, notes and reveals | Exported objects must preserve visible content and teaching behavior | Fix the importer/compiler/exporter responsible for the lost behavior |
| Atomic publication | Failed builds must not destroy good output | Keep the previous artifact; report and retry the failed operation |
| LibreOffice/PDF output | A requested PDF must actually exist | Report the converter failure; keep ODP and prior PDF; use external export on macOS |
| Terminal and capacity reporting | Authors need actionable diagnostics | Fix incorrect source attribution or missing recovery information |
| ASCII compliance | Explicit author preference for portable source text | Repair indicated text using ASCII equivalents/references; upstream licenses excluded |
| Import requirements and Pyflakes | Missing dependencies and undefined names cause real execution failures | Declare dependencies or fix the reported code |
| Shebang/executable alignment | Directly invoked scripts must launch | Correct the executable bit or interpreter line |
| Native-layout E2E runner | Actual ODP/PDF conversion catches integration failures that mocks miss | Inspect affected output; repair the export/converter path |
| Release destination/tag conflicts | Avoid overwriting a release | Choose a new destination/version or explicitly resolve the conflict |

Native Djot validation is opt-in. It runs the requested tool; no tool-version equality gate was
found in the build path. Release month drift already warns without blocking. Capacity thresholds
that trigger recovery remain advisory; physically impossible frames still produce source errors.

## Validation

One-time checks accepted changed font hash metadata, altered outline spacing, absent template
shrink metadata, a non-quarter-point size, and a reordered/compressed template ZIP. These checks
were run from temporary scripts and were not added to the permanent suite.

The default-template lecture was rebuilt through the normal CLI and external LibreOffice path.
The changelog records the final suite result and visual verification.
