"""BPQ table paint layers mapped from longitudinal/transverse coordinates to SVG."""

import bisect
import math
import xml.etree.ElementTree as ET

import svgpathtools


# BPQ translocationlib.py: dimensions at CHROMOSOME_HEIGHT=30, not fixed pixels.
REFERENCE_HEIGHT = 30
TEXTURE_STOPS = ((5, 7, 8), (18, 21, 22), (29, 30, 31),
	(46, 48, 49), (59, 62, 63))


class Surface:
	"""Sample only the bent surface; straight chromosomes retain exact coordinates."""

	def __init__(self, path, thickness):
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
				if self.positions and abs(position-self.positions[-1]) < 1e-10:
					continue
				if self.positions:
					distance += abs(position-self.positions[-1])
				self.positions.append(position)
				self.normals.append(segment.unit_tangent(index / count) * 1j)
				self.distances.append(distance)
		self.distances = [value * self.length / distance for value in self.distances]

	def point(self, along, across):
		index = min(len(self.distances)-2, max(0,
			bisect.bisect_right(self.distances, along)-1))
		fraction = (along-self.distances[index]) / (self.distances[index+1]-self.distances[index])
		position = self.positions[index] * (1-fraction) + self.positions[index+1] * fraction
		normal = self.normals[index] * (1-fraction) + self.normals[index+1] * fraction
		return position + normal / abs(normal) * across

	def polygon(self, coordinates):
		points = [self.point(along, across) for along, across in coordinates]
		return 'M ' + ' L '.join(f'{point.real:.4f},{point.imag:.4f}' for point in points) + ' Z'

	def ribbon(self, start, end, top, bottom):
		samples = [start] + [s for s in self.distances if start < s < end] + [end]
		return self.polygon([(s, top) for s in samples] + [(s, bottom) for s in reversed(samples)])

	def envelope(self, closed=False, cut=False):
		half = self.width / 2
		if closed or cut:
			return self.ribbon(0, self.length, -half, half)
		radius = min(6*self.scale, self.length/2)
		coordinates = [(s, -half) for s in [radius] +
			[s for s in self.distances if radius < s < self.length-radius] + [self.length-radius]]
		for cx, cy, start in ((self.length-radius, -half+radius, -90),
			(self.length-radius, half-radius, 0)):
			coordinates.extend((cx+radius*math.cos(math.radians(start+i*90/8)),
				cy+radius*math.sin(math.radians(start+i*90/8))) for i in range(9))
		coordinates.extend((s, half) for s in reversed(self.distances) if radius < s < self.length-radius)
		for cx, cy, start in ((radius, half-radius, 90), (radius, -half+radius, 180)):
			coordinates.extend((cx+radius*math.cos(math.radians(start+i*90/8)),
				cy+radius*math.sin(math.radians(start+i*90/8))) for i in range(9))
		return self.polygon(coordinates)

	def paint(self, parent, name, *, texture=True, texture_spans=None):
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
