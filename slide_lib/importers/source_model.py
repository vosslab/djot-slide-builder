"""Raw semantic facts extracted from an imported presentation."""

# Standard Library
import dataclasses


@dataclasses.dataclass(frozen=True)
class TextRun:
	"""Characters from one source run and its validated hyperlink, if any."""

	text: str
	link: str = ""


@dataclasses.dataclass(frozen=True)
class TextBlock:
	"""One positioned source text shape with raw paragraph runs."""

	left: int
	top: int
	lines: tuple[tuple[int, tuple[TextRun, ...]], ...]
	is_subtitle: bool


@dataclasses.dataclass(frozen=True)
class PositionedText:
	"""Raw positioned text evidence awaiting planner-owned normalization."""

	paragraphs: tuple[tuple[int, tuple[TextRun, ...]], ...]
	left: int
	top: int
	width: int
	height: int
	is_subtitle: bool
	placeholder_confidence: float
	title_identity: bool = False
	source_kind: str = "text"
	source_ordinal: int = 0
	table_row: int | None = None
	table_column: int | None = None
	table_row_count: int = 0
	table_column_count: int = 0
	table_id: int | None = None
	table_has_header: bool = False
	table_unsupported_reason: str | None = None
	rotation_degrees: float = 0.0
	has_positive_fill: bool = False
	has_positive_line: bool = False
	placeholder_role: str | None = None
	z_order: tuple[int, ...] = ()


@dataclasses.dataclass(frozen=True)
class ImageAsset:
	"""One extracted content image and its source geometry."""

	left: int
	top: int
	width: int
	height: int
	asset_path: str
	alt_text: str


@dataclasses.dataclass(frozen=True)
class PositionedVisual:
	"""Raw positioned visual evidence awaiting planner-owned normalization."""

	asset_reference: str
	left: int
	top: int
	width: int
	height: int
	source_kind: str = "picture"
	source_ordinal: int = 0
	stroke_width: float | None = None
	z_order: tuple[int, ...] = ()


@dataclasses.dataclass(frozen=True)
class TableBlock:
	"""One source table with raw inline runs, dimensions, and geometry."""

	headers: tuple[tuple[TextRun, ...], ...]
	rows: tuple[tuple[tuple[TextRun, ...], ...], ...]
	left: int
	top: int
	source_ordinal: int
	unsupported_reason: str | None = None


@dataclasses.dataclass(frozen=True)
class SourcePageEvidence:
	"""Immutable ODP-only page facts retained beside format-neutral content.

	The importer records original page-layout evidence without treating its
	identity or geometry as a target layout.  Future planning rules can use the
	positive source facts while ordinary content remains format-neutral.
	"""

	source_index: int
	layout_identity: str | None
	declared_placeholder_roles: tuple[str, ...]
	populated_placeholder_roles: tuple[str, ...]
	populated_text_placeholder_roles: tuple[str, ...]
	populated_image_placeholder_roles: tuple[str, ...]
	populated_table_placeholder_roles: tuple[str, ...]
	meaningful_content_count: int

	def is_section_page(self) -> bool:
		"""Return whether positive ODP evidence identifies a section page."""
		return (
			self.layout_identity is not None
			and self.declared_placeholder_roles == ("subtitle",)
			and self.populated_text_placeholder_roles == ("subtitle",)
			and self.meaningful_content_count == 1
		)


@dataclasses.dataclass(frozen=True)
class SlideData:
	"""Raw semantic content extracted from one imported slide."""

	source_index: int
	hidden: bool
	title_lines: tuple[tuple[TextRun, ...], ...]
	text_blocks: tuple[TextBlock, ...]
	images: tuple[ImageAsset, ...]
	notes: tuple[str, ...]
	review_reasons: tuple[str, ...]
	tables: tuple[TableBlock, ...] = ()
	page_evidence: SourcePageEvidence | None = None
