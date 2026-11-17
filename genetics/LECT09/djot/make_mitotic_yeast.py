#!/usr/bin/env python3
"""Rebuild LECT09 mitotic and yeast chromosome diagrams from durable models."""
import argparse
import json
import pathlib
import xml.etree.ElementTree as ET

import svg_tools.chromosomes


BASE = pathlib.Path(__file__).resolve().parent
DATA = BASE / 'assets/mitotic_yeast_templates'
OUTPUT = BASE / 'assets'
DESTINATIONS = {
	'mitotic_twin_spots.drawn.svg': 'lect09b-tetrads_1_introduction',
	'loh_outcome.drawn.svg': 'lect09c-mitotic_crossover',
	'repair_templates.drawn.svg': 'lect09c-mitotic_crossover',
	'yeast_meiosis.drawn.svg': 'lect09d-yeast_unordered_tetrads',
}
NS = 'http://www.w3.org/2000/svg'
TAG = '{' + NS + '}'
ET.register_namespace('', NS)


def namespaced(element: ET.Element) -> ET.Element:
	"""Apply the SVG namespace to a renderer fragment."""
	for node in element.iter():
		if not node.tag.startswith('{'):
			node.tag = TAG + node.tag
	return element


def body_part(model: dict) -> ET.Element:
	"""Render one explicit centerline model with the shared body tool."""
	segments = tuple(svg_tools.chromosomes.Segment('', region['color'], region['length'])
		for region in model['regions'])
	chromosome = svg_tools.chromosomes.Chromosome(segments)
	thickness = float(model['thickness'])
	if thickness.is_integer():
		thickness = int(thickness)
	part = svg_tools.chromosomes.chromosome_path_part(
		model['id'], chromosome, model['path'], thickness=thickness, labels=False)
	element = namespaced(ET.fromstring(part.fragment))
	for region, source in zip((node for node in element if node.get('data-source-label') is not None),
		model['regions']):
		path = next(node for node in region if node.tag == TAG + 'path')
		path.set('d', source['path'])
	return element


def marker_part(identifier: str, thickness: float) -> ET.Element:
	"""Render one hollow centromere marker with the shared tool."""
	part = svg_tools.chromosomes.centromere_part(identifier, thickness=thickness)
	element = namespaced(ET.fromstring(part.fragment))
	return element


def replace(parent: ET.Element, old: ET.Element, new: ET.Element) -> None:
	"""Replace one direct child while preserving source order."""
	position = list(parent).index(old)
	parent.remove(old)
	parent.insert(position, new)


def build(name: str, model: dict) -> bytes:
	"""Fill the body-free template for one output SVG."""
	root = ET.parse(DATA / name).getroot()
	bodies = {body['id']: body for body in model['bodies']}
	markers = {marker['id']: marker for marker in model['markers']}
	for parent in root.iter():
		for slot in list(parent):
			body_id = slot.get('data-body-slot')
			marker_id = slot.get('data-marker-slot')
			if body_id:
				replace(parent, slot, body_part(bodies[body_id]))
			elif marker_id:
				replace(parent, slot, marker_part(marker_id, markers[marker_id]['thickness']))
	data = ET.tostring(root, encoding='utf-8', xml_declaration=True)
	return data


def main() -> None:
	"""Write all four durable LECT09 SVG outputs."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--output-root', type=pathlib.Path, default=OUTPUT)
	args = parser.parse_args()
	models = json.loads((DATA / 'models.json').read_text())
	for name, model in models.items():
		output = args.output_root / DESTINATIONS[name] / name
		output.parent.mkdir(parents=True, exist_ok=True)
		output.write_bytes(build(name, model))


if __name__ == '__main__':
	main()
