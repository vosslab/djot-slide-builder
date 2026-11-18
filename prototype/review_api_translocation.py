"""Source-backed reciprocal and Robertsonian figures for the chromosome review."""

import math
from pathlib import Path

from prototype.make_chromosome_engine_mini2 import _c63_chromatids
import svg_tools.chromosomes as chromosomes
import svg_tools.chromosome_topology as topology
import svg_tools.drawing as drawing
import svg_tools.parts as parts
import svg_tools.text as text


INK = '#213449'
MUTED = '#536976'
ADJACENT = '#A2263B'
ALTERNATE = '#166758'
RECIPROCAL = {
	'X': ('#B74300', '#FFDFCC', 'X'),
	'Y': ('#003366', '#CCE6FF', 'Y'),
	'2': ('#BFFF80', '#E6FFCC', '2'),
	'2-wildtype': ('#BFFF80', '#E6FFCC', '2'),
}
HUMAN = {
	'4': ('#EE9D1C', '#FFE8C1', '4'),
	'12': ('#94C950', '#E6FFCC', '12'),
}
ROBERTSONIAN = {
	'14': ('#CB4D52', '#FADADC', '14'),
	'21': ('#2473AD', '#D1E7FC', '21'),
}
RECIPROCAL_PRODUCTS = (
	('Adjacent-1', '25%', (1, 2), (3, 4)),
	('Adjacent-2', '25%', (1, 3), (2, 4)),
	('Alternate', '50%', (1, 4), (2, 3)),
)
ROBERTSONIAN_PRODUCTS = (
	('Adjacent-1', '1/4', ('rob', '21'), ('14',), 'rob(14;21) +21', '-21'),
	('Adjacent-2', '1/4', ('rob', '14'), ('21',), 'rob(14;21) +14', '-14'),
	('Alternate', '1/2', ('rob',), ('21', '14'), 'rob(14;21)', 'normal'),
)


#============================================
def _appearance(colors: dict[str, tuple[str, str, str]]) -> dict:
	"""Paint source material and identify its active centromere."""
	palette = {(source, 'body'): body for source, (body, _, _) in colors.items()}
	collars = {(source, f'{source}.cen'): chromosomes.CentromereStyle(label, collar)
		for source, (_, collar, label) in colors.items()}
	return {'palette': palette, 'centromere_styles': collars}


#============================================
def _label(x: float, y: float, value: str, size: float, *, color: str = INK,
	anchor: str = 'middle', bold: bool = False) -> str:
	return text.label(x, y, value, size=size, color=color, anchor=anchor, bold=bold).fragment


#============================================
def _rod(name: str, model: topology.Chromatid, x: float, y: float, scale: float,
	width: float, appearance: dict) -> parts.SvgPart:
	end = x + model.length * scale
	return chromosomes.render(name, model, points=((x, y), (end, y)),
		width=width, scale=scale, **appearance)


#============================================
def _sisters(name: str, pair: topology.SisterPair, paths: tuple[str, str],
	width: float, appearance: dict) -> parts.SvgPart:
	"""Paint two independent centerlines and put one belt on their active sites."""
	first, second = [chromosomes.render_path(f'{name}-{index}', model, path,
		width=width, draw_centromeres=False, **appearance)
		for index, (model, path) in enumerate(zip((pair.first, pair.second), paths, strict=True))]
	site, = (site for site in topology.project_centromeres(pair.first) if site.active)
	belt = chromosomes._sister_belt_part(f'{name}-belt', first.anchors['centromere'],
		second.anchors['centromere'], width,
		style=appearance['centromere_styles'][site.source_id, site.id])
	belt = parts.SvgPart(belt.fragment, belt.bounds, {
		'center': tuple((a + b) / 2
			for a, b in zip(first.anchors['centromere'], second.anchors['centromere'], strict=True)),
	})
	return parts.group({'first': first, 'second': second, 'belt': belt})


