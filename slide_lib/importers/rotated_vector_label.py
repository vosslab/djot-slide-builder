"""Conservative geometry evidence for rotated vector-label source clusters."""

# Standard Library
import dataclasses

# Local modules
import slide_lib.importers.geometry as geometry


ROTATED_LABEL_MIN_ABSOLUTE_DEGREES = 1.0
ROTATED_VECTOR_LABEL_PROXIMITY_RATIO = 0.08
ROTATED_VECTOR_LABEL_LANE_GAP_RATIO = 0.12


@dataclasses.dataclass(frozen=True)
class RotatedVectorLabelMembers:
	"""Exact source members of one uniquely connected rotated-label figure."""

	text_regions: tuple[object, ...]
	image_regions: tuple[object, ...]
	bounds: geometry.NormalizedBounds


def rotated_vector_label_members(
	text_regions: tuple[object, ...], image_regions: tuple[object, ...],
) -> RotatedVectorLabelMembers | None:
	"""Return one bounded rotated-vector figure only when its graph is unique."""
	vectors = tuple(
		region for region in image_regions if region.source_kind in {"vector", "connector"}
	)
	labels = tuple(region for region in text_regions if (
		region.placeholder_confidence == 0.0
		and region.source_kind in {"auto-shape", "text-box"}
	))
	if len(vectors) < 2 or len(labels) < 2:
		return None
	nodes = (*vectors, *labels)
	components = connected_components(nodes)
	candidates = tuple(
		component for component in components if is_rotated_vector_label_component(component, nodes)
	)
	if len(candidates) != 1:
		return None
	component = candidates[0]
	component_nodes = tuple(nodes[index] for index in component)
	bounds = union_bounds(tuple(node.bounds for node in component_nodes))
	if bounds == geometry.NormalizedBounds(0.0, 0.0, 1.0, 1.0):
		return None
	if any(
		(region.source_kind == "table" or region.placeholder_confidence >= 0.75)
		and geometry.center_is_within(region.bounds, bounds)
		for region in text_regions
	):
		return None
	text_members = tuple(sorted(
		(node for node in component_nodes if node in labels), key=lambda node: node.source_ordinal,
	))
	image_members = tuple(sorted(
		(node for node in component_nodes if node in vectors), key=lambda node: node.source_ordinal,
	))
	return RotatedVectorLabelMembers(text_members, image_members, bounds)


def connected_components(nodes: tuple[object, ...]) -> tuple[set[int], ...]:
	"""Find bounded source-geometry components without joining remote figures."""
	remaining = set(range(len(nodes)))
	components: list[set[int]] = []
	while remaining:
		component = {remaining.pop()}
		while True:
			connected = {
				other for index in component for other in remaining
				if related(nodes[index].bounds, nodes[other].bounds)
			}
			if not connected:
				break
			component.update(connected)
			remaining.difference_update(connected)
		components.append(component)
	return tuple(components)


def is_rotated_vector_label_component(component: set[int], nodes: tuple[object, ...]) -> bool:
	"""Require a complete, non-placeholder vector-label component with rotation."""
	members = tuple(nodes[index] for index in component)
	vectors = tuple(member for member in members if member.source_kind in {"vector", "connector"})
	labels = tuple(member for member in members if member.source_kind not in {"vector", "connector"})
	return (
		len(vectors) >= 2
		and len(labels) >= 2
		and any(abs(label.rotation_degrees) >= ROTATED_LABEL_MIN_ABSOLUTE_DEGREES for label in labels)
		and all(label.placeholder_confidence == 0.0 and label.source_kind != "table" for label in labels)
	)


def related(
	first: geometry.NormalizedBounds, second: geometry.NormalizedBounds,
) -> bool:
	"""Associate only overlapping or slide-relative nearby visual label lanes."""
	if geometry.overlaps_or_contains(first, second):
		return True
	# A vertically stacked label lane can bridge a larger gap only while sharing
	# a substantial horizontal footprint; this avoids broad all-axis joining.
	if (
		geometry.overlap_width(first, second) >= 0.03
		and vertical_gap(first, second) <= ROTATED_VECTOR_LABEL_LANE_GAP_RATIO
	):
		return True
	return not (
		first.right + ROTATED_VECTOR_LABEL_PROXIMITY_RATIO < second.left
		or second.right + ROTATED_VECTOR_LABEL_PROXIMITY_RATIO < first.left
		or first.bottom + ROTATED_VECTOR_LABEL_PROXIMITY_RATIO < second.top
		or second.bottom + ROTATED_VECTOR_LABEL_PROXIMITY_RATIO < first.top
	)


def vertical_gap(
	first: geometry.NormalizedBounds, second: geometry.NormalizedBounds,
) -> float:
	"""Return non-overlapping vertical separation between two source regions."""
	return max(first.top - second.bottom, second.top - first.bottom, 0.0)


def union_bounds(
	bounds: tuple[geometry.NormalizedBounds, ...],
) -> geometry.NormalizedBounds:
	"""Return the bounded union of one nonempty source component."""
	result = bounds[0]
	for item in bounds[1:]:
		result = result.union(item)
	return result
