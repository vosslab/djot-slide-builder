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
	assert locus.find('path').attrib['fill'] == '#FFD080'
	assert [span.text for span in locus.iter('tspan')] == ['rb', '+']
	assert len(body.findall('./path[@data-layer="telomere"]')) == 2


#============================================
@pytest.mark.parametrize('paired', (False, True))
def test_texture_switch_preserves_source_bands_and_shading(paired: bool) -> None:
	chromatid = topology.chromosome('A', length=180, centromere=.5, regions=((0, 'body'), (.7, 'band')))
	model = topology.replicate(chromatid) if paired else chromatid
	palette = {('A', 'body'): '#3479A8', ('A', 'band'): '#D6533C'}
	points = ((0, 0), (180, 0))
	textured = lxml.etree.fromstring(chromosomes.render('bands', model, points=points, palette=palette).fragment)
	part = chromosomes.render('bands', model, points=points, palette=palette, texture=False)
	untextured = lxml.etree.fromstring(part.fragment)
	textures = textured.findall('.//g[@data-layer="texture"]')
	assert len(textures) == (2 if paired else 1)
	assert not untextured.findall('.//g[@data-layer="texture"]')
	for texture in textures:
		texture.getparent().remove(texture)
	assert lxml.etree.tostring(untextured) == lxml.etree.tostring(textured)
	for body in untextured.findall('.//g[@data-layer="body"]'):
		bands = body.findall('./g[@data-source-label]/path')
		assert [band.get('stroke') for band in bands] == list(palette.values())
		assert body.find('./g[@data-layer="sheen"]/path') is not None


#============================================
def test_adjacent_same_color_bands_share_one_stroke() -> None:
	model = topology.chromosome('A', length=200,
		regions=((0, 'a'), (.2, 'b'), (.4, 'c'), (.6, 'd'), (.8, 'e')))
	palette = {('A', band): color for band, color in zip('abcde',
		('#AAAAAA', '#aaaaaa', '#752499', '#AAAAAA', '#AAAAAA'))}
	part = chromosomes.render('bands', model, points=((0, 0), (200, 0)), palette=palette)
	root = lxml.etree.fromstring(part.fragment)
	regions = root.findall('./g[@data-layer="body"]/g[@data-source-label]')
	assert [region.get('data-source-label') for region in regions] == [f'A/{band}' for band in 'abcde']
	strokes = root.findall('./g[@data-layer="body"]/g[@data-source-label]/path')
	assert [stroke.get('stroke') for stroke in strokes] == ['#AAAAAA', '#752499', '#AAAAAA']
	paths = [svgpathtools.parse_path(stroke.get('d')) for stroke in strokes]
	assert [(path.start.real, path.end.real) for path in paths] == [(0, 80), (80, 120), (120, 200)]
	assert [part.anchors[f'boundary_{index}'] for index in range(6)] == [(x, 0) for x in range(0, 201, 40)]


#============================================
def test_internal_gene_borders_leave_body_color_at_both_telomeres() -> None:
	model = topology.chromosome('A', length=100, genes={'a': .16, 'b': .84})
	part = chromosomes.render('ends', model, points=((0, 0), (100, 0)), width=20,
		palette={('A', 'body'): '#3479A8'})
	root = lxml.etree.fromstring(part.fragment)
	left, right = [svgpathtools.parse_path(cap.attrib['d']).bbox()[:2]
		for cap in root.findall('.//path[@data-layer="telomere"]')]
	for allele, cap in (('a', left), ('b', right)):
		card = root.find(f'./g[@data-gene="{allele}"]/path')
		start, end, _, _ = svgpathtools.parse_path(card.attrib['d']).bbox()
		gap = start-cap[1] if allele == 'a' else cap[0]-end
		ink_gap = gap - float(card.attrib['stroke-width'])/2
		assert ink_gap >= cap[1]-cap[0] - 1e-3


