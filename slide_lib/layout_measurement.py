"""Pure physical measurement and preflight for the shared layout compiler."""

import dataclasses
import math

import PIL.ImageFont

import slide_lib.capacity_report
import slide_lib.editable_text
import slide_lib.layout_content
import slide_lib.layout_primitives
import slide_lib.layout_source_facts
import slide_lib.math_layout
import slide_lib.math_render
import slide_lib.native_model
import slide_lib.presentation_theme
import slide_lib.typography
import slide_lib.table_styles


LEFT = 60.0
RIGHT = 1220.0
TITLE_TOP = 52.0
CONTENT_BOTTOM = 700.0
CELL_GUTTER = 42.0
GRID_GUTTER = 24.0
ITEM_SPACE = .25
TEXT_FRAME_CLEARANCE_PT = 1.0
MeasuredToken = tuple[str, str, bool, bool, bool, float, int]


@dataclasses.dataclass(frozen=True)
class TextFrameMeasurement:
	"""Represent the logical line and block extents for one text frame."""

	wrapping_extent: float
	available_extent: float


#============================================
def text_frame_measurement(rectangle: slide_lib.layout_primitives.LogicalRectangle) -> TextFrameMeasurement:
	"""Map one horizontal native text frame to its wrap and available extents."""
	return TextFrameMeasurement(rectangle.width, rectangle.height)


