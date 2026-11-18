"""Schematic chromosomes, joined sisters and bounded segment rearrangements."""

import re
import math
import pathlib
import dataclasses
import urllib.parse
import collections.abc

import lxml.etree
import svgpathtools

import svg_tools._xml
import svg_tools.parts
import svg_tools.text
import svg_tools.palette
import svg_tools.chromosome_loci
import svg_tools.chromosome_surface
import svg_tools.chromosome_topology


_JUNCTION_HALF_SPAN = 3
_GENE_CARD_COLOR = svg_tools.palette.shade('light_orange', 'light')


#============================================
def _positive(value: float) -> bool:
	valid = (isinstance(value, (int, float)) and not isinstance(value, bool)
		and math.isfinite(value) and value > 0)
	return valid


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
class CentromereStyle:
	"""Optional label and face color for a centromere collar."""

	label: str | None = None
	fill: str | None = None

	def __post_init__(self) -> None:
		if self.label is not None and not isinstance(self.label, str):
			raise ValueError('Centromere label must be a string')
		if self.fill is not None and (not isinstance(self.fill, str)
			or not re.fullmatch(r'#[0-9A-Fa-f]{6}', self.fill)):
			raise ValueError('Centromere fill must be a six-digit hex color')


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


#============================================
def gene_locus_part(name: str, surface: svg_tools.chromosome_surface.Surface,
	center: float, gene: Segment, *, cut_ends: bool = False) -> svg_tools.parts.SvgPart:
	"""Label an explicit locus, leaving chromosome color next to any telomere caps."""
	if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.-]*', name):
		raise ValueError('Use an XML-safe unique namespace')
	if not isinstance(surface, svg_tools.chromosome_surface.Surface):
		raise ValueError('Gene loci need a prepared chromosome surface')
	if not isinstance(gene, Segment) or not gene.label:
		raise ValueError('Gene loci need a labeled Segment')
	if not isinstance(center, (int, float)) or not math.isfinite(center):
		raise ValueError('Gene locus center must be finite')
	terminal = not cut_ends and not surface.path.isclosed()
	part = svg_tools.chromosome_loci.card(name, surface, center, gene.label, gene.color,
		gene.length, minimum_size=0, terminal_ends=(terminal, terminal))
	if part is None:
		part = svg_tools.chromosome_loci.external(name, surface, center, gene.label, 0j)
	return part


#============================================
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
	junctions: tuple[int, ...] = (), labels: bool = True,
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
			marker_size=marker_size, texture=texture, junctions=junctions)
		first, second = (part.anchors.get('sister0.centromere'),
			part.anchors.get('sister1.centromere'))
		center = None if first is None else ((first[0]+second[0])/2, (first[1]+second[1])/2)
	else:
		part = chromosome_path_part(name, chromosome, path(thickness/2), thickness=thickness,
			labels=labels, texture=texture, junctions=junctions,
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
def _centromere_element(name: str, along: float, across: float, thickness: float,
	active: bool, style: CentromereStyle | None, angle: float = 0) -> lxml.etree._Element:
	"""The BPQ collar overlays continuing body color; belts add transverse overhang."""
	scale = thickness/30
	fill = '#e6eaf0' if active else '#D9DEE3'
	if style and style.fill:
		fill = style.fill
	group = lxml.etree.Element('g', {'id': name, 'data-layer': 'centromere'})
	shape = {'x': str(-along/2), 'y': str(-across/2), 'width': str(along),
		'height': str(across), 'rx': str(4*scale)}
	clip = lxml.etree.SubElement(group, 'clipPath', {'id': name+'-clip'})
	lxml.etree.SubElement(clip, 'rect', shape)
	face = lxml.etree.SubElement(group, 'g', {'clip-path': f'url(#{name}-clip)'})
	lxml.etree.SubElement(face, 'rect', {**shape, 'fill': fill})
	path = svgpathtools.Path(svgpathtools.Line(complex(-along/2, 0), complex(along/2, 0)))
	svg_tools.chromosome_surface.Surface(path, across).paint(face, name, texture=False)
	border = {**shape, 'fill': 'none', 'stroke': '#40474E', 'stroke-width': str(2*scale)}
	if not active:
		border['stroke-dasharray'] = f'{4*scale} {2*scale}'
	lxml.etree.SubElement(group, 'rect', border)
	if style and style.label:
		size = thickness*.72
		left, top, right, bottom = svg_tools.text.measure_text(style.label, size=size, bold=True)
		# Fit the ink inside the collar at any rotation, keeping the text upright.
		fit = min(1, min(along, across)*.86/math.hypot(right-left, bottom-top))
		part = svg_tools.text.label(-(left+right)*fit/2, -(top+bottom)*fit/2,
			style.label, size=size*fit, color=svg_tools.text.label_color(fill), bold=True)
		text = svg_tools._xml.parse(part.fragment)
		text.set('transform', f'rotate({-angle})')
		group.append(text)
	return group


#============================================
def centromere_part(name: str, *, thickness: float = 62, active: bool = True,
	label: str | None = None, across: float | None = None,
	fill: str | None = None) -> svg_tools.parts.SvgPart:
	"""Labelable rounded rectangular centromere centered on an axis-aligned chromatid."""
	if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.-]*', name):
		raise ValueError('Use an XML-safe unique namespace')
	if not _positive(thickness):
		raise ValueError('Supply a finite positive thickness')
	if type(active) is not bool:
		raise ValueError('Centromere activity must be a boolean')
	if across is not None and not _positive(across):
		raise ValueError("Across must be a finite positive span")
	rx, ry, stroke = thickness*16/30, max(thickness*1.3, across or 0)/2, thickness*2/30
	marker = _centromere_element(name+'-centromere', 2*rx, 2*ry, thickness, active,
		CentromereStyle(label=label, fill=fill))
	fragment = lxml.etree.tostring(marker, encoding='ascii', xml_declaration=False).decode('ascii')
	margin = stroke/2
	return svg_tools.parts.SvgPart(fragment, (-rx-margin, -ry-margin, rx+margin, ry+margin),
		{'center': (0, 0), 'left': (-rx, 0), 'right': (rx, 0),
			'top': (0, -ry), 'bottom': (0, ry)})


