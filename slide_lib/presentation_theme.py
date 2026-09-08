"""Format-neutral presentation theme loaded from the authoritative ODP template."""

# Standard Library
import pathlib
import zipfile
import functools
import dataclasses
import xml.etree.ElementTree

# PIP3 modules
import defusedxml.ElementTree

# local repo modules
import slide_lib.odf_package


LOGICAL_SLIDE_WIDTH = 1280.0
LOGICAL_SLIDE_HEIGHT = 800.0
EMU_PER_CM = 360000.0
POINTS_PER_LOGICAL_PIXEL = 0.75
OTP_MIMETYPE = "application/vnd.oasis.opendocument.presentation-template"
DEFAULT_TEMPLATE_PATH = pathlib.Path(__file__).resolve().parent.parent / \
	"genetics/xlect99-template_2023.otp"
NS = {
	"draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
	"fo": "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0",
	"presentation": "urn:oasis:names:tc:opendocument:xmlns:presentation:1.0",
	"style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
	"svg": "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0",
	"text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
}


class ThemeError(ValueError):
	"""Report a malformed or unsupported presentation-template theme."""


@dataclasses.dataclass(frozen=True)
class ListLevelStyle:
	"""Bullet and text positions for one native outline level, in logical pixels."""

	bullet_position: float
	text_position: float
	bullet_character: str


@dataclasses.dataclass(frozen=True)
class PresentationTheme:
	"""Validated theme values shared by the PPTX and ODP output adapters."""

	template_path: pathlib.Path
	master_name: str
	slide_width_cm: float
	slide_height_cm: float
	emu_per_logical_pixel: float
	top_band_height: float
	gradient_start_color: str
	gradient_end_color: str
	title_font_name: str
	standard_title_size: float
	list_levels: tuple[ListLevelStyle, ...]


#============================================
def qname(prefix: str, local_name: str) -> str:
	"""Build one namespace-qualified XML name."""
	return f"{{{NS[prefix]}}}{local_name}"


#============================================
def length_value(raw_value: str, unit: str) -> float:
	"""Read one positive template length with its required unit."""
	if not raw_value.endswith(unit):
		raise ThemeError(f"theme length must use {unit}: {raw_value}")
	value = float(raw_value[:-len(unit)])
	if value <= 0:
		raise ThemeError(f"theme length must be positive: {raw_value}")
	return value


#============================================
def nonnegative_length_value(raw_value: str, unit: str) -> float:
	"""Read one template length that may begin at the slide origin."""
	if not raw_value.endswith(unit):
		raise ThemeError(f"theme length must use {unit}: {raw_value}")
	value = float(raw_value[:-len(unit)])
	if value < 0:
		raise ThemeError(f"theme length must not be negative: {raw_value}")
	return value


#============================================
def named_element(root: xml.etree.ElementTree.Element, path: str,
		name_attribute: str, name: str) -> xml.etree.ElementTree.Element:
	"""Return one uniquely named XML element from the template."""
	matches = [element for element in root.findall(path, NS)
		if element.attrib.get(name_attribute) == name]
	if len(matches) != 1:
		raise ThemeError(f"theme requires exactly one {name}")
	return matches[0]


#============================================
def presentation_style(root: xml.etree.ElementTree.Element,
		name: str) -> xml.etree.ElementTree.Element:
	"""Return one named presentation-family style."""
	style = named_element(root, ".//style:style", qname("style", "name"), name)
	if style.attrib.get(qname("style", "family")) != "presentation":
		raise ThemeError(f"theme style is not a presentation style: {name}")
	return style


#============================================
def master_frame(master: xml.etree.ElementTree.Element,
		presentation_class: str) -> xml.etree.ElementTree.Element:
	"""Return one placeholder frame from the selected master page."""
	matches = [frame for frame in master.findall("draw:frame", NS)
		if frame.attrib.get(qname("presentation", "class")) == presentation_class]
	if len(matches) != 1:
		raise ThemeError(f"theme master requires one {presentation_class} frame")
	return matches[0]


#============================================
def list_level_styles(outline_style: xml.etree.ElementTree.Element,
		logical_pixels_per_cm: float) -> tuple[ListLevelStyle, ...]:
	"""Read the nine native PPTX outline levels from the ODP outline style."""
	levels: list[tuple[int, ListLevelStyle]] = []
	for bullet in outline_style.findall("./style:graphic-properties/text:list-style/"
			"text:list-level-style-bullet", NS):
		properties = bullet.find("style:list-level-properties", NS)
		if properties is None:
			raise ThemeError("theme outline level is missing positioning properties")
		level = int(bullet.attrib[qname("text", "level")])
		space_before = nonnegative_length_value(
			properties.attrib[qname("text", "space-before")], "cm")
		label_width = length_value(properties.attrib[qname("text", "min-label-width")], "cm")
		bullet_position = space_before * logical_pixels_per_cm
		text_position = (space_before + label_width) * logical_pixels_per_cm
		levels.append((level, ListLevelStyle(
			bullet_position, text_position, bullet.attrib[qname("text", "bullet-char")],
		)))
	levels.sort(key=lambda item: item[0])
	expected_levels = list(range(1, 10))
	if [level for level, _style in levels[:9]] != expected_levels:
		raise ThemeError("theme outline must define consecutive levels 1 through 9")
	styles = tuple(style for _level, style in levels[:9])
	return styles


