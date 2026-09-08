"""Format-neutral scalar, geometry, and presentation-layout facts."""

import enum
import math
import numbers
from dataclasses import dataclass


LOGICAL_SLIDE_WIDTH = 1280.0
LOGICAL_SLIDE_HEIGHT = 800.0


class PresentationRole(enum.Enum):
	TITLE = "title"
	SUBTITLE = "subtitle"
	OUTLINE = "outline"
	CONTENT = "content"
	GRAPHIC = "graphic"
	OBJECT = "object"
	COMPONENT = "component"


class PlaceholderKind(enum.Enum):
	TITLE = "title"
	SUBTITLE = "subtitle"
	OUTLINE = "outline"
	OBJECT = "object"
	NONE = "none"


class ObjectLayer(enum.Enum):
	BACKGROUND = "background"
	LAYOUT = "layout"
	CONTENT = "content"
	DECORATION = "decoration"
	FOREGROUND = "foreground"


class LayoutObjectOrigin(enum.Enum):
	"""Declare whether a physical object is authored, repeated, or chrome."""
	AUTHORED = "authored"
	REPEATED_CONTEXT = "repeated-context"
	GENERATED_CHROME = "generated-chrome"


class StyleRole(enum.Enum):
	TITLE = "title"
	SUBTITLE = "subtitle"
	OUTLINE = "outline"
	BODY = "body"
	LOCAL_HEADING = "local-heading"
	TABLE_HEADER = "table-header"
	TABLE_BODY = "table-body"
	ACCENT = "accent"
	MUTED = "muted"
	DECORATION = "decoration"


class OverflowPolicy(enum.Enum):
	SHRINK = "shrink"
	CLIP = "clip"


class LineSpacingMode(enum.Enum):
	"""Declare the physical meaning of a paragraph line-spacing value."""

	EXACT = "exact"


class ContinuationPolicy(enum.Enum):
	FORBID = "forbid"
	ALLOW = "allow"
	DECOMPOSE_TO_ONE_PANEL = "decompose-to-one-panel"


class ContinuationContextDisplay(enum.Enum):
	"""Declare how an inherited list trail is exposed on a physical slide."""
	INLINE_STATIC = "inline-static"
	HANDOFF_STATIC = "handoff-static"
	METADATA_ONLY = "metadata-only"


class ContinuationKind(enum.Enum):
	"""Keep authored and compiler-created continuation pages distinguishable."""
	NORMAL = "normal"
	AUTHORED = "authored"
	CONTEXT_HANDOFF = "context-handoff"


class ListKind(enum.Enum):
	ORDERED = "ordered"
	UNORDERED = "unordered"


class HorizontalAlignment(enum.Enum):
	START = "start"
	CENTER = "center"
	END = "end"
	JUSTIFY = "justify"


class VerticalAlignment(enum.Enum):
	TOP = "top"
	MIDDLE = "middle"
	BOTTOM = "bottom"


class TextWrap(enum.Enum):
	WRAP = "wrap"
	NO_WRAP = "no-wrap"


class TextDirection(enum.Enum):
	HORIZONTAL = "horizontal"
	VERTICAL = "vertical"


class PictureFit(enum.Enum):
	CONTAIN = "contain"
	COVER = "cover"
	STRETCH = "stretch"


class ShapeKind(enum.Enum):
	RECTANGLE = "rectangle"
	ROUNDED_RECTANGLE = "rounded-rectangle"
	LINE = "line"


class LinePattern(enum.Enum):
	SOLID = "solid"
	DASHED = "dashed"
	DOTTED = "dotted"
	NONE = "none"


def require_nonempty(value: str, label: str) -> None:
	if not value.strip():
		raise ValueError(f"{label} must not be empty")


def require_finite(value: float, label: str) -> None:
	"""Require a finite real number, never Python's integer-shaped boolean."""
	if isinstance(value, bool) or not isinstance(value, numbers.Real):
		raise ValueError(f"{label} must be a real finite number")
	if not math.isfinite(value):
		raise ValueError(f"{label} must be finite")


def require_nonnegative_finite(value: float, label: str) -> None:
	require_finite(value, label)
	if value < 0:
		raise ValueError(f"{label} must not be negative")


def require_positive_finite(value: float, label: str) -> None:
	require_finite(value, label)
	if value <= 0:
		raise ValueError(f"{label} must be positive")