#============================================
def sister_chromatid_parts(name: str, chromatids: tuple[tuple[Chromosome, str], ...], *,
	thickness: float = 28, labels: bool = False,
	marker_size: tuple[float, float] | None = None, texture: bool = True,
	junctions: tuple[int, ...] = ()) -> svg_tools.parts.SvgPart:
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
		junctions=junctions)
		for index, (chromosome, path_d) in enumerate(chromatids)}
	for key, part in list(parts.items()):
		root = svg_tools._xml.parse(part.fragment)
		for child in list(root):
			if child.get('data-layer') == 'centromere':
				root.remove(child)
		parts[key] = dataclasses.replace(part, fragment=lxml.etree.tostring(root, encoding='unicode'))
	for index, site in enumerate(chromatids[0][0].centromeres):
		first = parts['sister0'].anchors[f'centromere_{index}']
		second = parts['sister1'].anchors[f'centromere_{index}']
		parts[f'belt{index}'] = _sister_belt_part(f'{name}-belt-{index}', first, second,
			thickness, marker_size, active=site.active, style=CentromereStyle(label=site.label))
	return svg_tools.parts.group(parts)


#============================================
def _sister_belt_part(name: str, first: tuple[float, float], second: tuple[float, float],
	thickness: float, marker_size: tuple[float, float] | None = None, *,
	active: bool = True, style: CentromereStyle | None = None) -> svg_tools.parts.SvgPart:
	"""Span both attachment sites with the same BPQ centromere paint as a collar."""
	dx, dy = second[0]-first[0], second[1]-first[1]
	separation = math.hypot(dx, dy)
	along = marker_size[0] if marker_size else thickness*32/30
	across = max(separation+thickness*1.3, marker_size[1] if marker_size else 0)
	angle = math.degrees(math.atan2(dy, dx))-90
	marker = _centromere_element(name, along, across, thickness, active, style, angle)
	fragment = lxml.etree.tostring(marker, encoding='unicode')
	margin = thickness/30
	belt = svg_tools.parts.SvgPart(fragment,
		(-along/2-margin, -across/2-margin, along/2+margin, across/2+margin), {})
	part = svg_tools.parts.transform(belt, x=(first[0]+second[0])/2,
		y=(first[1]+second[1])/2, rotation=angle)
	return part


