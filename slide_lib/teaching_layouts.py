"""Apply the semantic term contract for dedicated definition slides."""

import dataclasses

import slide_lib.djot_errors
import slide_lib.native_model


#============================================
def definition_item(item: slide_lib.native_model.ListItem) -> slide_lib.native_model.ListItem:
	"""Emphasize a leading term while preserving its explanation and nested examples."""
	first, *rest = item.inlines
	if isinstance(first, slide_lib.native_model.Strong):
		term = slide_lib.native_model.StyledSpan((first,), underline=True)
		inlines = (term, *rest)
	elif isinstance(first, slide_lib.native_model.StyledSpan) and any(
			isinstance(child, slide_lib.native_model.Strong) for child in first.children):
		inlines = (dataclasses.replace(first, underline=True), *rest)
	elif isinstance(first, slide_lib.native_model.Text) and ": " in first.value:
		name, explanation = first.value.split(": ", 1)
		if not name.strip():
			raise slide_lib.djot_errors.source_error(item.location, "definition term must not be empty")
		term = slide_lib.native_model.StyledSpan((slide_lib.native_model.Strong(
			(slide_lib.native_model.Text(name),)),), underline=True)
		inlines = (term, slide_lib.native_model.Text(": " + explanation), *rest)
	else:
		raise slide_lib.djot_errors.source_error(item.location,
			"definitions items need Term: explanation or a leading bold term")
	result = dataclasses.replace(item, inlines=inlines)
	return result


#============================================
def format_definitions(slide: slide_lib.native_model.Slide) -> slide_lib.native_model.Slide:
	"""Enforce term emphasis only on top-level definition entries, leaving examples plain."""
	if slide.layout_class != "definitions":
		return slide
	count = 0
	cells = []
	for cell in slide.cells:
		blocks = []
		for block in cell.blocks:
			if isinstance(block, slide_lib.native_model.ListBlock):
				count += len(block.items)
				block = dataclasses.replace(block, items=tuple(definition_item(item)
					for item in block.items))
			blocks.append(block)
		cells.append(dataclasses.replace(cell, blocks=tuple(blocks)))
	if not count:
		raise slide_lib.djot_errors.source_error(slide.location,
			"definitions layout requires a list of terms in @body")
	result = dataclasses.replace(slide, cells=tuple(cells))
	return result
