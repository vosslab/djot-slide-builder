"""Read bounded ODF tables into the importer source model."""

# Standard Library
import xml.etree.ElementTree

# Local Modules
import slide_lib.importers.odf_styles as odf_styles
import slide_lib.importers.odf_text as odf_text
import slide_lib.importers.source_model as source_model


NS = {
	"table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
}
MAX_TABLE_CELLS = 2_000
MAX_TABLE_REPEAT = 100


#============================================
def qname(prefix: str, local_name: str) -> str:
	"""Build one namespace-qualified XML name."""
	return f"{{{NS[prefix]}}}{local_name}"


#============================================
def table_cell_runs(cell: xml.etree.ElementTree.Element,
		definitions: dict[str, odf_styles.StyleDefinition]) -> tuple[source_model.TextRun, ...]:
	"""Read one ODF table cell into the native inline table vocabulary."""
	result: list[source_model.TextRun] = []
	for _level, runs in odf_text.text_paragraphs(cell, definitions):
		if result:
			result.append(source_model.TextRun(" "))
		result.extend(runs)
	return tuple(result)


#============================================
def repeat_count(element: xml.etree.ElementTree.Element, attribute: str) -> int:
	"""Return one bounded ODF table repeat value."""
	raw_value = element.get(qname("table", attribute), "1")
	if not raw_value.isdigit() or not 1 <= int(raw_value) <= MAX_TABLE_REPEAT:
		raise ValueError("ODF table repeat count exceeds the supported range")
	return int(raw_value)


#============================================
def read_table(table: xml.etree.ElementTree.Element, left: float, top: float,
		source_ordinal: int, definitions: dict[str, odf_styles.StyleDefinition]) -> tuple[source_model.TableBlock,
		list[tuple[int, int, tuple[source_model.TextRun, ...]]]]:
	"""Extract a rectangular ODF table and its planner-facing cell facts."""
	rows: list[tuple[tuple[source_model.TextRun, ...], ...]] = []
	header_row_count = 0
	unsupported: list[str] = []
	total_cell_count = 0

	def add_row(row: xml.etree.ElementTree.Element, is_header: bool) -> None:
		nonlocal header_row_count, total_cell_count
		cells: list[tuple[source_model.TextRun, ...]] = []
		for cell in row:
			if cell.tag not in {qname("table", "table-cell"), qname("table", "covered-table-cell")}:
				continue
			if cell.tag == qname("table", "covered-table-cell"):
				unsupported.append("covered source table cells require span-aware emission")
			if cell.get(qname("table", "number-columns-spanned")) or \
					cell.get(qname("table", "number-rows-spanned")):
				unsupported.append("merged source table cells require span-aware emission")
			for _repeat in range(repeat_count(cell, "number-columns-repeated")):
				if len(cells) >= MAX_TABLE_CELLS:
					raise ValueError("ODF table exceeds the supported cell range")
				cells.append(table_cell_runs(cell, definitions))
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
			for row in child.findall("./table:table-row", {"table": NS["table"]}):
				add_row(row, True)
		elif child.tag == qname("table", "table-row"):
			add_row(child, False)
	if not rows:
		raise ValueError("ODF table has no rows")
	column_count = len(rows[0])
	if not column_count or any(len(row) != column_count for row in rows):
		unsupported.append("irregular source table rows require reconstruction")
	if header_row_count > 1:
		unsupported.append("multiple source table header rows require reconstruction")
	headers = rows[0] if header_row_count == 1 else ()
	body_rows = rows[1:] if header_row_count == 1 else rows
	cell_facts: list[tuple[int, int, tuple[source_model.TextRun, ...]]] = []
	for row_index, row in enumerate(rows):
		for column_index, cell in enumerate(row):
			if cell:
				cell_facts.append((row_index, column_index, cell))
	return source_model.TableBlock(
		headers, tuple(body_rows), left, top, source_ordinal,
		"; ".join(sorted(set(unsupported))) or None,
	), cell_facts
