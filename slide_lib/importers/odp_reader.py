"""Coordinate validated ODP package admission and page extraction."""

# Standard Library
import dataclasses
import pathlib
import zipfile

# PIP3 modules
# local repo modules
import slide_lib.importers.odp_geometry as odp_geometry
import slide_lib.importers.odp_page_objects as odp_page_objects
import slide_lib.odf_package
import slide_lib.importers.odf_styles as odf_styles
import slide_lib.importers.odp_media as odp_media
import slide_lib.importers.odp_reveals as odp_reveals
import slide_lib.importers.odp_visibility as odp_visibility
import slide_lib.importers.source_model as source_model


ODP_MIMETYPE = "application/vnd.oasis.opendocument.presentation"
MAX_PRESENTATION_PAGES = 1_000


@dataclasses.dataclass(frozen=True)
class ImportedPresentation:
	"""The bounded direct-reader result for one native ODP package."""

	slides: tuple[odp_page_objects.ReadSlide, ...]


#============================================
def validate_odp(input_path: pathlib.Path) -> list[zipfile.ZipInfo]:
	"""Validate ODP archive, XML, manifest, and consumed local references."""
	return slide_lib.odf_package.validate_package(
		input_path, ".odp", ODP_MIMETYPE, slide_lib.odf_package.REQUIRED_ODP_MEMBERS,
	)


#============================================
def read_slides(input_path: pathlib.Path) -> list[odp_page_objects.ImportedSlide]:
	"""Read imported slide order and visibility from ODP XML."""
	package = slide_lib.odf_package.admit_package(
		input_path, ".odp", ODP_MIMETYPE, slide_lib.odf_package.REQUIRED_ODP_MEMBERS,
	)
	root = package.content_root
	definitions = odp_visibility.style_definitions_from_root(package.styles_root)
	definitions.update(odp_visibility.style_definitions_from_root(root))
	pages = root.findall(".//draw:page", odp_geometry.NS)
	if len(pages) > MAX_PRESENTATION_PAGES:
		raise ValueError("ODF presentation page limit exceeded")
	slides: list[odp_page_objects.ImportedSlide] = []
	for source_index, page in enumerate(pages, start=1):
		slide_name = page.get(odp_geometry.qname("draw", "name"), f"slide_{source_index:03d}")
		slides.append(odp_page_objects.ImportedSlide(
			source_index, slide_name, odp_visibility.page_is_hidden(page, definitions),
		))
	return slides


#============================================
def read_presentation(input_path: pathlib.Path, assets_dir: pathlib.Path,
		djot_root: pathlib.PurePosixPath) -> ImportedPresentation:
	"""Read validated native ODP pages directly into raw semantic facts."""
	admitted = slide_lib.odf_package.admit_package(
		input_path, ".odp", ODP_MIMETYPE, slide_lib.odf_package.REQUIRED_ODP_MEMBERS,
	)
	archive = zipfile.ZipFile(input_path)
	try:
		member_names = admitted.member_names
		content_root = admitted.content_root
		styles_root = admitted.styles_root
		roots = (styles_root, content_root)
		definitions = odf_styles.definitions(roots)
		visibility = odp_visibility.style_definitions_from_root(styles_root)
		visibility.update(odp_visibility.style_definitions_from_root(content_root))
		style_layouts = odp_geometry.page_style_layouts(roots)
		master_layouts = odp_geometry.master_page_layouts(roots)
		layout_dimensions = odp_geometry.read_page_layout_dimensions(roots)
		declared_roles = odp_geometry.read_declared_placeholder_roles(roots)
		known_images: dict[str, str] = {}
		media_budget = odp_media.MediaBudget()
		read_slides_result: list[odp_page_objects.ReadSlide] = []
		pages = content_root.findall(".//draw:page", odp_geometry.NS)
		if len(pages) > MAX_PRESENTATION_PAGES:
			raise ValueError("ODF presentation page limit exceeded")
		for source_index, page in enumerate(pages, start=1):
			identity = odp_page_objects.ImportedSlide(
				source_index,
				page.get(odp_geometry.qname("draw", "name"), f"slide_{source_index:03d}"),
				odp_visibility.page_is_hidden(page, visibility),
			)
			page_width, page_height = odp_geometry.page_dimensions(
				page, style_layouts, master_layouts, layout_dimensions,
			)
			layout_identity = page.get(
				odp_geometry.qname("presentation", "presentation-page-layout-name"))
			accumulator = odp_page_objects.read_page_objects(
				page, source_index, page_width, page_height, archive, member_names,
				admitted.manifest_targets, assets_dir, djot_root, known_images, media_budget,
				definitions, odp_reveals.appear_target_ids(page),
			)
			accumulator.positioned_text, animation_reasons = odp_reveals.read_text_reveals(
				page, accumulator.positioned_text, accumulator.positioned_overlays)
			accumulator.review_reasons.extend(animation_reasons)
			for color in odp_page_objects.unrecognized_text_colors(page, definitions):
				accumulator.review_reasons.append(
					f"unrecognized source text color {color} requires review")
			line_count = sum(len(block.lines) for block in accumulator.text_blocks)
			character_count = sum(
				len(odp_page_objects.plain_text(runs)) for block in accumulator.text_blocks
				for _level, runs in block.lines
			)
			if line_count > 10 or character_count > 1200:
				accumulator.review_reasons.append("dense text requires post-conversion polish")
			evidence = source_model.SourcePageEvidence(
				source_index, layout_identity, declared_roles.get(layout_identity, ()),
				tuple(accumulator.populated_roles), tuple(accumulator.populated_text_roles),
				tuple(accumulator.populated_image_roles), tuple(accumulator.populated_table_roles),
				accumulator.meaningful_content_count,
			)
			data = source_model.SlideData(
				source_index, identity.hidden, tuple(accumulator.titles),
				tuple(sorted(accumulator.text_blocks, key=lambda block: (block.top, block.left))),
				tuple(sorted(accumulator.images, key=lambda image: (image.top, image.left))),
				odp_page_objects.page_notes(page, definitions),
				tuple(sorted(set(accumulator.review_reasons))),
				tuple(sorted(accumulator.tables, key=lambda table: (table.top, table.left))), evidence,
			)
			read_slides_result.append(odp_page_objects.ReadSlide(
				identity, data, tuple(accumulator.positioned_text),
				tuple(accumulator.positioned_visual), page_width, page_height,
				tuple(accumulator.raw_geometry), tuple(accumulator.positioned_overlays),
			))
		return ImportedPresentation(tuple(read_slides_result))
	finally:
		archive.close()
