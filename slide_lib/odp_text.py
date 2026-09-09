"""Project resolved text, lists, links, and tables into editable ODF content."""

# Standard Library
import xml.etree.ElementTree

# Local Modules
import slide_lib.layout_content
import slide_lib.layout_model
import slide_lib.layout_primitives
import slide_lib.presentation_theme


OFFICE_NS = "urn:oasis:names:tc:opendocument:xmlns:office:1.0"
STYLE_NS = "urn:oasis:names:tc:opendocument:xmlns:style:1.0"
TEXT_NS = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
FO_NS = "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
XLINK_NS = "http://www.w3.org/1999/xlink"
TABLE_NS = "urn:oasis:names:tc:opendocument:xmlns:table:1.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"
_FOREGROUND = "172033"
_ROLE_COLORS = {
	slide_lib.layout_primitives.StyleRole.ACCENT: "24578F",
	slide_lib.layout_primitives.StyleRole.TABLE_HEADER: "24578F",
	slide_lib.layout_primitives.StyleRole.MUTED: "526176",
	slide_lib.layout_primitives.StyleRole.DECORATION: "FFFFFF",
}

for _prefix, _namespace in (("office", OFFICE_NS), ("style", STYLE_NS),
		("text", TEXT_NS), ("fo", FO_NS), ("xlink", XLINK_NS),
		("table", TABLE_NS)):
	xml.etree.ElementTree.register_namespace(_prefix, _namespace)


#============================================
def _qname(namespace: str, local_name: str) -> str:
	"""Build one ElementTree-qualified name."""
	result = f"{{{namespace}}}{local_name}"
	return result


#============================================
def _color_for(role: slide_lib.layout_primitives.StyleRole) -> str:
	"""Return the resolved ODP palette color for a semantic role."""
	result = _ROLE_COLORS.get(role, _FOREGROUND)
	return result


#============================================
def _points(value: float) -> str:
	"""Format one exact point-valued layout fact for ODF."""
	result = f"{value:.4f}pt"
	return result


#============================================
def _centimeters_x(value: float, deck: slide_lib.layout_model.LayoutDeck,
		theme: slide_lib.presentation_theme.PresentationTheme) -> str:
	"""Convert a horizontal logical measurement to native centimeters."""
	result = f"{value * theme.slide_width_cm / deck.canvas.width:.6f}cm"
	return result


#============================================
def _centimeters_y(value: float, deck: slide_lib.layout_model.LayoutDeck,
		theme: slide_lib.presentation_theme.PresentationTheme) -> str:
	"""Convert a vertical logical measurement to native centimeters."""
	result = f"{value * theme.slide_height_cm / deck.canvas.height:.6f}cm"
	return result


#============================================
def _text_alignment(value: slide_lib.layout_primitives.HorizontalAlignment) -> str:
	"""Map neutral paragraph alignment to ODF values."""
	result = {
		slide_lib.layout_primitives.HorizontalAlignment.START: "start",
		slide_lib.layout_primitives.HorizontalAlignment.CENTER: "center",
		slide_lib.layout_primitives.HorizontalAlignment.END: "end",
		slide_lib.layout_primitives.HorizontalAlignment.JUSTIFY: "justify",
	}[value]
	return result


