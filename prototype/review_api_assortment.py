"""Rebuild three LECT06 review figures from their source poses and chromosome models."""

import collections
import json
import math
import pathlib

import lxml.etree

from svg_tools import _xml, chromosome_topology as topology, chromosomes, drawing, parts


PROTOTYPE = pathlib.Path(__file__).resolve().parent
SOURCE = PROTOTYPE.parent / 'genetics/LECT06/djot/chromosome_models'
REVIEW_SOURCES = PROTOTYPE / 'assets/chromosome_review_sources'
FONT = 'Atkinson Hyperlegible Next, sans-serif'


#============================================
def _scene(stem: str) -> tuple[lxml.etree._Element, dict[str, lxml.etree._Element], list[dict]]:
	"""Read the source poses and the template's empty chromosome slots."""
	path = SOURCE / stem
	placements = json.loads(path.with_suffix('.json').read_text(encoding='utf-8'))['placements']
	# ASVS 1.5.1: Use the shared XML parser with external entities disabled.
	root = _xml.read(REVIEW_SOURCES / f'{path.name}.drawn.svg')
	groups = {node.get('id'): node for node in root.iter() if node.get('id')}
	drawing.remove_canvas_background(root)
	for label in root.iter(f'{{{_xml.SVG}}}text'):
		label.set('font-family', FONT)
	return root, groups, placements


#============================================
def _place(group: lxml.etree._Element, bodies: list[dict],
	models: list[topology.Chromatid], palette: dict, *, centromere: bool) -> None:
	"""Place independent poses and add each common collar in the foreground."""
	name = group.get('id')
	if len(bodies) != len(models) or len(models) not in (1, 2, 4):
		raise ValueError(f'{name}: each chromatid needs one authored pose')
	paired = len(models) > 1
	rendered = []
	for index, (body, model) in enumerate(zip(bodies, models)):
		part = chromosomes.render_path(f'{name}-chromatid-{index}', model, body['path'],
			width=body['width'], palette=palette, texture=False,
			draw_centromeres=centromere and not paired)
		group.append(_xml.parse(part.fragment))
		rendered.append(part)
	if paired and centromere:
		for index in range(0, len(models), 2):
			left, right = rendered[index:index+2]
			first_site, = topology.project_centromeres(models[index])
			second_site, = topology.project_centromeres(models[index+1])
			if first_site.source_id != second_site.source_id or first_site.id != second_site.id:
				raise ValueError(f'{name}: sisters must share the same source centromere')
			x1, y1 = left.anchors['centromere']
			x2, y2 = right.anchors['centromere']
			width = bodies[index]['width']
			belt = chromosomes.centromere_part(f'{name}-belt-{index//2}', thickness=width,
				across=math.hypot(x2-x1, y2-y1)+width*1.3)
			angle = math.degrees(math.atan2(y2-y1, x2-x1))-90
			belt = parts.transform(belt, x=(x1+x2)/2, y=(y1+y2)/2, rotation=angle)
			group.append(_xml.parse(belt.fragment))


#============================================
def _assortment() -> lxml.etree._Element:
	root, groups, placements = _scene('assortment/assortment_full')
	first_a = topology.chromosome('A', length=56, centromere=.5)
	first_b = topology.chromosome('B', length=36, centromere=.5)
	models = {'A': first_a, 'a': topology.homolog(first_a, 'a'),
		'B': first_b, 'b': topology.homolog(first_b, 'b')}
	sisters = {allele: topology.replicate(model) for allele, model in models.items()}
	palette = {}
	gametes = collections.defaultdict(list)
	for placement in placements:
		group = groups[placement['group']]
		allele = group.get('data-homolog')
		paint, = {body['color'] for body in placement['parts']}
		key = (models[allele].id, 'body')
		if palette.setdefault(key, paint) != paint:
			raise ValueError(f'{allele}: conflicting source colors')
		count = int(group.get('data-chromatids'))
		pair = sisters[allele]
		if count == 2:
			view = [pair.first, pair.second]
		else:
			cell, sister, _ = placement['group'].rsplit('-', 2)
			gametes[f'{cell}-{sister}'].append(allele)
			view = [pair.first if sister == '0' else pair.second]
		_place(group, placement['parts'], view, palette, centromere=placement['centromere'])
	if collections.Counter(''.join(alleles) for alleles in gametes.values()) != {
		'AB': 2, 'ab': 2, 'Ab': 2, 'aB': 2,
	}:
		raise ValueError('Independent assortment must show two cells per gamete genotype')
	return root


