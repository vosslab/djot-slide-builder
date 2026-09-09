"""Pure physical measurement and preflight for the shared layout compiler."""

import collections.abc
import dataclasses

import PIL.Image
import PIL.ImageFont

import slide_lib.editable_text
import slide_lib.layout_content
import slide_lib.capacity_report
import slide_lib.layout_model
import slide_lib.layout_primitives
import slide_lib.native_model
import slide_lib.presentation_theme


LEFT = 60.0
RIGHT = 1220.0
TITLE_TOP = 52.0
CONTENT_BOTTOM = 754.0
CELL_GUTTER = 42.0
GRID_GUTTER = 24.0
ITEM_SPACE = .25
TABLE_HORIZONTAL_PADDING = 6.0
TABLE_VERTICAL_PADDING = 4.0
TEXT_FRAME_CLEARANCE_PT = 1.0


@dataclasses.dataclass(frozen=True)
class TextFrameMeasurement:
	"""Represent the logical line and block extents for one text frame."""

	wrapping_extent: float
	available_extent: float


@dataclasses.dataclass(frozen=True)
class CenteredHeadingSizes:
	"""Retain the independently selected title and subtitle sizes in one fixed frame."""

	title_size_pt: float
	subtitle_size_pt: float | None


#============================================
def text_frame_measurement(rectangle: slide_lib.layout_primitives.LogicalRectangle) -> TextFrameMeasurement:
	"""Map one horizontal native text frame to its wrap and available extents."""
	return TextFrameMeasurement(rectangle.width, rectangle.height)


def text_frame_fits(required_extent: float, measurement: TextFrameMeasurement,
		theme: slide_lib.presentation_theme.PresentationTheme) -> bool:
	"""Keep one rendered point clear at the bottom of every bounded text frame."""
	return required_extent + point_height(TEXT_FRAME_CLEARANCE_PT, theme) <= measurement.available_extent


#============================================
def heading_rectangle(rectangle: slide_lib.layout_primitives.LogicalRectangle,
		extent: float) -> slide_lib.layout_primitives.LogicalRectangle:
	"""Allocate a local heading above the horizontal body flow."""
	return slide_lib.layout_primitives.LogicalRectangle(rectangle.x, rectangle.y, rectangle.width, extent)


#============================================
def remaining_after_heading(rectangle: slide_lib.layout_primitives.LogicalRectangle,
		extent: float) -> slide_lib.layout_primitives.LogicalRectangle:
	"""Reserve a local-heading gap above the horizontal body flow."""
	gap = 10.0
	return slide_lib.layout_primitives.LogicalRectangle(rectangle.x, rectangle.y + extent + gap,
		rectangle.width, rectangle.height - extent - gap)


def point_height(size_pt: float, theme: slide_lib.presentation_theme.PresentationTheme) -> float:
	"""Convert points only for physical geometry; typography stays point-valued."""
	result = size_pt * 12700.0 / theme.emu_per_logical_pixel
	return result


def logical_points(value: float,
		theme: slide_lib.presentation_theme.PresentationTheme) -> float:
	"""Convert logical geometry into the plan's point-valued text properties."""
	result = value * theme.emu_per_logical_pixel / 12700.0
	return result


def visible_text(inlines: tuple[slide_lib.native_model.Inline, ...]) -> str:
	"""Collect visible inline text without projecting unsupported inline math."""
	parts: list[str] = []
	for inline in inlines:
		if isinstance(inline, (slide_lib.native_model.Text, slide_lib.native_model.InlineCode)):
			parts.append(inline.value)
		elif isinstance(inline, slide_lib.native_model.Break):
			parts.append(" ")
		elif isinstance(inline, (slide_lib.native_model.Strong, slide_lib.native_model.Emphasis,
				slide_lib.native_model.Link)):
			parts.append(visible_text(inline.children))
	result = "".join(parts).strip()
	return result


