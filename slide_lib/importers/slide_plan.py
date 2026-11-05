"""Geometry-first planning for imported presentation slides."""
import dataclasses
import slide_lib.importers.figure_regions as figure_regions
import slide_lib.importers.multiple_choice_plan as multiple_choice_plan
import slide_lib.importers.heading_relation as heading_relation
import slide_lib.importers.visual_relations as visual_relations
import slide_lib.importers.source_regions as source_regions
import slide_lib.importers.source_tables as source_tables
import slide_lib.importers.topology as topology
import slide_lib.layout_registry
TITLE_TOP_RATIO = 0.24
TITLE_BOTTOM_RATIO = 0.28
TITLE_MIN_WIDTH_RATIO = 0.34
SOLITARY_TITLE_TOP_RATIO = 0.12
SOLITARY_TITLE_MIN_WIDTH_RATIO = 0.75
FLOW_TEXT_BOUNDARY_EPSILON_RATIO = 0.02
@dataclasses.dataclass(frozen=True)
class TitleDecision:
	"""The deterministic title selection and the geometric evidence used."""
	region: source_regions.SourceTextRegion | None
	reason: str
@dataclasses.dataclass(frozen=True)
class SlotPlan:
	"""Editable source regions assigned to one named target slot."""
	name: str
	text_regions: tuple[source_regions.SourceTextRegion, ...]
	image_regions: tuple[source_regions.SourceImageRegion, ...] = ()
	flows_in_source_order: bool = False
	relation_id: str = ""
@dataclasses.dataclass(frozen=True)
class SlidePlan:
	"""Presentation-neutral import plan consumed by source emitters/renderers."""
	title: TitleDecision
	slots: tuple[SlotPlan, ...]
	content_region: figure_regions.ContentRegionPlan | None = None
	tables: tuple[source_tables.TablePlan, ...] = ()
	review_reason: str | None = None
	multiple_choice: multiple_choice_plan.MultipleChoicePlan | None = None
def select_title(text_regions: tuple[source_regions.SourceTextRegion, ...]) -> TitleDecision:
	"""Choose a native title from shallow, wide source evidence first."""
	plausible = tuple(
		region for region in text_regions
		if (
			region.source_kind != "table"
			and
			region.bounds.top <= TITLE_TOP_RATIO
			and region.bounds.width >= TITLE_MIN_WIDTH_RATIO
			and region.bounds.bottom <= TITLE_BOTTOM_RATIO
			and region.source_kind != "text-box"
		)
	)
	if plausible:
		region = min(
			plausible,
			key=lambda item: (
				item.bounds.top,
				-item.bounds.width,
				not item.title_identity,
				-item.placeholder_confidence,
				item.source_ordinal,
			),
		)
		return TitleDecision(region, "shallow-wide geometry")
	identity = tuple(
		region for region in text_regions
		if (
			region.source_kind != "table"
			and region.title_identity
			and region.bounds.bottom <= TITLE_BOTTOM_RATIO
		)
	)
	if identity:
		region = min(identity, key=lambda item: (item.bounds.top, item.bounds.left, item.source_ordinal))
		return TitleDecision(region, "placeholder identity fallback")
	return TitleDecision(None, "no native title evidence")
def select_solitary_title(
	text_regions: tuple[source_regions.SourceTextRegion, ...],
	image_regions: tuple[source_regions.SourceImageRegion, ...],
) -> TitleDecision | None:
	"""Allow one high-confidence title placeholder to own the sole text role.
	Images and tables retain their independent source roles; only competing text
	can make this otherwise unambiguous title placeholder ambiguous.
	"""
	if len(text_regions) != 1:
		return None
	region = text_regions[0]
	if (
		region.source_kind == "table"
		or not region.title_identity
		or region.placeholder_confidence < 0.75
		or region.bounds.width < SOLITARY_TITLE_MIN_WIDTH_RATIO
		or (image_regions and region.bounds.top > SOLITARY_TITLE_TOP_RATIO)
	):
		return None
	return TitleDecision(region, "solitary title identity")
