"""Load ordered chapter manifests without flattening physical source locations."""

# Standard Library
import re
import pathlib
import dataclasses
import subprocess

# Local Modules
import slide_lib.djot_errors
import slide_lib.djot_grammar
import slide_lib.native_model
import slide_lib.presentation_theme


@dataclasses.dataclass(frozen=True)
class SourceFile:
	"""One physical file containing complete slides."""
	path: pathlib.Path
	text: str
	hidden: bool = False


@dataclasses.dataclass(frozen=True)
class SourceBundle:
	"""Ordered slide sources, all visited files, and their common course theme."""
	files: tuple[SourceFile, ...]
	paths: tuple[pathlib.Path, ...]
	color_theme: str


#============================================
def fail(path: pathlib.Path, line: int, message: str) -> None:
	"""Report a file-loading failure at the physical directive."""
	location = slide_lib.native_model.SourceLocation(path, line)
	raise slide_lib.djot_errors.source_error(location, message)


#============================================
def read_source(path: pathlib.Path) -> str:
	"""Read UTF-8 source with an actionable diagnostic for unreadable input."""
	try:
		data = path.read_bytes()
	except OSError as error:
		fail(path, 1, f"cannot read UTF-8 Djot source: {error}")
	try:
		text = data.decode("utf-8")
	except UnicodeDecodeError as error:
		report_encoding_error(path, error)
	text = text.replace("\r\n", "\n").replace("\r", "\n")
	return text


#============================================
def report_encoding_error(path: pathlib.Path, error: UnicodeDecodeError) -> None:
	"""Locate invalid bytes using editor line and character-column coordinates."""
	prefix = error.object[:error.start].decode("utf-8")
	prefix = prefix.replace("\r\n", "\n").replace("\r", "\n")
	line = prefix.count("\n") + 1
	before = prefix.rsplit("\n", 1)[-1]
	column = len(before) + 1
	suffix = error.object[error.end:].decode("utf-8", errors="backslashreplace")
	after = suffix.replace("\r\n", "\n").replace("\r", "\n").split("\n", 1)[0]
	invalid = " ".join(f"0x{byte:02X}" for byte in error.object[error.start:error.end])
	excerpt = before[-45:] + f"[INVALID {invalid}]" + after[:45]
	fail(path, line, f"invalid UTF-8 at line {line}, column {column}; "
		f"near {excerpt!r}. Replace the marked text and save the file as UTF-8.")


#============================================
def source_header(path: pathlib.Path, text: str) -> tuple[str | None, list[tuple[int, str]]]:
	"""Read optional leading course metadata, leaving all physical line numbers intact."""
	lines = [(number, value) for number, value in enumerate(text.splitlines(), 1)
		if value.strip()]
	theme = None
	if lines and lines[0][1].strip().startswith("color-theme:"):
		number, value = lines.pop(0)
		match = slide_lib.djot_grammar.COLOR_THEME_DIRECTIVE_PATTERN.fullmatch(value)
		if match is None:
			fail(path, number, "color-theme metadata must be exactly color-theme: <course>")
		theme = match.group("theme")
		if theme not in slide_lib.presentation_theme.color_theme_names():
			fail(path, number, f"unknown color-theme: {theme}")
	return theme, lines


#============================================
def repository_root(path: pathlib.Path) -> pathlib.Path:
	"""Resolve a shared include against its containing Git checkout."""
	result = subprocess.run(["git", "-C", str(path.parent), "rev-parse", "--show-toplevel"],
		check=True, capture_output=True, text=True)
	root = pathlib.Path(result.stdout.strip()).resolve()
	return root


#============================================
def include_target(path: pathlib.Path, line: int, value: str,
		root: pathlib.Path) -> pathlib.Path:
	"""Resolve a local chapter or explicit repository include within its allowed tree."""
	if not value.startswith("include: ") or value != value.strip():
		fail(path, line, "manifest lines must be exactly include: <relative.djot>")
	name = value.removeprefix("include: ")
	shared = name.startswith("repo:")
	if shared:
		name = name.removeprefix("repo:")
	candidate = pathlib.PurePosixPath(name)
	# ASVS 2.2.1, 5.3.2: only local Djot paths; resolve symlinks before containment checks.
	if (not name or name != name.strip() or candidate.is_absolute() or
			".." in candidate.parts or "\\" in name or candidate.suffix != ".djot"):
		fail(path, line, "include needs a relative .djot path without traversal")
	allowed_root = repository_root(path) if shared else root
	base = allowed_root if shared else path.parent
	target = (base / name).resolve()
	if not target.is_relative_to(allowed_root):
		boundary = "repository" if shared else "master deck directory"
		fail(path, line, f"included source must stay inside the {boundary}")
	if not target.is_file():
		fail(path, line, f"included source is missing: {name}")
	return target


#============================================
def load_sources(input_path: pathlib.Path) -> SourceBundle:
	"""Expand include-only manifests; ordinary decks retain their existing grammar."""
	path = input_path.resolve()
	files: list[SourceFile] = []
	paths: list[pathlib.Path] = []
	color_theme = walk_sources(path, path.parent, None, (), files, paths)
	result = SourceBundle(tuple(files), tuple(paths), color_theme)
	return result


