"""Render slide-wide citations in the bottom margin without resizing layout slots."""

import dataclasses

import slide_lib.layout_content
import slide_lib.layout_measurement
import slide_lib.layout_model
import slide_lib.layout_object_builders
import slide_lib.layout_primitives
import slide_lib.layout_validation
import slide_lib.native_model
import slide_lib.presentation_theme


# The normal content area ends at 700; even big-image captions end at 752.
CITATION_RECTANGLE = slide_lib.layout_primitives.LogicalRectangle(60, 754, 1160, 42)


def add_citation(page: slide_lib.layout_model.LayoutSlide,
		source: slide_lib.native_model.Slide,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession) -> slide_lib.layout_model.LayoutSlide:
	"""Append selectable condensed text, preserving every authored layout allocation."""
	if not source.citation:
		return page
	slide_lib.layout_validation.validate_citation(source)
	frame = slide_lib.layout_primitives.FrameTextProperties(
		slide_lib.layout_primitives.Insets(0, 0, 0, 0),
		slide_lib.layout_primitives.VerticalAlignment.TOP,
		slide_lib.layout_primitives.TextWrap.WRAP,
		slide_lib.layout_primitives.OverflowPolicy.SHRINK)
	size = slide_lib.layout_measurement.select_size(
		slide_lib.layout_measurement.items_for(source.citation),
		slide_lib.layout_measurement.text_frame_measurement(CITATION_RECTANGLE),
		14.0, 12.0, theme, source.citation[0].location,
		source.layout_class, "citation", session)
	order = max((item.reading_order for item in page.objects), default=-1) + 1
	z_index = max((item.z_index for item in page.objects), default=-1) + 1
	item = slide_lib.layout_object_builders.text_object(
		"citation", source.citation, CITATION_RECTANGLE, size, 12.0,
		slide_lib.layout_primitives.StyleRole.BODY, frame, None, order,
		slide_lib.layout_primitives.PlaceholderKind.NONE, theme, session=session)
	# The ordinary-font measurement is conservative; all citation runs use the narrow face.
	paragraphs = tuple(dataclasses.replace(paragraph,
		typography=dataclasses.replace(paragraph.typography,
			font_family=slide_lib.presentation_theme.NARROW_FONT_FAMILY),
		inlines=tuple(dataclasses.replace(run, style=dataclasses.replace(run.style,
			font_family=slide_lib.presentation_theme.NARROW_FONT_FAMILY))
			if isinstance(run, slide_lib.layout_content.TextRun) else run
			for run in paragraph.inlines)) for paragraph in item.content.paragraphs)
	item = dataclasses.replace(item, z_index=z_index + 1,
		content=dataclasses.replace(item.content, paragraphs=paragraphs))
	objects = page.objects
	if page.surface.background_role is not None:
		# A white margin band keeps citations legible on saturated section/closing slides.
		style = slide_lib.layout_content.ShapeStyle(
			slide_lib.layout_primitives.StyleRole.DECORATION,
			slide_lib.layout_primitives.StyleRole.DECORATION, 1.0,
			slide_lib.layout_primitives.LinePattern.NONE)
		backing = slide_lib.layout_model.LayoutObject(
			"citation-backing", slide_lib.layout_primitives.PresentationRole.CONTENT,
			slide_lib.layout_primitives.StyleRole.DECORATION,
			slide_lib.layout_primitives.LogicalRectangle(0, 752, 1280, 48),
			slide_lib.layout_primitives.ObjectLayer.CONTENT, z_index, order,
			slide_lib.layout_content.ShapeContent(
				slide_lib.layout_primitives.ShapeKind.RECTANGLE, style,
				slide_lib.layout_primitives.ObjectAccessibility(decorative=True)),
			None, source=source.citation[0].location)
		objects = (*objects, backing)
		item = dataclasses.replace(item, reading_order=order + 1)
	result = dataclasses.replace(page, objects=(*objects, item))
	return result
