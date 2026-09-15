"""Build editable native content objects from resolved layout facts."""

import dataclasses
import math
import re

import slide_lib.editable_text
import slide_lib.layout_content
import slide_lib.layout_measurement
import slide_lib.layout_model
import slide_lib.layout_primitives
import slide_lib.native_model
import slide_lib.presentation_theme


FOREGROUND = "172033"
ACCENT = "24578F"
WHITE = "FFFFFF"


def text_object(object_id: str, block: object,
		rectangle: slide_lib.layout_primitives.LogicalRectangle,
		size: float, floor: float, role: slide_lib.layout_primitives.StyleRole,
		frame: slide_lib.layout_primitives.FrameTextProperties, slot: str, order: int,
		placeholder: slide_lib.layout_primitives.PlaceholderKind,
		theme: slide_lib.presentation_theme.PresentationTheme, bold: bool = False,
		session: slide_lib.layout_measurement.MeasurementSession | None = None,
		) -> slide_lib.layout_model.LayoutObject:
	"""Create one resolved editable text object with stable reveal identity."""
	blocks = (block,) if isinstance(block, (slide_lib.native_model.Heading,
		slide_lib.native_model.Paragraph, slide_lib.native_model.ListBlock)) else tuple(block)
	measure = slide_lib.layout_measurement.text_frame_measurement(rectangle)
	content = text_content(blocks, size, floor, role, FOREGROUND,
		measure.wrapping_extent, theme, bold, session)
	if frame.vertical_alignment is slide_lib.layout_primitives.VerticalAlignment.MIDDLE or \
			role is slide_lib.layout_primitives.StyleRole.TITLE:
		content = dataclasses.replace(content, paragraphs=tuple(dataclasses.replace(paragraph,
			properties=dataclasses.replace(paragraph.properties,
				horizontal_alignment=slide_lib.layout_primitives.HorizontalAlignment.CENTER))
			for paragraph in content.paragraphs))
	presentation = slot if placeholder is not slide_lib.layout_primitives.PlaceholderKind.NONE else None
	role_value = slide_lib.layout_primitives.PresentationRole.TITLE \
		if placeholder is slide_lib.layout_primitives.PlaceholderKind.TITLE else (
			slide_lib.layout_primitives.PresentationRole.SUBTITLE
			if placeholder is slide_lib.layout_primitives.PlaceholderKind.SUBTITLE
			else slide_lib.layout_primitives.PresentationRole.OUTLINE)
	location = block.location if hasattr(block, "location") else (
		block[0].location if block else None)
	return slide_lib.layout_model.LayoutObject(object_id, role_value, role, rectangle,
		slide_lib.layout_primitives.ObjectLayer.LAYOUT if presentation
		else slide_lib.layout_primitives.ObjectLayer.CONTENT,
		order, order, content, frame, slot, presentation, placeholder, location,
		reveal_targets(object_id, blocks, order))


def text_content(blocks: tuple[slide_lib.native_model.Block, ...], size: float, floor: float,
		role: slide_lib.layout_primitives.StyleRole, color: str, width: float,
		theme: slide_lib.presentation_theme.PresentationTheme,
		bold: bool = False,
		session: slide_lib.layout_measurement.MeasurementSession | None = None,
		) -> slide_lib.layout_content.TextContent:
	"""Project supported inline/list semantics into fully resolved text runs."""
	typography = slide_lib.layout_primitives.Typography(
		role, slide_lib.presentation_theme.ORDINARY_FONT_FAMILY, size, size, min(floor, size))
	entries: list[tuple[tuple[slide_lib.native_model.Inline, ...], bool,
		slide_lib.layout_content.ListMetadata | None]] = []
	for block in blocks:
		if isinstance(block, (slide_lib.native_model.Heading, slide_lib.native_model.Paragraph)):
			entries.append((block.inlines, False, None))
		elif isinstance(block, slide_lib.native_model.ListBlock):
			for item in slide_lib.editable_text.project_list(block):
				kind = slide_lib.layout_primitives.ListKind.ORDERED if item.ordered \
					else slide_lib.layout_primitives.ListKind.UNORDERED
				entries.append((item.inlines, True,
					slide_lib.layout_content.ListMetadata(kind, item.level, item.start)))
	paragraphs: list[slide_lib.layout_content.TextParagraph] = []
	for index, (inlines, listed, metadata) in enumerate(entries):
		level = metadata.level if metadata is not None else 0
		properties = slide_lib.layout_measurement.paragraph_properties(
			inlines, size, width, theme, level, listed, index == len(entries) - 1,
			bold, session=session)
		available = width - (theme.list_levels[level].text_position if listed else 0.0)
		paragraphs.append(slide_lib.layout_content.TextParagraph(
			_fragment_runs(resolved_runs(inlines, color, bold), size, available, theme, session),
			typography, properties, True, metadata))
	return slide_lib.layout_content.TextContent(tuple(paragraphs))


