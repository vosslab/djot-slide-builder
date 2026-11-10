"""Text layout contracts for readable links, citations, and content-preserving wrapping."""

import pathlib

import pytest

import slide_lib.djot_audit
import slide_lib.layout_content
import slide_lib.layout_measurement
import slide_lib.layout_object_builders
import slide_lib.layout_primitives
import slide_lib.native_model
import slide_lib.presentation_theme
import layout_test_helpers


def test_code_and_literal_links_use_their_semantic_font_roles(tmp_path: pathlib.Path) -> None:
	"""Code stays monospace while literal URLs receive the approved narrow face."""
	result = layout_test_helpers.compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\n"
		"Words `ATGC` [https://example.test](https://example.test) "
		"[`ATGC`](https://example.test)\n")
	paragraph = result.plan.slides[0].objects[0].content.paragraphs[0]
	runs = [run for run in paragraph.inlines
		if isinstance(run, slide_lib.layout_content.TextRun) and run.text.strip()]
	assert [(run.text.strip(), run.style.font_family) for run in runs] == [
		("Words", "Atkinson Hyperlegible Next"), ("ATGC", "Atkinson Hyperlegible Mono"),
		("https://example.test", "IBM Plex Sans Condensed"),
		("ATGC", "Atkinson Hyperlegible Mono")]
	assert all(run.style.underline for run in runs if run.style.link_url)


def test_visible_url_shrinks_independently_without_splitting(tmp_path: pathlib.Path) -> None:
	"""Long addresses keep their destination and use their own readable size."""
	url = "https://crossidiomas.com/build-the-plane-while-flying-it/"
	result = layout_test_helpers.compile_source(tmp_path, "=== layout: two-panels\n\n@left\n\n"
		f"[{url}]({url})\n\n@right\n\nImage placeholder\n")
	paragraph = result.plan.slides[0].objects[0].content.paragraphs[0]
	runs = [run for run in paragraph.inlines
		if isinstance(run, slide_lib.layout_content.TextRun)]
	assert len(runs) == 1
	assert "".join(run.text for run in runs) == url
	assert all(run.style.link_url == url for run in runs)
	assert 12 <= runs[0].style.size_pt < paragraph.typography.selected_size_pt
	session = slide_lib.layout_measurement.MeasurementSession(slide_lib.presentation_theme.default_theme())
	assert session.advance(runs[0].style.font_family, False, False, runs[0].style.size_pt,
		url) < result.plan.slides[0].objects[0].rectangle.width


def test_url_fits_remaining_space_or_moves_intact_to_next_line(tmp_path: pathlib.Path) -> None:
	"""URL sizing and placement leave the surrounding paragraph's size alone."""
	theme = slide_lib.presentation_theme.default_theme()
	session = slide_lib.layout_measurement.MeasurementSession(theme)
	url = "https://example.test/course"
	destination = url + "?section=genetics"
	prefix = "Join the course: "
	block = slide_lib.native_model.Paragraph(slide_lib.native_model.SourceLocation(tmp_path / "deck.djot", 1),
		(slide_lib.native_model.Text(prefix), slide_lib.native_model.Link(
			(slide_lib.native_model.Text(url),), destination)))
	minimum = session.advance(slide_lib.presentation_theme.ORDINARY_FONT_FAMILY, False, False, 28, prefix)
	minimum += session.advance(slide_lib.presentation_theme.NARROW_FONT_FAMILY, False, False, 12, url)
	clearance = slide_lib.layout_measurement.point_height(1, theme)
	for width, expect_break in ((minimum + clearance + 1, False), (minimum - 10, True)):
		content = slide_lib.layout_object_builders.text_content((block,), 28, 20,
			slide_lib.layout_primitives.StyleRole.BODY, "172033", width, theme, session=session)
		paragraph = content.paragraphs[0]
		run = next(r for r in paragraph.inlines if isinstance(r, slide_lib.layout_content.TextRun) and r.style.literal_url)
		assert paragraph.typography.selected_size_pt == 28
		assert any(isinstance(r, slide_lib.layout_content.LineBreak) for r in paragraph.inlines) == expect_break
		assert run.text == url and run.style.link_url == destination
		assert 12 <= run.style.size_pt < 28


def test_literal_url_keeps_narrow_font_despite_code_markup(tmp_path: pathlib.Path) -> None:
	"""Visible URLs retain the readable narrow face even inside inline code markup."""
	result = layout_test_helpers.compile_source(tmp_path, "=== layout: one-panel\n@body\n"
		"[`https://example.test/short`](https://example.test/full?key=value)\n")
	paragraph = result.plan.slides[0].objects[0].content.paragraphs[0]
	runs = [run for run in paragraph.inlines
		if isinstance(run, slide_lib.layout_content.TextRun)]
	assert runs
	assert all(run.style.font_family == slide_lib.presentation_theme.NARROW_FONT_FAMILY
		and run.style.literal_url for run in runs)


