"""Focused tests for direct native Djot presentation export."""

# Standard Library
import pathlib
from unittest import mock

# PIP3 modules
import PIL.Image
import pytest
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

# Local Modules
from slide_lib import layouts
import slide_lib.native_export
import slide_lib.layout_validation
import slide_lib.native_model
import slide_lib.presentation_theme


#============================================
def native_slide(blocks: tuple[slide_lib.native_model.Block, ...]) -> slide_lib.native_model.Slide:
	"""Return a direct named one-panel IR slide for layout-validation tests."""
	location = slide_lib.native_model.SourceLocation(pathlib.Path("inline.ir"), 1)
	title_blocks = tuple(block for block in blocks if isinstance(block, slide_lib.native_model.Heading))
	body_blocks = tuple(block for block in blocks if not isinstance(block, slide_lib.native_model.Heading))
	cells = (slide_lib.native_model.Cell(body_blocks[0].location, body_blocks, "body"),) if body_blocks else ()
	return slide_lib.native_model.Slide(location, "one-panel", False, (), title_blocks, cells)


#============================================
def write_png(output_path: pathlib.Path) -> pathlib.Path:
	"""Write one small component image fixture."""
	image = PIL.Image.new("RGB", (80, 40), (36, 87, 143))
	image.save(output_path)
	return output_path


#============================================
def layout_source(name: str, spec: layouts.LayoutSpec) -> str:
	"""Return the smallest valid source fixture for one registered layout."""
	lines = [f"=== layout: {name}"]
	if spec.allows_title:
		lines.append("# Layout title")
	if spec.allows_subtitle:
		lines.append("## Subtitle")
	for slot_name in spec.slot_names:
		lines.append(f"@{slot_name}")
		if name == "gallery":
			lines.extend(("![One](one.png)", "![Two](two.png)"))
		elif name == "multiple-choice" and slot_name == "question":
			lines.extend(("Which molecule carries genetic information?", "", "- A. Lipid", "- B. DNA"))
		elif name == "multiple-choice":
			lines.append("Answer: B. DNA")
		else:
			lines.extend((f"## {slot_name}", f"Editable {slot_name}"))
	return "\n".join(lines) + "\n"


#============================================
def test_horizontal_grid_layout_keeps_bullets_numbers_and_links(tmp_path: pathlib.Path) -> None:
	"""Two-content cells retain independently editable native text semantics."""
	deck_path = tmp_path / "two-content.djot"
	deck_path.write_text("=== layout: two-panels\n# Overview\n@left\n"
		"## [Left](https://example.edu/left)\n- First\n  - Nested\n1. Ordered\n"
		"@right\n## Right\n- Second\n", encoding="utf-8")
	output_path = tmp_path / "two-content.pptx"
	deck = slide_lib.native_export.parse_deck(deck_path)
	slide_lib.native_export.render_native_pptx(deck, output_path)
	shape_xml = "".join(shape.element.xml for shape in Presentation(output_path).slides[0].shapes)
	assert "buChar" in shape_xml and "buAutoNum" in shape_xml and "hlinkClick" in shape_xml


#============================================
def test_native_list_theme_uses_level_specific_hanging_indents(tmp_path: pathlib.Path) -> None:
	"""Nested bullets remain separate paragraphs with explicit theme tab stops."""
	deck_path = tmp_path / "nested-list.djot"
	deck_path.write_text("=== layout: one-panel\n# Outline\n@body\n"
		"- Parent wraps onto another line when the content is long enough to need it\n"
		"  - Child\n", encoding="utf-8")
	output_path = tmp_path / "nested-list.pptx"
	slide_lib.native_export.render_native_pptx(slide_lib.native_export.parse_deck(deck_path), output_path)
	paragraphs = {paragraph.text: paragraph for shape in Presentation(output_path).slides[0].shapes
		if shape.has_text_frame for paragraph in shape.text_frame.paragraphs if paragraph.text}
	root = paragraphs["Parent wraps onto another line when the content is long enough to need it"]
	child = paragraphs["Child"]
	assert (root.level, child.level) == (0, 1)
	assert all(marker in root._p.xml and marker in child._p.xml
		for marker in ('marL=', 'indent="-', '<a:tab pos=', '<a:buChar char='))
	assert root._p.xml != child._p.xml


#============================================
def test_standard_theme_uses_gradient_band_and_centered_title(tmp_path: pathlib.Path) -> None:
	"""Ordinary slides carry the shared native band and centered title semantics."""
	deck_path = tmp_path / "theme.djot"
	deck_path.write_text("=== layout: one-panel\n# Centered title\n@body\n- Body\n", encoding="utf-8")
	output_path = tmp_path / "theme.pptx"
	deck = slide_lib.native_export.parse_deck(deck_path)
	slide_lib.native_export.render_native_pptx(deck, output_path)
	presentation = Presentation(output_path)
	theme = slide_lib.presentation_theme.default_theme()
	shapes = presentation.slides[0].shapes
	title = next(shape for shape in shapes
		if shape.has_text_frame and shape.text == "Centered title")
	assert title.text_frame.paragraphs[0].alignment == PP_ALIGN.CENTER
	gradient_xml = next(shape.element.xml for shape in shapes if "gradFill" in shape.element.xml)
	assert presentation.slide_width == round(
		theme.emu_per_logical_pixel * slide_lib.presentation_theme.LOGICAL_SLIDE_WIDTH)
	assert presentation.slide_height == round(
		theme.emu_per_logical_pixel * slide_lib.presentation_theme.LOGICAL_SLIDE_HEIGHT)
	assert theme.gradient_start_color in gradient_xml and \
		theme.gradient_end_color in gradient_xml


#============================================
def test_title_only_theme_centers_its_single_title_both_ways(tmp_path: pathlib.Path) -> None:
	"""Title-only questions keep centered native text instead of a top-left title box."""
	deck_path = tmp_path / "question.djot"
	deck_path.write_text("=== layout: title-only\n# What causes mutation?\n", encoding="utf-8")
	output_path = tmp_path / "question.pptx"
	slide_lib.native_export.render_native_pptx(slide_lib.native_export.parse_deck(deck_path), output_path)
	title = next(shape for shape in Presentation(output_path).slides[0].shapes
		if shape.has_text_frame and shape.text == "What causes mutation?")
	assert title.text_frame.vertical_anchor == MSO_ANCHOR.MIDDLE
	assert title.text_frame.paragraphs[0].alignment == PP_ALIGN.CENTER


