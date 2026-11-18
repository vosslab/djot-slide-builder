#!/usr/bin/env python3
"""Regenerate the chromosome schematics for LECT06.

From the repository root, run:
source source_me.sh && python3 genetics/LECT06/djot/make_chromosome_xlinked.py
"""

import json
import pathlib
import subprocess


import lxml.etree
import svg_tools._xml
import svg_tools.annotations
import svg_tools.chromosomes
import svg_tools.chromosome_topology
import svg_tools.drawing
import svg_tools.palette
import svg_tools.parts


#============================================
def _figure_path(target: str, repository_root: pathlib.Path,
	output_root: pathlib.Path | None) -> pathlib.Path:
	output = (repository_root / target if output_root is None else
		output_root / 'assets' / target.split('/assets/', 1)[1])
	output.parent.mkdir(parents=True, exist_ok=True)
	return output


#============================================
def _write_figure(root: lxml.etree._Element, target: str, repository_root: pathlib.Path,
	output_root: pathlib.Path | None) -> None:
	output = _figure_path(target, repository_root, output_root)
	svg_tools.drawing.remove_canvas_background(root)

	# ASVS 1.2.1: Serialize SVG attributes through the XML writer.
	output.write_bytes(lxml.etree.tostring(svg_tools.drawing.svg_root(root), encoding='ascii', xml_declaration=False) + b'\n')


#============================================
def generate_complements(model_path: pathlib.Path, repository_root: pathlib.Path,
	output_root: pathlib.Path | None = None) -> None:
	"""Compare the XX and XY complements as if viewed at one magnification.

	The poses share a chromatid width and axial scale so chromosome 4 appears
	short while its collar remains comparable to the other centromeres. The
	arm colors distinguish identity and the teal regions show broad mitotic
	heterochromatin domains. Their boundaries are schematic.

	In the XY panel, place the two collars at comparable heights and turn the
	short arm of Y toward the proximal X pairing region. This lets the shape
	suggest the orientation at male metaphase I. The sources for the chromatin
	map, pairing region, and collar design are in prototype/chromosome_review_sources.md.
	"""
	topology = svg_tools.chromosome_topology
	data = json.loads(model_path.read_text(encoding='utf-8'))
	composition = data['composition']
	width = composition['chromosome_width']
	heterochromatin = svg_tools.palette.shade('teal', 'dark')
	paints = {rod: {region: svg_tools.palette.shade(*swatch)
		for region, swatch in regions.items()} for rod, regions in data['palette'].items()}
	font = 'Atkinson Hyperlegible Next, sans-serif'
	text_color = '#263844'
	body = lxml.etree.Element('g')
	for complement, layout in composition['panels'].items():
		dx, dy = layout['translation']
		panel = lxml.etree.SubElement(body, 'g', {'id': f'{complement}-complement',
			'transform': f'translate({dx} {dy})'})
		for kind in ('2', '3', '4', 'x'):
			mate = complement[1] if kind == 'x' else kind
			first_id = f'{complement}-chromosome-{kind}-1'
			second_id = f'{complement}-chromosome-{mate}-2'
			first = topology.chromosome(first_id, **data['chromosomes'][kind])
			second = (topology.homolog(first, second_id) if mate == kind else
				topology.chromosome(second_id, **data['chromosomes'][mate]))
			for model, rod in ((first, kind), (second, mate)):
				pose = data['poses'][rod]
				points = pose['points']
				if model is second and mate == kind:
					dx, dy = pose['homolog_offset']
					points = [(x + dx, y + dy) for x, y in points]
				palette = {(model.id, region): color for region, color in paints[rod].items()}
				palette[model.id, 'heterochromatin'] = heterochromatin
				collar = svg_tools.chromosomes.CentromereStyle(label=rod.upper(),
					fill=svg_tools.palette.shade(data['centromere_hues'][rod], 'extra_light'))
				part = svg_tools.chromosomes.render(model.id + '-shared', model,
					points=points, width=width, scale=composition['length_scale'], palette=palette,
					centromere_styles={(model.id, f'{model.id}.cen'): collar})
				chromosome = lxml.etree.SubElement(panel, 'g', {
					'id': model.id, 'data-chromosome': rod.upper()})
				chromosome.append(svg_tools._xml.parse(part.fragment))
		labels = lxml.etree.SubElement(panel, 'g', {'id': f'{complement}-labels'})
		for label in composition['arm_labels'] + layout['sex_labels']:
			callout = lxml.etree.SubElement(labels, 'g')
			label_svg = svg_tools.drawing.text(*label['position'], label['text'],
				size=31, color=text_color, font=font)
			callout.append(svg_tools._xml.parse(label_svg))
			for points in label['leaders']:
				leader = svg_tools.annotations.connector(points, kind='callout',
					color='#394952', stroke_width=2.5)
				callout.append(svg_tools._xml.parse(leader.fragment))
	legend = lxml.etree.SubElement(body, 'g', {'id': 'legend'})
	legend_layout = composition['legend']
	swatch_x, swatch_y = legend_layout['heterochromatin']['swatch_position']
	lxml.etree.SubElement(legend, 'rect', {'x': str(swatch_x), 'y': str(swatch_y),
		'width': '39', 'height': '39', 'fill': heterochromatin,
		'stroke': svg_tools.palette.shade('teal', 'extra_dark'), 'stroke-width': '2'})
	for label in legend_layout.values():
		label_svg = svg_tools.drawing.text(*label['position'], label['text'],
			size=30, color=text_color, anchor='start', font=font)
		legend.append(svg_tools._xml.parse(label_svg))
	marker = svg_tools.chromosomes.centromere_part('legend', thickness=width)
	marker = svg_tools.parts.transform(marker,
		*legend_layout['centromere']['marker_position'], rotation=90)
	legend.append(svg_tools._xml.parse(marker.fragment))
	output = _figure_path(data['target'], repository_root, output_root)
	body_svg = ''.join(lxml.etree.tostring(group, encoding='unicode') for group in body)
	# ASVS 1.2.1: Write labels and metadata through the SVG writer's XML serializer.
	svg_tools.drawing.write_svg(output, *composition['canvas'], composition['title'],
		composition['description'], body_svg)


