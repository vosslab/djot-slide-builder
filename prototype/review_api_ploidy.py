"""Draw the C37-C43 review figures from chromosome materials and division states."""

import math
import collections.abc
from pathlib import Path

import svgpathtools

from svg_tools import annotations, chromosomes, drawing
from svg_tools import chromosome_topology as topology


INK = '#263B48'


def _rod(name: str, model: topology.Chromatid | topology.SisterPair,
	x: float, y: float, width: float, palette: dict[tuple[str, str], str], *,
	angle: float = 0, scale: float = 1) -> str:
	"""Place a vertical rod or sister pair by its midpoint, with rotation from vertical."""
	material = model.first if isinstance(model, topology.SisterPair) else model
	half_length = material.length * scale / 2
	dx = -math.sin(math.radians(angle)) * half_length
	dy = math.cos(math.radians(angle)) * half_length
	start, end = (x-dx, y-dy), (x+dx, y+dy)
	if isinstance(model, topology.SisterPair):
		part = chromosomes.render_sisters(name, model, start=start, end=end,
			width=width, scale=scale, palette=palette, texture=False)
	else:
		part = chromosomes.render(name, model, points=(start, end), width=width,
			scale=scale, palette=palette, texture=False)
	return f'<g data-source="{material.spans[0].source.id}">{part.fragment}</g>'


def _ellipse(x: float, y: float, rx: float, ry: float, fill: str = '#F9F4E9',
	stroke: str = '#B19070', width: float = 2.5) -> str:
	return (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" '
		f'stroke="{stroke}" stroke-width="{width}"/>')


def _labels(labels: collections.abc.Iterable[tuple[float, float, str, float]], *,
	color: str = INK) -> str:
	return ''.join(drawing.text(x, y, label, size=size, color=color) for x, y, label, size in labels)


def _arrow(*points: tuple[float, float]) -> str:
	return annotations.connector(points, color=INK, stroke_width=3, head_size=13).fragment


def _sisters(pairs: collections.abc.Iterable[topology.SisterPair]) -> tuple[topology.Chromatid, ...]:
	return tuple(chromatid for pair in pairs for chromatid in (pair.first, pair.second))


def _diploid(types: collections.abc.Iterable[topology.Chromatid]
	) -> tuple[tuple[topology.Chromatid, topology.Chromatid], ...]:
	return tuple((model, topology.homolog(model, f'{model.id}-homolog')) for model in types)


def _palette(groups: collections.abc.Iterable[collections.abc.Iterable[topology.Chromatid]],
	colors: collections.abc.Iterable[str]) -> dict[tuple[str, str], str]:
	return {(model.id, 'body'): color
		for group, color in zip(groups, colors, strict=True) for model in group}


def _write(output: Path, number: int, dimensions: tuple[float, float], title: str,
	description: str, body: str) -> None:
	drawing.write_svg(output / f'c{number}.drawn.svg', *dimensions, title, description, body)


def _c37(output: Path) -> None:
	"""Compare one, two, three and four intact copies of each chromosome type."""
	spec = (
		('red', 239.4, 118.75, '#F7B9B6'),
		('purple', 285.95, 61.75, '#D1B8ED'),
		('yellow', 205.2, 101.65, '#E9D46B'),
	)
	models = tuple(topology.chromosome(f'c37-{kind}', length=length, centromere=center/length)
		for kind, length, center, _ in spec)
	palette = _palette(((model,) for model in models), (color for _, _, _, color in spec))
	body = []
	for ploidy, title in enumerate(('Haploid (N)', 'Diploid (2N)', 'Triploid (3N)', 'Tetraploid (4N)'), 1):
		x, y = (ploidy-1) % 2 * 340.5, (ploidy-1) // 2 * 384
		body.append(f'<g id="c37-panel-{ploidy}" data-chromosome-count="{ploidy*len(models)}">')
		body.append(drawing.text(x+170.25, y+37, title, size=30, color=INK))
		for column, model in enumerate(models):
			for index in range(ploidy):
				copy = topology.copy(model, f'{model.id}-{ploidy}-{index+1}')
				x_center = x+62+107*column+26*(index-(ploidy-1)/2)
				body.append(_rod(copy.id, copy, x_center, y+61+model.length/2, 17, palette))
		body.append('</g>')
	_write(output, 37, (681, 768), 'Chromosome copy number across four ploidy levels',
		'Each panel adds a full set. The red, purple and yellow types keep their lengths and centromere positions.',
		''.join(body))


