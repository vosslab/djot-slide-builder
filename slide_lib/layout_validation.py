"""Presentation-source semantic validation for native slide layouts."""

# Local Modules
import slide_lib.native_model


class LayoutError(ValueError):
	"""Report an expected source or native-layout validation failure."""


#============================================
def source_error(source: slide_lib.native_model.SourceLocation | slide_lib.native_model.Slide,
		message: str) -> ValueError:
	"""Attach a semantic layout failure to its canonical source location."""
	location = source.location if isinstance(source, slide_lib.native_model.Slide) else source
	return ValueError(f"{location.path}:{location.line}: {message}")


#============================================
def inline_text(inlines: tuple[slide_lib.native_model.Inline, ...]) -> str:
	"""Return visible authored text for semantic source validation."""
	parts: list[str] = []
	for inline in inlines:
		if isinstance(inline, (slide_lib.native_model.Text, slide_lib.native_model.InlineCode)):
			parts.append(inline.value)
		elif isinstance(inline, slide_lib.native_model.InlineMath):
			raise LayoutError("InlineMath requires source validation before native rendering")
		elif isinstance(inline, slide_lib.native_model.Break):
			parts.append(" ")
		else:
			parts.append(inline_text(inline.children))
	return "".join(parts).strip()


#============================================
def flatten_list(block: slide_lib.native_model.ListBlock, level: int = 0) -> list[tuple[tuple[slide_lib.native_model.Inline, ...], int, bool, bool, int]]:
	"""Flatten nested list items for visible-choice validation."""
	items: list[tuple[tuple[slide_lib.native_model.Inline, ...], int, bool, bool, int]] = []
	for offset, item in enumerate(block.items):
		items.append((item.inlines, level, block.ordered, False, block.start + offset))
		for child in item.children:
			items.extend(flatten_list(child, level + 1))
	return items


#============================================
def body_parts(blocks: tuple[slide_lib.native_model.Block, ...]) -> tuple[list[slide_lib.native_model.Heading], list[tuple[tuple[slide_lib.native_model.Inline, ...], int, bool, bool, int]], list[slide_lib.native_model.Image], list[slide_lib.native_model.Table]]:
	"""Classify supported semantic blocks for layout-contract checks."""
	headings: list[slide_lib.native_model.Heading] = []
	items: list[tuple[tuple[slide_lib.native_model.Inline, ...], int, bool, bool, int]] = []
	images: list[slide_lib.native_model.Image] = []
	tables: list[slide_lib.native_model.Table] = []
	for block in blocks:
		if isinstance(block, slide_lib.native_model.Heading):
			headings.append(block)
		elif isinstance(block, slide_lib.native_model.Paragraph):
			items.append((block.inlines, 0, False, True, 1))
		elif isinstance(block, slide_lib.native_model.ListBlock):
			items.extend(flatten_list(block))
		elif isinstance(block, slide_lib.native_model.Image):
			images.append(block)
		elif isinstance(block, slide_lib.native_model.Table):
			tables.append(block)
	return headings, items, images, tables


#============================================
def unsupported_block(blocks: tuple[slide_lib.native_model.Block, ...]) -> slide_lib.native_model.Block | None:
	"""Return the first semantic block without a native layout destination."""
	for block in blocks:
		if not isinstance(block, (slide_lib.native_model.Heading, slide_lib.native_model.Paragraph,
				slide_lib.native_model.Image, slide_lib.native_model.ListBlock, slide_lib.native_model.Table)):
			return block
	return None


#============================================
def attributed_list_item(item: slide_lib.native_model.ListItem) -> slide_lib.native_model.ListItem | slide_lib.native_model.Block | None:
	"""Return the first attributed nested list item or block in source order."""
	if item.attributes:
		return item
	for child in item.children:
		attributed = attributed_block(child)
		if attributed is not None:
			return attributed
	return None