#============================================
def add_list_styles(automatic: xml.etree.ElementTree.Element,
		deck: slide_lib.layout_model.LayoutDeck,
		theme: slide_lib.presentation_theme.PresentationTheme) -> None:
	"""Write native ordered and unordered list levels from the shared theme.

	Args:
		automatic: ODF automatic-styles element that receives the list styles.
		deck: Compiled physical deck defining the logical canvas.
		theme: Validated presentation theme defining list geometry.
	"""
	for kind, style_name in (
			(slide_lib.layout_primitives.ListKind.UNORDERED, "DjotBullets"),
			(slide_lib.layout_primitives.ListKind.ORDERED, "DjotNumbers")):
		list_style = xml.etree.ElementTree.SubElement(automatic, _qname(TEXT_NS, "list-style"), {
			_qname(STYLE_NS, "name"): style_name,
		})
		for level, level_theme in enumerate(theme.list_levels, start=1):
			if kind is slide_lib.layout_primitives.ListKind.ORDERED:
				level_style = xml.etree.ElementTree.SubElement(list_style,
					_qname(TEXT_NS, "list-level-style-number"), {
						_qname(TEXT_NS, "level"): str(level),
						_qname(STYLE_NS, "num-format"): "1",
						_qname(STYLE_NS, "num-suffix"): ".",
					})
			else:
				level_style = xml.etree.ElementTree.SubElement(list_style,
					_qname(TEXT_NS, "list-level-style-bullet"), {
						_qname(TEXT_NS, "level"): str(level),
						_qname(TEXT_NS, "bullet-char"): level_theme.bullet_character,
					})
			properties = xml.etree.ElementTree.SubElement(level_style,
				_qname(STYLE_NS, "list-level-properties"), {
					_qname(TEXT_NS, "space-before"): _centimeters_x(
						level_theme.bullet_position, deck, theme),
					_qname(TEXT_NS, "min-label-width"): _centimeters_x(
						level_theme.text_position - level_theme.bullet_position, deck, theme),
				})
			properties.set(_qname(TEXT_NS, "min-label-distance"), "0cm")


#============================================
def write_text(parent: xml.etree.ElementTree.Element,
		automatic: xml.etree.ElementTree.Element,
		content: slide_lib.layout_content.TextContent, slide_index: int,
		object_index: int, target_ids: dict[str, str],
		reveal_targets: tuple[slide_lib.layout_model.RevealTarget, ...]) -> None:
	"""Write editable paragraphs, native lists, styled runs, and links.

	Args:
		parent: ODF text container that receives paragraphs or lists.
		automatic: ODF automatic-styles element that receives generated styles.
		content: Compiler-resolved editable text content.
		slide_index: Zero-based physical slide index used for deterministic names.
		object_index: Zero-based object index used for deterministic names.
		target_ids: Mapping from plan reveal targets to ODF XML identifiers.
		reveal_targets: Reveal targets attached to the containing object.
	"""
	paragraph_targets = {target.paragraph_indexes[0]: target_ids[target.target_id]
		for target in reveal_targets if target.paragraph_indexes}
	list_stack: list[tuple[slide_lib.layout_primitives.ListKind,
		xml.etree.ElementTree.Element, xml.etree.ElementTree.Element]] = []
	for paragraph_index, paragraph in enumerate(content.paragraphs):
		if not paragraph.display:
			continue
		style_name = f"DjotParagraph{slide_index + 1}_{object_index + 1}_{paragraph_index + 1}"
		_add_paragraph_style(automatic, style_name, paragraph)
		attributes = {_qname(TEXT_NS, "style-name"): style_name}
		if paragraph_index in paragraph_targets:
			attributes[_qname(XML_NS, "id")] = paragraph_targets[paragraph_index]
			attributes[_qname(TEXT_NS, "id")] = paragraph_targets[paragraph_index]
		metadata = paragraph.list_metadata
		if metadata is None:
			list_stack = []
			paragraph_parent = parent
		else:
			paragraph_parent, list_stack = _append_list_item(parent, metadata, list_stack)
		paragraph_element = xml.etree.ElementTree.SubElement(paragraph_parent,
			_qname(TEXT_NS, "p"), attributes)
		_write_inlines(paragraph_element, automatic, paragraph, slide_index,
			object_index, paragraph_index)


