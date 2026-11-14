"""Protect editable scientific labels and existing drawings on invalid input."""

import pathlib
import xml.etree.ElementTree
import defusedxml.ElementTree

import pytest

import svg_tools.drawing


#============================================
def test_namespaced_import_serializes_for_libreoffice(tmp_path: pathlib.Path) -> None:
	"""Keep SVG elements and xlink references usable regardless of global registrations."""
	et = xml.etree.ElementTree
	svg = "http://www.w3.org/2000/svg"
	xlink = "http://www.w3.org/1999/xlink"
	body = (f'<svg xmlns="{svg}" xmlns:xlink="{xlink}">'
		'<defs><clipPath id="clip"><rect width="10" height="10"/></clipPath>'
		'<path id="mark" d="M0 0L1 1"/></defs>'
		'<g clip-path="url(#clip)"><use xlink:href="#mark"/>'
		'<text x="2">Live label</text></g></svg>')
	registry = et._namespace_map.copy()
	try:
		et.register_namespace("svg", "urn:other-svg")
		et.register_namespace("other", svg)
		et.register_namespace("custom", xlink)
		output = tmp_path / "import.svg"
		svg_tools.drawing.write_svg(output, 20, 20, "Title", "Description", body)
	finally:
		et._namespace_map.clear()
		et._namespace_map.update(registry)
	payload = output.read_bytes()
	root = defusedxml.ElementTree.fromstring(payload)
	assert b'<svg xmlns=' in payload and b'<use xlink:href="#mark"' in payload
	assert b'other:' not in payload and b'custom:' not in payload
	group = root.find(f'.//{{{svg}}}g')
	assert group.get('clip-path') == 'url(#clip)'
	assert group.find(f'{{{svg}}}use').get(f'{{{xlink}}}href') == '#mark'
	assert group.find(f'{{{svg}}}text').text == 'Live label'
	assert root.find(f'.//{{{svg}}}clipPath/{{{svg}}}rect').get('width') == '10'


#============================================
def test_scientific_labels_survive_and_invalid_xml_preserves_file(tmp_path: pathlib.Path) -> None:
	"""Fix serialization if labels change or malformed XML overwrites a usable drawing."""
	output = tmp_path / "labels.drawn.svg"
	label = "5\u2032 CH\u2082 \u03b1 & <allele>"
	body = '<g id="labels">' + svg_tools.drawing.text(
		10, 20, label, size=16, color="#123456", font='A "quoted" & font') + '</g>'
	svg_tools.drawing.write_svg(output, 300, 80, "A & B", label, body)
	payload = output.read_bytes()
	root = defusedxml.ElementTree.fromstring(payload)
	ns = {"s": "http://www.w3.org/2000/svg"}
	assert payload.isascii()
	assert root.find("s:g/s:text", ns).text == label
	assert root.find("s:g/s:text", ns).get("font-family") == 'A "quoted" & font'
	assert root.find("s:title", ns).text == "A & B"
	assert root.find("s:desc", ns).text == label
	with pytest.raises(xml.etree.ElementTree.ParseError):
		svg_tools.drawing.write_svg(output, 300, 80, "Broken", "", "<g>")
	assert output.read_bytes() == payload


#============================================
def test_constructed_solids_share_projection_and_escape_attributes() -> None:
	"""Repair shared geometry if faces separate or a cap drifts off its apparatus axis."""
	colors = ("#eeeeee", "#aaaaaa", "#666666")
	box_fragment = svg_tools.drawing.cuboid(
		'box&"one', 10, 20, 30, 100, 80, 60, colors=colors, stroke="#123456")
	box = defusedxml.ElementTree.fromstring("<svg>" + box_fragment + "</svg>")[0]
	front, right, top = [face.get("points").split() for face in box]
	assert box.get("id") == 'box&"one'
	assert front[1:3] == [right[0], right[3]]
	assert top[:2] == [front[3], front[2]]
	assert top[1:3] == [right[3], right[2]]
	assert svg_tools.drawing.project(0, 100, 0) == (46, -36)
	for top_radius in (None, 8):
		tube_fragment = svg_tools.drawing.cylinder(
			'tube&"one', 10, 20, 30, 5, 60, colors=colors, stroke="#123456",
			top_radius=top_radius)
		tube = defusedxml.ElementTree.fromstring("<svg>" + tube_fragment + "</svg>")[0]
		cap = tube.find("circle")
		cx, cy = svg_tools.drawing.project(10, 20, 90)
		assert tube.get("id") == 'tube&"one'
		assert cap.get("transform") == f"matrix(1 0 .46 -.36 {cx} {cy})"
		assert float(cap.get("r")) == (5 if top_radius is None else top_radius)
	with pytest.raises(ValueError, match="positive"):
		svg_tools.drawing.cuboid("flat", 0, 0, 0, 10, 10, 0, colors=colors, stroke="none")
	with pytest.raises(ValueError, match="positive"):
		svg_tools.drawing.cylinder(
			"bad", 0, 0, 0, float("nan"), 20, colors=colors, stroke="none")
