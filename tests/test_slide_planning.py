"""Fast format-neutral planning coverage for the direct ODP import path."""

# local repo modules
import slide_lib.importers.djot_emitter as emitter
import slide_lib.importers.geometry as geometry
import slide_lib.importers.odp_to_djot as odp_to_djot
import slide_lib.importers.slide_plan as slide_plan
import slide_lib.importers.source_regions as source_regions
import slide_lib.importers.source_model as source_model


#============================================
def text_region(
	left: float, top: float, right: float, bottom: float, text: str,
	*, placeholder_role: str | None = None,
) -> source_regions.SourceTextRegion:
	"""Build one small editable source region from direct import facts."""
	return source_regions.SourceTextRegion(
		((0, (source_model.TextRun(text),)),),
		geometry.NormalizedBounds(left, top, right, bottom), False, 0.0,
		placeholder_role=placeholder_role,
	)


#============================================
def image_region(
	left: float, top: float, right: float, bottom: float,
) -> source_regions.SourceImageRegion:
	"""Build one small image region from direct import facts."""
	return source_regions.SourceImageRegion(
		"assets/figure.png", geometry.NormalizedBounds(left, top, right, bottom),
	)


#============================================
def test_direct_odp_asset_binding_keeps_source_visual_ordinal() -> None:
	"""The direct ODP planner joins an extracted picture to its visual evidence."""
	visual = source_regions.SourceImageRegion(
		"unresolved", geometry.NormalizedBounds(.55, .25, .90, .75), "picture", 7,
	)
	asset = source_model.ImageAsset(55, 25, 35, 50, "assets/photo.png", "Photo")

	plan = odp_to_djot.plan_imported_slide((), (visual,), (asset,), 100, 100)

	assert plan.slots[0].image_regions[0].asset_reference == "assets/photo.png"
	assert plan.slots[0].image_regions[0].source_ordinal == 7


#============================================


#============================================
def test_vertical_mixed_sequence_shares_one_panel_before_caption_pairing() -> None:
	"""An image, caption-like text, and next image form one sequence rather than equal panels."""
	text = source_regions.SourceTextRegion(
		((0, (source_model.TextRun("How many arrangements?"),)),),
		geometry.NormalizedBounds(.10, .32, .90, .40), False, 0,
		source_kind="text-box", source_ordinal=2,
	)
	images = (
		source_regions.SourceImageRegion("question.png", geometry.NormalizedBounds(.05, .10, .95, .30),
			"picture", 1),
		source_regions.SourceImageRegion("diagram.svg", geometry.NormalizedBounds(.10, .45, .90, .85),
			"picture", 3),
	)
	plan = slide_plan.plan_slide((text,), images)
	assert len(plan.slots) == 1 and plan.slots[0].flows_in_source_order
	assets = tuple(source_model.ImageAsset(0, 0, 10, 10, image.asset_reference, image.asset_reference)
		for image in images)
	for reasons in ((), ("source animation requires review",)):
		data = source_model.SlideData(1, False, (), (), assets, (), reasons)
		source, records = emitter.render_planned_djot([emitter.PlannedSlide(data, plan)])
		assert records[0]["layout"] == "one-panel"
		assert source.index("question.png)") < source.index("How many arrangements?") < source.index("diagram.svg)")
		assert ("@replaceme" in source) == bool(reasons)
		assert records[0]["review_reasons"] == list(reasons)
