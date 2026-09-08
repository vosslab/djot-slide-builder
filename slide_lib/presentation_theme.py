"""Format-neutral presentation theme loaded from the authoritative ODP template."""

# Standard Library
import dataclasses
import enum
import functools
import hashlib
import json
import pathlib
import xml.etree.ElementTree
import zipfile

# PIP3 modules
import defusedxml.ElementTree
import fontTools.ttLib
import PIL.ImageFont

# local repo modules
import slide_lib.odf_package


LOGICAL_SLIDE_WIDTH = 1280.0
LOGICAL_SLIDE_HEIGHT = 800.0
EMU_PER_CM = 360000.0
OTP_MIMETYPE = "application/vnd.oasis.opendocument.presentation-template"
ORDINARY_LINE_SPACING_EM = 1.30
DEFAULT_TEMPLATE_PATH = pathlib.Path(__file__).resolve().parent.parent / \
	"genetics/xlect99-template_2023.otp"
REPOSITORY_ROOT = DEFAULT_TEMPLATE_PATH.parent.parent
FONT_MANIFEST_PATH = pathlib.PurePosixPath("assets/fonts/font_provenance.json")
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


class OverflowPolicy(enum.StrEnum):
	"""State the native frame behavior permitted after layout preflight."""

	SHRINK_ONLY = "shrink-only"


@dataclasses.dataclass(frozen=True)
class FontFaceProfile:
	"""One licensed, bundled face selected without host-font discovery."""

	family: str
	bold: bool
	italic: bool
	relative_path: pathlib.PurePosixPath
	sha256: str
	face_index: int


@dataclasses.dataclass(frozen=True)
class FontMetricProfile:
	"""Validated font metrics available to the physical layout measurement owner."""

	face: FontFaceProfile
	units_per_em: int
	ascender: int
	descender: int


@dataclasses.dataclass(frozen=True)
class FontProvenance:
	"""One pinned upstream source and local OFL record for a bundled face."""

	profile: FontFaceProfile
	upstream_url: str
	upstream_revision: str
	license_path: pathlib.PurePosixPath
	license_sha256: str


FONT_FACE_PROFILES = (
	FontFaceProfile("OpenDyslexic", False, False,
		pathlib.PurePosixPath("assets/fonts/opendyslexic/OpenDyslexic-Regular.otf"),
		"215f0b29780dbafa8c02f2f22118fb9e2ab6b27b6686e3f13c8754041a035f64", 0),
	FontFaceProfile("OpenDyslexic", True, False,
		pathlib.PurePosixPath("assets/fonts/opendyslexic/OpenDyslexic-Bold.otf"),
		"ee7a8b9590a78e183826d16d6a22a50f6253c62e2f7f5e0e01ef44eb0676a9e0", 0),
	FontFaceProfile("OpenDyslexic", False, True,
		pathlib.PurePosixPath("assets/fonts/opendyslexic/OpenDyslexic-Italic.otf"),
		"bd5c83e5c2a3e203fe816330572afe4ece576f8e2c20fb6359bd399e6ef37aaf", 0),
	FontFaceProfile("OpenDyslexic", True, True,
		pathlib.PurePosixPath("assets/fonts/opendyslexic/OpenDyslexic-Bold-Italic.otf"),
		"b50779f4f547917a648d38976a664cab8952563112ce03209ff568b1eb364090", 0),
	FontFaceProfile("PT Sans Narrow", False, False,
		pathlib.PurePosixPath("assets/fonts/pt_sans_narrow/PT_Sans-Narrow-Web-Regular.ttf"),
		"4102edda03059163771869d258df54ac8563c408fa6e9ef75b2ddc85eabea6f4", 0),
	FontFaceProfile("PT Sans Narrow", True, False,
		pathlib.PurePosixPath("assets/fonts/pt_sans_narrow/PT_Sans-Narrow-Web-Bold.ttf"),
		"e69d83bcf5bd647892b4e2b22f5098dabd55c989413513197722fc156fb9f00e", 0),
)


