"""Build immutable physical objects from resolved layout contracts and measurements."""

import dataclasses
import re
from collections.abc import Callable

import slide_lib.layout_measurement
import slide_lib.layout_registry
import slide_lib.editable_text
import slide_lib.layout_content
import slide_lib.layout_model
import slide_lib.layout_primitives
import slide_lib.native_model
import slide_lib.presentation_theme


FOREGROUND = "172033"
ACCENT = "24578F"
MUTED = "526176"
WHITE = "FFFFFF"


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
	if not contract.slot_names:
		return _heading_slide(source, theme, index, contract, session)
	return _standard_slide(deck, source, theme, index, contract, session)


def compile_grid_stream_page(deck: slide_lib.native_model.Deck, source: slide_lib.native_model.Slide,
		units: tuple[slide_lib.layout_measurement.GridStreamUnit, ...],
		theme: slide_lib.presentation_theme.PresentationTheme, index: int,
		session: slide_lib.layout_measurement.MeasurementSession | None = None) -> slide_lib.layout_model.LayoutSlide:
	"""Project a source-ordered grid stream without merging provenance groups."""
	session = session or slide_lib.layout_measurement.MeasurementSession(theme)
	return _with_fitting_title(source, theme, session, lambda candidate_theme:
		_compile_grid_stream_page_at_theme(deck, source, units, candidate_theme, index, session))


def _compile_grid_stream_page_at_theme(deck: slide_lib.native_model.Deck,
		source: slide_lib.native_model.Slide,
		units: tuple[slide_lib.layout_measurement.GridStreamUnit, ...],
		theme: slide_lib.presentation_theme.PresentationTheme,
		index: int, session: slide_lib.layout_measurement.MeasurementSession | None = None) -> slide_lib.layout_model.LayoutSlide:
	"""Build one grid-stream page at an already selected title size."""
	contract = slide_lib.layout_registry.contract_for("one-panel")
	title = _root_title(source)
	session = session or slide_lib.layout_measurement.MeasurementSession(theme)
	content, title_object = _content_area(source, title, theme, contract, index, session)
	frame = _frame_text(contract, "body")
	slots: list[slide_lib.layout_model.LayoutSlot] = []
	objects: list[slide_lib.layout_model.LayoutObject] = []
	if title_object is not None:
		slots.append(_slot("title", slide_lib.layout_primitives.PlaceholderKind.TITLE,
			slide_lib.layout_primitives.PresentationRole.TITLE, title_object.rectangle, 0,
			title_object.frame_text, slide_lib.layout_primitives.StyleRole.TITLE))
		objects.append(title_object)
	y = content.y
	for unit_index, stream_unit in enumerate(units):
		cell = _grid_stream_cell(stream_unit)
		height = _grid_stream_cell_height(deck, cell, content.width, content.height - (y - content.y), theme, session)
		allocation = slide_lib.layout_primitives.LogicalRectangle(content.x, y, content.width, height)
		cell_objects = _cell_objects(deck, cell, allocation, theme, contract, "body", len(objects), frame, session,
			occupy_placeholder=False)
		for object_index, item in enumerate(cell_objects):
			object_id = f"body-unit-{unit_index}-{object_index}"
			targets = tuple(dataclasses.replace(target,
				target_id=object_id + target.target_id[len(item.object_id):], object_id=object_id)
				for target in item.reveal_targets)
			objects.append(dataclasses.replace(item, object_id=object_id, reveal_targets=targets,
				decomposition_origin=stream_unit.origin))
		y += height + 12
	if y - content.y - 12 > content.height:
		location = units[0].unit.block.location
		raise ValueError(f"{location.path}:{location.line}: grid stream cannot fit within the supported readable minimum of {theme.body_floor_size_pt:g} pt")
	slots.append(_occupy_primary_slot("body", content, len(slots), objects))
	return _slide(source, index, contract, slots, objects)


