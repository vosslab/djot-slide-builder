#!/usr/bin/env python3
"""Draw a ligand, membrane receptor, and soluble protein in one family."""

import pathlib

import svg_tools.drawing
import svg_tools.parts
import svg_tools.signaling
import svg_tools.text


#============================================
def main() -> None:
	"""Write an editable signaling-components example."""
	membrane = svg_tools.signaling.membrane('M 30 150 L 330 150', spacing=10,
		thickness=32, color='#b9e3ea', gaps=((135, 165),))
	ligand = svg_tools.parts.transform(svg_tools.signaling.ligand(
		width=45, height=36, color='#f4cf9f'), x=180, y=55)
	receptor = svg_tools.parts.transform(svg_tools.signaling.receptor(
		width=95, height=160, color='#cbdcf0'), x=180, y=150)
	protein = svg_tools.parts.transform(svg_tools.signaling.protein(
		width=105, height=95, color='#d6e7c0'), x=400, y=150)
	kinase = svg_tools.parts.transform(svg_tools.signaling.protein(
		width=105, height=95, color='#e5d7ef', kind='kinase'), x=540, y=150)
	labels = [svg_tools.text.label(x, 255, value, size=16, color='#344651').fragment
		for x, value in ((180, 'Ligand and receptor'), (400, 'Globular'), (540, 'Kinase-like'))]
	output = pathlib.Path('_temp/svg_toolkit/proteins/proteins.svg')
	output.parent.mkdir(parents=True, exist_ok=True)
	svg_tools.drawing.write_svg(output, 610, 280, 'Signaling components',
		'Schematic ligand, membrane-spanning receptor, and soluble protein.',
		membrane.fragment + receptor.fragment + ligand.fragment + protein.fragment + kinase.fragment + ''.join(labels))


if __name__ == '__main__':
	main()
