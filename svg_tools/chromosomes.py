"""Editable schematic chromosomes, joined sisters and bounded segment rearrangements."""

import re
import math
import pathlib
import dataclasses
import xml.etree.ElementTree

import svgpathtools

import svg_tools.parts


_BANDS = (((.13, .045),), ((.84, .035),), ((.10, .025), (.89, .055)),
	((.79, .045),), ((.18, .035),))


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
	"""An immutable schematic region; band identity follows this region."""

	label: str
	color: str
	length: float = 64
	band: int = 0

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
		if type(self.band) is not int or not 0 <= self.band < len(_BANDS):
			raise ValueError("Band index must identify a supported pattern")


#============================================
@dataclasses.dataclass(frozen=True)
class Chromosome:
	"""Ordered regions and an optional internal centromere boundary."""

	segments: tuple[Segment, ...]
	centromere_after: int | None = None

	def __post_init__(self) -> None:
		object.__setattr__(self, "segments", tuple(self.segments))
		if not self.segments or not all(isinstance(segment, Segment) for segment in self.segments):
			raise ValueError("Supply nonempty Segment values")
		if not math.isfinite(sum(segment.length for segment in self.segments)):
			raise ValueError("Total segment length must be finite")
		c = self.centromere_after
		if c is not None and (type(c) is not int or not 0 < c < len(self.segments)):
			raise ValueError("Centromere must lie between regions")


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
	model = Chromosome(tuple(record.segment for record in records), acen[1])
	return model, tuple(records)


#============================================
def delete_segments(chromosome: Chromosome, start: int, stop: int) -> Chromosome:
	"""Remove an internal half-open range within one arm, retaining segment identity."""
	if type(start) is not int or type(stop) is not int or not 0 < start < stop < len(chromosome.segments):
		raise ValueError("Deletion must be a nonempty internal segment range")
	c = chromosome.centromere_after
	if c is not None:
		if start < c < stop:
			raise ValueError("Deletion cannot cross the centromere")
		if stop <= c:
			c -= stop - start
	result = Chromosome(chromosome.segments[:start] + chromosome.segments[stop:], c)
	return result


#============================================
def reciprocal_translocation(left: Chromosome, left_cut: int,
	right: Chromosome, right_cut: int) -> tuple[Chromosome, Chromosome]:
	"""Exchange ordered right tails distal to each known centromere."""
	for parent, cut in ((left, left_cut), (right, right_cut)):
		if (parent.centromere_after is None or type(cut) is not int
			or not parent.centromere_after < cut < len(parent.segments)):
			raise ValueError("Tail cuts must be internal and distal to a known centromere")
	products = (Chromosome(left.segments[:left_cut] + right.segments[right_cut:], left.centromere_after),
		Chromosome(right.segments[:right_cut] + left.segments[left_cut:], right.centromere_after))
	return products


#============================================
def render_chromosome(name: str, chromosome: Chromosome, *, width: float | None = None,
	height: float = 62, bands: bool = True, sisters: bool = False,
	junctions: tuple[int, ...] = (), allele_labels: bool = False) -> tuple[str, float, list[float]]:
	"""Return live SVG, complete outline width and actual inter-region x coordinates.

	Height covers the complete sister pair. Short labels are recommended; width fitting
	is approximate. Explicit width scales geometry, never the text glyphs.
	"""
	layout = _render(name, chromosome, width=width, height=height, bands=bands,
		sisters=sisters, junctions=junctions, allele_labels=allele_labels)
	result = (layout.svg, layout.width, [point[0] for point in layout.boundaries])
	return result


#============================================
def chromosome_svg(name: str, genes: list[tuple[str, str]], *,
	centromere_after: int | None = None, junctions: tuple[int, ...] = (),
	pitch: float = 64, height: float = 62,
	allele_labels: bool = False) -> tuple[str, float, list[float]]:
	"""Compatibility entry for equal-width regions with neutral terminal caps."""
	chromosome = Chromosome(tuple(Segment(label, color, pitch, index % len(_BANDS))
		for index, (label, color) in enumerate(genes)), centromere_after)
	layout = _render(name, chromosome, height=height, junctions=junctions,
		allele_labels=allele_labels, neutral_caps=True)
	result = (layout.svg, layout.width, [point[0] for point in layout.boundaries])
	return result


