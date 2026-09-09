"""Focused tests for direct bounded native-ODP source extraction."""

# Standard Library
import io
import pathlib
import xml.etree.ElementTree
import zipfile

# PIP3 modules
from PIL import Image
import pytest

# Local modules
import slide_lib.importers.odp_reader as odp_reader
import slide_lib.odf_package


CONTENT_PREFIX = """<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
 xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
 xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
 xmlns:presentation="urn:oasis:names:tc:opendocument:xmlns:presentation:1.0"
 xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
 xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
 xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
 xmlns:xlink="http://www.w3.org/1999/xlink">
 <office:body><office:presentation>"""
CONTENT_SUFFIX = "</office:presentation></office:body></office:document-content>"
STYLES_XML = """<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
 xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
 xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
 xmlns:presentation="urn:oasis:names:tc:opendocument:xmlns:presentation:1.0"
 xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0">
 <office:styles>
  <style:style style:name="dp" style:family="drawing-page" style:page-layout-name="pm"/>
  <style:style style:name="hidden" style:family="drawing-page" style:page-layout-name="pm">
   <style:drawing-page-properties presentation:visibility="hidden"/>
  </style:style>
 </office:styles>
 <office:automatic-styles>
  <style:page-layout style:name="pm"><style:page-layout-properties fo:page-width="28cm" fo:page-height="17.5cm"/></style:page-layout>
  <style:presentation-page-layout style:name="section"><presentation:placeholder presentation:object="subtitle"/></style:presentation-page-layout>
 </office:automatic-styles>
</office:document-styles>"""


#============================================
def png_bytes() -> bytes:
	"""Return one validated inline source image."""
	buffer = io.BytesIO()
	Image.new("RGB", (8, 6), (40, 120, 180)).save(buffer, format="PNG")
	return buffer.getvalue()


#============================================
def gif_bytes(frame_count: int) -> bytes:
	"""Return an animated GIF whose complete frames are available for decoding."""
	frames = [Image.new("RGB", (2, 2), (index, 0, 0)) for index in range(frame_count)]
	buffer = io.BytesIO()
	frames[0].save(buffer, format="GIF", save_all=True, append_images=frames[1:])
	return buffer.getvalue()


#============================================
def manifest_xml(media_names: tuple[str, ...] = ()) -> str:
	"""Build the matching minimal ODF manifest for an inline package."""
	entries = "".join(
		f'<manifest:file-entry manifest:full-path="{name}" manifest:media-type="image/png"/>'
		for name in media_names
	)
	return """<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">
 <manifest:file-entry manifest:full-path="/" manifest:media-type="application/vnd.oasis.opendocument.presentation"/>
 <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>""" + entries + "</manifest:manifest>"


#============================================
def write_odp(tmp_path: pathlib.Path, content: str, *, media: dict[str, bytes] | None = None,
		name: str = "source.odp") -> pathlib.Path:
	"""Write one bounded inline ODP fixture with its matching manifest."""
	media = {} if media is None else media
	path = tmp_path / name
	with zipfile.ZipFile(path, "w") as archive:
		archive.writestr("mimetype", odp_reader.ODP_MIMETYPE, compress_type=zipfile.ZIP_STORED)
		archive.writestr("content.xml", content)
		archive.writestr("styles.xml", STYLES_XML)
		archive.writestr("META-INF/manifest.xml", manifest_xml(tuple(media)))
		for media_name, media_bytes in media.items():
			archive.writestr(media_name, media_bytes)
	return path


#============================================
def page(name: str, body: str, *, style: str = "dp", layout: str | None = None,
		visibility: str = "") -> str:
	"""Build one physical ODP page from concise XML content."""
	layout_attribute = "" if layout is None else f' presentation:presentation-page-layout-name="{layout}"'
	visibility_attribute = "" if not visibility else f' presentation:visibility="{visibility}"'
	return f'<draw:page draw:name="{name}" draw:style-name="{style}"{layout_attribute}{visibility_attribute}>{body}</draw:page>'


#============================================
def frame(body: str, *, role: str = "", x: str = "1cm", y: str = "1cm",
		width: str = "10cm", height: str = "3cm") -> str:
	"""Build one positioned ODP frame with an optional placeholder role."""
	role_attribute = "" if not role else f' presentation:class="{role}"'
	return f'<draw:frame svg:x="{x}" svg:y="{y}" svg:width="{width}" svg:height="{height}"{role_attribute}>{body}</draw:frame>'


