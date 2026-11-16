"""Authored chromatid bends preserve source regions and acentric ring topology."""

import xml.etree.ElementTree

import pytest
import svgpathtools

import svg_tools.chromosomes
import svg_tools.parts
import genetics.LECT06.djot.make_chromosome_meiosis


#============================================
@pytest.mark.parametrize('thickness', [8, 62, 140])
def test_terminal_centromere_marker(thickness: float) -> None:
	"""The standalone marker matches path markers and includes its painted stroke."""
	c = svg_tools.chromosomes
	marker = c.centromere_part('terminal', thickness=thickness)
	element = xml.etree.ElementTree.fromstring(marker.fragment)
	model = c.Chromosome((c.Segment('p', '#D9C9EF'), c.Segment('q', '#C1E7EE')), 1)
	internal = c.chromosome_path_part('internal', model, 'M0 0 L200 0',
		thickness=thickness, labels=False)
	reference = xml.etree.ElementTree.fromstring(internal.fragment).find('.//ellipse')
	for attr in ('rx', 'ry', 'fill', 'stroke', 'stroke-width'):
		assert element.attrib[attr] == reference.attrib[attr]
	rx, ry = float(element.attrib['rx']), float(element.attrib['ry'])
	margin = float(element.attrib['stroke-width'])/2
	assert marker.bounds == pytest.approx((-rx-margin, -ry-margin, rx+margin, ry+margin))
	assert marker.anchors == {'center': (0, 0), 'left': (-rx, 0), 'right': (rx, 0),
		'top': (0, -ry), 'bottom': (0, ry)}
	placed = svg_tools.parts.transform(marker, x=20, y=30, rotation=90)
	assert placed.anchors['center'] == pytest.approx((20, 30))
	assert placed.anchors['right'] == pytest.approx((20, 30+rx))

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
	xml.etree.ElementTree.fromstring('<svg>' + part.fragment + '</svg>')
	root = xml.etree.ElementTree.fromstring(part.fragment)
	regions = root.findall('./g')
	assert [node.attrib['data-source-label'] for node in regions] == ['C', 'A&B', 'B']
	assert [node.find('path').attrib['stroke'] for node in regions] == [s.color for s in model.segments]
	assert [node.text for node in root.iter('text')] == ['C', 'A&B', 'B']
	assert all('transform' not in node.attrib for node in root.iter('text'))
	path = svgpathtools.parse_path(drawing)
	for region, segment in zip(regions, model.segments):
		paint = svgpathtools.parse_path(region.find('path').attrib['d'])
		assert paint.length()/path.length() == pytest.approx(segment.length/120)
	assert part.anchors['start'] == (10, 20) and part.anchors['end'] == (210, 40)
	boundary = path.point(path.ilength(path.length()/2))
	assert part.anchors['boundary_1'] == pytest.approx((boundary.real, boundary.imag))
	assert sum(node.tag == 'circle' for node in root) == 2
	assert not root.findall('.//ellipse')
	assert svg_tools.parts.include_text_bounds(part.fragment, part.bounds) == part.bounds
	xmin, xmax, ymin, ymax = path.bbox()
	assert part.bounds[0] < xmin-12 and part.bounds[2] > xmax+12
	assert part.bounds[1] < ymin-12 and part.bounds[3] > ymax+12
	assert model.segments[0] is source[2] and part.fragment.isascii()


#============================================
def test_closed_ring_and_flat_internal_ends() -> None:
	"""A ring has a continuous outlined seam, ordered source paint and no false ends."""
	c = svg_tools.chromosomes
	model = c.Chromosome((c.Segment('B', '#8DBCE0', 3), c.Segment('P', '#C695D4', 1)))
	drawing = 'M0 -60 A60 60 0 1 1 0 60 A60 60 0 1 1 0 -60 Z'
	part = c.chromosome_path_part('ring', model, drawing, closed=True, labels=False)
	root = xml.etree.ElementTree.fromstring(part.fragment)
	assert not root.findall('.//circle') and not root.findall('.//ellipse')
	assert not root.findall('.//text')
	assert 'start' not in part.anchors and 'end' not in part.anchors
	assert part.anchors['boundary_0'] == part.anchors['boundary_2']
	for outline in root.findall('./path'):
		assert svgpathtools.parse_path(outline.attrib['d']).isclosed()
		assert outline.attrib['stroke-linecap'] == 'butt'
	assert [node.attrib['data-source-label'] for node in root.findall('./g')] == ['B', 'P']
	assert part.bounds == pytest.approx((-74.98, -74.98, 74.98, 74.98))
	cut = c.chromosome_path_part('cut', model, 'M0 0 L120 0', cut_ends=True)
	cut_root = xml.etree.ElementTree.fromstring(cut.fragment)
	assert not cut_root.findall('.//circle')
	assert all(node.attrib['stroke-linecap'] == 'butt' for node in cut_root.iter('path'))
	assert cut.anchors['start'] == (0, 0) and cut.anchors['end'] == (120, 0)


#============================================
def test_curved_centromere_and_rejected_topology() -> None:
	"""The known source locus gets one short neck and hollow purple marker only."""
	c = svg_tools.chromosomes
	segments = (c.Segment('A', '#D9C9EF'), c.Segment('B', '#C1E7EE'))
	model = c.Chromosome(segments, 1)
	part = c.chromosome_path_part('neck', model, 'M0 0 Q75 70 150 0', labels=False)
	root = xml.etree.ElementTree.fromstring(part.fragment)
	marker = root.find('.//ellipse')
	assert marker.attrib['fill'] == 'none' and marker.attrib['stroke'] == '#72508C'
	assert part.anchors['centromere'] == pytest.approx((75, 35))
	assert (float(marker.attrib['cx']), float(marker.attrib['cy'])) == part.anchors['centromere']
	assert len(root.findall('.//clipPath/path')) == 1
	assert [node.attrib['data-source-label'] for node in root.findall('./g/g')] == ['A', 'B']
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
	project = genetics.LECT06.djot.make_chromosome_meiosis.nearest_distance
	for distance in (0, 200, 800, 1000):
		assert project(path, complex(distance, 0)) == pytest.approx(distance, abs=.001)
