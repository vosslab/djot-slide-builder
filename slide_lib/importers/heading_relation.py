"""Local editable heading detection for a single already-qualified source region."""

LOCAL_HEADING_MAX_GAP_RATIO = 0.05


def local_figure_heading(
	content: object,
	text_regions: tuple[object, ...],
	image_regions: tuple[object, ...],
	title: object,
	tables: tuple[object, ...],
) -> object | None:
	"""Return one short local label immediately above a solitary coupled region."""
	if content is None or tables or any(image not in content.image_regions for image in image_regions):
		return None
	exterior = tuple(
		region for region in text_regions
		if region is not title.region and region not in content.text_regions
	)
	if len(exterior) != 1:
		return None
	region = exterior[0]
	center_x = (region.bounds.left + region.bounds.right) / 2
	gap = content.bounds.top - region.bounds.bottom
	if (
		region.source_kind != "auto-shape" or region.placeholder_confidence != 0.0
		or len(region.paragraphs) != 1
		or not "".join(run.text for run in region.paragraphs[0][1]).strip()
		or region.source_ordinal in content.protected_text_shape_ids
		or not 0.0 <= gap <= LOCAL_HEADING_MAX_GAP_RATIO
		or not content.bounds.left <= center_x <= content.bounds.right
	):
		return None
	return region
