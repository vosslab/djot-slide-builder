"""Focused geometry behavior for immutable emitter component members."""

# local repo modules
import slide_lib.importers.emission_topology as emission_topology
import slide_lib.importers.emission_flow as emission_flow
import slide_lib.importers.geometry as geometry
import slide_lib.importers.native_normalization as native_normalization


#============================================
def bounds(values: tuple[float, float, float, float]) -> geometry.NormalizedBounds:
	"""Build concise normalized geometry for component behavior checks."""
	return geometry.NormalizedBounds(*values)


#============================================
def test_restored_figure_retains_five_component_table_content() -> None:
	"""A restored figure beside a table preserves each image and the editable explanation."""
	box = bounds((0.1, 0.2, 0.9, 0.8))
	components = [
		emission_flow.EmissionComponent(box, ("![Parent](parent.png)",), "image"),
		emission_flow.EmissionComponent(box, ("![Offspring](offspring.png)",), "image"),
		emission_flow.EmissionComponent(box, ("![Cross](figure.png)",), "image"),
		emission_flow.EmissionComponent(box, ("| Allele | Result |", "| --- | --- |", "| A | round |"), "table"),
		emission_flow.EmissionComponent(box, ("- conclusion",), "text"),
	]
	lines, _layout = native_normalization.table_grid_lines([], components)
	for component in components:
		for line in component.lines:
			assert lines.count(line) == 1
	assert lines.index("![Parent](parent.png)") < lines.index("![Offspring](offspring.png)")


#============================================
def test_only_coarse_direct_picture_peer_tolerates_raw_overlap() -> None:
	"""One coarse text and one direct picture retain their uniquely matched peer layout."""
	coarse = emission_flow.EmissionComponent(
		bounds((0.05, 0.20, 0.60, 0.80)), ("- prose",), "text",
		coarse_text_container=True, member_footprints=(bounds((0.05, 0.20, 0.60, 0.80)),),
	)
	image = emission_flow.EmissionComponent(
		bounds((0.45, 0.30, 0.95, 0.70)), ("![Figure](figure.png)",), "image",
		source_kind="picture", member_footprints=(bounds((0.45, 0.30, 0.95, 0.70)),),
	)

	assert emission_topology.component_layout([coarse, image])[0] == "two-panels"
	assert not emission_topology.components_overlap([coarse, image])


#============================================
def test_caption_footer_and_shared_footer_relations_are_individually_bounded() -> None:
	"""Caption and shared-footer padding use their distinct native topology mappings."""
	left = emission_flow.EmissionComponent(bounds((0.05, 0.20, 0.40, 0.50)), ("- left",), "text")
	caption_footer = emission_flow.EmissionComponent(
		bounds((0.05, 0.55, 0.69, 0.65)), ("- footer",), "text", source_kind="text-box",
	)
	image_caption = emission_flow.EmissionComponent(
		bounds((0.64, 0.20, 0.95, 0.59)), ("![image](image.png)", "", "- caption"), "image",
		source_kind="picture", member_footprints=(bounds((0.74, 0.20, 0.95, 0.50)), bounds((0.64, 0.51, 0.90, 0.59))),
	)
	coarse = emission_flow.EmissionComponent(bounds((0.05, 0.20, 0.40, 0.55)), ("- left",), "text", coarse_text_container=True)
	shared_footer = emission_flow.EmissionComponent(
		bounds((0.05, 0.55, 0.95, 0.65)), ("- footer",), "text", source_kind="text-box",
	)
	raw_image = emission_flow.EmissionComponent(
		bounds((0.60, 0.20, 0.95, 0.58)), ("![image](image.png)",), "image", source_kind="picture",
	)

	assert not emission_topology.components_overlap([left, caption_footer, image_caption])
	assert not emission_topology.components_overlap(emission_flow.coalesce_bottom_footer([coarse, shared_footer, raw_image]))


#============================================
def text_box(values: tuple[float, float, float, float], ordinal: int, *, coarse: bool = False,
		rotation: float = 0.0) -> emission_flow.EmissionComponent:
	"""Build one direct editable text-box component for shallow-flow behavior."""
	box = bounds(values)
	return emission_flow.EmissionComponent(box, (f"- text {ordinal}",), "text",
		coarse_text_container=coarse, source_kind="text-box", source_ordinals=(ordinal,),
		member_footprints=(box,), rotation_degrees=rotation)


#============================================
def test_shallow_same_lane_text_boxes_form_a_two_panel_flow() -> None:
	"""Aligned editable text boxes become one right-side flow beside another panel."""
	left = emission_flow.EmissionComponent(bounds((0.05, 0.20, 0.42, 0.65)), ("- left",), "text")
	first, second = text_box((0.58, 0.20, 0.945, 0.450), 10), text_box((0.585, 0.426, 0.945, 0.635), 11)

	result = emission_flow.coalesce_text_flows([left, first, second])
	flow = next(component for component in result if component.kind == "flow")

	assert flow.lines == ("- text 10", "", "- text 11")
	assert emission_topology.component_layout(result)[0] == "two-panels"
