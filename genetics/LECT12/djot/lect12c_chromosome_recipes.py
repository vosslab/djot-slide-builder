#!/usr/bin/env python3
"""Refresh LECT12C chromosomes while retaining authored labels and diagram geometry.

Run with source source_me.sh && python3 genetics/LECT12/djot/lect12c_chromosome_recipes.py.
Condensed Barr bodies,
expression bars, and the source-backed gene distribution map retain their own forms.
"""

import re
import pathlib
import subprocess

import lxml.etree
import svg_tools._xml
import svg_tools.chromosomes
import svg_tools.drawing


REPO_ROOT = pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip())
ROOT = REPO_ROOT / 'genetics/LECT12/djot/assets'
NS = 'http://www.w3.org/2000/svg'


# C44-C46 keep a measured 12-unit clear edge around the visible teaching content.
CANVAS_CROPS = {
	'x_inactivation_lineages.drawn.svg': ('44 9 1067 644', '1067', '644'),
	'calico_x_lineages.drawn.svg': ('80 1 455 541', '455', '541'),
	'pseudoautosomal_crossover.drawn.svg': ('59 29 532 554', '532', '554'),
}

#============================================
def rod(name: str, x: float, y: float, width: float, length: float,
	color: str, tip: str | None = None, centromere: float | None = None) -> lxml.etree._Element:
	"""Place a shared chromatid with only source-depicted centromere anatomy."""
	if color == '#888':
		color = '#888888'
	if centromere is None:
		model = svg_tools.chromosomes.Chromosome((
			svg_tools.chromosomes.Segment('', color, length),))
	else:
		upper = length * centromere
		segments = (svg_tools.chromosomes.Segment('', color, upper),
			svg_tools.chromosomes.Segment('', color, length - upper))
		boundary = 1
		if tip is not None:
			segments = (svg_tools.chromosomes.Segment('', tip, 70),
				svg_tools.chromosomes.Segment('', color, upper - 70), segments[-1])
			boundary = 2
		model = svg_tools.chromosomes.Chromosome(segments,
			centromeres=(svg_tools.chromosomes.Centromere(boundary),))
	part = svg_tools.chromosomes.chromosome_part(f'{name}-body', model, length=length,
		thickness=width, orientation='vertical', texture=False, labels=False)
	group = lxml.etree.Element(f'{{{NS}}}g', {'data-lect12c-chromosome': 'true',
		'transform': f'translate({x} {y})'})
	group.append(svg_tools._xml.parse(part.fragment))
	return group


#============================================
def replace_rect(parent: lxml.etree._Element, element: lxml.etree._Element, name: str,
	centromere: float | None) -> None:
	"""Replace one chromosome rectangle, preserving its surrounding ordering."""
	color = element.attrib['fill']
	if color == '#888':
		color = '#888888'
	replacement = rod(name, float(element.attrib['x']), float(element.attrib['y']),
		float(element.attrib['width']), float(element.attrib['height']), color,
		centromere=centromere)
	index = list(parent).index(element)
	parent.remove(element)
	parent.insert(index, replacement)


#============================================
def replace_barr_bodies(root: lxml.etree._Element, name: str) -> None:
	"""Render the source's inactive X circles from retained chromosome content."""
	serial = 0
	for parent in list(root.iter()):
		for child in list(parent):
			if (child.tag != f'{{{NS}}}circle' or child.attrib.get('r') != '12'
					or child.attrib.get('fill') not in ('#B74300', '#076DAD')):
				continue
			serial += 1
			model = svg_tools.chromosomes.Chromosome((
				svg_tools.chromosomes.Segment('', child.attrib['fill']),))
			part = svg_tools.chromosomes.condensed_chromosome_part(
				f'{name}-barr-{serial}', model, radius=12)
			replacement = svg_tools._xml.parse(part.fragment)
			replacement.set('transform', f'translate({child.attrib["cx"]} {child.attrib["cy"]})')
			index = list(parent).index(child)
			parent.remove(child)
			parent.insert(index, replacement)


