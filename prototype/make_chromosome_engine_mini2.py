#!/usr/bin/env python3
"""Regenerate the ten chromosome figures for the second engine review deck."""

# Standard library
import io
import math
import pathlib
import base64
import itertools

# Third-party modules
import lxml.etree
import PIL.Image
import PIL.ImageColor

# Local repo modules
import svg_tools._xml
import svg_tools.text
import svg_tools.parts
import svg_tools.palette
import svg_tools.drawing as drawing
import svg_tools.annotations
import svg_tools.chromosomes
import svg_tools.chromosome_topology as topology


#============================================
def build_c01(path: pathlib.Path) -> None:
	"""Draw insertional and reciprocal translocations of the same starting chromosomes."""
	# Source: LECT01B, slide 8 (chromosome_samples.csv).
	ink = '#213449'
	palette = {
		('chr1', 'body'): svg_tools.palette.shade('sky_blue', 'dark'),
		('chr2', 'body'): svg_tools.palette.shade('green', 'dark'),
	}
	gene_palette = {(source, locus): fill
		for source, loci, fill in (('chr1', 'ABCD', '#CEEBFD'), ('chr1', 'EF', '#EFD1FA'),
			('chr1', 'GH', '#FFDFCC'), ('chr2', 'JKLM', '#E6FFCC'), ('chr2', 'NO', '#FFCCEE'))
		for locus in loci}

	def parent(source_id: str, letters: str, positions: tuple[int, ...], length: float) -> topology.Chromatid:
		# The centromere sits between the second and third loci, with room for its collar.
		genes = {letter: position / length for letter, position in zip(letters, positions, strict=True)}
		return topology.chromosome(source_id, length=length, centromere=129 / length, genes=genes)

	donor = parent('chr1', 'ABCDEFGH', (39, 80, 178, 220, 282, 330, 392, 446), 485)
	recipient = parent('chr2', 'JKLMNO', (39, 80, 178, 240, 302, 352), 390)
	donor_left, donor_right = topology.split(donor, 251 / donor.length)
	insert, donor_tip = topology.split(donor_right, 110 / donor_right.length)
	recipient_head, recipient_tail = topology.split(recipient, 209 / recipient.length)
	donor_head, donor_end = topology.split(donor, 361 / donor.length)
	recipient_left, recipient_end = topology.split(recipient, 271 / recipient.length)
	rows = (
		('insertion', 'Insertional translocation', 122,
			(topology.join(donor_left, donor_tip),
				topology.join(recipient_head, insert, recipient_tail))),
		('reciprocal', 'Reciprocal translocation', 358,
			(topology.join(donor_head, recipient_end), topology.join(recipient_left, donor_end))),
	)

	body = drawing.text(288, 57, 'Before', size=30, color=ink)
	body += drawing.text(905, 57, 'After', size=30, color=ink)
	body += drawing.line(45, 305, 1155, 305, color='#C9D5DF', width=2)
	for row_id, label, y, products in rows:
		topology.validate_conservation((donor, recipient), products)
		body += f'<g id="c01-{row_id}">'
		body += drawing.text(600, y, label, size=34, color=ink)
		body += svg_tools.annotations.connector([(552, y+92), (633, y+92)], color=ink,
			stroke_width=4, head_size=18).fragment
		for state, x, chromatids in (
			('before', 45, (donor, recipient)), ('after', 655, products),
		):
			for index, chromatid in enumerate(chromatids):
				baseline = y + 59 + index*66
				part = svg_tools.chromosomes.render(f'c01-{row_id}-{state}-{index+1}', chromatid,
					points=[(x, baseline), (x+chromatid.length, baseline)], width=38,
					palette=palette, gene_palette=gene_palette)
				body += part.fragment
		body += '</g>'

	drawing.write_svg(path, 1200, 560, 'Insertional and reciprocal translocations',
		'Both rows start with ABCDEFGH in blue and JKLMNO in green. In the top row, '
		'EF moves into the other chromosome, yielding ABCDGH and JKLEFMNO. In the bottom '
		'row, GH and NO exchange places, yielding ABCDEFNO and JKLMGH. White zigzags mark '
		'new joins. Each chromosome retains its centromere.', body)


#============================================
def build_c16(path: pathlib.Path) -> None:
	"""Show mirrored cubic sisters with one hue per numbered group."""
	# Source: LECT06C, slide 37 (chromosome_samples.csv).
	ink = '#213449'
	hues = ('purple', 'sky_blue', 'teal', 'lime_green', 'dark_yellow', 'dark_orange', 'red')
	columns = tuple(206 + index * 154 for index in range(len(hues)))
	length, width = 120, 14
	# Keep each telomere on a vertical span so both cap edges are horizontal.
	pose = ((16, -60), (16, -55), (16, -52), (15, -48), (8.8, -30), (3, -12), (1.9, -5),
		(1.9, 5), (3, 12), (8.8, 30), (15, 48), (16, 52), (16, 55), (16, 60))
	definitions = []
	body = []
	for group, (x, hue) in enumerate(zip(columns, hues), start=1):
		name = f'wheat-group-{group}'
		model = topology.chromosome(name, length=length, centromere=.5)
		sisters = topology.replicate(model)
		palette = {(name, 'body'): svg_tools.palette.shade(hue, 'dark')}
		strands = []
		centromeres = []
		for model, side in ((sisters.first, -1), (sisters.second, 1)):
			points = tuple((side * dx, y) for dx, y in pose)
			part = svg_tools.chromosomes.render(model.id, model, points=points,
				width=width, palette=palette, texture=False)
			strand = svg_tools._xml.parse(part.fragment)
			strand.remove(strand.find("g[@data-layer='centromere']"))
			strands.append(lxml.etree.tostring(strand, encoding='unicode'))
			centromeres.append(part.anchors['centromere'])
		(left, y), (right, _) = centromeres
		belt = svg_tools.chromosomes.centromere_part(f'{name}-belt',
			thickness=width, across=right-left+width*1.3)
		belt = svg_tools.parts.transform(belt, x=(left+right)/2, y=y, rotation=90)
		definitions.append(f'<g id="{name}">{"".join(strands)}{belt.fragment}</g>')
		body.append(drawing.text(x, 61, str(group), size=36, color=ink))
	for row, genome in enumerate('ABD'):
		y = 155 + row * 164
		body.append(drawing.text(142, y + 9, f'Genome {genome}',
			size=25, color=ink, anchor='end'))
		for group, x in enumerate(columns, start=1):
			for copy, center in enumerate((x - 27, x + 27), start=1):
				body.append(f'<use id="wheat-{genome}-{group}-{copy}" xlink:href="#wheat-group-{group}" '
					f'x="{center}" y="{y}"/>')
	drawing.write_svg(path, 1200, 560, 'Bread wheat chromosome groups',
		'Bread wheat (AABBDD) has two homologs in each of seven numbered groups per genome. '
		'Each chromosome has two curved sister chromatids and one shared centromere belt. '
		'Colors match numbered groups across genomes A, B, and D.',
		f'<defs>{"".join(definitions)}</defs>' + ''.join(body))


