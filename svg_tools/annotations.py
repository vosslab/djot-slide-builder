"""Editable, locally positioned workflow nodes and authored connectors."""

import math
import xml.sax.saxutils

import svg_tools.parts
import svg_tools.text


#============================================
def box(label: str | list[svg_tools.text.TextRun], width: float, height: float, fill: str, *, shape: str = 'process',
	font_size: float = 16, stroke: str = '#344651', stroke_width: float = 2) -> svg_tools.parts.SvgPart:
	"""Create a process box or decision diamond centered on the local origin.

	Labels or styled text runs wrap inside the shape and raise ValueError when they cannot fit.
	"""
	if (shape not in ('process', 'decision') or not all(math.isfinite(v) and v > 0
		for v in (width, height, font_size, stroke_width))):
		raise ValueError('Shape and positive finite dimensions are required')
	available_width = width * (.46 if shape == 'decision' else .85)
	available_height = height * (.46 if shape == 'decision' else .8)
	runs = [svg_tools.text.TextRun(label)] if isinstance(label, str) else label
	text = svg_tools.text.wrapped_text(0, 0, runs,
		width=available_width, height=available_height, size=font_size, color=stroke)
	text = svg_tools.parts.transform(text, x=-(text.bounds[0] + text.bounds[2])/2,
		y=-(text.bounds[1] + text.bounds[3])/2)
	w, h = width/2, height/2
	if shape == 'decision' and (max(abs(text.bounds[0]), abs(text.bounds[2]))/w
		+ max(abs(text.bounds[1]), abs(text.bounds[3]))/h > 1):
		raise ValueError('Text overflows the decision diamond')
	fill = xml.sax.saxutils.quoteattr(fill)
	stroke_attr = xml.sax.saxutils.quoteattr(stroke)
	if shape == 'process':
		geometry = f'<rect x="{-w}" y="{-h}" width="{width}" height="{height}" rx="8"'
	else:
		geometry = f'<polygon points="0,{-h} {w},0 0,{h} {-w},0"'
	fragment = (f'<g><g fill={fill} stroke={stroke_attr} stroke-width="{stroke_width}" '
		f'stroke-linejoin="round">{geometry}/></g>{text.fragment}</g>')
	margin = stroke_width/2
	bounds = (min(-w-margin, text.bounds[0]), min(-h-margin, text.bounds[1]),
		max(w+margin, text.bounds[2]), max(h+margin, text.bounds[3]))
	return svg_tools.parts.SvgPart(fragment, bounds, {'center': (0, 0), 'left': (-w, 0),
		'right': (w, 0), 'top': (0, -h), 'bottom': (0, h)})


#============================================
def connector(points: list[tuple[float, float]], *, kind: str = 'activation',
	color: str = '#344651', stroke_width: float = 2, head_size: float = 10
	) -> svg_tools.parts.SvgPart:
	"""Connect authored points; heads follow the final nonzero segment.

	Binding, bracket, and callout draw plain lines; indirect draws a dashed line.
	Use text.label or text.wrapped_text for branch and callout labels.
	"""
	if (kind not in ('activation', 'inhibition', 'binding', 'indirect', 'bracket', 'callout')
		or len(points) < 2 or not all(len(p) == 2 and all(math.isfinite(v) for v in p) for p in points)
		or not all(math.isfinite(v) and v > 0 for v in (stroke_width, head_size))):
		raise ValueError('Invalid connector geometry or kind')
	end = points[-1]
	previous = next((p for p in reversed(points[:-1]) if p != end), None)
	if previous is None:
		raise ValueError('Connector requires a nonzero segment')
	dx, dy = end[0]-previous[0], end[1]-previous[1]
	length = math.hypot(dx, dy)
	ux, uy = dx/length, dy/length
	px, py = -uy, ux
	geometry = ' '.join(f'{x},{y}' for x, y in points)
	stroke = xml.sax.saxutils.quoteattr(color)
	dash = ' stroke-dasharray="6 5"' if kind == 'indirect' else ''
	fragment = (f'<g fill="none" stroke={stroke} stroke-width="{stroke_width}" '
		f'stroke-linecap="round" stroke-linejoin="round"><polyline points="{geometry}"{dash}/>')
	head_points = []
	if kind == 'activation':
		head_points = [(end[0]-head_size*ux + head_size*.5*px, end[1]-head_size*uy + head_size*.5*py),
			end, (end[0]-head_size*ux - head_size*.5*px, end[1]-head_size*uy - head_size*.5*py)]
	elif kind == 'inhibition':
		head_points = [(end[0]+head_size*.5*px, end[1]+head_size*.5*py),
			(end[0]-head_size*.5*px, end[1]-head_size*.5*py)]
	if head_points:
		fragment += '<polyline points="' + ' '.join(f'{x},{y}' for x, y in head_points) + '"/>'
	fragment += '</g>'
	all_points = list(points) + head_points
	margin = stroke_width/2
	bounds = (min(p[0] for p in all_points)-margin, min(p[1] for p in all_points)-margin,
		max(p[0] for p in all_points)+margin, max(p[1] for p in all_points)+margin)
	return svg_tools.parts.SvgPart(fragment, bounds, {'start': points[0], 'end': end})
