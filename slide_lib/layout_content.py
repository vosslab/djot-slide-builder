"""Editable, format-neutral content records for physical presentation objects."""

from dataclasses import dataclass

from slide_lib.layout_primitives import (CropInsets, Insets, LinePattern, ListKind,
	LogicalRectangle, ObjectAccessibility, ParagraphProperties, PictureFit, ShapeKind,
	StyleRole, Typography, VerticalAlignment, canonicalize_tuple, require_nonempty,
	require_boolean, require_nonnegative_finite, require_nonnegative_integer, require_positive_finite,
	require_positive_integer)

@dataclass(frozen=True)
class RunStyle:
	"""Resolved run facts; adapters never choose a font or color token."""
	font_family: str
	foreground: str
	underline: bool = False
	bold: bool = False
	italic: bool = False
	code: bool = False
	link_url: str | None = None
	literal_url: bool = False

	def __post_init__(self) -> None:
		require_nonempty(self.font_family, "run font family")
		require_nonempty(self.foreground, "run foreground")
		for label, value in (("run underline", self.underline), ("run bold", self.bold),
				("run italic", self.italic), ("run code", self.code),
				("run literal_url", self.literal_url)):
			require_boolean(value, label)
		if self.literal_url and self.link_url is None:
			raise ValueError("literal URL runs require a link URL")


@dataclass(frozen=True)
class TextRun:
	text: str
	style: RunStyle


@dataclass(frozen=True)
class LineBreak:
	pass


InlineContent = TextRun | LineBreak


@dataclass(frozen=True)
class ListMetadata:
	kind: ListKind
	level: int
	start: int

	def __post_init__(self) -> None:
		require_nonnegative_integer(self.level, "list level")
		require_positive_integer(self.start, "list start")


@dataclass(frozen=True)
class TextParagraph:
	inlines: tuple[InlineContent, ...]
	typography: Typography
	properties: ParagraphProperties
	display: bool = True
	list_metadata: ListMetadata | None = None

	def __post_init__(self) -> None:
		canonicalize_tuple(self, "inlines")
		require_boolean(self.display, "text paragraph display")


@dataclass(frozen=True)
class TextContent:
	paragraphs: tuple[TextParagraph, ...]

	def __post_init__(self) -> None:
		canonicalize_tuple(self, "paragraphs")


@dataclass(frozen=True)
class TableCell:
	paragraphs: tuple[TextParagraph, ...]
	padding: Insets
	vertical_alignment: VerticalAlignment
	column_span: int = 1
	row_span: int = 1

	def __post_init__(self) -> None:
		canonicalize_tuple(self, "paragraphs")
		require_positive_integer(self.column_span, "table column span")
		require_positive_integer(self.row_span, "table row span")


@dataclass(frozen=True)
class TableRow:
	cells: tuple[TableCell, ...]

	def __post_init__(self) -> None:
		canonicalize_tuple(self, "cells")


@dataclass(frozen=True)
class TableStyle:
	header_role: StyleRole
	body_role: StyleRole
	border_role: StyleRole
	border_width_pt: float
	border_pattern: LinePattern

	def __post_init__(self) -> None:
		require_positive_finite(self.border_width_pt, "table border width")


@dataclass(frozen=True)
class TableContent:
	header_rows: tuple[TableRow, ...]
	body_rows: tuple[TableRow, ...]
	column_widths: tuple[float, ...]
	row_heights: tuple[float, ...]
	style: TableStyle

	def __post_init__(self) -> None:
		for name in ("header_rows", "body_rows", "column_widths", "row_heights"):
			canonicalize_tuple(self, name)
		for value in self.column_widths + self.row_heights:
			require_positive_finite(value, "table dimension")
		if not self.column_widths or not self.row_heights:
			raise ValueError("tables require columns and rows")
		if len(self.header_rows) + len(self.body_rows) != len(self.row_heights):
			raise ValueError("table row heights must match rows")
		self._validate_grid()

	def _validate_grid(self) -> None:
		"""Require a rectangular cell grid while allowing rows covered by prior spans."""
		column_count = len(self.column_widths)
		row_count = len(self.row_heights)
		occupied = [[False for _ in range(column_count)] for _ in range(row_count)]
		rows = self.header_rows + self.body_rows
		for row_index, row in enumerate(rows):
			column_index = 0
			for cell in row.cells:
				while column_index < column_count and occupied[row_index][column_index]:
					column_index += 1
				if column_index == column_count:
					raise ValueError("table row has cells beyond its declared columns")
				end_column = column_index + cell.column_span
				end_row = row_index + cell.row_span
				if end_column > column_count or end_row > row_count:
					raise ValueError("table cell span exceeds the declared grid")
				for grid_row in range(row_index, end_row):
					for grid_column in range(column_index, end_column):
						if occupied[grid_row][grid_column]:
							raise ValueError("table cell spans overlap")
						occupied[grid_row][grid_column] = True
				column_index = end_column
			if not all(occupied[row_index]):
				raise ValueError("table row leaves part of the declared grid unfilled")


