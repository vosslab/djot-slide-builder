"""Assemble the repository-supported Djot subset into native slide objects."""

# Standard Library
import dataclasses
import pathlib
import re

# Local Modules
import slide_lib.djot_blocks
import slide_lib.djot_errors
import slide_lib.djot_grammar
import slide_lib.layouts
import slide_lib.native_model


_FENCE_OPEN = re.compile(r"^(?P<mark>`{3,}|~{3,}).*$")


@dataclasses.dataclass(frozen=True)
class _SourceLine:
	"""One normalized physical source line retained for deck assembly."""
	line: int
	value: str


@dataclasses.dataclass(frozen=True)
class _SlideSource:
	"""The directive and physical lines belonging to one Djot slide."""
	location: slide_lib.native_model.SourceLocation
	layout_name: str
	lines: tuple[_SourceLine, ...]


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
def visible_text(inlines: tuple[slide_lib.native_model.Inline, ...]) -> str:
	"""Return authored text for deck metadata without importing a renderer."""
	parts: list[str] = []
	for inline in inlines:
		if isinstance(inline, (slide_lib.native_model.Text, slide_lib.native_model.InlineCode,
				slide_lib.native_model.InlineMath)):
			parts.append(inline.value)
		elif isinstance(inline, slide_lib.native_model.Break):
			parts.append(" ")
		else:
			parts.append(visible_text(inline.children))
	result = "".join(parts).strip()
	return result


#============================================
def split_slides(path: pathlib.Path, source: str) -> tuple[_SlideSource, ...]:
	"""Split exact layout-directive lines while retaining physical line numbers."""
	lines = source.replace("\r\n", "\n").replace("\r", "\n").split("\n")
	slides: list[_SlideSource] = []
	layout_name: str | None = None
	layout_line = 0
	content: list[_SourceLine] = []
	fence: tuple[str, int] | None = None
	for number, value in enumerate(lines, start=1):
		if fence is not None:
			content.append(_SourceLine(number, value))
			if re.fullmatch(rf"{re.escape(fence[0])}{{{fence[1]},}}[ \t]*", value) is not None:
				fence = None
			continue
		fence_match = _FENCE_OPEN.fullmatch(value)
		if fence_match is not None:
			if layout_name is None:
				fail(path, number, "Djot decks must begin with an exact layout directive")
			content.append(_SourceLine(number, value))
			mark = fence_match.group("mark")
			fence = (mark[0], len(mark))
			continue
		match = slide_lib.djot_grammar.LAYOUT_DIRECTIVE_PATTERN.fullmatch(value)
		if match is not None:
			if layout_name is not None:
				slides.append(_SlideSource(location(path, layout_line), layout_name, tuple(content)))
			layout_name = match.group("layout")
			layout_line = number
			content = []
			continue
		if value.startswith("=== layout:"):
			fail(path, number, "layout directives must be exact whole lines: === layout: <name>")
		if layout_name is None:
			if value.strip():
				fail(path, number, "Djot decks must begin with an exact layout directive")
			continue
		content.append(_SourceLine(number, value))
	if layout_name is None:
		fail(path, 1, "Djot decks require at least one layout directive")
	slides.append(_SlideSource(location(path, layout_line), layout_name, tuple(content)))
	result = tuple(slides)
	return result


#============================================
def action_for(path: pathlib.Path, line: int, action: str) -> slide_lib.native_model.Reveal:
	"""Resolve one exact action spelling or report its source-local status."""
	if action in slide_lib.djot_grammar.DEFERRED_ACTIONS:
		fail(path, line, f"{action} is recognized but not yet supported")
	reveal = slide_lib.djot_grammar.ACTION_REVEALS.get(action)
	if reveal is None:
		fail(path, line, f"unknown Djot action: {action}")
	return reveal