#============================================
def render_chromosome_layout(name: str, chromosome: Chromosome, *,
	length: float | None = None, thickness: float = 62,
	orientation: str = 'horizontal', bands: bool = True, sisters: bool = False,
	junctions: tuple[int, ...] = (), allele_labels: bool = False, labels: bool = True,
	marker_size: tuple[float, float] | None = None,
	marker_label: str | None = None) -> ChromosomeLayout:
	"""Return explicit page-coordinate geometry and upright live labels.

	Length is longitudinal and thickness transverse, including the marker but not
	stroke. Portrait places the first region at the top. Segment bounds enclose
	paint conservatively across the entire transverse envelope, for annotations.
	Marker bounds expose exterior edge midpoints; label fit is approximate.
	"""
	result = _render(name, chromosome, width=length, height=thickness, bands=bands,
		sisters=sisters, junctions=junctions, allele_labels=allele_labels,
		orientation=orientation, labels=labels, marker_size=marker_size,
		marker_label=marker_label, broad_marker=True)
	return result


#============================================
def _sister_contour(width: float, height: float, center: float,
	copy: int) -> tuple[str, tuple]:
	"""Map the approved original curved concept, stretching each arm independently."""
	original = (
		((-120, -175), (-120, -222), (-50, -222), (-50, -175)),
		((-50, -175), (-50, -110), (-20, -65), (18, -20)),
		((18, -20), (55, 25), (135, 155), (135, 245)),
		((135, 245), (135, 292), (65, 292), (65, 245)),
		((65, 245), (65, 170), (20, 65), (-18, 20)),
		((-18, 20), (-65, -25), (-120, -105), (-120, -175)),
	)
	# Preserve the concept's control points while scaling the unequal p/q spans.
	curves = []
	for curve in original:
		mapped = []
		for transverse, longitudinal in curve:
			x = center + longitudinal * (center/210.25 if longitudinal < 0 else (width-center)/280.25)
			y = (transverse+135)/270
			mapped.append((x, height*(1-y if copy else y)))
		curves.append(tuple(mapped))
	path = f"M {curves[0][0][0]} {curves[0][0][1]}"
	for curve in curves:
		path += " C " + " ".join(f"{x} {y}" for x, y in curve[1:])
	path += " Z"
	return path, tuple(curves)


#============================================
def _sister_center(x: float, edges: tuple) -> float:
	"""Find the center of the painted cross-section on the actual curved outline."""
	values = []
	for curve in edges:
		# Each cap has one turning point at t=.5; other edges are longitudinally monotone.
		intervals = ((0.0, .5), (.5, 1.0)) if curve[0][0] == curve[-1][0] else ((0.0, 1.0),)
		def coordinate(t: float, axis: int) -> float:
			weights = ((1-t)**3, 3*(1-t)**2*t, 3*(1-t)*t*t, t**3)
			return sum(p[axis]*weight for p, weight in zip(curve, weights))
		for low, high in intervals:
			first, last = coordinate(low, 0), coordinate(high, 0)
			if not min(first, last) <= x <= max(first, last):
				continue
			for _ in range(35):
				t = (low+high)/2
				if (coordinate(t, 0) < x) == (first < last):
					low = t
				else:
					high = t
			values.append(coordinate((low+high)/2, 1))
	if not values:
		raise ValueError("No chromatid cross-section at requested coordinate")
	return (min(values)+max(values))/2


