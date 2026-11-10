"""Contracts for authored table formatting, role resolution, and native shared edges."""

import pathlib
import dataclasses

import pytest

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


def test_roles_are_conservative_and_heading_structure_is_authored(tmp_path: pathlib.Path) -> None:
	"""Numeric alignment and total labels are recognized without classifying scientific identities."""
	table = slide_lib.djot_blocks.parse_blocks(tmp_path / "roles.djot",
		"{table-style=testcross}\n| Class | 100 |\n| --- | --- |\n"
		"| Cc | 12.5% |\n| cC | 1e-4 |\n| Grand total | 100 |\n").blocks[0]
	registry = slide_lib.table_styles.load_registry()
	theme = slide_lib.presentation_theme.default_theme()
	resolved = slide_lib.table_styles.resolve_table(table, theme, registry)
	assert resolved.cells[0][1].text_alignment == "center"
	assert resolved.cells[1][0].text_alignment == "center"
	assert not resolved.cells[1][0].bold
	assert resolved.cells[1][1].text_alignment == "center"
	assert resolved.cells[2][1].text_alignment == "center"
	assert resolved.cells[3][0].bold
	no_header = dataclasses.replace(table, headers=(), rows=(table.headers,) + table.rows)
	assert not slide_lib.table_styles.resolve_table(no_header, theme, registry).cells[0][0].bold


@pytest.mark.parametrize("style,normal,numeric", (
	("standard", "left", "right"), ("comparison", "left", "right"),
	("working", "left", "right"), ("testcross", "center", "right"),
	("punnett", "center", "center"),
))
def test_columns_keep_mixed_notation_together(tmp_path: pathlib.Path,
		style: str, normal: str, numeric: str) -> None:
	"""Mixed notation and equations keep preset alignment; numeric columns include blanks."""
	table = slide_lib.djot_blocks.parse_blocks(tmp_path / "columns.djot",
		f"{{table-style={style}}}\n| Part | Count | Symbol | Empty |\n| --- | --- | --- | --- |\n"
		"| 47 | *1,400* | 7 | |\n| XY | -12.5% | $x$ | |\n| +21 | | | |\n").blocks[0]
	resolved = slide_lib.table_styles.resolve_table(table,
		slide_lib.presentation_theme.default_theme(), slide_lib.table_styles.load_registry())
	assert all(cell.text_alignment == "center" for cell in resolved.cells[0])
	assert [[cell.text_alignment for cell in row] for row in resolved.cells[1:]] == \
		[[normal, numeric, normal, normal]] * 3


def test_merged_cells_do_not_classify_columns(tmp_path: pathlib.Path) -> None:
	"""Merged totals neither contaminate numeric columns nor inherit one column's alignment."""
	table = slide_lib.djot_blocks.parse_blocks(tmp_path / "merged.djot",
		"| [Region]{colspan=2} | Count |\n| --- | --- | --- |\n"
		"| First | 10 | 12 |\n| Second | 20 | 24 |\n"
		"| [Total]{colspan=2} | 36 |\n| Combined | [30]{colspan=2} |\n").blocks[0]
	resolved = slide_lib.table_styles.resolve_table(table,
		slide_lib.presentation_theme.default_theme(), slide_lib.table_styles.load_registry())
	assert [cell.text_alignment for cell in resolved.cells[1]] == ["left", "right", "right"]
	assert [cell.text_alignment for cell in resolved.cells[3]] == ["left", "right"]
	assert resolved.cells[4][1].text_alignment == "left"


def test_matrix_cropped_axes_use_correspondence_and_preserve_values(tmp_path: pathlib.Path) -> None:
	"""Cropped labels A/B/C versus B/C/D do not create a false geometric diagonal."""
	table = slide_lib.djot_blocks.parse_blocks(tmp_path / "matrix.djot",
		"{table-style=matrix-lower}\n| | B | C | D |\n| --- | --- | --- | --- |\n"
		"| A | ? | 12 | 13 |\n| B | 0 | 22 | 23 |\n| C | 31 | 0 | 33 |\n").blocks[0]
	before = table.rows
	resolved = slide_lib.table_styles.resolve_table(table,
		slide_lib.presentation_theme.default_theme(), slide_lib.table_styles.load_registry())
	assert resolved.cells[1][1].background_color == "F2F3F5"
	assert resolved.cells[2][1].background_color == "E6E6E6"
	assert resolved.cells[3][2].background_color == "E6E6E6"
	assert resolved.cells[3][1].background_color == "FFFFFF"
	assert resolved.cells[3][1].text_alignment == "right"
	assert resolved.cells[1][1].border_right.style == "none"
	assert table.rows == before


@pytest.mark.parametrize("source", (
	"| | A | B |\n| --- | --- | --- |\n| A | 0 | 1 |\n| A | 1 | 0 |\n",
	"| | B | A |\n| --- | --- | --- |\n| A | 0 | 1 |\n| B | 1 | 0 |\n",
	"| | X | Y |\n| --- | --- | --- |\n| A | 0 | 1 |\n| B | 1 | 0 |\n",
	"| | B | C |\n| --- | --- | --- |\n| A | 0 | 1 |\n| C | 1 | 0 |\n",
))
def test_ambiguous_matrix_axes_request_explicit_formatting(tmp_path: pathlib.Path, source: str) -> None:
	"""Duplicate, contradictory, or unrelated axes must not trigger speculative masking."""
	path = tmp_path / "ambiguous.djot"
	table = slide_lib.djot_blocks.parse_blocks(path, "{table-style=matrix-upper}\n" + source).blocks[0]
	with pytest.raises(slide_lib.djot_errors.DjotParseError, match="standard with explicit cell borders") as error:
		slide_lib.table_styles.resolve_table(table,
			slide_lib.presentation_theme.default_theme(), slide_lib.table_styles.load_registry())
	assert str(path) in str(error.value)


@pytest.mark.parametrize("attributes", (
	'border="1px solid red"', 'border="1pt wavy red"', 'border="0pt solid red"',
	'border="1pt solid unknown"', 'padding="1pt 2pt 3pt 4pt 5pt"',
	'padding="-1pt"', 'padding-left=auto', 'vertical-align=baseline',
	'border=none border=none', 'background-color=red',
	'font-size=0pt', 'font-size=0.5pt', 'font-size=24px',
))
def test_invalid_native_formatting_is_source_located(tmp_path: pathlib.Path, attributes: str) -> None:
	"""Reject unsupported values before native measurement or export."""
	path = tmp_path / "invalid.djot"
	with pytest.raises(slide_lib.djot_errors.DjotParseError) as error:
		slide_lib.djot_blocks.parse_blocks(path, f"| [x]{{{attributes}}} |\n")
	assert f"{path}:1:" in str(error.value)


@pytest.mark.parametrize("source", (
	"styles:\n  standard: {defaults: {padding: 5px}}\n",
	"styles:\n  standard: {defaults: {position: absolute}}\n",
	"styles:\n  standard: {}\n  standard: {}\n",
	"styles:\n  standard: {regions: {genotype: {color: red}}}\n",
	"styles:\n  standard: {matrix: diagonal}\n",
	"styles: !!python/object:builtins.object {}\n",
))
def test_shared_yaml_rejects_invalid_or_unsafe_definitions(tmp_path: pathlib.Path, source: str) -> None:
	"""Shared configuration uses the same bounded formatting vocabulary and safe data loading."""
	path = tmp_path / "styles.yaml"
	path.write_text(source, encoding="utf-8")
	with pytest.raises(slide_lib.djot_errors.DjotParseError) as error:
		slide_lib.table_styles.load_registry(path)
	assert str(path) in str(error.value)
