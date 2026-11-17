#!/usr/bin/env python3
"""Regenerate source-based inversion figures using shared chromosome geometry."""

import argparse
import base64
import copy
import json
import math
import pathlib
import xml.etree.ElementTree as ET

import svg_tools.chromosomes as chromosomes
import svg_tools.parts


HERE = pathlib.Path(__file__).parent
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)


#============================================
def replace_markers(root: ET.Element, name: str) -> dict[str, tuple[ET.Element, ET.Element, float, float, float]]:
	"""Replace source centromere symbols at their recorded positions."""
	count = 0
	markers = {}
	for parent in list(root.iter()):
		for child in list(parent):
			ident = child.get('id', '')
			if child.tag.endswith('g') and 'centromere' in ident:
				first = next(iter(child))
				x, y = float(first.attrib['cx']), float(first.attrib['cy'])
				thickness, color = float(first.attrib['ry']) * 1.22, first.attrib['fill']
			elif child.tag.endswith('circle') and 'centromere' in ident:
				x, y = float(child.attrib['cx']), float(child.attrib['cy'])
				thickness, color = 32, '#8cafa1'
			elif child.get('data-marker-x') is not None:
				x, y = float(child.attrib['data-marker-x']), float(child.attrib['data-marker-y'])
				thickness, color = 49, child.attrib['fill']
			else:
				continue
			model = chromosomes.Chromosome((chromosomes.Segment('', color),
				chromosomes.Segment('', color)),
				centromeres=(chromosomes.Centromere(1),))
			part = chromosomes.chromosome_path_part(f'lect13b-{name}-marker-{count}', model,
				f'M {x-thickness/2} {y} L {x+thickness/2} {y}',
				thickness=thickness, cut_ends=True, labels=False)
			replacement = ET.fromstring(part.fragment)
			replacement.set('stroke', 'none')
			index = list(parent).index(child)
			parent.remove(child)
			parent.insert(index, replacement)
			markers[ident] = (parent, replacement, x, y, thickness)
			count += 1
	return markers


#============================================
def replace_sister_markers(name: str,
	markers: dict[str, tuple[ET.Element, ET.Element, float, float, float]], pairs: tuple[tuple[str, str], ...]) -> None:
	"""Replace two source collars with one foreground belt for each known sister pair."""
	for number, (first_name, second_name) in enumerate(pairs):
		first = markers[first_name]
		second = markers[second_name]
		if first[0] is not second[0]:
			raise ValueError(f'Sister centromeres do not share a coordinate frame: {first_name}, {second_name}')
		for parent, replacement, *_ in (first, second):
			parent.remove(replacement)
		x1, y1, thickness = first[2:]
		x2, y2 = second[2:4]
		span = math.hypot(x2-x1, y2-y1) + thickness*1.3
		belt = chromosomes.centromere_part(f'lect13b-{name}-sister-belt-{number}',
			thickness=thickness, across=span)
		angle = math.degrees(math.atan2(y2-y1, x2-x1))-90
		# Marker coordinates are local to their shared parent.  In the anaphase
		# figures that parent is the scaled Stage A group, not the document root.
		first[0].append(ET.fromstring(svg_tools.parts.transform(belt,
			x=(x1+x2)/2, y=(y1+y2)/2, rotation=angle).fragment))


#============================================
def render_source(name: str, source: dict) -> ET.Element:
	"""Build one source-preserving composition from its shell and body data."""
	root = ET.fromstring(source['svg'])
	for parent in root.iter():
		for child in list(parent):
			if 'data-shared-part' not in child.attrib:
				continue
			index = int(child.get('data-shared-part'))
			data = source['parts'][index]
			model = chromosomes.Chromosome((chromosomes.Segment('', data['color']),))
			part = chromosomes.chromosome_path_part(f'lect13b-{name}-{index}', model, data['path'],
				thickness=data['thickness'], cut_ends=data['cut'], labels=False)
			position = list(parent).index(child)
			parent.remove(child)
			replacement = ET.fromstring(part.fragment)
			replacement.set('stroke', 'none')
			parent.insert(position, replacement)
	markers = replace_markers(root, name)
	if name in ('paracentric-anaphase', 'pericentric-anaphase'):
		replace_sister_markers(name, markers, (
			('paired-orange-centromere', 'paired-ochre-centromere'),
			('paired-green-centromere', 'paired-blue-centromere'),
		))
	if name == 'pericentric-pairing':
		replace_sister_markers(name, markers, (
			('orange-centromere', 'ochre-centromere'),
			('green-centromere', 'blue-centromere'),
		))
		# Continuous chromatids establish the crossover order; separate overpass strokes
		# leave false white breaks at the starts of the lower loop.
		for parent in root.iter():
			for child in list(parent):
				if child.get('id') in ('green-foreground-overpass', 'blue-foreground-overpass'):
					parent.remove(child)
	if name == 'inversion_loop_without_crossover':
		markers = [item for item in root if item.get('id', '').startswith(
			'lect13b-inversion_loop_without_crossover-marker-')]
		labels = []
		for chromatid in root:
			if chromatid.get('id', '').startswith('chromatid-'):
				for child in list(chromatid):
					if child.tag.endswith('text'):
						chromatid.remove(child)
						labels.append(child)
		for node in markers:
			root.remove(node)
		last = max(i for i, item in enumerate(root) if item.get('id', '').startswith('chromatid-'))
		for node in reversed(markers + labels):
			root.insert(last + 1, node)
	return root


#============================================
def image_006(body: ET.Element, source: dict) -> ET.Element:
	"""Use the reference crop and callout with its four editable chromatids."""
	root = ET.Element(f'{{{NS}}}svg', {'width': '784', 'height': '467',
		'viewBox': '0 0 784 467', 'role': 'img'})
	ET.SubElement(root, f'{{{NS}}}title').text = 'Inversion loop'
	ET.SubElement(root, f'{{{NS}}}desc').text = 'Four chromatids pair in an inversion loop without crossing over.'
	group = ET.SubElement(root, f'{{{NS}}}g', {'transform': 'translate(-55 -55) scale(0.70)'})
	items = list(body)
	for prefix in ('chromatid-', 'lect13b-inversion_loop_without_crossover-marker-'):
		group.extend(copy.deepcopy(item) for item in items if item.get('id', '').startswith(prefix))
	group.extend(copy.deepcopy(item) for item in items if item.get('class') == 'gene-label')
	ET.SubElement(root, f'{{{NS}}}image', {'x': '400', 'y': '325', 'width': '384', 'height': '142',
		'href': 'data:image/png;base64,' + base64.b64encode(
			(HERE / source['callout_png']).read_bytes()).decode('ascii')})
	return root


#============================================
def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--output-root', type=pathlib.Path, default=HERE)
	args = parser.parse_args()
	sources = json.loads((HERE / 'lect13b_loop_chromosome_sources.json').read_text())
	out = args.output_root / 'assets' / 'lect13b-chromo_alter_3-inversion'
	out.mkdir(parents=True, exist_ok=True)
	loop = None
	for name, source in sources.items():
		if name == 'image_006':
			continue
		root = render_source(name, source)
		if name == 'inversion_loop_without_crossover':
			loop = root
		(out / (name + '.drawn.svg')).write_bytes(ET.tostring(root, encoding='ascii', xml_declaration=True))
	if loop is None:
		raise ValueError('Missing inversion loop source')
	root = image_006(loop, sources['image_006'])
	(out / 'image_006_replacement.svg').write_bytes(
		ET.tostring(root, encoding='ascii', xml_declaration=True))


if __name__ == '__main__':
	main()
