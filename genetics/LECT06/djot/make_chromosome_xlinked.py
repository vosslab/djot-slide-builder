#!/usr/bin/env python3
"""Regenerate LECT06 chromosome schematics while retaining their native figure shells.

Run from the repository root: python3 genetics/LECT06/djot/make_chromosome_xlinked.py
"""

import json
import pathlib
import xml.etree.ElementTree

import svg_tools.chromosomes


#============================================
def generate(data_directory: pathlib.Path, repository_root: pathlib.Path) -> None:
	"""Paint shared chromosome bodies into explicit source-preserving template groups."""
	xml.etree.ElementTree.register_namespace('', 'http://www.w3.org/2000/svg')
	for model_path in sorted(data_directory.glob('*.json')):
		data = json.loads(model_path.read_text(encoding='utf-8'))
		root = xml.etree.ElementTree.parse(model_path.with_suffix('.template.svg')).getroot()
		groups = {element.attrib['id']: element for element in root.iter()
			if 'id' in element.attrib}
		for item in data['placements']:
			model = item['model']
			chromosome = svg_tools.chromosomes.Chromosome(tuple(
				svg_tools.chromosomes.Segment('', color, length)
				for color, length in model['segments']), model['centromere'])
			if 'path' in item:
				part = svg_tools.chromosomes.chromosome_path_part(
					item['group'] + '-shared', chromosome, item['path'],
					thickness=item['thickness'], labels=False)
			else:
				part = svg_tools.chromosomes.chromosome_part(
					item['group'] + '-shared', chromosome, length=item['length'],
					orientation=item['orientation'], thickness=item['thickness'],
					bands=False, labels=False)
			element = xml.etree.ElementTree.fromstring(part.fragment)
			if 'marker_center' in item:
				marker = next(node for node in element.iter()
					if node.attrib.get('id', '').endswith('-centromere'))
				x, y = item['marker_center']
				angle = marker.attrib['transform'].split('(')[1].split()[0]
				marker.set('cx', str(x))
				marker.set('cy', str(y))
				marker.set('transform', f'rotate({angle} {x} {y})')
			if 'translate' in item:
				element.set('transform', 'translate(' +
					' '.join(str(value) for value in item['translate']) + ')')
			groups[item['group']].insert(0, element)
		output = repository_root / data['target']
		output.parent.mkdir(parents=True, exist_ok=True)
		output.write_text(xml.etree.ElementTree.tostring(root, encoding='unicode') + '\n',
			encoding='utf-8')


#============================================
def main() -> None:
	module_directory = pathlib.Path(__file__).resolve().parent
	generate(module_directory / 'chromosome_models' / 'xlinked', module_directory.parents[2])


if __name__ == '__main__':
	main()
