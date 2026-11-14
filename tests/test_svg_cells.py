"""Cell envelopes and explicitly composed nuclear parts."""

import math
import xml.etree.ElementTree

import pytest

import svg_tools.cells
import svg_tools.parts


def test_cell_envelopes_and_anchors():
	paths = []
	for kind in ('animal', 'bacterial', 'yeast', 'fused_yeast', 'plant'):
		part = svg_tools.cells.cell_envelope(kind=kind, width=200, height=100,
			color='#e8f2ed', wall_color='#c2ddb9' if kind == 'plant' else None)
		root = xml.etree.ElementTree.fromstring(part.fragment)
		shapes = root.findall('path')
		assert len(shapes) == (2 if kind == 'plant' else 1)
		assert root.attrib['stroke'] == '#344651'
		assert part.bounds == pytest.approx((-110.5, -55.25, 110.5, 55.25))
		assert {'center', 'top', 'bottom', 'left', 'right'} <= part.anchors.keys()
		assert all(part.bounds[0] <= x <= part.bounds[2] and part.bounds[1] <= y <= part.bounds[3]
			for x, y in part.anchors.values())
		paths.append(shapes[0].attrib['d'])
		if kind == 'fused_yeast':
			assert shapes[0].attrib['d'].count('M ') == 1
			assert shapes[0].attrib['d'].count(' Z') == 1
			assert part.anchors['left_lobe'][0] < 0 < part.anchors['right_lobe'][0]
	assert len(set(paths)) == 5
	with pytest.raises(ValueError):
		svg_tools.cells.cell_envelope(kind='plant', width=100, height=100, color='white')
	with pytest.raises(ValueError):
		svg_tools.cells.cell_envelope(kind='unknown', width=100, height=100, color='white')


def test_nuclear_parts_are_explicit_and_validate_dimensions():
	cell = svg_tools.cells.cell_envelope(kind='fused_yeast', width=300, height=150, color='white')
	nucleus = svg_tools.cells.nucleus(width=58, height=52, color='blue')
	nucleolus = svg_tools.cells.nucleolus(width=16, height=15, color='purple')
	parts = {'cell': cell, 'left': svg_tools.parts.transform(nucleus, x=cell.anchors['left_lobe'][0]),
		'right': svg_tools.parts.transform(nucleus, x=cell.anchors['right_lobe'][0]),
		'nucleolus': nucleolus}
	root = xml.etree.ElementTree.fromstring('<g>' + svg_tools.parts.group(parts).fragment + '</g>')
	assert len(root.findall('.//path')) == 4
	assert nucleus.anchors['center'] == nucleolus.anchors['center'] == (0, 0)
	for factory in (svg_tools.cells.nucleus, svg_tools.cells.nucleolus):
		for width, height in ((0, 10), (10, -1), (math.inf, 10), (10, math.nan)):
			with pytest.raises(ValueError):
				factory(width=width, height=height, color='white')
