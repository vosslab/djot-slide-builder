"""Rebuild review specimens C07-C10 from LECT06 division evidence and topology."""

import json
import math
import pathlib

import lxml.etree
import svgpathtools

import svg_tools._xml
import svg_tools.chromosome_surface
import svg_tools.chromosome_topology as topology
import svg_tools.chromosomes
import svg_tools.drawing
import svg_tools.parts


PROTOTYPE = pathlib.Path(__file__).resolve().parent
LECTURE = PROTOTYPE.parent / 'genetics/LECT06/djot'
MITOSIS_MODELS = LECTURE / 'chromosome_models'
REVIEW_SOURCES = PROTOTYPE / 'assets/chromosome_review_sources'
PANEL_SOURCES = MITOSIS_MODELS / 'mitosis_panel'
SVG = '{http://www.w3.org/2000/svg}'
LABEL_FONT = 'Atkinson Hyperlegible Next, sans-serif'


#============================================
def _write(root: lxml.etree._Element, path: pathlib.Path) -> None:
	"""Keep source vectors and raster links in the repository's SVG format."""
	for label in root.iter(SVG + 'text'):
		label.set('font-family', LABEL_FONT)
	payload = lxml.etree.tostring(svg_tools.drawing.svg_root(root), encoding='ascii')
	path.write_bytes(payload)


#============================================
def _intro(output_dir: pathlib.Path) -> None:
	"""Keep the source callouts and images, showing a single rod and its equal-length sisters."""
	model = topology.chromosome('intro-chromosome', length=80, centromere=20/62)
	sisters = topology.replicate(model)
	palette = {('intro-chromosome', 'body'): '#8A7BC4'}
	single = svg_tools.chromosomes.render('shared-single', model,
		points=((342, 63), (342, 143)), width=18, palette=palette, texture=False)
	pair = svg_tools.chromosomes.render('shared-sisters', sisters,
		points=((341.8, 223), (341.8, 303)), width=18, palette=palette, texture=False)
	sources = (
		('c07', 'chromosome_before_replication.image.svg', (single,)),
		('c08', 'chromosome_replication.image.svg', (single, pair)),
	)
	for sample, filename, parts in sources:
		root = svg_tools._xml.read(REVIEW_SOURCES / filename)
		bodies = lxml.etree.Element('g', id='shared-chromosome-bodies')
		for part in parts:
			bodies.append(svg_tools._xml.parse(part.fragment))
		canvas = root.find(SVG + 'g')
		canvas.insert(1, bodies)
		root.find(SVG + 'desc').text = (
			'LECT06B artwork, DNA and source callouts. The chromosomes show the same 80-unit '
			'length and 18-unit width before and after DNA replication.'
			if sample == 'c08' else
			'LECT06B artwork, DNA and source callouts. One chromosome with one chromatid, '
			'with the centromere and one arm indicated.'
		)
		_write(root, output_dir / f'{sample}.image.svg')


#============================================
def _centerline(path_d: str) -> svgpathtools.Path:
	"""Measure the same smooth path that the chromosome renderer paints."""
	path = svg_tools.chromosome_surface.authored_centerline(path_d, closed=False)
	return path


#============================================
def _material(name: str, path: svgpathtools.Path, position: complex) -> topology.Chromatid:
	"""Use the source path and localized centromere to establish the modeled material."""
	length = path.length()
	distance = svg_tools.chromosome_surface.nearest_distance(path, position)
	model = topology.chromosome(name, length=length, centromere=distance/length)
	return model


#============================================
def _body(name: str, model: topology.Chromatid, path_d: str, width: float, color: str,
	*, texture: bool) -> lxml.etree._Element:
	"""Paint material along a measured pose whose marker is composed at its source location."""
	source = model.spans[0].source.id
	part = svg_tools.chromosomes.render_path(name, model, path_d, width=width,
		palette={(source, 'body'): color}, texture=texture, draw_centromeres=False)
	return svg_tools._xml.parse(part.fragment)


#============================================
def _marker(name: str, path_data: tuple[str, ...], position: complex,
	width: float) -> lxml.etree._Element:
	"""Center one collar on the exact measured locus, using both sister tangents for a belt."""
	tangent = 0j
	for path_d in path_data:
		path = _centerline(path_d)
		distance = svg_tools.chromosome_surface.nearest_distance(path, position)
		parameter = path.ilength(distance)
		if abs(path.point(parameter) - position) > .001:
			raise ValueError(f'{name}: measured centromere is off the centerline')
		tangent += path.unit_tangent(parameter)
	across = width * (1.5 if len(path_data) == 2 else 1.3)
	part = svg_tools.chromosomes.centromere_part(name, thickness=width, across=across)
	placed = svg_tools.parts.transform(part, x=position.real, y=position.imag,
		rotation=math.degrees(math.atan2(tangent.imag, tangent.real)))
	return svg_tools._xml.parse(placed.fragment)


