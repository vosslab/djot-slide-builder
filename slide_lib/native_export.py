"""Parse canonical Djot source and export editable native presentations."""

# Standard Library
import os
import pathlib
import subprocess
import tempfile
import collections.abc

# PIP3 modules
from pptx import Presentation
from pptx.enum.text import PP_ALIGN

# Local Modules
from slide_lib import layouts
from slide_lib import libreoffice
from slide_lib import djot_parser
from slide_lib import pptx_animation
import slide_lib.native_model


SUPPORTED_SUFFIX = ".djot"


class PresentationInputError(ValueError):
	"""Report an expected presentation-build input selection failure."""


#============================================
def find_repo_root() -> pathlib.Path:
	"""Return the current Git repository root."""
	result = subprocess.run(["git", "rev-parse", "--show-toplevel"], check=True,
		capture_output=True, text=True)
	return pathlib.Path(result.stdout.strip()).resolve()


#============================================
def validate_input(input_value: str, repo_root: pathlib.Path) -> pathlib.Path:
	"""Resolve one supported source deck inside this repository."""
	input_path = pathlib.Path(input_value).expanduser().resolve()
	if not input_path.is_file():
		raise PresentationInputError(f"input is not a file: {input_value}")
	if not input_path.is_relative_to(repo_root):
		raise PresentationInputError("input must be inside this repository")
	# ASVS 2.2.1: one positive suffix check owns source admission.
	if input_path.suffix != SUPPORTED_SUFFIX:
		raise PresentationInputError("input must use the .djot extension")
	return input_path


#============================================
def discover_decks(input_value: str, repo_root: pathlib.Path,
		allow_folder: bool = True) -> list[pathlib.Path]:
	"""Resolve one deck or sorted supported decks recursively below one folder."""
	input_path = pathlib.Path(input_value).expanduser().resolve()
	if input_path.is_file():
		return [validate_input(input_value, repo_root)]
	if not input_path.is_dir():
		raise PresentationInputError(f"input is not a file or folder: {input_value}")
	if not allow_folder:
		raise PresentationInputError(f"input is not a presentation source file: {input_value}")
	if not input_path.is_relative_to(repo_root):
		raise PresentationInputError("input must be inside this repository")
	decks = [path for path in input_path.rglob(f"*{SUPPORTED_SUFFIX}") if path.is_file()]
	decks.sort(key=lambda path: path.relative_to(input_path).as_posix())
	if not decks:
		raise PresentationInputError(f"no presentation source decks found in: {input_value}")
	return decks


#============================================
def parse_deck(input_path: pathlib.Path) -> slide_lib.native_model.Deck:
	"""Parse one validated Djot source deck through its typed semantic parser."""
	if input_path.suffix != SUPPORTED_SUFFIX:
		raise PresentationInputError(f"input must use the .djot extension: {input_path}")
	return djot_parser.parse_deck(input_path)


#============================================
def render_native_pptx(deck: slide_lib.native_model.Deck, output_path: pathlib.Path) -> pathlib.Path:
	"""Write every parsed slide as separate editable native PPTX objects."""
	presentation = Presentation()
	presentation.slide_width = layouts.px(layouts.SLIDE_WIDTH)
	presentation.slide_height = layouts.px(layouts.SLIDE_HEIGHT)
	presentation.core_properties.title = deck.title
	blank_layout = presentation.slide_layouts[6]
	for number, source in enumerate(deck.slides, start=1):
		slide = presentation.slides.add_slide(blank_layout)
		writer = pptx_animation.PptxAnimationWriter(slide)
		layouts.render_layout(slide, source, deck, writer)
		if source.paginate:
			text_frame = layouts.add_textbox(slide, 1190, 762, 62, 22)
			text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT
			layouts.write_run(text_frame.paragraphs[0].add_run(), str(number), 18, layouts.MUTED)
		if source.notes:
			slide.notes_slide.notes_text_frame.text = "\n\n".join(source.notes)
		writer.finalize()
	output_path.parent.mkdir(parents=True, exist_ok=True)
	presentation.save(output_path)
	return output_path


#============================================
def convert_presentation(input_path: pathlib.Path, output_path: pathlib.Path,
		output_format: str, repo_root: pathlib.Path) -> None:
	"""Use LibreOffice to convert one editable presentation artifact."""
	output_root = repo_root / "output"
	output_root.mkdir(parents=True, exist_ok=True)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	with tempfile.TemporaryDirectory(prefix=".libreoffice.", dir=output_root) as temporary_value:
		temporary_root = pathlib.Path(temporary_value)
		conversion_path = temporary_root / "converted"
		conversion_path.mkdir()
		converted_path = libreoffice.convert_file(input_path, conversion_path, output_format)
		os.replace(converted_path, output_path)


#============================================
def report_progress(progress_callback: collections.abc.Callable[[str], None] | None,
		stage: str) -> None:
	"""Report a build stage when the caller supplied a progress callback."""
	if progress_callback is not None:
		progress_callback(stage)


#============================================
def export_deck(input_value: str, output_format: str,
		progress_callback: collections.abc.Callable[[str], None] | None = None) -> dict[str, pathlib.Path]:
	"""Export PPTX, then editable ODP, then PDF from that ODP when requested."""
	if output_format not in ("all", "odp", "pdf", "pptx"):
		raise ValueError(f"unsupported output format: {output_format}")
	repo_root = find_repo_root()
	input_path = validate_input(input_value, repo_root)
	deck_name = input_path.stem
	outputs = {"pptx": repo_root / f"output/pptx/{deck_name}.pptx",
		"odp": repo_root / f"output/odp/{deck_name}.odp",
		"pdf": repo_root / f"output/pdf/{deck_name}.pdf"}
	report_progress(progress_callback, "parsing")
	deck = parse_deck(input_path)
	report_progress(progress_callback, "pptx")
	generated = {"pptx": render_native_pptx(deck, outputs["pptx"])}
	if output_format in ("all", "odp", "pdf"):
		report_progress(progress_callback, "odp")
		convert_presentation(outputs["pptx"], outputs["odp"], "odp", repo_root)
		generated["odp"] = outputs["odp"]
	if output_format in ("all", "pdf"):
		report_progress(progress_callback, "pdf")
		convert_presentation(outputs["odp"], outputs["pdf"], "pdf", repo_root)
		generated["pdf"] = outputs["pdf"]
	return generated
