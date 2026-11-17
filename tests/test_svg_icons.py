"""Font Awesome icons retain their vector geometry, color, and attribution."""

import math
import pathlib

import defusedxml.ElementTree

import pytest

from svg_tools.drawing import write_svg
from svg_tools.icons import icon, search_icons
from svg_tools.parts import group


SVG = '{http://www.w3.org/2000/svg}'


def test_search_and_real_icon_geometry() -> None:
	assert 'microscope' in search_icons('MICRO')
	assert 'dna' in search_icons('dna')
	assert 'diagram-project' in search_icons('diagram')
	part = icon('microscope', size=48, color='#123456')
	root = defusedxml.ElementTree.fromstring(part.fragment)
	assert root.findall(SVG + 'path')
	assert '#123456' in part.fragment
	assert 'currentColor' not in part.fragment


def test_export_keeps_vector_and_attribution(tmp_path: pathlib.Path) -> None:
	part = icon('vial', size=24, color='red')
	path = tmp_path / 'icon.svg'
	write_svg(path, 24, 24, 'Vial', 'Vial icon', group({'vial': part}).fragment)
	root = defusedxml.ElementTree.parse(path).getroot()
	assert root.findall('.//' + SVG + 'path')
	assert 'Font Awesome Free' in path.read_text(encoding='utf-8')


@pytest.mark.parametrize('name', ['missing-icon-name', '../search', ''])
def test_invalid_name(name: str) -> None:
	with pytest.raises(ValueError):
		icon(name, size=24, color='black')


@pytest.mark.parametrize('size', [0, -1, math.inf])
def test_invalid_size(size: float) -> None:
	with pytest.raises(ValueError):
		icon('dna', size=size, color='black')


@pytest.mark.parametrize('color', ['', 'not-a-color', None])
def test_invalid_color(color: str | None) -> None:
	with pytest.raises(ValueError):
		icon('dna', size=24, color=color)


def test_missing_dependency(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
	import svg_tools.icons as icons
	monkeypatch.setattr(icons, '_PACKAGE', tmp_path)
	with pytest.raises(FileNotFoundError, match='npm ci'):
		search_icons('dna')


def test_non_square_viewport_keeps_aspect(
		monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
	import svg_tools.icons as icons
	icon_dir = tmp_path / 'svgs/solid'
	icon_dir.mkdir(parents=True)
	(tmp_path / 'LICENSE.txt').write_text('License')
	(icon_dir / 'wide.svg').write_text(
		'<svg viewBox="0 0 20 10"><!-- Font Awesome Free --><path fill="currentColor" d="M0 0L20 10"/></svg>')
	monkeypatch.setattr(icons, '_PACKAGE', tmp_path)
	assert icon('wide', size=40, color='blue').bounds == (0, 0, 40, 20)
