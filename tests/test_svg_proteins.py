"""Signaling molecule geometry and composition anchors."""

import math
import xml.etree.ElementTree

import pytest
import svgpathtools

import svg_tools.parts
import svg_tools.signaling


@pytest.mark.parametrize(('factory', 'ports'), [
	(lambda **kw: svg_tools.signaling.protein(**kw), {'binding': (1, 1), 'input': (5, .5), 'output': (3, .125)}),
	(lambda **kw: svg_tools.signaling.protein(kind='kinase', **kw),
		{'binding': (1, 1), 'input': (7, .5), 'output': (4, .125)}),
	(svg_tools.signaling.ligand, {'binding': (3, 1), 'input': (0, 0), 'output': (2, .125)}),
	(svg_tools.signaling.receptor, {'binding': (2, 1), 'input': (2, 1), 'extracellular': (2, 1),
		'output': (9, .125), 'cytoplasmic': (9, .125)}),
])
@pytest.mark.parametrize(('width', 'height'), [(100, 80), (53, 170)])
def test_attachment_anchors_touch_authored_contour(factory, ports, width, height):
	part = factory(width=width, height=height, color='blue')
	path = svgpathtools.parse_path(xml.etree.ElementTree.fromstring(part.fragment).find('path').attrib['d'])
	for name, (segment, position) in ports.items():
		point = path[segment].point(position)
		assert part.anchors[name] == pytest.approx((point.real, point.imag), abs=1e-10)


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