def slot_plans(
	text_regions: tuple[source_regions.SourceTextRegion, ...],
	image_regions: tuple[source_regions.SourceImageRegion, ...],
	content: figure_regions.ContentRegionPlan | None,
	tables: tuple[source_tables.TablePlan, ...],
	title: TitleDecision, picture_inset: visual_relations.CoarsePictureInsetMembers | None = None,
) -> tuple[SlotPlan, ...]:
	"""Keep ordinary prose editable in a live native topology where possible."""
	if picture_inset is not None:
		body_slot = "right" if picture_inset.picture_slot == "left" else "left"
		identifier = f"coarse-body-picture-inset:{picture_inset.body.source_ordinal}:{picture_inset.picture.source_ordinal}:{picture_inset.picture_slot}"
		return (SlotPlan(picture_inset.picture_slot, (), (picture_inset.picture,), False, identifier),
			SlotPlan(body_slot, (picture_inset.body,), (), False, identifier))
	excluded = {title.region}
	if content is not None:
		excluded.update(content.text_regions)
		excluded.add(content.local_heading)
	for table in tables:
		excluded.update(table.text_regions)
	ordinary = tuple(region for region in text_regions if region not in excluded)
	content_images = () if content is None else content.image_regions
	ordinary_images = tuple(image for image in image_regions if image not in content_images)
	direct = tuple(("text", region) for region in ordinary) + tuple(("image", image) for image in ordinary_images)
	flow_items = tuple(sorted(direct, key=lambda item: (item[1].bounds.top, item[1].bounds.left, item[1].source_ordinal)))
	if not tables and ordinary and ordinary_images and len(flow_items) > 1 and all(
		first[1].bounds.bottom <= second[1].bounds.top + FLOW_TEXT_BOUNDARY_EPSILON_RATIO and
		topology.material(first[1].bounds.left, first[1].bounds.width, second[1].bounds.left, second[1].bounds.width)
		for first, second in zip(flow_items, flow_items[1:])
	):
		return (SlotPlan("body", tuple(item for kind, item in flow_items if kind == "text"),
			tuple(item for kind, item in flow_items if kind == "image"), True),)
	pairs = visual_relations.caption_pairings(ordinary, ordinary_images)
	if pairs:
		paired_text = set(pairs.values())
		units = [((caption,), (image,), image.bounds.union(caption.bounds))
			for image, caption in sorted(pairs.items(), key=lambda item: item[0].source_ordinal)]
		units.extend(((text,), (), text.bounds) for text in ordinary if text not in paired_text)
		units.extend(((), (image,), image.bounds) for image in ordinary_images if image not in pairs)
		match = topology.ordinary_layout_match(tuple(bounds for _texts, _images, bounds in units))
		if match is not None:
			name, order = match
			return tuple(SlotPlan(slide_lib.layout_registry.contract_for(name).slot_names[index], units[item][0], units[item][1])
				for index, item in enumerate(order))
		return (SlotPlan("body", ordinary, ordinary_images),)
	match = topology.ordinary_layout_match(tuple(item.bounds for _kind, item in direct))
	if match is not None:
		name, order = match
		return tuple(
			SlotPlan(slide_lib.layout_registry.contract_for(name).slot_names[index], (item,) if kind == "text" else (),
				(item,) if kind == "image" else ())
			for index, (kind, item) in enumerate(direct[item_index] for item_index in order)
		)
	if len(ordinary) == 2:
		left, right = sorted(ordinary, key=lambda item: (item.bounds.left, item.bounds.top))
		if left.bounds.right <= right.bounds.left:
			left_images = tuple(image for image in ordinary_images if image.bounds.left < .50)
			right_images = tuple(image for image in ordinary_images if image not in left_images)
			return (SlotPlan("left", (left,), left_images), SlotPlan("right", (right,), right_images))
	return (
		SlotPlan(
			"body",
			tuple(sorted(ordinary, key=lambda item: (item.bounds.top, item.bounds.left))),
			ordinary_images,
		),
	)

