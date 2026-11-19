"""Compiler contracts for source preservation, capacity diagnostics, and teaching layouts."""

import pathlib

import pytest

import slide_lib.layout_size_selection
import slide_lib.capacity_report
import slide_lib.layout_content
import slide_lib.layout_engine
import slide_lib.layout_measurement
import slide_lib.layout_primitives
import slide_lib.native_model
import slide_lib.presentation_theme
import layout_test_helpers


#============================================
def test_hidden_source_is_compiled_and_retains_hidden_state(tmp_path: pathlib.Path) -> None:
	"""Hidden pages keep their source order and native hidden metadata."""
	source = ("=== layout: title-only\nhidden: true\n\n# Optional\n"
		"=== layout: title-only\n\n# Teaching\n"
		"=== layout: title-only\nhidden: false\n\n# Closing\n")
	deck = layout_test_helpers.parsed_source(tmp_path, source)
	result = slide_lib.layout_engine.compile_layout_deck(
		deck, slide_lib.presentation_theme.default_theme())
	assert deck.title == "Teaching" and deck.slides[0].blocks[0].inlines[0].value == "Optional"
	assert tuple(page.identity.source for page in result.plan.slides) == \
		tuple(slide.location for slide in deck.slides)
	assert tuple(page.hidden for page in result.plan.slides) == (True, False, False)


#============================================
def test_all_hidden_deck_has_no_classroom_output(tmp_path: pathlib.Path) -> None:
	"""A retained source-only deck gets a clear diagnostic instead of an empty export."""
	with pytest.raises(ValueError, match="deck has no visible slides"):
		layout_test_helpers.compile_source(tmp_path, "=== layout: blank\nhidden: true\n")


#============================================
@pytest.mark.parametrize("layout, slots", (("one-panel", ("body",)), ("two-panels", ("left", "right"))))
def test_overfull_representable_slide_stays_one_page_and_reports_capacity(
		tmp_path: pathlib.Path, layout: str, slots: tuple[str, ...]) -> None:
	long = "word " * 500
	regions = "".join(f"\n@{slot}\n\n{long}" for slot in slots)
	result = layout_test_helpers.compile_source(tmp_path, f"=== layout: {layout}\n{regions}")
	assert len(result.plan.slides) == 1
	diagnostic = result.capacity_diagnostics[0]
	assert diagnostic.location.path.name == "specimen.djot"
	assert diagnostic.layout == layout and diagnostic.slot in slots
	assert diagnostic.location.line > 0 and diagnostic.required_size_pt < diagnostic.floor_size_pt
	assert diagnostic.cause is slide_lib.capacity_report.CapacityCause.PARAGRAPH_LIST


#============================================
def test_impossible_content_reports_its_source_location(tmp_path: pathlib.Path) -> None:
	table = "| A |\n| - |\n" + "| word |\n" * 100
	with pytest.raises(slide_lib.capacity_report.PhysicalCapacityError,
			match=r"specimen\.djot:5: one-panel/body cannot fit at the 1 pt serializer-safe minimum") as raised:
		layout_test_helpers.compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\n" + table)
	assert raised.value.diagnostic.cause is slide_lib.capacity_report.CapacityCause.TABLE
	assert raised.value.diagnostic.required_size_pt is None


#============================================
def test_definitions_style_terms_without_styling_explanations_or_examples(tmp_path: pathlib.Path) -> None:
	"""Plain term syntax and existing bold terms receive automatic bold and underline."""
	page = layout_test_helpers.compile_source(tmp_path, "=== layout: definitions\n# Definitions\n@body\n"
		"- Parental type: same allele combination.\n  - An example.\n"
		"- *Recombinant type* - different allele combination.\n").plan.slides[0]
	paragraphs = [paragraph for item in page.objects
		if isinstance(item.content, slide_lib.layout_content.TextContent)
		and item.slot_id == "body" for paragraph in item.content.paragraphs]
	runs = [run for paragraph in paragraphs for run in paragraph.inlines
		if isinstance(run, slide_lib.layout_content.TextRun)]
	terms = [run for run in runs if run.text in ("Parental type", "Recombinant type")]
	assert len(terms) == 2 and all(run.style.bold and run.style.underline for run in terms)
	assert all(not run.style.bold and not run.style.underline for run in runs if run not in terms)


#============================================
def test_definitions_reject_missing_term_boundaries(tmp_path: pathlib.Path) -> None:
	"""Malformed entries must identify how to supply a term rather than silently look ordinary."""
	with pytest.raises(ValueError, match="Term: explanation"):
		layout_test_helpers.compile_source(tmp_path, "=== layout: definitions\n@body\n- No term separator\n")
