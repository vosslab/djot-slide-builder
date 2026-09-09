"""Build lossless diagnostic records for one-time presentation imports."""

# Standard Library
import dataclasses

# local repo modules
import slide_lib.importers.slide_plan as slide_plan
import slide_lib.importers.source_model as source_model


#============================================
def text_region_record(region: slide_plan.SourceTextRegion) -> dict[str, object]:
	"""Retain canonical source runs and geometry for later native reconstruction."""
	# ASVS 1.1.2: retain canonical text here; json.dumps performs final JSON escaping.
	paragraphs = [
		{
			"level": level,
			"runs": [{"text": run.text, "link": run.link} for run in runs],
		}
		for level, runs in region.paragraphs
	]
	return {
		"source_ordinal": region.source_ordinal,
		"source_order": list(region.z_order),
		"source_kind": region.source_kind,
		"bounds": dataclasses.asdict(region.bounds),
		"paragraphs": paragraphs,
	}


#============================================
def image_region_record(region: slide_plan.SourceImageRegion) -> dict[str, object]:
	"""Retain one normalized visual reference and its source geometry."""
	return {
		"source_ordinal": region.source_ordinal,
		"source_order": list(region.z_order),
		"source_kind": region.source_kind,
		"asset_reference": region.asset_reference,
		"bounds": dataclasses.asdict(region.bounds),
	}


#============================================
def content_region_record(
	content: slide_plan.ContentRegionPlan | None,
) -> dict[str, object] | None:
	"""Describe every retained member of one normalized spatial relationship."""
	if content is None:
		return None
	return {
		"region_key": content.region_key,
		"kind": content.kind,
		"classification_reason": content.classification_reason,
		"bounds": dataclasses.asdict(content.bounds),
		"local_heading": None if content.local_heading is None else
			text_region_record(content.local_heading),
		"text_regions": [text_region_record(region) for region in content.text_regions],
		"image_regions": [image_region_record(region) for region in content.image_regions],
	}


#============================================
def multiple_choice_record(
	choice: slide_plan.MultipleChoicePlan | None,
) -> dict[str, object] | None:
	"""Describe source evidence for one recognized multiple-choice structure."""
	if choice is None:
		return None
	return {
		"reason": choice.reason,
		"question": text_region_record(choice.question),
		"answer": text_region_record(choice.answer),
		"image": None if choice.image is None else image_region_record(choice.image),
		"question_visual_region": content_region_record(choice.question_visual_region),
	}


#============================================
def slide_record(data: source_model.SlideData, plan: slide_plan.SlidePlan | None,
		visible_page_index: int | None, layout: str, reasons: list[str]) -> dict[str, object]:
	"""Build one stable, JSON-ready import report record."""
	return {
		"source_slide": data.source_index,
		"visible_page": visible_page_index,
		"layout": layout,
		"text_blocks": len(data.text_blocks),
		"images": len(data.images),
		"presenter_notes": list(data.notes),
		"review_reasons": sorted(set(reasons)),
		"native_table_count": len(plan.tables) if plan else 0,
		"content_region": content_region_record(None if plan is None else plan.content_region),
		"multiple_choice": multiple_choice_record(None if plan is None else plan.multiple_choice),
	}