#============================================
def condensed_chromosome_part(name: str, chromosome: Chromosome, *, radius: float = 18,
	label: str | None = None) -> svg_tools.parts.SvgPart:
	"""Draw a compact, material-retaining chromosome state such as a Barr body."""
	if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.-]*', name):
		raise ValueError('Use an XML-safe unique namespace')
	if not isinstance(chromosome, Chromosome) or not _positive(radius):
		raise ValueError('Supply a Chromosome and finite positive radius')
	fill = chromosome.segments[0].color
	group = lxml.etree.Element('g', {'id': name, 'data-chromosome-state': 'condensed'})
	clip = lxml.etree.SubElement(group, 'clipPath', {'id': name+'-compact-clip'})
	lxml.etree.SubElement(clip, 'circle', {'cx': '0', 'cy': '0', 'r': str(radius)})
	face = lxml.etree.SubElement(group, 'g', {'clip-path': f'url(#{name}-compact-clip)'})
	lxml.etree.SubElement(face, 'circle', {'cx': '0', 'cy': '0', 'r': str(radius), 'fill': fill})
	path = svgpathtools.Path(svgpathtools.Line(complex(-radius, 0), complex(radius, 0)))
	svg_tools.chromosome_surface.Surface(path, radius*2).paint(face, name, texture=False)
	lxml.etree.SubElement(group, 'circle', {'cx': '0', 'cy': '0', 'r': str(radius),
		'fill': 'none', 'stroke': '#40474E', 'stroke-width': str(radius*.09)})
	if label:
		lxml.etree.SubElement(group, 'text', {'x': '0', 'y': str(radius*.18),
			'font-family': 'Atkinson Hyperlegible Next', 'font-size': str(radius*.72),
			'text-anchor': 'middle', 'fill': svg_tools.text.label_color(fill)}).text = label
	fragment = lxml.etree.tostring(group, encoding='ascii', xml_declaration=False).decode('ascii')
	stroke = radius*.09/2
	bounds = svg_tools.parts.include_text_bounds(fragment,
		(-radius-stroke, -radius-stroke, radius+stroke, radius+stroke))
	return svg_tools.parts.SvgPart(fragment, bounds, {'center': (0, 0)})


#============================================
def chromosome_part(name: str, chromosome: Chromosome, *,
	length: float | None = None, thickness: float = 62,
	orientation: str = 'horizontal', texture: bool = True, sisters: bool = False,
	junctions: tuple[int, ...] = (), labels: bool = True,
	marker_size: tuple[float, float] | None = None) -> svg_tools.parts.SvgPart:
	"""Render a local part with start, end, center, boundary_N and centromere anchors."""
	layout = render_chromosome_layout(name, chromosome, length=length, thickness=thickness,
		orientation=orientation, texture=texture, sisters=sisters, junctions=junctions,
		labels=labels, marker_size=marker_size)
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
	marker_size: tuple[float, float] | None = None) -> svg_tools.parts.SvgPart:
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
	path = svg_tools.chromosome_surface.smooth_centerline(path)
	length = path.length()
	if not _positive(length):
		raise ValueError('Centerline length must be finite and positive')
	if closed:
		area = path.area(chord_length=length/256)
		if not math.isfinite(area) or area == 0:
			raise ValueError('A ring must enclose nonzero finite area')
	surface = svg_tools.chromosome_surface.Surface(path, thickness)
	terminal_ends = (not closed and not cut_ends,) * 2
	total = sum(segment.length for segment in chromosome.segments)
	distances = [0.0]
	for segment in chromosome.segments:
		distances.append(distances[-1] + segment.length/total*surface.length)
	distances[-1] = surface.length
	sites = [(distances[site.after], site.active, CentromereStyle(label=site.label))
		for site in chromosome.centromeres]
	part = _paint_chromatid(name, chromosome.segments, surface, distances, sites, closed=closed,
		terminal_ends=terminal_ends, labels=labels, texture=texture,
		junctions=junctions, marker_size=marker_size)
	return part


#============================================
def _junction_coords(center: float, surface: svg_tools.chromosome_surface.Surface) -> list[tuple[float, float]]:
	"""Vertices of the white zigzag in along- and across-surface coordinates."""
	half_span = _JUNCTION_HALF_SPAN*surface.scale
	half_height = surface.width/2-surface.width*2/30
	coords = [(center+(half_span if step % 2 else 0), -half_height+2*half_height*step/6)
		for step in range(7)]
	coords += [(center-(half_span if step % 2 == 0 else 0), -half_height+2*half_height*step/6)
		for step in reversed(range(7))]
	return coords


