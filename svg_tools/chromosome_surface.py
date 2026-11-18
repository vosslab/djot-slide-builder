"""Build SVG centerlines and map BPQ paint onto their surfaces."""

import math
import bisect
import collections.abc

import lxml.etree
import svgpathtools


# BPQ translocationlib.py: dimensions at CHROMOSOME_HEIGHT=30, not fixed pixels.
REFERENCE_HEIGHT = 30
TEXTURE_STOPS = ((5, 7, 8), (18, 21, 22), (29, 30, 31),
	(46, 48, 49), (59, 62, 63))


#============================================
def _validate_spline_segment(segment: svgpathtools.CubicBezier, width: float) -> None:
	"""Check forward progress and the local curvature limit for a swept ribbon."""
	local = segment.translated(-segment.start)
	velocity = local.poly().deriv()
	forward = svgpathtools.real(velocity * local.end.conjugate())
	progress_checks = [0, 1, *svgpathtools.polyroots01(forward.deriv())]
	if min(forward(t) for t in progress_checks) <= 0:
		raise ValueError('Spline has a stationary or reversing span')
	dx, dy = svgpathtools.real(velocity), svgpathtools.imag(velocity)
	speed_squared = dx*dx + dy*dy
	cross = dx*dy.deriv() - dy*dx.deriv()
	# Signed curvature is cross/speed_squared**(3/2). Check its extrema and endpoints.
	curvature_extrema = 2*cross.deriv()*speed_squared - 3*cross*speed_squared.deriv()
	bend_checks = [0, 1, *svgpathtools.polyroots01(curvature_extrema)]
	if any(local.curvature(t) * (width/2) >= 1 for t in bend_checks):
		raise ValueError('Spline bend would fold the surface at this width')


#============================================
def centerline(points: collections.abc.Sequence[tuple[float, float]], *, length: float,
	width: float) -> svgpathtools.Path:
	"""Fit an open centripetal Catmull-Rom spline to SVG shape points.

	Scale uniformly about the first point to the requested arc length. The width
	is in display units and limits local bends anywhere along the scaled curve.
	"""
	for value, name in ((length, 'length'), (width, 'width')):
		if isinstance(value, bool) or not math.isfinite(value) or value <= 0:
			raise ValueError(f'Spline {name} must be positive and finite')
	if len(points) < 2:
		raise ValueError('Spline needs at least two shape points')
	positions = [complex(x, y) for x, y in points]
	if not all(math.isfinite(point.real) and math.isfinite(point.imag) for point in positions):
		raise ValueError('Spline points must be finite')
	anchor = positions[0]
	shape = [point-anchor for point in positions]
	extent = max(math.hypot(point.real, point.imag) for point in shape)
	if not extent or not math.isfinite(extent):
		raise ValueError('Consecutive spline points must be distinct and finitely separated')
	shape = [point/extent for point in shape]
	chords = [end-start for start, end in zip(shape, shape[1:])]
	if 0 in chords:
		raise ValueError('Consecutive spline points must be distinct')
	if positions[-1] == anchor:
		raise ValueError('Spline must be open with distinct first and last points')
	if len(shape) == 2:
		segments = [svgpathtools.Line(0j, shape[1])]
	else:
		# Extrapolate one chord at each end. Centripetal knots use square-root chord lengths.
		padded = [chords[0], *chords, chords[-1]]
		intervals = [math.sqrt(abs(chord)) for chord in padded]
		tangents = [(left/h_left * h_right + right/h_right * h_left) / (h_left+h_right)
			for left, right, h_left, h_right in zip(padded, padded[1:], intervals, intervals[1:])]
		segments = []
		for index, (start, end) in enumerate(zip(shape, shape[1:])):
			handle_scale = intervals[index+1]/3
			segments.append(svgpathtools.CubicBezier(start, start+tangents[index]*handle_scale,
				end-tangents[index+1]*handle_scale, end))
	native_length = svgpathtools.Path(*segments).length()
	display_segments = []
	for segment in segments:
		controls = [anchor + point/native_length * length for point in segment.bpoints()]
		if (controls[0] == controls[-1] or not all(
			math.isfinite(point.real) and math.isfinite(point.imag) for point in controls)):
			raise ValueError('Spline length cannot be represented at this position')
		display_segment = type(segment)(*controls)
		if isinstance(display_segment, svgpathtools.CubicBezier):
			_validate_spline_segment(display_segment, width)
		display_segments.append(display_segment)
	path = svgpathtools.Path(*display_segments)
	return path


