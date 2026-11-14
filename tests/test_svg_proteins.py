"""Signaling molecule geometry and composition anchors."""

import math
import xml.etree.ElementTree

import pytest

import svg_tools.parts
import svg_tools.signaling


@pytest.mark.parametrize('factory', [svg_tools.signaling.protein,
	svg_tools.signaling.ligand, svg_tools.signaling.receptor])
def test_molecule_bounds_anchors_and_dimensions(factory):
	part = factory(width=100, height=80, color='#cbdcf0')
	root = xml.etree.ElementTree.fromstring(part.fragment)
	assert root.attrib['fill'] == '#cbdcf0'
	assert root.find('path') is not None
	assert part.bounds[0] < 0 < part.bounds[2] and part.bounds[1] < 0 < part.bounds[3]
	assert {'center', 'binding', 'input', 'output', 'modification'} <= part.anchors.keys()
	assert all(part.bounds[0] <= x <= part.bounds[2] and part.bounds[1] <= y <= part.bounds[3]
		for x, y in part.anchors.values())
	for width, height in ((0, 80), (100, -1), (math.inf, 80), (100, math.nan)):
		with pytest.raises(ValueError):
			factory(width=width, height=height, color='#cbdcf0')


def test_receptor_membrane_anchors_transform():
	part = svg_tools.parts.transform(svg_tools.signaling.receptor(
		width=100, height=200, color='#cbdcf0'), x=20, y=40)
	assert part.anchors['membrane'] == (20, 40)
	assert part.anchors['extracellular'][1] < 40 < part.anchors['cytoplasmic'][1]


def test_protein_kinds_are_distinct_and_invalid_kind_rejected():
	globular = svg_tools.signaling.protein(width=100, height=80, color='blue')
	kinase = svg_tools.signaling.protein(width=100, height=80, color='blue', kind='kinase')
	assert globular.fragment != kinase.fragment
	with pytest.raises(ValueError):
		svg_tools.signaling.protein(width=100, height=80, color='blue', kind='other')