#============================================
def test_inline_runs_keep_native_formatting_and_url_typography(tmp_path: pathlib.Path) -> None:
	"""Typed emphasis, code, breaks, and bare URLs remain formatted editable runs."""
	deck_path = tmp_path / "formatting.djot"
	deck_path.write_text("=== layout: one-panel\n# [Heading](https://example.edu)\n@body\n"
		"_Italic_ and `code` [Course resource](https://example.edu/resource)  \n"
		"[https://example.edu/path](https://example.edu/path)\n", encoding="utf-8")
	output_path = tmp_path / "formatting.pptx"
	slide_lib.native_export.render_native_pptx(slide_lib.native_export.parse_deck(deck_path), output_path)
	runs = [run for shape in Presentation(output_path).slides[0].shapes if shape.has_text_frame
		for paragraph in shape.text_frame.paragraphs for run in paragraph.runs]
	assert any(run.text == "https://example.edu/path" and run.font.name == layouts.URL_FONT_NAME
		and run.hyperlink.address == "https://example.edu/path" for run in runs)
	assert any(run.text == "Italic" and run.font.italic for run in runs)


#============================================
def test_long_default_title_reports_the_causal_h1_before_mutating_content(tmp_path: pathlib.Path) -> None:
	"""A default H1 that crowds named cells reports its own authored source line."""
	deck_path = tmp_path / "long-title.djot"
	title = " ".join("adaptable" for _ in range(260))
	deck_path.write_text("=== layout: two-panels\n# " + title +
		"\n@left\n- Left\n@right\n- Right\n", encoding="utf-8")
	deck = slide_lib.native_export.parse_deck(deck_path)
	presentation = Presentation()
	slide = presentation.slides.add_slide(presentation.slide_layouts[6])
	with pytest.raises(ValueError, match=r"long-title\.djot:2:.*H1 allocation leaves left"):
		layouts.render_layout(slide, deck.slides[0], deck)
	assert not slide.shapes


#============================================
def test_titleless_one_panel_uses_its_full_editable_body_region(tmp_path: pathlib.Path) -> None:
	"""An ordinary body-only slide remains native editable text without an H1."""
	location = slide_lib.native_model.SourceLocation(tmp_path / "titleless-body.ir", 7)
	body = slide_lib.native_model.Paragraph(location, (slide_lib.native_model.Text("Editable body"),))
	source = native_slide((body,))
	deck = slide_lib.native_model.Deck(location.path, tmp_path, tmp_path, "Titleless", False, (source,), {})
	presentation = Presentation()
	slide = presentation.slides.add_slide(presentation.slide_layouts[6])
	layouts.render_layout(slide, source, deck)
	assert [shape.text for shape in slide.shapes if shape.has_text_frame and shape.text] == ["Editable body"]


#============================================
def test_titleless_named_panels_keep_their_editable_slot_content(tmp_path: pathlib.Path) -> None:
	"""A titleless ordinary panel layout keeps every named cell independently native."""
	location = slide_lib.native_model.SourceLocation(tmp_path / "titleless-panels.ir", 7)
	def paragraph(value: str) -> slide_lib.native_model.Paragraph:
		return slide_lib.native_model.Paragraph(location, (slide_lib.native_model.Text(value),))
	source = slide_lib.native_model.Slide(location, "two-panels", False, (), (), (
		slide_lib.native_model.Cell(location, (paragraph("Left"),), "left"),
		slide_lib.native_model.Cell(location, (paragraph("Right"),), "right"),
	))
	deck = slide_lib.native_model.Deck(location.path, tmp_path, tmp_path, "Titleless", False, (source,), {})
	presentation = Presentation()
	slide = presentation.slides.add_slide(presentation.slide_layouts[6])
	layouts.render_layout(slide, source, deck)
	assert {shape.text for shape in slide.shapes if shape.has_text_frame and shape.text} == {"Left", "Right"}


#============================================
@pytest.mark.parametrize("with_title", (False, True))
def test_root_body_allows_one_local_h2_with_or_without_a_global_title(tmp_path: pathlib.Path,
		with_title: bool) -> None:
	"""A root body subtitle shares the same native heading/body rendering as named cells."""
	location = slide_lib.native_model.SourceLocation(tmp_path / f"body-h2-{with_title}.ir", 7)
	local_heading = slide_lib.native_model.Heading(location, 2, (slide_lib.native_model.Text("Local heading"),))
	body = slide_lib.native_model.Paragraph(location, (slide_lib.native_model.Text("Editable body"),))
	global_blocks = ((slide_lib.native_model.Heading(location, 1,
		(slide_lib.native_model.Text("Global title"),)),) if with_title else ())
	source = slide_lib.native_model.Slide(location, "one-panel", False, (), global_blocks, (
		slide_lib.native_model.Cell(location, (local_heading, body), "body"),))
	deck = slide_lib.native_model.Deck(location.path, tmp_path, tmp_path, "Body heading", False, (source,), {})
	presentation = Presentation()
	slide = presentation.slides.add_slide(presentation.slide_layouts[6])
	layouts.render_layout(slide, source, deck)
	visible_text = {shape.text for shape in slide.shapes if shape.has_text_frame and shape.text}
	assert visible_text == ({"Global title", "Local heading", "Editable body"} if with_title else
		{"Local heading", "Editable body"})


#============================================
def test_root_body_rejects_multiple_local_h2_headings_before_mutating_a_slide(tmp_path: pathlib.Path) -> None:
	"""Root-body headings retain the same one-optional-heading contract as named slots."""
	location = slide_lib.native_model.SourceLocation(tmp_path / "many-body-h2.ir", 7)
	heading = slide_lib.native_model.Heading(location, 2, (slide_lib.native_model.Text("First"),))
	second = slide_lib.native_model.Heading(slide_lib.native_model.SourceLocation(location.path, 10), 2,
		(slide_lib.native_model.Text("Second"),))
	body = slide_lib.native_model.Paragraph(location, (slide_lib.native_model.Text("Editable body"),))
	source = slide_lib.native_model.Slide(location, "one-panel", False, (), (), (
		slide_lib.native_model.Cell(location, (heading, second, body), "body"),))
	deck = slide_lib.native_model.Deck(location.path, tmp_path, tmp_path, "Body heading", False, (source,), {})
	presentation = Presentation()
	slide = presentation.slides.add_slide(presentation.slide_layouts[6])
	with pytest.raises(ValueError, match=r"many-body-h2\.ir:10:.*one optional level-two heading"):
		layouts.render_layout(slide, source, deck)
	assert not slide.shapes


