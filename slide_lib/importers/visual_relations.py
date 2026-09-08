"""Conservative geometry relations for exceptional imported-deck visual regions.

The helpers deliberately return only source membership and normalized bounds.
Planning owns classification and emission; this module does not import it.
"""

# Standard Library
import dataclasses
from collections.abc import Callable

# Local modules
import slide_lib.importers.geometry as geometry


NEARBY_GAP_RATIO = 0.03
CALLOUT_LEFT_TOLERANCE_RATIO = 0.05
CALLOUT_MIN_WIDTH_RATIO = 0.5
CALLOUT_MAX_WIDTH_RATIO = 2.0
CALLOUT_CANDIDATE_MAX_PARAGRAPHS = 2
CALLOUT_ANCHOR_MAX_PARAGRAPHS = 4
INSET_MAX_RELATIVE_SIZE = 0.25
DOMINANT_MIN_AREA_MULTIPLIER = 4.0
SEQUENCE_CENTER_SPAN_RATIO = 0.10
SEQUENCE_ASPECT_RATIO_VARIATION = 1.5
CAPTION_MAX_VERTICAL_GAP_RATIO = .12
CAPTION_CENTER_ALIGNMENT_RATIO = .18
CAPTION_MAX_PARAGRAPHS = 2
CAPTION_BORDER_CONTACT_RATIO = .01
CAPTION_MIN_HORIZONTAL_OVERLAP_RATIO = .50
CAPTION_MAX_WIDTH_TO_IMAGE_RATIO = 1.60


@dataclasses.dataclass(frozen=True)
class VisualRelationMembers:
	"""Exact source membership and crop evidence for one visual relation."""

	text_regions: tuple[object, ...]
	image_regions: tuple[object, ...]
	bounds: geometry.NormalizedBounds
	protected_text_shape_ids: tuple[int, ...] = ()


@dataclasses.dataclass(frozen=True)
class CoarseInsetMembers:
	"""One editable body and its independently editable styled inset key."""

	body: object
	key: object


@dataclasses.dataclass(frozen=True)
class CoarsePictureInsetMembers:
	"""One transparent object body and its direct, small picture inset."""

	body: object
	picture: object
	picture_slot: str


def caption_pairings(texts: tuple[object, ...], images: tuple[object, ...]) -> dict[object, object]:
	"""Pair only mutually nearest short captions directly below a direct picture."""
	candidates: list[tuple[float, object, object]] = []
	for image in images:
		for text in texts:
			gap = text.bounds.top - image.bounds.bottom
			center = abs((text.bounds.left + text.bounds.right - image.bounds.left - image.bounds.right) / 2)
			overlap = min(text.bounds.right, image.bounds.right) - max(text.bounds.left, image.bounds.left)
			if getattr(image, "source_kind", None) == "picture" and getattr(text, "placeholder_confidence", 1.0) == 0.0 and \
				getattr(text, "source_kind", None) != "text" and len(text.paragraphs) <= CAPTION_MAX_PARAGRAPHS and \
				text.bounds.width <= image.bounds.width * CAPTION_MAX_WIDTH_TO_IMAGE_RATIO and \
				-CAPTION_BORDER_CONTACT_RATIO <= gap <= CAPTION_MAX_VERTICAL_GAP_RATIO and \
				(overlap / min(text.bounds.width, image.bounds.width) >= CAPTION_MIN_HORIZONTAL_OVERLAP_RATIO or center <= image.bounds.width * CAPTION_CENTER_ALIGNMENT_RATIO):
				candidates.append((gap + center, image, text))
	pairs: dict[object, object] = {}
	for _distance, image, text in candidates:
		by_text = nearest_caption_pair(tuple(item for item in candidates if item[2] is text))
		by_image = nearest_caption_pair(tuple(item for item in candidates if item[1] is image))
		if by_text is not None and by_image is not None and by_text[1] is image and by_image[2] is text:
			pairs[image] = text
	return pairs


def nearest_caption_pair(candidates: tuple[tuple[float, object, object], ...]) -> tuple[float, object, object] | None:
	"""Return one nearest candidate, rejecting exact-distance ties."""
	distance = min(item[0] for item in candidates)
	nearest = tuple(item for item in candidates if abs(item[0] - distance) <= 1e-9)
	return nearest[0] if len(nearest) == 1 else None