def _c38(output: Path) -> None:
	"""Follow two replicated homologs to the same pole when one pair fails to separate."""
	short = topology.chromosome('c38-short', length=32, centromere=.5)
	long = topology.chromosome('c38-blue', length=55, centromere=.5)
	shorts = _diploid((short,))[0]
	longs = (long, topology.homolog(long, 'c38-orange'))
	palette = _palette((shorts, (longs[0],), (longs[1],)), ('#687580', '#24689B', '#B75E31'))
	short_left, short_right = map(topology.replicate, shorts)
	long_left, long_right = map(topology.replicate, longs)
	all_sisters = _sisters((short_left, short_right, long_left, long_right))
	assignments = (
		('nondisjunction', 365, (short_left, long_left, long_right), (short_right,)),
		('separation', 1035, (short_left, long_left), (short_right, long_right)),
	)
	body = [drawing.text(700, 34, 'Meiosis I', size=30, color=INK)]
	for stage, center, left, right in assignments:
		topology.validate_conservation(all_sisters, _sisters(left + right))
		body.append(f'<g id="c38-{stage}" data-chromosome-count="{len(left)+len(right)}">')
		body.append(_ellipse(center, 142, 135, 92, width=3))
		pole_left, pole_right = center-123, center+123
		body.append(f'<path d="M {pole_left} 142 Q {center} 55 {pole_right} 142 '
			f'M {pole_left} 142 Q {center} 229 {pole_right} 142" '
			'fill="none" stroke="#D6C7B3" stroke-width="2"/>')
		for pole, group, x in (('left', left, center-75), ('right', right, center+75)):
			body.append(f'<circle cx="{center + (-123 if pole == "left" else 123)}" cy="142" r="4" fill="#9D826B"/>')
			body.append(f'<g id="c38-{stage}-{pole}" data-chromosome-count="{len(group)}">')
			for index, pair in enumerate(group):
				body.append(_rod(f'c38-{stage}-{pole}-{index+1}', pair, x+37*max(0, index-1),
					103 if index == 0 else 169, 11.5, palette))
			body.append('</g>')
		body.append('</g>')
	body.append(drawing.text(160, 246, 'Nondisjunction', size=24, color='#9A3927'))
	body.append(drawing.line(238, 236, 280, 198, color='#9A3927', width=2))
	_write(output, 38, (1400, 280), 'Nondisjunction in meiosis I',
		'The short gray homologs separate in both cells. Both long homologs move to one pole in the left cell. '
		'They move to opposite poles in the right cell. Each replicated chromosome retains its two sisters.',
		''.join(body))


def _c39(output: Path) -> None:
	"""Keep the four cohesin rings along the arms of one replicated chromosome."""
	model = topology.chromosome('c39-blue', length=272, centromere=(157-24)/272)
	pair = topology.replicate(model)
	palette = {(model.id, 'body'): '#24578F'}
	body = ['<g transform="translate(320 0) rotate(90)">']
	# Keep an even gap across the four rings.
	for chromatid, x in zip(_sisters((pair,)), (78, 122), strict=True):
		body.append(chromosomes.render_path(chromatid.id, chromatid, f'M {x} 24 V 296',
			width=23, palette=palette, texture=False, draw_centromeres=False).fragment)
	body.append('<g id="cohesin" fill="none" stroke="#935D00" stroke-width="7">')
	for y in (64, 116, 190, 254):
		body.append(f'<ellipse cx="100" cy="{y}" rx="41" ry="12"/>')
	body.append('</g></g>')
	_write(output, 39, (320, 200), 'Cohesion maintained',
		'Four orange cohesin rings hold the arms of two blue sister chromatids close together.', ''.join(body))


