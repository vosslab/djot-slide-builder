"""Editable SVG labels measured with the bundled Atkinson font faces."""

import dataclasses
import math
import re
import pathlib
import xml.etree.ElementTree

import defusedxml.ElementTree
import PIL.ImageFont

import svg_tools.parts


#============================================
def _font(role: str, bold: bool, italic: bool) -> tuple[pathlib.Path, PIL.ImageFont.FreeTypeFont]:
	if role not in ('normal', 'sequence'):
		raise ValueError('Role must be normal or sequence')
	family = 'Next' if role == 'normal' else 'Mono'
	face = ('Bold' if bold else '') + ('Italic' if italic else '') or 'Regular'
	font_dir = pathlib.Path(__file__).resolve().parent.parent / 'assets/fonts'
	path = font_dir / f'atkinson_hyperlegible_{family.lower()}' / f'AtkinsonHyperlegible{family}-{face}.ttf'
	# A fixed reference size avoids huge-font errors and retains fractional metrics.
	font = PIL.ImageFont.truetype(str(path), 1024)
	return path, font


#============================================
def measure_text(value: str, *, size: float, role: str = 'normal', bold: bool = False,
	italic: bool = False, anchor: str = 'middle') -> tuple[float, float, float, float]:
	"""Return conservative painted bounds relative to an SVG baseline origin.

	Missing glyphs receive extra space for fallback fonts; installed fallbacks can
	still exceed that allowance.
	"""
	if not math.isfinite(size) or size <= 0:
		raise ValueError('Font size must be finite and positive')
	if anchor not in ('start', 'middle', 'end'):
		raise ValueError('Anchor must be start, middle, or end')
	path, font = _font(role, bold, italic)
	scale = size / 1024
	left, top, right, bottom = font.getbbox(value, anchor='ls')
	advance = font.getlength(value) * scale
	offset = {'start': 0, 'middle': -advance / 2, 'end': -advance}[anchor]
	missing = sum(ord(char) not in svg_tools.parts._font_characters(path) for char in value)
	margin = .02 + 2 * scale
	# Allow one em per missing glyph on each side and one em vertically;
	# this is conservative, not a guarantee for every fallback font.
	fallback_width = missing * size
	fallback_height = size if missing else 0
	bounds = (offset + left * scale - margin - fallback_width,
		top * scale - margin - fallback_height,
		offset + right * scale + margin + fallback_width,
		bottom * scale + margin + fallback_height)
	if not all(math.isfinite(bound) for bound in bounds):
		raise ValueError('Text bounds must be finite')
	return bounds


#============================================
def label(x: float, y: float, value: str, *, size: float, color: str,
	anchor: str = 'middle', role: str = 'normal', bold: bool = False,
	italic: bool = False) -> svg_tools.parts.SvgPart:
	"""Create a measured editable label at the given SVG baseline."""
	if not all(math.isfinite(coordinate) for coordinate in (x, y)):
		raise ValueError('Label coordinates must be finite')
	left, top, right, bottom = measure_text(value, size=size, role=role,
		bold=bold, italic=italic, anchor=anchor)
	family = 'Atkinson Hyperlegible Next' if role == 'normal' else 'Atkinson Hyperlegible Mono'
	element = xml.etree.ElementTree.Element('text', {
		'x': str(x), 'y': str(y), 'font-size': str(size), 'fill': color,
		'text-anchor': anchor, 'font-family': family,
		'font-weight': 'bold' if bold else 'normal',
		'font-style': 'italic' if italic else 'normal',
		'{http://www.w3.org/XML/1998/namespace}space': 'preserve',
	})
	element.text = value
	fragment = xml.etree.ElementTree.tostring(element, encoding='ascii', xml_declaration=False).decode('ascii')
	defusedxml.ElementTree.fromstring(fragment)
	_, font = _font(role, bold, italic)
	advance = font.getlength(value) * (size / 1024)
	start = x - {'start': 0, 'middle': advance / 2, 'end': advance}[anchor]
	part = svg_tools.parts.SvgPart(fragment, (x + left, y + top, x + right, y + bottom), {
		'baseline': (x, y), 'start': (start, y), 'end': (start + advance, y),
		'center': (x + (left + right) / 2, y + (top + bottom) / 2),
	})
	return part


