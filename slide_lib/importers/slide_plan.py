"""Geometry-first planning for imported presentation slides."""
import collections.abc
import dataclasses
import itertools
import math
import slide_lib.importers.geometry as geometry
import slide_lib.importers.heading_relation as heading_relation
import slide_lib.importers.visual_relations as visual_relations
import slide_lib.importers.rotated_vector_label as rotated_vector_label
import slide_lib.importers.source_model as source_model
import slide_lib.importers.topology as topology
import slide_lib.layouts
TITLE_TOP_RATIO = 0.24
TITLE_BOTTOM_RATIO = 0.28
TITLE_MIN_WIDTH_RATIO = 0.34
SOLITARY_TITLE_TOP_RATIO = 0.12
SOLITARY_TITLE_MIN_WIDTH_RATIO = 0.75
CONTENT_IMAGE_MIN_AREA_RATIO = 0.12
SINGLE_ANNOTATION_IMAGE_MIN_AREA_RATIO = 0.50
ANNOTATION_MINIMUM_COUNT = 2
ANNOTATION_CENTER_SPAN_RATIO = 0.12
ANNOTATION_PROXIMITY_RATIO = 0.08
VECTOR_COMPONENT_PROXIMITY_RATIO = 0.08
FLOW_VERTICAL_CENTER_SEPARATION_RATIO = 0.05
FLOW_TEXT_BOUNDARY_EPSILON_RATIO = 0.02
CROP_EDGE_LABEL_PADDING = 0.02
TINY_DECORATIVE_VECTOR_AREA_RATIO = 0.002
TINY_DECORATIVE_VECTOR_SPAN_RATIO = 0.04
SHARED_FIGURE_ROW_ALIGNMENT_RATIO = 0.06
SHARED_FIGURE_CAPTION_MIN_SPAN_RATIO = 0.50
CONNECTOR_AXIAL_OVERLAP_RATIO = 0.50
CONNECTOR_PERPENDICULAR_PROXIMITY_RATIO = 0.04
MULTIPLE_CHOICE_MIN_PLACEHOLDER_CONFIDENCE = 0.75
MULTIPLE_CHOICE_ANSWER_MIN_CENTER_X_RATIO = 0.65
MULTIPLE_CHOICE_ANSWER_MIN_CENTER_Y_RATIO = 0.65
MULTIPLE_CHOICE_ANSWER_MAX_WIDTH_RATIO = 0.50
MC_ANSWER_MAX_NORMALIZED_AREA_RATIO = 0.16
MC_ANSWER_BELOW_GAP_RATIO = 0.08
CONTAINED_VECTOR_LABEL_MAX_PARAGRAPHS = 3
REPEATED_LABEL_SIDE_GAP_RATIO = 0.08
REPEATED_LABEL_CENTER_TOLERANCE_RATIO = 0.10
SIDE_LABEL_BORDER_OVERLAP = 0.02
MULTIPLE_CHOICE_FIGURE_MAX_WIDTH_RATIO = 0.60
MULTIPLE_CHOICE_FIGURE_MAX_HEIGHT_RATIO = 0.35
MULTIPLE_CHOICE_FIGURE_CENTER_OFFSET_RATIO = 0.20
MULTIPLE_CHOICE_FIGURE_TOP_CENTER_RATIO = 0.35
@dataclasses.dataclass(frozen=True)
class SourceTextRegion:
	"""One source text shape, retaining paragraph structure and geometry."""
	paragraphs: tuple[tuple[int, tuple[source_model.TextRun, ...]], ...]
	bounds: geometry.NormalizedBounds
	is_subtitle: bool
	placeholder_confidence: float
	title_identity: bool = False
	source_kind: str = "text"
	source_ordinal: int = 0
	table_row: int | None = None
	table_column: int | None = None
	table_row_count: int = 0
	table_column_count: int = 0
	table_id: int | None = None
	table_has_header: bool = False
	table_unsupported_reason: str | None = None
	rotation_degrees: float = 0.0
	has_positive_fill: bool = False
	has_positive_line: bool = False
	placeholder_role: str | None = None
	z_order: tuple[int, ...] = ()
	def __post_init__(self) -> None:
		if not self.paragraphs:
			raise ValueError("source text region requires at least one paragraph")
		if not 0.0 <= self.placeholder_confidence <= 1.0:
			raise ValueError("placeholder confidence must be within zero and one")
		if self.source_kind not in {"text", "text-box", "auto-shape", "table"}:
			raise ValueError("source text kind is not supported")
		if not math.isfinite(self.rotation_degrees):
			raise ValueError("source text rotation must be finite")
		rotation = self.rotation_degrees % 360.0
		if rotation > 180.0:
			rotation -= 360.0
		object.__setattr__(self, "rotation_degrees", rotation)
