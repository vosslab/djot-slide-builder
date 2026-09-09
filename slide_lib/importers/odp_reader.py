"""Validate and read an imported ODP before Djot emission."""

# Standard Library
import dataclasses
import hashlib
import io
import math
import pathlib
import re
import urllib.parse
import xml.etree.ElementTree
import zipfile

# PIP3 modules
from PIL import Image

# local repo modules
import slide_lib.odf_package
import slide_lib.importers.odp_visibility as odp_visibility
import slide_lib.importers.source_model as source_model


NS = {
	"draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
	"fo": "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0",
	"office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
	"presentation": "urn:oasis:names:tc:opendocument:xmlns:presentation:1.0",
	"style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
	"svg": "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0",
	"table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
	"text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
	"xlink": "http://www.w3.org/1999/xlink",
}
ODP_MIMETYPE = "application/vnd.oasis.opendocument.presentation"
SAFE_LINK_SCHEMES = frozenset({"http", "https", "mailto"})
SUPPORTED_IMAGE_SUFFIXES = frozenset({".gif", ".jpg", ".png"})
MAX_IMAGE_PIXELS = 100_000_000
MAX_IMAGE_FRAMES = 100
MAX_IMAGE_AGGREGATE_PIXELS = 500_000_000
MAX_ODF_LENGTH_POINTS = 100_000.0
MAX_TABLE_CELLS = 2_000
MAX_TABLE_REPEAT = 100
MAX_PRESENTATION_PAGES = 1_000
MAX_PAGE_OBJECTS = 1_000
MAX_DRAW_GROUP_DEPTH = 64
LENGTH_VALUE = re.compile(r"^([+-]?(?:\d+(?:\.\d*)?|\.\d+))(cm|in|mm|pc|pt|px)$")
ROTATION_VALUE = re.compile(r"rotate\s*\(\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))")


@dataclasses.dataclass(frozen=True)
class ImportedSlide:
	"""Imported slide identity and visibility retained from ODP XML."""

	source_index: int
	name: str
	hidden: bool


@dataclasses.dataclass(frozen=True)
class RawObjectGeometry:
	"""One raw ODF object rectangle retained for migration review."""

	source_ordinal: int
	source_kind: str
	left: float
	top: float
	width: float
	height: float
	z_order: tuple[int, ...]


@dataclasses.dataclass(frozen=True)
class ReadSlide:
	"""One physical ODP page and its planner-ready raw source facts."""

	identity: ImportedSlide
	data: source_model.SlideData
	positioned_text: tuple[source_model.PositionedText, ...]
	positioned_visual: tuple[source_model.PositionedVisual, ...]
	page_width: float
	page_height: float
	raw_geometry: tuple[RawObjectGeometry, ...]


@dataclasses.dataclass(frozen=True)
class ImportedPresentation:
	"""The bounded direct-reader result for one native ODP package."""

	slides: tuple[ReadSlide, ...]


@dataclasses.dataclass
class _PageAccumulator:
	"""Mutable extraction state used only while reading one XML page."""

	titles: list[tuple[source_model.TextRun, ...]]
	text_blocks: list[source_model.TextBlock]
	tables: list[source_model.TableBlock]
	images: list[source_model.ImageAsset]
	positioned_text: list[source_model.PositionedText]
	positioned_visual: list[source_model.PositionedVisual]
	review_reasons: list[str]
	populated_roles: list[str]
	populated_text_roles: list[str]
	populated_image_roles: list[str]
	populated_table_roles: list[str]
	raw_geometry: list[RawObjectGeometry]
	meaningful_content_count: int = 0
	next_ordinal: int = 0
	object_count: int = 0


@dataclasses.dataclass
class _MediaBudget:
	"""Bounded decoded media totals for one source presentation."""

	frame_count: int = 0
	pixel_count: int = 0


#============================================
def qname(prefix: str, local_name: str) -> str:
	"""Build one namespace-qualified XML name."""
	return f"{{{NS[prefix]}}}{local_name}"


#============================================
def validate_odp(input_path: pathlib.Path) -> list[zipfile.ZipInfo]:
	"""Validate ODP archive, XML, manifest, and consumed local references."""
	return slide_lib.odf_package.validate_package(
		input_path, ".odp", ODP_MIMETYPE, slide_lib.odf_package.REQUIRED_ODP_MEMBERS,
	)


