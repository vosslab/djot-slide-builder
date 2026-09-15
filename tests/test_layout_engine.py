"""Behavior coverage for the one-to-one layout compiler boundary."""

import dataclasses
import pathlib

import PIL.Image
import pytest

import slide_lib.capacity_report
import slide_lib.compilation_result
import slide_lib.djot_parser
import slide_lib.layout_content
import slide_lib.layout_engine
import slide_lib.layout_measurement
import slide_lib.layout_primitives
import slide_lib.layout_registry
import slide_lib.native_model
import slide_lib.presentation_theme


def parsed_source(tmp_path: pathlib.Path, source: str) -> slide_lib.native_model.Deck:
	"""Write and parse one test-owned Djot specimen."""
	path = tmp_path / "specimen.djot"
	path.write_text(source, encoding="utf-8")
	return slide_lib.djot_parser.parse_deck(path)


def compile_source(tmp_path: pathlib.Path, source: str) -> slide_lib.compilation_result.CompilationResult:
	"""Compile one test-owned source with the authoritative native theme."""
	return slide_lib.layout_engine.compile_layout_deck(
		parsed_source(tmp_path, source), slide_lib.presentation_theme.default_theme())


def write_image(tmp_path: pathlib.Path, name: str) -> None:
	"""Create one inline test-owned component image with an intentionally tall aspect ratio."""
	PIL.Image.new("RGB", (120, 320), (20, 90, 160)).save(tmp_path / name)


def test_two_sources_produce_two_stable_source_slides(tmp_path: pathlib.Path) -> None:
	result = compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\nFirst.\n\n=== layout: two-panels\n\n@left\n\nLeft.\n\n@right\n\nRight.")
	assert tuple(slide.identity.slide_id for slide in result.plan.slides) == ("slide-1", "slide-2")


def test_hidden_source_is_retained_but_not_compiled(tmp_path: pathlib.Path) -> None:
	"""Hide/show changes physical output without discarding authored slide content."""
	source = ("=== layout: title-only\nhidden: true\n\n# Optional\n"
		"=== layout: title-only\n\n# Teaching\n"
		"=== layout: title-only\nhidden: false\n\n# Closing\n")
	deck = parsed_source(tmp_path, source)
	result = slide_lib.layout_engine.compile_layout_deck(
		deck, slide_lib.presentation_theme.default_theme())
	assert deck.title == "Teaching" and deck.slides[0].blocks[0].inlines[0].value == "Optional"
	assert tuple(page.identity.source for page in result.plan.slides) == \
		tuple(slide.location for slide in deck.slides[1:])


def test_unhiding_source_restores_its_output_position(tmp_path: pathlib.Path) -> None:
	"""An explicit false value restores the slide before the following material."""
	result = compile_source(tmp_path,
		"=== layout: title-only\nhidden: false\n# Optional\n"
		"=== layout: title-only\n# Teaching\n")
	assert tuple(page.identity.source.line for page in result.plan.slides) == (1, 4)


def test_all_hidden_deck_has_no_classroom_output(tmp_path: pathlib.Path) -> None:
	"""A retained source-only deck gets a clear diagnostic instead of an empty export."""
	with pytest.raises(ValueError, match="deck has no visible slides"):
		compile_source(tmp_path, "=== layout: blank\nhidden: true\n")


def test_section_keeps_its_centered_libreoffice_layout_identity(tmp_path: pathlib.Path) -> None:
	"""The section semantic name remains native Centered Text."""
	result = compile_source(tmp_path, "=== layout: section\n\n# Section\n\n## Context")
	assert result.plan.slides[0].layout.topology.libreoffice_layout.autolayout is \
		slide_lib.layout_primitives.LibreOfficeAutoLayout.ONLY_TEXT


