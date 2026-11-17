"""Schematic chromosomes, joined sisters and bounded segment rearrangements."""

import re
import math
import pathlib
import dataclasses
import xml.etree.ElementTree

import svgpathtools

import svg_tools.parts
import svg_tools.chromosome_surface


#============================================
def _positive(value: float) -> bool:
	valid = (isinstance(value, (int, float)) and not isinstance(value, bool)
		and math.isfinite(value) and value > 0)
	return valid


#============================================
def _label_color(color: str) -> str:
	"""Choose readable live text while retaining the established ink on light fills."""
	channels = [int(color[pos:pos+2], 16) / 255 for pos in (1, 3, 5)]
	linear = [v / 12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in channels]
	luminance = sum(v * weight for v, weight in zip(linear, (.2126, .7152, .0722)))
	if luminance >= .29:
		return "#172B3A"
	if luminance > .179:
		return "#000000"
	return "#FFFFFF"


#============================================
@dataclasses.dataclass(frozen=True)
class Segment:
	"""An immutable colored region; biological bands are explicit regions."""

	label: str
	color: str
	length: float = 64

	def __post_init__(self) -> None:
		if (not isinstance(self.label, str) or not isinstance(self.color, str)
			or not re.fullmatch(r"#[0-9A-Fa-f]{6}", self.color)):
			raise ValueError("Regions need string labels and six-digit hex fills")
		if any((ord(char) < 32 and char not in "\t\n\r")
			or 0xD800 <= ord(char) <= 0xDFFF or ord(char) in (0xFFFE, 0xFFFF)
			for char in self.label):
			raise ValueError("Labels must contain XML-safe characters")
		if not _positive(self.length):
			raise ValueError("Segment length must be finite and positive")



#============================================
@dataclasses.dataclass(frozen=True)
class Centromere:
	"""A chromosome attachment site after a region; terminal sites are allowed."""

	after: int
	active: bool = True
	label: str | None = None


#============================================
@dataclasses.dataclass(frozen=True)
class Chromosome:
	"""Ordered regions and their structurally independent centromere sites."""

	segments: tuple[Segment, ...]
	centromeres: tuple[Centromere, ...] = ()

	def __post_init__(self) -> None:
		object.__setattr__(self, "segments", tuple(self.segments))
		if not self.segments or not all(isinstance(segment, Segment) for segment in self.segments):
			raise ValueError("Supply nonempty Segment values")
		if not math.isfinite(sum(segment.length for segment in self.segments)):
			raise ValueError("Total segment length must be finite")
		object.__setattr__(self, "centromeres", tuple(self.centromeres))
		if (not all(isinstance(site, Centromere) for site in self.centromeres)
			or len({site.after for site in self.centromeres}) != len(self.centromeres)
			or any(type(site.after) is not int or not 0 <= site.after <= len(self.segments)
				or type(site.active) is not bool
				or site.label is not None and not isinstance(site.label, str)
				for site in self.centromeres)):
			raise ValueError("Centromere sites must be distinct valid boundaries")


@dataclasses.dataclass(frozen=True)
class Cytoband:
	"""Original half-open source interval, linked to its immutable Segment by identity."""

	chromosome: str
	start: int
	end: int
	stain: str
	segment: Segment


@dataclasses.dataclass(frozen=True)
class SegmentAnchor:
	"""Page-coordinate centerline endpoints and conservative painted annotation bounds."""

	segment: Segment
	sister: int
	start: tuple[float, float]
	end: tuple[float, float]
	bounds: tuple[float, float, float, float]


@dataclasses.dataclass(frozen=True)
class ChromosomeLayout:
	"""Filled envelope and annotation geometry; caller reserves outline stroke margins."""

	svg: str
	width: float
	height: float
	boundaries: tuple[tuple[float, float], ...]
	segments: tuple[SegmentAnchor, ...]
	centromere: tuple[float, float] | None
	marker_bounds: tuple[float, float, float, float] | None
	bounds: tuple[float, float, float, float]


