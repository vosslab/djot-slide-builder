#!/usr/bin/env python3
"""Reconstruct the two raster scenes without changing their native surroundings."""
import pathlib
import xml.etree.ElementTree as ET

import svgpathtools
import svg_tools.chromosomes as chromosomes

BASE = pathlib.Path(__file__).resolve().parent
SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
FILENAMES = ('unlinked_segregation.svg', 'unlinked_tt.svg')
DESTINATIONS = {
	'unlinked_segregation.svg': BASE/'assets/lect09_tetrad_concepts/unlinked_segregation.svg',
	'unlinked_tt.svg': BASE/'assets/lect09e-tetrad_visuals/unlinked_tt.svg',
}


def tag(name: str) -> str:
	return f'{{{SVG}}}{name}'


def add(parent: ET.Element, name: str, **attrs: object) -> ET.Element:
	return ET.SubElement(parent, tag(name), {k.replace('_', '-'): str(v) for k, v in attrs.items()})


def part_node(fragment: str) -> ET.Element:
	node = ET.fromstring(fragment)
	for item in node.iter():
		if not item.tag.startswith('{'):
			item.tag = tag(item.tag)
	return node


def chromatid(parent: ET.Element, name: str, pieces: tuple[str, ...],
	colors: tuple[str, ...], width: float) -> None:
	"""The first source path piece ends at the real neck, never at a guessed midpoint."""
	paths = tuple(svgpathtools.parse_path(piece) for piece in pieces)
	full = svgpathtools.Path(*(segment for path in paths for segment in path))
	# Rounded arc weights avoid svgpathtools boundary inversion roundoff (<0.00001 units).
	model = chromosomes.Chromosome(tuple(chromosomes.Segment(f'{name}-{i}', color,
		round(path.length(), 5)) for i, (path, color) in enumerate(zip(paths, colors))),
		centromeres=(chromosomes.Centromere(1),))
	part = chromosomes.chromosome_path_part(name, model, full.d(), thickness=width,
		labels=False)
	node = part_node(part.fragment)
	# A joined sister pair shares one source-centered marker above both sisters.
	for item in list(node):
		if item.get('id', '').startswith(f'{name}-centromere-'):
			node.remove(item)
	node.set('data-chromatid', name)
	node.set('data-centerline', full.d())
	node.set('data-neck', f'{paths[0].end.real:g},{paths[0].end.imag:g}')
	node.set('data-colors', ','.join(colors))
	parent.append(node)


def centromere(parent: ET.Element, name: str, x: float, y: float,
	width: float, angle: float = 0) -> None:
	node = part_node(chromosomes.centromere_part(name, thickness=width).fragment)
	node.set('transform', f'translate({x:g} {y:g}) rotate({angle:g})')
	node.set('data-source-centromere', f'{x:g},{y:g}')
	parent.append(node)


def arrow(parent: ET.Element, x1: float, y1: float, x2: float, y2: float,
	width: float = 1.6) -> None:
	add(parent, 'path', d=f'M{x1} {y1} L{x2} {y2}', fill='none', stroke='#222222',
		stroke_width=width, marker_end='url(#scene-arrow)')


def scene_group() -> ET.Element:
	group = ET.Element(tag('g'), {'id': 'native-scene'})
	defs = add(group, 'defs')
	marker = add(defs, 'marker', id='scene-arrow', markerWidth=9, markerHeight=8,
		refX=8, refY=4, orient='auto', markerUnits='strokeWidth')
	add(marker, 'path', d='M0 0 L8 4 L0 8 L2 4Z', fill='#222222')
	return group


def cell(parent: ET.Element, x: float, y: float, radius: float,
	spindle: bool = False) -> None:
	add(parent, 'circle', cx=x, cy=y, r=radius, fill='#F8CA8E',
		stroke='#B88D62', stroke_width=1.6)
	if spindle:
		for sign in (-1, 1):
			add(parent, 'path', d=f'M{x-radius*.77} {y+sign*8} '
				f'Q{x} {y+sign*radius*.76} {x+radius*.77} {y+sign*8}',
				fill='none', stroke='#9A784E', stroke_width=.9)


def sisters(parent: ET.Element, name: str, x: float, y: float, length: float,
	color: str, crossing: bool) -> None:
	width = 6
	spread = 4.1
	for i, side in enumerate((-1, 1)):
		start, end = x+side*spread, x+side*spread*(-1 if crossing else 1)
		pieces = (f'M{start} {y-length/2} C{start} {y-7} {x} {y-5} {x} {y}',
			f'M{x} {y} C{x} {y+5} {end} {y+7} {end} {y+length/2}')
		chromatid(parent, f'{name}-sister-{i}', pieces, (color, color), width)
	centromere(parent, name, x, y, width, 90)