#============================================
def test_reader_extracts_direct_text_list_links_table_image_notes_and_visibility(
		tmp_path: pathlib.Path,
) -> None:
	"""Direct ODP facts preserve current planner inputs without a conversion bridge."""
	visible = page("visible", "".join((
		frame('<draw:text-box><text:p>Title</text:p></draw:text-box>', role="title"),
		frame("""<draw:text-box><text:list><text:list-item><text:p>Outer <text:a xlink:href="https://example.test/a">link</text:a></text:p><text:list><text:list-item><text:p>Inner</text:p></text:list-item></text:list></text:list-item></text:list></draw:text-box>""", y="5cm"),
		frame("""<table:table><table:table-header-rows><table:table-row><table:table-cell><text:p>Gene</text:p></table:table-cell><table:table-cell><text:p>Value</text:p></table:table-cell></table:table-row></table:table-header-rows><table:table-row><table:table-cell><text:p>lacZ</text:p></table:table-cell><table:table-cell/></table:table-row></table:table>
""", y="9cm"),
		frame('<draw:image xlink:href="Pictures/figure.png"/>', y="12cm"),
		'<presentation:notes><draw:frame><draw:text-box><text:p>Explain the mutation.</text:p></draw:text-box></draw:frame></presentation:notes>',
	)))
	hidden = page("hidden", frame('<draw:text-box><text:p>Skip me</text:p></draw:text-box>'),
		style="hidden")
	input_path = write_odp(tmp_path, CONTENT_PREFIX + visible + hidden + CONTENT_SUFFIX,
		media={"Pictures/figure.png": png_bytes()})
	assets_dir = tmp_path / "assets"
	assets_dir.mkdir()
	presentation = odp_reader.read_presentation(input_path, assets_dir,
		pathlib.PurePosixPath("assets/deck"))

	first, second = presentation.slides
	assert first.data.hidden is False and second.data.hidden is True
	assert first.data.notes == ("Explain the mutation.",)
	assert first.positioned_text[1].paragraphs[0][0] == 0
	assert first.positioned_text[1].paragraphs[1][0] == 1
	assert first.positioned_text[1].paragraphs[0][1][1].link == "https://example.test/a"
	assert first.data.tables[0].headers[0][0].text == "Gene"
	assert first.data.tables[0].rows[0][1] == ()
	assert first.data.images[0].asset_path == "assets/deck/image_001.png"
	assert (assets_dir / "image_001.png").is_file()
	assert first.page_width > first.page_height


#============================================
def test_page_evidence_keeps_section_positive_case_and_near_miss(tmp_path: pathlib.Path) -> None:
	"""Physical source indices retain exact layout and placeholder evidence."""
	section = page("section", frame('<draw:text-box><text:p>Unit two</text:p></draw:text-box>',
		role="subtitle"), layout="section")
	near_miss = page("near-miss", "".join((
		frame('<draw:text-box><text:p>Unit three</text:p></draw:text-box>', role="subtitle"),
		frame('<draw:text-box><text:p>Objectives</text:p></draw:text-box>', role="outline", y="5cm"),
	)), layout="section")
	input_path = write_odp(tmp_path, CONTENT_PREFIX + section + near_miss + CONTENT_SUFFIX)
	assets_dir = tmp_path / "assets"
	assets_dir.mkdir()
	presentation = odp_reader.read_presentation(input_path, assets_dir,
		pathlib.PurePosixPath("assets/deck"))

	first = presentation.slides[0].data.page_evidence
	second = presentation.slides[1].data.page_evidence
	assert first is not None and second is not None
	assert first.layout_identity == "section"
	assert first.declared_placeholder_roles == ("subtitle",)
	assert first.populated_placeholder_roles == ("subtitle",)
	assert first.populated_text_placeholder_roles == ("subtitle",)
	assert first.populated_image_placeholder_roles == ()
	assert first.populated_table_placeholder_roles == ()
	assert first.meaningful_content_count == 1
	assert second.populated_placeholder_roles == ("subtitle", "outline")
	assert second.populated_text_placeholder_roles == ("subtitle", "outline")
	assert second.meaningful_content_count == 2
	assert first.is_section_page()
	assert not second.is_section_page()