def text_frame_fits(required_extent: float, measurement: TextFrameMeasurement,
		theme: slide_lib.presentation_theme.PresentationTheme) -> bool:
	"""Keep one rendered point clear at the bottom of every bounded text frame."""
	return required_extent + point_height(TEXT_FRAME_CLEARANCE_PT, theme) <= measurement.available_extent


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
	"""Collect source text, including equation TeX, for labels and diagnostics."""
	parts: list[str] = []
	for inline in inlines:
		if isinstance(inline, (slide_lib.native_model.Text, slide_lib.native_model.InlineCode,
				slide_lib.native_model.InlineMath)):
			parts.append(inline.value)
		elif isinstance(inline, slide_lib.native_model.Break):
			parts.append(" ")
		elif isinstance(inline, (slide_lib.native_model.Strong, slide_lib.native_model.Emphasis,
				slide_lib.native_model.Link, slide_lib.native_model.StyledSpan)):
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
		self._faces: dict[tuple[tuple[object, ...], float], PIL.ImageFont.FreeTypeFont] = {}
		self._advances: dict[tuple[tuple[object, ...], float, str], float] = {}
		self._line_metrics: dict[tuple[tuple[object, ...], float], tuple[float, float]] = {}
		self._paragraphs: dict[tuple[object, ...], tuple[float, float, int]] = {}
		self._fragments: dict[tuple[object, ...], tuple[str, ...]] = {}
		self.capacity_diagnostics: list[slide_lib.capacity_report.CapacityDiagnostic] = []
		self.table_context: object | None = None
		self.table_registry = slide_lib.table_styles.load_registry()
		self._resolved_tables: dict[slide_lib.native_model.Table,
			slide_lib.table_styles.ResolvedTable] = {}
		self.equations: dict[tuple[str, bool], slide_lib.math_render.RenderedMath] = {}

	def resolved_table(self, table: slide_lib.native_model.Table) -> slide_lib.table_styles.ResolvedTable:
		"""Share one resolved style grid through group sizing, fitting, and construction."""
		if table not in self._resolved_tables:
			self._resolved_tables[table] = slide_lib.table_styles.resolve_table(
				table, self.theme, self.table_registry)
		return self._resolved_tables[table]

	def prepare_equations(self, deck: slide_lib.native_model.Deck) -> None:
		"""Render every distinct expression before fitting any candidate sizes."""
		requests = {}
		for source in deck.slides:
			blocks = source.blocks + tuple(block for cell in source.cells for block in cell.blocks)
			slide_lib.math_render.validate_equation_blocks(blocks)
			for block in slide_lib.layout_source_facts.descendant_blocks(blocks):
				for inline in slide_lib.layout_source_facts.block_inlines(block):
					if isinstance(inline, slide_lib.native_model.InlineMath):
						requests.setdefault((inline.value, inline.display), block.location)
		self.equations = slide_lib.math_render.render_equations(requests)
		self.math_directory = deck.repo_root / "_temp" / "math"

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

	def _size_key(self, size_pt: float) -> float:
		"""Cache the actual positive size without requiring a quarter-point grid."""
		if not isinstance(size_pt, (int, float)) or isinstance(size_pt, bool) or \
				not math.isfinite(size_pt) or size_pt <= 0:
			raise ValueError("font measurement size must be a positive point value")
		return size_pt

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
		size_key = self._size_key(size_pt)
		# Whole-pixel rounding can move an entire word across a line boundary.
		size_px = max(1.0, point_height(size_pt, self.theme))
		key = (self._face_identity(profile), size_key)
		if key not in self._faces:
			self._faces[key] = PIL.ImageFont.truetype(path, size_px, index=profile.face_index)
		return self._faces[key]

	def advance(self, family: str, bold: bool, italic: bool, size_pt: float, text: str) -> float:
		"""Measure one exact run with a cache keyed by face, size, and text."""
		profile, _metric, _path = self._entry(family, bold, italic)
		if not isinstance(profile, slide_lib.presentation_theme.FontFaceProfile):
			raise ValueError("theme measurement profile must be a FontFaceProfile")
		key = (self._face_identity(profile), self._size_key(size_pt), text)
		if key not in self._advances:
			self._advances[key] = self._face(family, bold, italic, size_pt).getlength(text)
		return self._advances[key]

	def line_metrics(self, family: str, bold: bool, italic: bool, size_pt: float) -> tuple[float, float]:
		"""Scale the selected validated profile's intrinsic metrics."""
		profile, metric, _path = self._entry(family, bold, italic)
		if not isinstance(profile, slide_lib.presentation_theme.FontFaceProfile) or \
				not isinstance(metric, slide_lib.presentation_theme.FontMetricProfile):
			raise ValueError("theme measurement profile must be a validated font metric")
		key = (self._face_identity(profile), self._size_key(size_pt))
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
		result = self._fragment_token(text, family, bold, italic, size_pt, width)
		self._fragments[key] = result
		return result

	def paragraph_metrics(self, inlines: tuple[slide_lib.native_model.Inline, ...], size_pt: float,
			width: float, level: int = 0, list_item: bool = False, bold: bool = False,
			italic: bool = False) -> tuple[float, float, int]:
		"""Measure paragraph wrapping once per immutable semantic and geometry key."""
		key = (inlines, size_pt, width, level, list_item, bold, italic)
		if key in self._paragraphs:
			return self._paragraphs[key]
		if slide_lib.math_layout.has_math(inlines):
			result = slide_lib.math_layout.paragraph_metrics(inlines, size_pt, width,
				level, list_item, bold, italic, self)
			self._paragraphs[key] = result
			return result
		available = max(width - (self.theme.list_levels[level].text_position if list_item else 0.0), 1.0)
		lines, _widths = self.wrap_tokens(_styled_tokens(inlines, bold, italic), size_pt, available)
		ordinary = point_height(size_pt * self.theme.ordinary_line_spacing_em, self.theme)
		advances = []
		for line in lines:
			metrics = [self.line_metrics(f, b, i, selected_size)
				for _text, f, b, i, _literal, selected_size, _index in line]
			advance = max(ordinary, max(item[0] for item in metrics) +
				max(item[1] for item in metrics)) if metrics else ordinary
			advances.append(advance)
		line_advance = max(advances)
		result = (line_advance * len(lines), logical_points(line_advance, self.theme), len(lines))
		self._paragraphs[key] = result
		return result

	def wrap_tokens(self, tokens: tuple[tuple[str, str, bool, bool, bool], ...],
			size_pt: float, available: float, balance: bool = True) -> tuple[list[list[MeasuredToken]], list[float]]:
		"""Share exact styled line wrapping between sizing and advisory audits."""
		lines: list[list[MeasuredToken]] = [[]]; line_widths = [0.0]
		for index, (text, family, token_bold, token_italic, literal) in enumerate(tokens):
			if text == "\n": lines.append([]); line_widths.append(0.0); continue
			token_size = slide_lib.presentation_theme.inline_size_pt(size_pt, literal)
			if literal:
				clearance = point_height(TEXT_FRAME_CLEARANCE_PT, self.theme)
				minimum_width = self.advance(family, token_bold, token_italic,
					slide_lib.presentation_theme.URL_FLOOR_SIZE_PT, text)
				if lines[-1] and minimum_width + clearance > available - line_widths[-1]:
					lines.append([]); line_widths.append(0.0)
				token_size = self.fit_url_size(text, family, token_bold, token_italic,
					token_size, available - line_widths[-1] - clearance)
			for token in ((text,) if literal else _split_wrap_tokens(text)):
				for fragment_index, fragment in enumerate(self._fragment_token(
						token, family, token_bold, token_italic, token_size, available)):
					advance = self.advance(family, token_bold, token_italic, token_size, fragment)
					if fragment_index or (lines[-1] and line_widths[-1] + advance > available
							and not fragment.isspace()):
						lines.append([]); line_widths.append(0.0)
					if not lines[-1] and fragment.isspace(): continue
					lines[-1].append((fragment, family, token_bold, token_italic, literal,
						token_size, index)); line_widths[-1] += advance
		if balance and not any(text == "\n" or literal for text, _family, _bold, _italic, literal in tokens):
			self.balance_tail(lines, line_widths, available)
		return lines, line_widths

	def balance_tail(self, lines: list[list[MeasuredToken]], widths: list[float], available: float) -> None:
		"""Move whole words into a runt without changing line count, text size, or styling."""
		if len(lines) < 2 or not lines[-2] or not lines[-2][-1][0].isspace():
			return
		original_lines = [list(line) for line in lines[-2:]]
		original_widths = widths[-2:]
		def ink(line: list[MeasuredToken]) -> float:
			trimmed = list(line)
			while trimmed and trimmed[-1][0].isspace():
				trimmed.pop()
			return sum(self.advance(family, bold, italic, size, text)
				for text, family, bold, italic, _literal, size, _index in trimmed)
		while slide_lib.typography.has_runt([
				("".join(token[0] for token in line).strip(), ink(line)) for line in lines[-2:]]):
			previous = list(lines[-2])
			while previous and previous[-1][0].isspace():
				previous.pop()
			boundary = next((index for index in range(len(previous) - 1, -1, -1)
				if previous[index][0].isspace()), None)
			if boundary is None:
				break
			prefix = previous[:boundary]
			if len("".join(token[0] for token in prefix).split()) < 2:
				break
			tail = previous[boundary + 1:] + [previous[boundary]] + lines[-1]
			if ink(tail) > available or ink(prefix) < ink(tail) / 3:
				break
			lines[-2], lines[-1] = prefix, tail
			widths[-2], widths[-1] = ink(prefix), ink(tail)
		if slide_lib.typography.has_runt([
				("".join(token[0] for token in line).strip(), ink(line)) for line in lines[-2:]]):
			lines[-2:] = original_lines
			widths[-2:] = original_widths


	def fit_url_size(self, text: str, family: str, bold: bool, italic: bool,
			start: float, width: float) -> float:
		"""Fit a visible URL independently, retaining the instructor's 12 pt floor."""
		floor = slide_lib.presentation_theme.URL_FLOOR_SIZE_PT
		advance = self.advance(family, bold, italic, start, text)
		if advance <= width:
			return start
		size = max(floor, math.floor(start * max(width, 0) / advance * 4) / 4)
		while size > floor and self.advance(family, bold, italic, size, text) > width:
			size = max(floor, size - .25)
		return size

	def _fragment_token(self, token: str, family: str, bold: bool, italic: bool, size_pt: float,
			available: float) -> tuple[str, ...]:
		if token.isspace() or self.advance(family, bold, italic, size_pt, token) <= available:
			return (token,)
		parts: list[str] = []; part = ""
		is_url = token.startswith(("https://", "http://"))
		for cluster in grapheme_clusters(token):
			candidate = part + cluster
			if part and self.advance(family, bold, italic, size_pt, candidate) > available:
				# Prefer address structure to arbitrary character splits; retain every byte.
				boundary = max((index + 1 for index, character in enumerate(part)
					if character in "/-_?&=" and (parts or index >= len("https://"))), default=0) \
					if is_url else 0
				if boundary:
					parts.append(part[:boundary]); part = part[boundary:] + cluster
				else:
					parts.append(part); part = cluster
			else: part = candidate
		if part: parts.append(part)
		if any(self.advance(family, bold, italic, size_pt, item) > available for item in parts):
			raise ValueError("an atomic Unicode code point cannot fit in the available text width")
		return tuple(parts)


