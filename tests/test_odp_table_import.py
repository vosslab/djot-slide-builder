"""Native source tables retain editable cells without their same-frame previews."""

# Standard Library
import pathlib
import xml.etree.ElementTree

# PIP3 modules
import pytest

# Local Modules
import slide_lib.djot_blocks
import slide_lib.djot_parser
import slide_lib.layout_engine
import slide_lib.odf_package
import slide_lib.presentation_theme
import slide_lib.importers.odf_text as odf_text
import slide_lib.importers.odf_styles as odf_styles
import slide_lib.importers.odp_media as odp_media
import slide_lib.importers.odp_tables as odp_tables
import slide_lib.importers.djot_emitter as djot_emitter
import slide_lib.importers.odp_page_objects as odp_page_objects
import slide_lib.importers.source_model as source_model
import slide_lib.importers.source_table_styles as source_table_styles


NAMESPACES = " ".join(f'xmlns:{name}="{value}"' for name, value in odf_text.NS.items())


@pytest.mark.parametrize("widths", ((100.0, 100.0), (100.0, 100.5)))
def test_imported_equal_and_near_equal_widths_survive_compilation(
	tmp_path: pathlib.Path, widths: tuple[float, ...],
) -> None:
	"""Source proportions must not become content-based widths for unequal cell text."""
	cells = tuple(source_model.SourceTableCell((source_model.TextRun(text),))
		for text in ("A long source label", "7"))
	block = source_model.TableBlock((), (tuple(cell.runs for cell in cells),), 0, 0, 1,
		cell_rows=(cells,), column_widths=widths)
	lines = djot_emitter.table_lines((block,))
	path = tmp_path / "widths.djot"
	native = slide_lib.djot_blocks.parse_blocks(path, "\n".join(lines) + "\n").blocks[0]
	assert native.column_weights == pytest.approx(tuple(width / min(widths) for width in widths))
	path.write_text("=== layout: one-panel\n\n@body\n\n" + "\n".join(lines) + "\n",
		encoding="utf-8")
	result = slide_lib.layout_engine.compile_layout_deck(
		slide_lib.djot_parser.parse_deck(path), slide_lib.presentation_theme.default_theme())
	compiled = result.plan.slides[0].objects[0].content.column_widths
	assert compiled[1] / compiled[0] == pytest.approx(widths[1] / widths[0])


@pytest.mark.parametrize("fill,drawing_color,paragraph_color,expected", (
	(None, "#ffffff", "#000000", "#FFFFFF"),
	(None, "#ffffff", "transparent", "#FFFFFF"),
	("none", "#000000", "#CCDDFF", None),
	("solid", "#CCDDEE", "#000000", "#CCDDEE"),
	("solid", "#000000", "#ffffff", "#000000"),
	(None, None, "#123456", "#123456"),
	("solid", None, "#123456", "#123456"),
	(None, None, "transparent", None),
))
def test_native_cell_fill_precedence_preserves_displayed_color(
	fill: str | None, drawing_color: str | None, paragraph_color: str, expected: str | None,
) -> None:
	"""Keep white source blanks and true solid fills despite stale paragraph colors."""
	properties = {odf_text.qname("fo", "background-color"): paragraph_color}
	if fill is not None:
		properties[odf_text.qname("draw", "fill")] = fill
	if drawing_color is not None:
		properties[odf_text.qname("draw", "fill-color")] = drawing_color
	cell = source_model.SourceTableCell((), properties=tuple(properties.items()))
	attributes, reason = source_table_styles.cell_attributes(cell)
	assert reason is None
	assert attributes == ({} if expected is None else {"background-color": expected})


