"""Advisory typography checks using final compiled geometry and shared font metrics."""

import collections

import slide_lib.layout_content
import slide_lib.layout_measurement
import slide_lib.layout_primitives
import slide_lib.native_export
import slide_lib.presentation_theme
import slide_lib.typography


def paragraph_lines(paragraph: slide_lib.layout_content.TextParagraph, width: float,
		session: slide_lib.layout_measurement.MeasurementSession) -> list[tuple[str, float]]:
	"""Return measured text and ink widths, excluding trailing whitespace."""
	tokens = tuple((run.text, run.style.font_family, run.style.bold, run.style.italic,
		run.style.literal_url) if isinstance(run, slide_lib.layout_content.TextRun)
		else ("\n", "", False, False, False) for run in paragraph.inlines)
	if paragraph.list_metadata is not None:
		width -= session.theme.list_levels[paragraph.list_metadata.level].text_position
	size = paragraph.typography.selected_size_pt
	wrapped, _widths = session.wrap_tokens(tokens, size, max(width, 1.0), balance=False)
	lines = []
	for line in wrapped:
		text = "".join(token[0] for token in line).rstrip()
		remaining = len(text)
		ink_width = 0.0
		for value, family, bold, italic, _literal, selected_size, _index in line:
			part = value[:remaining]
			remaining -= len(part)
			ink_width += session.advance(family, bold, italic, selected_size, part)
		lines.append((text, ink_width))
	return lines


def typography_issue(lines: list[tuple[str, float]], title: bool = False) -> str | None:
	"""Flag wrapped titles or short final lines; single-line text is never a runt."""
	if len(lines) < 2:
		return None
	if title:
		return "title-wrap"
	if slide_lib.typography.has_runt(lines):
		return "runt"
	return None


def audit(input_value: str) -> dict[str, object]:
	"""Audit a Djot file or tree without writing decks or invoking LibreOffice."""
	root = slide_lib.native_export.find_repo_root()
	# ASVS 5.2.2: reuse source discovery and semantic parsing before compilation.
	paths = slide_lib.native_export.discover_decks(input_value, root, True)
	findings = []
	skipped = collections.Counter()
	slides = 0
	paragraphs = 0
	for path in paths:
		deck = slide_lib.native_export.parse_deck(path)
		compilation, theme = slide_lib.native_export.compile_deck(deck)
		session = slide_lib.layout_measurement.MeasurementSession(theme)
		for slide in compilation.plan.slides:
			if slide.hidden:
				skipped["hidden-slides"] += 1
				continue
			slides += 1
			for item in slide.objects:
				if item.source is None or not isinstance(item.content, slide_lib.layout_content.TextContent):
					continue
				is_title = item.style_role is slide_lib.layout_primitives.StyleRole.TITLE
				if is_title and slide.layout.layout_name in ("title-slide", "section", "subsection", "theend"):
					skipped["special-layout-titles"] += 1
					continue
				for index, paragraph in enumerate(item.content.paragraphs, 1):
					if not paragraph.display:
						continue
					available = item.rectangle.width
					if paragraph.list_metadata is not None:
						available -= theme.list_levels[paragraph.list_metadata.level].text_position
					for run in paragraph.inlines:
						if not isinstance(run, slide_lib.layout_content.TextRun) or not run.style.literal_url:
							continue
						if session.advance(run.style.font_family, run.style.bold, run.style.italic,
								run.style.size_pt, run.text) <= available:
							continue
						findings.append({"file": str(path), "slide": slide.identity.index + 1,
							"source_line": item.source.line, "object": item.object_id,
							"paragraph": index, "check": "url-too-wide", "text": run.text,
							"font_size_pt": run.style.size_pt,
							"message": "URL still exceeds its text region at the 12 pt floor"})
					if any(not isinstance(run, slide_lib.layout_content.TextRun)
							and not (isinstance(run, slide_lib.layout_content.LineBreak) and run.automatic)
							for run in paragraph.inlines):
						skipped["math-or-explicit-break-paragraphs"] += 1
						continue
					paragraphs += 1
					lines = paragraph_lines(paragraph, item.rectangle.width, session)
					issue = typography_issue(lines, is_title)
					if issue is None:
						continue
					if issue == "runt" and paragraph.typography.selected_size_pt >= theme.ordinary_body_size_pt \
							and not any(tail.display for tail in item.content.paragraphs[index:]):
						skipped["final-paragraph-runts-at-max-size"] += 1
						continue
					findings.append({
						"file": str(path), "slide": slide.identity.index + 1,
						"source_line": item.source.line, "object": item.object_id,
						"paragraph": index, "check": issue,
						"font_size_pt": paragraph.typography.selected_size_pt,
						"lines": [text for text, _width in lines],
						"last_to_previous_width": round(lines[-1][1] / lines[-2][1], 3)
							if lines[-2][1] else None,
					})
	result = {"measurement": "compiled layout estimate; verify final LibreOffice rendering",
		"decks": len(paths), "visible_slides": slides, "paragraphs_checked": paragraphs,
		"skipped": dict(skipped),
		"summary": dict(collections.Counter(item["check"] for item in findings)),
		"findings": findings}
	return result