#============================================
def read_cytobands(path: pathlib.Path) -> tuple[Chromosome, tuple[Cytoband, ...]]:
	"""Read one intact UCSC full map, starting at zero, with adjacent p/q acen rows.

	G-positive stains darken monotonically; acen is lavender, gvar pale blue and
	stalk teal. These last fills indicate stain categories, not extra anatomy.
	"""
	fills = {'gneg': '#FFFFFF', 'gpos25': '#C0C0C0', 'gpos50': '#808080',
		'gpos75': '#404040', 'gpos100': '#151515', 'acen': '#D9C9EF',
		'gvar': '#C1E7EE', 'stalk': '#72B9A5'}
	records = []
	addresses = set()
	previous = 0
	for line in path.read_text(encoding='ascii').splitlines():
		fields = line.split('\t')
		if len(fields) != 5:
			raise ValueError('Cytobands require five tab-separated fields')
		chromosome, start_text, end_text, address, stain = fields
		if (not re.fullmatch(r'chr[A-Za-z0-9]+', chromosome)
			or not start_text.isdecimal() or not end_text.isdecimal()
			or not re.fullmatch(r'[pq][1-9][0-9]*(?:\.[1-9][0-9]*)?', address)
			or stain not in fills or address in addresses):
			raise ValueError('Unsupported cytoband chromosome, interval, address or stain')
		start, end = int(start_text), int(end_text)
		if (start != previous or end <= start
			or records and chromosome != records[0].chromosome):
			raise ValueError('Cytobands must be contiguous ordered intervals on one chromosome')
		segment = Segment(address, fills[stain], end-start)
		records.append(Cytoband(chromosome, start, end, stain, segment))
		addresses.add(address)
		previous = end
	acen = [i for i, record in enumerate(records) if record.stain == 'acen']
	if (len(acen) != 2 or acen[1] != acen[0]+1
		or any(not row.segment.label.startswith('p') for row in records[:acen[1]])
		or any(not row.segment.label.startswith('q') for row in records[acen[1]:])):
		raise ValueError('An intact map needs p then q arms and adjacent p/q acen rows')
	model = Chromosome(tuple(record.segment for record in records), (Centromere(acen[1]),))
	return model, tuple(records)


#============================================
def delete_segments(chromosome: Chromosome, start: int, stop: int) -> Chromosome:
	"""Remove an internal half-open range within one arm, retaining segment identity."""
	if type(start) is not int or type(stop) is not int or not 0 < start < stop < len(chromosome.segments):
		raise ValueError("Deletion must be a nonempty internal segment range")
	if any(start < site.after < stop for site in chromosome.centromeres):
			raise ValueError("Deletion cannot cross the centromere")
	sites = tuple(Centromere(site.after-(stop-start) if stop <= site.after else site.after,
		site.active, site.label) for site in chromosome.centromeres)
	result = Chromosome(chromosome.segments[:start] + chromosome.segments[stop:], sites)
	return result


#============================================
def reciprocal_translocation(left: Chromosome, left_cut: int,
	right: Chromosome, right_cut: int) -> tuple[Chromosome, Chromosome]:
	"""Exchange ordered right tails distal to each known centromere."""
	for parent, cut in ((left, left_cut), (right, right_cut)):
		if (not parent.centromeres or type(cut) is not int
			or not all(site.after < cut for site in parent.centromeres)):
			raise ValueError("Tail cuts must be internal and distal to a known centromere")
	products = (Chromosome(left.segments[:left_cut] + right.segments[right_cut:], left.centromeres),
		Chromosome(right.segments[:right_cut] + left.segments[left_cut:], right.centromeres))
	return products


