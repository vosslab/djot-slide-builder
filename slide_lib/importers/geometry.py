"""Normalized geometry primitives shared by imported-deck planning."""

# Standard Library
import dataclasses
import math


# Slide-relative tolerances keep raster-only mixed visuals stricter than ordinary
# border-contact collision handling.  ASVS 2.2.1 applies to normalized source bounds.
FLOW_BORDER_CONTACT_RATIO = 0.02
MIXED_VISUAL_OVERLAP_RATIO = 0.03
CONNECTOR_MIN_THICKNESS_RATIO = 0.001
CONNECTOR_MAX_THICKNESS_RATIO = 0.01


@dataclasses.dataclass(frozen=True)
class NormalizedBounds:
	"""A finite, ordered rectangle expressed as fractions of one slide."""

	left: float
	top: float
	right: float
	bottom: float

	def __post_init__(self) -> None:
		values = (self.left, self.top, self.right, self.bottom)
		if not all(math.isfinite(value) for value in values):
			raise ValueError("source bounds must be finite")
		if not 0.0 <= self.left < self.right <= 1.0:
			raise ValueError("source bounds must be ordered within slide width")
		if not 0.0 <= self.top < self.bottom <= 1.0:
			raise ValueError("source bounds must be ordered within slide height")

	@property
	def width(self) -> float:
		"""Return normalized width."""
		return self.right - self.left

	@property
	def height(self) -> float:
		"""Return normalized height."""
		return self.bottom - self.top

	def union(self, other: "NormalizedBounds") -> "NormalizedBounds":
		"""Return the smallest bounded rectangle containing both inputs."""
		return NormalizedBounds(min(self.left, other.left), min(self.top, other.top),
			max(self.right, other.right), max(self.bottom, other.bottom))


@dataclasses.dataclass(frozen=True)
class NormalizedLineEndpoints:
	"""The uninflated, clipped endpoints of one source connector."""

	left: float
	top: float
	right: float
	bottom: float

	def __post_init__(self) -> None:
		"""Validate endpoint provenance before it reaches planning metadata."""
		values = (self.left, self.top, self.right, self.bottom)
		if not all(math.isfinite(value) for value in values):
			raise ValueError("source connector endpoints must be finite")
		if not 0.0 <= self.left <= self.right <= 1.0 or not 0.0 <= self.top <= self.bottom <= 1.0:
			raise ValueError("source connector endpoints must remain within slide bounds")


@dataclasses.dataclass(frozen=True)
class DegenerateConnectorFootprint:
	"""A planning footprint paired with the original connector endpoints."""

	endpoints: NormalizedLineEndpoints
	footprint: NormalizedBounds


def degenerate_connector_footprint(
	left: int | float, top: int | float, width: int | float, height: int | float,
	stroke_width: int | float, slide_width: int | float, slide_height: int | float,
) -> DegenerateConnectorFootprint | None:
	"""Inflate one visible horizontal or vertical source connector for planning."""
	values = (left, top, width, height, stroke_width, slide_width, slide_height)
	if not all(math.isfinite(float(value)) for value in values):
		return None
	if width < 0 or height < 0 or stroke_width <= 0 or slide_width <= 0 or slide_height <= 0:
		return None
	if (width == 0) == (height == 0):
		return None
	start_x, end_x = clipped_pair(left, left + width, slide_width)
	start_y, end_y = clipped_pair(top, top + height, slide_height)
	if start_x == end_x and start_y == end_y:
		return None
	if width == 0 and start_y == end_y or height == 0 and start_x == end_x:
		return None
	endpoints = NormalizedLineEndpoints(start_x, start_y, end_x, end_y)
	if width == 0:
		thickness = bounded_thickness(stroke_width, slide_width)
		footprint = NormalizedBounds(max(0.0, start_x - thickness / 2), start_y,
			min(1.0, start_x + thickness / 2), end_y)
	else:
		thickness = bounded_thickness(stroke_width, slide_height)
		footprint = NormalizedBounds(start_x, max(0.0, start_y - thickness / 2),
			end_x, min(1.0, start_y + thickness / 2))
	return DegenerateConnectorFootprint(endpoints, footprint)


def clipped_pair(start: int | float, end: int | float, size: int | float) -> tuple[float, float]:
	"""Normalize one axis and clip it to the visible slide interval."""
	first = min(1.0, max(0.0, float(start) / float(size)))
	second = min(1.0, max(0.0, float(end) / float(size)))
	return first, second


def bounded_thickness(stroke_width: int | float, dimension: int | float) -> float:
	"""Return the named safe range for one normalized connector thickness."""
	return min(CONNECTOR_MAX_THICKNESS_RATIO,
		max(CONNECTOR_MIN_THICKNESS_RATIO, float(stroke_width) / float(dimension)))


def normalized_bounds(left: int | float, top: int | float, width: int | float, height: int | float,
	slide_width: int | float, slide_height: int | float) -> NormalizedBounds:
	"""Normalize finite visible source geometry after ranged-input validation."""
	values = (left, top, width, height, slide_width, slide_height)
	if not all(math.isfinite(float(value)) for value in values):
		raise ValueError("source geometry must be finite")
	if slide_width <= 0 or slide_height <= 0 or width <= 0 or height <= 0:
		raise ValueError("source geometry requires positive dimensions")
	right, bottom = left + width, top + height
	if right <= 0 or bottom <= 0 or left >= slide_width or top >= slide_height:
		raise ValueError("source geometry lies outside slide bounds")
	return NormalizedBounds(max(float(left), 0.0) / float(slide_width),
		max(float(top), 0.0) / float(slide_height), min(float(right), float(slide_width)) / float(slide_width),
		min(float(bottom), float(slide_height)) / float(slide_height))


def overlaps_or_contains(first: NormalizedBounds, second: NormalizedBounds) -> bool:
	"""Return whether two source rectangles physically overlap."""
	return first.left < second.right and second.left < first.right and first.top < second.bottom and second.top < first.bottom


def center_is_within(inner: NormalizedBounds, outer: NormalizedBounds) -> bool:
	"""Return whether a source region center lies within another region."""
	return outer.left <= (inner.left + inner.right) / 2 <= outer.right and outer.top <= (inner.top + inner.bottom) / 2 <= outer.bottom


def substantially_overlaps(first: NormalizedBounds, second: NormalizedBounds) -> bool:
	"""Treat only nontrivial two-axis overlap as a direct-component collision."""
	return overlap_width(first, second) > FLOW_BORDER_CONTACT_RATIO and overlap_height(first, second) > FLOW_BORDER_CONTACT_RATIO


def strictly_overlaps(first: NormalizedBounds, second: NormalizedBounds) -> bool:
	"""Require stronger two-axis overlap before a mixed visual needs raster ownership."""
	return overlap_width(first, second) >= MIXED_VISUAL_OVERLAP_RATIO and overlap_height(first, second) >= MIXED_VISUAL_OVERLAP_RATIO


def overlap_width(first: NormalizedBounds, second: NormalizedBounds) -> float:
	"""Return horizontal intersection depth."""
	return max(0.0, min(first.right, second.right) - max(first.left, second.left))


def overlap_height(first: NormalizedBounds, second: NormalizedBounds) -> float:
	"""Return vertical intersection depth."""
	return max(0.0, min(first.bottom, second.bottom) - max(first.top, second.top))
