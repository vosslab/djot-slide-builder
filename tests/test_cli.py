"""Behavior tests for the format-neutral presentation application CLI."""

# Standard Library
import pathlib

# PIP3 Modules
import pytest

# Local Modules
import slide_lib.cli
import slide_lib.terminal_output
import slide_lib.importers.odp_to_djot


#============================================
def test_import_command_dispatches_source_and_output(monkeypatch: pytest.MonkeyPatch,
		tmp_path: pathlib.Path) -> None:
	"""The native ODP extension selects the Djot importer and forwards output."""
	received: list[tuple[str, pathlib.Path, pathlib.Path | None]] = []
	def record(importer_name: str) -> slide_lib.cli.ImportOperation:
		def run_import(input_file: pathlib.Path, output_file: pathlib.Path | None) -> None:
			received.append((importer_name, input_file, output_file))
		return run_import
	monkeypatch.setattr(slide_lib.importers.odp_to_djot, "run_import", record("odp-djot"))

	odp_path = tmp_path / "lecture.odp"
	djot_path = tmp_path / "lecture.djot"
	status = slide_lib.cli.main(["import", str(odp_path), "--output", str(djot_path)])
	assert status == 0
	assert received == [("odp-djot", odp_path, djot_path)]


#============================================
def test_import_command_rejects_unsupported_source_suffix(tmp_path: pathlib.Path,
		capsys: pytest.CaptureFixture[str]) -> None:
	"""Only trusted native ODP reaches the importer."""
	status = slide_lib.cli.main(["import", str(tmp_path / "lecture.pdf")])
	assert status == 2
	assert "must use the .odp extension" in capsys.readouterr().err


#============================================
def test_build_command_dispatches_path_and_format(monkeypatch: pytest.MonkeyPatch,
		tmp_path: pathlib.Path) -> None:
	"""Parsed build arguments reach the existing application build operation."""
	deck_path = tmp_path / "lecture.djot"
	deck_path.write_text("=== layout: blank\n", encoding="utf-8")
	received: list[tuple[str, str]] = []
	def record(input_value: str, output_format: str) -> int:
		received.append((input_value, output_format))
		return 0
	monkeypatch.setattr(slide_lib.terminal_output, "run_build", record)
	status = slide_lib.cli.main(["build", str(deck_path), "-f", "odp"])
	assert received == [(str(deck_path), "odp")]
	assert status == 0


#============================================
def test_capacity_command_dispatches_its_source_path(monkeypatch: pytest.MonkeyPatch,
		tmp_path: pathlib.Path) -> None:
	"""The inspection command forwards only its source argument to the capacity runner."""
	deck_path = tmp_path / "lecture.djot"
	deck_path.write_text("=== layout: blank\n", encoding="utf-8")
	received: list[str] = []
	def record(input_value: str) -> int:
		received.append(input_value)
		return 1
	monkeypatch.setattr(slide_lib.terminal_output, "run_capacity", record)
	status = slide_lib.cli.main(["capacity", str(deck_path)])
	assert received == [str(deck_path)]
	assert status == 1