@dataclasses.dataclass(frozen=True)
class SourceImageRegion:
	"""One source image and its geometry, before any renderer conversion."""
	asset_reference: str
	bounds: geometry.NormalizedBounds
	source_kind: str = "picture"
	source_ordinal: int = 0
	source_line: geometry.DegenerateConnectorFootprint | None = None
	z_order: tuple[int, ...] = ()
@dataclasses.dataclass(frozen=True)
class TablePlan:
	"""A source table retained as editable structured content."""
	bounds: geometry.NormalizedBounds
	text_regions: tuple[SourceTextRegion, ...]
	rows: tuple[tuple["TableCellPlan", ...], ...]
	row_count: int
	column_count: int
	has_header: bool = False
	unsupported_reason: str | None = None
	table_id: int = 0
@dataclasses.dataclass(frozen=True)
class TableCellPlan:
	"""One native-table cell, including an intentional blank when no text exists."""
	row: int
	column: int
	text_regions: tuple[SourceTextRegion, ...]
	row_span: int = 1
	column_span: int = 1
@dataclasses.dataclass(frozen=True)
class TitleDecision:
	"""The deterministic title selection and the geometric evidence used."""
	region: SourceTextRegion | None
	reason: str
@dataclasses.dataclass(frozen=True)
class SlotPlan:
	"""Editable source regions assigned to one named target slot."""
	name: str
	text_regions: tuple[SourceTextRegion, ...]
	image_regions: tuple[SourceImageRegion, ...] = ()
	flows_in_source_order: bool = False
	relation_id: str = ""
@dataclasses.dataclass(frozen=True)
class ContentRegionPlan:
	"""A diagram and annotations that must remain spatially coupled."""
	asset_key: str
	bounds: geometry.NormalizedBounds
	text_regions: tuple[SourceTextRegion, ...]
	image_regions: tuple[SourceImageRegion, ...]
	protected_text_shape_ids: tuple[int, ...] = ()
	kind: str = "diagram"
	classification_reason: str = "qualified pictorial annotation component"
	local_heading: SourceTextRegion | None = None
@dataclasses.dataclass(frozen=True)
class MultipleChoicePlan:
	"""A complete structural question-and-answer pattern from one source slide."""
	question: SourceTextRegion
	answer: SourceTextRegion
	image: SourceImageRegion | None
	reason: str
	question_visual_region: ContentRegionPlan | None = None
@dataclasses.dataclass(frozen=True)
class SlidePlan:
	"""Presentation-neutral import plan consumed by source emitters/renderers."""
	title: TitleDecision
	slots: tuple[SlotPlan, ...]
	content_region: ContentRegionPlan | None = None
	tables: tuple[TablePlan, ...] = ()
	review_reason: str | None = None
	multiple_choice: MultipleChoicePlan | None = None
	omitted_vectors: tuple[SourceImageRegion, ...] = ()
	review_vectors: tuple[SourceImageRegion, ...] = ()
def select_title(text_regions: tuple[SourceTextRegion, ...]) -> TitleDecision:
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
	text_regions: tuple[SourceTextRegion, ...],
	image_regions: tuple[SourceImageRegion, ...],
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
	annotations: tuple[SourceTextRegion, ...],
) -> bool:
	"""Require several labels to occupy a real diagram component, not one caption."""
	centers_x = tuple((item.bounds.left + item.bounds.right) / 2 for item in annotations)
	centers_y = tuple((item.bounds.top + item.bounds.bottom) / 2 for item in annotations)
	return (
		max(centers_x) - min(centers_x) >= ANNOTATION_CENTER_SPAN_RATIO
		or max(centers_y) - min(centers_y) >= ANNOTATION_CENTER_SPAN_RATIO
	)
