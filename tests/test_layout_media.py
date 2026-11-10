"""Image and question layout contracts for containment, captions, and mixed content."""

import pathlib

import PIL.Image
import pytest

import slide_lib.capacity_report
import slide_lib.layout_content
import slide_lib.layout_primitives
import slide_lib.presentation_theme
import layout_test_helpers


def test_movie_panel_gives_text_the_space_left_of_a_portrait_poster(tmp_path: pathlib.Path) -> None:
	"""Movie descriptions stay editable beside a narrower, uncropped 2:3 poster."""
	PIL.Image.new("RGB", (120, 180), "navy").save(tmp_path / "poster.png")
	source = ("=== layout: movie-panel\n\n# Movie (2026)\n\n@body\n\n"
		"Original plot and review wording.\n\n@poster\n\n![Poster](poster.png)\n")
	slide = layout_test_helpers.compile_source(tmp_path, source).plan.slides[0]
	body = next(slot for slot in slide.slots if slot.slot_id == "body")
	poster = next(slot for slot in slide.slots if slot.slot_id == "poster")
	assert body.rectangle.width > poster.rectangle.width
	assert body.rectangle.x + body.rectangle.width < poster.rectangle.x
	assert poster.rectangle.width / poster.rectangle.height == pytest.approx(2 / 3)
	text = next(item.content for item in slide.objects
		if item.slot_id == "body" and isinstance(item.content, slide_lib.layout_content.TextContent))
	assert "".join(run.text for run in text.paragraphs[0].inlines) == "Original plot and review wording."
	picture = next(item for item in slide.objects
		if isinstance(item.content, slide_lib.layout_content.PictureContent))
	assert picture.rectangle == poster.rectangle
	with pytest.raises(ValueError, match="poster requires exactly one component image"):
		layout_test_helpers.compile_source(tmp_path,
			source.replace("![Poster](poster.png)", "Poster description"))


def test_prompt_supplies_emphasis_and_readable_examples_without_color_markup(
		tmp_path: pathlib.Path) -> None:
	"""Icebreakers retain their prompt/examples hierarchy and editable text."""
	slide = layout_test_helpers.compile_source(tmp_path, """=== layout: prompt

# Icebreaker

@prompt

Is a hot dog a sandwich? Is ice cream a soup?

@examples

State your name, major, and post-grad plans.

- Pick one and defend your rule: ingredients, shape, temperature, or how it is eaten.
- Examples: "A sandwich needs two slices." "Ice cream becomes soup when it melts!"
""").plan.slides[0]
	prompt = next(item for item in slide.objects if item.slot_id == "prompt")
	examples = next(item for item in slide.objects if item.slot_id == "examples")
	assert isinstance(prompt.content, slide_lib.layout_content.TextContent)
	assert isinstance(examples.content, slide_lib.layout_content.TextContent)
	assert all(run.style.foreground == "7B1E2B" and run.style.bold
		for paragraph in prompt.content.paragraphs for run in paragraph.inlines
		if isinstance(run, slide_lib.layout_content.TextRun))
	assert all(run.style.foreground == "333333"
		for paragraph in examples.content.paragraphs for run in paragraph.inlines
		if isinstance(run, slide_lib.layout_content.TextRun))
	assert prompt.content.paragraphs[0].typography.selected_size_pt > \
		examples.content.paragraphs[0].typography.selected_size_pt >= \
		slide_lib.presentation_theme.default_theme().body_floor_size_pt
	assert prompt.rectangle.y + prompt.rectangle.height <= examples.rectangle.y
	assert not prompt.reveal_targets and not examples.reveal_targets


def test_question_ask_is_one_editable_centered_question_without_examples(tmp_path: pathlib.Path) -> None:
	"""A lesson pause remains a single question rather than inheriting the icebreaker contract."""
	question = "Given Ss Yy Aa, what gametes are possible?"
	slide = layout_test_helpers.compile_source(tmp_path,
		f"=== layout: question-ask\n\n# {question}\n").plan.slides[0]
	text = [item for item in slide.objects
		if isinstance(item.content, slide_lib.layout_content.TextContent)]
	assert len(text) == 1
	paragraph = text[0].content.paragraphs[0]
	assert "".join(run.text for run in paragraph.inlines) == question
	assert paragraph.properties.horizontal_alignment is slide_lib.layout_primitives.HorizontalAlignment.CENTER
	assert all(run.style.foreground == "7B1E2B" for run in paragraph.inlines)
	assert not text[0].reveal_targets
	with pytest.raises(ValueError, match="subtitle"):
		layout_test_helpers.compile_source(tmp_path,
			f"=== layout: question-ask\n\n# {question}\n\n## Supporting examples\n")


def test_prompt_requires_supporting_examples(tmp_path: pathlib.Path) -> None:
	"""An icebreaker cannot silently regress to a question with empty supporting space."""
	with pytest.raises(ValueError, match="visible examples or suggestions"):
		layout_test_helpers.compile_source(tmp_path,
			"=== layout: prompt\n@prompt\nWhat is your sorting rule?\n@examples\n")


