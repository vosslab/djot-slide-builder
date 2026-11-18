#!/usr/bin/env python3
"""Regenerate LECT13D chromosome compositions from frozen source data."""
import argparse
import functools
import json
import pathlib
import re
import subprocess

import lxml.etree
import svg_tools._xml
import svg_tools.annotations
import svg_tools.chromosomes as chrom
import svg_tools.chromosome_surface
import svg_tools.chromosome_topology as topology
import svg_tools.drawing
import svg_tools.palette
import svg_tools.text

HERE = pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip()) / 'genetics/LECT13/djot'
NS = '{http://www.w3.org/2000/svg}'

NAMES = ('normal_y_chromosome_strip', 'normal_chromosome_2_strip',
		'translocated_x_chromosome_strip', 'translocated_2_chromosome_strip',
		'normal_y_translocated_2_subset', 'translocated_x_normal_y_subset',
		'translocated_2_normal_2_subset', 'ruby_translocation_chromosome_set',
		'reciprocal_translocation_gamete_products')
COLORS = {'slate': '#7895a2', 'blue': '#367cb7', 'red': '#df5146'}


#============================================
@functools.cache
def _legacy_shells() -> dict[str, pathlib.Path]:
	"""Load frozen SVG shells on the first legacy recipe call."""
	shells = json.loads((HERE / 'lect13d_chromosome_shells.json').read_text())
	return {name: HERE / path for name, path in shells.items()}


def write_svg(root: lxml.etree._Element, path: pathlib.Path) -> None:
	"""Write a source-derived SVG after removing only its canvas backdrop."""
	svg_tools.drawing.remove_canvas_background(root)
	lxml.etree.ElementTree(svg_tools.drawing.svg_root(root)).write(path, encoding='ascii', xml_declaration=True)

def marker(name: str, x: float, y: float, thickness: float, angle: float) -> lxml.etree._Element:
	"""Place the common structural marker without inventing chromosome material."""
	part = chrom.centromere_part(name, thickness=thickness)
	result = svg_tools._xml.parse(part.fragment)
	result.set('transform', f'translate({x} {y}) rotate({angle})')
	return result


def pairing() -> None:
	"""Retain source arms, paint boundaries, sisters and centromeres with smooth bends."""
	shells = _legacy_shells()
	names = [name for name in shells if name.startswith('pairing-') or name == 'segregation-three-forms.drawn.svg']
	for name in sorted(names):
		root = svg_tools._xml.read(shells[name])
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
			chromatids = []
			for sister in range(count):
				arms = paths[2*sister:2*sister+2]
				curves = [chrom.svgpathtools.parse_path(arm.attrib['d']) for arm in arms]
				curve = chrom.svgpathtools.Path(*curves[0], *curves[1])
				lengths = [arm.length() for arm in curves]
				if name == 'pairing-spindle.drawn.svg':
					# The source gives each chromatid as two perpendicular line segments.
					# Keep endpoints and material proportions around a smooth quarter-turn.
					start, elbow, end = curve.start, curves[0].end, curve.end
					incoming = (elbow-start) / abs(elbow-start)
					outgoing = (end-elbow) / abs(end-elbow)
					radius = 15
					corner_start = elbow - incoming*radius
					corner_end = elbow + outgoing*radius
					control = radius * 0.5522847498
					curve = chrom.svgpathtools.Path(
						chrom.svgpathtools.Line(start, corner_start),
						chrom.svgpathtools.CubicBezier(
							corner_start, corner_start + incoming*control,
							corner_end - outgoing*control, corner_end),
						chrom.svgpathtools.Line(corner_end, end))
					original_length = sum(lengths)
					lengths = [curve.length() * length / original_length for length in lengths]
				# Project the source pair's filled centromere onto each unchanged sister axis.
				tangent = curve.unit_tangent(0)
				center_length = ((complex(cx, cy)-curve.start)/tangent).real
				bounds = sorted({0, lengths[0], center_length, curve.length()})
				segments = tuple(chrom.Segment('', arms[0 if (a+b)/2 < lengths[0] else 1].attrib['stroke'], b-a)
					for a, b in zip(bounds, bounds[1:]))
				model = chrom.Chromosome(segments, (chrom.Centromere(bounds.index(center_length)),))
				chromatids.append((model, curve.d()))
			thickness = float(paths[0].attrib['stroke-width'])
			if count == 2:
				part = chrom.sister_chromatid_parts(f'{name[:-10]}-{number}', tuple(chromatids),
					thickness=thickness, labels=False)
			else:
				part = chrom.chromosome_path_part(f'{name[:-10]}-{number}', *chromatids[0],
					thickness=thickness, labels=False)
			group.insert(insert, svg_tools._xml.parse(part.fragment))
			for node in paths + ellipses:
				group.remove(node)
		write_svg(root, OUT / name)


