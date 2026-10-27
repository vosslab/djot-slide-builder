"""Build editable native content objects from resolved layout facts."""

import dataclasses
import math
import re

import slide_lib.editable_text
import slide_lib.djot_sources
import slide_lib.layout_content
import slide_lib.layout_measurement
import slide_lib.layout_model
import slide_lib.layout_primitives
import slide_lib.native_model
import slide_lib.presentation_theme


FOREGROUND = "172033"
WHITE = "FFFFFF"
OVERLAY_LINE_WIDTH_PT = 3.0
OVERLAY_ARROW_WIDTH_PT = 12.0


def text_object(object_id: str, block: object,
		rectangle: slide_lib.layout_primitives.LogicalRectangle,
		size: float, floor: float, role: slide_lib.layout_primitives.StyleRole,
		frame: slide_lib.layout_primitives.FrameTextProperties, slot: str | None, order: int,
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
		slide_lib.layout_content.ListMetadata | None,
		tuple[slide_lib.native_model.Attribute, ...]]] = []
	for block in blocks:
		if isinstance(block, (slide_lib.native_model.Heading, slide_lib.native_model.Paragraph)):
			entries.append((block.inlines, False, None, block.attributes))
		elif isinstance(block, slide_lib.native_model.ListBlock):
			for item in slide_lib.editable_text.project_list(block):
				kind = slide_lib.layout_primitives.ListKind.ORDERED if item.ordered \
					else slide_lib.layout_primitives.ListKind.UNORDERED
				entries.append((item.inlines, True,
					slide_lib.layout_content.ListMetadata(kind, item.level, item.start),
					item.attributes))
	paragraphs: list[slide_lib.layout_content.TextParagraph] = []
	for index, (inlines, listed, metadata, attributes) in enumerate(entries):
		level = metadata.level if metadata is not None else 0
		properties = slide_lib.layout_measurement.paragraph_properties(
			inlines, size, width, theme, level, listed, index == len(entries) - 1,
			bold, session=session)
		available = width - (theme.list_levels[level].text_position if listed else 0.0)
		paragraph_color = _authored_text_color(attributes, color, theme.accent_color)
		paragraphs.append(slide_lib.layout_content.TextParagraph(
			_fragment_runs(resolved_runs(inlines, paragraph_color, theme.accent_color, bold),
				size, available, theme, session),
			typography, properties, True, metadata,
			slide_lib.layout_measurement.paragraph_height(
				inlines, size, width, theme, level, listed, bold, session=session)))
	return slide_lib.layout_content.TextContent(tuple(paragraphs))


def _authored_text_color(attributes: tuple[slide_lib.native_model.Attribute, ...],
		default: str, accent_color: str) -> str:
	"""Resolve the nearest validated block or list-item text color."""
	colors = [attribute.value for attribute in attributes if attribute.name == "color"]
	if not colors:
		return default
	name = colors[-1]
	if name is None:
		raise ValueError("validated text-color attributes require a value")
	return slide_lib.presentation_theme.resolve_text_color(name, accent_color)