#============================================
def test_internal_gene_borders_leave_body_color_beside_the_centromere() -> None:
	model = topology.chromosome('A', length=200, centromere=.5, genes={'a': .32, 'b': .68})
	part = chromosomes.render('collar', model, points=((0, 0), (200, 0)), width=30,
		palette={('A', 'body'): '#3479A8'})
	root = lxml.etree.fromstring(part.fragment)
	border = root.find('./g[@data-layer="centromere"]/rect')
	collar_half = (float(border.attrib['width']) + float(border.attrib['stroke-width']))/2
	for allele, side in (('a', -1), ('b', 1)):
		card = root.find(f'./g[@data-gene="{allele}"]/path')
		start, end, _, _ = svgpathtools.parse_path(card.attrib['d']).bbox()
		edge = end if side < 0 else start
		ink_gap = side * (edge - 100) - collar_half - float(card.attrib['stroke-width'])/2
		assert ink_gap >= 8 - 1e-3


#============================================
def test_sisters_keep_both_copies_under_one_foreground_belt() -> None:
	model = topology.replicate(topology.chromosome('A', length=110, centromere=.44,
		genes={'rb': .80}))
	part = chromosomes.render('sisters', model, points=((4, 9), (49, 20), (100, 8)),
		width=16, palette={('A', 'body'): '#835BB2'},
		centromere_styles={('A', 'A.cen'): chromosomes.CentromereStyle(fill='#E1F3FE')})
	root = lxml.etree.fromstring(part.fragment)
	bodies = root.findall('.//g[@data-layer="body"]')
	paths = [svgpathtools.parse_path(body.find('./path').attrib['d']) for body in bodies]
	assert [path.length() for path in paths] == pytest.approx([110, 110])
	assert [float(body.find('./path').attrib['stroke-width']) for body in bodies] == [16, 16]
	assert len(root.findall('.//g[@data-gene="rb"]')) == 2
	assert part.anchors['first.gene_rb'] == part.anchors['first.gene:A/A.s1/rb']
	assert part.anchors['second.gene_rb'] == part.anchors['second.gene:A/A.s2/rb']
	first = part.anchors['first.centromere']
	second = part.anchors['second.centromere']
	offset = complex(second[0]-first[0], second[1]-first[1])
	assert abs(offset) == pytest.approx(16*1.2)
	for prefix, path, shift in zip(('first', 'second'), paths, (-offset/2, offset/2)):
		point = path.point(path.ilength(path.length()*.80)) + shift
		assert part.anchors[f'{prefix}.gene_rb'] == pytest.approx((point.real, point.imag), abs=1e-7)
	tangent = paths[0].unit_tangent(paths[0].ilength(110*.44))
	assert (offset * tangent.conjugate()).real == pytest.approx(0, abs=1e-9)
	assert part.anchors['centromere'] == pytest.approx(tuple((a+b)/2 for a, b in zip(first, second)))
	belt, = root.findall('.//g[@data-layer="centromere"]')
	assert float(belt.find('.//rect').attrib['height']) > 16*2.2
	assert belt.find('./g/rect').attrib['fill'] == '#E1F3FE'
	assert belt.find('text') is None
	order = list(root.iter())
	assert all(order.index(body) < order.index(belt) for body in bodies)


#============================================
def test_fusion_paints_one_walk_with_only_outer_caps() -> None:
	_, a = topology.split(topology.chromosome('A', length=100, centromere=.25), .25)
	_, b = topology.split(topology.chromosome('B', length=80, centromere=.25), .25)
	b = topology.with_centromere_activity(b, 'B.cen', active=False)
	product = topology.join(topology.reverse(a), b)
	palette = {('A', 'body'): '#3479A8', ('B', 'body'): '#D6533C'}
	points = ((0, 0), (90, 0))
	part = chromosomes.render('fusion', product, points=points, palette=palette)
	root = lxml.etree.fromstring(part.fragment)
	body, = root.findall('.//g[@data-layer="body"]')
	assert svgpathtools.parse_path(body.find('path').attrib['d']).length() == 135
	assert [node.attrib['data-source-label'] for node in body.findall('./g[@data-source-label]')] == [
		'A/body', 'B/body']
	assert len(body.findall('./path[@data-layer="telomere"]')) == 2
	assert len(root.findall('./g[@data-layer="centromere"]')) == 1
	assert part.anchors['centromere'] == pytest.approx((75, 0))
	inactive = topology.with_centromere_activity(product, 'A.cen', active=False)
	part = chromosomes.render('fusion', inactive, points=points, palette=palette)
	root = lxml.etree.fromstring(part.fragment)
	mark, = root.findall('./path')
	assert svgpathtools.parse_path(mark.attrib['d']).bbox()[:2] == pytest.approx((73, 77))
	assert 'centromere' not in part.anchors


