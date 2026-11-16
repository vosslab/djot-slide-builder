#!/usr/bin/env python3
"""Regenerate LECT13D chromosome compositions from frozen source data."""
import argparse
import json
import math
import pathlib
import re
import xml.etree.ElementTree as ET

import svg_tools.chromosomes as chrom

HERE = pathlib.Path(__file__).resolve().parent
SOURCES = json.loads((HERE / 'lect13d_chromosome_shells.json').read_text())
NS = '{http://www.w3.org/2000/svg}'
ET.register_namespace('', 'http://www.w3.org/2000/svg')
NAMES = ('normal_y_chromosome_strip', 'normal_chromosome_2_strip',
		 'translocated_x_chromosome_strip', 'translocated_2_chromosome_strip',
		 'normal_y_translocated_2_subset', 'translocated_x_normal_y_subset',
		 'translocated_2_normal_2_subset', 'ruby_translocation_chromosome_set',
		 'reciprocal_translocation_gamete_products')
COLORS = {'slate': '#7895a2', 'blue': '#367cb7', 'red': '#df5146'}

def marker(name: str, x: float, y: float, thickness: float, angle: float) -> ET.Element:
	"""Place the common structural marker without inventing chromosome material."""
	part = chrom.centromere_part(name, thickness=thickness)
	result = ET.fromstring(part.fragment)
	result.set('transform', f'translate({x} {y}) rotate({angle})')
	return result


def pairing() -> None:
	"""Retain every source path, paint boundary, sister and source-level centromere."""
	names = [name for name in SOURCES if name.startswith('pairing-') or name == 'segregation-three-forms.drawn.svg']
	for name in sorted(names):
		root = ET.fromstring(SOURCES[name])
		for number, group in enumerate(list(root.iter(NS + 'g'))):
			ellipses = group.findall(NS + 'ellipse')
			paths = group.findall(NS + 'path')
			if not ellipses:
				continue
			if len(ellipses) != 1 or len(paths) not in (2, 4):
				raise ValueError(f'Unexpected chromosome structure in {name}')
			ellipse = ellipses[0]
			cx, cy = float(ellipse.attrib['cx']), float(ellipse.attrib['cy'])
			count = len(paths) // 2
			insert = list(group).index(paths[0])
			necks = []
			for sister in range(count):
				arms = paths[2*sister:2*sister+2]
				curves = [chrom.svgpathtools.parse_path(arm.attrib['d']) for arm in arms]
				curve = chrom.svgpathtools.Path(*curves[0], *curves[1])
				lengths = [arm.length() for arm in curves]
				# Project the source pair's filled centromere onto each unchanged sister axis.
				tangent = curve.unit_tangent(0)
				center_length = ((complex(cx, cy)-curve.start)/tangent).real
				neck = curve.point(curve.ilength(center_length))
				necks.append(neck)
				bounds = sorted({0, lengths[0], center_length, curve.length()})
				segments = tuple(chrom.Segment('', arms[0 if (a+b)/2 < lengths[0] else 1].attrib['stroke'], b-a)
					for a, b in zip(bounds, bounds[1:]))
				model = chrom.Chromosome(segments, bounds.index(center_length))
				part = chrom.chromosome_path_part(f'{name[:-10]}-{number}-sister-{sister}',
					model, curve.d(), thickness=float(arms[0].attrib['stroke-width']), labels=False)
				body = ET.fromstring(part.fragment)
				if count == 2:
					body.remove(body.find('ellipse'))
					# Limit the shared neck envelope to its neck; keep distant source bends exact.
					if len({segment.unit_tangent(0) for segment in curve}) > 1:
						body = local_neck(body, curve, arms, neck)
				group.insert(insert+sister, body)
			# The source marker spans both sisters; its position and orientation carry pairing.
			first = chrom.svgpathtools.parse_path(paths[0].attrib['d'])
			tangent = first.unit_tangent(0)
			angle = math.degrees(math.atan2(tangent.imag, tangent.real))
			across = float(ellipse.attrib['ry'] if abs(tangent.real) > .5 else ellipse.attrib['rx'])
			if count == 2:
				# The source filled ellipse joins the sisters; retain that material at neck width.
				thickness = float(paths[0].attrib['stroke-width']) * .40
				bridge = chrom.chromosome_path_part(f'{name[:-10]}-{number}-attachment',
					chrom.Chromosome((chrom.Segment('', ellipse.attrib['fill'], abs(necks[1]-necks[0])),)),
					f'M {necks[0].real} {necks[0].imag} L {necks[1].real} {necks[1].imag}',
					thickness=thickness, labels=False)
				group.insert(insert, ET.fromstring(bridge.fragment))
				group.insert(insert+count+1, marker(f'{name[:-10]}-{number}', cx, cy, across*2*.61, angle))
			for node in paths + ellipses:
				group.remove(node)
		ET.ElementTree(root).write(OUT / name, encoding='ascii', xml_declaration=True)