#============================================
def _append_list_item(parent: xml.etree.ElementTree.Element,
		metadata: slide_lib.layout_content.ListMetadata,
		stack: list[tuple[slide_lib.layout_primitives.ListKind,
			xml.etree.ElementTree.Element,
			xml.etree.ElementTree.Element]]) -> tuple[xml.etree.ElementTree.Element,
		list[tuple[slide_lib.layout_primitives.ListKind,
			xml.etree.ElementTree.Element, xml.etree.ElementTree.Element]]]:
	"""Append one item to a persistent, genuinely hierarchical native ODF list."""
	level = metadata.level
	if level > len(stack):
		raise ValueError("native list level cannot skip its parent")
	style_name = "DjotNumbers" if metadata.kind is \
		slide_lib.layout_primitives.ListKind.ORDERED else "DjotBullets"
	if level == len(stack):
		list_parent = parent if level == 0 else stack[-1][2]
		list_element = xml.etree.ElementTree.SubElement(list_parent, _qname(TEXT_NS, "list"), {
			_qname(TEXT_NS, "style-name"): style_name,
		})
		stack.append((metadata.kind, list_element, list_element))
	else:
		stack = stack[:level + 1]
		kind, list_element, _previous_item = stack[level]
		if kind is not metadata.kind:
			list_parent = parent if level == 0 else stack[level - 1][2]
			list_element = xml.etree.ElementTree.SubElement(list_parent,
				_qname(TEXT_NS, "list"), {_qname(TEXT_NS, "style-name"): style_name})
	item_attributes = {}
	if metadata.kind is slide_lib.layout_primitives.ListKind.ORDERED:
		item_attributes[_qname(TEXT_NS, "start-value")] = str(metadata.start)
	item = xml.etree.ElementTree.SubElement(list_element, _qname(TEXT_NS, "list-item"),
		item_attributes)
	stack[level] = (metadata.kind, list_element, item)
	return item, stack


#============================================
def _add_paragraph_style(automatic: xml.etree.ElementTree.Element, style_name: str,
		paragraph: slide_lib.layout_content.TextParagraph) -> None:
	"""Serialize compiler-resolved paragraph spacing without choosing new values."""
	style = xml.etree.ElementTree.SubElement(automatic, _qname(STYLE_NS, "style"), {
		_qname(STYLE_NS, "name"): style_name,
		_qname(STYLE_NS, "family"): "paragraph",
	})
	properties = paragraph.properties
	attributes = {
		_qname(FO_NS, "text-align"): _text_alignment(properties.horizontal_alignment),
		_qname(FO_NS, "margin-top"): _points(properties.space_before_pt),
		_qname(FO_NS, "margin-bottom"): _points(properties.space_after_pt),
		_qname(FO_NS, "line-height"): _points(properties.line_spacing_pt),
	}
	if paragraph.list_metadata is None:
		attributes[_qname(FO_NS, "margin-left")] = _points(properties.indent_start_pt)
		attributes[_qname(FO_NS, "margin-right")] = _points(properties.indent_end_pt)
		attributes[_qname(FO_NS, "text-indent")] = _points(properties.first_line_indent_pt)
	paragraph_properties = xml.etree.ElementTree.SubElement(style,
		_qname(STYLE_NS, "paragraph-properties"), attributes)
	if properties.tab_stops_pt:
		tabs = xml.etree.ElementTree.SubElement(paragraph_properties,
			_qname(STYLE_NS, "tab-stops"))
		for position in properties.tab_stops_pt:
			xml.etree.ElementTree.SubElement(tabs, _qname(STYLE_NS, "tab-stop"), {
				_qname(STYLE_NS, "position"): _points(position),
			})