#============================================
def attributed_block(block: slide_lib.native_model.Block) -> slide_lib.native_model.ListItem | slide_lib.native_model.Block | None:
	"""Return the first attributed block, including recursively nested content."""
	if block.attributes:
		return block
	if isinstance(block, slide_lib.native_model.ListBlock):
		for item in block.items:
			attributed = attributed_list_item(item)
			if attributed is not None:
				return attributed
	if isinstance(block, slide_lib.native_model.QuoteBlock):
		for child in block.blocks:
			attributed = attributed_block(child)
			if attributed is not None:
				return attributed
	return None


#============================================
def attributed_source(blocks: tuple[slide_lib.native_model.Block, ...]) -> slide_lib.native_model.ListItem | slide_lib.native_model.Block | None:
	"""Return the first source item whose attributes lack a native mapping."""
	for block in blocks:
		attributed = attributed_block(block)
		if attributed is not None:
			return attributed
	return None


#============================================
def inline_math_location(inlines: tuple[slide_lib.native_model.Inline, ...],
		location: slide_lib.native_model.SourceLocation) -> slide_lib.native_model.SourceLocation | None:
	"""Return the containing source location for unsupported inline math."""
	for inline in inlines:
		if isinstance(inline, slide_lib.native_model.InlineMath):
			return location
		if isinstance(inline, (slide_lib.native_model.Strong, slide_lib.native_model.Emphasis,
				slide_lib.native_model.Link)):
			math_location = inline_math_location(inline.children, location)
			if math_location is not None:
				return math_location
	return None


#============================================
def list_item_inline_math_location(item: slide_lib.native_model.ListItem) -> slide_lib.native_model.SourceLocation | None:
	"""Return the first inline-math location in one list item or nested list."""
	math_location = inline_math_location(item.inlines, item.location)
	if math_location is not None:
		return math_location
	for child in item.children:
		math_location = block_inline_math_location(child)
		if math_location is not None:
			return math_location
	return None


#============================================
def block_inline_math_location(block: slide_lib.native_model.Block) -> slide_lib.native_model.SourceLocation | None:
	"""Return the first inline-math location in a renderable semantic block."""
	if isinstance(block, (slide_lib.native_model.Heading, slide_lib.native_model.Paragraph)):
		return inline_math_location(block.inlines, block.location)
	if isinstance(block, slide_lib.native_model.ListBlock):
		for item in block.items:
			math_location = list_item_inline_math_location(item)
			if math_location is not None:
				return math_location
	return None


#============================================
def source_inline_math_location(blocks: tuple[slide_lib.native_model.Block, ...]) -> slide_lib.native_model.SourceLocation | None:
	"""Return the first source location requiring an inline-math adapter."""
	for block in blocks:
		math_location = block_inline_math_location(block)
		if math_location is not None:
			return math_location
	return None


#============================================
def revealed_list_item(item: slide_lib.native_model.ListItem) -> slide_lib.native_model.ListItem | slide_lib.native_model.ListBlock | None:
	"""Return the first reveal attached to a list item or nested list."""
	if item.reveal is not None:
		return item
	for child in item.children:
		revealed = revealed_block(child)
		if revealed is not None:
			return revealed
	return None


#============================================
def revealed_block(block: slide_lib.native_model.Block) -> slide_lib.native_model.ListItem | slide_lib.native_model.Block | None:
	"""Return the first reveal-bearing source block in reading order."""
	if block.reveal is not None:
		return block
	if isinstance(block, slide_lib.native_model.ListBlock):
		for item in block.items:
			revealed = revealed_list_item(item)
			if revealed is not None:
				return revealed
	return None


#============================================
def revealed_source(blocks: tuple[slide_lib.native_model.Block, ...]) -> slide_lib.native_model.ListItem | slide_lib.native_model.Block | None:
	"""Return the first reveal-bearing block in a source region."""
	for block in blocks:
		revealed = revealed_block(block)
		if revealed is not None:
			return revealed
	return None