def test_heading_only_title_only_keeps_its_sole_native_title(tmp_path: pathlib.Path) -> None:
	"""An H1-only title-only slide has one TITLE_ONLY member and no body allocation."""
	slide = compile_source(tmp_path, "=== layout: title-only\n\n# Title").plan.slides[0]
	assert slide.layout.topology.libreoffice_layout.autolayout is \
		slide_lib.layout_primitives.LibreOfficeAutoLayout.TITLE_ONLY
	assert tuple(slot.placeholder_kind for slot in slide.slots) == \
		(slide_lib.layout_primitives.PlaceholderKind.TITLE,)
	assert len(slide.objects) == 1
	assert slide.objects[0].placeholder_kind is slide_lib.layout_primitives.PlaceholderKind.TITLE


def test_title_only_body_uses_ordinary_source_ordered_objects(tmp_path: pathlib.Path) -> None:
	"""Title Only retains its one title member while body content remains native objects."""
	write_image(tmp_path, "component.png")
	result = compile_source(tmp_path, "=== layout: title-only\n\n# Title\n\nParagraph.\n\n- First\n- Second\n\n![Tall](component.png)")
	slide = result.plan.slides[0]
	assert slide.layout.topology.libreoffice_layout.autolayout is \
		slide_lib.layout_primitives.LibreOfficeAutoLayout.TITLE_ONLY
	assert tuple(slot.placeholder_kind for slot in slide.slots) == \
		(slide_lib.layout_primitives.PlaceholderKind.TITLE, slide_lib.layout_primitives.PlaceholderKind.NONE)
	assert slide.objects[0].placeholder_kind is slide_lib.layout_primitives.PlaceholderKind.TITLE
	assert tuple(type(item.content) for item in slide.objects[1:]) == \
		(slide_lib.layout_content.TextContent, slide_lib.layout_content.TextContent,
			slide_lib.layout_content.PictureContent)
	assert all(item.placeholder_kind is slide_lib.layout_primitives.PlaceholderKind.NONE
		for item in slide.objects[1:])
	title = slide.objects[0]
	assert all(item.rectangle.y > title.rectangle.y + title.rectangle.height for item in slide.objects[1:])


def test_title_only_body_reports_source_located_capacity(tmp_path: pathlib.Path) -> None:
	"""Title Only body recovery retains the shared visible capacity diagnostic."""
	result = compile_source(tmp_path, "=== layout: title-only\n\n# Title\n\n" + "word " * 500)
	diagnostic = result.capacity_diagnostics[0]
	assert diagnostic.layout == "title-only" and diagnostic.slot == "body"
	assert diagnostic.location.path.name == "specimen.djot" and diagnostic.location.line == 5


def test_title_only_table_remains_an_ordinary_native_object(tmp_path: pathlib.Path) -> None:
	"""A sole root table uses the body allocation without an invented placeholder."""
	result = compile_source(tmp_path, "=== layout: title-only\n\n# Results\n\n| Sample | Result |\n| - | - |\n| A | pass |")
	table = result.plan.slides[0].objects[1]
	assert isinstance(table.content, slide_lib.layout_content.TableContent)
	assert table.placeholder_kind is slide_lib.layout_primitives.PlaceholderKind.NONE


@pytest.mark.parametrize("layout, slots", (("one-panel", ("body",)), ("two-panels", ("left", "right"))))
def test_overfull_representable_slide_stays_one_page_and_reports_capacity(
		tmp_path: pathlib.Path, layout: str, slots: tuple[str, ...]) -> None:
	long = "word " * 500
	regions = "".join(f"\n@{slot}\n\n{long}" for slot in slots)
	result = compile_source(tmp_path, f"=== layout: {layout}\n{regions}")
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
		compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\n" + table)
	assert raised.value.diagnostic.cause is slide_lib.capacity_report.CapacityCause.TABLE
	assert raised.value.diagnostic.required_size_pt is None