def title_excluded_content_bounds(
	bounds: geometry.NormalizedBounds,
	annotations: tuple[SourceTextRegion, ...],
	title: TitleDecision,
) -> tuple[geometry.NormalizedBounds, tuple[int, ...]]:
	"""Either crop a clear title strip or protect its source shape during rendering."""
	if title.region is None or not geometry.overlaps_or_contains(bounds, title.region.bounds):
		return bounds, ()
	top = max(bounds.top, title.region.bounds.bottom)
	if top >= bounds.bottom:
		raise ValueError("title-excluded diagram crop requires review")
	if any(region.bounds.top < top for region in annotations):
		if title.region.source_ordinal <= 0:
			raise ValueError("protected title source shape requires review")
		return bounds, (title.region.source_ordinal,)
	return geometry.NormalizedBounds(bounds.left, top, bounds.right, bounds.bottom), ()
def regular_text_grid(text_regions: tuple[SourceTextRegion, ...]) -> bool:
	"""Recognize a dense row-and-column lattice as an editable table candidate."""
	if len(text_regions) < 8:
		return False
	centers_x = sorted((item.bounds.left + item.bounds.right) / 2 for item in text_regions)
	centers_y = sorted((item.bounds.top + item.bounds.bottom) / 2 for item in text_regions)
	x_breaks = sum(
		second - first >= 0.08 for first, second in zip(centers_x, centers_x[1:])
	)
	y_breaks = sum(
		second - first >= 0.08 for first, second in zip(centers_y, centers_y[1:])
	)
	return x_breaks >= 2 and y_breaks >= 2
def table_plans(
	text_regions: tuple[SourceTextRegion, ...],
	image_regions: tuple[SourceImageRegion, ...],
	title: TitleDecision,
) -> tuple[TablePlan, ...]:
	"""Plan each actual source table independently before diagram coupling."""
	available = tuple(region for region in text_regions if region is not title.region)
	by_table: dict[int, list[SourceTextRegion]] = {}
	for region in available:
		if region.source_kind == "table" and region.table_id is not None:
			by_table.setdefault(region.table_id, []).append(region)
	plans: list[TablePlan] = []
	for table_id in sorted(by_table):
		table_regions = tuple(sorted(by_table[table_id], key=lambda item: item.source_ordinal))
		bounds = table_regions[0].bounds
		for region in table_regions[1:]:
			bounds = bounds.union(region.bounds)
		row_count = table_regions[0].table_row_count
		column_count = table_regions[0].table_column_count
		rows = table_rows(table_regions, row_count, column_count)
		plans.append(TablePlan(
			bounds,
			table_regions,
			rows,
			row_count,
			column_count,
			table_regions[0].table_has_header,
			table_regions[0].table_unsupported_reason,
			table_id,
		))
	return tuple(plans)
def table_rows(
	regions: tuple[SourceTextRegion, ...],
	row_count: int,
	column_count: int,
) -> tuple[tuple[TableCellPlan, ...], ...]:
	"""Preserve actual row-major dimensions, blanks, and cell ownership."""
	by_cell: dict[tuple[int, int], list[SourceTextRegion]] = {}
	for region in regions:
		key = (region.table_row, region.table_column)
		by_cell.setdefault(key, []).append(region)
	rows: list[tuple[TableCellPlan, ...]] = []
	for row in range(row_count):
		cells: list[TableCellPlan] = []
		for column in range(column_count):
			cell_regions = tuple(sorted(
				by_cell.get((row, column), []), key=lambda item: item.source_ordinal,
			))
			cells.append(TableCellPlan(row, column, cell_regions))
		rows.append(tuple(cells))
	planned_rows = tuple(rows)
	return planned_rows
def has_visible_list_structure(region: SourceTextRegion) -> bool:
	"""Require source hierarchy that separates one prompt from visible options."""
	if len(region.paragraphs) < 2:
		return False
	prompt_level = region.paragraphs[0][0]
	return any(level > prompt_level for level, _text in region.paragraphs[1:])
