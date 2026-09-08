"""Compact behavioral coverage for exceptional imported-slide visual planning."""

# Standard Library
import dataclasses
import types

# PIP3 modules
from pptx import Presentation
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.dml.color import RGBColor
from pptx.util import Inches

# Local modules
import slide_lib.importers.djot_emitter as djot_emitter
import slide_lib.importers.geometry as geometry
import slide_lib.importers.heading_relation as heading_relation
import slide_lib.importers.visual_relations as visual_relations
import slide_lib.importers.slide_plan as slide_plan
import slide_lib.importers.topology as topology
import slide_lib.importers.pptx_reader as pptx_reader
import slide_lib.importers.source_model as source_model


def bounds(left: float, top: float, right: float, bottom: float) -> geometry.NormalizedBounds:
	"""Build one normalized rectangle for inline planner evidence."""
	return geometry.NormalizedBounds(left, top, right, bottom)


def text(left: float, top: float, right: float, bottom: float, *, confidence: float = 0.0,
	kind: str = "auto-shape", ordinal: int = 1, paragraphs: int = 1,
	rotation: float = 0.0, fill: bool = False, line: bool = False,
	role: str | None = None, z_order: tuple[int, ...] = ()) -> slide_plan.SourceTextRegion:
	"""Build one short source text shape without a fixture file."""
	return slide_plan.SourceTextRegion(tuple((0, (source_model.TextRun("Label"),)) for _ in range(paragraphs)),
		bounds(left, top, right, bottom), False, confidence, False, kind, ordinal,
		rotation_degrees=rotation, has_positive_fill=fill, has_positive_line=line,
		placeholder_role=role, z_order=z_order)


def image(left: float, top: float, right: float, bottom: float, *, kind: str = "picture",
	ordinal: int = 1, z_order: tuple[int, ...] = ()) -> slide_plan.SourceImageRegion:
	"""Build one source visual with stable provenance."""
	return slide_plan.SourceImageRegion(
		f"source-{ordinal}", bounds(left, top, right, bottom), kind, ordinal, z_order=z_order,
	)


def test_source_text_inventory_preserves_canonical_shape_rotation() -> None:
	"""Rotation remains normalized source evidence without affecting text extraction."""
	presentation = Presentation()
	slide = presentation.slides.add_slide(presentation.slide_layouts[5])
	shape = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(2), Inches(1))
	shape.text = "Rotated label"
	shape.rotation = 315
	regions = pptx_reader.source_text_regions(slide, presentation.slide_width, presentation.slide_height)

	assert len(regions) == 1
	assert regions[0].rotation_degrees == -45.0


def test_source_visual_regions_preserve_top_level_and_group_z_paths() -> None:
	"""Visual source paths retain both top-level and grouped stack positions."""
	picture = lambda shape_id: types.SimpleNamespace(shape_type=MSO_SHAPE_TYPE.PICTURE, shape_id=shape_id,
		left=0, top=0, width=10, height=10)
	slide = types.SimpleNamespace(shapes=(picture(1), types.SimpleNamespace(
		shape_type=MSO_SHAPE_TYPE.GROUP, shapes=(picture(2),),
	)))

	regions = pptx_reader.source_visual_regions(slide, 100, 100)

	assert tuple(region.z_order for region in regions) == ((0,), (1, 0))


def test_degenerate_connectors_preserve_endpoints_and_planning_footprints() -> None:
	"""Horizontal and vertical source lines inflate only their zero planning axis."""
	vertical = geometry.degenerate_connector_footprint(500, 100, 0, 600, 20, 1000, 1000)
	horizontal = geometry.degenerate_connector_footprint(-100, 0, 600, 0, 1, 1000, 1000)

	assert (vertical, horizontal) == (
		geometry.DegenerateConnectorFootprint(
			geometry.NormalizedLineEndpoints(.5, .1, .5, .7), bounds(.495, .1, .505, .7),
		),
		geometry.DegenerateConnectorFootprint(
			geometry.NormalizedLineEndpoints(0.0, 0.0, .5, 0.0), bounds(0.0, 0.0, .5, .0005),
		),
	)