#============================================
def read_slides(input_path: pathlib.Path) -> list[ImportedSlide]:
	"""Read imported slide order and visibility from ODP XML."""
	package = slide_lib.odf_package.admit_package(
		input_path, ".odp", ODP_MIMETYPE, slide_lib.odf_package.REQUIRED_ODP_MEMBERS,
	)
	root = package.content_root
	definitions = odp_visibility.style_definitions_from_root(package.styles_root)
	definitions.update(odp_visibility.style_definitions_from_root(root))
	pages = root.findall(".//draw:page", NS)
	if len(pages) > MAX_PRESENTATION_PAGES:
		raise ValueError("ODF presentation page limit exceeded")
	slides: list[ImportedSlide] = []
	for source_index, page in enumerate(pages, start=1):
		slide_name = page.get(qname("draw", "name"), f"slide_{source_index:03d}")
		slides.append(ImportedSlide(
			source_index, slide_name, odp_visibility.page_is_hidden(page, definitions),
		))
	return slides


#============================================
def local_name(element: xml.etree.ElementTree.Element) -> str:
	"""Return an XML tag without its namespace."""
	return element.tag.rsplit("}", 1)[-1]


#============================================
def parse_length(raw_value: str | None, *, field_name: str,
		allow_negative: bool) -> float:
	"""Convert one bounded ODF physical length to points."""
	if raw_value is None:
		raise ValueError(f"ODF object is missing {field_name}")
	matched = LENGTH_VALUE.fullmatch(raw_value.strip())
	if matched is None:
		raise ValueError(f"ODF {field_name} is not a supported finite length")
	value = float(matched.group(1))
	points_per_unit = {
		"cm": 72.0 / 2.54,
		"in": 72.0,
		"mm": 72.0 / 25.4,
		"pc": 12.0,
		"pt": 1.0,
		"px": 0.75,
	}[matched.group(2)]
	points = value * points_per_unit
	if not math.isfinite(points) or abs(points) > MAX_ODF_LENGTH_POINTS or \
			(not allow_negative and points <= 0.0):
		raise ValueError(f"ODF {field_name} is outside the supported physical range")
	return points


#============================================
def page_style_layouts(
		roots: tuple[xml.etree.ElementTree.Element, ...],
) -> dict[str, tuple[str, str]]:
	"""Map drawing-page styles to their page-layout and parent style names."""
	definitions: dict[str, tuple[str, str]] = {}
	for root in roots:
		for style in root.findall(".//style:style", NS):
			if style.get(qname("style", "family")) != "drawing-page":
				continue
			name = style.get(qname("style", "name"))
			if not name:
				raise ValueError("ODF drawing-page style is missing its name")
			definitions[name] = (
				style.get(qname("style", "page-layout-name"), ""),
				style.get(qname("style", "parent-style-name"), ""),
			)
	return definitions


#============================================
def resolve_page_layout(style_name: str, definitions: dict[str, tuple[str, str]],
		ancestry: set[str]) -> str:
	"""Resolve one drawing-page style's physical page-layout identity."""
	if not style_name:
		return ""
	if style_name in ancestry:
		raise ValueError("ODF drawing-page style inheritance contains a cycle")
	definition = definitions.get(style_name)
	if definition is None:
		return ""
	layout_name, parent_name = definition
	if layout_name:
		return layout_name
	return resolve_page_layout(parent_name, definitions, ancestry | {style_name})


#============================================
def read_page_layout_dimensions(
		roots: tuple[xml.etree.ElementTree.Element, ...],
) -> dict[str, tuple[float, float]]:
	"""Read all named ODF physical page-layout dimensions."""
	dimensions: dict[str, tuple[float, float]] = {}
	for root in roots:
		for layout in root.findall(".//style:page-layout", NS):
			name = layout.get(qname("style", "name"))
			properties = layout.find("./style:page-layout-properties", NS)
			if not name or properties is None:
				continue
			dimensions[name] = (
				parse_length(properties.get(qname("fo", "page-width")),
					field_name="page width", allow_negative=False),
				parse_length(properties.get(qname("fo", "page-height")),
					field_name="page height", allow_negative=False),
			)
	return dimensions