@dataclasses.dataclass(frozen=True)
class ListLevelStyle:
	"""Bullet and text positions for one native outline level, in logical pixels."""

	bullet_position: float
	text_position: float
	bullet_character: str


@dataclasses.dataclass(frozen=True)
class FrameGeometry:
	"""Physical native-placeholder bounds retained from the authoritative master."""

	x_cm: float
	y_cm: float
	width_cm: float
	height_cm: float


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
	western_font_name: str
	title_frame: FrameGeometry
	outline_frame: FrameGeometry
	title_style_name: str
	outline_style_names: tuple[str, ...]
	standard_title_size_pt: float
	ordinary_body_size_pt: float
	ordinary_line_spacing_em: float
	title_floor_size_pt: float
	body_floor_size_pt: float
	overflow_policy: OverflowPolicy
	list_levels: tuple[ListLevelStyle, ...]
	font_metrics: tuple[FontMetricProfile, ...]

#============================================
def qname(prefix: str, local_name: str) -> str:
	"""Build one namespace-qualified XML name."""
	return f"{{{NS[prefix]}}}{local_name}"


#============================================
def font_asset_path(profile: FontFaceProfile,
		repository_root: pathlib.Path = REPOSITORY_ROOT) -> pathlib.Path:
	"""Resolve one declared asset while rejecting paths outside this repository."""
	if profile.relative_path.is_absolute() or ".." in profile.relative_path.parts:
		raise ThemeError(f"font asset path must be repository-relative: {profile.relative_path}")
	path = (repository_root / profile.relative_path).resolve()
	if not path.is_relative_to(repository_root.resolve()):
		raise ThemeError(f"font asset path escapes repository: {profile.relative_path}")
	return path


#============================================
def font_manifest_path(repository_root: pathlib.Path = REPOSITORY_ROOT) -> pathlib.Path:
	"""Resolve the one versioned font-provenance manifest within the repository."""
	path = (repository_root / FONT_MANIFEST_PATH).resolve()
	if not path.is_relative_to(repository_root.resolve()):
		raise ThemeError("font provenance manifest escapes repository")
	return path


#============================================
def font_name(font: fontTools.ttLib.TTFont, preferred_id: int,
		fallback_id: int) -> str:
	"""Read one Unicode name record with the typographic value preferred."""
	records = tuple(record.toUnicode() for record in font["name"].names
		if record.nameID == preferred_id and record.platformID == 3)
	if not records:
		records = tuple(record.toUnicode() for record in font["name"].names
			if record.nameID == fallback_id and record.platformID == 3)
	if not records:
		raise ThemeError("bundled font does not provide a Windows Unicode name")
	return records[0]


#============================================
def font_style_flags(style_name: str) -> tuple[bool, bool]:
	"""Map an intrinsic face style name to the declared bold and italic booleans."""
	normalized = style_name.lower().replace("-", " ")
	bold = "bold" in normalized
	italic = "italic" in normalized
	return bold, italic