def test_source_inventory_retains_only_visible_degenerate_connector_metadata() -> None:
	"""The PPTX boundary supplies a planning footprint without changing source endpoints."""
	presentation = Presentation()
	slide = presentation.slides.add_slide(presentation.slide_layouts[5])
	connector = slide.shapes.add_connector(
		MSO_CONNECTOR.STRAIGHT, Inches(1), Inches(2), Inches(5), Inches(2),
	)
	connector.line.color.rgb = RGBColor(0, 0, 0)
	connector.line.width = Inches(.02)
	slide.shapes.add_connector(
		MSO_CONNECTOR.STRAIGHT, Inches(1), Inches(3), Inches(5), Inches(3),
	)
	regions = pptx_reader.source_visual_regions(slide, presentation.slide_width, presentation.slide_height)

	assert len(regions) == 1 and regions[0].source_kind == "connector" and regions[0].source_line is not None \
		and regions[0].bounds.height > 0 and regions[0].source_line.endpoints.top == regions[0].source_line.endpoints.bottom


def test_source_inventory_rejects_unstroked_degenerate_connector() -> None:
	"""An unstroked line does not enter the visual inventory."""
	line = types.SimpleNamespace(
		find=lambda _name: None,
		get=lambda name: "12700" if name == "w" else None,
	)
	properties = types.SimpleNamespace(
		find=lambda name: line if name.endswith("ln") else None,
	)
	shape = types.SimpleNamespace(
		shape_type=MSO_SHAPE_TYPE.AUTO_SHAPE, is_placeholder=False, has_table=False,
		has_text_frame=False, text_frame=types.SimpleNamespace(paragraphs=()), element=types.SimpleNamespace(
			xml='<a:prstGeom prst="line">', find=lambda name: properties if name.endswith("spPr") else None,
		), shape_id=61, left=10, top=10, width=0, height=40,
	)

	assert not pptx_reader.source_visual_inventory(shape, 100, 100)


def test_degenerate_connector_normalization_rejects_point_geometry() -> None:
	"""A zero-area connector cannot receive a planning footprint."""
	line = geometry.degenerate_connector_footprint(0, 0, 0, 0, 10, 1000, 1000)

	assert line is None


def test_degenerate_connectors_join_existing_vector_scaffold_without_consuming_prose() -> None:
	"""Inflated connector footprints participate in the existing scaffold relation."""
	first = geometry.degenerate_connector_footprint(300, 300, 400, 0, 10, 1000, 1000)
	second = geometry.degenerate_connector_footprint(300, 500, 400, 0, 10, 1000, 1000)
	assert first is not None and second is not None
	connectors = (
		slide_plan.SourceImageRegion("source-connector-71", first.footprint, "connector", 71, first),
		slide_plan.SourceImageRegion("source-connector-72", second.footprint, "connector", 72, second),
	)
	labels = (text(.30, .34, .38, .40, ordinal=73), text(.62, .34, .70, .40, ordinal=74),
		text(.46, .43, .54, .50, ordinal=75))
	exterior = text(.02, .30, .20, .65, confidence=1.0, kind="text", ordinal=76)
	plan = slide_plan.plan_slide((*labels, exterior), connectors)

	assert plan.content_region is not None and plan.content_region.kind == "vector-scaffold" \
		and plan.content_region.image_regions == connectors and connectors[0].source_line is not None \
		and connectors[0].source_line.endpoints == first.endpoints and exterior in plan.slots[0].text_regions


def test_local_figure_heading_stays_editable_above_an_unchanged_crop() -> None:
	"""One short exterior auto-shape becomes local H2 before its source-region asset."""
	heading = text(.25, .13, .35, .17, ordinal=31)
	labels = (text(.30, .40, .37, .47, ordinal=32), text(.65, .60, .72, .67, ordinal=33))
	picture = image(.20, .20, .80, .80, ordinal=34)
	plan = slide_plan.plan_slide((heading, *labels), (picture,))
	content = plan.content_region
	planned = djot_emitter.PlannedSlide(
		source_model.SlideData(1, False, (), (), (), (), ()), plan,
	)
	lines, layout, _reasons = djot_emitter.render_planned_slide(
		planned, {(1, content.asset_key): "assets/crop.png"}, False,
	)

	assert content is not None and content.local_heading is heading and content.bounds == picture.bounds
	assert layout == "one-panel" and lines[-3:] == ["## Label", "", "![Coupled source region](assets/crop.png)"]


