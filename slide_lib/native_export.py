"""Parse canonical Djot source and export editable native presentations."""

# Standard Library
import collections.abc
import dataclasses
import os
import pathlib
import subprocess
import tempfile

# Local Modules
import slide_lib.djot_parser
import slide_lib.compilation_result
import slide_lib.layout_engine
import slide_lib.libreoffice
import slide_lib.native_model
import slide_lib.odp_export
import slide_lib.presentation_theme


SUPPORTED_SUFFIX = ".djot"


class PresentationInputError(ValueError):
	"""Report an expected presentation-build input selection failure."""


@dataclasses.dataclass(frozen=True)
class ExportResult:
	"""Retain one compile result beside the artifacts produced from its immutable plan."""
	compilation: slide_lib.compilation_result.CompilationResult
	artifacts: tuple[tuple[str, pathlib.Path], ...]

	def __post_init__(self) -> None:
		object.__setattr__(self, "artifacts", tuple(self.artifacts))

	def output_paths(self) -> dict[str, pathlib.Path]:
		"""Return a small copy of the artifacts keyed by requested format."""
		return dict(self.artifacts)


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
	return slide_lib.djot_parser.parse_deck(input_path)


#============================================
def compile_deck(deck: slide_lib.native_model.Deck) -> tuple[slide_lib.compilation_result.CompilationResult,
		slide_lib.presentation_theme.PresentationTheme]:
	"""Compile one semantic deck once against the authoritative OTP theme."""
	theme = slide_lib.presentation_theme.default_theme()
	compilation = slide_lib.layout_engine.compile_layout_deck(deck, theme)
	return compilation, theme


#============================================
def convert_odps_to_pdfs(input_paths: collections.abc.Sequence[pathlib.Path],
		output_paths: collections.abc.Sequence[pathlib.Path], repo_root: pathlib.Path) -> None:
	"""Stage a complete ODP-to-PDF batch before publishing its classroom artifacts."""
	inputs = tuple(input_paths)
	outputs = tuple(output_paths)
	if not inputs or len(inputs) != len(outputs):
		raise ValueError("LibreOffice PDF conversion needs matching nonempty ODP and PDF paths")
	if any(input_path.suffix.lower() != ".odp" for input_path in inputs):
		raise ValueError("LibreOffice PDF inputs must be ODP files")
	if any(output_path.suffix.lower() != ".pdf" for output_path in outputs):
		raise ValueError("LibreOffice PDF outputs must use .pdf")
	# ASVS 2.2.3: each staged artifact has one distinct requested publication target.
	if len(set(outputs)) != len(outputs):
		raise ValueError("LibreOffice PDF outputs must be distinct")
	output_root = repo_root / "output"
	output_root.mkdir(parents=True, exist_ok=True)
	for output_path in outputs:
		output_path.parent.mkdir(parents=True, exist_ok=True)
	with tempfile.TemporaryDirectory(prefix=".libreoffice.", dir=output_root) as temporary_value:
		temporary_root = pathlib.Path(temporary_value)
		conversion_path = temporary_root / "converted"
		conversion_path.mkdir()
		converted_paths = slide_lib.libreoffice.convert_files(inputs, conversion_path, "pdf")
		# ASVS 2.3.3: conversion completes for the whole batch before any final PDF changes.
		for converted_path, output_path in zip(converted_paths, outputs, strict=True):
			os.replace(converted_path, output_path)


#============================================
def convert_odp_to_pdf(input_path: pathlib.Path, output_path: pathlib.Path,
		repo_root: pathlib.Path) -> None:
	"""Use LibreOffice to derive one classroom PDF from its generated ODP."""
	if input_path.suffix.lower() != ".odp":
		raise ValueError(f"LibreOffice PDF input must be an ODP: {input_path}")
	if output_path.suffix.lower() != ".pdf":
		raise ValueError(f"LibreOffice PDF output must use .pdf: {output_path}")
	convert_odps_to_pdfs((input_path,), (output_path,), repo_root)


#============================================
def render_native_odp(deck: slide_lib.native_model.Deck,
		output_path: pathlib.Path) -> pathlib.Path:
	"""Compile and write one editable native ODP."""
	compilation, theme = compile_deck(deck)
	return slide_lib.odp_export.write_odp(compilation.plan, theme, output_path)


#============================================
def report_progress(progress_callback: collections.abc.Callable[[str], None] | None,
		stage: str) -> None:
	"""Report a build stage when the caller supplied a progress callback."""
	if progress_callback is not None:
		progress_callback(stage)


#============================================
def export_deck(input_value: str, output_format: str,
		progress_callback: collections.abc.Callable[[str], None] | None = None) -> ExportResult:
	"""Compile once, write ODP, and derive requested PDF from that ODP."""
	if output_format not in ("all", "odp", "pdf"):
		raise ValueError(f"unsupported output format: {output_format}")
	repo_root = find_repo_root()
	input_path = validate_input(input_value, repo_root)
	deck_name = input_path.stem
	outputs = {"odp": repo_root / f"output/odp/{deck_name}.odp",
		"pdf": repo_root / f"output/pdf/{deck_name}.pdf"}
	report_progress(progress_callback, "parsing")
	deck = parse_deck(input_path)
	compilation, theme = compile_deck(deck)
	generated: dict[str, pathlib.Path] = {}
	if output_format in ("all", "odp", "pdf"):
		report_progress(progress_callback, "odp")
		generated["odp"] = slide_lib.odp_export.write_odp(compilation.plan, theme, outputs["odp"])
	if output_format in ("all", "pdf"):
		report_progress(progress_callback, "pdf")
		convert_odp_to_pdf(outputs["odp"], outputs["pdf"], repo_root)
		generated["pdf"] = outputs["pdf"]
	return ExportResult(compilation, tuple(generated.items()))