#============================================
def test_junction_marks_clear_telomeres_cut_outlines_and_collars() -> None:
	a = topology.chromosome('A', length=100)
	b = topology.chromosome('B', length=80)
	palette = {('A', 'body'): '#3479A8', ('B', 'body'): '#D6533C'}
	left, _ = topology.split(a, .06)
	_, tip = topology.split(a, .99)
	product = topology.join(left, b, topology.copy(b, 'B2'), topology.reverse(tip))
	part = chromosomes.render('product', product, points=((0, 0), (product.length, 0)),
		palette=palette)
	root = lxml.etree.fromstring(part.fragment)
	assert product.junctions == (6, 86, 166)
	mark, = root.findall('./path')
	mark_left, mark_right, _, _ = svgpathtools.parse_path(mark.attrib['d']).bbox()
	assert mark_left < 86 < mark_right
	assert mark_left > 6 and mark_right < 166

	_, right = topology.split(a, .5)
	cut, _ = topology.split(right, .05)
	near_collar = topology.chromosome('A', length=100, centromere=.89)
	mark_counts = []
	for first in (cut, near_collar):
		product = topology.join(first, b)
		part = chromosomes.render('product', product, points=((0, 0), (product.length, 0)),
			palette=palette)
		root = lxml.etree.fromstring(part.fragment)
		mark_counts.append(len(root.findall('./path')))
	assert mark_counts == [0, 0]


#============================================
def test_joined_terminal_centromeres_share_ink_and_retain_both_anchors() -> None:
	left = topology.chromosome('A', length=80, centromere=1)
	right = topology.chromosome('B', length=80, centromere=0)
	part = chromosomes.render('joined', topology.join(left, right), points=((0, 0), (160, 0)),
		palette={('A', 'body'): '#3479A8', ('B', 'body'): '#D6533C'})
	root = lxml.etree.fromstring(part.fragment)
	assert part.anchors['centromere'] == part.anchors['centromere_0'] == part.anchors['centromere_1'] == (80, 0)
	assert len(root.findall('./g[@data-layer="centromere"]')) == 1


#============================================
def test_collar_at_rounded_region_boundary_preserves_both_regions() -> None:
	model = topology.chromosome('A', length=100, centromere=.1+.2, regions=((0, 'p'), (.3, 'q')))
	part = chromosomes.render('curve', model, points=((0, 0), (40, 10), (100, 0)),
		palette={('A', 'p'): '#3479A8', ('A', 'q'): '#D6533C'})
	root = lxml.etree.fromstring(part.fragment)
	regions = root.findall('./g[@data-layer="body"]/g[@data-source-label]')
	assert [region.get('data-source-label') for region in regions] == ['A/p', 'A/q']
	boundary = svgpathtools.parse_path(regions[0].find('path').get('d')).end
	assert part.anchors['centromere'] == pytest.approx((boundary.real, boundary.imag))


#============================================
def test_bent_junction_glyph_clears_collar_at_same_material_spacing() -> None:
	left = topology.chromosome('A', length=63.4, centromere=50/63.4)
	product = topology.join(left, topology.chromosome('B', length=56.6))
	counts = []
	for points in (((0, 0), (120, 0)), ((0, 0), (37, 0), (61, 17), (61, 70))):
		part = chromosomes.render('product', product, points=points,
			palette={('A', 'body'): '#3479A8', ('B', 'body'): '#D6533C'})
		root = lxml.etree.fromstring(part.fragment)
		counts.append(len(root.findall('./path[@fill="#FFFFFF"]')))
	assert counts == [1, 0]