#============================================
def _write_inlines(parent: xml.etree.ElementTree.Element,
		automatic: xml.etree.ElementTree.Element,
		paragraph: slide_lib.layout_content.TextParagraph, slide_index: int,
		object_index: int, paragraph_index: int) -> None:
	"""Write styled text, explicit line breaks, and hyperlink semantics."""
	for inline_index, inline in enumerate(paragraph.inlines):
		if isinstance(inline, slide_lib.layout_content.LineBreak):
			xml.etree.ElementTree.SubElement(parent, _qname(TEXT_NS, "line-break"))
			continue
		style_name = (f"DjotText{slide_index + 1}_{object_index + 1}_"
			f"{paragraph_index + 1}_{inline_index + 1}")
		_add_text_style(automatic, style_name, inline.style,
			paragraph.typography.selected_size_pt)
		container = parent
		if inline.style.link_url is not None:
			container = xml.etree.ElementTree.SubElement(parent, _qname(TEXT_NS, "a"), {
				_qname(XLINK_NS, "href"): inline.style.link_url,
				_qname(XLINK_NS, "type"): "simple",
			})
		span = xml.etree.ElementTree.SubElement(container, _qname(TEXT_NS, "span"), {
			_qname(TEXT_NS, "style-name"): style_name,
		})
		# ASVS 1.1.2: retain canonical text here; ElementTree performs final XML escaping.
		span.text = inline.text


#============================================
def _add_text_style(automatic: xml.etree.ElementTree.Element, style_name: str,
		style_value: slide_lib.layout_content.RunStyle, size_pt: float) -> None:
	"""Define one resolved run style with no host-font substitution."""
	style = xml.etree.ElementTree.SubElement(automatic, _qname(STYLE_NS, "style"), {
		_qname(STYLE_NS, "name"): style_name,
		_qname(STYLE_NS, "family"): "text",
	})
	color = style_value.foreground if len(style_value.foreground) == 6 else _FOREGROUND
	attributes = {
		_qname(STYLE_NS, "font-name"): style_value.font_family,
		_qname(FO_NS, "font-family"): style_value.font_family,
		_qname(FO_NS, "font-size"): _points(size_pt),
		_qname(FO_NS, "color"): f"#{color}",
		_qname(FO_NS, "font-weight"): "bold" if style_value.bold else "normal",
		_qname(FO_NS, "font-style"): "italic" if style_value.italic else "normal",
	}
	if style_value.underline:
		attributes[_qname(STYLE_NS, "text-underline-style")] = "solid"
		attributes[_qname(STYLE_NS, "text-underline-width")] = "auto"
	xml.etree.ElementTree.SubElement(style, _qname(STYLE_NS, "text-properties"), attributes)