def test_fixed_title_frame_reports_an_unrepresentable_source_heading(tmp_path: pathlib.Path) -> None:
	"""A fixed title frame raises one source-located physical title capacity result."""
	deck = parsed_source(tmp_path, "=== layout: title-only\n\n# Title")
	heading = next(block for block in deck.slides[0].blocks
		if isinstance(block, slide_lib.native_model.Heading))
	lines = tuple(item for _line in range(400)
		for item in (slide_lib.native_model.Text("line"), slide_lib.native_model.Break()))
	unrepresentable = dataclasses.replace(heading, inlines=lines)
	theme = slide_lib.presentation_theme.default_theme()
	session = slide_lib.layout_measurement.MeasurementSession(theme)
	with pytest.raises(slide_lib.capacity_report.PhysicalCapacityError) as raised:
		slide_lib.layout_measurement.select_fixed_heading_size((unrepresentable,),
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
		compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\n```\ncode\n```")


def test_title_slide_uses_native_master_frames_and_centered_text(tmp_path: pathlib.Path) -> None:
	"""Title Slide uses its native title and outline frames with centered text."""
	result = compile_source(tmp_path, "=== layout: title-slide\n\n# Genetics\n\n## Week one")
	items = result.plan.slides[0].objects
	objects = {item.placeholder_kind: item for item in items}
	title = objects[slide_lib.layout_primitives.PlaceholderKind.TITLE]
	subtitle = objects[slide_lib.layout_primitives.PlaceholderKind.SUBTITLE]
	decorations = tuple(item for item in items
		if isinstance(item.content, slide_lib.layout_content.ShapeContent))
	assert tuple((item.frame_text.vertical_alignment,
		item.content.paragraphs[0].properties.horizontal_alignment) for item in (title, subtitle)) == (
		(slide_lib.layout_primitives.VerticalAlignment.MIDDLE,
			slide_lib.layout_primitives.HorizontalAlignment.CENTER),
		(slide_lib.layout_primitives.VerticalAlignment.MIDDLE,
			slide_lib.layout_primitives.HorizontalAlignment.CENTER))
	assert decorations and all(item.origin is slide_lib.layout_primitives.LayoutObjectOrigin.THEME
		for item in decorations)


def test_section_uses_a_centered_transition_surface(tmp_path: pathlib.Path) -> None:
	"""A section keeps editable Centered Text inside its layout-owned transition card."""
	result = compile_source(tmp_path, "=== layout: section\n\n# Unit one\n\n## Central question")
	slide = result.plan.slides[0]
	section = next(item for item in slide.objects if item.object_id == "section")
	frame = next(item for item in slide.objects
		if isinstance(item.content, slide_lib.layout_content.ShapeContent))
	assert (section.frame_text.vertical_alignment,
		tuple(paragraph.properties.horizontal_alignment for paragraph in section.content.paragraphs)) == (
		slide_lib.layout_primitives.VerticalAlignment.MIDDLE,
		(slide_lib.layout_primitives.HorizontalAlignment.CENTER,
			slide_lib.layout_primitives.HorizontalAlignment.CENTER))
	assert section.rectangle.y + section.rectangle.height / 2 == \
		slide_lib.layout_primitives.LOGICAL_SLIDE_HEIGHT / 2
	assert (slide.surface.background_role, slide.surface.show_master_objects,
		frame.content.kind, frame.origin) == (
		slide_lib.layout_primitives.StyleRole.TRANSITION, False,
		slide_lib.layout_primitives.ShapeKind.ROUNDED_RECTANGLE,
		slide_lib.layout_primitives.LayoutObjectOrigin.THEME)


@pytest.mark.parametrize("source", (
	"=== layout: title-only\n\n# Title",
	"=== layout: one-panel\n\n# Title\n\n@body\n\nBody."))
def test_top_aligned_layouts_keep_start_top_titles(tmp_path: pathlib.Path, source: str) -> None:
	"""Title Only and one-panel preserve the non-centered title contrast."""
	title = compile_source(tmp_path, source).plan.slides[0].objects[0]
	assert (title.frame_text.vertical_alignment,
		title.content.paragraphs[0].properties.horizontal_alignment) == (
		slide_lib.layout_primitives.VerticalAlignment.TOP,
		slide_lib.layout_primitives.HorizontalAlignment.START)


def test_title_first_keeps_a_readable_title_and_reports_the_constrained_body(
		tmp_path: pathlib.Path) -> None:
	"""A dense standard cell absorbs capacity recovery after the independently fitting title."""
	result = compile_source(tmp_path, "=== layout: one-panel\n\n# " + "long title " * 20 +
		"\n\n@body\n\n" + "body " * 200)
	title = next(item for item in result.plan.slides[0].objects
		if item.placeholder_kind is slide_lib.layout_primitives.PlaceholderKind.TITLE)
	diagnostic = result.capacity_diagnostics[0]
	assert title.content.paragraphs[0].typography.selected_size_pt >= \
		slide_lib.presentation_theme.default_theme().title_floor_size_pt
	assert diagnostic.slot == "body"
	assert diagnostic.cause is slide_lib.capacity_report.CapacityCause.PARAGRAPH_LIST


def test_section_projection_preserves_plain_text_spacing(tmp_path: pathlib.Path) -> None:
	"""A section heading remains one editable text run with its authored spaces."""
	result = compile_source(tmp_path, "=== layout: section\n\n# Instructor Information")
	text = next(item.content for item in result.plan.slides[0].objects
		if isinstance(item.content, slide_lib.layout_content.TextContent))
	paragraph = text.paragraphs[0]
	assert tuple(run.text for run in paragraph.inlines
		if isinstance(run, slide_lib.layout_content.TextRun)) == ("Instructor Information",)


def test_the_end_section_is_large_two_line_text_with_a_native_star(tmp_path: pathlib.Path) -> None:
	"""The recurring closer stays editable while its vector star supplies the flourish."""
	slide = compile_source(tmp_path, "=== layout: section\n\n# THE END").plan.slides[0]
	text = next(item.content for item in slide.objects
		if isinstance(item.content, slide_lib.layout_content.TextContent))
	lines = tuple("".join(run.text for run in paragraph.inlines
		if isinstance(run, slide_lib.layout_content.TextRun)) for paragraph in text.paragraphs)
	star = next(item for item in slide.objects
		if isinstance(item.content, slide_lib.layout_content.ShapeContent) and
		item.content.kind is slide_lib.layout_primitives.ShapeKind.STAR)
	assert lines == ("THE", "END")
	assert text.paragraphs[0].typography.selected_size_pt >= 100
	assert star.origin is slide_lib.layout_primitives.LayoutObjectOrigin.THEME


def test_nonempty_notes_reveals_and_authored_content_remain_on_the_source_slide(tmp_path: pathlib.Path) -> None:
	parsed = parsed_source(tmp_path, "=== layout: one-panel\n\n@body\n\n=> appear\nVisible later.")
	slide = dataclasses.replace(parsed.slides[0], notes=("First note", "Second note"))
	deck = dataclasses.replace(parsed, slides=(slide,))
	result = slide_lib.layout_engine.compile_layout_deck(deck, slide_lib.presentation_theme.default_theme())
	compiled = result.plan.slides[0]
	targets = tuple(target for item in compiled.objects for target in item.reveal_targets)
	assert tuple(note.text for note in compiled.notes) == ("First note", "Second note")
	assert targets and tuple(target.activation_order for target in targets) == tuple(range(len(targets)))
	assert any(isinstance(item.content, slide_lib.layout_content.TextContent) for item in compiled.objects)
	assert all(item.origin is slide_lib.layout_primitives.LayoutObjectOrigin.AUTHORED for item in compiled.objects)


def test_multiple_choice_reserves_the_answer_popup_from_each_visible_choice(
		tmp_path: pathlib.Path) -> None:
	"""A text-only question uses the shared adaptive choice geometry before reveal."""
	result = compile_source(tmp_path, """=== layout: multiple-choice

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
