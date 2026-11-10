"""Fast XML and ZIP contract tests for the native ODP package skeleton."""

# Standard Library
import colorsys
import dataclasses
import io
import pathlib
import zipfile

import fontTools.ttLib
import lxml.etree
import PIL.Image
import pytest

import slide_lib.djot_parser
import slide_lib.layout_engine
import slide_lib.layout_content as content
import slide_lib.layout_model as model
import slide_lib.layout_primitives as primitives
import slide_lib.native_model
import slide_lib.odp_animation
import slide_lib.odf_package as package
import slide_lib.odp_export as exporter
import slide_lib.odp_text
import slide_lib.presentation_theme
import slide_lib.table_formatting


def source() -> slide_lib.native_model.SourceLocation:
	return slide_lib.native_model.SourceLocation(pathlib.Path("inline.djot"), 1)


def frame_text() -> primitives.FrameTextProperties:
	return primitives.FrameTextProperties(primitives.Insets(0.0, 0.0, 0.0, 0.0),
		primitives.VerticalAlignment.TOP, primitives.TextWrap.WRAP,
		primitives.OverflowPolicy.SHRINK)


def relative_luminance(hex_color: str) -> float:
	"""Measure sRGB surfaces with the WCAG relative-luminance formula."""
	channels = [int(hex_color.lstrip("#")[index:index + 2], 16) / 255 for index in (0, 2, 4)]
	linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
		for value in channels]
	result = sum(value * weight for value, weight in zip(linear, (0.2126, 0.7152, 0.0722)))
	return result


def deck() -> model.LayoutDeck:
	rectangle = primitives.LogicalRectangle(0.0, 0.0, 500.0, 300.0)
	slot = model.LayoutSlot("body", primitives.PlaceholderKind.OUTLINE,
		primitives.PresentationRole.OUTLINE, rectangle, 0,
		primitives.PlaceholderProperties(primitives.StyleRole.OUTLINE, frame_text()))
	topology = primitives.PlaceholderTopology("one-panel", (slot.topology_member(),))
	identity = model.LayoutIdentity("one-panel", topology)
	typography = primitives.Typography(primitives.StyleRole.OUTLINE, "Atkinson Hyperlegible Next", 28.0, 28.0, 24.0)
	paragraph = content.TextParagraph((content.TextRun("Body", content.RunStyle("Atkinson Hyperlegible Next", "ink")),),
		typography, primitives.ParagraphProperties(primitives.HorizontalAlignment.START, 0.0, 0.0,
			36.4, 0.0, 0.0, 0.0, ()))
	item = model.LayoutObject("body", primitives.PresentationRole.OUTLINE,
		primitives.StyleRole.OUTLINE, rectangle, primitives.ObjectLayer.LAYOUT, 0, 0,
		content.TextContent((paragraph,)), frame_text(), "body", "body",
		primitives.PlaceholderKind.OUTLINE, source())
	slide = model.LayoutSlide(model.SlideIdentity("slide-1", 0, source()), identity,
		(slot,), (item,), ())
	return model.LayoutDeck(model.DeckIdentity("deck", pathlib.Path("inline.djot")),
		primitives.LogicalCanvas(), (), (slide,))


def xml(value: str) -> bytes:
	return value.encode("utf-8")


def table_cell_properties(root: lxml.etree._Element) -> list[dict[str, str]]:
	"""Resolve each native cell's formatting through its actual style reference."""
	styles = {style.attrib[f"{{{exporter.STYLE_NS}}}name"]: style
		for style in root.findall(f".//{{{exporter.STYLE_NS}}}style")}
	return [styles[cell.attrib[f"{{{slide_lib.odp_text.TABLE_NS}}}style-name"]].find(
		f"{{{exporter.STYLE_NS}}}table-cell-properties").attrib
		for cell in root.findall(f".//{{{slide_lib.odp_text.TABLE_NS}}}table-cell")]


def payloads() -> dict[str, bytes]:
	items = {
		"mimetype": package.ODP_MIMETYPE.encode("ascii"),
		"content.xml": xml('<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" office:version="1.3"/>'),
		"styles.xml": xml('<office:document-styles xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" office:version="1.3"/>'),
		"settings.xml": xml('<office:document-settings xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" office:version="1.3"/>'),
		"meta.xml": xml('<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" office:version="1.3"/>'),
	}
	items[package.MANIFEST_NAME] = exporter._manifest_xml(items)
	return items


def template(path: pathlib.Path) -> pathlib.Path:
	with zipfile.ZipFile(slide_lib.presentation_theme.DEFAULT_TEMPLATE_PATH) as source:
		items = {info.filename: source.read(info.filename) for info in source.infolist()
			if not info.is_dir()}
	root = package.parse_xml(items["styles.xml"], "styles.xml")
	styles = root.find(f"{{{exporter.OFFICE_NS}}}styles")
	lxml.etree.SubElement(styles, f"{{{exporter.OFFICE_NS}}}annotation", {
		f"{{{exporter.XLINK_NS}}}href": "Pictures/theme.png",
	})
	items["styles.xml"] = exporter._XML_DECLARATION + lxml.etree.tostring(root, encoding="utf-8")
	items["Pictures/theme.png"] = b"theme image"
	items[package.MANIFEST_NAME] = exporter._manifest_xml(items)
	with zipfile.ZipFile(path, "w") as archive:
		for name, value in items.items():
			archive.writestr(name, value, compress_type=zipfile.ZIP_STORED)
	return path


def test_write_odp_replaces_content_and_preserves_reachable_template_resource(tmp_path: pathlib.Path) -> None:
	template_path = template(tmp_path / "theme.otp")
	theme = dataclasses.replace(slide_lib.presentation_theme.default_theme(), template_path=template_path)
	layout_deck = deck()
	layout_deck = dataclasses.replace(layout_deck, slides=(dataclasses.replace(
		layout_deck.slides[0], hidden=True),))
	destination = exporter.write_odp(layout_deck, theme, tmp_path / "deck.odp")
	package.validate_package(destination, ".odp", package.ODP_MIMETYPE, package.REQUIRED_ODP_MEMBERS)
	with zipfile.ZipFile(destination) as archive:
		members = archive.infolist()
		assert members[0].filename == "mimetype" and members[0].compress_type == zipfile.ZIP_STORED
		assert archive.read("Pictures/theme.png") == b"theme image"
		assert b'draw:name="slide-1"' in archive.read("content.xml")
		root = package.parse_xml(archive.read("content.xml"), "content.xml")
		page = root.find(f".//{exporter._qname(exporter.DRAW_NS, 'page')}")
		assert page is not None
		page_style = page.get(exporter._qname(exporter.DRAW_NS, "style-name"))
		styles = root.findall(f".//{exporter._qname(exporter.STYLE_NS, 'style')}")
		hidden_style = next(style for style in styles
			if style.get(exporter._qname(exporter.STYLE_NS, "name")) == page_style)
		properties = hidden_style.find(exporter._qname(exporter.STYLE_NS,
			"drawing-page-properties"))
		assert properties is not None and properties.get(
			exporter._qname(exporter.PRESENTATION_NS, "visibility")) == "hidden"
		package.validate_odp_members({info.filename: archive.read(info.filename) for info in members})


