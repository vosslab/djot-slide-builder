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
class ImageAsset:
	"""One extracted content image and its source geometry."""

	left: int
	top: int
	width: int
	height: int
	asset_path: str
	alt_text: str


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
