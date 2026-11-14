#!/usr/bin/env python3
"""Draw organelle parts and a separately composed animal cell."""

import pathlib

import svg_tools.cells
import svg_tools.drawing
import svg_tools.parts
import svg_tools.text


#============================================
def main() -> None:
	"""Write a labeled organelle gallery and a cell composition."""
	move = svg_tools.parts.transform
	parts = []
	items = (
		('mitochondrion', 'Mitochondrion', '#f3c8b7'),
		('chloroplast', 'Chloroplast', '#cce5be'),
		('er', 'Endoplasmic reticulum', '#d8d3ef'),
		('golgi', 'Golgi apparatus', '#f5dfb5'),
		('lysosome', 'Lysosome', '#e9c7d4'),
		('vesicle', 'Vesicle', '#d1e6eb'),
	)
	for index, (kind, title, color) in enumerate(items):
		x = 120 + (index % 3) * 260
		y = 110 + (index // 3) * 180
		width, height = ((130, 86) if index < 4 else (72, 72))
		parts.append(move(svg_tools.cells.organelle(kind=kind, width=width, height=height,
			color=color), x=x, y=y))
		parts.append(svg_tools.text.label(x, y + 75, title, size=18, color='#344651'))
	parts.append(move(svg_tools.cells.cell_envelope(kind='animal', width=440, height=340,
		color='#edf5f1'), x=1050, y=230))
	nucleus = svg_tools.cells.nucleus(width=130, height=115, color='#cbdcf0')
	parts.append(move(nucleus, x=1015, y=210))
	parts.append(move(svg_tools.cells.nucleolus(width=30, height=28, color='#b6a4cf'), x=1028, y=205))
	er = svg_tools.cells.organelle(kind='er', width=100, height=55, color='#d8d3ef')
	parts.append(move(er, x=1015 + nucleus.anchors['left'][0] - er.anchors['right'][0],
		y=210 + nucleus.anchors['left'][1] - er.anchors['right'][1]))
	for kind, x, y, width, height, color in (
		('mitochondrion', 940, 310, 90, 50, '#f3c8b7'),
		('golgi', 1115, 155, 100, 55, '#f5dfb5'),
		('lysosome', 1145, 245, 45, 45, '#e9c7d4'),
		('vesicle', 1095, 305, 35, 35, '#d1e6eb'),
	):
		parts.append(move(svg_tools.cells.organelle(kind=kind, width=width, height=height,
			color=color), x=x, y=y))
	parts.append(svg_tools.text.label(1050, 435, 'Composed animal cell', size=19, color='#344651'))
	output = pathlib.Path('_temp/svg_toolkit/organelles/organelles.svg')
	output.parent.mkdir(parents=True, exist_ok=True)
	svg_tools.drawing.write_svg(output, 1300, 465, 'Schematic organelles',
		'Six labeled organelle parts and an animal cell composed from separately placed parts.',
		''.join(part.fragment for part in parts))


if __name__ == '__main__':
	main()
