#!/usr/bin/env python3
"""Render three chromosome review sequences as transparent animated WebPs."""

import collections.abc
import io
import os
import pathlib
import subprocess
import tempfile

import PIL.Image

import prototype.make_chromosome_engine_mini2 as mini2
import svg_tools.chromosome_topology as topology
import svg_tools.chromosomes as chromosomes
import svg_tools.drawing as drawing
import svg_tools.palette
import svg_tools.parts


WIDTH, HEIGHT = 1200, 720
INK = '#213449'
STEP_MS = 80
Frame = tuple[str, int]


#============================================
def _label(x: float, y: float, value: str, size: float, *, anchor: str = 'middle',
	mono: bool = False) -> str:
	"""Outline captions for legibility over both light and dark backgrounds."""
	font = 'Atkinson Hyperlegible Mono' if mono else 'Atkinson Hyperlegible Next'
	text = drawing.text(x, y, value, size=size, color=INK, anchor=anchor, font=font)
	return ('<g stroke="#FFFFFF" stroke-width="6" stroke-linejoin="round" '
		f'paint-order="stroke">{text}</g>')


#============================================
def _stage(title: str, caption: str, scene: str) -> str:
	return _label(600, 82, title, 48) + scene + _label(600, 669, caption, 32)


#============================================
def _steps(count: int) -> collections.abc.Iterator[float]:
	"""Give each movement soft starts and stops."""
	for index in range(1, count + 1):
		t = index / count
		yield t*t*(3 - 2*t)


#============================================
def _allele_order(models: tuple[topology.Chromatid, ...]) -> tuple[str, ...]:
	return tuple(''.join(gene.allele for gene in topology.project_genes(model)) for model in models)


#============================================
def _break_ticks(x: float, y: float, width: float) -> str:
	half = width / 2
	return ''.join(drawing.line(x, y + side*(half + 5), x, y + side*(half + 22),
		color='#996000', width=5) for side in (-1, 1))


#============================================
def insertional_translocation() -> collections.abc.Iterator[Frame]:
	"""Move EF into the other chromosome and close both products."""
	title = 'Insertional translocation'
	x, donor_y, transit_y, recipient_y = 130, 232, 354, 476
	scale, width, gap = 1.78, 58, 12
	donor, recipient = mini2.c01_models()
	head, insert, tip, target_head, target_tail = mini2.c01_insertion_pieces(donor, recipient)
	pieces = head, insert, tip, target_head, target_tail
	products = topology.join(head, tip), topology.join(target_head, insert, target_tail)
	topology.validate_conservation((donor, recipient), pieces)
	topology.validate_conservation((donor, recipient), products)
	if _allele_order(products) != ('ABCDGH', 'JKLEFMNO'):
		raise ValueError('C01 must transfer EF into the recipient between L and M')

	donor_cut = x + scale*head.length
	target_cut = x + scale*target_head.length
	insert_length = scale*insert.length

	def rod(name: str, model: topology.Chromatid) -> svg_tools.parts.SvgPart:
		return chromosomes.render(name, model, points=((0, 0), (1, 0)), width=width,
			scale=scale, palette=mini2.C01_PALETTE, gene_palette=mini2.C01_GENE_PALETTE)

	row_labels = (_label(x, donor_y - 61, 'Donor', 27, anchor='start')
		+ _label(x, recipient_y - 61, 'Recipient', 27, anchor='start'))

	def rows(models: tuple[topology.Chromatid, ...]) -> str:
		return row_labels + ''.join(svg_tools.parts.transform(rod(f'row-{index}', model),
			x=x, y=y).fragment for index, (model, y) in enumerate(
				zip(models, (donor_y, recipient_y), strict=True)))

	intact = rows((donor, recipient))
	yield _stage(title, 'Follow the genes E and F', intact), 950
	marks = (_break_ticks(donor_cut, donor_y, width)
		+ _break_ticks(donor_cut + insert_length, donor_y, width)
		+ _break_ticks(target_cut, recipient_y, width))
	yield _stage(title, 'Two breaks release EF. One break opens the recipient.', intact + marks), 1250

	head_part, insert_part, tip_part, target_head_part, target_tail_part = (
		rod(f'piece-{index}', model) for index, model in enumerate(pieces))
	fixed = (row_labels + svg_tools.parts.transform(head_part, x=x, y=donor_y).fragment
		+ svg_tools.parts.transform(target_head_part, x=x, y=recipient_y).fragment)

	def transfer(insert_x: float, insert_y: float, donor_tip_x: float, target_tail_x: float) -> str:
		return (fixed + svg_tools.parts.transform(tip_part, x=donor_tip_x, y=donor_y).fragment
			+ svg_tools.parts.transform(target_tail_part, x=target_tail_x, y=recipient_y).fragment
			+ svg_tools.parts.transform(insert_part, x=insert_x, y=insert_y).fragment)

	donor_tip_x = donor_cut + insert_length + 2*gap
	for t in _steps(11):
		scene = transfer(donor_cut + gap, donor_y + t*(transit_y-donor_y),
			donor_tip_x, target_cut + gap)
		yield _stage(title, 'Separate EF from the donor', scene), STEP_MS
	for t in _steps(13):
		scene = transfer(donor_cut + gap + t*(target_cut-donor_cut), transit_y,
			donor_tip_x - t*(insert_length + gap), target_cut + gap + t*(insert_length + gap))
		yield _stage(title, 'Move EF to the opening in the recipient', scene), STEP_MS
	for t in _steps(12):
		scene = transfer(target_cut + gap*(1-t), transit_y + t*(recipient_y-transit_y),
			donor_cut + gap*(1-t), target_cut + insert_length + 2*gap*(1-t))
		yield _stage(title, 'Insert EF between L and M', scene), STEP_MS
	yield _stage(title, 'The donor loses EF. The recipient gains it.', rows(products)), 2250


