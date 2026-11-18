"""Build review figures C44-C46 from chromosome models and LECT12C scenes."""

import math
from pathlib import Path

from svg_tools import chromosome_topology as topology
from svg_tools import chromosomes
from svg_tools import drawing
from svg_tools import parts


INK = '#233345'
CONNECTOR = '#647681'


#============================================
def _label(x: float, y: float, value: str, size: float = 26, *, color: str = INK) -> str:
	return drawing.text(x, y, value, size=size, color=color)


#============================================
def _line(x1: float, y1: float, x2: float, y2: float) -> str:
	return drawing.line(x1, y1, x2, y2, color=CONNECTOR, width=2.8)


#============================================
def _x_glyph(name: str, model: topology.Chromatid, x: float, y: float,
	palette: dict[tuple[str, str], str], *, expressed: bool) -> str:
	"""Show the same X material as an open rod or compact Barr body."""
	if expressed:
		path = f'M{x} {y - 24} V{y + 24}'
		return chromosomes.render_path(name, model, path, width=13, palette=palette,
			texture=False, marker_size=(9, 15)).fragment
	# X-inactivation changes expression, independent of the centromere's attachment role.
	segments = tuple(chromosomes.Segment('', palette[region.source_id, region.region_id],
		region.stop - region.start) for region in topology.project_regions(model))
	compact = chromosomes.condensed_chromosome_part(name, chromosomes.Chromosome(segments),
		radius=12)
	return parts.transform(compact, x=x, y=y).fragment


#============================================
def _cell(name: str, x: float, y: float, homologs: tuple[topology.Chromatid, topology.Chromatid],
	palette: dict[tuple[str, str], str], *, silent: str | None = None) -> str:
	"""Keep both copies and their left/right order through each cell lineage."""
	membrane = (f'<ellipse cx="{x}" cy="{y}" rx="48" ry="43" fill="#F3F6F8" '
		f'stroke="{CONNECTOR}" stroke-width="2.4"/>')
	glyphs = []
	for model, offset in zip(homologs, (-18, 18)):
		identifier = f'{name}-{model.id}'
		copy = topology.copy(model, identifier)
		glyphs.append(_x_glyph(identifier, copy, x + offset, y, palette,
			expressed=model.id != silent))
	return f'<g id="{name}">{membrane}{"".join(glyphs)}</g>'


#============================================
def _state_key(prefix: str, model: topology.Chromatid, palette: dict[tuple[str, str], str],
	x: float, y: float) -> tuple[str, ...]:
	return (
		_x_glyph(f'{prefix}-active-key', model, x, y, palette, expressed=True),
		_label(x + 70, y + 8, 'Active X', 23),
		_x_glyph(f'{prefix}-inactive-key', model, x + 160, y, palette, expressed=False),
		_label(x + 290, y + 8, 'Inactive X (Barr body)', 23),
	)


#============================================
def _inactivation(output_dir: Path) -> None:
	first = topology.chromosome('X1', length=48, centromere=.28)
	second = topology.homolog(first, 'X2')
	homologs = (first, second)
	palette = {('X1', 'body'): '#B74300', ('X2', 'body'): '#076DAD'}
	# Source scene: zygote, four cleavage cells, four inactivation choices, eight descendants.
	body = [
		_label(135, 72, 'Zygote'),
		_label(135, 207, 'Early cleavage'),
		_label(135, 235, 'Both X chromosomes active', 20),
		_label(129, 366, 'Random X inactivation', 24),
		_label(121, 514, 'Somatic descendants', 21),
		_cell('zygote', 636, 64, homologs, palette),
	]
	for index, (x, silent) in enumerate(zip((336, 536, 736, 936), ('X1', 'X2', 'X1', 'X2'))):
		body.extend((
			_line(636, 108, x, 169),
			_cell(f'cleavage-{index}', x, 212, homologs, palette),
			_line(x, 256, x, 315),
			_cell(f'inactivation-{index}', x, 358, homologs, palette, silent=silent),
		))
		for offset in (-50, 50):
			body.extend((
				_line(x, 402, x + offset, 463),
				_cell(f'descendant-{index}-{x + offset}', x + offset, 506, homologs, palette,
					silent=silent),
			))
	body.extend(_state_key('lineage', first, palette, 345, 604))
	body.extend((
		_label(190, 613, 'X\u2081', color=palette['X1', 'body']),
		_label(253, 613, 'X\u2082', color=palette['X2', 'body']),
	))
	drawing.write_svg(output_dir / 'c44.drawn.svg', 1050, 648,
		'Random X inactivation is inherited within cell lineages',
		'Both X chromosomes are active at early cleavage. Each somatic descendant retains '
		'the inactive X of its lineage. A rod is active and a compact circle is inactive.',
		''.join(body))


