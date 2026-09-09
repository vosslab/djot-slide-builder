import dataclasses
import slide_lib.layout_builders
import slide_lib.layout_measurement
import slide_lib.layout_registry
import slide_lib.layout_content
import slide_lib.layout_model
import slide_lib.layout_primitives
import slide_lib.native_model
import slide_lib.presentation_theme

@dataclasses.dataclass(frozen=True)
class _PageCandidate:
	page: slide_lib.layout_model.LayoutSlide
	kind: slide_lib.layout_primitives.ContinuationKind = slide_lib.layout_primitives.ContinuationKind.NORMAL
	context: slide_lib.layout_model.ContinuationContext | None = None

def registered_layout_names() -> tuple[str, ...]:
	result = slide_lib.layout_registry.names()
	return result

def layout_contract(name: str) -> slide_lib.layout_primitives.LayoutContract:
	result = slide_lib.layout_registry.contract_for(name)
	return result

def compile_layout_deck(deck: slide_lib.native_model.Deck,
		theme: slide_lib.presentation_theme.PresentationTheme) -> slide_lib.layout_model.LayoutDeck:
	session = slide_lib.layout_measurement.MeasurementSession(theme)
	physical: list[slide_lib.layout_model.LayoutSlide] = []
	for source_index, source in enumerate(deck.slides):
		source_id = f"slide-{source_index + 1}"
		pages = _compile_source_pages(deck, source, theme, source_id, session)
		child_indexes: dict[str, int] = {}
		for continuation_index, candidate in enumerate(pages):
			page_id = f"{source_id}-p{continuation_index}"
			parent = None
			if continuation_index:
				previous = pages[continuation_index - 1]
				if candidate.kind is slide_lib.layout_primitives.ContinuationKind.AUTHORED and \
						candidate.context is not None and candidate.context.display is \
						slide_lib.layout_primitives.ContinuationContextDisplay.METADATA_ONLY and \
						previous.kind is slide_lib.layout_primitives.ContinuationKind.CONTEXT_HANDOFF:
					parent = f"{source_id}-p{continuation_index - 1}"
				else:
					parent = source_id + "-p0"
			parent_index = 0 if parent is None else child_indexes.get(parent, 0)
			if parent is not None:
				child_indexes[parent] = parent_index + 1
			identity = slide_lib.layout_model.SlideIdentity(page_id, len(physical), source.location,
				parent, parent_index)
			page = _with_page_number(candidate.page, source, theme, continuation_index + 1, len(pages) > 1)
			notes = tuple(slide_lib.layout_model.SpeakerNote(f"{page_id}-note-{note_index}", note.text)
				for note_index, note in enumerate(page.notes))
			physical.append(dataclasses.replace(page, identity=identity, notes=notes,
				continuation_kind=candidate.kind, continuation_context=candidate.context))
	slides = tuple(physical)
	metadata = (slide_lib.layout_model.MetadataEntry("title", deck.title),)
	identity = slide_lib.layout_model.DeckIdentity(deck.path.stem, deck.path)
	result = slide_lib.layout_model.LayoutDeck(identity, slide_lib.layout_primitives.LogicalCanvas(),
		metadata, slides)
	return result

def _compile_source_pages(deck: slide_lib.native_model.Deck, source: slide_lib.native_model.Slide,
		theme: slide_lib.presentation_theme.PresentationTheme, source_id: str,
		session: slide_lib.layout_measurement.MeasurementSession) -> tuple[_PageCandidate, ...]:
	# This is deliberately before the first candidate is built: a continuation
	# must never make an unsupported source fact disappear by omitting it.
	slide_lib.layout_model.reject_unsupported_source_facts(
		slide_lib.layout_measurement.unsupported_facts(source))
	failure: ValueError | None = None
	try:
		result = slide_lib.layout_builders.compile_slide(deck, source, theme, 0, session)
		return (_PageCandidate(result),)
	except ValueError as error:
		failure = error
		contract = layout_contract(source.layout_class)
		if not (deck.paginate and source.paginate):
			raise
	if contract.continuation_policy is slide_lib.layout_primitives.ContinuationPolicy.ALLOW:
		pages = _continuations(deck, source, theme, session)
	elif contract.continuation_policy is slide_lib.layout_primitives.ContinuationPolicy.DECOMPOSE_TO_ONE_PANEL:
		pages = _decompose_grid(deck, source, theme, source_id, session)
	else:
		raise failure
	if not pages:
		if failure is None:
			raise ValueError("continuation preflight failed without a source error")
		raise failure
	return pages