#============================================
def _junction_clears_collars(surface: svg_tools.chromosome_surface.Surface, distance: float,
	site_distances: list[float], outward: complex) -> bool:
	"""Compare the bent glyph with each collar's stroked rectangle in its own frame."""
	vertices = [surface.point(*xy) for xy in _junction_coords(distance, surface)]
	along = surface.width*16/30+surface.scale
	across = surface.width*.65+abs(outward)+surface.scale
	for site in site_distances:
		parameter = surface.path.ilength(site)
		center = surface.path.point(parameter)-outward
		tangent = surface.path.unit_tangent(parameter)
		local = [(vertex-center)*tangent.conjugate() for vertex in vertices]
		if (min(p.real for p in local) <= along and max(p.real for p in local) >= -along
			and min(p.imag for p in local) <= across and max(p.imag for p in local) >= -across):
			return False
	return True


#============================================
def _paint_chromatid(name: str, segments: collections.abc.Sequence[Segment],
	surface: svg_tools.chromosome_surface.Surface, distances: list[float],
	sites: list[tuple[float, bool, CentromereStyle | None]], *, closed: bool = False,
	terminal_ends: tuple[bool, bool] = (True, True), labels: bool = False,
	texture: bool = True, junctions: tuple[int, ...] = (),
	marker_size: tuple[float, float] | None = None,
	loci: tuple[svg_tools.parts.SvgPart, ...] = (),
	draw_centromeres: bool = True) -> svg_tools.parts.SvgPart:
	"""Use one clipped BPQ body surface for legacy and source-backed chromatids."""
	path, thickness, length = surface.path, surface.width, surface.length
	if not all(a < b for a, b in zip(distances, distances[1:])):
		raise ValueError('Geometry must retain distinct segment boundaries')
	parameters = [path.ilength(distance) if 0 < distance < length else
		(0.0 if distance == 0 else 1.0) for distance in distances]
	def point(parameter: float) -> tuple[float, float]:
		position = path.start if parameter == 0 else path.end if parameter == 1 else path.point(parameter)
		xy = (position.real, position.imag)
		return xy
	anchors = {f'boundary_{index}': point(parameter)
		for index, parameter in enumerate(parameters)}
	if not closed:
		anchors['start'], anchors['end'] = point(0), point(1)
	group = lxml.etree.Element('g', {'id': name})
	label_bounds = []
	path_text = path.d() + (' Z' if closed else '')
	stroke = thickness * 2/30
	envelope = surface.envelope(closed, terminal_ends=terminal_ends)
	defs = lxml.etree.SubElement(group, 'defs')
	clip = lxml.etree.SubElement(defs, 'clipPath', {'id': name+'-body-clip'})
	lxml.etree.SubElement(clip, 'path', {'d': envelope, 'clip-rule': 'evenodd'})
	paint = lxml.etree.SubElement(group, 'g', {'clip-path': f'url(#{name}-body-clip)',
		'data-layer': 'body'})
	lxml.etree.SubElement(paint, 'path', {'d': path_text, 'fill': 'none',
		'stroke': segments[0].color, 'stroke-width': str(thickness),
		'stroke-linecap': 'butt', 'stroke-linejoin': 'round'})
	for index, segment in enumerate(segments):
		region = lxml.etree.SubElement(paint, 'g', {
			'id': f'{name}-region-{index}', 'data-source-label': segment.label})
		portion = path.cropped(parameters[index], parameters[index+1])
		lxml.etree.SubElement(region, 'path', {'d': portion.d(), 'fill': 'none',
			'stroke': segment.color, 'stroke-width': str(thickness),
			'stroke-linecap': 'butt', 'stroke-linejoin': 'round'})
		middle = path.ilength((distances[index]+distances[index+1])/2)
		anchors[f'segment_{index}'] = point(middle)
	site_distances = {distance for distance, _, _ in sites}
	texture_edges = sorted({0.0, length, *site_distances,
		*(distances[i] for i in range(1, len(segments)) if segments[i].color != segments[i-1].color)})
	texture_spans = []
	cap_length = surface.cap_length
	collar_half = (marker_size[0] if marker_size else thickness*32/30)/2
	for start, stop in zip(texture_edges, texture_edges[1:]):
		left, right = start, stop
		if terminal_ends[0] and start == 0:
			left += cap_length
		if terminal_ends[1] and stop == length:
			right -= cap_length
		if start in site_distances:
			left += collar_half
		if right > left:
			texture_spans.append((left, right))
	surface.paint(paint, name, texture=texture and bool(texture_spans), texture_spans=texture_spans)
	for terminal, (left, right) in zip(terminal_ends, ((0, cap_length), (length-cap_length, length))):
		if terminal:
			lxml.etree.SubElement(paint, 'path', {
				'd': surface.ribbon(left, right, -thickness/2, thickness/2),
				'fill': '#888888', 'data-layer': 'telomere'})
	# A double-width clipped stroke puts the whole BPQ border inside the body.
	lxml.etree.SubElement(paint, 'path', {'d': envelope,
		'fill': 'none', 'stroke': '#000000', 'stroke-width': str(2*stroke),
		'stroke-linejoin': 'round', 'data-layer': 'outline'})
	for index in junctions:
		lxml.etree.SubElement(group, 'path', {'id': f'{name}-join-{index}',
			'd': surface.polygon(_junction_coords(distances[index], surface)), 'fill': '#FFFFFF'})
	for locus in loci:
		group.append(svg_tools._xml.parse(locus.fragment))
		anchors.update(locus.anchors)
		label_bounds.append(locus.bounds)
	painted = set()
	for site_number, (distance, active, style) in enumerate(sites):
		parameter = path.ilength(distance)
		cx, cy = point(parameter)
		anchors[f'centromere_{site_number}'] = (cx, cy)
		if site_number == 0:
			anchors['centromere'] = (cx, cy)
		if not draw_centromeres or distance in painted:
			continue
		painted.add(distance)
		tangent = path.unit_tangent(parameter)
		angle = math.degrees(math.atan2(tangent.imag, tangent.real))
		along, across = marker_size if marker_size is not None else (thickness*32/30, thickness*1.3)
		across = max(across, thickness*1.3)
		marker = _centromere_element(f'{name}-centromere-{site_number}', along, across,
			thickness, active, style, angle)
		marker.set('transform', f'translate({cx} {cy}) rotate({angle})')
		group.append(marker)
	if labels:
		for index, segment in enumerate(segments):
			if not segment.label:
				continue
			left, right = distances[index:index+2]
			if left in site_distances:
				left += collar_half
			if right in site_distances:
				right -= collar_half
			if right <= left:
				left, right = distances[index:index+2]
			center = (left+right)/2
			middle = path.ilength(center)
			x, y = point(middle)
			size = svg_tools.chromosome_loci.label_size(segment.label, surface, center,
				right-left, thickness, segment.color)
			label_bounds.append(svg_tools.chromosome_loci.append_label(group, x, y,
				segment.label, size, segment.color))
	fragment = lxml.etree.tostring(group, encoding='ascii', xml_declaration=False).decode('ascii')
	xmin, xmax, ymin, ymax = path.bbox()
	margin = thickness/2 + stroke
	if draw_centromeres and sites:
		margin = max(margin, max(marker_size or (thickness*32/30, thickness*1.3))/2+stroke)
	anchors['center'] = ((xmin+xmax)/2, (ymin+ymax)/2)
	# Collar labels fit inside the collars. Locus and segment labels supply measured bounds.
	bounds = (xmin-margin, ymin-margin, xmax+margin, ymax+margin)
	part = svg_tools.parts.SvgPart(fragment, svg_tools.parts.union_bounds(bounds, *label_bounds), anchors)
	return part