#============================================
def smooth_centerline(path: svgpathtools.Path) -> svgpathtools.Path:
	"""Return one tangent-continuous centerline without moving its joins.

	Collinear line subdivisions carry source intervals, not visible elbows, so they
	combine before the cubic join construction. Existing tangent paths are returned
	unchanged to preserve authored cubic geometry exactly.
	"""
	if len(path) < 2:
		return path
	joins = list(zip(path, path[1:]))
	if path.isclosed():
		joins.append((path[-1], path[0]))
	if all(abs(first.unit_tangent(1)-second.unit_tangent(0)) < 1e-9
		for first, second in joins):
		return path
	if path.isclosed():
		raise ValueError('A non-tangent closed centerline needs an authored curve')
	segments = []
	for segment in path:
		if (segments and isinstance(segments[-1], svgpathtools.Line)
			and isinstance(segment, svgpathtools.Line)
			and abs(segments[-1].unit_tangent(1)-segment.unit_tangent(0)) < 1e-9):
			segments[-1] = svgpathtools.Line(segments[-1].start, segment.end)
		else:
			segments.append(segment)
	joins = [(index, first, second) for index, (first, second) in
		enumerate(zip(segments, segments[1:]))
		if abs(first.unit_tangent(1)-second.unit_tangent(0)) >= 1e-9]
	if not joins:
		return svgpathtools.Path(*segments)
	corner_segments = {join[0] for join in joins} | {join[0]+1 for join in joins}
	expanded = []
	for index, segment in enumerate(segments):
		if isinstance(segment, svgpathtools.Arc) and index in corner_segments:
			expanded.extend(segment.as_cubic_curves(max(1, math.ceil(abs(segment.delta)/45))))
		else:
			expanded.append(segment)
	segments = expanded
	joins = [(index, first, second) for index, (first, second) in
		enumerate(zip(segments, segments[1:]))
		if abs(first.unit_tangent(1)-second.unit_tangent(0)) >= 1e-9]
	for _, first, second in joins:
		if not isinstance(first, (svgpathtools.Line, svgpathtools.QuadraticBezier,
			svgpathtools.CubicBezier)) or not isinstance(second, (svgpathtools.Line,
			svgpathtools.QuadraticBezier, svgpathtools.CubicBezier)):
			raise ValueError('A centerline corner needs an authored curve')
		if abs(first.unit_tangent(1)+second.unit_tangent(0)) < 1e-9:
			raise ValueError('A reversing centerline needs an authored curve')
	def cubic(segment: object) -> svgpathtools.CubicBezier:
		if isinstance(segment, svgpathtools.CubicBezier):
			return segment
		if isinstance(segment, svgpathtools.QuadraticBezier):
			return svgpathtools.CubicBezier(segment.start,
				segment.start+2*(segment.control-segment.start)/3,
				segment.end+2*(segment.control-segment.end)/3, segment.end)
		return svgpathtools.CubicBezier(segment.start,
			segment.start+(segment.end-segment.start)/3,
			segment.start+2*(segment.end-segment.start)/3, segment.end)
	corner_segments = {join[0] for join in joins} | {join[0]+1 for join in joins}
	result = [cubic(segment) if index in corner_segments else segment
		for index, segment in enumerate(segments)]
	for index, first, second in joins:
		tangent = first.unit_tangent(1)+second.unit_tangent(0)
		tangent /= abs(tangent)
		previous, following = result[index], result[index+1]
		previous_handle = abs(previous.end-previous.control2)
		following_handle = abs(following.control1-following.start)
		result[index] = svgpathtools.CubicBezier(previous.start, previous.control1,
			previous.end-previous_handle*tangent, previous.end)
		result[index+1] = svgpathtools.CubicBezier(following.start,
			following.start+following_handle*tangent, following.control2, following.end)
	return svgpathtools.Path(*result)


def nearest_distance(path: svgpathtools.Path, point: complex) -> float:
	"""Locate a source locus on its known centerline, measured by arc length."""
	length = path.length()
	if abs(path.start-point) < 1e-9:
		return 0.0
	if abs(path.end-point) < 1e-9:
		return length
	best = min(range(1001), key=lambda index: abs(path.point(index/1000)-point))
	low, high = max(0, best-2)/1000, min(1000, best+2)/1000
	for _ in range(24):
		left = low+(high-low)/3
		right = high-(high-low)/3
		if abs(path.point(left)-point) < abs(path.point(right)-point):
			high = right
		else:
			low = left
	distance = path.length(0, (low+high)/2)
	return distance


