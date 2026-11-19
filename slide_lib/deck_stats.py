"""Count authored visuals in the visible slides of a Djot deck."""

# Standard Library
import collections
import pathlib

# Local Modules
import slide_lib.djot_parser
import slide_lib.layout_source_facts
import slide_lib.native_model


SECTION_HEADINGS = {"section", "subsection", "subsubsection"}
STRUCTURAL_LAYOUTS = SECTION_HEADINGS | {"title-slide", "theend", "blank"}
DEDICATED_IMAGE_LAYOUTS = {"big-image", "gallery", "image-comparison", "movie-panel"}

GROUP_LABELS = {
	"all_visible": "All visible slides",
	"panel_layouts": "Panel layouts",
	"without_section_headings": "Without section headings",
	"content": "Content slides",
	"content_without_bookends": "Content without bookends",
	"dedicated_image_layouts": "Dedicated image layouts",
}


#============================================
def slide_counts(slide: slide_lib.native_model.Slide) -> collections.Counter[str]:
	"""Classify a slide once, even when several images, tables or equations share it."""
	roots = slide.blocks + tuple(block for cell in slide.cells for block in cell.blocks)
	blocks = slide_lib.layout_source_facts.descendant_blocks(roots)
	images = sum(isinstance(block, slide_lib.native_model.Image) for block in blocks)
	table = any(isinstance(block, slide_lib.native_model.Table) for block in blocks)
	equation = any(isinstance(block, slide_lib.native_model.DisplayMath) for block in blocks)
	visual = bool(images or table or equation)
	counts = collections.Counter(slides=1, image_placements=images, image_slides=int(images > 0),
		table_slides=int(table), display_math_slides=int(equation), visual_slides=int(visual),
		no_visual_slides=int(not visual), text_only_slides=int(bool(blocks) and not visual))
	return counts


#============================================
def coverage(counts: collections.Counter[str]) -> dict[str, int | float | None]:
	"""Expose zero counts and make undefined percentages explicit for empty groups."""
	fields = ("slides", "image_slides", "table_slides", "display_math_slides", "visual_slides",
		"no_visual_slides", "text_only_slides")
	row: dict[str, int | float | None] = {field: counts[field] for field in fields}
	total = counts["slides"]
	for key in ("image", "visual", "text_only"):
		row[f"{key}_percent"] = round(100 * counts[f"{key}_slides"] / total, 1) if total else None
	return row


#============================================
def deck_statistics(path: pathlib.Path) -> dict:
	"""Report classroom coverage from the source, including inherited hidden flags."""
	if path.suffix != ".djot":
		raise ValueError(f"expected a .djot source file: {path}")
	# ASVS 5.3.2: the Djot loader resolves and bounds chapter includes. Asset bytes are unnecessary.
	deck = slide_lib.djot_parser.parse_deck(path.expanduser(), expand_course_links=False)
	layouts: dict[str, collections.Counter[str]] = {}
	for slide in deck.slides:
		if not slide.hidden:
			layouts.setdefault(slide.layout_class, collections.Counter()).update(slide_counts(slide))

	all_layouts = set(layouts)
	content = all_layouts - STRUCTURAL_LAYOUTS
	selections = {
		"all_visible": all_layouts,
		"panel_layouts": {name for name in all_layouts if name == "one-panel" or name.endswith("-panels")},
		"without_section_headings": all_layouts - SECTION_HEADINGS,
		"content": content,
		"content_without_bookends": content - {"bookend"},
		"dedicated_image_layouts": all_layouts & DEDICATED_IMAGE_LAYOUTS,
	}
	groups = {}
	for group, selected in selections.items():
		counts: collections.Counter[str] = collections.Counter()
		for layout in selected:
			counts.update(layouts[layout])
		groups[group] = coverage(counts)
	visible = sum(counts["slides"] for counts in layouts.values())
	report = {
		"authored_slides": len(deck.slides), "hidden_slides": len(deck.slides) - visible,
		"image_placements": sum(counts["image_placements"] for counts in layouts.values()),
		"groups": groups, "layouts": {name: coverage(layouts[name]) for name in sorted(layouts)},
	}
	return report


#============================================
def format_report(report: dict) -> str:
	"""Format counts and percentages from the same rows used by JSON output."""
	lines = [f"Authored slides: {report['authored_slides']}    Hidden: {report['hidden_slides']}"
		f"    Visible image placements: {report['image_placements']}"]
	columns = "{:<26} {:>6} {:>13} {:>6} {:>5} {:>13} {:>10} {:>13}"
	for heading, rows in (("Slide group", report["groups"]), ("Layout", report["layouts"])):
		lines.extend(("", columns.format(heading, "Slides", "With image", "Table", "Eqn", "Any visual",
			"No visual", "Text only")))
		for name, row in rows.items():
			label = GROUP_LABELS.get(name, name)
			formatted = {}
			for key in ("image", "visual", "text_only"):
				rate = row[f"{key}_percent"]
				percent = "n/a" if rate is None else f"{rate:.1f}%"
				count = row[f"{key}_slides"]
				formatted[key] = f"{count} ({percent})"
			lines.append(columns.format(label, row["slides"], formatted["image"], row["table_slides"],
				row["display_math_slides"], formatted["visual"], row["no_visual_slides"], formatted["text_only"]))
	lines.extend(("", "Visual = authored image, native table, or display equation. A slide counts once.",
		"Content excludes section headings, covers, closers, and blank slides."))
	result = "\n".join(lines)
	return result
