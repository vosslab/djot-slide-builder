"""Recognition and ownership of coupled visual content regions."""
import dataclasses
import itertools
import slide_lib.importers.geometry as geometry
import slide_lib.importers.rotated_vector_label as rotated_vector_label
import slide_lib.importers.source_regions as source_regions

CONTENT_IMAGE_MIN_AREA_RATIO = 0.12
SINGLE_ANNOTATION_IMAGE_MIN_AREA_RATIO = 0.50
ANNOTATION_MINIMUM_COUNT = 2
ANNOTATION_CENTER_SPAN_RATIO = 0.12
ANNOTATION_PROXIMITY_RATIO = 0.08
VECTOR_COMPONENT_PROXIMITY_RATIO = 0.08
RELATION_EDGE_LABEL_PADDING = 0.02
TINY_DECORATIVE_VECTOR_AREA_RATIO = 0.002
TINY_DECORATIVE_VECTOR_SPAN_RATIO = 0.04
SHARED_FIGURE_ROW_ALIGNMENT_RATIO = 0.06
SHARED_FIGURE_CAPTION_MIN_SPAN_RATIO = 0.50
CONNECTOR_AXIAL_OVERLAP_RATIO = 0.50
CONNECTOR_PERPENDICULAR_PROXIMITY_RATIO = 0.04
CONTAINED_VECTOR_LABEL_MAX_PARAGRAPHS = 3
REPEATED_LABEL_SIDE_GAP_RATIO = 0.08
REPEATED_LABEL_CENTER_TOLERANCE_RATIO = 0.10
SIDE_LABEL_BORDER_OVERLAP = 0.02

@dataclasses.dataclass(frozen=True)
class ContentRegionPlan:
	"""A coupled visual component requiring native normalization or review."""
	region_key: str
	bounds: geometry.NormalizedBounds
	text_regions: tuple[source_regions.SourceTextRegion, ...]
	image_regions: tuple[source_regions.SourceImageRegion, ...]
	kind: str = "diagram"
	classification_reason: str = "qualified pictorial annotation component"
	local_heading: source_regions.SourceTextRegion | None = None

def center_is_near_image(inner: geometry.NormalizedBounds,
		image: geometry.NormalizedBounds) -> bool:
	"""Keep nearby diagram labels in a bounded envelope scaled to its anchor."""
	center_x = (inner.left + inner.right) / 2
	center_y = (inner.top + inner.bottom) / 2
	margin_x = image.width * ANNOTATION_PROXIMITY_RATIO
	margin_y = image.height * ANNOTATION_PROXIMITY_RATIO
	return (
		image.left - margin_x <= center_x <= image.right + margin_x
		and image.top - margin_y <= center_y <= image.bottom + margin_y
	)


def annotation_centers_are_distributed(
		annotations: tuple[source_regions.SourceTextRegion, ...],
) -> bool:
	"""Require several labels to occupy a real diagram component, not one caption."""
	centers_x = tuple((item.bounds.left + item.bounds.right) / 2 for item in annotations)
	centers_y = tuple((item.bounds.top + item.bounds.bottom) / 2 for item in annotations)
	return (
		max(centers_x) - min(centers_x) >= ANNOTATION_CENTER_SPAN_RATIO
		or max(centers_y) - min(centers_y) >= ANNOTATION_CENTER_SPAN_RATIO
	)

