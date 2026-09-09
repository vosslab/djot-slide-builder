"""Present native presentation builds through one concise Rich interface."""

# Standard Library
import pathlib
import re
import time

# PIP3 Modules
import rich.console
import rich.panel
import rich.progress
import rich.table
import rich.text

# Local Modules
from slide_lib import libreoffice
from slide_lib import djot_errors
from slide_lib import capacity_report
import slide_lib.layout_validation
import slide_lib.native_export


FORMAT_ORDER = ("odp", "pdf")
TEMP_PATH_PATTERN = re.compile(r"output/\.libreoffice\.[^/\s:;]+/converted/")


#============================================
def relative_label(path: pathlib.Path, repo_root: pathlib.Path) -> str:
	"""Return a repository-relative path without exposing an absolute path."""
	resolved = path.expanduser().resolve()
	if resolved.is_relative_to(repo_root):
		label = resolved.relative_to(repo_root).as_posix()
	else:
		label = resolved.name
	return label


#============================================
def input_label(input_value: str, repo_root: pathlib.Path) -> str:
	"""Return the concise source label used in permanent build output."""
	input_path = pathlib.Path(input_value).expanduser().resolve()
	label = relative_label(input_path, repo_root)
	if input_path.is_dir():
		label = f"{label.rstrip('/')}/"
	return label


#============================================
def format_file_size(size_bytes: int) -> str:
	"""Format an artifact size with one compact binary unit."""
	if size_bytes < 1024:
		return f"{size_bytes} B"
	units = ("KB", "MB", "GB", "TB")
	size = float(size_bytes)
	for unit in units:
		size /= 1024
		if size < 1024 or unit == units[-1]:
			return f"{size:.1f} {unit}"
	raise RuntimeError("file-size unit selection failed")


#============================================
def clean_reason(reason: str, repo_root: pathlib.Path) -> str:
	"""Remove repository and conversion-temporary path details from an error reason."""
	cleaned = reason.replace(f"{repo_root}/", "")
	cleaned = TEMP_PATH_PATTERN.sub("output/", cleaned)
	return cleaned


#============================================
def print_failure(error_console: rich.console.Console, repo_root: pathlib.Path,
		deck_path: pathlib.Path, stage: str, reason: str, completed_count: int) -> None:
	"""Write one concise expected-failure panel to stderr."""
	details = rich.table.Table.grid(padding=(0, 1))
	details.add_column(style="bold red", no_wrap=True)
	details.add_column()
	details.add_row("Deck", rich.text.Text(relative_label(deck_path, repo_root)))
	details.add_row("Stage", rich.text.Text(stage))
	details.add_row("Reason", rich.text.Text(clean_reason(reason, repo_root)))
	details.add_row("Completed decks", rich.text.Text(str(completed_count)))
	panel = rich.panel.Panel.fit(details, title="Build failed", border_style="red")
	error_console.print(panel)


#============================================
def print_summary(output_console: rich.console.Console,
		results: list[tuple[pathlib.Path, slide_lib.native_export.ExportResult]], elapsed_seconds: float,
		repo_root: pathlib.Path) -> None:
	"""Write one borderless artifact table and aggregate build result."""
	formats = [name for name in FORMAT_ORDER if name in results[0][1].output_paths()]
	table = rich.table.Table(box=None, pad_edge=False, show_edge=False, header_style="bold")
	table.add_column("Deck", style="cyan")
	for output_format in formats:
		table.add_column(output_format.upper(), justify="right")
	for deck_path, result in results:
		outputs = result.output_paths()
		row = [deck_path.stem]
		row.extend(format_file_size(outputs[name].stat().st_size) for name in formats)
		table.add_row(*(rich.text.Text(value) for value in row))
	output_console.print()
	output_console.print(table)
	output_console.print()
	if len(formats) == 1:
		location = f"output/{formats[0]}/"
	else:
		location = f"output/{{{','.join(formats)}}}/"
	output_console.print(rich.text.Text(f"Output: {location}"))
	deck_word = "deck" if len(results) == 1 else "decks"
	file_count = sum(len(result.artifacts) for _, result in results)
	file_word = "file" if file_count == 1 else "files"
	done = f"Done: {len(results)} {deck_word}, {file_count} {file_word} in {elapsed_seconds:.1f} seconds"
	output_console.print(rich.text.Text(done, style="green"))
	for _deck_path, result in results:
		for diagnostic in result.compilation.capacity_diagnostics:
			message = clean_reason(diagnostic.message(), repo_root)
			output_console.print(rich.text.Text(f"Capacity: {message}", style="yellow"))