def test_citation_preserves_layout_and_keeps_condensed_clickable_text(tmp_path: pathlib.Path) -> None:
	"""Citation text uses the bottom margin without consuming the existing panel space."""
	base = "=== layout: two-panels\n\n# Tutorial\n\n@left\n\nStory cue.\n\n@right\n\nComparison.\n"
	url = "https://example.test/tutorial"
	plain = layout_test_helpers.compile_source(tmp_path, base).plan.slides[0]
	cited = layout_test_helpers.compile_source(tmp_path, base + "\n@citation\n\nSmith. _Study title._ 2026. " + url).plan.slides[0]
	assert cited.slots == plain.slots
	assert cited.objects[:-1] == plain.objects
	citation = cited.objects[-1]
	assert citation.rectangle.y >= max(slot.rectangle.y + slot.rectangle.height for slot in plain.slots)
	runs = [run for paragraph in citation.content.paragraphs for run in paragraph.inlines
		if isinstance(run, slide_lib.layout_content.TextRun)]
	assert all(run.style.font_family == "IBM Plex Sans Condensed" for run in runs)
	assert any(run.style.italic for run in runs)
	assert any(run.style.link_url == url for run in runs)


@pytest.mark.parametrize("layout", ("section", "subsection", "theend"))
def test_dark_slide_citation_retains_readable_editable_text(tmp_path: pathlib.Path, layout: str) -> None:
	title = "THE END" if layout == "theend" else "Topic"
	result = layout_test_helpers.compile_source(tmp_path, f"=== layout: {layout}\n\n# {title}\n\n"
		"@citation\n\nAuthor. _Study._ https://example.test/study")
	objects = result.plan.slides[0].objects
	assert any(item.object_id == "citation-backing" for item in objects)
	citation = next(item for item in objects if item.object_id == "citation")
	assert any(run.style.link_url == "https://example.test/study"
		for paragraph in citation.content.paragraphs for run in paragraph.inlines
		if isinstance(run, slide_lib.layout_content.TextRun))


@pytest.mark.parametrize("content", ("- A list", "![Image](missing.png)", "$x$"))
def test_citation_rejects_nonprose_before_export(tmp_path: pathlib.Path, content: str) -> None:
	with pytest.raises(ValueError, match="@citation"):
		layout_test_helpers.compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\nContent.\n\n@citation\n\n" + content)


def test_automatic_runt_balancing_moves_words_and_preserves_styling(tmp_path: pathlib.Path) -> None:
	"""A short last line is rebalanced at the selected size, with identical words and run styles."""
	theme = slide_lib.presentation_theme.default_theme()
	session = slide_lib.layout_measurement.MeasurementSession(theme)
	family = slide_lib.presentation_theme.ORDINARY_FONT_FAMILY
	width = session.advance(family, False, False, 28, "Distances between genes can be expressed as ")
	width += session.advance(family, True, False, 28, "map ")
	deck = layout_test_helpers.parsed_source(tmp_path, "=== layout: one-panel\n@body\n"
		"Distances between genes can be expressed as [*map units*]{underline=true};\n")
	blocks = deck.slides[0].cells[0].blocks
	content = slide_lib.layout_object_builders.text_content(blocks, 28, 17,
		slide_lib.layout_primitives.StyleRole.BODY, "172033", width, theme, session=session)
	paragraph = content.paragraphs[0]
	assert paragraph.typography.selected_size_pt == 28
	assert sum(isinstance(run, slide_lib.layout_content.LineBreak) and run.automatic
		for run in paragraph.inlines) == 1
	runs = [run for run in paragraph.inlines if isinstance(run, slide_lib.layout_content.TextRun)]
	text = "".join(run.text if isinstance(run, slide_lib.layout_content.TextRun) else " "
		for run in paragraph.inlines)
	assert " ".join(text.split()) == (
		"Distances between genes can be expressed as map units;")
	assert all(run.style.bold and run.style.underline for run in runs if run.text in ("map", "units"))
	lines = slide_lib.djot_audit.paragraph_lines(paragraph, width, session)
	assert len(lines) == 2 and slide_lib.djot_audit.typography_issue(lines) is None
	assert all(ink_width <= width for _text, ink_width in lines)


def test_runt_balancing_preserves_authored_breaks_and_does_not_add_lines() -> None:
	"""Hard breaks and an unfixable narrow tail stay unchanged rather than adding a line."""
	theme = slide_lib.presentation_theme.default_theme()
	session = slide_lib.layout_measurement.MeasurementSession(theme)
	family = slide_lib.presentation_theme.ORDINARY_FONT_FAMILY
	for tokens, width in (
		((("Long preceding line", family, False, False, False), ("\n", "", False, False, False),
			("word", family, False, False, False)), 900),
		((("Longword tail", family, False, False, False),),
			session.advance(family, False, False, 28, "Longword "))):
		assert session.wrap_tokens(tokens, 28, width) == session.wrap_tokens(tokens, 28, width, balance=False)
