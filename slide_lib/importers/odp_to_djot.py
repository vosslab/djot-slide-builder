"""Convert an imported ODP into supported Djot slide source."""

# Standard Library
import dataclasses
import json
import os
import pathlib
import re
import shutil
import stat
import tempfile

# local repo modules
import slide_lib.djot_lint as djot_lint
import slide_lib.djot_parser
import slide_lib.importers.djot_emitter as djot_emitter
import slide_lib.importers.geometry as geometry
import slide_lib.importers.odp_reader as odp_reader
import slide_lib.importers.slide_plan as slide_plan
import slide_lib.importers.source_model as source_model


ASSET_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
IMPORT_ASSET_SUFFIXES = odp_reader.SUPPORTED_IMAGE_SUFFIXES


@dataclasses.dataclass(frozen=True)
class ConversionSummary:
	"""User-facing counts for one direct native ODP conversion."""

	visible_slides: int
	editable_slides: int
	hidden_slides: int
	extracted_images: int
	review_slides: int
	output_path: pathlib.Path
	report_path: pathlib.Path


#============================================
def plan_imported_slide(
		text_regions: tuple[slide_plan.SourceTextRegion, ...],
		visual_regions: tuple[slide_plan.SourceImageRegion, ...],
		images: tuple[source_model.ImageAsset, ...], slide_width: float,
		slide_height: float,
) -> slide_plan.SlidePlan:
	"""Bind staged image assets to source geometry before semantic planning."""
	picture_sources: dict[geometry.NormalizedBounds, list[slide_plan.SourceImageRegion]] = {}
	for region in visual_regions:
		if region.source_kind == "picture":
			picture_sources.setdefault(region.bounds, []).append(region)
	extracted_images: list[slide_plan.SourceImageRegion] = []
	for image in images:
		bounds = geometry.normalized_bounds(
			image.left, image.top, image.width, image.height, slide_width, slide_height,
		)
		sources = picture_sources.get(bounds, [])
		source = sources.pop(0) if sources else None
		extracted_images.append(slide_plan.SourceImageRegion(
			image.asset_path, bounds, "picture", 0 if source is None else source.source_ordinal,
			z_order=() if source is None else source.z_order,
		))
	known_bounds = {image.bounds for image in extracted_images}
	image_regions = tuple(extracted_images) + tuple(
		image for image in visual_regions if image.bounds not in known_bounds
	)
	return slide_plan.plan_slide(text_regions, image_regions)


#============================================
def plan_slides(presentation: odp_reader.ImportedPresentation) -> list[djot_emitter.PlannedSlide]:
	"""Plan direct raw ODP facts through the existing geometry planner."""
	planned_slides: list[djot_emitter.PlannedSlide] = []
	visible_page_index = 0
	for source_slide in presentation.slides:
		if source_slide.data.hidden:
			planned_slides.append(djot_emitter.PlannedSlide(source_slide.data, None))
			continue
		visible_page_index += 1
		text_regions = slide_plan.text_regions(
			source_slide.positioned_text, source_slide.page_width, source_slide.page_height,
		)
		visual_regions = slide_plan.visual_regions(
			source_slide.positioned_visual, source_slide.page_width, source_slide.page_height,
		)
		plan = plan_imported_slide(
			text_regions, visual_regions, source_slide.data.images,
			source_slide.page_width, source_slide.page_height,
		)
		planned_slides.append(djot_emitter.PlannedSlide(
			source_slide.data, plan, text_regions, visual_regions, visible_page_index,
		))
	return planned_slides


#============================================
def require_new_destination(output_path: pathlib.Path) -> pathlib.Path:
	"""Return a normal local Djot destination that has no published output yet."""
	# ASVS 2.2.1 and 5.3.2: allow only Djot and protect the caller-selected local output.
	output_path = output_path.absolute()
	if output_path.suffix.lower() != ".djot":
		raise ValueError("output must use the .djot extension")
	if output_path.exists() or output_path.is_symlink():
		raise FileExistsError("output Djot source already exists; import will not overwrite it")
	asset_path = output_path.parent / "assets" / output_path.stem
	if asset_path.exists() or asset_path.is_symlink():
		raise FileExistsError("output asset directory already exists")
	return output_path


#============================================
def media_references(staging_djot: pathlib.Path, deck_stem: str) -> set[str]:
	"""Return validated direct-child media names from generated Djot."""
	deck = slide_lib.djot_parser.parse_deck(staging_djot)
	expected_parent = pathlib.PurePosixPath("assets") / deck_stem
	references: set[str] = set()
	for slide in deck.slides:
		images = list(djot_lint.images_in_blocks(slide.blocks))
		for cell in slide.cells:
			images.extend(djot_lint.images_in_blocks(cell.blocks))
		for image in images:
			path = pathlib.PurePosixPath(image.source)
			if path.parent != expected_parent or len(path.parts) != 3:
				raise ValueError("generated Djot image must use its direct local asset namespace")
			if not ASSET_NAME.fullmatch(path.name) or path.suffix.lower() not in IMPORT_ASSET_SUFFIXES:
				raise ValueError("generated Djot image has an unsafe local asset name")
			references.add(path.name)
	return references


