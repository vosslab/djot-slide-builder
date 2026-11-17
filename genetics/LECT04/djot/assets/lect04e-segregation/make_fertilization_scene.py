#!/usr/bin/env python3
"""Build the LECT04 gamete-to-zygote scene as locally authored editable SVG.

The source is a watermarked stock raster.  This recipe preserves its teaching
composition but does not copy pixels or geometry from that source.
"""

import pathlib
import sys

import svg_tools.cells
import svg_tools.chromosomes
import svg_tools.drawing
import svg_tools.parts


INK = '#344651'
FONT = 'Atkinson Hyperlegible Next'
OUT = pathlib.Path(__file__).with_name('fertilization_scene.drawn.svg')


#============================================
def text(x: float, y: float, value: str, size: float) -> str:
	return svg_tools.drawing.text(x, y, value, size=size, color=INK, font=FONT)


#============================================
def nucleus_with_genotype(name: str, x: float, y: float, genotype: str) -> str:
	"""Show the source genotype labels with locally drawn sex chromosomes."""
	nucleus = svg_tools.cells.nucleus(width=68, height=58, color='#5e8fd6')
	placed = svg_tools.parts.transform(nucleus, x=x, y=y)
	colors = {'X': '#E7DDF1', 'Y': '#9CC9D8'}
	spacing = 14
	parts = []
	for index, chromosome_name in enumerate(genotype):
		model = svg_tools.chromosomes.Chromosome(
			(svg_tools.chromosomes.Segment(chromosome_name, colors[chromosome_name], 1),
			svg_tools.chromosomes.Segment(chromosome_name, colors[chromosome_name], 1)),
			(svg_tools.chromosomes.Centromere(1),))
		center_x = x + (index - (len(genotype)-1)/2)*spacing
		parts.append(svg_tools.chromosomes.chromosome_path_part(
			f'{name}-{chromosome_name}-{index}', model,
			f'M {center_x} {y-16} V {y+10}', thickness=7,
			labels=False, texture=False).fragment)
	return (f'<g id="{name}">{placed.fragment}{"".join(parts)}'
		f'<text x="{x}" y="{y+25}" text-anchor="middle" font-family="{FONT}" '
		f'font-size="14" font-weight="600" fill="#FFFFFF">{genotype}</text></g>')


#============================================
def cell(name: str, x: float, y: float, width: float, height: float, color: str,
	genotype: str) -> str:
	body = svg_tools.cells.cell_envelope(kind='animal', width=width, height=height, color=color)
	placed = svg_tools.parts.transform(body, x=x, y=y)
	return f'<g id="{name}">{placed.fragment}{nucleus_with_genotype(name+"-nucleus", x, y, genotype)}</g>'


#============================================
def sperm() -> str:
	"""A simple locally authored sperm: head, neck, and a tapering flagellum."""
	head = cell('sperm-head', 336, 159, 102, 72, '#b6cdec', 'XY')
	tail = ('<path id="sperm-neck" d="M 383 159 H 407" fill="none" stroke="#8ba9d8" '
		'stroke-width="9" stroke-linecap="round"/>'
		'<path id="sperm-flagellum" d="M 407 159 C 453 147 456 203 498 193 '
		'C 535 185 531 224 479 240" fill="none" stroke="#8ba9d8" '
		'stroke-width="5" stroke-linecap="round"/>')
	return f'<g id="sperm">{head}{tail}</g>'


#============================================
def main(output: pathlib.Path = OUT) -> None:
	"""Write one source-preserving, stand-alone figure at the source aspect ratio."""
	body = '<rect width="800" height="311" fill="#FFFFFF"/>'
	body += text(151, 30, 'Egg', 26)
	body += text(319, 85, 'Sperm', 26)
	body += text(647, 30, 'Zygote', 26)
	body += cell('egg', 151, 159, 178, 178, '#f6c955', 'XX')
	body += sperm()
	body += text(250, 177, '+', 48)
	body += text(529, 177, '=', 48)
	body += cell('zygote', 647, 159, 190, 190, '#e8ad36', 'XX')
	body += nucleus_with_genotype('zygote-second-nucleus', 700, 204, 'XY')
	svg_tools.drawing.write_svg(output, 800, 311, 'Egg and sperm form a zygote',
		'The locally authored teaching diagram preserves the source sequence Egg plus Sperm equals Zygote. '
		'It depicts one egg nucleus marked XX, one sperm nucleus marked XY, and two zygote nuclei marked XX and XY. '
		'The source genotype labels are retained as live text, with locally authored chromosome bodies.', body)


if __name__ == '__main__':
	main(pathlib.Path(sys.argv[1]) if len(sys.argv) == 2 else OUT)
