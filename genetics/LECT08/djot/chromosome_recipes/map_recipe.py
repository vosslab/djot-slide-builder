#!/usr/bin/env python3
"""Rebuild the map-unit meioses and their source chromosome paths."""
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
	source=json.loads((HERE/'map_sources.json').read_text())
	root=svg_tools._xml.read(HERE / source['artwork'])
	for parent in list(root.iter()):
		for child in list(parent):
			if child.get('data-source-centromere') == 'true':
				x,y=float(child.get('cx')),float(child.get('cy'))
				model=svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('','#777777',10),svg_tools.chromosomes.Segment('','#777777',10)),centromeres=(svg_tools.chromosomes.Centromere(1),))
				part=svg_tools.chromosomes.chromosome_path_part(f'marker-{parent.get("id")}-{int(y)}',model,f'M{x-10} {y} H{x+10}',thickness=12,labels=False)
				marker=next(n for n in svg_tools._xml.parse(part.fragment) if n.tag=='ellipse')
				parent.insert(list(parent).index(child),marker)
				parent.remove(child)
				continue
			if 'data-shared-part' not in child.attrib:
				continue
			i=int(child.get('data-shared-part'))
			item=source['parts'][i]
			model=svg_tools.chromosomes.Chromosome(tuple(svg_tools.chromosomes.Segment('',color,length) for color,length in item['regions']))
			part=svg_tools.chromosomes.chromosome_path_part(f'chromatid-{i}',model,item['path'],thickness=12,labels=False)
			parent.insert(list(parent).index(child),svg_tools._xml.parse(part.fragment))
			parent.remove(child)
	out=(OUTPUT / 'one_map_unit.drawn.svg' if OUTPUT is not None else HERE.parent / 'assets' / DESTINATIONS['one_map_unit.drawn.svg'])
	out.parent.mkdir(parents=True, exist_ok=True)
	out.write_bytes(lxml.etree.tostring(svg_tools.drawing.svg_root(root),encoding='utf-8',xml_declaration=True))


if __name__ == "__main__":
	main()