#============================================
@pytest.mark.parametrize("layout_name", ("one-panel", "two-panels"))
def test_a_lone_local_h2_is_visible_editable_cell_content(tmp_path: pathlib.Path,
		layout_name: str) -> None:
	"""A local H2 is valid visible content in root and named ordinary panel cells."""
	location = slide_lib.native_model.SourceLocation(tmp_path / f"h2-only-{layout_name}.ir", 7)
	def heading(value: str) -> slide_lib.native_model.Heading:
		return slide_lib.native_model.Heading(location, 2, (slide_lib.native_model.Text(value),))
	if layout_name == "one-panel":
		source = slide_lib.native_model.Slide(location, layout_name, False, (), (), (
			slide_lib.native_model.Cell(location, (heading("Body heading"),), "body"),))
	else:
		source = slide_lib.native_model.Slide(location, layout_name, False, (), (), (
			slide_lib.native_model.Cell(location, (heading("Left heading"),), "left"),
			slide_lib.native_model.Cell(location, (heading("Right heading"),), "right"),
		))
	deck = slide_lib.native_model.Deck(location.path, tmp_path, tmp_path, "Local heading", False, (source,), {})
	presentation = Presentation()
	slide = presentation.slides.add_slide(presentation.slide_layouts[6])
	layouts.render_layout(slide, source, deck)
	assert {shape.text for shape in slide.shapes if shape.has_text_frame and shape.text} == (
		{"Body heading"} if layout_name == "one-panel" else {"Left heading", "Right heading"})


#============================================
def test_unreadable_local_h2_fails_before_background_or_shapes(tmp_path: pathlib.Path) -> None:
	"""An assigned cell rejects an H2 that cannot fit even at the readable floor."""
	location = slide_lib.native_model.SourceLocation(tmp_path / "dense-h2.ir", 7)
	heading = slide_lib.native_model.Heading(location, 2,
		(slide_lib.native_model.Text(" ".join("adaptable" for _ in range(800))),))
	source = slide_lib.native_model.Slide(location, "one-panel", False, (), (), (
		slide_lib.native_model.Cell(location, (heading,), "body"),))
	deck = slide_lib.native_model.Deck(location.path, tmp_path, tmp_path, "Local heading", False, (source,), {})
	presentation = Presentation()
	slide = presentation.slides.add_slide(presentation.slide_layouts[6])
	with pytest.raises(ValueError, match=r"dense-h2\.ir:7:.*local H2 cannot fit"):
		layouts.render_layout(slide, source, deck)
	assert not slide.shapes


#============================================
def test_two_over_one_reserves_readable_footer_space(tmp_path: pathlib.Path) -> None:
	"""A dense full-width footer receives height from two short upper components."""
	deck_path = tmp_path / "footer.djot"
	footer = "\n".join(f"- Footer line {index}" for index in range(24))
	deck_path.write_text("=== layout: two-over-one-panels\n# Title\n@top-left\n- Left\n"
		"@top-right\n- Right\n@bottom\n" + footer + "\n", encoding="utf-8")
	source = slide_lib.native_export.parse_deck(deck_path).slides[0]
	plan = layouts.plan_content(source, layouts.LAYOUTS["two-over-one-panels"])
	canonical = layouts.cell_rectangles(layouts.LAYOUTS["two-over-one-panels"], plan.content_rectangle)
	responsive = layouts.content_cell_rectangles(source, layouts.LAYOUTS["two-over-one-panels"], plan.content_rectangle)

	assert responsive[2][3] > canonical[2][3]
	assert responsive[0][3] < canonical[0][3]


#============================================
@pytest.mark.parametrize("case", ("component-image", "vertical-title"))
def test_titleless_panel_variants_keep_native_content(tmp_path: pathlib.Path, case: str) -> None:
	"""Titleless component and title-strip panels retain their native body objects."""
	location = slide_lib.native_model.SourceLocation(tmp_path / f"{case}.ir", 7)
	if case == "component-image":
		write_png(tmp_path / "component.png")
		image = slide_lib.native_model.Image(location, "Component", "component.png", None)
		source = native_slide((image,))
	else:
		def paragraph(value: str) -> slide_lib.native_model.Paragraph:
			return slide_lib.native_model.Paragraph(location, (slide_lib.native_model.Text(value),))
		source = slide_lib.native_model.Slide(location, "vertical-title-two-panels", False, (), (), (
			slide_lib.native_model.Cell(location, (paragraph("Text"),), "text"),
			slide_lib.native_model.Cell(location, (paragraph("Chart"),), "chart"),
		))
	deck = slide_lib.native_model.Deck(location.path, tmp_path, tmp_path, "Titleless", False, (source,), {})
	presentation = Presentation()
	slide = presentation.slides.add_slide(presentation.slide_layouts[6])
	layouts.render_layout(slide, source, deck)
	visible_text = {shape.text for shape in slide.shapes if shape.has_text_frame and shape.text}
	if case == "component-image":
		assert len([shape for shape in slide.shapes if shape.shape_type == MSO_SHAPE_TYPE.PICTURE]) == 1 and not visible_text
	else:
		assert visible_text == {"Text", "Chart"}


#============================================
def test_title_only_still_requires_its_h1_before_mutating_a_slide(tmp_path: pathlib.Path) -> None:
	"""Titleless support does not weaken the intentionally title-only layout."""
	location = slide_lib.native_model.SourceLocation(tmp_path / "missing-title.ir", 7)
	source = slide_lib.native_model.Slide(location, "title-only", False, (), (), ())
	deck = slide_lib.native_model.Deck(location.path, tmp_path, tmp_path, "Titleless", False, (source,), {})
	presentation = Presentation()
	slide = presentation.slides.add_slide(presentation.slide_layouts[6])
	with pytest.raises(ValueError, match=r"missing-title\.ir:7:.*require exactly one level-one title"):
		layouts.render_layout(slide, source, deck)
	assert not slide.shapes


