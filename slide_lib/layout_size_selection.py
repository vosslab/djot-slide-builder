"""Choose serializer-safe font sizes from exact text measurements."""

import collections.abc
import dataclasses

import slide_lib.capacity_report
import slide_lib.layout_measurement
import slide_lib.layout_primitives
import slide_lib.native_model
import slide_lib.presentation_theme


@dataclasses.dataclass(frozen=True)
class CenteredHeadingSizes:
	"""Retain independently selected title and subtitle sizes in one fixed frame."""

	title_size_pt: float
	subtitle_size_pt: float | None


def _quarter_sizes(preferred: float, minimum: float) -> tuple[float, ...]:
	"""Return descending exact quarter-point candidates within one physical bound."""
	return tuple(quarters / 4 for quarters in range(int(preferred * 4), int(minimum * 4) - 1, -1))


def largest_fitting_size(preferred: float, minimum: float,
		fits: collections.abc.Callable[[float], bool]) -> float | None:
	"""Return the largest serializer-valid quarter point satisfying one exact predicate."""
	return next((size for size in _quarter_sizes(preferred, minimum) if fits(size)), None)


def select_title_size(preferred: float, floor: float,
		geometry_for_size: collections.abc.Callable[[float], slide_lib.layout_primitives.LogicalRectangle | None],
		body_fits_floor: collections.abc.Callable[[slide_lib.layout_primitives.LogicalRectangle], bool],
		location: slide_lib.native_model.SourceLocation, layout: str, slot: str,
		session: slide_lib.layout_measurement.MeasurementSession) -> float:
	"""Select the largest valid title whose canonical body geometry keeps its readable floor."""
	minimum = slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT
	fallback: float | None = None
	for size in _quarter_sizes(preferred, minimum):
		content = geometry_for_size(size)
		if content is None:
			continue
		if fallback is None:
			fallback = size
		if body_fits_floor(content):
			if size < floor:
				session.record_capacity(location, layout, slot, size, floor,
					slide_lib.capacity_report.CapacityCause.TITLE)
			return size
	if fallback is not None:
		if fallback < floor:
			session.record_capacity(location, layout, slot, fallback, floor,
				slide_lib.capacity_report.CapacityCause.TITLE)
		return fallback
	raise slide_lib.capacity_report.PhysicalCapacityError(location, layout, slot, floor,
		slide_lib.capacity_report.CapacityCause.TITLE, minimum)


def select_size(items: tuple[tuple[tuple[slide_lib.native_model.Inline, ...], int, bool], ...],
		measurement: slide_lib.layout_measurement.TextFrameMeasurement, preferred: float, floor: float,
		theme: slide_lib.presentation_theme.PresentationTheme, location: slide_lib.native_model.SourceLocation,
		layout: str, slot: str, session: slide_lib.layout_measurement.MeasurementSession | None = None,
		cause: slide_lib.capacity_report.CapacityCause =
		slide_lib.capacity_report.CapacityCause.PARAGRAPH_LIST,
		record_capacity: bool = True, bold: bool = False) -> float:
	"""Choose a quarter-point size, recording a visible sub-floor compromise."""
	minimum = slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT
	def fits(value: float) -> bool:
		"""Measure one candidate against the shared serialized-frame boundary."""
		required = slide_lib.layout_measurement.text_height(
			items, value, measurement.wrapping_extent, theme, session, bold=bold)
		return slide_lib.layout_measurement.text_frame_fits(required, measurement, theme)
	size = largest_fitting_size(preferred, minimum, fits)
	if size is None:
		raise slide_lib.capacity_report.PhysicalCapacityError(location, layout, slot, floor,
			cause, minimum)
	if size < floor and session is not None and record_capacity:
		session.record_capacity(location, layout, slot, size, floor, cause)
	return size


def heading_items(headings: tuple[slide_lib.native_model.Heading, ...]
		) -> tuple[tuple[tuple[slide_lib.native_model.Inline, ...], int, bool], ...]:
	"""Project fixed-frame heading paragraphs into the shared text measurement input."""
	return tuple((heading.inlines, 0, False) for heading in headings)


def select_fixed_heading_size(headings: tuple[slide_lib.native_model.Heading, ...],
		rectangle: slide_lib.layout_primitives.LogicalRectangle, preferred: float, floor: float,
		theme: slide_lib.presentation_theme.PresentationTheme, layout: str, slot: str,
		cause: slide_lib.capacity_report.CapacityCause, bold: bool,
		session: slide_lib.layout_measurement.MeasurementSession) -> float:
	"""Select one serializer-safe size for all heading paragraphs in a fixed frame."""
	items = heading_items(headings)
	if not items:
		raise ValueError("fixed heading measurement requires at least one heading")
	return select_size(items, slide_lib.layout_measurement.text_frame_measurement(rectangle),
		preferred, floor, theme, headings[0].location, layout, slot, session, cause, bold=bold)


