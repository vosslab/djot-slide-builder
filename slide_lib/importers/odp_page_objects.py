"""Extract page-local ODP content into source facts and review evidence."""

# Standard Library
import dataclasses
import hashlib
import pathlib
import zipfile
import xml.etree.ElementTree

# PIP3 modules
# local repo modules
import slide_lib.importers.odp_geometry as odp_geometry
import slide_lib.odf_package
import slide_lib.importers.odf_styles as odf_styles
import slide_lib.importers.odf_text as odf_text
import slide_lib.importers.odp_metafile as odp_metafile
import slide_lib.importers.odp_media as odp_media
import slide_lib.importers.odp_reveals as odp_reveals
import slide_lib.importers.odp_tables as odp_tables
import slide_lib.importers.source_model as source_model
import slide_lib.presentation_theme


MAX_PAGE_OBJECTS = 1_000
MAX_DRAW_GROUP_DEPTH = 64


@dataclasses.dataclass(frozen=True)
class ImportedSlide:
	"""Imported slide identity and visibility retained from ODP XML."""

	source_index: int
	name: str
	hidden: bool


@dataclasses.dataclass(frozen=True)
class ReadSlide:
	"""One physical ODP page and its planner-ready raw source facts."""

	identity: ImportedSlide
	data: source_model.SlideData
	positioned_text: tuple[source_model.PositionedText, ...]
	positioned_visual: tuple[source_model.PositionedVisual, ...]
	page_width: float
	page_height: float
	raw_geometry: tuple[odp_geometry.RawObjectGeometry, ...]
	positioned_overlays: tuple[source_model.PositionedOverlay, ...] = ()


@dataclasses.dataclass
class PageAccumulator:
	"""Mutable extraction state used only while reading one XML page."""

	titles: list[tuple[source_model.TextRun, ...]]
	text_blocks: list[source_model.TextBlock]
	tables: list[source_model.TableBlock]
	images: list[source_model.ImageAsset]
	positioned_text: list[source_model.PositionedText]
	positioned_visual: list[source_model.PositionedVisual]
	positioned_overlays: list[source_model.PositionedOverlay]
	review_reasons: list[str]
	populated_roles: list[str]
	populated_text_roles: list[str]
	populated_image_roles: list[str]
	populated_table_roles: list[str]
	raw_geometry: list[odp_geometry.RawObjectGeometry]
	meaningful_content_count: int = 0
	next_ordinal: int = 0
	object_count: int = 0


#============================================
def plain_text(runs: tuple[source_model.TextRun, ...]) -> str:
	"""Return visible source characters for density and identity checks."""
	return "".join(run.text for run in runs)


#============================================
def page_notes(page: xml.etree.ElementTree.Element,
		definitions: dict[str, odf_styles.StyleDefinition]) -> tuple[str, ...]:
	"""Read presenter-note paragraphs from one ODP page."""
	notes: list[str] = []
	for notes_element in page.findall("./presentation:notes", odp_geometry.NS):
		for _level, runs in odf_text.text_paragraphs(notes_element, definitions):
			text = plain_text(runs).strip()
			if text:
				notes.append(text)
	return tuple(notes)


#============================================
def unrecognized_text_colors(page: xml.etree.ElementTree.Element,
		definitions: dict[str, odf_styles.StyleDefinition]) -> tuple[str, ...]:
	"""Return explicit nonneutral source colors outside the semantic palette."""
	text_tags = {odp_geometry.qname("text", name) for name in ("a", "h", "p", "span")}
	text_tags.update(odp_geometry.qname("draw", name) for name in ("frame", "rect", "custom-shape"))
	colors = {
		color for element in page.iter() if element.tag in text_tags
		if (color := odf_styles.attribute(element, definitions, odp_geometry.qname("fo", "color")))
		if slide_lib.presentation_theme.source_text_color_requires_review(color)
	}
	return tuple(sorted(colors))


#============================================
def append_geometry(accumulator: PageAccumulator, source_ordinal: int,
		source_kind: str, geometry: tuple[float, float, float, float],
		z_order: tuple[int, ...]) -> None:
	"""Retain the original rectangle for the direct-import audit report."""
	left, top, width, height = geometry
	accumulator.raw_geometry.append(odp_geometry.RawObjectGeometry(
		source_ordinal, source_kind, left, top, width, height, z_order,
	))


