"""Contracts for authored table formatting, role resolution, and native shared edges."""

import pathlib
import slide_lib.djot_blocks
import slide_lib.djot_errors
import slide_lib.native_model
import slide_lib.table_styles
import slide_lib.presentation_theme


def test_table_style_cascade_preserves_inline_authorship(tmp_path: pathlib.Path) -> None:
	"""Local defaults beat named regions while cell overrides preserve the authored inline tree."""
	table = slide_lib.djot_blocks.parse_blocks(tmp_path / "styles.djot",
		'{table-style=working background-color=#FFEEDD text-align=left padding="2pt 3pt"}\n'
		"| Item | Count |\n| --- | --- |\n"
		'| [*Cc*]{color=red padding="1pt 2pt 3pt 4pt" padding-left=7pt vertical-align=top} | 1,400 |\n'
		"| Total | [1,400]{background-color=#FFFFFF text-align=center} |\n").blocks[0]
	resolved = slide_lib.table_styles.resolve_table(table,
		slide_lib.presentation_theme.default_theme(), slide_lib.table_styles.load_registry())
	assert table.style_name == "working"
	assert isinstance(table.rows[0][0].inlines[0], slide_lib.native_model.StyledSpan)
	assert isinstance(table.rows[0][0].inlines[0].children[0], slide_lib.native_model.Strong)
	assert resolved.cells[0][0].text_color == "000000"
	assert resolved.cells[0][0].background_color == "FFEEDD"
	assert resolved.cells[1][1].text_alignment == "left"
	assert resolved.cells[1][0].padding_left_pt == 7.0
	assert resolved.cells[1][0].padding_bottom_pt == 3.0
	assert resolved.cells[1][0].vertical_alignment == "top"
	assert resolved.cells[2][1].bold
	assert resolved.cells[2][1].background_color == "FFFFFF"
	assert resolved.cells[2][1].text_alignment == "center"


def test_shared_edges_honor_explicit_none_and_merged_native_sides(tmp_path: pathlib.Path) -> None:
	"""An explicit none suppresses inherited grid on both sides, including a merged perimeter."""
	table = slide_lib.djot_blocks.parse_blocks(tmp_path / "edges.djot",
		"{table-style=working}\n| [Merged]{colspan=2} |\n| --- | --- |\n"
		'| [left]{border-top=none border-right="2pt dashed red"} | right |\n').blocks[0]
	resolved = slide_lib.table_styles.resolve_table(table,
		slide_lib.presentation_theme.default_theme(), slide_lib.table_styles.load_registry())
	assert resolved.cells[0][0].border_bottom.style == "none"
	assert resolved.cells[1][0].border_top.style == "none"
	assert resolved.cells[1][1].border_top.style == "none"
	assert resolved.cells[1][0].border_right == resolved.cells[1][1].border_left
	assert resolved.cells[1][1].border_left.style == "dashed"
	assert resolved.cells[1][1].border_left.color == "C9211E"
