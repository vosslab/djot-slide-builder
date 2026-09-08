"""Block parser for the presentation-supported Djot subset."""

# Standard Library
import dataclasses
import pathlib
import re
from collections.abc import Callable

# Local Modules
import slide_lib.djot_errors
import slide_lib.djot_inline
import slide_lib.native_model


_ATTRIBUTE_LINE = re.compile(r"^\{(?P<body>[^{}]*)\}$")
_FENCE = re.compile(r"^(?P<mark>`{3,}|~{3,})(?P<info>.*)$")
_HEADING = re.compile(r"^(?P<marks>#{1,6})[ \t]+(?P<text>.+?)\s*$")
_LIST_ITEM = re.compile(r"^(?P<indent> *)"
	r"(?:(?P<bullet>[-+*])|(?P<number>[0-9]+)(?P<delimiter>[.)]))[ \t]+(?P<text>.*)$")
_QUOTE = re.compile(r"^>[ ]?(?P<text>.*)$")
_IMAGE = re.compile(r'^!\[(?P<alt>[^\]]+)\]\((?P<source>[^\s)]+)(?:\s+"(?P<title>[^"]*)")?\)$')
_KNOWN_UNSUPPORTED = (
	(":::", "generic divs are not supported"),
	("[^", "footnotes are not supported"),
	("{=", "raw blocks are not supported"),
)


@dataclasses.dataclass(frozen=True)
class _BlockSpan:
	"""One parsed block and its half-open physical source-line span."""
	block: slide_lib.native_model.Block
	first_line: int
	after_line: int


@dataclasses.dataclass(frozen=True)
class ParsedBlocks:
	"""Blocks plus source spans for the deck assembler's neighboring actions."""
	spans: tuple[_BlockSpan, ...]

	@property
	def blocks(self) -> tuple[slide_lib.native_model.Block, ...]:
		"""Return parsed blocks in source reading order."""
		blocks = tuple(span.block for span in self.spans)
		return blocks

	def block_before(self, line: int) -> slide_lib.native_model.Block | None:
		"""Return the closest complete block before one physical source line."""
		for span in reversed(self.spans):
			if span.after_line <= line:
				return span.block
		return None

	def block_after(self, line: int) -> slide_lib.native_model.Block | None:
		"""Return the first block beginning at or after one physical source line."""
		for span in self.spans:
			if span.first_line >= line:
				return span.block
		return None


#============================================
def location(path: pathlib.Path, line: int) -> slide_lib.native_model.SourceLocation:
	"""Create a physical Djot source location."""
	result = slide_lib.native_model.SourceLocation(path, line)
	return result


#============================================
def fail(path: pathlib.Path, line: int, message: str) -> None:
	"""Raise one source-located Djot parsing failure."""
	raise slide_lib.djot_errors.source_error(location(path, line), message)


#============================================
def parse_attribute_tokens(path: pathlib.Path, line: int, body: str) -> tuple[slide_lib.native_model.Attribute, ...]:
	"""Parse the compact one-line Djot attribute form without a new dependency."""
	attributes: list[slide_lib.native_model.Attribute] = []
	index = 0
	while index < len(body):
		while index < len(body) and body[index].isspace():
			index += 1
		if index == len(body):
			break
		start = index
		while index < len(body) and not body[index].isspace() and body[index] != "=":
			index += 1
		name = body[start:index]
		if not name:
			fail(path, line, "malformed Djot attribute")
		if name.startswith("#"):
			if len(name) == 1:
				fail(path, line, "Djot id attributes require a value")
			attributes.append(slide_lib.native_model.Attribute("id", name[1:]))
			continue
		if name.startswith("."):
			if len(name) == 1:
				fail(path, line, "Djot class attributes require a value")
			attributes.append(slide_lib.native_model.Attribute("class", name[1:]))
			continue
		if index == len(body) or body[index].isspace():
			attributes.append(slide_lib.native_model.Attribute(name, None))
			continue
		index += 1
		if index == len(body):
			fail(path, line, "Djot attribute values require a value")
		if body[index] in "\"'":
			quote = body[index]
			index += 1
			value_start = index
			while index < len(body) and body[index] != quote:
				index += 1
			if index == len(body):
				fail(path, line, "Djot attribute quotes must close on the same line")
			value = body[value_start:index]
			index += 1
		else:
			value_start = index
			while index < len(body) and not body[index].isspace():
				index += 1
			value = body[value_start:index]
		attributes.append(slide_lib.native_model.Attribute(name, value))
	result = tuple(attributes)
	return result


