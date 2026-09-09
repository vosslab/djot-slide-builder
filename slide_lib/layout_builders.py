"""Build immutable physical objects from resolved layout contracts and measurements."""

import dataclasses
import math
import re

import slide_lib.capacity_report
import slide_lib.layout_measurement
import slide_lib.layout_registry
import slide_lib.editable_text
import slide_lib.layout_content
import slide_lib.layout_model
import slide_lib.layout_primitives
import slide_lib.multiple_choice_layout
import slide_lib.native_model
import slide_lib.presentation_theme


FOREGROUND = "172033"
ACCENT = "24578F"
MUTED = "526176"
WHITE = "FFFFFF"
QUIZ_FLOOR_SIZE_PT = slide_lib.multiple_choice_layout.QUESTION_FLOOR_SIZE_PT

def compile_slide(deck: slide_lib.native_model.Deck, source: slide_lib.native_model.Slide,
		theme: slide_lib.presentation_theme.PresentationTheme, index: int,
		session: slide_lib.layout_measurement.MeasurementSession | None = None) -> slide_lib.layout_model.LayoutSlide:
	"""Compile one validated semantic slide without publishing a partial deck."""
	slide_lib.layout_model.reject_unsupported_source_facts(
		slide_lib.layout_measurement.unsupported_facts(source))
	session = session or slide_lib.layout_measurement.MeasurementSession(theme)
	contract = slide_lib.layout_registry.contract_for(source.layout_class)
	if source.layout_class == "multiple-choice":
		return _multiple_choice(deck, source, theme, index, contract, session)
	if source.layout_class == "gallery":
		return _gallery(deck, source, theme, index, contract, session)
	if source.layout_class == "title-only":
		return _title_only_slide(deck, source, theme, index, contract, session)
	if not contract.slot_names:
		return _heading_slide(source, theme, index, contract, session)
	return _standard_slide(deck, source, theme, index, contract, session)

def _standard_slide(deck: slide_lib.native_model.Deck, source: slide_lib.native_model.Slide,
		theme: slide_lib.presentation_theme.PresentationTheme, index: int,
		contract: slide_lib.layout_primitives.LayoutContract,
		session: slide_lib.layout_measurement.MeasurementSession) -> slide_lib.layout_model.LayoutSlide:
	"""Measure title/body capacity, select once, then construct one physical slide."""
	title_size = _title_size_for_source(deck, source, theme, contract, session)
	return _standard_slide_at_theme(deck, source,
		dataclasses.replace(theme, standard_title_size_pt=title_size), index, contract, session)

def _title_size_for_source(deck: slide_lib.native_model.Deck, source: slide_lib.native_model.Slide,
		theme: slide_lib.presentation_theme.PresentationTheme,
		contract: slide_lib.layout_primitives.LayoutContract,
		session: slide_lib.layout_measurement.MeasurementSession) -> float:
	"""Select a physically fitting title before independent body recovery."""
	title = _root_title(source)
	if title is None:
		return theme.standard_title_size_pt
	def content_geometry(size: float) -> slide_lib.layout_primitives.LogicalRectangle | None:
		geometry = _title_geometry(title, size, theme, contract, session)
		return geometry[1] if geometry is not None else None
	size = slide_lib.layout_measurement.largest_fitting_size(
		theme.standard_title_size_pt, theme.title_floor_size_pt,
		lambda candidate: (content := content_geometry(candidate)) is not None and
		_body_fits_floor(deck, source, contract, content, theme, session))
	if size is not None:
		return size
	size = slide_lib.layout_measurement.largest_fitting_size(
		theme.standard_title_size_pt, theme.title_floor_size_pt,
		lambda candidate: content_geometry(candidate) is not None)
	if size is not None:
		return size
	return slide_lib.layout_measurement.select_title_size(
		theme.standard_title_size_pt, theme.title_floor_size_pt,
		content_geometry,
		lambda _content: False, title.location, contract.name, "title", session)
def _title_geometry(title: slide_lib.native_model.Heading, size: float,
		theme: slide_lib.presentation_theme.PresentationTheme,
		contract: slide_lib.layout_primitives.LayoutContract,
		session: slide_lib.layout_measurement.MeasurementSession
		) -> tuple[slide_lib.layout_primitives.LogicalRectangle,
			slide_lib.layout_primitives.LogicalRectangle] | None:
	"""Return the final title frame and remaining body area for one measured candidate."""
	title_rectangle = slide_lib.layout_primitives.LogicalRectangle(60, 52, 1160, 672)
	measure = slide_lib.layout_measurement.text_frame_measurement(title_rectangle)
	height = slide_lib.layout_measurement.paragraph_height(title.inlines, size, measure.wrapping_extent,
		theme, bold=True, session=session)
	reserved_height = height + 8
	if not slide_lib.layout_measurement.text_frame_fits(reserved_height + 24, measure, theme):
		return None
	title_rectangle = slide_lib.layout_primitives.LogicalRectangle(60, 52, 1160, reserved_height)
	content = slide_lib.layout_primitives.LogicalRectangle(60, 52 + reserved_height + 24, 1160,
		754 - (52 + reserved_height + 24))
	return title_rectangle, content

def _body_fits_floor(deck: slide_lib.native_model.Deck, source: slide_lib.native_model.Slide,
		contract: slide_lib.layout_primitives.LayoutContract,
		content: slide_lib.layout_primitives.LogicalRectangle,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession) -> bool:
	cells = {cell.name: cell for cell in source.cells}
	return all(_cell_fits_floor(deck, cells[name], rectangle, theme, session)
		for name, rectangle in zip(contract.slot_names,
			slide_lib.layout_measurement.slot_rectangles(contract.name, content)))

def _cell_fits_floor(deck: slide_lib.native_model.Deck, cell: slide_lib.native_model.Cell,
		rectangle: slide_lib.layout_primitives.LogicalRectangle,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession) -> bool:
	headings = tuple(block for block in cell.blocks if isinstance(block, slide_lib.native_model.Heading))
	if headings:
		heading = headings[0]
		measure = slide_lib.layout_measurement.text_frame_measurement(rectangle)
		height = slide_lib.layout_measurement.paragraph_height(
			heading.inlines, theme.body_floor_size_pt, measure.wrapping_extent, theme,
			bold=True, session=session)
		if not slide_lib.layout_measurement.text_frame_fits(height + 10, measure, theme):
			return False
		rectangle = slide_lib.layout_measurement.remaining_after_heading(rectangle, height)
	blocks = tuple(block for block in cell.blocks if not isinstance(block, slide_lib.native_model.Heading))
	images = tuple(block for block in blocks if isinstance(block, slide_lib.native_model.Image))
	tables = tuple(block for block in blocks if isinstance(block, slide_lib.native_model.Table))
	text = tuple(block for block in blocks if isinstance(block,
		(slide_lib.native_model.Paragraph, slide_lib.native_model.ListBlock)))
	if tables and len(blocks) == 1:
		return slide_lib.layout_measurement.text_frame_fits(slide_lib.layout_measurement.table_height(
			tables[0], theme.body_floor_size_pt, rectangle.width, theme, session),
			slide_lib.layout_measurement.text_frame_measurement(rectangle), theme)
	if tables or images and text or len(text) > 1 and any(
			slide_lib.editable_text.has_reveal(block) for block in text):
		if images and text:
			return _mixed_flow_allocation_at_size(deck, text, images, rectangle,
				theme.body_floor_size_pt, theme, session) is not None
		return _flow_fits_at_size(deck, blocks, rectangle, theme.body_floor_size_pt, theme, session)
	if text:
		measure = slide_lib.layout_measurement.text_frame_measurement(rectangle)
		return slide_lib.layout_measurement.text_frame_fits(slide_lib.layout_measurement.text_height(
			slide_lib.layout_measurement.items_for(text), theme.body_floor_size_pt,
			measure.wrapping_extent, theme, session), measure, theme)
	return True