#============================================
def c22_products() -> tuple[
	topology.SisterPair, topology.SisterPair,
	tuple[topology.Chromatid, ...],
]:
	"""Replicate each homolog and exchange the tips of the two inner chromatids."""
	map_model = topology.chromosome('c22-map', length=313, centromere=.18,
		genes={'locus-a': .42, 'locus-b': .84})
	ab = topology.replicate(topology.homolog(map_model, 'ab', alleles={'locus-a': 'a', 'locus-b': 'b'}))
	plus = topology.replicate(topology.homolog(map_model, 'wild', alleles={'locus-a': '+', 'locus-b': '+'}))
	ab_left, ab_tip = topology.split(ab.second, .625)
	plus_left, plus_tip = topology.split(plus.first, .625)
	products = (ab.first, topology.join(ab_left, plus_tip), topology.join(plus_left, ab_tip), plus.second)
	return ab, plus, products


#============================================
def build_c22(path: pathlib.Path) -> None:
	"""Draw the replicated homologs, the crossover pose, and aligned products."""
	# Source: LECT08B, slide 36 (chromosome_samples.csv).
	render = svg_tools.chromosomes.render
	ink = '#213449'
	palette = {('ab', 'body'): '#076DAD', ('wild', 'body'): '#B74300'}
	width = 40
	ab, plus, products = c22_products()
	body = ''
	for x, label in ((180, 'Replicated homologs'), (549, 'Nonsisters exchange tips'), (911, 'Four products')):
		body += drawing.text(x, 98, label, size=28, color=ink)
	for x in (345, 711):
		body += drawing.line(x, 301, x+34, 301, color=ink, width=3)
		body += drawing.line(x+24, 292, x+34, 301, color=ink, width=3)
		body += drawing.line(x+24, 310, x+34, 301, color=ink, width=3)
	for key, pair, y in (('ab', ab, 216), ('wild', plus, 386)):
		body += render(f'c22-before-{key}', pair, points=((23, y), (336, y)),
			width=width, palette=palette).fragment
	# Three level knots at each end keep a straight run through the cap and its inner edge.
	bend = ((392, 268), (449, 268), (478, 268), (512, 268), (544.5, 279.25),
		(577, 304), (609.5, 328.75), (642, 340), (667, 340), (685, 340))
	exchange_poses = (
		((392, 220), (705, 220)),
		bend,
		tuple((x, 608 - y) for x, y in bend),
		((392, 388), (705, 388)),
	)
	exchange_parts = []
	for index, (product, pose) in enumerate(zip(products, exchange_poses), 1):
		part = render(f'c22-exchange-{index}', product, points=pose, width=width, palette=palette)
		exchange_parts.append(part)
		strand = svg_tools._xml.parse(part.fragment)
		strand.remove(strand.find("g[@data-layer='centromere']"))
		body += lxml.etree.tostring(strand, encoding='unicode')
	for index, (first, second) in enumerate(zip(exchange_parts[::2], exchange_parts[1::2]), 1):
		x, y1 = first.anchors['centromere']
		_, y2 = second.anchors['centromere']
		belt = svg_tools.chromosomes.centromere_part(f'c22-exchange-belt-{index}',
			thickness=width, across=y2-y1+width*1.3)
		body += svg_tools.parts.transform(belt, x=x, y=(y1+y2)/2).fragment
	for index, product in enumerate(products, 1):
		y = 176+(index-1)*85
		body += render(f'c22-product-{index}', product, points=((754, y), (1067, y)),
			width=width, palette=palette).fragment
		alleles = ''.join(gene.allele for gene in topology.project_genes(product))
		classification = 'Recombinant' if product.junctions else 'Parental'
		body += drawing.text(1082, y-1, alleles, size=26, color=ink, anchor='start')
		body += drawing.text(1082, y+25, classification, size=18, color=ink, anchor='start')
	drawing.write_svg(path, 1200, 560, 'One crossover between linked loci',
		'Two replicated homologs carry ab and ++. Each sister pair shares a centromere collar '
		'during the exchange. One nonsister from each homolog exchanges '
		'tips between the two loci. The four products are ab parental, a+ recombinant, '
		'+b recombinant, and ++ parental. A white zigzag marks each recombinant join.', body)


