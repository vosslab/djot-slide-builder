#!/usr/bin/env python3
"""Regenerate LECT13D chromosome compositions from frozen source data."""
import argparse
import json
import pathlib
import re
import subprocess
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as DET

import svg_tools.chromosomes as chrom
import svg_tools.chromosome_surface

HERE = pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip()) / 'genetics/LECT13/djot'
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
	result = DET.fromstring(part.fragment)
	result.set('transform', f'translate({x} {y}) rotate({angle})')
	return result


def pairing() -> None:
	"""Retain source arms, paint boundaries, sisters and centromeres with smooth bends."""
	names = [name for name in SOURCES if name.startswith('pairing-') or name == 'segregation-three-forms.drawn.svg']
	for name in sorted(names):
		root = DET.fromstring(SOURCES[name])
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
			group.insert(insert, DET.fromstring(part.fragment))
			for node in paths + ellipses:
				group.remove(node)
		ET.ElementTree(root).write(OUT / name, encoding='ascii', xml_declaration=True)


def color(value: str) -> str:
	return COLORS[value.removeprefix('url(#').removesuffix(')')]


def ruby() -> None:
	OUT.mkdir(parents=True, exist_ok=True)
	for name in NAMES:
		root = DET.fromstring(SOURCES[f'{name}.drawn.svg'])
		# Neighboring strip canvases overlap; transparent backgrounds preserve their collars.
		background = root.find(NS + "rect[@fill='white']")
		if background is not None:
			root.remove(background)
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
			group.append(DET.fromstring(part.fragment))
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
				group.append(DET.fromstring(chrom.gene_locus_part(
					f'{name}-{row_name}-gene', surface, center, gene).fragment))
		ET.ElementTree(root).write(OUT / f'{name}.drawn.svg', encoding='ascii', xml_declaration=True)

	for source_name, count in (('ruby-male', 4), ('gamete-products', 24)):
		convert_line_products(source_name, count)


def convert_line_products(source_name: str, count: int) -> None:
	root = DET.fromstring(SOURCES[f'{source_name}.drawn.svg'])
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
		root.insert(position, DET.fromstring(part.fragment))
		for node in paths + [circle]:
			root.remove(node)
	ET.ElementTree(root).write(OUT / f'{source_name}.drawn.svg', encoding='ascii', xml_declaration=True)


def gametes() -> None:
	name = 'robertsonian_gamete_products'
	root = DET.fromstring(SOURCES[f'{name}.drawn.svg'])
	count = 0
	for group in root.iter(NS + 'g'):
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
		group.append(DET.fromstring(part.fragment))
	if count != 18:
		raise ValueError(f'Expected 18 chromosomes, found {count}')
	ET.ElementTree(root).write(OUT / f'{name}.drawn.svg', encoding='ascii', xml_declaration=True)


def metaphase() -> None:
	name = 'robertsonian_metaphase_orientations'
	root = DET.fromstring(SOURCES[f'{name}.drawn.svg'])
	count = 0
	for group in root.iter(NS + 'g'):
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
		group.insert(position, DET.fromstring(part.fragment))
		count += len(sisters)
	if count != 18:
		raise ValueError(f'Expected 18 sister chromatids, found {count}')
	ET.ElementTree(root).write(OUT / f'{name}.drawn.svg', encoding='ascii', xml_declaration=True)


def fusion() -> None:
	"""Use medial arm curves from source contours and retain terminal centromeres."""
	# shortcut: filled source arms need medial estimates; replace only with measured source centerlines.
	name = 'robertsonian_centromeric_fusion'
	root = DET.fromstring(SOURCES[f'{name}.drawn.svg'])
	specs = {
		'blue-input': (152, 99, (('M 152 99 C 144 212 164 274 153 361 C 143.5 450.5 146 518 152 595', '#377eaf'),)),
		'red-input': (280, 99, (('M 280 99 C 276 206 294 262 283 326', '#d6533c'),)),
		'fused-product': (877, 113, (
			('M 877 113 C 869 226 889 288 878 375 C 868.5 464.5 871 532 877 609', '#377eaf'),
			('M 877 113 C 943.5 137.5 1001.5 180.5 1068 222.5', '#d6533c'))),
	}
	for group in root.iter(NS + 'g'):
		if group.get('id') not in specs:
			continue
		cx, cy, arms = specs[group.attrib['id']]
		for node in list(group):
			group.remove(node)
		for index, (path, paint) in enumerate(arms):
			curve = chrom.svgpathtools.parse_path(path)
			model = chrom.Chromosome((chrom.Segment('', paint, curve.length()),))
			part = chrom.chromosome_path_part(f'fusion-{group.attrib["id"]}-arm-{index}',
				model, path, thickness=50, labels=False)
			group.append(DET.fromstring(part.fragment))
		group.append(marker(f'fusion-{group.attrib["id"]}', cx, cy, 50, 90))
	ET.ElementTree(root).write(OUT / f'{name}.drawn.svg', encoding='ascii', xml_declaration=True)


def human_fusion() -> None:
	name = 'human_chromosome_2_fusion'
	root = DET.fromstring(SOURCES[f'{name}.drawn.svg'])
	for group in root.iter(NS + 'g'):
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
		group.insert(0, DET.fromstring(part.fragment))
		for index, circle in enumerate(circles):
			cx, cy = float(circle.get('cx')), float(circle.get('cy'))
			group.append(marker(f'human2-{group.attrib["id"]}-center-{index}', cx, cy, width, 90))
	ET.ElementTree(root).write(OUT / f'{name}.drawn.svg', encoding='ascii', xml_declaration=True)


def generate(source_path: pathlib.Path, output_root: pathlib.Path) -> None:
	"""Keep authored text/composition and replace source-data chromosome placeholders."""
	sources = json.loads(source_path.read_text())
	for relative, source in sources.items():
		root = DET.fromstring(source['svg'])
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
				replacement = DET.fromstring(part.fragment)
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
