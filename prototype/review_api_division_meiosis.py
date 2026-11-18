"""Redraw the authored meiotic chromatids over the original review compositions."""

import itertools
import json
from pathlib import Path

import lxml.etree
import svgpathtools

from genetics.LECT06.djot.chromosome_models.mixed.recombination import recombination_recipes
import svg_tools._xml as xml
import svg_tools.chromosome_surface as surface
import svg_tools.chromosome_topology as topology
import svg_tools.chromosomes as chromosomes
import svg_tools.drawing as drawing
import svg_tools.parts as parts


LECTURE = Path(__file__).resolve().parents[1] / 'genetics/LECT06/djot'
MODELS = LECTURE / 'chromosome_models'
REVIEW_SOURCES = Path(__file__).resolve().parent / 'assets/chromosome_review_sources'
SVG = f'{{{xml.SVG}}}'
FONT = 'Atkinson Hyperlegible Next, sans-serif'
THREAD_COLORS = {'blue': '#087faf', 'green': '#50a374', 'orange': '#df8746', 'purple': '#ab597b'}
PANEL_COLORS = {'blue': '#008EBC', 'green': '#5FA763', 'orange': '#E88B3E', 'purple': '#B4546A'}
RECOMBINATION_COLORS = {'blue': recombination_recipes.BLUE, 'red': recombination_recipes.RED}
MINIATURE_SOURCE_NAME = 'mini-telophase-II-upper-right-blue-recombinant-source-thumbnail'
MINIATURE_CORRECTED_NAME = 'mini-telophase-II-upper-right-green-recombinant'


#============================================
def _palette(colors: dict[str, str]) -> dict[tuple[str, str], str]:
	return {(source, 'body'): color for source, color in colors.items()}


#============================================
def _crossover(parent: topology.Chromatid, donor: topology.Chromatid,
	cuts: tuple[float, ...], donor_first: bool) -> tuple[topology.Chromatid, topology.Chromatid]:
	"""Exchange alternating homolog intervals at the source crossover breakpoints."""
	def fragments(chromatid: topology.Chromatid) -> list[topology.Chromatid]:
		result = []
		start = 0.0
		for cut in cuts:
			left, chromatid = topology.split(chromatid, (cut-start)/(1-start))
			result.append(left)
			start = cut
		return [*result, chromatid]

	left, right = fragments(parent), fragments(donor)
	from_parent = tuple(second if bool(index % 2) != donor_first else first
		for index, (first, second) in enumerate(zip(left, right)))
	from_donor = tuple(first if bool(index % 2) != donor_first else second
		for index, (first, second) in enumerate(zip(left, right)))
	products = topology.join(*from_parent), topology.join(*from_donor)
	topology.validate_conservation((parent, donor), products)
	return products


#============================================
def _belt(name: str, first: parts.SvgPart, second: parts.SvgPart, width: float,
	*, joined_neck: bool = False) -> lxml.etree._Element:
	first_center, second_center = first.anchors['centromere'], second.anchors['centromere']
	if joined_neck:
		# These vertical anaphase I sisters meet at one neck.
		first_center = second_center = tuple((a+b)/2 for a, b in zip(first_center, second_center))
	belt = chromosomes._sister_belt_part(name, first_center, second_center, width)
	return xml.parse(belt.fragment)


#============================================
def _write(root: lxml.etree._Element, output: Path) -> None:
	for label in root.iter(SVG+'text'):
		label.set('font-family', FONT)
	lxml.etree.ElementTree(drawing.svg_root(root)).write(output, encoding='utf-8', xml_declaration=True)


#============================================
def _early_prophase(output: Path) -> None:
	root = xml.read(MODELS/'early_meiosis/prophase_leptotene_zygotene.drawn.svg')
	colors = {color: source for source, color in THREAD_COLORS.items()}
	threads = [node for node in root.iter(SVG+'path') if node.get('stroke') in colors]
	if len(threads) != 16:
		raise ValueError('Early prophase source must contain 16 traced chromatin threads')
	for index, thread in enumerate(threads):
		# Each trace shows a chromosome before individual sisters resolve.
		model = topology.chromosome(colors[thread.get('stroke')], length=100)
		region, = topology.project_regions(model)
		thread.set('id', f'early-thread-{index}')
		thread.set('data-source-id', region.source_id)
		thread.set('data-copy-id', model.spans[0].copy_id)
		thread.set('stroke', THREAD_COLORS[region.source_id])
	drawing.remove_canvas_background(root)
	_write(root, output)


