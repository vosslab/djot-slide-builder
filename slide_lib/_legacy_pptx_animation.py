"""Temporary source-model animation bridge; delete with ``layouts.py`` in WP-I1."""

import slide_lib.editable_text
import slide_lib.native_model
from slide_lib.pptx_animation import AnimationError


def register_reveal(slide: object, shape: object, reveal: slide_lib.native_model.Reveal | None,
		paragraph_ranges: tuple[slide_lib.editable_text.ParagraphRevealRange, ...] = ()) -> None:
	"""Transfer legacy source intent to the compatibility timing writer."""
	writer = getattr(slide, "_slide_animation_writer", None)
	if writer is None:
		if reveal is not None or paragraph_ranges:
			raise AnimationError("native reveal registration requires an animation writer")
		return
	for paragraph_range in paragraph_ranges:
		writer.register(shape, paragraph_range.reveal,
			(paragraph_range.first_index, paragraph_range.last_index))
	if reveal is not None and reveal.sequence is slide_lib.native_model.RevealSequence.OBJECT:
		writer.register(shape, reveal)


def register_text_reveal(slide: object, frame: object,
		block: slide_lib.native_model.Heading | slide_lib.native_model.Paragraph |
		slide_lib.native_model.ListBlock) -> None:
	"""Register a legacy text block's whole-object or list cascade reveal."""
	projection = slide_lib.editable_text.project_block(block)
	register_reveal(slide, frame._parent, block.reveal, projection.reveal_ranges)
