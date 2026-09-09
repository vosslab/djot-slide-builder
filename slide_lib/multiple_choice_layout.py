"""Parse and measure adaptive multiple-choice regions before object construction."""

import dataclasses

import slide_lib.capacity_report
import slide_lib.layout_measurement
import slide_lib.layout_primitives
import slide_lib.native_model
import slide_lib.presentation_theme


QUESTION_FLOOR_SIZE_PT = 18.0


@dataclasses.dataclass(frozen=True)
class QuestionParts:
	"""Validated semantic regions inside one multiple-choice question."""

	image: slide_lib.native_model.Image | None
	context_labels: tuple[slide_lib.native_model.ListBlock, ...]
	context_prose: tuple[slide_lib.native_model.Block, ...]
	stem: tuple[slide_lib.native_model.Block, ...]
	choices: tuple[slide_lib.native_model.ListBlock, ...]


@dataclasses.dataclass(frozen=True)
class PromptMetrics:
	"""Measured geometry for context followed by a full-width question stem."""

	height: float
	leading_height: float
	label_columns: int
	label_item_heights: tuple[float, ...]
	prose_height: float
	stem_height: float


@dataclasses.dataclass(frozen=True)
class AnswerTrial:
	"""Represent one answer popup fit at one explored width without publishing a concern."""

	size_pt: float
	height: float


@dataclasses.dataclass(frozen=True)
class AdaptiveChoiceSelection:
	"""Retain one final question/choice geometry selected from adaptive trials."""

	question_size_pt: float
	left_height: float
	right_height: float
	split: int
	popup_column: int
	left_width: float
	answer_size_pt: float
	answer_height: float


@dataclasses.dataclass(frozen=True)
class AdaptiveChoiceResult:
	"""Keep the final geometry separate from evidence about unrepresentable answer trials."""

	selection: AdaptiveChoiceSelection | None
	answer_has_serializer_fit: bool


def question_parts(question: slide_lib.native_model.Cell) -> QuestionParts:
	"""Separate one validated question into context, stem, and choice regions."""
	# ASVS 2.2.1: the parser validates this closed block vocabulary before layout.
	image = next((block for block in question.blocks
		if isinstance(block, slide_lib.native_model.Image)), None)
	context_labels: list[slide_lib.native_model.ListBlock] = []
	context_prose: list[slide_lib.native_model.Block] = []
	stem: list[slide_lib.native_model.Block] = []
	choices: list[slide_lib.native_model.ListBlock] = []
	nested_choices = any(item.children for block in question.blocks
		if isinstance(block, slide_lib.native_model.ListBlock) for item in block.items)
	found_nested = False
	for block in question.blocks:
		if isinstance(block, slide_lib.native_model.Image):
			continue
		if isinstance(block, slide_lib.native_model.Paragraph):
			(context_prose if nested_choices and not found_nested else stem).append(block)
			continue
		if not isinstance(block, slide_lib.native_model.ListBlock):
			raise ValueError(
				f"{block.location.path}:{block.location.line}: unsupported multiple-choice question block")
		for offset, item in enumerate(block.items):
			item_block = dataclasses.replace(block, start=block.start + offset,
				items=(dataclasses.replace(item, children=()),))
			if item.children:
				stem.append(item_block)
				found_nested = True
				for child in item.children:
					choices.extend(dataclasses.replace(child,
						start=child.start + child_offset, items=(child_item,))
						for child_offset, child_item in enumerate(child.items))
			elif nested_choices and not found_nested:
				context_labels.append(item_block)
			else:
				choices.append(item_block)
	if len(choices) < 2:
		location = question.blocks[0].location
		raise ValueError(
			f"{location.path}:{location.line}: adaptive multiple-choice layout requires at least two choices")
	context_labels.sort(key=lambda block: block.location.line)
	context_prose.sort(key=lambda block: block.location.line)
	stem.sort(key=lambda block: block.location.line)
	choices.sort(key=lambda block: block.location.line)
	return QuestionParts(image, tuple(context_labels), tuple(context_prose),
		tuple(stem), tuple(choices))


