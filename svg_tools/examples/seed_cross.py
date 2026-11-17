#!/usr/bin/env python3
"""Draw the independent seed color and shape phenotype grid."""

import pathlib
import sys

import svg_tools.drawing
import svg_tools.parts
import svg_tools.phenotypes
import svg_tools.text


#============================================
def main() -> None:
	"""Write the editable figure to the requested path or lecture asset."""
	output = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
		'genetics/LECT04/djot/assets/lect04g-indep_assort/dihybrid_seed_phenotypes_toolkit.drawn.svg')
	output.parent.mkdir(parents=True, exist_ok=True)
	items = ['<rect width="1000" height="1090" fill="white"/>']
	for x, y, color in ((360, 330, '#a9c0d1'), (660, 330, '#d4e0e8'),
			(360, 600, '#cbdbe6'), (660, 600, '#edb49f')):
		items.append(f'<rect x="{x}" y="{y}" width="300" height="270" fill="{color}"/>')
	items.append('<path d="M660 330 V870 M360 600 H960" fill="none" stroke="white" stroke-width="3"/>')
	for x, y, shape, color in ((510, 178, 'round', '#b4bd46'), (810, 178, 'round', '#49835a'),
			(180, 440, 'round', '#49835a'), (180, 710, 'wrinkled', '#49835a'),
			(510, 440, 'round', '#b4bd46'), (810, 440, 'round', '#49835a'),
			(510, 710, 'wrinkled', '#b4bd46'), (810, 710, 'wrinkled', '#49835a')):
		seed = svg_tools.phenotypes.seed(size=150, color=color, shape=shape)
		items.append(svg_tools.parts.transform(seed, x=x, y=y).fragment)
	for x, y, value, size, bold in (
			(660, 55, 'Seed color phenotypes', 35, True), (180, 285, 'Seed shape', 32, True),
			(180, 321, 'phenotypes', 32, True), (510, 290, 'Yellow', 32, False),
			(810, 290, 'Green', 32, False), (180, 551, 'Round', 32, False),
			(180, 821, 'Wrinkled', 32, False), (400, 178, '3/4', 29, False),
			(700, 178, '1/4', 29, False), (67, 440, '3/4', 29, False),
			(67, 710, '1/4', 29, False), (510, 552, '9/16', 29, False),
			(810, 552, '3/16', 29, False), (510, 822, '3/16', 29, False),
			(810, 822, '1/16', 29, False), (510, 590, 'Round, yellow', 30, False),
			(810, 590, 'Round, green', 30, False), (510, 860, 'Wrinkled, yellow', 30, False),
			(810, 860, 'Wrinkled, green', 30, False),
			(660, 961, 'Ratio of phenotypes in the', 32, False),
			(660, 1039, 'cross is 9 : 3 : 3 : 1.', 32, False)):
		items.append(svg_tools.text.label(x, y, value, size=size, color='#263844', bold=bold).fragment)
	items.insert(-2, '<rect x="354" y="920" width="612" height="142" rx="10" fill="#e8f0f5" stroke="#7996a7" stroke-width="2"/>')
	run = svg_tools.text.TextRun
	items.append(svg_tools.text.styled_label(660, 1000,
		[run('F'), run('2', script='sub'), run(' progeny of a dihybrid')],
		size=32, color='#263844', anchor='middle').fragment)
	svg_tools.drawing.write_svg(output, 1000, 1090, 'Dihybrid seed phenotypes',
		'Independent seed color and shape phenotypes combine in a two-by-two grid.', ''.join(items))


if __name__ == '__main__':
	main()