#============================================
def _c23_products() -> tuple[
	tuple[topology.SisterPair, topology.SisterPair],
	tuple[topology.SisterPair, topology.SisterPair],
]:
	"""Exchange the same two nonsisters' middle intervals and group by centromere."""
	red = topology.chromosome('red', length=220, centromere=.5)
	blue = topology.homolog(red, 'blue')
	red_pair, blue_pair = topology.replicate(red), topology.replicate(blue)
	# The second cut is relative to the 167 units remaining after the first cut.
	first_cut, second_cut = 53 / 220, 114 / 167
	red_left, red_remainder = topology.split(red_pair.second, first_cut)
	red_middle, red_right = topology.split(red_remainder, second_cut)
	blue_left, blue_remainder = topology.split(blue_pair.first, first_cut)
	blue_middle, blue_right = topology.split(blue_remainder, second_cut)
	red_ends = topology.join(red_left, blue_middle, red_right)
	blue_ends = topology.join(blue_left, red_middle, blue_right)
	red_dyad = topology.SisterPair(red_pair.first, blue_ends)
	blue_dyad = topology.SisterPair(red_ends, blue_pair.second)
	return (red_pair, blue_pair), (red_dyad, blue_dyad)


#============================================
def build_c23(path: pathlib.Path) -> None:
	"""Draw the two crossover sites, homolog separation, and chromatid separation."""
	# Source: LECT08B, slide 40 (chromosome_samples.csv).
	ink = '#213449'
	palette = {('red', 'body'): '#C63D47', ('blue', 'body'): '#076DAD'}
	centromere_styles = {
		('red', 'red.cen'): svg_tools.chromosomes.CentromereStyle(label='R', fill='#F4C9CD'),
		('blue', 'blue.cen'): svg_tools.chromosomes.CentromereStyle(label='B', fill='#C4E3F7'),
	}
	outline = '#93A6B8'
	(red, blue), (red_dyad, blue_dyad) = _c23_products()
	body: list[str] = []

	def chromosome(name: str,
		model: topology.Chromatid | topology.SisterPair,
		points: tuple[tuple[float, float], ...], *, width: float, scale: float = 1) -> None:
		part = svg_tools.chromosomes.render(f'c23-{name}', model, points=points, width=width,
			scale=scale, palette=palette, centromere_styles=centromere_styles)
		body.append(part.fragment)

	def cell(x: int, y: int, height: int) -> None:
		body.append(f'<rect x="{x-127}" y="{y-height/2}" width="254" height="{height}" '
			f'rx="36" fill="none" stroke="{outline}" stroke-width="2.5"/>')

	def heading(x: int, title: str, subtitle: str) -> None:
		part = svg_tools.text.label(x, 35, title, size=26, color=ink, anchor='middle', bold=True)
		body.append(part.fragment)
		body.append(drawing.text(x, 68, subtitle, size=20, color=ink))

	def arrow(start: tuple[float, float], end: tuple[float, float]) -> None:
		part = svg_tools.annotations.connector([start, end], color=ink, stroke_width=2.5, head_size=8)
		body.append(part.fragment)

	heading(135, 'Two crossover sites', 'Same two nonsisters')
	heading(436, 'After exchange', 'Middle segments swap')
	heading(737, 'Meiosis I', 'Sort by centromere')
	heading(1065, 'Meiosis II', 'Sisters separate')
	cell(135, 280, 220)
	cell(436, 280, 220)

	# The bent prophase poses use individual bodies; link each pair at its two collars.
	for top, bottom in ((210, 250), (310, 350)):
		body.append(drawing.line(135, top, 135, bottom, color=ink, width=7))
	chromosome('before-red-outer', red.first, ((25, 210), (245, 210)), width=20)
	chromosome('before-blue-outer', blue.second, ((25, 350), (245, 350)), width=20)
	chromosome('before-red-inner', red.second,
		((25, 298), (78, 280), (135, 250), (192, 280), (245, 298)), width=20, scale=1.10)
	chromosome('before-blue-inner', blue.first,
		((25, 262), (78, 280), (135, 310), (192, 280), (245, 262)), width=20, scale=1.10)
	for x in (78, 192):
		body.append(f'<circle cx="{x}" cy="280" r="24" fill="none" '
			f'stroke="{ink}" stroke-width="3" stroke-dasharray="4 5"/>')

	chromosome('exchange-red-centromere', red_dyad, ((326, 227), (546, 227)), width=25)
	chromosome('exchange-blue-centromere', blue_dyad, ((326, 333), (546, 333)), width=25)
	body.append(drawing.text(436, 422, 'The centromeres swap with them.', size=19, color=ink))
	arrow((269, 280), (300, 280))

	for color, dyad, y in (('red', red_dyad, 173), ('blue', blue_dyad, 387)):
		cell(737, y, 126)
		chromosome(f'meiosis-i-{color}', dyad, ((627, y), (847, y)), width=28)
		arrow((568, 280), (603, y))

	products = (
		(red_dyad.first, 'Parental', 114),
		(red_dyad.second, 'Recombinant', 221),
		(blue_dyad.first, 'Recombinant', 328),
		(blue_dyad.second, 'Parental', 435),
	)
	for index, (chromatid, label, y) in enumerate(products, start=1):
		cell(1065, y + 22, 94)
		chromosome(f'product-{index}', chromatid, ((955, y + 11), (1175, y + 11)), width=27)
		body.append(drawing.text(1065, y + 55, label, size=21, color=ink))
		start_y = 173 if index <= 2 else 387
		arrow((869, start_y), (931, y + 22))

	drawing.write_svg(path, 1200, 515, 'Double-crossover meiosis',
		'The same two nonsister chromatids cross at two sites, swapping middle segments '
		'that contain the centromeres. R and B label the red and blue centromeres. '
		'Homologs separate by centromere in meiosis I. '
		'Meiosis II separates sisters, yielding solid red and blue parental chromatids '
		'and reciprocal blue-red-blue and red-blue-red recombinants.', '\n'.join(body))


