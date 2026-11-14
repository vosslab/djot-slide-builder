"""Schematic organelles expose useful placement geometry and distinct structures."""

import xml.etree.ElementTree

import pytest

import svg_tools.cells


def test_organelle_structures_and_anchors():
	fragments = {}
	for kind in ('mitochondrion', 'chloroplast', 'er', 'golgi', 'lysosome', 'vesicle'):
		part = svg_tools.cells.organelle(kind=kind, width=100, height=60, color='#eee')
		fragments[kind] = part.fragment
		assert {'center', 'top', 'bottom', 'left', 'right'} <= part.anchors.keys()
		assert part.anchors['center'] == (0, 0)
		assert all(part.bounds[0] <= x <= part.bounds[2] and part.bounds[1] <= y <= part.bounds[3]
			for x, y in part.anchors.values())
		assert part.bounds[0] < 0 < part.bounds[2] and part.bounds[1] < 0 < part.bounds[3]
	# ER is a connected membrane with enclosed openings; Golgi is a distinct structure.
	er = xml.etree.ElementTree.fromstring(fragments['er'])
	assert any(shape.get('fill-rule') == 'evenodd' for shape in er.findall('path'))
	assert fragments['er'] != fragments['golgi']
	with pytest.raises(ValueError):
		svg_tools.cells.organelle(kind='unknown', width=100, height=60, color='white')
	with pytest.raises(ValueError):
		svg_tools.cells.organelle(kind='er', width=0, height=60, color='white')