class MeasurementSession:
	"""One compile-scoped owner of pinned faces and exact physical measurements."""

	def __init__(self, theme: slide_lib.presentation_theme.PresentationTheme) -> None:
		self.theme = theme
		self._profiles: dict[tuple[str, bool, bool], tuple[object, object, str]] = {}
		for metric in theme.font_metrics:
			profile = metric.face
			key = (profile.family, profile.bold, profile.italic)
			if key in self._profiles:
				raise ValueError(f"theme has duplicate validated font face: {profile.family}")
			self._profiles[key] = (profile, metric, str(slide_lib.presentation_theme.font_asset_path(profile)))
		self._faces: dict[tuple[tuple[object, ...], int], PIL.ImageFont.FreeTypeFont] = {}
		self._advances: dict[tuple[tuple[object, ...], int, str], float] = {}
		self._line_metrics: dict[tuple[tuple[object, ...], int], tuple[float, float]] = {}
		self._paragraphs: dict[tuple[object, ...], tuple[float, float, int]] = {}
		self._fragments: dict[tuple[object, ...], tuple[str, ...]] = {}
		self.capacity_diagnostics: list[slide_lib.capacity_report.CapacityDiagnostic] = []

	def record_capacity(self, location: slide_lib.native_model.SourceLocation,
			layout: str, slot: str, required: float, floor: float,
			cause: slide_lib.capacity_report.CapacityCause) -> None:
		"""Retain a bounded, source-located compromise for the build result."""
		diagnostic = slide_lib.capacity_report.CapacityDiagnostic(location, layout, slot, required,
			floor, cause)
		if diagnostic not in self.capacity_diagnostics:
			self.capacity_diagnostics.append(diagnostic)

	def _entry(self, family: str, bold: bool, italic: bool) -> tuple[object, object, str]:
		try:
			return self._profiles[(family, bold, italic)]
		except KeyError as error:
			raise ValueError(f"theme has not validated the selected font face: {family}") from error

	def _size_quarters(self, size_pt: float) -> int:
		"""Return an exact quarter-point cache identity, rejecting ambiguous sizes."""
		if not isinstance(size_pt, (int, float)) or isinstance(size_pt, bool) or size_pt <= 0:
			raise ValueError("font measurement size must be a positive point value")
		quarters = round(size_pt * 4)
		if abs(size_pt * 4 - quarters) > 1e-9:
			raise ValueError("font measurement size must be an exact quarter-point value")
		return quarters

	def _face_identity(self, profile: object) -> tuple[object, ...]:
		"""Return the complete immutable bundled-face identity for cache ownership."""
		if not isinstance(profile, slide_lib.presentation_theme.FontFaceProfile):
			raise ValueError("theme measurement profile must be a FontFaceProfile")
		return (str(profile.relative_path), profile.sha256, profile.face_index,
			profile.family, profile.bold, profile.italic)

	def _face(self, family: str, bold: bool, italic: bool, size_pt: float) -> PIL.ImageFont.FreeTypeFont:
		profile, _metric, path = self._entry(family, bold, italic)
		if not isinstance(profile, slide_lib.presentation_theme.FontFaceProfile):
			raise ValueError("theme measurement profile must be a FontFaceProfile")
		quarters = self._size_quarters(size_pt)
		size_px = max(1, round(point_height(size_pt, self.theme)))
		key = (self._face_identity(profile), quarters)
		if key not in self._faces:
			self._faces[key] = PIL.ImageFont.truetype(path, size_px, index=profile.face_index)
		return self._faces[key]

	def advance(self, family: str, bold: bool, italic: bool, size_pt: float, text: str) -> float:
		"""Measure one exact run with a cache keyed by face, size, and text."""
		profile, _metric, _path = self._entry(family, bold, italic)
		if not isinstance(profile, slide_lib.presentation_theme.FontFaceProfile):
			raise ValueError("theme measurement profile must be a FontFaceProfile")
		key = (self._face_identity(profile), self._size_quarters(size_pt), text)
		if key not in self._advances:
			self._advances[key] = self._face(family, bold, italic, size_pt).getlength(text)
		return self._advances[key]

	def line_metrics(self, family: str, bold: bool, italic: bool, size_pt: float) -> tuple[float, float]:
		"""Scale the selected validated profile's intrinsic metrics."""
		profile, metric, _path = self._entry(family, bold, italic)
		if not isinstance(profile, slide_lib.presentation_theme.FontFaceProfile) or \
				not isinstance(metric, slide_lib.presentation_theme.FontMetricProfile):
			raise ValueError("theme measurement profile must be a validated font metric")
		key = (self._face_identity(profile), self._size_quarters(size_pt))
		if key not in self._line_metrics:
			scale = point_height(size_pt, self.theme) / metric.units_per_em
			self._line_metrics[key] = (metric.ascender * scale, -metric.descender * scale)
		return self._line_metrics[key]

	def fragment_text(self, text: str, family: str, bold: bool, italic: bool, size_pt: float,
			width: float) -> tuple[str, ...]:
		"""Return lossless grapheme-safe fragments shared by sizing and emission."""
		key = (text, family, bold, italic, size_pt, width)
		if key in self._fragments:
			return self._fragments[key]
		clusters = grapheme_clusters(text)
		if not clusters or self.advance(family, bold, italic, size_pt, text) <= width:
			result = (text,)
		else:
			parts: list[str] = []; start = 0
			while start < len(clusters):
				end = start + 1
				if self.advance(family, bold, italic, size_pt, clusters[start]) > width:
					raise ValueError("an atomic Unicode grapheme cannot fit in the available text width")
				while end < len(clusters) and self.advance(family, bold, italic, size_pt,
						"".join(clusters[start:end + 1])) <= width:
					end += 1
				parts.append("".join(clusters[start:end])); start = end
			result = tuple(parts)
		self._fragments[key] = result
		return result

	def paragraph_metrics(self, inlines: tuple[slide_lib.native_model.Inline, ...], size_pt: float,
			width: float, level: int = 0, list_item: bool = False, bold: bool = False,
			italic: bool = False) -> tuple[float, float, int]:
		"""Measure paragraph wrapping once per immutable semantic and geometry key."""
		key = (inlines, size_pt, width, level, list_item, bold, italic)
		if key in self._paragraphs:
			return self._paragraphs[key]
		available = max(width - (self.theme.list_levels[level].text_position if list_item else 0.0), 1.0)
		lines: list[list[tuple[str, str, bool, bool]]] = [[]]; line_widths = [0.0]
		for text, family, token_bold, token_italic in _styled_tokens(inlines, bold, italic):
			if text == "\n": lines.append([]); line_widths.append(0.0); continue
			for token in _split_wrap_tokens(text):
				for fragment in self._fragment_token(token, family, token_bold, token_italic, size_pt, available):
					advance = self.advance(family, token_bold, token_italic, size_pt, fragment)
					if lines[-1] and line_widths[-1] + advance > available and not fragment.isspace():
						lines.append([]); line_widths.append(0.0)
					if not lines[-1] and fragment.isspace(): continue
					lines[-1].append((fragment, family, token_bold, token_italic)); line_widths[-1] += advance
		ordinary = point_height(size_pt * self.theme.ordinary_line_spacing_em, self.theme)
		advances = [ordinary if not line else max(ordinary, max(self.line_metrics(f, b, i, size_pt)[0] for _t, f, b, i in line) + max(self.line_metrics(f, b, i, size_pt)[1] for _t, f, b, i in line)) for line in lines]
		line_advance = max(advances)
		result = (line_advance * len(lines), logical_points(line_advance, self.theme), len(lines))
		self._paragraphs[key] = result
		return result

	def _fragment_token(self, token: str, family: str, bold: bool, italic: bool, size_pt: float,
			available: float) -> tuple[str, ...]:
		if token.isspace() or self.advance(family, bold, italic, size_pt, token) <= available:
			return (token,)
		parts: list[str] = []; part = ""
		for cluster in grapheme_clusters(token):
			candidate = part + cluster
			if part and self.advance(family, bold, italic, size_pt, candidate) > available:
				parts.append(part); part = cluster
			else: part = candidate
		if part: parts.append(part)
		if any(self.advance(family, bold, italic, size_pt, item) > available for item in parts):
			raise ValueError("an atomic Unicode code point cannot fit in the available text width")
		return tuple(parts)