def select_centered_heading_sizes(title: slide_lib.native_model.Heading,
		subtitles: tuple[slide_lib.native_model.Heading, ...],
		rectangle: slide_lib.layout_primitives.LogicalRectangle,
		theme: slide_lib.presentation_theme.PresentationTheme, layout: str,
		session: slide_lib.layout_measurement.MeasurementSession) -> CenteredHeadingSizes:
	"""Fit centered title/subtitle text together while preserving title priority."""
	title_items = heading_items((title,))
	subtitle_items = heading_items(subtitles)
	minimum = slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT
	for title_size in _quarter_sizes(theme.standard_title_size_pt, minimum):
		title_height = slide_lib.layout_measurement.text_height(
			title_items, title_size, rectangle.width, theme, session, bold=True)
		gap = slide_lib.layout_measurement.point_height(title_size * slide_lib.layout_measurement.ITEM_SPACE, theme) if subtitle_items else 0.0
		available = rectangle.height - slide_lib.layout_measurement.point_height(
			slide_lib.layout_measurement.TEXT_FRAME_CLEARANCE_PT, theme) - title_height - gap
		if available <= 0:
			continue
		if not subtitle_items:
			if title_size < theme.title_floor_size_pt:
				session.record_capacity(title.location, layout, "title", title_size,
					theme.title_floor_size_pt, slide_lib.capacity_report.CapacityCause.TITLE)
			return CenteredHeadingSizes(title_size, None)
		subtitle_size = largest_fitting_size(theme.ordinary_body_size_pt, minimum,
			lambda size: slide_lib.layout_measurement.text_height(
				subtitle_items, size, rectangle.width, theme, session) <= available)
		if subtitle_size is None:
			continue
		if title_size < theme.title_floor_size_pt:
			session.record_capacity(title.location, layout, "title", title_size,
				theme.title_floor_size_pt, slide_lib.capacity_report.CapacityCause.TITLE)
		if subtitle_size < theme.body_floor_size_pt:
			session.record_capacity(subtitles[0].location, layout, "subtitle", subtitle_size,
				theme.body_floor_size_pt, slide_lib.capacity_report.CapacityCause.LOCAL_HEADING)
		return CenteredHeadingSizes(title_size, subtitle_size)
	if not slide_lib.layout_measurement.text_frame_fits(
			slide_lib.layout_measurement.text_height(title_items, minimum, rectangle.width, theme, session,
				bold=True), slide_lib.layout_measurement.text_frame_measurement(rectangle), theme):
		raise slide_lib.capacity_report.PhysicalCapacityError(title.location, layout, "title",
			theme.title_floor_size_pt, slide_lib.capacity_report.CapacityCause.TITLE, minimum)
	location = subtitles[0].location if subtitles else title.location
	raise slide_lib.capacity_report.PhysicalCapacityError(location, layout, "subtitle",
		theme.body_floor_size_pt, slide_lib.capacity_report.CapacityCause.LOCAL_HEADING, minimum)


def select_paragraph_size(inlines: tuple[slide_lib.native_model.Inline, ...],
		measurement: slide_lib.layout_measurement.TextFrameMeasurement, preferred: float, floor: float,
		theme: slide_lib.presentation_theme.PresentationTheme, location: slide_lib.native_model.SourceLocation,
		layout: str, slot: str, bold: bool, session: slide_lib.layout_measurement.MeasurementSession,
		cause: slide_lib.capacity_report.CapacityCause =
		slide_lib.capacity_report.CapacityCause.LOCAL_HEADING) -> float:
	"""Select one heading-like paragraph size that fully occupies its final text frame."""
	minimum = slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT
	def fits(value: float) -> bool:
		"""Measure one candidate against the shared serialized-frame boundary."""
		required = slide_lib.layout_measurement.paragraph_height(
			inlines, value, measurement.wrapping_extent, theme, bold=bold, session=session)
		return slide_lib.layout_measurement.text_frame_fits(required, measurement, theme)
	size = largest_fitting_size(preferred, minimum, fits)
	if size is None:
		raise slide_lib.capacity_report.PhysicalCapacityError(location, layout, slot, floor,
			cause, minimum)
	if size < floor:
		session.record_capacity(location, layout, slot, size, floor, cause)
	return size