def styled_callout_extension(
	content: object, texts: tuple[object, ...], title: object,
) -> VisualRelationMembers | None:
	"""Extend one vector-bearing region with one matched exterior styled callout."""
	if content is None or not any(
		getattr(image, "source_kind", None) in {"vector", "connector"}
		for image in content.image_regions
	):
		return None
	exterior = tuple(
		region for region in texts
		if region is not getattr(title, "region", None) and region not in content.text_regions
	)
	candidates = tuple(region for region in exterior if styled_callout_candidate(region, content.bounds))
	if len(candidates) != 1:
		return None
	candidate = candidates[0]
	matches = tuple(
		region for region in content.text_regions
		if styled_auto_shape(region, CALLOUT_ANCHOR_MAX_PARAGRAPHS)
		and matching_callout_style(candidate.bounds, region.bounds)
	)
	if len(matches) != 1:
		return None
	relation = members_for(
		(*content.text_regions, candidate), content.image_regions, title,
	)
	return protected_callout_relation(content, candidate, relation, title)


def protected_callout_relation(
		content: object, candidate: object, relation: VisualRelationMembers, title: object,
) -> VisualRelationMembers | None:
	"""Permit only an already-protected base/title overlap during callout expansion."""
	if relation.bounds == geometry.NormalizedBounds(0.0, 0.0, 1.0, 1.0):
		return None
	title_region = getattr(title, "region", None)
	if title_region is None:
		return relation if relation_is_safe(relation, title) else None
	if geometry.overlaps_or_contains(title_region.bounds, candidate.bounds):
		return None
	base_members = (*content.text_regions, *content.image_regions)
	base_overlaps = any(
		geometry.overlaps_or_contains(title_region.bounds, member.bounds)
		for member in base_members
	)
	protected = tuple(sorted(set((*content.protected_text_shape_ids, *relation.protected_text_shape_ids))))
	if base_overlaps and title_region.source_ordinal not in content.protected_text_shape_ids:
		return None
	if base_overlaps:
		return dataclasses.replace(relation, protected_text_shape_ids=protected)
	return relation if relation_is_safe(relation, title) else None


def coarse_body_styled_inset(texts: tuple[object, ...], images: tuple[object, ...], title: object) -> CoarseInsetMembers | None:
	"""Recognize one transparent object body with one later styled inset key."""
	eligible = tuple(region for region in texts if region is not getattr(title, "region", None))
	if images or len(eligible) != 2:
		return None
	bodies = tuple(region for region in eligible if (
		region.placeholder_confidence >= .75
		and getattr(region, "placeholder_role", None) == "OBJECT"
		and not getattr(region, "has_positive_fill", False) and not getattr(region, "has_positive_line", False)
	))
	if len(bodies) != 1:
		return None
	body = bodies[0]
	keys = tuple(region for region in eligible if region is not body and styled_auto_shape(region)
		and region.bounds.left >= .65 and region.bounds.width <= .25 and region.bounds.height <= .20
		and contains(body.bounds, region.bounds) and region.z_order > body.z_order
		and abs(region.bounds.top - body.bounds.top) <= .02)
	return CoarseInsetMembers(body, keys[0]) if len(keys) == 1 else None


def coarse_body_picture_inset(
		texts: tuple[object, ...], images: tuple[object, ...], title: object,
) -> CoarsePictureInsetMembers | None:
	"""Keep one small later-z picture inset direct beside its transparent object body."""
	if getattr(title, "region", None) is None or title.region not in texts or len(texts) != 2 or len(images) != 1:
		return None
	body = next((item for item in texts if item is not title.region), None)
	picture = images[0]
	if body is None or getattr(body, "placeholder_confidence", 0.0) < .75 or \
		getattr(body, "placeholder_role", None) != "OBJECT" or getattr(body, "has_positive_fill", False) or \
		getattr(body, "has_positive_line", False) or getattr(picture, "source_kind", None) != "picture" or \
		getattr(picture, "z_order", ()) <= getattr(body, "z_order", ()) or area(picture) > .08:
		return None
	if picture.bounds.top < body.bounds.top or picture.bounds.bottom > body.bounds.bottom or \
		max(body.bounds.left - picture.bounds.left, picture.bounds.right - body.bounds.right, 0.0) > .03:
		return None
	center = (picture.bounds.left + picture.bounds.right) / 2
	if center == .50:
		return None
	return CoarsePictureInsetMembers(body, picture, "left" if center < .50 else "right")


