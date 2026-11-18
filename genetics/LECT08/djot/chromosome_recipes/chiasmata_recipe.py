#!/usr/bin/env python3
"""Rebuild the two-chiasmata composition from source paths and shared parts."""
# Standard Library
import argparse
import json
import pathlib
# local repo modules
import lxml.etree
import svg_tools._xml
import svg_tools.chromosomes
import svg_tools.drawing



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
	source = json.loads((HERE / 'chiasmata_sources.json').read_text())
	root = svg_tools._xml.read(HERE / source['artwork'])
	markers = {}
	for parent in list(root.iter()):
		for child in list(parent):
			if 'data-shared-part' not in child.attrib:
				continue
			index = int(child.get('data-shared-part'))
			item = source['parts'][index]
			segments = (svg_tools.chromosomes.Segment('', item['color'], item['before']), svg_tools.chromosomes.Segment('', item['color'], item['after']))
			model = svg_tools.chromosomes.Chromosome(segments, 1 if item['marker'] else None)
			part = svg_tools.chromosomes.chromosome_path_part(f'chromatid-{index}', model, item['path'], thickness=23, labels=False)
			fragment = svg_tools._xml.parse(part.fragment)
			for node in list(fragment):
				if node.tag == 'ellipse' and node.get('id', '').endswith('-centromere'):
					if index in (0, 1):
						markers[index] = node
					fragment.remove(node)
			parent.insert(list(parent).index(child), fragment)
			parent.remove(child)
	for node in root.iter():
		if node.get('id') == 'teal-centromere':
			node.append(markers[0])
		if node.get('id') == 'blue-centromere':
			node.append(markers[1])
	output = (OUTPUT / 'two_chiasmata.drawn.svg' if OUTPUT is not None else HERE.parent / 'assets' / DESTINATIONS['two_chiasmata.drawn.svg'])
	output.parent.mkdir(parents=True, exist_ok=True)
	output.write_bytes(lxml.etree.tostring(svg_tools.drawing.svg_root(root), encoding='utf-8', xml_declaration=True))


if __name__ == "__main__":
	main()