#============================================
def master_page_layouts(
		roots: tuple[xml.etree.ElementTree.Element, ...],
) -> dict[str, str]:
	"""Map master-page names to their physical page-layout identities."""
	definitions: dict[str, str] = {}
	for root in roots:
		for master in root.findall(".//style:master-page", NS):
			name = master.get(qname("style", "name"))
			layout_name = master.get(qname("style", "page-layout-name"))
			if name and layout_name:
				definitions[name] = layout_name
	return definitions


#============================================
def page_dimensions(
		page: xml.etree.ElementTree.Element,
		style_layouts: dict[str, tuple[str, str]],
		master_layouts: dict[str, str],
		layout_dimensions: dict[str, tuple[float, float]],
) -> tuple[float, float]:
	"""Return the physical source dimensions declared for one ODP page."""
	style_name = page.get(qname("draw", "style-name"), "")
	layout_name = resolve_page_layout(style_name, style_layouts, set())
	if not layout_name:
		master_name = page.get(qname("draw", "master-page-name"), "")
		layout_name = master_layouts.get(master_name, "")
	if not layout_name:
		raise ValueError("ODF page has no resolvable physical page layout")
	dimensions = layout_dimensions.get(layout_name)
	if dimensions is None:
		raise ValueError("ODF drawing-page style references an unknown page layout")
	return dimensions


#============================================
def read_declared_placeholder_roles(
		roots: tuple[xml.etree.ElementTree.Element, ...],
) -> dict[str, tuple[str, ...]]:
	"""Read page-layout placeholder roles without inferring target layouts."""
	roles_by_layout: dict[str, tuple[str, ...]] = {}
	for root in roots:
		for layout in root.findall(".//style:presentation-page-layout", NS):
			name = layout.get(qname("style", "name"))
			if not name:
				raise ValueError("ODF presentation-page-layout is missing its name")
			roles_by_layout[name] = tuple(
				placeholder.get(qname("presentation", "object"))
				for placeholder in layout.findall(".//presentation:placeholder", NS)
				if placeholder.get(qname("presentation", "object"))
			)
	return roles_by_layout


#============================================
def safe_hyperlink(address: str | None) -> str:
	"""Return a direct http, https, or mailto source link when safe."""
	if not address:
		return ""
	parsed = urllib.parse.urlsplit(address)
	if parsed.scheme.lower() not in SAFE_LINK_SCHEMES:
		return ""
	return address


#============================================
def trim_runs(runs: list[source_model.TextRun]) -> tuple[source_model.TextRun, ...]:
	"""Strip paragraph-edge whitespace while retaining source run boundaries."""
	while runs and not runs[0].text:
		runs.pop(0)
	while runs and not runs[-1].text:
		runs.pop()
	if not runs:
		return ()
	runs[0] = source_model.TextRun(runs[0].text.lstrip(), runs[0].link)
	runs[-1] = source_model.TextRun(runs[-1].text.rstrip(), runs[-1].link)
	return tuple(run for run in runs if run.text)


#============================================
def append_run(runs: list[source_model.TextRun], text: str, link: str) -> None:
	"""Retain one visible source character sequence when it is nonempty."""
	if text:
		runs.append(source_model.TextRun(text, link))


#============================================
def inline_runs(element: xml.etree.ElementTree.Element,
		link: str = "") -> tuple[source_model.TextRun, ...]:
	"""Extract styled ODF inline text and allow-listed link targets."""
	runs: list[source_model.TextRun] = []

	def visit(node: xml.etree.ElementTree.Element, inherited_link: str) -> None:
		append_run(runs, node.text or "", inherited_link)
		for child in node:
			if child.tag == qname("text", "s"):
				count_raw = child.get(qname("text", "c"), "1")
				if not count_raw.isdigit() or int(count_raw) > MAX_TABLE_CELLS:
					raise ValueError("ODF text space count exceeds the supported range")
				append_run(runs, " " * int(count_raw), inherited_link)
			elif child.tag == qname("text", "tab"):
				append_run(runs, "\t", inherited_link)
			elif child.tag == qname("text", "line-break"):
				append_run(runs, " ", inherited_link)
			else:
				child_link = inherited_link
				if child.tag == qname("text", "a"):
					child_link = safe_hyperlink(child.get(qname("xlink", "href")))
				visit(child, child_link)
			append_run(runs, child.tail or "", inherited_link)

	visit(element, link)
	return trim_runs(runs)


