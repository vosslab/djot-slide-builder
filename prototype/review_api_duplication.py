"""Rebuild C53 and C54 from the LECT12E tandem and X-linked opsin schematics."""

import math
import pathlib

import svgpathtools

import svg_tools.chromosome_topology as topology
import svg_tools.chromosomes as chromosomes
import svg_tools.drawing as drawing
import svg_tools.parts as parts
import svg_tools.text as text


FONT = 'Atkinson Hyperlegible Next'
INK = '#213547'
LEADER = '#526879'
REPEAT_COLOR = '#995819'
REPEAT_LENGTH = 40
CHROMATID_WIDTH = 25


#============================================
def _shoulder(x: float, y: float, neck: float) -> str:
	"""Give each sister its own path into and out of the shared centromere."""
	return (f'M{x} {y} C{x+30} {y} {x+52} {neck} {x+80} {neck} '
		f'S{x+130} {y} {x+160} {y}')


#============================================
def _tandem_figure(path: pathlib.Path) -> None:
	"""Follow the two misaligned repeats and their reciprocal source material."""
	upper_end = _shoulder(40, 180, 160) + ' C221 180 230 200 251 220'
	lower_end = _shoulder(0, 260, 280) + ' H200 C221 260 230 240 251 220'
	first_cut = svgpathtools.parse_path(upper_end).length()
	second_cut = first_cut + REPEAT_LENGTH
	length = first_cut + 120
	half_repeat = REPEAT_LENGTH/2
	centromere = svgpathtools.parse_path(_shoulder(0, 180, 160))[0].length()
	regions = ((0, 'proximal'), ((first_cut-half_repeat)/length, 'L'),
		((first_cut+half_repeat)/length, 'R'), ((second_cut+half_repeat)/length, 'distal'))
	blue = topology.chromosome('blue', length=length, centromere=centromere/length,
		regions=regions)
	violet = topology.homolog(blue, 'violet')
	blue_pair, violet_pair = topology.replicate(blue), topology.replicate(violet)
	inputs = (blue_pair.first, blue_pair.second, violet_pair.first, violet_pair.second)
	blue_left, blue_right = topology.split(inputs[1], first_cut/length)
	violet_left, violet_right = topology.split(inputs[2], second_cut/length)
	single = topology.join(blue_left, violet_right)
	triple = topology.join(violet_left, blue_right)
	products = (inputs[0], single, triple, inputs[3])
	topology.validate_conservation(inputs, products)
	copy_lengths = tuple(sum(region.stop - region.start
		for region in topology.project_regions(model) if region.region_id in ('L', 'R'))
		for model in products)
	if any(not math.isclose(observed, count*REPEAT_LENGTH)
		for observed, count in zip(copy_lengths, (2, 1, 3, 2))) or any(
			len(topology.project_centromeres(model)) != 1 for model in products):
		raise ValueError('Expected 2, 1, 3, and 2 copies with one centromere per product')

	palette = {(source, region): REPEAT_COLOR if region in ('L', 'R') else color
		for source, color in (('blue', '#287caf'), ('violet', '#6076b2'))
		for _, region in regions}
	body = []

	def pose(name: str, model: topology.Chromatid, path_d: str, *,
		attached: bool = False, label_repeats: bool = False) -> parts.SvgPart:
		curve = svgpathtools.parse_path(path_d)
		curve_length = curve.length()
		end_x = curve.end.real + model.length - curve_length
		part = chromosomes.render_path(f'c53-{name}', model, f'{path_d} H{end_x:.9f}',
			width=CHROMATID_WIDTH, palette=palette, texture=False,
			draw_centromeres=not attached)
		body.append(part.fragment)
		projected = topology.project_regions(model)
		for index, (left, right) in enumerate(zip(projected, projected[1:]), start=1):
			if left.region_id in ('L', 'R') and right.region_id in ('L', 'R') and (
				left.source_id == right.source_id):
				x, y = part.anchors[f'boundary_{index}']
				tangent = curve.unit_tangent(curve.ilength(left.stop)) if left.stop < curve_length else 1
				delta = 1j * tangent * (CHROMATID_WIDTH/2 - 1)
				body.append(drawing.line(x-delta.real, y-delta.imag, x+delta.real,
					y+delta.imag, color='#56330f', width=1.7))
		if label_repeats:
			for index, region in enumerate(projected):
				if region.region_id in ('L', 'R'):
					x, y = part.anchors[f'segment_{index}']
					body.append(drawing.text(x, y+8, region.region_id,
						size=22, color='#ffffff', font=FONT))
		return part

	def belt(name: str, first: parts.SvgPart, second: parts.SvgPart) -> None:
		first_x, first_y = first.anchors['centromere']
		second_x, second_y = second.anchors['centromere']
		if not math.isclose(first_x, second_x, abs_tol=.01):
			raise ValueError('Sister poses must bring both centromeres into the same belt')
		part = chromosomes.centromere_part(f'c53-{name}', thickness=CHROMATID_WIDTH,
			across=abs(first_y - second_y) + CHROMATID_WIDTH*1.3)
		body.append(parts.transform(part, x=(first_x+second_x)/2,
			y=(first_y+second_y)/2).fragment)

	def pairing(stage: str, upper_x: float, lower_x: float, *, label_repeats: bool = False) -> parts.SvgPart:
		paths = (_shoulder(upper_x, 110, 130), _shoulder(upper_x, 180, 160),
			_shoulder(lower_x, 260, 280), _shoulder(lower_x, 330, 310))
		chromatids = [pose(f'{stage}-{index}', model, centerline,
			attached=True, label_repeats=label_repeats)
			for index, (model, centerline) in enumerate(zip(inputs, paths))]
		belt(f'{stage}-blue', *chromatids[:2])
		belt(f'{stage}-violet', *chromatids[2:])
		return chromatids[-1]

	for x, value in ((20, '(A) Normal pairing'), (394, '(B) Mispairing'),
		(790, '(C) Unequal crossing over'), (1210, '(D) Result of crossover')):
		body.append(text.label(x, 38, value, size=27, color=INK, bold=True,
			anchor='start').fragment)

	last = pairing('normal', 24, 24)
	body.append(drawing.text(198, 402, 'Tandem duplication', size=25, color=INK, font=FONT))
	for index in (1, 2):
		x, y = last.anchors[f'segment_{index}']
		body.append(drawing.line(178, 374, x, y+CHROMATID_WIDTH/2, color=LEADER, width=2))
	pairing('mispaired', 437, 397, label_repeats=True)

	exchange_start = len(body)
	upper_outer = pose('exchange-upper-outer', inputs[0], _shoulder(40, 110, 130),
		attached=True)
	lower_outer = pose('exchange-lower-outer', inputs[3], _shoulder(0, 330, 310),
		attached=True)
	upper_inner = pose('exchange-single', single, upper_end + ' C272 240 281 260 302 260',
		attached=True)
	lower_inner = pose('exchange-triple', triple, lower_end + ' C272 200 281 180 302 180',
		attached=True)
	belt('exchange-blue', upper_outer, upper_inner)
	belt('exchange-violet', lower_inner, lower_outer)
	exchange = ''.join(body[exchange_start:])
	body[exchange_start:] = [f'<g transform="translate(795 0)">{exchange}</g>']

	for x in (740, 1147):
		body.append(f'<path d="M{x} 220 h37 m-12 -9 l12 9 -12 9" fill="none" '
			f'stroke="{INK}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>')
	for index, (model, label) in enumerate(zip(products,
		('Duplication', 'Single copy', 'Triplication', 'Duplication'))):
		y = 95 + 90*index
		pose(f'product-{index}', model, f'M1215 {y} h1')
		body.append(drawing.text(1375, y+42, label, size=25, color=INK, font=FONT))

	drawing.write_svg(path, 1635, 430, 'Unequal crossing over expands or contracts a tandem duplication',
		'Two homologs each have two sister chromatids. In normal pairing the two amber repeats '
		'align. In mispairing, L on the blue homolog aligns with R on the violet homolog. '
		'The inner nonsister chromatids cross over inside those repeats. From top to bottom, '
		'the products carry two, one, three, and two copies. The two altered products exchange '
		'distal arms. Source: LECT12E slide 7, schematic lengths.', ''.join(body))


