"""BPQ table paint layers mapped from longitudinal/transverse coordinates to SVG."""

import bisect
import math
import xml.etree.ElementTree as ET

import svgpathtools


# BPQ translocationlib.py: dimensions at CHROMOSOME_HEIGHT=30, not fixed pixels.
REFERENCE_HEIGHT = 30
TEXTURE_STOPS = ((5, 7, 8), (18, 21, 22), (29, 30, 31),
	(46, 48, 49), (59, 62, 63))


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
		self.path = path
		self.width = thickness
		self.scale = thickness / REFERENCE_HEIGHT
		self.length = path.length()
		self.straight = len(path) == 1 and isinstance(path[0], svgpathtools.Line)
		self.positions = []
		self.normals = []
		self.distances = []
		distance = 0
		for segment in path:
			count = 1 if isinstance(segment, svgpathtools.Line) else max(16,
				math.ceil(segment.length() / (thickness / 12)))
			for index in range(count + 1):
				position = segment.point(index / count)
				normal = segment.unit_tangent(index / count) * 1j
				if self.positions and abs(position-self.positions[-1]) < 1e-10:
					# Keep both sides of a genuine corner.  They share a centerline
					# position and distance, but their surface offsets are different.
					if abs(normal-self.normals[-1]) < 1e-10:
						continue
					self.positions.append(position)
					self.normals.append(normal)
					self.distances.append(distance)
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
		# Simplification must not bridge a hard join.  Otherwise it may discard
		# one normal and interpolate that turn down an entire straight chromosome arm.
		corners = [index for index in range(1, len(self.positions))
			if abs(self.positions[index]-self.positions[index-1]) < 1e-10]
		for corner in corners:
			keep.update((corner-1, corner))
		spans = []
		first = 0
		for corner in corners:
			spans.append((first, corner-1))
			first = corner
		spans.append((first, len(self.positions)-1))
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

	def envelope(self, closed: bool = False, cut: bool = False) -> str:
		half = self.width / 2
		if closed or cut:
			return self.ribbon(0, self.length, -half, half)
		radius = min(6*self.scale, self.length/2)
		indices = [index for index, distance in enumerate(self.distances)
			if radius < distance < self.length-radius]
		points = [self.point(radius, -half)] + [self._offset(index, -half) for index in indices] + [
			self.point(self.length-radius, -half)]
		for cx, cy, start in ((self.length-radius, -half+radius, -90),
			(self.length-radius, half-radius, 0)):
			points.extend(self.point(cx+radius*math.cos(math.radians(start+i*90/8)),
				cy+radius*math.sin(math.radians(start+i*90/8))) for i in range(9))
		points.extend(self._offset(index, half) for index in reversed(indices))
		for cx, cy, start in ((radius, half-radius, 90), (radius, -half+radius, 180)):
			points.extend(self.point(cx+radius*math.cos(math.radians(start+i*90/8)),
				cy+radius*math.sin(math.radians(start+i*90/8))) for i in range(9))
		return self._points_polygon(points)

	def paint(self, parent: ET.Element, name: str, *, texture: bool = True,
		texture_spans: tuple[tuple[float, float], ...] | None = None) -> None:
		"""Background texture, foreground sheen, then zero-blur inset shadows."""
		half = self.width/2
		if texture:
			layer = ET.SubElement(parent, 'g', {'data-layer': 'texture'})
			# CSS 95deg gradient projected onto its 79 x 30 border-box tile.
			angle = math.radians(5)
			for number, (left, right) in enumerate(texture_spans or ((0, self.length),)):
				clip_id = f'{name}-texture-{number}'
				clip = ET.SubElement(layer, 'clipPath', {'id': clip_id})
				ET.SubElement(clip, 'path', {'d': self.ribbon(left, right, -half, half)})
				tile = ET.SubElement(layer, 'g', {'clip-path': f'url(#{clip_id})'})
				for origin in range(-1, math.ceil((right-left)/(79*self.scale))+1):
					for start, stop, end in TEXTURE_STOPS:
						for a, b, color, alpha in ((start, stop, '#000000', '.09'),
							(stop, end, '#FFFFFF', '.08')):
							coords = []
							for value, across in ((a, -half), (b, -half), (b, half), (a, half)):
								along = left + origin*79*self.scale + (value*self.scale-
									(across+half)*math.sin(angle))/math.cos(angle)
								coords.append((along, across))
							ET.SubElement(tile, 'path', {'d': self.polygon(coords), 'fill': color,
								'fill-opacity': alpha})
		layer = ET.SubElement(parent, 'g', {'data-layer': 'sheen'})
		if self.straight:
			gradient = ET.SubElement(layer, 'linearGradient', {'id': name+'-sheen',
				'gradientUnits': 'userSpaceOnUse'})
			for prefix, position in (('1', self.point(0, -half)), ('2', self.point(0, half))):
				gradient.set('x'+prefix, str(position.real))
				gradient.set('y'+prefix, str(position.imag))
			for offset, color, alpha in (('0', '#FFFFFF', '.25'), ('.45', '#FFFFFF', '0'),
				('.45', '#000000', '0'), ('1', '#000000', '.16')):
				ET.SubElement(gradient, 'stop', {'offset': offset, 'stop-color': color, 'stop-opacity': alpha})
			ET.SubElement(layer, 'path', {'d': self.ribbon(0, self.length, -half, half),
				'fill': f'url(#{name}-sheen)'})
		else:
			# SVG has no swept gradient: sample the BPQ alpha function across the rod.
			for index in range(48):
				t = (index+.5)/48
				alpha = .25*(1-t/.45) if t < .45 else .16*(t-.45)/.55
				ET.SubElement(layer, 'path', {'d': self.ribbon(0, self.length,
					-half+self.width*index/48, -half+self.width*(index+1)/48+.002*self.scale),
					'fill': '#FFFFFF' if t < .45 else '#000000', 'fill-opacity': str(alpha)})
		layer = ET.SubElement(parent, 'g', {'data-layer': 'inset-shadows'})
		for top, bottom, color, alpha in ((-half+2*self.scale, -half+4*self.scale, '#FFFFFF', '.55'),
			(half-5*self.scale, half-2*self.scale, '#000000', '.18')):
			ET.SubElement(layer, 'path', {'d': self.ribbon(0, self.length, top, bottom),
				'fill': color, 'fill-opacity': alpha})
