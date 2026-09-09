"""Fast XML and ZIP contract tests for the native ODP package skeleton."""

# Standard Library
import dataclasses
import pathlib
import zipfile

import defusedxml.ElementTree
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
		primitives.TextDirection.HORIZONTAL, primitives.OverflowPolicy.SHRINK)


def deck() -> model.LayoutDeck:
	rectangle = primitives.LogicalRectangle(0.0, 0.0, 500.0, 300.0)
	slot = model.LayoutSlot("body", primitives.PlaceholderKind.OUTLINE,
		primitives.PresentationRole.OUTLINE, rectangle, 0,
		primitives.PlaceholderProperties(primitives.StyleRole.OUTLINE, frame_text()))
	topology = primitives.PlaceholderTopology("one-panel", (slot.topology_member(),))
	identity = model.LayoutIdentity("one-panel", topology)
	typography = primitives.Typography(primitives.StyleRole.OUTLINE, "OpenDyslexic", 28.0, 28.0, 24.0)
	paragraph = content.TextParagraph((content.TextRun("Body", content.RunStyle("OpenDyslexic", "ink")),),
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
	items = payloads()
	items["mimetype"] = exporter.OTP_MIMETYPE.encode("ascii")
	items["styles.xml"] = xml('<office:document-styles xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" office:version="1.3"><office:styles><office:annotation xlink:href="Pictures/theme.png"/></office:styles></office:document-styles>')
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


def test_cascade_reveal_targets_resolve_to_native_paragraph_ids(tmp_path: pathlib.Path) -> None:
	"""Every native ODF timing step targets an emitted editable paragraph identity."""
	source_path = tmp_path / "cascade.djot"
	source_path.write_text("=== layout: one-panel\n\n@body\n\n=> cascade appear\n"
		"- Parent\n\n  - Child\n- Second\n", encoding="utf-8")
	theme = slide_lib.presentation_theme.default_theme()
	plan = slide_lib.layout_engine.compile_layout_deck(
		slide_lib.djot_parser.parse_deck(source_path), theme)
	output = exporter.write_odp(plan, theme, tmp_path / "cascade.odp")
	with zipfile.ZipFile(output) as archive:
		root = defusedxml.ElementTree.fromstring(archive.read("content.xml"))
	target_attribute = f"{{{slide_lib.odp_animation.SMIL_NS}}}targetElement"
	xml_id = "{http://www.w3.org/XML/1998/namespace}id"
	targets = [element.attrib[target_attribute] for element in root.findall(
		".//{urn:oasis:names:tc:opendocument:xmlns:animation:1.0}set")]
	ids = {element.attrib[xml_id] for element in root.iter() if xml_id in element.attrib}
	assert len(targets) == 2 and set(targets) <= ids


def test_object_reveal_target_is_a_libreoffice_presentation_frame(tmp_path: pathlib.Path) -> None:
	"""LibreOffice must retain the answer's layout membership and reveal identity."""
	source_path = tmp_path / "multiple_choice.djot"
	source_path.write_text("=== layout: multiple-choice\n\n@question\n\nQuestion?\n\n"
		"@answer\n\nAnswer.\n", encoding="utf-8")
	theme = slide_lib.presentation_theme.default_theme()
	plan = slide_lib.layout_engine.compile_layout_deck(
		slide_lib.djot_parser.parse_deck(source_path), theme)
	output = exporter.write_odp(plan, theme, tmp_path / "multiple_choice.odp")
	with zipfile.ZipFile(output) as archive:
		root = defusedxml.ElementTree.fromstring(archive.read("content.xml"))
	target_attribute = f"{{{slide_lib.odp_animation.SMIL_NS}}}targetElement"
	target = root.find(".//{urn:oasis:names:tc:opendocument:xmlns:animation:1.0}set").attrib[target_attribute]
	xml_id = "{http://www.w3.org/XML/1998/namespace}id"
	object_frame = next(item for item in root.iter() if item.attrib.get(xml_id) == target)
	assert object_frame.tag == f"{{{exporter.DRAW_NS}}}frame" and \
		object_frame.attrib[f"{{{exporter.PRESENTATION_NS}}}class"] == "object"


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
