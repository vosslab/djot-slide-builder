"""Editable exon blocks joined by thin schematic intron spans."""

import re
import math
import collections.abc
import xml.etree.ElementTree

import svg_tools.chromosomes
import svg_tools.parts


#============================================
def gene_track_svg(name: str,
	exons: collections.abc.Sequence[svg_tools.chromosomes.Segment],
	intron_lengths: collections.abc.Sequence[float], *,
	width: float | None = None, height: float = 50) -> tuple[str, float, list[float]]:
	"""Return an SVG group, whole track width, and exon starts plus final exon end.

	Lengths are schematic units. Positive introns connect thick exon blocks; zero
	introns join adjacent blocks. Segment bands are ignored. Unlike chromosome
	boundaries, these coordinates mark exon starts, including the preceding gap.
	Names must be unique XML-safe prefixes in the enclosing document. Height is
	the exon block height; provide external margins for outline strokes. Short
	labels work best; width-based font fitting is approximate.
	"""
	if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.-]*", name):
		raise ValueError("Use an XML-safe unique namespace")
	if not exons or not all(isinstance(exon, svg_tools.chromosomes.Segment) for exon in exons):
		raise ValueError("Supply at least one exon Segment")
	if len(intron_lengths) != len(exons) - 1:
		raise ValueError("Supply exactly one intron length between each pair of exons")
	if any(not isinstance(value, (int, float)) or isinstance(value, bool)
		or not math.isfinite(value) or value < 0 for value in intron_lengths):
		raise ValueError("Intron lengths must be finite and nonnegative")
	natural_width = sum(exon.length for exon in exons) + sum(intron_lengths)
	if width is None:
		width = natural_width
	if any(not isinstance(value, (int, float)) or isinstance(value, bool)
		or not math.isfinite(value) or value <= 0 for value in (natural_width, width, height)):
		raise ValueError("Track dimensions must be finite and positive")
	group = xml.etree.ElementTree.Element("g", {"id": name})
	boundaries = []
	x = 0.0
	for index, exon in enumerate(exons):
		boundaries.append(x)
		exon_width = exon.length / natural_width * width
		region = xml.etree.ElementTree.SubElement(group, "g", {"id": f"{name}-exon-{index}"})
		xml.etree.ElementTree.SubElement(region, "rect", {
			"x": str(x), "y": "0", "width": str(exon_width), "height": str(height),
			"fill": exon.color, "stroke": "#344651", "stroke-width": str(height * .035),
		})
		font_size = min(height * .59, exon_width * .8 / max(1, len(exon.label)))
		xml.etree.ElementTree.SubElement(region, "text", {
			"x": str(x + exon_width / 2), "y": str(height / 2 + font_size * .34),
			"font-family": "Atkinson Hyperlegible Next", "font-size": str(font_size),
			"font-weight": "600", "text-anchor": "middle",
			"fill": svg_tools.chromosomes._label_color(exon.color),
		}).text = exon.label
		x += exon_width
		if index < len(intron_lengths) and intron_lengths[index] > 0:
			end = x + intron_lengths[index] / natural_width * width
			xml.etree.ElementTree.SubElement(group, "line", {
				"id": f"{name}-intron-{index}", "x1": str(x), "x2": str(end),
				"y1": str(height / 2), "y2": str(height / 2),
				"stroke": "#344651", "stroke-width": str(height * .06),
			})
			x = end
	boundaries.append(x)
	fragment = xml.etree.ElementTree.tostring(
		group, encoding="ascii", xml_declaration=False).decode("ascii")
	return fragment, width, boundaries


#============================================
def gene_track_part(name: str,
	exons: collections.abc.Sequence[svg_tools.chromosomes.Segment],
	intron_lengths: collections.abc.Sequence[float], *,
	width: float | None = None, height: float = 50) -> svg_tools.parts.SvgPart:
	"""Render a local part with start, end, center and boundary_N exon anchors."""
	fragment, track_width, boundaries = gene_track_svg(name, exons, intron_lengths,
		width=width, height=height)
	margin = height * .035 / 2
	bounds = (-margin, -margin, track_width+margin, height+margin)
	bounds = svg_tools.parts.include_text_bounds(fragment, bounds)
	anchors = {f'boundary_{index}': (x, height/2) for index, x in enumerate(boundaries)}
	anchors['start'], anchors['end'] = anchors['boundary_0'], anchors[f'boundary_{len(boundaries)-1}']
	anchors['center'] = (track_width/2, height/2)
	part = svg_tools.parts.SvgPart(fragment, bounds, anchors)
	return part