def prompt_metrics(parts: QuestionParts, size: float, width: float,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession) -> PromptMetrics:
	"""Measure paired leading context and its question stem."""
	gap = 12.0
	if parts.context_labels:
		leading_width = (width - 30) / 2
		label_height, columns, label_heights = context_measure(
			parts.context_labels, size, leading_width, theme, session)
		prose_width = leading_width
	else:
		label_height, columns, label_heights = 0.0, 1, ()
		prose_width = width
	prose_height = slide_lib.layout_measurement.text_height(
		slide_lib.layout_measurement.items_for(parts.context_prose), size,
		prose_width, theme, session)
	leading_height = label_height + prose_height + \
		(gap if label_height and prose_height else 0)
	stem_width = prose_width if parts.context_labels else width
	stem_height = slide_lib.layout_measurement.text_height(
		slide_lib.layout_measurement.items_for(parts.stem), size, stem_width, theme, session)
	height = max(leading_height, stem_height) if parts.context_labels else \
		leading_height + stem_height + (gap if leading_height and stem_height else 0)
	return PromptMetrics(height, leading_height, columns,
		label_heights, prose_height, stem_height)


def context_measure(blocks: tuple[slide_lib.native_model.Block, ...],
		size: float, width: float, theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession) -> tuple[float, int, tuple[float, ...]]:
	"""Choose the shallowest editable grid for leading question labels."""
	if not blocks:
		return 0.0, 1, ()
	gap = 12.0
	best: tuple[tuple[float, int], int, tuple[float, ...]] | None = None
	for columns in range(1, min(4, len(blocks)) + 1):
		column_width = (width - gap * (columns - 1)) / columns
		heights = tuple(slide_lib.layout_measurement.text_height(
			slide_lib.layout_measurement.items_for((block,)), size, column_width,
			theme, session) for block in blocks)
		row_heights = tuple(max(heights[start:start + columns])
			for start in range(0, len(heights), columns))
		total = sum(row_heights) + gap * (len(row_heights) - 1)
		rank = total, -columns
		if best is None or rank < best[0]:
			best = rank, columns, heights
	assert best is not None
	return best[0][0], best[1], best[2]


def answer_trial(items: tuple[
		tuple[tuple[slide_lib.native_model.Inline, ...], int, bool], ...],
		width: float, answer: slide_lib.native_model.Cell,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession) -> AnswerTrial | None:
	"""Measure one answer trial without turning a rejected width into a deck failure."""
	inner_width = width - 36
	measurement = slide_lib.layout_measurement.text_frame_measurement(
		slide_lib.layout_primitives.LogicalRectangle(0, 0, inner_width, 210))
	size = slide_lib.layout_measurement.largest_fitting_size(theme.ordinary_body_size_pt,
		slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT,
		lambda value: slide_lib.layout_measurement.text_height(items, value,
			measurement.wrapping_extent, theme, session) <= measurement.available_extent)
	if size is None:
		return None
	height = max(90.0, slide_lib.layout_measurement.text_height(
		items, size, inner_width, theme, session) + 20)
	return AnswerTrial(size, height)


