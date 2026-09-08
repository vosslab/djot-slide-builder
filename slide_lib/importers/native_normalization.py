"""Canonical native fallbacks for legacy spatial presentation structures."""

# Standard Library
from typing import Protocol


MAX_POSITIONED_LABELS = 12


class LineComponent(Protocol):
	"""Structural line surface required by native source-order normalization."""
	lines: tuple[str, ...]


#============================================
def one_panel_lines(heading: list[str], components: list[LineComponent]) -> list[str]:
	"""Collapse components into one standard panel while retaining visible source order."""
	local_headings = [line for component in components for line in component.lines
		if line.startswith("## ")]
	body_groups: list[list[str]] = []
	for component in components:
		group = [line[3:] if line.startswith("## ") else line for line in component.lines
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
