"""Build the karyotype preparation and chromosome movement review diagrams."""

import pathlib

import lxml.etree
import svgpathtools

import svg_tools._xml
import svg_tools.chromosome_surface
import svg_tools.chromosome_topology as topology
import svg_tools.chromosomes as chromosomes
import svg_tools.drawing as drawing
import svg_tools.parts as parts


ROOT = pathlib.Path(__file__).resolve().parent
TEMPLATES = ROOT.parent / 'genetics/LECT10/djot/lect10b_chromosome_recipe/templates'
REVIEW_SOURCES = ROOT / 'assets/chromosome_review_sources'
SVG = f'{{{svg_tools._xml.SVG}}}'
FONT = 'Atkinson Hyperlegible Next'
BLUE = '#4c9ec7'


#============================================
def _write(root: lxml.etree._Element, path: pathlib.Path) -> None:
	for label in root.iter(f'{SVG}text'):
		label.set('font-family', FONT)
	drawing.remove_canvas_background(root)
	path.write_bytes(lxml.etree.tostring(drawing.svg_root(root), encoding='ascii'))


#============================================
def _distance_at_height(path: svgpathtools.Path, height: float) -> float:
	"""Project one horizontal source band boundary onto its downward spine."""
	if height == path.start.imag:
		return 0
	low, high = 0.0, 1.0
	for _ in range(40):
		middle = (low+high)/2
		if path.point(middle).imag < height:
			low = middle
		else:
			high = middle
	return path.length(0, (low+high)/2)


#============================================
def _preparation(path: pathlib.Path) -> None:
	"""Keep the image and source labels while regenerating the four diagram chromatids."""
	root = svg_tools._xml.read(REVIEW_SOURCES / 'karyotype_preparation.image.svg')
	overlay = root.find(f'.//{SVG}g[@id="chromosome-schematic-replacement"]')
	bands = ((190, '#d41489'), (219, '#f3ad59'), (235, '#258068'), (267, '#007096'),
		(281, '#f0ae5b'), (293, '#258068'), (301, '#258068'), (311, '#e4e77b'),
		(324, '#f3ae5c'), (349, '#26836b'), (357, '#a2cf68'), (374, '#258068'),
		(382, '#f3ad59'), (394, '#007096'), (400, '#d41489'))
	poses = (((55, 92, 52), (64, 99, 61)), ((169, 116, 137), (178, 123, 146)))
	for index, homolog in enumerate(poses, start=1):
		name = f'c30-homolog-{index}'
		paths = tuple(svg_tools.chromosome_surface.authored_centerline(
			f'M {top} 190 L {center} 301 L {bottom} 427', closed=False)
			for top, center, bottom in homolog)
		spine = paths[0]
		length = spine.length()
		regions = tuple((_distance_at_height(spine, height)/length, f'band-{number}')
			for number, (height, _) in enumerate(bands))
		centromere = regions[6][0]
		model = topology.chromosome(name, length=length, centromere=centromere, regions=regions)
		sisters = topology.replicate(model)
		palette = {(name, region_id): color for (_, region_id), (_, color) in zip(regions, bands, strict=True)}
		for number, (strand, authored) in enumerate(zip((sisters.first, sisters.second), paths, strict=True)):
			chromatid = chromosomes.render_path(f'{name}-sister-{number}', strand, authored.d(),
				width=8, palette=palette, texture=False)
			overlay.append(svg_tools._xml.parse(chromatid.fragment))
	for run in root.iter(f'{SVG}tspan'):
		if run.get('x'):
			run.set('x', run.get('x').split()[0])
	_write(root, path)


