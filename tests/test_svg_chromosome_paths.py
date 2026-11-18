"""Authored chromatid bends preserve source regions and acentric ring topology."""

import lxml.etree
import pytest
import svgpathtools

import svg_tools.chromosomes
import svg_tools.parts
import svg_tools.chromosome_surface


#============================================
@pytest.mark.parametrize('thickness', [8, 62, 140])
def test_terminal_centromere_marker(thickness: float) -> None:
	"""The standalone labelable rectangle matches path centromere geometry."""
	c = svg_tools.chromosomes
	marker = c.centromere_part('terminal', thickness=thickness)
	rx, ry = thickness * 16 / 30, thickness * 13 / 20
	margin = thickness/30
	assert marker.bounds == pytest.approx((-rx-margin, -ry-margin, rx+margin, ry+margin))
	assert marker.anchors['center'] == (0, 0)
	assert marker.anchors['left'] == pytest.approx((-rx, 0))
	assert marker.anchors['right'] == pytest.approx((rx, 0))
	assert marker.anchors['top'] == pytest.approx((0, -ry))
	assert marker.anchors['bottom'] == pytest.approx((0, ry))
	for invalid in (0, -1, float('inf'), True):
		with pytest.raises(ValueError):
			c.centromere_part('terminal', thickness=invalid)
	with pytest.raises(ValueError):
		c.centromere_part('bad name')


#============================================
def test_curved_source_order_anchors_and_bounds() -> None:
	"""Rearranged source objects paint proportional spans with upright escaped labels."""
	c = svg_tools.chromosomes
	source = (c.Segment('A&B', '#D9C9EF', 20), c.Segment('B', '#00775F', 40),
		c.Segment('C', '#C1E7EE', 60))
	model = c.Chromosome((source[2], source[0], source[1]))
	drawing = 'M10 20 C60 -10 60 90 110 80 S160 20 210 40'
	part = c.chromosome_path_part('curve', model, drawing, thickness=24)
	lxml.etree.fromstring('<svg>' + part.fragment + '</svg>')
	root = lxml.etree.fromstring(part.fragment)
	regions = root.findall('.//g[@data-source-label]')
	assert [node.attrib['data-source-label'] for node in regions] == ['C', 'A&B', 'B']
	assert [node.find('path').attrib['stroke'] for node in regions] == [s.color for s in model.segments]
	assert [''.join(node.itertext()) for node in root.iter('text')] == ['C', 'A&B', 'B']
	path = svgpathtools.parse_path(drawing)
	for region, segment in zip(regions, model.segments):
		paint = svgpathtools.parse_path(region.find('path').attrib['d'])
		assert paint.length()/path.length() == pytest.approx(segment.length/120)
	assert part.anchors['start'] == (10, 20) and part.anchors['end'] == (210, 40)
	boundary = path.point(path.ilength(path.length()/2))
	assert part.anchors['boundary_1'] == pytest.approx((boundary.real, boundary.imag))
	xmin, xmax, ymin, ymax = path.bbox()
	assert part.bounds[0] < xmin-12 and part.bounds[2] > xmax+12
	assert part.bounds[1] < ymin-12 and part.bounds[3] > ymax+12
	assert model.segments[0] is source[2]


#============================================
def test_closed_ring_and_flat_internal_ends() -> None:
	"""A ring has a continuous outlined seam, ordered source paint and no false ends."""
	c = svg_tools.chromosomes
	model = c.Chromosome((c.Segment('B', '#8DBCE0', 3), c.Segment('P', '#C695D4', 1)))
	drawing = 'M0 -60 A60 60 0 1 1 0 60 A60 60 0 1 1 0 -60 Z'
	part = c.chromosome_path_part('ring', model, drawing, closed=True, labels=False)
	root = lxml.etree.fromstring(part.fragment)
	assert 'start' not in part.anchors and 'end' not in part.anchors
	assert part.anchors['boundary_0'] == part.anchors['boundary_2']
	assert all(svgpathtools.parse_path(outline.attrib['d']).isclosed()
		for outline in root.findall('./path'))
	assert [node.attrib['data-source-label'] for node in root.findall('.//g[@data-source-label]')] == ['B', 'P']
	assert part.bounds[0] < -74 and part.bounds[2] > 74
	cut = c.chromosome_path_part('cut', model, 'M0 0 L120 0', cut_ends=True)
	assert cut.anchors['start'] == (0, 0) and cut.anchors['end'] == (120, 0)


#============================================
def test_curved_centromere_and_rejected_topology() -> None:
	"""Centromere collars follow their source locus without narrowing a curve."""
	c = svg_tools.chromosomes
	segments = (c.Segment('A', '#D9C9EF'), c.Segment('B', '#C1E7EE'))
	model = c.Chromosome(segments, (c.Centromere(1), c.Centromere(0, active=False)))
	part = c.chromosome_path_part('neck', model, 'M0 0 Q75 70 150 0', labels=False)
	root = lxml.etree.fromstring(part.fragment)
	marker = root.find(".//*[@id='neck-centromere-0']")
	assert marker.get('data-layer') == 'centromere'
	inactive = root.find(".//*[@id='neck-centromere-1']")
	assert inactive.find('.//rect[@stroke-dasharray]') is not None
	assert part.anchors['centromere'] == pytest.approx((75, 35))
	assert [node.attrib['data-source-label'] for node in root.findall('.//g[@data-source-label]')] == ['A', 'B']
	for drawing, kwargs in (('', {}), ('M0 0 L10 0 M20 0 L30 0', {}),
		('M0 0 L0 0', {}), ('M0 0 L100 0 Z', {'closed': True}),
		('M0 0 L100 0', {'closed': True}), ('M0 0 L100 0', {'thickness': 0})):
		with pytest.raises(ValueError):
			c.chromosome_path_part('bad', c.Chromosome(segments), drawing, **kwargs)
	ring = 'M0 -60 A60 60 0 1 1 0 60 A60 60 0 1 1 0 -60 Z'
	for parent, kwargs in ((model, {'closed': True}),
		(c.Chromosome(segments), {'closed': True, 'cut_ends': True}),
		(c.Chromosome(segments), {})):
		with pytest.raises(ValueError):
			c.chromosome_path_part('bad', parent, ring, **kwargs)


#============================================
def test_source_projection_measures_distance_from_start() -> None:
	"""Source-region projection preserves left/right ancestry and endpoint caps."""
	path = svgpathtools.parse_path("M0 0 L1000 0")
	project = svg_tools.chromosome_surface.nearest_distance
	for distance in (0, 200, 800, 1000):
		assert project(path, complex(distance, 0)) == pytest.approx(distance, abs=.001)
	for drawing in ('M0 0 C0 160 60 0 140 0', 'M100 0 A100 100 0 0 1 0 100'):
		path = svgpathtools.parse_path(drawing)
		point = path.point(.7)
		assert project(path, point) == pytest.approx(path.length(0, .7), abs=.001)