#============================================
def render_chromosome_layout(name: str, chromosome: Chromosome, *,
	length: float | None = None, thickness: float = 62,
	orientation: str = 'horizontal', texture: bool = True, sisters: bool = False,
	junctions: tuple[int, ...] = (), allele_labels: bool = False, labels: bool = True,
	marker_size: tuple[float, float] | None = None) -> ChromosomeLayout:
	"""Lay out straight chromatids with the same path geometry used for bends."""
	if (not _positive(thickness) or length is not None and not _positive(length)
		or orientation not in ('horizontal', 'vertical')):
		raise ValueError('Supply finite geometry and a horizontal or vertical orientation')
	axis = length if length is not None else sum(segment.length for segment in chromosome.segments)
	cap = 0
	if orientation == 'horizontal':
		path = lambda y: f'M {cap} {y} H {axis-cap}'
		width, height = axis, thickness
	else:
		path = lambda x: f'M {x} {cap} V {axis-cap}'
		width, height = thickness, axis
	if sisters:
		body = thickness
		if orientation == 'horizontal':
			paths = ((chromosome, path(thickness*.5)), (chromosome, path(thickness*1.7)))
		else:
			paths = ((chromosome, path(thickness*.5)), (chromosome, path(thickness*1.7)))
		if orientation == 'horizontal':
			height = thickness*2.2
		else:
			width = thickness*2.2
		part = sister_chromatid_parts(name, paths, thickness=body, labels=labels,
			marker_size=marker_size, texture=texture, junctions=junctions,
			allele_labels=allele_labels)
		first, second = (part.anchors.get('sister0.centromere'),
			part.anchors.get('sister1.centromere'))
		center = None if first is None else ((first[0]+second[0])/2, (first[1]+second[1])/2)
	else:
		part = chromosome_path_part(name, chromosome, path(thickness/2), thickness=thickness,
			labels=labels, texture=texture, junctions=junctions, allele_labels=allele_labels,
			marker_size=marker_size)
		center = part.anchors.get('centromere')
	prefix = 'sister0.' if sisters else ''
	boundaries = tuple(part.anchors[f'{prefix}boundary_{index}']
		for index in range(len(chromosome.segments)+1))
	segments = tuple(SegmentAnchor(segment, copy,
		part.anchors[f'{"sister" + str(copy) + "." if sisters else ""}boundary_{index}'],
		part.anchors[f'{"sister" + str(copy) + "." if sisters else ""}boundary_{index+1}'],
		part.bounds) for copy in range(2 if sisters else 1)
		for index, segment in enumerate(chromosome.segments))
	return ChromosomeLayout(part.fragment, width, height,
		boundaries, segments, center, None, part.bounds)


#============================================
def _centromere_element(name, along, across, thickness, active, label):
	"""The BPQ collar overlays continuing body color; belts add transverse overhang."""
	scale = thickness/30
	group = xml.etree.ElementTree.Element('g', {'id': name, 'data-layer': 'centromere'})
	shape = {'x': str(-along/2), 'y': str(-across/2), 'width': str(along),
		'height': str(across), 'rx': str(4*scale)}
	clip = xml.etree.ElementTree.SubElement(group, 'clipPath', {'id': name+'-clip'})
	xml.etree.ElementTree.SubElement(clip, 'rect', shape)
	face = xml.etree.ElementTree.SubElement(group, 'g', {'clip-path': f'url(#{name}-clip)'})
	xml.etree.ElementTree.SubElement(face, 'rect', {**shape,
		'fill': '#e6eaf0' if active else '#D9DEE3'})
	path = svgpathtools.Path(svgpathtools.Line(complex(-along/2, 0), complex(along/2, 0)))
	svg_tools.chromosome_surface.Surface(path, across).paint(face, name, texture=False)
	border = {**shape, 'fill': 'none', 'stroke': '#40474E', 'stroke-width': str(2*scale)}
	if not active:
		border['stroke-dasharray'] = f'{4*scale} {2*scale}'
	xml.etree.ElementTree.SubElement(group, 'rect', border)
	if label:
		xml.etree.ElementTree.SubElement(group, 'text', {'x': '0', 'y': str(thickness*.13),
			'font-family': 'Atkinson Hyperlegible Next', 'font-size': str(thickness*.38),
			'text-anchor': 'middle', 'fill': '#000000', 'font-weight': 'bold'}).text = label
	return group


#============================================
def centromere_part(name: str, *, thickness: float = 62, active: bool = True,
	label: str | None = None, across: float | None = None) -> svg_tools.parts.SvgPart:
	"""Labelable rounded rectangular centromere centered on an axis-aligned chromatid."""
	if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.-]*', name):
		raise ValueError('Use an XML-safe unique namespace')
	if not _positive(thickness):
		raise ValueError('Supply a finite positive thickness')
	if type(active) is not bool or label is not None and not isinstance(label, str):
		raise ValueError('Centromere activity and label must be valid')
	if across is not None and not _positive(across):
		raise ValueError("Across must be a finite positive span")
	rx, ry, stroke = thickness*16/30, max(thickness*1.3, across or 0)/2, thickness*2/30
	marker = _centromere_element(name+'-centromere', 2*rx, 2*ry, thickness, active, label)
	fragment = xml.etree.ElementTree.tostring(marker, encoding='ascii', xml_declaration=False).decode('ascii')
	margin = stroke/2
	return svg_tools.parts.SvgPart(fragment, (-rx-margin, -ry-margin, rx+margin, ry+margin),
		{'center': (0, 0), 'left': (-rx, 0), 'right': (rx, 0),
			'top': (0, -ry), 'bottom': (0, ry)})


