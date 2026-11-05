"""Classify emitted components and select bounded Djot layouts."""

# Standard Library
import dataclasses
import itertools

# Local Modules
import slide_lib.importers.emission_flow as emission_flow
import slide_lib.importers.geometry as geometry
import slide_lib.importers.topology as topology
import slide_lib.layout_registry


GALLERY_AREA_VARIATION_RATIO = 1.30
GALLERY_ASPECT_VARIATION_RATIO = 1.30
GALLERY_LINE_CENTER_TOLERANCE = 0.12
COARSE_IMAGE_ROW_CENTER_RATIO = 0.35
COARSE_IMAGE_SIDE_BY_SIDE_RATIO = 0.50
BOTTOM_FOOTER_SCORE_CEILING = 0.35
ASYMMETRIC_EXPLANATORY_PAIR_MAX_SCORE = 0.33
ASYMMETRIC_EXPLANATORY_COMPACT_AREA_RATIO = 0.75


@dataclasses.dataclass(frozen=True)
class OverlapPermission:
	"""One exact component-pair overlap allowed by a uniquely matched composition."""

	first_index: int
	second_index: int
	relation: str
	first_footprints: tuple[geometry.NormalizedBounds, ...]
	second_footprints: tuple[geometry.NormalizedBounds, ...]
	vertical_overlap: float
	layout: str
	order: tuple[int, ...]


#============================================
def components_overlap(components: list[emission_flow.EmissionComponent]) -> bool:
	"""Return whether direct components materially overlap beyond border contact."""
	permitted_pairs = {(record.first_index, record.second_index) for record in overlap_permissions(components)}
	for index, first in enumerate(components):
		for second_index, second in enumerate(components[index + 1:], start=index + 1):
			if (index, second_index) in permitted_pairs:
				continue
			for first_footprint in emission_flow.component_footprints(first):
				for second_footprint in emission_flow.component_footprints(second):
					if geometry.substantially_overlaps(first_footprint, second_footprint):
						return True
	return False


#============================================
def overlap_permissions(components: list[emission_flow.EmissionComponent]) -> tuple[OverlapPermission, ...]:
	"""Return only component-pair permissions proven by one unique native topology."""
	records: list[OverlapPermission] = []
	if coarse_inset_key_layout(components):
		record = pair_permission(components, 0, 1, "coarse-body-styled-inset", "two-panels")
		if record is not None:
			records.append(record)
	if coarse_picture_inset_layout(components):
		record = pair_permission(components, 0, 1, "coarse-body-picture-inset", "two-panels")
		if record is not None:
			records.append(record)
	if coarse_image_geometry(components) and not coarse_picture_inset_layout(components):
		record = pair_permission(components, 0, 1, "coarse-image-peer", "two-panels")
		if record is not None:
			records.append(record)
	if len(components) == 3:
		footer_indexes = [index for index, item in enumerate(components) if item.kind == "flow" and item.source_kind == "text-box"]
		if len(footer_indexes) == 1 and bottom_footer_structure(components, footer_indexes[0]):
			footer_index = footer_indexes[0]
			try:
				selected, _slots, _order = component_layout(components)
			except ValueError:
				selected = ""
			if selected in {"two-over-one-panels", "two-plus-one-panels"}:
				for peer_index in range(len(components)):
					if peer_index == footer_index:
						continue
					overlap = max(vertical_overlap(left, right) for left in emission_flow.component_footprints(components[footer_index])
						for right in emission_flow.component_footprints(components[peer_index]))
					if 0.0 < overlap <= emission_flow.FOOTER_IMAGE_PADDING_RATIO:
						record = pair_permission(components, peer_index, footer_index, "bottom-footer-padding", selected)
						if record is not None:
							records.append(record)
		caption_footer_indexes = [index for index, item in enumerate(components) if item.kind == "text" and item.source_kind == "text-box"]
		caption_indexes = [index for index, item in enumerate(components) if item.kind == "image" and
			item.source_kind == "picture" and len(emission_flow.component_footprints(item)) == 2]
		if len(caption_footer_indexes) == 1 and len(caption_indexes) == 1:
			footer_index, image_index = caption_footer_indexes[0], caption_indexes[0]
			footer, image = components[footer_index], components[image_index]
			overlap = vertical_overlap(emission_flow.component_footprints(image)[-1], footer.bounds)
			if emission_flow.shallow_broad_footer(components, footer) and 0.0 < overlap <= emission_flow.FOOTER_IMAGE_PADDING_RATIO and \
				not geometry.substantially_overlaps(emission_flow.component_footprints(image)[0], footer.bounds):
				record = pair_permission(components, footer_index, image_index, "caption-footer-padding", "two-plus-one-panels")
				if record is not None:
					records.append(record)
	return tuple(records)