#============================================
def test_native_table_keeps_headers_blank_cells_and_editable_runs(tmp_path: pathlib.Path) -> None:
	"""A typed table remains one native, selectable table rather than a flattened picture."""
	location = slide_lib.native_model.SourceLocation(tmp_path / "table.ir", 7)
	title = slide_lib.native_model.Heading(location, 1, (slide_lib.native_model.Text("Results"),))
	table = slide_lib.native_model.Table(location, (
		(slide_lib.native_model.Strong((slide_lib.native_model.Text("Condition"),)),),
		(slide_lib.native_model.Text("Value"),),
	), (
		((slide_lib.native_model.Text("Control"),), (slide_lib.native_model.Text(""),)),
		((slide_lib.native_model.Text("Treatment"),), (slide_lib.native_model.Link(
			(slide_lib.native_model.Text("Readout"),), "https://example.test/readout"),)),
	))
	source = native_slide((title, table))
	deck = slide_lib.native_model.Deck(location.path, tmp_path, tmp_path, "Tables", False, (source,), {})
	presentation = Presentation()
	slide = presentation.slides.add_slide(presentation.slide_layouts[6])
	layouts.render_layout(slide, source, deck)
	table_shapes = [shape.table for shape in slide.shapes if shape.has_table]
	assert len(table_shapes) == 1
	assert [(cell.text, bool(cell.text_frame.paragraphs[0].runs[0].font.bold),
		cell.text_frame.paragraphs[0].runs[0].hyperlink.address)
		for row in table_shapes[0].rows for cell in row.cells] == [
		("Condition", True, None), ("Value", True, None), ("Control", False, None),
		("", False, None), ("Treatment", False, None),
		("Readout", False, "https://example.test/readout"),
	]


#============================================
def test_mixed_table_content_fails_before_mutating_a_slide(tmp_path: pathlib.Path) -> None:
	"""A table's one-destination contract diagnoses the mixed authored block."""
	table_location = slide_lib.native_model.SourceLocation(tmp_path / "mixed-table.ir", 7)
	paragraph_location = slide_lib.native_model.SourceLocation(tmp_path / "mixed-table.ir", 10)
	title = slide_lib.native_model.Heading(table_location, 1, (slide_lib.native_model.Text("Results"),))
	table = slide_lib.native_model.Table(table_location, ((slide_lib.native_model.Text("Header"),),), (
		((slide_lib.native_model.Text("Value"),),),))
	paragraph = slide_lib.native_model.Paragraph(paragraph_location, (slide_lib.native_model.Text("Context"),))
	source = native_slide((title, table, paragraph))
	deck = slide_lib.native_model.Deck(table_location.path, tmp_path, tmp_path, "Tables", False, (source,), {})
	presentation = Presentation()
	slide = presentation.slides.add_slide(presentation.slide_layouts[6])
	with pytest.raises(ValueError, match=r"mixed-table\.ir:10:.*table cannot mix"):
		layouts.render_layout(slide, source, deck)
	assert not slide.shapes


#============================================
@pytest.mark.parametrize(("case", "line", "message"), (
	("second", 10, "supports one table"),
	("ragged", 7, "same number of columns"),
	("zero-column", 7, "at least one column"),
	("no-destination", 7, "do not have a native table destination"),
))
def test_table_contract_boundaries_fail_before_mutating_a_slide(tmp_path: pathlib.Path,
		case: str, line: int, message: str) -> None:
	"""Unsupported table destinations and shapes fail at their authored source."""
	path = tmp_path / f"{case}.ir"
	table_location = slide_lib.native_model.SourceLocation(path, 7)
	second_location = slide_lib.native_model.SourceLocation(path, 10)
	title = slide_lib.native_model.Heading(table_location, 1, (slide_lib.native_model.Text("Results"),))
	table = slide_lib.native_model.Table(table_location, ((slide_lib.native_model.Text("Header"),),), (
		((slide_lib.native_model.Text("Value"),),),))
	if case == "second":
		source = native_slide((title, table, slide_lib.native_model.Table(second_location,
			((slide_lib.native_model.Text("Header"),),), (((slide_lib.native_model.Text("Later"),),),))))
	elif case == "ragged":
		ragged = slide_lib.native_model.Table(table_location, (
			(slide_lib.native_model.Text("First"),), (slide_lib.native_model.Text("Second"),),),
			(((slide_lib.native_model.Text("Only"),),),))
		source = native_slide((title, ragged))
	elif case == "zero-column":
		source = native_slide((title, slide_lib.native_model.Table(table_location, (), ())))
	else:
		source = slide_lib.native_model.Slide(table_location, "title-only", False, (),
			(title, table), ())
	deck = slide_lib.native_model.Deck(path, tmp_path, tmp_path, "Tables", False, (source,), {})
	presentation = Presentation()
	slide = presentation.slides.add_slide(presentation.slide_layouts[6])
	with pytest.raises(ValueError, match=rf"{case}\.ir:{line}:.*{message}"):
		layouts.render_layout(slide, source, deck)
	assert not slide.shapes


#============================================
def test_named_slots_keep_their_tables_as_distinct_native_shapes(tmp_path: pathlib.Path) -> None:
	"""Separate table cells retain separately selectable table objects."""
	location = slide_lib.native_model.SourceLocation(tmp_path / "two-tables.ir", 7)
	title = slide_lib.native_model.Heading(location, 1, (slide_lib.native_model.Text("Comparison"),))
	def table(value: str) -> slide_lib.native_model.Table:
		return slide_lib.native_model.Table(location, ((slide_lib.native_model.Text("Header"),),), (
			((slide_lib.native_model.Text(value),),),))
	source = slide_lib.native_model.Slide(location, "two-panels", False, (), (title,), (
		slide_lib.native_model.Cell(location, (table("Left"),), "left"),
		slide_lib.native_model.Cell(location, (table("Right"),), "right"),
	))
	deck = slide_lib.native_model.Deck(location.path, tmp_path, tmp_path, "Tables", False, (source,), {})
	presentation = Presentation()
	slide = presentation.slides.add_slide(presentation.slide_layouts[6])
	layouts.render_layout(slide, source, deck)
	tables = [shape.table for shape in slide.shapes if shape.has_table]
	assert len(tables) == 2
	assert [table.cell(1, 0).text for table in tables] == ["Left", "Right"]


