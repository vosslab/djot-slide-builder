"""Build cover decorations, transitions, closers, and image-focus slides."""

import dataclasses

import slide_lib.capacity_report
import slide_lib.layout_content
import slide_lib.layout_measurement
import slide_lib.layout_model
import slide_lib.layout_object_builders
import slide_lib.layout_primitives
import slide_lib.native_model
import slide_lib.presentation_theme


FOREGROUND = "172033"
WHITE = "FFFFFF"
SECTION_TITLE_SIZE_PT = 48.0
SECTION_SUBTITLE_SIZE_PT = 30.0
END_TITLE_SIZE_PT = 156.0
END_TITLE_FLOOR_SIZE_PT = 110.0
END_LINE_SPACING_EM = 1.06
CAPTION_SIZE_PT = 22.0
CAPTION_FLOOR_SIZE_PT = 18.0


@dataclasses.dataclass(frozen=True)
class SpecialtySlideComponents:
	"""Carry complete physical components to the common slide finalizer."""

	slots: tuple[slide_lib.layout_model.LayoutSlot, ...]
	objects: tuple[slide_lib.layout_model.LayoutObject, ...]
	surface: slide_lib.layout_primitives.SlideSurface = slide_lib.layout_primitives.SlideSurface()


def title_slide_decorations(theme: slide_lib.presentation_theme.PresentationTheme
		) -> tuple[slide_lib.layout_model.LayoutObject, ...]:
	"""Frame title-slide metadata with restrained theme-derived native shapes."""
	outline = _master_rectangle(theme.outline_frame, theme)
	card = slide_lib.layout_primitives.LogicalRectangle(
		outline.x + 64, outline.y + 64, outline.width - 128, outline.height - 128)
	title = _master_rectangle(theme.title_frame, theme)
	accent = slide_lib.layout_primitives.LogicalRectangle(
		title.x + (title.width - 140) / 2, title.y + title.height + 24, 140, 7)
	return (
		_decorative_shape("title-metadata-frame", card,
			slide_lib.layout_primitives.ShapeKind.ROUNDED_RECTANGLE,
			slide_lib.layout_primitives.StyleRole.DECORATION,
			slide_lib.layout_primitives.StyleRole.TRANSITION,
			slide_lib.layout_primitives.LinePattern.SOLID, 2.5, 22, 0, 2),
		_decorative_shape("title-accent", accent,
			slide_lib.layout_primitives.ShapeKind.ROUNDED_RECTANGLE,
			slide_lib.layout_primitives.StyleRole.ACCENT,
			slide_lib.layout_primitives.StyleRole.ACCENT,
			slide_lib.layout_primitives.LinePattern.NONE, 1, 4, 1, 3),
	)


