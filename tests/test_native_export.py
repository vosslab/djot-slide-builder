"""Public-boundary tests for direct sibling presentation export."""

# Standard Library
import datetime
import pathlib
import zipfile
from unittest import mock

# PIP3 Modules
import pytest

# Local Modules
import slide_lib.capacity_report
import slide_lib.layout_content
import slide_lib.native_export
import slide_lib.odf_package
import slide_lib.odp_export
import slide_lib.presentation_theme


ODF_NAMESPACES = {
	"draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
	"presentation": "urn:oasis:names:tc:opendocument:xmlns:presentation:1.0",
	"text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
}


#============================================
def write_deck(tmp_path: pathlib.Path, source: str) -> pathlib.Path:
	"""Write one test-owned inline Djot source."""
	path = tmp_path / "deck.djot"
	path.write_text(source, encoding="utf-8")
	return path


#============================================
def test_render_timestamp_marks_cover_and_final_visible_closer(tmp_path: pathlib.Path) -> None:
	"""One native build date identifies the cover and the actual ending, not every closer."""
	source = write_deck(tmp_path, "=== layout: title-slide\n\n# Lecture 01A\n\n"
		"## Topic\n\n## Dr. Neil Voss\n\n## November 17, 2026\n\n"
		"=== layout: theend\n\n# THE END\n\n"
		"=== layout: one-panel\n\n# Teaching\n\n@body\n\nKeep this editable.\n\n"
		"=== layout: theend\n\n# THE END\n\n"
		"=== layout: theend\nhidden: true\n\n# THE END\n\n"
		"=== layout: reference\n\n# References\n\n@body\n\nFurther reading.\n")
	instant = datetime.datetime(2026, 11, 17, 8, 10, 23,
		tzinfo=datetime.timezone(datetime.timedelta(hours=-6), "CST"))
	with mock.patch.object(slide_lib.native_export, "datetime") as clock:
		clock.datetime.now.return_value.astimezone.return_value = instant
		compilation, _theme = slide_lib.native_export.compile_deck(
			slide_lib.native_export.parse_deck(source))
		clock.datetime.now.assert_called_once()
	stamps = [(index, item) for index, slide in enumerate(compilation.plan.slides)
		for item in slide.objects if item.object_id == "render-timestamp"]
	assert [index for index, _ in stamps] == [0, 3]
	assert all(isinstance(item.content, slide_lib.layout_content.TextContent)
		for _, item in stamps)
	assert all(item.content.paragraphs[0].typography.selected_size_pt < 18.0
		for _, item in stamps)
	assert all(run.style.font_family == "IBM Plex Sans Condensed"
		for _, item in stamps for run in item.content.paragraphs[0].inlines
		if isinstance(run, slide_lib.layout_content.TextRun))
	lines = ["".join(run.text for run in item.content.paragraphs[0].inlines
		if isinstance(run, slide_lib.layout_content.TextRun)) for _, item in stamps]
	assert lines == ["rendered on Tue, Nov 17, 2026 at 8:10:23 AM CST"] * 2


#============================================
def test_native_odp_renderer_writes_editable_objects(tmp_path: pathlib.Path) -> None:
	"""The public native renderer consumes Djot semantics directly into ODP."""
	source_path = write_deck(tmp_path,
		"color-theme: biochemistry\n\n=== layout: one-panel\n\n# Genetics\n\n@body\n\n"
		"[Course website](https://example.test/course)\n\n"
		"- Parent\n\n  - Child\n")
	deck = slide_lib.native_export.parse_deck(source_path)
	odp_path = slide_lib.native_export.render_native_odp(deck, tmp_path / "deck.odp")
	theme = slide_lib.presentation_theme.default_theme("biochemistry")
	with zipfile.ZipFile(odp_path) as archive:
		content_xml = archive.read("content.xml")
		styles_xml = archive.read("styles.xml")
		root = slide_lib.odf_package.parse_xml(content_xml, "content.xml")
	page = root.find(".//draw:page", ODF_NAMESPACES)
	assert page is not None and page.attrib[
		f"{{{ODF_NAMESPACES['presentation']}}}presentation-page-layout-name"]
	assert root.find(".//draw:frame[@presentation:class='outline']", ODF_NAMESPACES) is not None
	assert root.find(".//text:list-item/text:list/text:list-item", ODF_NAMESPACES) is not None
	assert "Course website" in "".join(root.itertext())
	assert f"#{theme.accent_color}".encode() in content_xml
	assert f"#{theme.gradient_start_color}".encode() in styles_xml