def test_native_table_roundtrip_keeps_style_inheritance_spans_blanks_and_scripts(tmp_path: pathlib.Path) -> None:
	"""Do not flatten scientifically meaningful styling or covered-cell ownership."""
	root = slide_lib.odf_package.parse_xml(f'''<office:document-content {NAMESPACES}>
	<style:style style:name="base" style:family="table-cell">
		<style:paragraph-properties fo:border="none" fo:text-align="center" fo:padding="0.1cm"/>
		<style:text-properties fo:font-style="italic" fo:color="#135790"/>
	</style:style>
	<style:style style:name="cell" style:family="table-cell" style:parent-style-name="base">
		<style:graphic-properties draw:fill="solid" draw:fill-color="#CCDDEE" draw:textarea-vertical-align="bottom"/>
		<style:paragraph-properties fo:border-bottom="0.5pt dashed #123456"/>
	</style:style>
	<style:style style:name="script"><style:text-properties style:text-position="33% 58%" fo:font-weight="bold"/></style:style>
	<style:style style:name="subscript"><style:text-properties style:text-position="-33% 58%"/></style:style>
	<style:style style:name="narrow"><style:table-column-properties style:column-width="1cm"/></style:style>
	<style:style style:name="wide"><style:table-column-properties style:column-width="2cm"/></style:style>
	<table:table table:use-first-row-styles="true">
		<table:table-column table:style-name="narrow"/><table:table-column table:style-name="wide"/>
		<table:table-row table:default-cell-style-name="cell">
			<table:table-cell table:number-columns-spanned="2"><text:p>A<text:span text:style-name="script">2</text:span><text:span text:style-name="subscript">n</text:span></text:p></table:table-cell>
			<table:covered-table-cell/>
		</table:table-row>
		<table:table-row table:default-cell-style-name="cell"><table:table-cell/><table:table-cell><text:p>Total</text:p></table:table-cell></table:table-row>
	</table:table></office:document-content>'''.encode("utf-8"), "content.xml")
	table = root.find("table:table", odf_text.NS)
	block, positions = odp_tables.read_table(table, 12, 34, 7, odf_styles.definitions((root,)))
	assert block.unsupported_reason is None
	assert block.headers == ()
	assert (block.left, block.top, block.source_ordinal) == (12, 34, 7)
	assert block.cell_rows[0][0].column_span == 2 and block.cell_rows[0][1].covered
	assert block.cell_rows[1][0].runs == ()
	assert [(row, column) for row, column, _runs in positions] == [(0, 0), (1, 0), (1, 1)]
	assert block.cell_rows[0][0].runs[1].script == "super"
	assert block.cell_rows[0][0].runs[2].script == "sub"
	assert block.cell_rows[0][0].runs[1].bold and block.cell_rows[0][0].runs[1].italic
	assert block.cell_rows[0][0].runs[1].color == "#135790"
	assert block.column_widths[1] == pytest.approx(2 * block.column_widths[0])
	lines = djot_emitter.table_lines((block,))
	assert 'border-bottom="0.5pt dashed #123456"' in lines[0]
	assert 'background-color=#CCDDEE' in lines[0]
	assert 'colspan=2' in lines[1] and '^2^' in lines[1] and '~n~' in lines[1]
	emitted = slide_lib.djot_blocks.parse_blocks(tmp_path / "table.djot", "\n".join(lines) + "\n").blocks[0]
	assert emitted.column_count == 2
	assert emitted.rows[0][0].column_span == 2 and emitted.rows[1][0].inlines == ()
	assert emitted.formatting.background_color == "#CCDDEE"


def test_preview_suppression_is_scoped_to_usable_table_frame(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
	"""Suppress the native-table preview only; unrelated or unsupported visuals stay."""
	images = []

	def add_picture(image: xml.etree.ElementTree.Element, *_unused: object) -> bool:
		images.append(image.get(odf_text.qname("xlink", "href")))
		return True

	monkeypatch.setattr(odp_page_objects, "add_picture", add_picture)
	accumulator = odp_page_objects.PageAccumulator(*([] for _index in range(13)))
	bodies = (
		'<table:table><table:table-row><table:table-cell><text:p>Cell</text:p></table:table-cell></table:table-row></table:table>'
		'<draw:text-box><text:p>Cell duplicate</text:p></draw:text-box><draw:image xlink:href="table-preview.png"/>',
		'<draw:image xlink:href="unrelated.png"/>',
		'<table:table><table:table-row><table:table-cell table:number-rows-spanned="2"><text:p>Unsupported merge</text:p></table:table-cell></table:table-row></table:table>'
		'<draw:image xlink:href="unsupported-preview.png"/>',
	)
	for index, body in enumerate(bodies):
		frame = slide_lib.odf_package.parse_xml(
			f'<draw:frame {NAMESPACES} svg:x="1cm" svg:y="2cm" svg:width="4cm" svg:height="3cm">{body}</draw:frame>'.encode("utf-8"),
			"content.xml")
		odp_page_objects.read_frame(frame, 1, 800, 600, None, frozenset(), frozenset(),
			tmp_path, pathlib.PurePosixPath("."), {}, accumulator, odp_media.MediaBudget(), (index,), index, {})
	assert images == ["unrelated.png", "unsupported-preview.png"]
	assert accumulator.text_blocks == []
	assert len(accumulator.tables) == 2 and accumulator.tables[1].unsupported_reason
	assert len(accumulator.positioned_text) == 2
