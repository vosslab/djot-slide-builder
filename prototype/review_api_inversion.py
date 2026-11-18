"""Build the inversion figures for the chromosome review."""

import json
import math
from pathlib import Path

from svg_tools import chromosome_surface, drawing, parts
from svg_tools import chromosome_topology as topology
from svg_tools.chromosomes import centromere_part, render_path


LOOP_SOURCE = (Path(__file__).resolve().parents[1] / 'genetics/LECT13/djot'
	/ 'lect13b_loop_chromosome_sources.json')
INK = '#213547'
BLUE, GREEN, ORANGE, OCHRE = '#4389C0', '#318F76', '#E98250', '#C89B3F'
LOOP_WIDTH = 25


def _invert(model: topology.Chromatid, start: float, stop: float) -> topology.Chromatid:
	left, remainder = topology.split(model, start)
	middle, right = topology.split(remainder, (stop-start)/(1-start))
	inverted = topology.join(left, topology.reverse(middle), right)
	topology.validate_conservation((model,), (inverted,))
	return inverted


def _parents(prefix: str, centromere: float) -> tuple[topology.SisterPair, topology.SisterPair]:
	normal = topology.chromosome(f'{prefix}-normal', length=1000, centromere=centromere,
		genes={'a': .10 if centromere == .5 else .145, 'b': .40, 'c': .60, 'd': .93})
	other = topology.homolog(normal, f'{prefix}-inverted')
	return topology.replicate(normal), topology.replicate(_invert(other, .24, .76))


def _belt(name: str, first: parts.SvgPart, second: parts.SvgPart, width: float) -> parts.SvgPart:
	x1, y1 = first.anchors['centromere']
	x2, y2 = second.anchors['centromere']
	belt = centromere_part(name, thickness=width,
		across=math.hypot(x2-x1, y2-y1)+width*1.08)
	return parts.transform(belt, x=(x1+x2)/2, y=(y1+y2)/2,
		rotation=math.degrees(math.atan2(y2-y1, x2-x1))-90)


def _center_on_site(path_d: str, target: complex) -> str:
	"""Trim the longer end so the midpoint source site falls on its recorded anchor."""
	path = chromosome_surface.authored_centerline(path_d, closed=False)
	distance = chromosome_surface.nearest_distance(path, target)
	length = path.length()
	before = max(0, 2*distance-length)
	after = min(length, 2*distance)
	start = path.ilength(before) if before else 0
	stop = path.ilength(after) if after < length else 1
	return path.cropped(start, stop).d()


def _pairing(prefix: str, source: list[dict], normal: topology.SisterPair,
	inverted: topology.SisterPair, *, pericentric: bool) -> str:
	"""Paint the four independent poses and place each shared belt in the foreground."""
	strands = []
	overpasses = []
	for index, model, color, site in (
		(0, inverted.first, ORANGE, 600+165j),
		(1, inverted.second, OCHRE, 600+135j),
		(2, normal.second, GREEN, 600+105j),
		(4, normal.first, BLUE, 600+75j),
	):
		(path_model_site,) = topology.project_centromeres(model)
		path_d = source[index]['path']
		if pericentric:
			if path_model_site.position != model.length/2:
				raise ValueError('C57 centromere must be at the midpoint of each chromatid')
			path_d = _center_on_site(path_d, site)
		part = render_path(f'{prefix}-pair-{index}', model, path_d, width=LOOP_WIDTH, texture=False,
			palette={(path_model_site.source_id, 'body'): color}, draw_centromeres=False)
		if pericentric and abs(complex(*part.anchors['centromere'])-site) >= 1:
			raise ValueError('C57 rendered centromere misses its authored anchor')
		strands.append(part)
		if index in (2, 4):
			overpasses.append(_overpass(f'{prefix}-overpass-{index}', model, path_d, color))
	inverted_belt = _belt(f'{prefix}-inverted-belt', *strands[:2], LOOP_WIDTH)
	normal_belt = _belt(f'{prefix}-normal-belt', *strands[2:], LOOP_WIDTH)
	leader = '<path d="M 702.5 147.46 L 822 167 L 870 145" fill="none" stroke="#213547" stroke-width="2.5"/>'
	leader += '<circle cx="702.5" cy="147.46" r="4" fill="#213547"/>'
	leader += drawing.text(865, 119, 'Crossover site', size=32, color=INK, anchor='start')
	return ''.join(part.fragment for part in (*strands, inverted_belt, normal_belt)) + ''.join(overpasses) + leader


def _build_c57(path: Path, source: list[dict]) -> None:
	normal, inverted = _parents('c57', .5)
	body = _pairing('c57', source, normal, inverted, pericentric=True)
	body += drawing.text(30, 43, 'Pericentric inversion', size=38, color=INK, anchor='start')
	drawing.write_svg(path, 1200, 665, 'Pairing in a pericentric inversion',
		'The four chromatids form an inversion loop. The centromere of each homolog is '
		'inside the loop and each belt spans the centromeres of its two sisters.', body)