def test_write_odp_embeds_and_selects_each_validated_font_face(tmp_path: pathlib.Path) -> None:
	"""Editable text styles select deterministic embedded resources for every supported face."""
	layout_deck = deck()
	item = layout_deck.slides[0].objects[0]
	styles = tuple(content.TextRun(str(index), content.RunStyle(profile.family, "ink",
		bold=profile.bold, italic=profile.italic)) for index, profile in enumerate(
		slide_lib.presentation_theme.FONT_FACE_PROFILES, start=1))
	paragraph = dataclasses.replace(item.content.paragraphs[0], inlines=styles)
	updated_item = dataclasses.replace(item, content=content.TextContent((paragraph,)))
	updated_deck = dataclasses.replace(layout_deck, slides=(dataclasses.replace(
		layout_deck.slides[0], objects=(updated_item,)),))
	output = exporter.write_odp(updated_deck, slide_lib.presentation_theme.default_theme(),
		tmp_path / "embedded.odp")
	with zipfile.ZipFile(output) as archive:
		root = package.parse_xml(archive.read("content.xml"), "content.xml")
		manifest = package.manifest_file_targets(archive.read(package.MANIFEST_NAME))
		faces = slide_lib.presentation_theme.odf_font_faces()
		assert all(face.package_member in archive.namelist() and face.package_member in manifest
			for face in faces)
		license_payloads, _license_media_types = \
			slide_lib.presentation_theme.odf_font_license_payloads()
		assert set(license_payloads) <= set(archive.namelist()) and set(license_payloads) <= manifest
		assert all(archive.read(member) == payload for member, payload in license_payloads.items())
		manifest_root = package.parse_xml(archive.read(package.MANIFEST_NAME), package.MANIFEST_NAME)
		manifest_media = {element.attrib[package.MANIFEST_FULL_PATH]: element.attrib[
			f"{{{exporter.MANIFEST_NS}}}media-type"]
			for element in manifest_root.findall(f".//{package.MANIFEST_FILE_ENTRY}")}
		assert all(manifest_media[face.package_member] == face.media_type for face in faces)
		assert all(manifest_media[member] == "text/plain" for member in license_payloads)
		declarations = {element.attrib[f"{{{exporter.STYLE_NS}}}name"]: element
			for element in root.findall(f".//{{{exporter.STYLE_NS}}}font-face")}
		assert set(declarations) == {face.odf_name for face in faces}
		for face in faces:
			assert face.embedded_family == face.profile.family
			assert archive.read(face.package_member) == \
				slide_lib.presentation_theme.font_asset_path(face.profile).read_bytes()
			uri = declarations[face.odf_name].find(
				f"{{{exporter.SVG_NS}}}font-face-src/{{{exporter.SVG_NS}}}font-face-uri")
			assert uri is not None and uri.attrib[f"{{{exporter.XLINK_NS}}}href"] == face.package_member
			assert uri.find(f"{{{exporter.SVG_NS}}}font-face-format").attrib[
				f"{{{exporter.SVG_NS}}}string"] == face.format_name
			with fontTools.ttLib.TTFont(io.BytesIO(archive.read(face.package_member))) as font:
				assert slide_lib.presentation_theme.font_name(font, 16, 1) == face.embedded_family
		font_names = {element.attrib[f"{{{exporter.STYLE_NS}}}font-name"]
			for element in root.findall(f".//{{{exporter.STYLE_NS}}}text-properties")}
		assert font_names == {face.odf_name for face in faces}
		font_families = {element.attrib[f"{{{exporter.FO_NS}}}font-family"]
			for element in root.findall(f".//{{{exporter.STYLE_NS}}}text-properties")}
		assert font_families == {face.embedded_family for face in faces}
		style_properties = {}
		for element in root.findall(f".//{{{exporter.STYLE_NS}}}style"):
			properties = element.find(f"{{{exporter.STYLE_NS}}}text-properties")
			if properties is not None:
				style_properties[element.attrib[f"{{{exporter.STYLE_NS}}}name"]] = properties.attrib
		for index, face in enumerate(faces[:4], start=1):
			span = next(element for element in root.findall(f".//{{{exporter.TEXT_NS}}}span")
				if element.text == str(index))
			properties = style_properties[span.attrib[f"{{{exporter.TEXT_NS}}}style-name"]]
			assert properties[f"{{{exporter.STYLE_NS}}}font-name"] == face.odf_name and \
				properties[f"{{{exporter.FO_NS}}}font-family"] == face.embedded_family
		for index, face in enumerate(faces[4:], start=5):
			span = next(element for element in root.findall(f".//{{{exporter.TEXT_NS}}}span")
				if element.text == str(index))
			properties = style_properties[span.attrib[f"{{{exporter.TEXT_NS}}}style-name"]]
			assert properties[f"{{{exporter.STYLE_NS}}}font-name"] == face.odf_name and \
				properties[f"{{{exporter.FO_NS}}}font-family"] == face.embedded_family


