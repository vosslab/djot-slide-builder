"""Semantic tests for concise presentation-build terminal output."""

# Standard Library
import io
import pathlib
import types
from unittest import mock

# PIP3 Modules
import pytest
import rich.console

# Local Modules
import slide_lib.djot_errors
import slide_lib.capacity_report
import slide_lib.native_model
import slide_lib.terminal_output


BLANK_DECK = "=== layout: blank\n"


def capacity_diagnostic(path: pathlib.Path, line: int, slot: str, required: float | None,
		cause: slide_lib.capacity_report.CapacityCause,
		minimum: float | None = None) -> slide_lib.capacity_report.CapacityDiagnostic:
	"""Build one minimal structured finding for terminal-only behavior tests."""
	return slide_lib.capacity_report.CapacityDiagnostic(
		slide_lib.native_model.SourceLocation(path, line), "one-panel", slot, required, 24,
		cause, minimum)


def plain_consoles() -> tuple[rich.console.Console, rich.console.Console, io.StringIO, io.StringIO]:
	"""Create redirected consoles whose plain text is safe for exact assertions."""
	stdout_stream = io.StringIO()
	stderr_stream = io.StringIO()
	stdout = rich.console.Console(file=stdout_stream, force_terminal=False, color_system=None, width=120)
	stderr = rich.console.Console(file=stderr_stream, force_terminal=False, color_system=None, width=120)
	return stdout, stderr, stdout_stream, stderr_stream


#============================================
def test_single_format_summary_is_relative_and_ansi_free(tmp_path: pathlib.Path) -> None:
	"""A redirected single-format summary stays concise, relative, and static."""
	deck_path = tmp_path / "deck.djot"
	deck_path.write_text(BLANK_DECK, encoding="utf-8")
	output_path = tmp_path / "output" / "odp" / "deck.odp"
	output_path.parent.mkdir(parents=True)
	output_path.write_bytes(b"odp")
	stdout_stream = io.StringIO()
	stderr_stream = io.StringIO()
	stdout = rich.console.Console(file=stdout_stream, force_terminal=False, color_system=None, width=100)
	stderr = rich.console.Console(file=stderr_stream, force_terminal=False, color_system=None, width=100)
	compilation, _theme = slide_lib.terminal_output.slide_lib.native_export.compile_deck(
		slide_lib.terminal_output.slide_lib.native_export.parse_deck(deck_path))
	export_result = slide_lib.terminal_output.slide_lib.native_export.ExportResult(
		compilation, (("odp", output_path),))
	with mock.patch.object(slide_lib.terminal_output.slide_lib.native_export, "find_repo_root",
		return_value=tmp_path), mock.patch.object(
		slide_lib.terminal_output.slide_lib.native_export, "export_deck",
		return_value=export_result), mock.patch.object(
		slide_lib.terminal_output.slide_lib.native_export, "compile_deck",
		side_effect=AssertionError("summary uses the export result")):
		status = slide_lib.terminal_output.run_build(str(deck_path), "odp", allow_folder=False,
			output_console=stdout, error_console=stderr)
	text = stdout_stream.getvalue()
	assert status == 0 and "ODP" in text and "PDF" not in text
	assert str(tmp_path) not in text and "\x1b" not in text and stderr_stream.getvalue() == ""


#============================================
def test_summary_prints_source_located_capacity_from_the_export_result(tmp_path: pathlib.Path) -> None:
	"""A completed representable build visibly reports its retained capacity compromise."""
	deck_path = tmp_path / "capacity.djot"
	deck_path.write_text("=== layout: one-panel\n\n@body\n\n" + "word " * 500, encoding="utf-8")
	output_path = tmp_path / "output" / "odp" / "capacity.odp"
	output_path.parent.mkdir(parents=True)
	output_path.write_bytes(b"odp")
	stdout_stream = io.StringIO()
	stderr_stream = io.StringIO()
	stdout = rich.console.Console(file=stdout_stream, force_terminal=False, color_system=None, width=120)
	stderr = rich.console.Console(file=stderr_stream, force_terminal=False, color_system=None, width=120)
	compilation, _theme = slide_lib.terminal_output.slide_lib.native_export.compile_deck(
		slide_lib.terminal_output.slide_lib.native_export.parse_deck(deck_path))
	export_result = slide_lib.terminal_output.slide_lib.native_export.ExportResult(
		compilation, (("odp", output_path),))
	with mock.patch.object(slide_lib.terminal_output.slide_lib.native_export, "find_repo_root",
			return_value=tmp_path), mock.patch.object(
		slide_lib.terminal_output.slide_lib.native_export, "export_deck", return_value=export_result):
		status = slide_lib.terminal_output.run_build(str(deck_path), "odp", allow_folder=False,
			output_console=stdout, error_console=stderr)
	text = stdout_stream.getvalue()
	assert status == 0 and "Capacity: capacity.djot:" in text and "one-panel/body" in text
	assert str(tmp_path) not in text and stderr_stream.getvalue() == ""


