"""Measure image assets and mixed text/image regions for layout compilation."""

import dataclasses
import itertools

import PIL.Image

import slide_lib.djot_sources
import slide_lib.layout_measurement
import slide_lib.layout_primitives
import slide_lib.native_model
import slide_lib.presentation_theme
import slide_lib.svg_images


@dataclasses.dataclass(frozen=True)
class MixedFlowAllocation:
	"""Retain the exact proportional image/text heights for one final mixed-flow frame."""

	size_pt: float
	blocks: tuple[slide_lib.native_model.Block, ...]
	heights: tuple[float, ...]
	score: float


def image_size(deck: slide_lib.native_model.Deck,
		image: slide_lib.native_model.Image) -> tuple[float, float]:
	"""Return the intrinsic dimensions of one ordinary image."""
	path = slide_lib.djot_sources.image_path(deck, image)
	if not path.is_relative_to(deck.repo_root) or not path.is_file():
		raise ValueError(f"{image.location.path}:{image.location.line}: component image is missing or outside the repository: {image.source}")
	if path.suffix.lower() == ".svg":
		return slide_lib.svg_images.dimensions(path)
	with PIL.Image.open(path) as opened:
		return opened.size


def _image_width_heights(natural: tuple[float, ...], maximum: tuple[float, ...],
		available: float, floor_ratio: float) -> tuple[float, ...] | None:
	"""Maximize summed displayed widths at vertices of the bounded height constraint."""
	minimum = tuple(height * floor_ratio for height in maximum)
	if available < sum(minimum) - 1e-9:
		return None
	if available >= sum(maximum):
		return maximum
	best: tuple[float, ...] | None = None
	best_score = -1.0
	for free in range(len(natural)):
		others = tuple(index for index in range(len(natural)) if index != free)
		for bounds in itertools.product((False, True), repeat=len(others)):
			heights = list(minimum)
			for index, upper in zip(others, bounds):
				heights[index] = maximum[index] if upper else minimum[index]
			remaining = available - sum(heights[index] for index in others)
			if remaining < minimum[free] - 1e-9 or remaining > maximum[free] + 1e-9:
				continue
			heights[free] = max(minimum[free], min(maximum[free], remaining))
			candidate = tuple(heights)
			score = sum(height / full for height, full in zip(candidate, natural))
			if (score, candidate) > (best_score, best or ()):
				best, best_score = candidate, score
	return best


def mixed_flow_allocation(deck: slide_lib.native_model.Deck,
		text_blocks: tuple[slide_lib.native_model.Block, ...],
		images: tuple[slide_lib.native_model.Image, ...],
		rectangle: slide_lib.layout_primitives.LogicalRectangle, size_pt: float,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession, *, review: bool = False) -> MixedFlowAllocation | None:
	"""Allocate the whole region with a linear size score; retain bounds for review recovery."""
	measure = slide_lib.layout_measurement
	if not review and size_pt < theme.body_floor_size_pt:
		return None
	blocks = tuple(sorted(text_blocks + images, key=lambda block: block.location.line))
	text_heights = {}
	for block in text_blocks:
		if isinstance(block, slide_lib.native_model.Heading):
			height = measure.paragraph_height(block.inlines, size_pt, rectangle.width, theme, bold=True, session=session)
		elif isinstance(block, slide_lib.native_model.Table):
			height = measure.table_height(block, size_pt, rectangle.width, theme, session)
		elif isinstance(block, (slide_lib.native_model.Paragraph, slide_lib.native_model.ListBlock)):
			height = measure.text_height(measure.items_for((block,)), size_pt, rectangle.width, theme, session)
		else:
			raise ValueError(f"{block.location}: unsupported flow content")
		text_heights[id(block)] = height
	natural_image_heights = {id(image): rectangle.width * image_size(deck, image)[1] /
		image_size(deck, image)[0] for image in images}
	available = rectangle.height - measure.point_height(measure.TEXT_FRAME_CLEARANCE_PT, theme) - \
		12 * (len(blocks) - 1) - sum(text_heights.values())
	if available <= 0:
		return None
	natural = tuple(natural_image_heights[id(image)] for image in images)
	maximum = tuple(min(height, rectangle.height - measure.point_height(measure.TEXT_FRAME_CLEARANCE_PT, theme))
		for height in natural)
	floor = slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT if review else theme.body_floor_size_pt
	image_heights = _image_width_heights(natural, maximum, available, floor / theme.ordinary_body_size_pt)
	if image_heights is None:
		return None
	allocated = {id(image): height for image, height in zip(images, image_heights)}
	heights = tuple(allocated[id(block)] if isinstance(block, slide_lib.native_model.Image)
		else text_heights[id(block)] for block in blocks)
	if sum(heights) + 12 * (len(blocks) - 1) + measure.point_height(measure.TEXT_FRAME_CLEARANCE_PT, theme) > rectangle.height + 1e-9:
		return None
	score = len(text_blocks) * measure.point_height(size_pt, theme) + rectangle.width * sum(
		height / full for height, full in zip(image_heights, natural))
	return MixedFlowAllocation(size_pt, blocks, heights, score)