def test_local_figure_heading_rejects_competing_heading() -> None:
	"""A figure heading is withheld when competing nearby text exists."""
	picture = image(.20, .20, .80, .80, ordinal=40)
	heading = text(.30, .13, .40, .17, ordinal=41)
	competing = text(.55, .13, .65, .17, ordinal=42)
	content = slide_plan.ContentRegionPlan("crop", picture.bounds, (), (picture,))

	assert heading_relation.local_figure_heading(
		content, (heading, competing), (picture,), slide_plan.TitleDecision(None, "test"), (),
	) is None


def test_rotated_vector_labels_keep_only_one_complete_connected_figure() -> None:
	"""A rotated three-label lane retains its vector scaffold and exterior prose stays native."""
	vectors = (image(.30, .38, .70, .42, kind="vector", ordinal=51),
		image(.30, .53, .70, .57, kind="vector", ordinal=52))
	labels = (text(.30, .30, .70, .366583, ordinal=53, rotation=18),
		text(.30, .4567, .70, .50, ordinal=54), text(.30, .60, .70, .65, ordinal=55))
	exterior = text(.02, .30, .20, .60, confidence=1.0, kind="text", ordinal=56)
	plan = slide_plan.plan_slide((*labels, exterior), vectors)
	content = plan.content_region

	assert content is not None and content.kind == "rotated-vector-label"
	assert exterior in plan.slots[0].text_regions


def test_rotated_vector_labels_require_rotation_evidence() -> None:
	"""An otherwise matching vector arrangement needs a rotated label."""
	vectors = (image(.30, .38, .70, .42, kind="vector", ordinal=61),
		image(.30, .53, .70, .57, kind="vector", ordinal=62))
	labels = (text(.30, .30, .70, .366, ordinal=63),
		text(.30, .456, .70, .50, ordinal=64))
	content = slide_plan.plan_slide(labels, vectors).content_region

	assert content is None or content.kind != "rotated-vector-label"


def test_styled_callout_requires_connector_and_matching_left_edge() -> None:
	"""A connector crop grows only for one matching, explicitly styled editable callout."""
	vector = image(.20, .25, .70, .70, kind="connector", ordinal=80)
	inside = text(.30, .35, .45, .42, ordinal=81, paragraphs=4, fill=True, line=True)
	callout = text(.31, .72, .46, .79, ordinal=82, fill=True, line=True)
	content = slide_plan.ContentRegionPlan("visual", vector.bounds, (inside,), (vector,))
	relation = visual_relations.styled_callout_extension(
		content, (inside, callout), slide_plan.TitleDecision(None, "test"),
	)

	assert relation is not None and relation.text_regions == (inside, callout)
	assert visual_relations.styled_callout_extension(
		content, (inside, dataclasses.replace(callout, bounds=bounds(.38, .72, .53, .79))),
		slide_plan.TitleDecision(None, "test"),
	) is None


def test_coarse_body_styled_key_plans_native_body_and_two_panel_asset() -> None:
	"""A transparent object placeholder retains a styled inset key as a crop asset."""
	body = text(.10, .10, .90, .90, confidence=1.0, ordinal=90, role="OBJECT", z_order=(1,))
	key = text(.68, .11, .82, .19, ordinal=91, fill=True, line=True, z_order=(2,))
	title = text(.10, .02, .90, .08, confidence=1.0, ordinal=89, role="TITLE", z_order=(0,))
	plan = slide_plan.plan_slide((title, body, key), ())
	content = plan.content_region
	planned = djot_emitter.PlannedSlide(
		source_model.SlideData(1, False, (), (), (), (), ()), plan,
	)
	lines, layout, reasons = djot_emitter.render_planned_slide(
		planned, {(1, content.asset_key): "assets/key.png"}, False,
	)

	assert content is not None and content.kind == "styled-inset-key" and plan.title.region is title \
		and plan.slots[0].text_regions == (body,)
	assert layout == "two-panels" and "@left" in lines and "@right" in lines and not reasons


