"""Stack whole equation boxes and native paragraphs without inline SVG flow."""

import dataclasses
import math

import slide_lib.layout_content
import slide_lib.layout_primitives
import slide_lib.native_model


#============================================
def has_math(inlines: tuple[slide_lib.native_model.Inline, ...]) -> bool:
	"""Find equations nested inside authored inline styles."""
	return any(isinstance(inline, slide_lib.native_model.InlineMath) or
		(hasattr(inline, "children") and has_math(inline.children)) for inline in inlines)


#============================================
def semantic_runs(inlines: tuple[slide_lib.native_model.Inline, ...],
		bold: bool = False, italic: bool = False
		) -> tuple[slide_lib.layout_content.InlineContent, ...]:
	"""Resolve authored equation styles before sizing and placing a block."""
	# Import at the call boundary: object builders themselves use measurement.
	import slide_lib.layout_object_builders
	return slide_lib.layout_object_builders.resolved_runs(inlines, "172033", "172033",
		bold, italic)


#============================================
def equation_run(runs: tuple[slide_lib.layout_content.InlineContent, ...]
		) -> slide_lib.layout_content.MathRun:
	"""Return the single equation in a validated equation-only paragraph."""
	values = [run for run in runs if not (
		isinstance(run, slide_lib.layout_content.TextRun) and not run.text.strip())]
	if len(values) != 1 or not isinstance(values[0], slide_lib.layout_content.MathRun):
		raise ValueError("equations must occupy a complete paragraph or list item")
	return values[0]


#============================================
def paragraph_metrics(inlines: tuple[slide_lib.native_model.Inline, ...], size: float,
		width: float, level: int, listed: bool, bold: bool, italic: bool,
		session: object) -> tuple[float, float, int]:
	"""Fit one complete equation box using the ordinary block sizing contract."""
	run = equation_run(semantic_runs(inlines, bold, italic))
	formula = session.equations[(run.text, run.display)]
	scale = 12700 / session.theme.emu_per_logical_pixel
	available = width - (session.theme.list_levels[level].text_position if listed else 0)
	height = max(size * session.theme.ordinary_line_spacing_em,
		(formula.ascent + formula.descent) * size) * scale
	return (height if formula.width * size * scale <= available else math.inf,
		height / scale, 1)


#============================================
def position_text(content: slide_lib.layout_content.TextContent, width: float, height: float,
		frame: slide_lib.layout_primitives.FrameTextProperties, session: object
		) -> slide_lib.layout_content.TextContent:
	"""Stack intact prose paragraphs and whole equations; never position prose fragments."""
	if not any(isinstance(run, slide_lib.layout_content.MathRun)
			for paragraph in content.paragraphs for run in paragraph.inlines):
		return content
	scale = 12700 / session.theme.emu_per_logical_pixel
	placed = []
	y = frame.padding.top
	usable_width = width - frame.padding.left - frame.padding.right
	for index, paragraph in enumerate(content.paragraphs):
		if not paragraph.display:
			continue
		properties = paragraph.properties
		size = paragraph.typography.selected_size_pt
		y += properties.space_before_pt * scale
		is_equation = any(isinstance(run, slide_lib.layout_content.MathRun)
			for run in paragraph.inlines)
		if not is_equation:
			# LibreOffice owns all glyph positions and wrapping inside this native paragraph.
			paragraph_height = paragraph.measured_height
			if paragraph_height <= 0:
				raise ValueError("native paragraphs beside equations require measured block height")
			native = dataclasses.replace(paragraph, properties=dataclasses.replace(
				properties, space_before_pt=0, space_after_pt=0))
			rectangle = slide_lib.layout_primitives.LogicalRectangle(
				frame.padding.left, y, usable_width, paragraph_height)
			placed.append(slide_lib.layout_content.PositionedRun(native, rectangle, size, index))
		else:
			run = equation_run(paragraph.inlines)
			formula = session.equations[(run.text, run.display)]
			equation_width = formula.width * size * scale
			equation_height = (formula.ascent + formula.descent) * size * scale
			paragraph_height = max(equation_height,
				size * session.theme.ordinary_line_spacing_em * scale)
			indent = properties.indent_start_pt * scale
			available = usable_width - indent - properties.indent_end_pt * scale
			x = frame.padding.left + indent
			if properties.horizontal_alignment is slide_lib.layout_primitives.HorizontalAlignment.CENTER:
				x += (available - equation_width) / 2
			elif properties.horizontal_alignment is slide_lib.layout_primitives.HorizontalAlignment.END:
				x += available - equation_width
			top = y + (paragraph_height - equation_height) / 2
			rectangle = slide_lib.layout_primitives.LogicalRectangle(
				x, top, max(equation_width, 0.001), max(equation_height, 0.001))
			path = formula.image_path(run.style.foreground, session.math_directory)
			placed.append(slide_lib.layout_content.PositionedRun(run, rectangle, size, index, path))
			if paragraph.list_metadata is not None:
				# Leave list-marker font, size, and numbering to the native list writer.
				native_height = size * session.theme.ordinary_line_spacing_em * scale
				marker = dataclasses.replace(paragraph,
					# Impress suppresses list markers on empty/space-only paragraphs.
					inlines=(slide_lib.layout_content.TextRun("\u200b", run.style),),
					properties=dataclasses.replace(properties, space_before_pt=0,
						space_after_pt=0, line_spacing_pt=native_height / scale))
				marker_box = slide_lib.layout_primitives.LogicalRectangle(
					frame.padding.left, y + (paragraph_height - native_height) / 2,
					usable_width, native_height)
				placed.append(slide_lib.layout_content.PositionedRun(
					marker, marker_box, size, index))

		y += paragraph_height + properties.space_after_pt * scale
	extent = y - frame.padding.top
	remaining = max(0, height - frame.padding.top - frame.padding.bottom - extent)
	offset = remaining / 2 if frame.vertical_alignment is \
		slide_lib.layout_primitives.VerticalAlignment.MIDDLE else (
			remaining if frame.vertical_alignment is
			slide_lib.layout_primitives.VerticalAlignment.BOTTOM else 0)
	return dataclasses.replace(content, positioned_runs=tuple(dataclasses.replace(run,
		rectangle=dataclasses.replace(run.rectangle, y=run.rectangle.y + offset))
		for run in placed))