#============================================
def text_paragraphs(container: xml.etree.ElementTree.Element) -> tuple[
	tuple[int, tuple[source_model.TextRun, ...]], ...,
]:
	"""Extract paragraphs and explicit ODF nested-list levels in source order."""
	lines: list[tuple[int, tuple[source_model.TextRun, ...]]] = []

	def visit_children(parent: xml.etree.ElementTree.Element, level: int) -> None:
		for child in parent:
			if child.tag in {qname("text", "p"), qname("text", "h")}:
				runs = inline_runs(child)
				if runs:
					lines.append((level, runs))
			elif child.tag == qname("text", "list"):
				visit_list(child, level)
			else:
				visit_children(child, level)

	def visit_list(list_element: xml.etree.ElementTree.Element, level: int) -> None:
		for item in list_element:
			if item.tag not in {qname("text", "list-header"), qname("text", "list-item")}:
				continue
			for child in item:
				if child.tag in {qname("text", "p"), qname("text", "h")}:
					runs = inline_runs(child)
					if runs:
						lines.append((level, runs))
				elif child.tag == qname("text", "list"):
					visit_list(child, level + 1)
				else:
					visit_children(child, level)

	visit_children(container, 0)
	return tuple(lines)


#============================================
def plain_text(runs: tuple[source_model.TextRun, ...]) -> str:
	"""Return visible source characters for density and identity checks."""
	return "".join(run.text for run in runs)


#============================================
def page_notes(page: xml.etree.ElementTree.Element) -> tuple[str, ...]:
	"""Read presenter-note paragraphs from one ODP page."""
	notes: list[str] = []
	for notes_element in page.findall("./presentation:notes", NS):
		for _level, runs in text_paragraphs(notes_element):
			text = plain_text(runs).strip()
			if text:
				notes.append(text)
	return tuple(notes)


#============================================
def frame_geometry(element: xml.etree.ElementTree.Element,
		source_index: int) -> tuple[float, float, float, float]:
	"""Read finite source geometry for one visible ODF object."""
	left = parse_length(element.get(qname("svg", "x"), "0cm"),
		field_name="x", allow_negative=True)
	top = parse_length(element.get(qname("svg", "y"), "0cm"),
		field_name="y", allow_negative=True)
	width = parse_length(element.get(qname("svg", "width")),
		field_name="width", allow_negative=False)
	height = parse_length(element.get(qname("svg", "height")),
		field_name="height", allow_negative=False)
	return left, top, width, height


#============================================
def vector_geometry(element: xml.etree.ElementTree.Element,
		source_index: int) -> tuple[float, float, float, float] | None:
	"""Read a finite vector rectangle or line endpoints when ODF supplies them."""
	if element.get(qname("svg", "width")) is not None and \
			element.get(qname("svg", "height")) is not None:
		return frame_geometry(element, source_index)
	if element.tag != qname("draw", "line"):
		return None
	first_x = parse_length(element.get(qname("svg", "x1")), field_name="line x1",
		allow_negative=True)
	first_y = parse_length(element.get(qname("svg", "y1")), field_name="line y1",
		allow_negative=True)
	second_x = parse_length(element.get(qname("svg", "x2")), field_name="line x2",
		allow_negative=True)
	second_y = parse_length(element.get(qname("svg", "y2")), field_name="line y2",
		allow_negative=True)
	if first_x == second_x and first_y == second_y:
		raise ValueError("ODF line has identical endpoints")
	return min(first_x, second_x), min(first_y, second_y), \
		abs(second_x - first_x), abs(second_y - first_y)


#============================================
def visible_geometry(
		geometry: tuple[float, float, float, float], page_width: float,
		page_height: float, source_index: int,
) -> bool:
	"""Reject fully outside objects and identify a partially outside rectangle."""
	left, top, width, height = geometry
	if left + width <= 0.0 or top + height <= 0.0 or left >= page_width or top >= page_height:
		raise ValueError(f"source slide {source_index}: source geometry lies outside page bounds")
	return left < 0.0 or top < 0.0 or left + width > page_width or top + height > page_height