#============================================
def _late_prophase(output: Path) -> None:
	root = xml.read(MODELS/'early_meiosis/prophase_diplotene_diakinesis.drawn.svg')
	bivalents = [node for node in root.iter(SVG+'g') if node.get('data-bivalent')]
	if len(bivalents) != 8:
		raise ValueError('Late prophase source must contain eight enlarged and miniature bivalents')
	for index, bivalent in enumerate(bivalents):
		is_long = bivalent.get('data-bivalent') == 'long'
		sources = ('green', 'blue') if is_long else ('orange', 'purple')
		parent = topology.chromosome(sources[0], length=160 if is_long else 100,
			centromere=.5 if is_long else .21)
		homologs = (parent, topology.homolog(parent, sources[1]))
		bodies = bivalent.findall(SVG+'path')
		centromeres = bivalent.findall(SVG+'ellipse')
		for position, (model, centromere) in enumerate(zip(homologs, centromeres, strict=True)):
			name = f'late-bivalent-{index}-{model.id}'
			outer, inner = bodies[position*2:position*2+2]
			width = float(outer.get('stroke-width'))
			pair = topology.replicate(model)
			sisters = []
			for chromatid, path_node in ((pair.first, outer), (pair.second, inner)):
				part = chromosomes.render_path(f'{name}-{len(sisters)+1}', chromatid, path_node.get('d'),
					width=width, palette=_palette(THREAD_COLORS), texture=False, draw_centromeres=False)
				sisters.append(part)
				bivalent.replace(path_node, xml.parse(part.fragment))
			bivalent.replace(centromere, _belt(f'{name}-belt', *sisters, width))
	drawing.remove_canvas_background(root)
	_write(root, output)


#============================================
def _recombination(output: Path) -> None:
	root = xml.read(REVIEW_SOURCES/'recombinant_chromosomes.image.svg')
	# The slide text replaces the callout attached to these leaders.
	for leader_id in ('source-shape-4', 'source-shape-5'):
		leader = root.find(f'.//{SVG}path[@id="{leader_id}"]')
		leader.getparent().remove(leader)
	bodies = root.find(f'.//{SVG}g[@id="shared-source-chromosome-bodies"]')
	blue = topology.chromosome('blue', length=100, centromere=.5)
	red = topology.homolog(blue, 'red')
	blue_pair, red_pair = topology.replicate(blue), topology.replicate(red)
	blue_cross, red_cross = _crossover(blue_pair.second, red_pair.first, (.2, .8), True)
	models = (
		red_pair.first, red_pair.second, blue_pair.first, blue_pair.second,
		blue_pair.first, red_pair.second, blue_pair.second, red_pair.first,
		blue_pair.first, blue_cross, red_cross, red_pair.second,
		blue_pair.first, blue_cross, red_cross, red_pair.second,
		blue_pair.first, blue_cross, red_cross, red_pair.second,
	)
	poses = recombination_recipes.source_bodies()
	paired = ((0, 1), (2, 3), (4, 6), (5, 7), (8, 9), (10, 11))
	belts = dict((second, first) for first, second in paired)
	parts_by_index = []
	for index, ((name, colors, path, width), model) in enumerate(zip(poses, models, strict=True)):
		projected = tuple(RECOMBINATION_COLORS[region.source_id] for region in topology.project_regions(model))
		if (projected*3 if len(projected) == 1 else projected) != colors:
			raise ValueError(f'{name}: projected ancestry does not match the recombination stage map')
		part = chromosomes.render_path(name, model, path, width=width,
			palette=_palette(RECOMBINATION_COLORS), texture=False, draw_centromeres=index >= 12)
		parts_by_index.append(part)
		bodies.append(xml.parse(part.fragment))
		if index in belts:
			first = parts_by_index[belts[index]]
			bodies.append(_belt(f'{name}-belt', first, part, width, joined_neck=index in (9, 11)))
	# Reverse the local stacking at the upper chiasma to retain the two source contacts.
	defs = lxml.etree.SubElement(bodies, SVG+'defs')
	clip = lxml.etree.SubElement(defs, SVG+'clipPath', id='upper-synapsis-contact')
	lxml.etree.SubElement(clip, SVG+'circle', cx='387.7', cy='144.2', r='4.5')
	bridge = lxml.etree.SubElement(bodies, SVG+'g', {'clip-path': 'url(#upper-synapsis-contact)'})
	lxml.etree.SubElement(bridge, SVG+'use', {f'{{{xml.XLINK}}}href': '#synapsis-blue-inner'})
	root.find(SVG+'title').set('id', 'title')
	desc = root.find(SVG+'desc')
	desc.set('id', 'desc')
	desc.text = 'Recombinant chromosomes through meiosis. Numbered marks refer to the slide text.'
	root.set('role', 'img')
	root.set('aria-labelledby', 'title desc')
	_write(root, output)