def _decompose_grid(deck: slide_lib.native_model.Deck, source: slide_lib.native_model.Slide,
		theme: slide_lib.presentation_theme.PresentationTheme, source_id: str,
		session: slide_lib.layout_measurement.MeasurementSession) -> tuple[_PageCandidate, ...]:
	contract = layout_contract(source.layout_class)
	units = slide_lib.layout_measurement.grid_stream_units(source, source_id,
		source.layout_class, contract.slot_names)
	if not units:
		return ()
	# The stream retains unit and grid-slot identity through preflight.  It must
	# never become an anonymous one-panel source, because that loses the native
	# object's provenance before the adapters can consume the physical plan.
	pages: list[_PageCandidate] = []
	start = 0
	while start < len(units):
		best: slide_lib.layout_model.LayoutSlide | None = None
		last_end = start
		for end in range(start + 1, len(units) + 1):
			try:
				candidate = slide_lib.layout_builders.compile_grid_stream_page(deck, source,
					units[start:end], theme, 0, session)
			except ValueError:
				break
			best, last_end = candidate, end
		if best is None:
			unit = units[start]
			if isinstance(unit.unit.block, slide_lib.native_model.ListBlock):
				replacements = slide_lib.layout_measurement.descendant_list_units(unit.unit)
				if replacements:
					fragments = tuple(slide_lib.layout_measurement.GridStreamUnit(fragment,
						unit.origin) for fragment in replacements)
					units = units[:start] + fragments + units[start + 1:]
					continue
			block = unit.unit.block
			raise ValueError(f"{block.location.path}:{block.location.line}: one atomic grid stream unit cannot fit within the supported readable minimum of {theme.body_floor_size_pt:g} pt")
		if start:
			best = dataclasses.replace(best, objects=tuple(dataclasses.replace(item,
				origin=slide_lib.layout_primitives.LayoutObjectOrigin.REPEATED_CONTEXT)
				if item.object_id == "title" else item for item in best.objects))
		pages.append(_PageCandidate(best))
		start = last_end
	return tuple(pages)

def _continuations(deck: slide_lib.native_model.Deck, source: slide_lib.native_model.Slide,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession) -> tuple[_PageCandidate, ...]:
	if len(source.cells) != 1:
		return ()
	cell = source.cells[0]
	units = slide_lib.layout_measurement.continuation_units(cell.blocks)
	if not units:
		return ()
	pages: list[_PageCandidate] = []
	start = 0
	while start < len(units):
		best: slide_lib.layout_model.LayoutSlide | None = None
		last_end = start
		low, high = start + 1, len(units)
		while low <= high:
			end = (low + high) // 2
			candidate = _continuation_source(source, cell, units[start:end], start != 0)
			try:
				best = slide_lib.layout_builders.compile_slide(deck, candidate, theme, 0, session)
				last_end = end
				low = end + 1
			except ValueError:
				high = end - 1
		if best is None and isinstance(units[start].block, slide_lib.native_model.ListBlock):
			replacement = slide_lib.layout_measurement.descendant_list_units(units[start])
			if replacement:
				units = units[:start] + replacement + units[start + 1:]
				continue
			handoff = _context_handoff_pages(deck, source, cell, units[start], theme, session)
			if handoff:
				pages.extend(handoff)
				start += 1
				continue
		if best is None:
			unit = units[start].block
			raise ValueError(f"{unit.location.path}:{unit.location.line}: one atomic continuation unit cannot fit within the supported readable minimum of {theme.body_floor_size_pt:g} pt")
		best = slide_lib.layout_measurement.mark_context_paragraphs(best, units[start:last_end])
		if start:
			best = dataclasses.replace(best, objects=tuple(dataclasses.replace(item,
				origin=slide_lib.layout_primitives.LayoutObjectOrigin.REPEATED_CONTEXT)
				if item.object_id == "title" else item for item in best.objects))
		context = slide_lib.layout_measurement.inline_context(best, units[start:last_end])
		kind = slide_lib.layout_primitives.ContinuationKind.AUTHORED if context is not None else \
			slide_lib.layout_primitives.ContinuationKind.NORMAL
		pages.append(_PageCandidate(best, kind, context))
		start = last_end
	return tuple(pages)
