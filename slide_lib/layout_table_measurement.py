"""Measure table-specific geometry against one compile-scoped text session."""

import math
import dataclasses

import slide_lib.layout_size_selection
import slide_lib.capacity_report
import slide_lib.layout_measurement
import slide_lib.layout_primitives
import slide_lib.layout_source_facts
import slide_lib.math_layout
import slide_lib.native_model
import slide_lib.presentation_theme
import slide_lib.table_formatting


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
	resolved = active.resolved_table(table)
	if table.column_weights:
		total = sum(table.column_weights)
		column_widths = tuple(width * (weight / total) for weight in table.column_weights)
	else:
		minimums, preferred = _table_context(active).group_bounds[table.table_group] \
			if table.table_group is not None else _table_column_bounds((table,), size_pt, active)
		column_widths = _distribute_table_widths(minimums, preferred, width)
	row_heights = []
	for row, formatting in zip(rows, resolved.cells):
		heights = []
		for (column, cell), appearance in zip(
				slide_lib.native_model.table_cell_positions(row), formatting):
			insets = formatting_insets(appearance, theme)
			usable = sum(column_widths[column:column + cell.column_span]) - insets.left - insets.right
			cell_size = appearance.font_size_pt if appearance.font_size_pt is not None else size_pt
			height = slide_lib.layout_measurement.paragraph_height(
				cell.inlines, cell_size, usable, theme, bold=appearance.bold, session=active) \
				if usable > 0 else math.inf
			heights.append(height + insets.top + insets.bottom)
		row_heights.append(max(heights))
	return TableMeasurements(column_widths, tuple(row_heights))


def _table_column_bounds(tables: tuple[slide_lib.native_model.Table, ...], size_pt: float,
		session: slide_lib.layout_measurement.MeasurementSession) -> tuple[tuple[float, ...], tuple[float, ...]]:
	"""Pool widest-token and full-line needs without inventing synthetic header rows."""
	minimums = [1.0] * tables[0].column_count
	preferred = [1.0] * tables[0].column_count
	spanning = []
	for table in tables:
		rows = ((table.headers,) if table.headers else ()) + table.rows
		for row, formatting in zip(rows, session.resolved_table(table).cells):
			for (column, cell), appearance in zip(
					slide_lib.native_model.table_cell_positions(row), formatting):
				cell_size = appearance.font_size_pt if appearance.font_size_pt is not None else size_pt
				low, high = _table_cell_widths(cell.inlines, cell_size, session, appearance.bold)
				insets = formatting_insets(appearance, session.theme)
				low += insets.left + insets.right
				high += insets.left + insets.right
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


def formatting_padding(formatting: slide_lib.table_formatting.CellFormatting,
		theme: slide_lib.presentation_theme.PresentationTheme) -> slide_lib.layout_primitives.Insets:
	"""Convert point-valued cell padding into the physical plan's logical units once."""
	result = slide_lib.layout_primitives.Insets(*(slide_lib.layout_measurement.point_height(
		getattr(formatting, f"padding_{side}_pt"), theme) for side in ("left", "top", "right", "bottom")))
	return result


def cell_content_insets(padding: slide_lib.layout_primitives.Insets,
		borders: tuple[slide_lib.table_formatting.Border, ...],
		theme: slide_lib.presentation_theme.PresentationTheme) -> slide_lib.layout_primitives.Insets:
	"""Share the native border occupancy and text clearance in both layout axes."""
	values = []
	for side, border in zip(("top", "right", "bottom", "left"), borders):
		width_pt = border.width_pt if border.style != "none" else 0.0
		values.append(getattr(padding, side) + slide_lib.layout_measurement.point_height(
			width_pt + slide_lib.layout_measurement.TEXT_FRAME_CLEARANCE_PT, theme))
	top, right, bottom, left = values
	result = slide_lib.layout_primitives.Insets(left, top, right, bottom)
	return result


def formatting_insets(formatting: slide_lib.table_formatting.CellFormatting,
		theme: slide_lib.presentation_theme.PresentationTheme) -> slide_lib.layout_primitives.Insets:
	"""Calculate usable cell space from the exact resolved side properties."""
	borders = tuple(getattr(formatting, f"border_{side}") for side in ("top", "right", "bottom", "left"))
	result = cell_content_insets(formatting_padding(formatting, theme), borders, theme)
	return result


def table_cell_text_width(column_width: float,
		formatting: slide_lib.table_formatting.CellFormatting,
		theme: slide_lib.presentation_theme.PresentationTheme) -> float:
	"""Return the same usable span width for fitting and physical text construction."""
	insets = formatting_insets(formatting, theme)
	result = column_width - insets.left - insets.right
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
	active = session or slide_lib.layout_measurement.MeasurementSession(theme)
	minimum = slide_lib.layout_primitives.MIN_SERIALIZABLE_FONT_SIZE_PT
	size = slide_lib.layout_size_selection.largest_fitting_size(preferred, minimum,
		lambda value: slide_lib.layout_measurement.text_frame_fits(
			table_height(table, value, rectangle.width, theme, active),
			slide_lib.layout_measurement.text_frame_measurement(rectangle), theme))
	if size is None:
		raise slide_lib.capacity_report.PhysicalCapacityError(table.location, layout, slot, floor,
			slide_lib.capacity_report.CapacityCause.TABLE, minimum)
	if size < floor and session is not None:
		session.record_capacity(table.location, layout, slot, size, floor,
			slide_lib.capacity_report.CapacityCause.TABLE)
	return size
