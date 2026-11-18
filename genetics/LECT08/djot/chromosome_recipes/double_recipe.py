#!/usr/bin/env python3
"""Rebuild the eight-cell double crossover composition."""
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
	HERE=pathlib.Path(__file__).resolve().parent
	args = parse_args()
	OUTPUT = args.output_root
	DESTINATIONS = json.loads((HERE / 'destinations.json').read_text())
	source=json.loads((HERE/'double_sources.json').read_text())
	root=svg_tools._xml.read(HERE / source['artwork'])
	for parent in list(root.iter()):
		for child in list(parent):
			if 'data-shared-part' not in child.attrib:
				continue
			i=int(child.get('data-shared-part'))
			item=source['parts'][i]
			model=svg_tools.chromosomes.Chromosome(tuple(svg_tools.chromosomes.Segment('',color,length) for color,length in item['regions']),centromeres=(() if item['center'] is None else (svg_tools.chromosomes.Centromere(item['center']),)))
			part=svg_tools.chromosomes.chromosome_path_part(f'chromatid-{i}',model,item['path'],thickness=9.5,labels=False)
			parent.insert(list(parent).index(child),svg_tools._xml.parse(part.fragment))
			parent.remove(child)
	out=(OUTPUT / 'double_crossover_meiosis.drawn.svg' if OUTPUT is not None else HERE.parent / 'assets' / DESTINATIONS['double_crossover_meiosis.drawn.svg'])
	out.parent.mkdir(parents=True, exist_ok=True)
	out.write_bytes(lxml.etree.tostring(svg_tools.drawing.svg_root(root),encoding='utf-8',xml_declaration=True))


if __name__ == "__main__":
	main()