#============================================
def _opsin_figure(path: pathlib.Path) -> None:
	"""Keep the illustrated X and make the expanded arrays from scoped gene copies."""
	# Band edges and the neck are traced from the source illustration in LECT12E.
	edges = (330, 333, 340, 351, 381, 409, 434, 449, 466, 470, 480, 487,
		523, 527, 545, 581, 590, 619, 637, 649, 663, 675, 688, 710, 713, 733, 757, 765, 809)
	purple = {333, 351, 409, 449, 470, 487, 527, 581, 637, 663, 688, 713, 757}
	length = edges[-1] - edges[0]
	regions = tuple(((edge-edges[0])/length, f'band-{edge}') for edge in edges[:-1])
	model = topology.chromosome('X', length=length, centromere=(619-edges[0])/length,
		regions=regions)
	palette = {('X', f'band-{edge}'): '#776098' if edge in purple else '#EDCF90'
		for edge in edges[:-1]}
	chromosome = chromosomes.render_path('c54-x', model, f'M280 54 h{length}',
		width=42, palette=palette, texture=False)
	chromosome_x, chromosome_y = chromosome.anchors['start']
	body = [chromosome.fragment, drawing.text(247, 65, 'X', size=32, color=INK, font=FONT),
		f'<path d="M{chromosome_x} {chromosome_y+24} V96 L32 172 V249 H53 '
		f'M{chromosome_x} 96 L968 172 V249 H947" fill="none" stroke="{LEADER}" '
		'stroke-width="2" stroke-linejoin="round"/>']

	unit = 180
	r = topology.chromosome('red-opsin', length=unit, genes={'r': 70/unit})
	g = topology.chromosome('green-opsin', length=unit, genes={'g': 70/unit})
	for count in (1, 2, 3):
		red = topology.copy(r, f'array-{count}-red')
		array = topology.join(red, *(topology.copy(g, f'array-{count}-green-{i+1}')
			for i in range(count)))
		genes = topology.project_genes(array)
		if (tuple(gene.allele for gene in genes) != ('r',) + ('g',)*count
			or len({gene.copy_id for gene in genes}) != 1 + count):
			raise ValueError('Expected one red opsin followed by distinct green opsin copies')
		y = 249 + (count-1)*131
		body.extend((drawing.text(53, y-49, f'X chromosome: r + {count} g', size=28,
			color=INK, anchor='start', font=FONT),
			drawing.line(53, y, 947, y, color='#655a85', width=9)))
		for gene in genes:
			x = 115 + gene.position
			color = '#bb2028' if gene.allele == 'r' else '#007a00'
			body.append(f'<g id="c54-{gene.copy_id}"><rect '
				f'x="{x-70:g}" y="{y-25}" width="140" height="50" rx="9" fill="{color}"/>')
			body.append(drawing.text(x, y+10, gene.allele, size=30,
				color='#ffffff', font=FONT) + '</g>')

	drawing.write_svg(path, 1000, 560, 'Red and green pigment gene arrays on the X chromosome',
		'A banded X chromosome leads from its left tip to an enlarged gene array. The '
		'three schematic variants have one r gene followed by one, two, or three g genes, '
		'respectively. Source: LECT12E slide 10. Whole-chromosome bands come from the '
		'source illustration. The enlargement is schematic.', ''.join(body))


#============================================
def build(output_dir: pathlib.Path) -> None:
	"""Write the two LECT12E figures in the review artifact directory."""
	_tandem_figure(output_dir / 'c53.drawn.svg')
	_opsin_figure(output_dir / 'c54.drawn.svg')