def test_multiple_choice_reserves_the_answer_popup_from_each_visible_choice(
		tmp_path: pathlib.Path) -> None:
	"""A text-only question uses the shared adaptive choice geometry before reveal."""
	result = layout_test_helpers.compile_source(tmp_path, """=== layout: multiple-choice

@question

Which statement best describes this teaching example?

- A) It identifies one observation.
- B) It compares two related observations.
- C) It explains why the observations matter.
- D) It asks learners to connect the observations to the underlying principle.

@answer

Answer: D
""")
	objects = result.plan.slides[0].objects
	answer = next(item for item in objects if item.object_id == "answer")
	choices = tuple(item for item in objects if item.object_id.startswith("question-choices-"))
	assert choices and all(isinstance(item.content, slide_lib.layout_content.TextContent)
		for item in choices)
	assert all(choice.rectangle.x + choice.rectangle.width <= answer.rectangle.x or
		answer.rectangle.x + answer.rectangle.width <= choice.rectangle.x or
		choice.rectangle.y + choice.rectangle.height <= answer.rectangle.y or
		answer.rectangle.y + answer.rectangle.height <= choice.rectangle.y
	for choice in choices)


def test_big_image_keeps_one_focal_image_above_a_full_width_caption(tmp_path: pathlib.Path) -> None:
	"""The image-focus layout preserves its editable image and caption contract."""
	layout_test_helpers.write_image(tmp_path, "focal.png")
	slide = layout_test_helpers.compile_source(tmp_path, """=== layout: big-image

@image

![Focal image](focal.png)

@caption

Short editable caption.
""").plan.slides[0]
	picture = next(item for item in slide.objects
		if isinstance(item.content, slide_lib.layout_content.PictureContent))
	caption = next(item for item in slide.objects if item.object_id == "caption")
	assert isinstance(caption.content, slide_lib.layout_content.TextContent)
	assert picture.rectangle.x == caption.rectangle.x
	assert picture.rectangle.width == caption.rectangle.width
	assert picture.rectangle.y + picture.rectangle.height < caption.rectangle.y
	assert caption.rectangle.y + caption.rectangle.height < \
		slide_lib.presentation_theme.LOGICAL_SLIDE_HEIGHT


def test_big_image_long_caption_grows_downward_without_moving_image_or_covering_citation(tmp_path: pathlib.Path) -> None:
	"""Forecast paragraphs can use the free lower margin while cited slides retain their footer."""
	layout_test_helpers.write_image(tmp_path, "focal.png")
	caption = ("Some may see intermittent light showers or sprinkles during trick or treating hours tonight. "
		"Seasonably mild temps and mostly cloudy skies will then follow into early next week. "
		"The highest chances of rain are expected towards mid-week.")
	prefix = "=== layout: big-image\n@image\n![Weather](focal.png)\n@caption\n"
	short = layout_test_helpers.compile_source(tmp_path, prefix + "Short caption.").plan.slides[0]
	long = layout_test_helpers.compile_source(tmp_path, prefix + caption).plan.slides[0]
	cited = layout_test_helpers.compile_source(tmp_path, prefix + caption + "\n\n@citation\nSource: https://example.test/weather").plan.slides[0]
	pictures = [next(item for item in slide.objects if item.object_id == "big-image") for slide in (short, long, cited)]
	captions = [next(item for item in slide.objects if item.object_id == "caption") for slide in (short, long, cited)]
	assert pictures[0].rectangle == pictures[1].rectangle == pictures[2].rectangle
	assert pictures[0].content.placement == pictures[1].content.placement == pictures[2].content.placement
	assert captions[0].rectangle.y == captions[1].rectangle.y == captions[2].rectangle.y
	assert captions[1].rectangle.height > captions[0].rectangle.height == captions[2].rectangle.height
	assert captions[1].rectangle.y + captions[1].rectangle.height < slide_lib.presentation_theme.LOGICAL_SLIDE_HEIGHT
	footer = next(item for item in cited.objects if item.object_id == "citation")
	assert captions[2].rectangle.y + captions[2].rectangle.height <= footer.rectangle.y
	assert captions[1].content.paragraphs[0].typography.selected_size_pt > \
		captions[2].content.paragraphs[0].typography.selected_size_pt


