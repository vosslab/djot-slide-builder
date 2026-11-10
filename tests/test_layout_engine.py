"""Compiler contracts for source preservation, capacity diagnostics, and teaching layouts."""

import dataclasses
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


def test_reference_layout_keeps_body_space_and_supplies_study_label(tmp_path: pathlib.Path) -> None:
	"""Reference decoration is behind editable content and its label is outside the body."""
	text = "\n\n# Explanation\n\n@body\n\nStudy this example.\n"
	ordinary = layout_test_helpers.compile_source(tmp_path, "=== layout: one-panel" + text).plan.slides[0]
	reference = layout_test_helpers.compile_source(tmp_path, "=== layout: reference" + text).plan.slides[0]
	body = next(slot for slot in reference.slots if slot.slot_id == "body")
	assert body.rectangle == next(slot.rectangle for slot in ordinary.slots
		if slot.slot_id == "body")
	border = next(item for item in reference.objects if item.object_id == "reference-border")
	label = next(item for item in reference.objects if item.object_id == "reference-label")
	assert border.content.style.fill_role is None
	assert all(border.z_index < item.z_index for item in reference.objects if item != border)
	assert label.rectangle.y >= body.rectangle.y + body.rectangle.height
	assert label.slot_id is None and label.presentation_member_id is None
	assert label.content.paragraphs[0].inlines[0].text == "For reference - not covered in class."


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


def test_all_hidden_deck_has_no_classroom_output(tmp_path: pathlib.Path) -> None:
	"""A retained source-only deck gets a clear diagnostic instead of an empty export."""
	with pytest.raises(ValueError, match="deck has no visible slides"):
		layout_test_helpers.compile_source(tmp_path, "=== layout: blank\nhidden: true\n")


def test_heading_only_title_only_keeps_its_sole_native_title(tmp_path: pathlib.Path) -> None:
	"""An H1-only title-only slide has one TITLE_ONLY member and no body allocation."""
	slide = layout_test_helpers.compile_source(tmp_path, "=== layout: title-only\n\n# Title").plan.slides[0]
	assert slide.layout.topology.libreoffice_layout.autolayout is \
		slide_lib.layout_primitives.LibreOfficeAutoLayout.TITLE_ONLY
	assert tuple(slot.placeholder_kind for slot in slide.slots) == \
		(slide_lib.layout_primitives.PlaceholderKind.TITLE,)
	assert len(slide.objects) == 1
	assert slide.objects[0].placeholder_kind is slide_lib.layout_primitives.PlaceholderKind.TITLE


def test_title_only_body_uses_ordinary_source_ordered_objects(tmp_path: pathlib.Path) -> None:
	"""Title Only retains its one title member while body content remains native objects."""
	layout_test_helpers.write_image(tmp_path, "component.png")
	result = layout_test_helpers.compile_source(tmp_path, "=== layout: title-only\n\n# Title\n\nParagraph.\n\n- First\n- Second\n\n![Tall](component.png)")
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


def test_title_only_body_reports_source_located_capacity(tmp_path: pathlib.Path) -> None:
	"""Title Only body recovery retains the shared visible capacity diagnostic."""
	result = layout_test_helpers.compile_source(tmp_path, "=== layout: title-only\n\n# Title\n\n" + "word " * 500)
	diagnostic = result.capacity_diagnostics[0]
	assert diagnostic.layout == "title-only" and diagnostic.slot == "body"
	assert diagnostic.location.path.name == "specimen.djot" and diagnostic.location.line == 5


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


def test_impossible_content_reports_its_source_location(tmp_path: pathlib.Path) -> None:
	table = "| A |\n| - |\n" + "| word |\n" * 100
	with pytest.raises(slide_lib.capacity_report.PhysicalCapacityError,
			match=r"specimen\.djot:5: one-panel/body cannot fit at the 1 pt serializer-safe minimum") as raised:
		layout_test_helpers.compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\n" + table)
	assert raised.value.diagnostic.cause is slide_lib.capacity_report.CapacityCause.TABLE
	assert raised.value.diagnostic.required_size_pt is None


def test_fixed_title_frame_reports_an_unrepresentable_source_heading(tmp_path: pathlib.Path) -> None:
	"""A fixed title frame raises one source-located physical title capacity result."""
	deck = layout_test_helpers.parsed_source(tmp_path, "=== layout: title-only\n\n# Title")
	heading = next(block for block in deck.slides[0].blocks
		if isinstance(block, slide_lib.native_model.Heading))
	lines = tuple(item for _line in range(400)
		for item in (slide_lib.native_model.Text("line"), slide_lib.native_model.Break()))
	unrepresentable = dataclasses.replace(heading, inlines=lines)
	theme = slide_lib.presentation_theme.default_theme()
	session = slide_lib.layout_measurement.MeasurementSession(theme)
	with pytest.raises(slide_lib.capacity_report.PhysicalCapacityError) as raised:
		slide_lib.layout_size_selection.select_fixed_heading_size((unrepresentable,),
			slide_lib.layout_primitives.LogicalRectangle(110, 180, 1060, 250),
			theme.standard_title_size_pt, theme.title_floor_size_pt, theme, "title-only", "title",
			slide_lib.capacity_report.CapacityCause.TITLE, True, session)
	diagnostic = raised.value.diagnostic
	assert diagnostic.location == heading.location
	assert diagnostic.layout == "title-only" and diagnostic.slot == "title"
	assert diagnostic.required_size_pt is None
	assert diagnostic.cause is slide_lib.capacity_report.CapacityCause.TITLE