def content_region(
	text_regions: tuple[source_regions.SourceTextRegion, ...],
	image_regions: tuple[source_regions.SourceImageRegion, ...],
	title_region: source_regions.SourceTextRegion | None,
) -> ContentRegionPlan | None:
	"""Plan one diagram-plus-annotation region without flattening its labels."""
	if not image_regions:
		return None
	available_text = tuple(region for region in text_regions if region is not title_region)
	for image_index, image in enumerate(image_regions, start=1):
		if image.source_kind not in {"picture", "vector"} or \
			image.bounds.width * image.bounds.height < CONTENT_IMAGE_MIN_AREA_RATIO:
			continue
		qualifying_annotations = tuple(
			region for region in available_text
			if (
				(center_is_near_image(region.bounds, image.bounds)
				or geometry.overlaps_or_contains(region.bounds, image.bounds))
				and region.placeholder_confidence == 0.0
			)
		)
		single_interior = tuple(region for region in available_text if (
			region.source_kind == "auto-shape"
			and region.placeholder_confidence == 0.0
			and geometry.center_is_within(region.bounds, image.bounds)
		))
		single_caption_qualified = (
			image.bounds.width * image.bounds.height >= SINGLE_ANNOTATION_IMAGE_MIN_AREA_RATIO
			and len(image_regions) == 1
			and len(single_interior) == 1
			and all(
				region is single_interior[0] or (
					region.source_kind == "auto-shape"
					and region.placeholder_confidence == 0.0
					and not center_is_near_image(region.bounds, image.bounds)
					and not geometry.overlaps_or_contains(region.bounds, image.bounds)
				)
				for region in available_text
			)
		)
		if (
			len(qualifying_annotations) >= ANNOTATION_MINIMUM_COUNT
			and annotation_centers_are_distributed(qualifying_annotations)
		) or single_caption_qualified:
			component_images = {image}
			while True:
				updated = component_images | {
					other for other in image_regions
					if other.source_kind != "connector"
					if any(
						geometry.overlaps_or_contains(other.bounds, member.bounds)
						or bounds_are_near(other.bounds, member.bounds)
						for member in component_images
					)
				}
				if updated == component_images:
					break
				component_images = updated
			annotations = tuple(sorted((
				region for region in available_text
				if (
					region.placeholder_confidence == 0.0
					and (
						any(center_is_near_image(region.bounds, member.bounds)
							or geometry.overlaps_or_contains(region.bounds, member.bounds)
							for member in component_images)
					)
				)
			), key=lambda region: region.source_ordinal,
			))
			bounds = next(iter(component_images)).bounds
			for member in component_images:
				bounds = bounds.union(member.bounds)
			for annotation in annotations:
				bounds = bounds.union(annotation.bounds)
			return ContentRegionPlan(
				region_key=f"content-region-{image_index}",
				bounds=bounds,
				text_regions=annotations,
				image_regions=tuple(sorted(component_images, key=lambda item: item.source_ordinal)),
				kind="diagram",
				classification_reason="distributed pictorial annotations",
			)
	rotated = rotated_vector_label.rotated_vector_label_members(available_text, image_regions)
	if rotated is not None:
		return ContentRegionPlan(
			"rotated-vector-label-1", rotated.bounds, rotated.text_regions, rotated.image_regions,
			"rotated-vector-label", "unique connected rotated vector-label graph",
		)
	vector_region = vector_scaffold_region(available_text, image_regions)
	if vector_region is not None:
		return vector_region
	return mixed_visual_region(available_text, image_regions)
def vector_scaffold_region(
	available_text: tuple[source_regions.SourceTextRegion, ...],
	image_regions: tuple[source_regions.SourceImageRegion, ...],
) -> ContentRegionPlan | None:
	"""Retain one connected vector scaffold with its distributed native labels."""
	vectors = tuple(image for image in image_regions if image.source_kind in {"vector", "connector"})
	if len(vectors) < 2:
		return None
	annotations = tuple(region for region in available_text if region.placeholder_confidence == 0.0)
	if len(annotations) < ANNOTATION_MINIMUM_COUNT or not annotation_centers_are_distributed(annotations):
		return None
	nodes = (*vectors, *annotations)
	connected = {0}
	while True:
		updated = set(connected)
		for index in connected:
			for other_index, other in enumerate(nodes):
				if other_index in connected:
					continue
				first = nodes[index].bounds
				second = other.bounds
				if geometry.overlaps_or_contains(first, second) or bounds_are_near(first, second):
					updated.add(other_index)
		if updated == connected:
			break
		connected = updated
	if len(connected) != len(nodes):
		return None
	bounds = nodes[0].bounds
	for node in nodes[1:]:
		bounds = bounds.union(node.bounds)
	return ContentRegionPlan(
		"vector-component-1", bounds, tuple(sorted(annotations, key=lambda item: item.source_ordinal)),
		tuple(sorted(vectors, key=lambda item: item.source_ordinal)),
		"vector-scaffold", "connected vector scaffold with distributed annotations",
	)
