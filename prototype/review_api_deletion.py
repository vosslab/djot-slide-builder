"""Topology-backed LECT12D figures for the chromosome review deck."""

from pathlib import Path

from svg_tools import _xml
from svg_tools import chromosome_topology as topology
from svg_tools import drawing
from svg_tools.chromosomes import render_path


FONT = 'Atkinson Hyperlegible Next'
INK = '#344651'
MAP_BODY = '#54798D'
MISSING = '#CC0066'
REVIEW_SOURCES = Path(__file__).resolve().parent / 'assets/chromosome_review_sources'


#============================================
def _label(x: float, y: float, value: str, size: float, *,
	anchor: str = 'middle', color: str = INK) -> str:
	return drawing.text(x, y, value, size=size, color=color, anchor=anchor, font=FONT)


#============================================
def _c47(output_dir: Path) -> None:
	labels = 'ABCDEFGH'
	intact = topology.chromosome('deletion-source', length=512, centromere=5/8,
		genes={label: (index+.5)/8 for index, label in enumerate(labels)},
		regions=tuple((index/8, label) for index, label in enumerate(labels)))
	left, rest = topology.split(intact, 3/8)
	removed, right = topology.split(rest, 1/5)
	deleted = topology.join(left, right)
	topology.validate_conservation((intact,), (deleted, removed))
	palette = {(intact.id, label): '#B48CDE' if label == 'D' else '#D9C9EF'
		for label in labels}
	body = []
	for name, model, y in (('before', intact, 94), ('after', deleted, 235)):
		part = render_path(name, model, f'M218 {y} H{218+model.length:g}',
			width=36, palette=palette, gene_palette=palette, marker_size=(20, 45))
		body.extend((_label(48, y+10, name.capitalize(), 32, anchor='start'), part.fragment))
		if model is intact:
			for boundary in ('boundary_3', 'boundary_4'):
				x, _ = part.anchors[boundary]
				body.append(f'<path d="M{x:g} 37 V59" stroke="#BD2929" stroke-width="4"/>'
					f'<path d="M{x-7:g} 55 L{x:g} 68 L{x+7:g} 55 Z" fill="#BD2929"/>')
	drawing.write_svg(output_dir / 'c47.drawn.svg', 775, 300, 'Deletion',
		'The intact chromatid has A through H and a centromere between E and F. '
		'Red arrows mark the two cuts around D. After D is removed, C and E join at the '
		'white zigzag and the centromere remains between E and F. Gene spacing is schematic.',
		''.join(body))


#============================================
def _c49(output_dir: Path) -> None:
	body = ['<path d="M20 250 H965" stroke="#72508C" stroke-width="1.5"/>',
		_label(890, 244, 'centromere', 20, anchor='start', color='#72508C')]
	for name, x, start, stop in (('X', 105, 42, 250), ('Y', 280, 72, 475),
		('2', 455, 42, 460), ('3', 625, 30, 510), ('4', 805, 242, 250)):
		model = topology.chromosome(f'map-{name}', length=stop-start,
			centromere=(250-start)/(stop-start))
		part = render_path(model.id, model, f'M{x} {start} V{stop}', width=14,
			palette={(model.id, 'body'): MAP_BODY}, draw_centromeres=False)
		cx, cy = part.anchors['centromere']
		body.extend((part.fragment, f'<ellipse cx="{cx:g}" cy="{cy:g}" rx="11" ry="6" '
			'fill="none" stroke="#72508C" stroke-width="1.6"/>', _label(x, 570, name, 40)))

	# The original figure uses different physical and genetic scales on the same drawing.
	for x, y, value in ((122, 46, '0 Mbp'), (123, 242, '22.4 Mbp'),
		(297, 76, '0 Mbp'), (297, 486, '~40 Mbp'),
		(472, 46, '0 Mbp'), (472, 242, '23.0 Mbp'), (472, 277, '0 Mbp'),
		(472, 466, '21.1 Mbp'), (642, 31, '0 Mbp'), (642, 242, '24.5 Mbp'),
		(642, 277, '0 Mbp'), (642, 518, '27.9 Mbp'), (815, 227, '0 Mbp'),
		(815, 275, '1.4 Mbp')):
		body.append(_label(x, y, value, 20, anchor='start'))
	for x, y, value in ((38, 46, '0 cM'), (18, 242, '~75 cM'),
		(392, 46, '0 cM'), (373, 242, '~55 cM'), (358, 460, '~107 cM'),
		(562, 31, '0 cM'), (540, 274, '~47 cM'), (527, 513, '~110 cM')):
		body.append(_label(x, y, value, 20, anchor='start', color='#660000'))
	for x, y, label in ((474, 122, '2L'), (474, 333, '2R'), (644, 122, '3L'),
		(644, 333, '3R')):
		body.extend((_label(x, y, label, 28, anchor='start'),
			_label(x, y+34, 'arm', 28, anchor='start')))
	body.extend((_label(500, 614, 'Drosophila melanogaster chromosomes', 34),
		_label(500, 649,
			'Data from the National Center for Biotechnology Information (NCBI) and Carvalho (2002)',
			16)))
	drawing.write_svg(output_dir / 'c49.drawn.svg', 1000, 660,
		'Drosophila melanogaster chromosomes',
		'The source drawing aligns the centromeres of X, Y, 2, 3 and 4. Dark labels show '
		'physical positions in Mbp. Red labels show approximate genetic map positions in cM. '
		'Chromosome arm extents follow the source schematic.', ''.join(body))