def local_neck(body: ET.Element, curve: chrom.svgpathtools.Path,
	arms: list[ET.Element], neck: complex) -> ET.Element:
	"""Compose shared bodies with rectangular clips, preserving every distant bend."""
	name = body.attrib['id']
	width = float(arms[0].attrib['stroke-width'])
	span = width * .45
	extent = curve.length() + width
	tangent = curve.unit_tangent(0)
	angle = math.degrees(math.atan2(tangent.imag, tangent.real))
	transform = f'translate({neck.real} {neck.imag}) rotate({angle})'
	result = ET.Element('g', {'id': name})
	defs = ET.SubElement(result, 'defs')
	inside = ET.SubElement(defs, 'clipPath', {'id': f'{name}-neck-window'})
	ET.SubElement(inside, 'rect', {'x': str(-span), 'y': str(-width),
		'width': str(span*2), 'height': str(width*2), 'transform': transform})
	outside = ET.SubElement(defs, 'clipPath', {'id': f'{name}-outside-neck'})
	for start in (-extent, span):
		ET.SubElement(outside, 'rect', {'x': str(start), 'y': str(-extent),
			'width': str(extent-span), 'height': str(extent*2), 'transform': transform})
	model = chrom.Chromosome(tuple(chrom.Segment('', arm.attrib['stroke'],
		chrom.svgpathtools.parse_path(arm.attrib['d']).length()) for arm in arms))
	original = chrom.chromosome_path_part(f'{name}-unconstricted', model,
		curve.d(), thickness=width, labels=False)
	old_body = ET.fromstring(original.fragment)
	old_body.set('clip-path', f'url(#{name}-outside-neck)')
	result.append(old_body)
	body.set('id', f'{name}-neck')
	body.set('clip-path', f'url(#{name}-neck-window)')
	result.append(body)
	return result


def color(value: str) -> str:
	return COLORS[value.removeprefix('url(#').removesuffix(')')]


def ruby() -> None:
	OUT.mkdir(parents=True, exist_ok=True)
	for name in NAMES:
		root = ET.fromstring(SOURCES[f'{name}.drawn.svg'])
		for group in list(root.iter()):
			gid = group.get('id', '')
			if not (gid.endswith('-rod') or (name.startswith('reciprocal_') and gid.startswith('chromosome-') and group.tag == NS + 'g')):
				continue
			body = group.find(NS + 'rect')
			center = group.find(NS + 'circle')
			x, y, width, height = (float(body.get(key)) for key in ('x', 'y', 'width', 'height'))
			start, end = x + height/2, x + width - height/2
			centromere = float(center.get('cx'))
			initial = color(body.get('fill'))
			distal = group.find(NS + 'g/' + NS + 'rect')
			if distal is None:
				distal = next((node for node in group if node.get('id', '').endswith('-distal')), None)
			boundaries = [start, centromere]
			if distal is not None:
				boundaries.append(float(distal.get('x')))
			boundaries.append(end)
			colors = [initial] * (len(boundaries)-1)
			if distal is not None:
				colors[-1] = color(distal.get('fill'))
			model = chrom.Chromosome(tuple(chrom.Segment('', c, b-a)
				for a, b, c in zip(boundaries, boundaries[1:], colors)), 1)
			part = chrom.chromosome_path_part(f'{name}-{group.get("id")}', model,
				f'M {start} {y+height/2} L {end} {y+height/2}', thickness=height, labels=False)
			row_id = group.get('id')
			group.clear()
			group.set('id', row_id)
			group.append(ET.fromstring(part.fragment))
		ET.ElementTree(root).write(OUT / f'{name}.drawn.svg', encoding='ascii', xml_declaration=True)

	for source_name, count in (('ruby-male', 4), ('gamete-products', 24)):
		convert_line_products(source_name, count)