def _standard_slide_at_theme(deck: slide_lib.native_model.Deck, source: slide_lib.native_model.Slide,
		theme: slide_lib.presentation_theme.PresentationTheme, index: int,
		contract: slide_lib.layout_primitives.LayoutContract,
		session: slide_lib.layout_measurement.MeasurementSession) -> slide_lib.layout_model.LayoutSlide:
	"""Build title, named cells, local headings, text, tables, and component images."""
	title = _root_title(source)
	content, title_object = _content_area(source, title, theme, contract, index, session)
	rectangles = slide_lib.layout_measurement.slot_rectangles(contract.name, content)
	slots: list[slide_lib.layout_model.LayoutSlot] = []
	objects: list[slide_lib.layout_model.LayoutObject] = []
	if title_object is not None:
		slots.append(_slot("title", slide_lib.layout_primitives.PlaceholderKind.TITLE,
			slide_lib.layout_primitives.PresentationRole.TITLE, title_object.rectangle, 0,
			title_object.frame_text, slide_lib.layout_primitives.StyleRole.TITLE))
		objects.append(title_object)
	for order, (name, rectangle) in enumerate(zip(contract.slot_names, rectangles), start=len(slots)):
		frame = _frame_text()
		cell = next(cell for cell in source.cells if cell.name == name)
		cell_objects = _cell_objects(deck, cell, rectangle, theme, contract, name, len(objects), frame,
			session, occupy_placeholder=False)
		slots.append(_occupy_primary_slot(name, rectangle, order, cell_objects))
		objects.extend(cell_objects)
	return _slide(source, index, contract, slots, objects)
def _heading_slide(source: slide_lib.native_model.Slide,
		theme: slide_lib.presentation_theme.PresentationTheme, index: int,
		contract: slide_lib.layout_primitives.LayoutContract,
		session: slide_lib.layout_measurement.MeasurementSession) -> slide_lib.layout_model.LayoutSlide:
	"""Build title-only, title-slide, section, and blank slide physical frames."""
	headings = tuple(block for block in source.blocks if isinstance(block, slide_lib.native_model.Heading))
	if contract.name == "section":
		return _section_slide(source, headings, theme, index, contract, session)
	slots: list[slide_lib.layout_model.LayoutSlot] = []
	objects: list[slide_lib.layout_model.LayoutObject] = []
	if headings:
		title = headings[0]
		is_title_slide = contract.name == "title-slide"
		rectangle = _master_rectangle(theme.title_frame, theme) if is_title_slide else \
			slide_lib.layout_primitives.LogicalRectangle(110, 180, 1060, 250)
		frame = dataclasses.replace(_frame_text(),
			vertical_alignment=slide_lib.layout_primitives.VerticalAlignment.MIDDLE) if is_title_slide else _frame_text()
		size = slide_lib.layout_measurement.select_fixed_heading_size((title,), rectangle,
			theme.standard_title_size_pt, theme.title_floor_size_pt, theme, contract.name, "title",
			slide_lib.capacity_report.CapacityCause.TITLE, True, session)
		slots.append(_slot("title", slide_lib.layout_primitives.PlaceholderKind.TITLE,
			slide_lib.layout_primitives.PresentationRole.TITLE, rectangle, 0, frame,
			slide_lib.layout_primitives.StyleRole.TITLE))
		objects.append(_text_object("title", title, rectangle, size,
			theme.title_floor_size_pt, slide_lib.layout_primitives.StyleRole.TITLE, frame, "title", 0,
			slide_lib.layout_primitives.PlaceholderKind.TITLE, theme, bold=True, session=session))
	if len(headings) > 1:
		rectangle = _master_rectangle(theme.outline_frame, theme)
		frame = dataclasses.replace(_frame_text(),
			vertical_alignment=slide_lib.layout_primitives.VerticalAlignment.MIDDLE)
		size = slide_lib.layout_measurement.select_fixed_heading_size(headings[1:], rectangle,
			theme.ordinary_body_size_pt, theme.body_floor_size_pt, theme, contract.name, "subtitle",
			slide_lib.capacity_report.CapacityCause.LOCAL_HEADING, False, session)
		slots.append(_slot("subtitle", slide_lib.layout_primitives.PlaceholderKind.SUBTITLE,
			slide_lib.layout_primitives.PresentationRole.SUBTITLE, rectangle, len(slots), frame,
			slide_lib.layout_primitives.StyleRole.SUBTITLE))
		objects.append(_text_object("subtitle", headings[1:], rectangle, size,
			theme.body_floor_size_pt, slide_lib.layout_primitives.StyleRole.SUBTITLE, frame, "subtitle",
			len(objects), slide_lib.layout_primitives.PlaceholderKind.SUBTITLE, theme, session=session))
	return _slide(source, index, contract, slots, objects)

def _title_only_slide(deck: slide_lib.native_model.Deck, source: slide_lib.native_model.Slide, theme: slide_lib.presentation_theme.PresentationTheme, index: int,
		contract: slide_lib.layout_primitives.LayoutContract,
		session: slide_lib.layout_measurement.MeasurementSession) -> slide_lib.layout_model.LayoutSlide:
	"""Place ordinary root body objects below Title Only's native title member."""
	title = _root_title(source)
	if title is None:
		raise ValueError("title-only requires its validated leading title")
	title_rectangle = slide_lib.layout_primitives.LogicalRectangle(110, 180, 1060, 250)
	frame = _frame_text()
	title_size = slide_lib.layout_measurement.select_fixed_heading_size((title,), title_rectangle,
		theme.standard_title_size_pt, theme.title_floor_size_pt, theme, contract.name, "title", slide_lib.capacity_report.CapacityCause.TITLE, True, session)
	slots = [_slot("title", slide_lib.layout_primitives.PlaceholderKind.TITLE,
		slide_lib.layout_primitives.PresentationRole.TITLE, title_rectangle, 0, frame, slide_lib.layout_primitives.StyleRole.TITLE)]
	objects = [_text_object("title", title, title_rectangle, title_size, theme.title_floor_size_pt,
		slide_lib.layout_primitives.StyleRole.TITLE, frame, "title", 0, slide_lib.layout_primitives.PlaceholderKind.TITLE, theme, bold=True, session=session)]
	body = tuple(block for block in source.blocks if block is not title)
	if body:
		content = slide_lib.layout_primitives.LogicalRectangle(60, 454, 1160, 286)
		cell = slide_lib.native_model.Cell(source.location, body, "body")
		slots.append(_slot("body", slide_lib.layout_primitives.PlaceholderKind.NONE,
			slide_lib.layout_primitives.PresentationRole.CONTENT, content, 1, frame, slide_lib.layout_primitives.StyleRole.BODY))
		objects.extend(_cell_objects(deck, cell, content, theme, contract, "body", len(objects), frame,
			session, occupy_placeholder=False))
	return _slide(source, index, contract, slots, objects)

def _master_rectangle(frame: slide_lib.presentation_theme.FrameGeometry,
		theme: slide_lib.presentation_theme.PresentationTheme) -> slide_lib.layout_primitives.LogicalRectangle:
	"""Convert an authoritative master-frame fact to compiler logical geometry."""
	logical_per_cm = 360000.0 / theme.emu_per_logical_pixel
	return slide_lib.layout_primitives.LogicalRectangle(
		frame.x_cm * logical_per_cm, frame.y_cm * logical_per_cm,
		frame.width_cm * logical_per_cm, frame.height_cm * logical_per_cm)