#============================================
def style_evidence(element: xml.etree.ElementTree.Element) -> tuple[bool, bool]:
	"""Read direct positive style facts without treating ODF style names as data."""
	fill = element.get(qname("draw", "fill"))
	stroke = element.get(qname("svg", "stroke-color"))
	return fill not in {None, "none"}, stroke not in {None, "none"}


#============================================
def rotation_degrees(element: xml.etree.ElementTree.Element) -> float:
	"""Return a finite explicit ODF rotation or zero when none is declared."""
	matched = ROTATION_VALUE.search(element.get(qname("draw", "transform"), ""))
	if matched is None:
		return 0.0
	rotation = float(matched.group(1))
	if not math.isfinite(rotation):
		raise ValueError("ODF source rotation must be finite")
	return rotation


#============================================
def validate_image_blob(blob: bytes, suffix: str, media_budget: _MediaBudget) -> None:
	"""Decode every raster frame before publishing a canonical asset extension."""
	# ASVS 5.2.2 and 5.2.6: decode all admitted media before it reaches staging.
	if suffix not in SUPPORTED_IMAGE_SUFFIXES:
		raise ValueError(f"unsupported ODP image type: {suffix}")
	if len(blob) > slide_lib.odf_package.MAX_MEMBER_BYTES:
		raise ValueError("ODP image exceeds the per-image size limit")
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


#============================================
def table_cell_runs(cell: xml.etree.ElementTree.Element) -> tuple[source_model.TextRun, ...]:
	"""Read one ODF table cell into the native inline table vocabulary."""
	result: list[source_model.TextRun] = []
	for _level, runs in text_paragraphs(cell):
		if result:
			result.append(source_model.TextRun(" "))
		result.extend(runs)
	return tuple(result)


#============================================
def repeat_count(element: xml.etree.ElementTree.Element, attribute: str) -> int:
	"""Return one bounded ODF table repeat value."""
	raw_value = element.get(qname("table", attribute), "1")
	if not raw_value.isdigit() or not 1 <= int(raw_value) <= MAX_TABLE_REPEAT:
		raise ValueError("ODF table repeat count exceeds the supported range")
	return int(raw_value)


#============================================
def read_table(table: xml.etree.ElementTree.Element, left: float, top: float,
		source_ordinal: int) -> tuple[source_model.TableBlock,
		list[tuple[int, int, tuple[source_model.TextRun, ...]]]]:
	"""Extract a rectangular ODF table and its planner-facing cell facts."""
	rows: list[tuple[tuple[source_model.TextRun, ...], ...]] = []
	header_row_count = 0
	unsupported: list[str] = []
	total_cell_count = 0

	def add_row(row: xml.etree.ElementTree.Element, is_header: bool) -> None:
		nonlocal header_row_count, total_cell_count
		cells: list[tuple[source_model.TextRun, ...]] = []
		for cell in row:
			if cell.tag not in {qname("table", "table-cell"), qname("table", "covered-table-cell")}:
				continue
			if cell.tag == qname("table", "covered-table-cell"):
				unsupported.append("covered source table cells require span-aware emission")
			if cell.get(qname("table", "number-columns-spanned")) or \
					cell.get(qname("table", "number-rows-spanned")):
				unsupported.append("merged source table cells require span-aware emission")
			for _repeat in range(repeat_count(cell, "number-columns-repeated")):
				if len(cells) >= MAX_TABLE_CELLS:
					raise ValueError("ODF table exceeds the supported cell range")
				cells.append(table_cell_runs(cell))
		row_repeats = repeat_count(row, "number-rows-repeated")
		if total_cell_count + len(cells) * row_repeats > MAX_TABLE_CELLS:
			raise ValueError("ODF table exceeds the supported cell range")
		for _repeat in range(row_repeats):
			if len(rows) >= MAX_TABLE_CELLS:
				raise ValueError("ODF table exceeds the supported cell range")
			rows.append(tuple(cells))
			total_cell_count += len(cells)
			if is_header:
				header_row_count += 1

	for child in table:
		if child.tag == qname("table", "table-header-rows"):
			for row in child.findall("./table:table-row", NS):
				add_row(row, True)
		elif child.tag == qname("table", "table-row"):
			add_row(child, False)
	if not rows:
		raise ValueError("ODF table has no rows")
	column_count = len(rows[0])
	if not column_count or any(len(row) != column_count for row in rows):
		unsupported.append("irregular source table rows require reconstruction")
	if header_row_count > 1:
		unsupported.append("multiple source table header rows require reconstruction")
	headers = rows[0] if header_row_count == 1 else ()
	body_rows = rows[1:] if header_row_count == 1 else rows
	cell_facts: list[tuple[int, int, tuple[source_model.TextRun, ...]]] = []
	for row_index, row in enumerate(rows):
		for column_index, cell in enumerate(row):
			if cell:
				cell_facts.append((row_index, column_index, cell))
	return source_model.TableBlock(
		headers, tuple(body_rows), left, top, source_ordinal,
		"; ".join(sorted(set(unsupported))) or None,
	), cell_facts