def _styled_tokens(inlines: tuple[slide_lib.native_model.Inline, ...], bold: bool = False,
		italic: bool = False, link_url: str | None = None) -> tuple[tuple[str, str, bool, bool], ...]:
	"""Flatten editable inlines into exact-face wrapping tokens and hard breaks."""
	result: list[tuple[str, str, bool, bool]] = []
	for inline in inlines:
		if isinstance(inline, (slide_lib.native_model.Text, slide_lib.native_model.InlineCode)):
			result.append((inline.value, "OpenDyslexic", bold, italic))
		elif isinstance(inline, slide_lib.native_model.Break):
			result.append(("\n", "", False, False))
		elif isinstance(inline, slide_lib.native_model.Strong):
			result.extend(_styled_tokens(inline.children, True, italic, link_url))
		elif isinstance(inline, slide_lib.native_model.Emphasis):
			result.extend(_styled_tokens(inline.children, bold, True, link_url))
		elif isinstance(inline, slide_lib.native_model.Link):
			literal = visible_text(inline.children) == inline.url
			family = "PT Sans Narrow" if literal else "OpenDyslexic"
			for text, _family, child_bold, child_italic in _styled_tokens(inline.children, bold, italic, inline.url):
				result.append((text, "" if text == "\n" else family, child_bold, child_italic))
	return tuple(result)

