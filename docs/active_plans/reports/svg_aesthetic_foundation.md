# SVG aesthetic foundation

`svg_tools._style.scaled_path(path, width, height)` bakes dimensions into normalized authored path geometry. It retains explicit close commands for the independent `M` subpaths used in the current cell, binding, and signaling artwork. `outline(width, height)` returns the shared `#344651` outline, rounded caps and joins, and a width of `0.02 * min(width, height)` in final coordinates. Family-specific inner lines can use `0.01 * min(width, height)` and callers retain ownership of bounds, anchors, and tone geometry.

The focused style test passes with `/opt/homebrew/bin/python3.12 -B -m pytest --noconftest tests/test_svg_style.py -q` using `PYTHONPATH="$PWD:$PWD/tests"`. It checks two closed subpaths, a curved final segment, scaled geometry bounds, and equal stroke attributes for transposed dimensions.

The temporary probe `_temp/svg_aesthetic/foundation/probe.svg` uses the existing animal cell contour at 300 x 100, 100 x 300, and 100 x 100. Its `rsvg-convert` rendering `_temp/svg_aesthetic/foundation/probe.png` was visually inspected: the 2-unit outline appears consistent around all three shapes and remains inside the probe canvas. The probe has no `vector-effect`; its path coordinates carry the aspect ratio. This is an SVG renderer check, not a LibreOffice import or slide review.

The helper is scoped to current normalized authored paths, where geometry following a close command starts a fresh `M` subpath. It is not a general-purpose SVG path transformer; nonuniform scaling of elliptical arc commands is not supported by the existing `svgpathtools` scaling method. Current family contours use lines and Bezier curves.