#============================================
def sister_chromatid_parts(name: str, chromatids: tuple[tuple[Chromosome, str], ...], *,
	thickness: float = 28, labels: bool = False,
	marker_size: tuple[float, float] | None = None, texture: bool = True,
	junctions: tuple[int, ...] = (), allele_labels: bool = False) -> svg_tools.parts.SvgPart:
	"""Assemble independent sister chromatids and join their corresponding centromeres."""
	if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.-]*', name):
		raise ValueError('Use an XML-safe unique namespace')
	if len(chromatids) != 2:
		raise ValueError('Supply exactly two sister chromatid models and centerlines')
	if any(tuple(site.after for site in chromosome.centromeres)
		!= tuple(site.after for site in chromatids[0][0].centromeres)
		for chromosome, _ in chromatids):
		raise ValueError('Sisters need corresponding centromere sites')
	parts = {f'sister{index}': chromosome_path_part(f'{name}-sister-{index}', chromosome,
		path_d, thickness=thickness, labels=labels, marker_size=marker_size, texture=texture,
		junctions=junctions, allele_labels=allele_labels)
		for index, (chromosome, path_d) in enumerate(chromatids)}
	for key, part in list(parts.items()):
		root = xml.etree.ElementTree.fromstring(part.fragment)
		for child in list(root):
			if child.get('data-layer') == 'centromere':
				root.remove(child)
		parts[key] = dataclasses.replace(part, fragment=xml.etree.ElementTree.tostring(root, encoding='unicode'))
	for index, site in enumerate(chromatids[0][0].centromeres):
		first = parts['sister0'].anchors[f'centromere_{index}']
		second = parts['sister1'].anchors[f'centromere_{index}']
		dx, dy = second[0]-first[0], second[1]-first[1]
		separation = math.hypot(dx, dy)
		along = marker_size[0] if marker_size else thickness*32/30
		across = max(separation+thickness*1.3, marker_size[1] if marker_size else 0)
		marker = _centromere_element(f'{name}-belt-{index}', along, across, thickness, site.active, site.label)
		fragment = xml.etree.ElementTree.tostring(marker, encoding='unicode')
		margin = thickness/30
		belt = svg_tools.parts.SvgPart(fragment,
			(-along/2-margin, -across/2-margin, along/2+margin, across/2+margin), {})
		parts[f'belt{index}'] = svg_tools.parts.transform(belt, x=(first[0]+second[0])/2,
			y=(first[1]+second[1])/2, rotation=math.degrees(math.atan2(dy, dx))-90)
	return svg_tools.parts.group(parts)