def grapheme_clusters(text: str) -> tuple[str, ...]:
	"""Return conservative Unicode clusters without splitting combining/ZWJ text."""
	import unicodedata
	clusters: list[str] = []
	current = ""
	join_next = False
	for character in text:
		modifier = unicodedata.combining(character) or "\ufe00" <= character <= "\ufe0f" or \
			"\U0001f3fb" <= character <= "\U0001f3ff"
		if current and not modifier and character != "\u200d" and not join_next:
			clusters.append(current)
			current = ""
		current += character
		join_next = character == "\u200d"
	if current:
		clusters.append(current)
	return tuple(clusters)


def fragment_text(text: str, family: str, bold: bool, italic: bool, size_pt: float,
		width: float, theme: slide_lib.presentation_theme.PresentationTheme,
		session: MeasurementSession | None = None) -> tuple[str, ...]:
	"""Compatibility probe outside compilation; compiler calls its session directly."""
	return (session or MeasurementSession(theme)).fragment_text(text, family, bold, italic, size_pt, width)


def paragraph_properties(inlines: tuple[slide_lib.native_model.Inline, ...], size_pt: float,
		width: float, theme: slide_lib.presentation_theme.PresentationTheme, level: int = 0,
		list_item: bool = False, terminal: bool = False, bold: bool = False,
		italic: bool = False, session: MeasurementSession | None = None) -> slide_lib.layout_primitives.ParagraphProperties:
	"""Resolve the sole paragraph spacing and indentation contract used by builders."""
	_height, line_spacing_pt, _lines = (session or MeasurementSession(theme)).paragraph_metrics(
		inlines, size_pt, width, level, list_item, bold, italic)
	indent_start = 0.0
	first_line = 0.0
	if list_item:
		level_style = theme.list_levels[level]
		indent_start = logical_points(level_style.text_position, theme)
		first_line = logical_points(level_style.bullet_position - level_style.text_position, theme)
	space_after = 0.0 if terminal else size_pt * ITEM_SPACE
	result = slide_lib.layout_primitives.ParagraphProperties(
		slide_lib.layout_primitives.HorizontalAlignment.START, 0, space_after,
		line_spacing_pt, indent_start, 0, first_line, ())
	return result


def paragraph_height(inlines: tuple[slide_lib.native_model.Inline, ...], size_pt: float,
		width: float, theme: slide_lib.presentation_theme.PresentationTheme, level: int = 0,
		list_item: bool = False, bold: bool = False, italic: bool = False,
		session: MeasurementSession | None = None) -> float:
	"""Expose exact one-paragraph geometry to title and local-heading allocation."""
	return (session or MeasurementSession(theme)).paragraph_metrics(
		inlines, size_pt, width, level, list_item, bold, italic)[0]


def _split_wrap_tokens(text: str) -> tuple[str, ...]:
	"""Keep whitespace and oversized lexical tokens deterministic during wrapping."""
	result: list[str] = []
	current = ""
	for character in text:
		if character.isspace():
			if current:
				result.append(current)
				current = ""
			result.append(character)
		else:
			current += character
	if current:
		result.append(current)
	return tuple(result)


def wrapped_lines(inlines: tuple[slide_lib.native_model.Inline, ...], size_pt: float,
		width: float, theme: slide_lib.presentation_theme.PresentationTheme, level: int = 0,
		list_item: bool = False, bold: bool = False, italic: bool = False) -> int:
	"""Return measured line count for callers that allocate a single heading."""
	_height, _spacing, lines = MeasurementSession(theme).paragraph_metrics(
		inlines, size_pt, width, level, list_item, bold, italic)
	return lines