#============================================
def invalid_cascade(blocks: tuple[slide_lib.native_model.Block, ...]) -> slide_lib.native_model.ListItem | slide_lib.native_model.Block | None:
	"""Return a reveal whose paragraph sequence cannot map to editable text."""
	for block in blocks:
		if isinstance(block, (slide_lib.native_model.Heading, slide_lib.native_model.Paragraph,
				slide_lib.native_model.Image, slide_lib.native_model.ListBlock, slide_lib.native_model.QuoteBlock)) and \
				block.reveal is not None and (block.reveal.sequence is
				slide_lib.native_model.RevealSequence.PARAGRAPHS and not isinstance(block,
				slide_lib.native_model.ListBlock)):
			return block
		if isinstance(block, slide_lib.native_model.ListBlock):
			for item in block.items:
				revealed = invalid_cascade_items(item)
				if revealed is not None:
					return revealed
	return None


#============================================
def invalid_cascade_items(item: slide_lib.native_model.ListItem) -> slide_lib.native_model.ListItem | None:
	"""Return a terminal cascade from an item or any nested list descendant."""
	if item.reveal is not None and item.reveal.sequence is slide_lib.native_model.RevealSequence.PARAGRAPHS:
		return item
	for child in item.children:
		for nested_item in child.items:
			revealed = invalid_cascade_items(nested_item)
			if revealed is not None:
				return revealed
	return None


#============================================
def has_visible_items(items: list[tuple[tuple[slide_lib.native_model.Inline, ...], int, bool, bool, int]]) -> bool:
	"""Return whether a text region has at least one visible authored item."""
	return any(inline_text(inlines) for inlines, _, _, _, _ in items)


#============================================
def is_implicit_answer_reveal(reveal: slide_lib.native_model.Reveal | None) -> bool:
	"""Recognize the sole whole-popup reveal the Djot parser adds."""
	return reveal == slide_lib.native_model.Reveal(
		slide_lib.native_model.RevealEffect.APPEAR,
		slide_lib.native_model.RevealSequence.OBJECT,
	)


#============================================
def validate_multiple_choice(source: slide_lib.native_model.Slide) -> None:
	"""Enforce the focused source contract for the automatic answer popup."""
	if source.blocks:
		raise source_error(source.blocks[0].location,
			"multiple-choice slides do not accept source-global title, subtitle, or body blocks")
	question = next(cell for cell in source.cells if cell.name == "question")
	answer = next(cell for cell in source.cells if cell.name == "answer")
	choice_list = next((block for block in question.blocks
		if isinstance(block, slide_lib.native_model.ListBlock) and has_visible_items(flatten_list(block))), None)
	if choice_list is None:
		offending = next((block.location for block in question.blocks
			if isinstance(block, slide_lib.native_model.ListBlock)),
			question.blocks[0].location if question.blocks else question.location)
		raise source_error(offending,
			"multiple-choice question requires at least one visible editable choice ListBlock")
	question_headings, _, question_images, question_tables = body_parts(question.blocks)
	if question_headings or question_tables:
		offending = next(block.location for block in question.blocks
			if isinstance(block, (slide_lib.native_model.Heading,
				slide_lib.native_model.Table)))
		raise source_error(offending,
			"multiple-choice question supports an optional prompt paragraph and visible choice ListBlock only")
	if len(question_images) > 1:
		raise source_error(question_images[1].location,
			"multiple-choice question supports one optional top component image")
	if question_images and not isinstance(question.blocks[0], slide_lib.native_model.Image):
		raise source_error(question_images[0].location,
			"multiple-choice component image must be the first question block")
	question_reveal = revealed_source(question.blocks)
	if question_reveal is not None:
		raise source_error(question_reveal.location,
			"multiple-choice question content is visible when the slide opens and cannot have a reveal")
	# ASVS 2.2.1: retain the parser's bounded, typed popup contract at render entry.
	if not 1 <= len(answer.blocks) <= 2:
		offending = answer.blocks[2].location if len(answer.blocks) > 2 else answer.location
		raise source_error(offending,
			"multiple-choice answer requires one or two editable text paragraphs")
	for index, answer_block in enumerate(answer.blocks):
		if not isinstance(answer_block, slide_lib.native_model.Paragraph):
			raise source_error(answer_block.location,
				"multiple-choice answer accepts editable text paragraphs only")
		if not inline_text(answer_block.inlines):
			raise source_error(answer_block.location, "multiple-choice answer requires visible editable text")
		# Imported and authored Djot without reveal intent still
		# means the layout-owned popup behavior. Djot supplies the typed form.
		if index == 0 and answer_block.reveal is not None and not is_implicit_answer_reveal(answer_block.reveal):
			raise source_error(answer_block.location,
				"multiple-choice answer only accepts its implicit on-click object appear reveal")
		if index and answer_block.reveal is not None:
			raise source_error(answer_block.location,
				"multiple-choice answer only accepts its implicit on-click object appear reveal on the first paragraph")


