"""Measure table-specific geometry against one compile-scoped text session."""

import dataclasses

import slide_lib.layout_size_selection
import slide_lib.capacity_report
import slide_lib.layout_measurement
import slide_lib.layout_primitives
import slide_lib.layout_source_facts
import slide_lib.math_layout
import slide_lib.native_model
import slide_lib.presentation_theme


TABLE_HORIZONTAL_PADDING = 12.0
TABLE_VERTICAL_PADDING = 4.0
TABLE_BORDER_WIDTH_PT = 1.0


@dataclasses.dataclass(frozen=True)
class TableMeasurements:
	"""Carry the column and row geometry used by fitting and final serialization."""

	column_widths: tuple[float, ...]
	row_heights: tuple[float, ...]


@dataclasses.dataclass(frozen=True)
class TableMeasurementContext:
	"""Retain pooled bounds for explicitly related tables in one deck compilation."""

	group_bounds: dict[str, tuple[tuple[float, ...], tuple[float, ...]]]


def prepare_table_groups(deck: slide_lib.native_model.Deck,
		session: slide_lib.layout_measurement.MeasurementSession) -> None:
	"""Measure all explicitly related tables before any slide chooses its text size."""
	groups: dict[str, list[slide_lib.native_model.Table]] = {}
	for source in deck.slides:
		blocks = source.blocks + tuple(block for cell in source.cells for block in cell.blocks)
		for block in slide_lib.layout_source_facts.descendant_blocks(blocks):
			if isinstance(block, slide_lib.native_model.Table) and block.table_group is not None:
				groups.setdefault(block.table_group, []).append(block)
	bounds = {}
	for name, tables in groups.items():
		columns = tables[0].column_count
		for table in tables:
			count = table.column_count
			if count != columns:
				raise ValueError(f"{table.location.path}:{table.location.line}: table-group "
					f"{name!r} requires {columns} columns, found {count}")
		bounds[name] = _table_column_bounds(
			tuple(tables), session.theme.ordinary_body_size_pt, session)
	session.table_context = TableMeasurementContext(bounds)


def _table_context(session: slide_lib.layout_measurement.MeasurementSession) -> TableMeasurementContext:
	"""Require the deck-level table bounds before measuring a grouped table."""
	context = session.table_context
	if not isinstance(context, TableMeasurementContext):
		raise ValueError("grouped table measurement requires prepared table bounds")
	return context


def table_measurements(table: slide_lib.native_model.Table, size_pt: float, width: float,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession | None = None) -> TableMeasurements:
	"""Measure exact content-aware columns and rows used by final output."""
	active = session or slide_lib.layout_measurement.MeasurementSession(theme)
	rows = (table.headers,) if table.headers else ()
	rows += table.rows
	columns = table.column_count
	padding = TABLE_HORIZONTAL_PADDING * 2
	clearance = slide_lib.layout_measurement.point_height(
		(TABLE_BORDER_WIDTH_PT + slide_lib.layout_measurement.TEXT_FRAME_CLEARANCE_PT) * 2, theme)
	content_width = width - (padding + clearance) * columns
	if table.column_weights:
		total = sum(table.column_weights)
		column_widths = tuple(width * (weight / total) for weight in table.column_weights)
	else:
		minimums, preferred = _table_context(active).group_bounds[table.table_group] \
			if table.table_group is not None else _table_column_bounds((table,), size_pt, active)
		column_widths = tuple(value + padding + clearance for value in
			_distribute_table_widths(minimums, preferred, content_width))
	row_heights = tuple(max(slide_lib.layout_measurement.paragraph_height(
		cell.inlines, size_pt, table_cell_text_width(sum(column_widths[column:column + cell.column_span]), theme),
		theme, bold=row_index == 0 and bool(table.headers), session=active) +
		TABLE_VERTICAL_PADDING * 2 for column, cell in slide_lib.native_model.table_cell_positions(row))
		for row_index, row in enumerate(rows))
	return TableMeasurements(column_widths, row_heights)


def _table_column_bounds(tables: tuple[slide_lib.native_model.Table, ...], size_pt: float,
		session: slide_lib.layout_measurement.MeasurementSession) -> tuple[tuple[float, ...], tuple[float, ...]]:
	"""Pool widest-token and full-line needs without inventing synthetic header rows."""
	rows = []
	for table in tables:
		if table.headers:
			rows.append((table.headers, True))
		rows.extend((row, False) for row in table.rows)
	minimums = [1.0] * tables[0].column_count
	preferred = [1.0] * tables[0].column_count
	spanning = []
	for row, header in rows:
		for column, cell in slide_lib.native_model.table_cell_positions(row):
			low, high = _table_cell_widths(cell.inlines, size_pt, session, header)
			if cell.column_span == 1:
				minimums[column] = max(minimums[column], low)
				preferred[column] = max(preferred[column], high)
			else:
				spanning.append((column, cell.column_span, low, high))
	for column, span, low, high in spanning:
		for bounds, required in ((minimums, low), (preferred, high)):
			extra = max(0.0, required - sum(bounds[column:column + span])) / span
			for index in range(column, column + span):
				bounds[index] += extra
	preferred = [max(low, high) for low, high in zip(minimums, preferred)]
	return tuple(minimums), tuple(preferred)


