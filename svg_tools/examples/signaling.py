#!/usr/bin/env python3
"""Draw an authored receptor-kinase-response signaling example."""

import pathlib

import svg_tools.annotations
import svg_tools.drawing
import svg_tools.parts
import svg_tools.signaling
import svg_tools.text


#============================================
def main() -> None:
	"""Write an editable example with independent activity and phosphate states."""
	move = svg_tools.parts.transform
	label = svg_tools.text.label
	connector = svg_tools.annotations.connector
	membrane = svg_tools.signaling.membrane('M 40 135 L 290 135', spacing=10,
		thickness=32, color='#b9e3ea', gaps=((95, 125),))
	receptor = move(svg_tools.signaling.receptor(width=90, height=150, color='#cbdcf0'), x=150, y=135)
	ligand = move(svg_tools.signaling.ligand(width=42, height=34, color='#f4cf9f'), x=150, y=38)
	kinase = move(svg_tools.signaling.protein(width=100, height=90, color='#e5d7ef',
		kind='kinase', activity='active'), x=350, y=245)
	inactive = move(svg_tools.signaling.phosphate(svg_tools.signaling.protein(width=100, height=90,
		color='#e5d7ef', kind='kinase', activity='inactive'), site_label='site A', radius=16), x=760, y=445)
	response = move(svg_tools.signaling.protein(width=100, height=90, color='#d6e7c0',
		activity='inactive'), x=555, y=245)
	branch_response = move(svg_tools.signaling.protein(width=100, height=90, color='#d6e7c0',
		activity='active'), x=555, y=445)
	parts = [membrane, receptor, ligand, kinase, inactive, response, branch_response,
		connector([(150, 205), (150, 245), (293, 245)]),
		connector([(407, 245), (498, 245)], kind='inhibition'),
		connector([(300, 260), (260, 260), (260, 445), (498, 445)]),
		label(150, 21, 'Ligand', size=16, color='#344651'),
		label(150, 340, 'Receptor', size=16, color='#344651'),
		label(350, 340, 'Kinase', size=16, color='#344651'),
		label(555, 340, 'Response protein', size=16, color='#344651'),
		label(450, 190, 'branch A: inhibits', size=15, color='#344651'),
		label(425, 428, 'branch B: activates', size=15, color='#344651'),
		label(555, 540, 'Response protein', size=16, color='#344651'),
		label(760, 540, 'Kinase', size=16, color='#344651'),
		label(760, 570, 'Phosphorylated, inactive', size=16, color='#344651')]
	output = pathlib.Path('_temp/svg_toolkit/signaling/signaling.svg')
	output.parent.mkdir(parents=True, exist_ok=True)
	svg_tools.drawing.write_svg(output, 900, 595, 'Signaling states',
		'Receptor, kinase and response proteins with independent activity and phosphorylation states.',
		''.join(part.fragment for part in parts))


if __name__ == '__main__':
	main()