def _grid_stream_cell(stream_unit: slide_lib.layout_measurement.GridStreamUnit) -> slide_lib.native_model.Cell:
	"""Materialize one stream unit with its cell-local heading, if one is active."""
	blocks: list[slide_lib.native_model.Block] = []
	if stream_unit.unit.active_heading is not None:
		blocks.append(dataclasses.replace(stream_unit.unit.active_heading, reveal=None))
	blocks.append(stream_unit.unit.block)
	result = slide_lib.native_model.Cell(stream_unit.origin.source, tuple(blocks),
		stream_unit.origin.original_slot)
	return result


def _grid_stream_cell_height(deck: slide_lib.native_model.Deck, cell: slide_lib.native_model.Cell,
		width: float, available: float, theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession) -> float:
	"""Measure one source slot atomically at the shared readable type floor."""
	blocks = tuple(block for block in cell.blocks if not isinstance(block, slide_lib.native_model.Heading))
	heading = next((block for block in cell.blocks if isinstance(block, slide_lib.native_model.Heading)), None)
	heading_height = 0.0 if heading is None else slide_lib.layout_measurement.paragraph_height(
		heading.inlines, theme.ordinary_body_size_pt, width, theme, bold=True, session=session) + 10
	if not blocks:
		return heading_height
	if len(blocks) == 1 and isinstance(blocks[0], slide_lib.native_model.Image):
		# A source image is atomic, but containment can use the remaining
		# one-panel frame; natural aspect ratio must not reject decomposition.
		return available
	rectangle = slide_lib.layout_primitives.LogicalRectangle(0, 0, width, available - heading_height)
	if len(blocks) == 1 and isinstance(blocks[0], slide_lib.native_model.Table):
		size = slide_lib.layout_measurement.select_table_size(blocks[0], rectangle,
			theme.ordinary_body_size_pt, theme.body_floor_size_pt, theme, session)
		return heading_height + slide_lib.layout_measurement.table_height(blocks[0], size, width, theme, session)
	if all(isinstance(block, (slide_lib.native_model.Paragraph, slide_lib.native_model.ListBlock)) for block in blocks):
		items = slide_lib.layout_measurement.items_for(blocks)
		size = slide_lib.layout_measurement.select_size(items, rectangle, theme.ordinary_body_size_pt,
			theme.body_floor_size_pt, theme, blocks[0].location, "grid stream content", session)
		return heading_height + slide_lib.layout_measurement.text_height(items, size, width, theme, session)
	_size, heights = _flow_size_and_heights(deck, blocks, rectangle, theme, session)
	if not heights:
		raise ValueError(f"{blocks[0].location.path}:{blocks[0].location.line}: grid stream content cannot fit within the supported readable minimum of {theme.body_floor_size_pt:g} pt")
	return heading_height + sum(heights) + 12 * (len(heights) - 1)


def _standard_slide(deck: slide_lib.native_model.Deck, source: slide_lib.native_model.Slide,
		theme: slide_lib.presentation_theme.PresentationTheme, index: int,
		contract: slide_lib.layout_primitives.LayoutContract,
		session: slide_lib.layout_measurement.MeasurementSession) -> slide_lib.layout_model.LayoutSlide:
	"""Use the largest title that leaves every body allocation above its floor."""
	return _with_fitting_title(source, theme, session, lambda candidate_theme:
		_standard_slide_at_theme(deck, source, candidate_theme, index, contract, session))