@pytest.mark.parametrize("literal,resolved_size", [(False, None), (True, None), (True, 12.0)])
def test_linked_text_nests_destination_inside_its_styled_span(literal: bool, resolved_size: float | None) -> None:
	"""LibreOffice receives a visible linked label within its resolved text style."""
	layout_deck = deck()
	item = layout_deck.slides[0].objects[0]
	label = "https://example.test/course" if literal else "Course website"
	family = "IBM Plex Sans Condensed" if literal else "Atkinson Hyperlegible Next"
	linked_run = content.TextRun(label, content.RunStyle(family, "24578F",
		underline=True, link_url="https://example.test/course", literal_url=literal, size_pt=resolved_size))
	paragraph = dataclasses.replace(item.content.paragraphs[0], inlines=(linked_run,))
	updated_item = dataclasses.replace(item, content=content.TextContent((paragraph,)))
	updated_deck = dataclasses.replace(layout_deck, slides=(dataclasses.replace(
		layout_deck.slides[0], objects=(updated_item,)),))
	root = package.parse_xml(exporter._content_xml(updated_deck,
		slide_lib.presentation_theme.default_theme(), exporter._layout_names(updated_deck), {}),
		"content.xml")
	span = root.find(f".//{{{exporter.TEXT_NS}}}span")
	link = span.find(f"{{{exporter.TEXT_NS}}}a")
	assert link is not None and link.text == label
	assert link.attrib[f"{{{exporter.XLINK_NS}}}href"] == "https://example.test/course" and \
		span.attrib[f"{{{exporter.TEXT_NS}}}style-name"].startswith("DjotText")
	name = span.attrib[f"{{{exporter.TEXT_NS}}}style-name"]
	style = next(element for element in root.findall(f".//{{{exporter.STYLE_NS}}}style")
		if element.attrib[f"{{{exporter.STYLE_NS}}}name"] == name)
	properties = style.find(f"{{{exporter.STYLE_NS}}}text-properties")
	expected_size = resolved_size if resolved_size is not None else paragraph.typography.selected_size_pt - (2 if literal else 0)
	assert float(properties.attrib[f"{{{exporter.FO_NS}}}font-size"].removesuffix("pt")) == expected_size
	assert properties.attrib[f"{{{exporter.FO_NS}}}font-family"] == family


def test_text_frames_preserve_the_compiler_selected_size() -> None:
	"""Text-frame styles keep the compiler's measured point size authoritative."""
	root = package.parse_xml(exporter._content_xml(deck(),
		slide_lib.presentation_theme.default_theme(), exporter._layout_names(deck()), {}), "content.xml")
	properties = root.find(f".//{{{exporter.STYLE_NS}}}graphic-properties").attrib
	assert properties[f"{{{exporter.STYLE_NS}}}shrink-to-fit"] == "false"


def test_picture_frames_use_the_compiler_resolved_display_rectangle() -> None:
	"""Contained pictures retain their aspect-correct displayed bounds in ODP."""
	layout_deck = deck()
	theme = slide_lib.presentation_theme.default_theme()
	text_item = layout_deck.slides[0].objects[0]
	displayed = primitives.LogicalRectangle(50.0, 60.0, 300.0, 100.0)
	picture = content.PictureContent("picture.png", content.PicturePlacement(
		text_item.rectangle, displayed, primitives.PictureFit.CONTAIN,
		primitives.CropInsets(0.0, 0.0, 0.0, 0.0)),
		primitives.ObjectAccessibility("Picture", "A wide illustration"))
	picture_item = dataclasses.replace(text_item, content=picture, frame_text=None,
		presentation_member_id=None, placeholder_kind=primitives.PlaceholderKind.NONE)
	picture_slide = dataclasses.replace(layout_deck.slides[0], objects=(picture_item,))
	picture_deck = dataclasses.replace(layout_deck, slides=(picture_slide,))
	root = package.parse_xml(exporter._content_xml(picture_deck, theme,
		exporter._layout_names(picture_deck), {("slide-1", "body"): "Pictures/picture.png"}),
		"content.xml")
	picture_attributes = root.find(f".//{{{exporter.DRAW_NS}}}frame").attrib
	text_attributes = exporter._frame_attributes(text_item, layout_deck, theme, "Text", {})
	assert (picture_attributes[f"{{{exporter.SVG_NS}}}x"],
		picture_attributes[f"{{{exporter.SVG_NS}}}y"],
		picture_attributes[f"{{{exporter.SVG_NS}}}width"],
		picture_attributes[f"{{{exporter.SVG_NS}}}height"]) == (
		exporter._cm_x(displayed.x, layout_deck, theme),
		exporter._cm_y(displayed.y, layout_deck, theme),
		exporter._cm_x(displayed.width, layout_deck, theme),
		exporter._cm_y(displayed.height, layout_deck, theme))
	assert text_attributes[f"{{{exporter.SVG_NS}}}width"] == exporter._cm_x(
		text_item.rectangle.width, layout_deck, theme)


def test_drawing_page_style_hides_master_chrome() -> None:
	"""Every emitted page suppresses master date, footer, and page-number placeholders."""
	layout_deck = deck()
	root = package.parse_xml(exporter._content_xml(layout_deck,
		slide_lib.presentation_theme.default_theme(), exporter._layout_names(layout_deck), {}),
		"content.xml")
	properties = root.find(f".//{{{exporter.STYLE_NS}}}drawing-page-properties").attrib
	assert (properties[f"{{{exporter.PRESENTATION_NS}}}background-visible"],
		properties[f"{{{exporter.PRESENTATION_NS}}}background-objects-visible"],
		properties[f"{{{exporter.PRESENTATION_NS}}}display-page-number"],
		properties[f"{{{exporter.PRESENTATION_NS}}}display-footer"],
		properties[f"{{{exporter.PRESENTATION_NS}}}display-date-time"]) == (
		"true", "true", "false", "false", "false")


@pytest.mark.parametrize("color_theme", ("genetics", "biotechnology"))
@pytest.mark.parametrize("layout", (
	"title-slide", "bookend", "definitions", "reference", "section", "subsection",
	"subsubsection", "question-ask", "prompt", "theend", "big-image"))
