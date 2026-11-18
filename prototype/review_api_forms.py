"""Render chromosome review C02, C03/C36, C05, and C06 from source topology."""

# Standard library
import pathlib

# Local repo modules
import svg_tools.cells as cells
import svg_tools.parts as parts
import svg_tools.drawing as drawing
import svg_tools.annotations as annotations
import svg_tools.chromosomes as chromosomes
import svg_tools.chromosome_topology as topology
import genetics.LECT10.djot.human_chromosome_2_fusion_recipe as fusion_source


INK = '#344651'
FONT = 'Atkinson Hyperlegible Next, sans-serif'


#============================================
def _label(x: float, y: float, value: str, size: float = 28) -> str:
	return drawing.text(x, y, value, size=size, color=INK, font=FONT)


#============================================
def _arrow(start: tuple[float, float], end: tuple[float, float]) -> str:
	return annotations.connector([start, end], stroke_width=3, head_size=15).fragment


#============================================
def _cell(x: float, y: float, width: float, height: float, color: str) -> str:
	part = cells.cell_envelope(kind='animal', width=width, height=height, color=color)
	return parts.transform(part, x=x, y=y).fragment


#============================================
def _meiosis(path: pathlib.Path) -> None:
	"""Keep LECT02B's two homolog pairs and both meiosis I orientations."""
	seed_shape = topology.chromosome('seed-shape-R', length=102, centromere=.6, genes={'R': .245})
	seed_color = topology.chromosome('seed-color-Y', length=69, centromere=.6, genes={'Y': .245})
	models = {
		'R': seed_shape,
		'Y': seed_color,
		'r': topology.homolog(seed_shape, 'seed-shape-r', alleles={'R': 'r'}),
		'y': topology.homolog(seed_color, 'seed-color-y', alleles={'Y': 'y'}),
	}
	pairs = {allele: topology.replicate(model) for allele, model in models.items()}
	palette = {(model.id, 'body'): '#FF8080' if allele.isupper() else '#80C0FF'
		for allele, model in models.items()}
	gene_palette = {(model.id, allele.upper()): '#FFCCCC' if allele.isupper() else '#CCE6FF'
		for allele, model in models.items()}

	def render_cell(name: str, x: float, y: float, width: float, height: float,
		alleles: str, spread: float = 0) -> str:
		body = _cell(x, y, width, height, '#FFECCC')
		for index, allele in enumerate(alleles):
			if spread:
				center_x = x + (-spread if index < 2 else spread)
				center_y = y + (-36 if index % 2 == 0 else 57)
			else:
				center_x, center_y = x + (index-1.5)*53, y
			length = models[allele].length
			start, end = (center_x, center_y-length/2), (center_x, center_y+length/2)
			if spread:
				part = chromosomes.render_sisters(f'{name}-{allele}', pairs[allele],
					start=start, end=end, width=22, palette=palette, gene_palette=gene_palette, texture=False)
			else:
				part = chromosomes.render(f'{name}-{allele}', models[allele], points=(start, end),
					width=22, palette=palette, gene_palette=gene_palette, texture=False)
			body += part.fragment
		return f'<g id="{name}">{body}</g>'

	body = _label(550, 36, 'F1 generation (YyRr)', 31)
	body += render_cell('f1', 550, 129, 256, 156, 'RYry')
	body += _label(326, 236, 'Orientation 1') + _label(774, 236, 'Orientation 2')
	body += _label(93, 374, 'Metaphase I') + _label(93, 662, 'Anaphase I')
	for x, number, alleles in ((326, 1, 'RYry'), (774, 2, 'rYRy')):
		body += _arrow((550+(x-550)*.36, 191), (x+(550-x)*.52, 245))
		body += render_cell(f'metaphase-{number}', x, 365, 290, 232, alleles, 50)
		body += _arrow((x, 482), (x, 519))
		body += render_cell(f'anaphase-{number}', x, 653, 326, 258, alleles, 77)
	drawing.write_svg(path, 1000, 791, 'Two meiotic orientations',
		'An F1 cell carries R/r and Y/y on two homologous pairs. At metaphase I the two '
		'pairs can orient independently. In anaphase I, homologs move apart and sisters '
		'stay attached. The poles receive R with Y and r with y, or r with Y and R with y.', body)


