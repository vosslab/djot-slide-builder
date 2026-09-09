"""Public-boundary tests for direct sibling presentation export."""

# Standard Library
import dataclasses
import pathlib
import re
import zipfile
from unittest import mock

# PIP3 Modules
import defusedxml.ElementTree
import pytest

# Local Modules
import slide_lib.capacity_report
import slide_lib.native_export
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
def test_native_odp_renderer_writes_editable_objects(tmp_path: pathlib.Path) -> None:
	"""The public native renderer consumes Djot semantics directly into ODP."""
	source_path = write_deck(tmp_path,
		"=== layout: one-panel\n\n# Genetics\n\n@body\n\nVisible prose.\n\n"
		"- Parent\n\n  - Child\n")
	deck = slide_lib.native_export.parse_deck(source_path)
	odp_path = slide_lib.native_export.render_native_odp(deck, tmp_path / "deck.odp")
	with zipfile.ZipFile(odp_path) as archive:
		root = defusedxml.ElementTree.fromstring(archive.read("content.xml"))
	page = root.find(".//draw:page", ODF_NAMESPACES)
	assert page is not None and page.attrib[
		f"{{{ODF_NAMESPACES['presentation']}}}presentation-page-layout-name"]
	assert root.find(".//draw:frame[@presentation:class='outline']", ODF_NAMESPACES) is not None
	assert root.find(".//text:list-item/text:list/text:list-item", ODF_NAMESPACES) is not None
	assert "Visible prose." in "".join(root.itertext())


def test_representable_capacity_recovery_exports_one_native_page_per_source_slide(
		tmp_path: pathlib.Path) -> None:
	"""A reported compromise remains editable at serializer-safe sizes."""
	long = "word " * 500
	source = write_deck(tmp_path, f"=== layout: one-panel\n\n@body\n\n{long}")
	compilation, theme = slide_lib.native_export.compile_deck(slide_lib.native_export.parse_deck(source))
	assert len(compilation.plan.slides) == 1 and compilation.capacity_diagnostics
	assert compilation.capacity_diagnostics[0].cause is \
		slide_lib.capacity_report.CapacityCause.PARAGRAPH_LIST
	odp_path = slide_lib.odp_export.write_odp(compilation.plan, theme, tmp_path / "deck.odp")
	with zipfile.ZipFile(odp_path) as archive:
		content = archive.read("content.xml").decode("utf-8")
	assert len(defusedxml.ElementTree.fromstring(content).findall(".//draw:page", ODF_NAMESPACES)) == 1
	sizes = tuple(float(value) for value in re.findall(r'font-size="([0-9.]+)pt"', content))
	assert sizes and all(size >= 1.0 for size in sizes)


#============================================
def test_table_capacity_cause_survives_the_native_compile_boundary(tmp_path: pathlib.Path) -> None:
	"""Table fitting retains its explicit source-region cause with the export compilation."""
	rows = "".join("| cell cell cell cell |\n" for _ in range(30))
	source = write_deck(tmp_path, "=== layout: one-panel\n\n@body\n\n| A |\n| - |\n" + rows)
	compilation, _theme = slide_lib.native_export.compile_deck(
		slide_lib.native_export.parse_deck(source))
	diagnostic = next(item for item in compilation.capacity_diagnostics
		if item.cause is slide_lib.capacity_report.CapacityCause.TABLE)
	assert diagnostic.location.path == source and diagnostic.slot == "body"
	assert diagnostic.required_size_pt is not None and diagnostic.required_size_pt < diagnostic.floor_size_pt


def test_nonempty_notes_and_reveals_survive_native_projection(tmp_path: pathlib.Path) -> None:
	"""One source slide retains authored notes and reveal timing in its editable ODP."""
	source = write_deck(tmp_path, "=== layout: one-panel\n\n@body\n\n=> appear\nVisible later.")
	deck = slide_lib.native_export.parse_deck(source)
	deck = dataclasses.replace(deck, slides=(dataclasses.replace(deck.slides[0], notes=("Speaker note",)),))
	compilation, theme = slide_lib.native_export.compile_deck(deck)
	odp_path = slide_lib.odp_export.write_odp(compilation.plan, theme, tmp_path / "deck.odp")
	with zipfile.ZipFile(odp_path) as archive:
		content = archive.read("content.xml")
	assert b"Speaker note" in content and b"presentation:notes" in content


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
def test_pdf_batch_publishes_only_after_all_staged_odp_results_exist(tmp_path: pathlib.Path) -> None:
	"""Two completed staged PDFs replace their requested classroom destinations together."""
	inputs = tuple(tmp_path / f"{name}.odp" for name in ("alpha", "beta"))
	outputs = tuple(tmp_path / "output" / "pdf" / f"{path.stem}.pdf" for path in inputs)
	for input_path in inputs:
		input_path.write_bytes(b"odp")
	def convert_files(input_paths: tuple[pathlib.Path, ...], staging: pathlib.Path,
			output_format: str) -> tuple[pathlib.Path, ...]:
		assert input_paths == inputs and output_format == "pdf"
		converted = tuple(staging / f"{path.stem}.pdf" for path in input_paths)
		for path in converted:
			path.write_bytes(b"pdf")
		return converted
	with mock.patch.object(slide_lib.native_export.slide_lib.libreoffice, "convert_files",
			side_effect=convert_files):
		slide_lib.native_export.convert_odps_to_pdfs(inputs, outputs, tmp_path)
	assert tuple(path.read_bytes() for path in outputs) == (b"pdf", b"pdf")


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
def test_libreoffice_pdf_helper_requires_odp_input_and_pdf_output(tmp_path: pathlib.Path) -> None:
	"""The focused conversion helper preserves the generated-ODP PDF boundary."""
	with pytest.raises(ValueError, match="must be an ODP"):
		slide_lib.native_export.convert_odp_to_pdf(tmp_path / "deck.wrong", tmp_path / "deck.pdf", tmp_path)
	with pytest.raises(ValueError, match="must use .pdf"):
		slide_lib.native_export.convert_odp_to_pdf(tmp_path / "deck.odp", tmp_path / "deck.wrong", tmp_path)


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
def test_folder_discovery_rejects_empty_source_selection(tmp_path: pathlib.Path) -> None:
	"""A folder without Djot sources receives an actionable input error."""
	folder = tmp_path / "slides"
	folder.mkdir()
	(folder / "notes.md").write_text("# Notes\n", encoding="utf-8")
	with pytest.raises(slide_lib.native_export.PresentationInputError,
			match="no presentation source decks found"):
		slide_lib.native_export.discover_decks(str(folder), tmp_path)