def _context_handoff_pages(deck: slide_lib.native_model.Deck,
		source: slide_lib.native_model.Slide, cell: slide_lib.native_model.Cell,
		unit: slide_lib.layout_measurement.ContinuationUnit,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession) -> tuple[_PageCandidate, ...]:
	block = unit.block
	if not isinstance(block, slide_lib.native_model.ListBlock) or len(block.items) != 1:
		return ()
	paths = slide_lib.layout_measurement.list_leaf_paths(block, block.items[0], ())
	if not paths:
		return ()
	pages: list[_PageCandidate] = []
	for path in paths:
		if len(path) < 2:
			return ()
		trail = path[:-1]
		entries = _context_entries(trail)
		leaf_list, leaf_item = path[-1]
		leaf_block = dataclasses.replace(leaf_list, items=(dataclasses.replace(leaf_item,
			children=(), reveal=leaf_item.reveal),), reveal=None)
		leaf_source = _continuation_source(source, cell,
			(slide_lib.layout_measurement.ContinuationUnit(leaf_block, unit.active_heading),), True)
		# Diagnose an unsplittable leaf before testing whether its static trail fits.
		authored = slide_lib.layout_builders.compile_slide(deck, leaf_source, theme, 0, session)
		metadata = slide_lib.layout_model.ContinuationContext(
			slide_lib.layout_primitives.ContinuationContextDisplay.METADATA_ONLY, entries)
		trail_block = slide_lib.layout_measurement.path_fragment(trail)
		trail_source = _continuation_source(source, cell,
			(slide_lib.layout_measurement.ContinuationUnit(trail_block, unit.active_heading),), True)
		try:
			handoff = slide_lib.layout_builders.compile_slide(deck, trail_source, theme, 0, session)
		except ValueError:
			pages.append(_PageCandidate(authored,
				slide_lib.layout_primitives.ContinuationKind.AUTHORED, metadata))
			continue
		static = slide_lib.layout_model.ContinuationContext(
			slide_lib.layout_primitives.ContinuationContextDisplay.HANDOFF_STATIC, entries)
		handoff = slide_lib.layout_measurement.mark_context_paragraphs(handoff, (
			slide_lib.layout_measurement.ContinuationUnit(trail_block, unit.active_heading,
				len(trail), tuple(item.location for _list, item in trail)),))
		handoff = dataclasses.replace(handoff, objects=tuple(dataclasses.replace(item,
			origin=slide_lib.layout_primitives.LayoutObjectOrigin.REPEATED_CONTEXT)
			for item in handoff.objects))
		pages.extend((_PageCandidate(handoff,
			slide_lib.layout_primitives.ContinuationKind.CONTEXT_HANDOFF, static),
			_PageCandidate(authored, slide_lib.layout_primitives.ContinuationKind.AUTHORED, metadata)))
	return tuple(pages)


