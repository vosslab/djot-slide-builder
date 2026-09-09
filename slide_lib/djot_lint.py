"""Source-only semantic linting for repository-supported Djot slide decks."""

# Standard Library
import dataclasses
import pathlib
import shutil
import subprocess
import sys

# Local Modules
import slide_lib.djot_parser
import slide_lib.layout_engine
import slide_lib.layout_validation
import slide_lib.native_model


@dataclasses.dataclass(frozen=True)
class LintProblem:
	"""One deterministic source-located lint failure."""

	path: pathlib.Path
	line: int
	message: str


@dataclasses.dataclass(frozen=True)
class LintSummary:
	"""Aggregate source counts after a clean semantic lint."""

	sources: int
	slides: int
	images: int


#============================================
def image_problem(path: pathlib.Path, deck: slide_lib.native_model.Deck,
		image: slide_lib.native_model.Image) -> LintProblem | None:
	"""Return one safe-local-image failure for a parsed component image."""
	candidate = pathlib.PurePosixPath(image.source)
	if candidate.is_absolute() or ".." in candidate.parts:
		return LintProblem(path, image.location.line,
			"image path must be a local relative path without traversal")
	image_path = (deck.asset_root / image.source).resolve()
	if not image_path.is_relative_to(deck.repo_root):
		return LintProblem(path, image.location.line,
			f"component image must be inside the repository: {image.source}")
	if not image_path.is_file():
		return LintProblem(path, image.location.line,
			f"component image is missing: {image.source}")
	return None


#============================================
def images_in_blocks(blocks: tuple[slide_lib.native_model.Block, ...]) -> tuple[slide_lib.native_model.Image, ...]:
	"""Return component images from nested supported source blocks in reading order."""
	images: list[slide_lib.native_model.Image] = []
	for block in blocks:
		if isinstance(block, slide_lib.native_model.Image):
			images.append(block)
		elif isinstance(block, slide_lib.native_model.ListBlock):
			images.extend(images_in_items(block.items))
		elif isinstance(block, slide_lib.native_model.QuoteBlock):
			images.extend(images_in_blocks(block.blocks))
	result = tuple(images)
	return result


#============================================
def images_in_items(items: tuple[slide_lib.native_model.ListItem, ...]) -> tuple[slide_lib.native_model.Image, ...]:
	"""Return images from recursively nested list items in source order."""
	images: list[slide_lib.native_model.Image] = []
	for item in items:
		for child in item.children:
			images.extend(images_in_blocks((child,)))
	result = tuple(images)
	return result


#============================================
def source_problem(path: pathlib.Path, error: ValueError) -> LintProblem:
	"""Project parser and layout errors into the linter's stable report shape."""
	prefix = f"{path.resolve()}:"
	text = str(error)
	if text.startswith(prefix):
		line_text, separator, message = text[len(prefix):].partition(": ")
		if separator and line_text.isdigit():
			return LintProblem(path, int(line_text), message)
	return LintProblem(path, 1, text)


#============================================
def lint_source(path: pathlib.Path) -> tuple[list[LintProblem], int, int]:
	"""Lint one source file through the parser and layout semantic authorities."""
	try:
		deck = slide_lib.djot_parser.parse_deck(path)
		for slide in deck.slides:
			contract = slide_lib.layout_engine.layout_contract(slide.layout_class)
			slide_lib.layout_validation.validate_layout_source(slide, contract)
	except ValueError as error:
		return [source_problem(path, error)], 0, 0
	images: list[slide_lib.native_model.Image] = []
	for slide in deck.slides:
		images.extend(images_in_blocks(slide.blocks))
		for cell in slide.cells:
			images.extend(images_in_blocks(cell.blocks))
	problems = [problem for image in images if (problem := image_problem(path, deck, image)) is not None]
	return problems, len(deck.slides), len(images)


#============================================
def djot_sources(paths: list[pathlib.Path]) -> list[pathlib.Path]:
	"""Resolve explicit source files and recursively supplied source folders."""
	sources: list[pathlib.Path] = []
	for path in paths:
		if path.is_file():
			if path.suffix != ".djot":
				raise ValueError(f"source must use the .djot suffix: {path}")
			sources.append(path)
			continue
		if path.is_dir():
			sources.extend(child for child in path.rglob("*.djot") if not child.is_symlink())
			continue
		raise ValueError(f"source path does not exist: {path}")
	result = sorted(set(sources))
	return result


#============================================
def native_validator(source: pathlib.Path, executable: str,
		arguments: list[str]) -> LintProblem | None:
	"""Run a user-pinned native Djot tool without invoking a shell."""
	resolved_executable = shutil.which(executable)
	if resolved_executable is None:
		return LintProblem(source, 1, f"native Djot executable was not found: {executable}")
	try:
		result = subprocess.run([resolved_executable, *arguments, str(source)], check=False,
			capture_output=True, text=True, timeout=30)
	except subprocess.TimeoutExpired:
		return LintProblem(source, 1, "native Djot validator timed out after 30 seconds")
	if result.returncode == 0:
		return None
	detail = (result.stderr or result.stdout).strip().replace("\n", " ")[:400]
	message = f"native Djot validator failed: {detail or result.returncode}"
	return LintProblem(source, 1, message)


#============================================
def lint_paths(paths: list[pathlib.Path], *, native_executable: str | None = None,
		native_arguments: list[str] | None = None) -> tuple[list[LintProblem], LintSummary]:
	"""Run optional native validation and then semantic source-only linting."""
	problems: list[LintProblem] = []
	slide_count = 0
	image_count = 0
	sources = djot_sources(paths)
	for source in sources:
		if native_executable is not None:
			native_problem = native_validator(source, native_executable, native_arguments or [])
			if native_problem is not None:
				problems.append(native_problem)
		source_problems, source_slides, source_images = lint_source(source)
		problems.extend(source_problems)
		slide_count += source_slides
		image_count += source_images
	summary = LintSummary(len(sources), slide_count, image_count)
	return problems, summary


#============================================
def run_lint(sources: list[pathlib.Path], native_executable: str | None,
		native_arguments: list[str], require_native: bool) -> int:
	"""Print source findings and return the lint command status."""
	if require_native and native_executable is None:
		print("error: --require-native needs --native-executable", file=sys.stderr)
		return 2
	try:
		problems, summary = lint_paths(sources, native_executable=native_executable,
			native_arguments=native_arguments)
	except ValueError as error:
		print(f"error: {error}", file=sys.stderr)
		return 2
	for problem in problems:
		print(f"{problem.path}:{problem.line}: {problem.message}")
	if problems:
		return 1
	print(f"Djot slide structure: {summary.sources} source(s), {summary.slides} slide(s), {summary.images} image(s)")
	if native_executable is None:
		print("Native Djot validation was not run; it remains required before source acceptance.")
	return 0
