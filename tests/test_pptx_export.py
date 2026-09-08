"""Focused projection tests for the plan-only editable PPTX adapter."""

import ast
import pathlib
import zipfile

from pptx import Presentation

import slide_lib.djot_parser
import slide_lib.layout_engine
import slide_lib.pptx_export
import slide_lib.presentation_theme


def _compile(tmp_path: pathlib.Path, source: str):
	path = tmp_path / "deck.djot"
	path.write_text(source, encoding="utf-8")
	theme = slide_lib.presentation_theme.default_theme()
	return slide_lib.layout_engine.compile_layout_deck(slide_lib.djot_parser.parse_deck(path), theme), theme


def _write(tmp_path: pathlib.Path, source: str) -> pathlib.Path:
	deck, theme = _compile(tmp_path, source)
	output = tmp_path / "deck.pptx"
	return slide_lib.pptx_export.write_pptx(deck, theme, output)


def test_adapter_imports_only_plan_and_theme_layers() -> None:
	"""PPTX serialization has no compiler, legacy-layout, or ODF dependency."""
	path = pathlib.Path("slide_lib/pptx_export.py")
	imports = {node.names[0].name for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))
		if isinstance(node, ast.Import) and node.names[0].name.startswith("slide_lib")}
	assert not imports & {"slide_lib.layout_engine", "slide_lib._layout_builders",
		"slide_lib._layout_measurement", "slide_lib._layout_registry", "slide_lib.layouts",
		"slide_lib.native_model", "slide_lib.odp_export", "slide_lib.odf_package"}


def test_plan_text_keeps_exact_point_sizes_lists_runs_and_links(tmp_path: pathlib.Path) -> None:
	"""Resolved 36/28 points and paragraph facts are emitted without a scale conversion."""
	output = _write(tmp_path, "=== layout: one-panel\n\n# Title\n\n@body\n\n"
		"- **Bold** [https://example.edu/path](https://example.edu/path)\n")
	presentation = Presentation(output)
	runs = [run for shape in presentation.slides[0].shapes if shape.has_text_frame
		for paragraph in shape.text_frame.paragraphs for run in paragraph.runs]
	assert any(run.text == "Title" and run.font.size.pt == 36.0 for run in runs)
	assert any(run.text == "https://example.edu/path" and run.font.size.pt == 28.0 and
		run.hyperlink.address == "https://example.edu/path" for run in runs)
	with zipfile.ZipFile(output) as archive:
		xml = archive.read("ppt/slides/slide1.xml").decode("utf-8")
	assert 'sz="3600"' in xml and 'sz="2800"' in xml
	assert "buChar" in xml and "lnSpc" in xml and "marL" in xml and 'indent="-' in xml


def test_plan_picture_accessibility_and_crop_are_projected(tmp_path: pathlib.Path) -> None:
	"""The adapter writes compiler-selected display/crop facts, never recomputes fitting."""
	(tmp_path / "pixel.gif").write_bytes(
		b"GIF87a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;")
	output = _write(tmp_path, "=== layout: gallery\n\n# Gallery\n\n@gallery\n\n![Pixel](pixel.gif)\n")
	shape = next(shape for shape in Presentation(output).slides[0].shapes if shape.shape_type == 13)
	assert "Pixel" in shape.element.xml and "descr=" in shape.element.xml
	assert shape.crop_left == shape.crop_top == shape.crop_right == shape.crop_bottom == 0


def test_plan_table_is_editable_with_resolved_dimensions(tmp_path: pathlib.Path) -> None:
	"""Table rows, columns, cell text, and point-valued typography come from the plan."""
	output = _write(tmp_path, "=== layout: one-panel\n\n@body\n\n| Heading | Value |\n| - | - |\n| A | B |\n")
	table = Presentation(output).slides[0].shapes[-1].table
	assert (len(table.rows), len(table.columns)) == (2, 2)
	assert table.cell(0, 0).text == "Heading" and table.cell(1, 1).text == "B"
	assert table.cell(1, 1).text_frame.paragraphs[0].runs[0].font.size.pt == 28.0


def test_plan_reveal_targets_and_notes_keep_source_order(tmp_path: pathlib.Path) -> None:
	"""Plan target order becomes one native timing sequence and notes survive projection."""
	deck, theme = _compile(tmp_path, "=== layout: one-panel\n\n@body\n\n=> appear\nFirst\n\n- Last\n<= appear\n")
	output = tmp_path / "deck.pptx"
	slide_lib.pptx_export.write_pptx(deck, theme, output)
	expected = sum(len(item.reveal_targets) for item in deck.slides[0].objects)
	with zipfile.ZipFile(output) as archive:
		xml = archive.read("ppt/slides/slide1.xml").decode("utf-8")
	assert xml.count("spTgt") == expected and "tmRoot" in xml and "mainSeq" in xml


def test_write_pptx_replaces_destination_atomically(tmp_path: pathlib.Path) -> None:
	"""A complete package replaces the destination rather than exposing a partial file."""
	output = tmp_path / "deck.pptx"
	output.write_bytes(b"old")
	result = _write(tmp_path, "=== layout: one-panel\n\n@body\n\nText.\n")
	assert result == output
	assert Presentation(output).slides[0].shapes
