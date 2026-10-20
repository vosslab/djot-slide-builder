"""Verify real cover text survives LibreOffice export and master round-trip."""

import pathlib
import subprocess
import zipfile

import pytest

import slide_lib.djot_parser
import slide_lib.layout_engine
import slide_lib.libreoffice
import slide_lib.odf_package
import slide_lib.odp_export
import slide_lib.presentation_theme


@pytest.mark.parametrize("course", ("genetics", "biotechnology"))
def test_cover_pdf_text(tmp_path: pathlib.Path, course: str) -> None:
	"""The background border must not replace or absorb selectable cover text."""
	source = tmp_path / "cover.djot"
	source.write_text("=== layout: title-slide\n# Lecture 07D\n"
		"## Chi-Square Method (&chi;^2^)\n## Chapter 7\n"
		"## Dr. Neil Voss\n## October 20, 2026\n", encoding="utf-8")
	theme = slide_lib.presentation_theme.default_theme(course)
	plan = slide_lib.layout_engine.compile_layout_deck(
		slide_lib.djot_parser.parse_deck(source), theme).plan
	odp = slide_lib.odp_export.write_odp(plan, theme, tmp_path / "cover.odp")
	pdf = slide_lib.libreoffice.convert_file(odp, tmp_path, "pdf")
	text = subprocess.run(["pdftotext", "-f", "1", "-l", "1", "-layout", str(pdf), "-"],
		check=True, capture_output=True, text=True).stdout
	assert [line.strip() for line in text.splitlines() if line.strip()] == [
		"Lecture 07D", "Chi-Square Method (\u03c72)", "Chapter 7",
		"Dr. Neil Voss", "October 20, 2026"]
	resaved = tmp_path / "resaved"
	resaved.mkdir()
	roundtrip = slide_lib.libreoffice.convert_file(odp, resaved, "odp")
	with zipfile.ZipFile(roundtrip) as archive:
		content = slide_lib.odf_package.parse_xml(archive.read("content.xml"), "content.xml")
		styles = slide_lib.odf_package.parse_xml(archive.read("styles.xml"), "styles.xml")
	ns = slide_lib.presentation_theme.NS
	page = content.find(".//draw:page", ns)
	master_name = page.attrib[slide_lib.presentation_theme.qname("draw", "master-page-name")]
	master = next(item for item in styles.findall(".//style:master-page", ns)
		if item.attrib[slide_lib.presentation_theme.qname("style", "name")] == master_name)
	name = slide_lib.presentation_theme.qname("draw", "name")
	assert any(item.attrib.get(name) == "title-metadata-frame" for item in master)
	assert not any(item.attrib.get(name) == "title-metadata-frame" for item in page)
