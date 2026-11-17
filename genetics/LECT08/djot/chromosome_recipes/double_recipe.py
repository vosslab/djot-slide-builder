#!/usr/bin/env python3
"""Rebuild the eight-cell double crossover composition."""
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
	HERE=pathlib.Path(__file__).resolve().parent
	args = parse_args()
	OUTPUT = args.output_root
	DESTINATIONS = json.loads((HERE / 'destinations.json').read_text())
	source=json.loads((HERE/'double_sources.json').read_text())
	root=xml.etree.ElementTree.fromstring(source['svg'])
	for parent in root.iter():
		for child in list(parent):
			if 'data-shared-part' not in child.attrib:
				continue
			i=int(child.get('data-shared-part'))
			item=source['parts'][i]
			model=svg_tools.chromosomes.Chromosome(tuple(svg_tools.chromosomes.Segment('',color,length) for color,length in item['regions']),centromeres=(() if item['center'] is None else (svg_tools.chromosomes.Centromere(item['center']),)))
			part=svg_tools.chromosomes.chromosome_path_part(f'chromatid-{i}',model,item['path'],thickness=9.5,labels=False)
			parent.insert(list(parent).index(child),xml.etree.ElementTree.fromstring(part.fragment))
			parent.remove(child)
	for node in root.iter():
		if node.tag.startswith('{http://www.w3.org/2000/svg}'):
			node.tag = node.tag.split('}',1)[1]
	root.set('xmlns','http://www.w3.org/2000/svg')
	out=(OUTPUT / 'double_crossover_meiosis.drawn.svg' if OUTPUT is not None else HERE.parent / 'assets' / DESTINATIONS['double_crossover_meiosis.drawn.svg'])
	out.parent.mkdir(parents=True, exist_ok=True)
	out.write_bytes(xml.etree.ElementTree.tostring(root,encoding='utf-8',xml_declaration=True))


if __name__ == "__main__":
	main()