def is_multiple_choice_answer(region: SourceTextRegion, question: SourceTextRegion) -> bool:
	"""Recognize one short lower-right non-placeholder answer callout."""
	center_x = (region.bounds.left + region.bounds.right) / 2
	center_y = (region.bounds.top + region.bounds.bottom) / 2
	return (
		region.placeholder_confidence == 0.0
		and 1 <= len(region.paragraphs) <= 2
		and len({level for level, _text in region.paragraphs}) == 1
		and center_x >= MULTIPLE_CHOICE_ANSWER_MIN_CENTER_X_RATIO
		and center_y >= MULTIPLE_CHOICE_ANSWER_MIN_CENTER_Y_RATIO
		and region.bounds.width <= MULTIPLE_CHOICE_ANSWER_MAX_WIDTH_RATIO
		and region.bounds.width * region.bounds.height <= MC_ANSWER_MAX_NORMALIZED_AREA_RATIO
		and (bounds_contains(question.bounds, region.bounds, 0.0)
			or answer_below_question(region.bounds, question.bounds))
	)
def answer_below_question(answer: geometry.NormalizedBounds,
		question: geometry.NormalizedBounds) -> bool:
	"""Allow a compact lower-right callout directly beneath its primary prompt."""
	return (answer.top >= question.bottom - geometry.FLOW_BORDER_CONTACT_RATIO
		and answer.top - question.bottom <= MC_ANSWER_BELOW_GAP_RATIO
		and min(answer.right, question.right) > max(answer.left, question.left))
def is_multiple_choice_figure(
	image: SourceImageRegion,
	question: SourceTextRegion,
) -> bool:
	"""Accept one bounded centered top figure inside a coarse question placeholder."""
	image_center_x = (image.bounds.left + image.bounds.right) / 2
	image_center_y = (image.bounds.top + image.bounds.bottom) / 2
	question_center_y = (question.bounds.top + question.bounds.bottom) / 2
	return (
		question.bounds.left <= image.bounds.left <= image.bounds.right <= question.bounds.right
		and question.bounds.top <= image.bounds.top <= image.bounds.bottom <= question.bounds.bottom
		and abs(image_center_x - (question.bounds.left + question.bounds.right) / 2) <= \
			question.bounds.width * MULTIPLE_CHOICE_FIGURE_CENTER_OFFSET_RATIO
		and image_center_y < question_center_y
		and image_center_y - question.bounds.top <= \
			question.bounds.height * MULTIPLE_CHOICE_FIGURE_TOP_CENTER_RATIO
		and image.bounds.width <= question.bounds.width * MULTIPLE_CHOICE_FIGURE_MAX_WIDTH_RATIO
		and image.bounds.height <= question.bounds.height * MULTIPLE_CHOICE_FIGURE_MAX_HEIGHT_RATIO
	)
def multiple_choice_plan(
	text_regions: tuple[SourceTextRegion, ...],
	image_regions: tuple[SourceImageRegion, ...],
) -> MultipleChoicePlan | None:
	"""Recognize only a complete editable question/list/answer source structure."""
	questions = tuple(region for region in text_regions if (
		region.placeholder_confidence >= MULTIPLE_CHOICE_MIN_PLACEHOLDER_CONFIDENCE
		and has_visible_list_structure(region)
	))
	if len(questions) != 1:
		return None
	question = questions[0]
	answers = tuple(region for region in text_regions if is_multiple_choice_answer(region, question))
	if len(answers) != 1:
		return None
	answer = answers[0]
	if answer is question:
		return None
	overlay_text = tuple(region for region in text_regions if region not in (question, answer))
	visuals = tuple(image for image in image_regions if image.source_kind in {"picture", "vector"})
	connectors = tuple(image for image in image_regions if image.source_kind == "connector")
	if len(visuals) + len(connectors) != len(image_regions):
		return None
	if not overlay_text and not image_regions:
		return MultipleChoicePlan(question, answer, None, "complete question-list-answer structure")
	if not overlay_text and len(visuals) == 1 and len(image_regions) == 1 and \
		is_multiple_choice_figure(visuals[0], question):
		return MultipleChoicePlan(question, answer, visuals[0],
			"complete question-list-answer structure with top figure")
	if any(not geometry.overlaps_or_contains(region.bounds, question.bounds) or
			geometry.overlaps_or_contains(region.bounds, answer.bounds) for region in overlay_text) or \
		any(not is_multiple_choice_figure(image, question) for image in visuals):
		return None
	members = (*overlay_text, *visuals)
	if not members or any(not any(geometry.overlaps_or_contains(connector.bounds, member.bounds)
		for member in members) for connector in connectors):
		return None
	bounds = question.bounds
	for member in (*members, *connectors):
		bounds = bounds.union(member.bounds)
	protected = tuple(sorted({question.source_ordinal, answer.source_ordinal}))
	if 0 in protected:
		return None
	visual = ContentRegionPlan("multiple-choice-visual-1", bounds, overlay_text, (*visuals, *connectors),
		protected, "multiple-choice-overlay", "question-associated overlay component")
	return MultipleChoicePlan(question, answer, None,
		"complete question-list-answer structure with associated overlay", visual)