#============================================
def reveal_block(path: pathlib.Path, line: int, block: slide_lib.native_model.Block,
		reveal: slide_lib.native_model.Reveal) -> slide_lib.native_model.Block:
	"""Attach one action to a block that owns reveal intent."""
	if not isinstance(block, (slide_lib.native_model.Heading, slide_lib.native_model.Paragraph,
			slide_lib.native_model.Image, slide_lib.native_model.ListBlock, slide_lib.native_model.QuoteBlock)):
		fail(path, line, f"{type(block).__name__} blocks cannot receive Djot actions")
	if block.reveal is not None:
		fail(path, line, "Djot actions cannot attach more than one reveal to the same block")
	if reveal.sequence is slide_lib.native_model.RevealSequence.PARAGRAPHS and not isinstance(block,
			slide_lib.native_model.ListBlock):
		fail(path, line, "cascade appear requires a following ListBlock")
	result = dataclasses.replace(block, reveal=reveal)
	return result


#============================================
def reveal_item(path: pathlib.Path, line: int, item: slide_lib.native_model.ListItem,
		reveal: slide_lib.native_model.Reveal) -> slide_lib.native_model.ListItem:
	"""Attach one terminal action to the final logical list item."""
	if item.reveal is not None:
		fail(path, line, "Djot actions cannot attach more than one reveal to the same list item")
	if reveal.sequence is slide_lib.native_model.RevealSequence.PARAGRAPHS:
		fail(path, line, "terminal cascade appear is not supported; use a prefix cascade on a ListBlock")
	result = dataclasses.replace(item, reveal=reveal)
	return result


#============================================
def attach_terminal(path: pathlib.Path, line: int, parsed: slide_lib.djot_blocks.ParsedBlocks,
		reveal: slide_lib.native_model.Reveal) -> slide_lib.djot_blocks.ParsedBlocks:
	"""Attach one terminal action to the immediately preceding source object."""
	block = parsed.block_before(line)
	if block is None:
		fail(path, line, "terminal Djot actions require a preceding block")
	try:
		if isinstance(block, slide_lib.native_model.ListBlock):
			result = slide_lib.djot_blocks.replace_last_list_item(parsed,
				lambda item: reveal_item(path, line, item, reveal))
		else:
			result = slide_lib.djot_blocks.replace_last_block(parsed,
				lambda target: reveal_block(path, line, target, reveal))
	except slide_lib.djot_errors.DjotParseError:
		raise
	except ValueError as exc:
		fail(path, line, str(exc))
	return result


#============================================
def attach_prefix(path: pathlib.Path, line: int, parsed: slide_lib.djot_blocks.ParsedBlocks,
		reveal: slide_lib.native_model.Reveal) -> slide_lib.djot_blocks.ParsedBlocks:
	"""Attach one prefix action to the next parsed source block."""
	block = parsed.block_after(line + 1)
	if block is None:
		fail(path, line, "prefix Djot actions require a following block")
	spans = list(parsed.spans)
	for index, span in enumerate(spans):
		if span.block is block:
			spans[index] = dataclasses.replace(span, block=reveal_block(path, line, block, reveal))
			return slide_lib.djot_blocks.ParsedBlocks(tuple(spans))
	fail(path, line, "prefix Djot action target was not found")


