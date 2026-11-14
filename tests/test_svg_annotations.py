"""Behavior checks for reusable workflow annotations."""

import xml.etree.ElementTree

import pytest

import svg_tools.annotations as annotations
import svg_tools.text


def test_boxes_preserve_words_and_reject_overflow():
	part = annotations.box('Signal received', 130, 70, '#dceef4')
	root = xml.etree.ElementTree.fromstring(part.fragment)
	assert ''.join(root.itertext()).strip() == 'Signal received'
	assert part.anchors['right'] == (65, 0)
	diamond = annotations.box('Signal strong?', 170, 116, '#fff', shape='decision', font_size=15)
	assert diamond.anchors['top'] == (0, -58)
	with pytest.raises(ValueError, match='overflow'):
		annotations.box('unbreakablelongword', 30, 30, '#fff')


def test_box_styled_gene_and_upright_status():
	runs = [svg_tools.text.TextRun('Sxl', italic=True), svg_tools.text.TextRun('\nON')]
	part = annotations.box(runs, 95, 50, '#fff', font_size=17)
	root = xml.etree.ElementTree.fromstring(part.fragment)
	text = root.find('.//text')
	spans = [element for element in text.iter('tspan') if element.text]
	assert [(span.text, span.get('font-style')) for span in spans] == [
		('Sxl', 'italic'), ('ON', 'normal')]
	assert part.bounds == (-48.5, -26, 48.5, 26)
	assert annotations.box('Sxl\nON', 95, 50, '#fff', font_size=17).fragment == annotations.box(
		[svg_tools.text.TextRun('Sxl\nON')], 95, 50, '#fff', font_size=17).fragment


def test_connector_head_orientation_and_bounds():
	part = annotations.connector([(0, 0), (0, 20), (0, 20)], head_size=10)
	root = xml.etree.ElementTree.fromstring(part.fragment)
	assert root[-1].attrib['points'] == '-5.0,10.0 0,20 5.0,10.0'
	assert part.bounds == (-6, -1, 6, 21)
	bar = annotations.connector([(0, 0), (20, 0)], kind='inhibition', head_size=10)
	assert bar.bounds == (-1, -6, 21, 6)


def test_connector_semantics():
	for kind in ('binding', 'bracket', 'callout', 'indirect'):
		part = annotations.connector([(0, 0), (10, 0)], kind=kind)
		root = xml.etree.ElementTree.fromstring(part.fragment)
		assert len(root) == 1
		assert ('stroke-dasharray' in root[0].attrib) == (kind == 'indirect')
	with pytest.raises(ValueError):
		annotations.connector([(0, 0), (0, 0)])