#============================================
def pair_permission(components: list[emission_flow.EmissionComponent], first_index: int, second_index: int,
		relation: str, layout: str) -> OverlapPermission | None:
	"""Record one exact pair only after the full component set selects its native layout."""
	try:
		selected, _slots, order = component_layout(components)
	except ValueError:
		return None
	if selected != layout:
		return None
	if first_index > second_index:
		first_index, second_index = second_index, first_index
	first, second = components[first_index], components[second_index]
	return OverlapPermission(first_index, second_index, relation, emission_flow.component_footprints(first),
		emission_flow.component_footprints(second), max(vertical_overlap(left, right) for left in emission_flow.component_footprints(first)
		for right in emission_flow.component_footprints(second)), selected, order)


#============================================
def vertical_overlap(first: geometry.NormalizedBounds, second: geometry.NormalizedBounds) -> float:
	"""Measure signed vertical intersection for a recorded source-padding relation."""
	return min(first.bottom, second.bottom) - max(first.top, second.top)


#============================================
def bottom_footer_structure(components: list[emission_flow.EmissionComponent], footer_index: int) -> bool:
	"""Validate one merged footer against exactly two disjoint top peers."""
	footer = components[footer_index]
	peers = [item for index, item in enumerate(components) if index != footer_index]
	return len(peers) == 2 and not emission_flow.raw_components_overlap(peers) and emission_flow.shallow_broad_footer(components, footer) and \
		all(footprint.top >= peer.bounds.bottom - emission_flow.column_footer_padding(peer)
			for footprint in emission_flow.component_footprints(footer) for peer in peers)


#============================================
def coarse_image_geometry(components: list[emission_flow.EmissionComponent]) -> bool:
	"""Recognize source geometry eligible for the explicit coarse-picture relation."""
	if len(components) != 2:
		return False
	coarse = next((item for item in components if item.kind == "text" and item.coarse_text_container), None)
	image = next((item for item in components if item.kind == "image" and item.source_kind == "picture"), None)
	if coarse is None or image is None or len(emission_flow.component_footprints(coarse)) != 1 or len(emission_flow.component_footprints(image)) != 1:
		return False
	coarse_center_y = (coarse.bounds.top + coarse.bounds.bottom) / 2
	image_center_y = (image.bounds.top + image.bounds.bottom) / 2
	coarse_center_x = (coarse.bounds.left + coarse.bounds.right) / 2
	image_center_x = (image.bounds.left + image.bounds.right) / 2
	if abs(coarse_center_y - image_center_y) > min(coarse.bounds.height, image.bounds.height) * COARSE_IMAGE_ROW_CENTER_RATIO or \
		abs(coarse_center_x - image_center_x) < min(coarse.bounds.width, image.bounds.width) * COARSE_IMAGE_SIDE_BY_SIDE_RATIO:
		return False
	return True


