"""A shared caption row beneath two equally allocated diagrams."""

import slide_lib.layout_measurement
import slide_lib.layout_primitives
import slide_lib.native_model
import slide_lib.presentation_theme


def rectangles(source: slide_lib.native_model.Slide,
		content: slide_lib.layout_primitives.LogicalRectangle,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession,
		) -> tuple[slide_lib.layout_primitives.LogicalRectangle, ...] | None:
	"""Reserve normal-size captions first, then give the figures the remaining height."""
	width = (content.width - slide_lib.layout_measurement.CELL_GUTTER) / 2
	cells = {cell.name: cell for cell in source.cells}
	caption_height = max(slide_lib.layout_measurement.text_height(
		slide_lib.layout_measurement.items_for(cells[name].blocks),
		theme.ordinary_body_size_pt, width, theme, session)
		for name in ("bottom-left", "bottom-right"))
	caption_height += slide_lib.layout_measurement.point_height(
		slide_lib.layout_measurement.TEXT_FRAME_CLEARANCE_PT, theme)
	gap = slide_lib.layout_measurement.GRID_GUTTER
	figure_height = content.height - gap - caption_height
	if figure_height <= 0:
		return None
	right = content.x + width + slide_lib.layout_measurement.CELL_GUTTER
	bottom = content.y + figure_height + gap
	rectangle = slide_lib.layout_primitives.LogicalRectangle
	result = (rectangle(content.x, content.y, width, figure_height),
		rectangle(right, content.y, width, figure_height),
		rectangle(content.x, bottom, width, caption_height),
		rectangle(right, bottom, width, caption_height))
	return result