def _section_slide(source: slide_lib.native_model.Slide,
		headings: tuple[slide_lib.native_model.Heading, ...],
		theme: slide_lib.presentation_theme.PresentationTheme, index: int,
		contract: slide_lib.layout_primitives.LayoutContract,
		session: slide_lib.layout_measurement.MeasurementSession) -> slide_lib.layout_model.LayoutSlide:
	"""Put mixed title/subtitle typography in LibreOffice's one Centered Text member."""
	rectangle = _master_rectangle(theme.outline_frame, theme)
	frame = dataclasses.replace(_frame_text(),
		vertical_alignment=slide_lib.layout_primitives.VerticalAlignment.MIDDLE)
	sizes = slide_lib.layout_measurement.select_centered_heading_sizes(headings[0], headings[1:],
		rectangle, theme, contract.name, session)
	subtitle_size = sizes.subtitle_size_pt if sizes.subtitle_size_pt is not None else \
		theme.ordinary_body_size_pt
	title = _text_content((headings[0],), sizes.title_size_pt,
		theme.title_floor_size_pt, slide_lib.layout_primitives.StyleRole.TITLE,
		FOREGROUND, rectangle.width, theme, bold=True, session=session)
	subtitle = _text_content(headings[1:], subtitle_size,
		theme.body_floor_size_pt, slide_lib.layout_primitives.StyleRole.SUBTITLE,
		FOREGROUND, rectangle.width, theme, session=session)
	paragraphs = tuple(dataclasses.replace(paragraph, properties=dataclasses.replace(
		paragraph.properties,
		horizontal_alignment=slide_lib.layout_primitives.HorizontalAlignment.CENTER))
		for paragraph in title.paragraphs + subtitle.paragraphs)
	content = slide_lib.layout_content.TextContent(paragraphs)
	slot = _slot("title", slide_lib.layout_primitives.PlaceholderKind.OUTLINE,
		slide_lib.layout_primitives.PresentationRole.OUTLINE, rectangle, 0, frame,
		slide_lib.layout_primitives.StyleRole.BODY)
	item = slide_lib.layout_model.LayoutObject("section",
		slide_lib.layout_primitives.PresentationRole.OUTLINE,
		slide_lib.layout_primitives.StyleRole.BODY, rectangle,
		slide_lib.layout_primitives.ObjectLayer.LAYOUT, 0, 0, content, frame,
		"title", "title", slide_lib.layout_primitives.PlaceholderKind.OUTLINE,
		headings[0].location, _reveal_targets("section", headings, 0))
	return _slide(source, index, contract, [slot], [item])

def _content_area(source: slide_lib.native_model.Slide, title: slide_lib.native_model.Heading | None,
		theme: slide_lib.presentation_theme.PresentationTheme, contract: slide_lib.layout_primitives.LayoutContract,
		index: int, session: slide_lib.layout_measurement.MeasurementSession) -> tuple[slide_lib.layout_primitives.LogicalRectangle, slide_lib.layout_model.LayoutObject | None]:
	"""Reserve a title at a bounded point size and return remaining body area."""
	if title is None:
		return slide_lib.layout_primitives.LogicalRectangle(60, 82, 1160, 672), None
	geometry = _title_geometry(title, theme.standard_title_size_pt, theme, contract, session)
	size = theme.standard_title_size_pt
	if geometry is None:
		size = slide_lib.layout_measurement.largest_fitting_size(
			theme.standard_title_size_pt,
			slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT,
			lambda candidate: _title_geometry(title, candidate, theme, contract, session) is not None)
		if size is None:
			raise slide_lib.capacity_report.PhysicalCapacityError(title.location, contract.name,
				"title", theme.title_floor_size_pt,
				slide_lib.capacity_report.CapacityCause.TITLE,
				slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT)
		if size < theme.title_floor_size_pt:
			session.record_capacity(title.location, contract.name, "title", size,
				theme.title_floor_size_pt, slide_lib.capacity_report.CapacityCause.TITLE)
		geometry = _title_geometry(title, size, theme, contract, session)
	if geometry is None:
		raise slide_lib.capacity_report.PhysicalCapacityError(title.location, contract.name,
			"title", theme.title_floor_size_pt, slide_lib.capacity_report.CapacityCause.TITLE,
			slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT)
	rectangle, content = geometry
	frame = _frame_text()
	title_object = _text_object("title", title, rectangle, size,
		theme.title_floor_size_pt, slide_lib.layout_primitives.StyleRole.TITLE, frame, "title", 0,
		slide_lib.layout_primitives.PlaceholderKind.TITLE, theme, bold=True, session=session)
	return content, title_object

def _cell_objects(deck: slide_lib.native_model.Deck, cell: slide_lib.native_model.Cell,
		rectangle: slide_lib.layout_primitives.LogicalRectangle,
		theme: slide_lib.presentation_theme.PresentationTheme, contract: slide_lib.layout_primitives.LayoutContract,
		slot_name: str, order: int, frame: slide_lib.layout_primitives.FrameTextProperties,
		session: slide_lib.layout_measurement.MeasurementSession, occupy_placeholder: bool = True) -> list[slide_lib.layout_model.LayoutObject]:
	"""Build source-ordered content inside one named layout slot."""
	objects: list[slide_lib.layout_model.LayoutObject] = []
	blocks = cell.blocks
	headings = tuple(block for block in blocks if isinstance(block, slide_lib.native_model.Heading))
	if headings:
		heading = headings[0]
		measure = slide_lib.layout_measurement.text_frame_measurement(rectangle)
		size = slide_lib.layout_measurement.largest_fitting_size(
			theme.ordinary_body_size_pt, slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT,
		lambda candidate: slide_lib.layout_measurement.text_frame_fits(
			slide_lib.layout_measurement.paragraph_height(heading.inlines, candidate,
				measure.wrapping_extent, theme, bold=True, session=session) + 10, measure, theme))
		if size is None:
			raise slide_lib.capacity_report.PhysicalCapacityError(heading.location, contract.name,
				slot_name, theme.body_floor_size_pt,
				slide_lib.capacity_report.CapacityCause.LOCAL_HEADING,
				slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT)
		if size < theme.body_floor_size_pt:
			session.record_capacity(heading.location, contract.name, slot_name, size,
				theme.body_floor_size_pt, slide_lib.capacity_report.CapacityCause.LOCAL_HEADING)
		height = slide_lib.layout_measurement.paragraph_height(
			heading.inlines, size, measure.wrapping_extent, theme, bold=True, session=session)
		heading_rect = slide_lib.layout_measurement.heading_rectangle(rectangle, height)
		objects.append(_text_object(f"{slot_name}-heading", heading, heading_rect, size,
			theme.body_floor_size_pt, slide_lib.layout_primitives.StyleRole.LOCAL_HEADING, frame,
			slot_name, order, slide_lib.layout_primitives.PlaceholderKind.NONE, theme, bold=True, session=session))
		rectangle = slide_lib.layout_measurement.remaining_after_heading(rectangle, height)
	content_blocks = tuple(block for block in blocks if not isinstance(block, slide_lib.native_model.Heading))
	images = tuple(block for block in content_blocks if isinstance(block,
		slide_lib.native_model.Image))
	tables = tuple(block for block in content_blocks if isinstance(block, slide_lib.native_model.Table))
	text_blocks = tuple(block for block in content_blocks if isinstance(block,
		(slide_lib.native_model.Paragraph, slide_lib.native_model.ListBlock)))
	if tables and len(content_blocks) == 1:
		objects.append(_table_object(f"{slot_name}-table", tables[0], rectangle, theme, contract.name,
			slot_name, order + len(objects), frame, session=session))
		return objects
	if tables:
		return objects + _ordered_flow(deck, content_blocks, rectangle, theme, contract.name, slot_name,
			order + len(objects), frame, session)
	if images and text_blocks:
		return objects + _mixed_flow(deck, text_blocks, images, rectangle, theme, contract.name, slot_name,
			order + len(objects), frame, session)
	if images:
		width = (rectangle.width - 12 * (len(images) - 1)) / len(images)
		for image_index, image in enumerate(images):
			allocation = slide_lib.layout_primitives.LogicalRectangle(rectangle.x + image_index * (width + 12), rectangle.y, width, rectangle.height)
			objects.append(_picture_object(f"{slot_name}-image-{image_index}", deck, image, allocation, slot_name,
				order + len(objects)))
		return objects
	if text_blocks:
		if occupy_placeholder and len(text_blocks) > 1 and any(slide_lib.editable_text.has_reveal(block)
				for block in text_blocks):
			flow = _ordered_flow(deck, text_blocks, rectangle, theme, contract.name, slot_name,
				order + len(objects), frame, session)
			first = flow[0]
			flow[0] = dataclasses.replace(first,
				layer=slide_lib.layout_primitives.ObjectLayer.LAYOUT,
				presentation_member_id=slot_name,
				placeholder_kind=slide_lib.layout_primitives.PlaceholderKind.OUTLINE)
			return objects + flow
		items = slide_lib.layout_measurement.items_for(text_blocks)
		size = slide_lib.layout_measurement.select_size(items, slide_lib.layout_measurement.text_frame_measurement(rectangle), theme.ordinary_body_size_pt,
			theme.body_floor_size_pt, theme, text_blocks[0].location, contract.name, slot_name, session,
			slide_lib.capacity_report.CapacityCause.PARAGRAPH_LIST)
		objects.append(_text_object(slot_name, _paragraph_block(text_blocks), rectangle, size,
			theme.body_floor_size_pt, slide_lib.layout_primitives.StyleRole.OUTLINE, frame, slot_name,
			order + len(objects), slide_lib.layout_primitives.PlaceholderKind.OUTLINE if occupy_placeholder else
			slide_lib.layout_primitives.PlaceholderKind.NONE, theme, session=session))
	return objects

