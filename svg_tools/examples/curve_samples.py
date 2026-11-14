#!/usr/bin/env python3
"""Draw oriented repeated marks along an authored cubic curve."""

import pathlib

import svg_tools.curves
import svg_tools.drawing


#============================================
def main() -> None:
	"""Write the curve placement example beside this script."""
	path = "M 40 150 C 115 15 235 285 320 100"
	body = f'<path d="{path}" fill="none" stroke="#b8c4ce" stroke-width="3"/>'
	for x, y, angle in svg_tools.curves.sample_curve(path, spacing=28):
		body += f'<g transform="translate({x:.3f} {y:.3f}) rotate({angle:.3f})">'
		body += '<circle r="9" fill="#276c78"/><path d="M 0 0 L 14 0" '
		body += 'stroke="#eab655" stroke-width="4" stroke-linecap="round"/></g>'
	output = pathlib.Path(__file__).with_suffix(".drawn.svg")
	svg_tools.drawing.write_svg(output, 360, 260, "Curve placement",
		"Repeated circles and tangent marks follow a cubic curve.", body)


if __name__ == "__main__":
	main()
