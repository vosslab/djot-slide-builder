"""Static figure import preserves viewports, references, and editable text."""

import xml.etree.ElementTree as ET

import pytest

from svg_tools.parts import group
from svg_tools.drawing import write_svg
from svg_tools.svg_import import import_svg


FIGURE = '''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
 xmlns:dc="http://purl.org/dc/elements/1.1/" viewBox="10 20 40 20" fill="red">
 <!-- License: ISC --><metadata><dc:title>Figure metadata</dc:title></metadata><defs><pattern id="p" width="2" height="2">
 <path id="line" d="M0 0L2 2"/></pattern></defs><rect x="10" y="20" width="40"
 height="20" fill="url(#p)"/><use xlink:href="#line"/><text x="12" y="30">Live words</text></svg>'''


#============================================
def test_repeated_figures_preserve_geometry_and_references():
	first = import_svg(FIGURE, name='first', size=80)
	second = import_svg(FIGURE.encode(), name='second', size=80)
	root = ET.fromstring('<svg>' + group({'a': first, 'b': second}).fragment + '</svg>')
	figures = root.findall('.//{http://www.w3.org/2000/svg}svg')
	assert first.bounds == (0, 0, 80, 40)
	assert all(e.get('viewBox') == '10 20 40 20' and e.get('fill') == 'red' for e in figures)
	assert [e.text for e in root.findall('.//{http://www.w3.org/2000/svg}text')] == ['Live words'] * 2
	assert 'url(#part0-first-p)' in ET.tostring(root, encoding='unicode')
	assert '#part1-second-line' in ET.tostring(root, encoding='unicode')


#============================================
@pytest.mark.parametrize('uri,prefix', [
	('http://www.w3.org/1999/xlink', 'previous'),
	('http://www.w3.org/2000/svg', 'xlink'),
	('http://purl.org/dc/elements/1.1/', 'xlink'),
])
def test_import_preserves_namespace_registry_and_xlink(monkeypatch, tmp_path, uri, prefix):
	monkeypatch.setattr(ET, '_namespace_map', ET._namespace_map.copy())
	ET.register_namespace(prefix, uri)
	before = ET._namespace_map.copy()
	part = import_svg(FIGURE, name='figure')
	assert ET._namespace_map == before
	assert ET.fromstring(part.fragment).find('.//{http://www.w3.org/2000/svg}use').get(
		'{http://www.w3.org/1999/xlink}href') == '#figure-line'
	output = tmp_path / 'figure.svg'
	write_svg(output, 40, 20, 'Figure', 'Imported figure', part.fragment)
	assert ET._namespace_map == before
	assert 'xlink:href="#figure-line"' in output.read_text()
	assert ET.parse(output).find('.//{http://www.w3.org/2000/svg}use').get(
		'{http://www.w3.org/1999/xlink}href') == '#figure-line'
	assert ET.parse(output).find('.//{http://purl.org/dc/elements/1.1/}title').text == 'Figure metadata'
	assert '<!-- License: ISC -->' in output.read_text()


#============================================
def test_matplotlib_universal_style_is_scoped_and_preserves_override():
	svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><defs><style>*{stroke-linejoin: round; stroke-linecap: butt}</style></defs><path style="stroke-linejoin: bevel" d="M0 0L10 10"/></svg>'
	part = import_svg(svg, name='plot')
	root = ET.fromstring(part.fragment)
	path = root.find('{http://www.w3.org/2000/svg}path')
	assert path.get('style').endswith('stroke-linejoin: bevel')
	assert 'stroke-linecap: butt' in path.get('style')
	assert '<style' not in part.fragment


#============================================
@pytest.mark.parametrize('svg', [
	'<svg viewBox="0 0 1 1"><script/></svg>',
	'<svg viewBox="0 0 1 1" xml:base="https://example.com/"/>',
	'<svg viewBox="0 0 1 1"><image href="https://example.com/a.png"/></svg>',
	'<svg viewBox="0 0 1 1"><path onclick="x()"/></svg>',
	'<svg viewBox="0 0 1 1"><use href="https://example.com/#x"/></svg>',
	'<svg viewBox="0 0 1 1"><path fill="url(https://example.com/a)"/></svg>',
	'<svg viewBox="0 0 1 1"><style>path {fill:red}</style></svg>',
	'<!DOCTYPE svg [<!ENTITY a "bad">]><svg viewBox="0 0 1 1">&a;</svg>',
	'<svg viewBox="0 0 1 1"><path></svg>',
])
def test_rejects_unsafe_or_malformed(svg):
	with pytest.raises(ValueError):
		import_svg(svg, name='x')


#============================================
def test_standard_matplotlib_doctype_is_accepted():
	doctype = '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
	assert import_svg(doctype + '<svg viewBox="0 0 1 1"/>', name='x').bounds == (0, 0, 1, 1)


#============================================
def test_license_comments_survive():
	part = import_svg('<!-- License: ISC --><svg viewBox="0 0 1 1"><!-- author --></svg>', name='icon')
	assert '<!-- License: ISC -->' in part.fragment
	assert '<!-- author -->' in part.fragment


#============================================
def test_group_imports_preserves_accessibility_and_metadata():
	svg = '''<svg viewBox="0 0 10 10" aria-labelledby="title" aria-describedby="desc">
	<!-- License: id="title" --><title id="title">Title</title><desc id="desc">Description</desc>
	<defs><path id="shape" d="M0 0"/></defs><use href="#shape" data-id="title"
	style="fill:url(#shape)"/></svg>'''
	first = import_svg(svg, name='first')
	second = import_svg(svg, name='second')
	fragment = group({'a': first, 'b': second}).fragment
	parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
	root = ET.fromstring(fragment, parser=parser)
	ids = {element.get('id') for element in root.iter() if element.get('id')}
	assert len(ids) == 6
	figures = root.findall('.//svg')
	for figure in figures:
		assert set(figure.get('aria-labelledby').split()) <= ids
		assert set(figure.get('aria-describedby').split()) <= ids
		use = figure.find('use')
		assert use.get('href')[1:] in ids
		assert use.get('style').split('url(#')[1].split(')')[0] in ids
		assert use.get('data-id') == 'title'
	assert fragment.count('<!-- License: id="title" -->') == 2
	assert [element.text for element in root.iter('title')] == ['Title', 'Title']
