"""Normalize and emit the bounded image-annotation vocabulary."""

# Standard Library
import dataclasses

# Local modules
import slide_lib.importers.slide_plan as slide_plan
import slide_lib.importers.source_model as source_model


@dataclasses.dataclass(frozen=True)
class SourceOverlay:
	"""One normalized native annotation awaiting an owning image."""

	kind: str
	first_x: float
	first_y: float
	second_x: float
	second_y: float
	color: str
	source_ordinal: int
	z_order: tuple[int, ...] = ()
	reveal: bool = False

	def __post_init__(self) -> None:
		if self.kind not in {"arrow", "outline"}:
			raise ValueError("source overlay kind is not supported")
		if not all(0.0 <= value <= 1.0 for value in (
				self.first_x, self.first_y, self.second_x, self.second_y)):
			raise ValueError("source overlay coordinates must remain within the slide")


#============================================
def normalized_overlays(positioned: tuple[source_model.PositionedOverlay, ...],
		slide_width: float, slide_height: float) -> tuple[SourceOverlay, ...]:
	"""Normalize supported native annotations into slide-relative coordinates."""
	return tuple(SourceOverlay(source.kind,
		source.first_x / slide_width, source.first_y / slide_height,
		source.second_x / slide_width, source.second_y / slide_height,
		source.color, source.source_ordinal, source.z_order, source.reveal)
		for source in positioned)


def contains_point(image: slide_plan.SourceImageRegion, x: float, y: float) -> bool:
	"""Return whether one normalized point lies within a source image."""
	return image.bounds.left <= x <= image.bounds.right and \
		image.bounds.top <= y <= image.bounds.bottom


def compact_percentage(value: float) -> str:
	"""Render a stable, concise percentage coordinate for authored Djot."""
	return f"{value:.2f}".rstrip("0").rstrip(".")


def overlay_lines(overlay: SourceOverlay,
		image: slide_plan.SourceImageRegion) -> tuple[str, ...]:
	"""Project one slide-relative annotation into its image coordinate space."""
	first_x = (overlay.first_x - image.bounds.left) / image.bounds.width * 100.0
	first_y = (overlay.first_y - image.bounds.top) / image.bounds.height * 100.0
	second_x = (overlay.second_x - image.bounds.left) / image.bounds.width * 100.0
	second_y = (overlay.second_y - image.bounds.top) / image.bounds.height * 100.0
	if overlay.kind == "arrow":
		values = (first_x, first_y, second_x, second_y)
	else:
		values = (min(first_x, second_x), min(first_y, second_y),
			abs(second_x - first_x), abs(second_y - first_y))
	directive = f"{overlay.kind}: {' '.join(compact_percentage(value) for value in values)}"
	prefix = ("=> appear",) if overlay.reveal else ()
	return (*prefix, f"{{color={overlay.color}}}", directive)


def render_big_image(overlays: tuple[SourceOverlay, ...],
		image: slide_plan.SourceImageRegion, image_line: str,
		caption_lines: list[str], review_reasons: tuple[str, ...]) \
		-> tuple[list[str], str, list[str]] | None:
	"""Emit one proven image-owned annotation composition as native Djot."""
	if any(not all((
		contains_point(image, overlay.first_x, overlay.first_y),
		contains_point(image, overlay.second_x, overlay.second_y),
		overlay.z_order > image.z_order,
	)) for overlay in overlays):
		return None
	lines = ["=== layout: big-image", "", "@image", "", image_line]
	for overlay in sorted(overlays, key=lambda item: item.z_order):
		lines.extend(("", *overlay_lines(overlay, image)))
	lines.extend(("", "@caption", ""))
	for index, line in enumerate(caption_lines):
		if index:
			lines.append("")
		lines.append(line)
	return lines, "big-image", list(review_reasons)