#============================================
def _elbows(x: float, y: float, vertical: float, sideways: int, length: float,
	width: float, radius: float, *, down: int = 1) -> tuple[str, str]:
	"""Give the two sisters equal arc length around a shared quarter turn."""
	paths = []
	corner_y = y + down * vertical
	center_x = x + sideways * radius
	sweep = int(sideways != down)
	for offset in (-width * .56, width * .56):
		curve = radius + offset
		start_x = center_x - sideways * curve
		turn_y = corner_y + down * curve
		end_x = center_x + sideways * (length - vertical - math.pi / 2 * curve)
		paths.append(f'M {start_x} {y} V {corner_y} A {curve} {curve} 0 0 {sweep} '
			f'{center_x} {turn_y} H {end_x}')
	return tuple(paths)


#============================================
def _c62(path: Path, models: dict[int, topology.Chromatid]) -> None:
	"""Compare the numbered Drosophila complement with its alternate orientation."""
	appearance = _appearance(RECIPROCAL)
	body = _label(35, 44, 'Chromosome complement', 33, anchor='start', bold=True)
	for row, (number, label) in enumerate(((4, 'Derivative 2'), (1, 'Derivative X'),
		(2, 'Normal 2'), (3, 'Normal Y'))):
		y = 128 + row * 111
		body += _label(36, y - 27, f'{number}  {label}', 28, anchor='start')
		body += _rod(f'c62-reference-{number}', models[number], 37, y, 6.3, 27, appearance).fragment

	body += drawing.line(465, 26, 465, 548, color='#CDD9E0', width=2)
	body += _label(818, 44, 'Metaphase I', 33, bold=True)
	poles = ((506, 286), (1159, 286))
	parts_by_id = {}
	for number, x, y, straight, side, down in (
		(1, 770, 78, 114, -1, 1), (3, 882, 78, 114, 1, 1),
		(2, 770, 514, 143, -1, -1), (4, 882, 514, 143, 1, -1),
	):
		model = models[number]
		paths = _elbows(x, y, straight, side, model.length * 5.4, 16, 34, down=down)
		parts_by_id[number] = _sisters(f'c62-spindle-{number}', topology.replicate(model),
			paths, 16, appearance)
	for number, pole, outer in ((1, 0, 115), (3, 1, 115), (2, 1, 535), (4, 0, 535)):
		px, py = poles[pole]
		ax, ay = parts_by_id[number].anchors['belt.center']
		control_x = px + (ax - px) * .35
		body += (f'<path d="M {px},{py} Q {control_x},{outer} {ax},{ay}" fill="none" '
			f'stroke="#607885" stroke-width="3.4"/>')
	for x, y in poles:
		body += f'<circle cx="{x}" cy="{y}" r="7" fill="#536976"/>'
	for number, part in parts_by_id.items():
		body += part.fragment
		x, y = part.anchors['belt.center']
		label_y = y - 12 if number in (1, 3) else y + 10
		body += _label(x + (-30 if number in (1, 2) else 30), label_y, str(number), 29,
			anchor=('end' if number in (1, 2) else 'start'), bold=True)
	body += _label(826, 561, '4 chromosomes / 8 chromatids', 30, bold=True)
	drawing.write_svg(path, 1190, 582, 'Numbered Drosophila chromosomes at metaphase I',
		'The reference complement lists derivative chromosome 2 (4), derivative X (1), '
		'normal chromosome 2 (2), and normal Y (3). The four replicated chromosomes form a '
		'quadrivalent. The left pole connects to 1 and 4; the right connects to 2 and 3. '
		'Each centromere belt connects both sister chromatids.', body)


#============================================
def _c64(path: Path, normal_y: topology.Chromatid) -> None:
	"""Enlarge chromosome 3 of the Drosophila complement."""
	body = _label(38, 105, 'Normal Y', 61, anchor='start', bold=True)
	body += _rod('c64-normal-y', normal_y, 361, 82, 18.6, 62,
		_appearance(RECIPROCAL)).fragment
	drawing.write_svg(path, 1160, 163, 'Normal Drosophila Y chromosome',
		'Chromosome 3 from the numbered parent complement. The centromere is marked Y.', body)