def _c40(output: Path) -> None:
	"""Draw one reference set of nine forms and complete diploid and tetraploid complements."""
	types = (
		('M-11 0 Q0 -7 11 0', '#B68C00'),
		('M-13 -4 Q8 -7 13 5', '#C06B35'),
		('M-14 6 Q12 -15 14 6', '#92734A'),
		('M-14 8 Q0 -18 14 8', '#398DB5'),
		('M-17 8 Q0 -23 17 8', '#A1467E'),
		('M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', '#2B896B'),
		('M-18 6 Q-8 -12 18 6', '#7E9C22'),
		('M-11 9 Q-21 -10 11 -8', '#C45462'),
		('M-18 0 L18 0', '#697AA6'),
	)
	models = tuple(topology.chromosome(f'c40-type-{index}', length=svgpathtools.parse_path(pose).length())
		for index, (pose, _) in enumerate(types, 1))
	palette = _palette(((model,) for model in models), (color for _, color in types))
	body = []
	for sets, x, y, label in (
		(1, 35, 215, 'Monoploid set: 9'),
		(2, 605, 75, 'Diploid (18)'),
		(4, 605, 340, 'Tetraploid (36)'),
	):
		count = sets*len(models)
		height = 56+36*(sets-1)
		body.append(f'<g id="c40-cell-{sets}" data-sets="{sets}" data-chromosome-count="{count}">')
		body.append(f'<rect x="{x}" y="{y}" width="460" height="{height}" rx="35" '
			'fill="#F3F6F8" stroke="#647681" stroke-width="2"/>')
		for row in range(sets):
			for column, (model, (pose, _)) in enumerate(zip(models, types, strict=True)):
				copy = topology.copy(model, f'{model.id}-{sets}-{row+1}')
				part = chromosomes.render_path(copy.id, copy, pose, width=8, palette=palette, texture=False)
				body.append(f'<g transform="translate({x+30+50*column} {y+25+36*row})">{part.fragment}</g>')
		body.append('</g>')
		body.append(drawing.text(x+230, y+height+(64 if sets == 1 else 45), label, size=26, color=INK))
	_write(output, 40, (1100, 630), 'Chrysanthemum chromosome sets',
		'Each row is one set of nine chromosome types. The diploid has 18 chromosomes and the tetraploid has 36.',
		''.join(body))