def _overpass(name: str, model: topology.Chromatid, path_d: str, color: str) -> str:
	"""Fill the self-crossing along the strand passing in front."""
	path = chromosome_surface.authored_centerline(path_d, closed=False)
	start, stop = .71, .88
	pose = path.cropped(path.ilength(start*path.length()), path.ilength(stop*path.length()))
	_, right = topology.split(model, start)
	front, _ = topology.split(right, (stop-start)/(1-start))
	source_id = front.spans[0].source.id
	part = render_path(name, front, pose.d(), width=LOOP_WIDTH, texture=False,
		palette={(source_id, 'body'): color})
	clip_id = f'{name}-clip'
	return (f'<defs><clipPath id="{clip_id}"><rect x="515" y="486" width="195" height="150"/>'
		f'</clipPath></defs><g clip-path="url(#{clip_id})">{part.fragment}</g>')


def _products(normal: topology.SisterPair, inverted: topology.SisterPair
	) -> tuple[topology.Chromatid, topology.Chromatid]:
	"""Exchange arms of the two chromatids paired in opposite directions."""
	standard_left, standard_right = topology.split(normal.second, .45)
	inverted_left, inverted_right = topology.split(inverted.second, .55)
	proximal = topology.join(inverted_left, topology.reverse(standard_left))
	distal = topology.join(topology.reverse(standard_right), inverted_right)
	topology.validate_conservation((normal.second, inverted.second), (proximal, distal))
	return proximal, distal


def _anaphase_figure(path: Path, source: list[dict], prefix: str, *, pericentric: bool) -> None:
	normal, inverted = _parents(prefix, .50 if pericentric else .045)
	proximal, distal = _products(normal, inverted)
	centromeres = tuple(len(topology.project_centromeres(product)) for product in (proximal, distal))
	if centromeres != ((1, 1) if pericentric else (2, 0)):
		raise ValueError(f'{prefix} inversion products have unexpected centromere counts')
	alleles = tuple(''.join(gene.allele for gene in topology.project_genes(product))
		for product in (proximal, distal))
	if alleles != ('acba', 'dcbd'):
		raise ValueError(f'{prefix} inversion products have unexpected allele orders')

	normal_id = normal.first.spans[0].source.id
	inverted_id = inverted.first.spans[0].source.id
	recombinant = {(normal_id, 'body'): GREEN, (inverted_id, 'body'): OCHRE}
	product_specs = (
		('normal', normal.first, (6 if pericentric else 7,), {(normal_id, 'body'): BLUE}),
		('inverted', inverted.first, (9 if pericentric else 6,), {(inverted_id, 'body'): ORANGE}),
		('proximal', proximal, (10, 11) if pericentric else (8, 9), recombinant),
		('distal', topology.reverse(distal) if pericentric else distal,
			(7, 8) if pericentric else (10, 11), recombinant),
	)
	products = {}
	for label, model, indices, palette in product_specs:
		pose = source[indices[0]]['path']
		for index in indices[1:]:
			# The existing constituent curves meet at a common endpoint.
			pose += ' ' + source[index]['path'].split(maxsplit=2)[2]
		products[label] = render_path(f'{prefix}-{label}', model, pose,
			width=23, texture=False, palette=palette, allow_external_genes=True)

	cell_d = ('M 745 110 C 840 40 918 110 1000 115 C 1080 120 1195 55 1305 110 '
		'C 1450 186 1440 410 1320 493 C 1210 545 1100 495 1010 508 '
		'C 900 527 775 505 723 416 C 664 316 668 175 745 110 Z')
	cell = f'<path d="{cell_d}" fill="#F3EEE7" stroke="#697788" stroke-width="2.5"/>'
	left_pole, right_pole = ((728, 305), (1390, 265)) if pericentric else ((719, 326), (1392, 326))
	left, right = (
		((('normal', 'centromere'), ('distal', 'centromere')),
			(('inverted', 'centromere'), ('proximal', 'centromere'))) if pericentric else
		((('inverted', 'centromere'), ('proximal', 'centromere_0')),
			(('normal', 'centromere'), ('proximal', 'centromere_1')))
	)
	for pole, targets, label_x in ((left_pole, left, 748), (right_pole, right, 1346)):
		for product, anchor in targets:
			cell += drawing.line(*pole, *products[product].anchors[anchor], color=INK, width=3)
		cell += drawing.line(*pole, label_x, 518, color=INK, width=2)
		cell += drawing.text(label_x, 548, 'Spindle pole', size=27, color=INK)
	cell += ''.join(part.fragment for part in products.values())
	if not pericentric:
		cell += drawing.text(1060, 376, 'Dicentric bridge', size=30, color=INK)
		cell += drawing.text(1140, 480, 'Acentric fragment', size=30, color=INK)

	kind = 'Pericentric' if pericentric else 'Paracentric'
	body = drawing.text(30, 100, f'{kind} inversion loop', size=36, color=INK, anchor='start')
	pairing = _pairing(prefix, source, normal, inverted, pericentric=pericentric)
	body += f'<g transform="translate(2 128) scale(.55)">{pairing}</g>'
	body += drawing.text(710, 47, 'Anaphase I', size=38, color=INK, anchor='start')
	body += cell
	description = ('The crossover yields two monocentric chromatids with reciprocal duplication '
		'and deletion of the distal arms.' if pericentric else
		'The crossover yields a dicentric bridge between the spindle poles and an acentric fragment.')
	drawing.write_svg(path, 1430, 566, f'{kind} inversion and anaphase I',
		description + ' The two parental chromatids are also shown.', body)