#============================================
def _human_models() -> dict[int, topology.Chromatid]:
	"""Use proportions and centromere positions from the four source strips."""
	normal_4 = topology.chromosome('4', length=120, centromere=.245)
	normal_12 = topology.chromosome('12', length=62, centromere=.23)
	partner_4 = topology.copy(normal_4, '4-translocated')
	partner_12 = topology.copy(normal_12, '12-translocated')
	head_4, tip_4 = topology.split(partner_4, 88 / 120)
	head_12, tip_12 = topology.split(partner_12, 30 / 62)
	der_4 = topology.join(head_4, tip_12)
	der_12 = topology.join(head_12, tip_4)
	topology.validate_conservation((partner_4, partner_12), (der_4, der_12))
	return {1: der_4, 2: normal_12, 3: normal_4, 4: der_12}


#============================================
def _c65(path: Path) -> None:
	"""Track the human t(4;12) products without the source's redundant generic inset."""
	models = _human_models()
	appearance = _appearance(HUMAN)
	body = ''
	for column, (number, label) in enumerate(((1, 'Derivative 4'), (2, 'Normal 12'),
		(3, 'Normal 4'), (4, 'Derivative 12'))):
		x = 31 + column * 302
		body += _label(x, 39, f'{number}  {label}', 29, anchor='start', bold=True)
		body += _rod(f'c65-reference-{number}', models[number], x, 78, 1.93, 26, appearance).fragment

	body += drawing.line(23, 113, 1197, 113, color='#CDD9E0', width=2)
	for column, (heading, frequency, first, second) in enumerate(RECIPROCAL_PRODUCTS):
		x = 24 + 401 * column
		color = ALTERNATE if column == 2 else ADJACENT
		body += _label(x + 185, 158, f'{heading} ({frequency})', 34, color=color, bold=True)
		statuses = ('Balanced translocation', 'Normal') if column == 2 else ('Unbalanced', 'Unbalanced')
		for row, (product, status) in enumerate(zip((first, second), statuses, strict=True)):
			top = 176 + 176 * row
			body += (f'<rect x="{x}" y="{top}" width="373" height="161" rx="14" '
				f'fill="#F7F9FC" stroke="{color}" stroke-width="2"/>')
			body += _label(x + 186, top + 38, f'{product[0]} + {product[1]}', 30, bold=True)
			for index, number in enumerate(product):
				y = top + 72 + index * 34
				body += _label(x + 40, y + 8, str(number), 24, bold=True)
				body += _rod(f'c65-gamete-{column}-{row}-{number}', models[number],
					x + 67, y, 1.93, 24, appearance).fragment
			frequency_label = f'25% {status.lower()}' if column == 2 else status
			body += _label(x + 186, top + 144, frequency_label, 25, color=color)
	body += _label(409, 555, '50% unbalanced in this example', 29, color=ADJACENT, bold=True)
	drawing.write_svg(path, 1220, 577, 'Six products of a human chromosome 4;12 translocation',
		'Adjacent-1 (25%) yields 1 + 2 or 3 + 4. Adjacent-2 (25%) yields 1 + 3 or 2 + 4. '
		'All adjacent types have a duplicated and a missing interval. Alternate (50%) yields '
		'1 + 4 or 2 + 3: 25% balanced translocation and 25% normal. Each type is shown once. '
		'Gold marks chromosome 4 ancestry and green marks chromosome 12 ancestry. Percentages '
		'are those assumed in the lecture example.', body)


