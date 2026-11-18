#!/usr/bin/env python3
"""Rebuild LECT09 mitotic and yeast chromosome diagrams from durable models."""
import argparse
import json
import pathlib
import subprocess

import lxml.etree
import svg_tools._xml
import svg_tools.chromosomes
import svg_tools.drawing


BASE = pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip()) / 'genetics/LECT09/djot'
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



def namespaced(element: lxml.etree._Element) -> lxml.etree._Element:
	"""Apply the SVG namespace to a renderer fragment."""
	for node in element.iter():
		if not node.tag.startswith('{'):
			node.tag = TAG + node.tag
	return element


def labeled_segments(model: dict) -> tuple:
	"""Split ancestry regions around explicitly modeled gene loci."""
	regions = model['regions']
	total = sum(region['length'] for region in regions)
	loci = model.get('loci', ())
	boundaries = {0, total}
	position = 0
	for region in regions:
		position += region['length']
		boundaries.add(position)
	for locus in loci:
		center = locus['center'] * total
		half = locus['length'] / 2
		if not 0 < center-half < center+half < total:
			raise ValueError(f"Locus does not fit its chromosome: {model['id']}")
		boundaries.update((center-half, center+half))
	intervals = []
	for start, end in zip(sorted(boundaries), sorted(boundaries)[1:]):
		middle = (start+end)/2
		locus = next((item for item in loci if abs(middle-item['center']*total) < item['length']/2), None)
		if locus:
			intervals.append(svg_tools.chromosomes.Segment(locus['label'], locus['color'], end-start))
			continue
		position = 0
		for region in regions:
			if middle < position+region['length']:
				intervals.append(svg_tools.chromosomes.Segment('', region['color'], end-start))
				break
			position += region['length']
	segments = tuple(intervals)
	return segments


def body_part(model: dict) -> lxml.etree._Element:
	"""Render one explicit centerline model with the shared body tool."""
	segments = labeled_segments(model)
	chromosome = svg_tools.chromosomes.Chromosome(segments)
	thickness = float(model['thickness'])
	if thickness.is_integer():
		thickness = int(thickness)
	part = svg_tools.chromosomes.chromosome_path_part(
		model['id'], chromosome, model['path'], thickness=thickness,
		labels=bool(model.get('loci')))
	element = namespaced(svg_tools._xml.parse(part.fragment))
	if not model.get('loci'):
		for region, source in zip((node for node in element if node.get('data-source-label') is not None),
			model['regions']):
			path = next(node for node in region if node.tag == TAG + 'path')
			path.set('d', source['path'])
	return element


def marker_part(identifier: str, thickness: float) -> lxml.etree._Element:
	"""Render one hollow centromere marker with the shared tool."""
	part = svg_tools.chromosomes.centromere_part(identifier, thickness=thickness)
	element = namespaced(svg_tools._xml.parse(part.fragment))
	return element


def replace(parent: lxml.etree._Element, old: lxml.etree._Element, new: lxml.etree._Element) -> None:
	"""Replace one direct child while preserving source order."""
	position = list(parent).index(old)
	parent.remove(old)
	parent.insert(position, new)


def build(name: str, model: dict) -> bytes:
	"""Fill the body-free template for one output SVG."""
	root = svg_tools._xml.read(DATA / name)
	bodies = {body['id']: body for body in model['bodies']}
	markers = {marker['id']: marker for marker in model['markers']}
	for parent in list(root.iter()):
		for slot in list(parent):
			body_id = slot.get('data-body-slot')
			marker_id = slot.get('data-marker-slot')
			if body_id:
				model = bodies[body_id]
				replace(parent, slot, body_part(model))
			elif marker_id:
				replace(parent, slot, marker_part(marker_id, markers[marker_id]['thickness']))
	svg_tools.drawing.remove_canvas_background(root)
	data = lxml.etree.tostring(svg_tools.drawing.svg_root(root), encoding='ascii', xml_declaration=True)
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
