"""Binding anchors are actual silhouette terminals and authored contacts coincide."""

import math
import xml.etree.ElementTree as ET

import pytest
import svgpathtools

from svg_tools import binding
from svg_tools.examples.binding import examples


def test_silhouette_anchors_and_bounds():
	part = binding.antibody(width=100, height=200, color='#abcd12')
	path = ET.fromstring(part.fragment).find('path')
	outline = svgpathtools.parse_path(path.get('d'))
	for anchor in ('Fab_left', 'Fab_right', 'Fc'):
		x, y = part.anchors[anchor]
		point = complex(x / 100, y / 200)
		assert any(abs(segment.point(.5) - point) < 1e-12 for segment in outline)
	assert part.anchors['Fab_left'] == (-45, -93)
	assert part.anchors['Fab_right'] == (45, -93)
	assert part.anchors['Fc'] == (0, 100)
	assert part.bounds == pytest.approx((-51.25, -102.5, 51.25, 102.5))
	assert ET.fromstring(part.fragment).get('fill') == '#abcd12'
	for factory in (binding.antibody, binding.antigen, binding.enzyme_tag):
		for bad in (0, -1, math.inf, math.nan):
			with pytest.raises(ValueError):
				factory(width=bad, height=20, color='blue')


def test_authored_contacts():
	western, sandwich = examples()
	for part, pairs in ((western, [('target.top', 'primary.Fab_left'),
		('primary.Fc', 'secondary.Fab_left'), ('secondary.Fc', 'enzyme.bottom')]),
		(sandwich, [('antigen.bottom', 'capture.Fab_right'),
		('antigen.top', 'detection.Fab_left')])):
		for a, b in pairs:
			assert part.anchors[a] == pytest.approx(part.anchors[b])
