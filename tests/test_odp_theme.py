"""Behavior tests for applying the authoritative ODP master theme."""

# Standard Library
import zipfile
import pathlib

# PIP3 modules
import defusedxml.ElementTree

# local repo modules
import slide_lib.odp_theme
import slide_lib.presentation_theme


CONTENT_XML = (
	'<?xml version="1.0" encoding="UTF-8"?>'
	'<office:document-content '
	'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
	'xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" '
	'xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" '
	'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">'
	'<office:automatic-styles>'
	'<style:style style:name="pr1" style:family="presentation" '
	'style:parent-style-name="Blank-notes"/>'
	'</office:automatic-styles>'
	'<office:body><office:presentation>'
	'<draw:page draw:name="page1" draw:master-page-name="Blank">'
	'<draw:frame><draw:text-box><text:p>Native content</text:p></draw:text-box></draw:frame>'
	'</draw:page>'
	'</office:presentation></office:body>'
	'</office:document-content>'
)
STYLES_XML = (
	'<?xml version="1.0" encoding="UTF-8"?>'
	'<office:document-styles '
	'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0">'
	'<office:styles/>'
	'</office:document-styles>'
)


#============================================
def write_generated_odp(output_path: pathlib.Path) -> pathlib.Path:
	"""Write one minimal generated ODP package with the default blank master."""
	with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
		mimetype = zipfile.ZipInfo("mimetype")
		mimetype.compress_type = zipfile.ZIP_STORED
		archive.writestr(mimetype, slide_lib.odp_theme.ODP_MIMETYPE)
		archive.writestr("content.xml", CONTENT_XML)
		archive.writestr("styles.xml", STYLES_XML)
	return output_path


#============================================
def test_template_master_replaces_blank_master_without_replacing_content(
		tmp_path: pathlib.Path) -> None:
	"""Generated content remains editable beneath the authoritative template master."""
	input_path = write_generated_odp(tmp_path / "generated.odp")
	output_path = tmp_path / "themed.odp"
	theme = slide_lib.presentation_theme.default_theme()
	slide_lib.odp_theme.apply_template_master(input_path, output_path)
	with zipfile.ZipFile(output_path) as archive:
		mimetype = archive.infolist()[0]
		content_root = defusedxml.ElementTree.fromstring(archive.read("content.xml"))
		styles_root = defusedxml.ElementTree.fromstring(archive.read("styles.xml"))
	page = content_root.find(f".//{slide_lib.odp_theme.DRAW_PAGE}")
	masters = styles_root.findall(".//style:master-page", slide_lib.presentation_theme.NS)
	assert page is not None and \
		page.attrib[slide_lib.odp_theme.DRAW_MASTER_PAGE_NAME] == theme.master_name
	assert mimetype.filename == "mimetype" and mimetype.compress_type == zipfile.ZIP_STORED
	assert "Native content" in "".join(page.itertext()) and any(
		master.attrib[slide_lib.presentation_theme.qname("style", "name")] == theme.master_name
		for master in masters)