def convert_line_products(source_name: str, count: int) -> None:
	root = ET.fromstring(SOURCES[f'{source_name}.drawn.svg'])
	for index in range(count):
		paths = [node for node in root if node.tag == NS + 'path'][:2]
		circle = next(node for node in root if node.tag == NS + 'circle')
		first = [float(v) for v in paths[0].get('d').replace('M', '').replace('L', '').split()]
		second = [float(v) for v in paths[1].get('d').replace('M', '').replace('L', '').split()]
		start, y, join = first[0], first[1], first[2]
		end, center = second[2], float(circle.get('cx'))
		bounds = sorted({start, center, join, end})
		model = chrom.Chromosome(tuple(chrom.Segment('', paths[0].get('stroke') if a < join else paths[1].get('stroke'), b-a)
			for a, b in zip(bounds, bounds[1:])), bounds.index(center))
		part = chrom.chromosome_path_part(f'{source_name}-{index}', model,
			f'M {start} {y} L {end} {y}', thickness=float(paths[0].get('stroke-width')), labels=False)
		position = list(root).index(paths[0])
		root.insert(position, ET.fromstring(part.fragment))
		for node in paths + [circle]:
			root.remove(node)
	ET.ElementTree(root).write(OUT / f'{source_name}.drawn.svg', encoding='ascii', xml_declaration=True)


def gametes() -> None:
	name = 'robertsonian_gamete_products'
	root = ET.fromstring(SOURCES[f'{name}.drawn.svg'])
	count = 0
	for group in root.iter(NS + 'g'):
		if group.get('data-chromosome') is None:
			continue
		arms = group.findall(NS + 'path')
		left = float(re.match(r'M(-?[\d.]+)', arms[0].get('d')).group(1))
		right = float(re.match(r'M(-?[\d.]+)', arms[1].get('d')).group(1))
		model = chrom.Chromosome((chrom.Segment('', arms[0].get('fill'), -left),
								  chrom.Segment('', arms[1].get('fill'), right)), 1)
		part = chrom.chromosome_path_part(f'robertsonian-gamete-{count}', model,
					f'M {left} 0 L {right} 0', thickness=18, labels=False)
		count += 1
		for node in list(group):
			group.remove(node)
		group.append(ET.fromstring(part.fragment))
	if count != 18:
		raise ValueError(f'Expected 18 chromosomes, found {count}')
	ET.ElementTree(root).write(OUT / f'{name}.drawn.svg', encoding='ascii', xml_declaration=True)


def metaphase() -> None:
	name = 'robertsonian_metaphase_orientations'
	root = ET.fromstring(SOURCES[f'{name}.drawn.svg'])
	count = 0
	for group in root.iter(NS + 'g'):
		if group.get('data-sister') is None:
			continue
		arms = group.findall(NS + 'path')
		if len(arms) == 2:
			a, b = [chrom.svgpathtools.parse_path(node.get('d')) for node in arms]
			path = chrom.svgpathtools.Path(*a, *b)
			lengths = [a.length(), b.length()]
			colors = [node.get('stroke') for node in arms]
		else:
			path = chrom.svgpathtools.parse_path(arms[0].get('d'))
			lengths = [path[0].length(), sum(segment.length() for segment in path[1:])]
			colors = [arms[0].get('stroke')] * 2
		model = chrom.Chromosome(tuple(chrom.Segment('', c, n) for c, n in zip(colors, lengths)), 1)
		part = chrom.chromosome_path_part(f'robertsonian-metaphase-{count}', model,
					path.d(), thickness=14, labels=False)
		count += 1
		for node in list(group):
			group.remove(node)
		group.append(ET.fromstring(part.fragment))
	if count != 18:
		raise ValueError(f'Expected 18 chromosomes, found {count}')
	ET.ElementTree(root).write(OUT / f'{name}.drawn.svg', encoding='ascii', xml_declaration=True)