def resolved_runs(inlines: tuple[slide_lib.native_model.Inline, ...], color: str,
		bold: bool = False, italic: bool = False,
		link: str | None = None) -> tuple[slide_lib.layout_content.InlineContent, ...]:
	"""Resolve recursive strong/emphasis/link styling before adapters receive runs."""
	runs: list[slide_lib.layout_content.InlineContent] = []
	for inline in inlines:
		if isinstance(inline, slide_lib.native_model.Text):
			style = slide_lib.layout_content.RunStyle(
				slide_lib.presentation_theme.ORDINARY_FONT_FAMILY,
				color, bold=bold, italic=italic, link_url=link)
			runs.append(slide_lib.layout_content.TextRun(inline.value, style))
		elif isinstance(inline, slide_lib.native_model.InlineCode):
			style = slide_lib.layout_content.RunStyle(
				slide_lib.presentation_theme.ORDINARY_FONT_FAMILY,
				color, bold=bold, italic=italic, code=True, link_url=link)
			runs.append(slide_lib.layout_content.TextRun(inline.value, style))
		elif isinstance(inline, slide_lib.native_model.Break):
			runs.append(slide_lib.layout_content.LineBreak())
		elif isinstance(inline, slide_lib.native_model.Strong):
			runs.extend(resolved_runs(inline.children, color, True, italic, link))
		elif isinstance(inline, slide_lib.native_model.Emphasis):
			runs.extend(resolved_runs(inline.children, color, bold, True, link))
		elif isinstance(inline, slide_lib.native_model.Link):
			literal = slide_lib.layout_measurement.visible_text(inline.children) == inline.url
			for run in resolved_runs(inline.children, ACCENT, bold, italic, inline.url):
				if isinstance(run, slide_lib.layout_content.TextRun):
					style = slide_lib.layout_content.RunStyle(
						"PT Sans Narrow" if literal else run.style.font_family,
						run.style.foreground, True, run.style.bold, run.style.italic,
						run.style.code, run.style.link_url, literal)
					runs.append(slide_lib.layout_content.TextRun(run.text, style))
				else:
					runs.append(run)
	return tuple(runs)


def _fragment_runs(inlines: tuple[slide_lib.layout_content.InlineContent, ...], size: float,
		width: float, theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession | None = None,
		) -> tuple[slide_lib.layout_content.InlineContent, ...]:
	"""Emit exact-width, grapheme-safe break markers retained by native adapters."""
	result: list[slide_lib.layout_content.InlineContent] = []
	for inline in inlines:
		if not isinstance(inline, slide_lib.layout_content.TextRun):
			result.append(inline)
			continue
		style = inline.style
		for token in re.findall(r"\s+|\S+", inline.text):
			fragments = slide_lib.layout_measurement.fragment_text(token, style.font_family,
				style.bold, style.italic, size, width, theme, session)
			for index, fragment in enumerate(fragments):
				if index:
					result.append(slide_lib.layout_content.LineBreak())
				if result and isinstance(result[-1], slide_lib.layout_content.TextRun) and \
						result[-1].style == style:
					result[-1] = dataclasses.replace(result[-1], text=result[-1].text + fragment)
				else:
					result.append(slide_lib.layout_content.TextRun(fragment, style))
	return tuple(result)