#============================================
def finalize_object(item: object, session: object) -> object:
	"""Resolve text, table-cell, and callout equation placement after final allocation."""
	content = item.content
	if isinstance(content, slide_lib.layout_content.TextContent):
		content = position_text(content, item.rectangle.width, item.rectangle.height,
			item.frame_text, session)
	elif isinstance(content, slide_lib.layout_content.ShapeContent) and content.text is not None:
		content = dataclasses.replace(content, text=position_text(content.text,
			item.rectangle.width, item.rectangle.height, item.frame_text, session))
	elif isinstance(content, slide_lib.layout_content.TableContent):
		if any(isinstance(run, slide_lib.layout_content.MathRun)
				for row in content.header_rows + content.body_rows for cell in row.cells
				for paragraph in cell.paragraphs for run in paragraph.inlines):
			# Impress stretches rows to the frame height. Give it exactly the
			# measured row sum so table backgrounds and equation baselines agree.
			item = dataclasses.replace(item, rectangle=dataclasses.replace(
				item.rectangle, height=sum(content.row_heights)))
		content = position_table(content, session)
	return dataclasses.replace(item, content=content)


#============================================
def position_table(content: slide_lib.layout_content.TableContent,
		session: object) -> slide_lib.layout_content.TableContent:
	"""Place equation-only cell content over the native table's unchanged backgrounds."""
	placed = []
	rows = []
	y = 0.0
	for row_index, row in enumerate(content.header_rows + content.body_rows):
		cells = []
		x = 0.0
		for column, cell in enumerate(row.cells):
			width = sum(content.column_widths[column:column + cell.column_span])
			height = sum(content.row_heights[row_index:row_index + cell.row_span])
			frame = slide_lib.layout_primitives.FrameTextProperties(cell.padding,
				cell.vertical_alignment, slide_lib.layout_primitives.TextWrap.WRAP,
				slide_lib.layout_primitives.OverflowPolicy.CLIP)
			text = position_text(slide_lib.layout_content.TextContent(cell.paragraphs),
				width, height, frame, session)
			if text.positioned_runs:
				placed.extend(dataclasses.replace(run, rectangle=dataclasses.replace(
					run.rectangle, x=run.rectangle.x + x, y=run.rectangle.y + y))
					for run in text.positioned_runs)
				cell = dataclasses.replace(cell, paragraphs=())
			cells.append(cell)
			x += width
		rows.append(dataclasses.replace(row, cells=tuple(cells)))
		y += content.row_heights[row_index]
	header_count = len(content.header_rows)
	return dataclasses.replace(content, header_rows=tuple(rows[:header_count]),
		body_rows=tuple(rows[header_count:]), positioned_runs=tuple(placed))
