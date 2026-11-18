"""Draw gene labels in chromosome blocks or beside a locus leader."""

import re
import dataclasses

import lxml.etree

import svg_tools._xml
import svg_tools.parts
import svg_tools.text
import svg_tools.annotations
import svg_tools.chromosome_surface


#============================================
def _gene_runs(label: str) -> list[svg_tools.text.TextRun]:
	"""Keep gene symbols together while raising a terminal allele sign."""
	match = re.fullmatch(r'(.+)([+-])', label)
	if match:
		runs = [svg_tools.text.TextRun(match.group(1), bold=True, italic=True),
			svg_tools.text.TextRun(match.group(2), bold=True, script='super')]
	else:
		runs = [svg_tools.text.TextRun(label, bold=True)]
	return runs


#============================================
def _gene_label_part(label: str, size: float, color: str) -> svg_tools.parts.SvgPart:
	"""Make one measured upright label without guessing its baseline offset."""
	part = svg_tools.text.styled_label(0, 0, _gene_runs(label), size=size,
		color=svg_tools.text.label_color(color), anchor='middle')
	root = svg_tools._xml.parse(part.fragment)
	root.set('class', 'gene-label')
	line = next(iter(root))
	for span in list(line):
		root.append(span)
	root.remove(line)
	fragment = lxml.etree.tostring(root, encoding='ascii', xml_declaration=False).decode('ascii')
	part = dataclasses.replace(part, fragment=fragment)
	return part


#============================================
def append_label(parent: lxml.etree._Element, x: float, y: float,
	label: str, size: float, color: str) -> tuple[float, float, float, float]:
	"""Center measured label ink over one chromosome point."""
	part = _gene_label_part(label, size, color)
	shift_x, shift_y = x-part.anchors['center'][0], y-part.anchors['center'][1]
	root = svg_tools._xml.parse(part.fragment)
	for node in root.iter():
		if node.get('x') is not None:
			node.set('x', str(float(node.get('x'))+shift_x))
		if node.get('y') is not None:
			node.set('y', str(float(node.get('y'))+shift_y))
	parent.append(root)
	xmin, ymin, xmax, ymax = part.bounds
	bounds = (xmin+shift_x, ymin+shift_y, xmax+shift_x, ymax+shift_y)
	return bounds


#============================================
def label_size(label: str, surface: svg_tools.chromosome_surface.Surface,
	center: float, length: float, width: float, color: str) -> float:
	"""Fit actual upright ink within a curved locus's tangent and normal spans."""
	tangent = surface.path.unit_tangent(surface.parameter(center))
	normal = tangent * 1j
	part = _gene_label_part(label, 100, color)
	xmin, ymin, xmax, ymax = part.bounds
	corners = [complex(x, y) for x in (xmin, xmax) for y in (ymin, ymax)]
	along = [point.real*tangent.real+point.imag*tangent.imag for point in corners]
	across = [point.real*normal.real+point.imag*normal.imag for point in corners]
	along_per_unit = (max(along)-min(along))/100
	across_per_unit = (max(across)-min(across))/100
	size = min(surface.width*.52, length*.82/along_per_unit, width*.82/across_per_unit)
	return size


