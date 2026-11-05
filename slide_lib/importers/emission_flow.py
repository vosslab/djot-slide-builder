"""Group imported text components into safe source-order flows."""

# Standard Library
import dataclasses
import itertools

# Local Modules
import slide_lib.importers.geometry as geometry


FLOW_MIN_HORIZONTAL_OVERLAP_RATIO = 0.60
FLOW_LANE_SPAN_VARIATION_RATIO = 1.35
FLOW_LANE_CENTER_OFFSET_RATIO = 0.20
FOOTER_MIN_WIDTH_RATIO = 0.70
FOOTER_MAX_HEIGHT_RATIO = 0.50
FOOTER_COLUMN_BOTTOM_PADDING_RATIO = 0.08
FOOTER_VERTICAL_PADDING_RATIO = 0.05
FOOTER_IMAGE_PADDING_RATIO = 0.05
BOTTOM_FOOTER_RELATION_REASON = "bottom-footer structural topology"
SHALLOW_FLOW_MAX_VERTICAL_OVERLAP = 0.03
SHALLOW_FLOW_MAX_SMALLER_HEIGHT_RATIO = 0.25


@dataclasses.dataclass(frozen=True)
class EmissionComponent:
	"""One bounded, single-kind source component assigned to one Djot cell."""

	bounds: geometry.NormalizedBounds
	lines: tuple[str, ...]
	kind: str
	image_references: tuple[str, ...] = ()
	source_image_ids: tuple[tuple[int, str], ...] = ()
	coarse_text_container: bool = False
	source_kind: str = ""
	source_ordinals: tuple[int, ...] = ()
	member_footprints: tuple[geometry.NormalizedBounds, ...] = ()
	classification_reason: str = ""
	placeholder_confidence: float = 0.0
	rotation_degrees: float = 0.0
	source_order: tuple[int, ...] = ()


#============================================
def component_read_key(component: EmissionComponent) -> tuple[float, float, int]:
	"""Order components geometrically; immutable source ordinals break exact ties."""
	return component.bounds.top, component.bounds.left, min(component.source_ordinals, default=0)


#============================================
def component_footprints(component: EmissionComponent) -> tuple[geometry.NormalizedBounds, ...]:
	"""Return immutable component members, with direct bounds for synthetic callers."""
	return component.member_footprints or (component.bounds,)


#============================================
def union_bounds(bounds: tuple[geometry.NormalizedBounds, ...]) -> geometry.NormalizedBounds:
	"""Return the geometric union of already-normalized source rectangles."""
	result = bounds[0]
	for item in bounds[1:]:
		result = result.union(item)
	return result


#============================================
def raw_components_overlap(components: list[EmissionComponent]) -> bool:
	"""Check member collisions without treating any composition as an allowed relation."""
	for index, first in enumerate(components):
		for second in components[index + 1:]:
			if any(geometry.substantially_overlaps(left, right) for left in component_footprints(first)
				for right in component_footprints(second)):
				return True
	return False


#============================================
def column_footer_padding(column: EmissionComponent) -> float:
	"""Bound source padding by both normalized and column-relative footer limits."""
	return min(FOOTER_IMAGE_PADDING_RATIO, FOOTER_COLUMN_BOTTOM_PADDING_RATIO * column.bounds.height)


#============================================
def shallow_broad_footer(components: list[EmissionComponent], footer: EmissionComponent) -> bool:
	"""Recognize one short lower textbox broad enough to be a footer reference."""
	envelope = union_bounds(tuple(item.bounds for item in components))
	return footer.bounds.width >= envelope.width * FOOTER_MIN_WIDTH_RATIO and \
		footer.bounds.height <= envelope.height * FOOTER_MAX_HEIGHT_RATIO


#============================================
def coalesce_bottom_footer(components: list[EmissionComponent]) -> list[EmissionComponent]:
	"""Merge broad bottom text boxes beneath exactly two disjoint peers."""
	footer = [item for item in components if item.kind == "text" and item.source_kind == "text-box"]
	peers = [item for item in components if item not in footer]
	if len(peers) != 2 or not footer or raw_components_overlap(peers):
		return components
	if any(not shallow_broad_footer(components, item) or item.bounds.top < peer.bounds.bottom - column_footer_padding(peer)
		for item in footer for peer in peers):
		return components
	footer.sort(key=component_read_key)
	if any(not follows_footer_lane(first, second) for first, second in zip(footer, footer[1:])):
		return components
	lines = tuple(line for index, item in enumerate(footer)
		for line in ((*item.lines, "") if index < len(footer) - 1 else item.lines))
	merged = EmissionComponent(union_bounds(tuple(item.bounds for item in footer)), lines, "flow",
		source_kind="text-box", source_ordinals=tuple(ordinal for item in footer for ordinal in item.source_ordinals),
		member_footprints=tuple(footprint for item in footer for footprint in component_footprints(item)),
		classification_reason=BOTTOM_FOOTER_RELATION_REASON,
		source_order=min((item.source_order for item in footer if item.source_order), default=()))
	return [item for item in components if item not in footer] + [merged]