#============================================
def test_folder_pdf_build_writes_all_odps_before_staged_pdf_conversion(tmp_path: pathlib.Path) -> None:
	"""A folder PDF build reuses completed ODP results in one staged conversion call."""
	decks = tuple(tmp_path / f"{name}.djot" for name in ("alpha", "beta"))
	for deck_path in decks:
		deck_path.write_text(BLANK_DECK, encoding="utf-8")
	events: list[str] = []
	def export_deck(input_value: str, output_format: str,
			progress_callback: object) -> slide_lib.native_export.ExportResult:
		path = pathlib.Path(input_value)
		odp = tmp_path / "output" / "odp" / f"{path.stem}.odp"
		odp.parent.mkdir(parents=True, exist_ok=True)
		odp.write_bytes(b"odp")
		events.append(f"odp:{path.stem}:{output_format}")
		return slide_lib.native_export.ExportResult(types.SimpleNamespace(capacity_diagnostics=()), (("odp", odp),))
	def convert_batch(inputs: tuple[pathlib.Path, ...], outputs: tuple[pathlib.Path, ...],
			repo_root: pathlib.Path) -> None:
		events.append("pdf")
		assert tuple(path.stem for path in inputs) == ("alpha", "beta")
		for output in outputs:
			output.parent.mkdir(parents=True, exist_ok=True)
			output.write_bytes(b"pdf")
	stdout, stderr, _stdout_stream, stderr_stream = plain_consoles()
	with mock.patch.object(slide_lib.terminal_output.slide_lib.native_export, "find_repo_root",
			return_value=tmp_path), mock.patch.object(
			slide_lib.terminal_output.slide_lib.native_export, "discover_decks", return_value=decks), mock.patch.object(
			slide_lib.terminal_output.slide_lib.native_export, "export_deck", side_effect=export_deck), mock.patch.object(
			slide_lib.terminal_output.slide_lib.native_export, "convert_odps_to_pdfs", side_effect=convert_batch):
		status = slide_lib.terminal_output.run_build(str(tmp_path), "all", output_console=stdout,
			error_console=stderr)
	assert status == 0 and events == ["odp:alpha:odp", "odp:beta:odp", "pdf"]
	assert stderr_stream.getvalue() == ""