def _with_fitting_title(source: slide_lib.native_model.Slide,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession,
		build: Callable[[slide_lib.presentation_theme.PresentationTheme],
		slide_lib.layout_model.LayoutSlide]) -> slide_lib.layout_model.LayoutSlide:
	"""Build at the largest quarter-point title size compatible with body capacity."""
	if _root_title(source) is None:
		return build(theme)
	last_error: ValueError | None = None
	for quarters in range(int(theme.standard_title_size_pt * 4), int(theme.title_floor_size_pt * 4) - 1, -1):
		candidate_theme = dataclasses.replace(theme, standard_title_size_pt=quarters / 4)
		try:
			return build(candidate_theme)
		except ValueError as error:
			last_error = error
	if last_error is None:
		raise ValueError("title fitting exhausted without a capacity diagnostic")
	raise last_error


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
		frame = _frame_text(contract, name)
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
	"""Build title-only, title-slide, centered-text, and blank slide physical frames."""
	headings = tuple(block for block in source.blocks if isinstance(block, slide_lib.native_model.Heading))
	if contract.name == "centered-text":
		return _centered_text_slide(source, headings, theme, index, contract, session)
	slots: list[slide_lib.layout_model.LayoutSlot] = []
	objects: list[slide_lib.layout_model.LayoutObject] = []
	if headings:
		title = headings[0]
		rectangle = slide_lib.layout_primitives.LogicalRectangle(110, 180, 1060, 250)
		frame = _frame_text(contract, "title")
		slots.append(_slot("title", slide_lib.layout_primitives.PlaceholderKind.TITLE,
			slide_lib.layout_primitives.PresentationRole.TITLE, rectangle, 0, frame,
			slide_lib.layout_primitives.StyleRole.TITLE))
		objects.append(_text_object("title", title, rectangle, theme.standard_title_size_pt,
			theme.title_floor_size_pt, slide_lib.layout_primitives.StyleRole.TITLE, frame, "title", 0,
			slide_lib.layout_primitives.PlaceholderKind.TITLE, theme, bold=True, session=session))
	if len(headings) > 1:
		rectangle = slide_lib.layout_primitives.LogicalRectangle(110, 445, 1060, 125)
		frame = _frame_text(contract, "subtitle")
		slots.append(_slot("subtitle", slide_lib.layout_primitives.PlaceholderKind.SUBTITLE,
			slide_lib.layout_primitives.PresentationRole.SUBTITLE, rectangle, len(slots), frame,
			slide_lib.layout_primitives.StyleRole.SUBTITLE))
		objects.append(_text_object("subtitle", headings[1:], rectangle, theme.ordinary_body_size_pt,
			theme.body_floor_size_pt, slide_lib.layout_primitives.StyleRole.SUBTITLE, frame, "subtitle",
			len(objects), slide_lib.layout_primitives.PlaceholderKind.SUBTITLE, theme, session=session))
	return _slide(source, index, contract, slots, objects)


