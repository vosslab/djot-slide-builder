"""Activity and phosphorylation are independent schematic annotations."""

import xml.etree.ElementTree as ET

import pytest

from svg_tools import parts, signaling


def test_activity_and_phosphate_are_independent():
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
	assert 'Atkinson Hyperlegible Next' in phosphorylated.fragment
	assert ET.fromstring('<g>' + active.fragment + '</g>').find('.//circle').get('fill') != \
		ET.fromstring('<g>' + inactive.fragment + '</g>').find('.//circle').get('fill')
	moved = parts.transform(phosphorylated, x=30, y=40)
	assert moved.anchors['phosphate'] == (phosphorylated.anchors['phosphate'][0] + 30,
		phosphorylated.anchors['phosphate'][1] + 40)


def test_default_and_invalid_annotations():
	plain = signaling.protein(width=100, height=80, color='blue')
	assert 'activity_label' not in plain.anchors
	with pytest.raises(ValueError):
		signaling.protein(width=100, height=80, color='blue', activity='unknown')
	with pytest.raises(ValueError):
		signaling.phosphate(plain, site='missing')
	with pytest.raises(ValueError):
		signaling.phosphate(plain, site_label=' ')
	with pytest.raises(ValueError):
		signaling.phosphate(plain, radius=0)