#============================================
def plan_slide(
	text_regions: tuple[source_regions.SourceTextRegion, ...],
	image_regions: tuple[source_regions.SourceImageRegion, ...],
) -> SlidePlan:
	"""Build one deterministic import plan from validated source regions."""
	choice = multiple_choice_plan.multiple_choice_plan(text_regions, image_regions)
	if choice is not None:
		return SlidePlan(
			TitleDecision(None, "multiple-choice structure"), (), multiple_choice=choice,
		)
	title = select_solitary_title(text_regions, image_regions) or select_title(text_regions)
	tables = source_tables.table_plans(text_regions, title.region); review_reason = None
	inset_pair = None if tables else visual_relations.coarse_body_styled_inset(text_regions, image_regions, title)
	picture_inset = None if tables else visual_relations.coarse_body_picture_inset(text_regions, image_regions, title)
	if not tables and source_tables.regular_text_grid(text_regions):
		review_reason = "regular text lattice requires border and span reconstruction"
	omitted_vectors = figure_regions.decorative_vectors(text_regions, image_regions)
	planning_images = tuple(item for item in image_regions if item not in omitted_vectors)
	repeated = None if tables else figure_regions.repeated_labeled_figure_region(text_regions, planning_images, title.region)
	shared = None if tables or repeated is not None else figure_regions.shared_figure_row_region(text_regions, planning_images, title.region)
	interior = None if tables else visual_relations.single_interior_overlay_label(text_regions, image_regions, title,
		lambda members: topology.ordinary_layout_viable(tuple(item.bounds for item in (*members.text_regions, *members.image_regions))))
	potential_content = None
	if repeated is not None:
		potential_content = repeated
	elif shared is not None:
		potential_content = shared
	elif not tables:
		potential_content = figure_regions.content_region(
			text_regions, planning_images, None,
		)
	if interior is None and figure_regions.title_is_component_member(title.region, potential_content):
		title = TitleDecision(None, "diagram component membership")
	try:
		content = repeated if repeated is not None else shared
		if content is None and interior is not None:
			content = figure_regions.ContentRegionPlan("single-interior-overlay-label-1", interior.bounds, interior.text_regions, interior.image_regions,
				"single-interior-overlay-label", "sole material interior overlay label")
		if content is None:
			content = None if tables else figure_regions.content_region(text_regions, planning_images, title.region)
		if not tables:
			relation = visual_relations.dominant_image_narrative(text_regions, planning_images, title)
			if relation is not None:
				content = figure_regions.ContentRegionPlan("dominant-image-narrative-1", relation.bounds, relation.text_regions,
					relation.image_regions, "dominant-image-narrative", "unique bounded visual composition")
			elif content is None:
				relation = visual_relations.coupled_visual_sequence(text_regions, planning_images, title,
					lambda members: topology.ordinary_layout_viable(tuple(item.bounds for item in members.image_regions)))
				if relation is not None:
					content = figure_regions.ContentRegionPlan("coupled-visual-sequence-1", relation.bounds, relation.text_regions, relation.image_regions,
						"coupled-visual-sequence", "unique bounded visual composition")
		content = figure_regions.absorb_connected_connectors(content, planning_images)
		extension = visual_relations.styled_callout_extension(content, text_regions, title)
		if extension is not None:
			content = dataclasses.replace(content, bounds=extension.bounds, text_regions=extension.text_regions,
				classification_reason=f"{content.classification_reason}; styled callout")
		if content is None and inset_pair is not None:
			content = figure_regions.ContentRegionPlan("styled-inset-key-1", inset_pair.key.bounds, (inset_pair.key,), (),
				"styled-inset-key", "styled inset key paired with coarse object body")
		content = figure_regions.absorb_contained_vector_label(content, text_regions, title.region)
		content = figure_regions.absorb_coarse_relation_text(content, text_regions, title.region)
		heading = heading_relation.local_figure_heading(content, text_regions,
			planning_images, title, tables)
		if heading is not None:
			content = dataclasses.replace(content, local_heading=heading,
				classification_reason=f"{content.classification_reason}; local figure heading")
	except ValueError as error:
		content = None
		review_reason = str(error)
	consumed = () if content is None else content.image_regions
	review_vectors = tuple(item for item in planning_images
		if item.source_kind in {"vector", "connector"} and item not in consumed)
	if review_vectors:
		vector_reason = "unconsumed vector requires review: " + ", ".join(
			str(item.source_ordinal) for item in review_vectors)
		review_reason = vector_reason if review_reason is None else f"{review_reason}; {vector_reason}"
	emittable_images = tuple(item for item in planning_images if item not in review_vectors)
	slots = slot_plans(text_regions, emittable_images, content, tables, title, picture_inset)
	plan = SlidePlan(title, slots, content, tables, review_reason)
	return plan
