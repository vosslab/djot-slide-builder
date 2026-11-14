#!/usr/bin/env python3
"""Plot supplied illustrative allele frequencies as an editable SVG."""

import pathlib
import sys

import matplotlib.figure

import svg_tools.drawing
import svg_tools.plots


GENERATION = [0, 1, 2, 3, 4, 5]
P = [0.40, 0.45, 0.43, 0.50, 0.55, 0.60]
Q = [0.60, 0.55, 0.57, 0.50, 0.45, 0.40]


#============================================
def generate(output: pathlib.Path) -> pathlib.Path:
	"""Write the supplied values without fitting or changing them."""
	with svg_tools.plots.plot_style():
		figure = matplotlib.figure.Figure(figsize=(6, 4), layout='tight')
		axes = figure.subplots()
		axes.plot(GENERATION, P, marker='o', color='#195f82', label='p')
		axes.plot(GENERATION, Q, marker='s', color='#a44232', label='q')
		axes.set(xlabel='Generation', ylabel='Allele frequency', ylim=(0, 1),
			xlim=(-0.25, 5.25), xticks=GENERATION)
		axes.legend()
		part = svg_tools.plots.figure_to_part(figure, name='allele_frequencies', size=600)
	output.parent.mkdir(parents=True, exist_ok=True)
	svg_tools.drawing.write_svg(output, 600, 400, 'Illustrative allele frequencies',
		'Supplied p and q values across six generations.', part.fragment)
	return output


#============================================
def main() -> None:
	output = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('_temp/allele_frequencies.svg')
	print(generate(output))


if __name__ == '__main__':
	main()
