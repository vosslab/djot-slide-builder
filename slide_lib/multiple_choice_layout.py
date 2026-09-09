"""Parse and measure adaptive multiple-choice regions before object construction."""

import dataclasses

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


def answer_metrics(items: tuple[
		tuple[tuple[slide_lib.native_model.Inline, ...], int, bool], ...],
		width: float, answer: slide_lib.native_model.Cell,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession) -> tuple[float, float]:
	"""Size one answer against the width offered by its selected choice column."""
	inner_width = width - 36
	size = slide_lib.layout_measurement.select_size(items,
		slide_lib.layout_primitives.LogicalRectangle(0, 0, inner_width, 210),
		theme.ordinary_body_size_pt, theme.body_floor_size_pt, theme,
		answer.blocks[0].location, "multiple-choice answer", session)
	height = max(90.0, slide_lib.layout_measurement.text_height(
		items, size, inner_width, theme, session) + 20)
	return size, height