#============================================
def load_theme(template_path: pathlib.Path) -> PresentationTheme:
	"""Load the master geometry and typography from one trusted ODP template."""
	resolved_path = template_path.resolve()
	required = frozenset({"mimetype", "content.xml", "styles.xml"})
	slide_lib.odf_package.validate_package(resolved_path, ".otp", OTP_MIMETYPE, required)
	with zipfile.ZipFile(resolved_path) as archive:
		styles_root = defusedxml.ElementTree.fromstring(archive.read("styles.xml"))
	masters = styles_root.findall(".//style:master-page", NS)
	if len(masters) != 1:
		raise ThemeError("theme template must define exactly one master page")
	master = masters[0]
	if master.findall(".//draw:image", NS):
		raise ThemeError("theme master images are unsupported by the styles-only transfer")
	master_name = master.attrib[qname("style", "name")]
	page_layout_name = master.attrib[qname("style", "page-layout-name")]
	page_layout = named_element(styles_root, ".//style:page-layout",
		qname("style", "name"), page_layout_name)
	page_properties = page_layout.find("style:page-layout-properties", NS)
	if page_properties is None:
		raise ThemeError("theme page layout is missing geometry")
	slide_width_cm = length_value(page_properties.attrib[qname("fo", "page-width")], "cm")
	slide_height_cm = length_value(page_properties.attrib[qname("fo", "page-height")], "cm")
	if abs(slide_width_cm / slide_height_cm - LOGICAL_SLIDE_WIDTH / LOGICAL_SLIDE_HEIGHT) > 0.001:
		raise ThemeError("theme page layout must use the 16:10 logical aspect ratio")
	emu_per_logical_pixel = slide_width_cm * EMU_PER_CM / LOGICAL_SLIDE_WIDTH
	logical_pixels_per_cm = LOGICAL_SLIDE_WIDTH / slide_width_cm
	bands = [shape for shape in master.findall("draw:custom-shape", NS)
		if length_value(shape.attrib[qname("svg", "width")], "cm") >= slide_width_cm - 0.1]
	if len(bands) != 1:
		raise ThemeError("theme master requires one full-width top-band shape")
	band = bands[0]
	if band.attrib[qname("svg", "x")] != "0cm" or band.attrib[qname("svg", "y")] != "0cm":
		raise ThemeError("theme top band must begin at the slide origin")
	band_style_name = band.attrib[qname("presentation", "style-name")]
	band_style = presentation_style(styles_root, band_style_name)
	graphic_properties = band_style.find("style:graphic-properties", NS)
	if graphic_properties is None or \
			graphic_properties.attrib.get(qname("draw", "fill")) != "gradient":
		raise ThemeError("theme top band must use a native gradient fill")
	gradient_name = graphic_properties.attrib[qname("draw", "fill-gradient-name")]
	gradient = named_element(styles_root, ".//draw:gradient", qname("draw", "name"), gradient_name)
	start_color = gradient.attrib[qname("draw", "start-color")].removeprefix("#").upper()
	end_color = gradient.attrib[qname("draw", "end-color")].removeprefix("#").upper()
	title_frame = master_frame(master, "title")
	title_style_name = title_frame.attrib[qname("presentation", "style-name")]
	title_style = presentation_style(styles_root, title_style_name)
	title_text = title_style.find("style:text-properties", NS)
	title_paragraph = title_style.find("style:paragraph-properties", NS)
	if title_text is None or title_paragraph is None:
		raise ThemeError("theme title style is missing text or paragraph properties")
	title_font = title_text.attrib[qname("fo", "font-family")].strip("'")
	title_size_pt = length_value(title_text.attrib[qname("fo", "font-size")], "pt")
	if title_paragraph.attrib.get(qname("fo", "text-align")) != "center":
		raise ThemeError("theme title style must be centered")
	outline_frame = master_frame(master, "outline")
	outline_style_name = outline_frame.attrib[qname("presentation", "style-name")]
	outline_style = presentation_style(styles_root, outline_style_name)
	levels = list_level_styles(outline_style, logical_pixels_per_cm)
	top_band_height = length_value(band.attrib[qname("svg", "height")], "cm") * logical_pixels_per_cm
	standard_title_size = title_size_pt / POINTS_PER_LOGICAL_PIXEL
	theme = PresentationTheme(
		resolved_path, master_name, slide_width_cm, slide_height_cm, emu_per_logical_pixel,
		top_band_height, start_color, end_color, title_font, standard_title_size, levels,
	)
	return theme


#============================================
@functools.cache
def default_theme() -> PresentationTheme:
	"""Return the immutable repository theme loaded from its ODP template."""
	return load_theme(DEFAULT_TEMPLATE_PATH)
