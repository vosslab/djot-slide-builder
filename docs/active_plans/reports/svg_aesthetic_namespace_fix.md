# SVG namespace collision correction

The importer now returns ElementTree's self-contained serialized fragment without manually assigning the `xlink` prefix. The final writer assigns local prefixes to foreign namespaces, while emitting SVG elements without a prefix and XLink attributes with `xlink` for LibreOffice. It preserves comments and does not change ElementTree's global namespace registry.

Before the fix, registering `xlink` for the SVG namespace made an imported fragment fail `ElementTree.fromstring` with `duplicate attribute`. Separately, registering `xlink` for Dublin Core made final writing fail the same way when metadata and an XLink reference coexisted. Afterward, a direct Python probe registered each mapping in turn and verified fragment parsing, final document parsing, metadata and reference values, the literal final `xlink:href`, and unchanged registry state. Both cases passed.

```sh
mkdir -p _temp/svg_aesthetic/namespace_fix
PYTHONPATH="$PWD:$PWD/tests" MPLCONFIGDIR="$PWD/_temp/mplconfig" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest --basetemp="$PWD/_temp/svg_aesthetic/namespace_fix/pytest" tests/test_svg_import.py tests/test_svg_drawing.py tests/test_svg_plots.py -q
```

Result: **25 passed in 0.75s**, including the existing real Matplotlib SVG import and plot tests. An initial test run had two setup errors because the scratch parent was missing; the remaining 18 tests passed. The parent was created before the successful run above.

These are XML and focused behavioral checks. LibreOffice rendering/import, the full suite, and visual acceptance were not run.