def require_nonnegative_integer(value: int, label: str) -> None:
	if type(value) is not int:
		raise ValueError(f"{label} must be a true integer")
	if value < 0:
		raise ValueError(f"{label} must not be negative")


def require_positive_integer(value: int, label: str) -> None:
	require_nonnegative_integer(value, label)
	if value == 0:
		raise ValueError(f"{label} must be positive")


def require_boolean(value: bool, label: str) -> None:
	"""Require a real boolean instead of an integer-shaped substitute."""
	if type(value) is not bool:
		raise ValueError(f"{label} must be a bool")


def canonicalize_tuple(instance: object, field_name: str) -> tuple:
	value = getattr(instance, field_name)
	canonical_value = tuple(value)
	if value is not canonical_value:
		object.__setattr__(instance, field_name, canonical_value)
	return canonical_value


def validate_unique(values: object, label: str) -> None:
	items = tuple(values)
	if len(items) != len(set(items)):
		raise ValueError(f"{label} must be unique")


@dataclass(frozen=True)
class LogicalCanvas:
	width: float = LOGICAL_SLIDE_WIDTH
	height: float = LOGICAL_SLIDE_HEIGHT

	def __post_init__(self) -> None:
		require_positive_finite(self.width, "logical canvas width")
		require_positive_finite(self.height, "logical canvas height")


@dataclass(frozen=True)
class LogicalRectangle:
	x: float
	y: float
	width: float
	height: float

	def __post_init__(self) -> None:
		require_finite(self.x, "logical rectangle x")
		require_finite(self.y, "logical rectangle y")
		require_positive_finite(self.width, "logical rectangle width")
		require_positive_finite(self.height, "logical rectangle height")


@dataclass(frozen=True)
class Insets:
	left: float
	top: float
	right: float
	bottom: float

	def __post_init__(self) -> None:
		for label, value in (("left inset", self.left), ("top inset", self.top),
				("right inset", self.right), ("bottom inset", self.bottom)):
			require_nonnegative_finite(value, label)


@dataclass(frozen=True)
class CropInsets:
	left: float
	top: float
	right: float
	bottom: float

	def __post_init__(self) -> None:
		for label, value in (("left crop", self.left), ("top crop", self.top),
				("right crop", self.right), ("bottom crop", self.bottom)):
			require_nonnegative_finite(value, label)
			if value >= 1:
				raise ValueError(f"{label} must be less than one")
		if self.left + self.right >= 1 or self.top + self.bottom >= 1:
			raise ValueError("picture crop must retain positive source width and height")


@dataclass(frozen=True)
class FrameTextProperties:
	padding: Insets
	vertical_alignment: VerticalAlignment
	wrap: TextWrap
	text_direction: TextDirection
	overflow_policy: OverflowPolicy


@dataclass(frozen=True)
class ParagraphProperties:
	horizontal_alignment: HorizontalAlignment
	space_before_pt: float
	space_after_pt: float
	line_spacing_pt: float
	indent_start_pt: float
	indent_end_pt: float
	first_line_indent_pt: float
	tab_stops_pt: tuple[float, ...]
	line_spacing_mode: LineSpacingMode = LineSpacingMode.EXACT

	def __post_init__(self) -> None:
		canonicalize_tuple(self, "tab_stops_pt")
		if not isinstance(self.line_spacing_mode, LineSpacingMode):
			raise ValueError("paragraph line_spacing_mode must be a LineSpacingMode")
		for label, value in (("paragraph space_before_pt", self.space_before_pt),
				("paragraph space_after_pt", self.space_after_pt)):
			require_nonnegative_finite(value, label)
		require_positive_finite(self.line_spacing_pt, "paragraph line_spacing_pt")
		for value in (self.indent_start_pt, self.indent_end_pt, self.first_line_indent_pt):
			require_finite(value, "paragraph indent")
		for tab_stop in self.tab_stops_pt:
			require_nonnegative_finite(tab_stop, "paragraph tab stop")


@dataclass(frozen=True)
class Typography:
	role: StyleRole
	font_family: str
	start_size_pt: float
	selected_size_pt: float
	floor_size_pt: float

	def __post_init__(self) -> None:
		require_nonempty(self.font_family, "typography font family")
		for value in (self.floor_size_pt, self.start_size_pt, self.selected_size_pt):
			require_positive_finite(value, "typography point size")
		if not self.floor_size_pt <= self.selected_size_pt <= self.start_size_pt:
			raise ValueError("typography selected_size_pt must remain within its point bounds")


