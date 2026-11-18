"""Build the topology-based linkage, loss-of-heterozygosity, and yeast figures."""

import json
import pathlib

import lxml.etree

import svg_tools._xml
import svg_tools.annotations
import svg_tools.chromosome_surface
import svg_tools.chromosome_topology as topology
import svg_tools.chromosomes
import svg_tools.drawing
import svg_tools.parts
import svg_tools.text


_INK = '#213449'
_BLUE = '#24578F'
_ORANGE = '#B74300'
_TEMPLATES = (pathlib.Path(__file__).resolve().parents[1]
	/ 'genetics/LECT09/djot/assets/mitotic_yeast_templates')
_SVG = '{' + svg_tools._xml.SVG + '}'


#============================================
def _haplotype(model: topology.Chromatid) -> str:
	"""Read allele symbols in the current material order."""
	return ''.join(gene.allele for gene in topology.project_genes(model))


#============================================
def _build_c24(path: pathlib.Path) -> None:
	"""Show both reciprocal products from the D-C-H two-strand double exchange."""
	# LECT08F, slides 43-44. One participating nonsister per homolog is shown.
	upper_path = ('M85 188 H270 C355 188 370 348 455 348 H745 '
		'C830 348 845 188 930 188 H1115')
	lower_path = ('M85 348 H270 C355 348 370 188 455 188 H745 '
		'C830 188 845 348 930 348 H1115')
	centerline = svg_tools.chromosome_surface.authored_centerline(upper_path, closed=False)
	length = centerline.length()
	first_cut = (185 + centerline[1].length() / 2) / length
	second_cut = 1 - first_cut
	loci = {'D': 95 / length, 'C': .5, 'H': 1 - 95 / length}
	template = topology.chromosome('c24-map', length=length, genes=loci)
	upper = topology.homolog(template, 'c24-upper', alleles={'D': '+', 'C': 'c', 'H': '+'})
	lower = topology.homolog(template, 'c24-lower', alleles={'D': 'd', 'C': '+', 'H': 'h'})
	upper_pair = topology.replicate(upper)
	lower_pair = topology.replicate(lower)
	participants = (upper_pair.second, lower_pair.first)
	upper_left, upper_rest = topology.split(participants[0], first_cut)
	lower_left, lower_rest = topology.split(participants[1], first_cut)
	middle_cut = (second_cut - first_cut) / (1 - first_cut)
	upper_middle, upper_right = topology.split(upper_rest, middle_cut)
	lower_middle, lower_right = topology.split(lower_rest, middle_cut)
	traced = topology.join(upper_left, lower_middle, upper_right)
	reciprocal = topology.join(lower_left, upper_middle, lower_right)
	topology.validate_conservation((*participants, upper_pair.first, lower_pair.second),
		(traced, reciprocal, upper_pair.first, lower_pair.second))
	if (_haplotype(traced), _haplotype(reciprocal)) != ('+++', 'dch'):
		raise ValueError('C24 double exchange must yield +++ and dch')

	palette = {('c24-upper', 'body'): _BLUE, ('c24-lower', 'body'): _ORANGE}
	fragments = []
	for x, locus in zip((180, 600, 1020), loci):
		fragments.append(svg_tools.text.label(x, 64, locus, size=43, color=_INK, bold=True).fragment)
	for x, interval, number in ((362.5, 'C\u2013D interval', '1'), (837.5, 'C\u2013H interval', '2')):
		fragments.append(svg_tools.text.label(x, 111, interval, size=30, color=_INK).fragment)
		fragments.append(svg_tools.text.label(x, 202, number, size=31, color=_INK, bold=True).fragment)
	for name, model, pose, width in (
		('reciprocal', reciprocal, lower_path, 46), ('traced', traced, upper_path, 58),
	):
		part = svg_tools.chromosomes.render_path(f'c24-{name}', model, pose, width=width,
			palette=palette)
		fragments.append(part.fragment)
	for start, end in ((40, 75), (1125, 1160)):
		fragments.append(svg_tools.annotations.connector([(start, 188), (end, 188)],
			color=_BLUE, stroke_width=3, head_size=10).fragment)
	for x, heading, model in ((335, 'Trace this chromatid', traced),
		(865, 'Reciprocal product', reciprocal)):
		fragments.append(svg_tools.text.label(x, 458, heading, size=31, color=_INK,
			bold=model is traced).fragment)
		fragments.append(svg_tools.text.label(x, 511, ' '.join(_haplotype(model)), size=40,
			color=_INK, role='sequence', bold=model is traced).fragment)
	svg_tools.drawing.write_svg(path, 1200, 548, 'Trace a Double-Recombinant Chromatid',
		'Two participating nonsister chromatids carry +c+ and d+h in D-C-H order. '
		'The wider chromatid switches parental origin at the first exchange and returns at '
		'the second. The products are +++ and dch. Both retain their parental outer alleles.',
		'\n'.join(fragments))


