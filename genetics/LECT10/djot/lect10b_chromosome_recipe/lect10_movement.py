"""Replace chromosome bodies in the immutable source compositions for LECT10."""
import pathlib
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as DET

import svg_tools.chromosomes
import svgpathtools

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
HERE = pathlib.Path(__file__).resolve().parent

# Source centerlines run from the long arm, through the pole-facing centromere,
# to the shorter arm.  The two cubic segments meet at the original attachment.
CENTERLINES = {
	'metacentric': ('M 1030 121 Q 980 169 928 220', 'Q 980 271 1030 319', 110, 330),
	'submetacentric': ('M 1038 132 Q 957 163 928 220', 'Q 944 256 982 265', 110, 279),
	'acrocentric': ('M 1038 132 Q 957 163 928 220', 'L 942 238', 110, 245),
}


def main(kind: str, destination: pathlib.Path) -> None:
	first, second, top, bottom = CENTERLINES[kind]
	root = DET.parse(HERE / 'templates' / f'{kind}_movement.drawn.svg').getroot()
	path = svgpathtools.parse_path(first + ' ' + second)
	long_len, short_len = (segment.length() for segment in path)
	daughter = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('', '#4c9ec7', long_len), svg_tools.chromosomes.Segment('', '#4c9ec7', short_len)),
		(svg_tools.chromosomes.Centromere(1),))
	length = bottom-top
	fraction = (220-top)/length
	metaphase = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('', '#4c9ec7', fraction), svg_tools.chromosomes.Segment('', '#4c9ec7', 1-fraction)),
		(svg_tools.chromosomes.Centromere(1),))
	rendered = svg_tools.chromosomes.render_chromosome_layout('metaphase-v2', metaphase, length=bottom-top,
		thickness=26, orientation='vertical', sisters=True, texture=False, labels=False)
	body = DET.fromstring(f'<g xmlns="{NS}" transform="translate(271.4 {top})">{rendered.svg}</g>')
	left = svg_tools.chromosomes.chromosome_path_part('left-daughter-v2', daughter, first + ' ' + second,
		thickness=26, labels=False)
	right = svg_tools.chromosomes.chromosome_path_part('right-daughter-v2', daughter, first + ' ' + second,
		thickness=26, labels=False)
	daughters = DET.fromstring(f'<g xmlns="{NS}">{left.fragment}<g transform="translate(2200 0) scale(-1 1)">{right.fragment}</g></g>')
	replacements = {'replicated-chromosome': body, 'daughter-chromosomes': daughters}
	remove = {'sister-join', 'paired-centromeric-units', 'daughter-centromeres'}
	for parent in root.iter():
		for child in list(parent):
			name = child.get('id')
			if name in replacements:
				index = list(parent).index(child)
				parent.remove(child)
				parent.insert(index, replacements[name])
			elif name in remove:
				parent.remove(child)
	ET.ElementTree(root).write(destination, encoding='unicode', xml_declaration=False)