#============================================
def test_titleless_table_readability_fails_before_mutating_a_slide(tmp_path: pathlib.Path) -> None:
	"""A body-only overfull table fails rather than reducing native text below 14px."""
	location = slide_lib.native_model.SourceLocation(tmp_path / "dense-table.ir", 7)
	cell = (slide_lib.native_model.Text(" ".join("adaptable" for _ in range(100))),)
	table = slide_lib.native_model.Table(location, ((slide_lib.native_model.Text("Header"),),),
		tuple((cell,) for _ in range(30)))
	source = native_slide((table,))
	deck = slide_lib.native_model.Deck(location.path, tmp_path, tmp_path, "Tables", False, (source,), {})
	presentation = Presentation()
	slide = presentation.slides.add_slide(presentation.slide_layouts[6])
	with pytest.raises(ValueError, match=r"dense-table\.ir:7:.*table cannot fit"):
		layouts.render_layout(slide, source, deck)
	assert not slide.shapes


#============================================
def test_two_panel_title_and_cells_remain_editable_and_nonoverlapping(tmp_path: pathlib.Path) -> None:
	"""A normal title preserves independently editable, non-overlapping native cells."""
	deck_path = tmp_path / "planned-two-panels.djot"
	deck_path.write_text("=== layout: two-panels\n# Overview\n@left\n- Left\n@right\n- Right\n",
		encoding="utf-8")
	output_path = tmp_path / "planned-two-panels.pptx"
	slide_lib.native_export.render_native_pptx(slide_lib.native_export.parse_deck(deck_path), output_path)
	shapes = [shape for shape in Presentation(output_path).slides[0].shapes if shape.has_text_frame]
	title = next(shape for shape in shapes if shape.text == "Overview")
	cells = [shape for shape in shapes if shape.text in ("Left", "Right")]
	assert all(title.top + title.height <= cell.top for cell in cells)


#============================================
@pytest.mark.parametrize("name", ["vertical-text-panel", "vertical-panel",
	"two-panels-vertical-clipart"])
def test_vertical_layouts_write_editable_ooxml_text_direction(tmp_path: pathlib.Path, name: str) -> None:
	"""Vertical layouts use editable text-body direction rather than a raster image."""
	spec = layouts.LAYOUTS[name]
	deck_path = tmp_path / f"{name}.djot"
	deck_path.write_text(layout_source(name, spec), encoding="utf-8")
	output_path = tmp_path / f"{name}.pptx"
	slide_lib.native_export.render_native_pptx(slide_lib.native_export.parse_deck(deck_path), output_path)
	shape_xml = "".join(shape.element.xml for shape in Presentation(output_path).slides[0].shapes)
	assert 'vert="vert"' in shape_xml


#============================================
def test_gallery_images_keep_descriptions_and_are_not_full_slide(tmp_path: pathlib.Path) -> None:
	"""Gallery components retain their independent descriptions after PPTX export."""
	write_png(tmp_path / "one.png")
	write_png(tmp_path / "two.png")
	deck_path = tmp_path / "gallery.djot"
	deck_path.write_text("=== layout: gallery\n# Components\n@gallery\n"
		"![First component](one.png)\n![Second component](two.png)\n", encoding="utf-8")
	output_path = tmp_path / "gallery.pptx"
	slide_lib.native_export.render_native_pptx(slide_lib.native_export.parse_deck(deck_path), output_path)
	presentation = Presentation(output_path)
	pictures = [shape for shape in presentation.slides[0].shapes
		if shape.shape_type == MSO_SHAPE_TYPE.PICTURE]
	assert [picture.element.nvPicPr.cNvPr.get("descr") for picture in pictures] == [
		"First component", "Second component",
	]
	assert all(picture.width < presentation.slide_width and picture.height < presentation.slide_height
		for picture in pictures)


#============================================
def test_one_panel_can_normalize_multiple_legitimate_images_natively(tmp_path: pathlib.Path) -> None:
	"""Standard content can retain several source images without a composite raster."""
	write_png(tmp_path / "one.png")
	write_png(tmp_path / "two.png")
	deck_path = tmp_path / "native-images.djot"
	deck_path.write_text("=== layout: one-panel\n# Native images\n@body\n"
		"![First component](one.png)\n![Second component](two.png)\n", encoding="utf-8")
	output_path = tmp_path / "native-images.pptx"
	slide_lib.native_export.render_native_pptx(slide_lib.native_export.parse_deck(deck_path), output_path)
	pictures = [shape for shape in Presentation(output_path).slides[0].shapes
		if shape.shape_type == MSO_SHAPE_TYPE.PICTURE]
	assert [picture.element.nvPicPr.cNvPr.get("descr") for picture in pictures] == [
		"First component", "Second component",
	]
	assert all(picture.width < Presentation(output_path).slide_width for picture in pictures)


#============================================
@pytest.mark.parametrize(("case", "line", "message"), (
	("table-image", 10, "table cannot mix with Image"),
	("multiple-choice-second-image", 10, "supports one optional top component image"),
	("multiple-choice-nonfirst-image", 10, "must be the first question block"),
))
def test_flow_boundaries_reject_ambiguous_image_modes_before_shapes(tmp_path: pathlib.Path,
		case: str, line: int, message: str) -> None:
	"""Table/image and invalid MC image order have no native destination ambiguity."""
	path = tmp_path / f"{case}.ir"
	first = slide_lib.native_model.SourceLocation(path, 7)
	second = slide_lib.native_model.SourceLocation(path, 10)
	image = slide_lib.native_model.Image(second, "Component", "component.png", None)
	if case == "table-image":
		table = slide_lib.native_model.Table(first, ((slide_lib.native_model.Text("Header"),),), (
			((slide_lib.native_model.Text("Value"),),),))
		source = native_slide((table, image))
	else:
		choice = slide_lib.native_model.ListBlock(first, False, 1, (
			slide_lib.native_model.ListItem(first, (slide_lib.native_model.Text("A. Choice"),)),))
		question_blocks = (image, image, choice) if case.endswith("second-image") else (choice, image)
		answer = slide_lib.native_model.Cell(first, (
			slide_lib.native_model.Paragraph(first, (slide_lib.native_model.Text("Answer"),)),), "answer")
		source = slide_lib.native_model.Slide(first, "multiple-choice", False, (), (), (
			slide_lib.native_model.Cell(first, question_blocks, "question"), answer))
	deck = slide_lib.native_model.Deck(path, tmp_path, tmp_path, "Flow", False, (source,), {})
	presentation = Presentation()
	slide = presentation.slides.add_slide(presentation.slide_layouts[6])
	with pytest.raises(ValueError, match=rf"{case}\.ir:{line}:.*{message}"):
		layouts.render_layout(slide, source, deck)
	assert not slide.shapes


