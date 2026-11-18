"""Schematic seed and radial wildflower parts for phenotype illustrations.

The radial flower is a generic wildflower, not realistic pea-flower anatomy.
Labels and any population or genetic interpretation belong to the caller.
"""

import math

import lxml.etree

import svg_tools.parts
import svg_tools._style


#============================================
def _size(size: float) -> None:
	if not math.isfinite(size) or size <= 0:
		raise ValueError('Size must be finite and positive')


#============================================
def _part(group: lxml.etree._Element, size: float) -> svg_tools.parts.SvgPart:
	# Bounds conservatively enclose the shapes and their strokes.
	radius = size * .56
	anchors = {'center': (0, 0), 'top': (0, -size*.5), 'bottom': (0, size*.5),
		'left': (-size*.5, 0), 'right': (size*.5, 0)}
	return svg_tools.parts.SvgPart(lxml.etree.tostring(group, encoding='unicode'),
		(-radius, -radius, radius, radius), anchors)


#============================================
def seed(*, size: float, color: str, shape: str = 'round') -> svg_tools.parts.SvgPart:
	"""Draw a round or visibly wrinkled seed centered at (0, 0)."""
	_size(size)
	if shape not in ('round', 'wrinkled'):
		raise ValueError('Shape must be round or wrinkled')
	group = lxml.etree.Element('g', {'fill': color, **svg_tools._style.outline(size, size)})
	if shape == 'round':
		path = ('M-73 -4 C-78 -45 -39 -78 2 -75 C48 -78 78 -38 74 5 '
			'C73 49 39 76 -4 76 C-48 76 -77 42 -73 -4 Z')
	else:
		path = ('M-68 -25 C-78 -48 -56 -69 -31 -62 C-12 -80 8 -63 25 -66 '
			'C50 -70 72 -45 64 -24 C82 -2 67 17 70 37 C73 66 41 72 21 61 '
			'C0 76 -18 62 -36 67 C-65 69 -76 47 -65 26 C-80 8 -63 -8 -68 -25 Z')
	lxml.etree.SubElement(group, 'path', {'d': svg_tools._style.scaled_path(path, size/150, size/150)})
	shadow = 'M-54 30 C-42 57 -12 67 18 62 C43 58 58 41 63 19 C46 42 25 48 2 49 C-21 50 -41 43 -54 30 Z'
	lxml.etree.SubElement(group, 'path', {
		'd': svg_tools._style.scaled_path(shadow, size/150, size/150),
		'fill': '#000000', 'fill-opacity': '.12', 'stroke': 'none'})
	highlight = 'M-58 -12 C-58 -40 -34 -59 -8 -60 C-31 -51 -48 -31 -58 -12 Z'
	lxml.etree.SubElement(group, 'path', {
		'd': svg_tools._style.scaled_path(highlight, size/150, size/150),
		'fill': 'white', 'fill-opacity': '.32', 'stroke': 'none'})
	if shape == 'wrinkled':
		lxml.etree.SubElement(group, 'path', {
			'd': svg_tools._style.scaled_path('M-42 -35 Q-20 -48 -18 -20 '
				'M17 -42 Q42 -35 34 -12 M-49 12 Q-44 35 -28 41 M4 10 Q29 17 25 41',
				size/150, size/150), 'fill': 'none'})
	return _part(group, size)


#============================================
def flower(*, size: float, color: str, petals: int = 5) -> svg_tools.parts.SvgPart:
	"""Draw a generic radial wildflower; this is not pea-flower anatomy."""
	_size(size)
	if isinstance(petals, bool) or not isinstance(petals, int) or petals < 3:
		raise ValueError('Petals must be an integer of at least three')
	group = lxml.etree.Element('g', svg_tools._style.outline(size, size))
	for index in range(petals):
		petal = lxml.etree.SubElement(group, 'g', {'transform': f'rotate({360 * index / petals})'})
		lxml.etree.SubElement(petal, 'ellipse', {'cx': '0', 'cy': str(-.27*size),
			'rx': str(.16*size), 'ry': str(.23*size), 'fill': color})
		lxml.etree.SubElement(petal, 'path', {
			'd': svg_tools._style.scaled_path('M -.10 -.31 Q -.10 -.45 0 -.47 Q -.055 -.42 -.10 -.31 Z', size, size),
			'fill': 'white', 'fill-opacity': '.3', 'stroke': 'none'})
	lxml.etree.SubElement(group, 'circle', {'cx': '0', 'cy': '0',
		'r': str(.12*size), 'fill': '#f4cf72'})
	return _part(group, size)