def content_region(
	text_regions: tuple[SourceTextRegion, ...],
	image_regions: tuple[SourceImageRegion, ...],
	title: TitleDecision,
) -> ContentRegionPlan | None:
	"""Plan one diagram-plus-annotation region without flattening its labels."""
	if not image_regions:
		return None
	available_text = tuple(region for region in text_regions if region is not title.region)
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
			bounds, protected_text_shape_ids = title_excluded_content_bounds(bounds, annotations, title)
			return ContentRegionPlan(
				asset_key=f"content-region-{image_index}",
				bounds=bounds,
				text_regions=annotations,
				image_regions=tuple(sorted(component_images, key=lambda item: item.source_ordinal)),
				protected_text_shape_ids=protected_text_shape_ids,
				kind="diagram",
				classification_reason="distributed pictorial annotations",
			)
	rotated = rotated_vector_label.rotated_vector_label_members(available_text, image_regions)
	if rotated is not None:
		bounds, protected = title_excluded_content_bounds(rotated.bounds, rotated.text_regions, title)
		return ContentRegionPlan(
			"rotated-vector-label-1", bounds, rotated.text_regions, rotated.image_regions, protected,
			"rotated-vector-label", "unique connected rotated vector-label graph",
		)
	vector_region = vector_scaffold_region(available_text, image_regions, title)
	if vector_region is not None:
		return vector_region
	return mixed_visual_region(available_text, image_regions, title)
def vector_scaffold_region(
	available_text: tuple[SourceTextRegion, ...],
	image_regions: tuple[SourceImageRegion, ...],
	title: TitleDecision,
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
	bounds, protected_text_shape_ids = title_excluded_content_bounds(bounds, annotations, title)
	return ContentRegionPlan(
		"vector-component-1", bounds, tuple(sorted(annotations, key=lambda item: item.source_ordinal)),
		tuple(sorted(vectors, key=lambda item: item.source_ordinal)), protected_text_shape_ids,
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
	available_text: tuple[SourceTextRegion, ...],
	image_regions: tuple[SourceImageRegion, ...],
	title: TitleDecision,
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
		any(isinstance(nodes[index], SourceImageRegion) for index in component)
		and any(
			geometry.strictly_overlaps(anchor.bounds, other.bounds)
			for anchor in (nodes[index] for index in component
				if isinstance(nodes[index], SourceImageRegion))
			for other in (nodes[index] for index in component)
			if other is not anchor
		)
		and (
			any(
				isinstance(nodes[index], SourceTextRegion)
				and nodes[index].source_kind in {"auto-shape", "text-box"}
				for index in component
			)
			or sum(isinstance(nodes[index], SourceImageRegion) for index in component) >= 2
		)
	))
	if len(candidates) != 1:
		return None
	member_indexes = candidates[0]
	text_members = tuple(nodes[index] for index in member_indexes if isinstance(nodes[index], SourceTextRegion))
	anchor_members = tuple(nodes[index] for index in member_indexes if isinstance(nodes[index], SourceImageRegion))
	bounds = nodes[next(iter(member_indexes))].bounds
	for index in member_indexes:
		node = nodes[index]
		bounds = bounds.union(node.bounds)
	if bounds.left == 0.0 and bounds.top == 0.0 and bounds.right == 1.0 and bounds.bottom == 1.0:
		return None
	bounds, protected_text_shape_ids = title_excluded_content_bounds(bounds, text_members, title)
	return ContentRegionPlan(
		"mixed-visual-1", bounds, tuple(sorted(text_members, key=lambda item: item.source_ordinal)),
		tuple(sorted(anchor_members, key=lambda item: item.source_ordinal)), protected_text_shape_ids,
		"mixed-visual", "single connected materially coupled visual graph",
	)
