"""Native table layout contracts for sizing, grouped reveals, spans, and formatting."""

import pathlib

import pytest

import slide_lib.layout_table_measurement
import slide_lib.djot_audit
import slide_lib.layout_content
import slide_lib.layout_measurement
import slide_lib.layout_primitives
import slide_lib.presentation_theme
import layout_test_helpers


def test_authored_table_proportions_stay_fixed_when_cell_text_changes(tmp_path: pathlib.Path) -> None:
	"""Question and answer tables keep the same column boundaries during a reveal sequence."""
	slides = []
	for text in ("?", "A1A3: BOTH"):
		slides.append("=== layout: one-panel\n\n@body\n\n"
			'{column-widths="1,3,3"}\n| | A3 | A4 |\n| --- | --- | --- |\n'
			f"| A1 | {text} | Neither |\n")
	result = layout_test_helpers.compile_source(tmp_path, "\n".join(slides))
	tables = [next(item.content for item in slide.objects
		if isinstance(item.content, slide_lib.layout_content.TableContent))
		for slide in result.plan.slides]
	assert tables[0].column_widths == tables[1].column_widths
	first, second, third = tables[0].column_widths
	assert second == pytest.approx(3 * first) and third == second


def test_table_group_uses_later_content_without_affecting_other_tables(tmp_path: pathlib.Path) -> None:
	"""A group measures the whole sequence, adapts to edits, and stays scoped to one compile."""
	prefix = '=== layout: one-panel\n\n@body\n\n{table-group="cross"}\n'
	header = "| | A3 | A4 |\n| --- | --- | --- |\n"
	question = prefix + header + "| A1 | ? | ? |\n"
	widths = []
	for answer in ("Both", "A much longer explanation of the shared outcome"):
		later = prefix + header + f"| A1 | {answer} | Neither |\n"
		ordinary = question.replace('{table-group="cross"}\n', "")
		result = layout_test_helpers.compile_source(tmp_path, "\n".join((question, later, ordinary)))
		tables = [next(item.content for item in slide.objects
			if isinstance(item.content, slide_lib.layout_content.TableContent))
			for slide in result.plan.slides]
		assert tables[0].column_widths == tables[1].column_widths
		widths.append((tables[0].column_widths, tables[2].column_widths))
	assert widths[1][0][1] > widths[0][0][1]
	assert widths[0][1] == widths[1][1]
	# Recompiling the short version must not retain the previous deck's wider group.
	short = layout_test_helpers.compile_source(tmp_path, question + "\n" + prefix + header + "| A1 | Both | Neither |\n")
	assert short.plan.slides[0].objects[0].content.column_widths == widths[0][0]


def test_table_group_rejects_incompatible_column_counts(tmp_path: pathlib.Path) -> None:
	"""Grouping unrelated table shapes produces an actionable source error."""
	source = '=== layout: one-panel\n\n@body\n\n{table-group="cross"}\n'
	with pytest.raises(ValueError, match="table-group 'cross' requires 2 columns, found 3"):
		layout_test_helpers.compile_source(tmp_path, source + "| A | B |\n\n" + source + "| A | B | C |\n")


def test_table_serializes_content_dependent_row_heights(tmp_path: pathlib.Path) -> None:
	"""A wrapped row receives more native height than a one-line row."""
	result = layout_test_helpers.compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\n"
		"| Label | Explanation |\n| - | - |\n| Short | Fits |\n"
		"| Long | This explanation wraps across several lines because it contains substantially more text than the short row. |")
	table = next(item.content for item in result.plan.slides[0].objects
		if isinstance(item.content, slide_lib.layout_content.TableContent))
	assert table.row_heights[-1] > table.row_heights[-2]


