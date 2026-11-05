"""Validate and stage the bounded raster facts admitted from an ODP package."""

# Standard Library
import dataclasses
import io
import pathlib

# PIP3 modules
from PIL import Image

# Local Modules
import slide_lib.odf_package
import slide_lib.svg_images


SUPPORTED_IMAGE_SUFFIXES = frozenset({".gif", ".jpg", ".png", ".svg"})
MAX_IMAGE_PIXELS = 100_000_000
MAX_IMAGE_FRAMES = 100
MAX_IMAGE_AGGREGATE_PIXELS = 500_000_000


@dataclasses.dataclass
class MediaBudget:
	"""Bounded decoded media totals for one source presentation."""

	frame_count: int = 0
	pixel_count: int = 0


#============================================
def validate_image_blob(blob: bytes, suffix: str, media_budget: MediaBudget) -> None:
	"""Validate SVG or decode every raster frame before publishing an asset."""
	if len(blob) > slide_lib.odf_package.MAX_MEMBER_BYTES:
		raise ValueError("ODP image exceeds the per-image size limit")
	if suffix == ".svg":
		slide_lib.svg_images.dimensions_blob(blob, "imported SVG")
		return
	# ASVS 5.2.2 and 5.2.6: decode all admitted media before it reaches staging.
	if suffix not in SUPPORTED_IMAGE_SUFFIXES:
		raise ValueError(f"unsupported ODP image type: {suffix}")
	expected_format = {".gif": "GIF", ".jpg": "JPEG", ".png": "PNG"}[suffix]
	with Image.open(io.BytesIO(blob)) as image:
		if image.format != expected_format:
			raise ValueError("ODP image bytes do not match their published extension")
		frame_total = getattr(image, "n_frames", 1)
		if frame_total < 1 or frame_total > MAX_IMAGE_FRAMES:
			raise ValueError("ODP image frame count exceeds the supported limit")
		if media_budget.frame_count + frame_total > MAX_IMAGE_FRAMES:
			raise ValueError("ODP aggregate image frame count exceeds the supported limit")
		image_pixels = 0
		for frame_index in range(frame_total):
			image.seek(frame_index)
			image.load()
			width, height = image.size
			pixels = width * height
			if width < 1 or height < 1 or pixels > MAX_IMAGE_PIXELS:
				raise ValueError("ODP image dimensions exceed the supported limit")
			image_pixels += pixels
		if media_budget.pixel_count + image_pixels > MAX_IMAGE_AGGREGATE_PIXELS:
			raise ValueError("ODP aggregate image pixels exceed the supported limit")
		media_budget.frame_count += frame_total
		media_budget.pixel_count += image_pixels


#============================================
def image_suffix(reference: str) -> str:
	"""Normalize a claimed package suffix for bounded raster validation."""
	suffix = pathlib.PurePosixPath(reference).suffix.lower()
	if suffix == ".jpeg":
		suffix = ".jpg"
	return suffix