#============================================
def _build_c26(path: pathlib.Path) -> None:
	"""Show the two ways chromatids can segregate after a distal crossover."""
	# LECT09C, slide 12 and speaker notes. The crossover is between the centromere and A.
	upper = topology.chromosome('c26-A', length=208, centromere=.16, genes={'A': .84})
	lower = topology.homolog(upper, 'c26-a', alleles={'A': 'a'})
	upper_pair, lower_pair = topology.replicate(upper), topology.replicate(lower)
	upper_head, upper_tip = topology.split(upper_pair.second, .448)
	lower_head, lower_tip = topology.split(lower_pair.first, .448)
	upper_recombinant = topology.join(upper_head, lower_tip)
	lower_recombinant = topology.join(lower_head, upper_tip)
	before = (upper_pair.first, upper_pair.second, lower_pair.first, lower_pair.second)
	loh = ((upper_pair.first, lower_recombinant), (lower_pair.second, upper_recombinant))
	retained = ((upper_pair.first, lower_pair.second), (upper_recombinant, lower_recombinant))
	for daughters in (loh, retained):
		topology.validate_conservation(before, daughters[0] + daughters[1])
		for daughter in daughters:
			sites = [site for strand in daughter for site in topology.project_centromeres(strand)]
			if len(sites) != 2 or {site.source_id for site in sites if site.active} != {'c26-A', 'c26-a'}:
				raise ValueError('C26 daughters must inherit one active centromere from each homolog')
	if tuple(tuple(sorted(map(_haplotype, daughter))) for daughter in loh) != (('A', 'A'), ('a', 'a')):
		raise ValueError('C26 loss of heterozygosity must yield two homozygous daughters')
	if any(tuple(sorted(map(_haplotype, daughter))) != ('A', 'a') for daughter in retained):
		raise ValueError('C26 retention of heterozygosity must yield two heterozygous daughters')

	palette = {('c26-A', 'body'): _BLUE, ('c26-a', 'body'): _ORANGE}
	fragments = []

	def cell(name: str, x: int, y: int, chromosomes: tuple[topology.Chromatid, topology.Chromatid],
		fill: str, stroke: str) -> None:
		fragments.append(f'<ellipse cx="{x}" cy="{y}" rx="143" ry="91" fill="{fill}" '
			f'stroke="{stroke}" stroke-width="3"/>')
		genotype = '/'.join(sorted(map(_haplotype, chromosomes)))
		fragments.append(svg_tools.text.label(x, y-37, genotype, size=34, color=_INK,
			role='sequence', bold=True).fragment)
		for index, model in enumerate(chromosomes):
			baseline = y + index*44
			part = svg_tools.chromosomes.render(f'c26-{name}-{index}', model,
				points=((x-104, baseline), (x+104, baseline)), width=30, palette=palette)
			fragments.append(part.fragment)

	cell('parent', 172, 275, (upper, lower), '#F0F3F7', '#788C9E')
	fragments.append(svg_tools.text.label(172, 156, 'Starting cell', size=29, color=_INK).fragment)
	fragments.append(svg_tools.text.label(365, 218, 'One crossover', size=24, color=_INK).fragment)
	for points in ([(330, 275), (409, 275), (498, 154)], [(409, 275), (498, 413)]):
		fragments.append(svg_tools.annotations.connector(points, color='#526879',
			stroke_width=3.5, head_size=14).fragment)
	for y, heading, daughters, colors in (
		(154, 'Loss of heterozygosity', loh, (('#E9F0F8', _BLUE), ('#FFF0E7', _ORANGE))),
		(413, 'Heterozygosity retained', retained, (('#F0F3F7', '#788C9E'),) * 2),
	):
		fragments.append(svg_tools.text.label(845, y-107, heading, size=32, color=_INK,
			bold=True).fragment)
		for index, (x, model, (fill, stroke)) in enumerate(zip((670, 1020), daughters, colors)):
			cell(f'daughter-{y}-{index}', x, y, model, fill, stroke)
	svg_tools.drawing.write_svg(path, 1200, 530, 'Copy-neutral loss of heterozygosity after crossover',
		'After one crossover between the centromere and A, two segregation patterns are possible. '
		'The A/A and a/a daughters lose heterozygosity at A. The alternative produces two A/a '
		'daughters. Both patterns retain two chromosomes in each cell.', '\n'.join(fragments))