#============================================
def _render(name: str, chromosome: Chromosome, *, width: float | None = None,
	height: float = 62, bands: bool = True, sisters: bool = False,
	junctions: tuple[int, ...] = (), allele_labels: bool = False,
	neutral_caps: bool = False, orientation: str = 'horizontal', labels: bool = True,
	marker_size: tuple[float, float] | None = None, marker_label: str | None = None,
	broad_marker: bool = False) -> ChromosomeLayout:
	"""Shared paint engine for legacy rods and segment-based chromosomes."""
	if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.-]*", name):
		raise ValueError("Use an XML-safe unique namespace")
	if not _positive(height) or width is not None and not _positive(width):
		raise ValueError("Supply finite positive geometry")
	if orientation not in ('horizontal', 'vertical'):
		raise ValueError('Orientation must be horizontal or vertical')
	if chromosome.centromere_after is None and (marker_size is not None or marker_label is not None):
		raise ValueError('Marker settings require a centromere')
	if marker_label is not None:
		Segment(marker_label, '#FFFFFF')
	if sisters and chromosome.centromere_after is None:
		raise ValueError("Sisters require a centromere")
	genes = [(segment.label, segment.color) for segment in chromosome.segments]
	centromere_after = chromosome.centromere_after
	if allele_labels and any(label and not re.fullmatch(r"[a-z][+-]", label)
		for label, _ in genes):
		raise ValueError("Allele labels need one lowercase letter and +/- or an empty label")
	indices = list(junctions)
	if centromere_after is not None:
		indices.append(centromere_after)
	if any(type(index) is not int or not 0 < index < len(genes) for index in indices):
		raise ValueError("Collars and joins must lie between regions")
	if len(set(junctions)) != len(junctions) or centromere_after in junctions:
		raise ValueError("Joins must be distinct from each other and the centromere")
	wide_marker = centromere_after is not None and (broad_marker or sisters)
	body_height = height * (.26 if sisters else .61 if wide_marker else 1)
	cap = body_height * .24
	collar = body_height * .48 if centromere_after is not None else 0
	natural_width = 2 * cap + sum(segment.length for segment in chromosome.segments) + collar
	if not math.isfinite(natural_width):
		raise ValueError("Rod width must be finite")
	scale = 1 if width is None else width / natural_width
	width = natural_width if width is None else width
	cap *= scale
	collar *= scale
	lengths = [segment.length * scale for segment in chromosome.segments]
	if broad_marker or sisters:
		# Caps and collars are drawing units, independent of the source interval units.
		cap = min(body_height*.5, width*.08)
		collar = min(body_height*.48, width*.06) if centromere_after is not None else 0
		data_scale = (width-2*cap-collar) / sum(segment.length for segment in chromosome.segments)
		lengths = [segment.length*data_scale for segment in chromosome.segments]
	if not all(_positive(length) for length in lengths):
		raise ValueError("Scaled segment lengths must remain finite and positive")
	starts = []
	x = cap
	for index, length in enumerate(lengths):
		if index == centromere_after:
			x += collar
		starts.append(x)
		x += length
	boundary = starts + [x]
	if centromere_after is not None:
		boundary[centromere_after] -= collar / 2
	if not all(0 < a < b < width for a, b in zip(boundary, boundary[1:])):
		raise ValueError("Geometry must retain distinct finite segment boundaries")
	group = xml.etree.ElementTree.Element("g", {"id": name})
	anchors = []
	def point(x: float, y: float) -> tuple[float, float]:
		return (y, x) if orientation == 'vertical' else (x, y)
	def bounds(x0: float, y0: float, x1: float, y1: float) -> tuple[float, float, float, float]:
		return (*point(x0, y0), *point(x1, y1))
	for copy in range(2 if sisters else 1):
		instance = f"{name}-sister-{copy}" if sisters else name
		defs = xml.etree.ElementTree.SubElement(group, "defs")
		clip = xml.etree.ElementTree.SubElement(defs, "clipPath", {"id": f"{instance}-clip"})
		radius = min(body_height * .32 * (1 if broad_marker or sisters else scale),
			cap + min(lengths) / 2)
		if sisters:
			cx = boundary[centromere_after]
			top, edges = _sister_contour(width, height, cx, copy)
			bottom = ''
		else:
			top = f"M {radius} 0"
			bottom = f"L {width-radius} {height}"
			if centromere_after is not None:
				x = boundary[centromere_after] - collar / 2
				top += f" H {x} Q {x+collar/2} {height*.25} {x+collar} 0"
				bottom += f" H {x+collar} Q {x+collar/2} {height*.75} {x} {height}"
			top += f" H {width-radius} Q {width} 0 {width} {body_height * .32}"
			top += f" V {height-body_height * .32} Q {width} {height} {width-radius} {height}"
			bottom += f" H {radius} Q 0 {height} 0 {height-body_height * .32} V {body_height * .32} Q 0 0 {radius} 0 Z"
			if broad_marker:
				# New layouts use full rounded terminal caps, including genomic-scale maps.
				top = f'M {cap} 0'
				bottom = f'L {width-cap} {height}'
				if centromere_after is not None:
					x = boundary[centromere_after]-collar/2
					top += f' H {x} Q {x+collar/2} {height*.5} {x+collar} 0'
					bottom += f' H {x+collar} Q {x+collar/2} {height*.5} {x} {height}'
				top += f' H {width-cap} Q {width} 0 {width} {height/2}'
				top += f' Q {width} {height} {width-cap} {height}'
				bottom += f' H {cap} Q 0 {height} 0 {height/2} Q 0 0 {cap} 0 Z'
		outline = {"d": top + bottom}
		if wide_marker and not sisters:
			# Reserve transverse space for the broad oval, keeping a narrower rod beneath.
			outline['transform'] = f'translate(0 {(height-body_height)/2}) scale(1 {body_height/height})'
		xml.etree.ElementTree.SubElement(clip, "path", outline)
		paint = xml.etree.ElementTree.SubElement(group, "g", {"clip-path": f"url(#{instance}-clip)"})
		xml.etree.ElementTree.SubElement(paint, "path", dict(outline, fill="#98A2AD" if neutral_caps else genes[0][1]))
		if not neutral_caps:
			xml.etree.ElementTree.SubElement(paint, "rect", {
				"x": str(starts[-1]), "y": "0", "width": str(width-starts[-1]),
				"height": str(height), "fill": genes[-1][1],
			})
		for index, (label, fill) in enumerate(genes):
			x = starts[index]
			pitch = lengths[index]
			region = xml.etree.ElementTree.SubElement(paint, "g", {"id": f"{instance}-region-{index}"})
			xml.etree.ElementTree.SubElement(region, "rect", {
				"x": str(x), "y": "0", "width": str(pitch), "height": str(height), "fill": fill,
			})
			# Sparse end stripes leave the live labels clear; these are not measured G-bands.
			for offset, thickness in _BANDS[chromosome.segments[index].band] if bands else ():
				xml.etree.ElementTree.SubElement(region, "path", {
					"d": f"M {x + pitch * offset} 0 l {-body_height * .055 * scale} {height}",
					"stroke": "#213547", "stroke-opacity": ".09",
					"stroke-width": str(pitch * thickness),
				})
			local_height = body_height
			middle = height/2
			start_y = end_y = middle
			if sisters:
				middle = _sister_center(x+pitch/2, edges)
				start_y = _sister_center(x, edges)
				end_y = _sister_center(x+pitch, edges)
			anchors.append(SegmentAnchor(chromosome.segments[index], copy,
				point(x, start_y), point(x+pitch, end_y), bounds(x, 0, x+pitch, height)))
			if not labels:
				continue
			label_units = 1.35 if allele_labels else max(1, len(label))
			font_size = min(local_height * .59, pitch * .82 / label_units / .65)
			if orientation == 'vertical':
				font_size = min(local_height*.82 / label_units / .65, pitch*.59)
			label_x, label_y = point(x+pitch/2, middle)
			label_y += font_size * (.2 / .59)
			ink = _label_color(fill)
			text = xml.etree.ElementTree.SubElement(region, "text", {
				"x": str(label_x), "y": str(label_y),
				"font-family": "Atkinson Hyperlegible Next", "font-size": str(font_size),
				"font-weight": "600", "text-anchor": "middle", "fill": ink,
			})
			if allele_labels and label:
				xml.etree.ElementTree.SubElement(text, "tspan", {"font-style": "italic"}).text = label[0]
				xml.etree.ElementTree.SubElement(text, "tspan", {
					"dx": str(font_size * .07 / .59), "dy": str(-font_size * .22 / .59),
					"font-size": str(font_size * .40 / .59),
				}).text = "+" if label[1] == "+" else "\u2212"
			else:
				text.text = label
		for index in junctions:
			x = boundary[index]
			points = [(x + (height * .035 if step % 2 else -height * .035), height * step / 6)
				for step in range(7)]
			xml.etree.ElementTree.SubElement(paint, "polyline", {
				"id": f"{instance}-join-{index}", "points": " ".join(f"{x},{y}" for x, y in points),
				"fill": "none", "stroke": "#FFFFFF", "stroke-width": str(height * .065),
			})
		xml.etree.ElementTree.SubElement(group, "path", dict(
			outline, fill="none", stroke="#344651", **{"stroke-width": str(body_height * .035)}))
	center = None
	marker_bounds = None
	if centromere_after is not None:
		x = boundary[centromere_after] - collar / 2
		cx = boundary[centromere_after]
		center = point(cx, height/2)
		# A pale collar narrows the rod while remaining visibly connected to both arms.
		if wide_marker:
			along, across = (height*.23, height*.43) if sisters else (height*.54, height)
			along = min(along, 2*cx, 2*(width-cx))
			if marker_size is not None:
				if len(marker_size) != 2 or not all(_positive(v) for v in marker_size):
					raise ValueError('Marker size must contain two finite positive lengths')
				along, across = marker_size
			if across <= body_height or across > height or along > 2*min(cx, width-cx):
				raise ValueError('Marker must fit the envelope and exceed the adjacent chromatid width')
			marker_bounds = bounds(cx-along/2, (height-across)/2,
				cx+along/2, (height+across)/2)
			xml.etree.ElementTree.SubElement(group, 'ellipse', {
				'id': f'{name}-centromere', 'cx': str(cx), 'cy': str(height/2),
				'rx': str(along/2), 'ry': str(across/2), 'fill': 'none',
				'stroke': '#72508C', 'stroke-width': str(body_height*.045),
			})
			if marker_label is not None:
				text_width, text_height = (across, along) if orientation == 'vertical' else (along, across)
				font_size = min(text_height*.65, text_width*.8/max(1, len(marker_label))/.60)
				xml.etree.ElementTree.SubElement(group, 'text', {
					'x': str(center[0]), 'y': str(center[1]+font_size*.34),
					'font-family': 'Atkinson Hyperlegible Next', 'font-size': str(font_size),
					'text-anchor': 'middle', 'fill': '#172B3A',
				}).text = marker_label
		else:
			path = f"M {x} 0 Q {x + collar/2} {height*.25} {x+collar} 0"
			path += f" L {x+collar} {height} Q {x+collar/2} {height*.75} {x} {height} Z"
			xml.etree.ElementTree.SubElement(group, "path", {
				"id": f"{name}-centromere", "d": path, "fill": "#EEF1F4",
				"stroke": "#344651", "stroke-width": str(body_height * .035),
			})
			marker_bounds = bounds(x, 0, x+collar, height)
	if orientation == 'vertical':
		for node in group.iter():
			if node.tag in ('path', 'rect', 'ellipse', 'polyline'):
				node.set('transform', 'matrix(0 1 1 0 0 0) ' + node.attrib.get('transform', ''))
	fragment = xml.etree.ElementTree.tostring(
		group, encoding="ascii", xml_declaration=False).decode("ascii")
	final_width, final_height = (height, width) if orientation == 'vertical' else (width, height)
	result = ChromosomeLayout(fragment, final_width, final_height,
		tuple(point(x, height/2) for x in boundary), tuple(anchors), center, marker_bounds)
	return result