#============================================
def card(name: str, surface: svg_tools.chromosome_surface.Surface, center: float,
	label: str, color: str, length: float, *, minimum_size: float,
	terminal_ends: tuple[bool, bool]) -> svg_tools.parts.SvgPart | None:
	"""Fit measured allele ink before committing to an internal card."""
	start, end = center-length/2, center+length/2
	if start < 0 or end > surface.length:
		raise ValueError('Gene locus must fit on its chromosome surface')
	stroke = max(.7, surface.scale*.8)
	# Reserve the painted cap, a cap-length of body color, and the near half of the card border.
	margin = 2*surface.cap_length + stroke/2
	half = min(length/2, center-margin if terminal_ends[0] else center,
		surface.length-center-margin if terminal_ends[1] else surface.length-center)
	if half < length/2:
		minimum_size = max(minimum_size, surface.width*.4)
		if 2*half < minimum_size:
			return None
		start, end = center-half, center+half
	inset = max(surface.scale, surface.width*.05)
	if surface.width <= inset*2:
		raise ValueError('Chromosome surface is too narrow for a gene locus')
	inner_width = surface.width-inset*2
	size = label_size(label, surface, center, 2*half, inner_width, color)
	if size < minimum_size:
		return None
	group = lxml.etree.Element('g', {'id': name, 'data-layer': 'gene-locus',
		'data-gene': label})
	lxml.etree.SubElement(group, 'path', {'d': surface.ribbon(start, end,
		-surface.width/2+inset, surface.width/2-inset), 'fill': color,
		'stroke': '#344651', 'stroke-width': str(stroke),
		'stroke-linejoin': 'round', 'class': 'gene-locus'})
	point = surface.path.point(surface.parameter(center))
	label_bounds = append_label(group, point.real, point.imag, label, size, color)
	fragment = lxml.etree.tostring(group, encoding='ascii', xml_declaration=False).decode('ascii')
	path = surface.path.cropped(surface.parameter(start), surface.parameter(end))
	xmin, xmax, ymin, ymax = path.bbox()
	margin = inner_width/2+stroke/2
	bounds = (min(xmin-margin, label_bounds[0]), min(ymin-margin, label_bounds[1]),
		max(xmax+margin, label_bounds[2]), max(ymax+margin, label_bounds[3]))
	start_point, end_point = surface.point(start, 0), surface.point(end, 0)
	anchors = {'start': (start_point.real, start_point.imag), 'center': (point.real, point.imag),
		'end': (end_point.real, end_point.imag)}
	part = svg_tools.parts.SvgPart(fragment, bounds, anchors)
	return part


#============================================
def external(name: str, surface: svg_tools.chromosome_surface.Surface,
	position: float, allele: str, outward: complex) -> svg_tools.parts.SvgPart:
	"""Keep a true locus dot and a readable upright label when a card cannot fit."""
	parameter = surface.parameter(position)
	point = surface.path.point(parameter)
	normal = surface.path.unit_tangent(parameter)*1j
	if (normal*outward.conjugate()).real < 0:
		normal = -normal
	width = surface.width
	ink = '#172B3A'
	label = _gene_label_part(allele, width*.52, '#FFFFFF')
	xmin, ymin, xmax, ymax = label.bounds
	ink_depth = (abs(normal.real)*(xmax-xmin)+abs(normal.imag)*(ymax-ymin))/2
	end = point+normal*width*.92
	label_center = end+normal*(width*.12+ink_depth)
	label = svg_tools.parts.transform(label, x=label_center.real-label.anchors['center'][0],
		y=label_center.imag-label.anchors['center'][1])
	anchor = (point.real, point.imag)
	stroke = max(.7, width*.04)
	leader = svg_tools.annotations.connector([anchor, (end.real, end.imag)],
		kind='callout', color=ink, stroke_width=stroke)
	group = lxml.etree.Element('g', {'id': name, 'data-layer': 'gene-locus',
		'data-gene': allele})
	group.append(svg_tools._xml.parse(leader.fragment))
	radius = width*.075
	lxml.etree.SubElement(group, 'circle', {'cx': str(point.real), 'cy': str(point.imag),
		'r': str(radius), 'fill': ink, 'stroke': '#FFFFFF', 'stroke-width': str(stroke)})
	group.append(svg_tools._xml.parse(label.fragment))
	margin = radius+stroke/2
	dot_bounds = (point.real-margin, point.imag-margin, point.real+margin, point.imag+margin)
	bounds = svg_tools.parts.union_bounds(label.bounds, leader.bounds, dot_bounds)
	fragment = lxml.etree.tostring(group, encoding='ascii', xml_declaration=False).decode('ascii')
	return svg_tools.parts.SvgPart(fragment, bounds, {'center': anchor})
