"""Import caller-owned Matplotlib figures as editable vector SVG parts."""

import contextlib
import io
import pathlib
import collections.abc

import matplotlib
import matplotlib.figure
import matplotlib.text

import slide_lib.presentation_theme
import svg_tools.parts
import svg_tools.svg_import


#============================================
@contextlib.contextmanager
def plot_style(course: str = 'genetics') -> collections.abc.Iterator[None]:
	"""Apply course colors and editable labels while constructing a plot."""
	color = '#' + slide_lib.presentation_theme.course_color_theme(course).accent_color
	with matplotlib.rc_context({'svg.fonttype': 'none',
		'font.family': 'Atkinson Hyperlegible Next', 'axes.prop_cycle': matplotlib.cycler(color=[color])}):
		yield


#============================================
def figure_to_part(figure: matplotlib.figure.Figure, *, name: str, size: float | None = None) -> svg_tools.parts.SvgPart:
	"""Convert a figure to a vector part without closing or changing its data.

	Raster artists are rejected by the SVG importer. The caller owns the figure.
	"""
	font_dir = pathlib.Path(__file__).resolve().parent.parent / 'assets/fonts/atkinson_hyperlegible_next'
	original = []
	try:
		for text in figure.findobj(match=matplotlib.text.Text):
			properties = text.get_fontproperties()
			face = ('Bold' if properties.get_weight() in ('bold', 'heavy', 'semibold', 'demibold', 'black', 600, 700, 800, 900) else '')
			face += 'Italic' if properties.get_style() in ('italic', 'oblique') else ''
			face = face or 'Regular'
			original.append((text, properties))
			properties = properties.copy()
			properties.set_family('Atkinson Hyperlegible Next')
			properties.set_file(font_dir / f'AtkinsonHyperlegibleNext-{face}.ttf')
			text.set_fontproperties(properties)
		with matplotlib.rc_context({'svg.fonttype': 'none', 'svg.hashsalt': 'djot_slide_builder'}):
			output = io.BytesIO()
			figure.savefig(output, format='svg', metadata={'Date': None})
		return svg_tools.svg_import.import_svg(output.getvalue(), name=name, size=size)
	finally:
		for text, properties in original:
			text.set_fontproperties(properties)
