"""Focused geometry behavior for immutable emitter component members."""

# local repo modules
import slide_lib.importers.djot_emitter as djot_emitter
import slide_lib.importers.geometry as geometry
import slide_lib.importers.slide_plan as slide_plan
import slide_lib.importers.source_model as source_model


#============================================
def bounds(values: tuple[float, float, float, float]) -> geometry.NormalizedBounds:
	"""Build concise normalized geometry for component behavior checks."""
	return geometry.NormalizedBounds(*values)


#============================================
def test_member_footprints_avoid_false_collision_from_union_bounds() -> None:
	"""Disjoint grouped members do not turn their enclosing union into a collision."""
	first = djot_emitter.EmissionComponent(
		bounds((0.10, 0.10, 0.90, 0.90)), ("- flow",), "flow",
		member_footprints=(bounds((0.10, 0.10, 0.20, 0.20)), bounds((0.80, 0.80, 0.90, 0.90))),
	)
	second = djot_emitter.EmissionComponent(bounds((0.45, 0.45, 0.55, 0.55)), ("- item",), "text")

	assert not djot_emitter.components_overlap([first, second])


#============================================
def test_only_coarse_direct_picture_peer_tolerates_raw_overlap() -> None:
	"""One coarse text and one direct picture retain their uniquely matched peer layout."""
	coarse = djot_emitter.EmissionComponent(
		bounds((0.05, 0.20, 0.60, 0.80)), ("- prose",), "text",
		coarse_text_container=True, member_footprints=(bounds((0.05, 0.20, 0.60, 0.80)),),
	)
	image = djot_emitter.EmissionComponent(
		bounds((0.45, 0.30, 0.95, 0.70)), ("![Figure](figure.png)",), "image",
		source_kind="picture", member_footprints=(bounds((0.45, 0.30, 0.95, 0.70)),),
	)

	assert djot_emitter.component_layout([coarse, image])[0] == "two-panels"
	assert not djot_emitter.components_overlap([coarse, image])


#============================================
def test_footer_padding_is_not_general_text_flow_tolerance() -> None:
	"""Only full-width ordered footer members accept a small vertical source overlap."""
	first = djot_emitter.EmissionComponent(bounds((0.05, 0.70, 0.95, 0.80)), ("- first",), "text")
	second = djot_emitter.EmissionComponent(bounds((0.05, 0.76, 0.95, 0.84)), ("- second",), "text")

	assert djot_emitter.follows_footer_lane(first, second)
	assert not djot_emitter.follows_text_lane(first, second)


#============================================
def test_caption_footer_and_shared_footer_relations_are_individually_bounded() -> None:
	"""Caption and shared-footer padding use their distinct native topology mappings."""
	left = djot_emitter.EmissionComponent(bounds((0.05, 0.20, 0.40, 0.50)), ("- left",), "text")
	caption_footer = djot_emitter.EmissionComponent(
		bounds((0.05, 0.55, 0.69, 0.65)), ("- footer",), "text", source_kind="text-box",
	)
	image_caption = djot_emitter.EmissionComponent(
		bounds((0.64, 0.20, 0.95, 0.59)), ("![image](image.png)", "", "- caption"), "image",
		source_kind="picture", member_footprints=(bounds((0.74, 0.20, 0.95, 0.50)), bounds((0.64, 0.51, 0.90, 0.59))),
	)
	coarse = djot_emitter.EmissionComponent(bounds((0.05, 0.20, 0.40, 0.55)), ("- left",), "text", coarse_text_container=True)
	shared_footer = djot_emitter.EmissionComponent(
		bounds((0.05, 0.55, 0.95, 0.65)), ("- footer",), "text", source_kind="text-box",
	)
	raw_image = djot_emitter.EmissionComponent(
		bounds((0.60, 0.20, 0.95, 0.58)), ("![image](image.png)",), "image", source_kind="picture",
	)

	assert not djot_emitter.components_overlap([left, caption_footer, image_caption])
	assert not djot_emitter.components_overlap(djot_emitter.coalesce_bottom_footer([coarse, shared_footer, raw_image]))


#============================================
def test_native_normalization_retains_individual_source_member_footprints() -> None:
	"""A normalized flow keeps source members for collisions while using their union as bounds."""
	text = slide_plan.SourceTextRegion(((0, (source_model.TextRun("Label"),)),),
		bounds((0.20, 0.20, 0.30, 0.30)), False, 0.0)
	image = slide_plan.SourceImageRegion("source.png", bounds((0.60, 0.60, 0.80, 0.80)))
	content = slide_plan.ContentRegionPlan("relation", bounds((0.20, 0.20, 0.80, 0.80)), (text,), (image,))
	plan = slide_plan.SlidePlan(slide_plan.TitleDecision(None, "test"), (), content)
	planned = djot_emitter.PlannedSlide(source_model.SlideData(1, False, (), (), (), (), ()), plan)

	components, _reasons = djot_emitter.emit_components(planned)
	gap = djot_emitter.EmissionComponent(bounds((0.40, 0.40, 0.50, 0.50)), ("- outside",), "text")

	assert not djot_emitter.components_overlap([components[0], gap])


#============================================
def text_box(values: tuple[float, float, float, float], ordinal: int, *, coarse: bool = False,
		rotation: float = 0.0) -> djot_emitter.EmissionComponent:
	"""Build one direct editable text-box component for shallow-flow behavior."""
	box = bounds(values)
	return djot_emitter.EmissionComponent(box, (f"- text {ordinal}",), "text",
		coarse_text_container=coarse, source_kind="text-box", source_ordinals=(ordinal,),
		member_footprints=(box,), rotation_degrees=rotation)


#============================================
def test_shallow_same_lane_text_boxes_form_a_two_panel_flow() -> None:
	"""Aligned editable text boxes become one right-side flow beside another panel."""
	left = djot_emitter.EmissionComponent(bounds((0.05, 0.20, 0.42, 0.65)), ("- left",), "text")
	first, second = text_box((0.58, 0.20, 0.945, 0.450), 10), text_box((0.585, 0.426, 0.945, 0.635), 11)

	result = djot_emitter.coalesce_text_flows([left, first, second])
	flow = next(component for component in result if component.kind == "flow")

	assert flow.lines == ("- text 10", "", "- text 11")
	assert djot_emitter.component_layout(result)[0] == "two-panels"
