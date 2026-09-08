"""Semantic tests for concise presentation-build terminal output."""

# Standard Library
import io
import pathlib
from unittest import mock

# PIP3 Modules
import pytest
import rich.console

# Local Modules
import slide_lib.djot_errors
import slide_lib.terminal_output


BLANK_DECK = "=== layout: blank\n"


#============================================
def test_single_format_summary_is_relative_and_ansi_free(tmp_path: pathlib.Path) -> None:
	"""A redirected single-format summary stays concise, relative, and static."""
	deck_path = tmp_path / "deck.djot"
	deck_path.write_text(BLANK_DECK, encoding="utf-8")
	output_path = tmp_path / "output" / "pptx" / "deck.pptx"
	output_path.parent.mkdir(parents=True)
	output_path.write_bytes(b"pptx")
	stdout_stream = io.StringIO()
	stderr_stream = io.StringIO()
	stdout = rich.console.Console(file=stdout_stream, force_terminal=False, color_system=None, width=100)
	stderr = rich.console.Console(file=stderr_stream, force_terminal=False, color_system=None, width=100)
	with mock.patch.object(slide_lib.terminal_output.slide_lib.native_export, "find_repo_root",
		return_value=tmp_path), mock.patch.object(
		slide_lib.terminal_output.slide_lib.native_export, "export_deck",
		return_value={"pptx": output_path}):
		status = slide_lib.terminal_output.run_build(str(deck_path), "pptx", allow_folder=False,
			output_console=stdout, error_console=stderr)
	text = stdout_stream.getvalue()
	assert status == 0 and "PPTX" in text and "ODP" not in text and "PDF" not in text
	assert str(tmp_path) not in text and "\x1b" not in text and stderr_stream.getvalue() == ""


#============================================
def test_expected_parse_failure_is_concise_relative_stderr(tmp_path: pathlib.Path) -> None:
	"""Expected parse failures return nonzero with deck, stage, reason, and completed count."""
	deck_path = tmp_path / "broken.djot"
	deck_path.write_text("=== layout: unknown\n", encoding="utf-8")
	stdout_stream = io.StringIO()
	stderr_stream = io.StringIO()
	stdout = rich.console.Console(file=stdout_stream, force_terminal=False, color_system=None, width=120)
	stderr = rich.console.Console(file=stderr_stream, force_terminal=False, color_system=None, width=120)
	with mock.patch.object(slide_lib.terminal_output.slide_lib.native_export, "find_repo_root",
		return_value=tmp_path):
		status = slide_lib.terminal_output.run_build(str(deck_path), "pptx", allow_folder=False,
			output_console=stdout, error_console=stderr)
	text = stderr_stream.getvalue()
	required = ("Build failed", "broken.djot", "parsing", "unknown Djot layout", "Completed decks", "0")
	assert status == 1 and all(value in text for value in required)
	assert str(tmp_path) not in text and "Done:" not in stdout_stream.getvalue()


#============================================
def test_djot_parse_failure_uses_the_expected_concise_terminal_lane(tmp_path: pathlib.Path) -> None:
	"""Djot source errors stay source-located without exposing local paths or tracebacks."""
	deck_path = tmp_path / "broken.djot"
	deck_path.write_text("=== layout: blank\n", encoding="utf-8")
	stdout_stream = io.StringIO()
	stderr_stream = io.StringIO()
	stdout = rich.console.Console(file=stdout_stream, force_terminal=False, color_system=None, width=120)
	stderr = rich.console.Console(file=stderr_stream, force_terminal=False, color_system=None, width=120)
	error = slide_lib.djot_errors.DjotParseError(f"{deck_path}:2: unsupported Djot construct")
	with mock.patch.object(slide_lib.terminal_output.slide_lib.native_export, "find_repo_root",
		return_value=tmp_path), mock.patch.object(
		slide_lib.terminal_output.slide_lib.native_export, "export_deck", side_effect=error):
		status = slide_lib.terminal_output.run_build(str(deck_path), "pptx", allow_folder=False,
			output_console=stdout, error_console=stderr)
	text = stderr_stream.getvalue()
	assert status == 1 and "broken.djot:2:" in text and "traceback" not in text.lower()
	assert str(tmp_path) not in text and "Done:" not in stdout_stream.getvalue()


#============================================
def test_unexpected_export_defect_retains_exception(tmp_path: pathlib.Path) -> None:
	"""Unexpected defects escape the expected-error interface for a normal traceback."""
	deck_path = tmp_path / "deck.djot"
	deck_path.write_text(BLANK_DECK, encoding="utf-8")
	console = rich.console.Console(file=io.StringIO(), force_terminal=False, color_system=None)
	with mock.patch.object(slide_lib.terminal_output.slide_lib.native_export, "find_repo_root",
		return_value=tmp_path), mock.patch.object(
		slide_lib.terminal_output.slide_lib.native_export, "export_deck",
		side_effect=ValueError("unexpected defect")):
		with pytest.raises(ValueError, match="unexpected defect"):
			slide_lib.terminal_output.run_build(str(deck_path), "pptx",
				output_console=console, error_console=console)
