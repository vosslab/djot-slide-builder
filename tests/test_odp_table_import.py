"""Preserve merged cells and scientific notation through native table import."""

# Standard Library
import pathlib

# PIP3 modules
import pytest

# Local Modules
import slide_lib.djot_blocks
import slide_lib.odf_package
import slide_lib.importers.odf_text as odf_text
import slide_lib.importers.odf_styles as odf_styles
import slide_lib.importers.odp_tables as odp_tables
import slide_lib.importers.djot_emitter as djot_emitter


NAMESPACES = " ".join(f'xmlns:{name}="{value}"' for name, value in odf_text.NS.items())


def test_native_table_roundtrip_keeps_style_inheritance_spans_blanks_and_scripts(tmp_path: pathlib.Path) -> None:
	"""Do not flatten scientifically meaningful styling or covered-cell ownership."""
	source = f'''<office:document-content {NAMESPACES}>
	<style:style style:name="base" style:family="table-cell">
		<style:paragraph-properties fo:border="none" fo:text-align="center" fo:padding="0.1cm"/>
		<style:text-properties fo:font-style="italic" fo:color="#135790"/>
	</style:style>
	<style:style style:name="cell" style:family="table-cell" style:parent-style-name="base">
		<style:graphic-properties draw:fill="solid" draw:fill-color="#CCDDEE" draw:textarea-vertical-align="bottom"/>
		<style:paragraph-properties fo:border-bottom="0.5pt dashed #123456"/>
	</style:style>
	<style:style style:name="script">
		<style:text-properties style:text-position="33% 58%" fo:font-weight="bold"/>
	</style:style>
	<style:style style:name="subscript"><style:text-properties style:text-position="-33% 58%"/></style:style>
	<style:style style:name="narrow"><style:table-column-properties style:column-width="1cm"/></style:style>
	<style:style style:name="wide"><style:table-column-properties style:column-width="2cm"/></style:style>
	<table:table table:use-first-row-styles="true">
		<table:table-column table:style-name="narrow"/><table:table-column table:style-name="wide"/>
		<table:table-row table:default-cell-style-name="cell">
'''
	source += (
		'\t\t\t<table:table-cell table:number-columns-spanned="2"><text:p>A'
		'<text:span text:style-name="script">2</text:span>'
		'<text:span text:style-name="subscript">n</text:span></text:p></table:table-cell>'
	)
	source += '''
			<table:covered-table-cell/>
		</table:table-row>
		<table:table-row table:default-cell-style-name="cell">
			<table:table-cell/><table:table-cell><text:p>Total</text:p></table:table-cell>
		</table:table-row>
	</table:table></office:document-content>'''
	root = slide_lib.odf_package.parse_xml(source.encode("utf-8"), "content.xml")
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
