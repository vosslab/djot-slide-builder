#!/usr/bin/env python3
"""Rebuild the map-unit trace with attached allele-locus blocks."""
# Standard Library
import argparse
import json
import pathlib
# local repo modules
import subprocess
import lxml.etree
import svg_tools._xml
import svg_tools.chromosomes
import svg_tools.drawing


LOCUS_FILL = '#F3D788'


#============================================
def attach_allele_loci(root: lxml.etree._Element) -> None:
	"""Place the six supplied allele blocks directly on their thin source chromatids."""
	positions = {('146', '126'): '169', ('566', '126'): '169', ('986', '126'): '169',
		('146', '286'): '329', ('566', '286'): '329', ('986', '286'): '329'}
	text_positions = {('180', '173'): '208', ('600', '173'): '208', ('1020', '173'): '208',
		('180', '333'): '368', ('600', '333'): '368', ('1020', '333'): '368'}
	for node in root.iter():
		if node.tag.endswith('rect') and (node.get('x'), node.get('y')) in positions:
			node.set('y', positions[(node.get('x'), node.get('y'))])
			node.set('fill', LOCUS_FILL)
			node.set('stroke', '#344651')
			node.set('rx', '8')
		elif node.tag.endswith('text') and (node.get('x'), node.get('y')) in text_positions:
			node.set('y', text_positions[(node.get('x'), node.get('y'))])
			node.set('fill', '#172B3A')


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
	HERE = pathlib.Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()) / 'genetics/LECT08/djot/chromosome_recipes'
	args = parse_args()
	OUTPUT = args.output_root
	DESTINATIONS = json.loads((HERE / 'destinations.json').read_text())
	source=json.loads((HERE/'exchanges_sources.json').read_text())
	root=svg_tools._xml.read(HERE / source['artwork'])
	attach_allele_loci(root)
	for parent in list(root.iter()):
		for child in list(parent):
			if 'data-shared-part' not in child.attrib:
				continue
			i=int(child.get('data-shared-part'))
			item=source['parts'][i]
			model=svg_tools.chromosomes.Chromosome(tuple(svg_tools.chromosomes.Segment('',color,length) for color,length in item['regions']))
			part=svg_tools.chromosomes.chromosome_path_part(f'chromatid-{i}',model,item['path'],thickness=item['width'],labels=False)
			parent.insert(list(parent).index(child),svg_tools._xml.parse(part.fragment))
			parent.remove(child)
	out=(OUTPUT if OUTPUT is not None else HERE.parent / 'assets') / DESTINATIONS['two_exchanges.drawn.svg']
	out.parent.mkdir(parents=True, exist_ok=True)
	out.write_bytes(lxml.etree.tostring(svg_tools.drawing.svg_root(root),encoding='utf-8',xml_declaration=True))


if __name__ == "__main__":
	main()