#============================================
def test_long_alleles_get_readable_external_labels_at_their_loci() -> None:
	model = topology.chromosome('A', length=180, genes={'eyeless+': .25, 'Notch+': .75})
	part = chromosomes.render('alleles', model, points=((0, 0), (180, 0)),
		palette={('A', 'body'): '#3479A8'}, allow_external_genes=True)
	root = lxml.etree.fromstring(part.fragment)
	for allele, x in (('eyeless+', 45), ('Notch+', 135)):
		locus = root.find(f'./g[@data-gene="{allele}"]')
		assert part.anchors[f'gene_{allele}'] == (x, 0)
		assert locus.find('.//polyline') is not None
		label = locus.find('.//text')
		assert ''.join(label.itertext()) == allele
		assert float(label.get('font-size')) >= 8


#============================================
def test_gene_at_visible_junction_keeps_its_label_and_ancestry_boundary() -> None:
	a = topology.chromosome('A', length=100)
	b = topology.chromosome('B', length=80, genes={'q': .5})
	_, tip = topology.split(b, .5)
	product = topology.join(a, tip)
	part = chromosomes.render('product', product, points=((0, 0), (140, 0)),
		palette={('A', 'body'): '#3479A8', ('B', 'body'): '#D6533C'}, allow_external_genes=True)
	root = lxml.etree.fromstring(part.fragment)
	assert part.anchors['gene:B/B/q'] == part.anchors['gene_q'] == (100, 0)
	locus, = root.findall('./g[@data-gene="q"]')
	assert locus.find('circle') is not None
	assert locus.find('.//polyline') is not None
	assert ''.join(locus.find('.//text').itertext()) == 'q'
	mark, = root.findall('./path[@fill="#FFFFFF"]')
	assert svgpathtools.parse_path(mark.attrib['d']).bbox()[:2] == (98, 102)
	regions = root.findall('./g[@data-layer="body"]/g[@data-source-label]')
	assert [region.attrib['data-source-label'] for region in regions] == ['A/body', 'B/body']


#============================================
def test_gene_card_needs_room_beside_junction_and_retains_its_fill() -> None:
	left = topology.chromosome('A', length=100, genes={'q': .87})
	right = topology.chromosome('B', length=80, genes={'q': .5})
	product = topology.join(left, right)
	points = ((0, 0), (180, 0))
	palette = {('A', 'body'): '#3479A8', ('B', 'body'): '#D6533C'}
	with pytest.raises(ValueError, match="product: gene 'q' cannot fit an internal card"):
		chromosomes.render('product', product, points=points, width=38, palette=palette)

	part = chromosomes.render('product', product, points=points, scale=2.5, width=38, palette=palette,
		gene_palette={('A', 'q'): '#EFD1FA', ('B', 'q'): '#E6FFCC'})
	root = lxml.etree.fromstring(part.fragment)
	cards = root.findall('./g[@data-layer="gene-locus"]/path')
	assert [card.get('fill') for card in cards] == ['#EFD1FA', '#E6FFCC']
	_, card_end, _, _ = svgpathtools.parse_path(cards[0].get('d')).bbox()
	mark, = root.findall('./path[@fill="#FFFFFF"]')
	mark_start, _, _, _ = svgpathtools.parse_path(mark.get('d')).bbox()
	assert mark_start - card_end - float(cards[0].get('stroke-width'))/2 >= 38*8/30 - 1e-3


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
		assert abs(edge.end.imag-edge.start.imag) == 20
		if cap_side == 'left':
			assert cap_left == 0
			assert edge.start.real == edge.end.real == fragment.length
		else:
			assert cap_right == fragment.length
			assert edge.start.real == edge.end.real == 0


#============================================
def test_rotated_terminal_collar_is_inside_reported_bounds() -> None:
	model = topology.chromosome('A', length=100, centromere=1)
	part = chromosomes.render('tip', model, points=((0, 0), (3, 4)),
		palette={('A', 'body'): '#3479A8'})
	assert part.anchors['centromere'] == pytest.approx((60, 80))
	# Right and bottom ink extents of the default rounded collar and its stroke.
	assert part.bounds[2] >= 76.4 - 1e-9
	assert part.bounds[3] >= 95.9333333333 - 1e-9