@dataclasses.dataclass(frozen=True)
class TextRun:
	"""One editable text run; script is None, 'sub', or 'super'."""
	text: str
	bold: bool = False
	italic: bool = False
	color: str | None = None
	script: str | None = None

	def __post_init__(self) -> None:
		if self.script not in (None, 'sub', 'super'):
			raise ValueError('Script must be sub, super, or None')


@dataclasses.dataclass(frozen=True)
class ExtractedLabel:
	text: str
	x: str | None
	y: str | None
	id: str | None


@dataclasses.dataclass(frozen=True)
class TextExtraction:
	labels: tuple[ExtractedLabel, ...]
	unavailable: str


#============================================
def _run_advance(run: TextRun, size: float, role: str, *, allowance: bool = False) -> float:
	path, font = _font(role, run.bold, run.italic)
	run_size = size * (.7 if run.script else 1)
	missing = sum(ord(char) not in svg_tools.parts._font_characters(path) for char in run.text)
	# Wrapping width includes the one-em fallback margin on both horizontal sides.
	return font.getlength(run.text) * (run_size / 1024) + (missing * run_size * 2 if allowance else 0)


#============================================
def _line_width(runs: list[TextRun], size: float, role: str) -> float:
	runs = list(runs)
	while runs and not runs[-1].text.rstrip():
		runs.pop()
	if runs:
		runs[-1] = dataclasses.replace(runs[-1], text=runs[-1].text.rstrip())
	width = sum(_run_advance(run, size, role, allowance=True) for run in runs)
	if not math.isfinite(width):
		raise ValueError('Text width must be finite')
	return width


#============================================
def _text_part(x: float, y: float, lines: list[list[TextRun]], *, size: float,
	color: str, role: str, anchor: str, line_height: float) -> svg_tools.parts.SvgPart:
	if not all(math.isfinite(v) for v in (x, y, line_height)) or line_height <= 0:
		raise ValueError('Coordinates and line height must be finite, with positive line height')
	# Validate size, role, and anchor through the existing font measurement contract.
	measure_text('', size=size, role=role, anchor=anchor)
	family = 'Atkinson Hyperlegible Next' if role == 'normal' else 'Atkinson Hyperlegible Mono'
	root = xml.etree.ElementTree.Element('text', {'x': str(x), 'y': str(y),
		'font-size': str(size), 'fill': color, 'font-family': family, 'text-anchor': anchor,
		'{http://www.w3.org/XML/1998/namespace}space': 'preserve'})
	boxes = []
	for index, line in enumerate(lines):
		baseline = y + index * line_height
		width = sum(_run_advance(run, size, role) for run in line)
		start = x - {'start': 0, 'middle': width / 2, 'end': width}[anchor]
		span = xml.etree.ElementTree.SubElement(root, 'tspan', {'x': str(x), 'y': str(baseline)})
		cursor = start
		for run in line:
			run_size = size * (.7 if run.script else 1)
			shift = {'sub': size * .2, 'super': -size * .4, None: 0}[run.script]
			if run.text.strip():
				left, top, right, bottom = measure_text(run.text, size=run_size, role=role,
					bold=run.bold, italic=run.italic, anchor='start')
				boxes.append((cursor + left, baseline + shift + top, cursor + right, baseline + shift + bottom))
			child = xml.etree.ElementTree.SubElement(span, 'tspan', {
				'font-weight': 'bold' if run.bold else 'normal',
				'font-style': 'italic' if run.italic else 'normal',
				'fill': run.color if run.color is not None else color,
				'font-size': str(run_size), 'baseline-shift': run.script or 'baseline'})
			child.text = run.text
			cursor += _run_advance(run, size, role)
	# ASVS 1.2.1: XML serialization escapes text and attribute values in context.
	fragment = xml.etree.ElementTree.tostring(root, encoding='ascii', xml_declaration=False).decode('ascii')
	defusedxml.ElementTree.fromstring(fragment)
	bounds = (min(box[0] for box in boxes), min(box[1] for box in boxes),
		max(box[2] for box in boxes), max(box[3] for box in boxes)) if boxes else (x, y, x, y)
	return svg_tools.parts.SvgPart(fragment, bounds, {'baseline': (x, y),
		'center': ((bounds[0] + bounds[2]) / 2, (bounds[1] + bounds[3]) / 2)})


