# Plot aesthetic implementation

The scoped Matplotlib style now uses larger labels and bold titles, stronger line and marker
defaults, muted blue-gray axes, light grids, and open top and right spines. The gallery line has
visible markers and error bars have caps. The allele example keeps its distinct colors and marker
shapes, with an unobtrusive legend. The genome chart uses vertical gridlines and retains the six
source values, including the approximate intron label; their sum is 99.5, without normalization.
The gallery accepts an optional output path and retains its existing default.

Validation on 2026-11-14:

- Focused command `PYTHONPATH="$PWD:$PWD/tests" MPLCONFIGDIR="$PWD/_temp/mplconfig" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest -q tests/test_svg_plots.py`: **3 passed**. This covers scoped restoration, data preservation, live text, determinism, and rejection of raster artists.
- Generated all three examples in `_temp/svg_aesthetic/plots/` and converted them to PNG on white with `rsvg-convert`. Visually inspected `plots.png` (650 x 490), `allele_frequencies.png` (600 x 400), and `genome_composition.png` (700 x 700): labels and data marks are legible and no clipping was observed at those sizes.
- Parsed generated SVGs: respectively 41, 16, and 19 live text elements and zero image elements. Genome source values sum to 99.5.

These checks do not establish LibreOffice rendering, slide-scale readability, or the behavior of
every Matplotlib artist. Canonical gallery and lecture outputs were not regenerated in this task.
