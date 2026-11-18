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

#============================================
@pytest.mark.parametrize("source", (
	"=== layout: one-panel\n# Content\n@body\n=> appear\nKeep this editable.\n",
	"=== layout: section\n# Red surface\n",
	"=== layout: blank\n",
))
def test_replaceme_adds_visible_editable_warning_without_changing_content(
		tmp_path: pathlib.Path, source: str) -> None:
	"""Review overlays preserve layout geometry and stay above images, text, and reveals."""
	ordinary = layout_test_helpers.compile_source(tmp_path, source).plan.slides[0]
	marked = layout_test_helpers.compile_source(tmp_path, source.replace("\n", "\n@replaceme\n", 1)).plan.slides[0]
	watermark = marked.objects[-1]
	assert marked.slots == ordinary.slots
	assert tuple((item.rectangle, item.content, item.reveal_targets) for item in marked.objects[:-1]) == \
		tuple((item.rectangle, item.content, item.reveal_targets) for item in ordinary.objects)
	assert all(watermark.z_index > item.z_index for item in ordinary.objects)
	assert watermark.content.text.paragraphs[0].inlines[0].text == "REPLACE ME"
	assert watermark.content.text.paragraphs[0].inlines[0].style.foreground == \
		slide_lib.presentation_theme.resolve_text_color("red", "24578F")
	assert watermark.content.style.fill_role is not None and not watermark.reveal_targets


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
def test_title_only_body_uses_ordinary_source_ordered_objects(tmp_path: pathlib.Path) -> None:
	"""Title Only retains its one title member while body content remains native objects."""
	layout_test_helpers.write_image(tmp_path, "component.png")
	result = layout_test_helpers.compile_source(
		tmp_path,
		"=== layout: title-only\n\n# Title\n\nParagraph.\n\n"
		"- First\n- Second\n\n![Tall](component.png)",
	)
	slide = result.plan.slides[0]
	assert slide.layout.topology.libreoffice_layout.autolayout is \
		slide_lib.layout_primitives.LibreOfficeAutoLayout.TITLE_ONLY
	assert tuple(slot.placeholder_kind for slot in slide.slots) == \
		(slide_lib.layout_primitives.PlaceholderKind.TITLE, slide_lib.layout_primitives.PlaceholderKind.NONE)
	assert slide.objects[0].placeholder_kind is slide_lib.layout_primitives.PlaceholderKind.TITLE
	body_objects = tuple(item for item in slide.objects[1:] if item.object_id != "replaceme-watermark")
	assert tuple(type(item.content) for item in body_objects) == \
		(slide_lib.layout_content.TextContent, slide_lib.layout_content.TextContent,
			slide_lib.layout_content.PictureContent)
	assert all(item.placeholder_kind is slide_lib.layout_primitives.PlaceholderKind.NONE
		for item in body_objects)
	title = slide.objects[0]
	assert all(item.rectangle.y > title.rectangle.y + title.rectangle.height for item in body_objects)


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

#============================================
def test_unsupported_source_still_fails_at_the_validation_boundary(tmp_path: pathlib.Path) -> None:
	with pytest.raises(ValueError, match=r"specimen\.djot:5: CodeBlock has no physical projection"):
		layout_test_helpers.compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\n```\ncode\n```")


#============================================

#============================================

#============================================

#============================================

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


#============================================
def test_multiple_choice_keeps_figure_and_choices_visible_before_answer(tmp_path: pathlib.Path) -> None:
	"""A diagram question keeps readable context while revealing only its wrapped answer."""
	(tmp_path / "tree.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" '
		'width="1126" height="757"><path d="M20 20V700H1100"/></svg>')
	result = layout_test_helpers.compile_source(tmp_path,
		"=== layout: multiple-choice\n@question\n![Tree](tree.svg)\n\nWhich pair shares the youngest ancestor?\n\n"
		"- A. Gorilla and human\n- B. Gibbon and gorilla\n- C. Bonobo and gorilla\n- D. Bonobo and human\n\n"
		"@answer\n\nD. Bonobo and human: shared ancestor 5 million years ago.\n")
	page = result.plan.slides[0]
	image = next(item for item in page.objects if item.object_id == "question-image")
	answer = next(item for item in page.objects if item.object_id == "answer")
	assert image.rectangle.height > 300
	assert answer.reveal_targets and all(not item.reveal_targets for item in page.objects if item is not answer)
	choices = [item for item in page.objects if item.object_id.startswith("question-choices-")]
	assert sum(len(item.content.paragraphs) for item in choices) == 4
	assert all(paragraph.typography.selected_size_pt >= 20 for item in choices
		for paragraph in item.content.paragraphs)
	assert any(isinstance(run, slide_lib.layout_content.LineBreak)
		for paragraph in answer.content.text.paragraphs for run in paragraph.inlines)