#============================================
def test_authored_notes_export_only_to_native_note_objects(tmp_path: pathlib.Path) -> None:
	"""Plain note text stays editable and cannot inject visible ODP XML."""
	source_path = write_deck(tmp_path, "=== layout: one-panel\n@speaker-notes\n"
		"Ask <why> & wait.\n\n- Instructor reminder.\n@body\nStudent content.\n"
		"=== layout: blank\nhidden: true\n@speaker-notes\nHidden reminder.\n")
	deck = slide_lib.native_export.parse_deck(source_path)
	odp_path = slide_lib.native_export.render_native_odp(deck, tmp_path / "deck.odp")
	with zipfile.ZipFile(odp_path) as archive:
		root = slide_lib.odf_package.parse_xml(archive.read("content.xml"), "content.xml")
	pages = root.findall(".//draw:page", ODF_NAMESPACES)
	note_text = [tuple("".join(node.itertext()) for node in page.findall(
		"presentation:notes/draw:frame/draw:text-box/text:p", ODF_NAMESPACES)) for page in pages]
	visible_text = "".join("".join(node.itertext()) for page in pages for node in page
		if node.tag != f"{{{ODF_NAMESPACES['presentation']}}}notes")
	assert note_text == [("Ask <why> & wait.", "", "- Instructor reminder."), ("Hidden reminder.",)]
	assert "Student content." in visible_text and "reminder" not in visible_text and "<why>" not in visible_text


#============================================


#============================================
def test_public_pdf_export_passes_the_generated_odp_to_libreoffice(tmp_path: pathlib.Path) -> None:
	"""The classroom PDF path derives only from the native ODP emitted in this build."""
	source = write_deck(tmp_path, "=== layout: one-panel\n\n@body\n\nText.\n")
	def convert_files(input_paths: tuple[pathlib.Path, ...], output_directory: pathlib.Path,
			output_format: str) -> tuple[pathlib.Path, ...]:
		assert len(input_paths) == 1 and input_paths[0].suffix == ".odp" and input_paths[0].is_file()
		assert output_format == "pdf"
		converted = output_directory / f"{input_paths[0].stem}.pdf"
		converted.write_bytes(b"%PDF-1.4\n")
		return (converted,)
	with mock.patch.object(slide_lib.native_export, "find_repo_root", return_value=tmp_path), \
			mock.patch.object(slide_lib.native_export.slide_lib.libreoffice, "convert_files",
				side_effect=convert_files) as converted:
		result = slide_lib.native_export.export_deck(str(source), "pdf")
	outputs = result.output_paths()
	assert outputs["odp"].is_file() and outputs["pdf"].is_file()
	assert converted.call_args.args[0] == (outputs["odp"],)


#============================================


#============================================
def test_pdf_batch_failure_preserves_existing_destinations(tmp_path: pathlib.Path) -> None:
	"""A failed staged conversion leaves every previously published classroom PDF intact."""
	inputs = tuple(tmp_path / f"{name}.odp" for name in ("alpha", "beta"))
	outputs = tuple(tmp_path / "output" / "pdf" / f"{path.stem}.pdf" for path in inputs)
	for input_path, output_path in zip(inputs, outputs, strict=True):
		input_path.write_bytes(b"odp")
		output_path.parent.mkdir(parents=True, exist_ok=True)
		output_path.write_bytes(f"old-{input_path.stem}".encode("ascii"))
	with mock.patch.object(slide_lib.native_export.slide_lib.libreoffice, "convert_files",
			side_effect=slide_lib.native_export.slide_lib.libreoffice.LibreOfficeError("conversion failed")):
		with pytest.raises(slide_lib.native_export.slide_lib.libreoffice.LibreOfficeError):
			slide_lib.native_export.convert_odps_to_pdfs(inputs, outputs, tmp_path)
	assert tuple(path.read_bytes() for path in outputs) == (b"old-alpha", b"old-beta")


#============================================
def test_folder_discovery_selects_sorted_supported_descendants(tmp_path: pathlib.Path) -> None:
	"""Folder builds retain only Djot decks in stable relative-path order."""
	folder = tmp_path / "slides"
	(folder / "nested").mkdir(parents=True)
	(folder / "z.djot").write_text("=== layout: blank\n", encoding="utf-8")
	(folder / "notes.md").write_text("# Notes\n", encoding="utf-8")
	(folder / "a.djot").write_text("=== layout: blank\n", encoding="utf-8")
	(folder / "nested" / "b.djot").write_text("=== layout: blank\n", encoding="utf-8")
	decks = slide_lib.native_export.discover_decks(str(folder), tmp_path)
	assert [path.relative_to(folder).as_posix() for path in decks] == [
		"a.djot", "nested/b.djot", "z.djot"]


#============================================
def test_input_boundary_rejects_wrong_suffix_and_repository_escape(tmp_path: pathlib.Path) -> None:
	"""Source selection admits only repository-local Djot files."""
	markdown_path = tmp_path / "deck.md"
	markdown_path.write_text("# Not a deck\n", encoding="utf-8")
	with pytest.raises(slide_lib.native_export.PresentationInputError,
			match="use the .djot extension"):
		slide_lib.native_export.validate_input(str(markdown_path), tmp_path)
	repository = tmp_path / "repository"
	repository.mkdir()
	djot_path = write_deck(tmp_path, "=== layout: blank\n")
	with pytest.raises(slide_lib.native_export.PresentationInputError,
			match="inside this repository"):
		slide_lib.native_export.validate_input(str(djot_path), repository)


#============================================