def text_height(items: tuple[tuple[tuple[slide_lib.native_model.Inline, ...], int, bool], ...],
		size_pt: float, width: float, theme: slide_lib.presentation_theme.PresentationTheme,
		session: MeasurementSession | None = None, bold: bool = False) -> float:
	"""Measure flattened body/list paragraphs at one selected size."""
	active = session or MeasurementSession(theme)
	result = sum(active.paragraph_metrics(inlines, size_pt, width, level, listed, bold=bold)[0] +
		point_height(size_pt * ITEM_SPACE, theme) for inlines, level, listed in items)
	# A physical text frame has no meaningful trailing paragraph gap.  Keeping
	# measurement aligned with projection prevents a terminal 6--7 px artefact
	# from falsely rejecting a floor-safe layout.
	if items:
		result -= point_height(size_pt * ITEM_SPACE, theme)
	return result


def items_for(blocks: tuple[slide_lib.native_model.Block, ...]) -> tuple[tuple[tuple[slide_lib.native_model.Inline, ...], int, bool], ...]:
	"""Flatten only supported editable paragraphs and lists."""
	items: list[tuple[tuple[slide_lib.native_model.Inline, ...], int, bool]] = []
	for block in blocks:
		if isinstance(block, slide_lib.native_model.Paragraph):
			items.append((block.inlines, 0, False))
		elif isinstance(block, slide_lib.native_model.ListBlock):
			for item in slide_lib.editable_text.project_list(block):
				items.append((item.inlines, item.level, not item.paragraph_only))
	return tuple(items)


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
		session: MeasurementSession) -> float:
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
		measurement: TextFrameMeasurement, preferred: float, floor: float,
		theme: slide_lib.presentation_theme.PresentationTheme, location: slide_lib.native_model.SourceLocation,
		layout: str, slot: str, session: MeasurementSession | None = None,
		cause: slide_lib.capacity_report.CapacityCause =
		slide_lib.capacity_report.CapacityCause.PARAGRAPH_LIST,
		record_capacity: bool = True, bold: bool = False) -> float:
	"""Choose a quarter-point size, recording a visible sub-floor compromise."""
	minimum = slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT
	def fits(value: float) -> bool:
		"""Measure one candidate against the shared serialized-frame boundary."""
		required = text_height(items, value, measurement.wrapping_extent, theme, session, bold=bold)
		return text_frame_fits(required, measurement, theme)
	size = largest_fitting_size(preferred, minimum, fits)
	if size is None:
		raise slide_lib.capacity_report.PhysicalCapacityError(location, layout, slot, floor,
			cause, minimum)
	if size < floor and session is not None and record_capacity:
		session.record_capacity(location, layout, slot, size, floor, cause)
	return size


#============================================
def heading_items(headings: tuple[slide_lib.native_model.Heading, ...]
		) -> tuple[tuple[tuple[slide_lib.native_model.Inline, ...], int, bool], ...]:
	"""Project fixed-frame heading paragraphs into the shared text measurement input."""
	return tuple((heading.inlines, 0, False) for heading in headings)


#============================================
def select_fixed_heading_size(headings: tuple[slide_lib.native_model.Heading, ...],
		rectangle: slide_lib.layout_primitives.LogicalRectangle, preferred: float, floor: float,
		theme: slide_lib.presentation_theme.PresentationTheme, layout: str, slot: str,
		cause: slide_lib.capacity_report.CapacityCause, bold: bool,
		session: MeasurementSession) -> float:
	"""Select one serializer-safe size for all heading paragraphs in a fixed frame."""
	items = heading_items(headings)
	if not items:
		raise ValueError("fixed heading measurement requires at least one heading")
	return select_size(items, text_frame_measurement(rectangle), preferred, floor, theme,
		headings[0].location, layout, slot, session, cause, bold=bold)