def _ordered_flow(deck: slide_lib.native_model.Deck, blocks: tuple[slide_lib.native_model.Block, ...],
		rectangle: slide_lib.layout_primitives.LogicalRectangle,
		theme: slide_lib.presentation_theme.PresentationTheme, layout: str, slot: str, order: int,
		frame: slide_lib.layout_primitives.FrameTextProperties,
		session: slide_lib.layout_measurement.MeasurementSession) -> list[slide_lib.layout_model.LayoutObject]:
	"""Plan mixed paragraph/list/table/image source in its authored vertical order."""
	size, heights = _flow_size_and_heights(deck, blocks, rectangle, theme, layout, slot, session)
	objects: list[slide_lib.layout_model.LayoutObject] = []
	y = rectangle.y
	for block, height in zip(blocks, heights):
		allocation = slide_lib.layout_primitives.LogicalRectangle(rectangle.x, y, rectangle.width, height)
		object_id = f"{slot}-{len(objects)}"
		if isinstance(block, (slide_lib.native_model.Paragraph, slide_lib.native_model.ListBlock)):
			objects.append(_text_object(object_id, block, allocation, size, theme.body_floor_size_pt,
				slide_lib.layout_primitives.StyleRole.OUTLINE, frame, slot, order + len(objects),
				slide_lib.layout_primitives.PlaceholderKind.NONE, theme, session=session))
		elif isinstance(block, slide_lib.native_model.Table):
			objects.append(_table_object(object_id, block, allocation, theme, layout, slot, order + len(objects), frame,
				selected_size=size, session=session))
		elif isinstance(block, slide_lib.native_model.Image):
			objects.append(_picture_object(object_id, deck, block, allocation, slot, order + len(objects)))
		else:
			raise ValueError(f"{block.location.path}:{block.location.line}: unsupported ordered flow block")
		y += height + 12
	return objects

def _mixed_flow(deck: slide_lib.native_model.Deck, text_blocks: tuple[slide_lib.native_model.Block, ...],
		images: tuple[slide_lib.native_model.Image, ...], rectangle: slide_lib.layout_primitives.LogicalRectangle,
			theme: slide_lib.presentation_theme.PresentationTheme, layout: str, slot: str, order: int,
			frame: slide_lib.layout_primitives.FrameTextProperties,
			session: slide_lib.layout_measurement.MeasurementSession) -> list[slide_lib.layout_model.LayoutObject]:
	"""Allocate mixed text/image flow in source order at a common body floor-safe size."""
	allocation = _select_mixed_flow_allocation(deck, text_blocks, images, rectangle, theme, layout, slot, session)
	y = rectangle.y
	objects: list[slide_lib.layout_model.LayoutObject] = []
	for item, height in zip(allocation.blocks, allocation.heights):
		item_rect = slide_lib.layout_primitives.LogicalRectangle(rectangle.x, y, rectangle.width, height)
		if isinstance(item, slide_lib.native_model.Image):
			objects.append(_picture_object(f"{slot}-image-{len(objects)}", deck, item, item_rect, slot, order + len(objects)))
		else:
			objects.append(_text_object(f"{slot}-text-{len(objects)}", item, item_rect, allocation.size_pt,
				theme.body_floor_size_pt, slide_lib.layout_primitives.StyleRole.OUTLINE, frame, slot,
				order + len(objects), slide_lib.layout_primitives.PlaceholderKind.NONE, theme, session=session))
		y += height + 12
	return objects

def _select_mixed_flow_allocation(deck: slide_lib.native_model.Deck,
		text_blocks: tuple[slide_lib.native_model.Block, ...], images: tuple[slide_lib.native_model.Image, ...],
		rectangle: slide_lib.layout_primitives.LogicalRectangle,
		theme: slide_lib.presentation_theme.PresentationTheme, layout: str, slot: str,
		session: slide_lib.layout_measurement.MeasurementSession) -> slide_lib.layout_measurement.MixedFlowAllocation:
	"""Select the largest serializer-safe size using the final proportional allocation predicate."""
	minimum = slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT
	def fits(value: float) -> bool:
		"""Use the final allocation as the size-search predicate."""
		return _mixed_flow_allocation_at_size(deck, text_blocks, images, rectangle, value,
			theme, session) is not None
	size = slide_lib.layout_measurement.largest_fitting_size(theme.ordinary_body_size_pt, minimum,
		fits)
	if size is None:
		raise slide_lib.capacity_report.PhysicalCapacityError(text_blocks[0].location, layout, slot,
			theme.body_floor_size_pt, slide_lib.capacity_report.CapacityCause.MIXED_FLOW, minimum)
	allocation = _mixed_flow_allocation_at_size(deck, text_blocks, images, rectangle, size, theme, session)
	if allocation is None:
		raise ValueError("mixed-flow selection lost its exact final allocation")
	if size < theme.body_floor_size_pt:
		session.record_capacity(text_blocks[0].location, layout, slot, size,
			theme.body_floor_size_pt, slide_lib.capacity_report.CapacityCause.MIXED_FLOW)
	return allocation

def _mixed_flow_allocation_at_size(deck: slide_lib.native_model.Deck,
		text_blocks: tuple[slide_lib.native_model.Block, ...], images: tuple[slide_lib.native_model.Image, ...],
		rectangle: slide_lib.layout_primitives.LogicalRectangle, size: float,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession
		) -> slide_lib.layout_measurement.MixedFlowAllocation | None:
	"""Return the exact result consumed by both title preflight and final construction."""
	return slide_lib.layout_measurement.mixed_flow_allocation(deck, text_blocks, images, rectangle,
		size, theme, session)