def test_decoration_is_master_owned_and_text_remains_on_slide(
		tmp_path: pathlib.Path, color_theme: str, layout: str) -> None:
	"""Decorative frames cannot intercept selection of slide text."""
	source_path = tmp_path / "title.djot"
	if layout == "title-slide":
		text = "# Lecture 05D\n\n## Probability Concepts\n\n## Chapter 5\n\n"
		text += "## Dr. Neil Voss\n\n## Sept 29, 2026\n"
		expected = ["Lecture 05D", "Probability Concepts", "Chapter 5", "Dr. Neil Voss", "Sept 29, 2026"]
	elif layout == "theend":
		text = "# THE END\n"
		expected = ["THE", "END"]
	elif layout == "prompt":
		text = "# Discussion\n\n@prompt\n\nWhat is your rule?\n\n@examples\n\n- Give one example.\n"
		expected = ["Discussion", "What is your rule?", "Give one example."]
	elif layout == "big-image":
		PIL.Image.new("RGB", (32, 18), "blue").save(tmp_path / "figure.png")
		text = "@image\n\n![Figure](figure.png)\n\n@caption\n\nCaption words.\n"
		expected = ["Caption words."]
	else:
		text = "# Framed Heading\n"
		expected = ["Framed Heading"]
		if layout in ("bookend", "definitions", "reference"):
			text += "\n@body\n\n" + ("- " if layout == "definitions" else "")
			text += "Term: Its definition.\n"
			expected.append("Term: Its definition.")
		if layout == "reference":
			expected.append("For reference - not covered in class.")
	source_path.write_text(f"=== layout: {layout}\n\n" + text +
		"\n=== layout: one-panel\n# Teaching\n@body\nText\n", encoding="utf-8")
	theme = slide_lib.presentation_theme.default_theme(color_theme)
	plan = slide_lib.layout_engine.compile_layout_deck(
		slide_lib.djot_parser.parse_deck(source_path), theme).plan
	names = exporter._layout_names(plan)
	pictures = {(slide.identity.slide_id, item.object_id): "Pictures/figure.png"
		for slide in plan.slides for item in slide.objects if isinstance(item.content, content.PictureContent)}
	root = package.parse_xml(exporter._content_xml(plan, theme, names, pictures), "content.xml")
	with zipfile.ZipFile(theme.template_path) as archive:
		styles = package.parse_xml(exporter._styles_xml(
			archive.read("styles.xml"), plan, theme, names), "styles.xml")
	pages = root.findall(f".//{{{exporter.DRAW_NS}}}page")
	master_name = pages[0].attrib[f"{{{exporter.DRAW_NS}}}master-page-name"]
	assert master_name != pages[1].attrib[f"{{{exporter.DRAW_NS}}}master-page-name"]
	master = next(item for item in styles.findall(f".//{{{exporter.STYLE_NS}}}master-page")
		if item.attrib[f"{{{exporter.STYLE_NS}}}name"] == master_name)
	decorations = {item.object_id for item in plan.slides[0].objects
		if item.origin is primitives.LayoutObjectOrigin.THEME}
	master_objects = {item.attrib.get(f"{{{exporter.DRAW_NS}}}name"): item for item in master}
	assert decorations and decorations <= master_objects.keys()
	assert all(master_objects[name].attrib[f"{{{exporter.DRAW_NS}}}layer"] == "backgroundobjects"
		for name in decorations)
	background_z = max((int(item.get(f"{{{exporter.DRAW_NS}}}z-index", str(index)))
		for index, item in enumerate(master)
		if item.get(f"{{{exporter.DRAW_NS}}}name") not in decorations), default=-1)
	assert all(int(master_objects[name].attrib[f"{{{exporter.DRAW_NS}}}z-index"]) > background_z
		for name in decorations)
	assert not decorations.intersection(item.attrib.get(f"{{{exporter.DRAW_NS}}}name")
		for item in pages[0])
	paragraphs = pages[0].findall(f".//{{{exporter.TEXT_NS}}}p")
	assert ["".join(item.itertext()) for item in paragraphs] == expected
	if layout == "prompt":
		markers = root.findall(f".//{{{exporter.TEXT_NS}}}list-level-style-bullet/"
			f"{{{exporter.STYLE_NS}}}text-properties")
		assert markers and all(item.attrib[f"{{{exporter.FO_NS}}}color"] == "#172033"
			for item in markers)
	for shape in master.findall(f"{{{exporter.DRAW_NS}}}rect"):
		if shape.attrib.get(f"{{{exporter.DRAW_NS}}}name") not in decorations:
			continue
		style_name = shape.attrib[f"{{{exporter.DRAW_NS}}}style-name"]
		style = next(item for item in styles.findall(f".//{{{exporter.STYLE_NS}}}style")
			if item.attrib.get(f"{{{exporter.STYLE_NS}}}name") == style_name)
		properties = style.find(f"{{{exporter.STYLE_NS}}}graphic-properties")
		assert properties.attrib[f"{{{exporter.DRAW_NS}}}fill"] == (
			"solid" if layout in ("title-slide", "big-image", "subsection", "subsubsection", "prompt") else "none")


def test_djot_inline_formatting_survives_editable_export(tmp_path: pathlib.Path) -> None:
	"""Standard Djot marks must style editable text instead of leaking delimiter characters."""
	source_path = tmp_path / "formatting.djot"
	source_path.write_text("=== layout: one-panel\n# Formatting\n@body\n\n"
		"_italic_ {*bold*} {_also italic_} *also bold* `code` H~2~O 20^th^\n\n"
		"{=Shark Talk presentations=}\n\n{+insert+} {-delete-}\n\n"
		"{=*bold highlight* and {+underlined+}=}\n", encoding="utf-8")
	theme = slide_lib.presentation_theme.default_theme()
	plan = slide_lib.layout_engine.compile_layout_deck(
		slide_lib.djot_parser.parse_deck(source_path), theme).plan
	root = package.parse_xml(exporter._content_xml(
		plan, theme, exporter._layout_names(plan), {}), "content.xml")
	styles = {element.attrib[f"{{{exporter.STYLE_NS}}}name"]:
		element.find(f"{{{exporter.STYLE_NS}}}text-properties").attrib
		for element in root.findall(f".//{{{exporter.STYLE_NS}}}style")
		if element.find(f"{{{exporter.STYLE_NS}}}text-properties") is not None}
	properties = {span.text: styles[span.attrib[f"{{{exporter.TEXT_NS}}}style-name"]]
		for span in root.findall(f".//{{{exporter.TEXT_NS}}}span")}
	for label in ("italic", "also italic"):
		assert properties[label][f"{{{exporter.FO_NS}}}font-style"] == "italic"
	for label in ("bold", "also bold", "bold highlight"):
		assert properties[label][f"{{{exporter.FO_NS}}}font-weight"] == "bold"
	assert "Mono" in properties["code"][f"{{{exporter.FO_NS}}}font-family"]
	assert properties["2"][f"{{{exporter.STYLE_NS}}}text-position"].startswith("sub ")
	assert properties["th"][f"{{{exporter.STYLE_NS}}}text-position"].startswith("super ")
	for label in ("Shark Talk presentations", "bold highlight", "underlined"):
		assert properties[label][f"{{{exporter.FO_NS}}}background-color"].startswith("#")
	for label in ("insert", "underlined"):
		assert properties[label][f"{{{exporter.STYLE_NS}}}text-underline-style"] == "solid"
	assert properties["delete"][f"{{{exporter.STYLE_NS}}}text-line-through-style"] == "solid"


