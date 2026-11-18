"""Replace chromosome bodies in the immutable source compositions for LECT10."""
import pathlib
import subprocess

import lxml.etree
import svg_tools._xml
import svg_tools.chromosomes
import svg_tools.chromosome_surface
import svg_tools.drawing
import svgpathtools

NS = 'http://www.w3.org/2000/svg'

HERE = pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip()) / 'genetics/LECT10/djot/lect10b_chromosome_recipe'

# Source centerlines run from the long arm, through the pole-facing centromere,
# to the shorter arm.  The two cubic segments meet at the original attachment.
CENTERLINES = {
	'metacentric': ('M 1030 121 Q 980 169 928 220', 'Q 980 271 1030 319', 110, 330),
	'submetacentric': ('M 1038 132 Q 957 163 928 220', 'Q 944 256 982 265', 110, 279),
	'acrocentric': ('M 1038 132 Q 957 163 928 220', 'L 942 238', 110, 245),
}


def main(kind: str, destination: pathlib.Path) -> None:
	first, second, top, bottom = CENTERLINES[kind]
	root = svg_tools._xml.read(HERE / 'templates' / f'{kind}_movement.drawn.svg')
	source_path = svgpathtools.parse_path(first + ' ' + second)
	source_join = source_path[0].end
	path = svg_tools.chromosome_surface.smooth_centerline(source_path)
	long_len = svg_tools.chromosome_surface.nearest_distance(path, source_join)
	short_len = path.length() - long_len
	daughter = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('', '#4c9ec7', long_len), svg_tools.chromosomes.Segment('', '#4c9ec7', short_len)),
		(svg_tools.chromosomes.Centromere(1),))
	length = bottom-top
	fraction = (220-top)/length
	metaphase = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('', '#4c9ec7', fraction), svg_tools.chromosomes.Segment('', '#4c9ec7', 1-fraction)),
		(svg_tools.chromosomes.Centromere(1),))
	rendered = svg_tools.chromosomes.render_chromosome_layout('metaphase-v2', metaphase, length=bottom-top,
		thickness=26, orientation='vertical', sisters=True, texture=False, labels=False)
	body = svg_tools._xml.parse(f'<g xmlns="{NS}" transform="translate(271.4 {top})">{rendered.svg}</g>')
	left = svg_tools.chromosomes.chromosome_path_part('left-daughter-v2', daughter, first + ' ' + second,
		thickness=26, labels=False)
	right = svg_tools.chromosomes.chromosome_path_part('right-daughter-v2', daughter, first + ' ' + second,
		thickness=26, labels=False)
	daughters = svg_tools._xml.parse(f'<g xmlns="{NS}">{left.fragment}<g transform="translate(2200 0) scale(-1 1)">{right.fragment}</g></g>')
	replacements = {'replicated-chromosome': body, 'daughter-chromosomes': daughters}
	remove = {'sister-join', 'paired-centromeric-units', 'daughter-centromeres'}
	for parent in list(root.iter()):
		for child in list(parent):
			name = child.get('id')
			if name in replacements:
				index = list(parent).index(child)
				parent.remove(child)
				parent.insert(index, replacements[name])
			elif name in remove:
				parent.remove(child)
	svg_tools.drawing.remove_canvas_background(root)
	lxml.etree.ElementTree(svg_tools.drawing.svg_root(root)).write(destination, encoding='utf-8', xml_declaration=False)