@dataclass(frozen=True)
class ObjectAccessibility:
	name: str | None = None
	description: str | None = None
	decorative: bool = False

	def __post_init__(self) -> None:
		require_boolean(self.decorative, "accessibility decorative")
		if self.name is not None:
			require_nonempty(self.name, "accessibility name")
		if self.description is not None:
			require_nonempty(self.description, "accessibility description")
		if not self.decorative and (self.name is None or self.description is None):
			raise ValueError("nondecorative objects require accessibility name and description")
		if self.decorative and (self.name is not None or self.description is not None):
			raise ValueError("decorative objects cannot carry accessibility text")


@dataclass(frozen=True)
class PlaceholderProperties:
	style_role: StyleRole
	frame_text: FrameTextProperties | None = None


def validate_placeholder_role(kind: PlaceholderKind, role: PresentationRole) -> None:
	allowed = {
		PlaceholderKind.TITLE: (PresentationRole.TITLE,),
		PlaceholderKind.SUBTITLE: (PresentationRole.SUBTITLE,),
		PlaceholderKind.OUTLINE: (PresentationRole.OUTLINE,),
		PlaceholderKind.OBJECT: (PresentationRole.CONTENT, PresentationRole.GRAPHIC,
			PresentationRole.OBJECT, PresentationRole.COMPONENT),
		PlaceholderKind.NONE: tuple(PresentationRole),
	}
	if role not in allowed[kind]:
		raise ValueError(f"{kind.value} placeholder kind is incompatible with {role.value} role")


@dataclass(frozen=True)
class PlaceholderTopologyMember:
	member_id: str
	placeholder_kind: PlaceholderKind
	role: PresentationRole
	rectangle: LogicalRectangle
	properties: PlaceholderProperties

	def __post_init__(self) -> None:
		require_nonempty(self.member_id, "presentation layout member identity")
		validate_placeholder_role(self.placeholder_kind, self.role)


@dataclass(frozen=True)
class PlaceholderTopology:
	declared_layout_id: str
	members: tuple[PlaceholderTopologyMember, ...]

	def __post_init__(self) -> None:
		canonicalize_tuple(self, "members")
		require_nonempty(self.declared_layout_id, "declared presentation layout identity")
		validate_unique((member.member_id for member in self.members), "presentation layout member identities")

	def key_for_canvas(self, canvas: LogicalCanvas) -> "PresentationPageLayoutKey":
		return PresentationPageLayoutKey(self.declared_layout_id, canvas, self.members)


@dataclass(frozen=True)
class PresentationPageLayoutKey:
	declared_layout_id: str
	canvas: LogicalCanvas
	members: tuple[PlaceholderTopologyMember, ...]

	def __post_init__(self) -> None:
		canonicalize_tuple(self, "members")
		require_nonempty(self.declared_layout_id, "declared presentation layout identity")
		validate_unique((member.member_id for member in self.members), "presentation layout member identities")


@dataclass(frozen=True)
class LayoutContract:
	"""Declarative source vocabulary and physical slot topology for one layout."""
	name: str
	slot_names: tuple[str, ...]
	allows_root_body: bool
	allows_title: bool
	allows_subtitle: bool
	vertical_title: bool = False
	vertical_slots: tuple[str, ...] = ()
	topology_matchable: bool = False
	topology_slots: tuple[tuple[float, float, float, float, float, float], ...] = ()
	continuation_policy: ContinuationPolicy = ContinuationPolicy.FORBID

	def __post_init__(self) -> None:
		canonicalize_tuple(self, "slot_names")
		canonicalize_tuple(self, "vertical_slots")
		canonicalize_tuple(self, "topology_slots")
		require_nonempty(self.name, "layout contract name")
		validate_unique(self.slot_names, "layout contract slots")
		validate_unique(self.vertical_slots, "layout contract vertical slots")
		if any(slot not in self.slot_names for slot in self.vertical_slots):
			raise ValueError("vertical layout slots must be declared layout slots")
		if self.topology_slots and len(self.topology_slots) != len(self.slot_names):
			raise ValueError("layout topology slots must match declared layout slots")
		for bounds in self.topology_slots:
			if len(bounds) != 6:
				raise ValueError("layout topology slots require normalized bounds and center")
			for value in bounds:
				require_finite(value, "layout topology coordinate")

	@property
	def cell_count(self) -> int:
		"""Return the declared named-cell count for source import planning."""
		result = len(self.slot_names)
		return result