class Surface:
	"""Sample only the bent surface; straight chromosomes retain exact coordinates."""

	def __init__(self, path: svgpathtools.Path, thickness: float) -> None:
		self.path = smooth_centerline(path)
		self.width = thickness
		self.scale = thickness / REFERENCE_HEIGHT
		self.length = self.path.length()
		self.cap_length = min(thickness*8/30, self.length/4)
		self.straight = len(self.path) == 1 and isinstance(self.path[0], svgpathtools.Line)
		self.positions = []
		self.normals = []
		self.distances = []
		distance = 0
		for segment in self.path:
			count = 1 if isinstance(segment, svgpathtools.Line) else max(16,
				math.ceil(segment.length() / (thickness / 12)))
			for index in range(count + 1):
				position = segment.point(index / count)
				normal = segment.unit_tangent(index / count) * 1j
				if self.positions and abs(position-self.positions[-1]) < 1e-10:
					continue
				if self.positions:
					distance += abs(position-self.positions[-1])
				self.positions.append(position)
				self.normals.append(normal)
				self.distances.append(distance)
		# Keep both surface edges accurate without repeating thousands of nearly collinear points.
		edges = [[position + side * thickness/2 * normal
			for position, normal in zip(self.positions, self.normals)] for side in (-1, 1)]
		keep = {0, len(self.positions)-1}
		spans = [(0, len(self.positions)-1)]
		while spans:
			first, last = spans.pop()
			if last-first < 2:
				continue
			error, split = 0, first
			for index in range(first+1, last):
				fraction = (self.distances[index]-self.distances[first]) / (
					self.distances[last]-self.distances[first])
				deviation = max(abs(edge[index] - (edge[first]*(1-fraction) + edge[last]*fraction))
					for edge in edges)
				if deviation > error:
					error, split = deviation, index
			if error > thickness/120:
				keep.add(split)
				spans.extend(((first, split), (split, last)))
		indices = sorted(keep)
		self.positions = [self.positions[index] for index in indices]
		self.normals = [self.normals[index] for index in indices]
		self.distances = [self.distances[index] for index in indices]
		self.distances = [value * self.length / distance for value in self.distances]

	def point(self, along: float, across: float) -> complex:
		index = min(len(self.distances)-2, max(0,
			bisect.bisect_right(self.distances, along)-1))
		fraction = (along-self.distances[index]) / (self.distances[index+1]-self.distances[index])
		position = self.positions[index] * (1-fraction) + self.positions[index+1] * fraction
		normal = self.normals[index] * (1-fraction) + self.normals[index+1] * fraction
		return position + normal / abs(normal) * across

	def _offset(self, index: int, across: float) -> complex:
		normal = self.normals[index]
		return self.positions[index] + normal / abs(normal) * across

	@staticmethod
	def _points_polygon(points: list[complex]) -> str:
		return 'M ' + ' L '.join(f'{point.real:.4f},{point.imag:.4f}' for point in points) + ' Z'

	def polygon(self, coordinates: list[tuple[float, float]]) -> str:
		return self._points_polygon([self.point(along, across) for along, across in coordinates])

	def ribbon(self, start: float, end: float, top: float, bottom: float) -> str:
		indices = [index for index, distance in enumerate(self.distances) if start < distance < end]
		points = [self.point(start, top)] + [self._offset(index, top) for index in indices] + [
			self.point(end, top), self.point(end, bottom)] + [
			self._offset(index, bottom) for index in reversed(indices)] + [self.point(start, bottom)]
		return self._points_polygon(points)

	def envelope(self, closed: bool = False, cut: bool = False, *,
		terminal_ends: tuple[bool, bool] | None = None) -> str:
		"""Round native ends and leave cut ends flat."""
		half = self.width / 2
		if closed or cut or terminal_ends == (False, False):
			return self.ribbon(0, self.length, -half, half)
		radius = min(6*self.scale, self.length/2)
		round_start, round_end = (True, True) if terminal_ends is None else terminal_ends
		start = radius if round_start else 0
		end = self.length-radius if round_end else self.length
		indices = [index for index, distance in enumerate(self.distances)
			if start < distance < end]
		points = [self.point(start, -half)] + [self._offset(index, -half) for index in indices] + [
			self.point(end, -half)]
		if round_end:
			for across, angle in ((-half+radius, -90), (half-radius, 0)):
				points.extend(self.point(end+radius*math.cos(math.radians(angle+i*90/8)),
					across+radius*math.sin(math.radians(angle+i*90/8))) for i in range(9))
		else:
			points.append(self.point(end, half))
		points.extend(self._offset(index, half) for index in reversed(indices))
		if round_start:
			for across, angle in ((half-radius, 90), (-half+radius, 180)):
				points.extend(self.point(start+radius*math.cos(math.radians(angle+i*90/8)),
					across+radius*math.sin(math.radians(angle+i*90/8))) for i in range(9))
		else:
			points.append(self.point(start, half))
		return self._points_polygon(points)

	def paint(self, parent: lxml.etree._Element, name: str, *, texture: bool = True,
		texture_spans: tuple[tuple[float, float], ...] | None = None) -> None:
		"""Background texture, foreground sheen, then zero-blur inset shadows."""
		half = self.width/2
		if texture:
			layer = lxml.etree.SubElement(parent, 'g', {'data-layer': 'texture'})
			# CSS 95deg gradient projected onto its 79 x 30 border-box tile.
			angle = math.radians(5)
			for number, (left, right) in enumerate(texture_spans or ((0, self.length),)):
				clip_id = f'{name}-texture-{number}'
				clip = lxml.etree.SubElement(layer, 'clipPath', {'id': clip_id})
				lxml.etree.SubElement(clip, 'path', {'d': self.ribbon(left, right, -half, half)})
				tile = lxml.etree.SubElement(layer, 'g', {'clip-path': f'url(#{clip_id})'})
				dark_marks, light_marks = [], []
				for origin in range(-1, math.ceil((right-left)/(79*self.scale))+1):
					for start, stop, end in TEXTURE_STOPS:
						for marks, a, b in ((dark_marks, start, stop), (light_marks, stop, end)):
							coords = []
							for value, across in ((a, -half), (b, -half), (b, half), (a, half)):
								along = left + origin*79*self.scale + (value*self.scale-
									(across+half)*math.sin(angle))/math.cos(angle)
								coords.append((along, across))
							marks.append(self.polygon(coords))
				# One paint operation per shade keeps translucent texture compact in PDF.
				for marks, color, alpha in ((dark_marks, '#000000', '.09'), (light_marks, '#FFFFFF', '.08')):
					lxml.etree.SubElement(tile, 'path', {'d': ' '.join(marks), 'fill': color,
						'fill-opacity': alpha})
		layer = lxml.etree.SubElement(parent, 'g', {'data-layer': 'sheen'})
		if self.straight:
			gradient = lxml.etree.SubElement(layer, 'linearGradient', {'id': name+'-sheen',
				'gradientUnits': 'userSpaceOnUse'})
			for prefix, position in (('1', self.point(0, -half)), ('2', self.point(0, half))):
				gradient.set('x'+prefix, str(position.real))
				gradient.set('y'+prefix, str(position.imag))
			for offset, color, alpha in (('0', '#FFFFFF', '.25'), ('.45', '#FFFFFF', '0'),
				('.45', '#000000', '0'), ('1', '#000000', '.16')):
				lxml.etree.SubElement(gradient, 'stop', {'offset': offset, 'stop-color': color, 'stop-opacity': alpha})
			lxml.etree.SubElement(layer, 'path', {'d': self.ribbon(0, self.length, -half, half),
				'fill': f'url(#{name}-sheen)'})
		else:
			# SVG has no swept gradient: sample the BPQ alpha function across the rod.
			for index in range(48):
				t = (index+.5)/48
				alpha = .25*(1-t/.45) if t < .45 else .16*(t-.45)/.55
				lxml.etree.SubElement(layer, 'path', {'d': self.ribbon(0, self.length,
					-half+self.width*index/48, -half+self.width*(index+1)/48+.002*self.scale),
					'fill': '#FFFFFF' if t < .45 else '#000000', 'fill-opacity': str(alpha)})
		layer = lxml.etree.SubElement(parent, 'g', {'data-layer': 'inset-shadows'})
		for top, bottom, color, alpha in ((-half+2*self.scale, -half+4*self.scale, '#FFFFFF', '.55'),
			(half-5*self.scale, half-2*self.scale, '#000000', '.18')):
			lxml.etree.SubElement(layer, 'path', {'d': self.ribbon(0, self.length, top, bottom),
				'fill': color, 'fill-opacity': alpha})
