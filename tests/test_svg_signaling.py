"""Activity and phosphorylation are independent schematic annotations."""

from svg_tools import parts, signaling


def test_activity_and_phosphate_are_independent() -> None:
	active = signaling.protein(width=100, height=80, color='#e5d7ef', activity='active')
	inactive = signaling.protein(width=100, height=80, color='#e5d7ef', activity='inactive')
	phosphorylated = signaling.phosphate(inactive, site_label='site A')
	assert 'active' in active.fragment and '>P<' not in active.fragment
	assert 'inactive' in phosphorylated.fragment and '>P<' in phosphorylated.fragment
	assert 'site A' in phosphorylated.fragment
	assert '>P<' in signaling.phosphate(active).fragment
	assert '>P<' not in inactive.fragment
	assert active.anchors['modification'] == inactive.anchors['modification']
	assert phosphorylated.anchors['phosphate'] == inactive.anchors['modification']
	assert phosphorylated.bounds[2] > inactive.bounds[2]
	moved = parts.transform(phosphorylated, x=30, y=40)
	assert moved.anchors['phosphate'] == (phosphorylated.anchors['phosphate'][0] + 30,
		phosphorylated.anchors['phosphate'][1] + 40)