#============================================
def single_crossover() -> collections.abc.Iterator[Frame]:
	"""Bring two inner chromatids together, exchange their tips, and show the products."""
	title = 'Single crossover'
	ab, wild, products = mini2.c22_products()
	parents = ab.first, ab.second, wild.first, wild.second
	topology.validate_conservation(parents, products)
	alleles = _allele_order(products)
	if alleles != ('ab', 'a+', '+b', '++'):
		raise ValueError('C22 must produce one parental and one recombinant chromatid per homolog')

	# Before exchange the tips stay in their starting lanes. A broad bend brings the
	# breaks together without pinching the chromosome bodies or turning the caps.
	approach = ((392, 268), (438, 268), (473, 268), (503, 274.9), (530, 288.71),
		(555, 300.17), (577, 304), (600, 297.14), (621, 283.18), (641, 271.44),
		(657, 268), (671, 268), (685, 268))

	def strands(model: tuple[topology.Chromatid, ...], bend: float, *, crossed: bool) -> str:
		template = mini2.C22_BEND if crossed else approach
		inner = tuple((x, 268 + bend*(y-268)) for x, y in template)
		poses = (((392, 220), (705, 220)), inner, tuple((x, 608-y) for x, y in inner),
			((392, 388), (705, 388)))
		body = mini2.c22_exchange_bodies(model, poses)
		return f'<g transform="translate(140 189) scale(2.24) translate(-392 -220)">{body}</g>'

	yield _stage(title, 'Start with two replicated homologs', strands(parents, 0, crossed=False)), 1000
	for t in _steps(20):
		scene = strands(parents, .48*t, crossed=False)
		yield _stage(title, 'The two inner nonsister chromatids meet between the loci', scene), STEP_MS

	contact = '<circle cx="554.4" cy="377.2" r="25" fill="none" stroke="#996000" stroke-width="5"/>'
	yield _stage(title, 'The nonsisters exchange tips',
		strands(products, 1, crossed=True) + contact), 950
	for t in _steps(20):
		scene = strands(products, 1-t, crossed=True)
		yield _stage(title, 'Follow the exchanged tips as the arms move apart', scene), STEP_MS

	key = ''
	for allele, model, y in zip(alleles, products, (189, 297, 458, 565), strict=True):
		key += _label(897, y + 8, allele, 33, anchor='start', mono=True)
		label = 'Recombinant' if model.junctions else 'Parental'
		key += _label(973, y + 7, label, 25, anchor='start')
	yield _stage(title, 'Two parental and two recombinant chromatids',
		strands(products, 0, crossed=True) + key), 2250


