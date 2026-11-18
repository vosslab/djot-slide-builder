"""Protect editable scientific labels and existing drawings on invalid input."""

import pathlib

import lxml.etree
import pytest

import svg_tools.drawing


#============================================
def test_namespaced_import_serializes_for_libreoffice(tmp_path: pathlib.Path) -> None:
	"""Normalize source prefixes so SVG elements and xlink references render in LibreOffice."""
	svg = "http://www.w3.org/2000/svg"
	xlink = "http://www.w3.org/1999/xlink"
	body = (f'<other:svg xmlns:other="{svg}" xmlns:custom="{xlink}">'
		'<other:defs><other:clipPath id="clip"><other:rect width="10" height="10"/></other:clipPath>'
		'<other:path id="mark" d="M0 0L1 1"/></other:defs>'
		'<other:g clip-path="url(#clip)"><other:use custom:href="#mark"/>'
		'<other:text x="2">Live label</other:text></other:g></other:svg>')
	output = tmp_path / "import.svg"
	svg_tools.drawing.write_svg(output, 20, 20, "Title", "Description", body)
	payload = output.read_bytes()
	root = lxml.etree.fromstring(payload)
	assert b'<svg xmlns=' in payload and b'<use xlink:href="#mark"' in payload
	assert b'other:' not in payload and b'custom:' not in payload
	group = root.find(f'.//{{{svg}}}g')
	assert group.get('clip-path') == 'url(#clip)'
	assert group.find(f'{{{svg}}}use').get(f'{{{xlink}}}href') == '#mark'
	assert group.find(f'{{{svg}}}text').text == 'Live label'
	assert root.find(f'.//{{{svg}}}clipPath/{{{svg}}}rect').get('width') == '10'


#============================================
def test_foreign_namespace_does_not_collide_with_xlink(tmp_path: pathlib.Path) -> None:
	dc = 'http://purl.org/dc/elements/1.1/'
	xlink = 'http://www.w3.org/1999/xlink'
	body = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="{dc}" xmlns:link="{xlink}">'
		'<metadata><!-- license --><xlink:title xlink:lang="en">Plot</xlink:title></metadata>'
		'<path id="mark"/><use link:href="#mark" xlink:href="metadata"/></svg>')
	output = tmp_path / 'metadata.svg'
	svg_tools.drawing.write_svg(output, 20, 20, 'Title', 'Description', body)
	root = lxml.etree.parse(output).getroot()
	title = root.find(f'.//{{{dc}}}title')
	assert title.text == 'Plot' and title.get(f'{{{dc}}}lang') == 'en'
	use = root.find('.//{http://www.w3.org/2000/svg}use')
	assert use.get(f'{{{xlink}}}href') == '#mark' and use.get(f'{{{dc}}}href') == 'metadata'
	assert '<!-- license -->' in output.read_text()


#============================================
def test_write_svg_removes_only_full_canvas_white_backgrounds(tmp_path: pathlib.Path) -> None:
	"""Keep white cells and definitions while clearing inherited viewport backgrounds."""
	output = tmp_path / "transparent.svg"
	body = (
		'<rect width="100" height="80" fill="white"/>'
		'<rect x="4" y="5" width="20" height="12" rx="3" fill="white"/>'
		'<defs><clipPath id="cell-clip"><rect width="20" height="12"/></clipPath>'
		'<mask id="opaque"><svg viewBox="0 0 20 10">'
		'<rect width="100%" height="100%" fill="white"/></svg></mask></defs>'
		'<svg viewBox="0 0 20 10"><rect width="100%" height="100%" fill="#fff"/>'
		'<rect x="2" y="2" width="8" height="4" rx="2" fill="white"/></svg>')
	svg_tools.drawing.write_svg(output, 100, 80, "Title", "Description", body)
	root = lxml.etree.parse(output).getroot()
	ns = {"s": "http://www.w3.org/2000/svg"}
	direct_rectangles = root.findall("s:rect", ns)
	assert len(direct_rectangles) == 1
	assert direct_rectangles[0].get("rx") == "3"
	assert root.find("s:defs/s:clipPath/s:rect", ns) is not None
	assert root.find("s:defs/s:mask/s:svg/s:rect", ns) is not None
	nested = root.find("s:svg", ns)
	assert nested is not None
	assert len(nested.findall("s:rect", ns)) == 1
	assert nested.find("s:rect", ns).get("rx") == "2"


#============================================
def test_scientific_labels_survive_and_invalid_xml_preserves_file(tmp_path: pathlib.Path) -> None:
	"""Fix serialization if labels change or malformed XML overwrites a usable drawing."""
	output = tmp_path / "labels.drawn.svg"
	label = "5\u2032 CH\u2082 \u03b1 & <allele>"
	body = '<g id="labels">' + svg_tools.drawing.text(
		10, 20, label, size=16, color="#123456", font='A "quoted" & font') + '</g>'
	svg_tools.drawing.write_svg(output, 300, 80, "A & B", label, body)
	payload = output.read_bytes()
	root = lxml.etree.fromstring(payload)
	ns = {"s": "http://www.w3.org/2000/svg"}
	assert payload.isascii()
	assert root.find("s:g/s:text", ns).text == label
	assert root.find("s:g/s:text", ns).get("font-family") == 'A "quoted" & font'
	assert root.find("s:title", ns).text == "A & B"
	assert root.find("s:desc", ns).text == label
	with pytest.raises(lxml.etree.XMLSyntaxError):
		svg_tools.drawing.write_svg(output, 300, 80, "Broken", "", "<g>")
	with pytest.raises(ValueError):
		svg_tools.drawing.write_svg(output, 300, 80, "\x01", "", body)
	assert output.read_bytes() == payload