def color(value: str) -> str:
	return COLORS[value.removeprefix('url(#').removesuffix(')')]


def ruby() -> None:
	OUT.mkdir(parents=True, exist_ok=True)
	shells = _legacy_shells()
	for name in NAMES:
		root = svg_tools._xml.read(shells[f'{name}.drawn.svg'])
		# Neighboring strip canvases overlap; transparent backgrounds preserve their collars.
		svg_tools.drawing.remove_canvas_background(root)
		parents = {child: parent for parent in root.iter() for child in parent}
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
					for a, b, c in zip(boundaries, boundaries[1:], colors)), (chrom.Centromere(1),))
			path = f'M {start} {y+height/2} L {end} {y+height/2}'
			# These small repeated strips need room for readable two-letter loci.
			thickness = 40
			part = chrom.chromosome_path_part(f'{name}-{group.get("id")}', model,
				path, thickness=thickness, labels=False)
			row_id = group.get('id')
			row_name = row_id.removesuffix('-rod')
			group.clear()
			group.set('id', row_id)
			group.append(svg_tools._xml.parse(part.fragment))
			row = parents[group]
			allele = row.find(f"{NS}text[@id='{row_name}-allele']")
			if allele is not None:
				label = ''.join(allele.itertext())
				row.remove(allele)
				surface = svg_tools.chromosome_surface.Surface(
					chrom.svgpathtools.parse_path(path), thickness)
				center = svg_tools.chromosome_surface.nearest_distance(
					surface.path, complex(float(allele.get('x')), y+height/2))
				gene = chrom.Segment(label, '#F3D788', 36)
				group.append(svg_tools._xml.parse(chrom.gene_locus_part(
					f'{name}-{row_name}-gene', surface, center, gene).fragment))
		if name.endswith('_strip') or name.endswith('_subset'):
			width, height = float(root.get('width')), float(root.get('height'))
			root.set('height', str(height+10))
			root.set('viewBox', f'0 -5 {width} {height+10}')
		write_svg(root, OUT / f'{name}.drawn.svg')

	for source_name, count in (('ruby-male', 4), ('gamete-products', 24)):
		convert_line_products(source_name, count)


def convert_line_products(source_name: str, count: int) -> None:
	root = svg_tools._xml.read(_legacy_shells()[f'{source_name}.drawn.svg'])
	for index in range(count):
		paths = [node for node in root if node.tag == NS + 'path'][:2]
		circle = next(node for node in root if node.tag == NS + 'circle')
		first = [float(v) for v in paths[0].get('d').replace('M', '').replace('L', '').split()]
		second = [float(v) for v in paths[1].get('d').replace('M', '').replace('L', '').split()]
		start, y, join = first[0], first[1], first[2]
		end, center = second[2], float(circle.get('cx'))
		bounds = sorted({start, center, join, end})
		model = chrom.Chromosome(tuple(chrom.Segment('', paths[0].get('stroke') if a < join else paths[1].get('stroke'), b-a)
			for a, b in zip(bounds, bounds[1:])), (chrom.Centromere(bounds.index(center)),))
		part = chrom.chromosome_path_part(f'{source_name}-{index}', model,
			f'M {start} {y} L {end} {y}', thickness=float(paths[0].get('stroke-width')), labels=False)
		position = list(root).index(paths[0])
		root.insert(position, svg_tools._xml.parse(part.fragment))
		for node in paths + [circle]:
			root.remove(node)
	write_svg(root, OUT / f'{source_name}.drawn.svg')