def test_coarse_body_picture_inset_keeps_both_members_native() -> None:
	"""A small late picture inset occupies its side while the transparent body stays editable."""
	title = text(.10, .02, .90, .08, confidence=1.0, ordinal=89, role="TITLE", z_order=(0,))
	body = text(.10, .10, .90, .90, confidence=1.0, ordinal=90, role="OBJECT", z_order=(1,))
	picture = image(.10, .30, .25, .60, ordinal=91, z_order=(2,))
	plan = slide_plan.plan_slide((title, body), (picture,))
	data = source_model.SlideData(
		1, False, (), (), (source_model.ImageAsset(0, 0, 1, 1, "source-91", "Inset"),), (), (),
	)
	lines, layout, reasons = djot_emitter.render_planned_slide(
		djot_emitter.PlannedSlide(data, plan), {}, False,
	)

	assert plan.title.region is title and plan.content_region is None \
		and tuple(slot.name for slot in plan.slots) == ("left", "right")
	assert layout == "two-panels" and "@left" in lines and "@right" in lines and not reasons


def test_caption_unit_and_footer_use_existing_two_plus_one_tolerance() -> None:
	"""One body, paired figure, and shallow overlapping footer remain native."""
	title = text(.05, .02, .95, .08, confidence=1.0, ordinal=80, role="TITLE")
	body = text(.68, .20, .92, .70, ordinal=81)
	picture = image(.10, .20, .42, .52, ordinal=82)
	caption = text(.13, .511, .39, .56, ordinal=83)
	footer = text(.10, .54, .68, .61, kind="text-box", ordinal=84)
	plan = slide_plan.plan_slide((title, body, caption, footer), (picture,))
	data = source_model.SlideData(
		1, False, (), (), (source_model.ImageAsset(0, 0, 1, 1, "source-82", "Figure"),), (), (),
	)
	planned = djot_emitter.PlannedSlide(data, plan)
	lines, layout, reasons = djot_emitter.render_planned_slide(planned, {}, False)
	components, _reasons = djot_emitter.emit_components(planned, None)
	permissions = djot_emitter.overlap_permissions(components)

	assert layout == "two-plus-one-panels" and not reasons
	assert any(item.relation == "caption-footer-padding" for item in permissions)


def test_coarse_body_picture_inset_rejects_multiple_insets() -> None:
	"""A coarse body crop needs exactly one side inset."""
	title = text(.10, .02, .90, .08, confidence=1.0, ordinal=89, role="TITLE")
	body = text(.10, .10, .90, .90, confidence=1.0, ordinal=90, role="OBJECT", z_order=(1,))
	picture = image(.10, .30, .25, .60, ordinal=91, z_order=(2,))
	images = (picture, image(.30, .30, .35, .35, ordinal=92))

	assert visual_relations.coarse_body_picture_inset(
		(title, body), images, slide_plan.TitleDecision(title, "test"),
	) is None


def test_dominant_picture_narrative_uses_the_complete_visual_membership() -> None:
	"""A large picture, upper-right inset, and lower prose form one bounded crop."""
	dominant = image(.10, .12, .80, .72, ordinal=100)
	inset = image(.65, .16, .75, .26, ordinal=101)
	narrative = text(.12, .74, .78, .82, ordinal=102)
	content = slide_plan.plan_slide((narrative,), (dominant, inset)).content_region

	assert content is not None and content.kind == "dominant-image-narrative"
	assert content.text_regions == (narrative,) and content.image_regions == (dominant, inset)


def test_dominant_picture_narrative_protects_title_overlapped_only_by_union() -> None:
	"""A full-width crop protects a title when only its union AABB reaches the title."""
	dominant = image(.10, .12, .80, .72, ordinal=103)
	inset = image(.65, .09, .75, .11, ordinal=104)
	narrative = text(.12, .74, .78, .82, ordinal=105)
	title_region = text(.78, .08, .95, .115, confidence=1.0, ordinal=106)
	title = slide_plan.TitleDecision(title_region, "test")
	relation = visual_relations.dominant_image_narrative((title_region, narrative),
		(dominant, inset), title)

	assert relation is not None and relation.protected_text_shape_ids == (106,)


def test_visual_relations_reject_exact_full_crop_bounds() -> None:
	"""Exceptional relations never rasterize an exact full-slide region."""
	relation = visual_relations.VisualRelationMembers((), (), bounds(0.0, 0.0, 1.0, 1.0))

	assert not visual_relations.relation_is_safe(
		relation, slide_plan.TitleDecision(None, "test"),
	)