#============================================
def run_capacity(input_value: str, allow_folder: bool = True,
		output_console: rich.console.Console | None = None,
		error_console: rich.console.Console | None = None) -> int:
	"""Inspect every selected deck once without creating native artifacts or PDFs."""
	repo_root = slide_lib.native_export.find_repo_root()
	stdout = output_console if output_console is not None else rich.console.Console()
	stderr = error_console if error_console is not None else rich.console.Console(stderr=True)
	try:
		decks = slide_lib.native_export.discover_decks(input_value, repo_root, allow_folder)
	except slide_lib.native_export.PresentationInputError as exc:
		print_failure(stderr, repo_root, pathlib.Path(input_value), "input", str(exc), 0)
		return 1
	diagnostics: list[capacity_report.CapacityDiagnostic] = []
	for deck_path in decks:
		try:
			deck = slide_lib.native_export.parse_deck(deck_path)
			compilation, _theme = slide_lib.native_export.compile_deck(deck)
		except capacity_report.PhysicalCapacityError as exc:
			diagnostics.append(exc.diagnostic)
			continue
		except (slide_lib.native_export.PresentationInputError, djot_errors.DjotParseError,
				slide_lib.layout_validation.LayoutError) as exc:
			print_failure(stderr, repo_root, deck_path, "compiling", str(exc), 0)
			return 1
		diagnostics.extend(compilation.capacity_diagnostics)
	ordered = capacity_report.sorted_diagnostics(diagnostics, repo_root)
	if not ordered:
		return 0
	for diagnostic in ordered:
		stdout.print(rich.text.Text(capacity_report.format_diagnostic(diagnostic, repo_root)), soft_wrap=True)
	stdout.print(rich.text.Text(capacity_report.format_summary(ordered)), soft_wrap=True)
	return 1


#============================================
def run_build(input_value: str, output_format: str, allow_folder: bool = True,
		output_console: rich.console.Console | None = None,
		error_console: rich.console.Console | None = None) -> int:
	"""Build one input through shared progress, summary, and expected-error output."""
	started = time.perf_counter()
	repo_root = slide_lib.native_export.find_repo_root()
	stdout = output_console if output_console is not None else rich.console.Console()
	stderr = error_console if error_console is not None else rich.console.Console(stderr=True)
	try:
		decks = slide_lib.native_export.discover_decks(input_value, repo_root, allow_folder)
	except slide_lib.native_export.PresentationInputError as exc:
		print_failure(stderr, repo_root, pathlib.Path(input_value), "input", str(exc), 0)
		return 1
	deck_word = "deck" if len(decks) == 1 else "decks"
	source = input_label(input_value, repo_root)
	stdout.print(rich.text.Text(f"Building {len(decks)} {deck_word} from {source}"))
	progress = rich.progress.Progress(
		rich.progress.SpinnerColumn(style="cyan"),
		rich.progress.TextColumn("{task.description}"),
		console=stdout,
		transient=True,
		disable=not stdout.is_terminal,
	)
	task_id = progress.add_task(f"{decks[0].stem}  PARSING", total=None)
	results: list[tuple[pathlib.Path, slide_lib.native_export.ExportResult]] = []
	failure: tuple[pathlib.Path, str, BaseException] | None = None
	current_stage = ["parsing"]
	with progress:
		for deck_path in decks:
			current_stage[0] = "parsing"
			def update_progress(stage: str) -> None:
				"""Update the one transient current-deck stage line."""
				current_stage[0] = stage
				description = f"{deck_path.stem}  {stage.upper()}"
				progress.update(task_id, description=description, refresh=True)
			try:
				deck_format = "odp" if output_format in ("all", "pdf") else output_format
				outputs = slide_lib.native_export.export_deck(str(deck_path), deck_format, update_progress)
			except (slide_lib.native_export.PresentationInputError, djot_errors.DjotParseError,
				slide_lib.layout_validation.LayoutError, libreoffice.LibreOfficeError,
				capacity_report.PhysicalCapacityError) as exc:
				failure = (deck_path, current_stage[0], exc)
				break
			results.append((deck_path, outputs))
		if failure is None and output_format in ("all", "pdf"):
			current_stage[0] = "pdf"
			progress.update(task_id, description="PDF", refresh=True)
			pdf_paths = tuple(repo_root / f"output/pdf/{deck_path.stem}.pdf" for deck_path, _result in results)
			try:
				slide_lib.native_export.convert_odps_to_pdfs(
					tuple(result.output_paths()["odp"] for _deck_path, result in results), pdf_paths, repo_root)
			except libreoffice.LibreOfficeError as exc:
				failure = (decks[-1], current_stage[0], exc)
			else:
				results = [(deck_path, slide_lib.native_export.ExportResult(
					result.compilation, (*result.artifacts, ("pdf", pdf_path))))
					for (deck_path, result), pdf_path in zip(results, pdf_paths, strict=True)]
	if failure is not None:
		deck_path, stage, exc = failure
		print_failure(stderr, repo_root, deck_path, stage, str(exc), len(results))
		return 1
	elapsed_seconds = time.perf_counter() - started
	print_summary(stdout, results, elapsed_seconds, repo_root)
	return 0
