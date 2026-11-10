"""Backend-neutral authored overrides and resolved native table formatting."""

import dataclasses


@dataclasses.dataclass(frozen=True)
class Border:
	"""One edge in points, retaining cascade priority for shared-edge conflicts."""

	width_pt: float
	style: str
	color: str
	priority: int = 0


@dataclasses.dataclass(frozen=True)
class CellOverrides:
	"""Only authored properties; None leaves the preceding cascade value intact."""

	background_color: str | None = None
	text_color: str | None = None
	text_alignment: str | None = None
	vertical_alignment: str | None = None
	bold: bool | None = None
	border_top: Border | None = None
	border_right: Border | None = None
	border_bottom: Border | None = None
	border_left: Border | None = None
	padding_top_pt: float | None = None
	padding_right_pt: float | None = None
	padding_bottom_pt: float | None = None
	padding_left_pt: float | None = None
	font_size_pt: float | None = None


@dataclasses.dataclass(frozen=True)
class CellFormatting:
	"""Complete measurement/export facts; colors are six RGB hex digits without #."""

	background_color: str
	text_color: str
	text_alignment: str
	vertical_alignment: str
	bold: bool
	border_top: Border
	border_right: Border
	border_bottom: Border
	border_left: Border
	padding_top_pt: float
	padding_right_pt: float
	padding_bottom_pt: float
	padding_left_pt: float
	font_size_pt: float | None = None