def _flow_size_and_heights(deck: slide_lib.native_model.Deck,
		blocks: tuple[slide_lib.native_model.Block, ...],
		rectangle: slide_lib.layout_primitives.LogicalRectangle,
		theme: slide_lib.presentation_theme.PresentationTheme,
		layout: str,
		slot: str,
		session: slide_lib.layout_measurement.MeasurementSession) -> tuple[float, list[float]]:
	"""Select one body size only after measuring the whole ordered flow."""
	minimum = slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT
	size = slide_lib.layout_measurement.largest_fitting_size(
		theme.ordinary_body_size_pt, minimum,
		lambda value: _flow_fits_at_size(deck, blocks, rectangle, value, theme, session))
	if size is None:
		raise slide_lib.capacity_report.PhysicalCapacityError(blocks[0].location, layout, slot,
			theme.body_floor_size_pt, slide_lib.capacity_report.CapacityCause.MIXED_FLOW, minimum)
	heights = _flow_heights_at_size(deck, blocks, rectangle, size, theme, session)
	if size < theme.body_floor_size_pt:
		session.record_capacity(blocks[0].location, layout, slot, size,
			theme.body_floor_size_pt, slide_lib.capacity_report.CapacityCause.MIXED_FLOW)
	return size, heights

def _flow_fits_at_size(deck: slide_lib.native_model.Deck,
		blocks: tuple[slide_lib.native_model.Block, ...],
		rectangle: slide_lib.layout_primitives.LogicalRectangle, size: float,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession) -> bool:
	"""Apply the final ordered-flow geometry predicate at one selected type size."""
	heights = _flow_heights_at_size(deck, blocks, rectangle, size, theme, session)
	return slide_lib.layout_measurement.text_frame_fits(
		sum(heights) + 12 * (len(blocks) - 1),
		slide_lib.layout_measurement.text_frame_measurement(rectangle), theme)

def _flow_heights_at_size(deck: slide_lib.native_model.Deck,
		blocks: tuple[slide_lib.native_model.Block, ...],
		rectangle: slide_lib.layout_primitives.LogicalRectangle, size: float,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession) -> list[float]:
	"""Measure every final ordered-flow allocation at one exact type size."""
	heights: list[float] = []
	for block in blocks:
		if isinstance(block, (slide_lib.native_model.Paragraph, slide_lib.native_model.ListBlock)):
			heights.append(slide_lib.layout_measurement.text_height(
				slide_lib.layout_measurement.items_for((block,)), size, rectangle.width, theme, session))
		elif isinstance(block, slide_lib.native_model.Table):
			heights.append(slide_lib.layout_measurement.table_height(block, size, rectangle.width, theme, session))
		elif isinstance(block, slide_lib.native_model.Image):
			width, height = slide_lib.layout_measurement.image_size(deck, block)
			heights.append(min(rectangle.width * height / width, rectangle.height / len(blocks)))
		else:
			raise ValueError(f"{block.location.path}:{block.location.line}: unsupported mixed content")
	return heights

def _gallery(deck: slide_lib.native_model.Deck, source: slide_lib.native_model.Slide,
		theme: slide_lib.presentation_theme.PresentationTheme, index: int,
		contract: slide_lib.layout_primitives.LayoutContract,
		session: slide_lib.layout_measurement.MeasurementSession) -> slide_lib.layout_model.LayoutSlide:
	"""Build contained gallery pictures inside the single gallery allocation."""
	title = _root_title(source)
	content, title_object = _content_area(source, title, theme, contract, index, session)
	gallery = next(cell for cell in source.cells if cell.name == "gallery")
	images = tuple(block for block in gallery.blocks if isinstance(block,
		slide_lib.native_model.Image))
	objects = [] if title_object is None else [title_object]
	pictures: list[slide_lib.layout_model.LayoutObject] = []
	width = (content.width - 18 * (len(images) - 1)) / len(images)
	for image_index, image in enumerate(images):
		allocation = slide_lib.layout_primitives.LogicalRectangle(content.x + image_index * (width + 18), content.y, width, content.height)
		pictures.append(_picture_object(f"gallery-image-{image_index}", deck, image, allocation,
			"gallery", len(objects) + len(pictures)))
	slot = _occupy_primary_slot("gallery", content, 1 if title else 0, pictures)
	objects.extend(pictures)
	slots = ([ _slot("title", slide_lib.layout_primitives.PlaceholderKind.TITLE,
		slide_lib.layout_primitives.PresentationRole.TITLE, title_object.rectangle, 0, title_object.frame_text,
		slide_lib.layout_primitives.StyleRole.TITLE)] if title_object else []) + [slot]
	return _slide(source, index, contract, slots, objects)

def _multiple_choice(deck: slide_lib.native_model.Deck, source: slide_lib.native_model.Slide,
		theme: slide_lib.presentation_theme.PresentationTheme, index: int,
		contract: slide_lib.layout_primitives.LayoutContract,
		session: slide_lib.layout_measurement.MeasurementSession) -> slide_lib.layout_model.LayoutSlide:
	"""Build one visible adaptive question and its on-click answer popup."""
	question = next(cell for cell in source.cells if cell.name == "question")
	answer = next(cell for cell in source.cells if cell.name == "answer")
	question_rect = slide_lib.layout_primitives.LogicalRectangle(60, 36, 1160, 728)
	frame = _frame_text()
	column_gap = 42.0
	answer_frame = dataclasses.replace(frame,
		padding=slide_lib.layout_primitives.Insets(18, 10, 18, 10),
		vertical_alignment=slide_lib.layout_primitives.VerticalAlignment.MIDDLE)
	objects, popup_column, left_width, answer_size, answer_height, answer_y = \
		_multiple_choice_question(deck, question, answer, question_rect,
			theme, frame, session)
	right_width = question_rect.width - column_gap - left_width
	popup_width = left_width if popup_column == 0 else right_width
	answer_rect = slide_lib.layout_primitives.LogicalRectangle(
		question_rect.x if popup_column == 0 else question_rect.x + left_width + column_gap,
		answer_y, popup_width, answer_height)
	slots = [_slot("question", slide_lib.layout_primitives.PlaceholderKind.OUTLINE,
		slide_lib.layout_primitives.PresentationRole.OUTLINE, question_rect, 0, frame,
		slide_lib.layout_primitives.StyleRole.OUTLINE), _slot("answer",
		slide_lib.layout_primitives.PlaceholderKind.OBJECT, slide_lib.layout_primitives.PresentationRole.OBJECT,
		answer_rect, 1, answer_frame, slide_lib.layout_primitives.StyleRole.ACCENT)]
	text = _text_content(answer.blocks, answer_size, theme.body_floor_size_pt,
		slide_lib.layout_primitives.StyleRole.ACCENT, WHITE, popup_width - 36, theme,
		bold=True, session=session)
	accessibility = slide_lib.layout_primitives.ObjectAccessibility("Answer", "Multiple-choice answer popup")
	style = slide_lib.layout_content.ShapeStyle(slide_lib.layout_primitives.StyleRole.ACCENT,
		slide_lib.layout_primitives.StyleRole.ACCENT, 1, slide_lib.layout_primitives.LinePattern.NONE, 12)
	shape = slide_lib.layout_content.ShapeContent(slide_lib.layout_primitives.ShapeKind.ROUNDED_RECTANGLE,
		style, accessibility, text)
	objects.append(slide_lib.layout_model.LayoutObject("answer", slide_lib.layout_primitives.PresentationRole.OBJECT,
		slide_lib.layout_primitives.StyleRole.ACCENT, answer_rect, slide_lib.layout_primitives.ObjectLayer.CONTENT,
		len(objects), len(objects), shape, answer_frame, "answer", "answer",
		slide_lib.layout_primitives.PlaceholderKind.OBJECT, answer.location, _reveal_targets("answer", answer.blocks, len(objects))))
	return _slide(source, index, contract, slots, objects)