def test_unsupported_source_still_fails_at_the_validation_boundary(tmp_path: pathlib.Path) -> None:
	with pytest.raises(ValueError, match=r"specimen\.djot:5: CodeBlock has no physical projection"):
		layout_test_helpers.compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\n```\ncode\n```")


def test_title_first_keeps_a_readable_title_and_reports_the_constrained_body(
		tmp_path: pathlib.Path) -> None:
	"""A dense standard cell absorbs capacity recovery after the independently fitting title."""
	result = layout_test_helpers.compile_source(tmp_path, "=== layout: one-panel\n\n# " + "long title " * 20 +
		"\n\n@body\n\n" + "body " * 200)
	title = next(item for item in result.plan.slides[0].objects
		if item.placeholder_kind is slide_lib.layout_primitives.PlaceholderKind.TITLE)
	diagnostic = result.capacity_diagnostics[0]
	assert title.content.paragraphs[0].typography.selected_size_pt >= \
		slide_lib.presentation_theme.default_theme().title_floor_size_pt
	assert diagnostic.slot == "body"
	assert diagnostic.cause is slide_lib.capacity_report.CapacityCause.PARAGRAPH_LIST


def test_theend_layout_is_large_two_line_text_with_a_native_star(tmp_path: pathlib.Path) -> None:
	"""The recurring closer stays editable while its vector star supplies the flourish."""
	slide = layout_test_helpers.compile_source(tmp_path, "=== layout: theend\n\n# THE END").plan.slides[0]
	text = next(item.content for item in slide.objects
		if isinstance(item.content, slide_lib.layout_content.TextContent))
	lines = tuple("".join(run.text for run in paragraph.inlines
		if isinstance(run, slide_lib.layout_content.TextRun)) for paragraph in text.paragraphs)
	star = next(item for item in slide.objects
		if isinstance(item.content, slide_lib.layout_content.ShapeContent) and
		item.content.kind is slide_lib.layout_primitives.ShapeKind.STAR)
	assert lines == ("THE", "END")
	assert star.origin is slide_lib.layout_primitives.LayoutObjectOrigin.THEME


def test_titleless_one_panel_reclaims_title_space(tmp_path: pathlib.Path) -> None:
	"""Omitting a title expands the body while retaining the ordinary page margins."""
	result = layout_test_helpers.compile_source(tmp_path,
		"=== layout: one-panel\n\n# Heading\n\n@body\n\nContent.\n\n"
		"=== layout: one-panel\n\n@body\n\nContent.\n")
	titled, untitled = result.plan.slides
	title = next(slot for slot in titled.slots if slot.slot_id == "title")
	body = next(slot for slot in titled.slots if slot.slot_id == "body")
	full = next(slot for slot in untitled.slots if slot.slot_id == "body")
	assert all(slot.slot_id != "title" for slot in untitled.slots)
	assert full.rectangle.y == title.rectangle.y
	assert full.rectangle.height > body.rectangle.height
	assert full.rectangle.y + full.rectangle.height == body.rectangle.y + body.rectangle.height
	text = next(item for item in untitled.objects if item.object_id == "body")
	assert text.frame_text.vertical_alignment is slide_lib.layout_primitives.VerticalAlignment.MIDDLE
	assert text.content.paragraphs[0].properties.horizontal_alignment is \
		slide_lib.layout_primitives.HorizontalAlignment.START


@pytest.mark.parametrize("layout", ("bookend", "definitions"))
def test_teaching_layouts_preserve_body_space_and_add_editable_frames(
		tmp_path: pathlib.Path, layout: str) -> None:
	"""Teaching frames keep content space and never label live content as reference-only."""
	text = "\n# Learning focus\n@body\n- Term: explanation\n"
	ordinary = layout_test_helpers.compile_source(tmp_path, "=== layout: one-panel" + text).plan.slides[0]
	theme = slide_lib.presentation_theme.default_theme()
	page = slide_lib.layout_engine.compile_layout_deck(
		layout_test_helpers.parsed_source(tmp_path, f"=== layout: {layout}" + text), theme).plan.slides[0]
	assert next(slot.rectangle for slot in page.slots if slot.slot_id == "body") == next(
		slot.rectangle for slot in ordinary.slots if slot.slot_id == "body")
	frame = [item for item in page.objects if item.object_id.startswith("teaching-")]
	assert all(item.content.style.line_pattern is slide_lib.layout_primitives.LinePattern.NONE
		for item in frame)
	for name in ("band", "corner"):
		first = next(item for item in frame if item.object_id == f"teaching-{name}-0")
		opposite = next(item for item in frame if item.object_id == f"teaching-{name}-1")
		assert [(1280 - first.rectangle.x - point.x,
			800 - first.rectangle.y - point.y) for point in first.content.points] == [
			(opposite.rectangle.x + point.x, opposite.rectangle.y + point.y)
			for point in opposite.content.points]
		assert first.content.style.fill_role == opposite.content.style.fill_role
		for shape in (first, opposite):
			assert min(point.x for point in shape.content.points) == 0
			assert min(point.y for point in shape.content.points) == 0
			assert max(point.x for point in shape.content.points) == shape.rectangle.width
			assert max(point.y for point in shape.content.points) == shape.rectangle.height
	assert not any(item.object_id.startswith("reference-") for item in page.objects)
	assert max(item.z_index for item in frame) < min(item.z_index for item in page.objects
		if item not in frame)


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


def test_definitions_reject_missing_term_boundaries(tmp_path: pathlib.Path) -> None:
	"""Malformed entries must identify how to supply a term rather than silently look ordinary."""
	with pytest.raises(ValueError, match="Term: explanation"):
		layout_test_helpers.compile_source(tmp_path, "=== layout: definitions\n@body\n- No term separator\n")