#============================================
def select_adaptive_choice_geometry(parts: QuestionParts, answer_items: tuple[
		tuple[tuple[slide_lib.native_model.Inline, ...], int, bool], ...],
		answer: slide_lib.native_model.Cell,
		rectangle: slide_lib.layout_primitives.LogicalRectangle, image_height: float,
		content_gap: float, column_gap: float,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession
		) -> AdaptiveChoiceResult:
	"""Find the largest serializer-safe adaptive question and answer geometry."""
	answer_has_serializer_fit = False
	for quarters in range(int(theme.ordinary_body_size_pt * 4),
			int(slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT * 4) - 1, -1):
		size = quarters / 4
		prompt = prompt_metrics(parts, size, rectangle.width, theme, session)
		gaps = content_gap * ((parts.image is not None) + bool(prompt.height))
		available = rectangle.height - image_height - prompt.height - gaps
		# Keep ordinary questions in their authored prompt-then-choice reading order
		# whenever one full-width editable list fits beside the separate answer reveal.
		choice_height = slide_lib.layout_measurement.text_height(
			slide_lib.layout_measurement.items_for(parts.choices), size,
			rectangle.width, theme, session)
		answer_measurement = answer_trial(answer_items, rectangle.width, answer, theme, session)
		if answer_measurement is not None:
			answer_has_serializer_fit = True
			if choice_height + answer_measurement.height + content_gap <= available:
				selection = AdaptiveChoiceSelection(size, choice_height, 0.0,
					len(parts.choices), 0, rectangle.width,
					answer_measurement.size_pt, answer_measurement.height)
				return AdaptiveChoiceResult(selection, answer_has_serializer_fit)
		best: tuple[tuple[float, float, float, int, int], float, float, float,
			float, float] | None = None
		for split in range(1, len(parts.choices)):
			for percent in range(30, 71, 5):
				left_width = (rectangle.width - column_gap) * percent / 100
				right_width = rectangle.width - column_gap - left_width
				left_height = slide_lib.layout_measurement.text_height(
					slide_lib.layout_measurement.items_for(parts.choices[:split]), size,
					left_width, theme, session)
				right_height = slide_lib.layout_measurement.text_height(
					slide_lib.layout_measurement.items_for(parts.choices[split:]), size,
					right_width, theme, session)
				popup_column = 0 if left_height <= right_height else 1
				popup_height = left_height if popup_column == 0 else right_height
				popup_width = left_width if popup_column == 0 else right_width
				answer_measurement = answer_trial(answer_items, popup_width, answer, theme, session)
				if answer_measurement is None:
					continue
				answer_has_serializer_fit = True
				answer_size = answer_measurement.size_pt
				answer_height = answer_measurement.height
				if max(left_height, right_height) > available or \
						popup_height + answer_height + content_gap > available:
					continue
				rank = (abs(percent - 50), max(left_height, right_height),
					popup_height, split, popup_column)
				if best is None or rank < best[0]:
					best = (rank, left_height, right_height, left_width,
						answer_size, answer_height)
		if best is None:
			continue
		rank, left_height, right_height, left_width, answer_size, answer_height = best
		selection = AdaptiveChoiceSelection(size, left_height, right_height, rank[3], rank[4],
			left_width, answer_size, answer_height)
		return AdaptiveChoiceResult(selection, answer_has_serializer_fit)
	return AdaptiveChoiceResult(None, answer_has_serializer_fit)


#============================================
def physical_capacity_error(question: slide_lib.native_model.Cell, answer: slide_lib.native_model.Cell,
		answer_has_serializer_fit: bool,
		theme: slide_lib.presentation_theme.PresentationTheme) -> slide_lib.capacity_report.PhysicalCapacityError:
	"""Build the final answer or geometry physical boundary after every trial completes."""
	minimum = slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT
	if not answer_has_serializer_fit:
		return slide_lib.capacity_report.PhysicalCapacityError(answer.blocks[0].location,
			"multiple-choice", "answer", theme.body_floor_size_pt,
			slide_lib.capacity_report.CapacityCause.PARAGRAPH_LIST, minimum)
	return slide_lib.capacity_report.PhysicalCapacityError(question.blocks[0].location,
		"multiple-choice", "question", QUESTION_FLOOR_SIZE_PT,
		slide_lib.capacity_report.CapacityCause.GEOMETRY_SLOT_CONSTRAINT, minimum)


#============================================
def record_final_capacity(question: slide_lib.native_model.Cell, answer: slide_lib.native_model.Cell,
		question_size: float, answer_size: float,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession) -> None:
	"""Record only the selected question and answer constraints, never trial candidates."""
	if question_size < QUESTION_FLOOR_SIZE_PT:
		session.record_capacity(question.blocks[0].location, "multiple-choice", "question",
			question_size, QUESTION_FLOOR_SIZE_PT,
			slide_lib.capacity_report.CapacityCause.GEOMETRY_SLOT_CONSTRAINT)
	if answer_size < theme.body_floor_size_pt:
		session.record_capacity(answer.blocks[0].location, "multiple-choice", "answer",
			answer_size, theme.body_floor_size_pt,
			slide_lib.capacity_report.CapacityCause.PARAGRAPH_LIST)
