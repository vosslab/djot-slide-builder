"""Semantic tests for concise presentation-build terminal output."""

# Standard Library
import io
import pathlib
from unittest import mock

# PIP3 Modules
import rich.console

# Local Modules
import slide_lib.terminal_output


#============================================
def plain_consoles() -> tuple[rich.console.Console, rich.console.Console, io.StringIO, io.StringIO]:
	"""Create redirected consoles whose plain text is safe for exact assertions."""
	stdout_stream = io.StringIO()
	stderr_stream = io.StringIO()
	stdout = rich.console.Console(file=stdout_stream, force_terminal=False, color_system=None, width=120)
	stderr = rich.console.Console(file=stderr_stream, force_terminal=False, color_system=None, width=120)
	return stdout, stderr, stdout_stream, stderr_stream


#============================================
def test_capacity_inspection_reports_source_and_slot(tmp_path: pathlib.Path) -> None:
	"""An overfull title points the author to the deck and region to edit."""
	deck_path = tmp_path / "deck.djot"
	deck_path.write_text("=== layout: title-only\n\n# " + "title " * 100 + "\n", encoding="utf-8")
	stdout, stderr, stdout_stream, stderr_stream = plain_consoles()
	with mock.patch.object(slide_lib.terminal_output.slide_lib.native_export, "find_repo_root",
			return_value=tmp_path):
		status = slide_lib.terminal_output.run_capacity(str(deck_path), allow_folder=False,
			output_console=stdout, error_console=stderr)
	line = stdout_stream.getvalue().splitlines()[0]
	assert status == 1 and "deck.djot:" in line
	assert "layout=title-only slot=title" in line
	assert stderr_stream.getvalue() == ""


#============================================
def test_expected_parse_failure_is_concise_relative_stderr(tmp_path: pathlib.Path) -> None:
	"""Expected parse failures return nonzero with deck, stage, reason, and completed count."""
	deck_path = tmp_path / "broken.djot"
	deck_path.write_text("=== layout: unknown\n", encoding="utf-8")
	stdout, stderr, stdout_stream, stderr_stream = plain_consoles()
	with mock.patch.object(slide_lib.terminal_output.slide_lib.native_export, "find_repo_root",
		return_value=tmp_path):
		status = slide_lib.terminal_output.run_build(str(deck_path), "odp", allow_folder=False,
			output_console=stdout, error_console=stderr)
	text = stderr_stream.getvalue()
	required = ("Build failed", "broken.djot", "parsing", "unknown Djot layout", "Completed decks", "0")
	assert status == 1 and all(value in text for value in required)
	assert str(tmp_path) not in text and "Done:" not in stdout_stream.getvalue()