#============================================
def test_page_evidence_distinguishes_text_placeholders_from_image_and_table_roles(
		tmp_path: pathlib.Path,
) -> None:
	"""Section eligibility can require a populated text subtitle, not any frame role."""
	image_page = page("image", frame(
		'<draw:image xlink:href="Pictures/figure.png"/>', role="subtitle"), layout="section")
	table_page = page("table", frame(
		'<table:table><table:table-row><table:table-cell><text:p>Fact</text:p></table:table-cell></table:table-row></table:table>',
		role="subtitle"), layout="section")
	input_path = write_odp(
		tmp_path, CONTENT_PREFIX + image_page + table_page + CONTENT_SUFFIX,
		media={"Pictures/figure.png": png_bytes()},
	)
	assets_dir = tmp_path / "assets"
	assets_dir.mkdir()
	presentation = odp_reader.read_presentation(input_path, assets_dir,
		pathlib.PurePosixPath("assets/deck"))

	image_evidence = presentation.slides[0].data.page_evidence
	table_evidence = presentation.slides[1].data.page_evidence
	assert image_evidence is not None and table_evidence is not None
	assert image_evidence.populated_text_placeholder_roles == ()
	assert image_evidence.populated_image_placeholder_roles == ("subtitle",)
	assert table_evidence.populated_text_placeholder_roles == ()
	assert table_evidence.populated_table_placeholder_roles == ("subtitle",)
	assert not image_evidence.is_section_page()
	assert not table_evidence.is_section_page()


#============================================
def test_page_evidence_excludes_decorative_shapes_and_surfaces_unknown_objects(
		tmp_path: pathlib.Path,
) -> None:
	"""Reviewable decoration stays out of instructional counts; unknown objects remain visible."""
	decorative = page("decorative", "".join((
		frame('<draw:text-box><text:p>Unit</text:p></draw:text-box>', role="subtitle"),
		'<draw:custom-shape svg:x="1cm" svg:y="6cm" svg:width="2cm" svg:height="2cm"/>',
	)), layout="section")
	unknown = page("unknown", "".join((
		frame('<draw:text-box><text:p>Unit</text:p></draw:text-box>', role="subtitle"),
		'<draw:object svg:x="1cm" svg:y="6cm" svg:width="2cm" svg:height="2cm"/>',
	)), layout="section")
	input_path = write_odp(tmp_path, CONTENT_PREFIX + decorative + unknown + CONTENT_SUFFIX)
	assets_dir = tmp_path / "assets"
	assets_dir.mkdir()
	presentation = odp_reader.read_presentation(input_path, assets_dir,
		pathlib.PurePosixPath("assets/deck"))

	decorative_data = presentation.slides[0].data
	unknown_data = presentation.slides[1].data
	assert decorative_data.page_evidence is not None
	assert decorative_data.page_evidence.meaningful_content_count == 1
	assert any("custom-shape" in reason for reason in decorative_data.review_reasons)
	assert unknown_data.page_evidence is not None
	assert unknown_data.page_evidence.meaningful_content_count == 2
	assert any("source slide 2" in reason and "draw:object" in reason
		for reason in unknown_data.review_reasons)


#============================================
def test_reader_reports_external_image_and_partial_geometry_without_losing_page(tmp_path: pathlib.Path) -> None:
	"""Review evidence makes unsupported media and clipped geometry observable."""
	body = "".join((
		frame('<draw:text-box><text:p>Visible title</text:p></draw:text-box>', role="title",
			x="-1cm"),
		frame('<draw:image xlink:href="https://example.test/figure.png"/>', y="6cm"),
	))
	input_path = write_odp(tmp_path, CONTENT_PREFIX + page("review", body) + CONTENT_SUFFIX)
	assets_dir = tmp_path / "assets"
	assets_dir.mkdir()
	result = odp_reader.read_presentation(input_path, assets_dir, pathlib.PurePosixPath("assets/deck"))
	data = result.slides[0].data

	assert any("external source image" in reason for reason in data.review_reasons)
	assert any("crosses physical page bounds" in reason for reason in data.review_reasons)
	assert result.slides[0].raw_geometry[0].left < 0.0


#============================================
def test_reader_rejects_missing_reference_and_unsafe_archive_member(tmp_path: pathlib.Path) -> None:
	"""The archive boundary validates manifest, XML references, and member paths."""
	missing = write_odp(tmp_path, CONTENT_PREFIX + page("bad", frame(
		'<draw:image xlink:href="Pictures/missing.png"/>')) + CONTENT_SUFFIX, name="missing.odp")
	with pytest.raises(ValueError, match="XML reference points to a missing member"):
		odp_reader.validate_odp(missing)

	unsafe = tmp_path / "unsafe.odp"
	with zipfile.ZipFile(unsafe, "w") as archive:
		archive.writestr("mimetype", odp_reader.ODP_MIMETYPE, compress_type=zipfile.ZIP_STORED)
		archive.writestr("../escape", b"blocked")
	with pytest.raises(ValueError, match="unsafe archive member path"):
		odp_reader.validate_odp(unsafe)


