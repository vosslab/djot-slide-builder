"""Independent schematic cell envelopes and nuclear parts.

All parts are centered at the local origin. Internal parts are placed by the
caller; these silhouettes do not imply a cell-cycle stage or organelle count.
"""

import math

import lxml.etree

import svg_tools._xml
import svg_tools.parts
import svg_tools._style


#============================================
def cell_envelope(*, kind: str, width: float, height: float, color: str,
	wall_color: str | None = None) -> svg_tools.parts.SvgPart:
	"""Draw one envelope; plant cells require an explicit wall color.

	The fused yeast contour is one continuous envelope with left and right lobe
	anchors. Edge anchors are approximate boundary placement points, excluding stroke.
	"""
	paths = {
		'animal': 'M 0 -0.48 C 0.31 -0.52 0.49 -0.32 0.48 -0.03 C 0.52 0.24 0.32 0.48 0.03 0.48 C -0.26 0.51 -0.49 0.32 -0.48 0.04 C -0.52 -0.24 -0.31 -0.49 0 -0.48 Z',
		'bacterial': 'M -0.28 -0.43 L 0.28 -0.43 C 0.57 -0.43 0.57 0.43 0.28 0.43 L -0.28 0.43 C -0.57 0.43 -0.57 -0.43 -0.28 -0.43 Z',
		'yeast': 'M 0 -0.48 C 0.30 -0.48 0.48 -0.28 0.48 0 C 0.48 0.28 0.30 0.48 0 0.48 C -0.30 0.48 -0.48 0.28 -0.48 0 C -0.48 -0.28 -0.30 -0.48 0 -0.48 Z',
		'fused_yeast': 'M 0 -0.28 C 0.14 -0.45 0.30 -0.48 0.39 -0.38 C 0.54 -0.24 0.54 0.24 0.39 0.38 C 0.30 0.48 0.14 0.45 0 0.28 C -0.14 0.45 -0.30 0.48 -0.39 0.38 C -0.54 0.24 -0.54 -0.24 -0.39 -0.38 C -0.30 -0.48 -0.14 -0.45 0 -0.28 Z',
		'plant': 'M -0.38 -0.48 L 0.38 -0.48 Q 0.48 -0.48 0.48 -0.38 L 0.48 0.38 Q 0.48 0.48 0.38 0.48 L -0.38 0.48 Q -0.48 0.48 -0.48 0.38 L -0.48 -0.38 Q -0.48 -0.48 -0.38 -0.48 Z',
	}
	if kind not in paths:
		raise ValueError('Unknown cell envelope kind')
	if kind == 'plant' and wall_color is None:
		raise ValueError('Plant cells require a wall color')
	anchors = {'center': (0, 0), 'top': (0, -.48), 'bottom': (0, .48),
		'left': (-.48, 0), 'right': (.48, 0)}
	if kind == 'bacterial':
		anchors.update(top=(0, -.43), bottom=(0, .43), left=(-.4975, 0), right=(.4975, 0))
	if kind == 'fused_yeast':
		anchors.update(top=(0, -.28), bottom=(0, .28), left=(-.5025, 0), right=(.5025, 0),
			left_lobe=(-.27, 0), right_lobe=(.27, 0))
	return _shape(paths[kind], width, height, color, anchors, wall_color if kind == 'plant' else None)


#============================================
def nucleus(*, width: float, height: float, color: str) -> svg_tools.parts.SvgPart:
	"""Draw a nucleus without automatically adding nucleoli or chromosomes."""
	part = _oval(width, height, color)
	group = svg_tools._xml.parse(part.fragment)
	group.insert(1, lxml.etree.Element('ellipse', {
		'cx': '0', 'cy': '0', 'rx': str(.435 * width), 'ry': str(.435 * height),
		'fill': 'none', 'stroke-width': str(.5 * float(group.attrib['stroke-width']))}))
	return svg_tools.parts.SvgPart(lxml.etree.tostring(group, encoding='unicode'),
		part.bounds, part.anchors)