#============================================
def validate_table(table: slide_lib.native_model.Table) -> None:
	"""Require a rectangular, non-empty native table surface (ASVS 2.2.1)."""
	column_count = len(table.headers) if table.headers else (len(table.rows[0]) if table.rows else 0)
	if column_count == 0:
		raise source_error(table.location, "tables require at least one column and one row")
	for row in table.rows:
		if len(row) != column_count:
			raise source_error(table.location, "table rows must have the same number of columns")


#============================================
def validate_table_region(blocks: tuple[slide_lib.native_model.Block, ...],
		location: slide_lib.native_model.SourceLocation, context: str) -> slide_lib.native_model.Table | None:
	"""Return a sole table, or explain why the region has no table destination."""
	tables = [block for block in blocks if isinstance(block, slide_lib.native_model.Table)]
	if not tables:
		return None
	if len(tables) > 1:
		raise source_error(tables[1].location,
			f"{context} supports one table; place the second table in a separate slot or use a one-table slide")
	table = tables[0]
	for block in blocks:
		if block is table or isinstance(block, slide_lib.native_model.Heading):
			continue
		raise source_error(block.location,
			f"{context} table cannot mix with {type(block).__name__}; place it in a separate slot or use a one-table slide")
	validate_table(table)
	return table


#============================================
def validate_flow_region(blocks: tuple[slide_lib.native_model.Block, ...],
		location: slide_lib.native_model.SourceLocation, context: str) -> None:
	"""Allow ordered text/list and image flow while retaining table's sole-mode rule."""
	headings = tuple(block for block in blocks if isinstance(block, slide_lib.native_model.Heading))
	if headings and blocks[0] is not headings[0]:
		raise source_error(headings[0].location,
			f"{context} local level-two heading must be the first cell block")
	non_headings = tuple(block for block in blocks if not isinstance(block, slide_lib.native_model.Heading))
	tables = tuple(block for block in non_headings if isinstance(block, slide_lib.native_model.Table))
	if tables:
		validate_table_region(blocks, location, context)


