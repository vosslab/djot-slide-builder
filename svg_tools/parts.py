"""Local-coordinate SVG fragments with painted bounds and named anchors."""

import math
import dataclasses
import functools
import pathlib
import re

import PIL.ImageFont
import fontTools.ttLib
import defusedxml.ElementTree
import xml.sax.saxutils
import xml.etree.ElementTree


@dataclasses.dataclass(frozen=True)
class SvgPart:
	"""An SVG fragment, its (xmin, ymin, xmax, ymax) bounds, and named points.

	All coordinates use the fragment's local coordinate system. Bounds include
	painted strokes and labels; anchors need not lie inside the bounds.
	"""

	fragment: str
	bounds: tuple[float, float, float, float]
	anchors: dict[str, tuple[float, float]]

	def __post_init__(self) -> None:
		if (len(self.bounds) != 4 or not all(math.isfinite(v) for v in self.bounds)
			or self.bounds[0] > self.bounds[2] or self.bounds[1] > self.bounds[3]):
			raise ValueError('Bounds must be finite and ordered')
		if any(len(point) != 2 or not all(math.isfinite(v) for v in point)
			for point in self.anchors.values()):
			raise ValueError('Anchor coordinates must be finite pairs')


#============================================
@functools.lru_cache(maxsize=None)
def _font_characters(path: pathlib.Path) -> frozenset[int]:
	with fontTools.ttLib.TTFont(path) as font:
		return frozenset(font.getBestCmap())


#============================================
def include_text_bounds(fragment: str, bounds: tuple[float, float, float, float]
	) -> tuple[float, float, float, float]:
	"""Expand bounds for centered live text, allowing for missing font glyphs.

	Fallback allowance is conservative, but cannot guarantee bounds for every
	user-installed fallback typeface.
	"""
	xmin, ymin, xmax, ymax = bounds
	font_dir = pathlib.Path(__file__).resolve().parent.parent / 'assets/fonts/atkinson_hyperlegible_next'
	for text in xml.etree.ElementTree.fromstring(fragment).iter('text'):
		x, y = float(text.attrib['x']), float(text.attrib['y'])
		size = float(text.attrib['font-size'])
		weight = 'Bold' if text.attrib.get('font-weight') == '600' else 'Regular'
		runs = [(text.text or '', size, weight, 0.0, 0.0)]
		for child in text:
			face = weight
			if child.attrib.get('font-style') == 'italic':
				face = 'BoldItalic' if weight == 'Bold' else 'Italic'
			runs.append((child.text or '', float(child.attrib.get('font-size', size)), face,
				float(child.attrib.get('dx', 0)), float(child.attrib.get('dy', 0))))
		advance = 0.0
		baseline = 0.0
		margin = .02
		fallback_width = 0.0
		fallback_height = 0.0
		boxes = []
		for content, run_size, face, dx, dy in runs:
			advance += dx
			baseline += dy
			font_path = font_dir / f'AtkinsonHyperlegibleNext-{face}.ttf'
			missing = sum(ord(char) not in _font_characters(font_path) for char in content)
			# Allow one em per missing glyph on each side and one em vertically;
			# this is conservative, not a guarantee for every fallback font.
			fallback_width += missing * run_size
			if missing:
				fallback_height = max(fallback_height, run_size)
			# A fixed reference size avoids huge-font errors and retains fractional metrics.
			font = PIL.ImageFont.truetype(str(font_path), 1024)
			scale = run_size/1024
			margin += 2*scale
			left, top, right, bottom = font.getbbox(content, anchor='ls')
			boxes.append((advance+left*scale, baseline+top*scale,
				advance+right*scale, baseline+bottom*scale))
			advance += font.getlength(content)*scale
		for left, top, right, bottom in boxes:
			xmin, xmax = (min(xmin, x-advance/2+left-margin-fallback_width),
				max(xmax, x-advance/2+right+margin+fallback_width))
			ymin, ymax = (min(ymin, y+top-margin-fallback_height),
				max(ymax, y+bottom+margin+fallback_height))
	result = (xmin, ymin, xmax, ymax)
	return result