#============================================
def parse_attributes(path: pathlib.Path, line: int, source: str) -> tuple[slide_lib.native_model.Attribute, ...] | None:
	"""Return attributes only when this complete line is a Djot attribute line."""
	match = _ATTRIBUTE_LINE.fullmatch(source.strip())
	if match is None:
		return None
	attributes = parse_attribute_tokens(path, line, match.group("body"))
	return attributes


#============================================
def add_attributes(block: slide_lib.native_model.Block,
		attributes: tuple[slide_lib.native_model.Attribute, ...]) -> slide_lib.native_model.Block:
	"""Attach pending metadata to the next parsed block."""
	combined = block.attributes + attributes
	result = dataclasses.replace(block, attributes=combined)
	return result


#============================================
def add_item_attributes(item: slide_lib.native_model.ListItem,
		attributes: tuple[slide_lib.native_model.Attribute, ...]) -> slide_lib.native_model.ListItem:
	"""Attach metadata to a list item, preserving its nested list structure."""
	combined = item.attributes + attributes
	result = dataclasses.replace(item, attributes=combined)
	return result


#============================================
def replace_last_block(parsed: ParsedBlocks,
		transform: Callable[[slide_lib.native_model.Block], slide_lib.native_model.Block]) -> ParsedBlocks:
	"""Apply a deck-assembly action to the most recently parsed block."""
	if not parsed.spans:
		raise ValueError("a terminal action requires a preceding block")
	spans = list(parsed.spans)
	last = spans[-1]
	spans[-1] = dataclasses.replace(last, block=transform(last.block))
	result = ParsedBlocks(tuple(spans))
	return result


#============================================
def replace_last_list_item(parsed: ParsedBlocks,
		transform: Callable[[slide_lib.native_model.ListItem], slide_lib.native_model.ListItem]) -> ParsedBlocks:
	"""Apply a deck-assembly action to the deepest preceding list item."""
	if not parsed.spans or not isinstance(parsed.spans[-1].block, slide_lib.native_model.ListBlock):
		raise ValueError("this action requires a preceding list")
	last = parsed.spans[-1]
	list_block = last.block
	replaced = replace_deepest_last_list_item(list_block, transform)
	spans = list(parsed.spans)
	spans[-1] = dataclasses.replace(last, block=replaced)
	result = ParsedBlocks(tuple(spans))
	return result


#============================================
def replace_deepest_last_list_item(list_block: slide_lib.native_model.ListBlock,
		transform: Callable[[slide_lib.native_model.ListItem], slide_lib.native_model.ListItem]) -> slide_lib.native_model.ListBlock:
	"""Replace the final logical item, descending through its final child list."""
	items = list(list_block.items)
	item = items[-1]
	if item.children:
		children = list(item.children)
		children[-1] = replace_deepest_last_list_item(children[-1], transform)
		items[-1] = dataclasses.replace(item, children=tuple(children))
	else:
		items[-1] = transform(item)
	result = dataclasses.replace(list_block, items=tuple(items))
	return result


#============================================
def parse_image(path: pathlib.Path, line: int, source: str) -> slide_lib.native_model.Image | None:
	"""Parse a standalone component image, leaving ordinary text to paragraph parsing."""
	match = _IMAGE.fullmatch(source)
	if match is None:
		return None
	image_source = match.group("source")
	if image_source.startswith(("http://", "https://", "data:")):
		fail(path, line, "component images must use a repository-relative source")
	image = slide_lib.native_model.Image(location(path, line), match.group("alt"), image_source,
		match.group("title"))
	return image