#============================================
def validate_font_manifest(repository_root: pathlib.Path = REPOSITORY_ROOT) -> tuple[FontProvenance, ...]:
	"""Verify every registered face has an immutable upstream source and OFL record."""
	path = font_manifest_path(repository_root)
	if not path.is_file():
		raise ThemeError("bundled font provenance manifest is missing")
	with path.open(encoding="utf-8") as manifest_file:
		manifest = json.load(manifest_file)
	if manifest["manifest_version"] != 1:
		raise ThemeError("unsupported bundled font provenance manifest version")
	entries = manifest["fonts"]
	if not isinstance(entries, list):
		raise ThemeError("bundled font provenance manifest fonts must be a list")
	provenance = []
	for profile in FONT_FACE_PROFILES:
		matches = [entry for entry in entries if entry["path"] == str(profile.relative_path)]
		if len(matches) != 1:
			raise ThemeError(f"font provenance must contain exactly one record: {profile.relative_path}")
		entry = matches[0]
		registered = (profile.family, profile.bold, profile.italic, profile.sha256, profile.face_index)
		declared = (entry["family"], entry["bold"], entry["italic"], entry["sha256"],
			entry["face_index"])
		if declared != registered:
			raise ThemeError(f"font provenance disagrees with registered face: {profile.relative_path}")
		license = entry["license"]
		license_path = pathlib.PurePosixPath(license["path"])
		if license["spdx"] != "OFL-1.1" or license_path.is_absolute() or ".." in license_path.parts:
			raise ThemeError(f"font provenance has invalid OFL record: {profile.relative_path}")
		absolute_license = (repository_root / license_path).resolve()
		if not absolute_license.is_file():
			raise ThemeError(f"bundled font license is missing: {license_path}")
		with absolute_license.open("rb") as license_file:
			license_digest = hashlib.file_digest(license_file, "sha256").hexdigest()
		if license_digest != license["sha256"]:
			raise ThemeError(f"bundled font license hash differs: {license_path}")
		upstream = entry["upstream"]
		if not upstream["url"].startswith("https://") or not upstream["revision"]:
			raise ThemeError(f"font provenance has invalid upstream source: {profile.relative_path}")
		provenance.append(FontProvenance(profile, upstream["url"], upstream["revision"],
			license_path, license["sha256"]))
	if len(entries) != len(provenance):
		raise ThemeError("bundled font provenance has unregistered font records")
	return tuple(provenance)


#============================================
def validate_font_face(profile: FontFaceProfile,
		repository_root: pathlib.Path = REPOSITORY_ROOT) -> FontMetricProfile:
	"""Verify one declared face and read its intrinsic metrics without fallback lookup."""
	path = font_asset_path(profile, repository_root)
	if not path.is_file():
		raise ThemeError(f"bundled font asset is missing: {profile.relative_path}")
	with path.open("rb") as asset_file:
		digest = hashlib.file_digest(asset_file, "sha256").hexdigest()
	if digest != profile.sha256:
		raise ThemeError(f"bundled font asset hash differs: {profile.relative_path}")
	try:
		# Pillow proves this exact indexed face is rasterizable without host-font lookup.
		pillow_face = PIL.ImageFont.truetype(str(path), 16, index=profile.face_index)
		pillow_face.getbbox("Ag")
		with fontTools.ttLib.TTFont(path, fontNumber=profile.face_index, lazy=True) as font:
			head = font["head"]
			hhea = font["hhea"]
			family = font_name(font, 16, 1)
			style = font_name(font, 17, 2)
			if family != profile.family or font_style_flags(style) != (profile.bold, profile.italic):
				raise ThemeError(f"bundled font identity differs: {profile.relative_path}")
			metrics = FontMetricProfile(profile, head.unitsPerEm, hhea.ascent, hhea.descent)
	except (OSError, fontTools.ttLib.TTLibError) as error:
		raise ThemeError(f"bundled font asset is unreadable: {profile.relative_path}") from error
	if metrics.units_per_em <= 0 or metrics.ascender <= 0 or metrics.descender >= 0:
		raise ThemeError(f"bundled font metrics are invalid: {profile.relative_path}")
	return metrics


#============================================
def validated_font_metrics(
		profiles: tuple[FontFaceProfile, ...] = FONT_FACE_PROFILES,
		repository_root: pathlib.Path = REPOSITORY_ROOT) -> tuple[FontMetricProfile, ...]:
	"""Return all verified profile metrics; system fonts are never a substitute."""
	metrics = tuple(validate_font_face(profile, repository_root) for profile in profiles)
	keys = tuple((item.face.family, item.face.bold, item.face.italic) for item in metrics)
	if len(set(keys)) != len(keys):
		raise ThemeError("bundled font faces must have unique family and style keys")
	return metrics


