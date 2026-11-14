#!/usr/bin/env python3
"""Draw the human genome composition plot used in Genetics lecture 3."""

import pathlib
import sys

import matplotlib.figure

import svg_tools.drawing
import svg_tools.plots


DATA = (
	('Exons', 1.5, '1.5%'),
	('Regulatory sequences', 5, '5%'),
	('Introns', 20, 'about 20%'),
	('Unique noncoding DNA', 15, '15%'),
	('Repeats related to\ntransposable elements', 44, '44%'),
	('Other repetitive DNA', 14, '14%'),
)


#============================================
def main() -> None:
	output = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '_temp/genome_composition.svg')
	with svg_tools.plots.plot_style():
		figure = matplotlib.figure.Figure(figsize=(7, 7))
		axes = figure.add_axes((.08, .08, .82, .88))
		for index, (name, value, display) in enumerate(DATA):
			y = 5 - index
			axes.barh(y, value, height=.22)
			axes.text(0, y + .25, name, fontsize=15, fontweight='bold', va='bottom', color='#172d3c')
			axes.text(value + .8, y, display, fontsize=14, fontweight='bold', va='center', color='#172d3c')
		axes.set(xlim=(0, 50), ylim=(-.45, 5.75), yticks=[])
		axes.set_xticks(range(0, 51, 10), [f'{value}%' for value in range(0, 51, 10)])
		axes.tick_params(axis='x', labelsize=13, colors='#344651')
		for side in ('top', 'left', 'right'):
			axes.spines[side].set_visible(False)
		axes.spines['bottom'].set_color('#344651')
		part = svg_tools.plots.figure_to_part(figure, name='genome_composition', size=700)
	output.parent.mkdir(parents=True, exist_ok=True)
	svg_tools.drawing.write_svg(output, 700, 700, 'Components of the human genome',
		'Genome composition percentages; introns are approximately 20 percent.', part.fragment)
	print(output)


if __name__ == '__main__':
	main()