#============================================
def test_reader_rejects_malformed_xml_before_source_object_extraction(tmp_path: pathlib.Path) -> None:
	"""Restrictive XML parsing prevents malformed package data from reaching facts."""
	malformed = tmp_path / "malformed.odp"
	with zipfile.ZipFile(malformed, "w") as archive:
		archive.writestr("mimetype", odp_reader.ODP_MIMETYPE, compress_type=zipfile.ZIP_STORED)
		archive.writestr("content.xml", "<office:document-content")
		archive.writestr("styles.xml", STYLES_XML)
		archive.writestr("META-INF/manifest.xml", manifest_xml())
	with pytest.raises(xml.etree.ElementTree.ParseError):
		odp_reader.validate_odp(malformed)


#============================================
def test_reader_rejects_fully_outside_geometry(tmp_path: pathlib.Path) -> None:
	"""An object with no visible intersection remains a source-located error."""
	input_path = write_odp(tmp_path, CONTENT_PREFIX + page("outside", frame(
		'<draw:text-box><text:p>Outside</text:p></draw:text-box>', x="40cm")) + CONTENT_SUFFIX)
	assets_dir = tmp_path / "assets"
	assets_dir.mkdir()
	with pytest.raises(ValueError, match="source slide 1: source geometry lies outside page bounds"):
		odp_reader.read_presentation(input_path, assets_dir, pathlib.PurePosixPath("assets/deck"))


#============================================
def test_reader_requires_manifest_for_each_consumed_local_media_reference(
		tmp_path: pathlib.Path,
) -> None:
	"""A ZIP member alone never authorizes a local image reference."""
	content = CONTENT_PREFIX + page("missing-manifest", frame(
		'<draw:image xlink:href="Pictures/figure.png"/>')) + CONTENT_SUFFIX
	input_path = tmp_path / "missing_manifest.odp"
	with zipfile.ZipFile(input_path, "w") as archive:
		archive.writestr("mimetype", odp_reader.ODP_MIMETYPE, compress_type=zipfile.ZIP_STORED)
		archive.writestr("content.xml", content)
		archive.writestr("styles.xml", STYLES_XML)
		archive.writestr("META-INF/manifest.xml", manifest_xml())
		archive.writestr("Pictures/figure.png", png_bytes())

	with pytest.raises(ValueError, match="misses a manifest target"):
		odp_reader.validate_odp(input_path)


#============================================
def test_reader_reports_unvalidated_vector_media_and_extension_mismatch(
		tmp_path: pathlib.Path,
) -> None:
	"""Unsupported metafiles and claimed-extension mismatches stay out of published assets."""
	content = CONTENT_PREFIX + "".join((
		page("metafile", frame('<draw:image xlink:href="Pictures/legacy.emf"/>')),
		page("mismatch", frame('<draw:image xlink:href="Pictures/mismatch.jpg"/>')),
	)) + CONTENT_SUFFIX
	input_path = write_odp(tmp_path, content, media={
		"Pictures/legacy.emf": b"\x01\x00\x00\x00not-a-maintained-metafile",
		"Pictures/mismatch.jpg": png_bytes(),
	})
	assets_dir = tmp_path / "assets"
	assets_dir.mkdir()
	presentation = odp_reader.read_presentation(input_path, assets_dir,
		pathlib.PurePosixPath("assets/deck"))

	assert not presentation.slides[0].data.images
	assert not presentation.slides[1].data.images
	assert any("unsupported ODP image type" in reason
		for reason in presentation.slides[0].data.review_reasons)
	assert any("bytes do not match" in reason
		for reason in presentation.slides[1].data.review_reasons)
	assert not any(assets_dir.iterdir())


#============================================
def test_reader_keeps_only_safe_hyperlink_schemes(tmp_path: pathlib.Path) -> None:
	"""Styled text retains classroom links while discarding active URI schemes."""
	content = CONTENT_PREFIX + page("links", frame(
		'<draw:text-box><text:p><text:a xlink:href="javascript:alert(1)">Unsafe</text:a> '
		'<text:a xlink:href="https://example.test/">Safe</text:a></text:p></draw:text-box>')) + CONTENT_SUFFIX
	input_path = write_odp(tmp_path, content)
	assets_dir = tmp_path / "assets"
	assets_dir.mkdir()
	presentation = odp_reader.read_presentation(input_path, assets_dir,
		pathlib.PurePosixPath("assets/deck"))
	runs = presentation.slides[0].data.text_blocks[0].lines[0][1]

	assert runs[0].link == ""
	assert runs[-1].link == "https://example.test/"


