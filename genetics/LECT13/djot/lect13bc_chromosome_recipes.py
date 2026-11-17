#!/usr/bin/env python3
"""Regenerate LECT13B/C source compositions using the shared chromosome family."""

import argparse
import base64
import json
import math
import pathlib
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as DET

import svgpathtools
import subprocess
import svg_tools.chromosomes
import svg_tools.chromosome_surface
import svg_tools.parts


#============================================
def integrate_loci(root: ET.Element, source: dict) -> None:
	"""Replace exercise cards with small regions swept inside their fixed rods."""
	cards = []
	for parent in root.iter():
		children = list(parent)
		for index, card in enumerate(children[:-1]):
			label = children[index+1]
			if (card.tag.endswith('rect') and label.tag.endswith('text')
				and card.get('width') == '34' and card.get('height') == '36'
				and card.get('fill') == 'white'):
				cards.append((parent, card, label))
	if len(cards) != 20:
		raise ValueError(f'Expected 20 fixed inversion loci, found {len(cards)}')
	for number, (parent, card, label) in enumerate(cards):
		part_number = number // 5
		data = source['parts'][part_number]
		path = svgpathtools.parse_path(data['path'])
		surface = svg_tools.chromosome_surface.Surface(path, data['thickness'])
		center_x, center_y = float(card.get('x'))+17, float(card.get('y'))+18
		# These four rods are straight, but retaining the centerline calculation keeps
		# the locus construction identical to curved chromatids.
		center = svg_tools.chromosome_surface.nearest_distance(surface.path, complex(center_x, center_y))
		parent.remove(card)
		parent.remove(label)
		gene = svg_tools.chromosomes.Segment(label.text or '', '#F3D788', 24)
		part = svg_tools.chromosomes.gene_locus_part(
			f'inversion-double-crossover-gene-{number}', surface, center, gene)
		parent.append(DET.fromstring(part.fragment))


#============================================
def generate(source_path: pathlib.Path, output_root: pathlib.Path) -> None:
	"""Keep authored text/composition and replace source-data chromosome placeholders."""
	sources = json.loads(source_path.read_text())
	image_name = 'lect13bc_inversion_exercise_source.png'
	image_uri = 'data:image/png;base64,' + base64.b64encode(
		(source_path.parent / image_name).read_bytes()).decode('ascii')
	for relative, source in sources.items():
		root = DET.fromstring(source['svg'].replace('local-image:' + image_name, image_uri))
		if relative.endswith('inversion-double-crossover-problem.drawn.svg'):
			integrate_loci(root, source)
		position_effect_loci = ()
		if relative.endswith('position-effect-chromosomes.drawn.svg'):
			position_effect_loci = ((0, complex(192.5, 110)), (1, complex(667.5, 300)))
			for parent in root.iter():
				children = list(parent)
				for card, label in zip(children, children[1:]):
					if (card.tag.endswith('rect') and label.tag.endswith('text')
						and card.get('fill') == '#812F46' and label.text == 'w+'):
						parent.remove(card)
						parent.remove(label)
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
				replacement = DET.fromstring(part.fragment)
				replacement.attrib['data-source-part'] = str(index)
				replacement.attrib['stroke'] = 'none'
				if 'centromere' in part.anchors:
					markers[index] = (replacement, part.anchors['centromere'], data['thickness'])
				position = list(parent).index(child)
				parent.remove(child)
				parent.insert(position, replacement)
				for locus_index, source_center in position_effect_loci:
					if index != locus_index:
						continue
					surface = svg_tools.chromosome_surface.Surface(
						svgpathtools.parse_path(data['path']), data['thickness'])
					center = svg_tools.chromosome_surface.nearest_distance(surface.path, source_center)
					gene = svg_tools.chromosomes.Segment('w+', '#812F46', 65)
					locus = svg_tools.chromosomes.gene_locus_part(
						f'migrated13bc-position-effect-gene-{index}', surface, center, gene)
					replacement.append(DET.fromstring(locus.fragment))
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
				root.append(DET.fromstring(svg_tools.parts.transform(belt,
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
	here = pathlib.Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()) / 'genetics/LECT13/djot'
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--output-root', type=pathlib.Path, default=here)
	args = parser.parse_args()
	generate(here / 'lect13bc_chromosome_sources.json', args.output_root)


if __name__ == '__main__':
	main()