#============================================
def generate(data_directory: pathlib.Path, repository_root: pathlib.Path,
	output_root: pathlib.Path | None = None) -> None:
	"""Generate the complements and update the four legacy schematics."""
	for model_path in sorted(data_directory.glob('*.json')):
		if model_path.stem == 'drosophila_chromosome_complements':
			generate_complements(model_path, repository_root, output_root)
			continue
		data = json.loads(model_path.read_text(encoding='utf-8'))
		root = svg_tools._xml.read(model_path.with_suffix('.template.svg'))
		groups = {element.attrib['id']: element for element in root.iter()
			if 'id' in element.attrib}
		for item in data['placements']:
			model = item['model']
			chromosome = svg_tools.chromosomes.Chromosome(tuple(
				svg_tools.chromosomes.Segment('', color, length)
			for color, length in model['segments']), centromeres=(
				svg_tools.chromosomes.Centromere(model['centromere']),)
			if model['centromere'] is not None else ())
			if 'path' in item:
				part = svg_tools.chromosomes.chromosome_path_part(
					item['group'] + '-shared', chromosome, item['path'],
					thickness=item['thickness'], labels=False)
			else:
				part = svg_tools.chromosomes.chromosome_part(
					item['group'] + '-shared', chromosome, length=item['length'],
					orientation=item['orientation'], thickness=item['thickness'],
					texture=False, labels=False)
			element = svg_tools._xml.parse(part.fragment)
			if 'translate' in item:
				element.set('transform', 'translate(' +
					' '.join(str(value) for value in item['translate']) + ')')
			groups[item['group']].insert(0, element)
		_write_figure(root, data['target'], repository_root, output_root)


#============================================
def main() -> None:
	repository = pathlib.Path(subprocess.check_output(
		['git', 'rev-parse', '--show-toplevel'], text=True).strip())
	generate(repository / 'genetics/LECT06/djot/chromosome_models/xlinked', repository)


if __name__ == '__main__':
	main()