#============================================
def _c25_exchange() -> tuple[topology.SisterPair, topology.SisterPair,
	topology.Chromatid, topology.Chromatid]:
	"""Exchange the inner nonsisters between the centromere and both loci."""
	loci = {'A': .66, 'B': .84}
	reference = topology.chromosome('c25-reference', length=240, centromere=.22, genes=loci)
	blue = topology.homolog(reference, 'c25-blue', alleles={'A': 'a'})
	green = topology.homolog(reference, 'c25-green', alleles={'B': 'b'})
	upper = topology.replicate(blue)
	lower = topology.replicate(green)
	blue_head, blue_tail = topology.split(upper.second, .50)
	green_head, green_tail = topology.split(lower.first, .50)
	return upper, lower, topology.join(blue_head, green_tail), topology.join(green_head, blue_tail)


#============================================
def _c25_genotype(first: topology.Chromatid, second: topology.Chromatid) -> str:
	"""Read the displayed genotype from the retained alleles."""
	haplotypes = [''.join(gene.allele for gene in topology.project_genes(chromatid))
		for chromatid in (first, second)]
	return '/'.join(sorted(haplotypes, reverse=True))


#============================================
def build_c25(path: pathlib.Path) -> None:
	"""Rebuild the generic twin-spot example from LECT09C slide 6."""
	# Source: LECT09C, slide 6 (chromosome_samples.csv).
	upper, lower, blue_recombinant, green_recombinant = _c25_exchange()
	palette = {('c25-blue', 'body'): '#076DAD', ('c25-green', 'body'): '#00775F'}
	ink = '#213449'
	width = 27
	fragments = []

	def label(x: float, y: float, value: str, size: float, *, bold: bool = False) -> None:
		fragments.append(svg_tools.text.label(x, y, value, size=size, color=ink, bold=bold).fragment)

	def arrow(points: list[tuple[float, float]]) -> None:
		fragments.append(svg_tools.annotations.connector(points, color=ink, stroke_width=3, head_size=13).fragment)

	def straight(name: str, model: topology.Chromatid | topology.SisterPair, x: float, y: float) -> str:
		return svg_tools.chromosomes.render(name, model, points=((x, y), (x+240, y)),
			width=width, palette=palette).fragment

	label(148, 174, 'Replicated homologs', 25, bold=True)
	fragments.append(straight('c25-parent-blue', upper, 28, 230))
	fragments.append(straight('c25-parent-green', lower, 28, 314))
	arrow([(283, 272), (315, 272)])

	label(450, 174, 'One crossover', 25, bold=True)
	crossing = []
	for name, model, points in (
		('blue-unchanged', upper.first, ((330, 213.8), (570, 213.8))),
		('green-unchanged', lower.second, ((330, 330.2), (570, 330.2))),
		('blue-recombinant', blue_recombinant,
			((330, 246.2), (377, 246.2), (392, 246.2), (494, 297.8), (509, 297.8), (556, 297.8))),
		('green-recombinant', green_recombinant,
			((330, 297.8), (377, 297.8), (392, 297.8), (494, 246.2), (509, 246.2), (556, 246.2))),
	):
		part = svg_tools.chromosomes.render(f'c25-{name}', model, points=points, width=width, palette=palette)
		crossing.append(part)
		fragments.append(part.fragment)
	for index, (outer, inner) in enumerate(((crossing[0], crossing[2]), (crossing[1], crossing[3]))):
		x1, y1 = outer.anchors['centromere']
		x2, y2 = inner.anchors['centromere']
		belt = svg_tools.chromosomes.centromere_part(f'c25-exchange-belt-{index}', thickness=width,
			across=abs(y2-y1)+width*1.3)
		fragments.append(svg_tools.parts.transform(belt, x=(x1+x2)/2, y=(y1+y2)/2).fragment)

	fragments.append(drawing.line(585, 272, 602, 272, color=ink))
	arrow([(602, 272), (625, 147), (643, 147)])
	arrow([(602, 272), (625, 417), (643, 417)])

	for row, center, heading, daughters in (
		(1, 147, 'Exchanged chromatids go together',
			((upper.first, lower.second), (green_recombinant, blue_recombinant))),
		(2, 417, 'Exchanged chromatids separate',
			((upper.first, green_recombinant), (blue_recombinant, lower.second))),
	):
		label(921, center-102, heading, 26, bold=True)
		for column, (x, (first, second)) in enumerate(zip((653, 925), daughters), start=1):
			fragments.append(f'<rect x="{x}" y="{center-78}" width="264" height="156" '
				'rx="35" fill="none" stroke="#788B9A" stroke-width="2"/>')
			fragments.append(straight(f'c25-daughter-{row}-{column}-first', first, x+12, center-47))
			fragments.append(straight(f'c25-daughter-{row}-{column}-second', second, x+12, center-4))
			label(x+132, center+52, _c25_genotype(first, second), 30, bold=True)
	label(921, 533, 'Can form twin spots', 26, bold=True)

	drawing.write_svg(path, 1200, 560, 'Mitotic recombination and twin spots',
		'Two replicated homologs carry aB and Ab. The two inner nonsister chromatids exchange '
		'material between their centromeres and both loci. When the exchanged chromatids go to the '
		'same daughter, both daughters are aB/Ab. When they go to different daughters, one is aB/aB '
		'and the other is Ab/Ab. These daughters can give rise to twin spots.', '\n'.join(fragments))


# The two paths ease into the shared centromere and are reflected for the other homolog.
_C28_OUTER = ((44, 124), (106, 132), (139, 140), (165, 153), (190, 165), (220, 166),
	(250, 166), (274, 157), (301, 138), (329, 121), (394, 113), (454, 140), (494, 202),
	(525, 278), (556, 358), (598, 421), (647, 442), (713, 447))
