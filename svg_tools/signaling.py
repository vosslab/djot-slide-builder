"""Small signaling-diagram parts.

The round heads and paired tails echo the membrane phospholipid motif in
biology-problems' biochemistry-problems/membranes/phospholipid-unit.svg.
"""

import math
import xml.etree.ElementTree

import svgpathtools

import svg_tools.curves
import svg_tools.parts
import svg_tools.text


#============================================
def membrane(path_d: str, *, spacing: float, thickness: float, color: str,
	gaps: tuple[tuple[float, float], ...] = ()) -> svg_tools.parts.SvgPart:
	"""Draw paired leaflets along an open centerline, omitting samples in gaps.

	Gaps are inclusive distances along the centerline, in its drawing units. The
	extracellular side is the negative normal (above a left-to-right line); the
	cytoplasmic side is the positive normal. Side anchors are at the path midpoint,
	even when that site is inside a gap. Start, center, and end are on the path.
	Thickness is the distance between the outer surfaces of the heads.
	Gaps omit lipid centers; allow clearance for heads and strokes when sizing them.
	"""
	if not math.isfinite(thickness) or thickness <= 0:
		raise ValueError('Thickness must be finite and positive')
	samples = svg_tools.curves.sample_curve(path_d, spacing=spacing)
	path = svgpathtools.parse_path(path_d)
	length = path.length()
	if path.start == path.end:
		raise ValueError('Membrane centerline must be open')
	for start, end in gaps:
		if not all(math.isfinite(value) for value in (start, end)) or not 0 <= start <= end <= length:
			raise ValueError('Gaps must be finite ordered intervals within the path')

	radius = thickness * 0.09
	head = thickness / 2 - radius
	stroke = thickness * 0.035
	group = xml.etree.ElementTree.Element('g', {
		'stroke': '#344651', 'stroke-width': str(stroke),
		'stroke-linecap': 'round', 'stroke-linejoin': 'round',
	})
	placed = []
	for index, (x, y, angle) in enumerate(samples):
		if any(start <= index * spacing <= end for start, end in gaps):
			continue
		lipids = xml.etree.ElementTree.SubElement(group, 'g', {
			'transform': f'translate({x} {y}) rotate({angle})',
		})
		for side in (-1, 1):
			for offset in (-radius * 0.35, radius * 0.35):
				xml.etree.ElementTree.SubElement(lipids, 'path', {
					'd': f'M {offset} {side * head} L {offset} {side * thickness * 0.04}', 'fill': 'none',
				})
			xml.etree.ElementTree.SubElement(lipids, 'circle', {
				'cx': '0', 'cy': str(side * head), 'r': str(radius), 'fill': color,
			})
		placed.append((x, y))
	if not placed:
		raise ValueError('Gaps cannot omit every lipid')
	# A circular envelope contains each rotated lipid, including its stroke.
	margin = math.hypot(radius, thickness / 2) + stroke / 2
	bounds = (min(x for x, y in placed) - margin, min(y for x, y in placed) - margin,
		max(x for x, y in placed) + margin, max(y for x, y in placed) + margin)
	middle = path.ilength(length / 2)
	point = path.point(middle)
	tangent = path.unit_tangent(middle)
	normal = complex(-tangent.imag, tangent.real) * thickness / 2
	anchors = {'start': (path.start.real, path.start.imag), 'end': (path.end.real, path.end.imag),
		'center': (point.real, point.imag),
		'extracellular': ((point - normal).real, (point - normal).imag),
		'cytoplasmic': ((point + normal).real, (point + normal).imag)}
	fragment = xml.etree.ElementTree.tostring(group, encoding='unicode')
	return svg_tools.parts.SvgPart(fragment, bounds, anchors)


#============================================
def _molecule(path: str, width: float, height: float, color: str,
	anchors: dict[str, tuple[float, float]]) -> svg_tools.parts.SvgPart:
	if not all(math.isfinite(value) and value > 0 for value in (width, height)):
		raise ValueError('Width and height must be finite and positive')
	group = xml.etree.ElementTree.Element('g', {
		'transform': f'scale({width} {height})', 'fill': color, 'stroke': '#344651',
		'stroke-width': '0.025', 'stroke-linecap': 'round', 'stroke-linejoin': 'round',
	})
	xml.etree.ElementTree.SubElement(group, 'path', {'d': path})
	return svg_tools.parts.SvgPart(xml.etree.ElementTree.tostring(group, encoding='unicode'),
		(-.5525*width, -.5525*height, .5525*width, .5525*height),
		{name: (x*width, y*height) for name, (x, y) in anchors.items()})


