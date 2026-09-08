"""Typed presentation-neutral semantic slide objects for supported front ends."""

# Standard Library
import enum
import pathlib
from dataclasses import dataclass, field


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
class Break:
	"""An author-requested editable line break."""


@dataclass(frozen=True)
class InlineMath:
	"""One source-neutral inline mathematics expression."""
	value: str


Inline = Text | Strong | Emphasis | InlineCode | Link | Break | InlineMath


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


Block = Heading | Paragraph | Image | ListBlock | CodeBlock | Table | DisplayMath | QuoteBlock


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
	paginate: bool
	notes: tuple[str, ...]
	blocks: tuple[Block, ...]
	cells: tuple[Cell, ...]


@dataclass(frozen=True)
class Deck:
	"""A parsed canonical deck and its authoritative source metadata."""
	path: pathlib.Path
	asset_root: pathlib.Path
	repo_root: pathlib.Path
	title: str
	paginate: bool
	slides: tuple[Slide, ...]
	front_matter: dict[str, object] = field(compare=False)
