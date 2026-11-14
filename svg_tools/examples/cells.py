#!/usr/bin/env python3
"""Draw cell envelopes and explicitly placed nuclear parts."""

import pathlib

import svg_tools.cells
import svg_tools.drawing
import svg_tools.parts
import svg_tools.text


#============================================
def main() -> None:
	"""Write a comparison of five schematic cell envelopes."""
	move = svg_tools.parts.transform
	parts = []
	for kind, title, x, y, width, height in (
		('animal', 'Animal', 150, 130, 185, 155),
		('bacterial', 'Bacterial', 445, 130, 210, 115),
		('yeast', 'Yeast', 745, 130, 165, 155),
		('fused_yeast', 'Fused yeast', 250, 390, 300, 155),
		('plant', 'Plant', 660, 390, 240, 165),
	):
		part = svg_tools.cells.cell_envelope(kind=kind, width=width, height=height,
			color='#e8f2ed', wall_color='#c2ddb9' if kind == 'plant' else None)
		parts.append(move(part, x=x, y=y))
		parts.append(svg_tools.text.label(x, y + height / 2 + 30, title, size=19, color='#344651'))
		if kind != 'bacterial':
			positions = (-.27, .27) if kind == 'fused_yeast' else (0,)
			for position in positions:
				nx = x + width * position
				parts.append(move(svg_tools.cells.nucleus(width=58, height=52, color='#cbdcf0'), x=nx, y=y))
				parts.append(move(svg_tools.cells.nucleolus(width=16, height=15, color='#b6a4cf'),
					x=nx + 8, y=y - 4))
	output = pathlib.Path('_temp/svg_toolkit/cells/cells.svg')
	output.parent.mkdir(parents=True, exist_ok=True)
	svg_tools.drawing.write_svg(output, 900, 530, 'Cell envelopes',
		'Animal, bacterial, yeast, fused yeast and plant envelopes with separately placed nuclei and nucleoli.',
		''.join(part.fragment for part in parts))


if __name__ == '__main__':
	main()
