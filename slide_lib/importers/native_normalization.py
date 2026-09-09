"""Canonical native fallbacks for legacy spatial presentation structures."""

# local repo modules
import slide_lib.layout_registry


MAX_POSITIONED_LABELS = 12
TABLE_GRID_LAYOUTS = {
	1: "one-panel",
	2: "two-panels",
	3: "one-plus-two-panels",
	4: "four-panels",
	6: "six-panels",
}


#============================================
def component_lines(component: object) -> tuple[str, ...]:
	"""Read the emitter component line surface without creating a circular import."""
	lines = getattr(component, "lines", None)
	if not isinstance(lines, tuple) or any(not isinstance(line, str) for line in lines):
		raise TypeError("native normalization requires a tuple of component lines")
	return lines


#============================================
def source_order_components(components: list[object]) -> list[object]:
	"""Return components in retained source stack order with stable input fallback."""
	indexed: list[tuple[tuple[int, tuple[int, ...], int], object]] = []
	for index, component in enumerate(components):
		source_order = getattr(component, "source_order", ())
		if not isinstance(source_order, tuple) or any(not isinstance(item, int)
				for item in source_order):
			raise TypeError("native normalization requires an integer source-order tuple")
		key = (0, source_order, index) if source_order else (1, (), index)
		indexed.append((key, component))
	result = [component for _key, component in sorted(indexed, key=lambda item: item[0])]
	return result


#============================================
def flow_lines(components: list[object]) -> list[str]:
	"""Flatten non-table components into one valid source-ordered native flow."""
	component_groups = [component_lines(component)
		for component in source_order_components(components)]
	local_headings = [line for lines in component_groups for line in lines
		if line.startswith("## ")]
	body_groups: list[list[str]] = []
	for lines in component_groups:
		group = [line[3:] if line.startswith("## ") else line for line in lines
			if not (line.startswith("## ") and line == local_headings[0] if local_headings else False)]
		while group and not group[0]:
			group.pop(0)
		while group and not group[-1]:
			group.pop()
		if group:
			body_groups.append(group)
	body = [line for index, group in enumerate(body_groups)
		for line in ((*group, "") if index < len(body_groups) - 1 else group)]
	lines: list[str] = []
	if local_headings:
		lines.extend((local_headings[0], ""))
	lines.extend(body)
	return lines


#============================================
def one_panel_lines(heading: list[str], components: list[object]) -> list[str]:
	"""Collapse non-table components into one standard source-ordered panel."""
	return ["=== layout: one-panel", "", *heading, "", "@body", "",
		*flow_lines(components)]


#============================================
def table_grid_lines(heading: list[str], components: list[object]) -> tuple[list[str], str]:
	"""Place each table-bearing fallback component in its own valid native cell.

	Args:
		heading: Optional emitted slide title lines.
		components: Source components that include at least one table.

	Returns:
		Generated Djot lines and the selected native layout name.

	Raises:
		ValueError: The components cannot occupy an exact supported native grid.
	"""
	ordered = source_order_components(components)
	if not any(getattr(component, "kind", None) == "table" for component in ordered):
		raise ValueError("table fallback requires a table component")
	layout = TABLE_GRID_LAYOUTS.get(len(ordered))
	if layout is None:
		raise ValueError(
			f"{len(ordered)} components including a table have no exact native grid"
		)
	slots = slide_lib.layout_registry.contract_for(layout).slot_names
	lines = [f"=== layout: {layout}", "", *heading]
	for component, slot in zip(ordered, slots, strict=True):
		lines.extend(("", f"@{slot}", "", *component_lines(component)))
	return lines, layout