#============================================
def test_reader_enforces_xml_and_page_object_limits(tmp_path: pathlib.Path,
		monkeypatch: pytest.MonkeyPatch) -> None:
	"""Explicit XML and object budgets fail at a deterministic import boundary."""
	content = CONTENT_PREFIX + page("objects", "".join(
		frame('<draw:text-box><text:p>Fact</text:p></draw:text-box>', y=f"{index + 1}cm")
		for index in range(2)
	)) + CONTENT_SUFFIX
	input_path = write_odp(tmp_path, content)
	assets_dir = tmp_path / "assets"
	assets_dir.mkdir()
	monkeypatch.setattr(odp_reader, "MAX_PAGE_OBJECTS", 1)
	with pytest.raises(ValueError, match="page object limit"):
		odp_reader.read_presentation(input_path, assets_dir, pathlib.PurePosixPath("assets/deck"))

	monkeypatch.setattr(slide_lib.odf_package, "MAX_XML_DEPTH", 1)
	with pytest.raises(ValueError, match="XML depth limit"):
		odp_reader.validate_odp(input_path)


#============================================
def test_reader_enforces_total_repeated_table_cell_limit(tmp_path: pathlib.Path,
		monkeypatch: pytest.MonkeyPatch) -> None:
	"""Repeated rows and columns cannot expand a native table beyond its cell budget."""
	table = """<table:table><table:table-row>
	<table:table-cell><text:p>A</text:p></table:table-cell>
	<table:table-cell><text:p>B</text:p></table:table-cell>
	<table:table-cell><text:p>C</text:p></table:table-cell>
	</table:table-row></table:table>"""
	input_path = write_odp(tmp_path, CONTENT_PREFIX + page("table", frame(table)) + CONTENT_SUFFIX)
	assets_dir = tmp_path / "assets"
	assets_dir.mkdir()
	monkeypatch.setattr(odp_reader, "MAX_TABLE_CELLS", 2)
	with pytest.raises(ValueError, match="table exceeds"):
		odp_reader.read_presentation(input_path, assets_dir, pathlib.PurePosixPath("assets/deck"))


#============================================
def test_reader_decodes_all_raster_frames_and_rejects_claimed_format_mismatch() -> None:
	"""Raster admission records aggregate decoding work before publication is possible."""
	budget = odp_reader._MediaBudget()
	odp_reader.validate_image_blob(gif_bytes(2), ".gif", budget)
	assert budget.frame_count == 2
	assert budget.pixel_count == 8
	with pytest.raises(ValueError, match="do not match"):
		odp_reader.validate_image_blob(png_bytes(), ".jpg", odp_reader._MediaBudget())


#============================================
def test_reader_rejects_entity_and_control_character_archive_input(tmp_path: pathlib.Path) -> None:
	"""Archive names and XML remain inert data at the package admission boundary."""
	entity_package = tmp_path / "entity.odp"
	entity_prefix = CONTENT_PREFIX.replace(
		"?>", "?>\n<!DOCTYPE office:document-content [<!ENTITY xxe 'blocked'>]>", 1,
	)
	with zipfile.ZipFile(entity_package, "w") as archive:
		archive.writestr("mimetype", odp_reader.ODP_MIMETYPE, compress_type=zipfile.ZIP_STORED)
		archive.writestr("content.xml", entity_prefix + page("entity", frame(
			'<draw:text-box><text:p>&xxe;</text:p></draw:text-box>')) + CONTENT_SUFFIX)
		archive.writestr("styles.xml", STYLES_XML)
		archive.writestr("META-INF/manifest.xml", manifest_xml())
	with pytest.raises(Exception):
		odp_reader.validate_odp(entity_package)

	control_package = tmp_path / "control.odp"
	with zipfile.ZipFile(control_package, "w") as archive:
		archive.writestr("mimetype", odp_reader.ODP_MIMETYPE, compress_type=zipfile.ZIP_STORED)
		archive.writestr("Pictures/control\x01.png", png_bytes())
	with pytest.raises(ValueError, match="unsafe archive member path"):
		odp_reader.validate_odp(control_package)


#============================================