#============================================
def _c50(output_dir: Path) -> None:
	photo = _xml.read(REVIEW_SOURCES / 'polytene_chromosome_photo.image.svg')
	href = photo.find(f'{{{_xml.SVG}}}image').attrib['href']
	body = [f'<image xlink:href="{href}" width="663" height="500"/>',
		'<rect x="183" y="42" width="151" height="133" fill="white"/>']
	for side in range(2):
		for chromosome, x, tip in (('2', 207+side*18, 231+side*18),
			('3', 293+side*18, 269+side*18)):
			name = f'inset-{chromosome}-{side}'
			model = topology.chromosome(name, length=1)
			body.append(render_path(name, model,
				f'M{x} 59 C{x} 70 {tip} 78 {tip} 88 C{tip} 98 {x} 109 {x} 122',
				width=8, palette={(name, 'body'): MAP_BODY}).fragment)
		name = f'inset-4-{side}'
		model = topology.chromosome(name, length=1)
		body.append(render_path(name, model, f'M{253+side*10} 88 V89',
			width=5, palette={(name, 'body'): MAP_BODY}).fragment)
	for name, color, path in (('inset-X', '#086898', 'M246 116 V146'),
		('inset-Y', '#417521', 'M262 146 C262 132 266 120 275 124')):
		model = topology.chromosome(name, length=1)
		body.append(render_path(name, model, path, width=8,
			palette={(name, 'body'): color}).fragment)
	for x, y, value in ((188, 57, 'R'), (188, 133, 'L'), (321, 57, 'R'), (321, 133, 'L'),
		(209, 96, '2'), (295, 96, '3'), (253, 77, '4'), (242, 169, 'X'), (258, 169, 'Y')):
		body.append(_label(x, y, value, 12, anchor='start'))
	drawing.write_svg(output_dir / 'c50.image.svg', 663, 500, 'Drosophila polytene chromosomes',
		'The original polytene micrograph, labels, arrows and caption surround a redrawn '
		'schematic inset of Drosophila chromosomes.', ''.join(body))


#============================================
def _map_reference(name: str, left: float, right: float,
	region_starts: list[tuple[float, str]]) -> topology.Chromatid:
	stops = [x for x, _ in region_starts[1:]] + [right]
	regions = tuple(topology.Region(label, start-left, stop-left)
		for (start, label), stop in zip(region_starts, stops))
	source = topology.SourceMaterial(name, right-left, regions, (), ())
	return topology.Chromatid(name, (topology.Span(source, name, 0, source.length),))


#============================================
def _evidence_row(reference: topology.Chromatid, name: str, y: float, left: float,
	interval: tuple[float, float] | None = None, *,
	expected_deleted_regions: tuple[str, ...] | None = None) -> str:
	source = reference.spans[0].source
	palette = {(source.id, region.id): '#B8C0C8' for region in source.regions}
	retained = (reference,)
	marker = ''
	if interval is not None:
		start, stop = interval
		left_arm, rest = topology.split(reference, (start-left)/reference.length)
		missing, right_arm = topology.split(rest, (stop-start)/rest.length)
		retained = (left_arm, right_arm)
		topology.validate_conservation((reference,), (left_arm, missing, right_arm))
		if expected_deleted_regions is not None:
			deleted_regions = tuple(region.region_id for region in topology.project_regions(missing))
			if deleted_regions != expected_deleted_regions:
				raise ValueError(f'{name} deletes {deleted_regions}, expected {expected_deleted_regions}')
		marker = (f'<rect data-layer="deleted-interval" x="{start:g}" y="{y-5.5:g}" '
			f'width="{stop-start:g}" height="11" fill="{MISSING}"/>')
	parts = []
	for index, piece in enumerate(retained):
		span, = piece.spans
		# Evidence rows keep each fragment at its reference-map position.
		parts.append(render_path(f'{name}-retained-{index}', piece,
			f'M{left+span.start:g} {y:g} H{left+span.stop:g}', width=25,
			palette=palette).fragment)
	return f'<g id="{name}"><g data-layer="retained-dna">{"".join(parts)}</g>{marker}</g>'