#============================================
def coalesce_text_flows(components: list[EmissionComponent]) -> list[EmissionComponent]:
	"""Join unique vertically stacked editable text blocks within one source lane."""
	available = set(range(len(components)))
	groups: list[tuple[int, ...]] = []
	for first in sorted(available, key=lambda index: component_read_key(components[index])):
		if first not in available or components[first].kind != "text":
			continue
		group = [first]
		while True:
			candidates = sorted((index for index in available - set(group)
				if components[index].kind == "text" and follows_text_lane(components[group[-1]], components[index])),
				key=lambda index: component_read_key(components[index]))
			if len(candidates) != 1 or image_interleaves_lane(components, components[group[-1]], components[candidates[0]]) or \
				(shallow_overlap_text_lane(components[group[-1]], components[candidates[0]]) and
					(shallow_overlap_lane_competes(components, components[group[-1]], components[candidates[0]]) or
						nontext_interleaves_lane(components, components[group[-1]], components[candidates[0]]))):
				break
			group.append(candidates[0])
		if len(group) > 1:
			groups.append(tuple(group))
			available.difference_update(group)
	result = [component for index, component in enumerate(components) if index in available]
	for group in groups:
		members = tuple(components[index] for index in group)
		lines = tuple(line for member_index, member in enumerate(members)
			for line in ((*member.lines, "") if member_index < len(members) - 1 else member.lines))
		result.append(EmissionComponent(union_bounds(tuple(member.bounds for member in members)), lines, "flow",
			source_ordinals=tuple(ordinal for member in members for ordinal in member.source_ordinals),
			member_footprints=tuple(footprint for member in members for footprint in component_footprints(member)),
			source_kind=members[0].source_kind if all(member.source_kind == members[0].source_kind for member in members) else "",
			source_order=min((member.source_order for member in members if member.source_order), default=())))
	return result


#============================================
def follows_text_lane(first: EmissionComponent, second: EmissionComponent) -> bool:
	"""Recognize a separated next text block that shares a substantial lane."""
	gap = second.bounds.top - first.bounds.bottom
	return gap >= 0.0 and follows_same_lane(first, second) or shallow_overlap_text_lane(first, second)


#============================================
def shallow_overlap_text_lane(first: EmissionComponent, second: EmissionComponent) -> bool:
	"""Recognize one adjacent direct text box with a bounded source border overlap."""
	if component_read_key(first) >= component_read_key(second) or any(item.kind != "text" or
		item.source_kind != "text-box" or item.coarse_text_container or abs(item.rotation_degrees) >= 1.0 or
		len(component_footprints(item)) != 1 for item in (first, second)):
		return False
	overlap = min(first.bounds.bottom, second.bounds.bottom) - second.bounds.top
	return abs(first.bounds.left - second.bounds.left) <= .01 and \
		abs(first.bounds.width - second.bounds.width) <= max(first.bounds.width, second.bounds.width) * .02 and \
		0.0 < overlap <= SHALLOW_FLOW_MAX_VERTICAL_OVERLAP and overlap <= min(first.bounds.height, second.bounds.height) * SHALLOW_FLOW_MAX_SMALLER_HEIGHT_RATIO


#============================================
def shallow_overlap_lane_competes(components: list[EmissionComponent], first: EmissionComponent,
		second: EmissionComponent) -> bool:
	"""Leave independent overlapping text lanes unmerged for manual topology review."""
	for candidate_first, candidate_second in itertools.permutations(components, 2):
		if (candidate_first, candidate_second) != (first, second) and shallow_overlap_text_lane(candidate_first, candidate_second) and \
			abs(candidate_first.bounds.left - first.bounds.left) > .01:
			return True
	return False


#============================================
def follows_footer_lane(first: EmissionComponent, second: EmissionComponent) -> bool:
	"""Allow bounded source padding only for ordered full-width footer members."""
	gap = second.bounds.top - first.bounds.bottom
	return component_read_key(first) < component_read_key(second) and gap >= -FOOTER_VERTICAL_PADDING_RATIO and \
		first.bounds.width >= FOOTER_MIN_WIDTH_RATIO and second.bounds.width >= FOOTER_MIN_WIDTH_RATIO and \
		follows_same_lane(first, second)


#============================================
def follows_same_lane(first: EmissionComponent, second: EmissionComponent) -> bool:
	"""Require substantial overlap, span agreement, and center agreement in one lane."""
	overlap = min(first.bounds.right, second.bounds.right) - max(first.bounds.left, second.bounds.left)
	overlap_ratio = overlap / min(first.bounds.width, second.bounds.width)
	center_offset = abs((first.bounds.left + first.bounds.right - second.bounds.left - second.bounds.right) / 2)
	return overlap_ratio >= FLOW_MIN_HORIZONTAL_OVERLAP_RATIO and \
		max(first.bounds.width, second.bounds.width) <= min(first.bounds.width, second.bounds.width) * FLOW_LANE_SPAN_VARIATION_RATIO and \
		center_offset <= min(first.bounds.width, second.bounds.width) * FLOW_LANE_CENTER_OFFSET_RATIO


#============================================
def image_interleaves_lane(components: list[EmissionComponent], first: EmissionComponent,
		second: EmissionComponent) -> bool:
	"""Preserve a spatial image component instead of folding text around it."""
	for component in components:
		if component.kind != "image" or not first.bounds.top <= component.bounds.top <= second.bounds.bottom:
			continue
		overlap = min(component.bounds.right, max(first.bounds.right, second.bounds.right)) - max(component.bounds.left, min(first.bounds.left, second.bounds.left))
		if overlap > 0:
			return True
	return False


#============================================
def nontext_interleaves_lane(components: list[EmissionComponent], first: EmissionComponent,
		second: EmissionComponent) -> bool:
	"""Keep a shallow text flow out of a lane occupied by another rendered component."""
	for component in components:
		if component in {first, second} or component.kind == "text" or \
			not first.bounds.top <= component.bounds.top <= second.bounds.bottom:
			continue
		if min(component.bounds.right, max(first.bounds.right, second.bounds.right)) > \
			max(component.bounds.left, min(first.bounds.left, second.bounds.left)):
			return True
	return False
