#!/usr/bin/env python3
"""Compose frozen accepted LECT13D components with source-backed associations."""

import argparse
import hashlib
import json
import pathlib
import subprocess
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as DET

import svg_tools.drawing
import svg_tools.parts
import svg_tools.svg_import


HERE = pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip()) / 'genetics/LECT13/djot'

#============================================
def compose(name: str, specification: dict,
		components: dict, component_dir: pathlib.Path | None = None) -> str:
	"""Place each original component occurrence without changing its geometry."""
	parts: dict[str, svg_tools.parts.SvgPart] = {}
	for index, placement in enumerate(specification['parts']):
		component = components[placement['asset']]
		path = component_dir / placement['asset'] if component_dir else None
		if path and path.is_file():
			markup = path.read_text()
		else:
			markup = component['svg']
			if hashlib.sha256(markup.encode()).hexdigest() != component['sha256']:
				raise ValueError(f"Frozen component hash differs: {placement['asset']}")
		component_root = DET.fromstring(markup)
		svg_tools.drawing.remove_canvas_background(component_root)
		markup = ET.tostring(component_root, encoding='unicode')
		part = svg_tools.svg_import.import_svg(markup, name=f'occurrence_{index}', size=placement['width'])
		viewbox = [float(value) for value in DET.fromstring(markup).attrib['viewBox'].split()]
		# Keep source centers fixed when a strip gains room for its centromere collar.
		y = placement['y'] + viewbox[1]*placement['width']/viewbox[2]
		parts[f'occurrence_{index}'] = svg_tools.parts.transform(part, x=placement['x'], y=y)
	group = svg_tools.parts.group(parts)
	width, height = specification['size']
	if group.bounds[0] < 0 or group.bounds[1] < 0 or group.bounds[2] > width or group.bounds[3] > height:
		raise ValueError(f'Composition bounds exceed viewport: {name}: {group.bounds}')
	root = ET.Element('svg', {'xmlns':'http://www.w3.org/2000/svg', 'width':str(width),
		'height':str(height), 'viewBox':f'0 0 {width} {height}', 'role':'img', 'aria-labelledby':'title description'})
	ET.SubElement(root, 'title', {'id':'title'}).text = name.replace('_', ' ')
	ET.SubElement(root, 'desc', {'id':'description'}).text = specification['description']
	root.append(DET.fromstring(group.fragment))
	for index, cross in enumerate(specification['crosses']):
		x, y, half = cross['x'], cross['y'], cross['size'] / 2
		path = f'M {x-half} {y-half} L {x+half} {y+half} M {x-half} {y+half} L {x+half} {y-half}'
		marker = ET.SubElement(root, 'g', {'id':f'source-rejection-cross-{index}'})
		for color, weight in (('#344651', 23), ('#F47777', 16)):
			ET.SubElement(marker, 'path', {'d':path, 'stroke':color, 'stroke-width':str(weight), 'fill':'none'})
	for index, label in enumerate(specification['labels']):
		ET.SubElement(root, 'text', {'id':f'source-label-{index}', 'x':str(label['x']),
			'y':str(label['y']), 'fill':label['color'], 'font-size':str(label['size']),
			'font-family':'Atkinson Hyperlegible Next'}).text = label['text']
	# LibreOffice needs SVG elements under the default namespace, without ns0 prefixes.
	for element in root.iter():
		if isinstance(element.tag, str):
			element.tag = element.tag.removeprefix('{http://www.w3.org/2000/svg}')
		for attribute in tuple(element.attrib):
			if attribute.startswith('{http://www.w3.org/1999/xlink}'):
				root.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')
				element.set('xlink:' + attribute.split('}', 1)[1], element.attrib.pop(attribute))
	result = ET.tostring(root, encoding='unicode')
	svg_tools.svg_import.import_svg(result, name='validated_composition')
	return result + '\n'


#============================================
def main() -> None:
	"""Write the reviewed compositions beside the original deck illustrations."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--output', type=pathlib.Path,
		default=HERE / 'assets/lect13d-meiosis_translocation')
	parser.add_argument('--components-dir', type=pathlib.Path,
		help='Use shared-geometry component SVGs instead of frozen source bodies.')
	args = parser.parse_args()
	data_path = HERE / 'lect13d_p1_composition_data.json'
	data: dict = json.loads(data_path.read_text())
	args.output.mkdir(parents=True, exist_ok=True)
	for name, specification in data['figures'].items():
		(args.output / f'{name}.drawn.svg').write_text(
			compose(name, specification, data['components'], args.components_dir))


if __name__ == '__main__':
	main()
