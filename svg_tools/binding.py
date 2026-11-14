"""Schematic binding parts with caller-authored contacts.

Anchors lie on the un-stroked silhouette; they are composition points, not
claims about molecular structure or affinity.
"""

import math
import xml.etree.ElementTree

import svg_tools.parts


#============================================
def _shape(tag: str, attributes: dict[str, str], width: float, height: float,
	color: str, anchors: dict[str, tuple[float, float]]) -> svg_tools.parts.SvgPart:
	if not all(math.isfinite(value) and value > 0 for value in (width, height)):
		raise ValueError('Width and height must be finite and positive')
	group = xml.etree.ElementTree.Element('g', {'transform': f'scale({width} {height})',
		'fill': color, 'stroke': '#344651', 'stroke-width': '0.025', 'stroke-linejoin': 'round'})
	xml.etree.ElementTree.SubElement(group, tag, attributes)
	return svg_tools.parts.SvgPart(xml.etree.ElementTree.tostring(group, encoding='unicode'),
		(-.5125*width, -.5125*height, .5125*width, .5125*height),
		{name: (x*width, y*height) for name, (x, y) in anchors.items()})


#============================================
def antibody(*, width: float, height: float, color: str) -> svg_tools.parts.SvgPart:
	"""Draw an upright Y, with Fab tips above and the Fc terminal below."""
	return _shape('path', {'d': 'M -0.5 -0.43 L -0.40 -0.50 L 0 -0.08 '
		'L 0.40 -0.50 L 0.5 -0.43 L 0.08 0.04 L 0.08 0.50 '
		'L -0.08 0.50 L -0.08 0.04 Z'}, width, height, color,
		{'center': (0, 0), 'Fab_left': (-.45, -.465),
			'Fab_right': (.45, -.465), 'Fc': (0, .50)})


#============================================
def antigen(*, width: float, height: float, color: str) -> svg_tools.parts.SvgPart:
	"""Draw an oval antigen with four explicit possible contact points."""
	return _shape('ellipse', {'cx': '0', 'cy': '0', 'rx': '.5', 'ry': '.5'},
		width, height, color, {'center': (0, 0), 'top': (0, -.5), 'bottom': (0, .5),
			'left': (-.5, 0), 'right': (.5, 0)})


#============================================
def enzyme_tag(*, width: float, height: float, color: str) -> svg_tools.parts.SvgPart:
	"""Draw an oval enzyme tag with four explicit possible contact points."""
	return _shape('ellipse', {'cx': '0', 'cy': '0', 'rx': '.5', 'ry': '.5'},
		width, height, color, {'center': (0, 0), 'top': (0, -.5), 'bottom': (0, .5),
			'left': (-.5, 0), 'right': (.5, 0)})