#============================================
def select_centered_heading_sizes(title: slide_lib.native_model.Heading,
		subtitles: tuple[slide_lib.native_model.Heading, ...],
		rectangle: slide_lib.layout_primitives.LogicalRectangle,
		theme: slide_lib.presentation_theme.PresentationTheme, layout: str,
		session: MeasurementSession) -> CenteredHeadingSizes:
	"""Fit centered title/subtitle text together while preserving title priority."""
	title_items = heading_items((title,))
	subtitle_items = heading_items(subtitles)
	minimum = slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT
	for title_size in _quarter_sizes(theme.standard_title_size_pt, minimum):
		title_height = text_height(title_items, title_size, rectangle.width, theme, session,
			bold=True)
		gap = point_height(title_size * ITEM_SPACE, theme) if subtitle_items else 0.0
		available = rectangle.height - point_height(TEXT_FRAME_CLEARANCE_PT, theme) - title_height - gap
		if available <= 0:
			continue
		if not subtitle_items:
			if title_size < theme.title_floor_size_pt:
				session.record_capacity(title.location, layout, "title", title_size,
					theme.title_floor_size_pt, slide_lib.capacity_report.CapacityCause.TITLE)
			return CenteredHeadingSizes(title_size, None)
		subtitle_size = largest_fitting_size(theme.ordinary_body_size_pt, minimum,
			lambda size: text_height(subtitle_items, size, rectangle.width, theme, session) <= available)
		if subtitle_size is None:
			continue
		if title_size < theme.title_floor_size_pt:
			session.record_capacity(title.location, layout, "title", title_size,
				theme.title_floor_size_pt, slide_lib.capacity_report.CapacityCause.TITLE)
		if subtitle_size < theme.body_floor_size_pt:
			session.record_capacity(subtitles[0].location, layout, "subtitle", subtitle_size,
				theme.body_floor_size_pt, slide_lib.capacity_report.CapacityCause.LOCAL_HEADING)
		return CenteredHeadingSizes(title_size, subtitle_size)
	if not text_frame_fits(text_height(title_items, minimum, rectangle.width, theme, session,
			bold=True), text_frame_measurement(rectangle), theme):
		raise slide_lib.capacity_report.PhysicalCapacityError(title.location, layout, "title",
			theme.title_floor_size_pt, slide_lib.capacity_report.CapacityCause.TITLE, minimum)
	location = subtitles[0].location if subtitles else title.location
	raise slide_lib.capacity_report.PhysicalCapacityError(location, layout, "subtitle",
		theme.body_floor_size_pt, slide_lib.capacity_report.CapacityCause.LOCAL_HEADING, minimum)


def select_paragraph_size(inlines: tuple[slide_lib.native_model.Inline, ...],
		measurement: TextFrameMeasurement, preferred: float, floor: float,
		theme: slide_lib.presentation_theme.PresentationTheme, location: slide_lib.native_model.SourceLocation,
		layout: str, slot: str, bold: bool, session: MeasurementSession,
		cause: slide_lib.capacity_report.CapacityCause =
		slide_lib.capacity_report.CapacityCause.LOCAL_HEADING) -> float:
	"""Select one heading-like paragraph size that fully occupies its final text frame."""
	minimum = slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT
	def fits(value: float) -> bool:
		"""Measure one candidate against the shared serialized-frame boundary."""
		required = paragraph_height(inlines, value, measurement.wrapping_extent, theme,
			bold=bold, session=session)
		return text_frame_fits(required, measurement, theme)
	size = largest_fitting_size(preferred, minimum, fits)
	if size is None:
		raise slide_lib.capacity_report.PhysicalCapacityError(location, layout, slot, floor,
			cause, minimum)
	if size < floor:
		session.record_capacity(location, layout, slot, size, floor, cause)
	return size


def table_height(table: slide_lib.native_model.Table, size_pt: float, width: float,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: MeasurementSession | None = None) -> float:
	"""Measure table rows by their tallest cell, never by a fictitious cell stack."""
	rows = (table.headers,) if table.headers else ()
	rows += table.rows
	columns = len(rows[0])
	cell_width = width / columns - TABLE_HORIZONTAL_PADDING * 2
	return sum(max(text_height(((cell, 0, False),), size_pt, cell_width, theme, session) +
		TABLE_VERTICAL_PADDING * 2 for cell in row) for row in rows)


def select_table_size(table: slide_lib.native_model.Table,
		rectangle: slide_lib.layout_primitives.LogicalRectangle, preferred: float, floor: float,
		theme: slide_lib.presentation_theme.PresentationTheme,
		layout: str, slot: str, session: MeasurementSession | None = None) -> float:
	"""Choose a table size and report when it must cross the readable floor."""
	minimum = slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT
	size = largest_fitting_size(preferred, minimum,
		lambda value: text_frame_fits(table_height(table, value, rectangle.width, theme, session),
			text_frame_measurement(rectangle), theme))
	if size is None:
		raise slide_lib.capacity_report.PhysicalCapacityError(table.location, layout, slot, floor,
			slide_lib.capacity_report.CapacityCause.TABLE, minimum)
	if size < floor and session is not None:
		session.record_capacity(table.location, layout, slot, size, floor,
			slide_lib.capacity_report.CapacityCause.TABLE)
	return size