#============================================
def centromere_part(name: str, *, thickness: float = 62) -> svg_tools.parts.SvgPart:
	"""Hollow marker centered at the origin; thickness is the adjacent chromatid width.

	The chromosome's axis is horizontal. Cardinal anchors lie on the ellipse,
	while bounds include its stroke. Rotate and translate to place the marker.
	"""
	if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.-]*', name):
		raise ValueError('Use an XML-safe unique namespace')
	if not _positive(thickness):
		raise ValueError('Supply a finite positive thickness')
	rx, ry, stroke = thickness*.54/.61/2, thickness/.61/2, thickness*.045
	marker = xml.etree.ElementTree.Element('ellipse', {'id': f'{name}-centromere',
		'cx': '0', 'cy': '0', 'rx': str(rx), 'ry': str(ry),
		'fill': 'none', 'stroke': '#72508C', 'stroke-width': str(stroke)})
	fragment = xml.etree.ElementTree.tostring(marker, encoding='ascii').decode('ascii')
	margin = stroke/2
	return svg_tools.parts.SvgPart(fragment, (-rx-margin, -ry-margin, rx+margin, ry+margin),
		{'center': (0, 0), 'left': (-rx, 0), 'right': (rx, 0),
			'top': (0, -ry), 'bottom': (0, ry)})