#============================================
def write_table(parent: xml.etree.ElementTree.Element,
		automatic: xml.etree.ElementTree.Element, object_id: str,
		content: slide_lib.layout_content.TableContent, deck: slide_lib.layout_model.LayoutDeck,
		theme: slide_lib.presentation_theme.PresentationTheme,
		slide_index: int, object_index: int) -> None:
	"""Write one editable native ODF table, including row and column spans.

	Args:
		parent: Existing ODF frame that receives the table.
		automatic: ODF automatic-styles element that receives table styles.
		object_id: Stable plan object identity used as the table name.
		content: Compiler-resolved table content and geometry.
		deck: Compiled physical deck defining the logical canvas.
		theme: Validated presentation theme defining physical page size.
		slide_index: Zero-based physical slide index used for deterministic names.
		object_index: Zero-based object index used for deterministic names.
	"""
	table = xml.etree.ElementTree.SubElement(parent, _qname(TABLE_NS, "table"), {
		_qname(TABLE_NS, "name"): object_id,
	})
	for column_index, width in enumerate(content.column_widths):
		column_style = f"DjotColumn{slide_index + 1}_{object_index + 1}_{column_index + 1}"
		_add_dimension_style(automatic, column_style, "table-column", "column-width",
			_centimeters_x(width, deck, theme))
		xml.etree.ElementTree.SubElement(table, _qname(TABLE_NS, "table-column"), {
			_qname(TABLE_NS, "style-name"): column_style,
		})
	rows = content.header_rows + content.body_rows
	grid = _table_grid(content)
	for row_index, _row in enumerate(rows):
		row_style = f"DjotRow{slide_index + 1}_{object_index + 1}_{row_index + 1}"
		_add_dimension_style(automatic, row_style, "table-row", "row-height",
			_centimeters_y(content.row_heights[row_index], deck, theme))
		row_element = xml.etree.ElementTree.SubElement(table, _qname(TABLE_NS, "table-row"), {
			_qname(TABLE_NS, "style-name"): row_style,
		})
		for column_index, cell in enumerate(grid[row_index]):
			if cell is None:
				xml.etree.ElementTree.SubElement(row_element,
					_qname(TABLE_NS, "covered-table-cell"))
				continue
			cell_style = (
				f"DjotCell{slide_index + 1}_{object_index + 1}_"
				f"{row_index + 1}_{column_index + 1}")
			_add_cell_style(automatic, cell_style, row_index < len(content.header_rows), content)
			attributes = {
				_qname(TABLE_NS, "style-name"): cell_style,
				_qname(OFFICE_NS, "value-type"): "string",
			}
			if cell.column_span > 1:
				attributes[_qname(TABLE_NS, "number-columns-spanned")] = str(cell.column_span)
			if cell.row_span > 1:
				attributes[_qname(TABLE_NS, "number-rows-spanned")] = str(cell.row_span)
			cell_element = xml.etree.ElementTree.SubElement(row_element,
				_qname(TABLE_NS, "table-cell"), attributes)
			write_text(cell_element, automatic,
				slide_lib.layout_content.TextContent(cell.paragraphs), slide_index,
				object_index * 100 + row_index * 10 + column_index, {}, ())


#============================================
def _table_grid(content: slide_lib.layout_content.TableContent) -> list[
		list[slide_lib.layout_content.TableCell | None]]:
	"""Expand a validated spanned table into start cells and covered positions."""
	rows = content.header_rows + content.body_rows
	grid: list[list[slide_lib.layout_content.TableCell | None]] = [
		[None for _column in content.column_widths] for _row in rows]
	occupied = [[False for _column in content.column_widths] for _row in rows]
	for row_index, row in enumerate(rows):
		column_index = 0
		for cell in row.cells:
			while occupied[row_index][column_index]:
				column_index += 1
			grid[row_index][column_index] = cell
			for y in range(row_index, row_index + cell.row_span):
				for x in range(column_index, column_index + cell.column_span):
					occupied[y][x] = True
			column_index += cell.column_span
	return grid


#============================================
def _add_dimension_style(automatic: xml.etree.ElementTree.Element, name: str,
		family: str, property_name: str, value: str) -> None:
	"""Define one table row or column dimension selected by the compiler."""
	style = xml.etree.ElementTree.SubElement(automatic, _qname(STYLE_NS, "style"), {
		_qname(STYLE_NS, "name"): name,
		_qname(STYLE_NS, "family"): family,
	})
	xml.etree.ElementTree.SubElement(style, _qname(STYLE_NS, f"{family}-properties"), {
		_qname(STYLE_NS, property_name): value,
	})


#============================================
def _add_cell_style(automatic: xml.etree.ElementTree.Element, name: str,
		header: bool, content: slide_lib.layout_content.TableContent) -> None:
	"""Define native table fill and border semantics."""
	style = xml.etree.ElementTree.SubElement(automatic, _qname(STYLE_NS, "style"), {
		_qname(STYLE_NS, "name"): name,
		_qname(STYLE_NS, "family"): "table-cell",
	})
	role = content.style.header_role if header else content.style.body_role
	xml.etree.ElementTree.SubElement(style, _qname(STYLE_NS, "table-cell-properties"), {
		_qname(FO_NS, "background-color"): f"#{_color_for(role)}",
		_qname(FO_NS, "border"): f"{_points(content.style.border_width_pt)} solid "
			f"#{_color_for(content.style.border_role)}",
	})