#============================================
def gene_feature_part(label: str, length: float, direction: str, *, color: str,
	height: float = 40) -> svg_tools.parts.SvgPart:
	"""Draw one explicitly oriented gene, with its label above the arrow.

	Coordinates run left to right; direction is 'forward' or 'reverse'. Length
	and height are drawing units, and no biological coordinates are inferred.
	"""
	if (direction not in ('forward', 'reverse') or not isinstance(label, str)
		or any(not isinstance(v, (int, float)) or isinstance(v, bool)
			or not math.isfinite(v) or v <= 0 for v in (length, height))):
		raise ValueError('Supply a label, positive dimensions and forward or reverse direction')
	svg_tools.chromosomes.Segment(label, color, length)
	head = min(height * .5, length * .35)
	points = (f'0,0 {length-head},0 {length},{height/2} {length-head},{height} 0,{height}'
		if direction == 'forward' else
		f'{length},0 {head},0 0,{height/2} {head},{height} {length},{height}')
	shape = xml.etree.ElementTree.Element('polygon', {'points': points, 'fill': color,
		'stroke': '#344651', 'stroke-width': '2', 'stroke-linejoin': 'round'})
	return _labeled_feature(shape, label, length, height,
		{'tip': (length if direction == 'forward' else 0, height/2)})


#============================================
def _labeled_feature(shape: xml.etree.ElementTree.Element, label: str, width: float,
	height: float, extra: dict[str, tuple[float, float]]) -> svg_tools.parts.SvgPart:
	import svg_tools.text
	fragment = xml.etree.ElementTree.tostring(shape, encoding='unicode')
	label_part = svg_tools.text.label(width/2, -8, label, size=15, color='#344651')
	bounds = (min(-1, label_part.bounds[0]), min(-1, label_part.bounds[1]),
		max(width+1, label_part.bounds[2]), max(height+1, label_part.bounds[3]))
	anchors = {'start': (0, height/2), 'end': (width, height/2),
		'center': (width/2, height/2), **extra}
	return svg_tools.parts.SvgPart('<g>' + fragment + label_part.fragment + '</g>', bounds, anchors)


#============================================
def landmark_part(kind: str, label: str, *, direction: str, width: float = 40,
	height: float = 40, color: str = '#dceef4') -> svg_tools.parts.SvgPart:
	"""Draw a supplied promoter, operator, or terminator landmark and label.

	The promoter arrow follows direction. Operator and terminator symbols are
	symmetric; direction remains an explicit part of the authored input.
	"""
	if (kind not in ('promoter', 'operator', 'terminator') or direction not in ('forward', 'reverse')
		or not isinstance(label, str) or any(not isinstance(v, (int, float)) or isinstance(v, bool)
			or not math.isfinite(v) or v <= 0 for v in (width, height))):
		raise ValueError('Supply a landmark, label, direction and positive dimensions')
	svg_tools.chromosomes.Segment(label, color, width)
	shape = xml.etree.ElementTree.Element('g', {'stroke': '#344651', 'stroke-width': '2',
		'stroke-linejoin': 'round', 'fill': color})
	if kind == 'operator':
		xml.etree.ElementTree.SubElement(shape, 'rect', {'x': '0', 'y': str(height*.25),
			'width': str(width), 'height': str(height*.5), 'rx': '3'})
	elif kind == 'terminator':
		xml.etree.ElementTree.SubElement(shape, 'path', {'d': f'M {width/2} {height} V {height*.2} M {width*.15} {height*.2} H {width*.85}', 'fill': 'none'})
	else:
		x = width if direction == 'forward' else 0
		back = width*.68 if direction == 'forward' else width*.32
		xml.etree.ElementTree.SubElement(shape, 'path', {'d': f'M {width/2} {height} V {height*.3} H {x} M {back} {height*.1} L {x} {height*.3} L {back} {height*.5}', 'fill': 'none'})
	return _labeled_feature(shape, label, width, height, {'landmark': (width/2, height/2)})


#============================================
def operon_part(features: dict[str, tuple[svg_tools.parts.SvgPart, float]], *,
	length: float) -> svg_tools.parts.SvgPart:
	"""Place named features at authored x offsets on a horizontal baseline.

	Each part's start anchor is placed on the baseline; order, positions, lengths,
	and directions are supplied by the caller, not inferred from an operon model.
	"""
	if (not isinstance(length, (int, float)) or isinstance(length, bool)
		or not math.isfinite(length) or length <= 0 or not features):
		raise ValueError('Supply features and a positive baseline length')
	placed = {'baseline': svg_tools.parts.SvgPart(
		f'<line x1="0" y1="0" x2="{length}" y2="0" stroke="#344651" stroke-width="2"/>',
		(-1, -1, length+1, 1), {})}
	for name, (part, x) in features.items():
		if name == 'baseline':
			raise ValueError('baseline is reserved')
		if (not isinstance(part, svg_tools.parts.SvgPart) or 'start' not in part.anchors
			or not isinstance(x, (int, float)) or isinstance(x, bool) or not math.isfinite(x)):
			raise ValueError('Each feature needs a part with a start anchor and a finite offset')
		start_x, start_y = part.anchors['start']
		placed[name] = svg_tools.parts.transform(part, x=x-start_x, y=-start_y)
	combined = svg_tools.parts.group(placed)
	return svg_tools.parts.SvgPart(combined.fragment, combined.bounds,
		{**combined.anchors, 'start': (0, 0), 'end': (length, 0), 'center': (length/2, 0)})