def bounds_are_near(first: geometry.NormalizedBounds,
		second: geometry.NormalizedBounds) -> bool:
	"""Connect source scaffolds only across a bounded slide-relative gap."""
	return not (
		first.right + VECTOR_COMPONENT_PROXIMITY_RATIO < second.left
		or second.right + VECTOR_COMPONENT_PROXIMITY_RATIO < first.left
		or first.bottom + VECTOR_COMPONENT_PROXIMITY_RATIO < second.top
		or second.bottom + VECTOR_COMPONENT_PROXIMITY_RATIO < first.top
	)
def mixed_visual_region(
	available_text: tuple[source_regions.SourceTextRegion, ...],
	image_regions: tuple[source_regions.SourceImageRegion, ...],
) -> ContentRegionPlan | None:
	"""Reserve one irreducibly coupled mixed visual graph for renderer ownership."""
	if any(region.source_kind == "table" for region in available_text):
		return None
	anchors = tuple(image for image in image_regions if image.source_kind in {"picture", "vector"})
	if not anchors:
		return None
	# Coarse placeholders are containers, not proof that nearby ink is coupled.
	# Keep them native while evaluating only the independent visual/text graph.
	nodes = (*anchors, *(region for region in available_text if region.placeholder_confidence < 0.75))
	edges = {
		(index, other_index)
		for index, node in enumerate(nodes)
		for other_index, other in enumerate(nodes[index + 1:], start=index + 1)
		if geometry.overlaps_or_contains(node.bounds, other.bounds) or bounds_are_near(node.bounds, other.bounds)
	}
	if not edges:
		return None
	components: list[set[int]] = []
	remaining = set(range(len(nodes)))
	while remaining:
		component = {remaining.pop()}
		while True:
			updated = set(component)
			for first, second in edges:
				if first in component:
					updated.add(second)
				if second in component:
					updated.add(first)
			if updated == component:
				break
			component = updated
		remaining.difference_update(component)
		components.append(component)
	candidates = tuple(component for component in components if (
		any(isinstance(nodes[index], source_regions.SourceImageRegion) for index in component)
		and any(
			geometry.strictly_overlaps(anchor.bounds, other.bounds)
			for anchor in (nodes[index] for index in component
				if isinstance(nodes[index], source_regions.SourceImageRegion))
			for other in (nodes[index] for index in component)
			if other is not anchor
		)
		and (
			any(
				isinstance(nodes[index], source_regions.SourceTextRegion)
				and nodes[index].source_kind in {"auto-shape", "text-box"}
				for index in component
			)
			or sum(isinstance(nodes[index], source_regions.SourceImageRegion) for index in component) >= 2
		)
	))
	if len(candidates) != 1:
		return None
	member_indexes = candidates[0]
	text_members = tuple(nodes[index] for index in member_indexes if isinstance(nodes[index], source_regions.SourceTextRegion))
	anchor_members = tuple(nodes[index] for index in member_indexes if isinstance(nodes[index], source_regions.SourceImageRegion))
	bounds = nodes[next(iter(member_indexes))].bounds
	for index in member_indexes:
		node = nodes[index]
		bounds = bounds.union(node.bounds)
	if bounds.left == 0.0 and bounds.top == 0.0 and bounds.right == 1.0 and bounds.bottom == 1.0:
		return None
	return ContentRegionPlan(
		"mixed-visual-1", bounds, tuple(sorted(text_members, key=lambda item: item.source_ordinal)),
		tuple(sorted(anchor_members, key=lambda item: item.source_ordinal)),
		"mixed-visual", "single connected materially coupled visual graph",
	)
