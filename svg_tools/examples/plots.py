#!/usr/bin/env python3
"""Build a gallery of four editable vector plots from caller-owned data."""

import pathlib

import matplotlib.figure

import svg_tools.drawing
import svg_tools.parts
import svg_tools.plots


#============================================
def main() -> None:
	with svg_tools.plots.plot_style():
		figures = [matplotlib.figure.Figure(figsize=(3.2, 2.4), layout='tight') for _ in range(4)]
		axes = [figure.subplots() for figure in figures]
		axes[0].plot([0, 1, 2, 3], [1, 2, 1.5, 3])
		axes[0].set(title='Response over time', xlabel='Time', ylabel='Response')
		axes[1].bar(['A', 'B', 'C'], [4, 7, 5])
		axes[1].set(title='Groups', ylabel='Count')
		axes[2].errorbar([1, 2, 3], [2, 3, 4], yerr=[.4, .3, .5], fmt='o')
		axes[2].set(title='Measurements', xlabel='Dose', ylabel='Response')
		axes[3].hist([1, 1, 2, 2, 2, 3, 3, 4], bins=[.5, 1.5, 2.5, 3.5, 4.5])
		axes[3].set(title='Distribution', xlabel='Value', ylabel='Count')
		parts = {f'plot{i}': svg_tools.parts.transform(svg_tools.plots.figure_to_part(figure, name=f'plot{i}', size=320),
			x=(i % 2) * 330, y=(i // 2) * 250) for i, figure in enumerate(figures)}
	combined = svg_tools.parts.group(parts)
	output = pathlib.Path('_temp/plots.svg')
	output.parent.mkdir(exist_ok=True)
	svg_tools.drawing.write_svg(output, 650, 490, 'Plot gallery', 'Line, bar, error bars, and histogram.', combined.fragment)
	print(output)


if __name__ == '__main__':
	main()
