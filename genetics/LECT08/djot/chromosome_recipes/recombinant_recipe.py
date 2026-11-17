#!/usr/bin/env python3
"""Rebuild the Morgan offspring composition using source chromosome colors."""
# Standard Library
import argparse
import json
import pathlib
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as DET
# local repo modules
import svg_tools.chromosomes


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse the output destination."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-o', '--output-root', dest='output_root', type=pathlib.Path)
	args = parser.parse_args()
	return args


#============================================
def main() -> None:
	"""Regenerate the source compositions."""
	HERE = pathlib.Path(__file__).resolve().parent
	args = parse_args()
	OUTPUT = args.output_root
	DESTINATIONS = json.loads((HERE / 'destinations.json').read_text())
	source = json.loads((HERE / 'recombinant_sources.json').read_text())
	root = DET.fromstring(source['svg'])
	for parent in root.iter():
		for child in list(parent):
			if 'data-shared-part' not in child.attrib:
				continue
			index = int(child.get('data-shared-part'))
			colors = source['parts'][index]
			if len(colors) == 1:
				regions = (svg_tools.chromosomes.Segment('', colors[0], 86), svg_tools.chromosomes.Segment('', colors[0], 86))
			else:
				regions = (svg_tools.chromosomes.Segment('', colors[0], 86), svg_tools.chromosomes.Segment('', colors[0], 50.22), svg_tools.chromosomes.Segment('', colors[1], 35.78))
			part = svg_tools.chromosomes.chromosome_path_part(f'chromosome-{index}', svg_tools.chromosomes.Chromosome(regions, centromeres=(svg_tools.chromosomes.Centromere(1),)), 'M-86 0 H86', thickness=12, labels=False)
			parent.insert(list(parent).index(child), DET.fromstring(part.fragment))
			parent.remove(child)
	for node in root.iter():
		if node.tag.startswith('{http://www.w3.org/2000/svg}'):
			node.tag = node.tag.split('}', 1)[1]
	root.set('xmlns', 'http://www.w3.org/2000/svg')
	output = (OUTPUT / 'morgan_recombinant_offspring.drawn.svg' if OUTPUT is not None else HERE.parent / 'assets' / DESTINATIONS['morgan_recombinant_offspring.drawn.svg'])
	output.parent.mkdir(parents=True, exist_ok=True)
	output.write_bytes(ET.tostring(root, encoding='utf-8', xml_declaration=True))


if __name__ == "__main__":
	main()
