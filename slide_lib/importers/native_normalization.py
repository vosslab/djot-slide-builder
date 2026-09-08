"""Canonical native fallbacks for legacy spatial presentation structures."""

MAX_POSITIONED_LABELS = 12


#============================================
def component_lines(component: object) -> tuple[str, ...]:
	"""Read the emitter component line surface without creating a circular import."""
	lines = getattr(component, "lines", None)
	if not isinstance(lines, tuple) or any(not isinstance(line, str) for line in lines):
		raise TypeError("native normalization requires a tuple of component lines")
	return lines


#============================================
def one_panel_lines(heading: list[str], components: list[object]) -> list[str]:
	"""Collapse components into one standard panel while retaining visible source order."""
	component_groups = [component_lines(component) for component in components]
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
	lines = ["=== layout: one-panel", "", *heading, "", "@body", ""]
	if local_headings:
		lines.extend((local_headings[0], ""))
	return [*lines, *body]
