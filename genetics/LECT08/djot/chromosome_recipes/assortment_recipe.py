#!/usr/bin/env python3
"""Rebuild independent-assortment panels with shared chromosome parts."""
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
	sources = json.loads((HERE / 'assortment_sources.json').read_text())
	for name, source in sources.items():
		root = svg_tools._xml.read(HERE / source['artwork'])
		for parent in list(root.iter()):
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
				group = lxml.etree.Element('g', {'transform': f"translate({item['x']-width*(1.1 if item['paired'] else .5)} {item['top']})"})
				group.append(svg_tools._xml.parse(part.fragment))
				parent.insert(list(parent).index(child), group)
				parent.remove(child)
		output = (OUTPUT / name if OUTPUT is not None else HERE.parent / 'assets' / DESTINATIONS[name])
		output.parent.mkdir(parents=True, exist_ok=True)
		output.write_bytes(lxml.etree.tostring(svg_tools.drawing.svg_root(root), encoding='utf-8', xml_declaration=True))


if __name__ == "__main__":
	main()