def test_table_allocates_more_width_to_a_content_heavy_column(tmp_path: pathlib.Path) -> None:
	"""Measured content controls native column widths without changing the table frame."""
	result = layout_test_helpers.compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\n"
		"| ID | Organism and strain | Cut |\n| - | - | - |\n"
		"| A | Haemophilus haemolyticus | blunt |\n")
	item = next(item for item in result.plan.slides[0].objects
		if isinstance(item.content, slide_lib.layout_content.TableContent))
	assert item.content.column_widths[1] > item.content.column_widths[0]
	assert sum(item.content.column_widths) == pytest.approx(item.rectangle.width)


@pytest.mark.parametrize("separator", ("-", "\u2010", "\u2013"))
def test_table_wraps_compounds_at_hyphens_before_fragmenting_words(
		tmp_path: pathlib.Path, separator: str) -> None:
	"""Native cells retain normal compound breaks and safely fragment genuinely long words."""
	compound = f"hardy{separator}weinberg"
	long_word = "W" * 30
	result = layout_test_helpers.compile_source(tmp_path, "=== layout: one-panel\n@body\n"
		'{column-widths="1,5"}\n| Label | Value |\n| - | - |\n'
		f"| {compound} | 0.234 |\n| {long_word} | 0.499 |\n")
	table = next(item.content for item in result.plan.slides[0].objects
		if isinstance(item.content, slide_lib.layout_content.TableContent))
	theme = slide_lib.presentation_theme.default_theme()
	session = slide_lib.layout_measurement.MeasurementSession(theme)
	for row, text in zip(table.body_rows, (compound, long_word)):
		cell = row.cells[0]
		paragraph = cell.paragraphs[0]
		insets = slide_lib.layout_table_measurement.cell_content_insets(
			cell.padding, cell.borders, theme)
		width = table.column_widths[0] - insets.left - insets.right
		lines = slide_lib.djot_audit.paragraph_lines(paragraph, width, session)
		assert "".join(line for line, _width in lines) == text
		assert all(ink_width <= width for _line, ink_width in lines)
		if text == compound:
			assert [line for line, _width in lines] == [f"hardy{separator}", "weinberg"]
			assert not any(isinstance(run, slide_lib.layout_content.LineBreak)
				for run in paragraph.inlines)
		else:
			assert len(lines) > 1
			assert any(isinstance(run, slide_lib.layout_content.LineBreak)
				for run in paragraph.inlines)


def test_numeric_table_alignment_and_total_emphasis(tmp_path: pathlib.Path) -> None:
	"""Keep numeric columns readable and totals distinct without changing cell text."""
	result = layout_test_helpers.compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\n"
		"| Class | O-E | Value |\n| --- | --- | --- |\n"
		"| A-B- | -1 | 0.033 |\n| C | -5 | 0.111 |\n| D | &#8211;15 | 1.000 |\n"
		"| E | -150 | 10.00 |\n| Total | 0 | 0.178 |\n")
	table = next(item.content for item in result.plan.slides[0].objects
		if isinstance(item.content, slide_lib.layout_content.TableContent))
	for row in table.header_rows:
		for cell in row.cells:
			assert cell.paragraphs[0].properties.horizontal_alignment is \
				slide_lib.layout_primitives.HorizontalAlignment.CENTER
	for row in table.body_rows:
		for cell in row.cells[1:]:
			assert cell.paragraphs[0].properties.horizontal_alignment is \
				slide_lib.layout_primitives.HorizontalAlignment.END
	for cell in table.body_rows[-1].cells:
		assert cell.fill_color == table.header_rows[0].cells[0].fill_color
		assert all(run.style.bold for run in cell.paragraphs[0].inlines
			if isinstance(run, slide_lib.layout_content.TextRun))


