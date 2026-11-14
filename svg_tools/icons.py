"""Offline icons from lucide-static >=1.72.0 (https://lucide.dev, ISC/Feather MIT).

The installed package's full license travels as nonvisual SVG metadata.
"""

import math
import pathlib
import re
import xml.sax.saxutils

import PIL.ImageColor

import svg_tools.parts
import svg_tools.svg_import


_PACKAGE = pathlib.Path(__file__).resolve().parent.parent / 'node_modules/lucide-static'


#============================================
def _icon_dir() -> pathlib.Path:
	path = _PACKAGE / 'icons'
	if not path.is_dir() or not (_PACKAGE / 'LICENSE').is_file():
		raise FileNotFoundError('lucide-static is missing; run npm ci in the repository root')
	return path


#============================================
def search_icons(query: str) -> list[str]:
	"""Return sorted icon names containing the case-insensitive query."""
	return sorted(path.stem for path in _icon_dir().glob('*.svg')
		if query.casefold() in path.stem.casefold())


#============================================
def icon(name: str, *, size: float, color: str, stroke_width: float = 2) -> svg_tools.parts.SvgPart:
	"""Load an editable icon with a Pillow-supported color name or hex color."""
	directory = _icon_dir()
	if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
		raise ValueError('Invalid Lucide icon name')
	path = directory / (name + '.svg')
	if not path.is_file():
		raise ValueError(f'Unknown Lucide icon: {name}')
	if not isinstance(stroke_width, (int, float)) or not math.isfinite(stroke_width) or stroke_width < 0:
		raise ValueError('Stroke width must be finite and nonnegative')
	if not isinstance(color, str):
		raise ValueError('Color must be a valid color name or hex color')
	color = '#' + ''.join(f'{channel:02x}' for channel in PIL.ImageColor.getrgb(color))
	markup = path.read_text(encoding='utf-8')
	markup = markup.replace('currentColor', xml.sax.saxutils.escape(color, {'"': '&quot;'}))
	markup = re.sub(r'stroke-width="[^"]*"', f'stroke-width="{stroke_width}"', markup)
	license_text = (_PACKAGE / 'LICENSE').read_text(encoding='utf-8')
	markup = re.sub(r'(<svg\b[^>]*>)', lambda match: match.group(1) +
		'<metadata>' + xml.sax.saxutils.escape(license_text) + '</metadata>', markup, count=1)
	return svg_tools.svg_import.import_svg(markup, name='icon-' + name, size=size)