def shared_figure_row_region(
	text_regions: tuple[SourceTextRegion, ...],
	image_regions: tuple[SourceImageRegion, ...],
	title: TitleDecision,
) -> ContentRegionPlan | None:
	"""Keep a shared caption with a coherent row of peer source figures."""
	images = tuple(image for image in image_regions if image.source_kind == "picture")
	available = tuple(region for region in text_regions if region is not title.region)
	candidates: list[tuple[tuple[SourceImageRegion, ...], SourceTextRegion]] = []
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
	bounds, protected = title_excluded_content_bounds(bounds, (caption,), title)
	return ContentRegionPlan(
		"shared-figure-row-1", bounds, (caption,), row, protected,
		"shared-figure-row", "peer figure row with one shared caption",
	)
def coherent_figure_row(row: tuple[SourceImageRegion, ...]) -> bool:
	"""Recognize two or three separated, similarly sized figures in one row."""
	if len(row) not in {2, 3} or any(geometry.substantially_overlaps(first.bounds, second.bounds)
		for index, first in enumerate(row) for second in row[index + 1:]):
		return False
	centers = tuple((item.bounds.top + item.bounds.bottom) / 2 for item in row)
	return max(centers) - min(centers) <= SHARED_FIGURE_ROW_ALIGNMENT_RATIO
def shared_row_caption(region: SourceTextRegion,
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
	text_regions: tuple[SourceTextRegion, ...], image_regions: tuple[SourceImageRegion, ...],
	title: TitleDecision,
) -> ContentRegionPlan | None:
	"""Reserve two same-band figures only when their side labels are mutual."""
	pictures = tuple(item for item in image_regions if item.source_kind == "picture")
	available = tuple(item for item in text_regions if item is not title.region)
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
	bounds, protected = title_excluded_content_bounds(bounds, tuple(label for _picture, label in pairs), title)
	return ContentRegionPlan("repeated-labeled-figure-1", bounds, tuple(label for _picture, label in pairs),
		pictures, protected, "repeated-labeled-figure", "mutual same-band side labels")
def nearest_side_label(picture: SourceImageRegion, labels: tuple[SourceTextRegion, ...]) -> SourceTextRegion | None:
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
def nearest_side_picture(label: SourceTextRegion, pictures: tuple[SourceImageRegion, ...]) -> SourceImageRegion | None:
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
	title: TitleDecision,
	content: ContentRegionPlan | None,
) -> bool:
	"""Keep an unmarked heading inside the visual component it labels."""
	if title.region is None or content is None:
		return False
	if title.region.placeholder_confidence > 0.0:
		return False
	return any(geometry.center_is_within(title.region.bounds, image.bounds)
		for image in content.image_regions)
def absorb_connected_connectors(
	content: ContentRegionPlan | None,
	image_regions: tuple[SourceImageRegion, ...],
	title: TitleDecision,
) -> ContentRegionPlan | None:
	"""Add uniquely aligned visible connectors to an already-coupled source region."""
	if content is None:
		return None
	connectors = tuple(item for item in image_regions if item.source_kind == "connector"
		and item not in content.image_regions and connector_belongs_to(item.bounds, content.bounds))
	if not connectors:
		return content
	bounds = union_bounds((content.bounds, *(item.bounds for item in connectors)))
	bounds, protected = title_excluded_content_bounds(bounds, content.text_regions, title)
	return dataclasses.replace(content, bounds=bounds,
		image_regions=tuple(sorted((*content.image_regions, *connectors), key=lambda item: item.source_ordinal)),
		protected_text_shape_ids=protected,
		classification_reason=f"{content.classification_reason}; aligned connectors")