def test_resolved_cell_insets_control_rows_and_native_frame(tmp_path: pathlib.Path) -> None:
	"""Asymmetric point padding and side borders share one measured physical geometry."""
	result = layout_test_helpers.compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\n"
		'{padding="2pt 7pt 5pt 11pt" border=none border-left="3pt solid #123456"}\n'
		"| Label | Value |\n| --- | --- |\n| Total | **Bold** `code` H~2~O |\n")
	item = next(item for item in result.plan.slides[0].objects
		if isinstance(item.content, slide_lib.layout_content.TableContent))
	table = item.content
	theme = slide_lib.presentation_theme.default_theme()
	cell = table.body_rows[0].cells[1]
	scale = slide_lib.layout_measurement.point_height(1, theme)
	assert cell.padding == slide_lib.layout_primitives.Insets(11 * scale, 2 * scale, 7 * scale, 5 * scale)
	insets = slide_lib.layout_table_measurement.cell_content_insets(cell.padding, cell.borders, theme)
	assert insets.left == pytest.approx(15 * scale)
	assert table.row_heights[1] == pytest.approx(cell.paragraphs[0].measured_height + 9 * scale)
	assert item.rectangle.height == pytest.approx(sum(table.row_heights))
	runs = cell.paragraphs[0].inlines
	assert all(run.style.bold for run in runs if isinstance(run, slide_lib.layout_content.TextRun))
	assert any(run.style.code for run in runs if isinstance(run, slide_lib.layout_content.TextRun))
	assert any(run.style.position == "sub" for run in runs if isinstance(run, slide_lib.layout_content.TextRun))


def test_grouped_columns_include_later_resolved_padding(tmp_path: pathlib.Path) -> None:
	"""A later padded cell contributes to the stable grid shared by related styles."""
	prefix = '=== layout: one-panel\n\n@body\n\n{table-group=padding table-style=working}\n'
	columns = "| A | B |\n| --- | --- |\n"
	result = layout_test_helpers.compile_source(tmp_path, prefix + columns + "| x | x |\n\n" +
		prefix + columns + '| [x]{padding-right=80pt} | x |\n')
	tables = [next(item.content for item in slide.objects
		if isinstance(item.content, slide_lib.layout_content.TableContent))
		for slide in result.plan.slides]
	assert tables[0].column_widths == tables[1].column_widths
	assert tables[0].column_widths[0] > tables[0].column_widths[1]


def test_merged_total_uses_combined_width_and_explicit_cell_alignment(tmp_path: pathlib.Path) -> None:
	"""Equal gene columns remain equal while the merged total occupies all three."""
	result = layout_test_helpers.compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\n"
		'{column-widths="1,1,1,2"}\n| C | D | H | Count |\n| --- | --- | --- | --- |\n'
		'| [c]{text-align=center} | d | h | 1 |\n'
		'| [Total]{colspan=3 background-color=#80BD80} | 1,400 |\n')
	table = next(item.content for item in result.plan.slides[0].objects
		if isinstance(item.content, slide_lib.layout_content.TableContent))
	assert table.column_widths[0] == table.column_widths[1] == table.column_widths[2]
	assert len(table.body_rows[1].cells) == 2
	assert table.body_rows[1].cells[0].column_span == 3
	assert table.body_rows[0].cells[0].paragraphs[0].properties.horizontal_alignment is \
		slide_lib.layout_primitives.HorizontalAlignment.CENTER
	assert table.body_rows[1].cells[1].paragraphs[0].properties.horizontal_alignment is \
		slide_lib.layout_primitives.HorizontalAlignment.END


def test_grouped_tables_allow_merged_rows_on_the_same_column_grid(tmp_path: pathlib.Path) -> None:
	"""A reveal may merge cells without changing the group's logical column schema."""
	header = '=== layout: one-panel\n\n@body\n\n{table-group="merged"}\n'
	columns = '| C | D | Count |\n| --- | --- | --- |\n'
	result = layout_test_helpers.compile_source(tmp_path, header + columns + '| c | d | ? |\n\n' +
		header + columns + '| [Total]{colspan=2} | 350 |\n')
	tables = [next(item.content for item in slide.objects
		if isinstance(item.content, slide_lib.layout_content.TableContent))
		for slide in result.plan.slides]
	assert tables[0].column_widths == tables[1].column_widths
	assert tables[1].body_rows[0].cells[0].column_span == 2