#============================================
def _render_topology_chromatid(name: str, model: svg_tools.chromosome_topology.Chromatid,
	surface: svg_tools.chromosome_surface.Surface, palette: dict[tuple[str, str], str], *,
	sites: tuple[svg_tools.chromosome_topology.ProjectedCentromere, ...],
	centromere_styles: dict[tuple[str, str], CentromereStyle],
	outward: complex = 0j) -> tuple[svg_tools.parts.SvgPart, list[svg_tools.parts.SvgPart]]:
	"""Project source features once into the existing BPQ paint and label inputs."""
	topology = svg_tools.chromosome_topology
	regions = topology.project_regions(model)
	genes = topology.project_genes(model)
	length, width = surface.length, surface.width
	material_length = model.length
	ratio = length/material_length
	collar_half = width*16/30
	collar_ink_half = collar_half+surface.scale
	site_distances = [site.position/material_length*length for site in sites]
	terminal_ends = (model.ends[0] == 'telomere', model.ends[1] == 'telomere')
	left_cap, right_cap = (surface.cap_length if terminal else 0 for terminal in terminal_ends)
	mark_half = _JUNCTION_HALF_SPAN*surface.scale
	inset_outline = width*2/30
	left_clearance = max(left_cap, inset_outline)+mark_half
	right_clearance = max(right_cap, inset_outline)+mark_half
	distances = [region.start/material_length*length for region in regions] + [length]
	joins = set(model.junctions)
	junctions = tuple(index for index, region in enumerate(regions) if region.start in joins
		and left_clearance <= distances[index] <= length-right_clearance
		and _junction_clears_collars(surface, distances[index], site_distances, outward))
	junction_distances = [distances[index] for index in junctions]
	segments = []
	for region in regions:
		key = (region.source_id, region.region_id)
		if key not in palette:
			raise ValueError(f'Missing palette color for source region {key!r}')
		label = '/'.join(urllib.parse.quote(value, safe='') for value in key)
		segments.append(Segment(label, palette[key], region.stop-region.start))
	gene_positions = [length if gene.position == material_length else gene.position*ratio for gene in genes]
	locus_ids = [gene.locus_id for gene in genes]
	loci = []
	external = []
	for index, (gene, position) in enumerate(zip(genes, gene_positions)):
		left = gene_positions[index-1] if index > 0 else -math.inf
		right = gene_positions[index+1] if index+1 < len(genes) else math.inf
		clearance = min(position, length-position,
			*(abs(position-site)-collar_ink_half for site in site_distances),
			*(abs(position-junction)-mark_half for junction in junction_distances))
		block_length = min(width*.8, 2*clearance, position-left, right-position)
		locus_name = f'{name}-gene-{index}'
		locus = None
		if block_length >= width*.4:
			block = Segment(gene.allele, _GENE_CARD_COLOR, block_length)
			locus = svg_tools.chromosome_loci.card(locus_name, surface, position,
				block.label, block.color, block.length, minimum_size=width*.4,
				terminal_ends=terminal_ends)
		layer = loci
		if locus is None:
			locus = svg_tools.chromosome_loci.external(locus_name, surface, position, gene.allele, outward)
			layer = external
		key = '/'.join(urllib.parse.quote(value, safe='')
			for value in (gene.source_id, gene.copy_id, gene.locus_id))
		point = surface.path.point(surface.path.ilength(position))
		anchor = (point.real, point.imag)
		anchors = {f'gene:{key}': anchor}
		if locus_ids.count(gene.locus_id) == 1:
			anchors[f'gene_{gene.locus_id}'] = anchor
		layer.append(dataclasses.replace(locus, anchors=anchors))
	paint_sites = [(distance, True, centromere_styles.get((site.source_id, site.id)))
		for distance, site in zip(site_distances, sites)]
	part = _paint_chromatid(name, segments, surface, distances, paint_sites, terminal_ends=terminal_ends,
		junctions=junctions, loci=tuple(loci), draw_centromeres=not outward)
	bounds = part.bounds
	if not outward:
		# The rounded rectangle is an inset rectangle plus the corner and stroke radii.
		radius = 4*surface.scale
		along, across = collar_half-radius, width*1.3/2-radius
		margin = radius+surface.scale
		for index, distance in enumerate(site_distances):
			x, y = part.anchors[f'centromere_{index}']
			tangent = surface.path.unit_tangent(surface.path.ilength(distance))
			dx, dy = abs(tangent.real), abs(tangent.imag)
			half_x = dx*along+dy*across+margin
			half_y = dy*along+dx*across+margin
			bounds = svg_tools.parts.union_bounds(bounds, (x-half_x, y-half_y, x+half_x, y+half_y))
	center = surface.path.point(surface.path.ilength(length/2))
	anchors = {**part.anchors, 'center': (center.real, center.imag)}
	for locus in external:
		anchors.update(locus.anchors)
	part = dataclasses.replace(part, bounds=bounds, anchors=anchors)
	return part, external