def section_components(headings: tuple[slide_lib.native_model.Heading, ...],
		theme: slide_lib.presentation_theme.PresentationTheme,
		contract: slide_lib.layout_primitives.LayoutContract,
		session: slide_lib.layout_measurement.MeasurementSession) -> SpecialtySlideComponents:
	"""Build one centered transition card in LibreOffice's Centered Text member."""
	if len(headings) == 1 and slide_lib.layout_measurement.visible_text(
			headings[0].inlines) == "THE END":
		return _end_components(headings[0], theme, contract, session)
	rectangle = slide_lib.layout_primitives.LogicalRectangle(150, 235, 980, 330)
	frame = dataclasses.replace(_frame_text(),
		vertical_alignment=slide_lib.layout_primitives.VerticalAlignment.MIDDLE)
	transition_theme = dataclasses.replace(theme,
		standard_title_size_pt=SECTION_TITLE_SIZE_PT,
		ordinary_body_size_pt=SECTION_SUBTITLE_SIZE_PT)
	sizes = slide_lib.layout_measurement.select_centered_heading_sizes(
		headings[0], headings[1:], rectangle, transition_theme, contract.name, session)
	subtitle_size = sizes.subtitle_size_pt if sizes.subtitle_size_pt is not None \
		else theme.ordinary_body_size_pt
	title = slide_lib.layout_object_builders.text_content(
		(headings[0],), sizes.title_size_pt, theme.title_floor_size_pt,
		slide_lib.layout_primitives.StyleRole.TITLE, WHITE,
		rectangle.width, theme, bold=True, session=session)
	subtitle = slide_lib.layout_object_builders.text_content(
		headings[1:], subtitle_size, theme.body_floor_size_pt,
		slide_lib.layout_primitives.StyleRole.SUBTITLE, WHITE,
		rectangle.width, theme, session=session)
	paragraphs = tuple(dataclasses.replace(paragraph, properties=dataclasses.replace(
		paragraph.properties,
		horizontal_alignment=slide_lib.layout_primitives.HorizontalAlignment.CENTER))
		for paragraph in title.paragraphs + subtitle.paragraphs)
	content = slide_lib.layout_content.TextContent(paragraphs)
	slot = _slot("title", slide_lib.layout_primitives.PlaceholderKind.OUTLINE,
		slide_lib.layout_primitives.PresentationRole.OUTLINE, rectangle, 0, frame,
		slide_lib.layout_primitives.StyleRole.BODY)
	item = slide_lib.layout_model.LayoutObject(contract.name,
		slide_lib.layout_primitives.PresentationRole.OUTLINE,
		slide_lib.layout_primitives.StyleRole.BODY, rectangle,
		slide_lib.layout_primitives.ObjectLayer.LAYOUT, 1, 0, content, frame,
		"title", "title", slide_lib.layout_primitives.PlaceholderKind.OUTLINE,
		headings[0].location,
		slide_lib.layout_object_builders.reveal_targets(contract.name, headings, 0))
	border = _decorative_shape(f"{contract.name}-frame",
		slide_lib.layout_primitives.LogicalRectangle(105, 190, 1070, 420),
		slide_lib.layout_primitives.ShapeKind.ROUNDED_RECTANGLE,
		slide_lib.layout_primitives.StyleRole.ANSWER if contract.name == "subsection" else
		slide_lib.layout_primitives.StyleRole.TRANSITION,
		slide_lib.layout_primitives.StyleRole.DECORATION,
		slide_lib.layout_primitives.LinePattern.SOLID, 2.5, 24, 0, 1)
	surface = slide_lib.layout_primitives.SlideSurface(
		slide_lib.layout_primitives.StyleRole.ANSWER if contract.name == "subsection" else
		slide_lib.layout_primitives.StyleRole.TRANSITION, False)
	return SpecialtySlideComponents((slot,), (border, item), surface)