#============================================
@pytest.mark.parametrize('model, position', (
	(topology.split(topology.chromosome('A', length=100, genes={'q': .4}), .4)[1], 0),
	(topology.chromosome('A', length=80, centromere=.5, genes={'q': .6}), 48),
))
def test_cramped_locus_keeps_an_exact_anchor_and_external_label(model: topology.Chromatid,
	position: float) -> None:
	with pytest.raises(ValueError, match="gene 'q' cannot fit an internal card"):
		chromosomes.render('cramped', model, points=((0, 0), (120, 0)),
			palette={('A', 'body'): '#3479A8'})
	part = chromosomes.render('cramped', model, points=((0, 0), (120, 0)),
		palette={('A', 'body'): '#3479A8'}, allow_external_genes=True)
	root = lxml.etree.fromstring(part.fragment)
	locus, = root.findall('./g[@data-gene="q"]')
	dot = locus.find('circle')
	assert part.anchors['gene:A/A/q'] == part.anchors['gene_q'] == (position, 0)
	assert (float(dot.attrib['cx']), float(dot.attrib['cy'])) == (position, 0)
	leader_start, leader_end = locus.find('.//polyline').attrib['points'].split()
	assert tuple(map(float, leader_start.split(','))) == (position, 0)
	assert float(leader_end.split(',')[1]) > 10
	text = locus.find('.//text')
	assert ''.join(text.itertext()) == 'q'
	assert float(text.attrib['font-size']) == pytest.approx(20*.52)
	assert part.bounds[3] > float(leader_end.split(',')[1])


#============================================
def test_sisters_label_cramped_loci_outside_the_belt() -> None:
	model = topology.replicate(topology.chromosome('A', length=80, centromere=.5,
		genes={'q': .6}))
	part = chromosomes.render('sisters', model, points=((0, 0), (80, 0)),
		palette={('A', 'body'): '#3479A8'}, allow_external_genes=True)
	root = lxml.etree.fromstring(part.fragment)
	belt, = root.findall('.//g[@data-layer="centromere"]')
	order = list(root.iter())
	labels = root.findall('.//g[@data-gene="q"]')
	assert len(labels) == 2
	leader_ends = []
	for label in labels:
		assert label.find('circle') is not None
		assert order.index(label) > order.index(belt)
		leader_end = label.find('.//polyline').attrib['points'].split()[-1]
		leader_ends.append(float(leader_end.split(',')[1]))
	assert min(leader_ends) < -10 and max(leader_ends) > 10
	assert part.anchors['first.gene_q'] == (48, -12)
	assert part.anchors['second.gene_q'] == (48, 12)
	assert part.bounds[1] < -30
	assert part.bounds[3] > 30


#============================================
def test_repeat_loci_use_source_and_copy_qualified_anchors() -> None:
	model = topology.chromosome('A/B', length=70, genes={'q/r': .5})
	product = topology.join(model, topology.copy(model, 'copy/2'))
	part = chromosomes.render('repeat', product, points=((0, 0), (140, 0)),
		palette={('A/B', 'body'): '#3479A8'})
	assert 'gene_q/r' not in part.anchors
	assert part.anchors['gene:A%2FB/A%2FB/q%2Fr'] == (35, 0)
	assert part.anchors['gene:A%2FB/copy%2F2/q%2Fr'] == (105, 0)


#============================================
def test_render_rejects_missing_palette_and_pair_without_centromere() -> None:
	model = topology.chromosome('A', length=100, genes={'tip': 0})
	points = ((0, 0), (100, 0))
	with pytest.raises(ValueError, match='Missing palette color'):
		chromosomes.render('missing', model, points=points, palette={})
	with pytest.raises(ValueError, match='six-digit hex'):
		chromosomes.render('bad-fill', model, points=points, palette={('A', 'body'): 'blue'})
	with pytest.raises(ValueError, match='one active centromere'):
		chromosomes.render('no-belt', topology.replicate(model), points=points,
			palette={('A', 'body'): '#835BB2'})
