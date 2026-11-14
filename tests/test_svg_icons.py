"""Lucide icons remain editable SVGs with explicit styling and attribution."""

import math
import xml.etree.ElementTree as ET

import pytest

from svg_tools.drawing import write_svg
from svg_tools.icons import icon, search_icons
from svg_tools.parts import group


SVG = '{http://www.w3.org/2000/svg}'


def test_search_and_real_icon_geometry():
	assert 'microscope' in search_icons('MICRO')
	assert 'dna' in search_icons('dna')
	assert 'workflow' in search_icons('workflow')
	part = icon('microscope', size=48, color='#123456', stroke_width=3)
	root = ET.fromstring(part.fragment)
	assert part.bounds == (0, 0, 48, 48)
	assert root.get('viewBox') == '0 0 24 24'
	assert root.get('stroke') == '#123456'
	assert root.get('stroke-width') == '3'
	assert root.findall(SVG + 'path')
	assert 'currentColor' not in part.fragment


def test_export_keeps_vector_and_license(tmp_path):
	part = icon('search', size=24, color='red')
	path = tmp_path / 'icon.svg'
	write_svg(path, 24, 24, 'Search', 'Search icon', group({'search': part}).fragment)
	root = ET.parse(path).getroot()
	assert root.findall('.//' + SVG + 'circle')
	license_text = root.find('.//' + SVG + 'metadata').text
	assert 'Lucide Icons and Contributors' in license_text
	assert 'Copyright (c) 2013-present Cole Bemis' in license_text
	assert 'Permission is hereby granted' in license_text


@pytest.mark.parametrize('name', ['missing-icon-name', '../search', ''])
def test_invalid_name(name):
	with pytest.raises(ValueError):
		icon(name, size=24, color='black')


@pytest.mark.parametrize('size', [0, -1, math.inf])
def test_invalid_size(size):
	with pytest.raises(ValueError):
		icon('dna', size=size, color='black')


@pytest.mark.parametrize('color', ['', 'not-a-color', None])
def test_invalid_color(color):
	with pytest.raises(ValueError):
		icon('dna', size=24, color=color)


def test_missing_dependency(monkeypatch, tmp_path):
	import svg_tools.icons as icons
	monkeypatch.setattr(icons, '_PACKAGE', tmp_path)
	with pytest.raises(FileNotFoundError, match='npm ci'):
		search_icons('dna')


def test_non_square_viewport_keeps_aspect(monkeypatch, tmp_path):
	import svg_tools.icons as icons
	(tmp_path / 'icons').mkdir()
	(tmp_path / 'LICENSE').write_text('License')
	(tmp_path / 'icons' / 'wide.svg').write_text(
		'<svg viewBox="0 0 20 10" stroke="currentColor" stroke-width="2"><path d="M0 0L20 10"/></svg>')
	monkeypatch.setattr(icons, '_PACKAGE', tmp_path)
	assert icon('wide', size=40, color='blue').bounds == (0, 0, 40, 20)
