"""Preserve extracted source tables as editable import-plan structures."""

import dataclasses

import slide_lib.importers.geometry as geometry
import slide_lib.importers.source_regions as source_regions


#============================================
@dataclasses.dataclass(frozen=True)
class TablePlan:
	"""A source table retained as editable structured content."""

	bounds: geometry.NormalizedBounds
	text_regions: tuple[source_regions.SourceTextRegion, ...]
	rows: tuple[tuple["TableCellPlan", ...], ...]
	row_count: int
	column_count: int
	has_header: bool = False
	unsupported_reason: str | None = None
	table_id: int = 0


#============================================
@dataclasses.dataclass(frozen=True)
class TableCellPlan:
	"""One native-table cell, including an intentional blank when no text exists."""

	row: int
	column: int
	text_regions: tuple[source_regions.SourceTextRegion, ...]
	row_span: int = 1
	column_span: int = 1


#============================================
def regular_text_grid(text_regions: tuple[source_regions.SourceTextRegion, ...]) -> bool:
	"""Recognize a dense row-and-column lattice as an editable table candidate."""
	if len(text_regions) < 8:
		return False
	centers_x = sorted((item.bounds.left + item.bounds.right) / 2 for item in text_regions)
	centers_y = sorted((item.bounds.top + item.bounds.bottom) / 2 for item in text_regions)
	x_breaks = sum(
		second - first >= 0.08 for first, second in zip(centers_x, centers_x[1:])
	)
	y_breaks = sum(
		second - first >= 0.08 for first, second in zip(centers_y, centers_y[1:])
	)
	return x_breaks >= 2 and y_breaks >= 2


#============================================
def table_plans(
	text_regions: tuple[source_regions.SourceTextRegion, ...],
	title_region: source_regions.SourceTextRegion | None,
) -> tuple[TablePlan, ...]:
	"""Plan each actual source table independently before diagram coupling."""
	available = tuple(region for region in text_regions if region is not title_region)
	by_table: dict[int, list[source_regions.SourceTextRegion]] = {}
	for region in available:
		if region.source_kind == "table" and region.table_id is not None:
			by_table.setdefault(region.table_id, []).append(region)
	plans: list[TablePlan] = []
	for table_id in sorted(by_table):
		table_regions = tuple(sorted(by_table[table_id], key=lambda item: item.source_ordinal))
		bounds = table_regions[0].bounds
		for region in table_regions[1:]:
			bounds = bounds.union(region.bounds)
		row_count = table_regions[0].table_row_count
		column_count = table_regions[0].table_column_count
		plans.append(TablePlan(
			bounds,
			table_regions,
			table_rows(table_regions, row_count, column_count),
			row_count,
			column_count,
			table_regions[0].table_has_header,
			table_regions[0].table_unsupported_reason,
			table_id,
		))
	return tuple(plans)


#============================================
def table_rows(
	regions: tuple[source_regions.SourceTextRegion, ...],
	row_count: int,
	column_count: int,
) -> tuple[tuple[TableCellPlan, ...], ...]:
	"""Preserve actual row-major dimensions, blanks, and cell ownership."""
	by_cell: dict[tuple[int, int], list[source_regions.SourceTextRegion]] = {}
	for region in regions:
		key = (region.table_row, region.table_column)
		by_cell.setdefault(key, []).append(region)
	rows: list[tuple[TableCellPlan, ...]] = []
	for row in range(row_count):
		cells: list[TableCellPlan] = []
		for column in range(column_count):
			cell_regions = tuple(sorted(
				by_cell.get((row, column), []), key=lambda item: item.source_ordinal,
			))
			cells.append(TableCellPlan(row, column, cell_regions))
		rows.append(tuple(cells))
	return tuple(rows)
