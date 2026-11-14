"""Schematic seed and radial wildflower parts for phenotype illustrations.

The radial flower is a generic wildflower, not realistic pea-flower anatomy.
Labels and any population or genetic interpretation belong to the caller.
"""

import math
import xml.etree.ElementTree

import svg_tools.parts


#============================================
def _size(size: float) -> None:
	if not math.isfinite(size) or size <= 0:
		raise ValueError('Size must be finite and positive')


#============================================
def _part(group: xml.etree.ElementTree.Element, size: float) -> svg_tools.parts.SvgPart:
	# Bounds conservatively enclose the scaled shapes and their strokes.
	radius = size * .56
	anchors = {'center': (0, 0), 'top': (0, -size*.5), 'bottom': (0, size*.5),
		'left': (-size*.5, 0), 'right': (size*.5, 0)}
	return svg_tools.parts.SvgPart(xml.etree.ElementTree.tostring(group, encoding='unicode'),
		(-radius, -radius, radius, radius), anchors)


#============================================
def seed(*, size: float, color: str, shape: str = 'round') -> svg_tools.parts.SvgPart:
	"""Draw a round or visibly wrinkled seed centered at (0, 0)."""
	_size(size)
	if shape not in ('round', 'wrinkled'):
		raise ValueError('Shape must be round or wrinkled')
	group = xml.etree.ElementTree.Element('g', {'transform': f'scale({size / 150})',
		'fill': color, 'stroke': '#344651', 'stroke-width': '3',
		'stroke-linecap': 'round', 'stroke-linejoin': 'round'})
	if shape == 'round':
		path = ('M-73 -4 C-78 -45 -39 -78 2 -75 C48 -78 78 -38 74 5 '
			'C73 49 39 76 -4 76 C-48 76 -77 42 -73 -4 Z')
	else:
		path = ('M-68 -25 C-78 -48 -56 -69 -31 -62 C-12 -80 8 -63 25 -66 '
			'C50 -70 72 -45 64 -24 C82 -2 67 17 70 37 C73 66 41 72 21 61 '
			'C0 76 -18 62 -36 67 C-65 69 -76 47 -65 26 C-80 8 -63 -8 -68 -25 Z')
	xml.etree.ElementTree.SubElement(group, 'path', {'d': path})
	if shape == 'wrinkled':
		xml.etree.ElementTree.SubElement(group, 'path', {'d': 'M-42 -35 Q-20 -48 -18 -20 '
			'M17 -42 Q42 -35 34 -12 M-49 12 Q-44 35 -28 41 M4 10 Q29 17 25 41',
			'fill': 'none', 'stroke-width': '4'})
	return _part(group, size)


#============================================
def flower(*, size: float, color: str, petals: int = 5) -> svg_tools.parts.SvgPart:
	"""Draw a generic radial wildflower; this is not pea-flower anatomy."""
	_size(size)
	if isinstance(petals, bool) or not isinstance(petals, int) or petals < 3:
		raise ValueError('Petals must be an integer of at least three')
	group = xml.etree.ElementTree.Element('g', {'transform': f'scale({size})',
		'stroke': '#344651', 'stroke-width': '.025', 'stroke-linejoin': 'round'})
	for index in range(petals):
		xml.etree.ElementTree.SubElement(group, 'ellipse', {'cx': '0', 'cy': '-.27',
			'rx': '.16', 'ry': '.23', 'fill': color,
			'transform': f'rotate({360 * index / petals})'})
	xml.etree.ElementTree.SubElement(group, 'circle', {'cx': '0', 'cy': '0',
		'r': '.12', 'fill': '#f4cf72'})
	return _part(group, size)