#============================================
def condensed_chromosome_part(name: str, chromosome: Chromosome, *, radius: float = 18,
	label: str | None = None) -> svg_tools.parts.SvgPart:
	"""Draw a compact, material-retaining chromosome state such as a Barr body."""
	if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.-]*', name):
		raise ValueError('Use an XML-safe unique namespace')
	if not isinstance(chromosome, Chromosome) or not _positive(radius):
		raise ValueError('Supply a Chromosome and finite positive radius')
	fill = chromosome.segments[0].color
	group = xml.etree.ElementTree.Element('g', {'id': name, 'data-chromosome-state': 'condensed'})
	clip = xml.etree.ElementTree.SubElement(group, 'clipPath', {'id': name+'-compact-clip'})
	xml.etree.ElementTree.SubElement(clip, 'circle', {'cx': '0', 'cy': '0', 'r': str(radius)})
	face = xml.etree.ElementTree.SubElement(group, 'g', {'clip-path': f'url(#{name}-compact-clip)'})
	xml.etree.ElementTree.SubElement(face, 'circle', {'cx': '0', 'cy': '0', 'r': str(radius), 'fill': fill})
	path = svgpathtools.Path(svgpathtools.Line(complex(-radius, 0), complex(radius, 0)))
	svg_tools.chromosome_surface.Surface(path, radius*2).paint(face, name, texture=False)
	xml.etree.ElementTree.SubElement(group, 'circle', {'cx': '0', 'cy': '0', 'r': str(radius),
		'fill': 'none', 'stroke': '#40474E', 'stroke-width': str(radius*.09)})
	if label:
		xml.etree.ElementTree.SubElement(group, 'text', {'x': '0', 'y': str(radius*.18),
			'font-family': 'Atkinson Hyperlegible Next', 'font-size': str(radius*.72),
			'text-anchor': 'middle', 'fill': _label_color(fill)}).text = label
	fragment = xml.etree.ElementTree.tostring(group, encoding='ascii', xml_declaration=False).decode('ascii')
	stroke = radius*.09/2
	bounds = svg_tools.parts.include_text_bounds(fragment,
		(-radius-stroke, -radius-stroke, radius+stroke, radius+stroke))
	return svg_tools.parts.SvgPart(fragment, bounds, {'center': (0, 0)})


#============================================
def chromosome_part(name: str, chromosome: Chromosome, *,
	length: float | None = None, thickness: float = 62,
	orientation: str = 'horizontal', texture: bool = True, sisters: bool = False,
	junctions: tuple[int, ...] = (), allele_labels: bool = False, labels: bool = True,
	marker_size: tuple[float, float] | None = None) -> svg_tools.parts.SvgPart:
	"""Render a local part with start, end, center, boundary_N and centromere anchors."""
	layout = render_chromosome_layout(name, chromosome, length=length, thickness=thickness,
		orientation=orientation, texture=texture, sisters=sisters, junctions=junctions,
		allele_labels=allele_labels, labels=labels, marker_size=marker_size)
	bounds = layout.bounds
	anchors = {f'boundary_{index}': point for index, point in enumerate(layout.boundaries)}
	anchors['start'], anchors['end'] = layout.boundaries[0], layout.boundaries[-1]
	anchors['center'] = (layout.width/2, layout.height/2)
	if layout.centromere is not None:
		anchors['centromere'] = layout.centromere
	for index, site in enumerate(chromosome.centromeres):
		anchors[f'centromere_{index}'] = layout.boundaries[site.after]
	part = svg_tools.parts.SvgPart(layout.svg, bounds, anchors)
	return part