#============================================
def test_capacity_inspection_continues_after_physical_error_and_never_exports(
		tmp_path: pathlib.Path) -> None:
	"""A corpus scan keeps later decks and reports recovered plus physical findings once."""
	alpha = tmp_path / "djot" / "alpha.djot"
	beta = tmp_path / "djot" / "beta.djot"
	gamma = tmp_path / "djot" / "gamma.djot"
	for path in (alpha, beta, gamma):
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_text(BLANK_DECK, encoding="utf-8")
	recovered = capacity_diagnostic(gamma, 12, "body", 19.5,
		slide_lib.capacity_report.CapacityCause.PARAGRAPH_LIST)
	physical = slide_lib.capacity_report.PhysicalCapacityError(
		slide_lib.native_model.SourceLocation(beta, 7), "one-panel", "body", 24,
		slide_lib.capacity_report.CapacityCause.TABLE, 1)
	stdout, stderr, stdout_stream, stderr_stream = plain_consoles()
	with mock.patch.object(slide_lib.terminal_output.slide_lib.native_export, "find_repo_root",
			return_value=tmp_path), mock.patch.object(
			slide_lib.terminal_output.slide_lib.native_export, "discover_decks",
			return_value=[alpha, beta, gamma]), mock.patch.object(
			slide_lib.terminal_output.slide_lib.native_export, "parse_deck",
			side_effect=(object(), object(), object())) as parsed, mock.patch.object(
			slide_lib.terminal_output.slide_lib.native_export, "compile_deck",
			side_effect=((types.SimpleNamespace(capacity_diagnostics=()), object()), physical,
				(types.SimpleNamespace(capacity_diagnostics=(recovered,)), object()))) as compiled, mock.patch.object(
			slide_lib.terminal_output.slide_lib.native_export, "export_deck") as exported, mock.patch.object(
			slide_lib.terminal_output.slide_lib.native_export, "convert_odp_to_pdf") as converted:
		status = slide_lib.terminal_output.run_capacity(str(tmp_path / "djot"),
			output_console=stdout, error_console=stderr)
	assert status == 1 and parsed.call_count == 3 and compiled.call_count == 3
	exported.assert_not_called()
	converted.assert_not_called()
	assert stdout_stream.getvalue().splitlines() == [
		"djot/beta.djot:7 layout=one-panel slot=body required<1pt floor=24pt minimum=1pt cause=table",
		"djot/gamma.djot:12 layout=one-panel slot=body required=19.5pt floor=24pt cause=paragraph/list",
		"Capacity summary: 2 concerns (paragraph/list=1, table=1)",
	]
	assert stderr_stream.getvalue() == ""


#============================================
def test_capacity_inspection_is_silent_and_zero_when_every_deck_is_floor_safe(
		tmp_path: pathlib.Path) -> None:
	"""A concern-free compile-only inspection leaves ordinary terminal automation quiet."""
	deck_path = tmp_path / "deck.djot"
	deck_path.write_text(BLANK_DECK, encoding="utf-8")
	stdout, stderr, stdout_stream, stderr_stream = plain_consoles()
	with mock.patch.object(slide_lib.terminal_output.slide_lib.native_export, "find_repo_root",
			return_value=tmp_path), mock.patch.object(
			slide_lib.terminal_output.slide_lib.native_export, "discover_decks",
			return_value=[deck_path]), mock.patch.object(
			slide_lib.terminal_output.slide_lib.native_export, "parse_deck", return_value=object()), mock.patch.object(
			slide_lib.terminal_output.slide_lib.native_export, "compile_deck",
			return_value=(types.SimpleNamespace(capacity_diagnostics=()), object())):
		status = slide_lib.terminal_output.run_capacity(str(deck_path), allow_folder=False,
			output_console=stdout, error_console=stderr)
	assert status == 0 and stdout_stream.getvalue() == "" and stderr_stream.getvalue() == ""


#============================================
@pytest.mark.parametrize(("layout", "source", "slot", "cause"), (
	("title-only", "# " + "title " * 100, "title", "title"),
	("title-slide", "# A concise title\n\n## " + "subtitle " * 100,
		"subtitle", "local-heading"),
	("section", "# A concise title\n\n## " + "subtitle " * 100,
		"subtitle", "local-heading"),
))
def test_capacity_inspection_reports_fixed_frame_recovery(
		tmp_path: pathlib.Path, layout: str, source: str, slot: str, cause: str) -> None:
	"""Each fixed-frame layout reports its selected sub-floor title region to capacity."""
	deck_path = tmp_path / f"{layout}.djot"
	deck_path.write_text(f"=== layout: {layout}\n\n{source}\n", encoding="utf-8")
	stdout, stderr, stdout_stream, stderr_stream = plain_consoles()
	with mock.patch.object(slide_lib.terminal_output.slide_lib.native_export, "find_repo_root",
			return_value=tmp_path):
		status = slide_lib.terminal_output.run_capacity(str(deck_path), allow_folder=False,
			output_console=stdout, error_console=stderr)
	line = stdout_stream.getvalue().splitlines()[0]
	assert status == 1 and f"{layout}.djot:" in line
	assert f"layout={layout} slot={slot}" in line and f"cause={cause}" in line
	assert stderr_stream.getvalue() == ""


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
		status = slide_lib.terminal_output.run_build(str(deck_path), "odp", allow_folder=False,
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
		status = slide_lib.terminal_output.run_build(str(deck_path), "odp", allow_folder=False,
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
			slide_lib.terminal_output.run_build(str(deck_path), "odp",
				output_console=console, error_console=console)
