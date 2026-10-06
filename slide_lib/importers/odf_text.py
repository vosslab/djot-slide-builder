"""Read inherited inline formatting and list paragraphs from ODF text."""

import dataclasses
import re
import urllib.parse
import xml.etree.ElementTree

import slide_lib.importers.odf_styles as odf_styles
import slide_lib.importers.source_model as source_model
import slide_lib.presentation_theme

NS = {
	"draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
	"fo": "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0",
	"office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
	"presentation": "urn:oasis:names:tc:opendocument:xmlns:presentation:1.0",
	"style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
	"svg": "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0",
	"table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
	"text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
	"xlink": "http://www.w3.org/1999/xlink",
}

SAFE_LINK_SCHEMES = frozenset({"http", "https", "mailto"})
MAX_TEXT_SPACES = 2_000


@dataclasses.dataclass(frozen=True)
class TextStyle:
	"""Inherited source formatting, including explicit resets."""

	color: str = ""
	bold: bool = False
	underline: bool = False
	italic: bool = False
	transform: str = "none"


def text_style(element: xml.etree.ElementTree.Element,
		definitions: dict[str, odf_styles.StyleDefinition], inherited: TextStyle) -> TextStyle:
	"""Resolve properties independently so partial styles retain their context."""
	source_color = odf_styles.attribute(element, definitions, qname("fo", "color"))
	color = inherited.color
	if source_color is not None:
		color = slide_lib.presentation_theme.source_text_color_name(source_color) or ""
		if not color and re.fullmatch(r"#[0-9a-fA-F]{6}", source_color):
			if slide_lib.presentation_theme.source_text_color_requires_review(source_color):
				color = source_color.upper()
			elif inherited.color:
				color = "black"
	bold, underline = odf_styles.emphasis(element, definitions, inherited.bold, inherited.underline)
	font_style = odf_styles.attribute(element, definitions, qname("fo", "font-style"))
	italic = inherited.italic if font_style is None else font_style in {"italic", "oblique"}
	transform = odf_styles.attribute(element, definitions, qname("fo", "text-transform"))
	return TextStyle(color, bold, underline, italic,
		inherited.transform if transform is None else transform)

def qname(prefix: str, local_name: str) -> str:
	"""Build an ODF text attribute name."""
	result = f"{{{NS[prefix]}}}{local_name}"
	return result


def safe_hyperlink(address: str | None) -> str:
	"""Return a direct http, https, or mailto source link when safe."""
	if not address:
		return ""
	parsed = urllib.parse.urlsplit(address)
	if parsed.scheme.lower() not in SAFE_LINK_SCHEMES:
		return ""
	return address


#============================================
def trim_runs(runs: list[source_model.TextRun]) -> tuple[source_model.TextRun, ...]:
	"""Strip paragraph-edge whitespace while retaining source run boundaries."""
	while runs and not runs[0].text:
		runs.pop(0)
	while runs and not runs[-1].text:
		runs.pop()
	if not runs:
		return ()
	runs[0] = dataclasses.replace(runs[0], text=runs[0].text.lstrip())
	runs[-1] = dataclasses.replace(runs[-1], text=runs[-1].text.rstrip())
	return tuple(run for run in runs if run.text)


#============================================
def append_run(runs: list[source_model.TextRun], text: str, link: str,
		style: TextStyle) -> None:
	"""Retain one visible source character sequence when it is nonempty."""
	if text:
		if style.transform == "uppercase":
			text = text.upper()
		elif style.transform == "lowercase":
			text = text.lower()
		runs.append(source_model.TextRun(text, link, style.color, style.bold,
			style.underline, style.italic))


#============================================
def inline_runs(element: xml.etree.ElementTree.Element,
		definitions: dict[str, odf_styles.StyleDefinition], link: str = "",
		color: str = "", inherited: TextStyle | None = None) -> tuple[source_model.TextRun, ...]:
	"""Extract styled ODF inline text and allow-listed link targets."""
	runs: list[source_model.TextRun] = []

	def visit(node: xml.etree.ElementTree.Element, inherited_link: str,
			inherited_style: TextStyle) -> None:
		style = text_style(node, definitions, inherited_style)
		append_run(runs, node.text or "", inherited_link, style)
		for child in node:
			if child.tag == qname("text", "s"):
				count_raw = child.get(qname("text", "c"), "1")
				if not count_raw.isdigit() or int(count_raw) > MAX_TEXT_SPACES:
					raise ValueError("ODF text space count exceeds the supported range")
				append_run(runs, " " * int(count_raw), inherited_link, style)
			elif child.tag == qname("text", "tab"):
				append_run(runs, "\t", inherited_link, style)
			elif child.tag == qname("text", "line-break"):
				append_run(runs, " ", inherited_link, style)
			else:
				child_link = inherited_link
				if child.tag == qname("text", "a"):
					child_link = safe_hyperlink(child.get(qname("xlink", "href")))
				visit(child, child_link, style)
			append_run(runs, child.tail or "", inherited_link, style)

	visit(element, link, TextStyle(color=color) if inherited is None else inherited)
	return trim_runs(runs)


#============================================
def text_paragraphs(container: xml.etree.ElementTree.Element,
		definitions: dict[str, odf_styles.StyleDefinition],
		inherited: TextStyle = TextStyle()) -> tuple[
	tuple[int, tuple[source_model.TextRun, ...]], ...,
]:
	"""Extract paragraphs and explicit ODF nested-list levels in source order."""
	lines: list[tuple[int, tuple[source_model.TextRun, ...]]] = []

	def visit_children(parent: xml.etree.ElementTree.Element, level: int,
			context: TextStyle) -> None:
		style = text_style(parent, definitions, context)
		for child in parent:
			if child.tag in {qname("text", "p"), qname("text", "h")}:
				runs = inline_runs(child, definitions, inherited=style)
				if runs:
					lines.append((level, runs))
			elif child.tag == qname("text", "list"):
				visit_list(child, level, style)
			else:
				visit_children(child, level, style)

	def visit_list(list_element: xml.etree.ElementTree.Element, level: int,
			context: TextStyle) -> None:
		style = text_style(list_element, definitions, context)
		for item in list_element:
			if item.tag not in {qname("text", "list-header"), qname("text", "list-item")}:
				continue
			for child in item:
				if child.tag in {qname("text", "p"), qname("text", "h")}:
					runs = inline_runs(child, definitions, inherited=style)
					if runs:
						lines.append((level, runs))
				elif child.tag == qname("text", "list"):
					visit_list(child, level + 1, style)
				else:
					visit_children(child, level, style)

	visit_children(container, 0, inherited)
	return tuple(lines)


#============================================
