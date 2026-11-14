#!/usr/bin/env python3
"""Draw the array comparison workflow used in Genetics lecture 11."""

import pathlib
import sys

import svg_tools.annotations as annotations
import svg_tools.drawing as drawing
import svg_tools.parts as parts
import svg_tools.text as text


#============================================
def array_grid() -> parts.SvgPart:
	"""Twelve spots on the original four-column, three-row array."""
	circles = ''.join(
		f'<circle cx="{x}" cy="{y}" r="7" fill="#076DAD"/>'
		for x in (-57.5, -19.5, 18.5, 56.5) for y in (-32.5, -2.5, 27.5)
	)
	return parts.SvgPart('<g>' + circles + '</g>', (-64.5, -39.5, 63.5, 34.5), {})


#============================================
def main() -> None:
	output = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '_temp/array_comparison.svg')
	items = {}
	for index, (x, y) in enumerate(((142.5, 267.5), (377.5, 267.5), (737.5, 307.5))):
		items[f'array{index}'] = parts.transform(
			annotations.box(' ', 175, 115, '#DBEAF3', stroke='#076DAD', stroke_width=3), x=x, y=y)
		items[f'spots{index}'] = parts.transform(array_grid(), x=x, y=y)
	labels = (
		(35, 40, 'SNP genotyping arrays', 29),
		(515, 40, 'Comparative genomic hybridization', 25),
		(40, 115, 'Reference DNAs', 21), (290, 115, 'Test DNA', 21),
		(525, 115, 'Test DNA', 21), (760, 115, 'Reference DNA', 21),
		(55, 355, 'Reference baseline', 19), (290, 355, 'Test SNP calls', 19),
		(650, 395, 'Combined hybridization', 19),
		(50, 425, 'Indirect comparison of DNA samples', 23),
		(555, 425, 'Direct comparison of DNA samples', 23),
	)
	for index, (x, y, value, size) in enumerate(labels):
		items[f'label{index}'] = text.label(x, y, value, size=size, color='#242334', anchor='start')
	for index, points in enumerate(([(120, 135), (120, 170)], [(355, 135), (355, 170)],
		[(590, 135), (700, 240)], [(850, 135), (760, 240)])):
		items[f'link{index}'] = annotations.connector(points, kind='activation' if index < 2 else 'binding',
			color='#34344A', stroke_width=3 if index < 2 else 4, head_size=20)
	output.parent.mkdir(parents=True, exist_ok=True)
	drawing.write_svg(output, 1000, 470, 'array comparison workflow',
		'Separate reference-baseline SNP genotyping versus combined test/reference CGH. '
		'Original schematic; not to scale.', parts.group(items).fragment)
	print(output)


if __name__ == '__main__':
	main()