#============================================
def add_picture(
		image: xml.etree.ElementTree.Element,
		geometry: tuple[float, float, float, float], source_ordinal: int,
		archive: zipfile.ZipFile, member_names: frozenset[str], manifest_targets: frozenset[str],
		assets_dir: pathlib.Path, djot_root: pathlib.PurePosixPath,
		known_images: dict[str, str], accumulator: PageAccumulator,
		media_budget: odp_media.MediaBudget, z_order: tuple[int, ...],
) -> bool:
	"""Stage one validated package-local image, retaining external evidence."""
	reference = image.get(odp_geometry.qname("xlink", "href"))
	if not reference:
		accumulator.review_reasons.append("source image is missing its package reference")
		return True
	target = slide_lib.odf_package.package_reference_target("content.xml", reference)
	if target is None:
		accumulator.review_reasons.append("external source image reference requires review")
		return True
	if target not in member_names:
		raise ValueError("ODF image reference points to a missing package member")
	if target not in manifest_targets:
		raise ValueError("ODF image reference misses its manifest target")
	blob = archive.read(target)
	suffix = odp_media.image_suffix(target)
	if not suffix and blob.startswith(b"VCLMTF"):
		suffix = ".svm"
	is_metafile = suffix in odp_metafile.METAFILE_SUFFIXES
	try:
		blob, suffix = odp_metafile.component_image(blob, suffix, geometry)
		odp_media.validate_image_blob(blob, suffix, media_budget)
	except (OSError, ValueError) as error:
		accumulator.review_reasons.append(f"source image requires review: {error}")
		return True
	if is_metafile:
		root = slide_lib.odf_package.parse_xml(blob, "converted metafile")
		if not any("".join(node.itertext()).strip()
				for node in root.iter("{http://www.w3.org/2000/svg}text")):
			accumulator.review_reasons.append(
				"metafile SVG has no live text; review bitmap content or glyph outlines")
	digest = hashlib.sha256(blob).hexdigest()
	asset_name = known_images.get(digest)
	if asset_name is None:
		asset_name = f"image_{len(known_images) + 1:03d}{suffix}"
		(assets_dir / asset_name).write_bytes(blob)
		known_images[digest] = asset_name
	left, top, width, height = geometry
	asset_path = (djot_root / asset_name).as_posix()
	accumulator.images.append(source_model.ImageAsset(
		left, top, width, height, asset_path, f"Slide image {len(known_images)}",
	))
	accumulator.positioned_visual.append(source_model.PositionedVisual(
		asset_path, left, top, width, height, "picture", source_ordinal, z_order=z_order,
	))
	return True


#============================================
def add_text(
		text_box: xml.etree.ElementTree.Element,
		geometry: tuple[float, float, float, float], source_ordinal: int,
		role: str | None, element: xml.etree.ElementTree.Element,
		accumulator: PageAccumulator, z_order: tuple[int, ...],
		definitions: dict[str, odf_styles.StyleDefinition],
) -> bool:
	"""Add text runs and positioned facts from one visible ODP text object."""
	context = odf_text.text_style(element, definitions, odf_text.TextStyle())
	paragraphs = odf_text.text_paragraphs(text_box, definitions, context)
	if not paragraphs:
		return False
	left, top, width, height = geometry
	is_subtitle = False
	title_identity = role == "title"
	source_kind = "text" if role else "text-box"
	has_fill, has_line = odp_geometry.style_evidence(element, definitions)
	positioned = source_model.PositionedText(
		paragraphs, left, top, width, height, is_subtitle, 1.0 if role else 0.0,
		title_identity, source_kind, source_ordinal,
		rotation_degrees=odp_geometry.rotation_degrees(element), has_positive_fill=has_fill,
		has_positive_line=has_line, placeholder_role=role, z_order=z_order,
	)
	accumulator.positioned_text.append(positioned)
	if title_identity:
		accumulator.titles.extend(runs for _level, runs in paragraphs)
	else:
		accumulator.text_blocks.append(source_model.TextBlock(left, top, paragraphs, is_subtitle))
	return True