def test_repeated_figures_accept_mutual_labels_on_the_same_side() -> None:
	"""Both repeated figures may use their left-side labels when each pairing is unique."""
	left, right = image(.20, .30, .40, .55, ordinal=110), image(.60, .30, .80, .55, ordinal=111)
	labels = (text(.11, .37, .19, .45, ordinal=112), text(.51, .37, .59, .45, ordinal=113))
	content = slide_plan.repeated_labeled_figure_region(
		labels, (left, right), slide_plan.TitleDecision(None, "test"),
	)

	assert content is not None and content.kind == "repeated-labeled-figure"
	assert content.text_regions == labels and content.image_regions == (left, right)


def test_visual_sequence_and_topology_viability_suppress_nonunique_crops() -> None:
	"""A qualified sequence is withheld when an existing native topology can represent it."""
	images = (image(.15, .15, .35, .30, ordinal=120), image(.30, .32, .50, .47, ordinal=121),
		image(.45, .49, .65, .64, ordinal=122))
	title = slide_plan.TitleDecision(None, "test")
	relation = visual_relations.coupled_visual_sequence((), images, title)

	assert relation is not None and relation.image_regions == images
	assert visual_relations.coupled_visual_sequence((), images, title, lambda _relation: True) is None


def test_single_interior_overlay_label_uses_one_named_crop() -> None:
	"""One large source picture and its sole interior label remain spatially coupled."""
	label = text(.42, .42, .58, .50, confidence=1.0, role="BODY", ordinal=205)
	picture = image(.10, .20, .90, .80, ordinal=206)

	planned = slide_plan.plan_slide((label,), (picture,))

	assert planned.content_region is not None and planned.content_region.kind == "single-interior-overlay-label" \
		and planned.content_region.text_regions == (label,) and planned.content_region.image_regions == (picture,)


def test_single_interior_overlay_label_protects_overlapping_title() -> None:
	"""A title overlapping only the picture remains outside its full protected crop."""
	title = slide_plan.SourceTextRegion(
		((0, (source_model.TextRun("Title"),)),),
		bounds(.10, .05, .90, .15), False, 1.0, True, "text", 204,
	)
	label = text(.42, .42, .58, .50, ordinal=205)
	picture = image(.10, .10, .90, .80, ordinal=206)

	planned = slide_plan.plan_slide((title, label), (picture,))

	assert planned.content_region is not None and planned.content_region.bounds == picture.bounds \
		and planned.content_region.protected_text_shape_ids == (204,) and planned.title.region is title \
		and title not in planned.content_region.text_regions


def test_single_interior_overlay_label_rejects_exterior_label() -> None:
	"""A label outside the source picture stays uncoupled."""
	label = text(.01, .42, .09, .50, ordinal=210)
	planned = slide_plan.plan_slide((label,), (image(.10, .20, .90, .80, ordinal=220),))

	assert planned.content_region is None or planned.content_region.kind != "single-interior-overlay-label"


def test_visual_sequence_rejects_vertical_overlap() -> None:
	"""A sequence requires each later picture to begin at or below the prior bottom."""
	images = (image(.10, .10, .30, .30, ordinal=123), image(.35, .29, .55, .45, ordinal=124),
		image(.60, .47, .80, .63, ordinal=125))

	assert visual_relations.coupled_visual_sequence(
		(), images, slide_plan.TitleDecision(None, "test"),
	) is None


def test_shared_topology_rejects_ambiguous_geometry() -> None:
	"""Both shared topology entry points reject ambiguous geometry."""
	regions = (bounds(.58, .56, .81, .68), bounds(.49, .42, .69, .63))

	assert topology.ordinary_layout_match(regions) is None
	assert not topology.ordinary_layout_viable(regions)


def test_shared_topology_agrees_with_live_registry_for_unique_geometry() -> None:
	"""The matcher and viability use the same live two-panel registry policy."""
	regions = (bounds(.10, .20, .50, .80), bounds(.55, .20, .95, .80))

	assert topology.ordinary_layout_match(regions) == ("two-panels", (0, 1))
	assert topology.ordinary_layout_viable(regions)
