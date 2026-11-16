#!/usr/bin/env python3
"""Rebuild the centromere teaching figure from its template and chromosome model."""
import pathlib
import xml.etree.ElementTree as ET

import svg_tools.chromosomes


BASE = pathlib.Path(__file__).resolve().parent
ASSETS = BASE / 'assets/lect09_ordered_templates'
OUTPUT = BASE / 'assets/lect09_tetrad_concepts'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)


#============================================
def chromosome_body() -> ET.Element:
	"""Build the two-sister chromosome with its source-positioned marker.

	Returns:
		Shared chromosome-tool SVG group for the illustrated chromosome.
	"""
	model = svg_tools.chromosomes.Chromosome((
		svg_tools.chromosomes.Segment('', '#4D8EC3', 70),
		svg_tools.chromosomes.Segment('', '#9773B8', 115),
	), 1)
	layout = svg_tools.chromosomes.render_chromosome_layout(
		'centromere-drawn', model, length=190, thickness=103, orientation='vertical',
		sisters=True, bands=False, labels=False,
	)
	replacement = ET.fromstring(layout.svg)
	marker = replacement.find(".//ellipse[@id='centromere-drawn-centromere']")
	marker_parent = next(group for group in replacement.iter() if marker in list(group))
	marker_position = list(marker_parent).index(marker)
	source_transform = marker.get('transform')
	marker_parent.remove(marker)
	canonical = ET.fromstring(svg_tools.chromosomes.centromere_part(
		'centromere-drawn', thickness=27,
	).fragment)
	canonical.set('cx', '76.5354054054054')
	canonical.set('cy', '51.5')
	if source_transform:
		canonical.set('transform', source_transform)
	marker_parent.insert(marker_position, canonical)
	return replacement


#============================================
def main() -> None:
	"""Render the shared chromosome into the durable nonbody composition template."""
	ET.register_namespace('', NS)
	root = ET.parse(ASSETS / 'centromere.svg').getroot()
	for parent in root.iter():
		for node in list(parent):
			if node.get('data-chromosome-slot'):
				index = list(parent).index(node)
				parent.remove(node)
				parent.insert(index, chromosome_body())
	for element in root.iter():
		element.tag = element.tag.rsplit('}', 1)[-1]
	OUTPUT.mkdir(parents=True, exist_ok=True)
	data = ET.tostring(root, encoding='unicode')
	data = data.replace('<svg ', '<svg xmlns="' + NS + '" ', 1)
	(OUTPUT / 'centromere.drawn.svg').write_text("<?xml version='1.0' encoding='utf-8'?>\n" + data)


if __name__ == '__main__':
	main()