#============================================
def _fusion(path: pathlib.Path) -> None:
	"""Reuse the irregular band intervals from the original LECT02C illustration."""
	ancestors = []
	palette = {}
	for name, runs, center in zip(('ancestor-a', 'ancestor-b'), fusion_source.RUNS, (260, 295)):
		start = runs[0][0]
		length = runs[-1][1]-start
		chromatid = topology.chromosome(name, length=length, centromere=(center-start)/length,
			regions=tuple(((left-start)/length, f'band-{index}') for index, (left, _, _) in enumerate(runs)))
		ancestors.append(chromatid)
		for index, (_, _, color) in enumerate(runs):
			palette[name, f'band-{index}'] = fusion_source.PURPLE if color == 'purple' else fusion_source.GOLD
	dicentric = topology.join(*ancestors)
	inactive = topology.with_centromere_activity(dicentric, 'ancestor-b.cen', active=False)
	topology.validate_conservation(ancestors, (dicentric,))
	topology.validate_conservation((dicentric,), (inactive,))
	original_center, inactive_center = topology.project_centromeres(inactive)

	def rod(name: str, model: topology.Chromatid, x: float, top: float) -> str:
		points = ((x, top), (x, top+model.length))
		return chromosomes.render(name, model, points=points, width=24,
			palette=palette, texture=False).fragment

	top = 94
	body = rod('ancestor-a', ancestors[0], 110, top)
	body += rod('ancestor-b', ancestors[1], 193, top+ancestors[0].length)
	body += rod('dicentric', dicentric, 440, top)
	body += rod('inactivation', inactive, 698, top)
	body += rod('human-chromosome-2', inactive, 970, top)
	marker = chromosomes.centromere_part('inactive-site', thickness=24, active=False)
	inactive_y = top+inactive_center.position
	body += parts.transform(marker, x=698, y=inactive_y, rotation=90).fragment
	junction_y = top+ancestors[0].length
	body += drawing.line(126, junction_y, 177, junction_y, color=INK, width=2, dash='3 5')
	for start, end in ((224, 406), (471, 660), (732, 931)):
		body += _arrow((start, junction_y), (end, junction_y))
	body += _label(318, 219, 'Short-arm', 23) + _label(318, 247, 'telomere fusion', 23)
	body += _label(564, 219, 'Centromere', 23) + _label(564, 247, 'inactivation', 23)
	body += _label(830, 346, 'Ancestral centromere', 23)
	body += drawing.line(728, inactive_y, 781, 321, color=INK, width=2)
	body += drawing.line(880, 321, 952, inactive_y, color=INK, width=2)
	for x, labels in ((151, ('Ancestral', 'acrocentrics')), (440, ('Dicentric', 'chromosome')),
		(698, ('One active', 'centromere')), (970, ('Human', 'chromosome 2'))):
		body += _label(x, 38, labels[0], 25) + _label(x, 67, labels[1], 25)
	body += _label(440, 554, 'Two active centromeres', 23)
	body += _label(440, 581, 'can make it unstable', 23)
	active_y = top + original_center.position
	for start_y, end_y, arm in ((top, active_y-13, 'Short arm'),
		(active_y+13, top+inactive.length, 'Long arm')):
		midpoint = (start_y+end_y)/2
		body += (f'<path d="M 991 {start_y} h 10 V {end_y} h -10" '
			f'fill="none" stroke="{INK}" stroke-width="2"/>')
		body += _label(1053, midpoint+7, arm, 20)
	drawing.write_svg(path, 1110, 601, 'Human chromosome 2 fusion',
		'Two ancestral acrocentric chromosomes join end to end at their short-arm telomeres. '
		'The resulting dicentric chromosome can be unstable while both centromeres are active. '
		'The second centromere becomes inactive '
		'(dashed collar). Human chromosome 2 has one active centromere and retains DNA '
		'at the ancestral site. Band lengths are schematic. The three fused bodies share '
		'the same length, band order, and ancestry.', body)


