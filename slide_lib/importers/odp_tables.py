"""Read bounded ODF tables into the importer source model."""

# Standard Library
import xml.etree.ElementTree

# Local Modules
import slide_lib.importers.odf_styles as odf_styles
import slide_lib.importers.odf_text as odf_text
import slide_lib.importers.odp_geometry as odp_geometry
import slide_lib.importers.source_model as source_model
import slide_lib.importers.source_table_styles as source_table_styles


NS = dict(odf_text.NS)
MAX_TABLE_CELLS = 2_000
MAX_TABLE_REPEAT = 100


def qname(prefix: str, local_name: str) -> str:
	"""Build one namespace-qualified XML name."""
	return f"{{{NS[prefix]}}}{local_name}"


def table_cell_runs(cell: xml.etree.ElementTree.Element,
		definitions: dict[str, odf_styles.StyleDefinition]) -> tuple[source_model.TextRun, ...]:
	"""Read cell text, inheriting its default style without changing source colors."""
	result: list[source_model.TextRun] = []
	for _level, runs in odf_text.text_paragraphs(
			cell, definitions, odf_text.TextStyle(preserve_color=True)):
		if result:
			result.append(source_model.TextRun(" "))
		result.extend(runs)
	return tuple(result)


def repeat_count(element: xml.etree.ElementTree.Element, attribute: str) -> int:
	"""Return one bounded ODF repeat or span value."""
	# ASVS 2.2.1: bound expansion before constructing the physical cell matrix.
	raw_value = element.get(qname("table", attribute), "1")
	if not raw_value.isdigit() or not 1 <= int(raw_value) <= MAX_TABLE_REPEAT:
		raise ValueError("ODF table repeat count exceeds the supported range")
	return int(raw_value)


def source_cell(cell: xml.etree.ElementTree.Element, default_style: str,
		definitions: dict[str, odf_styles.StyleDefinition]) -> source_model.SourceTableCell:
	"""Keep physical-cell text, spans, and resolved ODF properties together."""
	if default_style and not cell.get(qname("table", "style-name")):
		styled = cell.makeelement(cell.tag, dict(cell.attrib))
		styled.set(qname("table", "style-name"), default_style)
		styled.extend(cell)
		cell = styled
	properties = odf_styles.properties(cell, definitions)
	alignments = {odf_styles.attribute(paragraph, definitions, qname("fo", "text-align"))
		for paragraph in cell.iter() if paragraph.tag in {qname("text", "p"), qname("text", "h")}}
	alignments.discard(None)
	if len(alignments) == 1:
		properties[qname("fo", "text-align")] = alignments.pop()
	elif len(alignments) > 1:
		properties["unsupported-paragraph-alignment"] = ",".join(sorted(alignments))
	result = source_model.SourceTableCell(
		table_cell_runs(cell, definitions), repeat_count(cell, "number-columns-spanned"),
		repeat_count(cell, "number-rows-spanned"),
		cell.tag == qname("table", "covered-table-cell"), tuple(sorted(properties.items())),
	)
	return result


def read_table(table: xml.etree.ElementTree.Element, left: float, top: float,
		source_ordinal: int, definitions: dict[str, odf_styles.StyleDefinition]) -> tuple[source_model.TableBlock,
		list[tuple[int, int, tuple[source_model.TextRun, ...]]]]:
	"""Extract a physical grid, preserving covered cells and default cell styles."""
	rows: list[tuple[source_model.SourceTableCell, ...]] = []
	header_row_count = 0
	unsupported: list[str] = []
	total_cell_count = 0
	column_widths: list[float] = []
	column_defaults: list[str] = []
	for column in table.findall("./table:table-column", NS):
		repeats = repeat_count(column, "number-columns-repeated")
		if len(column_defaults) + repeats > MAX_TABLE_CELLS:
			raise ValueError("ODF table exceeds the supported cell range")
		column_defaults.extend([column.get(qname("table", "default-cell-style-name"), "")] * repeats)
		width = odf_styles.attribute(column, definitions, qname("style", "column-width"))
		if width is not None:
			points = odp_geometry.parse_length(width, field_name="table column width", allow_negative=False)
			column_widths.extend([points] * repeats)

	def add_row(row: xml.etree.ElementTree.Element, is_header: bool) -> None:
		nonlocal header_row_count, total_cell_count
		cells: list[source_model.SourceTableCell] = []
		row_default = row.get(qname("table", "default-cell-style-name"), "")
		for cell in row:
			if cell.tag not in {qname("table", "table-cell"), qname("table", "covered-table-cell")}:
				continue
			for _repeat in range(repeat_count(cell, "number-columns-repeated")):
				if len(cells) >= MAX_TABLE_CELLS:
					raise ValueError("ODF table exceeds the supported cell range")
				column_default = column_defaults[len(cells)] if len(cells) < len(column_defaults) else ""
				cells.append(source_cell(cell, row_default or column_default, definitions))
		row_repeats = repeat_count(row, "number-rows-repeated")
		if total_cell_count + len(cells) * row_repeats > MAX_TABLE_CELLS:
			raise ValueError("ODF table exceeds the supported cell range")
		for _repeat in range(row_repeats):
			if len(rows) >= MAX_TABLE_CELLS:
				raise ValueError("ODF table exceeds the supported cell range")
			rows.append(tuple(cells))
			total_cell_count += len(cells)
			if is_header:
				header_row_count += 1

	for child in table:
		if child.tag == qname("table", "table-header-rows"):
			for row in child.findall("./table:table-row", NS):
				add_row(row, True)
		elif child.tag == qname("table", "table-row"):
			add_row(child, False)
	if not rows:
		raise ValueError("ODF table has no rows")
	column_count = len(rows[0])
	if not column_count or any(len(row) != column_count for row in rows):
		unsupported.append("irregular source table rows require reconstruction")
	if column_widths and len(column_widths) != column_count:
		unsupported.append("incomplete source table column widths require reconstruction")
	if header_row_count > 1:
		unsupported.append("multiple source table header rows require reconstruction")
	for row in rows:
		covered_until = 0
		for index, cell in enumerate(row):
			if cell.row_span != 1:
				unsupported.append("vertical source table merges require reconstruction")
			if cell.covered != (index < covered_until):
				unsupported.append("invalid source table covered-cell ownership")
			if cell.covered:
				if cell.runs:
					unsupported.append("covered source table cells contain text")
				continue
			covered_until = index + cell.column_span
			if covered_until > len(row):
				unsupported.append("source table span exceeds its row")
			if "unsupported-paragraph-alignment" in dict(cell.properties):
				unsupported.append("mixed source paragraph alignment requires reconstruction")
			_attributes, reason = source_table_styles.cell_attributes(cell)
			if reason:
				unsupported.append(reason)
	run_rows = tuple(tuple(cell.runs for cell in row) for row in rows)
	headers = run_rows[0] if header_row_count == 1 else ()
	body_rows = run_rows[1:] if header_row_count == 1 else run_rows
	cell_facts = [(row_index, column_index, cell.runs)
		for row_index, row in enumerate(rows) for column_index, cell in enumerate(row)
		if not cell.covered]
	block = source_model.TableBlock(
		headers, body_rows, left, top, source_ordinal,
		"; ".join(sorted(set(unsupported))) or None, tuple(rows), tuple(column_widths),
		tuple(sorted(odf_styles.properties(table, definitions).items())),
	)
	return block, cell_facts
