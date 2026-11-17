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
import genetics.LECT11.djot.gene_tree_recipes


#============================================


#============================================
def test_gene_tree_merge_marks_original_pairs_and_centers_each_cell(tmp_path: pathlib.Path) -> None:
	"""The four original distances feeding one average share a cue, regardless of triangle position."""
	recipe = genetics.LECT11.djot.gene_tree_recipes
	pairs = {'ab': 16, 'ac': 6, 'ad': 18, 'bc': 20, 'bd': 10, 'cd': 22}
	source = recipe.matrix(['a', 'b', 'c', 'd'], pairs, 'example', None,
		merging=('b', 'd'), targets=['ac'])
	deck = layout_test_helpers.parsed_source(tmp_path, '=== layout: one-panel\n@body\n' + source)
	table = deck.slides[0].cells[0].blocks[0]
	assert all(cell.formatting.text_alignment == 'center'
		for row in (table.headers, *table.rows) for cell in row)
	assert all(table.rows[row][column].formatting.background_color == '#B8FFF0'
		for row, column in ((1, 1), (2, 2), (3, 1), (3, 3)))
	assert recipe.distance('ac', 'bd', pairs) == 19


#============================================
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


#============================================
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


#============================================
def test_table_group_rejects_incompatible_column_counts(tmp_path: pathlib.Path) -> None:
	"""Grouping unrelated table shapes produces an actionable source error."""
	source = '=== layout: one-panel\n\n@body\n\n{table-group="cross"}\n'
	with pytest.raises(ValueError, match="table-group 'cross' requires 2 columns, found 3"):
		layout_test_helpers.compile_source(tmp_path, source + "| A | B |\n\n" + source + "| A | B | C |\n")


#============================================


#============================================


#============================================


#============================================


#============================================


#============================================
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
