#!/usr/bin/env python3
"""Rebuild the centromere teaching figure from its template and chromosome model."""
import argparse
import pathlib
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as DET

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
	), centromeres=(svg_tools.chromosomes.Centromere(1),))
	layout = svg_tools.chromosomes.render_chromosome_layout(
		'centromere-drawn', model, length=190, thickness=27, orientation='vertical',
		sisters=True, texture=False, labels=False)
	return DET.fromstring(layout.svg)



#============================================
def main() -> None:
	"""Render the shared chromosome into the durable nonbody composition template."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--output-root', type=pathlib.Path, default=OUTPUT.parent)
	args = parser.parse_args()
	ET.register_namespace('', NS)
	root = DET.parse(ASSETS / 'centromere.svg').getroot()
	for parent in root.iter():
		for node in list(parent):
			if node.get('data-chromosome-slot'):
				index = list(parent).index(node)
				parent.remove(node)
				parent.insert(index, chromosome_body())
	for element in root.iter():
		element.tag = element.tag.rsplit('}', 1)[-1]
	output_dir = args.output_root / 'lect09_tetrad_concepts'
	output_dir.mkdir(parents=True, exist_ok=True)
	data = ET.tostring(root, encoding='unicode')
	data = data.replace('<svg ', '<svg xmlns="' + NS + '" ', 1)
	(output_dir / 'centromere.drawn.svg').write_text("<?xml version='1.0' encoding='utf-8'?>\n" + data)


if __name__ == '__main__':
	main()