#============================================
def namespace_ids(fragment: str, prefix: str) -> str:
	"""Prefix native fragment IDs and their local URL and href references."""
	if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.-]*', prefix):
		raise ValueError('Prefix must be an SVG identifier')
	# ASVS 1.5.1: reject DTDs and entities when parsing fragment XML.
	parser = defusedxml.ElementTree.DefusedXMLParser(
		target=xml.etree.ElementTree.TreeBuilder(insert_comments=True), forbid_dtd=True)
	parser.feed('<wrapper xmlns:xlink="http://www.w3.org/1999/xlink">' + fragment + '</wrapper>')
	root = parser.close()
	ids = [element.attrib['id'] for element in root.iter() if 'id' in element.attrib]
	if len(ids) != len(set(ids)):
		raise ValueError('Fragment contains duplicate IDs')
	names = {old: f'{prefix}-{old}' for old in ids}
	for element in root.iter():
		for attr, value in element.attrib.items():
			if attr == 'id':
				element.set(attr, names[value])
			elif attr in ('href', '{http://www.w3.org/1999/xlink}href') and value.startswith('#'):
				element.set(attr, '#' + names.get(value[1:], value[1:]))
			elif attr in ('aria-labelledby', 'aria-describedby'):
				element.set(attr, re.sub(r'\S+', lambda m: names.get(m.group(), m.group()), value))
			elif not attr.startswith('data-'):
				element.set(attr, re.sub(r'(url\(\s*["\']?#)([^"\'\s)]+)(["\']?\s*\))',
					lambda m: m.group(1) + names.get(m.group(2), m.group(2)) + m.group(3), value))
	return xml.sax.saxutils.escape(root.text or '') + ''.join(
		xml.etree.ElementTree.tostring(child, encoding='unicode') for child in root)



#============================================
def transform(part: SvgPart, x: float = 0, y: float = 0, rotation: float = 0,
	scale: float = 1) -> SvgPart:
	"""Scale, rotate in degrees about the origin, then translate a part."""
	if not all(math.isfinite(v) for v in (x, y, rotation, scale)) or scale <= 0:
		raise ValueError('Transform values must be finite and scale must be positive')
	angle = math.radians(rotation)
	a = scale * math.cos(angle)
	b = scale * math.sin(angle)
	c, d = -b, a
	def point(px: float, py: float) -> tuple[float, float]:
		return (a*px + c*py + x, b*px + d*py + y)
	xmin, ymin, xmax, ymax = part.bounds
	corners = [point(px, py) for px in (xmin, xmax) for py in (ymin, ymax)]
	bounds = (min(p[0] for p in corners), min(p[1] for p in corners),
		max(p[0] for p in corners), max(p[1] for p in corners))
	anchors = {name: point(*value) for name, value in part.anchors.items()}
	fragment = f'<g transform="matrix({a} {b} {c} {d} {x} {y})">{part.fragment}</g>'
	return SvgPart(fragment, bounds, anchors)


#============================================
def group(parts: dict[str, SvgPart]) -> SvgPart:
	"""Group named parts, qualifying anchors as name.anchor and isolating IDs.

	Names must be XML-safe identifiers without dots. Nest groups to qualify further.
	"""
	if not parts or any(not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_-]*', name) for name in parts):
		raise ValueError('Group names must be XML-safe identifiers without dots')
	values = list(parts.values())
	bounds = (min(p.bounds[0] for p in values), min(p.bounds[1] for p in values),
		max(p.bounds[2] for p in values), max(p.bounds[3] for p in values))
	anchors = {f'{name}.{key}': point for name, part in parts.items()
		for key, point in part.anchors.items()}
	fragments = [namespace_ids(part.fragment, f'part{index}')
		for index, part in enumerate(values)]
	return SvgPart('<g>' + ''.join(fragments) + '</g>', bounds, anchors)


#============================================
def align(parts: list[SvgPart], edge: str, coordinate: float) -> list[SvgPart]:
	"""Align painted bounds at left, right, top, bottom, center_x or center_y."""
	if edge not in ('left', 'right', 'top', 'bottom', 'center_x', 'center_y'):
		raise ValueError('Unknown alignment edge')
	if not math.isfinite(coordinate):
		raise ValueError('Coordinate must be finite')
	result = []
	for part in parts:
		xmin, ymin, xmax, ymax = part.bounds
		positions = {'left': xmin, 'right': xmax, 'top': ymin, 'bottom': ymax,
			'center_x': (xmin + xmax)/2, 'center_y': (ymin + ymax)/2}
		delta = coordinate - positions[edge]
		result.append(transform(part, x=delta if edge in ('left', 'right', 'center_x') else 0,
			y=delta if edge in ('top', 'bottom', 'center_y') else 0))
	return result


#============================================
def distribute(parts: list[SvgPart], axis: str, gap: float) -> list[SvgPart]:
	"""Space parts in input order by painted bounds, keeping the first in place."""
	if axis not in ('x', 'y') or not math.isfinite(gap) or gap <= 0:
		raise ValueError('Axis must be x or y and gap must be finite and positive')
	if not parts:
		return []
	low, high = (0, 2) if axis == 'x' else (1, 3)
	position = parts[0].bounds[low]
	result = []
	for part in parts:
		delta = position - part.bounds[low]
		placed = transform(part, x=delta if axis == 'x' else 0,
			y=delta if axis == 'y' else 0)
		result.append(placed)
		position = placed.bounds[high] + gap
	return result