def table_object(object_id: str, table: slide_lib.native_model.Table,
		rectangle: slide_lib.layout_primitives.LogicalRectangle,
		theme: slide_lib.presentation_theme.PresentationTheme, layout: str, slot: str,
		order: int, frame: slide_lib.layout_primitives.FrameTextProperties,
		selected_size: float | None = None,
		session: slide_lib.layout_measurement.MeasurementSession | None = None,
		) -> slide_lib.layout_model.LayoutObject:
	"""Project a rectangular semantic table with resolved 28-to-24 point fitting."""
	rows = ((table.headers, True),) if table.headers else ()
	rows += tuple((row, False) for row in table.rows)
	columns = len(rows[0][0])
	size = selected_size if selected_size is not None else \
		slide_lib.layout_measurement.select_table_size(table, rectangle,
			theme.ordinary_body_size_pt, theme.body_floor_size_pt,
			theme, layout, slot, session)
	typography = slide_lib.layout_primitives.Typography(
		slide_lib.layout_primitives.StyleRole.TABLE_BODY,
		slide_lib.presentation_theme.ORDINARY_FONT_FAMILY, size, size,
		min(theme.body_floor_size_pt, size))
	def row_content(cells: tuple[tuple[slide_lib.native_model.Inline, ...], ...],
			header: bool) -> slide_lib.layout_content.TableRow:
		"""Project one semantic table row."""
		return slide_lib.layout_content.TableRow(tuple(slide_lib.layout_content.TableCell(
			(slide_lib.layout_content.TextParagraph(_fragment_runs(
				resolved_runs(cell, WHITE if header else FOREGROUND, header), size,
				rectangle.width / columns - 12, theme, session), typography,
				slide_lib.layout_measurement.paragraph_properties(
					cell, size, rectangle.width / columns - 12,
					theme, terminal=True, session=session)),),
			slide_lib.layout_primitives.Insets(
				slide_lib.layout_measurement.TABLE_HORIZONTAL_PADDING,
				slide_lib.layout_measurement.TABLE_VERTICAL_PADDING,
				slide_lib.layout_measurement.TABLE_HORIZONTAL_PADDING,
				slide_lib.layout_measurement.TABLE_VERTICAL_PADDING),
			slide_lib.layout_primitives.VerticalAlignment.MIDDLE) for cell in cells))
	headers = (row_content(table.headers, True),) if table.headers else ()
	body = tuple(row_content(row, False) for row in table.rows)
	content = slide_lib.layout_content.TableContent(headers, body,
		tuple(rectangle.width / columns for _ in range(columns)),
		tuple(rectangle.height / len(rows) for _ in rows),
		slide_lib.layout_content.TableStyle(
			slide_lib.layout_primitives.StyleRole.TABLE_HEADER,
			slide_lib.layout_primitives.StyleRole.TABLE_BODY,
			slide_lib.layout_primitives.StyleRole.ACCENT, 1,
			slide_lib.layout_primitives.LinePattern.SOLID))
	return slide_lib.layout_model.LayoutObject(object_id,
		slide_lib.layout_primitives.PresentationRole.OUTLINE,
		slide_lib.layout_primitives.StyleRole.BODY, rectangle,
		slide_lib.layout_primitives.ObjectLayer.CONTENT, order, order, content, frame,
		slot, None, slide_lib.layout_primitives.PlaceholderKind.NONE, table.location)


def picture_object(object_id: str, deck: slide_lib.native_model.Deck,
		image: slide_lib.native_model.Image,
		allocation: slide_lib.layout_primitives.LogicalRectangle,
		slot: str, order: int) -> slide_lib.layout_model.LayoutObject:
	"""Resolve contained display geometry and accessibility before adapter projection."""
	width, height = slide_lib.layout_measurement.image_size(deck, image)
	scale = math.nextafter(min(allocation.width / width, allocation.height / height), 0.0)
	display_width, display_height = width * scale, height * scale
	display = slide_lib.layout_primitives.LogicalRectangle(
		allocation.x + (allocation.width - display_width) / 2,
		allocation.y + (allocation.height - display_height) / 2,
		display_width, display_height)
	placement = slide_lib.layout_content.PicturePlacement(allocation, display,
		slide_lib.layout_primitives.PictureFit.CONTAIN,
		slide_lib.layout_primitives.CropInsets(0, 0, 0, 0))
	accessibility = slide_lib.layout_primitives.ObjectAccessibility(
		image.title or "Component image", image.alt_text)
	content = slide_lib.layout_content.PictureContent(image.source, placement, accessibility)
	return slide_lib.layout_model.LayoutObject(object_id,
		slide_lib.layout_primitives.PresentationRole.COMPONENT,
		slide_lib.layout_primitives.StyleRole.BODY, allocation,
		slide_lib.layout_primitives.ObjectLayer.CONTENT, order, order, content, None,
		slot, None, slide_lib.layout_primitives.PlaceholderKind.NONE, image.location,
		reveal_targets(object_id, (image,), order))


def reveal_targets(object_id: str, blocks: tuple[object, ...],
		order: int) -> tuple[slide_lib.layout_model.RevealTarget, ...]:
	"""Create stable whole-object and inclusive paragraph reveal targets."""
	targets: list[slide_lib.layout_model.RevealTarget] = []
	paragraph_offset = 0
	for block in blocks:
		if not isinstance(block, (slide_lib.native_model.Heading,
				slide_lib.native_model.Paragraph, slide_lib.native_model.ListBlock)):
			reveal = getattr(block, "reveal", None)
			if reveal is not None:
				target_id = f"{object_id}-reveal-{len(targets)}"
				targets.append(slide_lib.layout_model.RevealTarget(
					target_id, object_id, reveal, order))
			continue
		projection = slide_lib.editable_text.project_block(block)
		reveal = getattr(block, "reveal", None)
		if reveal is not None and reveal.sequence is slide_lib.native_model.RevealSequence.OBJECT:
			target_id = f"{object_id}-reveal-{len(targets)}"
			targets.append(slide_lib.layout_model.RevealTarget(
				target_id, object_id, reveal, order))
		for reveal_range in projection.reveal_ranges:
			target_id = f"{object_id}-reveal-{len(targets)}"
			indexes = tuple(range(paragraph_offset + reveal_range.first_index,
				paragraph_offset + reveal_range.last_index + 1))
			targets.append(slide_lib.layout_model.RevealTarget(
				target_id, object_id, reveal_range.reveal, order, indexes))
		paragraph_offset += len(projection.paragraphs)
	return tuple(targets)
