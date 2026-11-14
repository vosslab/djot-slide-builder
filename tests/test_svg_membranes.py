"""Behavior of membrane leaflets and receptor gaps."""

import pytest

import svg_tools.signaling


def test_membrane_bounds_and_anchors_with_gap():
	part = svg_tools.signaling.membrane('M 0 0 L 40 0', spacing=10,
		thickness=20, color='#b9e3ea', gaps=((15, 25),))
	assert part.anchors == {'start': (0, 0), 'end': (40, 0), 'center': (20, 0),
		'extracellular': (20, -10), 'cytoplasmic': (20, 10)}
	assert part.bounds[0] < -10 and part.bounds[1] < -10
	assert part.bounds[2] > 50 and part.bounds[3] > 10


def test_curved_membrane_and_invalid_gap():
	part = svg_tools.signaling.membrane('M 0 0 Q 50 50 100 0', spacing=10,
		thickness=20, color='#b9e3ea')
	assert part.anchors['center'] == pytest.approx((50, 25))
	assert part.anchors['extracellular'] == pytest.approx((50, 15))
	with pytest.raises(ValueError):
		svg_tools.signaling.membrane('M 0 0 L 40 0', spacing=10,
			thickness=20, color='#b9e3ea', gaps=((0, 41),))