#============================================
def protein(*, width: float, height: float, color: str,
	kind: str = 'globular', activity: str | None = None) -> svg_tools.parts.SvgPart:
	"""Draw a schematic globular or kinase-like protein centered at the origin.

	The upper binding anchor marks a schematic attachment point. Anchors indicate
	locations for composition, not experimentally determined molecular structure.
	"""
	if activity not in (None, 'active', 'inactive'):
		raise ValueError('Activity must be active, inactive, or None')
	if kind not in ('globular', 'kinase'):
		raise ValueError('Kind must be globular or kinase')
	if kind == 'globular':
		part = _molecule(
			'M -0.42 -0.10 C -0.48 -0.29 -0.33 -0.43 -0.17 -0.40 '
			'C -0.04 -0.49 0.08 -0.45 0.15 -0.37 C 0.33 -0.43 0.48 -0.27 0.43 -0.10 '
			'C 0.51 0.04 0.44 0.20 0.32 0.24 C 0.26 0.43 0.09 0.47 -0.03 0.40 '
			'C -0.18 0.47 -0.34 0.38 -0.35 0.26 C -0.49 0.20 -0.50 0.02 -0.42 -0.10 Z',
			width, height, color, {'center': (0, 0), 'binding': (.15, -.37),
				'input': (-.44, 0), 'output': (.44, 0), 'modification': (.25, .38)})
	else:
		part = _molecule(
		'M -0.45 -0.06 C -0.52 -0.25 -0.39 -0.44 -0.22 -0.43 '
		'C -0.09 -0.49 -0.04 -0.37 0 -0.27 C 0.04 -0.38 0.13 -0.45 0.25 -0.41 '
		'C 0.44 -0.42 0.52 -0.25 0.45 -0.08 C 0.54 0.10 0.44 0.23 0.35 0.28 '
		'C 0.29 0.46 0.10 0.48 0 0.40 C -0.14 0.49 -0.30 0.44 -0.35 0.31 '
		'C -0.50 0.25 -0.52 0.09 -0.45 -0.06 Z', width, height, color,
		{'center': (0, 0), 'binding': (0, -.27), 'input': (-.46, 0),
			'output': (.46, 0), 'modification': (.25, .40)})
	if activity is None:
		return part
	return _activity(part, activity, min(width, height))


#============================================
def _activity(part: svg_tools.parts.SvgPart, activity: str, size: float) -> svg_tools.parts.SvgPart:
	"""Add an explicit state label and a filled or crossed state symbol."""
	font_size = size * .16
	y = part.bounds[3] + font_size * 1.25
	label = svg_tools.text.label(0, y, activity, size=font_size, color='#344651', bold=True)
	r = font_size * .24
	x = label.bounds[0] - r * 2
	cy = y - font_size * .33
	mark = xml.etree.ElementTree.Element('g', {'stroke': '#344651', 'stroke-width': str(r*.22)})
	xml.etree.ElementTree.SubElement(mark, 'circle', {'cx': str(x), 'cy': str(cy),
		'r': str(r), 'fill': '#467449' if activity == 'active' else 'white'})
	if activity == 'inactive':
		xml.etree.ElementTree.SubElement(mark, 'path', {'d': f'M {x-r*.7} {cy+r*.7} L {x+r*.7} {cy-r*.7}'})
	margin = r * 1.11
	bounds = (min(part.bounds[0], label.bounds[0], x-margin), min(part.bounds[1], label.bounds[1], cy-margin),
		max(part.bounds[2], label.bounds[2], x+margin), max(part.bounds[3], label.bounds[3], cy+margin))
	anchors = dict(part.anchors, activity_label=label.anchors['center'])
	return svg_tools.parts.SvgPart(part.fragment + xml.etree.ElementTree.tostring(mark, encoding='unicode')
		+ label.fragment, bounds, anchors)


