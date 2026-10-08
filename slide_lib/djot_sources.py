"""Load ordered chapter manifests without flattening physical source locations."""

# Standard Library
import dataclasses
import pathlib

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
		text = path.read_text(encoding="utf-8")
	except (OSError, UnicodeDecodeError) as error:
		fail(path, 1, f"cannot read UTF-8 Djot source: {error}")
	return text


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
def include_target(path: pathlib.Path, line: int, value: str,
		root: pathlib.Path) -> pathlib.Path:
	"""Resolve an exact include inside the master file's directory tree."""
	if not value.startswith("include: ") or value != value.strip():
		fail(path, line, "manifest lines must be exactly include: <relative.djot>")
	name = value.removeprefix("include: ")
	candidate = pathlib.PurePosixPath(name)
	# ASVS 2.2.1, 5.3.2: only local Djot paths; resolve symlinks before containment checks.
	if (not name or name != name.strip() or candidate.is_absolute() or
			".." in candidate.parts or "\\" in name or candidate.suffix != ".djot"):
		fail(path, line, "include needs a relative .djot path without traversal")
	target = (path.parent / name).resolve()
	if not target.is_relative_to(root):
		fail(path, line, "included source must stay inside the master deck directory")
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
def walk_sources(path: pathlib.Path, root: pathlib.Path, inherited_theme: str | None,
		ancestors: tuple[pathlib.Path, ...], files: list[SourceFile],
		paths: list[pathlib.Path]) -> str:
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
	if not lines or not lines[0][1].strip().startswith("include:"):
		files.append(SourceFile(path, text))
		return theme
	for number, value in lines:
		target = include_target(path, number, value, root)
		if target in (*ancestors, path):
			fail(path, number, f"circular include: {target.name}")
		if len(ancestors) >= 31:
			fail(path, number, "includes exceed 32 nested manifests; flatten the chapter list")
		walk_sources(target, root, theme, (*ancestors, path), files, paths)
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
		if not lines or not lines[0][1].strip().startswith("include:"):
			continue
		manifests.append(path)
		included.update(include_target(path, number, value, path.parent.resolve())
			for number, value in lines)
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
