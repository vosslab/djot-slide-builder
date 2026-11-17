"""Behavior checks for vector plot import and scoped styling."""

import defusedxml.ElementTree
import matplotlib
import pytest
from matplotlib.figure import Figure

from svg_tools.plots import figure_to_part, plot_style


#============================================
def test_plot_import_preserves_data_and_live_labels() -> None:
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
	root = defusedxml.ElementTree.fromstring(part.fragment)
	texts = list(root.iter('{http://www.w3.org/2000/svg}text'))
	assert any('Measured response' == text.text for text in texts)
	assert any('Dose' == text.text for text in texts)
	assert all('Atkinson Hyperlegible Next' in text.get('style', '') for text in texts)
	backing_patches = [
		path
		for group in root.iter('{http://www.w3.org/2000/svg}g')
		if group.get('id', '').endswith(('-patch_1', '-patch_2'))
		for path in group.findall('{http://www.w3.org/2000/svg}path')
	]
	assert len(backing_patches) == 2
	assert all('fill: none' in path.get('style', '') for path in backing_patches)
	assert '#ffffff' not in part.fragment.lower()
	assert part.bounds[2] == 300


#============================================
def test_plot_import_rejects_raster_artists() -> None:
	with plot_style():
		figure = Figure()
		figure.subplots().imshow([[1, 2], [3, 4]])
		with pytest.raises(ValueError, match='Unsupported SVG element: image'):
			figure_to_part(figure, name='raster')


