"""Compile one immutable physical slide for each source slide."""

import dataclasses

import slide_lib.capacity_report
import slide_lib.citation_layout
import slide_lib.compilation_result
import slide_lib.layout_builders
import slide_lib.layout_measurement
import slide_lib.layout_model
import slide_lib.layout_primitives
import slide_lib.layout_specialty_builders
import slide_lib.math_layout
import slide_lib.math_render
import slide_lib.native_model
import slide_lib.presentation_theme


def compile_layout_deck(deck: slide_lib.native_model.Deck,
		theme: slide_lib.presentation_theme.PresentationTheme) -> slide_lib.compilation_result.CompilationResult:
	"""Compile every authored slide once and retain each page's hidden state."""
	if not any(not source.hidden for source in deck.slides):
		raise ValueError(f"{deck.path}:1: deck has no visible slides")
	deck = dataclasses.replace(deck, slides=tuple(
		slide_lib.math_render.lower_display_math(source) for source in deck.slides))
	session = slide_lib.layout_measurement.MeasurementSession(theme)
	session.prepare_equations(deck)
	session.prepare_table_groups(deck)
	slides: list[slide_lib.layout_model.LayoutSlide] = []
	for index, source in enumerate(deck.slides):
		diagnostic_start = len(session.capacity_diagnostics)
		slide_lib.layout_model.reject_unsupported_source_facts(
			slide_lib.layout_measurement.unsupported_facts(source))
		page = slide_lib.layout_builders.compile_slide(deck, source, theme, index, session)
		page = slide_lib.citation_layout.add_citation(page, source, theme, session)
		page = dataclasses.replace(page, objects=tuple(
			slide_lib.math_layout.finalize_object(item, session) for item in page.objects))
		title = next((slide_lib.layout_measurement.visible_text(block.inlines)
			for block in source.blocks if isinstance(block, slide_lib.native_model.Heading)), "")
		for diagnostic_index in range(diagnostic_start, len(session.capacity_diagnostics)):
			session.capacity_diagnostics[diagnostic_index] = dataclasses.replace(
				session.capacity_diagnostics[diagnostic_index], slide_number=index + 1,
				slide_title=title)
		replacement_diagnostics = tuple(diagnostic for diagnostic in
			session.capacity_diagnostics[diagnostic_start:]
			if diagnostic.cause is slide_lib.capacity_report.CapacityCause.MIXED_READABILITY)
		if source.replaceme or replacement_diagnostics:
			order = max((item.reading_order for item in page.objects), default=-1) + 1
			z_index = max((item.z_index for item in page.objects), default=-1) + 1
			watermark = slide_lib.layout_specialty_builders.replaceme_watermark(
				source, theme, order, z_index, session)
			page = dataclasses.replace(page, objects=(*page.objects, watermark))
		if replacement_diagnostics:
			page = dataclasses.replace(page, notes=(*page.notes, *(
				slide_lib.layout_model.SpeakerNote(f"replacement-{number}", diagnostic.message())
				for number, diagnostic in enumerate(replacement_diagnostics))))
		identity = slide_lib.layout_model.SlideIdentity(f"slide-{index + 1}", index, source.location)
		notes = tuple(slide_lib.layout_model.SpeakerNote(
			f"slide-{index + 1}-note-{note_index}", note_index and note.text or note.text)
			for note_index, note in enumerate(page.notes))
		slides.append(dataclasses.replace(page, identity=identity, notes=notes, hidden=source.hidden))
	plan = slide_lib.layout_model.LayoutDeck(
		slide_lib.layout_model.DeckIdentity(deck.path.stem, deck.path),
		slide_lib.layout_primitives.LogicalCanvas(),
		(slide_lib.layout_model.MetadataEntry("title", deck.title),
			slide_lib.layout_model.MetadataEntry("color-theme", deck.color_theme)), tuple(slides))
	return slide_lib.compilation_result.CompilationResult(plan, tuple(session.capacity_diagnostics))
