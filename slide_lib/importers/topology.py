"""Shared registry-derived viability for ordinary source component geometry."""

# Standard Library
import itertools

# Local modules
import slide_lib.importers.geometry as geometry
import slide_lib.layout_registry


TOPOLOGY_MAX_SCORE = .32
TOPOLOGY_RUNNER_UP_MARGIN = .035
MATERIAL_AXIS_OVERLAP_RATIO = .60


#============================================
def ordinary_layout_viable(bounds: tuple[geometry.NormalizedBounds, ...]) -> bool:
	"""Return whether live registry topology accepts ordinary direct components."""
	return ordinary_layout_match(bounds) is not None


#============================================
def ordinary_layout_match(
		bounds: tuple[geometry.NormalizedBounds, ...],
		preserve_axis_overlap: bool = True,
) -> tuple[str, tuple[int, ...]] | None:
	"""Return one unique live-registry topology match within shared thresholds."""
	if not 1 <= len(bounds) <= 6:
		return None
	source = normalized_boxes(bounds)
	ranked: list[tuple[float, str, tuple[int, ...]]] = []
	for name in slide_lib.layout_registry.names():
		spec = slide_lib.layout_registry.contract_for(name)
		if not spec.topology_matchable or spec.cell_count != len(bounds):
			continue
		slots = spec.topology_slots
		matches = [
			(score(source, slots, order), order)
			for order in itertools.permutations(range(len(bounds)))
			if relations_match(source, slots, order, preserve_axis_overlap)
		]
		if matches:
			best = min(value for value, _order in matches)
			order = min(item for value, item in matches if abs(value - best) <= 1e-9)
			ranked.append((best, spec.name, order))
	ranked.sort()
	if not ranked or ranked[0][0] > TOPOLOGY_MAX_SCORE:
		return None
	if len(ranked) > 1 and ranked[1][0] - ranked[0][0] < TOPOLOGY_RUNNER_UP_MARGIN:
		return None
	_score, name, order = ranked[0]
	return name, order


#============================================
def normalized_boxes(
		bounds: tuple[geometry.NormalizedBounds, ...],
) -> tuple[tuple[float, float, float, float], ...]:
	"""Normalize source boxes against their shared envelope."""
	envelope = bounds[0]
	for item in bounds[1:]:
		envelope = envelope.union(item)
	return tuple(
		(
			(item.left - envelope.left) / envelope.width,
			(item.top - envelope.top) / envelope.height,
			item.width / envelope.width,
			item.height / envelope.height,
		)
		for item in bounds
	)


#============================================
def relations_match(
		source: tuple[tuple[float, float, float, float], ...],
		slots: tuple[tuple[float, float, float, float, float, float], ...],
		order: tuple[int, ...],
		preserve_axis_overlap: bool = True,
) -> bool:
	"""Preserve source separation and material-axis relations in registry slots."""
	for first, second in itertools.combinations(range(len(source)), 2):
		x, y, width, height = source[first]
		other_x, other_y, other_width, other_height = source[second]
		destination = slots[order.index(first)]
		other_destination = slots[order.index(second)]
		if preserve_axis_overlap and material(x, width, other_x, other_width):
			if not material(destination[0], destination[2], other_destination[0], other_destination[2]):
				return False
		if preserve_axis_overlap and material(y, height, other_y, other_height):
			if not material(destination[1], destination[3], other_destination[1], other_destination[3]):
				return False
		if x + width <= other_x and destination[0] + destination[2] > other_destination[0]:
			return False
		if other_x + other_width <= x and other_destination[0] + other_destination[2] > destination[0]:
			return False
		if y + height <= other_y and destination[1] + destination[3] > other_destination[1]:
			return False
		if other_y + other_height <= y and other_destination[1] + other_destination[3] > destination[1]:
			return False
	return True


#============================================
def material(start: float, span: float, other_start: float, other_span: float) -> bool:
	"""Return whether two projections materially overlap."""
	overlap = min(start + span, other_start + other_span) - max(start, other_start)
	return overlap >= min(span, other_span) * MATERIAL_AXIS_OVERLAP_RATIO


#============================================
def score(
		source: tuple[tuple[float, float, float, float], ...],
		slots: tuple[tuple[float, float, float, float, float, float], ...],
		order: tuple[int, ...],
) -> float:
	"""Measure geometry agreement with one registry permutation."""
	value = 0.0
	for index, item in enumerate(order):
		x, y, width, height = source[item]
		_slot_x, _slot_y, slot_width, slot_height, center_x, center_y = slots[index]
		value += ((x + width / 2 - center_x) ** 2 + (y + height / 2 - center_y) ** 2) ** .5
		value += .20 * (abs(width - slot_width) + abs(height - slot_height))
	return value / len(source)
