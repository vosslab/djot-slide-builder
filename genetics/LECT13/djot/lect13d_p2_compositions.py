#!/usr/bin/env python3
"""Restore source-native chromosome rows and their exact gamete associations."""

import hashlib
import json
import pathlib
import typing
import xml.etree.ElementTree

import svg_tools.chromosomes
import svg_tools.drawing
import svg_tools.parts
import svg_tools.svg_import
import svg_tools.text


class Model(typing.TypedDict):
	segments: list[list[str | float]]
	centromere_after: int
	source_styles: list[str]


class Column(typing.TypedDict):
	name: str
	equation: list[str]
	pairs: list[list[str]]


class Footer(typing.TypedDict):
	association: str
	original_text: str
	lines: list[str]
	center: int
	font_size: int


class Robertsonian(typing.TypedDict):
	reference: str
	reference_svg: str
	reference_sha256: str
	clip_bounds: list[int]
	footers: list[Footer]


class RejectionCross(typing.TypedDict):
	source_pdf_points: list[list[float]]
	source_pdf_bounds: list[float]
	source_fill: str
	source_fill_opacity: float
	source_stroke: str
	source_stroke_width: float
	target_bounds: list[float]
	target_id: str


class SourceData(typing.TypedDict):
	reference: str
	reference_svg: str
	reference_sha256: str
	models: dict[str, Model]
	columns: list[Column]
	robertsonian: Robertsonian
	rejection_cross: RejectionCross


#============================================
def chromosome(name: str, source: Model) -> svg_tools.parts.SvgPart:
	"""Keep source segment lengths, colors, labels, and established centromeres."""
	segments = tuple(svg_tools.chromosomes.Segment(str(label), str(color), float(length) * 48)
		for label, color, length in source['segments'])
	model = svg_tools.chromosomes.Chromosome(segments, (
		svg_tools.chromosomes.Centromere(source['centromere_after']),))
	parts = {'body': svg_tools.chromosomes.chromosome_part(name, model,
		thickness=42, texture=False, labels=False, sisters=False)}
	x = 0.0
	for index, segment in enumerate(segments):
		if segment.label:
			parts[f'label_{index}'] = svg_tools.text.label(x + segment.length / 2, 34,
				segment.label, size=38, color='#172B3A')
		x += segment.length
	return svg_tools.parts.group(parts)


#============================================
def equation(tokens: list[str], center: float, y: float) -> svg_tools.parts.SvgPart:
	"""Keep the original magenta chromosome identifiers within source equations."""
	bounds = [svg_tools.text.measure_text(token, size=36) for token in tokens]
	widths = [52.0 if '\u2194' in token else right - left
		for token, (left, top, right, bottom) in zip(tokens, bounds)]
	x = center - sum(widths) / 2
	parts: dict[str, svg_tools.parts.SvgPart] = {}
	for index, (token, width) in enumerate(zip(tokens, widths)):
		if '\u2194' in token:
			# Atkinson lacks this source symbol; retain it as live text in the installed symbol face.
			fragment = svg_tools.drawing.text(x + width / 2, y, '\u2194', size=36,
				color='#172B3A', font='Arial')
			parts[f'token_{index}'] = svg_tools.parts.SvgPart(fragment, (x, y - 36, x + width, y + 5), {})
		else:
			parts[f'token_{index}'] = svg_tools.text.label(x, y, token, size=36,
				color='#FF00FF' if token in ('1', '4') else '#172B3A', anchor='start')
		x += width
	return svg_tools.parts.group(parts)


#============================================
def robertsonian_footer(source: Robertsonian,
	output_directory: pathlib.Path) -> pathlib.Path:
	"""Reuse the shared-geometry Robertsonian product sheet with its source labels."""
	shared = output_directory / 'robertsonian_gamete_products.drawn.svg'
	if not shared.is_file():
		raise ValueError('Generate shared Robertsonian gamete products before this composition')
	root = xml.etree.ElementTree.parse(shared).getroot()
	root.set('data-chromosome-review', 'C68')
	for element in root:
		if element.tag.endswith('title'):
			element.text = 'Robertsonian gamete outcomes'
		elif element.tag.endswith('desc'):
			element.text = ('Shared-geometry Robertsonian gamete products with all source '
				'outcomes, probabilities, and explanatory labels retained.')
	path = output_directory / 'lect13d_p2_robertsonian_footer.drawn.svg'
	xml.etree.ElementTree.ElementTree(root).write(path, encoding='ascii', xml_declaration=True)
	return path


#============================================
def normalize_namespace(path: pathlib.Path) -> None:
	"""Avoid LibreOffice's blank-import bug with prefixed SVG element names."""
	root = xml.etree.ElementTree.parse(path).getroot()
	for element in root.iter():
		if element.tag.startswith('{http://www.w3.org/2000/svg}'):
			element.tag = element.tag.split('}', 1)[1]
	root.set('xmlns', 'http://www.w3.org/2000/svg')
	markup = xml.etree.ElementTree.tostring(root, encoding='ascii', xml_declaration=True)
	if any(not e.tag.startswith('{http://www.w3.org/2000/svg}')
		for e in xml.etree.ElementTree.fromstring(markup).iter()):
		raise ValueError('A composition element lost its SVG namespace')
	path.write_bytes(markup)