def absorb_coarse_crop_text(
	content: ContentRegionPlan | None,
	text_regions: tuple[SourceTextRegion, ...],
	title: TitleDecision,
) -> ContentRegionPlan | None:
	"""Assign one short coarse placeholder only when its complete shape is inside one crop."""
	if content is None:
		return None
	candidates = tuple(region for region in text_regions if (
		region is not title.region and region not in content.text_regions
		and region.source_kind != "table" and region.placeholder_confidence >= 0.75
		and len(region.paragraphs) <= 2 and bounds_contains(content.bounds, region.bounds, CROP_EDGE_LABEL_PADDING)
	))
	if len(candidates) != 1:
		return content
	region = candidates[0]
	bounds = content.bounds.union(region.bounds)
	if bounds.left == 0.0 and bounds.top == 0.0 and bounds.right == 1.0 and bounds.bottom == 1.0:
		raise ValueError("coarse crop expansion would cover the full slide")
	bounds, protected = title_excluded_content_bounds(bounds, (*content.text_regions, region), title)
	return dataclasses.replace(content, bounds=bounds, protected_text_shape_ids=protected,
		text_regions=tuple(sorted((*content.text_regions, region), key=lambda item: item.source_ordinal)),
		classification_reason=f"{content.classification_reason}; enclosed coarse text")
def absorb_contained_vector_label(
	content: ContentRegionPlan | None, text_regions: tuple[SourceTextRegion, ...], title: TitleDecision,
) -> ContentRegionPlan | None:
	"""Keep one short coarse label with its already-qualified vector scaffold."""
	if content is None:
		return None
	vectors = tuple(item for item in content.image_regions if item.source_kind in {"vector", "connector"})
	candidates = tuple(region for region in text_regions if region is not title.region
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
	"""Require center and every edge within a bounded crop padding envelope."""
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
	text_regions: tuple[SourceTextRegion, ...], image_regions: tuple[SourceImageRegion, ...],
) -> tuple[SourceImageRegion, ...]:
	"""Omit only isolated tiny vectors; long or related marks remain reviewable."""
	return tuple(item for item in image_regions if item.source_kind in {"vector", "connector"}
		and item.bounds.width * item.bounds.height < TINY_DECORATIVE_VECTOR_AREA_RATIO
		and max(item.bounds.width, item.bounds.height) < TINY_DECORATIVE_VECTOR_SPAN_RATIO
		and not any(bounds_are_near(item.bounds, other.bounds) for other in (*text_regions, *image_regions)
			if other is not item))