@pytest.mark.parametrize("course", slide_lib.presentation_theme.color_theme_names())
def test_dividers_preserve_course_color_and_background_contrast(
		tmp_path: pathlib.Path, course: str) -> None:
	"""Prevent washed-out tints while preserving the agreed 2:1 background separation."""
	source_path = tmp_path / "transitions.djot"
	source_path.write_text(f"color-theme: {course}\n\n=== layout: section\n\n# Topic\n\n"
		"=== layout: subsection\n\n# Subtopic\n\n"
		"=== layout: subsubsection\n\n# Detail\n", encoding="utf-8")
	theme = slide_lib.presentation_theme.default_theme(course)
	plan = slide_lib.layout_engine.compile_layout_deck(
		slide_lib.djot_parser.parse_deck(source_path), theme).plan
	root = package.parse_xml(exporter._content_xml(
		plan, theme, exporter._layout_names(plan), {}), "content.xml")
	colors = []
	frame = next(item for item in plan.slides[0].objects
		if isinstance(item.content, content.ShapeContent))
	assert frame.content.style.fill_role is None
	for page in root.findall(f".//{{{exporter.DRAW_NS}}}page"):
		style = next(style for style in root.findall(f".//{{{exporter.STYLE_NS}}}style")
			if style.attrib.get(f"{{{exporter.STYLE_NS}}}name") == page.attrib[f"{{{exporter.DRAW_NS}}}style-name"])
		colors.append(style.find(f"{{{exporter.STYLE_NS}}}drawing-page-properties").attrib[
			f"{{{exporter.DRAW_NS}}}fill-color"])
	palette = slide_lib.presentation_theme.course_color_theme(course)
	luminances = [0.0, *(relative_luminance(color) for color in colors), 1.0]
	for dark, light in zip(luminances, luminances[1:]):
		assert (light + 0.05) / (dark + 0.05) >= 2.0
	assert 1.05 / (relative_luminance(colors[0]) + 0.05) >= 5.5
	assert (relative_luminance(colors[2]) + 0.05) / 0.05 >= 5.5
	assert relative_luminance(colors[2]) < relative_luminance(palette.ultra_light_color) < 1
	assert theme.gradient_start_color == palette.medium_color
	palette_hls = [colorsys.rgb_to_hls(*(int(color.lstrip("#")[index:index + 2], 16) / 255
		for index in (0, 2, 4))) for color in (theme.accent_color, *colors, palette.ultra_light_color)]
	accent_hue, _, accent_saturation = palette_hls[0]
	for hue, _, saturation in palette_hls[1:]:
		# Broad tolerances allow 8-bit rounding without pinning the palette's exact hex values.
		hue_difference = abs(hue - accent_hue)
		assert min(hue_difference, 1 - hue_difference) < 0.01
		assert abs(saturation - accent_saturation) < 0.02
	assert plan.slides[1].surface.background_role is primitives.StyleRole.SUBSECTION
	assert plan.slides[2].surface.background_role is primitives.StyleRole.SUBSUBSECTION
	# The hierarchy must remain visible without relying only on hue differences.
	shapes = [next(item.content.kind for item in slide.objects
		if isinstance(item.content, content.ShapeContent)) for slide in plan.slides]
	assert shapes == [primitives.ShapeKind.ROUNDED_RECTANGLE,
		primitives.ShapeKind.RECTANGLE, primitives.ShapeKind.RECTANGLE]
	for slide in plan.slides:
		title = next(item for item in slide.objects if isinstance(item.content, content.TextContent))
		assert title.content.paragraphs[0].properties.horizontal_alignment is \
			primitives.HorizontalAlignment.CENTER
	for slide, ink, fill in zip(plan.slides[1:], ("000000", "FFFFFF"),
			(palette.light_color, palette.dark_color)):
		runs = [run for item in slide.objects if isinstance(item.content, content.TextContent)
			for paragraph in item.content.paragraphs for run in paragraph.inlines
			if isinstance(run, content.TextRun)]
		assert runs and all(run.style.foreground == ink for run in runs)
		panel = next(item for item in slide.objects if isinstance(item.content, content.ShapeContent))
		assert exporter._color_for(panel.content.style.fill_role, theme) == fill
		assert panel.rectangle.y + panel.rectangle.height / 2 == primitives.LOGICAL_SLIDE_HEIGHT / 2
	band = next(item.rectangle for item in plan.slides[1].objects
		if isinstance(item.content, content.ShapeContent))
	assert band.x == 0 and band.width == primitives.LOGICAL_SLIDE_WIDTH