@pytest.mark.parametrize("label", (
	"## Cis isomer: The two Xs are on the same side.",
	"Cis isomer: The two Xs are on the same side.",
	"- Cis isomer: The two Xs are on the same side.",
))
def test_region_text_and_images_share_size_selection(tmp_path: pathlib.Path, label: str) -> None:
	"""Local headings compete with images rather than reserving their preferred size first."""
	PIL.Image.new("RGB", (225, 155), "blue").save(tmp_path / "diagram.png")
	result = layout_test_helpers.compile_source(tmp_path, "=== layout: two-over-one-panels\n\n# Topic\n\n"
		f"@top-left\n\n{label}\n\n![Diagram](diagram.png)\n\n"
		"@top-right\n\nOther comparison\n\n@bottom\n\nExplanation\n")
	page = result.plan.slides[0]
	text = next(item for item in page.objects if item.slot_id == "top-left"
		and isinstance(item.content, slide_lib.layout_content.TextContent))
	picture = next(item for item in page.objects if item.slot_id == "top-left"
		and isinstance(item.content, slide_lib.layout_content.PictureContent))
	theme = slide_lib.presentation_theme.default_theme()
	font = text.content.paragraphs[0].typography.selected_size_pt
	assert theme.body_floor_size_pt <= font < theme.ordinary_body_size_pt
	assert text.rectangle.y + text.rectangle.height <= picture.rectangle.y
	if label.startswith("##"):
		assert text.style_role is slide_lib.layout_primitives.StyleRole.LOCAL_HEADING
		assert all(run.style.bold for run in text.content.paragraphs[0].inlines
			if isinstance(run, slide_lib.layout_content.TextRun))


def test_region_heading_table_and_image_share_one_allocation(tmp_path: pathlib.Path) -> None:
	PIL.Image.new("RGB", (300, 120), "blue").save(tmp_path / "diagram.png")
	result = layout_test_helpers.compile_source(tmp_path, "=== layout: one-panel\n\n# Topic\n\n@body\n\n"
		"## Local heading\n\n| Sample | Value |\n| --- | --- |\n| A | 1 |\n\n![Diagram](diagram.png)\n")
	objects = [item for item in result.plan.slides[0].objects if item.slot_id == "body"]
	assert [type(item.content) for item in objects] == [
		slide_lib.layout_content.TextContent, slide_lib.layout_content.TableContent,
		slide_lib.layout_content.PictureContent]
	heading, table, image = objects
	assert heading.content.paragraphs[0].typography.selected_size_pt == \
		table.content.header_rows[0].cells[0].paragraphs[0].typography.selected_size_pt
	assert heading.rectangle.y + heading.rectangle.height <= table.rectangle.y
	assert table.rectangle.y + table.rectangle.height <= image.rectangle.y


def test_mixed_images_scale_independently_and_preserve_geometry(tmp_path: pathlib.Path) -> None:
	"""Width scoring preserves source order/aspects while allowing different image widths."""
	PIL.Image.new("RGB", (1000, 200), "blue").save(tmp_path / "wide.png")
	PIL.Image.new("RGB", (1000, 350), "green").save(tmp_path / "diagram.png")
	source = ("=== layout: one-panel\n@body\n![Question](wide.png)\n\n"
		"- How many different ways can we arrange the offspring?\n\n![Diagram](diagram.png)\n")
	result = layout_test_helpers.compile_source(tmp_path, source)
	page = result.plan.slides[0]
	assert not result.capacity_diagnostics
	assert [type(item.content) for item in page.objects] == [
		slide_lib.layout_content.PictureContent, slide_lib.layout_content.TextContent,
		slide_lib.layout_content.PictureContent]
	pictures = [item.content.placement.displayed_rectangle for item in page.objects
		if isinstance(item.content, slide_lib.layout_content.PictureContent)]
	assert pictures[0].width != pytest.approx(pictures[1].width)
	assert pictures[0].width / pictures[0].height == pytest.approx(5)
	assert pictures[1].width / pictures[1].height == pytest.approx(1000 / 350)
	body = page.slots[0].rectangle
	assert all(item.rectangle.y >= body.y and
		item.rectangle.y + item.rectangle.height <= body.y + body.height + 1e-8
		for item in page.objects)


def test_mixed_content_starvation_requires_replacement_and_split(tmp_path: pathlib.Path) -> None:
	"""An image cannot silently collapse to accommodate an otherwise representable text block."""
	PIL.Image.new("RGB", (1000, 250), "blue").save(tmp_path / "question.png")
	source = ("=== layout: one-panel\n@body\n![Question](question.png)\n\n" +
		"\n".join("- " + "offspring probability " * 7 for _ in range(16)) + "\n")
	result = layout_test_helpers.compile_source(tmp_path, source)
	diagnostic = next(item for item in result.capacity_diagnostics
		if item.cause is slide_lib.capacity_report.CapacityCause.MIXED_READABILITY)
	assert "@replaceme" in diagnostic.message() and "Split" in diagnostic.message()
	assert "split" in slide_lib.capacity_report.format_diagnostic(diagnostic, tmp_path)
	page = result.plan.slides[0]
	assert page.objects[-1].object_id == "replaceme-watermark"
	assert any("Split" in note.text for note in page.notes)
	assert (tmp_path / "specimen.djot").read_text() == source
	marked = layout_test_helpers.compile_source(tmp_path, source.replace("\n", "\n@replaceme\n", 1))
	assert sum(item.object_id == "replaceme-watermark" for item in marked.plan.slides[0].objects) == 1
