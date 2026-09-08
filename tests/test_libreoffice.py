"""Focused tests for the shared LibreOffice batch-conversion contract."""

# Standard Library
import pathlib
import subprocess
from unittest import mock

# PIP3 modules
import pytest

# Local Modules
from slide_lib import libreoffice


#============================================
def test_convert_file_uses_headless_norestore_and_established_profile(
		tmp_path: pathlib.Path) -> None:
	"""Normal conversion uses batch flags without a disposable user profile."""
	input_path = tmp_path / "deck.odp"
	input_path.write_bytes(b"source")
	output_dir = tmp_path / "converted"
	output_dir.mkdir()
	commands: list[list[str]] = []

	def write_converted_file(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
		"""Create the output that the mocked LibreOffice command represents."""
		commands.append(command)
		(output_dir / "deck.pdf").write_bytes(b"pdf")
		return subprocess.CompletedProcess(command, 0)

	with mock.patch.object(libreoffice, "require_libreoffice_closed"), \
		mock.patch.object(libreoffice, "require_soffice", return_value=pathlib.Path("/usr/bin/soffice")), \
		mock.patch.object(libreoffice.subprocess, "run", side_effect=write_converted_file):
		converted_path = libreoffice.convert_file(input_path, output_dir, "pdf")

	assert converted_path == output_dir / "deck.pdf"
	assert "--headless" in commands[0]
	assert "--norestore" in commands[0]
	assert all(not value.startswith("-env:UserInstallation=") for value in commands[0])


#============================================
def test_require_libreoffice_closed_rejects_desktop_process() -> None:
	"""A running main LibreOffice process receives an actionable batch-build error."""
	processes = "/Applications/LibreOffice.app/Contents/MacOS/soffice.bin --writer\n"
	result = subprocess.CompletedProcess(["ps"], 0, stdout=processes)
	with mock.patch.object(libreoffice.subprocess, "run", return_value=result):
		with pytest.raises(RuntimeError, match="LibreOffice is running; close it"):
			libreoffice.require_libreoffice_closed()


#============================================
def test_require_libreoffice_closed_ignores_quicklook_extension() -> None:
	"""The LibreOffice Quick Look extension does not block presentation builds."""
	processes = "/Applications/LibreOffice.app/Contents/PlugIns/QuickLookThumbnail.appex/helper\n"
	result = subprocess.CompletedProcess(["ps"], 0, stdout=processes)
	with mock.patch.object(libreoffice.subprocess, "run", return_value=result):
		libreoffice.require_libreoffice_closed()


#============================================
def test_successful_conversion_captures_and_hides_libreoffice_output(
		tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]) -> None:
	"""Successful third-party chatter never reaches the presentation build stream."""
	input_path = tmp_path / "deck.pptx"
	input_path.write_bytes(b"source")
	output_dir = tmp_path / "converted"
	output_dir.mkdir()
	call_options: list[dict[str, object]] = []

	def finish_conversion(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
		"""Return noisy success while creating the represented ODP artifact."""
		call_options.append(kwargs)
		(output_dir / "deck.odp").write_bytes(b"odp")
		return subprocess.CompletedProcess(command, 0, stdout="convert chatter\n", stderr="warning\n")

	with mock.patch.object(libreoffice, "require_libreoffice_closed"), \
		mock.patch.object(libreoffice, "require_soffice", return_value=pathlib.Path("/usr/bin/soffice")), \
		mock.patch.object(libreoffice.subprocess, "run", side_effect=finish_conversion):
		libreoffice.convert_file(input_path, output_dir, "odp")
	captured = capsys.readouterr()
	assert captured.out == "" and captured.err == ""
	assert call_options[0]["capture_output"] is True and call_options[0]["text"] is True


#============================================
def test_failed_conversion_reports_captured_diagnostics(tmp_path: pathlib.Path) -> None:
	"""A failed conversion retains actionable stdout and stderr without a raw command."""
	input_path = tmp_path / "deck.pptx"
	input_path.write_bytes(b"source")
	output_dir = tmp_path / "converted"
	output_dir.mkdir()
	result = subprocess.CompletedProcess(["soffice"], 7,
		stdout="source format rejected\n", stderr="presentation filter unavailable\n")
	with mock.patch.object(libreoffice, "require_libreoffice_closed"), \
		mock.patch.object(libreoffice, "require_soffice", return_value=pathlib.Path("/usr/bin/soffice")), \
		mock.patch.object(libreoffice.subprocess, "run", return_value=result):
		with pytest.raises(libreoffice.LibreOfficeError,
			match="presentation filter unavailable; source format rejected"):
			libreoffice.convert_file(input_path, output_dir, "odp")
