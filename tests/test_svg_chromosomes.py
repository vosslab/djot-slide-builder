"""Stable structural contracts for the chromosome drawing primitives."""

import defusedxml.ElementTree
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
	root = defusedxml.ElementTree.fromstring(part.fragment)
	regions = root.findall('.//g[@data-source-label]')
	assert [node.attrib['data-source-label'] for node in regions] == ['A', 'B', 'C']
	assert all(float(node.find('path').get('stroke-width')) == 24 for node in regions)
	body = root.find('./g[@data-layer="body"]')
	marker = root.find(".//*[@id='curve-centromere-0']")
	assert list(root).index(marker) > list(root).index(body)
	assert float(marker.find('.//rect').get('height')) > 24
	assert part.anchors['centromere'] == part.anchors['centromere_0']


def test_internal_gene_labels_retain_regions_without_decorative_texture() -> None:
	"""Gene regions and their labels remain legible when a recipe suppresses BPQ texture."""
	model = chromosomes.Chromosome((
		chromosomes.Segment('A', '#F3D788', 1),
		chromosomes.Segment('', '#D9C9EF', 1),
		chromosomes.Segment('b', '#00775F', 1),
	))
	part = chromosomes.chromosome_path_part('loci', model,
		'M0 0 C45 -25 75 25 120 0', thickness=24, texture=False)
	root = defusedxml.ElementTree.fromstring(part.fragment)
	regions = root.findall('.//g[@data-source-label]')
	assert [node.find('./path').get('stroke') for node in regions] == ['#F3D788', '#D9C9EF', '#00775F']
	labels = {node.text: node for node in root.findall('./text')}
	assert set(labels) == {'A', 'b'}
	assert labels['A'].get('fill') != labels['b'].get('fill')
	assert float(labels['A'].get('x')) == pytest.approx(part.anchors['segment_0'][0])
	assert float(labels['b'].get('x')) == pytest.approx(part.anchors['segment_2'][0])


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
	root = defusedxml.ElementTree.fromstring(compact.fragment)
	assert root.attrib['data-chromosome-state'] == 'condensed'
	assert root.find('./circle') is not None and root.find('./text').text == 'Xi'
def test_replication_keeps_each_chromatid_length_and_thickness() -> None:
	model = chromosomes.Chromosome((chromosomes.Segment('', '#8A7BC4', 20),
		chromosomes.Segment('', '#8A7BC4', 42)), (chromosomes.Centromere(1),))
	for sisters in (False, True):
		layout = chromosomes.render_chromosome_layout('replication', model,
			length=62, thickness=18, sisters=sisters, labels=False)
		root = defusedxml.ElementTree.fromstring(layout.svg)
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