#============================================
def add_table(
		table: xml.etree.ElementTree.Element,
		geometry: tuple[float, float, float, float], source_ordinal: int,
		role: str | None, element: xml.etree.ElementTree.Element,
		accumulator: PageAccumulator, z_order: tuple[int, ...],
		definitions: dict[str, odf_styles.StyleDefinition],
) -> bool:
	"""Add a real ODF table and its planning evidence without flattening cells."""
	left, top, width, height = geometry
	block, cells = odp_tables.read_table(table, left, top, source_ordinal, definitions)
	accumulator.tables.append(block)
	has_fill, has_line = odp_geometry.style_evidence(element, definitions)
	row_count = len(block.rows) + (1 if block.headers else 0)
	column_count = len(block.headers or block.rows[0])
	for row_index, column_index, runs in cells:
		accumulator.positioned_text.append(source_model.PositionedText(
			((0, runs),), left, top, width, height, False, 1.0 if role else 0.0,
			False, "table", source_ordinal * 10_000 + row_index * column_count + column_index,
			row_index, column_index, row_count, column_count, source_ordinal,
			bool(block.headers), block.unsupported_reason, odp_geometry.rotation_degrees(element),
			has_fill, has_line, role, z_order,
		))
	return True


#============================================
def read_frame(
		frame: xml.etree.ElementTree.Element, source_index: int, page_width: float,
		page_height: float, archive: zipfile.ZipFile, member_names: frozenset[str],
		manifest_targets: frozenset[str], assets_dir: pathlib.Path,
		djot_root: pathlib.PurePosixPath, known_images: dict[str, str],
		accumulator: PageAccumulator, media_budget: odp_media.MediaBudget,
		z_order: tuple[int, ...], source_ordinal: int,
		definitions: dict[str, odf_styles.StyleDefinition],
) -> None:
	"""Read one ODP frame into supported facts or an explicit review lane."""
	text_box = frame.find("./draw:text-box", odp_geometry.NS)
	table = frame.find(".//table:table", odp_geometry.NS)
	image = odp_metafile.frame_image(frame)
	geometry = odp_geometry.frame_geometry(frame, source_index)
	if odp_geometry.visible_geometry(geometry, page_width, page_height, source_index):
		accumulator.review_reasons.append("source object crosses physical page bounds")
	role = frame.get(odp_geometry.qname("presentation", "class"))
	contains_table = table is not None and add_table(
		table, geometry, source_ordinal, role, frame, accumulator, z_order, definitions)
	usable_table = contains_table and accumulator.tables[-1].unsupported_reason is None
	contains_text = not usable_table and text_box is not None and add_text(
		text_box, geometry, source_ordinal, role, frame, accumulator, z_order, definitions)
	# A same-frame image is the native table's preview; other frames remain independent.
	contains_image = not usable_table and image is not None and add_picture(
		image, geometry, source_ordinal, archive, member_names, manifest_targets, assets_dir,
		djot_root, known_images, accumulator, media_budget, z_order)
	if contains_text or contains_table or contains_image:
		append_geometry(accumulator, source_ordinal, "frame", geometry, z_order)
		accumulator.meaningful_content_count += 1
		if role:
			accumulator.populated_roles.append(role)
			if contains_text:
				accumulator.populated_text_roles.append(role)
			if contains_image:
				accumulator.populated_image_roles.append(role)
			if contains_table:
				accumulator.populated_table_roles.append(role)
		return
	append_geometry(accumulator, source_ordinal, "vector", geometry, z_order)
	accumulator.review_reasons.append(
		f"unsupported source object draw:{odp_geometry.local_name(frame)} requires reconstruction")