#============================================
def gallery_eligible(components: list[emission_flow.EmissionComponent]) -> bool:
	"""Allow gallery only for equal-status, non-overlapping image components."""
	if not 2 <= len(components) <= 6 or not all(item.kind == "image" for item in components):
		return False
	if components_overlap(components):
		return False
	areas = [item.bounds.width * item.bounds.height for item in components]
	aspects = [item.bounds.width / item.bounds.height for item in components]
	if max(areas) > min(areas) * GALLERY_AREA_VARIATION_RATIO or \
		max(aspects) > min(aspects) * GALLERY_ASPECT_VARIATION_RATIO:
		return False
	if len(components) == 2:
		return False
	if len(components) == 3:
		centers_x = [(item.bounds.left + item.bounds.right) / 2 for item in components]
		centers_y = [(item.bounds.top + item.bounds.bottom) / 2 for item in components]
		return (
			min(centers_x) < max(centers_x) and
			max(centers_y) - min(centers_y) <= GALLERY_LINE_CENTER_TOLERANCE
		) or (
			min(centers_y) < max(centers_y) and
			max(centers_x) - min(centers_x) <= GALLERY_LINE_CENTER_TOLERANCE
		)
	try:
		component_layout(components)
	except ValueError:
		return False
	return True


#============================================
def component_layout(components: list[emission_flow.EmissionComponent]) -> tuple[str, tuple[str, ...], tuple[int, ...]]:
	"""Match source components to native cell geometry without source-specific rules."""
	if not 1 <= len(components) <= 6:
		raise ValueError("source components require manual layout review before Djot emission")
	if coarse_inset_key_layout(components):
		return "two-panels", slide_lib.layout_registry.contract_for("two-panels").slot_names, (0, 1)
	if coarse_picture_inset_layout(components):
		picture_index = next(index for index, item in enumerate(components) if item.kind == "image")
		body_index = next(index for index, item in enumerate(components) if item.kind == "text")
		return "two-panels", slide_lib.layout_registry.contract_for("two-panels").slot_names, (picture_index, body_index) \
			if components[picture_index].classification_reason.endswith(":left") else (body_index, picture_index)
	footer_match = bottom_footer_layout(components)
	if footer_match is not None:
		_score, order = footer_match
		return "two-over-one-panels", slide_lib.layout_registry.contract_for("two-over-one-panels").slot_names, order
	explanatory_match = asymmetric_explanatory_pair_layout(components)
	if explanatory_match is not None:
		_score, order = explanatory_match
		return "two-panels", slide_lib.layout_registry.contract_for("two-panels").slot_names, order
	match = topology.ordinary_layout_match(
		tuple(component.bounds for component in components), not coarse_image_geometry(components),
	)
	if match is None:
		bounds = ", ".join(str(component.bounds) for component in components)
		raise ValueError(f"ambiguous topology bounds [{bounds}]")
	name, order = match
	return name, slide_lib.layout_registry.contract_for(name).slot_names, order


#============================================
def coarse_inset_key_layout(components: list[emission_flow.EmissionComponent]) -> bool:
	"""Assign one body and wholly contained compact key to the existing two panels."""
	if len(components) != 2:
		return False
	body = next((item for item in components if item.coarse_text_container), None)
	key = next((item for item in components if item is not body), None)
	return body is not None and key is not None and key.source_kind == "native-reconstruction" and \
		key.classification_reason == "styled-inset-key" and \
		key.bounds.left >= .65 and key.bounds.width <= .25 and key.bounds.height <= .20 and \
		body.bounds.left <= key.bounds.left and key.bounds.right <= body.bounds.right and \
		body.bounds.top <= key.bounds.top and key.bounds.bottom <= body.bounds.bottom


#============================================
def coarse_picture_inset_layout(components: list[emission_flow.EmissionComponent]) -> bool:
	"""Assign one proven coarse body and direct picture inset to opposite panels."""
	if len(components) != 2 or any(not item.classification_reason.startswith("coarse-body-picture-inset:") for item in components):
		return False
	return sum(item.kind == "text" and item.coarse_text_container for item in components) == 1 and \
		sum(item.kind == "image" and item.source_kind == "picture" for item in components) == 1 and \
		len({item.classification_reason for item in components}) == 1