#============================================
def test_native_layout_rejects_nested_bare_attributes_at_their_source() -> None:
	"""Nested bare attributes receive a source-located native-layout diagnostic."""
	location = slide_lib.native_model.SourceLocation(pathlib.Path("nested.ir"), 11)
	nested_item = slide_lib.native_model.ListItem(location, (slide_lib.native_model.Text("Body"),),
		attributes=(slide_lib.native_model.Attribute("bare"),))
	nested_list = slide_lib.native_model.ListBlock(location, False, 1, (nested_item,))
	root_item = slide_lib.native_model.ListItem(location, (slide_lib.native_model.Text("Parent"),),
		children=(nested_list,))
	root_list = slide_lib.native_model.ListBlock(location, False, 1, (root_item,))
	with pytest.raises(ValueError, match=r"nested\.ir:11:.*attributes on ListItem"):
		layouts.validate_layout_source(native_slide((root_list,)))


#============================================
def test_native_layout_rejects_quote_blocks_at_their_source() -> None:
	"""Quote blocks retain the explicit unsupported-block diagnostic."""
	location = slide_lib.native_model.SourceLocation(pathlib.Path("quote.ir"), 19)
	quote = slide_lib.native_model.QuoteBlock(location, ())
	with pytest.raises(ValueError, match=r"quote\.ir:19:.*QuoteBlock blocks"):
		layouts.validate_layout_source(native_slide((quote,)))


#============================================
def test_native_layout_rejects_nested_inline_math_at_its_source() -> None:
	"""Inline math in nested formatted list content waits for a native adapter."""
	title_location = slide_lib.native_model.SourceLocation(pathlib.Path("math.ir"), 1)
	math_location = slide_lib.native_model.SourceLocation(pathlib.Path("math.ir"), 9)
	math = slide_lib.native_model.InlineMath("x^2")
	formatted = slide_lib.native_model.Strong((slide_lib.native_model.Emphasis((
		slide_lib.native_model.Link((math,), "https://example.test/math"),)),))
	nested_item = slide_lib.native_model.ListItem(math_location, (formatted,))
	nested_list = slide_lib.native_model.ListBlock(math_location, False, 1, (nested_item,))
	root_item = slide_lib.native_model.ListItem(math_location, (slide_lib.native_model.Text("Parent"),),
		children=(nested_list,))
	root_list = slide_lib.native_model.ListBlock(math_location, False, 1, (root_item,))
	title = slide_lib.native_model.Heading(title_location, 1, (slide_lib.native_model.Text("Title"),))
	with pytest.raises(ValueError, match=r"math\.ir:9:.*InlineMath until a native math adapter exists"):
		layouts.validate_layout_source(native_slide((title, root_list)))


#============================================
def test_missing_component_image_reports_its_authored_image_line(tmp_path: pathlib.Path) -> None:
	"""Image-resolution failures retain the precise component image location."""
	deck_path = tmp_path / "missing-image.djot"
	deck_path.write_text("=== layout: one-panel\n# Missing\n@body\n"
		"![Absent component](absent.png)\n", encoding="utf-8")
	with pytest.raises(ValueError, match=r"missing-image\.djot:4:.*component image is missing"):
		slide_lib.native_export.render_native_pptx(slide_lib.native_export.parse_deck(deck_path),
			tmp_path / "missing-image.pptx")


#============================================
@pytest.mark.parametrize("name", ["vertical-text-panel", "vertical-panel"])
@pytest.mark.parametrize("body", ["Vertical paragraph\n", "- Vertical list item\n"])
def test_vertical_root_body_layouts_accept_one_text_block(tmp_path: pathlib.Path, name: str,
		body: str) -> None:
	"""Each root-body vertical layout creates exactly one editable vertical body frame."""
	deck_path = tmp_path / f"{name}.djot"
	deck_path.write_text(f"=== layout: {name}\n# Vertical\n@body\n" + body, encoding="utf-8")
	output_path = tmp_path / f"{name}.pptx"
	slide_lib.native_export.render_native_pptx(slide_lib.native_export.parse_deck(deck_path), output_path)
	vertical_frames = [shape for shape in Presentation(output_path).slides[0].shapes if shape.has_text_frame
		and 'vert="vert"' in shape.element.xml and shape.text != "Vertical"]
	assert len(vertical_frames) == 1


#============================================
@pytest.mark.parametrize("name", ["vertical-text-panel", "vertical-panel"])
def test_vertical_root_body_layouts_accept_one_component_image(tmp_path: pathlib.Path, name: str) -> None:
	"""A single component image is the legal native picture form of a vertical body."""
	write_png(tmp_path / "component.png")
	deck_path = tmp_path / f"{name}-image.djot"
	deck_path.write_text(f"=== layout: {name}\n# Vertical\n@body\n"
		"![Vertical component](component.png)\n", encoding="utf-8")
	output_path = tmp_path / f"{name}-image.pptx"
	slide_lib.native_export.render_native_pptx(slide_lib.native_export.parse_deck(deck_path), output_path)
	pictures = [shape for shape in Presentation(output_path).slides[0].shapes
		if shape.shape_type == MSO_SHAPE_TYPE.PICTURE]
	assert len(pictures) == 1


#============================================
@pytest.mark.parametrize("name", ["vertical-text-panel", "vertical-panel"])
def test_vertical_root_body_layouts_reject_multiple_blocks_at_the_second_block(tmp_path: pathlib.Path,
		name: str) -> None:
	"""A second root body block receives its own actionable source location."""
	deck_path = tmp_path / f"{name}-invalid.djot"
	deck_path.write_text(f"=== layout: {name}\n# Vertical\n@body\nFirst paragraph\n\n- Second block\n",
		encoding="utf-8")
	with pytest.raises(ValueError, match=rf"{name}-invalid\.djot:6:.*exactly one body block"):
		slide_lib.native_export.render_native_pptx(slide_lib.native_export.parse_deck(deck_path),
			tmp_path / "invalid.pptx")


