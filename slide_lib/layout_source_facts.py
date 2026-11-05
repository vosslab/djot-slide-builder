"""Collect source constructs that lack an approved editable layout projection."""

import slide_lib.layout_model
import slide_lib.native_model


def unsupported_facts(slide: slide_lib.native_model.Slide) -> tuple[slide_lib.layout_model.UnsupportedSourceFact, ...]:
	"""Collect constructs without a deliberately approved editable projection."""
	facts: list[slide_lib.layout_model.UnsupportedSourceFact] = []
	blocks = slide.blocks + tuple(block for cell in slide.cells for block in cell.blocks)
	for block in descendant_blocks(blocks):
		attributes = _unsupported_attributes(block)
		if isinstance(block, (slide_lib.native_model.CodeBlock, slide_lib.native_model.QuoteBlock)) or attributes:
			facts.append(slide_lib.layout_model.UnsupportedSourceFact(block.location, type(block).__name__, attributes))
		if isinstance(block, slide_lib.native_model.ListBlock):
			for item in _descendant_list_items(block):
				attributes = _unsupported_attributes(item)
				if attributes:
					facts.append(slide_lib.layout_model.UnsupportedSourceFact(item.location, type(item).__name__, attributes))
	return tuple(facts)


def descendant_blocks(blocks: tuple[slide_lib.native_model.Block, ...]) -> tuple[slide_lib.native_model.Block, ...]:
	"""Return nested source blocks in reading order."""
	result: list[slide_lib.native_model.Block] = []
	for block in blocks:
		result.append(block)
		if isinstance(block, slide_lib.native_model.QuoteBlock):
			result.extend(descendant_blocks(block.blocks))
		elif isinstance(block, slide_lib.native_model.ListBlock):
			for item in block.items:
				for child in item.children:
					result.extend(descendant_blocks((child,)))
	return tuple(result)


def descendant_inlines(inlines: tuple[slide_lib.native_model.Inline, ...]) -> tuple[slide_lib.native_model.Inline, ...]:
	"""Return nested inline source facts in reading order."""
	result: list[slide_lib.native_model.Inline] = []
	for inline in inlines:
		result.append(inline)
		if isinstance(inline, (slide_lib.native_model.Strong, slide_lib.native_model.Emphasis,
				slide_lib.native_model.Link, slide_lib.native_model.StyledSpan)):
			result.extend(descendant_inlines(inline.children))
	return tuple(result)


def block_inlines(block: slide_lib.native_model.Block) -> tuple[slide_lib.native_model.Inline, ...]:
	"""Return nested inline facts from one editable source block."""
	if isinstance(block, (slide_lib.native_model.Heading, slide_lib.native_model.Paragraph)):
		return descendant_inlines(block.inlines)
	if isinstance(block, slide_lib.native_model.ListBlock):
		return tuple(inline for item in block.items for inline in descendant_inlines(item.inlines))
	if isinstance(block, slide_lib.native_model.Table):
		return tuple(inline for row in (block.headers,) + block.rows for cell in row
			for inline in descendant_inlines(cell.inlines))
	return ()


def _unsupported_attributes(item: slide_lib.native_model.Block | slide_lib.native_model.ListItem) -> tuple[slide_lib.native_model.Attribute, ...]:
	attributes = getattr(item, "attributes", ())
	if isinstance(item, (slide_lib.native_model.Heading, slide_lib.native_model.Paragraph,
			slide_lib.native_model.ListBlock, slide_lib.native_model.ListItem,
			slide_lib.native_model.ImageArrow, slide_lib.native_model.ImageOutline)):
		return tuple(attribute for attribute in attributes if attribute.name != "color")
	return attributes


def _descendant_list_items(block: slide_lib.native_model.ListBlock) -> tuple[slide_lib.native_model.ListItem, ...]:
	result: list[slide_lib.native_model.ListItem] = []
	for item in block.items:
		result.append(item)
		for child in item.children:
			result.extend(_descendant_list_items(child))
	return tuple(result)
