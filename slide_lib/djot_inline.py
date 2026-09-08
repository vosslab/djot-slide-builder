"""Small, source-located parser for the supported Djot inline subset."""

# Standard Library
import pathlib
import string

# Local Modules
import slide_lib.djot_errors
import slide_lib.djot_grammar
import slide_lib.native_model


# Djot lets a backslash quote ASCII punctuation.  Keep this grammar fact local
# to scanning: the resulting character is ordinary text, never a delimiter.
ESCAPABLE_PUNCTUATION = frozenset(string.punctuation)


#============================================
def parse_inlines(path: pathlib.Path, line: int, source: str) -> tuple[slide_lib.native_model.Inline, ...]:
	"""Parse one logical Djot text span into presentation-neutral inline runs."""
	return _parse_runs(path, line, source, 0, len(source))


#============================================
def _parse_runs(path: pathlib.Path, line: int, source: str, start: int,
		end: int) -> tuple[slide_lib.native_model.Inline, ...]:
	"""Parse a bounded span, retaining its original offsets for diagnostics."""
	runs: list[slide_lib.native_model.Inline] = []
	text_start = start
	index = start
	while index < end:
		character = source[index]
		if character == "\\" and index + 1 < end and source[index + 1] == "\n":
			_append_text(runs, source[text_start:index])
			runs.append(slide_lib.native_model.Break())
			index += 2
			text_start = index
			continue
		if character == "\\" and index + 1 < end and source[index + 1] in ESCAPABLE_PUNCTUATION:
			# Consume the quote before checking inline delimiters.  Appending through
			# _append_text deliberately retains normal-text projections for this text.
			_append_text(runs, source[text_start:index])
			_append_text(runs, source[index + 1])
			index += 2
			text_start = index
			continue
		if character == "\n":
			_append_text(runs, source[text_start:index] + " ")
			index += 1
			text_start = index
			continue
		if source.startswith("![", index):
			raise _error(path, line, source, index,
				"images must be standalone component-image blocks")
		if character in ("_", "*") and _opens_delimiter(source, index, end):
			if character == "_" and index + 1 < end and source[index + 1] == "_":
				# Consecutive underscores are visible fill-in-the-blank prose in the
				# imported lectures, not an emphasis delimiter run.
				index += 1
				continue
			close = _find_delimiter(source, character, index + 1, end)
			if close is None:
				# Preserve unmatched delimiter characters as ordinary lecture prose.
				index += 1
				continue
			_append_text(runs, source[text_start:index])
			children = _parse_runs(path, line, source, index + 1, close)
			if not children:
				raise _error(path, line, source, index, "empty inline content is not supported")
			if character == "_":
				runs.append(slide_lib.native_model.Emphasis(children))
			else:
				runs.append(slide_lib.native_model.Strong(children))
			index = close + 1
			text_start = index
			continue
		if character == "`":
			close = _find_unescaped_character(source, "`", index + 1, end)
			if close is None:
				raise _error(path, line, source, index, "unterminated verbatim inline content")
			_append_text(runs, source[text_start:index])
			value = source[index + 1:close]
			if not value:
				raise _error(path, line, source, index, "empty verbatim inline content is not supported")
			runs.append(slide_lib.native_model.InlineCode(value))
			index = close + 1
			text_start = index
			continue
		if character == "[":
			label_end = _find_closing_bracket(source, index, end)
			if label_end is None or label_end + 1 >= end or source[label_end + 1] != "(":
				raise _error(path, line, source, index, "unsupported or unterminated link syntax")
			url_end = _find_closing_parenthesis(source, label_end + 1, end)
			if url_end is None:
				raise _error(path, line, source, label_end + 1, "unterminated link destination")
			url = source[label_end + 2:url_end]
			if not url or any(character.isspace() for character in url):
				raise _error(path, line, source, label_end + 2, "link destinations must be non-empty and unbroken")
			_append_text(runs, source[text_start:index])
			children = _parse_runs(path, line, source, index + 1, label_end)
			if not children:
				raise _error(path, line, source, index, "links require visible label text")
			runs.append(slide_lib.native_model.Link(children, url))
			index = url_end + 1
			text_start = index
			continue
		if character == "$":
			if index + 1 < end and source[index + 1] == "$":
				raise _error(path, line, source, index,
					"display mathematics must be a block, not inline content")
			close = _find_unescaped_character(source, "$", index + 1, end)
			if close is None:
				# A lone dollar is ordinary visible text, notably for currency in
				# imported lecture prose.  Only a paired delimiter enters the local
				# inline-mathematics extension.
				index += 1
				continue
			_append_text(runs, source[text_start:index])
			value = source[index + 1:close]
			if not value:
				raise _error(path, line, source, index, "empty inline mathematics is not supported")
			runs.append(slide_lib.native_model.InlineMath(value))
			index = close + 1
			text_start = index
			continue
		if character == "~":
			if _find_unescaped_character(source, "~", index + 1, end) is None:
				# A bare tilde is ordinary approximation prose such as ``~640``.
				# Only an actual paired form reaches the unsupported-subset boundary.
				index += 1
				continue
			raise _error(path, line, source, index, "unsupported Djot inline syntax")
		if character in ("^", "{"):
			raise _error(path, line, source, index, "unsupported Djot inline syntax")
		if character == ":" and _is_symbol(source, index, end):
			raise _error(path, line, source, index, "Djot symbols are not supported")
		index += 1
	_append_text(runs, source[text_start:end])
	return tuple(runs)


