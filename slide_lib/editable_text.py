"""Source-neutral projections of editable text blocks into Office paragraphs."""

# Standard Library
from dataclasses import dataclass

# Local Modules
import slide_lib.native_model


@dataclass(frozen=True)
class EditableParagraph:
	"""One editable paragraph, including list presentation metadata."""
	inlines: tuple[slide_lib.native_model.Inline, ...]
	level: int
	ordered: bool
	paragraph_only: bool
	start: int


@dataclass(frozen=True)
class ParagraphRevealRange:
	"""One inclusive native paragraph target and its source-owned reveal."""
	first_index: int
	last_index: int
	reveal: slide_lib.native_model.Reveal


@dataclass(frozen=True)
class EditableTextProjection:
	"""Editable paragraphs and source-relative reveal groups for one text block."""
	paragraphs: tuple[EditableParagraph, ...]
	reveal_ranges: tuple[ParagraphRevealRange, ...]


#============================================
def project_list(block: slide_lib.native_model.ListBlock, level: int = 0) -> tuple[EditableParagraph, ...]:
	"""Flatten a nested list while preserving its native paragraph metadata."""
	paragraphs: list[EditableParagraph] = []
	for offset, item in enumerate(block.items):
		paragraphs.append(EditableParagraph(item.inlines, level, block.ordered, False, block.start + offset))
		for child in item.children:
			paragraphs.extend(project_list(child, level + 1))
	return tuple(paragraphs)


#============================================
def item_reveal_ranges(block: slide_lib.native_model.ListBlock, start: int = 0) -> tuple[ParagraphRevealRange, ...]:
	"""Return terminal item reveals as inclusive ranges that retain descendants."""
	ranges: list[ParagraphRevealRange] = []
	position = start
	for item in block.items:
		first_index = position
		position += 1
		for child in item.children:
			child_ranges = item_reveal_ranges(child, position)
			ranges.extend(child_ranges)
			position += len(project_list(child))
		if item.reveal is not None:
			ranges.append(ParagraphRevealRange(first_index, position - 1, item.reveal))
	return tuple(ranges)


#============================================
def cascade_ranges(block: slide_lib.native_model.ListBlock) -> tuple[ParagraphRevealRange, ...]:
	"""Return top-level cascade ranges, each including all nested descendants."""
	if block.reveal is None:
		return ()
	ranges: list[ParagraphRevealRange] = []
	start = 0
	for item in block.items:
		count = 1 + sum(len(project_list(child)) for child in item.children)
		ranges.append(ParagraphRevealRange(start, start + count - 1, block.reveal))
		start += count
	return tuple(ranges)


#============================================
def project_block(block: slide_lib.native_model.Heading | slide_lib.native_model.Paragraph |
		slide_lib.native_model.ListBlock) -> EditableTextProjection:
	"""Project a supported editable text block without choosing a renderer."""
	if isinstance(block, slide_lib.native_model.ListBlock):
		paragraphs = project_list(block)
		ranges = item_reveal_ranges(block)
		if block.reveal is not None and block.reveal.sequence is slide_lib.native_model.RevealSequence.PARAGRAPHS:
			ranges = cascade_ranges(block) + ranges
		return EditableTextProjection(paragraphs, ranges)
	return EditableTextProjection((EditableParagraph(block.inlines, 0, False, True, 1),), ())


#============================================
def has_reveal(block: slide_lib.native_model.Paragraph | slide_lib.native_model.ListBlock) -> bool:
	"""Return whether a text block or one of its editable paragraphs reveals."""
	return block.reveal is not None or bool(project_block(block).reveal_ranges)


#============================================
def flow_items(block: slide_lib.native_model.Paragraph | slide_lib.native_model.ListBlock) -> list[tuple[tuple[slide_lib.native_model.Inline, ...], int, bool, bool, int]]:
	"""Return a renderer-neutral tuple form for one editable flow block."""
	return [(paragraph.inlines, paragraph.level, paragraph.ordered, paragraph.paragraph_only,
		paragraph.start) for paragraph in project_block(block).paragraphs]
