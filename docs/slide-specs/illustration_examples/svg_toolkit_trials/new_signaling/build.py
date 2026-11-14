#!/usr/bin/env python3
"""Build a receptor signaling teaching illustration."""

import pathlib

import svg_tools.annotations
import svg_tools.drawing
import svg_tools.parts
import svg_tools.signaling
import svg_tools.text


def main() -> None:
	move = svg_tools.parts.transform
	label = svg_tools.text.label
	connector = svg_tools.annotations.connector
	membrane = svg_tools.signaling.membrane('M 30 145 L 280 145', spacing=10,
		thickness=32, color='#b9e3ea', gaps=((95, 125),))
	receptor = move(svg_tools.signaling.receptor(width=90, height=150, color='#cbdcf0'), x=140, y=145)
	ligand = move(svg_tools.signaling.ligand(width=42, height=34, color='#f4cf9f'), x=140, y=48)
	kinase = move(svg_tools.signaling.protein(width=105, height=90, color='#e5d7ef',
		kind='kinase', activity='active'), x=375, y=250)
	response_a = move(svg_tools.signaling.protein(width=105, height=90, color='#d6e7c0',
		activity='active'), x=680, y=135)
	response_b = move(svg_tools.signaling.phosphate(svg_tools.signaling.protein(width=105,
		height=90, color='#f4cf9f', activity='inactive'), radius=16), x=680, y=365)
	items = [membrane, receptor, ligand, kinase, response_a, response_b,
		connector([(140, 220), (140, 250), (315, 250)]),
		connector([(435, 235), (520, 235), (520, 135), (620, 135)], kind='activation'),
		connector([(435, 265), (520, 265), (520, 365), (620, 365)], kind='inhibition'),
		label(140, 20, 'Ligand', size=19, color='#344651'),
		label(140, 305, 'Membrane receptor', size=19, color='#344651'),
		label(375, 350, 'Kinase', size=21, color='#344651'),
		label(375, 375, 'Active', size=19, color='#344651'),
		label(680, 235, 'Response A', size=21, color='#344651'),
		label(680, 260, 'Active', size=19, color='#344651'),
		label(680, 465, 'Response B', size=21, color='#344651'),
		label(680, 490, 'Inactive; phosphorylated', size=19, color='#344651'),
		label(550, 115, 'activates', size=17, color='#344651'),
		label(550, 345, 'inhibits', size=17, color='#344651')]
	output = pathlib.Path(__file__).with_name('new_signaling_trial.drawn.svg')
	svg_tools.drawing.write_svg(output, 820, 520, 'Protein activity and phosphorylation',
		'A receptor signals to an active kinase that activates response A and inhibits phosphorylated response B.',
		''.join(item.fragment for item in items))


if __name__ == '__main__':
	main()
