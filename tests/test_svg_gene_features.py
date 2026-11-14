"""Behavior checks for explicit directional gene-track parts."""

import xml.etree.ElementTree as ET

import pytest

from svg_tools.chromosomes import Segment
from svg_tools.gene_tracks import gene_feature_part, gene_track_part, gene_track_svg, landmark_part, operon_part


def test_orientation_and_authored_order():
	forward = gene_feature_part('A', 100, 'forward', color='#a9d5df')
	reverse = gene_feature_part('B', 80, 'reverse', color='#b8d8b3')
	assert forward.anchors['tip'] == (100, 20)
	assert reverse.anchors['tip'] == (0, 20)
	assert ET.fromstring(forward.fragment).find('polygon').attrib['points'].split()[2] == '100,20.0'
	assert ET.fromstring(reverse.fragment).find('polygon').attrib['points'].split()[2] == '0,20.0'
	part = operon_part({'later': (forward, 200), 'earlier': (reverse, 20)}, length=320)
	assert part.anchors['earlier.tip'] == (20, 0)
	assert part.anchors['later.tip'] == (300, 0)
	assert part.anchors['end'] == (320, 0)
	assert part.bounds[1] < -20
	with pytest.raises(ValueError):
		gene_feature_part('A', 10, 'sideways', color='#a9d5df')


def test_landmark_direction_and_labels():
	for kind in ('promoter', 'operator', 'terminator'):
		part = landmark_part(kind, kind.title(), direction='forward')
		assert ET.fromstring(part.fragment).find('text').text == kind.title()
		assert part.anchors['landmark'] == (20, 20)
	forward = landmark_part('promoter', 'P', direction='forward')
	reverse = landmark_part('promoter', 'P', direction='reverse')
	assert ET.fromstring(forward.fragment).find('g/path').attrib['d'] != ET.fromstring(reverse.fragment).find('g/path').attrib['d']


def test_existing_track_gap_and_width_contract():
	exons = [Segment('A', '#a9d5df', 30), Segment('B', '#b8d8b3', 50), Segment('C', '#f2d28d', 20)]
	fragment, width, boundaries = gene_track_svg('g', exons, [10, 25])
	assert width == 135
	assert boundaries == [0, 40, 115, 135]
	assert len(ET.fromstring(fragment).findall('line')) == 2
	joined = gene_track_part('joined', exons, [0, 0])
	assert joined.anchors['end'] == (100, 25)
	assert not ET.fromstring(joined.fragment).findall('line')
	assert [float(x.attrib['width']) for x in ET.fromstring(joined.fragment).iter('rect')] == [30, 50, 20]
