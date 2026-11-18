#!/usr/bin/env python3
"""Compose frozen accepted LECT13D components with source-backed associations."""

import argparse
import hashlib
import json
import pathlib
import subprocess

import lxml.etree
import svg_tools._xml
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
			markup = path.read_bytes()
		else:
			markup = (HERE / component['artwork']).read_bytes()
			if hashlib.sha256(markup).hexdigest() != component['sha256']:
				raise ValueError(f"Frozen component hash differs: {placement['asset']}")
		component_root = svg_tools._xml.parse_document(markup)
		svg_tools.drawing.remove_canvas_background(component_root)
		markup = lxml.etree.tostring(component_root, encoding='unicode')
		part = svg_tools.svg_import.import_svg(markup, name=f'occurrence_{index}', size=placement['width'])
		viewbox = [float(value) for value in component_root.attrib['viewBox'].split()]
		# Keep source centers fixed when a strip gains room for its centromere collar.
		y = placement['y'] + viewbox[1]*placement['width']/viewbox[2]
		parts[f'occurrence_{index}'] = svg_tools.parts.transform(part, x=placement['x'], y=y)
	group = svg_tools.parts.group(parts)
	width, height = specification['size']
	if group.bounds[0] < 0 or group.bounds[1] < 0 or group.bounds[2] > width or group.bounds[3] > height:
		raise ValueError(f'Composition bounds exceed viewport: {name}: {group.bounds}')
	root = lxml.etree.Element('svg', {'xmlns':'http://www.w3.org/2000/svg', 'width':str(width),
		'height':str(height), 'viewBox':f'0 0 {width} {height}', 'role':'img', 'aria-labelledby':'title description'})
	lxml.etree.SubElement(root, 'title', {'id':'title'}).text = name.replace('_', ' ')
	lxml.etree.SubElement(root, 'desc', {'id':'description'}).text = specification['description']
	root.append(svg_tools._xml.parse(group.fragment))
	for index, cross in enumerate(specification['crosses']):
		x, y, half = cross['x'], cross['y'], cross['size'] / 2
		path = f'M {x-half} {y-half} L {x+half} {y+half} M {x-half} {y+half} L {x+half} {y-half}'
		marker = lxml.etree.SubElement(root, 'g', {'id':f'source-rejection-cross-{index}'})
		for color, weight in (('#344651', 23), ('#F47777', 16)):
			lxml.etree.SubElement(marker, 'path', {'d':path, 'stroke':color, 'stroke-width':str(weight), 'fill':'none'})
	for index, label in enumerate(specification['labels']):
		lxml.etree.SubElement(root, 'text', {'id':f'source-label-{index}', 'x':str(label['x']),
			'y':str(label['y']), 'fill':label['color'], 'font-size':str(label['size']),
			'font-family':'Atkinson Hyperlegible Next'}).text = label['text']
	result = lxml.etree.tostring(svg_tools.drawing.svg_root(root), encoding='unicode')
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
