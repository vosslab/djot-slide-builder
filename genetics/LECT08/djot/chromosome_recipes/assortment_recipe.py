#!/usr/bin/env python3
"""Rebuild independent-assortment panels with shared chromosome parts."""
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
	sources = json.loads((HERE / 'assortment_sources.json').read_text())
	for name, source in sources.items():
		root = DET.fromstring(source['svg'])
		for parent in root.iter():
			for child in list(parent):
				if 'data-shared-part' not in child.attrib:
					continue
				index = int(child.get('data-shared-part'))
				item = source['parts'][index]
				model = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('', item['color'], item['center']-item['top']),
									svg_tools.chromosomes.Segment('', item['color'], item['bottom']-item['center'])),
									centromeres=(svg_tools.chromosomes.Centromere(1),))
				width = 7
				part = svg_tools.chromosomes.chromosome_part(f'chromosome-{index}', model,
					length=item['bottom']-item['top'], thickness=width,
					orientation='vertical', sisters=item['paired'], texture=False, labels=False)
				group = ET.Element('g', {'transform': f"translate({item['x']-width*(1.1 if item['paired'] else .5)} {item['top']})"})
				group.append(DET.fromstring(part.fragment))
				parent.insert(list(parent).index(child), group)
				parent.remove(child)
		for node in root.iter():
			if node.tag.startswith('{http://www.w3.org/2000/svg}'):
				node.tag = node.tag.split('}', 1)[1]
		root.set('xmlns', 'http://www.w3.org/2000/svg')
		output = (OUTPUT / name if OUTPUT is not None else HERE.parent / 'assets' / DESTINATIONS[name])
		output.parent.mkdir(parents=True, exist_ok=True)
		output.write_bytes(ET.tostring(root, encoding='utf-8', xml_declaration=True))


if __name__ == "__main__":
	main()
