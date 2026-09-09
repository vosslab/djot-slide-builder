"""Run simple, sequential LibreOffice presentation conversions."""

# Standard Library
import collections.abc
import pathlib
import shutil
import subprocess
import time


SOFFICE_CANDIDATES = (
	pathlib.Path("/Applications/LibreOffice.app/Contents/MacOS/soffice"),
	pathlib.Path("/Applications/LibreOffice-Still.app/Contents/MacOS/soffice"),
)
SOFFICE_PROCESS_MARKER = ".app/Contents/MacOS/soffice"
IMPRESS_PDF_EXPORT = (
	'pdf:impress_pdf_Export:{'
	'"Quality":{"type":"long","value":"70"},'
	'"ReduceImageResolution":{"type":"boolean","value":"true"},'
	'"MaxImageResolution":{"type":"long","value":"100"},'
	'"SelectPdfVersion":{"type":"long","value":"3"}'
	'}'
)
SETTLING_SECONDS = 2


class LibreOfficeError(RuntimeError):
	"""Report an expected LibreOffice preflight or conversion failure."""


#============================================
def format_diagnostics(stdout: str | bytes | None, stderr: str | bytes | None) -> str:
	"""Return concise nonempty LibreOffice diagnostics from captured streams."""
	lines: list[str] = []
	for stream in (stderr, stdout):
		if isinstance(stream, bytes):
			stream = stream.decode("utf-8", errors="replace")
		if stream:
			lines.extend(line.strip() for line in stream.splitlines() if line.strip())
	return "; ".join(dict.fromkeys(lines))


#============================================
def require_soffice() -> pathlib.Path:
	"""Resolve the LibreOffice command used for local conversion."""
	command_value = shutil.which("soffice")
	if command_value is not None:
		return pathlib.Path(command_value).resolve()
	for candidate in SOFFICE_CANDIDATES:
		if candidate.is_file():
			return candidate
	raise LibreOfficeError("LibreOffice is not installed; run brew bundle")


#============================================
def require_libreoffice_closed() -> None:
	"""Require the desktop LibreOffice process to be closed before conversion."""
	result = subprocess.run(
		["ps", "-axo", "command="],
		check=True,
		capture_output=True,
		text=True,
	)
	for command in result.stdout.splitlines():
		if SOFFICE_PROCESS_MARKER in command:
			raise LibreOfficeError("LibreOffice is running; close it before building presentations")


#============================================
def convert_files(input_paths: collections.abc.Sequence[pathlib.Path], output_dir: pathlib.Path,
		output_format: str) -> tuple[pathlib.Path, ...]:
	"""Convert ordered presentations one at a time after one desktop preflight."""
	inputs = tuple(input_paths)
	if not inputs:
		raise ValueError("LibreOffice conversion needs at least one input file")
	expected_paths = tuple(output_dir / f"{input_path.stem}.{output_format}" for input_path in inputs)
	if len(set(expected_paths)) != len(expected_paths):
		raise ValueError("LibreOffice conversion inputs must have distinct output filenames")
	require_libreoffice_closed()
	soffice_path = require_soffice()
	conversion_target = IMPRESS_PDF_EXPORT if output_format == "pdf" else output_format
	for input_path, expected_path in zip(inputs, expected_paths, strict=True):
		command = [
			str(soffice_path),
			"--headless",
			"--norestore",
			"--convert-to",
			conversion_target,
			"--outdir",
			str(output_dir),
			str(input_path),
		]
		result = subprocess.run(command, capture_output=True, text=True)
		if result.returncode != 0:
			diagnostics = format_diagnostics(result.stdout, result.stderr)
			reason = f"LibreOffice {output_format.upper()} conversion failed for {input_path}"
			if diagnostics:
				reason += f": {diagnostics}"
			else:
				reason += f" with exit status {result.returncode}"
			raise LibreOfficeError(reason)
		if not expected_path.is_file():
			diagnostics = format_diagnostics(result.stdout, result.stderr)
			reason = f"LibreOffice did not create expected {output_format.upper()} output: {expected_path}"
			if diagnostics:
				reason += f": {diagnostics}"
			raise LibreOfficeError(reason)
		time.sleep(SETTLING_SECONDS)
	return expected_paths


#============================================
def convert_file(input_path: pathlib.Path, output_dir: pathlib.Path, output_format: str) -> pathlib.Path:
	"""Convert one presentation through the shared sequential conversion boundary."""
	return convert_files((input_path,), output_dir, output_format)[0]