#============================================
def split_table_row(path: pathlib.Path, line: int, source: str) -> tuple[str, ...]:
	"""Split one pipe-table row while retaining escaped pipes in inline source."""
	source = source.strip()
	if not source.startswith("|") or source.count("|") < 2:
		fail(path, line, "pipe tables require a leading pipe and at least one cell")
	cells: list[str] = []
	current: list[str] = []
	escaped = False
	for character in source[1:]:
		if escaped:
			current.append(character)
			escaped = False
		elif character == "\\":
			current.append(character)
			escaped = True
		elif character == "|":
			cells.append("".join(current).strip())
			current = []
		else:
			current.append(character)
	if current:
		fail(path, line, "pipe table rows must end with a pipe")
	result = tuple(cells)
	return result


#============================================
def table_separator_alignment(cells: tuple[str, ...]) -> tuple[str | None, ...] | None:
	"""Return Djot table alignment metadata when cells form a separator row.

	A plain hyphen cell has no alignment.  The native table IR has no place for
	alignment, so callers use a nonempty result to reject an otherwise valid row
	instead of silently changing its meaning.
	"""
	alignments: list[str | None] = []
	for cell in cells:
		match = re.fullmatch(r"(?P<left>:)?-+(?P<right>:)?", cell)
		if match is None:
			return None
		left = match.group("left") is not None
		right = match.group("right") is not None
		if left and right:
			alignments.append("center")
		elif left:
			alignments.append("left")
		elif right:
			alignments.append("right")
		else:
			alignments.append(None)
	result = tuple(alignments)
	return result


#============================================
def parse_fence(path: pathlib.Path, lines: list[str], index: int,
		base_line: int) -> tuple[slide_lib.native_model.CodeBlock, int]:
	"""Parse one Djot fenced code block and retain its optional language label."""
	match = _FENCE.fullmatch(lines[index])
	if match is None:
		fail(path, base_line + index, "malformed code fence")
	mark = match.group("mark")
	close = re.compile(rf"^{re.escape(mark[0])}{{{len(mark)},}}[ \t]*$")
	end = index + 1
	while end < len(lines) and close.fullmatch(lines[end]) is None:
		end += 1
	if end == len(lines):
		fail(path, base_line + index, "fenced code block is not closed")
	info = match.group("info").strip()
	language = info if info else None
	value = "\n".join(lines[index + 1:end])
	block = slide_lib.native_model.CodeBlock(location(path, base_line + index), value, language)
	return block, end + 1


#============================================
def parse_display_math(path: pathlib.Path, lines: list[str], index: int,
		base_line: int) -> tuple[slide_lib.native_model.DisplayMath, int]:
	"""Parse one single-line or fenced Djot display-mathematics expression."""
	source = lines[index].strip()
	if source != "$$":
		value = source[2:-2].strip()
		block = slide_lib.native_model.DisplayMath(location(path, base_line + index), value)
		return block, index + 1
	end = index + 1
	while end < len(lines) and lines[end].strip() != "$$":
		end += 1
	if end == len(lines):
		fail(path, base_line + index, "display mathematics is not closed")
	value = "\n".join(lines[index + 1:end]).strip()
	block = slide_lib.native_model.DisplayMath(location(path, base_line + index), value)
	return block, end + 1


