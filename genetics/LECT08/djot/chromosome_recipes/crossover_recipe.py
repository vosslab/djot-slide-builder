#!/usr/bin/env python3
"""Rebuild crossover chromatids while preserving labels and source centromere marks."""
# Standard Library
import argparse
import json
import pathlib
import xml.etree.ElementTree
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
	for name, source in json.loads((HERE / 'crossover_sources.json').read_text()).items():
		root = xml.etree.ElementTree.fromstring(source['svg'])
		for parent in root.iter():
			for child in list(parent):
				if child.get('data-source-centromere') == 'true':
					x, y = float(child.get('cx')), float(child.get('cy'))
					marker_model = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('', '#777777', 10), svg_tools.chromosomes.Segment('', '#777777', 10)), 1)
					marker_part = svg_tools.chromosomes.chromosome_path_part(f'marker-{parent.get("id")}-{int(y)}', marker_model, f'M{x-10} {y} H{x+10}', thickness=14, labels=False)
					marker = next(n for n in xml.etree.ElementTree.fromstring(marker_part.fragment) if n.tag == 'ellipse')
					parent.insert(list(parent).index(child), marker)
					parent.remove(child)
					continue
				if 'data-shared-part' not in child.attrib:
					continue
				index = int(child.get('data-shared-part'))
				item = source['parts'][index]
				colors, lengths = item['colors'], item['lengths']
				if item['product']:
					model = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('', colors[0], 35), svg_tools.chromosomes.Segment('', colors[0], lengths[0]-35), svg_tools.chromosomes.Segment('', colors[1], lengths[1])), 1)
				else:
					model = svg_tools.chromosomes.Chromosome(tuple(svg_tools.chromosomes.Segment('', color, length) for color, length in zip(colors, lengths)))
				part = svg_tools.chromosomes.chromosome_path_part(f'chromatid-{index}', model, item['path'], thickness=14, labels=False)
				parent.insert(list(parent).index(child), xml.etree.ElementTree.fromstring(part.fragment))
				parent.remove(child)
		for node in root.iter():
			if node.tag.startswith('{http://www.w3.org/2000/svg}'):
				node.tag = node.tag.split('}', 1)[1]
		root.set('xmlns', 'http://www.w3.org/2000/svg')
		output = (OUTPUT / name if OUTPUT is not None else HERE.parent / 'assets' / DESTINATIONS[name])
		output.parent.mkdir(parents=True, exist_ok=True)
		output.write_bytes(xml.etree.ElementTree.tostring(root, encoding='utf-8', xml_declaration=True))


if __name__ == "__main__":
	main()