def big_image_components(deck: slide_lib.native_model.Deck,
		source: slide_lib.native_model.Slide,
		theme: slide_lib.presentation_theme.PresentationTheme,
		contract: slide_lib.layout_primitives.LayoutContract,
		session: slide_lib.layout_measurement.MeasurementSession) -> SpecialtySlideComponents:
	"""Give one component image the page and retain a short editable bottom caption."""
	image_cell = next(cell for cell in source.cells if cell.name == "image")
	caption_cell = next(cell for cell in source.cells if cell.name == "caption")
	image = image_cell.blocks[0]
	if not isinstance(image, slide_lib.native_model.Image):
		raise ValueError("validated big-image source must begin with its component image")
	overlays = tuple(block for block in image_cell.blocks[1:] if isinstance(block,
		(slide_lib.native_model.ImageArrow, slide_lib.native_model.ImageOutline)))
	image_rectangle = slide_lib.layout_primitives.LogicalRectangle(60, 26, 1160, 590)
	caption_rectangle = slide_lib.layout_primitives.LogicalRectangle(60, 634, 1160, 118)
	caption_frame = dataclasses.replace(_frame_text(),
		padding=slide_lib.layout_primitives.Insets(18, 10, 18, 10),
		vertical_alignment=slide_lib.layout_primitives.VerticalAlignment.MIDDLE)
	inner = slide_lib.layout_primitives.LogicalRectangle(
		0, 0, caption_rectangle.width - 36, caption_rectangle.height - 20)
	size = slide_lib.layout_measurement.select_size(
		slide_lib.layout_measurement.items_for(caption_cell.blocks),
		slide_lib.layout_measurement.text_frame_measurement(inner),
		CAPTION_SIZE_PT, CAPTION_FLOOR_SIZE_PT, theme, caption_cell.location,
		contract.name, "caption", session)
	caption_text = slide_lib.layout_object_builders.text_content(
		caption_cell.blocks, size, CAPTION_FLOOR_SIZE_PT,
		slide_lib.layout_primitives.StyleRole.BODY, FOREGROUND,
		inner.width, theme, session=session)
	caption_text = dataclasses.replace(caption_text, paragraphs=tuple(
		dataclasses.replace(paragraph, properties=dataclasses.replace(
			paragraph.properties,
			horizontal_alignment=slide_lib.layout_primitives.HorizontalAlignment.CENTER))
		for paragraph in caption_text.paragraphs))
	caption_shape = slide_lib.layout_content.ShapeContent(
		slide_lib.layout_primitives.ShapeKind.ROUNDED_RECTANGLE,
		slide_lib.layout_content.ShapeStyle(
			slide_lib.layout_primitives.StyleRole.PANEL,
			slide_lib.layout_primitives.StyleRole.PANEL,
			1, slide_lib.layout_primitives.LinePattern.NONE, 16),
		slide_lib.layout_primitives.ObjectAccessibility(
			"Caption", "Caption for the primary slide image"), caption_text)
	image_object = slide_lib.layout_object_builders.picture_object(
		"big-image", deck, image, image_rectangle, "image", 0)
	if not isinstance(image_object.content, slide_lib.layout_content.PictureContent):
		raise ValueError("big-image picture builder must return native picture content")
	overlay_objects = tuple(slide_lib.layout_object_builders.image_overlay_object(
		f"big-image-overlay-{index + 1}", overlay,
		image_object.content.placement.displayed_rectangle, "image", index + 1, theme)
		for index, overlay in enumerate(overlays))
	caption_order = len(overlay_objects) + 1
	caption_object = slide_lib.layout_model.LayoutObject("caption",
		slide_lib.layout_primitives.PresentationRole.CONTENT,
		slide_lib.layout_primitives.StyleRole.BODY, caption_rectangle,
		slide_lib.layout_primitives.ObjectLayer.CONTENT, caption_order, caption_order,
		caption_shape, caption_frame, "caption", source=caption_cell.location)
	image_slot = _slot("image", slide_lib.layout_primitives.PlaceholderKind.NONE,
		slide_lib.layout_primitives.PresentationRole.COMPONENT,
		image_rectangle, 0, None, slide_lib.layout_primitives.StyleRole.BODY)
	caption_slot = _slot("caption", slide_lib.layout_primitives.PlaceholderKind.NONE,
		slide_lib.layout_primitives.PresentationRole.CONTENT,
		caption_rectangle, 1, caption_frame, slide_lib.layout_primitives.StyleRole.BODY)
	return SpecialtySlideComponents(
		(image_slot, caption_slot), (image_object, *overlay_objects, caption_object))


