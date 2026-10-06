"""Compare source artwork with its compiled displayed share of a slide."""

import hashlib
import io
import math
import pathlib
import zipfile

import PIL.Image
import PIL.ImageChops

import slide_lib.djot_parser
import slide_lib.importers.odp_reader as reader
import slide_lib.layout_content
import slide_lib.layout_engine
import slide_lib.odf_package
import slide_lib.presentation_theme


def area_change(source: float, target: float, threshold: float = 30) -> dict[str, object]:
	"""Report slide fractions, percentage-point change, and relative area loss."""
	if not all(math.isfinite(value) for value in (source, target, threshold)) or \
			source <= 0 or target < 0 or not 0 <= threshold <= 100:
		raise ValueError("invalid area or loss threshold; threshold must be within 0..100")
	loss = 100 * (1 - target / source)
	return {"source_slide_percent": round(100 * source, 2),
		"target_slide_percent": round(100 * target, 2),
		"percentage_point_change": round(100 * (target - source), 2),
		"relative_loss_percent": round(loss, 2), "warning": loss >= threshold}


def margin_fraction(payload: bytes) -> float | None:
	"""Suggest exact white/transparent border trimming without editing artwork."""
	try:
		with PIL.Image.open(io.BytesIO(payload)) as image:
			rgba = image.convert("RGBA")
			white = PIL.Image.new("RGBA", rgba.size, "white")
			white.alpha_composite(rgba)
			box = PIL.ImageChops.difference(white.convert("RGB"),
				PIL.Image.new("RGB", rgba.size, "white")).getbbox()
			if box is None:
				return None
			return 1 - (box[2] - box[0]) * (box[3] - box[1]) / (image.width * image.height)
	except (OSError, ValueError):
		return None


def audit(source: pathlib.Path, converted: pathlib.Path,
		threshold: float = 30) -> list[dict[str, object]]:
	"""Match identical artwork per slide, aggregating repeated uses of each asset.

	Edited/composite artwork and transformed frames require manual correspondence review.
	The caller must supply matching slide order; count mismatches are rejected.
	"""
	if not 0 <= threshold <= 100:
		raise ValueError("image loss threshold must be within 0..100")
	package = slide_lib.odf_package.admit_package(source, ".odp",
		slide_lib.odf_package.ODP_MIMETYPE, slide_lib.odf_package.REQUIRED_ODP_MEMBERS)
	roots = (package.styles_root, package.content_root)
	pages = package.content_root.findall(".//draw:page", reader.NS)
	style_layouts = reader.page_style_layouts(roots)
	masters = reader.master_page_layouts(roots)
	dimensions = reader.read_page_layout_dimensions(roots)
	deck = slide_lib.djot_parser.parse_deck(converted)
	plan = slide_lib.layout_engine.compile_layout_deck(deck,
		slide_lib.presentation_theme.default_theme(deck.color_theme)).plan
	if len(pages) != len(plan.slides):
		raise ValueError("image audit requires matching source/output slide order and count")
	results: list[dict[str, object]] = []
	with zipfile.ZipFile(source) as archive:
		for index, (page, output) in enumerate(zip(pages, plan.slides, strict=True), 1):
			width, height = reader.page_dimensions(page, style_layouts, masters, dimensions)
			targets: dict[str, float] = {}
			for item in output.objects:
				if isinstance(item.content, slide_lib.layout_content.PictureContent):
					path = pathlib.Path(item.content.source_path)
					if not path.is_absolute():
						path = converted.parent / path
					digest = hashlib.sha256(path.read_bytes()).hexdigest()
					r = item.content.placement.displayed_rectangle
					targets[digest] = targets.get(digest, 0) + r.width * r.height / (
						plan.canvas.width * plan.canvas.height)
			sources: dict[str, tuple[str, float, float | None]] = {}
			for frame in page.findall(".//draw:frame", reader.NS):
				image = frame.find("draw:image", reader.NS)
				if image is None:
					continue
				ref = image.get(reader.qname("xlink", "href"), "")
				member = slide_lib.odf_package.package_reference_target("content.xml", ref)
				if member not in package.member_names:
					results.append({"slide": index, "asset": ref,
						"status": "manual review: missing or external artwork"})
					continue
				if any(node.get(reader.qname("draw", "transform")) is not None
						for node in (frame, *frame.iterancestors())):
					results.append({"slide": index, "asset": ref,
						"status": "manual review: transformed source frame"})
					continue
				payload = archive.read(member)
				digest = hashlib.sha256(payload).hexdigest()
				w = reader.parse_length(frame.get(reader.qname("svg", "width")),
					field_name="image width", allow_negative=False)
				h = reader.parse_length(frame.get(reader.qname("svg", "height")),
					field_name="image height", allow_negative=False)
				if w * h <= 0:
					continue
				old = sources.get(digest, (ref, 0, margin_fraction(payload)))
				sources[digest] = (ref, old[1] + w * h / (width * height), old[2])
			for digest, (ref, area, margin) in sources.items():
				record: dict[str, object] = {"slide": index, "asset": ref,
					"empty_margin_fraction": margin}
				if digest in targets:
					record.update(area_change(area, targets[digest], threshold))
					record["status"] = "matched"
				else:
					record.update({"status": "manual review: artwork replaced or omitted",
						"source_slide_percent": round(100 * area, 2)})
				results.append(record)
	return results