def dominant_image_narrative(
	texts: tuple[object, ...], images: tuple[object, ...], title: object,
) -> VisualRelationMembers | None:
	"""Return a dominant picture with one inset and one immediately lower narrative."""
	pictures = tuple(image for image in images if getattr(image, "source_kind", None) == "picture")
	if len(pictures) != 2:
		return None
	dominant = max(pictures, key=area)
	inset = next(image for image in pictures if image is not dominant)
	if area(dominant) < DOMINANT_MIN_AREA_MULTIPLIER * area(inset):
		return None
	if not upper_right_inset(inset.bounds, dominant.bounds):
		return None
	available = tuple(region for region in texts if region is not getattr(title, "region", None))
	candidates = tuple(region for region in available if lower_narrative(region, dominant.bounds))
	if len(candidates) != 1:
		return None
	relation = members_for((candidates[0],), (dominant, inset), title)
	return relation if relation_is_safe(relation, title) else None


def single_interior_overlay_label(
		texts: tuple[object, ...], images: tuple[object, ...], title: object,
		viable_callback: Callable[[VisualRelationMembers], bool] | None = None,
) -> VisualRelationMembers | None:
	"""Crop one large picture only with its sole materially interior short label."""
	available = tuple(region for region in texts if region is not getattr(title, "region", None))
	if len(available) != 1 or len(images) != 1 or getattr(images[0], "source_kind", None) != "picture":
		return None
	label, picture = available[0], images[0]
	if getattr(label, "source_kind", None) == "table" or len(label.paragraphs) > 2 or area(picture) < .25:
		return None
	center_x, center_y = (label.bounds.left + label.bounds.right) / 2, (label.bounds.top + label.bounds.bottom) / 2
	overlap_x = min(label.bounds.right, picture.bounds.right) - max(label.bounds.left, picture.bounds.left)
	overlap_y = min(label.bounds.bottom, picture.bounds.bottom) - max(label.bounds.top, picture.bounds.top)
	if not (picture.bounds.left < center_x < picture.bounds.right and picture.bounds.top < center_y < picture.bounds.bottom
		and overlap_x >= label.bounds.width * .50 and overlap_y >= label.bounds.height * .50):
		return None
	relation = members_for((label,), (picture,), title)
	title_region = getattr(title, "region", None)
	if relation.bounds == geometry.NormalizedBounds(0.0, 0.0, 1.0, 1.0) or (
		title_region is not None and (
			geometry.overlaps_or_contains(title_region.bounds, label.bounds) or
			(not geometry.overlaps_or_contains(title_region.bounds, picture.bounds) and
			geometry.overlaps_or_contains(title_region.bounds, relation.bounds))
		)
	):
		return None
	return relation if viable_callback is None or not viable_callback(relation) else None


def coupled_visual_sequence(
	texts: tuple[object, ...], images: tuple[object, ...], title: object,
	viable_callback: Callable[[VisualRelationMembers], bool] | None = None,
) -> VisualRelationMembers | None:
	"""Return a coherent, three-picture vertical sequence with no competing source role."""
	if any(region is not getattr(title, "region", None) for region in texts):
		return None
	if len(images) != 3 or any(getattr(image, "source_kind", None) != "picture" for image in images):
		return None
	ordered = tuple(sorted(images, key=lambda image: (image.bounds.top, image.bounds.left)))
	if getattr(title, "region", None) is not None and any(
		geometry.overlaps_or_contains(title.region.bounds, image.bounds)
		for image in ordered
	):
		return None
	if any(geometry.overlaps_or_contains(first.bounds, second.bounds)
		or second.bounds.top < first.bounds.bottom
		or second.bounds.top - first.bounds.bottom > NEARBY_GAP_RATIO
		for first, second in zip(ordered, ordered[1:])):
		return None
	centers_x = tuple((image.bounds.left + image.bounds.right) / 2 for image in ordered)
	aspects = tuple(image.bounds.width / image.bounds.height for image in ordered)
	if max(centers_x) - min(centers_x) < SEQUENCE_CENTER_SPAN_RATIO and \
		max(aspects) / min(aspects) < SEQUENCE_ASPECT_RATIO_VARIATION:
		return None
	result = members_for((), ordered, title)
	if not relation_is_safe(result, title):
		return None
	return result if viable_callback is None or not viable_callback(result) else None


def styled_callout_candidate(region: object, content: geometry.NormalizedBounds) -> bool:
	"""Require a short exterior auto-shape immediately below or beside content."""
	if not styled_auto_shape(region, CALLOUT_CANDIDATE_MAX_PARAGRAPHS):
		return False
	bounds = region.bounds
	return not contains(content, bounds) and bounds.top >= content.top and \
		bounds.bottom >= content.bottom - NEARBY_GAP_RATIO