def resolved_runs(inlines: tuple[slide_lib.native_model.Inline, ...], color: str,
		accent_color: str,
		bold: bool = False, italic: bool = False,
		link: str | None = None) -> tuple[slide_lib.layout_content.InlineContent, ...]:
	"""Resolve recursive strong/emphasis/link styling before adapters receive runs."""
	runs: list[slide_lib.layout_content.InlineContent] = []
	for inline in inlines:
		if isinstance(inline, slide_lib.native_model.InlineMath):
			style = slide_lib.layout_content.RunStyle(
				slide_lib.presentation_theme.ORDINARY_FONT_FAMILY,
				color, bold=bold, italic=italic, link_url=link)
			runs.append(slide_lib.layout_content.MathRun(inline.value, inline.display, style))
		elif isinstance(inline, slide_lib.native_model.Text):
			style = slide_lib.layout_content.RunStyle(
				slide_lib.presentation_theme.ORDINARY_FONT_FAMILY,
				color, bold=bold, italic=italic, link_url=link)
			if slide_lib.presentation_theme.is_visible_url(inline.value):
				style = dataclasses.replace(style,
					font_family=slide_lib.presentation_theme.NARROW_FONT_FAMILY,
					literal_url=True, link_url=link or inline.value, underline=True)
			runs.append(slide_lib.layout_content.TextRun(inline.value, style))
		elif isinstance(inline, slide_lib.native_model.InlineCode):
			style = slide_lib.layout_content.RunStyle(
				slide_lib.presentation_theme.MONOSPACE_FONT_FAMILY,
				color, bold=bold, italic=italic, code=True, link_url=link)
			if slide_lib.presentation_theme.is_visible_url(inline.value):
				style = dataclasses.replace(style,
					font_family=slide_lib.presentation_theme.NARROW_FONT_FAMILY,
					literal_url=True, link_url=link or inline.value, underline=True)
			runs.append(slide_lib.layout_content.TextRun(inline.value, style))
		elif isinstance(inline, slide_lib.native_model.Break):
			runs.append(slide_lib.layout_content.LineBreak())
		elif isinstance(inline, slide_lib.native_model.Strong):
			runs.extend(resolved_runs(inline.children, color, accent_color, True, italic, link))
		elif isinstance(inline, slide_lib.native_model.Emphasis):
			runs.extend(resolved_runs(inline.children, color, accent_color, bold, True, link))
		elif isinstance(inline, slide_lib.native_model.Link):
			literal = slide_lib.presentation_theme.is_visible_url(
				slide_lib.layout_measurement.visible_text(inline.children))
			for run in resolved_runs(inline.children, accent_color, accent_color,
					bold, italic, inline.url):
				if isinstance(run, (slide_lib.layout_content.TextRun, slide_lib.layout_content.MathRun)):
					style = dataclasses.replace(run.style, font_family=
						slide_lib.presentation_theme.NARROW_FONT_FAMILY
						if literal else run.style.font_family,
						underline=True, literal_url=literal)
					runs.append(dataclasses.replace(run, style=style))
				else:
					runs.append(run)
		elif isinstance(inline, slide_lib.native_model.StyledSpan):
			color_name = inline.color.value if isinstance(inline.color,
				slide_lib.native_model.TextColor) else inline.color
			span_color = slide_lib.presentation_theme.resolve_text_color(
				color_name, accent_color) if color_name is not None else color
			for run in resolved_runs(inline.children, span_color, accent_color,
					bold, italic, link):
				if isinstance(run, (slide_lib.layout_content.TextRun, slide_lib.layout_content.MathRun)):
					style = dataclasses.replace(run.style,
						underline=inline.underline or run.style.underline,
						strikethrough=inline.strikethrough or run.style.strikethrough,
						background="FFF2A8" if inline.highlight else run.style.background,
						position=run.style.position or inline.position)
					run = dataclasses.replace(run, style=style)
				runs.append(run)
	return tuple(runs)