#============================================
def _build_c27(path: pathlib.Path) -> None:
	"""Retain the lecture's ascus arrangement and render one tracked homolog pair."""
	# LECT09D, slide 13. The authored templates contain only poses and non-chromosome artwork.
	filename = 'yeast_meiosis.drawn.svg'
	models = json.loads((_TEMPLATES / 'models.json').read_text())[filename]
	root = svg_tools._xml.read(_TEMPLATES / filename)
	upper = topology.chromosome('c27-A', length=160, centromere=.215, genes={'A': .92})
	lower = topology.homolog(upper, 'c27-a', alleles={'A': 'a'})
	upper_pair, lower_pair = topology.replicate(upper), topology.replicate(lower)
	meiotic_products = (lower_pair.first, lower_pair.second, upper_pair.first, upper_pair.second)
	spores = (upper_pair.first, lower_pair.first, upper_pair.second, lower_pair.second)
	topology.validate_conservation(meiotic_products, spores)
	stages = (upper, lower, upper_pair.first, upper_pair.second, lower_pair.first,
		lower_pair.second, *meiotic_products, *meiotic_products, *spores)
	palette = {('c27-A', 'body'): '#805333', ('c27-a', 'body'): '#A7730B'}
	shapes = {}
	slots = root.findall(".//*[@data-body-slot]")
	for index, (slot, model, pose) in enumerate(zip(slots, stages, models['bodies'], strict=True), 1):
		if slot.get('data-body-slot') != pose['id']:
			raise ValueError(f"C27 pose {pose['id']} does not match its template slot")
		part = svg_tools.chromosomes.render_path(f'c27-chromatid-{index}', model, pose['path'],
			width=12, palette=palette, texture=False, draw_centromeres=index not in range(3, 11),
			allow_external_genes=True)
		node = svg_tools._xml.parse(part.fragment)
		allele = _haplotype(model)
		node.set('data-haplotype', allele)
		# The portrait layout uses large labels beside the tips.
		for card in node.xpath(".//g[@data-layer='gene-locus']"):
			card.getparent().remove(card)
		shapes[index] = part.anchors['centromere']
		slot.getparent().replace(slot, node)
	labels = [node for node in root.iter(_SVG + 'text') if node.text in ('A', 'a')]
	for label, model in zip(labels, stages, strict=True):
		allele = _haplotype(model)
		label.text = allele
		label.set('fill', '#805333' if allele == 'A' else '#80570B')
		label.set('font-family', 'Atkinson Hyperlegible Mono')
		label.set('font-weight', 'bold')
	for marker in root.findall(".//*[@data-marker-slot]"):
		parent = marker.getparent()
		parent.getparent().remove(parent)
	for first, group_id in ((3, 'duplicated-homologs'), (5, 'duplicated-homologs'),
		(7, 'after-meiosis-i'), (9, 'after-meiosis-i')):
		x1, y1 = shapes[first]
		x2, y2 = shapes[first + 1]
		belt = svg_tools.chromosomes.centromere_part(f'c27-belt-{first}', thickness=12,
			across=abs(y2-y1)+15.6)
		belt = svg_tools.parts.transform(belt, x=(x1+x2)/2, y=(y1+y2)/2)
		root.find(f".//*[@id='{group_id}']").append(svg_tools._xml.parse(belt.fragment))
	path.write_bytes(lxml.etree.tostring(svg_tools.drawing.svg_root(root), encoding='ascii'))


#============================================
def build(output_dir: pathlib.Path) -> None:
	"""Write the three linkage and tetrad review figures."""
	output_dir.mkdir(parents=True, exist_ok=True)
	_build_c24(output_dir / 'c24.drawn.svg')
	_build_c26(output_dir / 'c26.drawn.svg')
	_build_c27(output_dir / 'c27.drawn.svg')
