"""Schematic organelles expose useful placement geometry and distinct structures."""

import xml.etree.ElementTree

import pytest
import svgpathtools

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
	# ER comprises distinct folded cisternae; Golgi remains a different structure.
	er = xml.etree.ElementTree.fromstring(fragments['er'])
	assert len(er.findall('path')) >= 3
	assert fragments['er'] != fragments['golgi']
	with pytest.raises(ValueError):
		svg_tools.cells.organelle(kind='unknown', width=100, height=60, color='white')
	with pytest.raises(ValueError):
		svg_tools.cells.organelle(kind='er', width=0, height=60, color='white')


def test_mitochondrial_membranes_are_closed_and_cristae_do_not_cross():
	part = svg_tools.cells.organelle(kind='mitochondrion', width=130, height=86, color='#f3c8b7')
	root = xml.etree.ElementTree.fromstring(part.fragment)
	outer = svgpathtools.parse_path(root.find("path[@data-role='outer-membrane']").get('d'))
	inner = svgpathtools.parse_path(root.find("path[@data-role='inner-membrane']").get('d'))
	for membrane in (outer, inner):
		assert membrane.iscontinuous() and membrane.isclosed()
		for index, segment in enumerate(membrane):
			for other_index in range(index + 2, len(membrane)):
				if index == 0 and other_index == len(membrane) - 1:
					continue
				assert not segment.intersect(membrane[other_index])
	assert not outer.intersect(inner)
	# Multiple transverse crossings distinguish folds from a plain nested oval.
	assert len(inner.intersect(svgpathtools.Path(svgpathtools.Line(-100, 100)))) >= 6
	for name in ('top', 'bottom', 'left', 'right'):
		point = complex(*part.anchors[name])
		assert any(abs(segment.start - point) < 1e-9 for segment in outer)