#============================================
@pytest.mark.parametrize(("names", "message"), [
	(("left", "left"), "duplicate cell slot"),
	(("left", "other"), "unknown slot"),
	(("left", None), "must name a declared slot"),
])
def test_layout_validation_rejects_invalid_named_cells_at_their_source(
		names: tuple[str | None, str | None], message: str) -> None:
	"""Direct IR cannot bypass the named-slot contract used by rendering."""
	location = slide_lib.native_model.SourceLocation(pathlib.Path("named.ir"), 7)
	title = slide_lib.native_model.Heading(location, 1, (slide_lib.native_model.Text("Title"),))
	body = slide_lib.native_model.Paragraph(location, (slide_lib.native_model.Text("Text"),))
	source = slide_lib.native_model.Slide(location, "two-panels", False, (), (title,), (
		slide_lib.native_model.Cell(location, (body,), names[0]),
		slide_lib.native_model.Cell(location, (body,), names[1]),
	))
	with pytest.raises(ValueError, match=rf"named\.ir:7:.*{message}"):
		layouts.validate_layout_source(source)


#============================================
def test_named_cells_render_in_their_declared_slots_not_source_order(tmp_path: pathlib.Path) -> None:
	"""Named cells retain their semantic positions when their source order changes."""
	location = slide_lib.native_model.SourceLocation(tmp_path / "named.ir", 1)
	title = slide_lib.native_model.Heading(location, 1, (slide_lib.native_model.Text("Title"),))
	cells_by_name = tuple(slide_lib.native_model.Cell(location, (
		slide_lib.native_model.Paragraph(location, (slide_lib.native_model.Text(name),)),), name)
		for name in ("bottom-right", "left", "top-right"))
	source = slide_lib.native_model.Slide(location, "one-plus-two-panels", False, (), (title,), cells_by_name)
	deck = slide_lib.native_model.Deck(location.path, tmp_path, tmp_path, "Named slots", False, (source,), {})
	output_path = tmp_path / "named-slots.pptx"
	slide_lib.native_export.render_native_pptx(deck, output_path)
	placements = {shape.text: (shape.left, shape.top) for shape in Presentation(output_path).slides[0].shapes
		if shape.has_text_frame and shape.text in ("left", "top-right", "bottom-right")}
	assert placements["left"][0] < placements["top-right"][0] and \
		placements["top-right"][1] < placements["bottom-right"][1]


#============================================
def test_multiple_choice_renders_a_native_question_and_answer_popup(tmp_path: pathlib.Path) -> None:
	"""The automatic answer remains one editable popup object beside its visible question."""
	location = slide_lib.native_model.SourceLocation(tmp_path / "choice.ir", 7)
	question = slide_lib.native_model.Cell(location, (
		slide_lib.native_model.Paragraph(location, (slide_lib.native_model.Text("Which molecule stores heredity?"),)),
		slide_lib.native_model.ListBlock(location, False, 1, (
			slide_lib.native_model.ListItem(location, (slide_lib.native_model.Text("A. Lipid"),)),
			slide_lib.native_model.ListItem(location, (slide_lib.native_model.Text("B. DNA"),)),
		)),
	), "question")
	implicit_appear = slide_lib.native_model.Reveal(slide_lib.native_model.RevealEffect.APPEAR,
		slide_lib.native_model.RevealSequence.OBJECT)
	answer = slide_lib.native_model.Cell(location, (
		slide_lib.native_model.Paragraph(location, (slide_lib.native_model.Text("Answer: B. DNA"),), implicit_appear),
		slide_lib.native_model.Paragraph(location, (slide_lib.native_model.Text("DNA stores hereditary information."),)),
	), "answer")
	source = slide_lib.native_model.Slide(location, "multiple-choice", False, (), (), (question, answer))
	deck = slide_lib.native_model.Deck(location.path, tmp_path, tmp_path, "Choice", False, (source,), {})
	output_path = tmp_path / "choice.pptx"
	slide_lib.native_export.render_native_pptx(deck, output_path)
	shapes = [shape for shape in Presentation(output_path).slides[0].shapes if shape.has_text_frame]
	popups = [shape for shape in shapes if shape.text == "Answer: B. DNA\nDNA stores hereditary information."]
	assert len(popups) == 1


#============================================
@pytest.mark.parametrize(("case", "line", "message"), [
	("paragraph-only", 11, "at least one visible editable choice ListBlock"),
	("empty", 7, "at least one visible editable choice ListBlock"),
	("heading", 13, "at least one visible editable choice ListBlock"),
	("global-content", 3, "do not accept source-global title, subtitle, or body blocks"),
	("question-reveal", 17, "question content is visible when the slide opens"),
	("answer-reveal", 19, "only accepts its implicit on-click object appear reveal"),
])
def test_multiple_choice_rejects_invalid_source_at_the_authored_location(
		case: str, line: int, message: str) -> None:
	"""Question, global, and reveal contracts identify the authored offending block."""
	path = pathlib.Path("choice.ir")
	question_location = slide_lib.native_model.SourceLocation(path, 7)
	paragraph_location = slide_lib.native_model.SourceLocation(path, 11)
	heading_location = slide_lib.native_model.SourceLocation(path, 13)
	list_location = slide_lib.native_model.SourceLocation(path, 17)
	answer_location = slide_lib.native_model.SourceLocation(path, 19)
	choices = slide_lib.native_model.ListBlock(list_location, False, 1, (
		slide_lib.native_model.ListItem(list_location, (slide_lib.native_model.Text("A. Lipid"),)),
	))
	if case == "paragraph-only":
		question_blocks = (slide_lib.native_model.Paragraph(paragraph_location,
			(slide_lib.native_model.Text("Which molecule?"),)),)
	elif case == "empty":
		question_blocks = ()
	elif case == "heading":
		question_blocks = (slide_lib.native_model.Heading(heading_location, 2,
			(slide_lib.native_model.Text("Which molecule?"),)),)
	else:
		question_blocks = (choices,)
	if case == "question-reveal":
		question_blocks = (slide_lib.native_model.ListBlock(list_location, False, 1, choices.items,
			slide_lib.native_model.Reveal(slide_lib.native_model.RevealEffect.APPEAR,
				slide_lib.native_model.RevealSequence.OBJECT)),)
	answer_reveal = slide_lib.native_model.Reveal(slide_lib.native_model.RevealEffect.APPEAR,
		slide_lib.native_model.RevealSequence.PARAGRAPHS) if case == "answer-reveal" else None
	answer = slide_lib.native_model.Cell(answer_location, (
		slide_lib.native_model.Paragraph(answer_location, (slide_lib.native_model.Text("Answer: DNA"),), answer_reveal),
	), "answer")
	root_blocks = (slide_lib.native_model.Paragraph(slide_lib.native_model.SourceLocation(path, 3),
		(slide_lib.native_model.Text("Global"),)),) if case == "global-content" else ()
	source = slide_lib.native_model.Slide(question_location, "multiple-choice", False, (), root_blocks, (
		slide_lib.native_model.Cell(question_location, question_blocks, "question"), answer))
	with pytest.raises(ValueError, match=rf"choice\.ir:{line}:.*{message}"):
		layouts.validate_layout_source(source)


