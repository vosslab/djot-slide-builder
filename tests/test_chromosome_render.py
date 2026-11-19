"""Source-backed chromosomes keep material and annotations through BPQ painting."""

import lxml.etree
import pytest
import svgpathtools

import svg_tools.chromosome_topology as topology
import svg_tools.chromosomes as chromosomes


#============================================
def test_recolor_keeps_geometry_and_source_positioned_features() -> None:
	model = topology.chromosome('A', length=120, centromere=.43,
		genes={'rb+': .24, 'm': .81}, regions=((0, 'body'), (.65, 'band')))
	points = ((10, 20), (55, 29), (115, 18))
	first = chromosomes.render('A', model, points=points, width=16, scale=1.5,
		palette={('A', 'body'): '#00775F', ('A', 'band'): '#C1E7EE'})
	second = chromosomes.render('A', model, points=points, width=16, scale=1.5,
		palette={('A', 'body'): '#835BB2', ('A', 'band'): '#F0BDD2'},
		centromere_styles={('A', 'A.cen'): chromosomes.CentromereStyle(label='2', fill='#FFE7DE')})
	assert first.anchors == second.anchors
	assert first.bounds == second.bounds
	styled_root = lxml.etree.fromstring(second.fragment)
	collar = styled_root.find('./g[@data-layer="centromere"]')
	label = collar.find('text')
	assert label.text == '2'
	angle = float(collar.attrib['transform'].split('rotate(')[1][:-1])
	assert angle != 0
	assert label.attrib['transform'] == f'rotate({-angle})'
	assert collar.find('./g/rect').attrib['fill'] == '#FFE7DE'
	root = lxml.etree.fromstring(first.fragment)
	body = root.find('./g[@data-layer="body"]')
	path = svgpathtools.parse_path(body.find('./path').attrib['d'])
	assert path.length() == pytest.approx(180)
	assert first.anchors['start'] == (10, 20)
	for anchor, fraction in (('center', .5), ('centromere', .43), ('gene_rb+', .24), ('gene_m', .81)):
		point = path.point(path.ilength(path.length()*fraction))
		assert first.anchors[anchor] == pytest.approx((point.real, point.imag), abs=1e-7)
	assert first.anchors['centromere'] == first.anchors['centromere_0']
	assert first.anchors['gene_rb+'] == first.anchors['gene:A/A/rb%2B']
	regions = body.findall('./g[@data-source-label]')
	assert {node.attrib['data-source-label'] for node in regions} == {'A/body', 'A/band'}
	assert {node.find('path').attrib['stroke'] for node in regions} == {'#00775F', '#C1E7EE'}
	locus = root.find('./g[@data-gene="rb+"]')
	assert ''.join(locus.find('text').itertext()) == 'rb+'
	assert len(body.findall('./path[@data-layer="telomere"]')) == 2


#============================================
def test_split_fragment_has_only_its_native_end_cap() -> None:
	model = topology.chromosome('A', length=100)
	pieces = topology.split(model, .4)
	for fragment, cap_side in zip(pieces, ('left', 'right')):
		part = chromosomes.render('fragment', fragment, points=((0, 0), (100, 0)),
			palette={('A', 'body'): '#3479A8'})
		root = lxml.etree.fromstring(part.fragment)
		cap, = root.findall('.//path[@data-layer="telomere"]')
		cap_left, cap_right, _, _ = svgpathtools.parse_path(cap.attrib['d']).bbox()
		outline = root.find('.//path[@data-layer="outline"]')
		edge = max(svgpathtools.parse_path(outline.attrib['d']), key=lambda segment: abs(segment.end.imag-segment.start.imag))
		if cap_side == 'left':
			assert cap_left == 0
			assert edge.start.real == edge.end.real == fragment.length
		else:
			assert cap_right == fragment.length
			assert edge.start.real == edge.end.real == 0


#============================================
def test_ring_preserves_material_and_has_a_seamless_outline() -> None:
	left = topology.chromosome('A', length=100, genes={'q+': .4})
	right = topology.chromosome('B', length=100, genes={'m': .6})
	_, left = topology.split(left, .2)
	_, right = topology.split(right, .2)
	left, _ = topology.split(left, .75)
	right, _ = topology.split(right, .75)
	model = topology.join(topology.reverse(left), topology.reverse(right))
	palette = {('A', 'body'): '#3479A8', ('B', 'body'): '#D6533C'}
	part = chromosomes.render_ring('ring', model, center=(150, 90), width=14,
		scale=2, palette=palette)
	root = lxml.etree.fromstring(part.fragment)
	body = root.find('./g[@data-layer="body"]')
	path = svgpathtools.parse_path(body.find('./path').get('d'))
	assert path.isclosed() and path.length() == pytest.approx(model.length*2)
	assert part.anchors['center'] == pytest.approx((150, 90))
	assert part.anchors['boundary_0'] == part.anchors['boundary_2']
	assert 'start' not in part.anchors and 'end' not in part.anchors
	assert 'centromere' not in part.anchors and body.find('./path[@data-layer="telomere"]') is None
	assert [band.get('data-source-label') for band in body.findall('./g[@data-source-label]')] == ['A/body', 'B/body']
	for anchor, fraction in (('gene:A/A/q%2B', 1/3), ('gene:B/B/m', 2/3)):
		point = path.point(path.ilength(path.length()*fraction))
		assert part.anchors[anchor] == pytest.approx((point.real, point.imag))