#============================================
def _c51(output_dir: Path) -> None:
	body = []
	region_starts = [(125, 'body')]
	for x, band, gene, role in ((230, '3A3', 'zeste', 'eye-color gene'),
		(500, '3A9', 'zw2', 'lethal gene'), (800, '3C2', 'white', 'eye-color gene')):
		start, stop = x-16, x+16
		region_starts.extend(((start, band), (stop, 'body')))
		body.append(f'<rect x="{start}" y="45" width="{stop-start}" height="300" fill="#E2E7EC"/>')
		body.extend(_label(x, y, label, size) for y, label, size in
			((385, band, 27), (430, gene, 28), (470, role, 23)))
	reference = _map_reference('cytological-reference', 125, 885, region_starts)
	# The schematic includes partial band overlaps, so keep the measured endpoints.
	intervals = ((150, 784), (214, 816), (246, 816), (246, 835), (484, 540), (511, 650))
	for index, (label, interval) in enumerate(zip(('I', 'II', 'III', 'IV', 'V', 'VI'), intervals)):
		y = 80+index*45
		body.extend((_label(70, y+8, label, 27, anchor='start'),
			_evidence_row(reference, f'deletion-{label}', y, 125, interval)))
	body.append(_label(465, 520, 'Gray rods = retained DNA; magenta = deleted interval', 25))
	drawing.write_svg(output_dir / 'c51.drawn.svg', 930, 540, 'Cytological deletion intervals',
		'Six deletion intervals aligned to cytological bands 3A3 (zeste), 3A9 (zw2), and '
		'3C2 (white). Band spacing and each deletion endpoint follow the source. '
		'Deletion V and deletion VI have distinct endpoints and widths.', ''.join(body))


#============================================
def _c52(output_dir: Path) -> None:
	body = []
	positions = (240, 345, 450, 555, 660, 765)
	labels = tuple(str(index) for index in range(1, len(positions)+1))
	half_slot = (positions[1]-positions[0])/2
	slot_edges = tuple(x-half_slot for x in positions) + (positions[-1]+half_slot,)
	for x, label in zip(positions, labels):
		body.extend((_label(x, 42, label, 40),
			f'<path d="M{x} 55 V455" stroke="#DFE6EC" stroke-width="1.5"/>'))
	region_starts = [(155, 'body'), *zip(slot_edges[:-1], labels), (slot_edges[-1], 'body')]
	reference = _map_reference('aligned-reference', 155, 850, region_starts)
	body.extend((_label(135, 98, 'Reference', 23, anchor='end'),
		_evidence_row(reference, 'reference', 88, 155)))
	for index, (first, last) in enumerate(((1, 3), (2, 3), (2, 4), (3, 5), (4, 6)), 1):
		y = 185+(index-1)*62
		interval = (slot_edges[first-1], slot_edges[last])
		body.extend((_label(135, y+9, f'Del {index}', 32, anchor='end'),
			_evidence_row(reference, f'deletion-{index}', y, 155, interval,
				expected_deleted_regions=labels[first-1:last])))
	body.append(_label(435, 505, 'Gray rods = retained DNA; magenta = deleted interval', 25))
	drawing.write_svg(output_dir / 'c52.drawn.svg', 870, 520, 'Aligned deletion evidence',
		'Five deletion intervals aligned to six equal gene slots. Del 1 removes genes 1\u20133, '
		'Del 2 removes 2\u20133, Del 3 removes 2\u20134, Del 4 removes 3\u20135, and Del 5 removes 4\u20136. '
		'Gray shows the retained DNA and magenta marks the missing intervals.', ''.join(body))


#============================================
def build(output_dir: Path) -> None:
	"""Write the deletion overview, quantitative map, inset and evidence tracks."""
	output_dir.mkdir(parents=True, exist_ok=True)
	_c47(output_dir)
	_c49(output_dir)
	_c50(output_dir)
	_c51(output_dir)
	_c52(output_dir)
