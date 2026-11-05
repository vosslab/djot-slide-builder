"""ODF namespaces, page layouts, and bounded source-object geometry."""

# Standard Library
import dataclasses
import math
import re
import xml.etree.ElementTree

# PIP3 modules
# local repo modules
import slide_lib.importers.odf_styles as odf_styles


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
MAX_ODF_LENGTH_POINTS = 100_000.0
LENGTH_VALUE = re.compile(r"^([+-]?(?:\d+(?:\.\d*)?|\.\d+))(cm|in|mm|pc|pt|px)$")
ROTATION_VALUE = re.compile(r"rotate\s*\(\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))")


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


#============================================
def qname(prefix: str, local_name: str) -> str:
	"""Build one namespace-qualified XML name."""
	return f"{{{NS[prefix]}}}{local_name}"


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
	if element.tag == qname("draw", "polyline"):
		# ASVS 2.2.1: validate bounded lengths even for unsupported flat polylines.
		dimensions = tuple(parse_length(element.get(qname("svg", name)),
			field_name=f"polyline {name}", allow_negative=True) for name in ("width", "height"))
		if min(dimensions) < 0.0:
			raise ValueError("ODF polyline dimensions must be nonnegative")
		if min(dimensions) == 0.0:
			return None
	if element.get(qname("svg", "width")) is not None and \
			element.get(qname("svg", "height")) is not None:
		return frame_geometry(element, source_index)
	if element.tag != qname("draw", "line"):
		return None
	first_x, first_y, second_x, second_y = line_endpoints(element)
	return min(first_x, second_x), min(first_y, second_y), \
		abs(second_x - first_x), abs(second_y - first_y)


#============================================
def line_endpoints(element: xml.etree.ElementTree.Element) \
		-> tuple[float, float, float, float]:
	"""Read one native line without discarding its authored direction."""
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
	return first_x, first_y, second_x, second_y


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
def style_evidence(element: xml.etree.ElementTree.Element,
		definitions: dict[str, odf_styles.StyleDefinition]) -> tuple[bool, bool]:
	"""Read direct positive style facts without treating ODF style names as data."""
	fill = odf_styles.attribute(element, definitions, qname("draw", "fill"))
	stroke = odf_styles.attribute(element, definitions, qname("svg", "stroke-color"))
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