def segregation() -> ET.Element:
	group = scene_group()
	scene = add(group, 'g', transform='translate(90 50)')
	blue, red = '#078DC1', '#E5464B'
	for possibility, topx in enumerate((163, 689)):
		cell(scene, topx, 108, 71, True)
		for pair, (cy, length) in enumerate(((87, 51), (142, 35))):
			for homolog, dx in enumerate((-8, 9)):
				color = (blue, red)[homolog if possibility == 0 or pair == 0 else 1-homolog]
				sisters(scene, f'p{possibility}-mi-pair{pair}-homolog{homolog}',
					topx+dx, cy, length, color, False)
		for branch, x in enumerate((83, 252) if possibility == 0 else (601, 772)):
			arrow(scene, topx+(-26 if branch == 0 else 26), 174, x, 233)
			cell(scene, x, 295, 59, True)
			for pair, (cy, length) in enumerate(((272, 51), (325, 32))):
				color = (blue, red)[branch if possibility == 0 or pair == 0 else 1-branch]
				sisters(scene, f'p{possibility}-mii-{branch}-pair{pair}',
					x, cy, length, color, True)
			for child, dx in enumerate((-40, 41)):
				xx = x+dx
				arrow(scene, x+(-20 if child == 0 else 24), 351, xx+8*(-1 if child == 0 else 1), 395)
				cell(scene, xx, 432, 34)
				for pair, (cy, length) in enumerate(((427, 50), (439, 35))):
					color = (blue, red)[branch if possibility == 0 or pair == 0 else 1-branch]
					name = f'p{possibility}-daughter-{branch}-{child}-pair{pair}'
					chromatid(scene, name, (f'M{xx-length/2} {cy} L{xx} {cy}',
						f'M{xx} {cy} L{xx+length/2} {cy}'), (color, color), 6)
					centromere(scene, name, xx, cy, 6)
	return group


def history(parent: ET.Element, name: str, x: float, upper_y: float,
	lower_y: float, colors: tuple[str, str], alleles: tuple[str, str],
	crossing: bool) -> None:
	"""Four continuous sisters retain four separate left arms and two joined necks."""
	scale = .80 if name.endswith('-B') else 1.0
	for index in (0, 3, 1, 2):
		upper = index < 2
		cy = upper_y if upper else lower_y
		side = -1 if index % 2 == 0 else 1
		starty = cy+side*43
		prefix = f'M{x-118} {starty} C{x-69} {starty} {x-22} {cy+side*28} {x} {cy}'
		color = colors[0 if upper else 1]
		other = colors[1 if upper else 0]
		if crossing and index in (1, 2):
			midy = (upper_y+lower_y)/2
			endy = lower_y-20 if upper else upper_y+35
			middle = f'M{x} {cy} C{x+44*scale} {cy+side*40} {x+109*scale} {midy-side*13} {x+170*scale} {midy}'
			end = f'M{x+170*scale} {midy} C{x+230*scale} {midy+side*30} {x+295*scale} {endy} {x+372*scale} {endy}'
			pieces, fills = (prefix, middle, end), (color, color, other)
			allele = alleles[1 if upper else 0]
		else:
			endy = cy+side*64
			end = f'M{x} {cy} C{x+64*scale} {cy+side*54} {x+78*scale} {endy-8} {x+137*scale} {endy} '
			end += f'C{x+260*scale} {endy+10} {x+288*scale} {endy-6} {x+372*scale} {endy}'
			pieces, fills = (prefix, end), (color, color)
			allele = alleles[0 if upper else 1]
		chromatid(parent, f'{name}-sister-{index}', pieces, fills, 38)
		label = add(parent, 'text', x=x+372*scale-35, y=endy+13, fill='white',
			font_family='Atkinson Hyperlegible Next', font_size=39,
			font_style='italic', font_weight='bold', text_anchor='middle')
		label.text = allele
	for cy in (upper_y, lower_y):
		centromere(parent, f'{name}-neck-{cy:g}', x, cy, 38)


def tetratype() -> ET.Element:
	group = scene_group()
	scene = add(group, 'g', transform='translate(0 -82)')
	history(scene, 'top-A', 175, 212, 344, ('#784927', '#B67112'), ('A', 'a'), True)
	history(scene, 'top-B', 779, 193, 391, ('#9B714A', '#C99435'), ('B', 'b'), False)
	history(scene, 'bottom-A', 170, 606, 825, ('#784927', '#B67112'), ('A', 'a'), False)
	history(scene, 'bottom-B', 781, 665, 796, ('#C99435', '#9B714A'), ('b', 'B'), True)
	arrow(scene, 1120, 288, 1250, 288, 3.6)
	arrow(scene, 1120, 736, 1250, 736, 3.6)
	return group


def generate(filename: str) -> None:
	source = BASE/'assets/lect09_unlinked_scene_templates'/filename
	root = ET.parse(source).getroot()
	slot = next(node for node in root.iter() if node.get('id') == 'native-scene-slot')
	parent = next(node for node in root.iter() if slot in list(node))
	index = list(parent).index(slot)
	parent.remove(slot)
	parent.insert(index, segregation() if filename == 'unlinked_segregation.svg' else tetratype())
	output = ET.tostring(root, encoding='utf-8', xml_declaration=True)
	destination = DESTINATIONS[filename]
	destination.parent.mkdir(parents=True, exist_ok=True)
	destination.write_bytes(output)


def main() -> None:
	for filename in FILENAMES:
		generate(filename)


if __name__ == '__main__':
	main()
