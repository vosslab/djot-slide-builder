"""Recognition of complete multiple-choice source-slide structures."""
import dataclasses
import slide_lib.importers.figure_regions as figure_regions
import slide_lib.importers.geometry as geometry
import slide_lib.importers.source_regions as source_regions

MULTIPLE_CHOICE_MIN_PLACEHOLDER_CONFIDENCE = 0.75
MULTIPLE_CHOICE_ANSWER_MIN_CENTER_X_RATIO = 0.65
MULTIPLE_CHOICE_ANSWER_MIN_CENTER_Y_RATIO = 0.65
MULTIPLE_CHOICE_ANSWER_MAX_WIDTH_RATIO = 0.50
MC_ANSWER_MAX_NORMALIZED_AREA_RATIO = 0.16
MC_ANSWER_BELOW_GAP_RATIO = 0.08
MULTIPLE_CHOICE_FIGURE_MAX_WIDTH_RATIO = 0.60
MULTIPLE_CHOICE_FIGURE_MAX_HEIGHT_RATIO = 0.35
MULTIPLE_CHOICE_FIGURE_CENTER_OFFSET_RATIO = 0.20
MULTIPLE_CHOICE_FIGURE_TOP_CENTER_RATIO = 0.35


@dataclasses.dataclass(frozen=True)
class MultipleChoicePlan:
	"""A complete structural question-and-answer pattern from one source slide."""
	question: source_regions.SourceTextRegion
	answer: source_regions.SourceTextRegion
	image: source_regions.SourceImageRegion | None
	reason: str
	question_visual_region: figure_regions.ContentRegionPlan | None = None


def has_visible_list_structure(region: source_regions.SourceTextRegion) -> bool:
	"""Require source hierarchy that separates one prompt from visible options."""
	if len(region.paragraphs) < 2:
		return False
	prompt_level = region.paragraphs[0][0]
	return any(level > prompt_level for level, _text in region.paragraphs[1:])


def answer_below_question(answer: geometry.NormalizedBounds,
		question: geometry.NormalizedBounds) -> bool:
	"""Allow a compact lower-right callout directly beneath its primary prompt."""
	return (answer.top >= question.bottom - geometry.FLOW_BORDER_CONTACT_RATIO
		and answer.top - question.bottom <= MC_ANSWER_BELOW_GAP_RATIO
		and min(answer.right, question.right) > max(answer.left, question.left))


def is_multiple_choice_answer(region: source_regions.SourceTextRegion,
		question: source_regions.SourceTextRegion) -> bool:
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
		and (figure_regions.bounds_contains(question.bounds, region.bounds, 0.0)
			or answer_below_question(region.bounds, question.bounds))
	)


def is_multiple_choice_figure(image: source_regions.SourceImageRegion,
		question: source_regions.SourceTextRegion) -> bool:
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
		text_regions: tuple[source_regions.SourceTextRegion, ...],
		image_regions: tuple[source_regions.SourceImageRegion, ...],
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
	visual = figure_regions.ContentRegionPlan("multiple-choice-visual-1", bounds, overlay_text,
		(*visuals, *connectors), "multiple-choice-overlay", "question-associated overlay component")
	return MultipleChoicePlan(question, answer, None,
		"complete question-list-answer structure with associated overlay", visual)