def test_transition_surface_and_end_star_are_native_odf(tmp_path: pathlib.Path) -> None:
	"""LibreOffice receives the dark transition as a page style and the flourish as a vector."""
	source_path = tmp_path / "closer.djot"
	source_path.write_text("=== layout: theend\n\n# THE END\n", encoding="utf-8")
	theme = slide_lib.presentation_theme.default_theme()
	plan = slide_lib.layout_engine.compile_layout_deck(
		slide_lib.djot_parser.parse_deck(source_path), theme).plan
	root = package.parse_xml(exporter._content_xml(
		plan, theme, exporter._layout_names(plan), {}), "content.xml")
	with zipfile.ZipFile(theme.template_path) as archive:
		styles = package.parse_xml(exporter._styles_xml(
			archive.read("styles.xml"), plan, theme, exporter._layout_names(plan)), "styles.xml")
	page = root.find(f".//{{{exporter.DRAW_NS}}}page")
	page_style_name = page.attrib[f"{{{exporter.DRAW_NS}}}style-name"]
	page_style = next(style for style in root.findall(f".//{{{exporter.STYLE_NS}}}style")
		if style.attrib.get(f"{{{exporter.STYLE_NS}}}name") == page_style_name)
	properties = page_style.find(f"{{{exporter.STYLE_NS}}}drawing-page-properties").attrib
	master = next(item for item in styles.findall(f".//{{{exporter.STYLE_NS}}}master-page")
		if item.attrib[f"{{{exporter.STYLE_NS}}}name"] == page.attrib[
			f"{{{exporter.DRAW_NS}}}master-page-name"])
	star = next(shape for shape in master.findall(f"{{{exporter.DRAW_NS}}}custom-shape")
		if shape.find(f"{{{exporter.DRAW_NS}}}enhanced-geometry").attrib[
			f"{{{exporter.DRAW_NS}}}type"] == "star5")
	star_style_name = star.attrib[f"{{{exporter.DRAW_NS}}}style-name"]
	star_style = next(style for style in styles.findall(f".//{{{exporter.STYLE_NS}}}style")
		if style.attrib.get(f"{{{exporter.STYLE_NS}}}name") == star_style_name)
	star_properties = star_style.find(f"{{{exporter.STYLE_NS}}}graphic-properties").attrib
	rounded_rectangles = tuple(master.findall(f"{{{exporter.DRAW_NS}}}rect"))
	assert (properties[f"{{{exporter.DRAW_NS}}}fill"],
		properties[f"{{{exporter.DRAW_NS}}}fill-color"],
		properties[f"{{{exporter.PRESENTATION_NS}}}background-objects-visible"]) == (
		"solid", f"#{slide_lib.presentation_theme.course_color_theme(theme.color_theme_name).dark_color}", "true")
	assert {item.attrib[f"{{{exporter.DRAW_NS}}}name"] for item in master
		if item.tag.startswith(f"{{{exporter.DRAW_NS}}}")} == {
		"end-outer-frame", "end-inner-frame", "end-star"}
	assert star.find(f"{{{exporter.SVG_NS}}}title") is None
	assert star_properties[f"{{{exporter.DRAW_NS}}}opacity"] == "100%"
	assert rounded_rectangles and all(
		f"{{{exporter.DRAW_NS}}}corner-radius" in rectangle.attrib
		for rectangle in rounded_rectangles)


def test_cascade_reveal_targets_resolve_to_native_paragraph_ids(tmp_path: pathlib.Path) -> None:
	"""Every native ODF timing step targets an emitted editable paragraph identity."""
	source_path = tmp_path / "cascade.djot"
	source_path.write_text("=== layout: one-panel\n\n@body\n\n=> cascade appear\n"
		"- Parent\n\n  - Child\n- Second\n", encoding="utf-8")
	theme = slide_lib.presentation_theme.default_theme()
	plan = slide_lib.layout_engine.compile_layout_deck(
		slide_lib.djot_parser.parse_deck(source_path), theme).plan
	output = exporter.write_odp(plan, theme, tmp_path / "cascade.odp")
	with zipfile.ZipFile(output) as archive:
		root = package.parse_xml(archive.read("content.xml"), "content.xml")
	target_attribute = f"{{{slide_lib.odp_animation.SMIL_NS}}}targetElement"
	xml_id = "{http://www.w3.org/XML/1998/namespace}id"
	targets = [element.attrib[target_attribute] for element in root.findall(
		".//{urn:oasis:names:tc:opendocument:xmlns:animation:1.0}set")]
	ids = {element.attrib[xml_id] for element in root.iter() if xml_id in element.attrib}
	assert len(targets) == 2 and set(targets) <= ids


def test_object_reveal_target_is_a_native_rounded_answer_popup(tmp_path: pathlib.Path) -> None:
	"""The answer retains its reveal identity and native editable popup styling."""
	source_path = tmp_path / "multiple_choice.djot"
	source_path.write_text("=== layout: multiple-choice\n\n@question\n\nQuestion?\n\n"
		"- Choice A\n- Choice B\n\n@answer\n\nAnswer.\n", encoding="utf-8")
	theme = slide_lib.presentation_theme.default_theme()
	plan = slide_lib.layout_engine.compile_layout_deck(
		slide_lib.djot_parser.parse_deck(source_path), theme).plan
	output = exporter.write_odp(plan, theme, tmp_path / "multiple_choice.odp")
	with zipfile.ZipFile(output) as archive:
		root = package.parse_xml(archive.read("content.xml"), "content.xml")
	target_attribute = f"{{{slide_lib.odp_animation.SMIL_NS}}}targetElement"
	target = root.find(".//{urn:oasis:names:tc:opendocument:xmlns:animation:1.0}set").attrib[target_attribute]
	xml_id = "{http://www.w3.org/XML/1998/namespace}id"
	answer = next(item for item in root.iter() if item.attrib.get(xml_id) == target)
	assert answer.tag == f"{{{exporter.DRAW_NS}}}rect"
	assert answer.attrib[f"{{{exporter.PRESENTATION_NS}}}class"] == "object"
	radius = answer.attrib[f"{{{exporter.DRAW_NS}}}corner-radius"]
	assert float(radius.removesuffix("pt")) == 16
	style_name = answer.attrib[f"{{{exporter.PRESENTATION_NS}}}style-name"]
	style = next(item for item in root.findall(f".//{{{exporter.STYLE_NS}}}style")
		if item.attrib[f"{{{exporter.STYLE_NS}}}name"] == style_name)
	properties = style.find(f"{{{exporter.STYLE_NS}}}graphic-properties").attrib
	assert properties[f"{{{exporter.DRAW_NS}}}fill-color"] == "#F2F3F5"
	assert properties[f"{{{exporter.SVG_NS}}}stroke-color"] == "#7B1E2B"
	assert properties[f"{{{exporter.DRAW_NS}}}stroke"] == "solid"
	span = answer.find(f".//{{{exporter.TEXT_NS}}}span")
	text_style_name = span.attrib[f"{{{exporter.TEXT_NS}}}style-name"]
	text_style = next(item for item in root.findall(f".//{{{exporter.STYLE_NS}}}style")
		if item.attrib[f"{{{exporter.STYLE_NS}}}name"] == text_style_name)
	text_properties = text_style.find(f"{{{exporter.STYLE_NS}}}text-properties").attrib
	assert text_properties[f"{{{exporter.FO_NS}}}color"] == "#7B1E2B"