#============================================
def parse_region(path: pathlib.Path, lines: tuple[_SourceLine, ...], layout_name: str,
		slot_name: str | None) -> tuple[slide_lib.native_model.Block, ...]:
	"""Parse one global or named-slot region and bind its neighboring actions."""
	spans: list[object] = []
	pending: tuple[int, slide_lib.native_model.Reveal] | None = None
	segment: list[_SourceLine] = []
	fence: tuple[str, int] | None = None

	def append_segment() -> None:
		nonlocal pending, segment
		if not segment:
			return
		# The imported ODP corpus has adjacent component-image paragraphs without
		# intervening blank lines.  Keep each complete component image a block while
		# leaving text-plus-image paragraphs intact for the block parser to reject.
		pieces: list[list[_SourceLine]] = [[]]
		for index, source_line in enumerate(segment):
			pieces[-1].append(source_line)
			if index + 1 == len(segment):
				continue
			next_line = segment[index + 1]
			if not source_line.value.startswith("![") or not next_line.value.startswith("!["):
				continue
			if (slide_lib.djot_blocks.parse_image(path, source_line.line, source_line.value) is not None and
					slide_lib.djot_blocks.parse_image(path, next_line.line, next_line.value) is not None):
				pieces.append([])
		parsed_spans: list[object] = []
		for piece in pieces:
			if not piece:
				continue
			parsed_piece = slide_lib.djot_blocks.parse_blocks(path,
				"\n".join(source_line.value for source_line in piece), piece[0].line)
			parsed_spans.extend(parsed_piece.spans)
		parsed = slide_lib.djot_blocks.ParsedBlocks(tuple(parsed_spans))
		if pending is not None:
			parsed = attach_prefix(path, pending[0], parsed, pending[1])
			pending = None
		spans.extend(parsed.spans)
		segment = []

	for source_line in lines:
		value = source_line.value
		if fence is not None:
			segment.append(source_line)
			if re.fullmatch(rf"{re.escape(fence[0])}{{{fence[1]},}}[ \t]*", value) is not None:
				fence = None
			continue
		fence_match = _FENCE_OPEN.fullmatch(value)
		if fence_match is not None:
			segment.append(source_line)
			mark = fence_match.group("mark")
			fence = (mark[0], len(mark))
			continue
		prefix = slide_lib.djot_grammar.PREFIX_ACTION_PATTERN.fullmatch(value)
		terminal = slide_lib.djot_grammar.TERMINAL_ACTION_PATTERN.fullmatch(value)
		if prefix is None and terminal is None and value.startswith(("=>", "<=")):
			fail(path, source_line.line, "Djot action directives must be exact whole lines")
		if prefix is None and terminal is None:
			segment.append(source_line)
			continue
		append_segment()
		if layout_name == "multiple-choice" and slot_name == "answer":
			fail(path, source_line.line, "multiple-choice answer uses an implicit on-click object appear reveal")
		if prefix is not None:
			if pending is not None:
				fail(path, source_line.line, "prefix Djot actions require a block before another action")
			pending = (source_line.line, action_for(path, source_line.line, prefix.group("action")))
		else:
			parsed = slide_lib.djot_blocks.ParsedBlocks(tuple(spans))
			updated = attach_terminal(path, source_line.line, parsed,
				action_for(path, source_line.line, terminal.group("action")))
			spans = list(updated.spans)
	append_segment()
	if pending is not None:
		fail(path, pending[0], "prefix Djot actions require a following block")
	blocks = tuple(span.block for span in spans)
	return blocks


#============================================
def validate_global_titles(path: pathlib.Path, layout: slide_lib.layouts.LayoutSpec,
		blocks: tuple[slide_lib.native_model.Block, ...]) -> None:
	"""Enforce title and subtitle regions before source reaches a layout builder."""
	for block in blocks:
		if not isinstance(block, slide_lib.native_model.Heading):
			continue
		if block.level == 1 and not layout.allows_title:
			fail(path, block.location.line, f"{layout.name} slides do not accept a title")
		if block.level == 2 and not layout.allows_subtitle:
			fail(path, block.location.line, f"{layout.name} slides do not accept a subtitle")


#============================================
def implicit_multiple_choice_answer(path: pathlib.Path, cell: slide_lib.native_model.Cell) -> slide_lib.native_model.Cell:
	"""Add one implicit popup reveal to a one- or two-paragraph answer."""
	# ASVS 2.2.1: accept only the bounded answer structure with a native destination.
	if not 1 <= len(cell.blocks) <= 2:
		offending = cell.blocks[2].location if len(cell.blocks) > 2 else cell.location
		fail(path, offending.line, "multiple-choice answer requires one or two editable text paragraphs")
	for answer in cell.blocks:
		if not isinstance(answer, slide_lib.native_model.Paragraph):
			fail(path, answer.location.line, "multiple-choice answer accepts editable text paragraphs only")
		if not visible_text(answer.inlines):
			fail(path, answer.location.line, "multiple-choice answer requires visible editable text")
		if answer.reveal is not None:
			fail(path, answer.location.line, "multiple-choice answer only accepts its implicit reveal")
	reveal = slide_lib.native_model.Reveal(slide_lib.native_model.RevealEffect.APPEAR,
		slide_lib.native_model.RevealSequence.OBJECT)
	first, *remaining = cell.blocks
	updated = dataclasses.replace(first, reveal=reveal)
	result = dataclasses.replace(cell, blocks=(updated, *remaining))
	return result