#============================================
def styled_label(x: float, y: float, runs: list[TextRun], *, size: float, color: str,
	anchor: str = 'start', role: str = 'normal') -> svg_tools.parts.SvgPart:
	"""Create an editable single-line label with individually styled runs."""
	return _text_part(x, y, [runs], size=size, color=color, role=role, anchor=anchor,
		line_height=size * 1.2)


#============================================
def wrapped_text(x: float, y: float, runs: list[TextRun], *, width: float, size: float,
	color: str, line_height: float | None = None, height: float | None = None,
	role: str = 'normal') -> svg_tools.parts.SvgPart:
	"""Wrap at word boundaries; raise ValueError if width or height cannot fit."""
	if not math.isfinite(width) or width <= 0:
		raise ValueError('Width must be finite and positive')
	measure_text('', size=size, role=role, anchor='start')
	value = ''.join(run.text for run in runs)
	# Split at word boundaries, then map each token back to its styled pieces.
	segments = []
	for match in re.finditer(r'[^\S\n]+|\n|\S+', value):
		pieces = []
		position = 0
		for run in runs:
			end = position + len(run.text)
			start_slice, end_slice = max(match.start(), position), min(match.end(), end)
			if start_slice < end_slice:
				pieces.append(dataclasses.replace(run, text=run.text[start_slice-position:end_slice-position]))
			position = end
		segments.append((match.group(), pieces))
	lines: list[list[TextRun]] = [[]]
	for token, pieces in segments:
		if token == '\n':
			lines.append([])
			continue
		if not token.isspace() and lines[-1] and _line_width(lines[-1] + pieces, size, role) > width:
			lines.append([])
		lines[-1].extend(pieces)
	if any(_line_width(line, size, role) > width for line in lines):
		raise ValueError('Text overflows the requested width')
	spacing = line_height if line_height is not None else size * 1.2
	part = _text_part(x, y, lines, size=size, color=color, role=role, anchor='start',
		line_height=spacing)
	if height is not None:
		if not math.isfinite(height) or height <= 0:
			raise ValueError('Height must be finite and positive')
		# Include every line box, even when an explicit line has no painted glyphs.
		top = min(y - size, part.bounds[1])
		bottom = max(y + (len(lines) - 1) * spacing, part.bounds[3])
		if bottom - top > height:
			raise ValueError('Text overflows the requested height')
	return part


#============================================
def extract_text(path: pathlib.Path | str) -> TextExtraction:
	"""Read live SVG text and report content that cannot be extracted as text.

	Positions are the literal attributes on each text element, not transformed coordinates.
	Paths and images may contain labels, but cannot be identified as such reliably.
	"""
	# ASVS 1.5.1: defusedxml rejects unsafe entity expansion in imported XML.
	root = defusedxml.ElementTree.parse(path).getroot()
	labels = []
	images = paths = 0
	for element in root.iter():
		tag = element.tag.rsplit('}', 1)[-1]
		if tag == 'text':
			labels.append(ExtractedLabel(''.join(element.itertext()), element.get('x'),
				element.get('y'), element.get('id')))
		elif tag == 'image':
			images += 1
		elif tag == 'path':
			paths += 1
	return TextExtraction(tuple(labels), f'Raster or outlined labels are unavailable; '
		f'{images} image(s) and {paths} path(s) may contain such labels.')