#============================================
def chromosome_part(name: str, chromosome: Chromosome, *,
	length: float | None = None, thickness: float = 62,
	orientation: str = 'horizontal', bands: bool = True, sisters: bool = False,
	junctions: tuple[int, ...] = (), allele_labels: bool = False, labels: bool = True,
	marker_size: tuple[float, float] | None = None,
	marker_label: str | None = None) -> svg_tools.parts.SvgPart:
	"""Render a local part with start, end, center, boundary_N and centromere anchors."""
	layout = render_chromosome_layout(name, chromosome, length=length, thickness=thickness,
		orientation=orientation, bands=bands, sisters=sisters, junctions=junctions,
		allele_labels=allele_labels, labels=labels, marker_size=marker_size,
		marker_label=marker_label)
	margin = thickness * .035 / 2
	bounds = (-margin, -margin, layout.width+margin, layout.height+margin)
	bounds = svg_tools.parts.include_text_bounds(layout.svg, bounds)
	anchors = {f'boundary_{index}': point for index, point in enumerate(layout.boundaries)}
	anchors['start'], anchors['end'] = layout.boundaries[0], layout.boundaries[-1]
	anchors['center'] = (layout.width/2, layout.height/2)
	if layout.centromere is not None:
		anchors['centromere'] = layout.centromere
	part = svg_tools.parts.SvgPart(layout.svg, bounds, anchors)
	return part


