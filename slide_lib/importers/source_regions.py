"""Normalize extracted text and visual regions before slide planning."""

import dataclasses
import math

import slide_lib.importers.geometry as geometry
import slide_lib.importers.source_model as source_model


#============================================
@dataclasses.dataclass(frozen=True)
class SourceTextRegion:
	"""One source text shape, retaining paragraph structure and geometry."""

	paragraphs: tuple[tuple[int, tuple[source_model.TextRun, ...]], ...]
	bounds: geometry.NormalizedBounds
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

	def __post_init__(self) -> None:
		if not self.paragraphs:
			raise ValueError("source text region requires at least one paragraph")
		if not 0.0 <= self.placeholder_confidence <= 1.0:
			raise ValueError("placeholder confidence must be within zero and one")
		if self.source_kind not in {"text", "text-box", "auto-shape", "table"}:
			raise ValueError("source text kind is not supported")
		if not math.isfinite(self.rotation_degrees):
			raise ValueError("source text rotation must be finite")
		rotation = self.rotation_degrees % 360.0
		if rotation > 180.0:
			rotation -= 360.0
		object.__setattr__(self, "rotation_degrees", rotation)


#============================================
@dataclasses.dataclass(frozen=True)
class SourceImageRegion:
	"""One source image and its geometry, before any renderer conversion."""

	asset_reference: str
	bounds: geometry.NormalizedBounds
	source_kind: str = "picture"
	source_ordinal: int = 0
	source_line: geometry.DegenerateConnectorFootprint | None = None
	z_order: tuple[int, ...] = ()


#============================================
def text_regions(
	positioned: tuple[source_model.PositionedText, ...],
	slide_width: int,
	slide_height: int,
) -> tuple[SourceTextRegion, ...]:
	"""Validate and normalize raw positioned text at the planning boundary."""
	# ASVS 2.2.1 and 2.2.2: normalize external geometry at one trusted layer.
	return tuple(SourceTextRegion(
		source.paragraphs,
		geometry.normalized_bounds(
			source.left, source.top, source.width, source.height, slide_width, slide_height,
		),
		source.is_subtitle, source.placeholder_confidence, source.title_identity,
		source.source_kind, source.source_ordinal, source.table_row, source.table_column,
		source.table_row_count, source.table_column_count, source.table_id,
		source.table_has_header, source.table_unsupported_reason, source.rotation_degrees,
		source.has_positive_fill, source.has_positive_line, source.placeholder_role,
		source.z_order,
	) for source in positioned)


#============================================
def visual_regions(
	positioned: tuple[source_model.PositionedVisual, ...],
	slide_width: int,
	slide_height: int,
) -> tuple[SourceImageRegion, ...]:
	"""Validate and normalize raw positioned visuals at the planning boundary."""
	# ASVS 2.2.1 and 2.2.2: reject unusable external geometry before planning.
	result: list[SourceImageRegion] = []
	for source in positioned:
		line = None
		if source.width <= 0 or source.height <= 0:
			if source.source_kind != "connector" or source.stroke_width is None:
				continue
			line = geometry.degenerate_connector_footprint(
				source.left, source.top, source.width, source.height, source.stroke_width,
				slide_width, slide_height,
			)
			if line is None:
				continue
			bounds = line.footprint
		else:
			bounds = geometry.normalized_bounds(
				source.left, source.top, source.width, source.height,
				slide_width, slide_height,
			)
		result.append(SourceImageRegion(source.asset_reference, bounds, source.source_kind,
			source.source_ordinal, line, source.z_order))
	return tuple(result)