def test_native_table_preserves_compiler_resolved_fills(tmp_path: pathlib.Path) -> None:
	"""The native writer must use resolved fills without selecting its own theme defaults."""
	source_path = tmp_path / "table.djot"
	source_path.write_text("=== layout: one-panel\n\n@body\n\n"
		"| Sample | Result |\n| - | - |\n| A | pass |\n", encoding="utf-8")
	theme = slide_lib.presentation_theme.default_theme()
	plan = slide_lib.layout_engine.compile_layout_deck(
		slide_lib.djot_parser.parse_deck(source_path), theme).plan
	output = exporter.write_odp(plan, theme, tmp_path / "table.odp")
	with zipfile.ZipFile(output) as archive:
		root = package.parse_xml(archive.read("content.xml"), "content.xml")
	backgrounds = [properties[f"{{{exporter.FO_NS}}}background-color"]
		for properties in table_cell_properties(root)]
	table = next(item.content for item in plan.slides[0].objects
		if isinstance(item.content, content.TableContent))
	assert backgrounds == [f"#{cell.fill_color}"
		for row in table.header_rows + table.body_rows for cell in row.cells]
	assert backgrounds[0] == backgrounds[1]
	assert backgrounds[0] != f"#{theme.accent_color}"
	cell_styles = root.findall(f".//{{{exporter.STYLE_NS}}}style[@{{{exporter.STYLE_NS}}}family='table-cell']")
	for style in cell_styles:
		fill = style.find(f"{{{exporter.STYLE_NS}}}graphic-properties")
		assert fill.attrib[f"{{{exporter.DRAW_NS}}}opacity"] == "100%"


def test_native_table_exports_explicit_cell_fills_over_theme_defaults(tmp_path: pathlib.Path) -> None:
	"""Explicit fills reach editable ODP cell styles, including empty and total cells."""
	path = tmp_path / "fills.djot"
	path.write_text("=== layout: one-panel\n\n@body\n\n"
		"| [Gene]{background-color=#123456} | Count |\n| --- | --- |\n"
		"| []{background-color=#E6E6E6} | [350]{background-color=#E6F2E6} |\n"
		"| Total | [350]{background-color=#F6E8FB} |\n", encoding="utf-8")
	theme = slide_lib.presentation_theme.default_theme()
	plan = slide_lib.layout_engine.compile_layout_deck(
		slide_lib.djot_parser.parse_deck(path), theme).plan
	output = exporter.write_odp(plan, theme, tmp_path / "fills.odp")
	with zipfile.ZipFile(output) as archive:
		root = package.parse_xml(archive.read("content.xml"), "content.xml")
	backgrounds = [properties[f"{{{exporter.FO_NS}}}background-color"]
		for properties in table_cell_properties(root)]
	assert [backgrounds[index] for index in (0, 2, 3)] == ["#123456", "#E6E6E6", "#E6F2E6"]
	assert backgrounds[-1] == "#F6E8FB"


def test_authored_colspan_exports_native_merge_and_covered_cells(tmp_path: pathlib.Path) -> None:
	"""A source colspan becomes one native merged cell and real covered grid positions."""
	path = tmp_path / "merge.djot"
	path.write_text("=== layout: one-panel\n\n@body\n\n"
		"| C | D | H | Count |\n| --- | --- | --- | --- |\n"
		"| [Total]{colspan=3 background-color=#80BD80} | 1,400 |\n", encoding="utf-8")
	theme = slide_lib.presentation_theme.default_theme()
	plan = slide_lib.layout_engine.compile_layout_deck(slide_lib.djot_parser.parse_deck(path), theme).plan
	output = exporter.write_odp(plan, theme, tmp_path / "merge.odp")
	with zipfile.ZipFile(output) as archive:
		root = package.parse_xml(archive.read("content.xml"), "content.xml")
	ns = {"table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0"}
	row = root.findall(".//table:table-row", ns)[-1]
	assert row[0].get(f"{{{ns['table']}}}number-columns-spanned") == "3"
	assert len(row.findall("table:covered-table-cell", ns)) == 2
	assert len(row.findall("table:table-cell", ns)) == 2


def test_native_tables_share_effective_styles_across_objects_and_slides() -> None:
	"""Repeated formatting shares styles without colliding in wide tables or losing cell text."""
	layout_deck = deck()
	base_item = layout_deck.slides[0].objects[0]
	paragraph = base_item.content.paragraphs[0]
	border = slide_lib.table_formatting.Border(0.5, "solid", "123456")
	rows = []
	for row_index in range(2):
		cells = []
		for column_index in range(12):
			text = f"R{row_index}C{column_index}"
			cell_paragraph = dataclasses.replace(paragraph, inlines=(content.TextRun(
				text, dataclasses.replace(paragraph.inlines[0].style, foreground="172033")),))
			cell = content.TableCell((cell_paragraph,), primitives.Insets(2, 3, 4, 5),
				primitives.VerticalAlignment.MIDDLE, "FFFFFF", tuple(
					dataclasses.replace(border, priority=column_index) for _side in range(4)))
			if row_index == 1 and column_index == 11:
				cell = dataclasses.replace(cell, fill_color="ABCDEF")
			cells.append(cell)
		rows.append(content.TableRow(tuple(cells)))
	table = content.TableContent((), tuple(rows), (20.0,) * 12, (24.0, 24.0))
	table_item = dataclasses.replace(base_item, content=table)
	slide = dataclasses.replace(layout_deck.slides[0], objects=(table_item,))
	second = dataclasses.replace(slide,
		identity=dataclasses.replace(slide.identity, slide_id="slide-2", index=1),
		objects=(dataclasses.replace(table_item, object_id="second-table"),))
	layout_deck = dataclasses.replace(layout_deck, slides=(slide, second))
	theme = slide_lib.presentation_theme.default_theme()
	root = package.parse_xml(exporter._content_xml(layout_deck, theme,
		exporter._layout_names(layout_deck), {}), "content.xml")
	styles = root.findall(f".//{{{exporter.STYLE_NS}}}style")
	names = [style.attrib[f"{{{exporter.STYLE_NS}}}name"] for style in styles]
	assert len(names) == len(set(names))
	for family, count in (("table-cell", 2), ("paragraph", 1), ("text", 1),
			("table-column", 1), ("table-row", 1)):
		assert sum(style.attrib[f"{{{exporter.STYLE_NS}}}family"] == family for style in styles) == count
	cells = root.findall(f".//{{{slide_lib.odp_text.TABLE_NS}}}table-cell")
	references = [cell.attrib[f"{{{slide_lib.odp_text.TABLE_NS}}}style-name"] for cell in cells]
	assert references[:24] == references[24:]
	assert len(set(references[:23])) == 1 and references[23] != references[0]
	assert ["".join(cell.itertext()) for cell in cells] == [
		f"R{row_index}C{column_index}" for row_index in range(2) for column_index in range(12)] * 2


