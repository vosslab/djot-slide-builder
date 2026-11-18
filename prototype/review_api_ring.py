"""C48 diagram of direct-repeat recombination and its two products."""

import math
import pathlib

import svg_tools.annotations
import svg_tools.chromosome_topology as topology
import svg_tools.chromosomes as chromosomes
import svg_tools.drawing as drawing
import svg_tools.parts


WIDTH = 28
INK = '#344651'
REGIONS = ((0, 'left-flank'), (.18, 'left-repeat'), (.30, 'intervening'),
	(.70, 'right-repeat'), (.82, 'right-flank'))
PALETTE = {('direct-repeat', key): color for key, color in zip(
	(region for _, region in REGIONS), ('#A6BAC7', '#C695D4', '#D8B98E', '#8DBCE0', '#A6BAC7'))}
GENES = {'A': .329, 'B': .362, 'Y': .615, 'Z': .672}
GENE_PALETTE = {('direct-repeat', gene): '#F5E4CA' for gene in GENES}
FOLDS = (
	('M326 278 C400 278 450 325 450 420 C450 510 390 548 300 548 '
		'C200 548 175 520 175 475 C175 420 200 385 244 385'),
	('M326 313 C365 313 415 340 415 420 C415 485 375 513 300 513 '
		'C230 513 210 500 210 475 C210 445 225 420 244 420'),
)


#============================================
def _products(original: topology.Chromatid) -> tuple[topology.Chromatid, topology.Chromatid]:
	"""Exchange at the midpoints of the directly oriented repeats."""
	left_cut, right_cut = .24, .76
	left, remainder = topology.split(original, left_cut)
	ring, right = topology.split(remainder, (right_cut-left_cut)/(1-left_cut))
	return topology.join(left, right), ring


#============================================
def _label(x: float, y: float, value: str, size: float = 25) -> str:
	return drawing.text(x, y, value, size=size, color=INK)


#============================================
def _path(name: str, model: topology.Chromatid, geometry: str) -> svg_tools.parts.SvgPart:
	return chromosomes.render_path(name, model, geometry, width=WIDTH,
		palette=PALETTE, gene_palette=GENE_PALETTE, texture=False)


#============================================
def _continuation(x: float, y: float, direction: int) -> str:
	"""Indicate sequence beyond the window with a source-style chevron."""
	points = [(x-5*direction, y-9), (x+5*direction, y), (x-5*direction, y+9)]
	return svg_tools.annotations.connector(points, kind='callout', stroke_width=1.7).fragment