#============================================
def refresh(path: pathlib.Path) -> None:
	"""Migrate old primitives or refresh renderer-owned groups idempotently."""
	root = svg_tools._xml.read(path)
	name = path.stem.replace('.', '-')
	serial = 0
	# image_005 necks: 70..241 with center 119 (~28%); image_009: central.
	centromere = {
		'worms_dosage': None, 'flies_dosage': None, 'mammals_dosage': None,
		'dosage_compensation_summary': None, 'x_activity': None,
		'x_inactivation_lineages': .28, 'calico_x_lineages': .5,
		'pseudoautosomal_crossover': None,  # X and Y positions are set separately below.
	}[path.name.removesuffix('.drawn.svg')]
	for parent in list(root.iter()):
		for child in list(parent):
			# Renderer-owned groups record their input to regenerate from the shared core.
			if 'data-lect12c-input' in child.attrib:
				values = child.attrib['data-lect12c-input'].split(',')
				x, y, width, length = map(float, values[:4])
				tip = values[5] if len(values) == 6 else None
				updated = rod(child.attrib['id'], x, y, width, length, values[4], tip, centromere)
				updated.attrib.update(child.attrib)
				index = list(parent).index(child)
				parent.remove(child)
				parent.insert(index, updated)
				continue
			if child.tag == f'{{{NS}}}rect' and 'rx' in child.attrib:
				# Panel borders and expression bars have no chromosome fill/radius pairing.
				if child.attrib['fill'] in ('none', 'white', '#ffffff'):
					continue
				if path.name == 'pseudoautosomal_crossover.drawn.svg':
					continue
				serial += 1
				index = list(parent).index(child)
				replace_rect(parent, child, f'{name}-chromosome-{serial}', centromere)
				group = list(parent)[index]
				group.attrib['id'] = f'{name}-chromosome-{serial}'
				group.attrib['data-lect12c-input'] = ','.join(child.attrib[k]
					for k in ('x', 'y', 'width', 'height', 'fill'))
			elif (child.tag == f'{{{NS}}}path' and child.attrib.get('stroke-width') == '9'
				and re.fullmatch(r'M[0-9.]+ [0-9.]+ V[0-9.]+', child.attrib['d'])):
				serial += 1
				x, y, end = map(float, re.findall(r'[0-9.]+', child.attrib['d']))
				identifier = f'{name}-chromosome-{serial}'
				group = rod(identifier, x-5, y, 10, end-y, child.attrib['stroke'], centromere=centromere)
				group.attrib['id'] = identifier
				group.attrib['data-lect12c-input'] = f'{x-5},{y},10,{end-y},{child.attrib["stroke"]}'
				index = list(parent).index(child)
				parent.remove(child)
				parent.insert(index, group)
	# Summary highlight strokes belong to the replaced old rectangle silhouettes.
	if path.name == 'dosage_compensation_summary.drawn.svg':
		for parent in list(root.iter()):
			if parent.attrib.get('data-chromosome') in ('X', 'Y'):
				for child in list(parent):
					if child.tag == f'{{{NS}}}path':
						parent.remove(child)
	if path.name == 'pseudoautosomal_crossover.drawn.svg':
		group = root.find(f'{{{NS}}}g[@id="chromosomes"]')
		if not any(element.attrib.get('id') in (
			'par-chromosome-0-body', 'par-chromosome-1-body')
			for element in group.iter()):
			# Only these four exact rectangles belong to the original PAR body drawing.
			for child in list(group):
				if child.tag == f'{{{NS}}}rect' and child.attrib in (
					{'x': '145', 'y': '100', 'width': '65', 'height': '415',
						'rx': '25', 'fill': '#CFE9BB'},
					{'x': '385', 'y': '100', 'width': '65', 'height': '275',
						'rx': '25', 'fill': '#CFE9BB'},
					{'x': '145', 'y': '100', 'width': '65', 'height': '70',
						'rx': '25', 'fill': '#E8D8EC'},
					{'x': '385', 'y': '100', 'width': '65', 'height': '70',
						'rx': '25', 'fill': '#E8D8EC'},
				):
					group.remove(child)
		# image_012: X spans y39..240, neck y122; Y spans y39..178, neck y90.
		for serial, (x, length, position) in enumerate(((145, 415, .41), (385, 275, .37))):
			identifier = f'par-chromosome-{serial}-body'
			replacement = rod(f'par-chromosome-{serial}', x, 100, 65, length,
				'#CFE9BB', '#E8D8EC', position)
			for parent in group:
				body = parent.find(f'{{{NS}}}g[@id="{identifier}"]')
				if body is not None:
					index = list(parent).index(body)
					parent.remove(body)
					parent.insert(index, replacement[0])
					break
			else:
				group.append(replacement)
	if path.name == 'x_inactivation_lineages.drawn.svg':
		replace_barr_bodies(root, name)
	svg_tools.drawing.remove_canvas_background(root)
	crop = CANVAS_CROPS.get(path.name)
	if crop is not None:
		root.set('viewBox', crop[0])
		root.set('width', crop[1])
		root.set('height', crop[2])
	lxml.etree.indent(root, space='  ')
	path.write_bytes(lxml.etree.tostring(svg_tools.drawing.svg_root(root),
		encoding='ascii', xml_declaration=True))


#============================================
def main() -> None:
	"""Update only the eight chromosome-bearing LECT12C vector drawings."""
	names = ('worms_dosage', 'flies_dosage', 'mammals_dosage',
		'x_inactivation_lineages', 'calico_x_lineages', 'pseudoautosomal_crossover', 'x_activity')
	for name in names:
		refresh(ROOT / 'visual_renewal' / f'{name}.drawn.svg')
	refresh(ROOT / 'lect12c-sex_dosage' / 'dosage_compensation_summary.drawn.svg')


if __name__ == '__main__':
	main()
