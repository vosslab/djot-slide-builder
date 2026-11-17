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
def test_foreign_namespace_does_not_collide_with_xlink(
		tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
	et = xml.etree.ElementTree
	dc = 'http://purl.org/dc/elements/1.1/'
	xlink = 'http://www.w3.org/1999/xlink'
	monkeypatch.setattr(et, '_namespace_map', et._namespace_map.copy())
	et.register_namespace('xlink', dc)
	before = et._namespace_map.copy()
	body = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:dc="{dc}" xmlns:xlink="{xlink}">'
		'<metadata><!-- license --><dc:title dc:lang="en">Plot</dc:title></metadata>'
		'<path id="mark"/><use xlink:href="#mark"/></svg>')
	output = tmp_path / 'metadata.svg'
	svg_tools.drawing.write_svg(output, 20, 20, 'Title', 'Description', body)
	assert et._namespace_map == before
	root = defusedxml.ElementTree.parse(output).getroot()
	title = root.find(f'.//{{{dc}}}title')
	assert title.text == 'Plot' and title.get(f'{{{dc}}}lang') == 'en'
	assert root.find('.//{http://www.w3.org/2000/svg}use').get(f'{{{xlink}}}href') == '#mark'
	assert '<!-- license -->' in output.read_text()


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
