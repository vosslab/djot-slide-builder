#!/usr/bin/env python3
"""Rebuild linked and unlinked genes in the original cells."""
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
	source=json.loads((HERE/'cell_sources.json').read_text())
	root=svg_tools._xml.read(HERE / source['artwork'])
	for parent in list(root.iter()):
		for child in list(parent):
			if 'data-shared-part' not in child.attrib:
				continue
			index=int(child.get('data-shared-part'))
			item=source['parts'][index]
			model=svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('',item['color'],item['center']-item['top']),svg_tools.chromosomes.Segment('',item['color'],item['bottom']-item['center'])),centromeres=(svg_tools.chromosomes.Centromere(1),))
			path=f"M{item['x']} {item['top']} V{item['bottom']}"
			part=svg_tools.chromosomes.chromosome_path_part(f'chromosome-{index}',model,path,thickness=20,labels=False)
			parent.insert(list(parent).index(child),svg_tools._xml.parse(part.fragment))
			parent.remove(child)
	for node in root.iter():
		if node.tag.startswith('{http://www.w3.org/2000/svg}'):
			node.tag=node.tag.split('}',1)[1]
	root.set('xmlns','http://www.w3.org/2000/svg')
	output=(OUTPUT / 'linked_unlinked_gene_cell.drawn.svg' if OUTPUT is not None else HERE.parent / 'assets' / DESTINATIONS['linked_unlinked_gene_cell.drawn.svg'])
	output.parent.mkdir(parents=True, exist_ok=True)
	output.write_bytes(lxml.etree.tostring(svg_tools.drawing.svg_root(root),encoding='utf-8',xml_declaration=True))


if __name__ == "__main__":
	main()