def grid(left: float, top: float, width: float, height: float, columns: int, rows: int) -> tuple[slide_lib.layout_primitives.LogicalRectangle, ...]:
	"""Allocate a reading-order grid without output-format geometry."""
	cell_width = (width - CELL_GUTTER * (columns - 1)) / columns
	cell_height = (height - GRID_GUTTER * (rows - 1)) / rows
	result = tuple(slide_lib.layout_primitives.LogicalRectangle(
		left + column * (cell_width + CELL_GUTTER), top + row * (cell_height + GRID_GUTTER),
		cell_width, cell_height,
	) for row in range(rows) for column in range(columns))
	return result


def slot_rectangles(name: str, content: slide_lib.layout_primitives.LogicalRectangle) -> tuple[slide_lib.layout_primitives.LogicalRectangle, ...]:
	"""Return all standard named-cell allocations from a contract name."""
	left, top, width, height = content.x, content.y, content.width, content.height
	if name == "one-panel":
		return (content,)
	if name == "two-panels":
		return grid(left, top, width, height, 2, 1)
	if name == "one-plus-two-panels":
		cell_width = (width - CELL_GUTTER) / 2
		half = (height - GRID_GUTTER) / 2
		return (slide_lib.layout_primitives.LogicalRectangle(left, top, cell_width, height),
			slide_lib.layout_primitives.LogicalRectangle(left + cell_width + CELL_GUTTER, top, cell_width, half),
			slide_lib.layout_primitives.LogicalRectangle(left + cell_width + CELL_GUTTER, top + half + GRID_GUTTER, cell_width, half))
	if name == "two-plus-one-panels":
		cell_width = (width - CELL_GUTTER) / 2
		half = (height - GRID_GUTTER) / 2
		return (slide_lib.layout_primitives.LogicalRectangle(left, top, cell_width, half),
			slide_lib.layout_primitives.LogicalRectangle(left, top + half + GRID_GUTTER, cell_width, half),
			slide_lib.layout_primitives.LogicalRectangle(left + cell_width + CELL_GUTTER, top, cell_width, height))
	if name == "stacked-panels":
		return grid(left, top, width, height, 1, 2)
	if name == "two-over-one-panels":
		half = (height - GRID_GUTTER) / 2
		return (*grid(left, top, width, half, 2, 1),
			slide_lib.layout_primitives.LogicalRectangle(left, top + half + GRID_GUTTER, width, half))
	if name == "four-panels":
		return grid(left, top, width, height, 2, 2)
	if name == "six-panels":
		return grid(left, top, width, height, 3, 2)
	raise ValueError(f"unknown physical geometry: {name}")


def image_size(deck: slide_lib.native_model.Deck,
		image: slide_lib.native_model.Image) -> tuple[float, float]:
	"""Return the intrinsic dimensions of one ordinary image."""
	path = (deck.asset_root / image.source).resolve()
	if not path.is_relative_to(deck.repo_root) or not path.is_file():
		raise ValueError(f"{image.location.path}:{image.location.line}: component image is missing or outside the repository: {image.source}")
	with PIL.Image.open(path) as opened:
		result = opened.size
	return result


@dataclasses.dataclass(frozen=True)
class MixedFlowAllocation:
	"""Retain the exact proportional image/text heights for one final mixed-flow frame."""

	size_pt: float
	blocks: tuple[slide_lib.native_model.Block, ...]
	heights: tuple[float, ...]