#============================================
def _append_text(runs: list[slide_lib.native_model.Inline], value: str) -> None:
	"""Append ordinary projected text, coalescing only adjacent text runs."""
	if not value:
		return
	if runs and isinstance(runs[-1], slide_lib.native_model.Text):
		previous = runs.pop()
		# Re-project the coalesced run so a quoted character cannot split a
		# normal-text projection such as ``&prime;`` across append calls.
		projected = slide_lib.djot_grammar.project_text(previous.value + value)
		runs.append(slide_lib.native_model.Text(projected))
	else:
		projected = slide_lib.djot_grammar.project_text(value)
		runs.append(slide_lib.native_model.Text(projected))


#============================================
def _opens_delimiter(source: str, index: int, end: int) -> bool:
	"""Recognize a nonblank Djot delimiter, including intraword paired forms."""
	if index + 1 >= end or source[index + 1].isspace():
		return False
	return True


#============================================
def _find_delimiter(source: str, delimiter: str, start: int, end: int) -> int | None:
	"""Find a closing delimiter that can terminate one simple inline span."""
	index = start
	while index < end:
		if source[index] == "\\" and index + 1 < end and source[index + 1] in ESCAPABLE_PUNCTUATION:
			index += 2
			continue
		if source[index] == delimiter and index > start and not source[index - 1].isspace():
			return index
		index += 1
	return None


#============================================
def _find_unescaped_character(source: str, character: str, start: int, end: int) -> int | None:
	"""Find an inline boundary while preserving quoted punctuation as text."""
	index = start
	while index < end:
		if source[index] == "\\" and index + 1 < end and source[index + 1] in ESCAPABLE_PUNCTUATION:
			index += 2
			continue
		if source[index] == character:
			return index
		index += 1
	return None


#============================================
def _find_closing_bracket(source: str, start: int, end: int) -> int | None:
	"""Find the closing bracket for a link label, permitting nested brackets."""
	depth = 1
	index = start + 1
	while index < end:
		if source[index] == "\\" and index + 1 < end and source[index + 1] in ESCAPABLE_PUNCTUATION:
			index += 2
			continue
		if source[index] == "[":
			depth += 1
		elif source[index] == "]":
			depth -= 1
			if depth == 0:
				return index
		index += 1
	return None


#============================================
def _find_closing_parenthesis(source: str, start: int, end: int) -> int | None:
	"""Find the closing parenthesis for a link destination, permitting nesting."""
	depth = 1
	index = start + 1
	while index < end:
		if source[index] == "\\" and index + 1 < end and source[index + 1] in ESCAPABLE_PUNCTUATION:
			index += 2
			continue
		if source[index] == "(":
			depth += 1
		elif source[index] == ")":
			depth -= 1
			if depth == 0:
				return index
		index += 1
	return None


#============================================
def _is_symbol(source: str, start: int, end: int) -> bool:
	"""Recognize Djot's named-symbol form without reserving ordinary colons."""
	index = start + 1
	if index >= end or not source[index].isalpha():
		return False
	while index < end and (source[index].isalnum() or source[index] in ("-", "_")):
		index += 1
	return index < end and source[index] == ":"


#============================================
def _error(path: pathlib.Path, line: int, source: str, index: int,
		message: str) -> slide_lib.djot_errors.DjotParseError:
	"""Create one diagnostic at the physical line containing an inline token."""
	location = slide_lib.native_model.SourceLocation(path, line + source[:index].count("\n"))
	return slide_lib.djot_errors.source_error(location, message)