#============================================
def parse_list(path: pathlib.Path, lines: list[str], index: int, base_line: int,
		indent: int | None = None) -> tuple[slide_lib.native_model.ListBlock, int]:
	"""Parse Djot lists, requiring a blank boundary before nested lists."""
	# Attributes immediately before a nested list apply to the list element, not
	# to its first item.  Djot does not require their indentation to reproduce
	# the following marker's indentation, so discover the marker after collecting
	# those attributes rather than deriving list depth from the attribute line.
	block_attributes: tuple[slide_lib.native_model.Attribute, ...] = ()
	pending_line: int | None = None
	while index < len(lines):
		attributes = parse_attributes(path, base_line + index, lines[index])
		if attributes is None:
			break
		block_attributes += attributes
		pending_line = base_line + index
		index += 1
	if index >= len(lines):
		fail(path, pending_line or base_line + index, "Djot attributes must precede a list item")
	first_index = index
	first = _LIST_ITEM.fullmatch(lines[index])
	if first is None:
		fail(path, pending_line or base_line + index, "Djot attributes must precede a list item")
	current_indent = len(first.group("indent"))
	if indent is not None and current_indent != indent:
		fail(path, pending_line or base_line + index, "malformed Djot list indentation")
	ordered = first.group("number") is not None
	marker = first.group("delimiter") if ordered else first.group("bullet")
	start = int(first.group("number")) if ordered else 1
	items: list[slide_lib.native_model.ListItem] = []
	while index < len(lines):
		match = _LIST_ITEM.fullmatch(lines[index])
		if match is None or len(match.group("indent")) != current_indent:
			break
		is_ordered = match.group("number") is not None
		item_marker = match.group("delimiter") if is_ordered else match.group("bullet")
		if is_ordered != ordered or item_marker != marker:
			break
		line = base_line + index
		text_lines = [match.group("text")]
		index += 1
		children: list[slide_lib.native_model.ListBlock] = []
		nested_boundary = False
		while index < len(lines):
			next_item = _LIST_ITEM.fullmatch(lines[index])
			if next_item is not None and len(next_item.group("indent")) == current_indent:
				break
			attributes = parse_attributes(path, base_line + index, lines[index])
			leading = len(lines[index]) - len(lines[index].lstrip(" "))
			if attributes is not None and leading == current_indent:
				break
			if (nested_boundary and next_item is not None and
					len(next_item.group("indent")) > current_indent):
				child_indent = len(next_item.group("indent"))
				child, index = parse_list(path, lines, index, base_line, child_indent)
				children.append(child)
				continue
			if nested_boundary and attributes is not None and leading > current_indent:
				child, index = parse_list(path, lines, index, base_line)
				children.append(child)
				continue
			if not lines[index].strip():
				index += 1
				nested_boundary = True
				continue
			leading = len(lines[index]) - len(lines[index].lstrip(" "))
			if leading <= current_indent:
				break
			text_lines.append(lines[index].lstrip(" "))
			index += 1
			nested_boundary = False
		text = "\n".join(text_lines)
		inlines = slide_lib.djot_inline.parse_inlines(path, line, text)
		items.append(slide_lib.native_model.ListItem(location(path, line), inlines, tuple(children),
			attributes=()))
	if not items:
		fail(path, base_line + index, "Djot lists require an item")
	block = slide_lib.native_model.ListBlock(location(path, base_line + first_index), ordered, start, tuple(items),
		attributes=block_attributes)
	return block, index


#============================================
def parse_table(path: pathlib.Path, lines: list[str], index: int,
		base_line: int) -> tuple[slide_lib.native_model.Table, int]:
	"""Parse a Djot table, preserving only metadata expressible in the IR."""
	first_line = base_line + index
	rows: list[tuple[tuple[slide_lib.native_model.Inline, ...], ...]] = []
	width: int | None = None
	separator_index: int | None = None
	while index < len(lines) and lines[index].lstrip(" ").startswith("|"):
		line = base_line + index
		cells = split_table_row(path, line, lines[index])
		if width is None:
			width = len(cells)
		elif len(cells) != width:
			fail(path, line, "pipe table rows must have the same number of cells")
		alignment = table_separator_alignment(cells)
		if alignment is not None:
			if separator_index is not None:
				fail(path, line, "pipe tables support exactly one header-separator row")
			if len(rows) > 1:
				fail(path, line, "pipe table header separators must follow exactly one header row")
			if any(value is not None for value in alignment):
				fail(path, line, "pipe table alignment is not supported")
			separator_index = len(rows)
			index += 1
			continue
		parsed_cells = tuple(
			slide_lib.djot_inline.parse_inlines(path, base_line + index, cell)
			for cell in cells
		)
		rows.append(parsed_cells)
		index += 1
	if separator_index in (None, 0):
		headers: tuple[tuple[slide_lib.native_model.Inline, ...], ...] = ()
		body_rows = tuple(rows)
	else:
		headers = rows[0]
		body_rows = tuple(rows[1:])
	block = slide_lib.native_model.Table(location(path, first_line), headers, body_rows)
	return block, index