#============================================
def _centromere_positions(path: pathlib.Path) -> None:
	"""Compare the four centromere classes, including a truly terminal site."""
	root = svg_tools._xml.read(TEMPLATES / 'centromere_positions.drawn.svg')
	slots = {node.get('id'): node for node in root.iter(f'{SVG}g')}
	for name, center in (('acrocentric', 140), ('submetacentric', 210), ('metacentric', 247)):
		top, bottom = 84, 410
		length = bottom-top
		model = topology.chromosome(name, length=length, centromere=(center-top)/length)
		sisters = chromosomes.render(name, topology.replicate(model), points=[(0, top), (0, bottom)],
			width=28, palette={(name, 'body'): BLUE}, texture=False)
		slots[f'{name}-body-slot'].append(svg_tools._xml.parse(sisters.fragment))

	name = 'telocentric'
	width = 30
	model = topology.chromosome(name, length=298, centromere=0)
	sisters = topology.replicate(model)
	slot = slots['telocentric-body-slot']
	strands = tuple(chromosomes.render_path(f'{name}-sister-{index}', strand,
		f'M {side*10} 96 C {side*14} 190 {side*42} 330 {side*48} 394',
		width=width, palette={(name, 'body'): BLUE}, texture=False, draw_centromeres=False)
		for index, (side, strand) in enumerate(((-1, sisters.first), (1, sisters.second))))
	for strand in strands:
		slot.append(svg_tools._xml.parse(strand.fragment))
	(left, y), (right, _) = (strand.anchors['centromere'] for strand in strands)
	belt = chromosomes.centromere_part('telocentric-terminal', thickness=width, across=right-left+width*1.3)
	slot.append(svg_tools._xml.parse(parts.transform(belt, x=(left+right)/2, y=y, rotation=90).fragment))
	_write(root, path)


#============================================
def _movement(path: pathlib.Path, kind: str, daughter_path: str, *, length: float) -> None:
	"""Track the same sisters from metaphase attachment to anaphase movement."""
	root = svg_tools._xml.read(TEMPLATES / f'{kind}_movement.drawn.svg')
	authored = svg_tools.chromosome_surface.authored_centerline(daughter_path, closed=False)
	authored_length = authored.length()
	centromere = authored[0].length()/authored_length
	# Match display length without moving either spindle attachment.
	authored = authored.scaled(length/authored_length, origin=authored[0].end)
	top = 220 - centromere*length
	model = topology.chromosome(kind, length=length, centromere=centromere)
	sisters = topology.replicate(model)
	palette = {(kind, 'body'): BLUE}
	metaphase = chromosomes.render(f'{kind}-metaphase', sisters, points=[(300, top), (300, top+length)],
		width=26, palette=palette, texture=False)
	slot = root.find(f'.//{SVG}g[@id="replicated-chromosome"]')
	slot.append(svg_tools._xml.parse(metaphase.fragment))

	slot = root.find(f'.//{SVG}g[@id="daughter-chromosomes"]')
	for side, strand, pose in (
		('left', sisters.first, authored), ('right', sisters.second, authored.scaled(-1, 1).translated(2200)),
	):
		daughter = chromosomes.render_path(f'{kind}-{side}', strand, pose.d(),
			width=26, palette=palette, texture=False)
		slot.append(svg_tools._xml.parse(daughter.fragment))
	_write(root, path)


#============================================
def _forms(path: pathlib.Path) -> None:
	"""Show the rod and joined sisters as replication states of one chromosome."""
	black = '#111111'
	model = topology.chromosome('forms', length=112, centromere=.5)
	palette = {('forms', 'body'): black}
	pose = svg_tools.chromosome_surface.authored_centerline('M 20 31 Q 34 48 34 78 Q 32 103 20 128', closed=False)
	pose = pose.scaled(model.length/pose.length(), origin=34+79j)
	rod = chromosomes.render_path('c35-unreplicated', model, pose.d(),
		width=17, palette=palette, texture=False)
	sisters = chromosomes.render('c35-replicated', topology.replicate(model), points=[(135, 24), (135, 136)],
		width=17, palette=palette, texture=False)
	body = rod.fragment + sisters.fragment
	body += drawing.text(36, 157, 'Unreplicated', size=11, color=black)
	body += drawing.text(36, 171, 'chromosome', size=11, color=black)
	body += drawing.text(135, 157, 'Replicated', size=11, color=black)
	body += drawing.text(135, 171, 'chromosome', size=11, color=black)
	drawing.write_svg(path, 182, 179, 'Unreplicated and replicated chromosome',
		'One chromatid on the left and two sister chromatids joined at the centromere on the right.', body)


#============================================
def build(output_dir: pathlib.Path) -> None:
	"""Generate the five karyotype and movement review figures."""
	_preparation(output_dir / 'c30.image.svg')
	_centromere_positions(output_dir / 'c32.drawn.svg')
	_movement(output_dir / 'c33.drawn.svg', 'metacentric',
		'M 1030 121 Q 980 169 928 220 Q 980 271 1030 319', length=224)
	# Keep a short arm visible beyond the collar in both poses at the same material fraction.
	_movement(output_dir / 'c34.drawn.svg', 'acrocentric', 'M 1038 132 Q 957 163 928 220 L 948 247', length=138)
	_forms(output_dir / 'c35.drawn.svg')