def _fragment_runs(inlines: tuple[slide_lib.layout_content.InlineContent, ...], size: float,
		width: float, theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession | None = None,
		) -> tuple[slide_lib.layout_content.InlineContent, ...]:
	"""Emit exact-width, grapheme-safe break markers retained by native adapters."""
	if inlines and all(isinstance(run, slide_lib.layout_content.TextRun)
			and not run.style.literal_url for run in inlines):
		measure = session or slide_lib.layout_measurement.MeasurementSession(theme)
		tokens = tuple((run.text, run.style.font_family, run.style.bold, run.style.italic, False)
			for run in inlines)
		lines, _widths = measure.wrap_tokens(tokens, size, max(width, 1.0))
		ordinary, _widths = measure.wrap_tokens(tokens, size, max(width, 1.0), balance=False)
		if lines != ordinary:
			balanced = []
			for number, line in enumerate(lines):
				if number:
					balanced.append(slide_lib.layout_content.LineBreak(automatic=True))
				for text, _family, _bold, _italic, _literal, _size, source_index in line:
					balanced.append(dataclasses.replace(inlines[source_index], text=text))
			return tuple(balanced)
	result: list[slide_lib.layout_content.InlineContent] = []
	url_sizes = {}
	if any(isinstance(run, slide_lib.layout_content.TextRun) and run.style.literal_url for run in inlines):
		measure = session or slide_lib.layout_measurement.MeasurementSession(theme)
		tokens = tuple((run.text, run.style.font_family, run.style.bold, run.style.italic,
			run.style.literal_url) if isinstance(run, slide_lib.layout_content.TextRun)
			else ("\n", "", False, False, False) for run in inlines)
		lines, _widths = measure.wrap_tokens(tokens, size, max(width, 1.0))
		for line_index, line in enumerate(lines):
			for position, token in enumerate(line):
				if token[4] and token[6] not in url_sizes:
					url_sizes[token[6]] = (token[5], line_index > 0 and position == 0)
	for index, inline in enumerate(inlines):
		if not isinstance(inline, slide_lib.layout_content.TextRun):
			result.append(inline)
			continue
		style = inline.style
		if style.literal_url:
			url_size, new_line = url_sizes[index]
			if new_line and result and not isinstance(result[-1], slide_lib.layout_content.LineBreak):
				result.append(slide_lib.layout_content.LineBreak())
			result.append(dataclasses.replace(inline, style=dataclasses.replace(style, size_pt=url_size)))
			continue
		run_size = slide_lib.presentation_theme.inline_size_pt(size, style.literal_url)
		for token in re.findall(r"\s+|\S+", inline.text):
			fragments = slide_lib.layout_measurement.fragment_text(token, style.font_family,
				style.bold, style.italic, run_size, width, theme, session)
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
	size = selected_size if selected_size is not None else \
		slide_lib.layout_measurement.select_table_size(table, rectangle,
			theme.ordinary_body_size_pt, theme.body_floor_size_pt,
			theme, layout, slot, session)
	typography = slide_lib.layout_primitives.Typography(
		slide_lib.layout_primitives.StyleRole.TABLE_BODY,
		slide_lib.presentation_theme.ORDINARY_FONT_FAMILY, size, size,
		min(theme.body_floor_size_pt, size))
	measurements = slide_lib.layout_measurement.table_measurements(
		table, size, rectangle.width, theme, session)
	def row_content(cells: tuple[slide_lib.native_model.TableCell, ...],
			header: bool) -> slide_lib.layout_content.TableRow:
		"""Project one semantic table row."""
		projected = []
		labels = ["".join(run.text for run in resolved_runs(cell.inlines, FOREGROUND,
			theme.accent_color, False) if isinstance(run, slide_lib.layout_content.TextRun))
			for cell in cells]
		total = not header and labels[0].strip().casefold() in ("total", "totals", "grand total")
		for index, (column, cell) in enumerate(slide_lib.native_model.table_cell_positions(cells)):
			width = slide_lib.layout_measurement.table_cell_text_width(
				sum(measurements.column_widths[column:column + cell.column_span]), theme)
			properties = slide_lib.layout_measurement.paragraph_properties(
				cell.inlines, size, width, theme, terminal=True, bold=header or total, session=session)
			if header:
				properties = dataclasses.replace(properties,
					horizontal_alignment=slide_lib.layout_primitives.HorizontalAlignment.CENTER)
			if not header and re.fullmatch(r"[+−–-]?(?:[0-9][0-9,]*(?:\.[0-9]+)?|\.[0-9]+)%?", labels[index].strip()):
				properties = dataclasses.replace(properties,
					horizontal_alignment=slide_lib.layout_primitives.HorizontalAlignment.END)
			if cell.text_alignment is not None:
				alignment = {"left": slide_lib.layout_primitives.HorizontalAlignment.START,
					"center": slide_lib.layout_primitives.HorizontalAlignment.CENTER,
					"right": slide_lib.layout_primitives.HorizontalAlignment.END}[cell.text_alignment]
				properties = dataclasses.replace(properties, horizontal_alignment=alignment)
			paragraph = slide_lib.layout_content.TextParagraph(_fragment_runs(
				resolved_runs(cell.inlines, "000000" if header else FOREGROUND,
					theme.accent_color, header or total), size, width, theme, session),
				typography, properties)
			projected.append(slide_lib.layout_content.TableCell((paragraph,),
				slide_lib.layout_primitives.Insets(
					slide_lib.layout_measurement.TABLE_HORIZONTAL_PADDING,
					slide_lib.layout_measurement.TABLE_VERTICAL_PADDING,
					slide_lib.layout_measurement.TABLE_HORIZONTAL_PADDING,
					slide_lib.layout_measurement.TABLE_VERTICAL_PADDING),
				slide_lib.layout_primitives.VerticalAlignment.MIDDLE,
				fill_role=slide_lib.layout_primitives.StyleRole.ACCENT_TINT if total else None,
				fill_color=cell.background_color[1:] if cell.background_color else None,
				column_span=cell.column_span))
		return slide_lib.layout_content.TableRow(tuple(projected))
	headers = (row_content(table.headers, True),) if table.headers else ()
	body = tuple(row_content(row, False) for row in table.rows)
	content = slide_lib.layout_content.TableContent(headers, body,
		measurements.column_widths, measurements.row_heights,
		slide_lib.layout_content.TableStyle(
			slide_lib.layout_primitives.StyleRole.TABLE_HEADER,
			slide_lib.layout_primitives.StyleRole.TABLE_BODY,
			slide_lib.layout_primitives.StyleRole.ACCENT,
			slide_lib.layout_measurement.TABLE_BORDER_WIDTH_PT,
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
	source_path = image.source
	if image.source.startswith("repo:"):
		source_path = str(slide_lib.djot_sources.image_path(deck, image))
	content = slide_lib.layout_content.PictureContent(source_path, placement, accessibility)
	return slide_lib.layout_model.LayoutObject(object_id,
		slide_lib.layout_primitives.PresentationRole.COMPONENT,
		slide_lib.layout_primitives.StyleRole.BODY, allocation,
		slide_lib.layout_primitives.ObjectLayer.CONTENT, order, order, content, None,
		slot, None, slide_lib.layout_primitives.PlaceholderKind.NONE, image.location,
		reveal_targets(object_id, (image,), order))


def image_overlay_object(object_id: str,
		overlay: slide_lib.native_model.ImageArrow | slide_lib.native_model.ImageOutline,
		displayed_image: slide_lib.layout_primitives.LogicalRectangle,
		slot: str, order: int, theme: slide_lib.presentation_theme.PresentationTheme,
		) -> slide_lib.layout_model.LayoutObject:
	"""Map one normalized annotation into editable image-relative native geometry."""
	line_color = _authored_text_color(overlay.attributes, theme.accent_color,
		theme.accent_color)
	accessibility = slide_lib.layout_primitives.ObjectAccessibility(decorative=True)
	if isinstance(overlay, slide_lib.native_model.ImageArrow):
		start = slide_lib.layout_primitives.LogicalPoint(
			displayed_image.x + overlay.start_x * displayed_image.width,
			displayed_image.y + overlay.start_y * displayed_image.height)
		end = slide_lib.layout_primitives.LogicalPoint(
			displayed_image.x + overlay.end_x * displayed_image.width,
			displayed_image.y + overlay.end_y * displayed_image.height)
		content: slide_lib.layout_content.ObjectContent = slide_lib.layout_content.LineContent(
			slide_lib.layout_content.LineGeometry(start, end),
			slide_lib.layout_content.LineStyle(
				slide_lib.layout_primitives.StyleRole.ACCENT,
				OVERLAY_LINE_WIDTH_PT, slide_lib.layout_primitives.LinePattern.SOLID,
				slide_lib.layout_primitives.LineEndMarker.ARROW,
				OVERLAY_ARROW_WIDTH_PT, line_color), accessibility)
		rectangle = displayed_image
	else:
		is_cover = isinstance(overlay, slide_lib.native_model.ImageCover)
		rectangle = slide_lib.layout_primitives.LogicalRectangle(
			displayed_image.x + overlay.x * displayed_image.width,
			displayed_image.y + overlay.y * displayed_image.height,
			overlay.width * displayed_image.width,
			overlay.height * displayed_image.height)
		content = slide_lib.layout_content.ShapeContent(
			slide_lib.layout_primitives.ShapeKind.RECTANGLE,
			slide_lib.layout_content.ShapeStyle(
				slide_lib.layout_primitives.StyleRole.DECORATION if is_cover else None,
				slide_lib.layout_primitives.StyleRole.ACCENT,
				OVERLAY_LINE_WIDTH_PT, slide_lib.layout_primitives.LinePattern.NONE if is_cover
				else slide_lib.layout_primitives.LinePattern.SOLID,
				line_color=line_color), accessibility)
	return slide_lib.layout_model.LayoutObject(object_id,
		slide_lib.layout_primitives.PresentationRole.GRAPHIC,
		slide_lib.layout_primitives.StyleRole.ACCENT, rectangle,
		slide_lib.layout_primitives.ObjectLayer.FOREGROUND, order, order, content,
		slot_id=slot, source=overlay.location,
		reveal_targets=reveal_targets(object_id, (overlay,), order))


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