#============================================
def read_page_objects(
		page: xml.etree.ElementTree.Element, source_index: int, page_width: float,
		page_height: float, archive: zipfile.ZipFile, member_names: frozenset[str],
		manifest_targets: frozenset[str], assets_dir: pathlib.Path,
		djot_root: pathlib.PurePosixPath, known_images: dict[str, str],
		media_budget: odp_media.MediaBudget, definitions: dict[str, odf_styles.StyleDefinition],
		appear_targets: frozenset[str],
) -> PageAccumulator:
	"""Extract direct visible page objects in their original nested z-order."""
	accumulator = PageAccumulator([], [], [], [], [], [], [], [], [], [], [], [], [])

	def next_object() -> int:
		accumulator.object_count += 1
		if accumulator.object_count > MAX_PAGE_OBJECTS:
			raise ValueError(f"source slide {source_index}: ODF page object limit exceeded")
		accumulator.next_ordinal += 1
		return accumulator.next_ordinal

	def read_vector(element: xml.etree.ElementTree.Element, z_order: tuple[int, ...]) -> None:
		ordinal = next_object()
		geometry = odp_geometry.vector_geometry(element, source_index)
		if geometry is None:
			accumulator.review_reasons.append(
				f"source slide {source_index}: unsupported draw:{odp_geometry.local_name(element)} has no bounded geometry")
			return
		crosses_bounds = odp_geometry.visible_geometry(geometry, page_width, page_height, source_index)
		if crosses_bounds:
			accumulator.review_reasons.append("source object crosses physical page bounds")
		append_geometry(accumulator, ordinal, "vector", geometry, z_order)
		if any(element.findall(path, odp_geometry.NS) for path in ("./text:p", "./text:h", "./text:list")) and \
				add_text(element, geometry, ordinal, None, element, accumulator, z_order, definitions):
			accumulator.meaningful_content_count += 1
			return
		color = slide_lib.presentation_theme.source_overlay_color_name(
			odf_styles.attribute(element, definitions, odp_geometry.qname("svg", "stroke-color")))
		if not crosses_bounds and element.tag == odp_geometry.qname("draw", "line") and color and \
				odf_styles.attribute(element, definitions, odp_geometry.qname("draw", "marker-end")) not in {None, "none"}:
			first_x, first_y, second_x, second_y = odp_geometry.line_endpoints(element)
			accumulator.positioned_overlays.append(source_model.PositionedOverlay(
				"arrow", first_x, first_y, second_x, second_y, color, ordinal, z_order,
				odp_reveals.element_appears(element, appear_targets)))
			accumulator.meaningful_content_count += 1
			return
		if not crosses_bounds and element.tag == odp_geometry.qname("draw", "rect") and color and \
				odf_styles.attribute(element, definitions, odp_geometry.qname("draw", "fill")) == "none":
			left, top, width, height = geometry
			accumulator.positioned_overlays.append(source_model.PositionedOverlay(
				"outline", left, top, left + width, top + height, color, ordinal, z_order,
				odp_reveals.element_appears(element, appear_targets)))
			accumulator.meaningful_content_count += 1
			return
		accumulator.review_reasons.append(
			f"unsupported source object draw:{odp_geometry.local_name(element)} requires reconstruction")

	known_vectors = {
		odp_geometry.qname("draw", "rect"), odp_geometry.qname("draw", "ellipse"),
		odp_geometry.qname("draw", "line"), odp_geometry.qname("draw", "custom-shape"),
		odp_geometry.qname("draw", "path"), odp_geometry.qname("draw", "connector"),
	}
	stack = [
		(child, (child_index,)) for child_index, child in reversed(list(enumerate(page)))
		if child.tag not in {odp_geometry.qname("presentation", "notes"), odp_geometry.qname("office", "forms")}
	]
	while stack:
		element, z_order = stack.pop()
		if element.tag == odp_geometry.qname("draw", "frame"):
			ordinal = next_object()
			read_frame(element, source_index, page_width, page_height, archive, member_names,
				manifest_targets, assets_dir, djot_root, known_images, accumulator, media_budget,
				z_order, ordinal, definitions)
			continue
		if element.tag == odp_geometry.qname("draw", "g"):
			if len(z_order) >= MAX_DRAW_GROUP_DEPTH:
				raise ValueError(f"source slide {source_index}: ODF draw group depth limit exceeded")
			stack.extend((child, (*z_order, child_index))
				for child_index, child in reversed(list(enumerate(element))))
			continue
		if element.tag in known_vectors:
			read_vector(element, z_order)
			continue
		if element.tag.startswith(f"{{{odp_geometry.NS['draw']}}}"):
			ordinal = next_object()
			accumulator.meaningful_content_count += 1
			accumulator.review_reasons.append(
				f"source slide {source_index}: unsupported meaningful draw:{odp_geometry.local_name(element)} requires review")
			geometry = odp_geometry.vector_geometry(element, source_index)
			if geometry is not None:
				append_geometry(accumulator, ordinal, "unknown", geometry, z_order)
	return accumulator
