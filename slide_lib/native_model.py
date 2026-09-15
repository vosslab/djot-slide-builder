"""Typed presentation-neutral semantic slide objects for supported front ends."""

# Standard Library
import enum
import math
import pathlib
from dataclasses import dataclass

@dataclass(frozen=True)
class SourceLocation:
	"""One physical source position retained through native rendering."""
	path: pathlib.Path
	line: int


class RevealEffect(enum.Enum):
	"""The small set of supported visual reveal effects."""
	APPEAR = "appear"
	FADE = "fade"


class RevealSequence(enum.Enum):
	"""The authored unit that advances during a reveal."""
	OBJECT = "object"
	PARAGRAPHS = "paragraphs"


class RevealTrigger(enum.Enum):
	"""The event that advances a reveal."""
	ON_CLICK = "on-click"


class TextColor(enum.Enum):
	"""Closed authored text-color vocabulary with native editable output."""

	ACCENT = "accent"
	RED = "red"
	ORANGE = "orange"
	GREEN = "green"
	BLUE = "blue"
	PURPLE = "purple"
	GRAY = "gray"


@dataclass(frozen=True)
class Reveal:
	"""Source-neutral reveal intent for one editable native object."""
	effect: RevealEffect
	sequence: RevealSequence
	trigger: RevealTrigger = RevealTrigger.ON_CLICK


@dataclass(frozen=True)
class Attribute:
	"""One source-neutral element attribute, retaining an optional bare value."""
	name: str
	value: str | None = None


@dataclass(frozen=True)
class Text:
	"""Visible editable text."""
	value: str


@dataclass(frozen=True)
class Strong:
	"""Strong inline content."""
	children: tuple["Inline", ...]


@dataclass(frozen=True)
class Emphasis:
	"""Emphasized inline content."""
	children: tuple["Inline", ...]


@dataclass(frozen=True)
class InlineCode:
	"""Editable inline code content."""
	value: str


@dataclass(frozen=True)
class Link:
	"""Editable external hyperlink content."""
	children: tuple["Inline", ...]
	url: str


@dataclass(frozen=True)
class StyledSpan:
	"""Editable inline content carrying one supported semantic text color."""

	children: tuple["Inline", ...]
	color: TextColor


@dataclass(frozen=True)
class Break:
	"""An author-requested editable line break."""


@dataclass(frozen=True)
class InlineMath:
	"""One source-neutral inline mathematics expression."""
	value: str


Inline = Text | Strong | Emphasis | InlineCode | Link | StyledSpan | Break | InlineMath


@dataclass(frozen=True)
class Heading:
	"""A semantic heading block."""
	location: SourceLocation
	level: int
	inlines: tuple[Inline, ...]
	reveal: Reveal | None = None
	attributes: tuple[Attribute, ...] = ()


@dataclass(frozen=True)
class Paragraph:
	"""A semantic editable paragraph."""
	location: SourceLocation
	inlines: tuple[Inline, ...]
	reveal: Reveal | None = None
	attributes: tuple[Attribute, ...] = ()


@dataclass(frozen=True)
class Image:
	"""One ordinary component image with its author-provided description."""
	location: SourceLocation
	alt_text: str
	source: str
	title: str | None
	reveal: Reveal | None = None
	attributes: tuple[Attribute, ...] = ()


def _require_normalized(value: float, label: str) -> None:
	if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
		raise ValueError(f"{label} must be a finite number")
	if value < 0 or value > 1:
		raise ValueError(f"{label} must be between zero and one")


@dataclass(frozen=True)
class ImageArrow:
	"""One editable one-ended arrow positioned within a displayed image."""

	location: SourceLocation
	start_x: float
	start_y: float
	end_x: float
	end_y: float
	reveal: Reveal | None = None
	attributes: tuple[Attribute, ...] = ()

	def __post_init__(self) -> None:
		for label, value in (("arrow start x", self.start_x), ("arrow start y", self.start_y),
				("arrow end x", self.end_x), ("arrow end y", self.end_y)):
			_require_normalized(value, label)
		if self.start_x == self.end_x and self.start_y == self.end_y:
			raise ValueError("image arrows require distinct endpoints")


@dataclass(frozen=True)
class ImageOutline:
	"""One editable unfilled rectangle positioned within a displayed image."""

	location: SourceLocation
	x: float
	y: float
	width: float
	height: float
	reveal: Reveal | None = None
	attributes: tuple[Attribute, ...] = ()

	def __post_init__(self) -> None:
		for label, value in (("outline x", self.x), ("outline y", self.y),
				("outline width", self.width), ("outline height", self.height)):
			_require_normalized(value, label)
		if self.width <= 0 or self.height <= 0:
			raise ValueError("image outlines require positive width and height")
		if self.x + self.width > 1 or self.y + self.height > 1:
			raise ValueError("image outlines must remain inside the displayed image")


@dataclass(frozen=True)
class ListItem:
	"""One list item and its nested semantic lists."""
	location: SourceLocation
	inlines: tuple[Inline, ...]
	children: tuple["ListBlock", ...] = ()
	reveal: Reveal | None = None
	attributes: tuple[Attribute, ...] = ()


@dataclass(frozen=True)
class ListBlock:
	"""An ordered or unordered semantic list."""
	location: SourceLocation
	ordered: bool
	start: int
	items: tuple[ListItem, ...]
	reveal: Reveal | None = None
	attributes: tuple[Attribute, ...] = ()


@dataclass(frozen=True)
class CodeBlock:
	"""One typed fenced-code representation pending a native export owner."""
	location: SourceLocation
	value: str
	language: str | None = None
	attributes: tuple[Attribute, ...] = ()


@dataclass(frozen=True)
class Table:
	"""One semantic table with editable inline header and body cells."""
	location: SourceLocation
	headers: tuple[tuple[Inline, ...], ...]
	rows: tuple[tuple[tuple[Inline, ...], ...], ...]
	attributes: tuple[Attribute, ...] = ()


@dataclass(frozen=True)
class DisplayMath:
	"""One source-neutral display mathematics expression."""
	location: SourceLocation
	value: str
	attributes: tuple[Attribute, ...] = ()


@dataclass(frozen=True)
class QuoteBlock:
	"""One source-neutral quotation containing ordinary semantic blocks."""
	location: SourceLocation
	blocks: tuple["Block", ...]
	reveal: Reveal | None = None
	attributes: tuple[Attribute, ...] = ()


Block = Heading | Paragraph | Image | ImageArrow | ImageOutline | ListBlock | CodeBlock | Table | \
	DisplayMath | QuoteBlock


@dataclass(frozen=True)
class Cell:
	"""One content cell in source reading order."""
	location: SourceLocation
	blocks: tuple[Block, ...]
	name: str | None = None


@dataclass(frozen=True)
class Slide:
	"""One canonical source slide, ready for a named native layout builder."""
	location: SourceLocation
	layout_class: str
	notes: tuple[str, ...]
	blocks: tuple[Block, ...]
	cells: tuple[Cell, ...]
	hidden: bool = False


@dataclass(frozen=True)
class Deck:
	"""A parsed canonical deck and its authoritative source metadata."""
	path: pathlib.Path
	asset_root: pathlib.Path
	repo_root: pathlib.Path
	title: str
	slides: tuple[Slide, ...]
	color_theme: str = "genetics"

	def __post_init__(self) -> None:
		if not self.color_theme.strip():
			raise ValueError("deck color theme must not be empty")
