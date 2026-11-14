"""Placement preserves geometry and local references."""

import xml.etree.ElementTree

import pytest

import svg_tools.chromosomes
import svg_tools.parts


def test_transform_and_layout() -> None:
	part = svg_tools.parts.SvgPart('<rect/>', (0, 0, 10, 20), {'tip': (10, 0)})
	placed = svg_tools.parts.transform(part, x=30, y=5, rotation=90, scale=2)
	assert placed.bounds == pytest.approx((-10, 5, 30, 25))
	assert placed.anchors['tip'] == pytest.approx((30, 25))
	assert 'matrix(' in placed.fragment
	aligned = svg_tools.parts.align([part, placed], 'top', 7)
	assert [p.bounds[1] for p in aligned] == pytest.approx([7, 7])
	spaced = svg_tools.parts.distribute(aligned, 'x', 4)
	assert spaced[1].bounds[0] - spaced[0].bounds[2] == pytest.approx(4)
	combined = svg_tools.parts.group({'first': spaced[0], 'second': spaced[1]})
	assert combined.anchors['second.tip'] == pytest.approx(spaced[1].anchors['tip'])
	assert combined.bounds[2] == pytest.approx(spaced[1].bounds[2])
	assert part.bounds == (0, 0, 10, 20)


def test_group_repeated_chromosome_ids_and_references() -> None:
	segment = svg_tools.chromosomes.Segment('A', '#FFFFFF', 40)
	model = svg_tools.chromosomes.Chromosome((segment, segment), 1)
	part = svg_tools.chromosomes.chromosome_part('chrom', model, orientation='vertical')
	combined = svg_tools.parts.group({'one': part, 'two': svg_tools.parts.transform(part, x=80)})
	root = xml.etree.ElementTree.fromstring(combined.fragment)
	ids = [el.attrib['id'] for el in root.iter() if 'id' in el.attrib]
	assert len(ids) == len(set(ids))
	clips = [el.attrib['clip-path'][5:-1] for el in root.iter() if 'clip-path' in el.attrib]
	assert len(clips) == 2 and all(value in ids for value in clips)
	assert combined.anchors['two.centromere'][0] == pytest.approx(part.anchors['centromere'][0] + 80)


def test_namespaced_href_and_input_validation() -> None:
	fragment = '<g><path id="a"/><use href="#a"/><path fill="url(#a)"/></g>'
	result = svg_tools.parts.namespace_ids(fragment, 'copy')
	assert 'href="#copy-a"' in result and 'url(#copy-a)' in result
	with pytest.raises(ValueError):
		svg_tools.parts.transform(svg_tools.parts.SvgPart('', (0, 0, 1, 1), {}), scale=0)
	with pytest.raises(ValueError):
		svg_tools.parts.group({'bad.name': svg_tools.parts.SvgPart('', (0, 0, 1, 1), {})})