def _multiple_choice_question(deck: slide_lib.native_model.Deck,
		question: slide_lib.native_model.Cell,
		answer: slide_lib.native_model.Cell,
		rectangle: slide_lib.layout_primitives.LogicalRectangle,
		theme: slide_lib.presentation_theme.PresentationTheme,
		frame: slide_lib.layout_primitives.FrameTextProperties,
		session: slide_lib.layout_measurement.MeasurementSession
		) -> tuple[list[slide_lib.layout_model.LayoutObject], int, float, float, float, float]:
	"""Keep all final-state question text outside the adaptive answer popup."""
	answer_items = slide_lib.layout_measurement.items_for(answer.blocks)
	content_gap = 12.0
	parts = slide_lib.multiple_choice_layout.question_parts(question)
	image_height = 0.0
	if parts.image is not None:
		# ASVS 5.3.2: image_size retains the existing repository-containment check.
		width, height = slide_lib.layout_measurement.image_size(deck, parts.image)
		image_height = min(rectangle.width * height / width, rectangle.height * .30)
	column_gap = 42.0
	adaptive_result = slide_lib.multiple_choice_layout.select_adaptive_choice_geometry(parts,
		answer_items, answer, rectangle, image_height, content_gap, column_gap, theme, session)
	if adaptive_result.selection is None:
		raise slide_lib.multiple_choice_layout.physical_capacity_error(question, answer,
			adaptive_result.answer_has_serializer_fit, theme)
	selected = adaptive_result.selection
	size, left_height, right_height, split, popup_column, left_width, \
		answer_size, answer_height = (selected.question_size_pt, selected.left_height,
			selected.right_height, selected.split, selected.popup_column, selected.left_width,
			selected.answer_size_pt, selected.answer_height)
	slide_lib.multiple_choice_layout.record_final_capacity(question, answer, size, answer_size,
		theme, session)
	right_width = rectangle.width - column_gap - left_width
	prompt = slide_lib.multiple_choice_layout.prompt_metrics(
		parts, size, rectangle.width, theme, session)
	objects: list[slide_lib.layout_model.LayoutObject] = []
	y = rectangle.y
	if parts.image is not None:
		allocation = slide_lib.layout_primitives.LogicalRectangle(
			rectangle.x, y, rectangle.width, image_height)
		objects.append(_picture_object("question-image", deck, parts.image, allocation,
			"question", len(objects)))
		y += image_height + content_gap
	if parts.context_labels:
		leading_gap = 30.0
		leading_width = (rectangle.width - leading_gap) / 2
		context_gap = 12.0
		context_width = (leading_width - context_gap * (prompt.label_columns - 1)) / \
			prompt.label_columns
		label_y = y
		for start in range(0, len(parts.context_labels), prompt.label_columns):
			row = parts.context_labels[start:start + prompt.label_columns]
			row_heights = prompt.label_item_heights[start:start + len(row)]
			for column, (block, height) in enumerate(zip(row, row_heights)):
				allocation = slide_lib.layout_primitives.LogicalRectangle(
					rectangle.x + column * (context_width + context_gap), label_y,
					context_width, height)
				objects.append(_text_object(f"question-context-{start + column + 1}",
					block, allocation, size, QUIZ_FLOOR_SIZE_PT,
					slide_lib.layout_primitives.StyleRole.OUTLINE, frame, "question",
					len(objects), slide_lib.layout_primitives.PlaceholderKind.NONE,
					theme, session=session))
			label_y += max(row_heights) + context_gap
		if parts.context_prose:
			allocation = slide_lib.layout_primitives.LogicalRectangle(
				rectangle.x, label_y,
				leading_width, prompt.prose_height)
			objects.append(_text_object("question-context-prose", parts.context_prose,
				allocation, size, QUIZ_FLOOR_SIZE_PT,
				slide_lib.layout_primitives.StyleRole.OUTLINE, frame, "question",
				len(objects), slide_lib.layout_primitives.PlaceholderKind.NONE,
				theme, session=session))
		if parts.stem:
			allocation = slide_lib.layout_primitives.LogicalRectangle(
				rectangle.x + leading_width + leading_gap, y,
				leading_width, prompt.stem_height)
			objects.append(_text_object("question-stem", parts.stem, allocation, size,
				QUIZ_FLOOR_SIZE_PT,
				slide_lib.layout_primitives.StyleRole.OUTLINE, frame, "question", len(objects),
				slide_lib.layout_primitives.PlaceholderKind.NONE, theme, session=session))
		y += prompt.height
	elif parts.context_prose:
		allocation = slide_lib.layout_primitives.LogicalRectangle(
			rectangle.x, y, rectangle.width, prompt.prose_height)
		objects.append(_text_object("question-context-prose", parts.context_prose,
			allocation, size,
			QUIZ_FLOOR_SIZE_PT,
			slide_lib.layout_primitives.StyleRole.OUTLINE, frame, "question", len(objects),
			slide_lib.layout_primitives.PlaceholderKind.NONE, theme, session=session))
		y += prompt.leading_height
	if not parts.context_labels and prompt.leading_height and prompt.stem_height:
		y += content_gap
	if not parts.context_labels and parts.stem:
		allocation = slide_lib.layout_primitives.LogicalRectangle(
			rectangle.x, y, rectangle.width, prompt.stem_height)
		objects.append(_text_object("question-stem", parts.stem, allocation, size,
			QUIZ_FLOOR_SIZE_PT,
			slide_lib.layout_primitives.StyleRole.OUTLINE, frame, "question", len(objects),
			slide_lib.layout_primitives.PlaceholderKind.NONE, theme, session=session))
		y += prompt.stem_height
	if prompt.height:
		y += content_gap
	if split == len(parts.choices):
		columns = ((parts.choices, left_height, rectangle.x, left_width),)
	else:
		columns = ((parts.choices[:split], left_height, rectangle.x, left_width),
			(parts.choices[split:], right_height, rectangle.x + left_width + column_gap,
				right_width))
	for column, (blocks, height, x, width) in enumerate(columns):
		allocation = slide_lib.layout_primitives.LogicalRectangle(
			x, y, width, height)
		objects.append(_text_object(f"question-choices-{column + 1}", blocks, allocation,
			size, QUIZ_FLOOR_SIZE_PT,
			slide_lib.layout_primitives.StyleRole.OUTLINE, frame, "question", len(objects),
			slide_lib.layout_primitives.PlaceholderKind.NONE, theme, session=session))
	text_index = next(index for index, item in enumerate(objects)
		if isinstance(item.content, slide_lib.layout_content.TextContent))
	objects[text_index] = dataclasses.replace(objects[text_index],
		layer=slide_lib.layout_primitives.ObjectLayer.LAYOUT,
		presentation_member_id="question",
		placeholder_kind=slide_lib.layout_primitives.PlaceholderKind.OUTLINE)
	answer_y = rectangle.y + rectangle.height - answer_height
	return objects, popup_column, left_width, answer_size, answer_height, answer_y