def gametes() -> None:
	name = 'robertsonian_gamete_products'
	root = svg_tools._xml.read(_legacy_shells()[f'{name}.drawn.svg'])
	count = 0
	for group in list(root.iter(NS + 'g')):
		if group.get('data-chromosome') is None:
			continue
		arms = group.findall(NS + 'path')
		left = float(re.match(r'M(-?[\d.]+)', arms[0].get('d')).group(1))
		right = float(re.match(r'M(-?[\d.]+)', arms[1].get('d')).group(1))
		model = chrom.Chromosome((chrom.Segment('', arms[0].get('fill'), -left),
									chrom.Segment('', arms[1].get('fill'), right)), (chrom.Centromere(1),))
		part = chrom.chromosome_path_part(f'robertsonian-gamete-{count}', model,
					f'M {left} 0 L {right} 0', thickness=18, labels=False)
		count += 1
		for node in list(group):
			group.remove(node)
		group.append(svg_tools._xml.parse(part.fragment))
	if count != 18:
		raise ValueError(f'Expected 18 chromosomes, found {count}')
	write_svg(root, OUT / f'{name}.drawn.svg')


def metaphase() -> None:
	name = 'robertsonian_metaphase_orientations'
	root = svg_tools._xml.read(_legacy_shells()[f'{name}.drawn.svg'])
	count = 0
	for group in list(root.iter(NS + 'g')):
		sisters = [child for child in group if child.get('data-sister') is not None]
		if not sisters:
			continue
		if len(sisters) != 2:
			raise ValueError(f'Expected sister pairs in {name}')
		chromatids = []
		for sister in sisters:
			match = re.fullmatch(r'translate\((-?[\d.]+) (-?[\d.]+)\)', sister.get('transform', ''))
			if match is None:
				raise ValueError(f'Expected translated sister in {name}')
			shift = complex(float(match.group(1)), float(match.group(2)))
			arms = sister.findall(NS + 'path')
			if len(arms) not in (1, 2):
				raise ValueError(f'Unexpected sister arms in {name}')
			curves = [chrom.svgpathtools.parse_path(arm.get('d')).translated(shift) for arm in arms]
			path = chrom.svgpathtools.Path(*(segment for curve in curves for segment in curve))
			model = chrom.Chromosome(tuple(chrom.Segment('', arm.get('stroke'), curve.length())
				for arm, curve in zip(arms, curves)), (chrom.Centromere(1),))
			chromatids.append((model, path.d()))
		part = chrom.sister_chromatid_parts(f'robertsonian-metaphase-{count}', tuple(chromatids),
			thickness=14, labels=False)
		position = list(group).index(sisters[0])
		for sister in sisters:
			group.remove(sister)
		group.insert(position, svg_tools._xml.parse(part.fragment))
		count += len(sisters)
	if count != 18:
		raise ValueError(f'Expected 18 sister chromatids, found {count}')
	write_svg(root, OUT / f'{name}.drawn.svg')


def fusion(output_dir: pathlib.Path = HERE / 'assets/lect13d-meiosis_translocation') -> None:
	"""Draw both products of a schematic Robertsonian long-arm fusion."""
	ink = '#293e43'
	root = lxml.etree.Element(NS + 'svg', {'width': '1120', 'height': '742',
		'viewBox': '35 51 1120 742', 'font-family': 'Atkinson Hyperlegible Next',
		'fill': ink, 'role': 'img', 'aria-labelledby': 'title desc'})
	lxml.etree.SubElement(root, NS + 'title', {'id': 'title'}).text = 'Robertsonian centromeric fusion'
	lxml.etree.SubElement(root, NS + 'desc', {'id': 'desc'}).text = (
		'The long arms of two acrocentric chromosomes join near their centromeres. '
		'The main product has one active centromere in this model. '
		'The short arms form a separate product that is usually lost.')
	blue_cut, red_cut = 10/110, 5.6/51.6
	blue = topology.chromosome('A', length=110, centromere=blue_cut)
	red = topology.chromosome('B', length=51.6, centromere=red_cut)
	blue_short, blue_long = topology.split(blue, blue_cut)
	red_short, red_long = topology.split(red, red_cut)
	red_long = topology.with_centromere_activity(red_long, 'B.cen', active=False)
	long_product = topology.join(topology.reverse(blue_long), red_long)
	short_product = topology.join(blue_short, topology.reverse(red_short))
	palette = {('A', 'body'): svg_tools.palette.shade('sky_blue', 'dark'),
		('B', 'body'): svg_tools.palette.shade('red', 'dark')}
	specs = {
		'blue-input': (blue, [(132, 82), (143, 252), (138, 434), (149, 654)]),
		'red-input': (red, [(278, 82), (271, 194), (287, 344)]),
		'fused-product': (long_product, [(831, 624), (853, 404), (838, 233),
			(890, 129), (983, 103), (1071, 150), (1132, 227)]),
		'short-arm-product': (short_product, [(1000, 436), (1076, 436)]),
	}
	# ASVS 1.5.1: use the restricted parser on fragments from drawing helpers.
	for name, (model, points) in specs.items():
		part = chrom.render(f'fusion-{name}', model, points=points,
			width=30, scale=5.2, palette=palette)
		root.append(svg_tools._xml.parse(part.fragment))

	arrow = svg_tools.annotations.connector([(405, 323), (741, 323)], color=ink,
		stroke_width=4, head_size=25)
	root.append(svg_tools._xml.parse(arrow.fragment))
	labels = (
		(575, 230, 46, 'Centromeric'),
		(575, 282, 46, 'fusion'),
		(205, 708, 45, 'Normal'),
		(205, 761, 45, 'chromosomes'),
		(925, 708, 45, 'Robertsonian'),
		(925, 761, 45, 'translocation'),
		(1038, 493, 34, 'Short-arm'),
		(1038, 532, 34, 'product'),
	)
	for x, y, size, value in labels:
		label = svg_tools.text.label(x, y, value, size=size, color=ink)
		root.append(svg_tools._xml.parse(label.fragment))
	write_svg(root, output_dir / 'robertsonian_centromeric_fusion.drawn.svg')


