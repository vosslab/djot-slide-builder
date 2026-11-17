#!/usr/bin/env python3
"""Regenerate LECT13B/C source compositions using the shared chromosome family."""

import argparse
import base64
import json
import math
import pathlib
import xml.etree.ElementTree as ET

import svg_tools.chromosomes
import svg_tools.parts


#============================================
def generate(source_path: pathlib.Path, output_root: pathlib.Path) -> None:
	"""Keep authored text/composition and replace source-data chromosome placeholders."""
	sources = json.loads(source_path.read_text())
	image_name = 'lect13bc_inversion_exercise_source.png'
	image_uri = 'data:image/png;base64,' + base64.b64encode(
		(source_path.parent / image_name).read_bytes()).decode('ascii')
	for relative, source in sources.items():
		root = ET.fromstring(source['svg'].replace('local-image:' + image_name, image_uri))
		markers = {}
		for parent in list(root.iter()):
			for child in list(parent):
				if 'data-shared-part' not in child.attrib:
					continue
				index = int(child.attrib['data-shared-part'])
				data = source['parts'][index]
				centromeres = () if data['centromere_after'] is None else (
					svg_tools.chromosomes.Centromere(data['centromere_after']),)
				model = svg_tools.chromosomes.Chromosome(tuple(
					svg_tools.chromosomes.Segment(*segment) for segment in data['segments']),
					centromeres=centromeres)
				part = svg_tools.chromosomes.chromosome_path_part(f'migrated13bc-chromosome-{index}',
					model, data['path'], thickness=data['thickness'],
					cut_ends=data['cut_ends'], labels=False)
				replacement = ET.fromstring(part.fragment)
				replacement.attrib['data-source-part'] = str(index)
				replacement.attrib['stroke'] = 'none'
				if 'centromere' in part.anchors:
					markers[index] = (replacement, part.anchors['centromere'], data['thickness'])
				position = list(parent).index(child)
				parent.remove(child)
				parent.insert(position, replacement)
		if relative.endswith('inversion-double-crossover-problem.drawn.svg'):
			for number, (first_index, second_index) in enumerate(((0, 1), (2, 3))):
				first, second = markers[first_index], markers[second_index]
				for item in (first[0], second[0]):
					for marker in list(item):
						if marker.get('data-layer') == 'centromere':
							item.remove(marker)
				x1, y1 = first[1]
				x2, y2 = second[1]
				thickness = first[2]
				belt = svg_tools.chromosomes.centromere_part(
					f'migrated13bc-sister-belt-{number}', thickness=thickness,
					across=math.hypot(x2-x1, y2-y1)+thickness*1.3)
				root.append(ET.fromstring(svg_tools.parts.transform(belt,
					x=(x1+x2)/2, y=(y1+y2)/2,
					rotation=math.degrees(math.atan2(y2-y1, x2-x1))-90).fragment))
		path = output_root / relative
		path.parent.mkdir(parents=True, exist_ok=True)
		for node in root.iter():
			if node.tag.startswith('{http://www.w3.org/2000/svg}'):
				node.tag = node.tag.split('}', 1)[1]
		root.attrib['xmlns'] = 'http://www.w3.org/2000/svg'
		path.write_bytes(ET.tostring(root, encoding='ascii', xml_declaration=True))


#============================================
def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--output-root', type=pathlib.Path, default=pathlib.Path(__file__).parent)
	args = parser.parse_args()
	generate(pathlib.Path(__file__).with_name('lect13bc_chromosome_sources.json'), args.output_root)


if __name__ == '__main__':
	main()