def _styled_tokens(inlines: tuple[slide_lib.native_model.Inline, ...], bold: bool = False,
		italic: bool = False, link_url: str | None = None) -> tuple[tuple[str, str, bool, bool, bool], ...]:
	"""Flatten editable inlines into exact-face wrapping tokens and hard breaks."""
	result: list[tuple[str, str, bool, bool, bool]] = []
	for inline in inlines:
		if isinstance(inline, (slide_lib.native_model.Text, slide_lib.native_model.InlineCode)):
			family = slide_lib.presentation_theme.MONOSPACE_FONT_FAMILY \
				if isinstance(inline, slide_lib.native_model.InlineCode) \
				else slide_lib.presentation_theme.ORDINARY_FONT_FAMILY
			literal = slide_lib.presentation_theme.is_visible_url(inline.value)
			if literal:
				family = slide_lib.presentation_theme.NARROW_FONT_FAMILY
			result.append((inline.value, family, bold, italic, literal))
		elif isinstance(inline, slide_lib.native_model.Break):
			result.append(("\n", "", False, False, False))
		elif isinstance(inline, slide_lib.native_model.Strong):
			result.extend(_styled_tokens(inline.children, True, italic, link_url))
		elif isinstance(inline, slide_lib.native_model.Emphasis):
			result.extend(_styled_tokens(inline.children, bold, True, link_url))
		elif isinstance(inline, slide_lib.native_model.Link):
			literal = slide_lib.presentation_theme.is_visible_url(visible_text(inline.children))
			for text, family, child_bold, child_italic, _literal in _styled_tokens(inline.children, bold, italic, inline.url):
				if literal:
					family = slide_lib.presentation_theme.NARROW_FONT_FAMILY
				result.append((text, family, child_bold, child_italic, literal))
		elif isinstance(inline, slide_lib.native_model.StyledSpan):
			result.extend(_styled_tokens(inline.children, bold, italic, link_url))
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
	if len(inlines) == 1 and isinstance(inlines[0], slide_lib.native_model.InlineMath) \
			and inlines[0].display:
		result = dataclasses.replace(result,
			horizontal_alignment=slide_lib.layout_primitives.HorizontalAlignment.CENTER)
	return result


def paragraph_height(inlines: tuple[slide_lib.native_model.Inline, ...], size_pt: float,
		width: float, theme: slide_lib.presentation_theme.PresentationTheme, level: int = 0,
		list_item: bool = False, bold: bool = False, italic: bool = False,
		session: MeasurementSession | None = None) -> float:
	"""Expose exact one-paragraph geometry to title and local-heading allocation."""
	return (session or MeasurementSession(theme)).paragraph_metrics(
		inlines, size_pt, width, level, list_item, bold, italic)[0]


def _split_wrap_tokens(text: str) -> tuple[str, ...]:
	"""Retain whitespace and allow native breaks after ordinary hyphens and en dashes."""
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
			if character in "-\u2010\u2013":
				result.append(current)
				current = ""
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
	if name in ("one-panel", "reference", "bookend", "definitions"):
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
