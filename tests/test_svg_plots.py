"""Behavior checks for vector plot import and scoped styling."""

import xml.etree.ElementTree as ET

import matplotlib
import pytest
from matplotlib.figure import Figure

from svg_tools.plots import figure_to_part, plot_style


def test_plot_import_preserves_data_and_live_labels():
	before = matplotlib.rcParams['font.family'][:]
	values = [2, 5, 3]
	with plot_style():
		figure = Figure()
		axes = figure.subplots()
		line, = axes.plot([1, 2, 3], values)
		title = axes.set_title('Measured response', fontweight='bold', fontstyle='italic')
		axes.set_xlabel('Dose')
		original = title.get_fontproperties().copy()
		part = figure_to_part(figure, name='response', size=300)
		assert title.get_fontproperties() == original
	assert matplotlib.rcParams['font.family'] == before
	assert list(line.get_ydata()) == values == [2, 5, 3]
	root = ET.fromstring(part.fragment)
	texts = list(root.iter('{http://www.w3.org/2000/svg}text'))
	assert any('Measured response' == text.text for text in texts)
	assert any('Dose' == text.text for text in texts)
	assert all('Atkinson Hyperlegible Next' in text.get('style', '') for text in texts)
	assert part.bounds[2] == 300


def test_plot_import_rejects_raster_artists():
	with plot_style():
		figure = Figure()
		figure.subplots().imshow([[1, 2], [3, 4]])
		with pytest.raises(ValueError, match='Unsupported SVG element: image'):
			figure_to_part(figure, name='raster')


def test_default_plot_exports_deterministically_and_restores_fonts(monkeypatch):
	monkeypatch.delenv('SOURCE_DATE_EPOCH', raising=False)
	figure = Figure()
	axes = figure.subplots()
	axes.plot([1, 2], [3, 4])
	title = axes.set_title('Default title', fontweight='bold', fontstyle='italic')
	original = title.get_fontproperties().copy()
	with matplotlib.rc_context({'svg.hashsalt': None, 'svg.fonttype': 'path'}):
		first = figure_to_part(figure, name='default')
		second = figure_to_part(figure, name='default')
	assert first.fragment == second.fragment
	assert title.get_fontproperties() == original
	root = ET.fromstring(first.fragment)
	texts = list(root.iter('{http://www.w3.org/2000/svg}text'))
	assert texts and all('Atkinson Hyperlegible Next' in text.get('style', '') for text in texts)
	title_style = next(text.get('style', '') for text in texts if text.text == 'Default title')
	assert 'font-weight: 700' in title_style and 'font-style: italic' in title_style
	assert any(element.get('id') for element in root.iter())