#============================================
def select_font_face(family: str, bold: bool = False,
		italic: bool = False) -> FontFaceProfile:
	"""Select exactly one bundled run face or fail before any adapter can substitute."""
	matches = tuple(profile for profile in FONT_FACE_PROFILES
		if (profile.family, profile.bold, profile.italic) == (family, bold, italic))
	if len(matches) != 1:
		raise ThemeError(f"no bundled font face for {family!r}, bold={bold}, italic={italic}")
	return matches[0]


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
	frame = matches[0]
	if frame.attrib.get(qname("presentation", "placeholder")) != "true":
		raise ThemeError(f"theme master {presentation_class} frame must be a placeholder")
	return frame


#============================================
def frame_geometry(frame: xml.etree.ElementTree.Element) -> FrameGeometry:
	"""Read one master-placeholder rectangle in physical ODF centimeters."""
	geometry = FrameGeometry(
		nonnegative_length_value(frame.attrib[qname("svg", "x")], "cm"),
		nonnegative_length_value(frame.attrib[qname("svg", "y")], "cm"),
		length_value(frame.attrib[qname("svg", "width")], "cm"),
		length_value(frame.attrib[qname("svg", "height")], "cm"),
	)
	return geometry


#============================================
def outline_style_names(styles_root: xml.etree.ElementTree.Element) -> tuple[str, ...]:
	"""Return the complete ordinary outline style hierarchy in native order."""
	names = tuple(f"Default-outline{level}" for level in range(1, 10))
	for name in names:
		presentation_style(styles_root, name)
	return names


#============================================
def effective_text_properties(styles_root: xml.etree.ElementTree.Element,
		style: xml.etree.ElementTree.Element, name: str) -> dict[str, str]:
	"""Resolve inherited presentation text properties from child through parent styles."""
	properties: dict[str, str] = {}
	current = style
	current_name = name
	while True:
		text_properties = current.find("style:text-properties", NS)
		if text_properties is not None:
			for attribute, value in text_properties.attrib.items():
				if attribute not in properties:
					properties[attribute] = value
		parent_name = current.attrib.get(qname("style", "parent-style-name"))
		if parent_name is None:
			break
		current = presentation_style(styles_root, parent_name)
		current_name = parent_name
	if not properties:
		raise ThemeError(f"theme style is missing inherited text properties: {current_name}")
	return properties


#============================================
def effective_paragraph_properties(styles_root: xml.etree.ElementTree.Element,
		style: xml.etree.ElementTree.Element, name: str) -> dict[str, str]:
	"""Resolve inherited presentation paragraph properties from child through parent styles."""
	properties: dict[str, str] = {}
	current = style
	current_name = name
	while True:
		paragraph_properties = current.find("style:paragraph-properties", NS)
		if paragraph_properties is not None:
			for attribute, value in paragraph_properties.attrib.items():
				if attribute not in properties:
					properties[attribute] = value
		parent_name = current.attrib.get(qname("style", "parent-style-name"))
		if parent_name is None:
			break
		current = presentation_style(styles_root, parent_name)
		current_name = parent_name
	if not properties:
		raise ThemeError(f"theme style is missing inherited paragraph properties: {current_name}")
	return properties


#============================================
def ordinary_line_spacing(properties: dict[str, str], name: str) -> float:
	"""Read the ordinary outline line-height as an exact positive em multiplier."""
	raw_value = properties.get(qname("fo", "line-height"))
	if raw_value is None or not raw_value.endswith("%"):
		raise ThemeError(f"theme outline style must define percentage line height: {name}")
	value = float(raw_value[:-1]) / 100.0
	if value != ORDINARY_LINE_SPACING_EM:
		raise ThemeError(
			f"theme outline style must use {ORDINARY_LINE_SPACING_EM:.2f}em line height: {name}")
	return value


