"""Independent schematic cell envelopes and nuclear parts.

All parts are centered at the local origin. Internal parts are placed by the
caller; these silhouettes do not imply a cell-cycle stage or organelle count.
"""

import math
import xml.etree.ElementTree

import svg_tools.parts


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
	return _oval(width, height, color)


#============================================
def nucleolus(*, width: float, height: float, color: str) -> svg_tools.parts.SvgPart:
	"""Draw one nucleolus as a separate, caller-placed part."""
	return _oval(width, height, color)


#============================================
def _oval(width: float, height: float, color: str) -> svg_tools.parts.SvgPart:
	return _shape('M 0 -0.48 C 0.265 -0.48 0.48 -0.265 0.48 0 C 0.48 0.265 0.265 0.48 0 0.48 C -0.265 0.48 -0.48 0.265 -0.48 0 C -0.48 -0.265 -0.265 -0.48 0 -0.48 Z',
		width, height, color, {'center': (0, 0), 'top': (0, -.48), 'bottom': (0, .48),
			'left': (-.48, 0), 'right': (.48, 0)})


#============================================
def _shape(path: str, width: float, height: float, color: str,
	anchors: dict[str, tuple[float, float]], wall_color: str | None = None) -> svg_tools.parts.SvgPart:
	if not all(math.isfinite(value) and value > 0 for value in (width, height)):
		raise ValueError('Width and height must be finite and positive')
	group = xml.etree.ElementTree.Element('g', {'transform': f'scale({width} {height})',
		'fill': color, 'stroke': '#344651', 'stroke-width': '0.025',
		'stroke-linecap': 'round', 'stroke-linejoin': 'round'})
	if wall_color is not None:
		xml.etree.ElementTree.SubElement(group, 'path', {'d': path, 'fill': wall_color})
		xml.etree.ElementTree.SubElement(group, 'path', {'d': path, 'transform': 'scale(.87)', 'fill': color})
	else:
		xml.etree.ElementTree.SubElement(group, 'path', {'d': path})
	return svg_tools.parts.SvgPart(xml.etree.ElementTree.tostring(group, encoding='unicode'),
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
			'M 0 -.36 C .22 -.36 .40 -.20 .40 0 C .40 .20 .22 .36 0 .36 C -.22 .36 -.40 .20 -.40 0 C -.40 -.20 -.22 -.36 0 -.36 Z',
			'M -.26 -.27 C -.20 -.16 -.08 -.20 -.13 -.06 C -.16 .03 -.09 .07 -.06 .08',
			'M -.16 .33 C -.09 .22 -.18 .18 -.10 .13',
			'M .02 -.36 C .07 -.24 -.02 -.20 .05 -.11',
			'M .23 .29 C .15 .19 .28 .14 .20 .04 C .16 -.01 .13 -.02 .11 -.03',
		],
		'chloroplast': [
			'M -.29 -.16 H -.17 M -.29 -.08 H -.17 M -.29 0 H -.17 M -.29 .08 H -.17 M -.29 .16 H -.17',
			'M -.06 -.23 H .06 M -.06 -.15 H .06 M -.06 -.07 H .06 M -.06 .01 H .06 M -.06 .09 H .06 M -.06 .17 H .06',
			'M .17 -.16 H .29 M .17 -.08 H .29 M .17 0 H .29 M .17 .08 H .29 M .17 .16 H .29',
			'M -.17 -.08 H -.06 M .06 .09 H .17',
		],
		'er': [
			'M -.48 0 Q -.48 -.40 -.32 -.40 H .32 Q .48 -.40 .48 0 Q .48 .40 .32 .40 H -.32 Q -.48 .40 -.48 0 Z '
			'M -.36 -.28 Q -.39 -.28 -.39 -.22 Q -.39 -.16 -.36 -.16 H -.06 Q -.03 -.16 -.03 -.22 Q -.03 -.28 -.06 -.28 Z '
			'M .06 -.28 Q .03 -.28 .03 -.22 Q .03 -.16 .06 -.16 H .36 Q .39 -.16 .39 -.22 Q .39 -.28 .36 -.28 Z '
			'M -.36 -.06 Q -.39 -.06 -.39 0 Q -.39 .06 -.36 .06 H .13 Q .16 .06 .16 0 Q .16 -.06 .13 -.06 Z '
			'M .25 -.06 Q .22 -.06 .22 0 Q .22 .06 .25 .06 H .36 Q .39 .06 .39 0 Q .39 -.06 .36 -.06 Z '
			'M -.36 .16 Q -.39 .16 -.39 .22 Q -.39 .28 -.36 .28 H -.24 Q -.21 .28 -.21 .22 Q -.21 .16 -.24 .16 Z '
			'M -.12 .16 Q -.15 .16 -.15 .22 Q -.15 .28 -.12 .28 H .36 Q .39 .28 .39 .22 Q .39 .16 .36 .16 Z',
		],
		'golgi': [
			'M -.31 -.42 Q 0 -.25 .31 -.42 Q .35 -.39 .31 -.34 Q 0 -.17 -.31 -.34 Q -.35 -.39 -.31 -.42 Z',
			'M -.38 -.26 Q 0 -.09 .38 -.26 Q .42 -.23 .38 -.18 Q 0 -.01 -.38 -.18 Q -.42 -.23 -.38 -.26 Z',
			'M -.45 -.10 Q 0 .07 .45 -.10 Q .51 -.07 .45 -.02 Q 0 .15 -.45 -.02 Q -.51 -.07 -.45 -.10 Z',
			'M -.38 .06 Q 0 .23 .38 .06 Q .42 .09 .38 .14 Q 0 .31 -.38 .14 Q -.42 .09 -.38 .06 Z',
			'M -.31 .22 Q 0 .39 .31 .22 Q .35 .25 .31 .30 Q 0 .47 -.31 .30 Q -.35 .25 -.31 .22 Z',
		],
		'lysosome': [],
		'vesicle': [],
	}
	if kind not in features:
		raise ValueError('Unknown organelle kind')
	part = _oval(width, height, color)
	group = xml.etree.ElementTree.fromstring(part.fragment)
	if kind in ('er', 'golgi'):
		group.remove(group[0])
	for path in features[kind]:
		attributes = {'d': path}
		if kind == 'er':
			attributes['fill-rule'] = 'evenodd'
		if kind not in ('er', 'golgi'):
			attributes['fill'] = 'none'
		xml.etree.ElementTree.SubElement(group, 'path', attributes)
	anchors = part.anchors.copy()
	if kind == 'er':
		anchors.update(top=(0, -.40 * height), bottom=(0, .40 * height),
			left=(-.48 * width, 0), right=(.48 * width, 0))
	elif kind == 'golgi':
		anchors.update(top=(0, -.335 * height), bottom=(0, .385 * height),
			left=(-.48 * width, -.065 * height), right=(.48 * width, -.065 * height))
	return svg_tools.parts.SvgPart(xml.etree.ElementTree.tostring(group, encoding='unicode'),
		part.bounds, anchors)