def shared_figure_row_region(
	text_regions: tuple[source_regions.SourceTextRegion, ...],
	image_regions: tuple[source_regions.SourceImageRegion, ...],
	title_region: source_regions.SourceTextRegion | None,
) -> ContentRegionPlan | None:
	"""Keep a shared caption with a coherent row of peer source figures."""
	images = tuple(image for image in image_regions if image.source_kind == "picture")
	available = tuple(region for region in text_regions if region is not title_region)
	candidates: list[tuple[tuple[source_regions.SourceImageRegion, ...], source_regions.SourceTextRegion]] = []
	for count in (2, 3):
		for row in itertools.combinations(images, count):
			if not coherent_figure_row(row):
				continue
			bounds = union_bounds(tuple(item.bounds for item in row))
			captions = tuple(region for region in available if shared_row_caption(region, bounds))
			if len(captions) == 1:
				candidates.append((row, captions[0]))
	maximal = tuple(candidate for candidate in candidates if not any(
		candidate[1] is other[1] and set(candidate[0]) < set(other[0])
		for other in candidates
	))
	if len(maximal) != 1:
		return None
	row, caption = maximal[0]
	bounds = union_bounds((*tuple(item.bounds for item in row), caption.bounds))
	return ContentRegionPlan(
		"shared-figure-row-1", bounds, (caption,), row,
		"shared-figure-row", "peer figure row with one shared caption",
	)
def coherent_figure_row(row: tuple[source_regions.SourceImageRegion, ...]) -> bool:
	"""Recognize two or three separated, similarly sized figures in one row."""
	if len(row) not in {2, 3} or any(geometry.substantially_overlaps(first.bounds, second.bounds)
		for index, first in enumerate(row) for second in row[index + 1:]):
		return False
	centers = tuple((item.bounds.top + item.bounds.bottom) / 2 for item in row)
	return max(centers) - min(centers) <= SHARED_FIGURE_ROW_ALIGNMENT_RATIO
def shared_row_caption(region: source_regions.SourceTextRegion,
		row: geometry.NormalizedBounds) -> bool:
	"""Require a non-placeholder caption immediately beneath the full figure row."""
	center = (region.bounds.left + region.bounds.right) / 2
	row_center = (row.left + row.right) / 2
	return (
		region.placeholder_confidence == 0.0
		and region.bounds.top >= row.bottom - geometry.FLOW_BORDER_CONTACT_RATIO
		and region.bounds.top - row.bottom <= min(0.10, row.height * 0.25)
		and region.bounds.width >= row.width * SHARED_FIGURE_CAPTION_MIN_SPAN_RATIO
		and (abs(center - row_center) <= SHARED_FIGURE_ROW_ALIGNMENT_RATIO
			or region.bounds.left <= row.left and row.right <= region.bounds.right)
	)
def repeated_labeled_figure_region(
	text_regions: tuple[source_regions.SourceTextRegion, ...], image_regions: tuple[source_regions.SourceImageRegion, ...],
	title_region: source_regions.SourceTextRegion | None,
) -> ContentRegionPlan | None:
	"""Reserve two same-band figures only when their side labels are mutual."""
	pictures = tuple(item for item in image_regions if item.source_kind == "picture")
	available = tuple(item for item in text_regions if item is not title_region)
	if len(image_regions) != 2 or len(pictures) != 2 or len(available) != 2 or any(geometry.overlaps_or_contains(first.bounds, second.bounds)
		for first, second in ((pictures[0], pictures[1]),)):
		return None
	if abs((pictures[0].bounds.top + pictures[0].bounds.bottom - pictures[1].bounds.top - pictures[1].bounds.bottom) / 2) > SHARED_FIGURE_ROW_ALIGNMENT_RATIO:
		return None
	labels = tuple(item for item in available if item.source_kind == "auto-shape"
		and item.placeholder_confidence == 0.0 and len(item.paragraphs) <= 2)
	if len(labels) != 2:
		return None
	pairs = tuple((picture, nearest_side_label(picture, labels)) for picture in pictures)
	if any(label is None for _picture, label in pairs) or len({label for _picture, label in pairs}) != 2:
		return None
	if any(nearest_side_picture(label, pictures) is not picture for picture, label in pairs):
		return None
	bounds = union_bounds((*tuple(item.bounds for item in pictures), *(label.bounds for _picture, label in pairs)))
	return ContentRegionPlan("repeated-labeled-figure-1", bounds, tuple(label for _picture, label in pairs),
		pictures, "repeated-labeled-figure", "mutual same-band side labels")
