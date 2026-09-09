"""Focused public-behavior tests for sequential LibreOffice conversion."""

# Standard Library
import pathlib
import subprocess
from unittest import mock

# PIP3 Modules
import pytest

# Local Modules
from slide_lib import libreoffice


#============================================
def test_convert_files_runs_direct_commands_in_source_order(tmp_path: pathlib.Path) -> None:
	"""One desktop preflight precedes direct sequential conversion commands."""
	inputs = tuple(tmp_path / name for name in ("alpha.odp", "beta.odp"))
	for input_path in inputs:
		input_path.write_bytes(b"source")
	output_dir = tmp_path / "converted"
	output_dir.mkdir()
	commands: list[list[str]] = []

	def run(command: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
		commands.append(command)
		(output_dir / f"{pathlib.Path(command[-1]).stem}.pdf").write_bytes(b"pdf")
		return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

	with mock.patch.object(libreoffice, "require_libreoffice_closed") as preflight, \
			mock.patch.object(libreoffice, "require_soffice", return_value=pathlib.Path("/usr/bin/soffice")), \
			mock.patch.object(libreoffice.subprocess, "run", side_effect=run), \
			mock.patch.object(libreoffice.time, "sleep") as settle:
		converted = libreoffice.convert_files(inputs, output_dir, "pdf")

	assert converted == tuple(output_dir / f"{path.stem}.pdf" for path in inputs)
	assert preflight.call_count == 1 and [command[-1] for command in commands] == [str(path) for path in inputs]
	assert all("--headless" in command and "--norestore" in command and "--outdir" in command
		and command[command.index("--convert-to") + 1].startswith("pdf:impress_pdf_Export:")
		and not any(value.startswith("-env:UserInstallation=") for value in command)
		for command in commands) and settle.call_count == 2


#============================================
def test_convert_files_reports_missing_expected_output(tmp_path: pathlib.Path) -> None:
	"""A successful converter result still requires the expected PDF artifact."""
	input_path = tmp_path / "deck.odp"
	input_path.write_bytes(b"source")
	output_dir = tmp_path / "converted"
	output_dir.mkdir()
	result = subprocess.CompletedProcess(["soffice"], 0, stdout="", stderr="")
	with mock.patch.object(libreoffice, "require_libreoffice_closed"), \
			mock.patch.object(libreoffice, "require_soffice", return_value=pathlib.Path("/usr/bin/soffice")), \
			mock.patch.object(libreoffice.subprocess, "run", return_value=result):
		with pytest.raises(libreoffice.LibreOfficeError, match="deck.pdf"):
			libreoffice.convert_files((input_path,), output_dir, "pdf")


#============================================
def test_convert_file_delegates_one_input_to_sequential_boundary(tmp_path: pathlib.Path) -> None:
	"""The one-file API remains a compact wrapper around the common converter."""
	input_path = tmp_path / "deck.odp"
	output_dir = tmp_path / "converted"
	with mock.patch.object(libreoffice, "convert_files", return_value=(output_dir / "deck.pdf",)) as convert:
		converted = libreoffice.convert_file(input_path, output_dir, "pdf")
	assert converted == output_dir / "deck.pdf" and convert.call_args.args == ((input_path,), output_dir, "pdf")