def _end_components(title: slide_lib.native_model.Heading,
		theme: slide_lib.presentation_theme.PresentationTheme,
		contract: slide_lib.layout_primitives.LayoutContract,
		session: slide_lib.layout_measurement.MeasurementSession) -> SpecialtySlideComponents:
	"""Build the two-line THE END closer with editable type and a vector star inside the D."""
	rectangle = slide_lib.layout_primitives.LogicalRectangle(190, 130, 900, 600)
	frame = dataclasses.replace(_frame_text(),
		vertical_alignment=slide_lib.layout_primitives.VerticalAlignment.MIDDLE)
	def fits(candidate: float) -> bool:
		"""Keep both display lines inside their exact native frame."""
		width = max(session.advance(slide_lib.presentation_theme.ORDINARY_FONT_FAMILY,
			True, False, candidate, value) for value in ("THE", "END"))
		line_spacing_pt = candidate * END_LINE_SPACING_EM
		height = 2 * slide_lib.layout_measurement.point_height(line_spacing_pt, theme)
		return width <= rectangle.width and slide_lib.layout_measurement.text_frame_fits(
			height, slide_lib.layout_measurement.text_frame_measurement(rectangle), theme)
	size = slide_lib.layout_measurement.largest_fitting_size(
		END_TITLE_SIZE_PT, END_TITLE_FLOOR_SIZE_PT, fits)
	if size is None:
		raise slide_lib.capacity_report.PhysicalCapacityError(title.location, contract.name,
			"title", END_TITLE_FLOOR_SIZE_PT,
			slide_lib.capacity_report.CapacityCause.TITLE, END_TITLE_FLOOR_SIZE_PT)
	the_heading = dataclasses.replace(title, inlines=(slide_lib.native_model.Text("THE"),))
	end_heading = dataclasses.replace(title, inlines=(slide_lib.native_model.Text("END"),))
	content = slide_lib.layout_object_builders.text_content(
		(the_heading, end_heading), size, END_TITLE_FLOOR_SIZE_PT,
		slide_lib.layout_primitives.StyleRole.TITLE, WHITE,
		rectangle.width, theme, bold=True, session=session)
	line_spacing_pt = size * END_LINE_SPACING_EM
	content = dataclasses.replace(content, paragraphs=tuple(dataclasses.replace(paragraph,
		properties=dataclasses.replace(paragraph.properties,
			horizontal_alignment=slide_lib.layout_primitives.HorizontalAlignment.CENTER,
			space_after_pt=0, line_spacing_pt=line_spacing_pt))
		for paragraph in content.paragraphs))
	slot = _slot("title", slide_lib.layout_primitives.PlaceholderKind.OUTLINE,
		slide_lib.layout_primitives.PresentationRole.OUTLINE, rectangle, 0, frame,
		slide_lib.layout_primitives.StyleRole.TITLE)
	text = slide_lib.layout_model.LayoutObject("end-title",
		slide_lib.layout_primitives.PresentationRole.OUTLINE,
		slide_lib.layout_primitives.StyleRole.TITLE, rectangle,
		slide_lib.layout_primitives.ObjectLayer.LAYOUT, 2, 0, content, frame,
		"title", "title", slide_lib.layout_primitives.PlaceholderKind.OUTLINE,
		title.location)
	outer = _decorative_shape("end-outer-frame",
		slide_lib.layout_primitives.LogicalRectangle(110, 40, 1060, 720),
		slide_lib.layout_primitives.ShapeKind.ROUNDED_RECTANGLE,
		slide_lib.layout_primitives.StyleRole.TRANSITION,
		slide_lib.layout_primitives.StyleRole.DECORATION,
		slide_lib.layout_primitives.LinePattern.SOLID, 3, 54, 0, 1)
	inner = _decorative_shape("end-inner-frame",
		slide_lib.layout_primitives.LogicalRectangle(155, 75, 970, 650),
		slide_lib.layout_primitives.ShapeKind.ROUNDED_RECTANGLE,
		slide_lib.layout_primitives.StyleRole.ACCENT,
		slide_lib.layout_primitives.StyleRole.DECORATION,
		slide_lib.layout_primitives.LinePattern.SOLID, 2.5, 44, 1, 2)
	total_width = session.advance(slide_lib.presentation_theme.ORDINARY_FONT_FAMILY,
		True, False, size, "END")
	prefix_width = session.advance(slide_lib.presentation_theme.ORDINARY_FONT_FAMILY,
		True, False, size, "EN")
	d_width = session.advance(slide_lib.presentation_theme.ORDINARY_FONT_FAMILY,
		True, False, size, "D")
	text_left = rectangle.x + (rectangle.width - total_width) / 2
	line_height = slide_lib.layout_measurement.point_height(line_spacing_pt, theme)
	star_size = 34.0
	star_center_x = text_left + prefix_width + d_width / 2
	star = _decorative_shape("end-star",
		slide_lib.layout_primitives.LogicalRectangle(
			star_center_x - star_size / 2,
			rectangle.y + rectangle.height / 2 + line_height / 2 - 28 - star_size / 2,
			star_size, star_size),
		slide_lib.layout_primitives.ShapeKind.STAR,
		slide_lib.layout_primitives.StyleRole.DECORATION,
		slide_lib.layout_primitives.StyleRole.DECORATION,
		slide_lib.layout_primitives.LinePattern.NONE, 1, 0, 3, 3)
	surface = slide_lib.layout_primitives.SlideSurface(
		slide_lib.layout_primitives.StyleRole.TRANSITION, False)
	return SpecialtySlideComponents((slot,), (outer, inner, text, star), surface)