def _build_c59(path: Path) -> None:
	prefix = 'c59'
	positions = (127, 232, 337, 442, 547)
	as_fraction = {letter: position/569 for letter, position in zip('ABCDE', positions)}
	standard = topology.chromosome('c59-standard', length=569, centromere=22/569, genes=as_fraction)
	other = topology.homolog(standard, 'c59-inverted', alleles={letter: letter.lower() for letter in 'ABCDE'})
	inverted = topology.reverse(_invert(other, 180/569, 494/569))
	if ''.join(gene.allele for gene in topology.project_genes(inverted)) != 'ebcda':
		raise ValueError('C59 inverted chromatid must present ebcda in the pairing pose')
	fig = drawing.text(35, 45, 'Pairing in the inverted region', size=33, color=INK, anchor='start')
	for model, y1, x, color in ((standard, 115, 88, BLUE), (inverted, 275, 193, ORANGE)):
		pair = topology.replicate(model)
		source_id = model.spans[0].source.id
		strands = [render_path(f'{prefix}-{source_id}-{index}', chromatid,
			f'M {x} {y} h 569', width=23, texture=False,
			palette={(source_id, 'body'): color}, draw_centromeres=False)
			for index, (y, chromatid) in enumerate(((y1, pair.first), (y1+80, pair.second)))]
		fig += ''.join(part.fragment for part in strands)
		fig += _belt(f'{source_id}-belt', *strands, 23).fragment
	fig += '<path d="M 366 214 L 402 256 M 402 214 L 366 256" stroke="#AC233F" stroke-width="5" stroke-linecap="round"/>'
	drawing.write_svg(path, 842, 408, 'Inversion crossover problem',
		'Four chromatids align loci B, C, and D. The two middle chromatids cross between B and C. '
		'For the second crossover, use C/c-D/d.', fig)


def _build_c60(path: Path) -> None:
	length, origin = 935, 65
	start, stop = 85, 680
	normal = topology.chromosome('c60-x', length=length, centromere=870/length,
		genes={'w+': 127.5/length}, regions=((0, 'euchromatin'), (645/length, 'heterochromatin')))
	inverted = _invert(normal, start/length, stop/length)
	if not math.isclose(topology.project_genes(inverted)[0].position, start+stop-127.5):
		raise ValueError('C60 inversion must move w+ beside heterochromatin')
	palette = {('c60-x', 'euchromatin'): '#338B7B', ('c60-x', 'heterochromatin'): '#B15C12'}
	fig = ''
	for y, model, name, header in ((110, normal, 'normal', 'Normal X chromosome'),
		(300, inverted, 'inverted', 'Inverted X chromosome')):
		part = render_path(f'c60-{name}', model, f'M {origin} {y} h {length}', width=44,
			palette=palette, gene_palette={('c60-x', 'w+'): '#812F46'})
		fig += drawing.text(35, y-57, header, size=33, color=INK, anchor='start')
		fig += part.fragment
		for position in (start, stop):
			x = origin+position
			fig += (f'<path d="M {x} {y-53} v 24 m -6 -9 l 6 9 6 -9" fill="none" '
				'stroke="#AC233F" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
		fig += drawing.text(840, y+62, 'Heterochromatin', size=25, color=INK)
	fig += drawing.text(150, 172, 'Inversion breakpoints', size=25, color=INK, anchor='start')
	fig += drawing.text(150, 362, 'w+ beside heterochromatin', size=25, color=INK, anchor='start')
	drawing.write_svg(path, 1065, 399, 'Position effect on the X chromosome',
		'The inversion moves the w+ locus next to heterochromatin and brings a small segment of '
		'heterochromatin into the euchromatic arm.', fig)


def build(output_dir: Path) -> None:
	"""Write C56-C60 under the review generator's destination."""
	output_dir.mkdir(parents=True, exist_ok=True)
	source = json.loads(LOOP_SOURCE.read_text())
	_build_c57(output_dir / 'c57.drawn.svg', source['pericentric-pairing']['parts'])
	_anaphase_figure(output_dir / 'c56.drawn.svg', source['paracentric-anaphase']['parts'], 'c56',
		pericentric=False)
	_anaphase_figure(output_dir / 'c58.drawn.svg', source['pericentric-anaphase']['parts'], 'c58',
		pericentric=True)
	_build_c59(output_dir / 'c59.drawn.svg')
	_build_c60(output_dir / 'c60.drawn.svg')
