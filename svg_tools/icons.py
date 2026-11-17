"""Offline Font Awesome Free solid SVG icons."""

import pathlib
import re
import subprocess
import xml.sax.saxutils

import PIL.ImageColor

import svg_tools.parts
import svg_tools.svg_import


_REPO_ROOT = pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip())
_PACKAGE = _REPO_ROOT / 'node_modules/@fortawesome/fontawesome-free'


#============================================
def _icon_dir() -> pathlib.Path:
	path = _PACKAGE / 'svgs/solid'
	if not path.is_dir() or not (_PACKAGE / 'LICENSE.txt').is_file():
		raise FileNotFoundError('Font Awesome Free is missing; run npm ci in the repository root')
	return path


#============================================
def search_icons(query: str) -> list[str]:
	"""Return sorted icon names containing the case-insensitive query."""
	return sorted(path.stem for path in _icon_dir().glob('*.svg')
		if query.casefold() in path.stem.casefold())


#============================================
def icon(name: str, *, size: float, color: str) -> svg_tools.parts.SvgPart:
	"""Load a Font Awesome SVG with a Pillow-supported color name or hex color."""
	directory = _icon_dir()
	# ASVS 2.2.1/5.3.2: allow a filename only, never a path.
	if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
		raise ValueError('Invalid Font Awesome icon name')
	path = directory / (name + '.svg')
	if not path.is_file():
		raise ValueError(f'Unknown Font Awesome icon: {name}')
	if not isinstance(color, str):
		raise ValueError('Color must be a valid color name or hex color')
	color = '#' + ''.join(f'{channel:02x}' for channel in PIL.ImageColor.getrgb(color))
	markup = path.read_text(encoding='utf-8')
	markup = markup.replace('currentColor', xml.sax.saxutils.escape(color, {'"': '&quot;'}))
	return svg_tools.svg_import.import_svg(markup, name='icon-' + name, size=size)