#============================================
def nucleolus(*, width: float, height: float, color: str) -> svg_tools.parts.SvgPart:
	"""Draw one nucleolus as a separate, caller-placed part."""
	return _oval(width, height, color)


#============================================
def _oval(width: float, height: float, color: str) -> svg_tools.parts.SvgPart:
	part = _shape('M 0 -0.48 C 0.265 -0.48 0.48 -0.265 0.48 0 C 0.48 0.265 0.265 0.48 0 0.48 C -0.265 0.48 -0.48 0.265 -0.48 0 C -0.48 -0.265 -0.265 -0.48 0 -0.48 Z',
		width, height, color, {'center': (0, 0), 'top': (0, -.48), 'bottom': (0, .48),
			'left': (-.48, 0), 'right': (.48, 0)})
	group = svg_tools._xml.parse(part.fragment)
	group.remove(group[0])
	group.insert(0, lxml.etree.Element('ellipse', {'cx': '0', 'cy': '0',
		'rx': str(.48 * width), 'ry': str(.48 * height), 'fill': color}))
	return svg_tools.parts.SvgPart(lxml.etree.tostring(group, encoding='unicode'),
		part.bounds, part.anchors)


#============================================
def _shape(path: str, width: float, height: float, color: str,
	anchors: dict[str, tuple[float, float]], wall_color: str | None = None) -> svg_tools.parts.SvgPart:
	if not all(math.isfinite(value) and value > 0 for value in (width, height)):
		raise ValueError('Width and height must be finite and positive')
	group = lxml.etree.Element('g', svg_tools._style.outline(width, height))
	shape = svg_tools._style.scaled_path(path, width, height)
	if wall_color is not None:
		lxml.etree.SubElement(group, 'path', {'d': shape, 'fill': wall_color})
		shape = svg_tools._style.scaled_path(path, .87 * width, .87 * height)
		lxml.etree.SubElement(group, 'path', {'d': shape, 'fill': color})
	else:
		lxml.etree.SubElement(group, 'path', {'d': shape, 'fill': color})
	# Inset highlights follow the edges and leave the interior available for parts.
	if 'left_lobe' in anchors:
		edges = ('M -.46 -.06 C -.45 -.31 -.31 -.43 -.16 -.38 L -.17 -.36 C -.31 -.40 -.42 -.28 -.43 -.06 Z M .08 -.34 C .25 -.45 .39 -.40 .44 -.20 L .42 -.20 C .36 -.38 .23 -.41 .09 -.31 Z',
			'M -.45 .16 C -.40 .38 -.22 .45 -.08 .32 L -.09 .30 C -.22 .41 -.37 .36 -.42 .16 Z M .08 .32 C .23 .45 .40 .38 .45 .16 L .42 .16 C .37 .36 .23 .41 .09 .30 Z')
	else:
		edges = ('M -.43 -.08 C -.43 -.30 -.25 -.44 0 -.44 L 0 -.41 C -.23 -.41 -.40 -.27 -.40 -.08 Z',
			'M -.34 .30 C -.18 .45 .17 .46 .35 .27 L .32 .26 C .15 .42 -.16 .42 -.32 .28 Z')
	for edge, shade, opacity in zip(edges, ('#ffffff', '#344651'), ('.60', '.18')):
		scale = .9 if wall_color is not None or anchors['top'][1] == -.43 else 1
		lxml.etree.SubElement(group, 'path', {
			'd': svg_tools._style.scaled_path(edge, scale * width, scale * height),
			'fill': shade, 'fill-opacity': opacity, 'stroke': 'none'})
	return svg_tools.parts.SvgPart(lxml.etree.tostring(group, encoding='unicode'),
		(-.5525 * width, -.5525 * height, .5525 * width, .5525 * height),
		{name: (x * width, y * height) for name, (x, y) in anchors.items()})