def _text_object(object_id: str, block: object, rectangle: slide_lib.layout_primitives.LogicalRectangle,
		size: float, floor: float, role: slide_lib.layout_primitives.StyleRole,
		frame: slide_lib.layout_primitives.FrameTextProperties, slot: str, order: int,
		placeholder: slide_lib.layout_primitives.PlaceholderKind,
		theme: slide_lib.presentation_theme.PresentationTheme, bold: bool = False,
		session: slide_lib.layout_measurement.MeasurementSession | None = None) -> slide_lib.layout_model.LayoutObject:
	"""Create one resolved editable text object with stable reveal identity."""
	blocks = (block,) if isinstance(block, (slide_lib.native_model.Heading, slide_lib.native_model.Paragraph,
		slide_lib.native_model.ListBlock)) else tuple(block)
	measure = slide_lib.layout_measurement.text_frame_measurement(rectangle)
	content = _text_content(blocks, size, floor, role, FOREGROUND,
		measure.wrapping_extent, theme, bold, session)
	if frame.vertical_alignment is slide_lib.layout_primitives.VerticalAlignment.MIDDLE:
		content = dataclasses.replace(content, paragraphs=tuple(dataclasses.replace(paragraph, properties=
			dataclasses.replace(paragraph.properties, horizontal_alignment=slide_lib.layout_primitives.HorizontalAlignment.CENTER)) for paragraph in content.paragraphs))
	presentation = slot if placeholder is not slide_lib.layout_primitives.PlaceholderKind.NONE else None
	role_value = slide_lib.layout_primitives.PresentationRole.TITLE if placeholder is slide_lib.layout_primitives.PlaceholderKind.TITLE else (
		slide_lib.layout_primitives.PresentationRole.SUBTITLE if placeholder is slide_lib.layout_primitives.PlaceholderKind.SUBTITLE else slide_lib.layout_primitives.PresentationRole.OUTLINE)
	location = block.location if hasattr(block, "location") else (
		block[0].location if block else None)
	return slide_lib.layout_model.LayoutObject(object_id, role_value, role, rectangle,
		slide_lib.layout_primitives.ObjectLayer.LAYOUT if presentation else slide_lib.layout_primitives.ObjectLayer.CONTENT,
		order, order, content, frame, slot, presentation, placeholder, location,
		_reveal_targets(object_id, blocks, order))

def _text_content(blocks: tuple[slide_lib.native_model.Block, ...], size: float, floor: float,
		role: slide_lib.layout_primitives.StyleRole, color: str, width: float,
		theme: slide_lib.presentation_theme.PresentationTheme,
		bold: bool = False, session: slide_lib.layout_measurement.MeasurementSession | None = None) -> slide_lib.layout_content.TextContent:
	"""Project supported inline/list semantics into fully resolved text runs."""
	typography = slide_lib.layout_primitives.Typography(role, "OpenDyslexic", size, size, min(floor, size))
	entries: list[tuple[tuple[slide_lib.native_model.Inline, ...], bool,
		slide_lib.layout_content.ListMetadata | None]] = []
	for block in blocks:
		if isinstance(block, (slide_lib.native_model.Heading, slide_lib.native_model.Paragraph)):
			entries.append((block.inlines, False, None))
		elif isinstance(block, slide_lib.native_model.ListBlock):
			for item in slide_lib.editable_text.project_list(block):
				metadata = slide_lib.layout_content.ListMetadata(
					slide_lib.layout_primitives.ListKind.ORDERED if item.ordered else slide_lib.layout_primitives.ListKind.UNORDERED,
					item.level, item.start)
				entries.append((item.inlines, True, metadata))
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
	result = slide_lib.layout_content.TextContent(tuple(paragraphs))
	return result

def resolved_runs(inlines: tuple[slide_lib.native_model.Inline, ...], color: str, bold: bool = False,
		italic: bool = False, link: str | None = None) -> tuple[slide_lib.layout_content.InlineContent, ...]:
	"""Resolve recursive strong/emphasis/link styling before adapters receive runs."""
	runs: list[slide_lib.layout_content.InlineContent] = []
	for inline in inlines:
		if isinstance(inline, slide_lib.native_model.Text):
			style = slide_lib.layout_content.RunStyle("OpenDyslexic", color, bold=bold, italic=italic, link_url=link)
			runs.append(slide_lib.layout_content.TextRun(inline.value, style))
		elif isinstance(inline, slide_lib.native_model.InlineCode):
			style = slide_lib.layout_content.RunStyle("OpenDyslexic", color, bold=bold, italic=italic, code=True, link_url=link)
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
					style = slide_lib.layout_content.RunStyle("PT Sans Narrow" if literal else run.style.font_family,
						run.style.foreground, True, run.style.bold, run.style.italic, run.style.code,
						run.style.link_url, literal)
					runs.append(slide_lib.layout_content.TextRun(run.text, style))
				else:
					runs.append(run)
	return tuple(runs)

def _fragment_runs(inlines: tuple[slide_lib.layout_content.InlineContent, ...], size: float,
		width: float, theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession | None = None) -> tuple[slide_lib.layout_content.InlineContent, ...]:
	"""Emit exact-width, grapheme-safe break markers retained by both adapters."""
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
				if result and isinstance(result[-1], slide_lib.layout_content.TextRun) and result[-1].style == style:
					result[-1] = dataclasses.replace(result[-1], text=result[-1].text + fragment)
				else:
					result.append(slide_lib.layout_content.TextRun(fragment, style))
	return tuple(result)

def _table_object(object_id: str, table: slide_lib.native_model.Table,
		rectangle: slide_lib.layout_primitives.LogicalRectangle,
		theme: slide_lib.presentation_theme.PresentationTheme, layout: str, slot: str, order: int,
		frame: slide_lib.layout_primitives.FrameTextProperties,
		selected_size: float | None = None,
		session: slide_lib.layout_measurement.MeasurementSession | None = None) -> slide_lib.layout_model.LayoutObject:
	"""Project a rectangular semantic table with resolved 28-to-24 point fitting."""
	rows = ((table.headers, True),) if table.headers else ()
	rows += tuple((row, False) for row in table.rows)
	columns = len(rows[0][0])
	size = selected_size if selected_size is not None else slide_lib.layout_measurement.select_table_size(table, rectangle,
		theme.ordinary_body_size_pt, theme.body_floor_size_pt, theme, layout, slot, session)
	typography = slide_lib.layout_primitives.Typography(slide_lib.layout_primitives.StyleRole.TABLE_BODY,
		"OpenDyslexic", size, size, min(theme.body_floor_size_pt, size))
	def row_content(cells: tuple[tuple[slide_lib.native_model.Inline, ...], ...], header: bool) -> slide_lib.layout_content.TableRow:
		result = slide_lib.layout_content.TableRow(tuple(slide_lib.layout_content.TableCell(
			(slide_lib.layout_content.TextParagraph(_fragment_runs(resolved_runs(cell, WHITE if header else FOREGROUND, header),
				size, rectangle.width / columns - 12, theme, session), typography,
				slide_lib.layout_measurement.paragraph_properties(cell, size, rectangle.width / columns - 12,
				theme, terminal=True, session=session)),),
			slide_lib.layout_primitives.Insets(slide_lib.layout_measurement.TABLE_HORIZONTAL_PADDING,
				slide_lib.layout_measurement.TABLE_VERTICAL_PADDING,
				slide_lib.layout_measurement.TABLE_HORIZONTAL_PADDING,
				slide_lib.layout_measurement.TABLE_VERTICAL_PADDING), slide_lib.layout_primitives.VerticalAlignment.MIDDLE) for cell in cells))
		return result
	headers = (row_content(table.headers, True),) if table.headers else ()
	body = tuple(row_content(row, False) for row in table.rows)
	content = slide_lib.layout_content.TableContent(headers, body, tuple(rectangle.width / columns for _ in range(columns)),
		tuple(rectangle.height / len(rows) for _ in rows), slide_lib.layout_content.TableStyle(
			slide_lib.layout_primitives.StyleRole.TABLE_HEADER, slide_lib.layout_primitives.StyleRole.TABLE_BODY,
			slide_lib.layout_primitives.StyleRole.ACCENT, 1, slide_lib.layout_primitives.LinePattern.SOLID))
	return slide_lib.layout_model.LayoutObject(object_id, slide_lib.layout_primitives.PresentationRole.OUTLINE,
		slide_lib.layout_primitives.StyleRole.BODY, rectangle, slide_lib.layout_primitives.ObjectLayer.CONTENT,
		order, order, content, frame, slot, None, slide_lib.layout_primitives.PlaceholderKind.NONE, table.location)