#============================================
def _robertsonian_models() -> tuple[dict[str, topology.Chromatid], topology.Chromatid]:
	"""Join acrocentric long arms and conserve the short-arm product separately."""
	normal_14 = topology.chromosome('14', length=146, centromere=21 / 146)
	normal_21 = topology.chromosome('21', length=101, centromere=18 / 101)
	partner_14 = topology.copy(normal_14, '14-fusing')
	partner_21 = topology.copy(normal_21, '21-fusing')
	short_14, long_14 = topology.split(partner_14, 18 / 146)
	short_21, long_21 = topology.split(partner_21, 15 / 101)
	fused = topology.join(topology.reverse(long_14), long_21)
	fused = topology.with_centromere_activity(fused, '21.cen', active=False)
	short_product = topology.join(short_14, topology.reverse(short_21))
	topology.validate_conservation((partner_14, partner_21), (fused, short_product))
	return {'14': normal_14, '21': normal_21, 'rob': fused}, short_product


#============================================
def _pole_fibers(pole: tuple[float, float], anchors: tuple[tuple[float, float], ...]) -> str:
	"""Connect each pole only to the centromeres traveling toward it."""
	px, py = pole
	segments = [f'M {px},{py} L {x},{y}' for x, y in anchors]
	fibers = (f'<path d="{" ".join(segments)}" fill="none" stroke="#506E80" stroke-width="2.8"/>'
		f'<circle cx="{px}" cy="{py}" r="5" fill="#506E80"/>')
	return fibers


#============================================
def _c67(path: Path, models: dict[str, topology.Chromatid]) -> None:
	"""Orient the same three replicated chromosomes toward different poles."""
	appearance = _appearance(ROBERTSONIAN)
	pairs = {key: topology.replicate(model) for key, model in models.items()}
	body = _label(612, 42, 'Metaphase I', 34, bold=True)
	for index, (heading, _, first, second, _, _) in enumerate(ROBERTSONIAN_PRODUCTS):
		x = 208 + index * 402
		body += _label(x, 98, f'{heading} segregation', 30, bold=True)
		fusion_paths = _elbows(x - 19, 169, 106, -1, models['rob'].length, 12, 23)
		fused = _sisters(f'c67-{index}-fused', pairs['rob'], fusion_paths, 12, appearance)
		chr_14 = chromosomes.render_sisters(f'c67-{index}-normal-14', pairs['14'],
			start=(x + 42, 332), end=(x + 32, 191), width=12, **appearance)
		chr_21 = chromosomes.render_sisters(f'c67-{index}-normal-21', pairs['21'],
			start=(x + 4, 379), end=(x - 91, 340), width=12, **appearance)
		chromosome_parts = {'rob': fused, '14': chr_14, '21': chr_21}
		anchors = {'rob': fused.anchors['belt.center'], '14': chr_14.anchors['centromere'],
			'21': chr_21.anchors['centromere']}
		relative_poles = (
			((-173, 286), (172, 318)),
			((-8, 130), (42, 483)),
			((163, 200), (-147, 429)),
		)
		(first_x, first_y), (second_x, second_y) = relative_poles[index]
		pole_1, pole_2 = (x + first_x, first_y), (x + second_x, second_y)
		body += _spindle_outline(pole_1, pole_2, spread=(.58, .81, .59)[index])
		body += _pole_fibers(pole_1, tuple(anchors[key] for key in first))
		body += _pole_fibers(pole_2, tuple(anchors[key] for key in second))
		for part in chromosome_parts.values():
			body += part.fragment

	for index, (key, label) in enumerate((('14', 'Chromosome 14'), ('21', 'Chromosome 21'),
		('rob', 'rob(14;21)'))):
		x = 81 + index * 402
		body += _rod(f'c67-key-{key}', models[key], x, 534, .53, 12, appearance).fragment
		body += _label(x + 128, 542, label, 28, anchor='start')
	drawing.write_svg(path, 1220, 565, 'Three Robertsonian translocation orientations',
		'Each metaphase-I spindle shows one replicated chromosome 14, one replicated chromosome '
		'21, and one replicated rob(14;21). Adjacent-1 sends rob with 21, adjacent-2 sends rob '
		'with 14, and alternate sends rob to one pole and both normal acrocentrics to the '
		'other. The model uses the rearranged chromosome 14 centromere as the single active '
		'site. The short-arm product is usually lost before this stage.', body)