def human_fusion() -> None:
	name = 'human_chromosome_2_fusion'
	root = svg_tools._xml.read(_legacy_shells()[f'{name}.drawn.svg'])
	for group in list(root.iter(NS + 'g')):
		if group.get('id') not in ('ancestor-a', 'ancestor-b', 'dicentric', 'inactivation', 'human-2'):
			continue
		body = group.find(NS + 'rect')
		x, y, width, height = (float(body.get(key)) for key in ('x', 'y', 'width', 'height'))
		circles = group.findall(NS + 'circle')
		start, end = y + width/2, y + height-width/2
		model = chrom.Chromosome((chrom.Segment('', body.get('fill'), end-start),))
		part = chrom.chromosome_path_part(f'human2-{group.get("id")}-body', model,
					f'M {x+width/2} {start} L {x+width/2} {end}', thickness=width, labels=False)
		group.remove(body)
		group.insert(0, svg_tools._xml.parse(part.fragment))
		for index, circle in enumerate(circles):
			cx, cy = float(circle.get('cx')), float(circle.get('cy'))
			group.append(marker(f'human2-{group.attrib["id"]}-center-{index}', cx, cy, width, 90))
	write_svg(root, OUT / f'{name}.drawn.svg')


def generate(source_path: pathlib.Path, output_root: pathlib.Path) -> None:
	"""Keep authored text/composition and replace source-data chromosome placeholders."""
	sources = json.loads(source_path.read_text())
	for relative, source in sources.items():
		root = svg_tools._xml.read(source_path.parent / source['artwork'])
		for parent in list(root.iter()):
			for child in list(parent):
				if 'data-shared-part' not in child.attrib:
					continue
				index = int(child.attrib['data-shared-part'])
				data = source['parts'][index]
				centromeres = () if data['centromere_after'] is None else (
					chrom.Centromere(data['centromere_after']),)
				model = chrom.Chromosome(tuple(
					chrom.Segment(*segment) for segment in data['segments']),
					centromeres=centromeres)
				part = chrom.chromosome_path_part(f'migrated13bc-chromosome-{index}',
					model, data['path'], thickness=data['thickness'],
					cut_ends=data['cut_ends'], labels=False)
				replacement = svg_tools._xml.parse(part.fragment)
				replacement.attrib['data-source-part'] = str(index)
				replacement.attrib['stroke'] = 'none'
				position = list(parent).index(child)
				parent.remove(child)
				parent.insert(position, replacement)
		path = output_root / relative
		path.parent.mkdir(parents=True, exist_ok=True)
		svg_tools.drawing.remove_canvas_background(root)
		path.write_bytes(lxml.etree.tostring(svg_tools.drawing.svg_root(root), encoding='ascii', xml_declaration=True))


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
	fusion(OUT)
	human_fusion()
	generate(HERE / 'lect13d_chromosome_duplicates.json', args.output_root)


if __name__ == '__main__':
	main()