#============================================
def presentation_font_sizes(properties: dict[str, str], name: str) -> tuple[float, float, float]:
	"""Read the Western, Asian, and complex point sizes from resolved properties."""
	sizes = tuple(length_value(properties[attribute], "pt") for attribute in (
		qname("fo", "font-size"), qname("style", "font-size-asian"),
		qname("style", "font-size-complex"),
	))
	if len(sizes) != 3:
		raise ThemeError(f"theme style is missing complete font sizes: {name}")
	return sizes


#============================================
def fixed_shrink_only(style: xml.etree.ElementTree.Element, name: str) -> None:
	"""Require the bounded native overflow mode for generated standard frames."""
	properties = style.find("style:graphic-properties", NS)
	if properties is None:
		raise ThemeError(f"theme style is missing graphic properties: {name}")
	if properties.attrib.get(qname("draw", "auto-grow-height")) != "false" or \
			properties.attrib.get(qname("draw", "fit-to-size")) != "false" or \
			properties.attrib.get(qname("style", "shrink-to-fit")) != "true":
		raise ThemeError(f"theme style must use fixed shrink-only overflow: {name}")


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
	validate_font_manifest()
	font_metrics = validated_font_metrics()
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
	title_frame_element = master_frame(master, "title")
	title_style_name = title_frame_element.attrib[qname("presentation", "style-name")]
	title_style = presentation_style(styles_root, title_style_name)
	title_text = title_style.find("style:text-properties", NS)
	title_paragraph = title_style.find("style:paragraph-properties", NS)
	if title_text is None or title_paragraph is None:
		raise ThemeError("theme title style is missing text or paragraph properties")
	title_properties = effective_text_properties(styles_root, title_style, title_style_name)
	title_font = title_properties[qname("fo", "font-family")].strip("'")
	title_sizes = presentation_font_sizes(title_properties, title_style_name)
	if title_paragraph.attrib.get(qname("fo", "text-align")) != "center":
		raise ThemeError("theme title style must be centered")
	if title_font != "OpenDyslexic":
		raise ThemeError("theme title style must use OpenDyslexic")
	if title_sizes != (36.0, 36.0, 36.0):
		raise ThemeError("theme title style must use 36 pt")
	fixed_shrink_only(title_style, title_style_name)
	outline_frame_element = master_frame(master, "outline")
	outline_style_name = outline_frame_element.attrib[qname("presentation", "style-name")]
	outline_style = presentation_style(styles_root, outline_style_name)
	style_names = outline_style_names(styles_root)
	if outline_style_name != style_names[0]:
		raise ThemeError("theme outline placeholder must use Default-outline1")
	for name in style_names:
		style = presentation_style(styles_root, name)
		properties = effective_text_properties(styles_root, style, name)
		paragraph_properties = effective_paragraph_properties(styles_root, style, name)
		if properties[qname("fo", "font-family")].strip("'") != "OpenDyslexic":
			raise ThemeError(f"theme outline style must inherit OpenDyslexic: {name}")
		if presentation_font_sizes(properties, name) != (28.0, 28.0, 28.0):
			raise ThemeError(f"theme outline style must use 28 pt: {name}")
		ordinary_line_spacing(paragraph_properties, name)
	fixed_shrink_only(outline_style, outline_style_name)
	levels = list_level_styles(outline_style, logical_pixels_per_cm)
	top_band_height = length_value(band.attrib[qname("svg", "height")], "cm") * logical_pixels_per_cm
	theme = PresentationTheme(
		resolved_path, master_name, slide_width_cm, slide_height_cm, emu_per_logical_pixel,
		top_band_height, start_color, end_color, title_font, frame_geometry(title_frame_element),
		frame_geometry(outline_frame_element), title_style_name, style_names, title_sizes[0],
		28.0, ORDINARY_LINE_SPACING_EM, 30.0, 24.0, OverflowPolicy.SHRINK_ONLY, levels, font_metrics,
	)
	return theme


#============================================
@functools.cache
def default_theme() -> PresentationTheme:
	"""Return the immutable repository theme loaded from its ODP template."""
	return load_theme(DEFAULT_TEMPLATE_PATH)