#============================================
def validate_layout_source(source: slide_lib.native_model.Slide, spec: object) -> None:
	"""Prove every supported source block has a native destination in ``spec``."""
	if spec.name != "multiple-choice":
		for blocks in (source.blocks,) + tuple(cell.blocks for cell in source.cells):
			cascade = invalid_cascade(blocks)
			if cascade is not None:
				raise source_error(cascade.location,
					"paragraph cascade reveals require a prefix ListBlock and cannot be terminal")
	for blocks, location in ((source.blocks, source.location),) + tuple(
		(cell.blocks, cell.location) for cell in source.cells):
		if any(isinstance(block, slide_lib.native_model.Table) for block in blocks):
			validate_table_region(blocks, location, "table region")
	unsupported = unsupported_block(source.blocks)
	if unsupported is not None:
		raise source_error(unsupported.location,
			f"{spec.name} slides cannot yet place {type(unsupported).__name__} blocks")
	for cell in source.cells:
		unsupported = unsupported_block(cell.blocks)
		if unsupported is not None:
			raise source_error(unsupported.location,
				f"{spec.name} slides cannot yet place {type(unsupported).__name__} blocks")
	attributed = attributed_source(source.blocks)
	if attributed is None:
		for cell in source.cells:
			attributed = attributed_source(cell.blocks)
			if attributed is not None:
				break
	if attributed is not None:
		raise source_error(attributed.location,
			f"{spec.name} slides cannot yet place attributes on {type(attributed).__name__}")
	math_location = source_inline_math_location(source.blocks)
	if math_location is None:
		for cell in source.cells:
			math_location = source_inline_math_location(cell.blocks)
			if math_location is not None:
				break
	if math_location is not None:
		raise source_error(math_location,
			f"{spec.name} slides cannot yet place InlineMath until a native math adapter exists")
	headings, items, images, root_tables = body_parts(source.blocks)
	cells = source.cells
	if spec.cell_count != len(spec.slot_names):
		raise LayoutError(f"{spec.name} has inconsistent cell and slot counts")
	if spec.slot_names:
		if len(cells) != len(spec.slot_names):
			offending = cells[-1].location if cells else source.location
			raise source_error(offending,
				f"{spec.name} slides require exactly one cell for each named slot: {', '.join(spec.slot_names)}")
		cell_names = [cell.name for cell in cells]
		unnamed = next((cell for cell in cells if cell.name is None), None)
		if unnamed is not None:
			raise source_error(unnamed.location, f"{spec.name} cells must name a declared slot")
		unknown = next((cell for cell in cells if cell.name not in spec.slot_names), None)
		if unknown is not None:
			raise source_error(unknown.location, f"{spec.name} cell names unknown slot: {unknown.name}")
		duplicate = next((name for name in spec.slot_names if cell_names.count(name) > 1), None)
		if duplicate is not None:
			offending = next(cell for cell in cells if cell.name == duplicate)
			raise source_error(offending.location, f"{spec.name} contains duplicate cell slot: {duplicate}")
		missing = next((name for name in spec.slot_names if name not in cell_names), None)
		if missing is not None:
			raise source_error(source.location, f"{spec.name} is missing required cell slot: {missing}")
	elif cells:
		raise source_error(cells[0].location, f"{spec.name} slides do not accept component cells")
	if spec.name == "blank":
		if source.blocks or cells:
			offending = source.blocks[0].location if source.blocks else cells[0].location
			raise source_error(offending, "blank slides must be empty")
		return
	if spec.name == "multiple-choice":
		validate_multiple_choice(source)
		return
	if spec.name in ("title-slide", "title-only", "centered-text", "gallery") and root_tables:
		raise source_error(root_tables[0].location, f"{spec.name} slides do not have a native table destination")
	if spec.cell_count and not spec.allows_root_body and spec.name != "gallery":
		if items or images or root_tables or any(heading.level != 1 for heading in headings):
			offending = next((block.location for block in source.blocks if not isinstance(block,
				slide_lib.native_model.Heading) or block.level != 1), source.location)
			raise source_error(offending, f"{spec.name} slides support a title and blockquote cells only")
		if not spec.allows_title and headings:
			raise source_error(headings[0].location, f"{spec.name} slides do not accept a title")
		if spec.allows_title and (len(headings) > 1 or any(heading.level != 1 for heading in headings)):
			offending = next((heading.location for heading in headings if heading.level != 1),
				headings[1].location if len(headings) > 1 else source.location)
			raise source_error(offending, f"{spec.name} slides accept zero or one level-one title")
		for index, slot_name in enumerate(spec.slot_names, start=1):
			cell = next(cell for cell in cells if cell.name == slot_name)
			cell_headings, cell_items, cell_images, cell_tables = body_parts(cell.blocks)
			if len(cell_headings) > 1 or any(heading.level != 2 for heading in cell_headings):
				offending = next((block.location for block in cell.blocks if isinstance(block,
					slide_lib.native_model.Heading) and block.level != 2), cell.location)
				raise source_error(offending, f"{spec.name} cell {index} supports one optional level-two heading")
			validate_flow_region(cell.blocks, cell.location, f"{spec.name} cell {index}")
			if cell_tables:
				continue
			if not cell_headings and not cell_items and not cell_images:
				raise source_error(cell.location, f"{spec.name} cell {index} requires editable text or component images")
		return
	if spec.name in ("title-slide", "centered-text"):
		if not headings or headings[0].level != 1 or items or images:
			raise source_error(source, f"{spec.name} slides support a title and level-two subtitle lines only")
		if any(heading.level != 2 for heading in headings[1:]):
			raise source_error(source, f"{spec.name} subtitle lines must use level-two Markdown")
		return
	if spec.name == "title-only":
		if len(headings) != 1 or headings[0].level != 1 or items or images:
			raise source_error(source, "title-only slides require exactly one level-one title")
		return
	if spec.name == "gallery":
		gallery = next(cell for cell in cells if cell.name == "gallery")
		_, gallery_items, gallery_images, gallery_tables = body_parts(gallery.blocks)
		if len(headings) > 1 or any(heading.level != 1 for heading in headings) or items or images or root_tables or gallery_items or gallery_tables or not 2 <= len(gallery_images) <= 6:
			raise source_error(source, "gallery slides support an optional title and two through six component images")
		return
	if not spec.allows_title and headings:
		raise source_error(headings[0].location, f"{spec.name} slides do not accept a title")
	if spec.allows_title and (len(headings) > 1 or any(heading.level != 1 for heading in headings)):
		offending = next((heading.location for heading in headings if heading.level != 1),
			headings[1].location if len(headings) > 1 else source.location)
		raise source_error(offending, f"{spec.name} slides accept zero or one level-one title")
	body = next(cell for cell in cells if cell.name == "body")
	body_headings, body_items, body_images, body_tables = body_parts(body.blocks)
	if len(body_headings) > 1 or any(heading.level != 2 for heading in body_headings):
		offending = next((heading.location for heading in body_headings if heading.level != 2),
			body_headings[1].location if len(body_headings) > 1 else body.location)
		raise source_error(offending, f"{spec.name} body supports one optional level-two heading")
	validate_flow_region(body.blocks, body.location, f"{spec.name} body")
	if spec.name in ("vertical-text-panel", "vertical-panel"):
		body_blocks = tuple(block for block in body.blocks if not isinstance(block,
			slide_lib.native_model.Heading))
		if len(body_blocks) != 1:
			offending = body_blocks[1].location if len(body_blocks) > 1 else body.location
			raise source_error(offending, f"{spec.name} slides require exactly one body block")
		if not isinstance(body_blocks[0], (slide_lib.native_model.Paragraph,
				slide_lib.native_model.ListBlock, slide_lib.native_model.Image)):
			raise source_error(body_blocks[0].location,
				f"{spec.name} slides require exactly one body block")
	if body_tables:
		if spec.name in ("vertical-text-panel", "vertical-panel"):
			raise source_error(body_tables[0].location, f"{spec.name} slides do not have a native table destination")
		return
	if not spec.allows_root_body:
		offending = next((block.location for block in body.blocks if isinstance(block,
			slide_lib.native_model.Image)), body.location)
		raise source_error(offending, f"{spec.name} slides require one body mode: editable text or component images")
	if not body_headings and not body_items and not body_images:
		raise source_error(body.location, f"{spec.name} slides require editable body text or one component image")
	if len(body_images) > 6:
		raise source_error(body_images[6].location,
			f"{spec.name} slides support at most six contained component images")
