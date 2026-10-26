"""Bind bounded click-to-remove covers to their immediately preceding image."""

import dataclasses

import slide_lib.djot_errors
import slide_lib.layout_content
import slide_lib.layout_model
import slide_lib.layout_object_builders
import slide_lib.native_model
import slide_lib.presentation_theme


def extract(source: slide_lib.native_model.Slide) -> tuple[slide_lib.native_model.Slide,
		tuple[tuple[slide_lib.native_model.SourceLocation, slide_lib.native_model.ImageCover], ...]]:
	"""Validate image ownership and remove covers from space-consuming content flow."""
	bindings = []
	def content(blocks: tuple[slide_lib.native_model.Block, ...]) -> tuple[slide_lib.native_model.Block, ...]:
		remaining = []
		previous = None
		for block in blocks:
			if isinstance(block, slide_lib.native_model.ImageCover):
				# ASVS 2.2.1: accept only bounded covers with explicit image ownership and click intent.
				if not isinstance(previous, slide_lib.native_model.Image):
					raise slide_lib.djot_errors.source_error(block.location,
						"cover must immediately follow its image in the same region")
				if previous.reveal is not None or block.attributes or block.reveal != slide_lib.native_model.Reveal(
						slide_lib.native_model.RevealEffect.DISAPPEAR, slide_lib.native_model.RevealSequence.OBJECT):
					raise slide_lib.djot_errors.source_error(block.location,
						"cover requires disappear, no attributes, and an initially visible image")
				bindings.append((previous.location, block))
			else:
				remaining.append(block)
			previous = block
		return tuple(remaining)
	root_blocks = content(source.blocks)
	cells = tuple(dataclasses.replace(cell, blocks=content(cell.blocks)) for cell in source.cells)
	return dataclasses.replace(source, blocks=root_blocks, cells=cells), tuple(bindings)


def project(page: slide_lib.layout_model.LayoutSlide,
		bindings: tuple[tuple[slide_lib.native_model.SourceLocation, slide_lib.native_model.ImageCover], ...],
		theme: slide_lib.presentation_theme.PresentationTheme) -> slide_lib.layout_model.LayoutSlide:
	"""Place covers against final displayed image geometry, preserving source click order."""
	if not bindings:
		return page
	# Import at the call boundary: validation also uses cover extraction during builder import.
	import slide_lib.layout_builders
	objects = list(page.objects)
	for location, cover in bindings:
		owners = [item for item in page.objects if item.source == location
			and isinstance(item.content, slide_lib.layout_content.PictureContent)]
		if len(owners) != 1:
			raise slide_lib.djot_errors.source_error(cover.location, "cover requires one native image destination")
		order = max((item.reading_order for item in objects), default=-1) + 1
		item = slide_lib.layout_object_builders.image_overlay_object(
			f"{owners[0].object_id}-cover", cover, owners[0].content.placement.displayed_rectangle,
			owners[0].slot_id, order, theme)
		objects.insert(objects.index(owners[0]) + 1,
			dataclasses.replace(item, z_index=max(obj.z_index for obj in objects) + 1))
	objects = [dataclasses.replace(item, reading_order=index) for index, item in enumerate(objects)]
	return dataclasses.replace(page, objects=tuple(slide_lib.layout_builders._renumber_reveals(objects)))
