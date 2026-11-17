#!/usr/bin/env python3
"""Regenerate LECT06 chromosome schematics while retaining their native figure shells.

Run from the repository root: python3 genetics/LECT06/djot/make_chromosome_xlinked.py
"""

import json
import pathlib
import subprocess
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as DET

import svg_tools.chromosomes
import svg_tools.drawing


#============================================
def generate(data_directory: pathlib.Path, repository_root: pathlib.Path,
	output_root: pathlib.Path | None = None) -> None:
	"""Paint shared chromosome bodies into explicit source-preserving template groups."""
	ET.register_namespace('', 'http://www.w3.org/2000/svg')
	for model_path in sorted(data_directory.glob('*.json')):
		data = json.loads(model_path.read_text(encoding='utf-8'))
		root = DET.parse(model_path.with_suffix('.template.svg')).getroot()
		groups = {element.attrib['id']: element for element in root.iter()
			if 'id' in element.attrib}
		for item in data['placements']:
			model = item['model']
			chromosome = svg_tools.chromosomes.Chromosome(tuple(
				svg_tools.chromosomes.Segment('', color, length)
			for color, length in model['segments']), centromeres=(
				svg_tools.chromosomes.Centromere(model['centromere']),)
			if model['centromere'] is not None else ())
			if 'path' in item:
				part = svg_tools.chromosomes.chromosome_path_part(
					item['group'] + '-shared', chromosome, item['path'],
					thickness=item['thickness'], labels=False)
			else:
				part = svg_tools.chromosomes.chromosome_part(
					item['group'] + '-shared', chromosome, length=item['length'],
					orientation=item['orientation'], thickness=item['thickness'],
					texture=False, labels=False)
			element = DET.fromstring(part.fragment)
			if 'translate' in item:
				element.set('transform', 'translate(' +
					' '.join(str(value) for value in item['translate']) + ')')
			groups[item['group']].insert(0, element)
		output = (repository_root / data['target'] if output_root is None else
			output_root / 'assets' / data['target'].split('/assets/', 1)[1])
		output.parent.mkdir(parents=True, exist_ok=True)
		svg_tools.drawing.remove_canvas_background(root)
		output.write_bytes(ET.tostring(root, encoding='ascii', xml_declaration=False) + b'\n')


#============================================
def main() -> None:
	repository = pathlib.Path(subprocess.check_output(
		['git', 'rev-parse', '--show-toplevel'], text=True).strip())
	generate(repository / 'genetics/LECT06/djot/chromosome_models/xlinked', repository)


if __name__ == '__main__':
	main()
