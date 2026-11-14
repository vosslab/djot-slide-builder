# SVG toolkit documentation audit

## Findings

1. **Medium — Installation omits font installation needed for faithful output.** `docs/SVG_TOOLKIT.md:86-90` says to install the two Atkinson families and points to `docs/INSTALL.md`, but `docs/INSTALL.md:6-46` neither lists the fonts as requirements nor says how to install the bundled files. The Python tools measure with bundled font files (`svg_tools/text.py:21-22`); renderers use installed font families, so a fresh setup can silently substitute fonts and invalidate text layout. Add concise macOS installation and verification instructions for the bundled Next and Mono families, distinguishing measurement files from renderer installation.

2. **Low — Gallery rendering dependency is undocumented in setup.** The catalogue points to the gallery builder (`docs/SVG_TOOLKIT.md:43-44`), which executes `rsvg-convert` (`svg_tools/examples/build_gallery.py:60-63`). The requirements and Brewfile (`docs/INSTALL.md:6-27`, `Brewfile:1-6`) do not install or name it. A reader following installation cannot regenerate gallery previews on a clean machine. Document librsvg/rsvg-convert as a requirement for gallery and preview generation, with its installation command; it need not be mandatory for ordinary SVG authoring.

3. **Low — Architecture and file map omit the toolkit.** `docs/FILE_STRUCTURE.md:5-19` omits `svg_tools/`, and `docs/CODE_ARCHITECTURE.md:3-9` describes only the deck compiler. The newly documented reusable authoring package and its relationship to generated SVG assets and Djot are difficult to discover from these maintainer entry points. Add a short toolkit entry linking the catalogue; no full API duplication is needed.

4. **Low — New changelog section does not follow the repository category convention.** `docs/CHANGELOG.md:1-10` uses `### SVG Toolkit`, whereas `docs/REPO_STYLE.md` requires entries under the named ordered changelog categories. Place this entry under the applicable additions category. The changelog is already 2,184 lines and exceeds the 800-line rotation trigger; determine separately how to rotate existing history while preserving complete day blocks and avoiding duplicate dates, using the repository's approved Git workflow.

## Scope and evidence limits

Reviewed toolkit catalogue, cookbook, installation, usage, implementation report, roadmap, SVG README, architecture, file structure, changelog and reported final checks against the cited current source. The install and build instructions were inspected, not run on a clean macOS installation; I did not invoke LibreOffice or perform a new native visual review. The existing report appropriately distinguishes 107 focused tests, 41 regenerated outputs, native page reviews, earlier whole-deck compilation, and untested interactive/projector/Zoom behavior. No documentation finding was identified in those evidence qualifications or the stated pilot overwrite warning. No new permanent test is proposed.