#============================================
def organelle(*, kind: str, width: float, height: float, color: str) -> svg_tools.parts.SvgPart:
	"""Draw a schematic organelle, centered at the origin, without a label.

	Kinds are mitochondrion, chloroplast, er, golgi, lysosome and vesicle.
	ER shows generic cisternae; it does not distinguish rough and smooth ER.
	Lysosome and vesicle are generic outlines; callers compose their contents.
	Cardinal anchors mark the body boundary, excluding stroke.
	"""
	features = {
		'mitochondrion': [
			'M -.44 0 C -.44 -.21 -.34 -.35 -.20 -.35 C -.04 -.35 .04 -.22 .19 -.27 C .33 -.32 .44 -.18 .44 0 C .44 .23 .24 .37 .02 .37 C -.23 .37 -.44 .24 -.44 0 Z',
			# A single closed matrix boundary leaves each crista lumen open to the intermembrane space.
			'M -.37 0 C -.37 -.13 -.33 -.24 -.27 -.27 C -.25 -.28 -.23 -.27 -.23 -.24 L -.21 .06 C -.21 .12 -.16 .13 -.16 .07 L -.17 -.19 C -.172 -.22 -.17 -.23 -.15 -.23 C -.12 -.23 -.09 -.21 -.085 -.205 C -.07 -.20 -.067 -.19 -.065 -.17 L -.045 .11 C -.04 .17 .01 .17 .005 .10 L -.005 -.15 C -.008 -.17 -.003 -.18 .015 -.18 C .065 -.175 .11 -.18 .14 -.195 C .155 -.20 .16 -.19 .165 -.17 L .19 .025 C .20 .09 .25 .09 .245 .015 L .225 -.175 C .22 -.195 .22 -.205 .24 -.205 C .30 -.20 .37 -.12 .37 0 C .37 .13 .29 .24 .20 .28 C .17 .29 .15 .30 .145 .30 C .13 .30 .13 .285 .127 .265 L .095 -.025 C .09 -.085 .04 -.085 .045 -.025 L .062 .25 C .065 .275 .065 .28 .05 .285 C .02 .30 0 .30 -.02 .29 C -.035 .285 -.036 .27 -.04 .25 L -.10 -.06 C -.11 -.115 -.16 -.10 -.15 -.045 L -.133 .23 C -.13 .25 -.13 .26 -.15 .255 C -.26 .24 -.37 .15 -.37 0 Z',
		],
		'chloroplast': [
			'M -.44 0 C -.44 -.22 -.25 -.35 0 -.35 C .25 -.35 .44 -.21 .44 0 C .44 .21 .24 .35 0 .35 C -.25 .35 -.44 .21 -.44 0 Z',
			'M -.38 0 C -.38 -.18 -.21 -.29 0 -.29 C .21 -.29 .38 -.18 .38 0 C .38 .18 .21 .29 0 .29 C -.21 .29 -.38 .18 -.38 0 Z',
		],
		'er': [
			'M -.45 -.29 C -.29 -.42 -.14 -.38 .01 -.30 C .17 -.22 .31 -.22 .44 -.31 C .48 -.34 .49 -.27 .45 -.24 C .31 -.13 .15 -.14 -.01 -.22 C -.18 -.30 -.30 -.32 -.43 -.21 C -.48 -.18 -.49 -.26 -.45 -.29 Z',
			'M -.45 -.09 C -.29 -.22 -.14 -.18 .01 -.10 C .17 -.02 .31 -.02 .44 -.11 C .48 -.14 .49 -.07 .45 -.04 C .31 .07 .15 .06 -.01 -.02 C -.18 -.10 -.30 -.12 -.43 -.01 C -.48 .02 -.49 -.06 -.45 -.09 Z',
			'M -.45 .11 C -.29 -.02 -.14 .02 .01 .10 C .17 .18 .31 .18 .44 .09 C .48 .06 .49 .13 .45 .16 C .31 .27 .15 .26 -.01 .18 C -.18 .10 -.30 .08 -.43 .19 C -.48 .22 -.49 .14 -.45 .11 Z',
			'M -.38 .29 C -.25 .20 -.12 .23 .01 .30 C .15 .37 .27 .36 .38 .28 C .42 .25 .44 .32 .40 .35 C .27 .44 .14 .45 -.01 .38 C -.16 .30 -.26 .29 -.36 .36 C -.40 .39 -.43 .32 -.38 .29 Z',
		],
		'golgi': [
			'M -.28 -.39 Q 0 -.24 .28 -.39 Q .34 -.42 .35 -.36 Q .35 -.33 .30 -.31 Q 0 -.16 -.30 -.31 Q -.35 -.33 -.35 -.36 Q -.34 -.42 -.28 -.39 Z',
			'M -.36 -.22 Q 0 -.06 .36 -.22 Q .42 -.25 .43 -.19 Q .43 -.16 .38 -.14 Q 0 .02 -.38 -.14 Q -.43 -.16 -.43 -.19 Q -.42 -.25 -.36 -.22 Z',
			'M -.40 -.03 Q 0 .13 .40 -.03 Q .46 -.06 .47 0 Q .47 .03 .42 .05 Q 0 .21 -.42 .05 Q -.47 .03 -.47 0 Q -.46 -.06 -.40 -.03 Z',
			'M -.34 .16 Q 0 .31 .34 .16 Q .40 .13 .41 .19 Q .41 .22 .36 .24 Q 0 .39 -.36 .24 Q -.41 .22 -.41 .19 Q -.40 .13 -.34 .16 Z',
		],
		'lysosome': [], 'vesicle': [],
	}
	if kind not in features:
		raise ValueError('Unknown organelle kind')
	part = _oval(width, height, color)
	if kind in ('lysosome', 'vesicle'):
		return part
	group = lxml.etree.Element('g', svg_tools._style.outline(width, height))
	stroke_width = float(group.attrib['stroke-width'])
	if kind == 'er':
		for bridge in (
			'M .41 -.29 Q .49 -.31 .48 -.24 L .48 -.10 Q .48 -.04 .41 -.05 Z',
			'M -.42 -.10 Q -.49 -.12 -.48 -.05 L -.48 .11 Q -.48 .18 -.42 .16 Z',
			'M .39 .10 Q .48 .08 .47 .16 L .44 .30 Q .43 .36 .37 .33 Z',
		):
			lxml.etree.SubElement(group, 'path', {
				'd': svg_tools._style.scaled_path(bridge, width, height), 'fill': color})
	for index, path in enumerate(features[kind]):
		attributes = {'d': svg_tools._style.scaled_path(path, width, height)}
		if kind in ('er', 'golgi') or index == 0:
			attributes['fill'] = color
		else:
			attributes.update(fill='none', **{'stroke-width': str(.5 * stroke_width)})
		if kind == 'mitochondrion':
			attributes['data-role'] = 'outer-membrane' if index == 0 else 'inner-membrane'
			if index == 1:
				attributes.update(fill='#ffffff', **{'fill-opacity': '.45'})
		if kind == 'chloroplast' and index == 1:
			attributes.update(fill='#ffffff', **{'fill-opacity': '.25'})
		lxml.etree.SubElement(group, 'path', attributes)
		if kind == 'mitochondrion' and index == 0:
			for plane, shade, opacity in (
				('M -.41 .09 C -.28 .31 .05 .33 .23 .25 C .36 .19 .40 .08 .40 -.06 C .44 .19 .25 .37 .02 .37 C -.20 .37 -.38 .25 -.41 .09 Z', '#344651', '.18'),
				('M -.415 -.04 C -.40 -.22 -.32 -.32 -.20 -.32 C -.09 -.32 -.01 -.25 .07 -.25 C -.06 -.28 -.10 -.30 -.20 -.30 C -.31 -.30 -.38 -.19 -.395 -.04 Z', '#ffffff', '.50'),
			):
				lxml.etree.SubElement(group, 'path', {
					'd': svg_tools._style.scaled_path(plane, width, height),
					'fill': shade, 'fill-opacity': opacity, 'stroke': 'none'})
	if kind == 'er':
		for join in ('M .415 -.265 L .465 -.265 M .415 -.08 L .465 -.08',
			'M -.465 -.075 L -.415 -.075 M -.465 .14 L -.415 .14',
			'M .405 .13 L .46 .13 M .39 .31 L .43 .31'):
			lxml.etree.SubElement(group, 'path', {
				'd': svg_tools._style.scaled_path(join, width, height), 'fill': 'none',
				'stroke': color, 'stroke-width': str(.03 * min(width, height))})
	if kind == 'chloroplast':
		# Narrow sacs connect the grana; all stack counts are schematic.
		for lamella in (
			'M -.24 .015 C -.14 .015 -.11 -.045 0 -.045 L 0 -.025 C -.11 -.025 -.14 .035 -.24 .035 Z',
			'M 0 .015 C .10 .015 .14 .035 .23 .035 L .23 .055 C .14 .055 .10 .035 0 .035 Z',
		):
			lxml.etree.SubElement(group, 'path', {
				'd': svg_tools._style.scaled_path(lamella, width, height),
				'fill': color, 'stroke-width': str(.4 * stroke_width),
				'data-role': 'stroma-lamella'})
		for x, top, count in ((-.23, -.11, 4), (0, -.17, 5), (.23, -.09, 4)):
			for layer in range(count):
				y = top + .06 * layer
				sac = (f'M {x - .075} {y} C {x - .075} {y - .022} {x + .075} {y - .022} {x + .075} {y} '
					f'L {x + .075} {y + .023} C {x + .075} {y + .047} {x - .075} {y + .047} {x - .075} {y + .023} Z')
				lxml.etree.SubElement(group, 'path', {
					'd': svg_tools._style.scaled_path(sac, width, height), 'fill': color,
					'stroke-width': str(.4 * stroke_width), 'data-role': 'thylakoid'})
				lxml.etree.SubElement(group, 'ellipse', {
					'cx': str(x * width), 'cy': str(y * height), 'rx': str(.075 * width),
					'ry': str(.018 * height), 'fill': '#ffffff', 'fill-opacity': '.30',
					'stroke-width': str(.3 * stroke_width)})
		for edge, shade, opacity in (
			('M -.405 -.03 C -.39 -.19 -.24 -.315 -.04 -.315', '#ffffff', '.65'),
			('M -.22 .285 C -.02 .36 .25 .29 .36 .14', '#344651', '.22'),
		):
			lxml.etree.SubElement(group, 'path', {
				'd': svg_tools._style.scaled_path(edge, width, height), 'fill': 'none',
				'stroke': shade, 'stroke-opacity': opacity,
				'stroke-width': str(.015 * min(width, height))})
	anchors = part.anchors.copy()
	if kind == 'mitochondrion':
		anchors.update(top=(-.20 * width, -.35 * height), bottom=(.02 * width, .37 * height),
			left=(-.44 * width, 0), right=(.44 * width, 0))
	elif kind == 'chloroplast':
		anchors.update(top=(0, -.35 * height), bottom=(0, .35 * height),
			left=(-.44 * width, 0), right=(.44 * width, 0))
	elif kind == 'er':
		anchors.update(top=(-.2323 * width, -.3741 * height), bottom=(.1773 * width, .4259 * height),
			left=(-.4812 * width, -.0661 * height), right=(.4811 * width, -.2544 * height))
	elif kind == 'golgi':
		anchors.update(top=(.3144 * width, -.40 * height), bottom=(0, .315 * height),
			left=(-.47 * width, 0), right=(.47 * width, 0))
	return svg_tools.parts.SvgPart(lxml.etree.tostring(group, encoding='unicode'),
		part.bounds, anchors)
