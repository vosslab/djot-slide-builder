"""Font-backed editable SVG labels."""

import xml.etree.ElementTree

import pytest

import svg_tools.drawing
import svg_tools.text


def test_label_escapes_and_measures_faces():
	part = svg_tools.text.label(10, 40, 'A < B & \u03b1', size=24, color='red & blue',
		role='sequence', bold=True, italic=True, anchor='start')
	node = xml.etree.ElementTree.fromstring(part.fragment)
	xml.etree.ElementTree.fromstring('<svg>' + part.fragment + '</svg>')
	assert node.text == 'A < B & \u03b1'
	assert node.attrib['fill'] == 'red & blue'
	assert node.attrib['font-family'] == 'Atkinson Hyperlegible Mono'
	assert node.attrib['font-weight'] == 'bold'
	assert node.attrib['font-style'] == 'italic'
	assert part.bounds[0] < 10 < part.bounds[2]
	assert part.bounds[1] < 40 < part.bounds[3]
	assert part.anchors['baseline'] == (10, 40)
	assert svg_tools.text.measure_text('iiii', size=24, role='normal') != svg_tools.text.measure_text(
		'iiii', size=24, role='sequence')
	spaced = svg_tools.text.label(100, 180, 'A   G', size=80, color='black',
		role='sequence', anchor='start')
	spaced_node = xml.etree.ElementTree.fromstring(spaced.fragment)
	assert spaced_node.text == 'A   G'
	assert spaced_node.get('{http://www.w3.org/XML/1998/namespace}space') == 'preserve'
	assert spaced.anchors['end'][0] > svg_tools.text.label(100, 180, 'A G', size=80,
		color='black', role='sequence', anchor='start').anchors['end'][0]


def test_anchors_validation_and_existing_font_override():
	start = svg_tools.text.measure_text('HELLO', size=20, anchor='start')
	end = svg_tools.text.measure_text('HELLO', size=20, anchor='end')
	assert end[2] < start[2]
	for size in (0, -1, float('inf'), float('nan'), 1e308):
		with pytest.raises(ValueError):
			svg_tools.text.label(0, 0, 'xxxx', size=size, color='black')
	with pytest.raises(ValueError):
		svg_tools.text.label(0, 0, 'x', size=12, color='black', role='other')
	with pytest.raises(xml.etree.ElementTree.ParseError):
		svg_tools.text.label(0, 0, '\x01', size=12, color='black')
	default = xml.etree.ElementTree.fromstring(svg_tools.drawing.text(0, 0, 'x', size=12, color='black'))
	override = xml.etree.ElementTree.fromstring(svg_tools.drawing.text(
		0, 0, 'x', size=12, color='black', font='Custom & font'))
	assert default.attrib['font-family'] == 'Atkinson Hyperlegible Next'
	assert override.attrib['font-family'] == 'Custom & font'


def test_styled_wrapping_preserves_words_styles_and_scripts():
	short = svg_tools.text.wrapped_text(0, 20, [svg_tools.text.TextRun('a b')],
		width=12, size=20, color='black')
	short_node = xml.etree.ElementTree.fromstring(short.fragment)
	assert ''.join(short_node.itertext()) == 'a b'
	assert len(list(short_node)) == 2
	assert short.bounds[2] <= 12
	runs = [svg_tools.text.TextRun('The '), svg_tools.text.TextRun('BRCA1', bold=True, italic=True),
		svg_tools.text.TextRun(' gene has H'), svg_tools.text.TextRun('2', color='blue', script='sub'),
		svg_tools.text.TextRun('O and more words.')]
	part = svg_tools.text.wrapped_text(10, 30, runs, width=130, size=20, color='black')
	node = xml.etree.ElementTree.fromstring(part.fragment)
	assert ''.join(node.itertext()) == ''.join(run.text for run in runs)
	lines = list(node)
	assert len(lines) > 1
	children = list(node.iter('tspan'))
	assert any(child.get('font-weight') == 'bold' and child.text == 'BRCA1' for child in children)
	assert any(child.get('baseline-shift') == 'sub' and child.get('fill') == 'blue' for child in children)
	assert any(child.get('baseline-shift') == 'baseline' and child.text == 'O' for child in children)
	styled = svg_tools.text.styled_label(0, 20, [svg_tools.text.TextRun('x', script='super'),
		svg_tools.text.TextRun('y')], size=20, color='black')
	styled_children = list(xml.etree.ElementTree.fromstring(styled.fragment).iter('tspan'))
	assert any(child.get('baseline-shift') == 'super' and child.text == 'x' for child in styled_children)
	assert any(child.get('baseline-shift') == 'baseline' and child.text == 'y' for child in styled_children)
	with pytest.raises(ValueError, match='width'):
		svg_tools.text.wrapped_text(0, 20, [svg_tools.text.TextRun('unbreakable')],
			width=1, size=20, color='black')
	with pytest.raises(ValueError, match='height'):
		svg_tools.text.wrapped_text(0, 20, runs, width=130, height=1, size=20, color='black')
	for value in ('\n\nA', 'A\n\n', '\n\n'):
		with pytest.raises(ValueError, match='height'):
			svg_tools.text.wrapped_text(0, 20, [svg_tools.text.TextRun(value)],
				width=130, height=40, line_height=20, size=20, color='black')
		svg_tools.text.wrapped_text(0, 20, [svg_tools.text.TextRun(value)],
			width=130, height=65, line_height=20, size=20, color='black')