def _master_rectangle(frame: slide_lib.presentation_theme.FrameGeometry,
		theme: slide_lib.presentation_theme.PresentationTheme
		) -> slide_lib.layout_primitives.LogicalRectangle:
	"""Convert an authoritative master-frame fact to compiler logical geometry."""
	logical_per_cm = 360000.0 / theme.emu_per_logical_pixel
	return slide_lib.layout_primitives.LogicalRectangle(
		frame.x_cm * logical_per_cm, frame.y_cm * logical_per_cm,
		frame.width_cm * logical_per_cm, frame.height_cm * logical_per_cm)


def _decorative_shape(object_id: str,
		rectangle: slide_lib.layout_primitives.LogicalRectangle,
		kind: slide_lib.layout_primitives.ShapeKind,
		fill_role: slide_lib.layout_primitives.StyleRole,
		line_role: slide_lib.layout_primitives.StyleRole,
		line_pattern: slide_lib.layout_primitives.LinePattern,
		line_width_pt: float, corner_radius_pt: float, z_index: int,
		reading_order: int) -> slide_lib.layout_model.LayoutObject:
	"""Build one editable layout-owned decoration outside presentation members."""
	style = slide_lib.layout_content.ShapeStyle(fill_role, line_role, line_width_pt,
		line_pattern, corner_radius_pt)
	content = slide_lib.layout_content.ShapeContent(kind, style,
		slide_lib.layout_primitives.ObjectAccessibility(decorative=True))
	return slide_lib.layout_model.LayoutObject(object_id,
		slide_lib.layout_primitives.PresentationRole.GRAPHIC,
		slide_lib.layout_primitives.StyleRole.DECORATION, rectangle,
		slide_lib.layout_primitives.ObjectLayer.DECORATION,
		z_index, reading_order, content,
		origin=slide_lib.layout_primitives.LayoutObjectOrigin.THEME)


def _slot(name: str, kind: slide_lib.layout_primitives.PlaceholderKind,
		role: slide_lib.layout_primitives.PresentationRole,
		rectangle: slide_lib.layout_primitives.LogicalRectangle, order: int,
		frame: slide_lib.layout_primitives.FrameTextProperties | None,
		style: slide_lib.layout_primitives.StyleRole) -> slide_lib.layout_model.LayoutSlot:
	"""Construct one specialty-layout slot and matching topology member."""
	return slide_lib.layout_model.LayoutSlot(name, kind, role, rectangle, order,
		slide_lib.layout_primitives.PlaceholderProperties(style, frame))


def _frame_text() -> slide_lib.layout_primitives.FrameTextProperties:
	"""Give specialty text frames explicit horizontal shrink-only behavior."""
	return slide_lib.layout_primitives.FrameTextProperties(
		slide_lib.layout_primitives.Insets(0, 0, 0, 0),
		slide_lib.layout_primitives.VerticalAlignment.TOP,
		slide_lib.layout_primitives.TextWrap.WRAP,
		slide_lib.layout_primitives.OverflowPolicy.SHRINK)