#============================================
def phosphate(part: svg_tools.parts.SvgPart, *, site: str = 'modification',
	site_label: str | None = None, radius: float = 10) -> svg_tools.parts.SvgPart:
	"""Attach a phosphate badge at a named anchor, independently of activity.

	The optional site label is authored by the caller; no molecular activity is inferred.
	"""
	if site not in part.anchors:
		raise ValueError('Unknown modification site anchor')
	if not math.isfinite(radius) or radius <= 0:
		raise ValueError('Radius must be finite and positive')
	if site_label is not None and not site_label.strip():
		raise ValueError('Site label must not be empty')
	x, y = part.anchors[site]
	circle = xml.etree.ElementTree.Element('circle', {'cx': str(x), 'cy': str(y),
		'r': str(radius), 'fill': '#f4cf9f', 'stroke': '#344651', 'stroke-width': str(radius*.12)})
	badge = svg_tools.text.label(x, y + radius*.38, 'P', size=radius*1.15, color='#344651', bold=True)
	labels = [badge]
	if site_label is not None:
		labels.append(svg_tools.text.label(x + radius*1.35, y + radius*.4, site_label,
			size=radius*1.15, color='#344651', anchor='start'))
	margin = radius * 1.06
	bounds = (min(part.bounds[0], x-margin, *(p.bounds[0] for p in labels)),
		min(part.bounds[1], y-margin, *(p.bounds[1] for p in labels)),
		max(part.bounds[2], x+margin, *(p.bounds[2] for p in labels)),
		max(part.bounds[3], y+margin, *(p.bounds[3] for p in labels)))
	anchors = dict(part.anchors, phosphate=(x, y))
	return svg_tools.parts.SvgPart(part.fragment + xml.etree.ElementTree.tostring(circle, encoding='unicode')
		+ ''.join(p.fragment for p in labels), bounds, anchors)


#============================================
def ligand(*, width: float, height: float, color: str) -> svg_tools.parts.SvgPart:
	"""Draw a ligand centered at local origin (0, 0), with a lower binding point."""
	return _molecule(
		'M -0.40 -0.12 C -0.49 -0.30 -0.31 -0.46 -0.14 -0.40 '
		'C -0.01 -0.52 0.15 -0.46 0.21 -0.36 C 0.42 -0.38 0.50 -0.21 0.43 -0.07 '
		'C 0.50 0.09 0.39 0.23 0.24 0.24 C 0.20 0.41 0.06 0.48 -0.04 0.38 '
		'C -0.17 0.48 -0.31 0.36 -0.30 0.23 C -0.48 0.20 -0.51 0.03 -0.40 -0.12 Z',
		width, height, color, {'center': (0, 0), 'binding': (0, .42),
			'input': (-.45, 0), 'output': (.45, 0), 'modification': (.20, -.38)})


#============================================
def receptor(*, width: float, height: float, color: str) -> svg_tools.parts.SvgPart:
	"""Draw an upright receptor with its center and stalk at x=0.

	The membrane plane is y=0; the extracellular domain is above it and the cytoplasmic domain below.
	Its narrow central stalk can be placed in a caller-sized membrane gap.
	"""
	return _molecule(
		'M -0.10 -0.13 C -0.14 -0.20 -0.36 -0.21 -0.37 -0.32 '
		'C -0.43 -0.43 -0.29 -0.49 -0.18 -0.44 C -0.09 -0.50 -0.04 -0.44 0 -0.37 '
		'C 0.04 -0.44 0.12 -0.50 0.21 -0.44 C 0.34 -0.47 0.43 -0.39 0.37 -0.30 '
		'C 0.34 -0.22 0.14 -0.19 0.10 -0.13 L 0.10 0.13 '
		'C 0.16 0.19 0.37 0.19 0.39 0.31 C 0.44 0.42 0.30 0.49 0.17 0.44 '
		'C 0.06 0.50 -0.05 0.47 -0.10 0.43 C -0.24 0.48 -0.40 0.42 -0.39 0.31 '
		'C -0.38 0.20 -0.16 0.19 -0.10 0.13 Z', width, height, color,
		{'center': (0, 0), 'binding': (0, -.37), 'input': (0, -.37),
			'output': (0, .46), 'modification': (.28, .42), 'extracellular': (0, -.37),
			'membrane': (0, 0), 'cytoplasmic': (0, .46)})