#============================================
def _division() -> lxml.etree._Element:
	root, groups, placements = _scene('assortment/mitosis_meiosis_comparison')
	parents = {}
	palette = {}
	for placement in placements:
		name = placement['group']
		if name.startswith('parent-'):
			_, number, homolog = name.split('-')
			segments = placement['parts'][0]['segments']
			color, arm_length = segments[0]
			length = 2*arm_length
			source_id = f'ch{int(number)+1}-{homolog}'
			if homolog == 'R':
				model = topology.chromosome(source_id, length=length, centromere=.5)
			else:
				model = topology.homolog(parents[length, 'R'], source_id)
			parents[length, homolog] = model
			palette[source_id, 'body'] = color
	sisters = {key: topology.replicate(model) for key, model in parents.items()}
	colors = {color: source.rsplit('-', 1)[1] for (source, _), color in palette.items()}
	recombinants = {}
	for placement in placements:
		name = placement['group']
		if name.startswith('meiosis-metaphase-i-') and name.endswith('--1'):
			# The separated metaphase I homologs set the crossover for every view.
			segments, = (pose['segments'] for pose in placement['parts'] if len(pose['segments']) == 3)
			length = round(sum(amount for _, amount in segments))
			cut = sum(amount for _, amount in segments[:2])/length
			red, blue = (sisters[length, homolog].second for homolog in ('R', 'B'))
			red_head, red_tail = topology.split(red, cut)
			blue_head, blue_tail = topology.split(blue, cut)
			red_product = topology.join(red_head, blue_tail)
			blue_product = topology.join(blue_head, red_tail)
			topology.validate_conservation((red, blue), (red_product, blue_product))
			recombinants[length, 'R'] = red_product
			recombinants[length, 'B'] = blue_product
	for placement in placements:
		name = placement['group']
		poses = placement['parts']
		models = []
		for index, pose in enumerate(poses):
			segments = pose['segments']
			length = round(sum(amount for _, amount in segments))
			homolog = colors[segments[0][0]]
			pair = sisters[length, homolog]
			if name.startswith('parent-'):
				model = parents[length, homolog]
			elif name.startswith('mitosis-'):
				second = index == 1 or name.startswith('mitosis-daughter-1-')
				model = pair.second if second else pair.first
			elif len(segments) == 3:
				model = recombinants[length, homolog]
			else:
				model = pair.first
			models.append(model)
		_place(groups[name], poses, models, palette, centromere=placement['centromere'])
	return root


#============================================
def _genotypes() -> dict[str, tuple[str, str]]:
	"""Generate the represented offspring of the two reciprocal parental crosses."""
	genotypes = {}
	for cross, maternal, paternal in (('A', 'w+', 'w'), ('B', 'w', 'w+')):
		# F1 females carry both X alleles. The F1 male carries his mother's X.
		# F2 displays the daughters and sons for each egg allele, w+ then w.
		stages = {
			'P': [(maternal, maternal), (paternal, 'Y')],
			'F1': [(maternal, paternal), (maternal, 'Y')],
			'F2': [('w+', maternal), ('w+', 'Y'), (maternal, 'w'), ('w', 'Y')],
		}
		for stage, rows in stages.items():
			for index, genotype in enumerate(rows, 1):
				genotypes[f'{cross}-{stage}-{index}'] = genotype
	return genotypes


#============================================
def _reciprocal_crosses() -> lxml.etree._Element:
	root, groups, placements = _scene('xlinked/reciprocal_eye_crosses')
	genotypes = _genotypes()
	source_models = {pose['group']: pose['model']['segments'] for pose in placements}
	x_material = source_models['A-P-1-chromosome-1']
	y_material = source_models['A-P-2-chromosome-2']
	x_length = sum(amount for _, amount in x_material)
	y_length = sum(amount for _, amount in y_material)
	x_model = topology.chromosome('X-white', length=x_length,
		centromere=x_material[0][1]/x_length, genes={'w': 117.5/x_length})
	y_model = topology.chromosome('Y', length=y_length, centromere=y_material[0][1]/y_length)
	models = {'w': x_model, 'w+': topology.homolog(x_model, 'X-red', alleles={'w': 'w+'}),
		'Y': y_model}
	for placement in placements:
		name = placement['group']
		fly, _, slot = name.rsplit('-', 2)
		allele = genotypes[fly][int(slot)-1]
		source = models[allele]
		model = topology.copy(source, f'{source.id}.{name}')
		group = groups[name]
		paint = placement['model']['segments'][0][0]
		part = chromosomes.render_path(f'{name}-chromatid', model, placement['path'],
			width=placement['thickness'], palette={(source.id, 'body'): paint},
			allow_external_genes=True)
		body = _xml.parse(part.fragment)
		group.insert(0, body)
		group.set('data-chromosome', 'Y' if allele == 'Y' else 'X')
		if allele == 'Y':
			continue
		patch, label = list(group)[1:]
		if ''.join(label.itertext()) != allele:
			raise ValueError(f'{name}: source allele diverges from the reciprocal cross')
		# The source locus cards keep their full drawing width for slide legibility.
		gene, = body.xpath('./*[@data-layer="gene-locus"]')
		body.remove(gene)
		x, y = part.anchors['gene_w']
		patch.set('x', str(x-float(patch.get('width'))/2))
		patch.set('y', str(y-float(patch.get('height'))/2))
		label.set('x', str(x))
		label.set('y', str(y+6))
		gene[:] = [patch, label]
		group.append(gene)
	return root


#============================================
def build(output_dir: pathlib.Path) -> None:
	"""Write the reviewed layouts under their prototype sample IDs."""
	output_dir.mkdir(parents=True, exist_ok=True)
	for sample, draw in (('c15', _assortment), ('c17', _division), ('c19', _reciprocal_crosses)):
		root = drawing.svg_root(draw())
		# ASVS 1.2.1: Serialize labels and geometry through the SVG XML writer.
		(output_dir / f'{sample}.drawn.svg').write_bytes(
			lxml.etree.tostring(root, encoding='ascii') + b'\n')
