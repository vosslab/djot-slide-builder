#!/usr/bin/env python3
"""Rebuild the ordered-half crossover figure from its layout model."""
import json
import pathlib

import lxml.etree
import svg_tools._xml
import svg_tools.chromosomes
import svg_tools.drawing


BASE = pathlib.Path(__file__).resolve().parent
ASSETS = BASE / 'assets/lect09_ordered_templates'
OUTPUT = BASE / 'assets/lect09c-tetrad_worked_examples_bpw'
NS = 'http://www.w3.org/2000/svg'
TAG = '{' + NS + '}'



#============================================
def build_body(model: dict) -> lxml.etree._Element:
	"""Build one ordered chromatid with the shared straight-rod renderer.

	Args:
		model: Explicit color, size, and placement for one product.

	Returns:
		SVG group positioned at the source location.
	"""
	chromosome = svg_tools.chromosomes.Chromosome((
		svg_tools.chromosomes.Segment('', model['color'], model['length']),
	))
	layout = svg_tools.chromosomes.render_chromosome_layout(
		model['id'], chromosome, length=model['length'], thickness=model['thickness'],
		texture=False, labels=False,
	)
	wrapper = '<g xmlns="' + NS + '">' + layout.svg + '</g>'
	element = list(svg_tools._xml.parse(wrapper))[0]
	return element


#============================================
def main() -> None:
	"""Render all modeled chromosome bodies into the durable figure template."""
	root = svg_tools._xml.read(ASSETS / 'ordered_half.svg')
	models = json.loads((ASSETS / 'ordered_half_models.json').read_text())
	by_id = {model['id']: model for model in models}
	for parent in list(root.iter()):
		for node in list(parent):
			body_id = node.get('data-chromosome-slot')
			if body_id:
				index = list(parent).index(node)
				parent.remove(node)
				parent.insert(index, build_body(by_id[body_id]))
	OUTPUT.mkdir(parents=True, exist_ok=True)
	lxml.etree.ElementTree(svg_tools.drawing.svg_root(root)).write(OUTPUT / 'ordered_half.svg', encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
	main()