def _context_entries(path: tuple[tuple[slide_lib.native_model.ListBlock,
		slide_lib.native_model.ListItem], ...]) -> tuple[slide_lib.layout_model.ContinuationContextEntry, ...]:
	"""Resolve every outer-to-inner ancestor once, independently of frame capacity."""
	entries: list[slide_lib.layout_model.ContinuationContextEntry] = []
	for level, (list_block, item) in enumerate(path):
		inlines = slide_lib.layout_builders.resolved_runs(item.inlines,
			slide_lib.layout_builders.FOREGROUND)
		if not inlines:
			raise ValueError(f"{item.location.path}:{item.location.line}: list context item has no text")
		entries.append(slide_lib.layout_model.ContinuationContextEntry(inlines,
			slide_lib.layout_primitives.ListKind.ORDERED if list_block.ordered else
				slide_lib.layout_primitives.ListKind.UNORDERED,
			level, list_block.start, item.location))
	return tuple(entries)
def _continuation_source(source: slide_lib.native_model.Slide, cell: slide_lib.native_model.Cell,
		units: tuple[slide_lib.layout_measurement.ContinuationUnit, ...], continuation: bool) -> slide_lib.native_model.Slide:
	blocks: list[slide_lib.native_model.Block] = []
	active_heading = units[0].active_heading
	if active_heading is not None:
		blocks.append(dataclasses.replace(active_heading, reveal=None) if continuation else active_heading)
	for unit in units:
		if isinstance(unit.block, slide_lib.native_model.Table) and blocks and \
				isinstance(blocks[-1], slide_lib.native_model.Table) and \
				blocks[-1].location == unit.block.location:
			previous = blocks[-1]
			if not isinstance(previous, slide_lib.native_model.Table):
				raise ValueError("continuation table aggregation requires a preceding table")
			blocks[-1] = dataclasses.replace(previous, rows=previous.rows + unit.block.rows)
		else:
			blocks.append(unit.block)
	source_blocks = tuple(
		dataclasses.replace(block, reveal=None) if continuation and
		isinstance(block, slide_lib.native_model.Heading) and block.level == 1 else block
		for block in source.blocks)
	return dataclasses.replace(source, blocks=source_blocks,
		cells=(dataclasses.replace(cell, blocks=tuple(blocks)),))
def _with_page_number(page: slide_lib.layout_model.LayoutSlide, source: slide_lib.native_model.Slide,
		theme: slide_lib.presentation_theme.PresentationTheme, number: int,
		is_continued: bool) -> slide_lib.layout_model.LayoutSlide:
	if not source.paginate or not is_continued:
		return page
	typography = slide_lib.layout_primitives.Typography(slide_lib.layout_primitives.StyleRole.MUTED,
		"OpenDyslexic", 18.0, 18.0, 18.0)
	inlines = (slide_lib.native_model.Text(str(number)),)
	properties = slide_lib.layout_measurement.paragraph_properties(
		inlines, 18.0, 62.0, theme, terminal=True)
	properties = dataclasses.replace(properties,
		horizontal_alignment=slide_lib.layout_primitives.HorizontalAlignment.END)
	content = slide_lib.layout_content.TextContent((slide_lib.layout_content.TextParagraph((
		slide_lib.layout_content.TextRun(str(number), slide_lib.layout_content.RunStyle("OpenDyslexic", "526176")),
	), typography, properties),))
	frame = slide_lib.layout_primitives.FrameTextProperties(slide_lib.layout_primitives.Insets(0, 0, 0, 0),
		slide_lib.layout_primitives.VerticalAlignment.TOP, slide_lib.layout_primitives.TextWrap.WRAP,
		slide_lib.layout_primitives.TextDirection.HORIZONTAL, slide_lib.layout_primitives.OverflowPolicy.SHRINK)
	object_id = "page-number"
	page_number = slide_lib.layout_model.LayoutObject(object_id,
		slide_lib.layout_primitives.PresentationRole.CONTENT, slide_lib.layout_primitives.StyleRole.MUTED,
		slide_lib.layout_primitives.LogicalRectangle(1190, 762, 62, 22),
		slide_lib.layout_primitives.ObjectLayer.DECORATION, len(page.objects), len(page.objects), content,
		frame, None, None, slide_lib.layout_primitives.PlaceholderKind.NONE, source.location,
		origin=slide_lib.layout_primitives.LayoutObjectOrigin.GENERATED_CHROME)
	return dataclasses.replace(page, objects=page.objects + (page_number,))