#============================================
def chromosome_path_part(name: str, chromosome: Chromosome, path_d: str, *,
	thickness: float = 28, closed: bool = False, cut_ends: bool = False,
	labels: bool = True, texture: bool = True, junctions: tuple[int, ...] = (),
	allele_labels: bool = False, marker_size: tuple[float, float] | None = None) -> svg_tools.parts.SvgPart:
	"""Paint ordered regions along one authored continuous chromatid centerline.

	Lengths give relative arc spans. Closed acentric rings have neither terminal caps
	nor start/end anchors. Open internal fragments use cut_ends=True. Labels stay
	upright, and source-boundary and segment-midpoint anchors follow the path.
	The caller supplies biologically meaningful bends, spacing and crossing order.
	"""
	if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.-]*', name):
		raise ValueError('Use an XML-safe unique namespace')
	if not isinstance(chromosome, Chromosome) or not _positive(thickness):
		raise ValueError('Supply a Chromosome and finite positive thickness')
	if (any(type(index) is not int or not 0 < index < len(chromosome.segments)
		for index in junctions) or len(set(junctions)) != len(junctions)
		or any(index == site.after for index in junctions for site in chromosome.centromeres)):
		raise ValueError('Junctions must be distinct internal non-centromere boundaries')
	if allele_labels and any(segment.label and not re.fullmatch(r'[a-z][+-]', segment.label)
		for segment in chromosome.segments):
		raise ValueError('Allele labels need one lowercase letter and +/- or an empty label')
	if marker_size is not None and (len(marker_size) != 2 or not all(_positive(value) for value in marker_size)):
		raise ValueError('Marker size must contain two finite positive lengths')
	if closed and (cut_ends or chromosome.centromeres):
		raise ValueError('Closed acentric rings have no cut ends or centromere')
	path = svgpathtools.parse_path(path_d)
	if not path or not path.iscontinuous():
		raise ValueError('Supply one continuous nonempty centerline')
	control_points = [point for segment in path for point in
		((segment.start, segment.end, segment.radius, segment.center)
		if isinstance(segment, svgpathtools.Arc) else segment.bpoints())]
	if any(not math.isfinite(value) for point in control_points
		for value in (point.real, point.imag)):
		raise ValueError('Path coordinates must be finite')
	if any(segment.length() <= 0 for segment in path):
		raise ValueError('Centerline segments must have positive length')
	if path.isclosed() != closed:
		raise ValueError('Path closure must match the closed setting')
	length = path.length()
	if not _positive(length):
		raise ValueError('Centerline length must be finite and positive')
	if closed:
		area = path.area(chord_length=length/256)
		if not math.isfinite(area) or area == 0:
			raise ValueError('A ring must enclose nonzero finite area')
	lengths = [segment.length for segment in chromosome.segments]
	distances = [0.0]
	for segment_length in lengths:
		distances.append(distances[-1] + segment_length/sum(lengths)*length)
	distances[-1] = length
	if not all(a < b for a, b in zip(distances, distances[1:])):
		raise ValueError('Geometry must retain distinct segment boundaries')
	parameters = [path.ilength(distance) if 0 < distance < length else
		(0.0 if distance == 0 else 1.0) for distance in distances]
	def point(parameter: float) -> tuple[float, float]:
		position = path.start if parameter == 0 else path.end if parameter == 1 else path.point(parameter)
		return (position.real, position.imag)
	anchors = {f'boundary_{index}': point(parameter)
		for index, parameter in enumerate(parameters)}
	if not closed:
		anchors['start'], anchors['end'] = point(0), point(1)
	group = xml.etree.ElementTree.Element('g', {'id': name})
	path_text = path.d() + (' Z' if closed else '')
	stroke = thickness * 2/30
	surface = svg_tools.chromosome_surface.Surface(path, thickness)
	envelope = surface.envelope(closed, cut_ends)
	defs = xml.etree.ElementTree.SubElement(group, 'defs')
	clip = xml.etree.ElementTree.SubElement(defs, 'clipPath', {'id': name+'-body-clip'})
	xml.etree.ElementTree.SubElement(clip, 'path', {'d': envelope, 'clip-rule': 'evenodd'})
	paint = xml.etree.ElementTree.SubElement(group, 'g', {'clip-path': f'url(#{name}-body-clip)',
		'data-layer': 'body'})
	xml.etree.ElementTree.SubElement(paint, 'path', {'d': path_text, 'fill': 'none',
		'stroke': chromosome.segments[0].color, 'stroke-width': str(thickness),
		'stroke-linecap': 'butt', 'stroke-linejoin': 'round'})
	for index, segment in enumerate(chromosome.segments):
		region = xml.etree.ElementTree.SubElement(paint, 'g', {
			'id': f'{name}-region-{index}', 'data-source-label': segment.label})
		portion = path.cropped(parameters[index], parameters[index+1])
		xml.etree.ElementTree.SubElement(region, 'path', {'d': portion.d(), 'fill': 'none',
			'stroke': segment.color, 'stroke-width': str(thickness),
			'stroke-linecap': 'butt', 'stroke-linejoin': 'round'})
		middle = path.ilength((distances[index]+distances[index+1])/2)
		anchors[f'segment_{index}'] = point(middle)
	texture_edges = [0] + [index for index in range(1, len(chromosome.segments))
		if chromosome.segments[index].color != chromosome.segments[index-1].color
		or any(site.after == index for site in chromosome.centromeres)] + [len(chromosome.segments)]
	texture_spans = []
	for first, last in zip(texture_edges, texture_edges[1:]):
		left, right = distances[first], distances[last]
		if not closed and not cut_ends:
			if first == 0:
				left += min(thickness*8/30, length/4)
			if last == len(chromosome.segments):
				right -= min(thickness*8/30, length/4)
		if any(site.after == first for site in chromosome.centromeres):
			left += (marker_size[0] if marker_size else thickness*32/30)/2
		if right > left:
			texture_spans.append((left, right))
	surface.paint(paint, name, texture=texture and bool(texture_spans), texture_spans=texture_spans)
	if not closed and not cut_ends:
		cap_length = min(thickness*8/30, length/4)
		for left, right in ((0, cap_length), (length-cap_length, length)):
			xml.etree.ElementTree.SubElement(paint, 'path', {
				'd': surface.ribbon(left, right, -thickness/2, thickness/2),
				'fill': '#888888', 'data-layer': 'telomere'})
	# A double-width clipped stroke puts the whole BPQ border inside the body.
	xml.etree.ElementTree.SubElement(paint, 'path', {'d': envelope,
		'fill': 'none', 'stroke': '#000000', 'stroke-width': str(2*stroke),
		'stroke-linejoin': 'round', 'data-layer': 'outline'})
	for index in junctions:
		scale = thickness/30
		center = distances[index]
		coords = [(center+(3 if step % 2 else 0)*scale,
			-thickness/2+stroke+(thickness-2*stroke)*step/6) for step in range(7)]
		coords += [(center+(-3 if step % 2 == 0 else 0)*scale,
			-thickness/2+stroke+(thickness-2*stroke)*step/6) for step in reversed(range(7))]
		xml.etree.ElementTree.SubElement(group, 'path', {'id': f'{name}-join-{index}',
			'd': surface.polygon(coords), 'fill': '#FFFFFF'})
	for site_number, site in enumerate(chromosome.centromeres):
		cx, cy = anchors[f'boundary_{site.after}']
		anchors[f'centromere_{site_number}'] = (cx, cy)
		if site_number == 0:
			anchors['centromere'] = (cx, cy)
		tangent = path.unit_tangent(parameters[site.after])
		angle = math.degrees(math.atan2(tangent.imag, tangent.real))
		along, across = marker_size if marker_size is not None else (thickness*32/30, thickness*1.3)
		across = max(across, thickness*1.3)
		marker = _centromere_element(f'{name}-centromere-{site_number}', along, across,
			thickness, site.active, site.label)
		marker.set('transform', f'translate({cx} {cy}) rotate({angle})')
		group.append(marker)
	if labels:
		for index, segment in enumerate(chromosome.segments):
			if not segment.label:
				continue
			left, right = distances[index:index+2]
			clearance = (marker_size[0] if marker_size else thickness*32/30)/2
			if any(site.after == index for site in chromosome.centromeres):
				left += clearance
			if any(site.after == index+1 for site in chromosome.centromeres):
				right -= clearance
			if right <= left:
				left, right = distances[index:index+2]
			middle = path.ilength((left+right)/2)
			x, y = point(middle)
			size = min(thickness*.5, (right-left)*.82/max(1, len(segment.label))/.65)
			text = xml.etree.ElementTree.SubElement(group, 'text', {'x': str(x), 'y': str(y+size*.34),
				'font-family': 'monospace', 'font-size': str(size),
				'font-weight': 'bold', 'text-anchor': 'middle', 'fill': _label_color(segment.color),
				'stroke': 'none'})
			if allele_labels and segment.label:
				xml.etree.ElementTree.SubElement(text, 'tspan', {'font-style': 'italic'}).text = segment.label[0]
				xml.etree.ElementTree.SubElement(text, 'tspan', {'dy': str(-size*.22),
					'font-size': str(size*.40)}).text = '+' if segment.label[1] == '+' else '\u2212'
			else:
				text.text = segment.label
	fragment = xml.etree.ElementTree.tostring(group, encoding='ascii', xml_declaration=False).decode('ascii')
	xmin, xmax, ymin, ymax = path.bbox()
	margin = thickness/2 + stroke
	if chromosome.centromeres:
		margin = max(margin, max(marker_size or (thickness*32/30, thickness*1.3))/2+stroke)
	anchors['center'] = ((xmin+xmax)/2, (ymin+ymax)/2)
	bounds = svg_tools.parts.include_text_bounds(fragment,
		(xmin-margin, ymin-margin, xmax+margin, ymax+margin))
	part = svg_tools.parts.SvgPart(fragment, bounds, anchors)
	return part