def styled_auto_shape(
		region: object,
		maximum_paragraphs: int = CALLOUT_CANDIDATE_MAX_PARAGRAPHS,
) -> bool:
	"""Keep style inference limited to editable non-placeholder auto-shapes."""
	return (
		getattr(region, "source_kind", None) == "auto-shape"
		and getattr(region, "placeholder_confidence", 1.0) == 0.0
		and getattr(region, "has_positive_fill", False)
		and getattr(region, "has_positive_line", False)
		and len(getattr(region, "paragraphs", ())) <= maximum_paragraphs
	)


def matching_callout_style(
	first: geometry.NormalizedBounds, second: geometry.NormalizedBounds,
) -> bool:
	"""Use stable geometry as a minimal styled-callout equivalence signal."""
	if abs(first.left - second.left) > CALLOUT_LEFT_TOLERANCE_RATIO:
		return False
	ratio = first.width / second.width
	return CALLOUT_MIN_WIDTH_RATIO <= ratio <= CALLOUT_MAX_WIDTH_RATIO


def upper_right_inset(
	inset: geometry.NormalizedBounds, dominant: geometry.NormalizedBounds,
) -> bool:
	"""Require a small inset in the dominant image's upper-right neighborhood."""
	return (
		bounds_area(inset) <= bounds_area(dominant) * INSET_MAX_RELATIVE_SIZE
		and inset.left >= dominant.left + dominant.width / 2
		and inset.bottom <= dominant.top + dominant.height / 2
		and bounds_gap(inset, dominant) <= NEARBY_GAP_RATIO
	)


def lower_narrative(region: object, dominant: geometry.NormalizedBounds) -> bool:
	"""Recognize one broad editable narrative directly below its primary image."""
	bounds = region.bounds
	return (
		getattr(region, "placeholder_confidence", 1.0) == 0.0
		and getattr(region, "source_kind", None) != "table"
		and bounds.width >= dominant.width * CALLOUT_MIN_WIDTH_RATIO
		and abs(bounds.top - dominant.bottom) <= NEARBY_GAP_RATIO
	)


def members_for(
	texts: tuple[object, ...], images: tuple[object, ...], title: object,
) -> VisualRelationMembers:
	"""Build source membership and protect an overlapping selected title by ordinal."""
	bounds = union_bounds(tuple(region.bounds for region in (*texts, *images)))
	title_region = getattr(title, "region", None)
	protected = ()
	if title_region is not None and geometry.overlaps_or_contains(title_region.bounds, bounds):
		protected = (title_region.source_ordinal,)
	return VisualRelationMembers(texts, images, bounds, protected)


def relation_is_safe(relation: VisualRelationMembers, title: object) -> bool:
	"""Reject exact-full and actual member/title collisions, retaining AABB protection."""
	if relation.bounds == geometry.NormalizedBounds(0.0, 0.0, 1.0, 1.0):
		return False
	title_region = getattr(title, "region", None)
	return title_region is None or not any(
		geometry.overlaps_or_contains(title_region.bounds, item.bounds)
		for item in (*relation.text_regions, *relation.image_regions)
	)


def area(region: object) -> float:
	"""Return normalized source area for positive bounds."""
	return bounds_area(region.bounds)


def bounds_area(bounds: geometry.NormalizedBounds) -> float:
	"""Return normalized area for source geometry without source-type coupling."""
	return bounds.width * bounds.height


def bounds_gap(
	first: geometry.NormalizedBounds, second: geometry.NormalizedBounds,
) -> float:
	"""Return the largest axis gap between two source rectangles."""
	return max(
		second.left - first.right, first.left - second.right,
		second.top - first.bottom, first.top - second.bottom, 0.0,
	)


def union_bounds(
	bounds: tuple[geometry.NormalizedBounds, ...],
) -> geometry.NormalizedBounds:
	"""Return the bounded union of nonempty relation member geometry."""
	result = bounds[0]
	for item in bounds[1:]:
		result = result.union(item)
	return result


def contains(outer: geometry.NormalizedBounds, inner: geometry.NormalizedBounds) -> bool:
	"""Require every inset edge to remain within its body container."""
	return outer.left <= inner.left and inner.right <= outer.right and outer.top <= inner.top and inner.bottom <= outer.bottom