#============================================
def _with_external_loci(part: svg_tools.parts.SvgPart,
	loci: list[svg_tools.parts.SvgPart]) -> svg_tools.parts.SvgPart:
	"""Overlay locus annotations on the completed body, including any sister belt."""
	if not loci:
		return part
	group = svg_tools._xml.parse(part.fragment)
	for locus in loci:
		group.append(svg_tools._xml.parse(locus.fragment))
	fragment = lxml.etree.tostring(group, encoding='ascii', xml_declaration=False).decode('ascii')
	bounds = svg_tools.parts.union_bounds(part.bounds, *(locus.bounds for locus in loci))
	return dataclasses.replace(part, fragment=fragment, bounds=bounds)


#============================================
def render(name: str, model: svg_tools.chromosome_topology.Chromatid | svg_tools.chromosome_topology.SisterPair, *,
	points: collections.abc.Sequence[tuple[float, float]], width: float = 20,
	scale: float = 1, palette: dict[tuple[str, str], str],
	centromere_styles: dict[tuple[str, str], CentromereStyle] | None = None) -> svg_tools.parts.SvgPart:
	"""Render source material along a spline, at display length model.length*scale.
	Anchors include start, end, center (arc midpoint), and active centromere sites.
	Locus anchors use gene_<locus_id> when unique and always gene:source/copy/locus
	with URL-encoded components. Pairs qualify child anchors with first. and second.
	Gene cards leave one cap-length of body color at each telomere. Loci with
	insufficient room for a card receive a linked external label.
	Centromere styles are keyed by (source_id, site_id), including for shared sister belts.
	"""
	if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.-]*', name):
		raise ValueError('Use an XML-safe unique namespace')
	if not _positive(width) or not _positive(scale) or not isinstance(palette, dict):
		raise ValueError('Supply finite positive width and scale and a source-region palette')
	topology = svg_tools.chromosome_topology
	paired = isinstance(model, topology.SisterPair)
	first = model.first if paired else model
	if not isinstance(first, topology.Chromatid):
		raise ValueError('Supply a Chromatid or SisterPair')
	if paired:
		second = model.second
		# Cutting and rejoining the same material can round its projected distances differently.
		material_tolerance = 2 * math.ulp(first.length)
		if not isinstance(second, topology.Chromatid) or abs(first.length-second.length) > material_tolerance:
			raise ValueError('Sisters must be chromatids of equal material length')
		if {span.copy_id for span in first.spans} & {span.copy_id for span in second.spans}:
			raise ValueError('Sisters must have distinct copy IDs')
	path = svg_tools.chromosome_surface.centerline(points, length=first.length*scale, width=width)
	if path.isclosed():
		raise ValueError('Chromatid poses require an open centerline')
	surface = svg_tools.chromosome_surface.Surface(path, width)
	first_sites = tuple(site for site in topology.project_centromeres(first) if site.active)
	offset = 0j
	if paired:
		second_sites = tuple(site for site in topology.project_centromeres(second) if site.active)
		if len(first_sites) != 1 or len(second_sites) != 1:
			raise ValueError('Automatic sister poses need one active centromere on each chromatid')
		left, right = first_sites[0], second_sites[0]
		if ((left.source_id, left.id) != (right.source_id, right.id)
			or abs(left.position-right.position) > material_tolerance):
			raise ValueError('Sisters need corresponding active centromeres at the same position')
		parameter = surface.path.ilength(left.position/first.length*surface.length)
		offset = surface.path.unit_tangent(parameter)*1j*(width*.6)
	first_name = f'{name}-first' if paired else name
	styles = centromere_styles or {}
	first_part, first_external = _render_topology_chromatid(first_name, first, surface, palette,
		sites=first_sites, centromere_styles=styles, outward=-offset)
	if not paired:
		return _with_external_loci(first_part, first_external)
	second_part, second_external = _render_topology_chromatid(f'{name}-second', second, surface,
		palette, sites=second_sites, centromere_styles=styles, outward=offset)
	first_sister = svg_tools.parts.transform(first_part, x=-offset.real, y=-offset.imag)
	second_sister = svg_tools.parts.transform(second_part, x=offset.real, y=offset.imag)
	belt = _sister_belt_part(f'{name}-belt', first_sister.anchors['centromere'],
		second_sister.anchors['centromere'], width, style=styles.get((left.source_id, left.id)))
	part = svg_tools.parts.group({'first': first_sister, 'second': second_sister, 'belt': belt})
	anchors = {key: first_part.anchors[key] for key in ('start', 'end', 'center', 'centromere')}
	part = dataclasses.replace(part, anchors={**part.anchors, **anchors})
	external = [svg_tools.parts.transform(locus, x=-offset.real, y=-offset.imag)
		for locus in first_external]
	external.extend(svg_tools.parts.transform(locus, x=offset.real, y=offset.imag)
		for locus in second_external)
	return _with_external_loci(part, external)
