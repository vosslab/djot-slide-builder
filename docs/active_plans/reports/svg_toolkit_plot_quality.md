# SVG toolkit plot quality review

**M13: PASS** for the scoped plot-import milestone. The four current gallery examples cover line, bar, error bars, and histogram plots. `figure_to_part` saves the caller's Matplotlib Figure to an in-memory SVG and imports it through the validated SVG importer. Its `finally` block restores temporarily assigned font properties; it does not close the figure or alter plotted data. A direct check confirmed restoration of a bold italic title, retained axes and line data, and restoration of `font.family`, `svg.fonttype`, and `axes.prop_cycle` after the style context. The genetics default cycle is the course accent `#24578F`.

The current gallery SVG contains 41 live `text` elements, all declaring `Atkinson Hyperlegible Next`, and zero `image` elements. The focused raster-artist test confirms that image elements are rejected. `fc-match` resolves the intended installed family; the white-background `PANGOCAIRO_BACKEND=fc` render shows ordinary labels and titles, including tick labels, without evident clipping or overlap. At 720 pixels high (955 pixels wide), the full four-plot gallery is readable on the inspected image, though tick labels are relatively small for remote viewing and a smaller placement should use larger labels or fewer plots. This is an image-scale assessment, not a classroom or Zoom usability test.

Validation: `MPLCONFIGDIR="$PWD/_temp/mplconfig" PYTHONPATH="$PWD:$PWD/tests" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest -q tests/test_svg_icons.py tests/test_svg_plots.py` — **15 passed**. Regenerated `_temp/plots.svg` using the example and rendered with `rsvg-convert` on white, then encoded WebP at quality 90:

- `_temp/svg_toolkit/plot_quality/plots.webp` (1300 × 980)
- `_temp/svg_toolkit/plot_quality/plots_slide.webp` (955 × 720)

No LibreOffice, ODP, or PDF export was run; this does not establish cross-renderer font fidelity or validate all Matplotlib artist types. SVG import intentionally rejects unsupported content, including raster artists.