#============================================
def _neck_envelope(path: svgpathtools.Path, thickness: float,
	centromere_distance: float, cut_ends: bool) -> str:
	"""Offset a sampled centerline only where a short centromere neck needs varying width."""
	length = path.length()
	count = max(24, math.ceil(length / (thickness * .08)))
	distances = {length * index/count for index in range(count+1)}
	neck = min(thickness * .45, centromere_distance, length-centromere_distance)
	distances.update(centromere_distance + neck * step/12 for step in range(-12, 13))
	sides = [[], []]
	for distance in sorted(distances):
		parameter = path.ilength(distance) if 0 < distance < length else (0.0 if distance <= 0 else 1.0)
		center = path.point(parameter)
		normal = path.unit_tangent(parameter) * 1j
		ratio = min(1.0, abs(distance-centromere_distance)/neck)
		radius = thickness/2 * (.40 + .60*(.5-.5*math.cos(math.pi*ratio)))
		for side, sign in zip(sides, (1, -1)):
			side.append(center + sign*normal*radius)
	def coordinates(point: complex) -> str:
		return f'{point.real} {point.imag}'
	outline = 'M ' + coordinates(sides[0][0])
	outline += ''.join(' L ' + coordinates(point) for point in sides[0][1:])
	if cut_ends:
		outline += ' L ' + coordinates(sides[1][-1])
	else:
		outline += f' A {thickness/2} {thickness/2} 0 0 0 ' + coordinates(sides[1][-1])
	outline += ''.join(' L ' + coordinates(point) for point in reversed(sides[1][:-1]))
	if not cut_ends:
		outline += f' A {thickness/2} {thickness/2} 0 0 0 ' + coordinates(sides[0][0])
	outline += ' Z'
	return outline


