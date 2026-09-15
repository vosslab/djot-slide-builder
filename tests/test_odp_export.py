"""Fast XML and ZIP contract tests for the native ODP package skeleton."""

# Standard Library
import dataclasses
import io
import pathlib
import zipfile

import fontTools.ttLib
import lxml.etree
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
import slide_lib.presentation_theme


def source() -> slide_lib.native_model.SourceLocation:
	return slide_lib.native_model.SourceLocation(pathlib.Path("inline.djot"), 1)


def frame_text() -> primitives.FrameTextProperties:
	return primitives.FrameTextProperties(primitives.Insets(0.0, 0.0, 0.0, 0.0),
		primitives.VerticalAlignment.TOP, primitives.TextWrap.WRAP,
		primitives.OverflowPolicy.SHRINK)


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
	destination = exporter.write_odp(deck(), theme, tmp_path / "deck.odp")
	package.validate_package(destination, ".odp", package.ODP_MIMETYPE, package.REQUIRED_ODP_MEMBERS)
	with zipfile.ZipFile(destination) as archive:
		members = archive.infolist()
		assert members[0].filename == "mimetype" and members[0].compress_type == zipfile.ZIP_STORED
		assert archive.read("Pictures/theme.png") == b"theme image"
		assert b'draw:name="slide-1"' in archive.read("content.xml")
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


def test_linked_text_nests_destination_inside_its_styled_span() -> None:
	"""LibreOffice receives a visible linked label within its resolved text style."""
	layout_deck = deck()
	item = layout_deck.slides[0].objects[0]
	linked_run = content.TextRun("Course website", content.RunStyle("Atkinson Hyperlegible Next", "24578F",
		underline=True, link_url="https://example.test/course"))
	paragraph = dataclasses.replace(item.content.paragraphs[0], inlines=(linked_run,))
	updated_item = dataclasses.replace(item, content=content.TextContent((paragraph,)))
	updated_deck = dataclasses.replace(layout_deck, slides=(dataclasses.replace(
		layout_deck.slides[0], objects=(updated_item,)),))
	root = package.parse_xml(exporter._content_xml(updated_deck,
		slide_lib.presentation_theme.default_theme(), exporter._layout_names(updated_deck), {}),
		"content.xml")
	span = root.find(f".//{{{exporter.TEXT_NS}}}span")
	link = span.find(f"{{{exporter.TEXT_NS}}}a")
	assert link is not None and link.text == "Course website"
	assert link.attrib[f"{{{exporter.XLINK_NS}}}href"] == "https://example.test/course" and \
		span.attrib[f"{{{exporter.TEXT_NS}}}style-name"].startswith("DjotText")


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


def test_transition_surface_and_end_star_are_native_odf(tmp_path: pathlib.Path) -> None:
	"""LibreOffice receives the dark transition as a page style and the flourish as a vector."""
	source_path = tmp_path / "closer.djot"
	source_path.write_text("=== layout: section\n\n# THE END\n", encoding="utf-8")
	theme = slide_lib.presentation_theme.default_theme()
	plan = slide_lib.layout_engine.compile_layout_deck(
		slide_lib.djot_parser.parse_deck(source_path), theme).plan
	root = package.parse_xml(exporter._content_xml(
		plan, theme, exporter._layout_names(plan), {}), "content.xml")
	page = root.find(f".//{{{exporter.DRAW_NS}}}page")
	page_style_name = page.attrib[f"{{{exporter.DRAW_NS}}}style-name"]
	page_style = next(style for style in root.findall(f".//{{{exporter.STYLE_NS}}}style")
		if style.attrib.get(f"{{{exporter.STYLE_NS}}}name") == page_style_name)
	properties = page_style.find(f"{{{exporter.STYLE_NS}}}drawing-page-properties").attrib
	star = next(shape for shape in page.findall(f"{{{exporter.DRAW_NS}}}custom-shape")
		if shape.find(f"{{{exporter.DRAW_NS}}}enhanced-geometry").attrib[
			f"{{{exporter.DRAW_NS}}}type"] == "star5")
	star_style_name = star.attrib[f"{{{exporter.DRAW_NS}}}style-name"]
	star_style = next(style for style in root.findall(f".//{{{exporter.STYLE_NS}}}style")
		if style.attrib.get(f"{{{exporter.STYLE_NS}}}name") == star_style_name)
	star_properties = star_style.find(f"{{{exporter.STYLE_NS}}}graphic-properties").attrib
	rounded_rectangles = tuple(page.findall(f"{{{exporter.DRAW_NS}}}rect"))
	assert (properties[f"{{{exporter.DRAW_NS}}}fill"],
		properties[f"{{{exporter.DRAW_NS}}}fill-color"],
		properties[f"{{{exporter.PRESENTATION_NS}}}background-objects-visible"]) == (
		"solid", f"#{theme.accent_color}", "false")
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


def test_native_table_uses_light_body_cells_and_theme_header(tmp_path: pathlib.Path) -> None:
	"""Native table styles keep body text readable while retaining the deck accent header."""
	source_path = tmp_path / "table.djot"
	source_path.write_text("=== layout: one-panel\n\n@body\n\n"
		"| Sample | Result |\n| - | - |\n| A | pass |\n", encoding="utf-8")
	theme = slide_lib.presentation_theme.default_theme()
	plan = slide_lib.layout_engine.compile_layout_deck(
		slide_lib.djot_parser.parse_deck(source_path), theme).plan
	output = exporter.write_odp(plan, theme, tmp_path / "table.odp")
	with zipfile.ZipFile(output) as archive:
		root = package.parse_xml(archive.read("content.xml"), "content.xml")
	backgrounds = [element.attrib[f"{{{exporter.FO_NS}}}background-color"]
		for element in root.findall(f".//{{{exporter.STYLE_NS}}}table-cell-properties")]
	assert backgrounds == [f"#{theme.accent_color}", f"#{theme.accent_color}",
		"#F2F3F5", "#F2F3F5"]


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


def test_validate_package_rejects_duplicate_member_unsafe_path_and_bad_mimetype(tmp_path: pathlib.Path) -> None:
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
	bad = tmp_path / "bad.odp"
	with zipfile.ZipFile(bad, "w") as archive:
		archive.writestr("content.xml", b"x")
		archive.writestr("mimetype", package.ODP_MIMETYPE)
	with pytest.raises(ValueError, match="first uncompressed"):
		package.validate_package(bad, ".odp", package.ODP_MIMETYPE, frozenset({"mimetype"}))
	compressed = tmp_path / "compressed.odp"
	with zipfile.ZipFile(compressed, "w", compression=zipfile.ZIP_DEFLATED) as archive:
		archive.writestr("mimetype", package.ODP_MIMETYPE)
	with pytest.raises(ValueError, match="first uncompressed"):
		package.validate_package(compressed, ".odp", package.ODP_MIMETYPE, frozenset({"mimetype"}))


def test_atomic_publish_preserves_existing_destination_on_validation_failure(tmp_path: pathlib.Path) -> None:
	destination = tmp_path / "existing.odp"
	destination.write_bytes(b"known good")
	items = payloads()
	items.pop("content.xml")
	with pytest.raises(ValueError, match="required"):
		package.publish_odp(destination, items)
	assert destination.read_bytes() == b"known good"