#============================================
def source_parts(text: str) -> list[tuple[int, str, bool]]:
	"""Separate explicit include blocks from slides, preserving physical line offsets."""
	lines = text.splitlines(keepends=True)
	boundaries = [0]
	fence = None
	for index, value in enumerate(lines):
		line = value.rstrip("\r\n")
		if fence is not None:
			if re.fullmatch(rf"{re.escape(fence[0])}{{{len(fence)},}}[ \t]*", line):
				fence = None
			continue
		match = re.fullmatch(r"(`{3,}|~{3,}).*", line)
		if match:
			fence = match.group(1)
		elif line.startswith(("=== include:", "=== layout:")) and index:
			boundaries.append(index)
	boundaries.append(len(lines))
	return [(start + 1, "".join(lines[start:end]),
		lines[start].startswith("=== include:"))
		for start, end in zip(boundaries, boundaries[1:]) if start < end]


#============================================
def walk_sources(path: pathlib.Path, root: pathlib.Path, inherited_theme: str | None,
		ancestors: tuple[pathlib.Path, ...], files: list[SourceFile],
		paths: list[pathlib.Path], hidden: bool = False) -> str:
	"""Visit chapter files in authored order, rejecting recursion and theme conflicts."""
	text = read_source(path)
	declared_theme, lines = source_header(path, text)
	if inherited_theme is not None and declared_theme not in (None, inherited_theme):
		metadata_line = next(number for number, value in enumerate(text.splitlines(), 1)
			if value.strip())
		fail(path, metadata_line,
			f"chapter color-theme conflicts with master theme: {inherited_theme}")
	theme = declared_theme or inherited_theme or slide_lib.presentation_theme.DEFAULT_COLOR_THEME
	paths.append(path)
	manifest = bool(lines and lines[0][1].strip().startswith("include:"))
	parts = [(number, value, True) for number, value in lines] if manifest else source_parts(text)
	if not manifest and not any(is_include for _number, _part, is_include in parts):
		files.append(SourceFile(path, text, hidden))
		return theme
	for number, part, is_include in parts:
		if not is_include:
			if "=== layout:" in part:
				files.append(SourceFile(path, "\n" * (number - 1) + part, hidden))
			elif part.strip() and not part.strip().startswith("color-theme:"):
				fail(path, number, "expected a layout or include directive")
			continue
		block = part.splitlines()
		value = block[0].removeprefix("=== ")
		include_hidden = hidden
		for offset, metadata in enumerate(block[1:], 1):
			if not metadata.strip():
				continue
			if metadata not in ("hidden: true", "hidden: false"):
				fail(path, number + offset, "include blocks accept only hidden: true or hidden: false")
			include_hidden = hidden or metadata == "hidden: true"
		target = include_target(path, number, value, root)
		if target in (*ancestors, path):
			fail(path, number, f"circular include: {target.name}")
		if len(ancestors) >= 31:
			fail(path, number, "includes exceed 32 nested manifests; flatten the chapter list")
		target_root = repository_root(path) if value.startswith("include: repo:") else root
		walk_sources(target, target_root, theme, (*ancestors, path), files, paths, include_hidden)
	return theme


#============================================
def root_sources(candidates: list[pathlib.Path]) -> list[pathlib.Path]:
	"""Select master decks once when recursively building or linting a folder."""
	included: set[pathlib.Path] = set()
	manifests: list[pathlib.Path] = []
	for path in candidates:
		lines = [(number, value) for number, value in enumerate(read_source(path).splitlines(), 1)
			if value.strip()]
		if lines and lines[0][1].strip().startswith("color-theme:"):
			lines.pop(0)
		if lines and lines[0][1].strip().startswith("include:"):
			directives = lines
		else:
			directives = [(number, part.splitlines()[0].removeprefix("=== "))
				for number, part, is_include in source_parts(read_source(path)) if is_include]
		if directives:
			manifests.append(path)
			included.update(include_target(path, number, value, path.parent.resolve())
				for number, value in directives)
	result = [path for path in candidates if path.resolve() not in included]
	visited: set[pathlib.Path] = set()
	for path in result:
		if path in manifests:
			visited.update(load_sources(path).paths)
	# A disconnected cycle has no root, so it must not silently disappear from discovery.
	for path in manifests:
		if path.resolve() not in visited:
			visited.update(load_sources(path).paths)
	return result


#============================================
def image_path(deck: slide_lib.native_model.Deck,
		image: slide_lib.native_model.Image) -> pathlib.Path:
	"""Resolve explicit repository assets or ordinary master-relative component images."""
	shared = image.source.startswith("repo:")
	name = image.source.removeprefix("repo:") if shared else image.source
	candidate = pathlib.PurePosixPath(name)
	if candidate.is_absolute() or ".." in candidate.parts or "\\" in name:
		raise ValueError("image path must be a local relative path without traversal")
	base = deck.repo_root if shared else deck.asset_root
	path = (base / name).resolve()
	return path