#============================================
def append_geometry(accumulator: _PageAccumulator, source_ordinal: int,
		source_kind: str, geometry: tuple[float, float, float, float],
		z_order: tuple[int, ...]) -> None:
	"""Retain the original rectangle for the direct-import audit report."""
	left, top, width, height = geometry
	accumulator.raw_geometry.append(RawObjectGeometry(
		source_ordinal, source_kind, left, top, width, height, z_order,
	))


#============================================
def add_picture(
		image: xml.etree.ElementTree.Element,
		geometry: tuple[float, float, float, float], source_ordinal: int,
		archive: zipfile.ZipFile, member_names: frozenset[str], manifest_targets: frozenset[str],
		assets_dir: pathlib.Path,
		djot_root: pathlib.PurePosixPath, known_images: dict[str, str],
		accumulator: _PageAccumulator, media_budget: _MediaBudget,
		z_order: tuple[int, ...],
) -> bool:
	"""Stage one validated package-local image, retaining external evidence."""
	reference = image.get(qname("xlink", "href"))
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
	suffix = image_suffix(target)
	try:
		validate_image_blob(blob, suffix, media_budget)
	except (OSError, ValueError) as error:
		accumulator.review_reasons.append(f"source image requires review: {error}")
		return True
	digest = hashlib.sha256(blob).hexdigest()
	asset_name = known_images.get(digest)
	if asset_name is None:
		asset_name = f"image_{len(known_images) + 1:03d}{suffix}"
		# ASVS 5.3.2: digest-derived names select only the private staging path.
		(assets_dir / asset_name).write_bytes(blob)
		known_images[digest] = asset_name
	left, top, width, height = geometry
	asset_path = (djot_root / asset_name).as_posix()
	accumulator.images.append(source_model.ImageAsset(
		left, top, width, height, asset_path, f"Slide image {len(known_images)}",
	))
	accumulator.positioned_visual.append(source_model.PositionedVisual(
		asset_path, left, top, width, height, "picture", source_ordinal,
		z_order=z_order,
	))
	return True


#============================================
def add_text(
		text_box: xml.etree.ElementTree.Element,
		geometry: tuple[float, float, float, float], source_ordinal: int,
		role: str | None, element: xml.etree.ElementTree.Element,
		accumulator: _PageAccumulator, z_order: tuple[int, ...],
) -> bool:
	"""Add text runs and positioned facts from one visible ODP text object."""
	paragraphs = text_paragraphs(text_box)
	if not paragraphs:
		return False
	left, top, width, height = geometry
	# Preserve the ODP subtitle role in page evidence and the raw placeholder
	# field while the generalized emitter receives ordinary text.
	is_subtitle = False
	title_identity = role == "title"
	source_kind = "text" if role else "text-box"
	has_fill, has_line = style_evidence(element)
	positioned = source_model.PositionedText(
		paragraphs, left, top, width, height, is_subtitle, 1.0 if role else 0.0,
		title_identity, source_kind, source_ordinal,
		rotation_degrees=rotation_degrees(element), has_positive_fill=has_fill,
		has_positive_line=has_line, placeholder_role=role, z_order=z_order,
	)
	accumulator.positioned_text.append(positioned)
	if title_identity:
		accumulator.titles.extend(runs for _level, runs in paragraphs)
	else:
		accumulator.text_blocks.append(source_model.TextBlock(
			left, top, paragraphs, is_subtitle,
		))
	return True