_C28_INNER = ((48, 229), (111, 225), (144, 216), (168, 200), (190, 191), (220, 190),
	(250, 190), (271, 200), (296, 218), (321, 245), (359, 278), (404, 311),
	(458, 329), (525, 334), (610, 334), (713, 334))


#============================================
def _c28_exchange(first: topology.Chromatid, second: topology.Chromatid,
	cut: float) -> tuple[topology.Chromatid, topology.Chromatid]:
	"""Exchange the distal material between two nonsister chromatids."""
	first_left, first_right = topology.split(first, cut)
	second_left, second_right = topology.split(second, cut)
	products = (topology.join(first_left, second_right), topology.join(second_left, first_right))
	return products


#============================================
def build_c28(path: pathlib.Path) -> None:
	"""Show two reciprocal exchanges and the resulting nonparental ditype."""
	# Source: LECT09E, slide 16. Pose reference: LECT09B image_019.png.
	width = 46
	ink = '#213449'
	brown = '#774627'
	ochre = '#BD760E'
	palette = {('AB', 'body'): brown, ('ab', 'body'): ochre}
	upper = topology.chromosome('AB', length=100, centromere=.23, genes={'A': .36, 'B': .895})
	lower = topology.homolog(upper, 'ab', alleles={'A': 'a', 'B': 'b'})
	upper_sisters, lower_sisters = topology.replicate(upper), topology.replicate(lower)
	# Each displayed length preserves the authored pose. Cuts fall at the shared crossing knots.
	inner = _c28_exchange(upper_sisters.second, lower_sisters.first, .488531771)
	outer = _c28_exchange(upper_sisters.first, lower_sisters.second, .678062389)
	scene = lxml.etree.Element('g', {'id': 'c28-chromatids'})
	belt_centers: dict[str, list[tuple[float, float]]] = {'AB': [], 'ab': []}
	haplotypes = []
	# Paint the rising path over the descending path at each crossover.
	for name, points, products, scale in (
		('inner', _C28_INNER, inner, 7.200652259), ('outer', _C28_OUTER, outer, 8.764213621),
	):
		rising = tuple((x, 556-y) for x, y in points)
		for pose, product, origin in zip((points, rising), products, ('AB', 'ab')):
			part = svg_tools.chromosomes.render(f'c28-{name}-{origin}', product, points=pose,
				width=width, scale=scale, palette=palette, texture=False)
			strand = svg_tools._xml.parse(part.fragment)
			# The two independently posed sisters share one collar at the source locus.
			strand.remove(strand.find("g[@data-layer='centromere']"))
			belt_centers[origin].append(part.anchors['centromere'])
			haplotype = ''.join(gene.allele for gene in topology.project_genes(product))
			strand.set('data-haplotype', haplotype)
			haplotypes.append(haplotype)
			scene.append(strand)
	for origin, centers in belt_centers.items():
		(x1, y1), (x2, y2) = centers
		belt = svg_tools.chromosomes.centromere_part(f'c28-{origin}-belt', thickness=width, across=86)
		belt = svg_tools.parts.transform(belt, x=(x1+x2)/2, y=(y1+y2)/2)
		scene.append(svg_tools._xml.parse(belt.fragment))
	ascus = lxml.etree.Element('g', {'id': 'c28-ascus'})
	lxml.etree.SubElement(ascus, 'circle', {'cx': '990', 'cy': '266', 'r': '151',
		'fill': '#B4DAD3', 'stroke': ink, 'stroke-width': '3'})
	for (x, y), haplotype in zip(((990, 179), (1077, 266), (903, 266), (990, 353)), haplotypes):
		spore = lxml.etree.SubElement(ascus, 'g', {'data-haplotype': haplotype})
		lxml.etree.SubElement(spore, 'circle', {'cx': str(x), 'cy': str(y), 'r': '61',
			'fill': '#F3DF87', 'stroke': '#9B6519', 'stroke-width': '3'})
		label = svg_tools.text.label(x, y+14, haplotype, size=43, color=ink, italic=True)
		spore.append(svg_tools._xml.parse(label.fragment))
	for group in (scene, ascus):
		for gene_text in group.iter('text'):
			gene_text.set('font-family', 'Atkinson Hyperlegible Next, sans-serif')
	label = svg_tools.text.label(990, 473, 'Nonparental ditype (NPD)', size=30, color=ink)
	ascus.append(svg_tools._xml.parse(label.fragment))
	body = lxml.etree.tostring(scene, encoding='unicode')
	body += lxml.etree.tostring(ascus, encoding='unicode')
	drawing.write_svg(path, 1200, 560, 'Four-strand double crossover',
		'The inner and outer nonsister pairs exchange at different points between A and B. '
		'The four spores are Ab, Ab, aB, and aB, giving a nonparental ditype.', body)