#============================================
def _hla(path: pathlib.Path) -> None:
	"""Keep the source arm split and the DP, DQ, DR, B, C, A locus order."""
	start, stop, center = 100, 1090, 752.5
	hla_start, hla_stop = 850, 895
	length = stop-start
	interval_length = hla_stop-hla_start
	regions = ((0, 'arm'), ((hla_start-start)/length, 'HLA'), ((hla_stop-start)/length, 'arm'))
	six = topology.chromosome('chromosome-6', length=length, centromere=(center-start)/length,
		regions=regions)
	overview = chromosomes.render('hla-chromosome-6', six, points=((start, 127), (stop, 127)),
		width=53, palette={('chromosome-6', 'arm'): '#BFE3DC', ('chromosome-6', 'HLA'): '#D40000'},
		texture=False)

	# Map the source's schematic locus positions onto the highlighted interval.
	left, right = 62, 1140
	loci = {'DP': 120, 'DQ': 270, 'DR': 420, 'B': 800, 'C': 900, 'A': 1090}
	zoom_scale = (right-left)/interval_length
	with_loci = topology.chromosome('chromosome-6', length=length, centromere=(center-start)/length,
		regions=regions, genes={name: (hla_start-start+(x-left)/zoom_scale)/length
			for name, x in loci.items()})
	_, remainder = topology.split(with_loci, (hla_start-start)/length)
	interval, _ = topology.split(remainder, interval_length/remainder.length)
	palette = {('chromosome-6', name): '#CCFFCC' if name in ('DP', 'DQ', 'DR') else '#CCE6FF'
		for name in loci}
	zoom = chromosomes.render('hla-molecular-track', interval, points=((left, 383), (right, 383)),
		width=60, scale=zoom_scale, palette={('chromosome-6', 'HLA'): '#E3BFD7'},
		gene_palette=palette, texture=False)
	body = _label(600, 42, 'Chromosome 6', 32) + overview.fragment
	body += _label(426, 197, 'Long arm') + _label(1044, 197, 'Short arm')
	body += _label(872, 74, 'HLA region', 23)
	for anchor_x, detail_x in ((hla_start, left), (hla_stop, right)):
		body += drawing.line(anchor_x, 154, detail_x, 353, color='#666666', width=2)
	body += zoom.fragment
	body += _label(270, 464, 'Class II') + _label(930, 464, 'Class I')
	drawing.write_svg(path, 1200, 491, 'HLA genes on chromosome 6',
		'The short arm of chromosome 6 contains the HLA region. An enlarged view shows '
		'class II loci DP, DQ, DR on the left and class I loci B, C, A on the right. '
		'The displayed intervals are schematic.', body)


#============================================
def _fertilization(path: pathlib.Path) -> None:
	"""Keep the cell scene and illustrate one X-bearing egg and Y-bearing sperm."""
	models = {
		'X': topology.chromosome('chromosome-X', length=57, centromere=.38),
		'Y': topology.chromosome('chromosome-Y', length=29, centromere=.38),
	}
	palette = {('chromosome-X', 'body'): '#D78DF2', ('chromosome-Y', 'body'): '#80FFE5'}

	def nucleus(name: str, x: float, genotype: str) -> str:
		part = cells.nucleus(width=105, height=108, color='#CCE6FF')
		body = parts.transform(part, x=x, y=149).fragment
		for index, symbol in enumerate(genotype):
			model = models[symbol]
			center_x = x + (index-(len(genotype)-1)/2)*37
			top = 141-model.length/2
			part = chromosomes.render(f'{name}-{symbol}', model, width=12 if symbol == 'X' else 9,
				points=((center_x, top), (center_x, top+model.length)), palette=palette, texture=False)
			body += part.fragment + _label(center_x, 187, symbol, 21)
		return f'<g id="{name}">{body}</g>'

	body = _label(125, 37, 'Egg', 31) + _label(432, 37, 'Sperm', 31) + _label(768, 37, 'Zygote', 31)
	body += _cell(125, 149, 196, 193, '#FFD080') + nucleus('egg-nucleus', 125, 'X')
	body += ('<path d="M 491 147 H 509 C 545 138 555 175 584 179 '
		'C 610 182 612 204 585 220" fill="none" stroke="#076DAD" '
		'stroke-width="5" stroke-linecap="round"/>')
	body += _cell(432, 149, 139, 123, '#84CDFA') + nucleus('sperm-nucleus', 432, 'Y')
	body += _cell(768, 149, 207, 193, '#FFD080') + nucleus('zygote-nucleus', 768, 'XY')
	body += _label(286, 170, '+', 50) + _label(647, 166, '=', 47)
	drawing.write_svg(path, 890, 256, 'Egg and sperm form a zygote',
		'One X-bearing egg and one Y-bearing sperm produce an XY zygote. '
		'Each gamete contributes one sex chromosome. Only the sex chromosomes are shown.', body)


#============================================
def build(output_dir: pathlib.Path) -> None:
	"""Write four original drawings; C03 and C36 share the fusion asset."""
	output_dir.mkdir(parents=True, exist_ok=True)
	_meiosis(output_dir / 'c02.drawn.svg')
	_fusion(output_dir / 'c03.drawn.svg')
	_hla(output_dir / 'c05.drawn.svg')
	_fertilization(output_dir / 'c06.drawn.svg')
