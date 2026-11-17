"""Behavior checks for explicit directional gene-track parts."""

import pytest

from svg_tools.gene_tracks import gene_feature_part, operon_part


#============================================
def test_orientation_and_authored_order() -> None:
	forward = gene_feature_part('A', 100, 'forward', color='#a9d5df')
	reverse = gene_feature_part('B', 80, 'reverse', color='#b8d8b3')
	assert forward.anchors['tip'] == (100, 20)
	assert reverse.anchors['tip'] == (0, 20)
	part = operon_part({'later': (forward, 200), 'earlier': (reverse, 20)}, length=320)
	assert part.anchors['earlier.tip'] == (20, 0)
	assert part.anchors['later.tip'] == (300, 0)
	assert part.anchors['end'] == (320, 0)
	assert part.bounds[1] < -20
	with pytest.raises(ValueError):
		gene_feature_part('A', 10, 'sideways', color='#a9d5df')


