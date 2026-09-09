"""Compile one immutable physical slide for each validated source slide."""

import dataclasses

import slide_lib.compilation_result
import slide_lib.layout_builders
import slide_lib.layout_measurement
import slide_lib.layout_model
import slide_lib.layout_primitives
import slide_lib.native_model
import slide_lib.presentation_theme


def compile_layout_deck(deck: slide_lib.native_model.Deck,
		theme: slide_lib.presentation_theme.PresentationTheme) -> slide_lib.compilation_result.CompilationResult:
	"""Compile every authored slide once, preserving source order and identity."""
	session = slide_lib.layout_measurement.MeasurementSession(theme)
	slides: list[slide_lib.layout_model.LayoutSlide] = []
	for index, source in enumerate(deck.slides):
		slide_lib.layout_model.reject_unsupported_source_facts(
			slide_lib.layout_measurement.unsupported_facts(source))
		page = slide_lib.layout_builders.compile_slide(deck, source, theme, index, session)
		identity = slide_lib.layout_model.SlideIdentity(f"slide-{index + 1}", index, source.location)
		notes = tuple(slide_lib.layout_model.SpeakerNote(
			f"slide-{index + 1}-note-{note_index}", note_index and note.text or note.text)
			for note_index, note in enumerate(page.notes))
		slides.append(dataclasses.replace(page, identity=identity, notes=notes))
	plan = slide_lib.layout_model.LayoutDeck(
		slide_lib.layout_model.DeckIdentity(deck.path.stem, deck.path),
		slide_lib.layout_primitives.LogicalCanvas(),
		(slide_lib.layout_model.MetadataEntry("title", deck.title),), tuple(slides))
	return slide_lib.compilation_result.CompilationResult(plan, tuple(session.capacity_diagnostics))