#============================================
def _spindle_outline(first: tuple[float, float], second: tuple[float, float], *, spread: float) -> str:
	"""Draw the faint outer and interpolar fibers behind the centromere attachments."""
	x1, y1 = first
	x2, y2 = second
	mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
	ortho_x, ortho_y = (y1 - y2) * spread, (x2 - x1) * spread
	paths = []
	for offset in (-1, -.57, .57, 1):
		cx, cy = mid_x + offset * ortho_x, mid_y + offset * ortho_y
		paths.append(f'M {x1},{y1} Q {cx},{cy} {x2},{y2}')
	return f'<path d="{" ".join(paths)}" fill="none" stroke="#AEBEC8" stroke-width="2.1"/>'


#============================================
def _c68(path: Path, models: dict[str, topology.Chromatid]) -> None:
	"""Draw all four meiotic products for each source spindle orientation."""
	appearance = _appearance(ROBERTSONIAN)
	reversed_models = {key: topology.reverse(model) for key, model in models.items()}
	body = _label(612, 38, 'Gametes after meiosis II', 34, bold=True)
	for column, (heading, frequency, first, second, first_label, second_label) in enumerate(ROBERTSONIAN_PRODUCTS):
		x = 210 + 400 * column
		color = ALTERNATE if column == 2 else ADJACENT
		body += _label(x, 87, f'{heading} ({frequency})', 32, color=color, bold=True)
		for row, (product, label) in enumerate(((first, first_label), (first, first_label),
			(second, second_label), (second, second_label))):
			y = 147 + row * 96
			body += (f'<ellipse cx="{x}" cy="{y}" rx="183" ry="43" fill="#FBF1DC" '
				'stroke="#AE793F" stroke-width="2"/>')
			screen_models = [reversed_models[key] if (key == '21' or (column > 0 and key == 'rob')
				or (column != 1 and key == '14')) else models[key] for key in product]
			scale, gap = .78, 16
			length = sum(model.length for model in screen_models) * scale + gap * (len(product) - 1)
			left = x - length / 2
			for index, model in enumerate(screen_models):
				body += _rod(f'c68-gamete-{column}-{row}-{index}', model, left, y - 10,
					scale, 15, appearance).fragment
				left += model.length * scale + gap
			body += _label(x, y + 25, label, 25)

	body += drawing.line(31, 489, 791, 489, color=ADJACENT, width=3)
	body += drawing.line(822, 489, 1194, 489, color=ALTERNATE, width=3)
	body += _label(410, 534, 'Unbalanced gametes', 31, color=ADJACENT, bold=True)
	body += _label(1010, 534, 'Balanced gametes', 31, color=ALTERNATE, bold=True)
	drawing.write_svg(path, 1220, 551, 'Robertsonian gamete products',
		'Adjacent-1 segregation yields two rob(14;21) +21 gametes and two -21 gametes. '
		'Adjacent-2 yields two rob(14;21) +14 gametes and two -14 gametes. Alternate yields '
		'two balanced rob(14;21) gametes and two normal gametes. A +21 gamete can yield a '
		'zygote with trisomy 21 after fertilization.', body)


#============================================
def build(output_dir: Path) -> None:
	"""Regenerate the translocation review figures through the shared renderer."""
	output_dir.mkdir(parents=True, exist_ok=True)
	models = _c63_chromatids()
	_c62(output_dir / 'c62.drawn.svg', models)
	_c64(output_dir / 'c64.drawn.svg', models[3])
	_c65(output_dir / 'c65.drawn.svg')
	robertsonian, _short_product = _robertsonian_models()
	_c67(output_dir / 'c67.drawn.svg', robertsonian)
	_c68(output_dir / 'c68.drawn.svg', robertsonian)