#============================================
def build_c31(path: pathlib.Path) -> None:
	"""Show how three banding patterns highlight regions of the same chromosome."""
	# Source: LECT10B, slide 14 (chromosome_samples.csv).
	# The prototype's intervals are schematic. The centromere lies between the two C-band regions.
	lengths = (14, 7, 18, 9, 13, 6, 15, 8, 17, 10, 11, 7, 15, 9,
		26, 26, 8, 14, 5, 16, 7, 12, 8, 15, 19)
	c_regions = (14, 15)
	boundaries = tuple(itertools.accumulate(lengths, initial=0))
	regions = tuple(topology.Region(f'band-{index}', start, stop)
		for index, (start, stop) in enumerate(itertools.pairwise(boundaries)))
	length = boundaries[-1]
	site = topology.CentromericSite('centromere', boundaries[c_regions[1]])
	source = topology.SourceMaterial('c31', length, regions, (), (site,))
	model = topology.Chromatid(source.id, (topology.Span(source, source.id, 0, length),))
	sisters = topology.replicate(model)

	gray = '#AAAAAA'
	purple, yellow, teal = '#752499', '#FFFF80', '#00775F'
	ink = '#213449'
	yellow_ink = svg_tools.palette.shade('dark_yellow', 'extra_dark')
	indices = range(len(regions))
	methods = (
		('reference', 'All regions', ink, 150,
			tuple(teal if index in c_regions else (purple if index % 2 else yellow) for index in indices), teal),
		('g', 'G-bands', purple, 450,
			tuple(purple if index % 2 and index not in c_regions else gray for index in indices), gray),
		('r', 'R-bands', yellow_ink, 750,
			tuple(yellow if not index % 2 and index not in c_regions else gray for index in indices), gray),
		('c', 'C-bands', teal, 1050, tuple(teal if index in c_regions else gray for index in indices), teal),
	)
	fragments = [svg_tools.annotations.connector([(150, 54), (150, 16), (1050, 16)],
		kind='bracket', color=ink, stroke_width=4).fragment]
	for _, _, _, x, _, _ in methods[1:]:
		fragments.append(svg_tools.annotations.connector([(x, 16), (x, 54)],
			color=ink, stroke_width=4, head_size=15).fragment)
	top, bottom, width = 68, 512, 60
	for method, label, label_color, x, colors, belt in methods:
		palette = {(source.id, region.id): color for region, color in zip(regions, colors)}
		style = {(source.id, site.id): svg_tools.chromosomes.CentromereStyle(fill=belt)}
		pair = svg_tools.chromosomes.render(f'c31-{method}', sisters, points=((x, top), (x, bottom)),
			width=width, scale=(bottom-top) / length, palette=palette, texture=False, centromere_styles=style)
		# One opaque color strip avoids PDF stitching between separately painted bands.
		rows = [rgb for rgb, band_length in zip(map(PIL.ImageColor.getrgb, colors), lengths)
			for _ in range(band_length*8)]
		strip = PIL.Image.new('RGB', (1, len(rows)))
		strip.putdata(rows)
		png = io.BytesIO()
		strip.save(png, format='PNG')
		strip_uri = 'data:image/png;base64,' + base64.b64encode(png.getvalue()).decode('ascii')
		pair_svg = svg_tools._xml.parse(pair.fragment)
		for body in pair_svg.findall('.//g[@data-layer="body"]'):
			image = lxml.etree.Element('image', {'data-layer': 'band-colors',
				'x': str(x-width/2), 'y': str(top), 'width': str(width), 'height': str(bottom-top),
				'preserveAspectRatio': 'none', f'{{{svg_tools._xml.XLINK}}}href': strip_uri})
			body.replace(body[0], image)
			for stroke in body.findall('./g[@data-source-label]/path'):
				stroke.getparent().remove(stroke)
		fragments.append(lxml.etree.tostring(pair_svg, encoding='unicode'))
		fragments.append(drawing.text(x, 556, label, size=42, color=label_color))
		if method == 'reference':
			_, y = pair.anchors['centromere']
			fragments.append(drawing.line(x+76, y, x+87, y, color=ink, width=2))
			fragments.append(drawing.text(x+93, y+7, 'Centromere', size=22, color=ink, anchor='start'))
	drawing.write_svg(path, 1200, 570, 'Chromosome banding comparison',
		'The reference at left combines the regions highlighted by three separate staining methods. '
		'Arrows point to the individual staining patterns on the same chromosome. '
		'All three views use the same gray outside the highlighted bands. Purple G-bands and '
		'yellow R-bands highlight complementary regions outside the centromeric bands. '
		'Teal C-bands flank the centromere. Colors and widths are schematic.',
		''.join(fragments))


