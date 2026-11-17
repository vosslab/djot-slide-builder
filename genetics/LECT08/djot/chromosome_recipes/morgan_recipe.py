#!/usr/bin/env python3
"""Rebuild Morgan rod panels using shared chromosome parts."""
# Standard Library
import argparse
import json
import pathlib
import defusedxml.ElementTree as ET
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
	for name, source in json.loads((HERE / 'morgan_sources.json').read_text()).items():
		root = ET.fromstring(source['svg'])
		for parent in root.iter():
			for child in list(parent):
				if 'data-shared-part' not in child.attrib:
					continue
				index = int(child.get('data-shared-part'))
				item = source['parts'][index]
				model = svg_tools.chromosomes.Chromosome(tuple(svg_tools.chromosomes.Segment('', c, n) for c, n in zip(item['colors'], item['lengths'])))
				part = svg_tools.chromosomes.chromosome_path_part(f'chromosome-{index}', model, item['path'], thickness=item['width'], labels=False)
				parent.insert(list(parent).index(child), ET.fromstring(part.fragment))
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
