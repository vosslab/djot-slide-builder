"""Small source-compilation helpers shared by layout behavior tests."""

import pathlib

import PIL.Image

import slide_lib.compilation_result
import slide_lib.djot_parser
import slide_lib.layout_engine
import slide_lib.native_model
import slide_lib.presentation_theme


def parsed_source(tmp_path: pathlib.Path, source: str) -> slide_lib.native_model.Deck:
	"""Write and parse one test-owned Djot specimen."""
	path = tmp_path / "specimen.djot"
	path.write_text(source, encoding="utf-8")
	return slide_lib.djot_parser.parse_deck(path)


def compile_source(tmp_path: pathlib.Path, source: str) -> slide_lib.compilation_result.CompilationResult:
	"""Compile one test-owned source with the authoritative native theme."""
	return slide_lib.layout_engine.compile_layout_deck(
		parsed_source(tmp_path, source), slide_lib.presentation_theme.default_theme())


def write_image(tmp_path: pathlib.Path, name: str) -> None:
	"""Create one inline test-owned component image with an intentionally tall aspect ratio."""
	PIL.Image.new("RGB", (120, 320), (20, 90, 160)).save(tmp_path / name)