#============================================
def assemble_slide(path: pathlib.Path, source: _SlideSource) -> slide_lib.native_model.Slide:
	"""Bind one layout directive's global and named regions to a native slide."""
	if source.layout_name not in slide_lib.djot_grammar.legal_layout_names():
		fail(path, source.location.line, f"unknown Djot layout: {source.layout_name}")
	layout = slide_lib.layouts.LAYOUTS[source.layout_name]
	global_lines: list[_SourceLine] = []
	regions: dict[str, list[_SourceLine]] = {}
	active_slot: str | None = None
	fence: tuple[str, int] | None = None
	for source_line in source.lines:
		if fence is not None:
			if active_slot is None:
				global_lines.append(source_line)
			else:
				regions[active_slot].append(source_line)
			if re.fullmatch(rf"{re.escape(fence[0])}{{{fence[1]},}}[ \t]*", source_line.value) is not None:
				fence = None
			continue
		fence_match = _FENCE_OPEN.fullmatch(source_line.value)
		if fence_match is not None:
			if active_slot is None:
				global_lines.append(source_line)
			else:
				regions[active_slot].append(source_line)
			mark = fence_match.group("mark")
			fence = (mark[0], len(mark))
			continue
		match = slide_lib.djot_grammar.SLOT_DIRECTIVE_PATTERN.fullmatch(source_line.value)
		if match is not None:
			slot_name = match.group("slot")
			if slot_name not in slide_lib.djot_grammar.legal_slot_names(source.layout_name):
				fail(path, source_line.line, f"{source.layout_name} slides do not declare slot: {slot_name}")
			if slot_name in regions:
				fail(path, source_line.line, f"{source.layout_name} slides contain duplicate slot: {slot_name}")
			regions[slot_name] = []
			active_slot = slot_name
			continue
		near_slot = re.fullmatch(r"@(?P<slot>[a-z][a-z0-9-]*)(?P<suffix>.*)", source_line.value)
		if (near_slot is not None and near_slot.group("slot") in layout.slot_names and
				near_slot.group("suffix")):
			fail(path, source_line.line, "slot directives must be exact whole lines")
		if active_slot is None:
			global_lines.append(source_line)
		else:
			regions[active_slot].append(source_line)
	global_blocks = parse_region(path, tuple(global_lines), source.layout_name, None)
	validate_global_titles(path, layout, global_blocks)
	cells: list[slide_lib.native_model.Cell] = []
	for slot_name in layout.slot_names:
		if slot_name not in regions:
			fail(path, source.location.line, f"{source.layout_name} slides are missing required slot: {slot_name}")
		region_lines = tuple(regions[slot_name])
		cell_line = region_lines[0].line if region_lines else source.location.line
		blocks = parse_region(path, region_lines, source.layout_name, slot_name)
		cells.append(slide_lib.native_model.Cell(location(path, cell_line), blocks, slot_name))
	if len(regions) != len(layout.slot_names):
		# The individual unknown/duplicate cases have already failed; this protects
		# future grammar changes from silently accepting an unbound region.
		fail(path, source.location.line, f"{source.layout_name} slots do not match its layout contract")
	if source.layout_name == "multiple-choice":
		answer_index = layout.slot_names.index("answer")
		cells[answer_index] = implicit_multiple_choice_answer(path, cells[answer_index])
	slide = slide_lib.native_model.Slide(source.location, source.layout_name, True, (), global_blocks,
		tuple(cells))
	return slide


#============================================
def parse_deck(input_path: pathlib.Path) -> slide_lib.native_model.Deck:
	"""Parse one source-only Djot deck into the native presentation-neutral IR."""
	path = input_path.resolve()
	try:
		source = path.read_text(encoding="utf-8")
	except UnicodeDecodeError:
		fail(path, 1, "Djot source must use UTF-8 text")
		source = ""  # Satisfy static analyzers after fail's intentional exception.
	slides = tuple(assemble_slide(path, slide_source) for slide_source in split_slides(path, source))
	first_title = next((block for slide in slides for block in slide.blocks
		if isinstance(block, slide_lib.native_model.Heading) and block.level == 1), None)
	title = visible_text(first_title.inlines) if first_title is not None else ""
	repo_root = next((candidate for candidate in (path.parent, *path.parents)
		if (candidate / ".git").exists()), path.parent).resolve()
	deck = slide_lib.native_model.Deck(path, path.parent, repo_root, title, True, slides, {})
	return deck