#============================================
def _mitosis_panel(output_dir: pathlib.Path) -> None:
	"""Keep the 48 source chromosomes in their measured poses and frozen image layers."""
	ledger_path = PANEL_SOURCES / 'source-ledger.json'
	ledger = json.loads(ledger_path.read_text())
	objects = ledger['objects']
	width, height = ledger['source_dimensions']
	sources = {}
	for record in objects:
		if record['stage'] == 'prophase':
			path_data = ' '.join(record['paths'][0])
			position = complex(*record['centromere'])
			identity = record['identity']
			model = _material(f'mitosis-{identity}', _centerline(path_data), position)
			sources[identity] = topology.replicate(model)

	layers = svg_tools._xml.read(REVIEW_SOURCES / 'mitosis_panel_layers.image.svg')
	background, leaders = (layer.attrib['href'] for layer in layers.findall(SVG + 'image'))
	body = [f'<image href="{background}" width="{width}" height="{height}"/>']
	for record in objects:
		name, stage, identity = (record[key] for key in ('id', 'stage', 'identity'))
		# The left copy of the large blue pair is colored light blue in the ledger.
		pair = sources['blue' if identity == 'lightblue' else identity]
		paths = tuple(' '.join(sections) for sections in record['paths'])
		state = 'replicated' if len(paths) == 2 else 'single-chromatid'
		group = lxml.etree.Element('g', {'id': name, 'data-state': state})
		models = ((pair.first, pair.second) if len(paths) == 2
			else (pair.second if stage.endswith('-left') else pair.first,))
		thickness = record['thickness']
		for index, (model, path_d, color) in enumerate(zip(models, paths, record['colors'], strict=True), 1):
			chromatid = _body(f'{name}-chromatid-{index}', model, path_d, thickness, ledger['colors'][color],
				texture=not stage.startswith('mini-'))
			group.append(chromatid)
		if record['centromere'] is not None:
			marker_name = f'{name}-belt' if len(paths) == 2 else name
			group.append(_marker(marker_name, paths, complex(*record['centromere']), thickness))
		body.append(lxml.etree.tostring(group, encoding='unicode'))
	body.append(f'<image href="{leaders}" width="{width}" height="{height}"/>')
	svg_tools.drawing.write_svg(output_dir / 'c09.image.svg', width, height, 'Stages of mitosis',
		'Chromosomes condense in prophase and align at metaphase. Sister chromatids separate in '
		'anaphase, and two daughter nuclei form in telophase. Enlarged and miniature views '
		'show these stages.', ''.join(body))


#============================================
def _anaphase_telophase(output_dir: pathlib.Path) -> None:
	"""Track both copies of each chromosome from anaphase into the daughter nuclei."""
	root = svg_tools._xml.read(MITOSIS_MODELS / 'mitosis/mitosis_anaphase_telophase.drawn.svg')
	poles = ('upper', 'lower')
	telophase = tuple(root.find(f"{SVG}g[@id='telophase-{pole}-uncondensed-chromatin']")
		for pole in poles)
	for index in range(1, 7):
		names = tuple(f'anaphase-{pole}-daughter-{index}' for pole in poles)
		groups = tuple(root.find(f"{SVG}g[@id='{name}']") for name in names)
		paths = tuple(group.find(SVG + 'path').get('d') for group in groups)
		markers = tuple(group.find(SVG + 'ellipse') for group in groups)
		positions = tuple(complex(float(marker.get('cx')), float(marker.get('cy')))
			for marker in markers)
		pair = topology.replicate(_material(f'anaphase-{index}', _centerline(paths[0]), positions[0]))
		for group, model, path_d, position, nucleus in zip(groups, (pair.first, pair.second),
			paths, positions, telophase, strict=True):
			name = group.get('id')
			width = float(group.find(SVG + 'path').get('stroke-width'))
			for child in list(group):
				group.remove(child)
			group.append(_body(f'{name}-shared', model, path_d, width, '#56529A', texture=True))
			group.append(_marker(name, (path_d,), position, width))
			pose = nucleus[index-1]
			# Draw decondensed chromatin with the source stroke and no condensed body features.
			chromatin = lxml.etree.Element(SVG + 'path', {
				'id': f'telophase-{model.id}',
				'data-source-id': model.spans[0].source.id,
				'd': pose.get('d'),
				'fill': 'none',
				'stroke': pose.get('stroke'),
				'stroke-width': pose.get('stroke-width'),
				'stroke-linecap': 'round',
				'stroke-linejoin': 'round',
			})
			nucleus.replace(pose, chromatin)
	svg_tools.drawing.remove_canvas_background(root)
	_write(root, output_dir / 'c10.drawn.svg')


#============================================
def build(output_dir: pathlib.Path) -> None:
	"""Write the four review specimens to a staging or delivery directory."""
	output_dir.mkdir(parents=True, exist_ok=True)
	_intro(output_dir)
	_mitosis_panel(output_dir)
	_anaphase_telophase(output_dir)
