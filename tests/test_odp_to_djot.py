"""Behavioral tests for direct native-ODP-to-Djot publication."""

# Standard Library
import io
import json
import pathlib
import xml.etree.ElementTree
import zipfile

# PIP3 modules
from PIL import Image
import pytest

# Local modules
import slide_lib.djot_parser
import slide_lib.importers.odp_reader as odp_reader
import slide_lib.importers.odp_to_djot as odp_to_djot


STYLES_XML = """<office:document-styles
 xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
 xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
 xmlns:presentation="urn:oasis:names:tc:opendocument:xmlns:presentation:1.0"
 xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0">
 <office:styles><style:style style:name="dp" style:family="drawing-page" style:page-layout-name="pm"/></office:styles>
 <office:automatic-styles><style:page-layout style:name="pm"><style:page-layout-properties fo:page-width="28cm" fo:page-height="17.5cm"/></style:page-layout><style:presentation-page-layout style:name="section"><presentation:placeholder presentation:object="subtitle"/></style:presentation-page-layout></office:automatic-styles>
</office:document-styles>"""


#============================================
def png_bytes() -> bytes:
	"""Return a validated inline source PNG."""
	buffer = io.BytesIO()
	Image.new("RGB", (8, 6), (40, 120, 180)).save(buffer, format="PNG")
	return buffer.getvalue()


#============================================
def write_source_odp(tmp_path: pathlib.Path) -> pathlib.Path:
	"""Write one small direct-import ODP with visible and hidden media."""
	content = """<office:document-content
 xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
 xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
 xmlns:presentation="urn:oasis:names:tc:opendocument:xmlns:presentation:1.0"
 xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
 xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
 xmlns:xlink="http://www.w3.org/1999/xlink">
 <office:body><office:presentation>
  <draw:page draw:name="section" draw:style-name="dp" presentation:presentation-page-layout-name="section">
   <draw:frame svg:x="1cm" svg:y="1cm" svg:width="20cm" svg:height="3cm" presentation:class="subtitle"><draw:text-box><text:p>Unit one</text:p></draw:text-box></draw:frame>
   <presentation:notes><draw:frame><draw:text-box><text:p>Start with the central question.</text:p></draw:text-box></draw:frame></presentation:notes>
  </draw:page>
  <draw:page draw:name="image" draw:style-name="dp">
   <draw:frame svg:x="1cm" svg:y="1cm" svg:width="20cm" svg:height="3cm" presentation:class="title"><draw:text-box><text:p>Visible figure</text:p></draw:text-box></draw:frame>
   <draw:frame svg:x="5cm" svg:y="5cm" svg:width="8cm" svg:height="6cm"><draw:image xlink:href="Pictures/visible.png"/></draw:frame>
  </draw:page>
  <draw:page draw:name="hidden" draw:style-name="dp" presentation:visibility="hidden">
   <draw:frame svg:x="5cm" svg:y="5cm" svg:width="8cm" svg:height="6cm"><draw:image xlink:href="Pictures/hidden.png"/></draw:frame>
  </draw:page>
 </office:presentation></office:body></office:document-content>"""
	manifest = """<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">
 <manifest:file-entry manifest:full-path="/" manifest:media-type="application/vnd.oasis.opendocument.presentation"/>
 <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="Pictures/visible.png" manifest:media-type="image/png"/>
 <manifest:file-entry manifest:full-path="Pictures/hidden.png" manifest:media-type="image/png"/>
</manifest:manifest>"""
	path = tmp_path / "source.odp"
	with zipfile.ZipFile(path, "w") as archive:
		archive.writestr("mimetype", odp_reader.ODP_MIMETYPE, compress_type=zipfile.ZIP_STORED)
		archive.writestr("content.xml", content)
		archive.writestr("styles.xml", STYLES_XML)
		archive.writestr("META-INF/manifest.xml", manifest)
		archive.writestr("Pictures/visible.png", png_bytes())
		archive.writestr("Pictures/hidden.png", png_bytes())
	return path


#============================================
def test_direct_conversion_publishes_valid_djot_reachable_media_and_source_evidence(
		tmp_path: pathlib.Path,
) -> None:
	"""Native ODP extraction publishes editable Djot and only reachable media."""
	output_path = tmp_path / "lecture.djot"
	summary = odp_to_djot.convert_odp(write_source_odp(tmp_path), output_path)
	report = json.loads(summary.report_path.read_text(encoding="utf-8"))
	parsed = slide_lib.djot_parser.parse_deck(output_path)

	assert summary.visible_slides == len(parsed.slides) == 2
	assert (tmp_path / "assets" / "lecture" / "image_001.png").is_file()
	assert not (tmp_path / "assets" / "lecture" / "image_002.png").exists()
	assert report["slides"][0]["presenter_notes"] == ["Start with the central question."]
	assert report["slides"][0]["source_page_evidence"]["layout_identity"] == "section"


#============================================
def test_direct_conversion_keeps_existing_destination_untouched(tmp_path: pathlib.Path) -> None:
	"""Existing authored targets remain protected before source publication."""
	output_path = tmp_path / "lecture.djot"
	output_path.write_text("authored source\n", encoding="utf-8")
	with pytest.raises(FileExistsError, match="will not overwrite"):
		odp_to_djot.convert_odp(write_source_odp(tmp_path), output_path)
	assert output_path.read_text(encoding="utf-8") == "authored source\n"


#============================================
def test_direct_conversion_removes_assets_when_djot_publication_fails(
		tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""A failed Djot commit marker leaves no deck publication behind."""
	def fail_link(*_args: object, **_kwargs: object) -> None:
		raise OSError("simulated Djot publication failure")

	monkeypatch.setattr(odp_to_djot.os, "link", fail_link)
	with pytest.raises(OSError, match="simulated Djot publication failure"):
		odp_to_djot.convert_odp(write_source_odp(tmp_path), tmp_path / "lecture.djot")
	assert not (tmp_path / "lecture.djot").exists()
	assert not (tmp_path / "assets" / "lecture").exists()


#============================================
def test_direct_conversion_rolls_back_private_staging_after_validation_failure(
		tmp_path: pathlib.Path,
) -> None:
	"""A malformed source leaves no authored Djot or assets publication behind."""
	bad_source = tmp_path / "bad.odp"
	with zipfile.ZipFile(bad_source, "w") as archive:
		archive.writestr("mimetype", odp_reader.ODP_MIMETYPE, compress_type=zipfile.ZIP_STORED)
		archive.writestr("content.xml", "<office:document-content")
		archive.writestr("styles.xml", STYLES_XML)
		archive.writestr("META-INF/manifest.xml", "<manifest:manifest/>")
	with pytest.raises(xml.etree.ElementTree.ParseError):
		odp_to_djot.convert_odp(bad_source, tmp_path / "lecture.djot")
	assert not (tmp_path / "lecture.djot").exists()
	assert not (tmp_path / "assets").exists()
	assert not any(path.name.startswith(".odp_to_djot_") for path in tmp_path.iterdir())