def nearest_side_label(picture: source_regions.SourceImageRegion, labels: tuple[source_regions.SourceTextRegion, ...]) -> source_regions.SourceTextRegion | None:
	"""Return one unique, vertically aligned neighboring auto-shape label."""
	candidates = tuple((side_gap(label.bounds, picture.bounds), label) for label in labels
		if is_side_label(label.bounds, picture.bounds)
		and side_gap(label.bounds, picture.bounds) <= REPEATED_LABEL_SIDE_GAP_RATIO
		and abs((label.bounds.top + label.bounds.bottom - picture.bounds.top - picture.bounds.bottom) / 2) <= REPEATED_LABEL_CENTER_TOLERANCE_RATIO)
	if not candidates:
		return None
	minimum = min(distance for distance, _label in candidates)
	nearest = tuple(label for distance, label in candidates if abs(distance - minimum) <= 1e-9)
	return nearest[0] if len(nearest) == 1 else None
def side_gap(label: geometry.NormalizedBounds,
		picture: geometry.NormalizedBounds) -> float:
	"""Return horizontal separation for a disjoint side label."""
	return max(picture.left - label.right, label.left - picture.right, 0.0)
def nearest_side_picture(label: source_regions.SourceTextRegion, pictures: tuple[source_regions.SourceImageRegion, ...]) -> source_regions.SourceImageRegion | None:
	"""Confirm a label also has one unique neighboring picture."""
	candidates = tuple((side_gap(label.bounds, picture.bounds), picture) for picture in pictures
		if is_side_label(label.bounds, picture.bounds)
		and side_gap(label.bounds, picture.bounds) <= REPEATED_LABEL_SIDE_GAP_RATIO)
	minimum = min(distance for distance, _picture in candidates)
	nearest = tuple(picture for distance, picture in candidates if abs(distance - minimum) <= 1e-9)
	return nearest[0] if len(nearest) == 1 else None
def side_of(label: geometry.NormalizedBounds,
		picture: geometry.NormalizedBounds) -> str:
	"""Classify a side label relative to one picture."""
	return "left" if (label.left + label.right) / 2 < (picture.left + picture.right) / 2 else "right"
def is_side_label(label: geometry.NormalizedBounds,
		picture: geometry.NormalizedBounds) -> bool:
	"""Allow only a tiny border overlap when a label center remains lateral."""
	return (label.right <= picture.left + SIDE_LABEL_BORDER_OVERLAP
		if side_of(label, picture) == "left"
		else label.left >= picture.right - SIDE_LABEL_BORDER_OVERLAP)
def union_bounds(bounds: tuple[geometry.NormalizedBounds, ...]) -> geometry.NormalizedBounds:
	"""Return the bounded union for a nonempty set of source rectangles."""
	result = bounds[0]
	for item in bounds[1:]:
		result = result.union(item)
	return result
def title_is_component_member(
	title_region: source_regions.SourceTextRegion | None,
	content: ContentRegionPlan | None,
) -> bool:
	"""Keep an unmarked heading inside the visual component it labels."""
	if title_region is None or content is None:
		return False
	if title_region.placeholder_confidence > 0.0:
		return False
	return any(geometry.center_is_within(title_region.bounds, image.bounds)
		for image in content.image_regions)
def absorb_connected_connectors(
	content: ContentRegionPlan | None,
	image_regions: tuple[source_regions.SourceImageRegion, ...],
) -> ContentRegionPlan | None:
	"""Add uniquely aligned visible connectors to an already-coupled source region."""
	if content is None:
		return None
	connectors = tuple(item for item in image_regions if item.source_kind == "connector"
		and item not in content.image_regions and connector_belongs_to(item.bounds, content.bounds))
	if not connectors:
		return content
	bounds = union_bounds((content.bounds, *(item.bounds for item in connectors)))
	return dataclasses.replace(content, bounds=bounds,
		image_regions=tuple(sorted((*content.image_regions, *connectors), key=lambda item: item.source_ordinal)),
		classification_reason=f"{content.classification_reason}; aligned connectors")