def _picture_object(object_id: str, deck: slide_lib.native_model.Deck,
		image: slide_lib.native_model.Image,
		allocation: slide_lib.layout_primitives.LogicalRectangle, slot: str,
		order: int) -> slide_lib.layout_model.LayoutObject:
	"""Resolve contained display geometry and accessibility before adapter projection."""
	width, height = slide_lib.layout_measurement.image_size(deck, image)
	# Stay one representable step within the allocation after proportional rounding.
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
		_reveal_targets(object_id, (image,), order))

def _slot(name: str, kind: slide_lib.layout_primitives.PlaceholderKind,
		role: slide_lib.layout_primitives.PresentationRole, rectangle: slide_lib.layout_primitives.LogicalRectangle,
		order: int, frame: slide_lib.layout_primitives.FrameTextProperties | None,
		style: slide_lib.layout_primitives.StyleRole) -> slide_lib.layout_model.LayoutSlot:
	"""Construct one native-presentation slot and matching topology member."""
	result = slide_lib.layout_model.LayoutSlot(name, kind, role, rectangle, order,
		slide_lib.layout_primitives.PlaceholderProperties(style, frame))
	return result

def _occupy_primary_slot(name: str, rectangle: slide_lib.layout_primitives.LogicalRectangle,
		order: int, objects: list[slide_lib.layout_model.LayoutObject]) -> slide_lib.layout_model.LayoutSlot:
	"""Bind one primary object to the LibreOffice presentation-layout member."""
	index = next((index for index, item in enumerate(objects)
		if item.style_role is not slide_lib.layout_primitives.StyleRole.LOCAL_HEADING), 0)
	item = objects[index]
	text = isinstance(item.content, slide_lib.layout_content.TextContent)
	kind = slide_lib.layout_primitives.PlaceholderKind.OUTLINE if text else slide_lib.layout_primitives.PlaceholderKind.OBJECT
	role = slide_lib.layout_primitives.PresentationRole.OUTLINE if text else (
		slide_lib.layout_primitives.PresentationRole.GRAPHIC if isinstance(item.content,
			slide_lib.layout_content.PictureContent) else slide_lib.layout_primitives.PresentationRole.OBJECT)
	objects[index] = dataclasses.replace(item, role=role, layer=slide_lib.layout_primitives.ObjectLayer.LAYOUT,
		presentation_member_id=name, placeholder_kind=kind)
	result = _slot(name, kind, role, rectangle, order, item.frame_text, item.style_role)
	return result

def _frame_text() -> slide_lib.layout_primitives.FrameTextProperties:
	"""Give every text frame explicit horizontal shrink-only behavior."""
	return slide_lib.layout_primitives.FrameTextProperties(slide_lib.layout_primitives.Insets(0, 0, 0, 0),
		slide_lib.layout_primitives.VerticalAlignment.TOP, slide_lib.layout_primitives.TextWrap.WRAP,
		slide_lib.layout_primitives.OverflowPolicy.SHRINK)

def _root_title(source: slide_lib.native_model.Slide) -> slide_lib.native_model.Heading | None:
	"""Return the canonical H1 title if present."""
	result = next((block for block in source.blocks if isinstance(block, slide_lib.native_model.Heading) and block.level == 1), None)
	return result

def _paragraph_block(blocks: tuple[slide_lib.native_model.Block, ...]) -> tuple[slide_lib.native_model.Block, ...]:
	"""Keep source body/list sequence intact for one text frame."""
	return blocks

def _reveal_targets(object_id: str, blocks: tuple[object, ...], order: int) -> tuple[slide_lib.layout_model.RevealTarget, ...]:
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

def _slide(source: slide_lib.native_model.Slide, index: int, contract: slide_lib.layout_primitives.LayoutContract,
		slots: list[slide_lib.layout_model.LayoutSlot], objects: list[slide_lib.layout_model.LayoutObject]) -> slide_lib.layout_model.LayoutSlide:
	"""Finalize one slide with occupied topology and independent AutoLayout hints."""
	topology = slide_lib.layout_primitives.PlaceholderTopology(contract.name,
		tuple(slot.topology_member() for slot in slots), _libreoffice_layout(contract, slots))
	identity = slide_lib.layout_model.SlideIdentity(f"slide-{index + 1}", index, source.location)
	notes = tuple(slide_lib.layout_model.SpeakerNote(f"slide-{index + 1}-note-{note_index}", text)
		for note_index, text in enumerate(source.notes))
	result = slide_lib.layout_model.LayoutSlide(identity, slide_lib.layout_model.LayoutIdentity(contract.name, topology),
		tuple(slots), tuple(_renumber_reveals(objects)), notes)
	return result

def _libreoffice_layout(contract: slide_lib.layout_primitives.LayoutContract,
		slots: list[slide_lib.layout_model.LayoutSlot]
		) -> slide_lib.layout_primitives.LibreOfficeLayoutSignature | None:
	"""Resolve importer classifier tokens without changing occupied frame semantics."""
	if contract.libreoffice_autolayout is None:
		return None
	rectangles = {slot.slot_id: slot.rectangle for slot in slots}
	placeholders: list[slide_lib.layout_primitives.LibreOfficeLayoutPlaceholder] = []
	for object_name, member_id in contract.libreoffice_placeholder_members:
		if member_id in rectangles:
			rectangle = rectangles[member_id]
		else:
			rectangle = _unoccupied_classifier_rectangle(contract, member_id)
		placeholders.append(slide_lib.layout_primitives.LibreOfficeLayoutPlaceholder(
			object_name, rectangle))
	result = slide_lib.layout_primitives.LibreOfficeLayoutSignature(
		contract.libreoffice_autolayout, tuple(placeholders))
	return result

def _unoccupied_classifier_rectangle(contract: slide_lib.layout_primitives.LayoutContract,
		member_id: str) -> slide_lib.layout_primitives.LogicalRectangle:
	"""Give an optional absent title/subtitle a stable page-layout-only rectangle."""
	if member_id == "title" and contract.allows_title:
		return slide_lib.layout_primitives.LogicalRectangle(60, 52, 1160, 80)
	if member_id == "subtitle" and contract.allows_subtitle:
		return slide_lib.layout_primitives.LogicalRectangle(110, 445, 1060, 125)
	raise ValueError(f"LibreOffice classifier member has no physical or optional slot: {member_id}")

def _renumber_reveals(objects: list[slide_lib.layout_model.LayoutObject]) -> list[slide_lib.layout_model.LayoutObject]:
	"""Make slide-wide reveal activation order contiguous after source-order construction."""
	result: list[slide_lib.layout_model.LayoutObject] = []
	activation = 0
	for item in objects:
		targets: list[slide_lib.layout_model.RevealTarget] = []
		for target in item.reveal_targets:
			targets.append(slide_lib.layout_model.RevealTarget(target.target_id, target.object_id,
				target.reveal, activation, target.paragraph_indexes))
			activation += 1
		result.append(slide_lib.layout_model.LayoutObject(item.object_id, item.role, item.style_role,
			item.rectangle, item.layer, item.z_index, item.reading_order, item.content, item.frame_text,
			item.slot_id, item.presentation_member_id, item.placeholder_kind, item.source, tuple(targets),
			item.origin))
	return result
