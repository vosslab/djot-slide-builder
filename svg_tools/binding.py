"""Schematic binding parts with caller-authored contacts.

Anchors lie on the un-stroked silhouette; they are composition points, not
claims about molecular structure or affinity.
"""

import math

import lxml.etree

import svg_tools.parts
import svg_tools._style


#============================================
def _shape(path: str, highlight: str, shadow: str, width: float, height: float,
	color: str, anchors: dict[str, tuple[float, float]]) -> svg_tools.parts.SvgPart:
	if not all(math.isfinite(value) and value > 0 for value in (width, height)):
		raise ValueError('Width and height must be finite and positive')
	group = lxml.etree.Element('g', {'fill': color, **svg_tools._style.outline(width, height)})
	lxml.etree.SubElement(group, 'path', {
		'd': svg_tools._style.scaled_path(path, width, height)})
	lxml.etree.SubElement(group, 'path', {
		'd': svg_tools._style.scaled_path(shadow, width, height),
		'fill': '#000000', 'fill-opacity': '.12', 'stroke': 'none'})
	lxml.etree.SubElement(group, 'path', {
		'd': svg_tools._style.scaled_path(highlight, width, height),
		'fill': 'white', 'fill-opacity': '.22', 'stroke': 'none'})
	pad = .01 * min(width, height)
	return svg_tools.parts.SvgPart(lxml.etree.tostring(group, encoding='unicode'),
		(-.5*width-pad, -.5*height-pad, .5*width+pad, .5*height+pad),
		{name: (x*width, y*height) for name, (x, y) in anchors.items()})


#============================================
def antibody(*, width: float, height: float, color: str) -> svg_tools.parts.SvgPart:
	"""Draw an upright Y, with Fab tips above and the Fc terminal below."""
	return _shape('M -.5 -.43 L -.4 -.5 C -.31 -.38 -.12 -.19 0 -.10 '
		'C .12 -.19 .31 -.38 .4 -.5 L .5 -.43 C .38 -.29 .21 -.10 .10 .015 '
		'Q .08 .035 .08 .055 L .08 .5 L -.08 .5 L -.08 .055 '
		'Q -.08 .035 -.10 .015 C -.21 -.10 -.38 -.29 -.5 -.43 Z',
		'M -.46 -.43 L -.41 -.47 C -.30 -.32 -.15 -.17 -.035 -.07 '
		'L -.035 .43 L -.065 .43 L -.065 .025 C -.18 -.10 -.36 -.30 -.46 -.43 Z',
		'M .45 -.43 C .33 -.27 .18 -.10 .055 .025 L .055 .47 L .025 .47 L .025 .01 C .16 -.12 .34 -.32 .45 -.43 Z',
		width, height, color, {'center': (0, 0), 'Fab_left': (-.45, -.465),
			'Fab_right': (.45, -.465), 'Fc': (0, .50)})


#============================================
def antigen(*, width: float, height: float, color: str) -> svg_tools.parts.SvgPart:
	"""Draw an oval antigen with four explicit possible contact points."""
	return _shape('M 0 -.5 C .276 -.5 .5 -.276 .5 0 C .5 .276 .276 .5 0 .5 '
		'C -.276 .5 -.5 .276 -.5 0 C -.5 -.276 -.276 -.5 0 -.5 Z',
		'M -.38 -.12 C -.36 -.32 -.16 -.44 .07 -.42 C -.12 -.38 -.29 -.26 -.38 -.12 Z',
		'M -.40 .12 C -.31 .35 -.10 .45 .06 .44 C .28 .42 .42 .26 .46 .06 C .33 .29 .13 .36 -.06 .35 C -.20 .34 -.32 .25 -.40 .12 Z',
		width, height, color, {'center': (0, 0), 'top': (0, -.5), 'bottom': (0, .5),
			'left': (-.5, 0), 'right': (.5, 0)})


#============================================
def enzyme_tag(*, width: float, height: float, color: str) -> svg_tools.parts.SvgPart:
	"""Draw an oval enzyme tag with four explicit possible contact points."""
	return antigen(width=width, height=height, color=color)
