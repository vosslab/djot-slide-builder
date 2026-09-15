"""Compile one immutable physical slide for each visible source slide."""

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
	"""Compile visible authored slides once, retaining their physical source locations."""
	visible_slides = tuple(source for source in deck.slides if not source.hidden)
	if not visible_slides:
		raise ValueError(f"{deck.path}:1: deck has no visible slides")
	session = slide_lib.layout_measurement.MeasurementSession(theme)
	slides: list[slide_lib.layout_model.LayoutSlide] = []
	for index, source in enumerate(visible_slides):
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
		(slide_lib.layout_model.MetadataEntry("title", deck.title),
			slide_lib.layout_model.MetadataEntry("color-theme", deck.color_theme)), tuple(slides))
	return slide_lib.compilation_result.CompilationResult(plan, tuple(session.capacity_diagnostics))