#============================================
def robertsonian_fusion() -> collections.abc.Iterator[Frame]:
	"""Join the long arms, then show what usually happens to the small product."""
	title = 'Robertsonian fusion'
	# Use the schematic material and colors from LECT13D slide 54 (C66).
	blue_cut, red_cut = 10/110, 5.6/51.6
	blue = topology.chromosome('A', length=110, centromere=blue_cut)
	red = topology.chromosome('B', length=51.6, centromere=red_cut)
	palette = {('A', 'body'): svg_tools.palette.shade('sky_blue', 'dark'),
		('B', 'body'): svg_tools.palette.shade('red', 'dark')}
	blue_short, blue_long = topology.split(blue, blue_cut)
	red_short, red_long = topology.split(red, red_cut)
	fused = topology.join(topology.reverse(blue_long), red_long)
	fused = topology.with_centromere_activity(fused, 'B.cen', active=False)
	short_product = topology.join(blue_short, topology.reverse(red_short))
	topology.validate_conservation((blue, red), (fused, short_product))
	if tuple(site.active for site in topology.project_centromeres(fused)) != (True, False):
		raise ValueError('C66 must retain two centromere sites with just one active')

	join_x, blue_y, red_y = 656, 244, 375
	short_x, short_y = 1007, 474
	scale, width, gap = 5, 31, 10

	def rod(name: str, model: topology.Chromatid, *, end_at_cut: bool = False) -> svg_tools.parts.SvgPart:
		x = -model.length*scale if end_at_cut else 0
		return chromosomes.render(name, model, points=((x, 0), (x+1, 0)),
			width=width, scale=scale, palette=palette)

	def place(part: svg_tools.parts.SvgPart, x: float, y: float, angle: float = 0) -> str:
		return svg_tools.parts.transform(part, x=x, y=y, rotation=angle).fragment

	blue_input = rod('blue-parent', topology.reverse(blue))
	red_input = rod('red-parent', topology.reverse(red))
	parents = (place(blue_input, join_x-blue_long.length*scale, blue_y)
		+ place(red_input, join_x-red_long.length*scale, red_y))
	yield _stage(title, 'Start with two acrocentric chromosomes', parents), 900
	marks = _break_ticks(join_x, blue_y, width) + _break_ticks(join_x, red_y, width)
	yield _stage(title, 'Break near both centromeres', parents + marks), 1000

	blue_base = rod('blue-long', topology.reverse(blue_long), end_at_cut=True)
	red_base = rod('red-long', red_long)
	blue_tip = rod('blue-short', blue_short, end_at_cut=True)
	red_tip = rod('red-short', topology.reverse(red_short))
	small = place(rod('short-product', short_product), short_x-blue_short.length*scale, short_y)
	for t in _steps(17):
		x = join_x + gap + t*(short_x - join_x - gap)
		scene = (place(blue_base, join_x-gap*(1-t), blue_y)
			+ place(red_base, join_x-gap + 2*gap*t, red_y, 180*(1-t))
			+ place(blue_tip, x-gap*t, blue_y+t*(short_y-blue_y), 180*(1-t))
			+ place(red_tip, x+gap*t, red_y+t*(short_y-red_y)))
		yield _stage(title, 'Turn the red long arm and bring the short arms together', scene), STEP_MS
	for t in _steps(12):
		scene = (place(blue_base, join_x, blue_y)
			+ place(red_base, join_x+gap*(1-t), red_y+t*(blue_y-red_y)) + small)
		yield _stage(title, 'Join the long arms near their centromeres', scene), STEP_MS

	main = place(rod('fused', fused), join_x-blue_long.length*scale, blue_y)
	main += (_label(join_x, blue_y-66, 'One active centromere', 27)
		+ drawing.line(join_x, blue_y-53, join_x, blue_y-24, color='#996000', width=4))
	yield _stage(title, 'Fusion makes a large chromosome and a small product',
		main + small + _label(short_x-10, short_y+57, 'Short-arm product', 27)), 1250
	for t in _steps(12):
		scene = main + f'<g opacity="{1-t}">{small}</g>'
		yield _stage(title, 'The short-arm product is usually lost', scene), STEP_MS
	yield _stage(title, 'The fused chromosome remains', main), 2000


#============================================
def _write_clip(path: pathlib.Path, sequence: collections.abc.Iterable[Frame]) -> None:
	"""Rasterize authored SVG frames and preserve alpha in the finished WebP."""
	frames, durations = [], []
	env = dict(os.environ, PANGOCAIRO_BACKEND='fc')
	for body, duration in sequence:
		svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
			f'viewBox="0 0 {WIDTH} {HEIGHT}">{body}</svg>')
		# ASVS 1.2.5: Pass SVG as stdin to a fixed command without shell interpretation.
		png = subprocess.run(('rsvg-convert',), input=svg.encode(), stdout=subprocess.PIPE,
			check=True, env=env).stdout
		with PIL.Image.open(io.BytesIO(png)) as image:
			frames.append(image.convert('RGBA'))
		durations.append(duration)
	frames[0].save(path, format='WEBP', save_all=True, append_images=frames[1:],
		duration=durations, loop=0, lossless=True, quality=90)


#============================================
def main() -> None:
	"""Generate and publish the three finished clips from the repository root."""
	root = pathlib.Path(subprocess.check_output(
		('git', 'rev-parse', '--show-toplevel'), text=True).strip())
	output = root / 'prototype/assets/chromosome_animations'
	output.mkdir(parents=True, exist_ok=True)
	scratch = root / '_temp'
	scratch.mkdir(exist_ok=True)
	clips = {
		'c01_insertional_translocation.webp': insertional_translocation,
		'c22_single_crossover.webp': single_crossover,
		'c66_robertsonian_fusion.webp': robertsonian_fusion,
	}
	with tempfile.TemporaryDirectory(dir=scratch) as temporary:
		staged = pathlib.Path(temporary)
		for filename, sequence in clips.items():
			_write_clip(staged / filename, sequence())
		for filename in clips:
			(staged / filename).replace(output / filename)
			print(output / filename)


if __name__ == '__main__':
	main()
