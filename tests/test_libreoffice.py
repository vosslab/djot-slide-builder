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
def test_convert_files_reports_missing_expected_output(tmp_path: pathlib.Path) -> None:
	"""A successful converter result still requires the expected PDF artifact."""
	input_path = tmp_path / "deck.odp"
	input_path.write_bytes(b"source")
	output_dir = tmp_path / "converted"
	output_dir.mkdir()
	result = subprocess.CompletedProcess(["soffice"], 0, stdout="", stderr="")
	with mock.patch.object(libreoffice, "require_soffice", return_value=pathlib.Path("/usr/bin/soffice")), \
			mock.patch.object(libreoffice.subprocess, "run", return_value=result):
		with pytest.raises(libreoffice.LibreOfficeError, match="deck.pdf"):
			libreoffice.convert_files((input_path,), output_dir, "pdf")