#============================================
def build(output_dir: pathlib.Path) -> None:
	"""Render two DNA ribbons as pictured, without assigning a replication stage."""
	material = topology.chromosome('direct-repeat', length=100, genes=GENES, regions=REGIONS)
	# The drawing shows a sequence window, so its flanks have no telomeres.
	original = topology.Chromatid(material.id, material.spans, ('break', 'break'))
	copies = original, topology.copy(original, 'direct-repeat-second')
	products = tuple(_products(copy) for copy in copies)
	topology.validate_conservation(copies, tuple(product for pair in products for product in pair))

	start = []
	clips = [
		'<clipPath id="fold-in-clip"><rect width="330.5" height="630"/></clipPath>',
		'<clipPath id="fold-out-clip"><rect x="239.5" width="760.5" height="630"/></clipPath>',
	]
	folded = []
	overpass = []
	deletions = []
	rings = []
	for index, (copy, (deletion, ring)) in enumerate(zip(copies, products), start=1):
		offset = (index-1)*35
		direction = 1 if index == 1 else -1
		if tuple(gene.allele for gene in topology.project_genes(ring)) != tuple(GENES):
			raise ValueError('C48 ring must contain the intervening alleles in order')

		y = 117+offset
		part = _path(f'initial-{index}', copy, f'M40 {y} H610')
		start.extend((part.fragment, _continuation(40, y, direction),
			_continuation(610, y, direction), _label(325, y+5, '...', 22)))

		# Place the repeat blocks on the two straight arms of the schematic folded pose.
		incoming, remainder = topology.split(copy, .30)
		loop, outgoing = topology.split(remainder, (.70-.30)/(1-.30))
		y_in, y_out = 278+offset, 385+offset
		fold = _path(f'fold-loop-{index}', loop, FOLDS[index-1])
		# Trim the overlapping internal edges and reveal only the upper ribbon at the crossing.
		clip_id = f'fold-loop-clip-{index}'
		clip_geometry = (f'M0 0 H1000 V630 H0 Z M0 {y_in-15} H330 V{y_in+15} H0 Z '
			'M240 367 H1000 V438 H240 Z')
		clips.append(f'<clipPath id="{clip_id}"><path clip-rule="evenodd" d="{clip_geometry}"/></clipPath>')
		folded.extend((f'<g clip-path="url(#{clip_id})">', fold.fragment, '</g>',
			'<g clip-path="url(#fold-in-clip)">',
			_path(f'fold-in-{index}', incoming, f'M65 {y_in} H334').fragment, '</g>',
			_label(300, 553-offset, '...', 22), _continuation(65, y_in, direction)))
		overpass.extend(('<g clip-path="url(#fold-out-clip)">',
			_path(f'fold-out-{index}', outgoing, f'M236 {y_out} H512').fragment, '</g>',
			_continuation(512, y_out, direction)))

		y_del = 220+offset
		x_end = 690+570*deletion.length/copy.length
		deletions.extend((_path(f'deletion-{index}', deletion, f'M690 {y_del} H{x_end}').fragment,
			_continuation(690, y_del, direction), _continuation(x_end, y_del, direction)))

		radius = 108-offset
		closed = chromosomes.render_ring(f'ring-{index}', ring, center=(810, 453),
			width=WIDTH, scale=math.tau*radius/ring.length, palette=PALETTE,
			gene_palette=GENE_PALETTE, texture=False)
		rings.extend((closed.fragment, _label(810, 453+radius+5, '...', 22)))

	body = [
		'<defs>', *clips, '</defs>',
		'<g id="initial">', *start,
		_label(325, 36, 'Repeated DNA sequences with'),
		_label(325, 65, 'same (direct) orientation.'),
		drawing.line(205, 77, 177, 101, color=INK, width=1.8),
		drawing.line(447, 77, 473, 101, color=INK, width=1.8),
		'</g>',
		svg_tools.annotations.connector([(300, 184), (300, 237)], head_size=17).fragment,
		'<g id="folded">', *folded,
		'<g id="outgoing-overpass">', *overpass, '</g>',
		'<path id="exchange-x" d="M267 338 L288 359 M288 338 L267 359" '
		'fill="none" stroke="#20252B" stroke-width="3"/>',
		'</g>',
		svg_tools.annotations.connector([(545, 338), (650, 252)], head_size=17).fragment,
		svg_tools.annotations.connector([(545, 484), (658, 461)], head_size=17).fragment,
		'<g id="deletion">', *deletions, _label(825, 301, 'Deletion', 27), '</g>',
		'<g id="acentric-ring">', *rings, _label(810, 608, 'Acentric ring fragment (lost)'), '</g>',
	]
	drawing.write_svg(output_dir / 'c48.drawn.svg', 1000, 630, 'Direct-repeat recombination',
		'Two parallel ribbons have directly oriented purple and blue repeats around A B ... Y Z. '
		'The ribbons fold so the repeats can exchange at the X. The outgoing arms pass over the '
		'right bends. The shorter deletion product joins purple to blue. The closed acentric ring '
		'retains A B ... Y Z, with blue joined to purple. Chevrons show continuation beyond the '
		'sequence window. The paired ribbons have no specified molecular or replication state.',
		''.join(body))