def test_native_table_emits_each_border_padding_alignment_and_spanned_cell() -> None:
	"""Concrete edge patterns and cell geometry survive native export, including a two-axis merge."""
	layout_deck = deck()
	base_item = layout_deck.slides[0].objects[0]
	paragraph = base_item.content.paragraphs[0]
	paragraph = dataclasses.replace(paragraph, properties=dataclasses.replace(
		paragraph.properties, horizontal_alignment=primitives.HorizontalAlignment.END))
	borders = tuple(slide_lib.table_formatting.Border(width, pattern, color)
		for width, pattern, color in ((0, "none", "000000"), (1.25, "solid", "123456"),
			(0.75, "dashed", "ABCDEF"), (0.5, "dotted", "654321")))
	cell = content.TableCell((paragraph,), primitives.Insets(2, 3, 4, 5),
		primitives.VerticalAlignment.BOTTOM, "FEDCBA", borders, column_span=2, row_span=2)
	table = content.TableContent((), (content.TableRow((cell,)), content.TableRow(())),
		(40, 60), (24, 30))
	slide = dataclasses.replace(layout_deck.slides[0], objects=(
		dataclasses.replace(base_item, content=table),))
	layout_deck = dataclasses.replace(layout_deck, slides=(slide,))
	theme = slide_lib.presentation_theme.default_theme()
	root = package.parse_xml(exporter._content_xml(layout_deck, theme,
		exporter._layout_names(layout_deck), {}), "content.xml")
	properties = table_cell_properties(root)[0]
	assert [properties[f"{{{exporter.FO_NS}}}border-{side}"]
		for side in ("top", "right", "bottom", "left")] == [
		"none", "1.2500pt solid #123456", "0.7500pt dashed #ABCDEF", "0.5000pt dotted #654321"]
	assert f"{{{exporter.FO_NS}}}border" not in properties
	assert properties[f"{{{exporter.STYLE_NS}}}vertical-align"] == "bottom"
	for side, value, canvas, centimeters in (("left", 2, layout_deck.canvas.width, theme.slide_width_cm),
			("right", 4, layout_deck.canvas.width, theme.slide_width_cm),
			("top", 3, layout_deck.canvas.height, theme.slide_height_cm),
			("bottom", 5, layout_deck.canvas.height, theme.slide_height_cm)):
		assert float(properties[f"{{{exporter.FO_NS}}}padding-{side}"].removesuffix("cm")) == pytest.approx(
			value * centimeters / canvas, abs=0.000001)
	ns = {"table": slide_lib.odp_text.TABLE_NS}
	cell_element = root.find(".//table:table-cell", ns)
	assert [cell_element.attrib[f"{{{ns['table']}}}number-{axis}-spanned"]
		for axis in ("columns", "rows")] == ["2", "2"]
	assert len(root.findall(".//table:covered-table-cell", ns)) == 3
	assert "".join(cell_element.itertext()) == "Body"
	paragraph_style = root.find(f".//{{{exporter.STYLE_NS}}}paragraph-properties")
	assert paragraph_style.attrib[f"{{{exporter.FO_NS}}}text-align"] == "end"


def test_scoped_xml_parser_rejects_dtds() -> None:
	"""ODF XML cannot declare entities even when lxml would leave them unresolved."""
	with pytest.raises(ValueError, match="DTD is not allowed"):
		package.parse_xml(b'<!DOCTYPE root [<!ENTITY local "blocked">]><root/>', "content.xml")


def test_validation_rejects_manifest_and_reference_consistency_errors() -> None:
	items = payloads()
	items["extra.bin"] = b"orphan"
	with pytest.raises(ValueError, match="missing a manifest"):
		package.validate_odp_members(items)
	items = payloads()
	items["Pictures/reachable.png"] = b"reachable"
	items["content.xml"] = xml('<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" office:version="1.3" xlink:href="Pictures/reachable.png"/>')
	with pytest.raises(ValueError, match="missing a manifest"):
		package.validate_odp_members(items)
	items = payloads()
	items[package.MANIFEST_NAME] = items[package.MANIFEST_NAME].replace(b'<manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml" />', b"")
	with pytest.raises(ValueError, match="missing a manifest"):
		package.validate_odp_members(items)
	items = payloads()
	items[package.MANIFEST_NAME] = items[package.MANIFEST_NAME].replace(b"content.xml", b"absent.xml")
	with pytest.raises(ValueError, match="manifest references missing"):
		package.validate_odp_members(items)
	items = payloads()
	items["content.xml"] = xml('<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" office:version="1.3" xlink:href="Pictures/missing.png"/>')
	with pytest.raises(ValueError, match="XML reference"):
		package.validate_odp_members(items)
	items = payloads()
	items["Pictures/generated.png"] = b"generated"
	items[package.MANIFEST_NAME] = exporter._manifest_xml(items)
	with pytest.raises(ValueError, match="generated media is unreachable"):
		package.validate_odp_members(items, frozenset({"Pictures/generated.png"}))


def test_validate_package_rejects_duplicate_member_and_unsafe_path(tmp_path: pathlib.Path) -> None:
	duplicate = tmp_path / "duplicate.odp"
	with pytest.warns(UserWarning, match="Duplicate"):
		with zipfile.ZipFile(duplicate, "w") as archive:
			archive.writestr("mimetype", package.ODP_MIMETYPE)
			archive.writestr("mimetype", package.ODP_MIMETYPE)
	with pytest.raises(ValueError, match="repeats"):
		package.validate_package(duplicate, ".odp", package.ODP_MIMETYPE, frozenset({"mimetype"}))
	unsafe = tmp_path / "unsafe.odp"
	with zipfile.ZipFile(unsafe, "w") as archive:
		archive.writestr("mimetype", package.ODP_MIMETYPE, compress_type=zipfile.ZIP_STORED)
		archive.writestr("../unsafe", b"bad")
	with pytest.raises(ValueError, match="unsafe"):
		package.validate_package(unsafe, ".odp", package.ODP_MIMETYPE, frozenset({"mimetype"}))


def test_atomic_publish_preserves_existing_destination_on_validation_failure(tmp_path: pathlib.Path) -> None:
	destination = tmp_path / "existing.odp"
	destination.write_bytes(b"known good")
	items = payloads()
	items.pop("content.xml")
	with pytest.raises(ValueError, match="required"):
		package.publish_odp(destination, items)
	assert destination.read_bytes() == b"known good"