#============================================
def _calico(output_dir: Path) -> None:
	orange = topology.chromosome('X-orange', length=48, centromere=.5, genes={'O': .78})
	black = topology.homolog(orange, 'X-black', alleles={'O': 'o'})
	homologs = (orange, black)
	palette = {('X-orange', 'body'): '#DA8A35', ('X-black', 'body'): '#29292D'}
	body = [
		_label(300, 37, 'Early embryo'),
		_label(300, 68, 'Both X-linked fur-color alleles active', 23),
		_cell('embryo', 300, 129, homologs, palette),
		_line(279, 169, 145, 280),
		_line(321, 169, 455, 280),
		_label(300, 258, 'Random X inactivation', 22),
		_cell('black-fur', 145, 324, homologs, palette, silent='X-orange'),
		_cell('orange-fur', 455, 324, homologs, palette, silent='X-black'),
		_label(145, 407, 'Black fur', 33),
		_label(455, 407, 'Orange fur', 33, color='#A84400'),
		_label(145, 443, 'Black-allele X active', 23),
		_label(145, 472, 'Orange-allele X inactive', 23),
		_label(455, 443, 'Orange-allele X active', 23),
		_label(455, 472, 'Black-allele X inactive', 23),
		_label(300, 524, 'Two cell populations in the adult cat', 28),
	]
	drawing.write_svg(output_dir / 'c45.drawn.svg', 600, 549,
		'Orange and black fur alleles in X-inactivation lineages',
		'The early embryo has the orange and black X-linked alleles. Each adult patch has '
		'two X chromosomes. The active orange allele gives orange fur and the active black '
		'allele gives black fur. The inactive X is drawn as a compact circle.', ''.join(body))


#============================================
def _par_crossover(output_dir: Path) -> None:
	# LECT12C depicts homologous short-arm tips with X longer than Y. Diagram units are schematic.
	par_length, exchanged = 68, 43
	first = topology.chromosome('X', length=326, centromere=.41,
		regions=((0, 'PAR'), (par_length/326, 'body')))
	second = topology.chromosome('Y', length=216, centromere=.44,
		regions=((0, 'PAR'), (par_length/216, 'body')))
	x_tip, x_body = topology.split(first, exchanged / first.length)
	y_tip, y_body = topology.split(second, exchanged / second.length)
	products = (topology.join(y_tip, x_body), topology.join(x_tip, y_body))
	topology.validate_conservation((first, second), products)
	for product, tip_origin in zip(products, ('Y', 'X')):
		if (product.spans[0].source.id != tip_origin or len(product.junctions) != 1
			or not math.isclose(product.junctions[0], exchanged)):
			raise ValueError('C46 crossover must exchange only the paired short-arm tips')

	palette = {
		('X', 'PAR'): '#C581C2', ('Y', 'PAR'): '#795394',
		('X', 'body'): '#CFE9BB', ('Y', 'body'): '#CFE9BB',
	}
	body = [
		_label(251, 38, 'Paired short-arm tips', 29),
		_label(657, 38, 'After crossover', 29),
	]
	for stage, models, positions in (
		('paired', (first, second), (166, 336)), ('product', products, (572, 742)),
	):
		for model, x, label in zip(models, positions, ('X', 'Y')):
			part = chromosomes.render_path(f'{stage}-{label}', model, f'M{x} 122 v{model.length}',
				width=43, palette=palette, texture=False, marker_size=(29, 54))
			body.extend((part.fragment, _label(x, 88, label, 28)))
	# The crossings meet X and Y inside their purple pseudoautosomal regions.
	body.extend((
		'<path d="M187 141 C227 141 273 175 315 175 M187 175 C227 175 273 141 315 141" '
		'fill="none" stroke="#724686" stroke-width="3.2"/>',
		f'<path d="M131 122 H120 v{par_length} H131" fill="none" stroke="#724686" stroke-width="2.6"/>',
		_label(72, 164, 'PAR', 24, color='#724686'),
		'<path d="M405 203 H496 l-15 -12 m15 12 l-15 12" fill="none" '
		f'stroke="{CONNECTOR}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',
		_label(454, 490, 'PAR = pseudoautosomal region', 26),
	))
	drawing.write_svg(output_dir / 'c46.drawn.svg', 900, 516,
		'X and Y exchange tips within a pseudoautosomal region',
		'X and Y pair at homologous tips on their short arms. Crossover within the '
		'pseudoautosomal region leaves each chromosome with a tip from the other. '
		'Chromosome lengths and region sizes are schematic.', ''.join(body))


#============================================
def build(output_dir: Path) -> None:
	"""Write the three dosage figures into the review asset directory."""
	_inactivation(output_dir)
	_calico(output_dir)
	_par_crossover(output_dir)