#============================================
def rejection_cross(source: RejectionCross) -> str:
	"""Reflow the one original shared rejection polygon behind adjacent products."""
	left, top, right, bottom = source['source_pdf_bounds']
	x1, y1, x2, y2 = source['target_bounds']
	points = ' '.join(f'{x1 + (x-left)*(x2-x1)/(right-left):.6f},'
		f'{y1 + (y-top)*(y2-y1)/(bottom-top):.6f}' for x, y in source['source_pdf_points'])
	polygon = xml.etree.ElementTree.Element('polygon', {
		'id': source['target_id'], 'points': points, 'fill': source['source_fill'],
		'fill-opacity': str(source['source_fill_opacity']), 'stroke': source['source_stroke'],
		'stroke-width': str(source['source_stroke_width'] * (x2-x1)/(right-left)),
		'stroke-linejoin': 'round',
	})
	fragment = xml.etree.ElementTree.tostring(polygon, encoding='unicode')
	return fragment


#============================================
def render(output_directory: pathlib.Path) -> list[pathlib.Path]:
	"""Write only the four new compositions; verify both frozen reference inputs."""
	base = pathlib.Path(__file__).resolve().parent
	source: SourceData = json.loads((base / 'lect13d_p2_sources.json').read_text())
	reference_bytes = source['reference_svg'].encode('utf-8')
	if hashlib.sha256(reference_bytes).hexdigest() != source['reference_sha256']:
		raise ValueError('The reviewed reference component changed; review before regenerating')
	reference = svg_tools.svg_import.import_svg(reference_bytes, name='frozen_reference', size=450)
	output_directory.mkdir(parents=True, exist_ok=True)
	outputs = []
	for original_slide in (46, 47, 48):
		parts: dict[str, svg_tools.parts.SvgPart] = {}
		parts['reference'] = svg_tools.parts.transform(reference, x=900, y=8)
		for index, number in enumerate(('1', '2', '3', '4')):
			parts[f'input_{number}'] = svg_tools.parts.transform(
				chromosome(f'input_{number}', source['models'][number]), x=95, y=15 + index * 66)
			parts[f'input_number_{number}'] = svg_tools.text.label(45, 49 + index * 66,
				number, size=42, color='#FF00FF' if number in ('1', '4') else '#172B3A')
		for column_index, column in enumerate(source['columns']):
			left = 32 + column_index * 460
			center = left + 207
			parts[f'heading_{column_index}'] = svg_tools.text.label(center, 330,
				column['name'], size=41, color='#172B3A')
			parts[f'equation_{column_index}'] = equation(column['equation'], center, 378)
			if original_slide > 46:
				for pair_index, pair in enumerate(column['pairs']):
					for row_index, number in enumerate(pair):
						key = f'product_{column_index}_{pair_index}_{row_index}'
						parts[key] = svg_tools.parts.transform(chromosome(key, source['models'][number]),
							x=left + 45, y=414 + pair_index * 154 + row_index * 54)
		if original_slide == 48:
			parts['adjacent_outcome'] = svg_tools.text.label(475, 727,
				'50% really bad', size=39, color='#172B3A')
			parts['balanced_outcome'] = svg_tools.text.label(1155, 550,
				'25% balanced translocation', size=31, color='#CC00CC')
			parts['normal_outcome'] = svg_tools.text.label(1155, 705,
				'25% normal', size=36, color='#008000')
		composite = svg_tools.parts.group(parts)
		if composite.bounds[0] < 0 or composite.bounds[1] < 0 or composite.bounds[2] > 1400 or composite.bounds[3] > 750:
			raise ValueError(f'Composite exceeds its viewport: {composite.bounds}')
		path = output_directory / f'lect13d_p2_gametes_{original_slide}.drawn.svg'
		cross = rejection_cross(source['rejection_cross']) if original_slide == 48 else ''
		svg_tools.drawing.write_svg(path, 1400, 750,
			f'Chromosome 4 and 12 gamete associations, source slide {original_slide}',
			'Original ODP native chromosome rows restored with shared vector chromosome components. '
			'One complete frozen gamete reference remains at upper right. Columns preserve '
			'adjacent-1, adjacent-2, and alternate product associations; source labels stay live.',
			'<rect width="1400" height="750" fill="white" />' + cross + composite.fragment)
		outputs.append(path)
	outputs.append(robertsonian_footer(source['robertsonian'], output_directory))
	for path in outputs:
		normalize_namespace(path)
	return outputs


#============================================
def main() -> None:
	render(pathlib.Path(__file__).resolve().parent / 'assets/lect13d-meiosis_translocation')


if __name__ == '__main__':
	main()
