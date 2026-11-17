#!/usr/bin/env python3
"""Draw LECT10's four-stage somatic proto-oncogene activation schematic.

The retained inherited_cancer_legacy.png establishes cell count, locus states,
labels and arrows. Its chromosome centromere positions are unknown.
Run from the repository root with PYTHONPATH set to that root.
"""

# Standard Library
import pathlib

# Local modules
import svg_tools.cells
import svg_tools.drawing
import svg_tools.chromosomes


#============================================
def cell(stage: int, x: float, locus: str) -> str:
	"""Place one nucleus and one source-matched single chromosome in a cell."""
	if stage < 4:
		envelope = svg_tools.cells.cell_envelope(kind='animal', width=130,
			height=148, color='#FFC5BC').fragment
	else:
		envelope = ('<path d="M -48 -55 C -81 -83 -43 -111 -17 -93 '
			'C 4 -83 22 -109 32 -83 C 43 -57 78 -78 91 -55 '
			'C 111 -21 72 3 57 19 C 37 40 56 81 26 86 '
			'C -3 90 1 36 -24 36 C -51 37 -64 72 -96 64 '
			'C -136 53 -106 15 -84 14 C -60 13 -84 -15 -65 -24 '
			'C -47 -32 -44 -37 -48 -55 Z" fill="#D9D3B7" '
			'stroke="#344651" stroke-width="2.6"/>'
			'<path d="M -104 46 C -76 68 -51 29 -25 27 '
			'C 13 22 7 77 28 73 C 44 69 25 34 47 13 '
			'C 76 -10 91 -31 83 -50 C 105 -20 71 5 57 19 '
			'C 37 40 56 81 26 86 C -3 90 1 36 -24 36 '
			'C -51 37 -64 72 -96 64 Z" fill="#344651" opacity=".14"/>')
	nucleus = svg_tools.cells.nucleus(width=82, height=87, color='#C7A6C8').fragment
	model = svg_tools.chromosomes.Chromosome((
		svg_tools.chromosomes.Segment('', '#F2D16F', 5),
		svg_tools.chromosomes.Segment('', locus, 9),
		svg_tools.chromosomes.Segment('', '#F2D16F', 49),
	))
	rod = svg_tools.chromosomes.chromosome_part(f'stage-{stage}-chromosome', model,
		length=65, thickness=11, orientation='vertical', texture=False, labels=False)
	return (f'<g id="stage-{stage}" transform="translate({x} 198)">'
		f'<g id="stage-{stage}-cell">{envelope}</g>'
		f'<g id="stage-{stage}-nucleus">{nucleus}</g>'
		f'<g transform="translate(9 -38) rotate(20)">{rod.fragment}</g></g>')


#============================================
def main() -> None:
	"""Write one pure-vector original drawing with the preserved source relationships."""
	ink = '#344651'
	body = [cell(stage, x, '#E5BB45' if stage < 3 else '#D8433D')
		for stage, x in enumerate((120, 395, 660, 946), 1)]
	for start, end in ((218, 299), (484, 565), (744, 827)):
		body.append(f'<g id="transition-{start}"><path d="M {start} 198 H {end-15}" '
			f'fill="none" stroke="{ink}" stroke-width="2.5"/>'
			f'<path d="M {end-19} 192 L {end} 198 L {end-19} 204 Z" fill="{ink}"/></g>')
	body.append('<g id="mutagen-arrow"><path d="M 332 68 L 355 111 L 359 99 '
		'L 395 163" fill="none" stroke="#D8433D" stroke-width="5" '
		'stroke-linejoin="miter"/><path d="M 387 160 L 400 175 L 399 153 Z" '
		'fill="#D8433D"/></g>')
	body.append(f'<g id="locus-leaders" stroke="{ink}" stroke-width="1.8" '
		'fill="none"><path d="M 64 91 L 123 174"/>'
		'<path d="M 607 91 L 666 174"/></g>')
	for x, y, label in ((112, 78, 'proto-oncogene'), (360, 28, 'cancer-promoting agent'),
		(360, 56, '(UV light, chemicals, etc.)'), (600, 78, 'oncogene'),
		(950, 78, 'cancerous cell')):
		body.append(svg_tools.drawing.text(x, y, label, size=24, color=ink))
	svg_tools.drawing.write_svg(pathlib.Path(__file__).with_name('inherited_cancer.drawn.svg'),
		1090, 360, 'Somatic activation of a proto-oncogene',
		'Biotechnology LECT10 Topic 35. Four cells each contain one purple nucleus '
		'and one yellow single chromosome. A yellow proto-oncogene locus in the first '
		'two cells becomes a red oncogene locus in the last two. A red arrow from '
		'UV light or chemical agents points into the second cell. Three arrows show '
		'progression toward an irregular cancerous cell. Centromere positions are '
		'unknown; chromosome lengths are schematic. Source: inherited_cancer_legacy.png.',
		''.join(body))


if __name__ == '__main__':
	main()