def _centered_text_slide(source: slide_lib.native_model.Slide,
		headings: tuple[slide_lib.native_model.Heading, ...],
		theme: slide_lib.presentation_theme.PresentationTheme, index: int,
		contract: slide_lib.layout_primitives.LayoutContract,
		session: slide_lib.layout_measurement.MeasurementSession) -> slide_lib.layout_model.LayoutSlide:
	"""Put mixed title/subtitle typography in LibreOffice's one centered-text member."""
	rectangle = slide_lib.layout_primitives.LogicalRectangle(110, 180, 1060, 390)
	frame = dataclasses.replace(_frame_text(contract, "title"),
		vertical_alignment=slide_lib.layout_primitives.VerticalAlignment.MIDDLE)
	title = _text_content((headings[0],), theme.standard_title_size_pt,
		theme.title_floor_size_pt, slide_lib.layout_primitives.StyleRole.TITLE,
		FOREGROUND, rectangle.width, theme, bold=True, session=session)
	subtitle = _text_content(headings[1:], theme.ordinary_body_size_pt,
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
	item = slide_lib.layout_model.LayoutObject("centered-text",
		slide_lib.layout_primitives.PresentationRole.OUTLINE,
		slide_lib.layout_primitives.StyleRole.BODY, rectangle,
		slide_lib.layout_primitives.ObjectLayer.LAYOUT, 0, 0, content, frame,
		"title", "title", slide_lib.layout_primitives.PlaceholderKind.OUTLINE,
		headings[0].location, _reveal_targets("centered-text", headings, 0))
	return _slide(source, index, contract, [slot], [item])


def _content_area(source: slide_lib.native_model.Slide, title: slide_lib.native_model.Heading | None,
		theme: slide_lib.presentation_theme.PresentationTheme, contract: slide_lib.layout_primitives.LayoutContract,
		index: int, session: slide_lib.layout_measurement.MeasurementSession) -> tuple[slide_lib.layout_primitives.LogicalRectangle, slide_lib.layout_model.LayoutObject | None]:
	"""Reserve a title at a bounded point size and return remaining body area."""
	if title is None:
		return slide_lib.layout_primitives.LogicalRectangle(60, 82, 1160, 672), None
	if contract.vertical_title:
		rectangle = slide_lib.layout_primitives.LogicalRectangle(1126, 60, 94, 666)
		frame = _frame_text(contract, "title", vertical=True)
		title_object = _text_object("title", title, rectangle, theme.standard_title_size_pt,
			theme.title_floor_size_pt, slide_lib.layout_primitives.StyleRole.TITLE, frame, "title", 0,
			slide_lib.layout_primitives.PlaceholderKind.TITLE, theme, bold=True, session=session)
		return slide_lib.layout_primitives.LogicalRectangle(60, 82, 1042, 672), title_object
	size = theme.standard_title_size_pt
	height = slide_lib.layout_measurement.paragraph_height(
		title.inlines, size, 1160, theme, bold=True, session=session)
	if height + 24 < 672:
		rectangle = slide_lib.layout_primitives.LogicalRectangle(60, 52, 1160, height)
		frame = _frame_text(contract, "title")
		title_object = _text_object("title", title, rectangle, size, theme.title_floor_size_pt,
			slide_lib.layout_primitives.StyleRole.TITLE, frame, "title", 0,
			slide_lib.layout_primitives.PlaceholderKind.TITLE, theme, bold=True, session=session)
		return slide_lib.layout_primitives.LogicalRectangle(60, 52 + height + 24, 1160,
			754 - (52 + height + 24)), title_object
	raise ValueError(f"{title.location.path}:{title.location.line}: {contract.name} H1 cannot fit within the supported readable minimum of {theme.title_floor_size_pt:g} pt")


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
		size = theme.ordinary_body_size_pt
		height = slide_lib.layout_measurement.paragraph_height(
			heading.inlines, size, rectangle.width, theme, bold=True, session=session)
		heading_rect = slide_lib.layout_primitives.LogicalRectangle(rectangle.x, rectangle.y, rectangle.width, height)
		objects.append(_text_object(f"{slot_name}-heading", heading, heading_rect, size,
			theme.body_floor_size_pt, slide_lib.layout_primitives.StyleRole.LOCAL_HEADING, frame,
			slot_name, order, slide_lib.layout_primitives.PlaceholderKind.NONE, theme, bold=True, session=session))
		rectangle = slide_lib.layout_primitives.LogicalRectangle(rectangle.x, rectangle.y + height + 10,
			rectangle.width, rectangle.height - height - 10)
	content_blocks = tuple(block for block in blocks if not isinstance(block, slide_lib.native_model.Heading))
	images = tuple(block for block in content_blocks if isinstance(block, slide_lib.native_model.Image))
	tables = tuple(block for block in content_blocks if isinstance(block, slide_lib.native_model.Table))
	text_blocks = tuple(block for block in content_blocks if isinstance(block,
		(slide_lib.native_model.Paragraph, slide_lib.native_model.ListBlock)))
	if tables and len(content_blocks) == 1:
		objects.append(_table_object(f"{slot_name}-table", tables[0], rectangle, theme, slot_name, order + len(objects), frame, session=session))
		return objects
	if tables:
		return objects + _ordered_flow(deck, content_blocks, rectangle, theme, slot_name,
			order + len(objects), frame, session)
	if images and text_blocks:
		return objects + _mixed_flow(deck, text_blocks, images, rectangle, theme, slot_name, order + len(objects), frame, session)
	if images:
		width = (rectangle.width - 12 * (len(images) - 1)) / len(images)
		for image_index, image in enumerate(images):
			allocation = slide_lib.layout_primitives.LogicalRectangle(rectangle.x + image_index * (width + 12), rectangle.y, width, rectangle.height)
			objects.append(_picture_object(f"{slot_name}-image-{image_index}", deck, image, allocation, slot_name,
				order + len(objects)))
		return objects
	if text_blocks:
		if len(text_blocks) > 1 and any(slide_lib.editable_text.has_reveal(block)
				for block in text_blocks):
			flow = _ordered_flow(deck, text_blocks, rectangle, theme, slot_name,
				order + len(objects), frame, session)
			first = flow[0]
			flow[0] = dataclasses.replace(first,
				layer=slide_lib.layout_primitives.ObjectLayer.LAYOUT,
				presentation_member_id=slot_name,
				placeholder_kind=slide_lib.layout_primitives.PlaceholderKind.OUTLINE)
			return objects + flow
		items = slide_lib.layout_measurement.items_for(text_blocks)
		size = slide_lib.layout_measurement.select_size(items, rectangle, theme.ordinary_body_size_pt,
			theme.body_floor_size_pt, theme, text_blocks[0].location, f"{contract.name} {slot_name} content", session)
		objects.append(_text_object(slot_name, _paragraph_block(text_blocks), rectangle, size,
			theme.body_floor_size_pt, slide_lib.layout_primitives.StyleRole.OUTLINE, frame, slot_name,
			order + len(objects), slide_lib.layout_primitives.PlaceholderKind.OUTLINE if occupy_placeholder else
			slide_lib.layout_primitives.PlaceholderKind.NONE, theme, session=session))
	return objects


def _ordered_flow(deck: slide_lib.native_model.Deck, blocks: tuple[slide_lib.native_model.Block, ...],
		rectangle: slide_lib.layout_primitives.LogicalRectangle,
		theme: slide_lib.presentation_theme.PresentationTheme, slot: str, order: int,
		frame: slide_lib.layout_primitives.FrameTextProperties,
		session: slide_lib.layout_measurement.MeasurementSession) -> list[slide_lib.layout_model.LayoutObject]:
	"""Plan mixed paragraph/list/table/image source in its authored vertical order."""
	size, heights = _flow_size_and_heights(deck, blocks, rectangle, theme, session)
	if not heights:
		raise ValueError(f"{blocks[0].location.path}:{blocks[0].location.line}: {slot} mixed content cannot fit within the supported readable minimum of {theme.body_floor_size_pt:g} pt")
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
			objects.append(_table_object(object_id, block, allocation, theme, slot, order + len(objects), frame,
				selected_size=size, session=session))
		elif isinstance(block, slide_lib.native_model.Image):
			objects.append(_picture_object(object_id, deck, block, allocation, slot, order + len(objects)))
		else:
			raise ValueError(f"{block.location.path}:{block.location.line}: unsupported ordered flow block")
		y += height + 12
	return objects


def _mixed_flow(deck: slide_lib.native_model.Deck, text_blocks: tuple[slide_lib.native_model.Block, ...],
		images: tuple[slide_lib.native_model.Image, ...], rectangle: slide_lib.layout_primitives.LogicalRectangle,
		theme: slide_lib.presentation_theme.PresentationTheme, slot: str, order: int,
		frame: slide_lib.layout_primitives.FrameTextProperties,
		session: slide_lib.layout_measurement.MeasurementSession) -> list[slide_lib.layout_model.LayoutObject]:
	"""Allocate mixed text/image flow in source order at a common body floor-safe size."""
	sequence = tuple(block for block in text_blocks + images)
	sequence = tuple(block for block in sorted(sequence, key=lambda item: item.location.line))
	size, all_heights = _flow_size_and_heights(deck, sequence, rectangle, theme, session)
	if not all_heights:
		raise ValueError(f"{images[0].location.path}:{images[0].location.line}: {slot} ordered text and component-image flow cannot fit within the supported readable minimum of {theme.body_floor_size_pt:g} pt")
	text_heights = {id(block): all_heights[index] for index, block in enumerate(sequence)
		if not isinstance(block, slide_lib.native_model.Image)}
	image_heights = {id(image): rectangle.width * slide_lib.layout_measurement.image_size(deck, image)[1] /
		slide_lib.layout_measurement.image_size(deck, image)[0] for image in images}
	available = rectangle.height - 12 * (len(sequence) - 1) - sum(text_heights.values())
	if available <= 0:
		raise ValueError(f"{images[0].location.path}:{images[0].location.line}: {slot} ordered text and component-image flow cannot fit within the supported readable minimum of {theme.body_floor_size_pt:g} pt")
	scale = min(1.0, available / sum(image_heights.values()))
	y = rectangle.y
	objects: list[slide_lib.layout_model.LayoutObject] = []
	for item in sequence:
		height = image_heights[id(item)] * scale if isinstance(item, slide_lib.native_model.Image) else text_heights[id(item)]
		item_rect = slide_lib.layout_primitives.LogicalRectangle(rectangle.x, y, rectangle.width, height)
		if isinstance(item, slide_lib.native_model.Image):
			objects.append(_picture_object(f"{slot}-image-{len(objects)}", deck, item, item_rect, slot, order + len(objects)))
		else:
			objects.append(_text_object(f"{slot}-text-{len(objects)}", item, item_rect, size,
				theme.body_floor_size_pt, slide_lib.layout_primitives.StyleRole.OUTLINE, frame, slot,
				order + len(objects), slide_lib.layout_primitives.PlaceholderKind.NONE, theme, session=session))
		y += height + 12
	return objects


def _flow_size_and_heights(deck: slide_lib.native_model.Deck,
		blocks: tuple[slide_lib.native_model.Block, ...],
		rectangle: slide_lib.layout_primitives.LogicalRectangle,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession) -> tuple[float, list[float]]:
	"""Select one body size only after measuring the whole ordered flow."""
	for quarters in range(int(theme.ordinary_body_size_pt * 4), int(theme.body_floor_size_pt * 4) - 1, -1):
		size = quarters / 4
		heights: list[float] = []
		for block in blocks:
			if isinstance(block, (slide_lib.native_model.Paragraph, slide_lib.native_model.ListBlock)):
				heights.append(slide_lib.layout_measurement.text_height(
					slide_lib.layout_measurement.items_for((block,)), size, rectangle.width, theme, session))
			elif isinstance(block, slide_lib.native_model.Table):
				heights.append(slide_lib.layout_measurement.table_height(block, size, rectangle.width, theme, session))
			elif isinstance(block, slide_lib.native_model.Image):
				width, height = slide_lib.layout_measurement.image_size(deck, block)
				heights.append(rectangle.width * height / width)
			else:
				raise ValueError(f"{block.location.path}:{block.location.line}: unsupported mixed content")
		if sum(heights) + 12 * (len(blocks) - 1) <= rectangle.height:
			return size, heights
	return theme.body_floor_size_pt, []


def _gallery(deck: slide_lib.native_model.Deck, source: slide_lib.native_model.Slide,
		theme: slide_lib.presentation_theme.PresentationTheme, index: int,
		contract: slide_lib.layout_primitives.LayoutContract,
		session: slide_lib.layout_measurement.MeasurementSession) -> slide_lib.layout_model.LayoutSlide:
	"""Build contained gallery pictures inside the single gallery allocation."""
	title = _root_title(source)
	content, title_object = _content_area(source, title, theme, contract, index, session)
	gallery = next(cell for cell in source.cells if cell.name == "gallery")
	images = tuple(block for block in gallery.blocks if isinstance(block, slide_lib.native_model.Image))
	objects = [] if title_object is None else [title_object]
	pictures: list[slide_lib.layout_model.LayoutObject] = []
	width = (content.width - 18 * (len(images) - 1)) / len(images)
	for image_index, image in enumerate(images):
		allocation = slide_lib.layout_primitives.LogicalRectangle(content.x + image_index * (width + 18), content.y, width, content.height)
		pictures.append(_picture_object(f"gallery-image-{image_index}", deck, image, allocation, "gallery", len(objects) + len(pictures)))
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
	"""Build non-overlapping question and answer-popup objects."""
	question = next(cell for cell in source.cells if cell.name == "question")
	answer = next(cell for cell in source.cells if cell.name == "answer")
	question_rect = slide_lib.layout_primitives.LogicalRectangle(60, 82, 1160, 390)
	answer_rect = slide_lib.layout_primitives.LogicalRectangle(600, 496, 580, 230)
	frame = _frame_text(contract, "question")
	slots = [_slot("question", slide_lib.layout_primitives.PlaceholderKind.OUTLINE,
		slide_lib.layout_primitives.PresentationRole.OUTLINE, question_rect, 0, frame,
		slide_lib.layout_primitives.StyleRole.OUTLINE), _slot("answer",
		slide_lib.layout_primitives.PlaceholderKind.OBJECT, slide_lib.layout_primitives.PresentationRole.OBJECT,
		answer_rect, 1, frame, slide_lib.layout_primitives.StyleRole.ACCENT)]
	objects = _cell_objects(deck, question, question_rect, theme, contract, "question", 0, frame, session)
	items = slide_lib.layout_measurement.items_for(answer.blocks)
	size = slide_lib.layout_measurement.select_size(items,
		slide_lib.layout_primitives.LogicalRectangle(618, 506, 544, 210), theme.ordinary_body_size_pt,
		theme.body_floor_size_pt, theme, answer.blocks[0].location, "multiple-choice answer", session)
	text = _text_content(answer.blocks, size, theme.body_floor_size_pt,
		slide_lib.layout_primitives.StyleRole.ACCENT, WHITE, answer_rect.width, theme,
		bold=True, session=session)
	accessibility = slide_lib.layout_primitives.ObjectAccessibility("Answer", "Multiple-choice answer popup")
	style = slide_lib.layout_content.ShapeStyle(slide_lib.layout_primitives.StyleRole.ACCENT,
		slide_lib.layout_primitives.StyleRole.ACCENT, 1, slide_lib.layout_primitives.LinePattern.NONE, 12)
	shape = slide_lib.layout_content.ShapeContent(slide_lib.layout_primitives.ShapeKind.ROUNDED_RECTANGLE,
		style, accessibility, text)
	objects.append(slide_lib.layout_model.LayoutObject("answer", slide_lib.layout_primitives.PresentationRole.OBJECT,
		slide_lib.layout_primitives.StyleRole.ACCENT, answer_rect, slide_lib.layout_primitives.ObjectLayer.CONTENT,
		len(objects), len(objects), shape, frame, "answer", "answer",
		slide_lib.layout_primitives.PlaceholderKind.OBJECT, answer.location, _reveal_targets("answer", answer.blocks, len(objects))))
	return _slide(source, index, contract, slots, objects)


def _text_object(object_id: str, block: object, rectangle: slide_lib.layout_primitives.LogicalRectangle,
		size: float, floor: float, role: slide_lib.layout_primitives.StyleRole,
		frame: slide_lib.layout_primitives.FrameTextProperties, slot: str, order: int,
		placeholder: slide_lib.layout_primitives.PlaceholderKind,
		theme: slide_lib.presentation_theme.PresentationTheme, bold: bool = False,
		session: slide_lib.layout_measurement.MeasurementSession | None = None) -> slide_lib.layout_model.LayoutObject:
	"""Create one resolved editable text object with stable reveal identity."""
	blocks = (block,) if isinstance(block, (slide_lib.native_model.Heading, slide_lib.native_model.Paragraph,
		slide_lib.native_model.ListBlock)) else tuple(block)
	content = _text_content(blocks, size, floor, role, FOREGROUND,
		rectangle.width, theme, bold, session)
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
	typography = slide_lib.layout_primitives.Typography(role, "OpenDyslexic", size, size, floor)
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
				result.append(slide_lib.layout_content.TextRun(fragment, style))
	return tuple(result)


def _table_object(object_id: str, table: slide_lib.native_model.Table,
		rectangle: slide_lib.layout_primitives.LogicalRectangle,
		theme: slide_lib.presentation_theme.PresentationTheme, slot: str, order: int,
		frame: slide_lib.layout_primitives.FrameTextProperties,
		selected_size: float | None = None,
		session: slide_lib.layout_measurement.MeasurementSession | None = None) -> slide_lib.layout_model.LayoutObject:
	"""Project a rectangular semantic table with resolved 28-to-24 point fitting."""
	rows = ((table.headers, True),) if table.headers else ()
	rows += tuple((row, False) for row in table.rows)
	columns = len(rows[0][0])
	size = selected_size if selected_size is not None else slide_lib.layout_measurement.select_table_size(table, rectangle,
		theme.ordinary_body_size_pt, theme.body_floor_size_pt, theme, session)
	typography = slide_lib.layout_primitives.Typography(slide_lib.layout_primitives.StyleRole.TABLE_BODY,
		"OpenDyslexic", size, size, theme.body_floor_size_pt)
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


def _picture_object(object_id: str, deck: slide_lib.native_model.Deck, image: slide_lib.native_model.Image,
		allocation: slide_lib.layout_primitives.LogicalRectangle, slot: str, order: int) -> slide_lib.layout_model.LayoutObject:
	"""Resolve contained display geometry and accessibility before adapter projection."""
	width, height = slide_lib.layout_measurement.image_size(deck, image)
	scale = min(allocation.width / width, allocation.height / height)
	display_width, display_height = width * scale, height * scale
	display = slide_lib.layout_primitives.LogicalRectangle(allocation.x + (allocation.width - display_width) / 2,
		allocation.y + (allocation.height - display_height) / 2, display_width, display_height)
	placement = slide_lib.layout_content.PicturePlacement(allocation, display,
		slide_lib.layout_primitives.PictureFit.CONTAIN, slide_lib.layout_primitives.CropInsets(0, 0, 0, 0))
	accessibility = slide_lib.layout_primitives.ObjectAccessibility(image.title or "Component image", image.alt_text)
	content = slide_lib.layout_content.PictureContent(image.source, placement, accessibility)
	return slide_lib.layout_model.LayoutObject(object_id, slide_lib.layout_primitives.PresentationRole.COMPONENT,
		slide_lib.layout_primitives.StyleRole.BODY, allocation, slide_lib.layout_primitives.ObjectLayer.CONTENT,
		order, order, content, None, slot, None, slide_lib.layout_primitives.PlaceholderKind.NONE,
		image.location, _reveal_targets(object_id, (image,), order))


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


def _frame_text(contract: slide_lib.layout_primitives.LayoutContract, slot: str,
		vertical: bool = False) -> slide_lib.layout_primitives.FrameTextProperties:
	"""Give every text frame explicit fixed shrink-only behavior."""
	direction = slide_lib.layout_primitives.TextDirection.VERTICAL if vertical or slot in contract.vertical_slots else slide_lib.layout_primitives.TextDirection.HORIZONTAL
	return slide_lib.layout_primitives.FrameTextProperties(slide_lib.layout_primitives.Insets(0, 0, 0, 0),
		slide_lib.layout_primitives.VerticalAlignment.TOP, slide_lib.layout_primitives.TextWrap.WRAP,
		direction, slide_lib.layout_primitives.OverflowPolicy.SHRINK)


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
		if contract.vertical_title:
			return slide_lib.layout_primitives.LogicalRectangle(1126, 60, 94, 666)
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
			item.decomposition_origin, item.origin))
	return result
