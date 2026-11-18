"""Schematic organelles expose useful placement geometry and distinct structures."""

import svgpathtools

import lxml.etree
import svg_tools.cells
def test_mitochondrial_membranes_are_closed_and_cristae_do_not_cross() -> None:
	part = svg_tools.cells.organelle(kind='mitochondrion', width=130, height=86, color='#f3c8b7')
	root = lxml.etree.fromstring(part.fragment)
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