def slot_plans(
	text_regions: tuple[SourceTextRegion, ...],
	image_regions: tuple[SourceImageRegion, ...],
	content: ContentRegionPlan | None,
	tables: tuple[TablePlan, ...],
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
			return tuple(SlotPlan(slide_lib.layouts.LAYOUTS[name].slot_names[index], units[item][0], units[item][1])
				for index, item in enumerate(order))
		return (SlotPlan("body", ordinary, ordinary_images),)
	direct = tuple(("text", region) for region in ordinary) + tuple(("image", image) for image in ordinary_images)
	flow_items = tuple(sorted(direct, key=lambda item: (item[1].bounds.top, item[1].bounds.left, item[1].source_ordinal)))
	if not pairs and ordinary and ordinary_images and len(flow_items) > 1 and all(
		first[1].bounds.bottom <= second[1].bounds.top + FLOW_TEXT_BOUNDARY_EPSILON_RATIO and
		topology.material(first[1].bounds.left, first[1].bounds.width, second[1].bounds.left, second[1].bounds.width)
		for first, second in zip(flow_items, flow_items[1:])
	):
		return (SlotPlan("body", tuple(item for kind, item in flow_items if kind == "text"),
			tuple(item for kind, item in flow_items if kind == "image"), True),)
	match = topology.ordinary_layout_match(tuple(item.bounds for _kind, item in direct))
	if match is not None:
		name, order = match
		return tuple(
			SlotPlan(slide_lib.layouts.LAYOUTS[name].slot_names[index], (item,) if kind == "text" else (),
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
	text_regions: tuple[SourceTextRegion, ...],
	image_regions: tuple[SourceImageRegion, ...],
) -> SlidePlan:
	"""Build one deterministic import plan from validated source regions."""
	choice = multiple_choice_plan(text_regions, image_regions)
	if choice is not None:
		return SlidePlan(
			TitleDecision(None, "multiple-choice structure"), (), multiple_choice=choice,
		)
	title = select_solitary_title(text_regions, image_regions) or select_title(text_regions)
	tables = table_plans(text_regions, image_regions, title); review_reason = None
	inset_pair = None if tables else visual_relations.coarse_body_styled_inset(text_regions, image_regions, title)
	picture_inset = None if tables else visual_relations.coarse_body_picture_inset(text_regions, image_regions, title)
	if not tables and regular_text_grid(text_regions):
		review_reason = "regular text lattice requires border and span reconstruction"
	omitted_vectors = decorative_vectors(text_regions, image_regions)
	planning_images = tuple(item for item in image_regions if item not in omitted_vectors)
	repeated = None if tables else repeated_labeled_figure_region(text_regions, planning_images, title)
	shared = None if tables or repeated is not None else shared_figure_row_region(text_regions, planning_images, title)
	interior = None if tables else visual_relations.single_interior_overlay_label(text_regions, image_regions, title,
		lambda members: topology.ordinary_layout_viable(tuple(item.bounds for item in (*members.text_regions, *members.image_regions))))
	potential_content = None
	if repeated is not None:
		potential_content = repeated
	elif shared is not None:
		potential_content = shared
	elif not tables:
		potential_content = content_region(
			text_regions, planning_images, TitleDecision(None, "component check"),
		)
	if interior is None and title_is_component_member(title, potential_content):
		title = TitleDecision(None, "diagram component membership")
	try:
		content = repeated if repeated is not None else shared
		if content is None and interior is not None:
			content = ContentRegionPlan("single-interior-overlay-label-1", interior.bounds, interior.text_regions, interior.image_regions,
				interior.protected_text_shape_ids, "single-interior-overlay-label", "sole material interior overlay label")
		if content is None:
			content = None if tables else content_region(text_regions, planning_images, title)
		if not tables:
			relation = visual_relations.dominant_image_narrative(text_regions, planning_images, title)
			if relation is not None:
				content = ContentRegionPlan("dominant-image-narrative-1", relation.bounds, relation.text_regions,
					relation.image_regions, relation.protected_text_shape_ids, "dominant-image-narrative", "unique bounded visual composition")
			elif content is None:
				relation = visual_relations.coupled_visual_sequence(text_regions, planning_images, title,
					lambda members: topology.ordinary_layout_viable(tuple(item.bounds for item in members.image_regions)))
				if relation is not None:
					content = ContentRegionPlan("coupled-visual-sequence-1", relation.bounds, relation.text_regions, relation.image_regions,
						relation.protected_text_shape_ids, "coupled-visual-sequence", "unique bounded visual composition")
		content = absorb_connected_connectors(content, planning_images, title)
		extension = visual_relations.styled_callout_extension(content, text_regions, title)
		if extension is not None:
			content = dataclasses.replace(content, bounds=extension.bounds, text_regions=extension.text_regions,
				protected_text_shape_ids=extension.protected_text_shape_ids, classification_reason=f"{content.classification_reason}; styled callout")
		if content is None and inset_pair is not None:
			content = ContentRegionPlan("styled-inset-key-1", inset_pair.key.bounds, (inset_pair.key,), (), (),
				"styled-inset-key", "styled inset key paired with coarse object body")
		content = absorb_contained_vector_label(content, text_regions, title)
		content = absorb_coarse_crop_text(content, text_regions, title)
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
	plan = SlidePlan(title, slots, content, tables, review_reason, None, omitted_vectors, review_vectors)
	return plan


#============================================
def require_region_asset(
	content: ContentRegionPlan | None,
	assets: collections.abc.Mapping[str, str] | None,
) -> str | None:
	"""Resolve a renderer-produced region asset without inventing a fallback.
	ASVS 5.3.2: region assets use internally generated keys, never archive names.
	"""
	if content is None:
		return None
	if assets is None or content.asset_key not in assets:
		raise ValueError(
			f"required renderer asset is missing for {content.asset_key}; "
			"supply the coupled-region asset before emission"
		)
	asset = assets[content.asset_key]
	if not asset:
		raise ValueError(f"renderer supplied an empty asset for {content.asset_key}")
	return asset