def fusion() -> None:
	"""Use medial arm curves from source contours and retain terminal centromeres."""
	# shortcut: filled source arms need medial estimates; replace only with measured source centerlines.
	name = 'robertsonian_centromeric_fusion'
	root = ET.fromstring(SOURCES[f'{name}.drawn.svg'])
	specs = {
		'blue-input': (152, (('M 151 147 C 144 212 164 274 153 361 C 143.5 450.5 146 518 152 595', '#377eaf'),)),
		'red-input': (280, (('M 279 147 C 276 206 294 262 283 326', '#d6533c'),)),
		'fused-product': (863, (
			('M 862 147 C 855 212 875 274 864 361 C 854.5 450.5 857 518 863 595', '#377eaf'),
			('M 877 113 C 943.5 137.5 1001.5 180.5 1068 222.5', '#d6533c'))),
	}
	for group in root.iter(NS + 'g'):
		if group.get('id') not in specs:
			continue
		cx, arms = specs[group.attrib['id']]
		source_center = group.find(NS + 'circle')
		for node in list(group):
			group.remove(node)
		if group.attrib['id'] != 'fused-product':
			# The source terminal circle supplies the collar, entirely below its center.
			cy, radius = float(source_center.attrib['cy']), float(source_center.attrib['r'])
			neck_width = 50 * .40
			collar = chrom.chromosome_path_part(f'fusion-{group.attrib["id"]}-attachment',
				chrom.Chromosome((chrom.Segment('', source_center.attrib['fill'], radius-neck_width/2),)),
				f'M {cx} {cy+neck_width/2} L {cx} {cy+radius}', thickness=neck_width, labels=False)
			group.append(ET.fromstring(collar.fragment))
		for index, (path, paint) in enumerate(arms):
			curve = chrom.svgpathtools.parse_path(path)
			model = chrom.Chromosome((chrom.Segment('', paint, curve.length()),), None)
			part = chrom.chromosome_path_part(f'fusion-{group.attrib["id"]}-arm-{index}',
				model, path, thickness=50, labels=False)
			group.append(ET.fromstring(part.fragment))
		group.append(marker(f'fusion-{group.attrib["id"]}', cx, 99, 50, 90))
	ET.ElementTree(root).write(OUT / f'{name}.drawn.svg', encoding='ascii', xml_declaration=True)


def human_fusion() -> None:
	name = 'human_chromosome_2_fusion'
	root = ET.fromstring(SOURCES[f'{name}.drawn.svg'])
	for group in root.iter(NS + 'g'):
		if group.get('id') not in ('ancestor-a', 'ancestor-b', 'dicentric', 'inactivation', 'human-2'):
			continue
		body = group.find(NS + 'rect')
		x, y, width, height = (float(body.get(key)) for key in ('x', 'y', 'width', 'height'))
		circles = group.findall(NS + 'circle')
		start, end = y + width/2, y + height-width/2
		model = chrom.Chromosome((chrom.Segment('', body.get('fill'), end-start),), None)
		part = chrom.chromosome_path_part(f'human2-{group.get("id")}-body', model,
					f'M {x+width/2} {start} L {x+width/2} {end}', thickness=width, labels=False)
		group.remove(body)
		group.insert(0, ET.fromstring(part.fragment))
		for index, circle in enumerate(circles):
			cx, cy = float(circle.get('cx')), float(circle.get('cy'))
			group.append(marker(f'human2-{group.attrib["id"]}-center-{index}', cx, cy, width, 90))
	ET.ElementTree(root).write(OUT / f'{name}.drawn.svg', encoding='ascii', xml_declaration=True)


def generate(source_path: pathlib.Path, output_root: pathlib.Path) -> None:
	"""Keep authored text/composition and replace source-data chromosome placeholders."""
	sources = json.loads(source_path.read_text())
	for relative, source in sources.items():
		root = ET.fromstring(source['svg'])
		for parent in list(root.iter()):
			for child in list(parent):
				if 'data-shared-part' not in child.attrib:
					continue
				index = int(child.attrib['data-shared-part'])
				data = source['parts'][index]
				model = chrom.Chromosome(tuple(
					chrom.Segment(*segment) for segment in data['segments']),
					data['centromere_after'])
				part = chrom.chromosome_path_part(f'migrated13bc-chromosome-{index}',
					model, data['path'], thickness=data['thickness'],
					cut_ends=data['cut_ends'], labels=False)
				replacement = ET.fromstring(part.fragment)
				replacement.attrib['data-source-part'] = str(index)
				replacement.attrib['stroke'] = 'none'
				position = list(parent).index(child)
				parent.remove(child)
				parent.insert(position, replacement)
		path = output_root / relative
		path.parent.mkdir(parents=True, exist_ok=True)
		for node in root.iter():
			if node.tag.startswith('{http://www.w3.org/2000/svg}'):
				node.tag = node.tag.split('}', 1)[1]
		root.attrib['xmlns'] = 'http://www.w3.org/2000/svg'
		path.write_bytes(ET.tostring(root, encoding='ascii', xml_declaration=True))


def main() -> None:
	global OUT
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--output-root', type=pathlib.Path, default=HERE)
	args = parser.parse_args()
	OUT = args.output_root / 'assets/lect13d-meiosis_translocation'
	OUT.mkdir(parents=True, exist_ok=True)
	pairing()
	ruby()
	gametes()
	metaphase()
	fusion()
	human_fusion()
	generate(HERE / 'lect13d_chromosome_duplicates.json', args.output_root)


if __name__ == '__main__':
	main()