#============================================
def mixed_flow_allocation(deck: slide_lib.native_model.Deck,
		text_blocks: tuple[slide_lib.native_model.Block, ...],
		images: tuple[slide_lib.native_model.Image, ...],
		rectangle: slide_lib.layout_primitives.LogicalRectangle, size_pt: float,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: MeasurementSession) -> MixedFlowAllocation | None:
	"""Allocate floor-safe text then proportionally scale images into every remaining pixel."""
	blocks = tuple(sorted(text_blocks + images, key=lambda block: block.location.line))
	text_heights = {id(block): text_height(items_for((block,)), size_pt, rectangle.width, theme, session)
		for block in text_blocks}
	natural_image_heights = {id(image): rectangle.width * image_size(deck, image)[1] /
		image_size(deck, image)[0] for image in images}
	available = rectangle.height - point_height(TEXT_FRAME_CLEARANCE_PT, theme) - \
		12 * (len(blocks) - 1) - sum(text_heights.values())
	if available <= 0:
		return None
	scale = min(1.0, available / sum(natural_image_heights.values()))
	heights = tuple(natural_image_heights[id(block)] * scale if isinstance(block,
		slide_lib.native_model.Image) else text_heights[id(block)] for block in blocks)
	if not text_frame_fits(sum(heights) + 12 * (len(blocks) - 1),
			text_frame_measurement(rectangle), theme):
		return None
	return MixedFlowAllocation(size_pt, blocks, heights)


def unsupported_facts(slide: slide_lib.native_model.Slide) -> tuple[slide_lib.layout_model.UnsupportedSourceFact, ...]:
	"""Collect constructs without a deliberately approved editable projection."""
	facts: list[slide_lib.layout_model.UnsupportedSourceFact] = []
	for block in _descendant_blocks(slide.blocks + tuple(block for cell in slide.cells for block in cell.blocks)):
		attributes = getattr(block, "attributes", ())
		if isinstance(block, (slide_lib.native_model.CodeBlock, slide_lib.native_model.DisplayMath,
			slide_lib.native_model.QuoteBlock)):
			facts.append(slide_lib.layout_model.UnsupportedSourceFact(block.location, type(block).__name__, attributes))
		elif attributes:
			facts.append(slide_lib.layout_model.UnsupportedSourceFact(block.location, type(block).__name__, attributes))
		for inline in _block_inlines(block):
			if isinstance(inline, slide_lib.native_model.InlineMath):
				facts.append(slide_lib.layout_model.UnsupportedSourceFact(block.location, "InlineMath"))
		if isinstance(block, slide_lib.native_model.ListBlock):
			for item in _descendant_list_items(block):
				if item.attributes:
					facts.append(slide_lib.layout_model.UnsupportedSourceFact(
						item.location, type(item).__name__, item.attributes))
	return tuple(facts)


def _block_inlines(block: slide_lib.native_model.Block) -> tuple[slide_lib.native_model.Inline, ...]:
	"""Return recursive inline facts for every editable block container."""
	if isinstance(block, (slide_lib.native_model.Heading, slide_lib.native_model.Paragraph)):
		return _descendant_inlines(block.inlines)
	if isinstance(block, slide_lib.native_model.ListBlock):
		return tuple(inline for item in block.items for inline in _descendant_inlines(item.inlines))
	if isinstance(block, slide_lib.native_model.Table):
		return tuple(inline for row in (block.headers,) + block.rows for cell in row
			for inline in _descendant_inlines(cell))
	return ()


def _descendant_inlines(inlines: tuple[slide_lib.native_model.Inline, ...]) -> tuple[slide_lib.native_model.Inline, ...]:
	result: list[slide_lib.native_model.Inline] = []
	for inline in inlines:
		result.append(inline)
		if isinstance(inline, (slide_lib.native_model.Strong, slide_lib.native_model.Emphasis,
				slide_lib.native_model.Link)):
			result.extend(_descendant_inlines(inline.children))
	return tuple(result)


def _descendant_blocks(blocks: tuple[slide_lib.native_model.Block, ...]) -> tuple[slide_lib.native_model.Block, ...]:
	result: list[slide_lib.native_model.Block] = []
	for block in blocks:
		result.append(block)
		if isinstance(block, slide_lib.native_model.QuoteBlock):
			result.extend(_descendant_blocks(block.blocks))
		elif isinstance(block, slide_lib.native_model.ListBlock):
			for item in block.items:
				for child in item.children:
					result.extend(_descendant_blocks((child,)))
	return tuple(result)


def _descendant_list_items(block: slide_lib.native_model.ListBlock) -> tuple[slide_lib.native_model.ListItem, ...]:
	result: list[slide_lib.native_model.ListItem] = []
	for item in block.items:
		result.append(item)
		for child in item.children:
			result.extend(_descendant_list_items(child))
	return tuple(result)