def absorb_coarse_relation_text(
	content: ContentRegionPlan | None,
	text_regions: tuple[source_regions.SourceTextRegion, ...],
	title_region: source_regions.SourceTextRegion | None,
) -> ContentRegionPlan | None:
	"""Assign one short coarse placeholder only when its shape belongs to the relation."""
	if content is None:
		return None
	candidates = tuple(region for region in text_regions if (
		region is not title_region and region not in content.text_regions
		and region.source_kind != "table" and region.placeholder_confidence >= 0.75
		and len(region.paragraphs) <= 2 and bounds_contains(content.bounds, region.bounds, RELATION_EDGE_LABEL_PADDING)
	))
	if len(candidates) != 1:
		return content
	region = candidates[0]
	bounds = content.bounds.union(region.bounds)
	if bounds.left == 0.0 and bounds.top == 0.0 and bounds.right == 1.0 and bounds.bottom == 1.0:
		raise ValueError("coarse relation expansion would cover the full slide")
	return dataclasses.replace(content, bounds=bounds,
		text_regions=tuple(sorted((*content.text_regions, region), key=lambda item: item.source_ordinal)),
		classification_reason=f"{content.classification_reason}; enclosed coarse text")
def absorb_contained_vector_label(
	content: ContentRegionPlan | None, text_regions: tuple[source_regions.SourceTextRegion, ...],
	title_region: source_regions.SourceTextRegion | None,
) -> ContentRegionPlan | None:
	"""Keep one short coarse label with its already-qualified vector scaffold."""
	if content is None:
		return None
	vectors = tuple(item for item in content.image_regions if item.source_kind in {"vector", "connector"})
	candidates = tuple(region for region in text_regions if region is not title_region
		and region not in content.text_regions and region.source_kind != "table"
		and region.placeholder_confidence >= 0.75 and len(region.paragraphs) <= CONTAINED_VECTOR_LABEL_MAX_PARAGRAPHS
		and sum(bounds_contains(vector.bounds, region.bounds, 0.0) for vector in vectors) == 1)
	if len(candidates) != 1:
		return content
	region = candidates[0]
	return dataclasses.replace(content,
		text_regions=tuple(sorted((*content.text_regions, region), key=lambda item: item.source_ordinal)),
		classification_reason=f"{content.classification_reason}; contained vector label")
def bounds_contains(outer: geometry.NormalizedBounds,
		inner: geometry.NormalizedBounds, padding: float) -> bool:
	"""Require center and every edge within a bounded relation padding envelope."""
	return (outer.left - padding <= inner.left and inner.right <= outer.right + padding
		and outer.top - padding <= inner.top and inner.bottom <= outer.bottom + padding
		and geometry.center_is_within(inner, outer))
def connector_belongs_to(connector: geometry.NormalizedBounds,
		content: geometry.NormalizedBounds) -> bool:
	"""Require a long-axis projection and close cross-axis relation to one component."""
	horizontal = connector.width >= connector.height
	axis_start, axis_end = (connector.left, connector.right) if horizontal else (connector.top, connector.bottom)
	content_start, content_end = (content.left, content.right) if horizontal else (content.top, content.bottom)
	axis_overlap = max(0.0, min(axis_end, content_end) - max(axis_start, content_start))
	perpendicular_gap = max(
		(content.top - connector.bottom if horizontal else content.left - connector.right),
		(connector.top - content.bottom if horizontal else connector.left - content.right), 0.0,
	)
	return axis_overlap >= (axis_end - axis_start) * CONNECTOR_AXIAL_OVERLAP_RATIO and \
		perpendicular_gap <= CONNECTOR_PERPENDICULAR_PROXIMITY_RATIO
def decorative_vectors(
	text_regions: tuple[source_regions.SourceTextRegion, ...], image_regions: tuple[source_regions.SourceImageRegion, ...],
) -> tuple[source_regions.SourceImageRegion, ...]:
	"""Omit only isolated tiny vectors; long or related marks remain reviewable."""
	return tuple(item for item in image_regions if item.source_kind in {"vector", "connector"}
		and item.bounds.width * item.bounds.height < TINY_DECORATIVE_VECTOR_AREA_RATIO
		and max(item.bounds.width, item.bounds.height) < TINY_DECORATIVE_VECTOR_SPAN_RATIO
		and not any(bounds_are_near(item.bounds, other.bounds) for other in (*text_regions, *image_regions)
			if other is not item))