#============================================
def bottom_footer_layout(components: list[emission_flow.EmissionComponent]) -> tuple[float, tuple[int, ...]] | None:
	"""Accept only a unique same-band peer/footer relation within its local score ceiling."""
	footer_indexes = [index for index, item in enumerate(components) if item.kind == "flow" and
		item.source_kind == "text-box" and item.classification_reason == emission_flow.BOTTOM_FOOTER_RELATION_REASON]
	if len(components) != 3 or len(footer_indexes) != 1 or not bottom_footer_structure(components, footer_indexes[0]):
		return None
	peers = [item for index, item in enumerate(components) if index != footer_indexes[0]]
	if not topology.material(peers[0].bounds.top, peers[0].bounds.height, peers[1].bounds.top, peers[1].bounds.height):
		return None
	source = topology.normalized_boxes(tuple(component.bounds for component in components))
	slots = slide_lib.layout_registry.contract_for("two-over-one-panels").topology_slots
	matches = [(topology.score(source, slots, order), order) for order in itertools.permutations(range(3))
		if order[2] == footer_indexes[0] and topology.relations_match(source, slots, order)]
	if not matches:
		return None
	score = min(item[0] for item in matches)
	if score > BOTTOM_FOOTER_SCORE_CEILING:
		return None
	order = min(item for item_score, item in matches if abs(item_score - score) <= 1e-9)
	return score, order


#============================================
def asymmetric_explanatory_pair_layout(components: list[emission_flow.EmissionComponent]) -> tuple[float, tuple[int, ...]] | None:
	"""Accept one aligned, disjoint coarse-plus-compact text pair at a local ceiling."""
	if not asymmetric_explanatory_pair(components):
		return None
	source = topology.normalized_boxes(tuple(component.bounds for component in components))
	candidates: list[tuple[str, list[tuple[float, tuple[int, ...]]]]] = []
	for name in slide_lib.layout_registry.names():
		spec = slide_lib.layout_registry.contract_for(name)
		if not spec.topology_matchable or spec.cell_count != 2:
			continue
		slots = spec.topology_slots
		matches = [(topology.score(source, slots, order), order) for order in itertools.permutations(range(2))
			if topology.relations_match(source, slots, order)]
		if matches:
			candidates.append((spec.name, matches))
	if [name for name, _matches in candidates] != ["two-panels"]:
		return None
	matches = candidates[0][1]
	score = min(item[0] for item in matches)
	if score > ASYMMETRIC_EXPLANATORY_PAIR_MAX_SCORE:
		return None
	order = min(item for item_score, item in matches if abs(item_score - score) <= 1e-9)
	return score, order


#============================================
def asymmetric_explanatory_pair(components: list[emission_flow.EmissionComponent]) -> bool:
	"""Recognize only two direct, aligned textual components with asymmetric roles."""
	if len(components) != 2 or any(item.kind != "text" or not any(line.strip() for line in item.lines) or
		item.source_kind in {"table", "native-reconstruction"} or item.classification_reason or
		len(emission_flow.component_footprints(item)) != 1 for item in components):
		return False
	coarse = [item for item in components if item.coarse_text_container]
	compact = [item for item in components if not item.coarse_text_container]
	if len(coarse) != 1 or len(compact) != 1 or compact[0].placeholder_confidence != 0.0 or \
		emission_flow.raw_components_overlap(components):
		return False
	large, small = coarse[0], compact[0]
	if small.bounds.width * small.bounds.height > large.bounds.width * large.bounds.height * \
		ASYMMETRIC_EXPLANATORY_COMPACT_AREA_RATIO:
		return False
	left, right = sorted(components, key=lambda item: item.bounds.left)
	return right.bounds.left - left.bounds.right >= 0.05 and abs(left.bounds.top - right.bounds.top) <= 0.03
