"""Stable structural contracts for the chromosome drawing primitives."""

import xml.etree.ElementTree

import pytest

import svg_tools.chromosomes as chromosomes


def test_centromeres_are_independent_sites_with_activity() -> None:
	segments = (chromosomes.Segment('p', '#D9C9EF'), chromosomes.Segment('q', '#C1E7EE'))
	model = chromosomes.Chromosome(segments, (chromosomes.Centromere(0, active=False),
		chromosomes.Centromere(1, label='cen'), chromosomes.Centromere(2)))
	assert [site.after for site in model.centromeres] == [0, 1, 2]
	with pytest.raises(ValueError):
		chromosomes.Chromosome(segments, (chromosomes.Centromere(1), chromosomes.Centromere(1)))
	with pytest.raises(ValueError):
		chromosomes.Chromosome(segments, (chromosomes.Centromere(3),))


def test_curved_chromatid_keeps_width_and_source_order() -> None:
	model = chromosomes.Chromosome((
		chromosomes.Segment('A', '#D9C9EF', 2),
		chromosomes.Segment('B', '#00775F', 1),
		chromosomes.Segment('C', '#C1E7EE', 2)), (chromosomes.Centromere(1),))
	part = chromosomes.chromosome_path_part('curve', model,
		'M0 0 C35 -55 85 55 120 0', thickness=24)
	root = xml.etree.ElementTree.fromstring(part.fragment)
	regions = root.findall('.//g[@data-source-label]')
	assert [node.attrib['data-source-label'] for node in regions] == ['A', 'B', 'C']
	assert all(float(node.find('path').get('stroke-width')) == 24 for node in regions)
	body = root.find('./g[@data-layer="body"]')
	assert [node.get('data-layer') for node in body if node.get('data-layer')] == [
		'texture', 'sheen', 'inset-shadows', 'telomere', 'telomere', 'outline']
	marker = root.find(".//*[@id='curve-centromere-0']")
	assert list(root).index(marker) > list(root).index(body)
	assert float(marker.find('.//rect').get('height')) > 24
	assert part.anchors['centromere'] == part.anchors['centromere_0']


def test_independent_sisters_and_compaction_keep_models() -> None:
	first = chromosomes.Chromosome((chromosomes.Segment('A', '#D9C9EF'),
		chromosomes.Segment('B', '#C1E7EE')), (chromosomes.Centromere(1),))
	second = chromosomes.Chromosome((chromosomes.Segment('A', '#D9C9EF'),
		chromosomes.Segment('b', '#00775F')), (chromosomes.Centromere(1),))
	paired = chromosomes.sister_chromatid_parts('pair', ((first, 'M0 0 C35 0 65 0 100 0'),
		(second, 'M0 30 C35 30 65 30 100 30')), thickness=16)
	assert {'sister0.centromere', 'sister1.centromere'} <= set(paired.anchors)
	assert 'data-source-label="b"' in paired.fragment
	compact = chromosomes.condensed_chromosome_part('barr', first, radius=18, label='Xi')
	root = xml.etree.ElementTree.fromstring(compact.fragment)
	assert root.attrib['data-chromosome-state'] == 'condensed'
	assert root.find('./circle') is not None and root.find('./text').text == 'Xi'


def test_layout_exposes_real_sister_geometry_and_bounds() -> None:
	model = chromosomes.Chromosome((chromosomes.Segment('a+', '#D9C9EF'),
		chromosomes.Segment('b-', '#C1E7EE')), (chromosomes.Centromere(1, label='cen'),))
	layout = chromosomes.render_chromosome_layout('straight', model, length=40,
		thickness=30, sisters=True, allele_labels=True, marker_size=(12, 20))
	assert len(layout.segments) == 4
	assert layout.segments[0].start != layout.segments[2].start
	assert layout.centromere == pytest.approx(((layout.segments[0].end[0]+layout.segments[2].end[0])/2,
		(layout.segments[0].end[1]+layout.segments[2].end[1])/2))
	part = chromosomes.chromosome_part('bounds', model, length=40, thickness=30,
		marker_size=(12, 38))
	assert part.bounds[1] < 0 and part.bounds[3] > 30


def test_replication_keeps_each_chromatid_length_and_thickness() -> None:
	model = chromosomes.Chromosome((chromosomes.Segment('', '#8A7BC4', 20),
		chromosomes.Segment('', '#8A7BC4', 42)), (chromosomes.Centromere(1),))
	for sisters in (False, True):
		layout = chromosomes.render_chromosome_layout('replication', model,
			length=62, thickness=18, sisters=sisters, labels=False)
		root = xml.etree.ElementTree.fromstring(layout.svg)
		regions = root.findall('.//g[@data-source-label]')
		assert len(regions) == (4 if sisters else 2)
		assert all(float(node.find('path').get('stroke-width')) == 18 for node in regions)
		for copy in range(2 if sisters else 1):
			first, last = layout.segments[copy*2:copy*2+2]
			assert last.end[0]-first.start[0] == pytest.approx(62)
		if sisters:
			belt = root.find('.//g[@data-layer="centromere"]')
			assert float(belt.find('.//rect').get('height')) > 18*2.2


def test_bent_surface_keeps_normal_width_at_different_sizes() -> None:
	"""Bending and resizing cannot pinch the painted chromosome envelope."""
	import svgpathtools
	from svg_tools.chromosome_surface import Surface
	path = svgpathtools.parse_path('M0 0 C60 -80 120 80 180 0')
	for width in (8, 30, 62):
		surface = Surface(path, width)
		for fraction in (.1, .25, .5, .75, .9):
			distance = surface.length*fraction
			assert abs(surface.point(distance, width/2)-surface.point(distance, -width/2)) == pytest.approx(width)


def test_hard_corner_keeps_each_straight_arm_normal_and_outline_offsets() -> None:
	"""C62-style corners retain both perpendicular surface offsets, not a long wedge."""
	import svgpathtools
	from svg_tools.chromosome_surface import Surface
	path = svgpathtools.parse_path('M233 460 L233 307 L80 307')
	surface = Surface(path, 10)
	for distance, tangent in ((76.5, -1j), (229.5, -1)):
		upper = surface.point(distance, 5)
		lower = surface.point(distance, -5)
		offset = upper-lower
		assert abs(offset) == pytest.approx(10)
		assert (offset/tangent).real == pytest.approx(0, abs=1e-10)
	outline = surface.envelope(cut=True)
	for point in ('228.0000,307.0000', '233.0000,312.0000',
		'233.0000,302.0000', '238.0000,307.0000'):
		assert point in outline


def test_long_curved_chromosome_stays_compact_and_follows_its_centerline() -> None:
	"""Repeated surface coordinates must not turn one thin rod into megabytes of SVG."""
	import svgpathtools
	import svg_tools.chromosome_surface
	drawing = 'M0 0 C300 -120 600 120 900 0'
	path = svgpathtools.parse_path(drawing)
	width = 4
	surface = svg_tools.chromosome_surface.Surface(path, width)
	for index in range(101):
		distance = path.length()*index/100
		parameter = path.ilength(distance)
		for side in (-1, 1):
			expected = path.point(parameter) + path.unit_tangent(parameter)*1j*side*width/2
			assert abs(surface.point(distance, side*width/2)-expected) < width*.02
	model = chromosomes.Chromosome((chromosomes.Segment('', '#087faf'),))
	part = chromosomes.chromosome_path_part('long_curve', model, drawing,
		thickness=width, labels=False, bands=False)
	assert len(part.fragment.encode('ascii')) < 500_000