#============================================
def build_c55(path: pathlib.Path) -> None:
	"""Compare straight gene order with the opposite paths through a pairing loop."""
	# Source: LECT13B, slide 8 (chromosome_samples.csv).
	render = svg_tools.chromosomes.render
	genes = {'A': .071, 'B': .42, 'C': .5, 'D': .58, 'E': .929}
	normal = topology.chromosome('c55-normal', length=1000, centromere=.17, genes=genes)
	intact = topology.homolog(normal, 'c55-inverted')
	lower_cut, upper_cut = .26, .74
	left, rest = topology.split(intact, lower_cut)
	middle, right = topology.split(rest, (upper_cut-lower_cut)/(1-lower_cut))
	inverted = topology.join(left, topology.reverse(middle), right)
	palette = {('c55-normal', 'body'): '#83BCE3', ('c55-inverted', 'body'): '#CE9A74'}

	straight_normal = render('c55-straight-normal', normal, points=((35, 231), (374, 231)),
		width=29, scale=.339, palette=palette, texture=False)
	straight_inverted = render('c55-straight-inverted', inverted, points=((35, 345), (374, 345)),
		width=29, scale=.339, palette=palette, texture=False)
	loop_width, loop_scale = 32, 1.13
	axis = 810
	# The head turns back inward above the flared arms of the omega.
	normal_half = ((552, 384), (616, 384), (641, 379), (663, 369), (682, 351),
		(683, 330), (667, 309), (650, 295), (638, 276), (628, 239), (633, 195),
		(650, 153), (682, 117), (728, 92), (786, 83))
	crossing = (axis, 292)
	inverted_half = ((555, 445), (620, 434), (686, 397), (750, 344), crossing,
		(870, 240), (891, 216), (903, 189), (898, 165), (877, 145),
		(844, 134), (axis, 132))
	normal_pose = normal_half + tuple((2*axis-x, y) for x, y in reversed(normal_half))
	inverted_pose = inverted_half + tuple((2*axis-x, y) for x, y in inverted_half[-2::-1])
	loop_normal = render('c55-loop-normal', normal, points=normal_pose,
		width=loop_width, scale=loop_scale, palette=palette, texture=False)
	loop_inverted = render('c55-loop-inverted', inverted, points=inverted_pose,
		width=loop_width, scale=loop_scale, palette=palette, texture=False)
	loop_normal = svg_tools.parts.transform(loop_normal,
		x=loop_inverted.anchors['gene_C'][0]-loop_normal.anchors['gene_C'][0])

	# Paint just the nearly straight foreground at the self-crossing.
	x0, y0 = inverted_pose[0]
	pose_scale = (loop_inverted.anchors['end'][0]-x0)/(inverted_pose[-1][0]-x0)
	front_x = x0 + (crossing[0]-x0)*pose_scale
	front_y = y0 + (crossing[1]-y0)*pose_scale
	dx, dy = 60, -52
	front_material, _ = topology.split(right, .45)
	front = render('c55-loop-front', front_material,
		points=((front_x-dx, front_y-dy), (front_x+dx, front_y+dy)), width=loop_width,
		scale=2*math.hypot(dx, dy)/front_material.length, palette=palette, texture=False)
	angle = math.degrees(math.atan2(dy, dx))
	clip = (f'<clipPath id="c55-loop-overpass"><rect x="{front_x-32}" y="{front_y-loop_width/2}" '
		f'width="64" height="{loop_width}" transform="rotate({angle} {front_x} {front_y})"/></clipPath>')

	ink = '#213449'
	body = drawing.text(35, 187, 'Standard order', size=32, color=ink, anchor='start')
	body += drawing.text(35, 301, 'Inverted order', size=32, color=ink, anchor='start')
	body += drawing.text(axis, 34, 'Paired homologs', size=32, color=ink)
	body += straight_normal.fragment + straight_inverted.fragment
	for locus in 'ABCDE':
		anchor = f'gene_{locus}'
		body += drawing.line(*loop_normal.anchors[anchor], *loop_inverted.anchors[anchor],
			color='#52657A', width=4)
	body += loop_normal.fragment + loop_inverted.fragment
	body += f'<defs>{clip}</defs><g clip-path="url(#c55-loop-overpass)">{front.fragment}</g>'
	drawing.write_svg(path, 1200, 546, 'Homolog pairing with an inversion',
		'Standard ABCDE and inverted ADCBE homologs. Their matching loci pair along the flanks '
		'and around an omega-shaped loop. The centromeres stay outside the reversed interval. The curved '
		'homologs share one scale and preserve the distances between loci.', body)


#============================================
def build_c61(path: pathlib.Path) -> None:
	"""Exchange the LECT13C terminal intervals and keep the proximal centromeres fixed."""
	# Source: LECT13C, slide 10 (chromosome_samples.csv).
	ink = '#213449'
	palette = {
		('chr9', 'body'): '#9D90C2',
		('chr22', 'body'): '#74396B',
	}
	centromere_styles = {
		('chr9', 'chr9.cen'): svg_tools.chromosomes.CentromereStyle(label='9'),
		('chr22', 'chr22.cen'): svg_tools.chromosomes.CentromereStyle(label='22'),
	}
	chr9 = topology.chromosome('chr9', length=310, centromere=68.2 / 310)
	chr22 = topology.chromosome('chr22', length=155, centromere=34.1 / 155)
	left9, tip9 = topology.split(chr9, (chr9.length - 25) / chr9.length)
	left22, tip22 = topology.split(chr22, (chr22.length - 75) / chr22.length)
	der9 = topology.join(left9, tip22)
	der22 = topology.join(left22, tip9)
	topology.validate_conservation((chr9, chr22), (der9, der22))

	scale = 1.29
	width = 36
	before, after = 65, 675
	body = drawing.text(298, 62, 'Before', size=36, color=ink)
	body += drawing.text(907, 62, 'After', size=36, color=ink)
	for x in (before, after):
		body += drawing.line(x, 85, x + 465, 85, color='#C9D5DF', width=2)
	body += svg_tools.annotations.connector([(548, 282), (652, 282)],
		color=ink, stroke_width=5, head_size=22).fragment

	for name, label, model, x, y in (
		('chr9', 'Chromosome 9', chr9, before, 186),
		('der9', 'Derivative chromosome 9', der9, after, 186),
		('chr22', 'Chromosome 22', chr22, before, 389),
		('der22', 'Philadelphia chromosome', der22, after, 389),
	):
		body += drawing.text(x, y - 48, label, size=34, color=ink, anchor='start')
		part = svg_tools.chromosomes.render(f'c61-{name}', model,
			points=[(x, y), (x + 1, y)], width=width, scale=scale, palette=palette,
			centromere_styles=centromere_styles)
		body += part.fragment
	for left, y in ((left9, 186), (left22, 389)):
		cut_x = before + scale * left.length
		body += drawing.line(cut_x, y - 36, cut_x, y - 25, color=ink, width=3)
		body += drawing.line(cut_x, y + 25, cut_x, y + 36, color=ink, width=3)
	body += drawing.text(after, 453, 'Derivative chromosome 22', size=29, color=ink,
		anchor='start')

	drawing.write_svg(path, 1200, 520, 'Formation of the Philadelphia chromosome',
		'Lavender chromosome 9 and plum chromosome 22 exchange the tips marked by ticks. '
		'The derivative chromosome 9 is longer and has a plum tip. The Philadelphia '
		'chromosome is the shorter derivative chromosome 22 and has a lavender tip. The '
		'centromere collars retain their chromosome numbers and positions relative to the left ends. '
		'Lengths share one schematic scale.', body)