def table_cell_text_width(column_width: float,
		theme: slide_lib.presentation_theme.PresentationTheme) -> float:
	"""Return serializer-safe text extent inside one bordered native cell."""
	border_and_clearance = slide_lib.layout_measurement.point_height(
		(TABLE_BORDER_WIDTH_PT + slide_lib.layout_measurement.TEXT_FRAME_CLEARANCE_PT) * 2, theme)
	result = column_width - TABLE_HORIZONTAL_PADDING * 2 - border_and_clearance
	return result


def _table_cell_widths(inlines: tuple[slide_lib.native_model.Inline, ...], size_pt: float,
		session: slide_lib.layout_measurement.MeasurementSession, bold: bool) -> tuple[float, float]:
	"""Return widest-token and widest-line advances for one native table cell."""
	if slide_lib.math_layout.has_math(inlines):
		run = slide_lib.math_layout.equation_run(
			slide_lib.math_layout.semantic_runs(inlines, bold))
		width = session.equations[(run.text, run.display)].width * slide_lib.layout_measurement.point_height(size_pt, session.theme)
		return width, width
	minimum = 0.0
	line_width = 0.0
	preferred = 0.0
	for text, family, token_bold, token_italic, literal in slide_lib.layout_measurement._styled_tokens(inlines, bold):
		if text == "\n":
			preferred = max(preferred, line_width)
			line_width = 0.0
			continue
		for token in slide_lib.layout_measurement._split_wrap_tokens(text):
			advance = session.advance(family, token_bold, token_italic,
				slide_lib.presentation_theme.inline_size_pt(size_pt, literal), token)
			line_width += advance
			if not token.isspace():
				minimum = max(minimum, advance)
	preferred = max(preferred, line_width)
	return minimum, preferred


def _distribute_table_widths(minimums: tuple[float, ...], preferred: tuple[float, ...],
		available: float) -> tuple[float, ...]:
	"""Allocate table content width between measured token and single-line bounds."""
	if available <= 0:
		raise ValueError("table width cannot accommodate cell padding")
	minimum_total = sum(minimums)
	if minimum_total >= available:
		return tuple(available * value / minimum_total for value in minimums)
	needs = tuple(max(0.0, preferred[index] - minimums[index])
		for index in range(len(minimums)))
	need_total = sum(needs)
	usable = min(available - minimum_total, need_total)
	widths = [minimums[index] + (usable * needs[index] / need_total if need_total else 0.0)
		for index in range(len(minimums))]
	remaining = available - sum(widths)
	return tuple(value + remaining / len(widths) for value in widths)


def table_height(table: slide_lib.native_model.Table, size_pt: float, width: float,
		theme: slide_lib.presentation_theme.PresentationTheme,
		session: slide_lib.layout_measurement.MeasurementSession | None = None) -> float:
	"""Return measured height of exact rows used by final serialization."""
	return sum(table_measurements(table, size_pt, width, theme, session).row_heights)


def select_table_size(table: slide_lib.native_model.Table,
		rectangle: slide_lib.layout_primitives.LogicalRectangle, preferred: float, floor: float,
		theme: slide_lib.presentation_theme.PresentationTheme,
		layout: str, slot: str, session: slide_lib.layout_measurement.MeasurementSession | None = None) -> float:
	"""Choose a table size and report when it must cross the readable floor."""
	minimum = slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT
	size = slide_lib.layout_size_selection.largest_fitting_size(preferred, minimum,
		lambda value: slide_lib.layout_measurement.text_frame_fits(
			table_height(table, value, rectangle.width, theme, session),
			slide_lib.layout_measurement.text_frame_measurement(rectangle), theme))
	if size is None:
		raise slide_lib.capacity_report.PhysicalCapacityError(table.location, layout, slot, floor,
			slide_lib.capacity_report.CapacityCause.TABLE, minimum)
	if size < floor and session is not None:
		session.record_capacity(table.location, layout, slot, size, floor,
			slide_lib.capacity_report.CapacityCause.TABLE)
	return size
