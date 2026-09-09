"""Fast format-neutral planning coverage for the direct ODP import path."""

# local repo modules
import slide_lib.importers.geometry as geometry
import slide_lib.importers.odp_to_djot as odp_to_djot
import slide_lib.importers.slide_plan as slide_plan
import slide_lib.importers.source_model as source_model


def text_region(
	left: float, top: float, right: float, bottom: float, text: str,
	*, placeholder_role: str | None = None,
) -> slide_plan.SourceTextRegion:
	"""Build one small editable source region from direct import facts."""
	return slide_plan.SourceTextRegion(
		((0, (source_model.TextRun(text),)),),
		geometry.NormalizedBounds(left, top, right, bottom), False, 0.0,
		placeholder_role=placeholder_role,
	)


def image_region(
	left: float, top: float, right: float, bottom: float,
) -> slide_plan.SourceImageRegion:
	"""Build one small image region from direct import facts."""
	return slide_plan.SourceImageRegion(
		"assets/figure.png", geometry.NormalizedBounds(left, top, right, bottom),
	)


def test_direct_source_connector_retains_a_nonzero_planning_footprint() -> None:
	"""A stroked zero-width ODP connector remains available to relation planning."""
	regions = slide_plan.visual_regions((source_model.PositionedVisual(
		"connector-1", 500, 100, 0, 600, "connector", 1, 20,
	),), 1000, 1000)

	assert regions[0].source_line is not None
	assert regions[0].bounds.width > 0


def test_direct_odp_asset_binding_keeps_source_visual_ordinal() -> None:
	"""The direct ODP planner joins an extracted picture to its visual evidence."""
	visual = slide_plan.SourceImageRegion(
		"unresolved", geometry.NormalizedBounds(.55, .25, .90, .75), "picture", 7,
	)
	asset = source_model.ImageAsset(55, 25, 35, 50, "assets/photo.png", "Photo")

	plan = odp_to_djot.plan_imported_slide((), (visual,), (asset,), 100, 100)

	assert plan.slots[0].image_regions[0].asset_reference == "assets/photo.png"
	assert plan.slots[0].image_regions[0].source_ordinal == 7


def test_planner_assigns_clear_text_and_image_columns_to_named_slots() -> None:
	"""Side-by-side editable prose and an image keep separate native destinations."""
	plan = slide_plan.plan_slide(
		(text_region(.08, .32, .45, .76, "Editable prose"),),
		(image_region(.55, .32, .92, .76),),
	)

	assert tuple(slot.name for slot in plan.slots) == ("left", "right")


def test_planner_preserves_a_unique_interior_label_with_its_image() -> None:
	"""A sole label inside a large figure remains a bounded native relation."""
	label = text_region(.42, .42, .58, .50, "Figure label", placeholder_role="BODY")
	plan = slide_plan.plan_slide((label,), (image_region(.10, .20, .90, .80),))

	assert plan.content_region is not None
	assert plan.content_region.kind == "single-interior-overlay-label"
