#!/usr/bin/env python3
"""Regenerate the spore-color segregation illustration."""
import json
import pathlib

import lxml.etree
import svg_tools._xml
import svg_tools.chromosomes
import svg_tools.drawing

BASE = pathlib.Path(__file__).resolve().parent
DATA = BASE / 'assets/lect09_spore_color_templates'
OUTPUT = BASE / 'assets/lect09b-tetrads_1_introduction/spore_color_segregation.drawn.svg'
NS = 'http://www.w3.org/2000/svg'



def main() -> None:
	models = json.loads((DATA / 'models.json').read_text())
	root = svg_tools._xml.read(DATA / 'composition.svg')
	for parent in list(root.iter()):
		for slot in list(parent):
			body = slot.get('data-body-slot')
			marker = slot.get('data-marker-slot')
			if body is not None:
				index = int(body)
				model = models['segments'][index]
				chromosome = svg_tools.chromosomes.Chromosome((
					svg_tools.chromosomes.Segment('', model['stroke']),))
				part = svg_tools.chromosomes.chromosome_path_part(
					f'chromatid-{index:02d}', chromosome, model['d'], thickness=8, labels=False)
				element = svg_tools._xml.parse(part.fragment)
				for key, value in slot.attrib.items():
					if key.startswith('data-') and key != 'data-body-slot':
						element.set(key, value)
			elif marker is not None:
				index = int(marker)
				model = models['markers'][index]
				part = svg_tools.chromosomes.centromere_part(f'centromere-{index:02d}', thickness=8)
				element = svg_tools._xml.parse(part.fragment)
				element.set('transform', f"translate({model['cx']} {model['cy']})")
			else:
				continue
			position = list(parent).index(slot)
			parent.remove(slot)
			parent.insert(position, element)
	OUTPUT.parent.mkdir(parents=True, exist_ok=True)
	lxml.etree.ElementTree(svg_tools.drawing.svg_root(root)).write(OUTPUT, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
	main()