#============================================
def parse_quote(path: pathlib.Path, lines: list[str], index: int,
		base_line: int) -> tuple[slide_lib.native_model.QuoteBlock, int]:
	"""Parse ordinary quote lines as nested semantic blocks, not layout cells."""
	first_line = base_line + index
	quoted: list[str] = []
	while index < len(lines):
		match = _QUOTE.fullmatch(lines[index])
		if match is None:
			break
		quoted.append(match.group("text"))
		index += 1
	nested = parse_blocks(path, "\n".join(quoted), first_line)
	block = slide_lib.native_model.QuoteBlock(location(path, first_line), nested.blocks)
	return block, index


#============================================
def reject_known_unsupported(path: pathlib.Path, line: int, source: str) -> None:
	"""Give recognized Djot forms a diagnostic instead of silently flattening them."""
	for prefix, message in _KNOWN_UNSUPPORTED:
		if source.startswith(prefix):
			fail(path, line, message)
	if source.startswith(": "):
		fail(path, line, "definition lists are not supported")
	if re.fullmatch(r"[*-]{3,}[ \t]*", source):
		fail(path, line, "thematic breaks are not supported")


#============================================
def parse_blocks(path: pathlib.Path, source: str, base_line: int = 1) -> ParsedBlocks:
	"""Parse supported Djot blocks with 1-based physical source locations."""
	normalized = source.replace("\r\n", "\n").replace("\r", "\n")
	lines = normalized.split("\n")
	spans: list[_BlockSpan] = []
	index = 0
	pending_attributes: tuple[slide_lib.native_model.Attribute, ...] = ()
	pending_line: int | None = None
	while index < len(lines):
		if not lines[index].strip():
			index += 1
			continue
		line = base_line + index
		attributes = parse_attributes(path, line, lines[index])
		if attributes is not None:
			pending_attributes += attributes
			pending_line = line
			index += 1
			continue
		fence = _FENCE.fullmatch(lines[index])
		if fence is not None:
			block, next_index = parse_fence(path, lines, index, base_line)
		elif _QUOTE.fullmatch(lines[index]) is not None:
			block, next_index = parse_quote(path, lines, index, base_line)
		elif _LIST_ITEM.fullmatch(lines[index]) is not None:
			block, next_index = parse_list(path, lines, index, base_line)
		elif lines[index].lstrip(" ").startswith("|"):
			block, next_index = parse_table(path, lines, index, base_line)
		elif lines[index].strip().startswith("$$"):
			if not lines[index].strip().endswith("$$") or len(lines[index].strip()) < 4:
				if lines[index].strip() != "$$":
					fail(path, line, "display mathematics must close with $$")
			block, next_index = parse_display_math(path, lines, index, base_line)
		else:
			heading = _HEADING.fullmatch(lines[index])
			if heading is not None:
				block = slide_lib.native_model.Heading(location(path, line), len(heading.group("marks")),
					slide_lib.djot_inline.parse_inlines(path, line, heading.group("text")))
				next_index = index + 1
			else:
				reject_known_unsupported(path, line, lines[index])
				# A component image is a whole Djot paragraph, never an inline
				# shortcut.  Gather soft-wrapped source before classifying it so an
				# image-looking line beside ordinary text reaches the inline parser
				# and receives its normal source-located unsupported-subset error.
				paragraph_lines = [lines[index].lstrip(" ")]
				index += 1
				while index < len(lines) and lines[index].strip():
					reject_known_unsupported(path, base_line + index, lines[index])
					paragraph_lines.append(lines[index].lstrip(" "))
					index += 1
				paragraph = "\n".join(paragraph_lines)
				image = parse_image(path, line, paragraph)
				if image is not None:
					block = image
					next_index = index
				else:
					block = slide_lib.native_model.Paragraph(location(path, line),
						slide_lib.djot_inline.parse_inlines(path, line, paragraph))
					next_index = index
		if pending_attributes:
			block = add_attributes(block, pending_attributes)
			pending_attributes = ()
			pending_line = None
		spans.append(_BlockSpan(block, line, base_line + next_index))
		index = next_index
	if pending_attributes:
		fail(path, pending_line or base_line + len(lines), "dangling Djot attributes")
	result = ParsedBlocks(tuple(spans))
	return result