#============================================
def _c63_chromatids() -> dict[int, topology.Chromatid]:
	"""Use whole-chromosome lengths in Mb and retain the schematic exchange and loci."""
	# Hoskins et al. (2002), Fig. 1: https://doi.org/10.1186/gb-2002-3-12-research0085
	x = topology.chromosome('X', length=41.8, centromere=.11, genes={'rb+': .41})
	normal_2 = topology.chromosome('2', length=60.8, centromere=28.4/60.8, genes={'dp': .16})
	partner_2 = topology.homolog(normal_2, '2-wildtype', alleles={'dp': 'dp+'})
	y = topology.chromosome('Y', length=40.9, centromere=.30)
	tip_length = 15
	x_base, x_tip = topology.split(x, 1-tip_length/x.length)
	two_base, two_tip = topology.split(partner_2, 1-tip_length/partner_2.length)
	der_x = topology.join(x_base, two_tip)
	der_2 = topology.join(two_base, x_tip)
	topology.validate_conservation((x, partner_2), (der_x, der_2))
	models = {1: der_x, 2: normal_2, 3: y, 4: der_2}
	return models


#============================================
def build_c63(path: pathlib.Path) -> None:
	"""Lay out two products in each segregation column on a shared chromosome scale."""
	# Source: LECT13D, slide 41 (chromosome_samples.csv).
	models = _c63_chromatids()
	labels = {1: 'Derivative X', 2: 'Normal 2', 3: 'Normal Y', 4: 'Derivative 2'}
	columns = (
		('Adjacent-1', ((1, 2), (3, 4))),
		('Adjacent-2', ((1, 3), (2, 4))),
		('Alternate', ((1, 4), (2, 3))),
	)
	ink, navy = '#333333', '#003366'
	colors = {
		'X': ('X', '#B74300', '#FFDFCC'),
		'Y': ('Y', navy, '#CCE6FF'),
		'2': ('2', '#BFFF80', '#E6FFCC'),
	}
	colors['2-wildtype'] = colors['2']
	palette = {(source, 'body'): fill for source, (_, fill, _) in colors.items()}
	collars = {(source, f'{source}.cen'): svg_tools.chromosomes.CentromereStyle(label, fill)
		for source, (label, _, fill) in colors.items()}
	text = svg_tools.text.label
	scale = 5.45
	body = []
	for column, (heading, pairs) in enumerate(columns):
		left = 21 + column * 390
		mid = left + 189
		body.append(text(mid, 43, heading, size=34, color=ink, bold=True, anchor='middle').fragment)
		for row, pair in enumerate(pairs):
			top = 65 + row * 245
			pair_id = f'{pair[0]}-{pair[1]}'
			body.append(f'<g id="c63-pair-{pair_id}">')
			body.append(f'<rect x="{left}" y="{top}" width="378" height="229" rx="14" '
				'fill="#FFFFFF" stroke="#BFD1E3" stroke-width="2"/>')
			body.append(text(mid, top + 34, f'{pair[0]} + {pair[1]}', size=29,
				color=navy, bold=True, anchor='middle').fragment)
			for chromosome_row, chromosome_id in enumerate(pair):
				y = top + 104 + chromosome_row * 88
				body.append(text(left + 20, y - 30, f'{chromosome_id}  {labels[chromosome_id]}',
					size=24, color=ink, anchor='start').fragment)
				model = models[chromosome_id]
				x = left + 24
				part = svg_tools.chromosomes.render(f'c63-pair-{pair_id}-chr-{chromosome_id}', model,
					points=((x, y), (x + scale * model.length, y)), width=30, scale=scale,
					palette=palette, centromere_styles=collars)
				body.append(part.fragment)
			body.append('</g>')
	collar_marker = svg_tools.chromosomes.centromere_part('c63-legend', thickness=20,
		label='X', fill=colors['X'][2])
	body.append(svg_tools.parts.transform(collar_marker, 428, 567).fragment)
	body.append(text(451, 575, 'Centromere', size=24, color=ink, anchor='start').fragment)
	body.append(drawing.line(643, 567, 643+10*scale, 567, color=ink, width=3))
	body.append(text(712, 575, '10 Mb', size=24, color=ink, anchor='start').fragment)
	drawing.write_svg(path, 1200, 590, 'Six Drosophila gametes after reciprocal translocation',
		'Adjacent-1 gives 1 + 2 and 3 + 4. Adjacent-2 gives 1 + 3 and 2 + 4. '
		'Alternate gives 1 + 4 and 2 + 3. Chromosome 1 is derivative X (rb+), '
		'2 is normal 2 (dp), 3 is normal Y, and 4 is derivative 2 (dp+). '
		'The chromosomes share a DNA length scale. The pale collars carry centromere IDs. '
		'White zigzags mark the exchanged tips in the two derivatives.', ''.join(body))


#============================================
def generate(output_dir: pathlib.Path) -> None:
	"""Write the review figures to the caller's output directory."""
	output_dir.mkdir(parents=True, exist_ok=True)
	# Use fixed filenames. C31 contains an embedded band-color image (ASVS 5.3.2).
	for filename, build in (
		('c01.drawn.svg', build_c01),
		('c16.drawn.svg', build_c16),
		('c22.drawn.svg', build_c22),
		('c23.drawn.svg', build_c23),
		('c25.drawn.svg', build_c25),
		('c28.drawn.svg', build_c28),
		('c31.image.svg', build_c31),
		('c55.drawn.svg', build_c55),
		('c61.drawn.svg', build_c61),
		('c63.drawn.svg', build_c63),
	):
		build(output_dir / filename)


#============================================
def main() -> None:
	"""Regenerate the deck's canonical figure assets."""
	generate(pathlib.Path(__file__).resolve().parent / 'assets' / 'chromosome_engine_mini2')


if __name__ == '__main__':
	main()