@dataclass(frozen=True)
class PicturePlacement:
	allocation_rectangle: LogicalRectangle
	displayed_rectangle: LogicalRectangle
	fit: PictureFit
	crop: CropInsets

	def __post_init__(self) -> None:
		allocation = self.allocation_rectangle
		displayed = self.displayed_rectangle
		# Keep an adapter from emitting an image frame outside its assigned slot.
		if not _rectangle_contains(allocation, displayed):
			raise ValueError("picture displayed rectangle must remain inside its allocation")
		# Contain is the sole supported image policy: preserve source proportions without crop.
		if self.fit is not PictureFit.CONTAIN:
			raise ValueError("pictures require the contain fit policy")
		if self.crop != CropInsets(0.0, 0.0, 0.0, 0.0):
			raise ValueError("contained pictures cannot crop their source")


def _rectangle_contains(outer: LogicalRectangle, inner: LogicalRectangle) -> bool:
	"""Return whether an adapter can paint the resolved image inside its allocation."""
	return (outer.x <= inner.x and outer.y <= inner.y and
		outer.x + outer.width >= inner.x + inner.width and
		outer.y + outer.height >= inner.y + inner.height)


@dataclass(frozen=True)
class PictureContent:
	source_path: str
	placement: PicturePlacement
	accessibility: ObjectAccessibility
	link_url: str | None = None

	def __post_init__(self) -> None:
		require_nonempty(self.source_path, "picture source path")
		if self.accessibility.decorative and self.link_url is not None:
			raise ValueError("decorative pictures cannot carry links")


@dataclass(frozen=True)
class ShapeStyle:
	fill_role: StyleRole
	line_role: StyleRole
	line_width_pt: float
	line_pattern: LinePattern
	corner_radius_pt: float = 0.0

	def __post_init__(self) -> None:
		require_positive_finite(self.line_width_pt, "shape line width")
		require_nonnegative_finite(self.corner_radius_pt, "shape corner radius")


@dataclass(frozen=True)
class ShapeContent:
	kind: ShapeKind
	style: ShapeStyle
	accessibility: ObjectAccessibility
	text: TextContent | None = None
	link_url: str | None = None

	def __post_init__(self) -> None:
		if self.accessibility.decorative and (self.text is not None or self.link_url is not None):
			raise ValueError("decorative shapes cannot carry semantic text or links")
		if self.kind is ShapeKind.ROUNDED_RECTANGLE and self.style.corner_radius_pt <= 0:
			raise ValueError("rounded rectangles require a positive corner radius")


ObjectContent = TextContent | TableContent | PictureContent | ShapeContent


def adapter_projectable_content(content: object) -> bool:
	"""Return whether a physical adapter has an approved editable representation."""
	return isinstance(content, (TextContent, TableContent, PictureContent, ShapeContent))


def text_capable_content(content: ObjectContent) -> bool:
	return isinstance(content, (TextContent, TableContent)) or \
		(isinstance(content, ShapeContent) and content.text is not None)


def content_paragraph_count(content: ObjectContent) -> int | None:
	if isinstance(content, TextContent):
		return len(content.paragraphs)
	if isinstance(content, ShapeContent) and content.text is not None:
		return len(content.text.paragraphs)
	return None