#============================================
def chromosome_path_part(name: str, chromosome: Chromosome, path_d: str, *,
	thickness: float = 28, closed: bool = False, cut_ends: bool = False,
	labels: bool = True) -> svg_tools.parts.SvgPart:
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
	if closed and (cut_ends or chromosome.centromere_after is not None):
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
	stroke = thickness * .035
	linecap = 'butt' if cut_ends or closed else 'round'
	center_index = chromosome.centromere_after
	paint = group
	if center_index is not None:
		envelope = _neck_envelope(path, thickness, distances[center_index], cut_ends)
		defs = xml.etree.ElementTree.SubElement(group, 'defs')
		clip = xml.etree.ElementTree.SubElement(defs, 'clipPath', {'id': f'{name}-clip'})
		xml.etree.ElementTree.SubElement(clip, 'path', {'d': envelope})
		xml.etree.ElementTree.SubElement(group, 'path', {'d': envelope,
			'fill': chromosome.segments[0].color, 'stroke': '#344651',
			'stroke-width': str(stroke), 'stroke-linejoin': 'round'})
		paint = xml.etree.ElementTree.SubElement(group, 'g', {'clip-path': f'url(#{name}-clip)'})
	else:
		xml.etree.ElementTree.SubElement(group, 'path', {'d': path_text, 'fill': 'none',
			'stroke': '#344651', 'stroke-width': str(thickness+stroke),
			'stroke-linecap': linecap, 'stroke-linejoin': 'round'})
		xml.etree.ElementTree.SubElement(group, 'path', {'d': path_text, 'fill': 'none',
			'stroke': chromosome.segments[0].color, 'stroke-width': str(thickness),
			'stroke-linecap': linecap, 'stroke-linejoin': 'round'})
	for index, segment in enumerate(chromosome.segments):
		region = xml.etree.ElementTree.SubElement(paint, 'g', {
			'id': f'{name}-region-{index}', 'data-source-label': segment.label})
		portion = path.cropped(parameters[index], parameters[index+1])
		xml.etree.ElementTree.SubElement(region, 'path', {'d': portion.d(), 'fill': 'none',
			'stroke': segment.color, 'stroke-width': str(thickness),
			'stroke-linecap': 'butt', 'stroke-linejoin': 'round'})
		middle = path.ilength((distances[index]+distances[index+1])/2)
		anchors[f'segment_{index}'] = point(middle)
	if not closed and not cut_ends:
		for parameter, segment in ((0.0, chromosome.segments[0]), (1.0, chromosome.segments[-1])):
			x, y = point(parameter)
			xml.etree.ElementTree.SubElement(paint, 'circle', {'cx': str(x), 'cy': str(y),
				'r': str(thickness/2), 'fill': segment.color})
	if center_index is not None:
		cx, cy = anchors[f'boundary_{center_index}']
		anchors['centromere'] = (cx, cy)
		tangent = path.unit_tangent(parameters[center_index])
		angle = math.degrees(math.atan2(tangent.imag, tangent.real))
		xml.etree.ElementTree.SubElement(group, 'ellipse', {'id': f'{name}-centromere',
			'cx': str(cx), 'cy': str(cy), 'rx': str(thickness*.54/.61/2),
			'ry': str(thickness/.61/2), 'transform': f'rotate({angle} {cx} {cy})',
			'fill': 'none', 'stroke': '#72508C', 'stroke-width': str(thickness*.045)})
	if labels:
		for index, segment in enumerate(chromosome.segments):
			x, y = anchors[f'segment_{index}']
			size = min(thickness*.59,
				(distances[index+1]-distances[index])*.82/max(1, len(segment.label))/.65)
			xml.etree.ElementTree.SubElement(group, 'text', {'x': str(x), 'y': str(y+size*.34),
				'font-family': 'Atkinson Hyperlegible Next', 'font-size': str(size),
				'font-weight': '600', 'text-anchor': 'middle', 'fill': _label_color(segment.color)}).text = segment.label
	fragment = xml.etree.ElementTree.tostring(group, encoding='ascii', xml_declaration=False).decode('ascii')
	xmin, xmax, ymin, ymax = path.bbox()
	margin = thickness/2 + stroke
	if center_index is not None:
		margin = thickness/.61/2 + thickness*.045
	anchors['center'] = ((xmin+xmax)/2, (ymin+ymax)/2)
	bounds = svg_tools.parts.include_text_bounds(fragment,
		(xmin-margin, ymin-margin, xmax+margin, ymax+margin))
	part = svg_tools.parts.SvgPart(fragment, bounds, anchors)
	return part