#============================================
def add_table(
		table: xml.etree.ElementTree.Element,
		geometry: tuple[float, float, float, float], source_ordinal: int,
		role: str | None, element: xml.etree.ElementTree.Element,
		accumulator: _PageAccumulator, z_order: tuple[int, ...],
) -> bool:
	"""Add a real ODF table and its planning evidence without flattening cells."""
	left, top, width, height = geometry
	block, cells = read_table(table, left, top, source_ordinal)
	accumulator.tables.append(block)
	has_fill, has_line = style_evidence(element)
	row_count = len(block.rows) + (1 if block.headers else 0)
	column_count = len(block.headers or block.rows[0])
	for row_index, column_index, runs in cells:
		accumulator.positioned_text.append(source_model.PositionedText(
			((0, runs),), left, top, width, height, False, 1.0 if role else 0.0,
			False, "table", source_ordinal * 10_000 + row_index * column_count + column_index,
			row_index, column_index, row_count, column_count, source_ordinal,
			bool(block.headers), block.unsupported_reason, rotation_degrees(element),
			has_fill, has_line, role, z_order,
		))
	return True


#============================================
def read_frame(
		frame: xml.etree.ElementTree.Element, source_index: int, page_width: float,
		page_height: float, archive: zipfile.ZipFile, member_names: frozenset[str],
		manifest_targets: frozenset[str], assets_dir: pathlib.Path,
		djot_root: pathlib.PurePosixPath, known_images: dict[str, str],
		accumulator: _PageAccumulator, media_budget: _MediaBudget,
		z_order: tuple[int, ...], source_ordinal: int,
) -> None:
	"""Read one ODP frame into supported facts or an explicit review lane."""
	text_box = frame.find("./draw:text-box", NS)
	table = frame.find(".//table:table", NS)
	image = frame.find("./draw:image", NS)
	ordinal = source_ordinal
	geometry = frame_geometry(frame, source_index)
	if visible_geometry(geometry, page_width, page_height, source_index):
		accumulator.review_reasons.append("source object crosses physical page bounds")
	role = frame.get(qname("presentation", "class"))
	contains_text = False
	contains_table = False
	contains_image = False
	if text_box is not None:
		contains_text = add_text(text_box, geometry, ordinal, role, frame, accumulator, z_order)
	if table is not None:
		contains_table = add_table(table, geometry, ordinal, role, frame, accumulator, z_order)
	if image is not None:
		contains_image = add_picture(
			image, geometry, ordinal, archive, member_names, manifest_targets, assets_dir,
			djot_root, known_images, accumulator, media_budget, z_order,
		)
	if contains_text or contains_table or contains_image:
		append_geometry(accumulator, ordinal, "frame", geometry, z_order)
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
	append_geometry(accumulator, ordinal, "vector", geometry, z_order)
	accumulator.review_reasons.append(
		f"unsupported source object draw:{local_name(frame)} requires reconstruction")