#============================================
def test_multiple_choice_reports_the_forbidden_question_block_location() -> None:
	"""A valid choice list does not hide the later forbidden heading location."""
	path = pathlib.Path("choice.ir")
	question_location = slide_lib.native_model.SourceLocation(path, 7)
	choice_location = slide_lib.native_model.SourceLocation(path, 11)
	heading_location = slide_lib.native_model.SourceLocation(path, 13)
	answer_location = slide_lib.native_model.SourceLocation(path, 17)
	choices = slide_lib.native_model.ListBlock(choice_location, False, 1, (
		slide_lib.native_model.ListItem(choice_location, (slide_lib.native_model.Text("A. Lipid"),)),
	))
	heading = slide_lib.native_model.Heading(heading_location, 2, (slide_lib.native_model.Text("Nope"),))
	question = slide_lib.native_model.Cell(question_location, (choices, heading), "question")
	answer = slide_lib.native_model.Cell(answer_location, (
		slide_lib.native_model.Paragraph(answer_location, (slide_lib.native_model.Text("Answer: DNA"),)),
	), "answer")
	source = slide_lib.native_model.Slide(question_location, "multiple-choice", False, (), (),
		(question, answer))
	with pytest.raises(ValueError, match=r"choice\.ir:13:.*optional prompt paragraph"):
		layouts.validate_layout_source(source)


#============================================
def test_title_slide_keeps_multiple_subtitle_lines_in_one_text_shape(tmp_path: pathlib.Path) -> None:
	"""Consecutive level-two source headings share the title slide's subtitle region."""
	deck_path = tmp_path / "multiple-subtitles.djot"
	deck_path.write_text("=== layout: title-slide\n# Title\n## First subtitle\n## Second subtitle\n",
		encoding="utf-8")
	output_path = tmp_path / "multiple-subtitles.pptx"
	slide_lib.native_export.render_native_pptx(slide_lib.native_export.parse_deck(deck_path), output_path)
	subtitle_shapes = [shape for shape in Presentation(output_path).slides[0].shapes if shape.has_text_frame
		and "First subtitle" in shape.text]
	assert len(subtitle_shapes) == 1 and "Second subtitle" in subtitle_shapes[0].text


#============================================
def test_presentation_chain_converts_odp_to_pdf(tmp_path: pathlib.Path) -> None:
	"""PDF export uses ODP as its required LibreOffice predecessor."""
	deck_path = tmp_path / "chain.djot"
	deck_path.write_text("=== layout: one-panel\n# Chain\n@body\n- Editable body\n", encoding="utf-8")
	with mock.patch.object(slide_lib.native_export, "find_repo_root", return_value=tmp_path), \
		mock.patch.object(slide_lib.native_export, "render_template_odp"), \
		mock.patch.object(slide_lib.native_export, "convert_presentation"):
		outputs = slide_lib.native_export.export_deck(str(deck_path), "pdf")
	assert list(outputs) == ["pptx", "odp", "pdf"]


#============================================
def test_folder_discovery_selects_sorted_supported_descendants(tmp_path: pathlib.Path) -> None:
	"""Folder builds recursively retain only Djot decks in stable relative-path order."""
	folder = tmp_path / "slides"
	folder.mkdir()
	(folder / "z_deck.djot").write_text("=== layout: blank\n", encoding="utf-8")
	(folder / "notes.md").write_text("# Notes\n", encoding="utf-8")
	(folder / "a_deck.djot").write_text("=== layout: blank\n", encoding="utf-8")
	nested = folder / "nested"
	nested.mkdir()
	(nested / "hidden_deck.djot").write_text("=== layout: blank\n", encoding="utf-8")
	(nested / "imported.odp").write_text("not a source deck\n", encoding="utf-8")
	decks = slide_lib.native_export.discover_decks(str(folder), tmp_path)
	assert [path.relative_to(folder).as_posix() for path in decks] == [
		"a_deck.djot", "nested/hidden_deck.djot", "z_deck.djot"]


#============================================
def test_validate_input_rejects_markdown_source(tmp_path: pathlib.Path) -> None:
	"""The public build boundary accepts Djot source only."""
	markdown_path = tmp_path / "deck.md"
	markdown_path.write_text("# Not a deck\n", encoding="utf-8")
	with pytest.raises(ValueError, match="use the .djot extension"):
		slide_lib.native_export.validate_input(str(markdown_path), tmp_path)


#============================================
def test_folder_discovery_rejects_an_empty_source_selection(tmp_path: pathlib.Path) -> None:
	"""A folder tree without a presentation source receives an actionable input error."""
	folder = tmp_path / "slides"
	folder.mkdir()
	(folder / "notes.md").write_text("---\ntitle: Notes\n---\n", encoding="utf-8")
	with pytest.raises(ValueError, match="no presentation source decks found"):
		slide_lib.native_export.discover_decks(str(folder), tmp_path)


#============================================
def test_export_progress_follows_artifact_dependency_order(tmp_path: pathlib.Path) -> None:
	"""Progress reports parsing before the unchanged PPTX, ODP, and PDF chain."""
	deck_path = tmp_path / "stages.djot"
	deck_path.write_text("=== layout: blank\n", encoding="utf-8")
	stages: list[str] = []
	with mock.patch.object(slide_lib.native_export, "find_repo_root", return_value=tmp_path), \
		mock.patch.object(slide_lib.native_export, "render_template_odp"), \
		mock.patch.object(slide_lib.native_export, "convert_presentation"):
		slide_lib.native_export.export_deck(str(deck_path), "all", stages.append)
	assert stages == ["parsing", "pptx", "odp", "pdf"]
