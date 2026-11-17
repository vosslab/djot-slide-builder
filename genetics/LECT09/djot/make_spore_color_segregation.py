#!/usr/bin/env python3
"""Regenerate the spore-color segregation illustration."""
import json
import pathlib
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as DET

import svg_tools.chromosomes

BASE = pathlib.Path(__file__).resolve().parent
DATA = BASE / 'assets/lect09_spore_color_templates'
OUTPUT = BASE / 'assets/lect09b-tetrads_1_introduction/spore_color_segregation.drawn.svg'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)


def main() -> None:
	models = json.loads((DATA / 'models.json').read_text())
	root = DET.parse(DATA / 'composition.svg').getroot()
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
				element = DET.fromstring(part.fragment)
				for key, value in slot.attrib.items():
					if key.startswith('data-') and key != 'data-body-slot':
						element.set(key, value)
			elif marker is not None:
				index = int(marker)
				model = models['markers'][index]
				part = svg_tools.chromosomes.centromere_part(f'centromere-{index:02d}', thickness=8)
				element = DET.fromstring(part.fragment)
				element.set('transform', f"translate({model['cx']} {model['cy']})")
			else:
				continue
			position = list(parent).index(slot)
			parent.remove(slot)
			parent.insert(position, element)
	OUTPUT.parent.mkdir(parents=True, exist_ok=True)
	ET.ElementTree(root).write(OUTPUT, encoding='unicode', xml_declaration=True)


if __name__ == '__main__':
	main()