#============================================
def _panel_lineages() -> dict[str, topology.SisterPair]:
	"""Retain each physical chromatid and exchange breakpoint through both divisions."""
	lineages = {}
	# Representative arc fractions from the traced stage maps place the same loci in each pose.
	for first, second, length, centromere, cuts in (
		('green', 'blue', 160, .5, (.245, .765)),
		('orange', 'purple', 100, .34, (.68,)),
	):
		parent = topology.chromosome(first, length=length, centromere=centromere)
		pair = topology.replicate(parent)
		homolog = topology.replicate(topology.homolog(parent, second))
		products = _crossover(pair.second, homolog.second, cuts, len(cuts) == 2)
		lineages[first] = topology.SisterPair(pair.first, products[0])
		lineages[second] = topology.SisterPair(homolog.first, products[1])
	return lineages


#============================================
def _panel_material(record: dict, path: svgpathtools.Path,
	lineages: dict[str, topology.SisterPair], name: str, full_size: dict[str, dict]) -> topology.Chromatid:
	"""Choose the traced chromosome's lineage and reading direction."""
	source = next(source for source in PANEL_COLORS if source in name.split('-'))
	ancestry = [color for color, _ in itertools.groupby(color for color, _ in record['segments'])]
	if record['name'] == MINIATURE_SOURCE_NAME:
		# The enlargement and earlier stages trace this daughter to the green centromere.
		ancestry = [PANEL_COLORS['blue'], PANEL_COLORS['green'], PANEL_COLORS['blue']]
	pair = lineages[source]
	model = pair.first if len(ancestry) == 1 else pair.second
	if source in ('orange', 'purple'):
		# Some short poses trace from the opposite end. Locate direction in the enlargement
		# when the original miniature omits the site.
		orientation_record = record
		if record['center'] is None:
			orientation_record = full_size[name.removeprefix('mini-')]
			path = surface.authored_centerline(orientation_record['path_d'], closed=False)
		locus = complex(*orientation_record['points'][orientation_record['center']])
		if surface.nearest_distance(path, locus) > path.length()/2:
			model = topology.reverse(model)
	if [PANEL_COLORS[region.source_id] for region in topology.project_regions(model)] != ancestry:
		raise ValueError(f'{name}: projected ancestry does not match the meiosis stage map')
	if tuple(site.source_id for site in topology.project_centromeres(model)) != (source,):
		raise ValueError(f'{name}: projected centromere does not belong to {source}')
	return model


#============================================
def _complete_panel(output: Path) -> None:
	root = xml.read(REVIEW_SOURCES/'meiosis_panel.image.svg')
	bodies = root.find(f'{SVG}g[@id="chromosome-bodies"]')
	records = json.loads((MODELS/'meiosis_panel/chromatids.json').read_text())
	if len(records) != 144 or sum(record['center'] is not None for record in records) != 136:
		raise ValueError('Meiosis stage map must contain 144 chromatids and 136 localized centromeres')
	full_size = {record['name']: record for record in records if not record['name'].startswith('mini-')}
	lineages = _panel_lineages()
	paired = {}
	for record in records:
		name = MINIATURE_CORRECTED_NAME if record['name'] == MINIATURE_SOURCE_NAME else record['name']
		path = surface.authored_centerline(record['path_d'], closed=False)
		model = _panel_material(record, path, lineages, name, full_size)
		width = record['width']
		is_sister = name.endswith(('-1', '-2'))
		part = chromosomes.render_path(name, model, path.d(), width=width,
			palette=_palette(PANEL_COLORS), texture=False,
			draw_centromeres=not is_sister and record['center'] is not None)
		bodies.append(xml.parse(part.fragment))
		if is_sister:
			key = name[:-2]
			if key in paired:
				bodies.append(_belt(f'{key}-belt', paired.pop(key), part, width))
			else:
				paired[key] = part
	if paired:
		raise ValueError(f'Missing sister pose for {", ".join(paired)}')
	_write(root, output)


#============================================
def build(output_dir: Path) -> None:
	"""Generate C11-C14; C21 uses the same artwork as C13."""
	output_dir.mkdir(parents=True, exist_ok=True)
	_early_prophase(output_dir/'c11.drawn.svg')
	_late_prophase(output_dir/'c12.drawn.svg')
	_recombination(output_dir/'c13.image.svg')
	_complete_panel(output_dir/'c14.image.svg')