#============================================
def prune_staged_media(staging_djot: pathlib.Path, staging_assets: pathlib.Path,
		deck_stem: str) -> int:
	"""Keep only parsed-Djot-reachable regular media in private staging assets."""
	references = media_references(staging_djot, deck_stem)
	media = {candidate.name: candidate for candidate in staging_assets.iterdir()}
	for name, candidate in media.items():
		metadata = candidate.lstat()
		if not stat.S_ISREG(metadata.st_mode) or not ASSET_NAME.fullmatch(name) or \
				candidate.suffix.lower() not in IMPORT_ASSET_SUFFIXES:
			raise ValueError("staged assets must contain safe regular media files")
	if missing := references - media.keys():
		raise ValueError(f"generated Djot references missing staged media: {sorted(missing)[0]}")
	for name, candidate in media.items():
		if name not in references:
			candidate.unlink()
	return len(references)


#============================================
def validate_staged_djot(staging_djot: pathlib.Path) -> None:
	"""Parse, lay out, and resolve staged assets before publication."""
	problems, _slides, _images = djot_lint.lint_source(staging_djot)
	if problems:
		problem = problems[0]
		raise ValueError(
			f"generated Djot staging validation failed: {problem.path}:{problem.line}: {problem.message}"
		)


#============================================
def publish_conversion(staging_djot: pathlib.Path, staging_assets: pathlib.Path,
		output_path: pathlib.Path) -> None:
	"""Publish assets first, then use the Djot file as the commit marker."""
	# ASVS 2.3.3: roll back this import's assets if its final Djot commit marker fails.
	require_new_destination(output_path)
	assets_parent = output_path.parent / "assets"
	assets_parent.mkdir(exist_ok=True)
	final_assets = assets_parent / output_path.stem
	created_assets = False
	try:
		staging_assets.rename(final_assets)
		created_assets = True
		os.link(staging_djot, output_path)
	except BaseException:
		if created_assets:
			shutil.rmtree(final_assets)
		raise


#============================================
def direct_record(record: dict[str, object], source_slide: odp_reader.ReadSlide) -> dict[str, object]:
	"""Add ODP-only immutable source evidence to one normal import report record."""
	evidence = source_slide.data.page_evidence
	if evidence is None:
		raise RuntimeError("direct ODP reader omitted required source page evidence")
	record["source_page_evidence"] = dataclasses.asdict(evidence)
	record["source_geometry"] = [dataclasses.asdict(item) for item in source_slide.raw_geometry]
	return record


#============================================
def convert_odp(input_path: pathlib.Path, output_path: pathlib.Path) -> ConversionSummary:
	"""Convert one bounded native ODP into editable Djot without conversion."""
	output_path = require_new_destination(output_path)
	with tempfile.TemporaryDirectory(prefix=".odp_to_djot_", dir=output_path.parent) as name:
		staging_root = pathlib.Path(name)
		staging_assets = staging_root / "assets" / output_path.stem
		staging_assets.mkdir(parents=True)
		djot_root = pathlib.PurePosixPath("assets") / output_path.stem
		presentation = odp_reader.read_presentation(input_path, staging_assets, djot_root)
		if not presentation.slides:
			raise ValueError("ODP contains no presentation slides")
		slides = plan_slides(presentation)
		visible_slides = [slide for slide in slides if not slide.data.hidden]
		if not visible_slides:
			raise ValueError("ODP contains no visible presentation slides")
		djot, records = djot_emitter.render_planned_djot(slides)
		visible_source_slides = [slide for slide in presentation.slides if not slide.data.hidden]
		for record, source_slide in zip(records, visible_source_slides, strict=True):
			direct_record(record, source_slide)
		staging_djot = staging_root / output_path.name
		staging_djot.write_text(djot, encoding="utf-8")
		published_media_count = prune_staged_media(staging_djot, staging_assets, output_path.stem)
		report = {
			"source": input_path.name,
			"slide_count": len(slides),
			"visible_slides": len(visible_slides),
			"hidden_slides": [slide.data.source_index for slide in slides if slide.data.hidden],
			"unique_media_assets": published_media_count,
			"slides": records,
		}
		report_path = staging_assets / "import_report.json"
		report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
		validate_staged_djot(staging_djot)
		publish_conversion(staging_djot, staging_assets, output_path)
		return ConversionSummary(
			len(visible_slides), len(visible_slides), len(slides) - len(visible_slides),
			published_media_count, sum(bool(record["review_reasons"]) for record in records),
			output_path, output_path.parent / "assets" / output_path.stem / "import_report.json",
		)


#============================================
def run_import(input_file: pathlib.Path, output_file: pathlib.Path | None = None) -> None:
	"""Run one ODP-to-Djot conversion."""
	output_path = input_file.with_suffix(".djot") if output_file is None else output_file
	summary = convert_odp(input_file, output_path)
	print(
		f"Converted {summary.visible_slides} visible slides: "
		f"{summary.editable_slides} editable, {summary.review_slides} layout review, "
		f"{summary.hidden_slides} hidden, {summary.extracted_images} content images"
	)
	print(f"Djot: {summary.output_path}")
	print(f"Import report: {summary.report_path}")