#============================================
def read_page_objects(
		page: xml.etree.ElementTree.Element, source_index: int, page_width: float,
		page_height: float, archive: zipfile.ZipFile, member_names: frozenset[str],
		manifest_targets: frozenset[str], assets_dir: pathlib.Path,
		djot_root: pathlib.PurePosixPath, known_images: dict[str, str],
		media_budget: _MediaBudget,
) -> _PageAccumulator:
	"""Extract direct visible page objects in their original nested z-order."""
	accumulator = _PageAccumulator([], [], [], [], [], [], [], [], [], [], [], [])

	def next_object() -> int:
		accumulator.object_count += 1
		if accumulator.object_count > MAX_PAGE_OBJECTS:
			raise ValueError(f"source slide {source_index}: ODF page object limit exceeded")
		accumulator.next_ordinal += 1
		return accumulator.next_ordinal

	def read_vector(element: xml.etree.ElementTree.Element, z_order: tuple[int, ...]) -> None:
		ordinal = next_object()
		geometry = vector_geometry(element, source_index)
		if geometry is None:
			accumulator.review_reasons.append(
				f"source slide {source_index}: unsupported draw:{local_name(element)} has no bounded geometry",
			)
			return
		if visible_geometry(geometry, page_width, page_height, source_index):
			accumulator.review_reasons.append("source object crosses physical page bounds")
		append_geometry(accumulator, ordinal, "vector", geometry, z_order)
		accumulator.review_reasons.append(
			f"unsupported source object draw:{local_name(element)} requires reconstruction")

	known_vectors = {
		qname("draw", "rect"), qname("draw", "ellipse"), qname("draw", "line"),
		qname("draw", "custom-shape"), qname("draw", "path"), qname("draw", "connector"),
	}
	stack = [
		(child, (child_index,)) for child_index, child in reversed(list(enumerate(page)))
		if child.tag not in {qname("presentation", "notes"), qname("office", "forms")}
	]
	while stack:
		element, z_order = stack.pop()
		if element.tag == qname("draw", "frame"):
			ordinal = next_object()
			read_frame(element, source_index, page_width, page_height, archive, member_names,
				manifest_targets, assets_dir, djot_root, known_images, accumulator, media_budget,
				z_order, ordinal)
			continue
		if element.tag == qname("draw", "g"):
			if len(z_order) >= MAX_DRAW_GROUP_DEPTH:
				raise ValueError(f"source slide {source_index}: ODF draw group depth limit exceeded")
			stack.extend(
				(child, (*z_order, child_index))
				for child_index, child in reversed(list(enumerate(element)))
			)
			continue
		if element.tag in known_vectors:
			read_vector(element, z_order)
			continue
		if element.tag.startswith(f"{{{NS['draw']}}}"):
			ordinal = next_object()
			accumulator.meaningful_content_count += 1
			accumulator.review_reasons.append(
				f"source slide {source_index}: unsupported meaningful draw:{local_name(element)} requires review",
			)
			geometry = vector_geometry(element, source_index)
			if geometry is not None:
				append_geometry(accumulator, ordinal, "unknown", geometry, z_order)
	return accumulator


#============================================
def read_presentation(input_path: pathlib.Path, assets_dir: pathlib.Path,
		djot_root: pathlib.PurePosixPath) -> ImportedPresentation:
	"""Read validated native ODP pages directly into raw semantic facts."""
	# ASVS 1.5.1, 2.2.1, 5.2.2, and 5.2.3: admit bounded package facts before extraction.
	admitted = slide_lib.odf_package.admit_package(
		input_path, ".odp", ODP_MIMETYPE, slide_lib.odf_package.REQUIRED_ODP_MEMBERS,
	)
	archive = zipfile.ZipFile(input_path)
	try:
		member_names = admitted.member_names
		content_root = admitted.content_root
		styles_root = admitted.styles_root
		roots = (styles_root, content_root)
		visibility = odp_visibility.style_definitions_from_root(styles_root)
		visibility.update(odp_visibility.style_definitions_from_root(content_root))
		style_layouts = page_style_layouts(roots)
		master_layouts = master_page_layouts(roots)
		layout_dimensions = read_page_layout_dimensions(roots)
		declared_roles = read_declared_placeholder_roles(roots)
		known_images: dict[str, str] = {}
		media_budget = _MediaBudget()
		read_slides_result: list[ReadSlide] = []
		pages = content_root.findall(".//draw:page", NS)
		if len(pages) > MAX_PRESENTATION_PAGES:
			raise ValueError("ODF presentation page limit exceeded")
		for source_index, page in enumerate(pages, start=1):
			identity = ImportedSlide(
				source_index, page.get(qname("draw", "name"), f"slide_{source_index:03d}"),
				odp_visibility.page_is_hidden(page, visibility),
			)
			page_width, page_height = page_dimensions(
				page, style_layouts, master_layouts, layout_dimensions,
			)
			layout_identity = page.get(qname("presentation", "presentation-page-layout-name"))
			accumulator = read_page_objects(
				page, source_index, page_width, page_height, archive, member_names,
				admitted.manifest_targets, assets_dir, djot_root, known_images, media_budget,
			)
			line_count = sum(len(block.lines) for block in accumulator.text_blocks)
			character_count = sum(
				len(plain_text(runs)) for block in accumulator.text_blocks
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
				page_notes(page), tuple(sorted(set(accumulator.review_reasons))),
				tuple(sorted(accumulator.tables, key=lambda table: (table.top, table.left))), evidence,
			)
			read_slides_result.append(ReadSlide(
				identity, data, tuple(accumulator.positioned_text),
				tuple(accumulator.positioned_visual), page_width, page_height,
				tuple(accumulator.raw_geometry),
			))
		return ImportedPresentation(tuple(read_slides_result))
	finally:
		archive.close()
