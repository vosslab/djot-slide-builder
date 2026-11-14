#!/usr/bin/env python3
"""Draw straight and curved membrane strips with a receptor-sized gap."""

import pathlib

import svg_tools.drawing
import svg_tools.signaling


#============================================
def main() -> None:
	"""Write the example to the temporary SVG toolkit gallery."""
	straight = svg_tools.signaling.membrane('M 40 65 L 360 65', spacing=12,
		thickness=38, color='#b9e3ea', gaps=((140, 180),))
	curved = svg_tools.signaling.membrane('M 40 180 C 130 105 260 255 360 180',
		spacing=12, thickness=38, color='#d6e7c0', gaps=((150, 190),))
	output = pathlib.Path('_temp/svg_toolkit/membranes/membranes.svg')
	output.parent.mkdir(parents=True, exist_ok=True)
	svg_tools.drawing.write_svg(output, 400, 270, 'Membrane strips',
		'Straight and curved bilayers with explicit gaps.', straight.fragment + curved.fragment)


if __name__ == '__main__':
	main()