def _c41(output: Path) -> None:
	"""Trace unreduced gametes and the union of their unchanged chromosome complements."""
	types = tuple(topology.chromosome(f'c41-{name}', length=length, centromere=.5)
		for name, length in (('blue', 61), ('red', 76), ('green', 43)))
	parent = _diploid(types)
	palette = _palette(parent, ('#617DE0', '#E66B58', '#57A68C'))
	replicated = tuple(tuple(map(topology.replicate, group)) for group in parent)
	first_gamete = tuple(tuple(pair.first for pair in group) for group in replicated)
	second_gamete = tuple(tuple(pair.second for pair in group) for group in replicated)
	zygote = tuple(first + second for first, second in zip(first_gamete, second_gamete, strict=True))
	topology.validate_conservation(_sisters(pair for group in replicated for pair in group),
		tuple(model for group in zygote for model in group))

	body = ['<defs><radialGradient id="c41-cell-fill" cx="30%" cy="25%" r="80%">'
		'<stop offset="0" stop-color="#FFF2D8"/><stop offset="1" stop-color="#EFC296"/>'
		'</radialGradient></defs>']
	poses = (
		('parent', (155, 265, 115), parent, ((107, 270, 12), (199, 230, -25), (158, 337, 0))),
		('upper-gamete', (600, 135, 94), first_gamete, ((632, 94, -38), (562, 130, 10), (633, 170, 12))),
		('lower-gamete', (600, 420, 94), second_gamete, ((560, 416, 25), (638, 399, -12), (603, 471, -25))),
		('zygote', (1040, 265, 132), zygote, ((959, 272, 10), (1020, 199, 25), (1069, 270, 28))),
	)
	extra = ((1015, 335, -22), (1102, 217, -22), (1112, 323, 45))
	for stage, (x, y, radius), groups, centers in poses:
		body.append(f'<g id="c41-{stage}" data-chromosome-count="{sum(map(len, groups))}">')
		body.append(_ellipse(x, y, radius, radius, 'url(#c41-cell-fill)', '#C9A895', 2))
		for kind, (group, center) in enumerate(zip(groups, centers, strict=True)):
			pair_centers = (center, extra[kind]) if stage == 'zygote' else (center,)
			for index, model in enumerate(group):
				cx, cy, angle = pair_centers[index//2]
				offset = -9 if index % 2 == 0 else 9
				dx = math.cos(math.radians(angle))*offset
				dy = math.sin(math.radians(angle))*offset
				body.append(_rod(f'c41-{stage}-{kind+1}-{index+1}', model, cx+dx, cy+dy, 10, palette,
					angle=angle+(-2 if offset < 0 else 2)))
		body.append('</g>')
	for start, end in (((297, 200), (488, 143)), ((297, 328), (488, 404)),
		((712, 143), (895, 201)), ((712, 404), (895, 330))):
		body.append(_arrow(start, end))
	body.append(_labels((
		(155, 93, 'Parent Species', 29), (155, 422, '2n = 6', 29), (155, 459, 'Diploid', 29),
		(393, 269, 'Meiotic error', 29), (802, 253, 'Self-', 29), (802, 287, 'fertilisation', 29),
		(600, 552, 'Unreduced', 29), (600, 587, 'gametes', 29), (1040, 93, 'Zygote', 29),
		(1040, 440, '4n = 12', 29), (1040, 477, 'Tetraploid', 29),
	)))
	_write(output, 41, (1200, 600), 'Unreduced gametes and tetraploid zygote',
		'The diploid parent and each unreduced gamete contain six chromosomes. '
		'The two gametes fuse to give a tetraploid zygote with twelve chromosomes.', ''.join(body))


def _c42(output: Path) -> None:
	"""Show doubling after a division error, followed by meiosis and gamete fusion."""
	types = tuple(topology.chromosome(f'c42-type-{index}', length=length, centromere=.5)
		for index, length in enumerate((94, 66, 42), 1))
	parent = _diploid(types)
	palette = _palette(parent, ('#9277BF',)*len(parent))
	doubled = tuple(_sisters(map(topology.replicate, group)) for group in parent)
	meiosis = tuple(tuple(map(topology.replicate, group)) for group in doubled)
	# One gamete from each of the two meiosis I cells is shown; their other gametes are implicit.
	gamete_a = tuple((group[0].first, group[2].first) for group in meiosis)
	gamete_b = tuple((group[1].second, group[3].second) for group in meiosis)
	zygote = tuple(first + second for first, second in zip(gamete_a, gamete_b, strict=True))
	body = []
	for stage, x, y, radius, groups in (
		('parent', 138, 168, 117, parent), ('doubled', 510, 168, 117, doubled),
		('gamete-a', 150, 566, 75, gamete_a), ('gamete-b', 150, 787, 75, gamete_b),
		('zygote', 510, 679, 117, zygote),
	):
		body.append(f'<g id="c42-{stage}" data-chromosome-count="{sum(map(len, groups))}">')
		body.append(_ellipse(x, y, radius, radius, '#F5D59A', '#344651'))
		rows = tuple(zip(*groups, strict=True))
		column_pitch, row_pitch, scale, width = (30, 39, .34, 8) if radius == 75 else (43, 49, .43, 10)
		for row_index, row in enumerate(rows):
			y_center = y+row_pitch*(row_index-(len(rows)-1)/2)
			for column, model in enumerate(row):
				body.append(_rod(f'c42-{stage}-{row_index+1}-{column+1}',
					model, x+column_pitch*(column-1), y_center, width, palette, scale=scale))
		body.append('</g>')
	body.append(_arrow((260, 168), (382, 168)))
	body.append(_arrow((405, 350), (295, 420), (44, 420), (44, 787), (67, 787)))
	body.append(_arrow((44, 566), (67, 566)))
	body.append(_arrow((223, 600), (280, 669), (383, 669)))
	body.append(drawing.line(223, 751, 280, 669, color=INK, width=3))
	body.append(_labels((
		(320, 70, 'Cell division error', 29), (138, 319, '2n = 6', 32),
		(510, 319, 'Tetraploid cell', 30), (510, 356, '4n = 12', 32),
		(180, 401, 'Meiosis', 36), (150, 668, '2n = 6', 30), (150, 889, '2n = 6', 30),
		(460, 460, 'Gametes produced', 32), (460, 500, 'by tetraploids', 32),
		(510, 854, 'New species', 30), (510, 890, '(4n = 12)', 30),
		(330, 1015, 'Autopolyploid speciation', 32),
	)))
	_write(output, 42, (659, 1056), 'Autopolyploid division error',
		'The parent has six chromosomes. A division error leaves both sets of separated sisters in one cell, '
		'which now has twelve chromosomes. Meiosis produces gametes with six chromosomes each. '
		'Two such gametes fuse to form a tetraploid with twelve chromosomes.', ''.join(body))


def _c43(output: Path) -> None:
	"""Contrast doubling within one species with combining two species' genomes."""
	a_types, b_types = (tuple(topology.chromosome(f'c43-{species}-{kind}', length=length, centromere=.5)
		for kind, length in (('long', 112), ('short', 72))) for species in ('a', 'b'))
	a_groups, b_groups = _diploid(a_types), _diploid(b_types)
	palette = _palette(a_groups + b_groups, ('#2D719E', '#B95040', '#7BA9CA', '#DE8E77'))
	a_parent = tuple(chromatid for group in a_groups for chromatid in group)
	b_parent = tuple(chromatid for group in b_groups for chromatid in group)
	a_extra = tuple(topology.copy(model, f'{model.id}-extra') for model in a_parent)
	a_hybrid = _sisters(map(topology.replicate, a_types))
	b_hybrid = _sisters(map(topology.replicate, b_types))
	outline = ('M -139,-6 C -144,-66 -93,-101 -29,-103 C 40,-114 117,-85 137,-29 '
		'C 162,40 111,94 44,104 C -29,121 -129,84 -139,-6 Z')
	shadow = ('M -128,24 C -101,82 -27,100 41,90 C 91,84 124,57 137,26 '
		'C 124,75 92,97 44,101 C -31,117 -111,84 -128,24 Z')
	body = [drawing.line(534, 38, 534, 801, color='#E4E9EB', width=1.5)]
	cells = (
		('auto-a-parent', 255, 218, (a_parent,)), ('allo-a-parent', 708, 218, (a_parent,)),
		('allo-b-parent', 1040, 218, (b_parent,)), ('auto-product', 255, 580, (a_parent, a_extra)),
		('allo-product', 870, 580, (a_hybrid, b_hybrid)),
	)
	for stage, x, y, genomes in cells:
		product = len(genomes) == 2
		body.append(f'<g id="c43-{stage}" data-chromosome-count="{sum(map(len, genomes))}" '
			f'transform="translate({x} {y})">')
		body.append(f'<g transform="scale({1.27 if product else 1} {1.31 if product else 1})">'
			f'<path d="{outline}" fill="#F4ECDC" stroke="#667A80" stroke-width="2.7"/>'
			f'<path d="{shadow}" fill="#E4D9C3"/>'
			'<path d="M -114,-40 C -95,-76 -56,-88 -24,-89" fill="none" stroke="#FFFAF0" '
			'stroke-width="4.5" stroke-linecap="round"/></g>')
		for index, genome in enumerate(genomes):
			baseline = 122*index-61 if product else 0
			for column, (model, (cx, cy, angle)) in enumerate(zip(genome,
				((-80, -1, -13), (-27, 2, 9), (40, -8, -17), (91, 9, 14)), strict=True), 1):
				body.append(_rod(f'c43-{stage}-{index+1}-{column}', model, cx, baseline+cy,
					19, palette, angle=angle, scale=.94 if product else 1))
		body.append('</g>')
	body.append(_arrow((230, 340), (230, 423)))
	body.append(_arrow((870, 365), (870, 423)))
	body.append('<path d="M 708,336 Q 708,347 724,347 H 853 Q 870,347 870,365 '
		'M 1040,336 Q 1040,347 1024,347 H 887 Q 870,347 870,365" '
		'fill="none" stroke="#263B48" stroke-width="3"/>')
	for x in (255, 870):
		body.append(drawing.line(x, 723, x, 735, color='#667A80', width=2))
	body.append(_labels((
		(255, 46, 'Autopolyploidy', 32), (873, 46, 'Allopolyploidy', 32),
		(255, 100, 'Species A (diploid)', 25), (708, 100, 'Species A (diploid)', 25),
		(1040, 100, 'Species B (diploid)', 25),
		(255, 765, 'Two complete diploid A genomes', 23),
		(870, 765, 'Complete diploid A genome plus', 23), (870, 792, 'complete diploid B genome', 23),
		(255, 827, 'New autotetraploid species', 25), (870, 827, 'New allotetraploid species', 25),
	)))
	for x, y, label in (
		(264, 371, 'Sexual or asexual'), (264, 400, 'polyploidization'),
		(899, 378, 'Hybridization accompanied'), (899, 404, 'by sexual or asexual'),
		(899, 430, 'polyploidization'),
	):
		body.append(drawing.text(x, y, label, size=23, color=INK, anchor='start'))
	_write(output, 43, (1200, 841), 'Autopolyploidy and allopolyploidy',
		'Each diploid parent has two long and two short chromosomes. Dark colors identify species A and light '
		'colors identify species B. The autotetraploid contains eight A chromosomes. '
		'The allotetraploid contains four A and four B chromosomes.', ''.join(body))


def build(output_dir: Path) -> None:
	"""Generate the seven ploidy review SVGs in one directory."""
	output_dir.mkdir(parents=True, exist_ok=True)
	for figure in (_c37, _c38, _c39, _c40, _c41, _c42, _c43):
		figure(output_dir)
