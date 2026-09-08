"""Native editable PPTX builders for the repository's slide-layout vocabulary."""

# Standard Library
import pathlib
from collections.abc import Callable
from dataclasses import dataclass

# PIP3 modules
import PIL.Image
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Emu, Pt

# Local Modules
import slide_lib.native_model
import slide_lib.layout_validation
import slide_lib.editable_text
import slide_lib.pptx_animation


PX = 9525
SLIDE_WIDTH = 1280
SLIDE_HEIGHT = 800
LEFT = 60.0
RIGHT = 1220.0
TITLE_TOP = 52.0
CONTENT_BOTTOM = 754.0
CELL_GUTTER = 42.0
GRID_GUTTER = 24.0
CSS_TO_OFFICE_POINTS = 0.75
BODY_LINE_HEIGHT = 1.3
LIST_ITEM_SPACE_EM = 0.25
MIN_READABLE_BODY_SIZE = 14.0
FONT_NAME = "OpenDyslexic"
URL_FONT_NAME = "PT Sans Narrow"
ACCENT = RGBColor(0x24, 0x57, 0x8F)
FOREGROUND = RGBColor(0x17, 0x20, 0x33)
MUTED = RGBColor(0x52, 0x61, 0x76)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
MULTIPLE_CHOICE_ANSWER_RECTANGLE = (820.0, 618.0, 360.0, 108.0)
MULTIPLE_CHOICE_POPUP_GUTTER = 24.0
# The full-width question stops above the popup's reserved bottom-right footprint.
MULTIPLE_CHOICE_QUESTION_RECTANGLE = (LEFT, 82.0, RIGHT - LEFT,
	MULTIPLE_CHOICE_ANSWER_RECTANGLE[1] - MULTIPLE_CHOICE_POPUP_GUTTER - 82.0)


LayoutError = slide_lib.layout_validation.LayoutError


@dataclass(frozen=True)
class LayoutSpec:
	"""Stable authoring contract and renderer for one named slide layout."""
	name: str
	cell_count: int
	allows_root_body: bool
	vertical_title: bool
	vertical_cells: frozenset[int]
	builder: Callable[[object, object, object, "LayoutSpec"], None]
	slot_names: tuple[str, ...] = ()
	allows_title: bool = False
	allows_subtitle: bool = False
	topology_matchable: bool = False


@dataclass(frozen=True)
class TitleBodyPlan:
	"""One validated title and content allocation before native shapes exist."""
	title_rectangle: tuple[float, float, float, float] | None
	title_size: float
	content_rectangle: tuple[float, float, float, float]
	vertical_title: bool


@dataclass(frozen=True)
class CellBodyPlan:
	"""One shared local-H2 size and remaining body rectangle for a cell."""
	body_rectangle: tuple[float, float, float, float]
	heading_size: float | None


@dataclass(frozen=True)
class FlowStep:
	"""One source-ordered native text or image placement within a mixed cell."""
	block: slide_lib.native_model.Paragraph | slide_lib.native_model.ListBlock | slide_lib.native_model.Image
	rectangle: tuple[float, float, float, float]


@dataclass(frozen=True)
class CellFlowPlan:
	"""One preflight-approved ordered text/image flow and shared text size."""
	steps: tuple[FlowStep, ...]
	text_size: float


#============================================
def px(value: float) -> Emu:
	"""Convert a 1280x800 CSS-pixel coordinate to Office EMUs."""
	return Emu(round(value * PX))


#============================================
def css_px_to_pt(value: float) -> float:
	"""Convert CSS font pixels to Office points exactly once."""
	return value * CSS_TO_OFFICE_POINTS


#============================================
def inline_text(inlines: tuple[slide_lib.native_model.Inline, ...]) -> str:
	"""Return visible authored text while retaining native runs for rendering."""
	parts: list[str] = []
	for inline in inlines:
		if isinstance(inline, (slide_lib.native_model.Text, slide_lib.native_model.InlineCode)):
			parts.append(inline.value)
		elif isinstance(inline, slide_lib.native_model.InlineMath):
			raise LayoutError("InlineMath requires source validation before native rendering")
		elif isinstance(inline, slide_lib.native_model.Break):
			parts.append(" ")
		else:
			parts.append(inline_text(inline.children))
	return "".join(parts).strip()


#============================================
def add_textbox(slide: object, left: float, top: float, width: float, height: float,
		vertical_anchor: object = MSO_ANCHOR.TOP, vertical_text: bool = False) -> object:
	"""Add one editable native text frame with Office autofit protection."""
	shape = slide.shapes.add_textbox(px(left), px(top), px(width), px(height))
	frame = shape.text_frame
	frame.clear()
	frame.margin_left = frame.margin_right = 0
	frame.margin_top = frame.margin_bottom = 0
	frame.vertical_anchor = vertical_anchor
	frame.word_wrap = True
	body_properties = frame._txBody.bodyPr
	for child in list(body_properties):
		if child.tag.endswith(("noAutofit", "normAutofit", "spAutoFit")):
			body_properties.remove(child)
	autofit = OxmlElement("a:normAutofit")
	autofit.set("fontScale", "100000")
	autofit.set("lnSpcReduction", "0")
	body_properties.append(autofit)
	if vertical_text:
		body_properties.set("vert", "vert")
	return frame


#============================================
def write_run(run: object, text: str, size: float, color: object, bold: bool = False,
		italic: bool = False, url: str | None = None, displayed_url: bool = False) -> None:
	"""Apply the repository font contract to one editable run."""
	run.text = text
	run.font.name = URL_FONT_NAME if displayed_url else FONT_NAME
	run.font.size = Pt(css_px_to_pt(size))
	run.font.bold = bold
	run.font.italic = italic
	run.font.color.rgb = color
	if url is not None:
		run.hyperlink.address = url
		run.font.underline = True


#============================================
def add_inline_runs(paragraph: object, inlines: tuple[slide_lib.native_model.Inline, ...], size: float,
		color: object = FOREGROUND, bold: bool = False, italic: bool = False,
		url: str | None = None, displayed_url: bool = False) -> None:
	"""Write the typed inline tree as editable, formatted Office text runs."""
	for inline in inlines:
		if isinstance(inline, slide_lib.native_model.Text):
			write_run(paragraph.add_run(), inline.value, size, color, bold, italic, url, displayed_url)
		elif isinstance(inline, slide_lib.native_model.InlineCode):
			write_run(paragraph.add_run(), inline.value, size, color, bold, italic, url, displayed_url)
		elif isinstance(inline, slide_lib.native_model.InlineMath):
			raise LayoutError("InlineMath requires source validation before native rendering")
		elif isinstance(inline, slide_lib.native_model.Break):
			paragraph.add_line_break()
		elif isinstance(inline, slide_lib.native_model.Strong):
			add_inline_runs(paragraph, inline.children, size, color, True, italic, url, displayed_url)
		elif isinstance(inline, slide_lib.native_model.Emphasis):
			add_inline_runs(paragraph, inline.children, size, color, bold, True, url, displayed_url)
		elif isinstance(inline, slide_lib.native_model.Link):
			is_literal_url = inline_text(inline.children) == inline.url
			add_inline_runs(paragraph, inline.children, size, ACCENT, bold, italic, inline.url, is_literal_url)
	if not paragraph.runs:
		write_run(paragraph.add_run(), "", size, color, bold, italic, url, displayed_url)


#============================================
def flatten_list(block: slide_lib.native_model.ListBlock, level: int = 0) -> list[tuple[tuple[slide_lib.native_model.Inline, ...], int, bool, bool, int]]:
	"""Flatten nested lists into Office paragraphs, preserving ordered starts."""
	return [(paragraph.inlines, paragraph.level + level, paragraph.ordered,
		paragraph.paragraph_only, paragraph.start) for paragraph in
		slide_lib.editable_text.project_list(block)]


#============================================
def body_parts(blocks: tuple[slide_lib.native_model.Block, ...]) -> tuple[list[slide_lib.native_model.Heading], list[tuple[tuple[slide_lib.native_model.Inline, ...], int, bool, bool, int]], list[slide_lib.native_model.Image], list[slide_lib.native_model.Table]]:
	"""Classify already typed blocks without reparsing canonical Markdown."""
	headings: list[slide_lib.native_model.Heading] = []
	items: list[tuple[tuple[slide_lib.native_model.Inline, ...], int, bool, bool, int]] = []
	images: list[slide_lib.native_model.Image] = []
	tables: list[slide_lib.native_model.Table] = []
	for block in blocks:
		if isinstance(block, slide_lib.native_model.Heading):
			headings.append(block)
		elif isinstance(block, slide_lib.native_model.Paragraph):
			items.append((block.inlines, 0, False, True, 1))
		elif isinstance(block, slide_lib.native_model.ListBlock):
			items.extend(flatten_list(block))
		elif isinstance(block, slide_lib.native_model.Image):
			images.append(block)
		elif isinstance(block, slide_lib.native_model.Table):
			tables.append(block)
	return headings, items, images, tables


#============================================
def wrapped_line_count(inlines: tuple[slide_lib.native_model.Inline, ...], size: float, width: float,
		level: int = 0) -> int:
	"""Estimate wrapped editable text lines conservatively."""
	available_width = max(width - level * size * 1.43, size * 3)
	characters_per_line = max(int(available_width / (size * 0.54)), 1)
	words = inline_text(inlines).split()
	if not words:
		return 1
	lines, current = 1, 0
	for word in words:
		if current and current + len(word) + 1 > characters_per_line:
			lines, current = lines + 1, len(word)
		else:
			current += len(word) + (1 if current else 0)
		lines += max((len(word) - 1) // characters_per_line, 0)
	return lines


#============================================
def estimate_items_height(items: list[tuple[tuple[slide_lib.native_model.Inline, ...], int, bool, bool, int]], size: float, width: float) -> float:
	"""Estimate native paragraph height in CSS pixels."""
	return sum(wrapped_line_count(inlines, size, width, level) * size * BODY_LINE_HEIGHT +
		size * LIST_ITEM_SPACE_EM for inlines, level, _, _, _ in items)


#============================================
def fit_body_size(item_sets: list[list[tuple[tuple[slide_lib.native_model.Inline, ...], int, bool, bool, int]]], width: float,
		height: float, preferred_size: float, source: slide_lib.native_model.SourceLocation,
		context: str) -> float:
	"""Choose one shared readable body size or report a capacity violation."""
	for quarter_points in range(int(preferred_size * 4), int(MIN_READABLE_BODY_SIZE * 4) - 1, -1):
		size = quarter_points / 4
		if all(estimate_items_height(items, size, width) <= height for items in item_sets):
			return size
	raise LayoutError(f"{source.path}:{source.line}: {context} content cannot fit within the supported readable minimum of "
		f"{MIN_READABLE_BODY_SIZE:g} CSS px")


#============================================
def table_dimensions(table: slide_lib.native_model.Table) -> tuple[int, int]:
	"""Return already validated native table row and column counts."""
	column_count = len(table.headers) if table.headers else len(table.rows[0])
	return len(table.rows) + (1 if table.headers else 0), column_count


#============================================
def estimate_table_height(table: slide_lib.native_model.Table, size: float, width: float) -> float:
	"""Estimate equal-column wrapped cell rows within one native table rectangle."""
	_, column_count = table_dimensions(table)
	cell_width = width / column_count
	rows = ((table.headers,) if table.headers else ()) + table.rows
	return sum(max(wrapped_line_count(cell, size, cell_width) for cell in row) * size * BODY_LINE_HEIGHT +
		8 for row in rows)


#============================================
def fit_table_size(table: slide_lib.native_model.Table, width: float, height: float,
		context: str) -> float:
	"""Choose readable shared native table type before any table shape allocation."""
	for quarter_points in range(22 * 4, int(MIN_READABLE_BODY_SIZE * 4) - 1, -1):
		size = quarter_points / 4
		if estimate_table_height(table, size, width) <= height:
			return size
	raise layout_error(table.location,
		f"{context} table cannot fit within the supported readable minimum of {MIN_READABLE_BODY_SIZE:g} CSS px")


#============================================
def render_table(slide: object, table: slide_lib.native_model.Table,
		rectangle: tuple[float, float, float, float], context: str) -> None:
	"""Render one selectable native table with its typed editable cell runs."""
	left, top, width, height = rectangle
	row_count, column_count = table_dimensions(table)
	size = fit_table_size(table, width, height, context)
	shape = slide.shapes.add_table(row_count, column_count, px(left), px(top), px(width), px(height))
	native_table = shape.table
	rows = ((table.headers, True),) if table.headers else ()
	rows += tuple((row, False) for row in table.rows)
	for row_index, (row, is_header) in enumerate(rows):
		for column_index, inlines in enumerate(row):
			cell = native_table.cell(row_index, column_index)
			cell.margin_left = cell.margin_right = px(6)
			cell.margin_top = cell.margin_bottom = px(4)
			cell.vertical_anchor = MSO_ANCHOR.MIDDLE
			if is_header:
				cell.fill.solid()
				cell.fill.fore_color.rgb = ACCENT
			paragraph = cell.text_frame.paragraphs[0]
			paragraph.alignment = PP_ALIGN.LEFT
			add_inline_runs(paragraph, inlines, size, WHITE if is_header else FOREGROUND)
			if is_header:
				for run in paragraph.runs:
					run.font.bold = True


#============================================
def write_items(frame: object, items: list[tuple[tuple[slide_lib.native_model.Inline, ...], int, bool, bool, int]], size: float,
		first_paragraph: object | None = None) -> None:
	"""Write paragraphs using native bullet and automatic-number OOXML."""
	for index, (inlines, level, ordered, paragraph_only, start) in enumerate(items):
		paragraph = first_paragraph if index == 0 and first_paragraph is not None else (
			frame.paragraphs[0] if index == 0 else frame.add_paragraph())
		paragraph.level = level
		paragraph.space_after = Pt(css_px_to_pt(size * LIST_ITEM_SPACE_EM))
		paragraph.line_spacing = BODY_LINE_HEIGHT
		bullet = OxmlElement("a:buNone" if paragraph_only else
			"a:buAutoNum" if ordered else "a:buChar")
		if ordered:
			bullet.set("type", "arabicPeriod")
			bullet.set("startAt", str(start))
		elif not paragraph_only:
			bullet.set("char", "\u2022")
		paragraph._p.get_or_add_pPr().insert(0, bullet)
		add_inline_runs(paragraph, inlines, size)


#============================================
def add_background(slide: object) -> None:
	"""Write the white canvas and native blue accent rule."""
	slide.background.fill.solid()
	slide.background.fill.fore_color.rgb = WHITE
	accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(0), px(0), px(SLIDE_WIDTH), px(10))
	accent.fill.solid()
	accent.fill.fore_color.rgb = ACCENT
	accent.line.fill.background()


#============================================
def resolve_image_path(deck: object, image: slide_lib.native_model.Image) -> pathlib.Path:
	"""Resolve a component image within its canonical repository boundary."""
	image_path = (deck.asset_root / image.source).resolve()
	if not image_path.is_relative_to(deck.repo_root):
		raise LayoutError(f"{image.location.path}:{image.location.line}: component image must be inside the repository: {image.source}")
	if not image_path.is_file():
		raise LayoutError(f"{image.location.path}:{image.location.line}: component image is missing: {image.source}")
	return image_path


#============================================
def add_picture(slide: object, image_path: pathlib.Path, image: slide_lib.native_model.Image,
		left: float, top: float, width: float, height: float) -> object:
	"""Add one contained component picture with its authored description."""
	with PIL.Image.open(image_path) as opened_image:
		image_width, image_height = opened_image.size
	scale = min(width / image_width, height / image_height)
	display_width, display_height = image_width * scale, image_height * scale
	if display_width >= SLIDE_WIDTH or display_height >= SLIDE_HEIGHT:
		raise LayoutError(f"{image.location.path}:{image.location.line}: component image occupies a full slide: {image.source}")
	picture = slide.shapes.add_picture(str(image_path), px(left + (width - display_width) / 2),
		px(top + (height - display_height) / 2), px(display_width), px(display_height))
	picture.element.nvPicPr.cNvPr.set("descr", image.alt_text)
	return picture


#============================================
def image_flow_height(deck: slide_lib.native_model.Deck, image: slide_lib.native_model.Image,
		width: float) -> float:
	"""Reserve a full-width contained component image at its source aspect ratio."""
	image_path = resolve_image_path(deck, image)
	with PIL.Image.open(image_path) as opened_image:
		image_width, image_height = opened_image.size
	return width * image_height / image_width


#============================================
def plan_cell_flow(deck: slide_lib.native_model.Deck, cell: slide_lib.native_model.Cell,
		rectangle: tuple[float, float, float, float], preferred_size: float,
		context: str) -> CellFlowPlan | None:
	"""Allocate source-ordered mixed flow while preserving readable text first."""
	_, items, images, tables = body_parts(cell.blocks)
	if not items or not images or tables:
		return None
	left, top, width, height = rectangle
	blocks = tuple(block for block in cell.blocks if isinstance(block,
		(slide_lib.native_model.Paragraph, slide_lib.native_model.ListBlock, slide_lib.native_model.Image)))
	image_heights = {id(block): image_flow_height(deck, block, width) for block in blocks
		if isinstance(block, slide_lib.native_model.Image)}
	gap_height = 12 * (len(blocks) - 1)
	for quarter_points in range(int(preferred_size * 4), int(MIN_READABLE_BODY_SIZE * 4) - 1, -1):
		size = quarter_points / 4
		text_heights = {id(block): estimate_items_height(slide_lib.editable_text.flow_items(block), size, width) for block in blocks
			if not isinstance(block, slide_lib.native_model.Image)}
		remaining_image_height = height - gap_height - sum(text_heights.values())
		if remaining_image_height > 0:
			full_image_height = sum(image_heights.values())
			image_scale = min(1.0, remaining_image_height / full_image_height)
			y = top
			steps: list[FlowStep] = []
			for block in blocks:
				block_height = (image_heights[id(block)] * image_scale if
					isinstance(block, slide_lib.native_model.Image) else text_heights[id(block)])
				steps.append(FlowStep(block, (left, y, width, block_height)))
				y += block_height + 12
			return CellFlowPlan(tuple(steps), size)
	offending = next(block for block in blocks if isinstance(block, slide_lib.native_model.Image))
	raise layout_error(offending.location,
		f"{context} ordered text and component-image flow cannot fit within the supported readable minimum of "
		f"{MIN_READABLE_BODY_SIZE:g} CSS px")


#============================================
def render_cell_flow(slide: object, deck: slide_lib.native_model.Deck, plan: CellFlowPlan) -> None:
	"""Write the exact preflight-approved source order as native shapes."""
	for step in plan.steps:
		left, top, width, height = step.rectangle
		if isinstance(step.block, slide_lib.native_model.Image):
			picture = add_picture(slide, resolve_image_path(deck, step.block), step.block, left, top, width, height)
			slide_lib.pptx_animation.register_reveal(slide, picture, step.block.reveal)
		else:
			frame = add_textbox(slide, left, top, width, height)
			write_items(frame, slide_lib.editable_text.flow_items(step.block), plan.text_size)
			slide_lib.pptx_animation.register_text_reveal(slide, frame, step.block)


#============================================
def title_height(title: slide_lib.native_model.Heading, size: float,
		width: float, vertical: bool = False) -> float:
	"""Measure the layout's authored title at its fixed native size."""
	if vertical:
		line_count = max(len(inline_text(title.inlines).replace(" ", "")), 1)
	else:
		line_count = wrapped_line_count(title.inlines, size, width)
	return line_count * size * 1.12


#============================================
def title_and_content_top(slide: object, source: slide_lib.native_model.Slide,
		title: slide_lib.native_model.Heading, vertical_title: bool = False) -> tuple[float, float, float]:
	"""Write a title and return the remaining content rectangle origin and size."""
	if vertical_title:
		frame = add_textbox(slide, LEFT, 60, 94, 666, vertical_text=True)
		paragraph = frame.paragraphs[0]
		size = 38.0
		add_inline_runs(paragraph, title.inlines, size)
		for run in paragraph.runs:
			run.font.bold = True
		slide_lib.pptx_animation.register_text_reveal(slide, frame, title)
		return 178, 82, RIGHT - 178
	size = 48.0
	height = title_height(title, size, RIGHT - LEFT)
	frame = add_textbox(slide, LEFT, TITLE_TOP, RIGHT - LEFT, height)
	paragraph = frame.paragraphs[0]
	add_inline_runs(paragraph, title.inlines, size)
	for run in paragraph.runs:
		run.font.bold = True
	slide_lib.pptx_animation.register_text_reveal(slide, frame, title)
	return LEFT, TITLE_TOP + height + 24, RIGHT - LEFT


#============================================
def cell_rectangles(spec: LayoutSpec, content: tuple[float, float, float, float]) -> list[tuple[float, float, float, float]]:
	"""Return the named-cell geometry derived from one common content rectangle."""
	left, top, width, height = content
	if spec.name in ("one-panel", "vertical-panel", "vertical-text-panel"):
		return [content]
	if spec.name in ("two-panels", "vertical-title-two-panels"):
		return grid_rectangles(left, top, width, height, 2, 1)
	if spec.name == "one-plus-two-panels":
		cell_width = (width - CELL_GUTTER) / 2
		half_height = (height - GRID_GUTTER) / 2
		return [(left, top, cell_width, height),
			(left + cell_width + CELL_GUTTER, top, cell_width, half_height),
			(left + cell_width + CELL_GUTTER, top + half_height + GRID_GUTTER, cell_width, half_height)]
	if spec.name == "two-plus-one-panels":
		cell_width = (width - CELL_GUTTER) / 2
		half_height = (height - GRID_GUTTER) / 2
		return [(left, top, cell_width, half_height),
			(left, top + half_height + GRID_GUTTER, cell_width, half_height),
			(left + cell_width + CELL_GUTTER, top, cell_width, height)]
	if spec.name == "stacked-panels":
		return grid_rectangles(left, top, width, height, 1, 2)
	if spec.name == "two-over-one-panels":
		half_height = (height - GRID_GUTTER) / 2
		rectangles = grid_rectangles(left, top, width, half_height, 2, 1)
		rectangles.append((left, top + half_height + GRID_GUTTER, width, half_height))
		return rectangles
	if spec.name == "four-panels":
		return grid_rectangles(left, top, width, height, 2, 2)
	if spec.name == "six-panels":
		return grid_rectangles(left, top, width, height, 3, 2)
	if spec.name == "two-panels-vertical-clipart":
		right_width = (width - CELL_GUTTER) * .34
		left_width = width - CELL_GUTTER - right_width
		half_height = (height - GRID_GUTTER) / 2
		return [(left, top, left_width, half_height),
			(left, top + half_height + GRID_GUTTER, left_width, half_height),
			(left + left_width + CELL_GUTTER, top, right_width, height)]
	raise LayoutError(f"{spec.name} does not define native cell geometry")


#============================================
def normalized_topology_slots(spec: LayoutSpec) -> tuple[tuple[float, float, float, float, float, float], ...]:
	"""Return normalized slot spans and centers from canonical content geometry."""
	content = (LEFT, 160.0, RIGHT - LEFT, CONTENT_BOTTOM - 160.0)
	left, top, width, height = content
	return tuple(((x - left) / width, (y - top) / height, w / width, h / height,
		(x - left + w / 2) / width, (y - top + h / 2) / height)
		for x, y, w, h in cell_rectangles(spec, content))


#============================================
def plan_cell_body(cell: slide_lib.native_model.Cell,
		rectangle: tuple[float, float, float, float]) -> CellBodyPlan:
	"""Choose a readable local-H2 size and reserve its matching body rectangle."""
	left, top, width, height = rectangle
	headings, _, _, _ = body_parts(cell.blocks)
	if not headings:
		return CellBodyPlan(rectangle, None)
	for quarter_points in range(28 * 4, int(MIN_READABLE_BODY_SIZE * 4) - 1, -1):
		size = quarter_points / 4
		heading_height = wrapped_line_count(headings[0].inlines, size, width) * size * 1.2
		if heading_height + 10 <= height:
			return CellBodyPlan((left, top + heading_height + 10, width, height - heading_height - 10), size)
	raise layout_error(headings[0].location,
		f"local H2 cannot fit within the supported readable minimum of {MIN_READABLE_BODY_SIZE:g} CSS px")


#============================================
def content_cell_rectangles(source: slide_lib.native_model.Slide, spec: LayoutSpec,
		content: tuple[float, float, float, float]) -> list[tuple[float, float, float, float]]:
	"""Allocate the existing footer layout from its readable lower-cell need."""
	if spec.name != "two-over-one-panels":
		return cell_rectangles(spec, content)
	left, top, width, height = content
	bottom = next(cell for cell in source.cells if cell.name == "bottom")
	_headings, items, _images, tables = body_parts(bottom.blocks)
	need = estimate_items_height(items, MIN_READABLE_BODY_SIZE, width) if items else 0.0
	if tables:
		need = max(need, estimate_table_height(tables[0], MIN_READABLE_BODY_SIZE, width))
	bottom_height = max((height - GRID_GUTTER) / 2, need)
	top_height = height - GRID_GUTTER - bottom_height
	top_rectangles = grid_rectangles(left, top, width, top_height, 2, 1)
	return [*top_rectangles, (left, top + top_height + GRID_GUTTER, width, bottom_height)]
def readability_failure(source: slide_lib.native_model.Slide, spec: LayoutSpec,
		content: tuple[float, float, float, float]) -> tuple[str, slide_lib.native_model.SourceLocation] | None:
	"""Return the first region that cannot retain the minimum readable body type."""
	for slot_name, rectangle in zip(spec.slot_names, content_cell_rectangles(source, spec, content)):
		cell = next(cell for cell in source.cells if cell.name == slot_name)
		_, items, images, _ = body_parts(cell.blocks)
		body_plan = plan_cell_body(cell, rectangle)
		if not items or images:
			continue
		_, _, width, _ = rectangle
		_, _, _, body_height = body_plan.body_rectangle
		if estimate_items_height(items, MIN_READABLE_BODY_SIZE, width) > body_height:
			body_block = next(block for block in cell.blocks if not isinstance(block,
				slide_lib.native_model.Heading))
			return slot_name, body_block.location
	return None


#============================================
def plan_title_body(source: slide_lib.native_model.Slide, title: slide_lib.native_model.Heading,
		spec: LayoutSpec) -> TitleBodyPlan:
	"""Allocate title and body space before native title or body shapes are written."""
	if spec.vertical_title:
		size = 38.0
		content = (178.0, 82.0, RIGHT - 178, CONTENT_BOTTOM - 82)
		failure = readability_failure(source, spec, content)
		if failure is not None:
			slot_name, location = failure
			raise layout_error(location,
				f"{spec.name} {slot_name} content cannot fit within the supported readable minimum of "
				f"{MIN_READABLE_BODY_SIZE:g} CSS px")
		return TitleBodyPlan((LEFT, 60.0, 94.0, 666.0), size, content, True)
	size = 48.0
	title_height_value = title_height(title, size, RIGHT - LEFT)
	content_top = TITLE_TOP + title_height_value + 24
	content = (LEFT, content_top, RIGHT - LEFT, CONTENT_BOTTOM - content_top)
	failure = readability_failure(source, spec, content)
	if failure is None:
		return TitleBodyPlan((LEFT, TITLE_TOP, RIGHT - LEFT, title_height_value), size, content, False)
	maximum_content = (LEFT, TITLE_TOP + 24, RIGHT - LEFT, CONTENT_BOTTOM - TITLE_TOP - 24)
	if title_height_value <= 170 or readability_failure(source, spec, maximum_content) is not None:
		slot_name, location = failure
		raise layout_error(location,
			f"{spec.name} {slot_name} content cannot fit within the supported readable minimum of "
			f"{MIN_READABLE_BODY_SIZE:g} CSS px")
	slot_name, _ = failure
	raise layout_error(title.location,
		f"{spec.name} H1 allocation leaves {slot_name} without its readable body region")


#============================================
def plan_content(source: slide_lib.native_model.Slide, spec: LayoutSpec) -> TitleBodyPlan:
	"""Allocate an optional H1 or the titleless full-width body region without shapes."""
	headings, _, _, _ = body_parts(source.blocks)
	if headings:
		return plan_title_body(source, headings[0], spec)
	content = (LEFT, 82.0, RIGHT - LEFT, CONTENT_BOTTOM - 82.0)
	failure = readability_failure(source, spec, content)
	if failure is not None:
		slot_name, location = failure
		raise layout_error(location,
			f"{spec.name} {slot_name} content cannot fit within the supported readable minimum of "
			f"{MIN_READABLE_BODY_SIZE:g} CSS px")
	return TitleBodyPlan(None, 0.0, content, False)


#============================================
def write_planned_title(slide: object, title: slide_lib.native_model.Heading,
		plan: TitleBodyPlan) -> None:
	"""Write one preflight-approved editable title frame."""
	if plan.title_rectangle is None:
		return
	left, top, width, height = plan.title_rectangle
	frame = add_textbox(slide, left, top, width, height, vertical_text=plan.vertical_title)
	paragraph = frame.paragraphs[0]
	add_inline_runs(paragraph, title.inlines, plan.title_size)
	for run in paragraph.runs:
		run.font.bold = True
	slide_lib.pptx_animation.register_text_reveal(slide, frame, title)


#============================================
def layout_error(source: slide_lib.native_model.SourceLocation | slide_lib.native_model.Slide,
		message: str) -> ValueError:
	"""Attach a layout-capacity failure to its canonical source location."""
	location = source.location if isinstance(source, slide_lib.native_model.Slide) else source
	return ValueError(f"{location.path}:{location.line}: {message}")


#============================================
def validate_layout_source(source: slide_lib.native_model.Slide) -> LayoutSpec:
	"""Select the live layout then validate its presentation-source contract."""
	spec = LAYOUTS[source.layout_class]
	slide_lib.layout_validation.validate_layout_source(source, spec)
	return spec


def render_cell(slide: object, deck: slide_lib.native_model.Deck, cell: slide_lib.native_model.Cell, rectangle: tuple[float, float, float, float],
		vertical: bool = False, preferred_body_size: float = 22, context: str = "cell") -> None:
	"""Render one independently editable cell in its assigned rectangle."""
	left, top, width, height = rectangle
	headings, items, images, tables = body_parts(cell.blocks)
	body_plan = plan_cell_body(cell, rectangle)
	body_left, body_top, body_width, body_height = body_plan.body_rectangle
	if headings:
		heading = headings[0]
		heading_size = body_plan.heading_size
		if heading_size is None:
			raise LayoutError("local H2 requires a readable cell-body plan")
		heading_height = wrapped_line_count(heading.inlines, heading_size, width) * heading_size * 1.2
		head_frame = add_textbox(slide, left, top, width, heading_height, vertical_text=vertical)
		heading_paragraph = head_frame.paragraphs[0]
		add_inline_runs(heading_paragraph, heading.inlines, heading_size)
		for run in heading_paragraph.runs:
			run.font.bold = True
		slide_lib.pptx_animation.register_text_reveal(slide, head_frame, heading)
	flow_plan = plan_cell_flow(deck, cell, body_plan.body_rectangle, preferred_body_size, context)
	if flow_plan is not None:
		render_cell_flow(slide, deck, flow_plan)
		return
	if tables:
		render_table(slide, tables[0], (body_left, body_top, body_width, body_height), context)
	elif images:
		gap = 12
		image_width = (body_width - gap * (len(images) - 1)) / len(images)
		for index, image in enumerate(images):
			picture = add_picture(slide, resolve_image_path(deck, image), image,
				body_left + index * (image_width + gap), body_top, image_width, body_height)
			slide_lib.pptx_animation.register_reveal(slide, picture, image.reveal)
	elif items:
		text_blocks = tuple(block for block in cell.blocks if isinstance(block,
			(slide_lib.native_model.Paragraph, slide_lib.native_model.ListBlock)))
		item_sets = [slide_lib.editable_text.flow_items(block) for block in text_blocks]
		size = fit_body_size(item_sets if any(slide_lib.editable_text.has_reveal(block) for block in text_blocks) else [items],
			body_width, body_height, preferred_body_size, text_blocks[0].location, context)
		if any(slide_lib.editable_text.has_reveal(block) for block in text_blocks):
			y = body_top
			for block, block_items in zip(text_blocks, item_sets):
				block_height = estimate_items_height(block_items, size, body_width)
				frame = add_textbox(slide, body_left, y, body_width, block_height, vertical_text=vertical)
				write_items(frame, block_items, size)
				slide_lib.pptx_animation.register_text_reveal(slide, frame, block)
				y += block_height
		else:
			frame = add_textbox(slide, body_left, body_top, body_width, body_height, vertical_text=vertical)
			write_items(frame, items, size)


#============================================
def grid_rectangles(left: float, top: float, width: float, height: float, columns: int,
		rows: int) -> list[tuple[float, float, float, float]]:
	"""Return reading-order grid cells from shared geometry constants."""
	cell_width = (width - CELL_GUTTER * (columns - 1)) / columns
	cell_height = (height - GRID_GUTTER * (rows - 1)) / rows
	return [(left + column * (cell_width + CELL_GUTTER), top + row * (cell_height + GRID_GUTTER),
		cell_width, cell_height) for row in range(rows) for column in range(columns)]


#============================================
def build_blank(slide: object, source: object, deck: object, spec: LayoutSpec) -> None:
	"""Render an empty native canvas."""


#============================================
def build_title_slide(slide: object, source: slide_lib.native_model.Slide, deck: slide_lib.native_model.Deck, spec: LayoutSpec) -> None:
	"""Render centered title and optional subtitle."""
	headings, _, _, _ = body_parts(source.blocks)
	title_size_value = 60.0
	if any(heading.reveal is not None for heading in headings):
		title_heights = [wrapped_line_count(heading.inlines, title_size_value if index == 0 else 31, 1060) *
			(title_size_value if index == 0 else 31) * 1.12 for index, heading in enumerate(headings)]
		gutter = 18.6666666667
		top = 180 + (390 - sum(title_heights) - gutter * (len(headings) - 1)) / 2
		for index, (heading, height) in enumerate(zip(headings, title_heights)):
			frame = add_textbox(slide, 110, top, 1060, height, MSO_ANCHOR.MIDDLE)
			paragraph = frame.paragraphs[0]
			paragraph.alignment = PP_ALIGN.CENTER
			add_inline_runs(paragraph, heading.inlines, title_size_value if index == 0 else 31,
				FOREGROUND if index == 0 else MUTED)
			for run in paragraph.runs:
				run.font.bold = index == 0
			slide_lib.pptx_animation.register_text_reveal(slide, frame, heading)
			top += height + gutter
		return
	frame = add_textbox(slide, 110, 180, 1060, 390, MSO_ANCHOR.MIDDLE)
	for index, heading in enumerate(headings):
		paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
		paragraph.alignment = PP_ALIGN.CENTER
		paragraph.space_after = Pt(14)
		add_inline_runs(paragraph, heading.inlines, title_size_value if index == 0 else 31,
			FOREGROUND if index == 0 else MUTED)
		for run in paragraph.runs:
			run.font.bold = index == 0
		slide_lib.pptx_animation.register_text_reveal(slide, frame, heading)
#============================================
def build_title_only(slide: object, source: slide_lib.native_model.Slide, deck: slide_lib.native_model.Deck, spec: LayoutSpec) -> None:
	"""Render only the native title region."""
	title = body_parts(source.blocks)[0][0]
	title_and_content_top(slide, source, title)
#============================================
def build_centered_text(slide: object, source: slide_lib.native_model.Slide, deck: slide_lib.native_model.Deck, spec: LayoutSpec) -> None:
	"""Render centered editable title and optional subtitle."""
	build_title_slide(slide, source, deck, spec)
#============================================
def render_root_body(slide: object, source: slide_lib.native_model.Slide, deck: slide_lib.native_model.Deck,
		spec: LayoutSpec) -> None:
	"""Render an optional title and delegate its root body to the cell renderer."""
	headings, _, _, _ = body_parts(source.blocks)
	body = next(cell for cell in source.cells if cell.name == "body")
	plan = plan_content(source, spec)
	if headings:
		write_planned_title(slide, headings[0], plan)
	render_cell(slide, deck, body, plan.content_rectangle, bool(spec.vertical_cells), 26, spec.name)
#============================================
def build_title_content(slide: object, source: slide_lib.native_model.Slide,
		deck: slide_lib.native_model.Deck, spec: LayoutSpec) -> None:
	"""Render the ordinary title-and-content native layout."""
	render_root_body(slide, source, deck, spec)
#============================================
def build_vertical_title_vertical_text(slide: object, source: slide_lib.native_model.Slide,
		deck: slide_lib.native_model.Deck, spec: LayoutSpec) -> None:
	"""Render one vertical body pane beside its vertical title strip."""
	render_root_body(slide, source, deck, spec)
#============================================
def build_title_vertical_text(slide: object, source: slide_lib.native_model.Slide,
		deck: slide_lib.native_model.Deck, spec: LayoutSpec) -> None:
	"""Render one vertical body pane below its horizontal title."""
	render_root_body(slide, source, deck, spec)
#============================================
def render_cells(slide: object, source: slide_lib.native_model.Slide,
		deck: slide_lib.native_model.Deck, spec: LayoutSpec,
		rectangles: list[tuple[float, float, float, float]]) -> None:
	"""Render native cell rectangles by their declared layout slot."""
	for index, (slot_name, rectangle) in enumerate(zip(spec.slot_names, rectangles)):
		cell = next(cell for cell in source.cells if cell.name == slot_name)
		render_cell(slide, deck, cell, rectangle, index in spec.vertical_cells)
#============================================
def content_rectangle(slide: object, source: slide_lib.native_model.Slide,
		spec: LayoutSpec) -> tuple[float, float, float, float]:
	"""Write an optional title then return the preflight-approved body region."""
	headings, _, _, _ = body_parts(source.blocks)
	plan = plan_content(source, spec)
	if headings:
		write_planned_title(slide, headings[0], plan)
	return plan.content_rectangle
#============================================
def build_standard_cells(slide: object, source: slide_lib.native_model.Slide,
		deck: slide_lib.native_model.Deck, spec: LayoutSpec) -> None:
	"""Render ordinary named cells from their layout-owned content allocation."""
	content = content_rectangle(slide, source, spec)
	render_cells(slide, source, deck, spec, content_cell_rectangles(source, spec, content))


def build_title_two_content(slide: object, source: slide_lib.native_model.Slide, deck: slide_lib.native_model.Deck, spec: LayoutSpec) -> None:
	"""Render two peer cells."""
	build_standard_cells(slide, source, deck, spec)
def build_title_content_and_two_content(slide: object, source: slide_lib.native_model.Slide, deck: slide_lib.native_model.Deck, spec: LayoutSpec) -> None:
	"""Render one cell beside two peers."""
	build_standard_cells(slide, source, deck, spec)
def build_title_two_content_and_content(slide: object, source: slide_lib.native_model.Slide, deck: slide_lib.native_model.Deck, spec: LayoutSpec) -> None:
	"""Render two peers beside one cell."""
	build_standard_cells(slide, source, deck, spec)
def build_title_content_over_content(slide: object, source: slide_lib.native_model.Slide, deck: slide_lib.native_model.Deck, spec: LayoutSpec) -> None:
	"""Render stacked full-width cells."""
	build_standard_cells(slide, source, deck, spec)
def build_title_two_content_over_content(slide: object, source: slide_lib.native_model.Slide, deck: slide_lib.native_model.Deck, spec: LayoutSpec) -> None:
	"""Render upper peers and a lower footer."""
	build_standard_cells(slide, source, deck, spec)
def build_title_four_content(slide: object, source: slide_lib.native_model.Slide, deck: slide_lib.native_model.Deck, spec: LayoutSpec) -> None:
	"""Render a two-by-two grid."""
	build_standard_cells(slide, source, deck, spec)
def build_title_six_content(slide: object, source: slide_lib.native_model.Slide, deck: slide_lib.native_model.Deck, spec: LayoutSpec) -> None:
	"""Render a three-by-two grid."""
	build_standard_cells(slide, source, deck, spec)
#============================================
def build_vertical_title_text_chart(slide: object, source: slide_lib.native_model.Slide,
		deck: slide_lib.native_model.Deck, spec: LayoutSpec) -> None:
	"""Render two peer cells beside the fixed-width vertical title strip."""
	content = content_rectangle(slide, source, spec)
	render_cells(slide, source, deck, spec, cell_rectangles(spec, content))
#============================================
def build_title_two_vertical_text_clipart(slide: object, source: slide_lib.native_model.Slide,
		deck: slide_lib.native_model.Deck, spec: LayoutSpec) -> None:
	"""Render two stacked cells beside one vertical native pane."""
	content = content_rectangle(slide, source, spec)
	render_cells(slide, source, deck, spec, cell_rectangles(spec, content))
#============================================
def build_multiple_choice(slide: object, source: slide_lib.native_model.Slide,
		deck: slide_lib.native_model.Deck, spec: LayoutSpec) -> None:
	"""Render an initially visible question and one independent answer popup."""
	question = next(cell for cell in source.cells if cell.name == "question")
	answer = next(cell for cell in source.cells if cell.name == "answer")
	render_cell(slide, deck, question, MULTIPLE_CHOICE_QUESTION_RECTANGLE)
	left, top, width, height = MULTIPLE_CHOICE_ANSWER_RECTANGLE
	popup = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px(left), px(top), px(width), px(height))
	popup.fill.solid()
	popup.fill.fore_color.rgb = ACCENT
	popup.line.fill.background()
	frame = popup.text_frame
	frame.clear()
	frame.margin_left = frame.margin_right = 18
	frame.margin_top = frame.margin_bottom = 10
	frame.vertical_anchor = MSO_ANCHOR.MIDDLE
	frame.word_wrap = True
	body_properties = frame._txBody.bodyPr
	for child in list(body_properties):
		if child.tag.endswith(("noAutofit", "normAutofit", "spAutoFit")):
			body_properties.remove(child)
	autofit = OxmlElement("a:normAutofit")
	autofit.set("fontScale", "100000")
	autofit.set("lnSpcReduction", "0")
	body_properties.append(autofit)
	answer_items = [(block.inlines, 0, False, True, 1) for block in answer.blocks]
	size = fit_body_size([answer_items], width - 36, height - 20,
		26, answer.blocks[0].location, "multiple-choice answer")
	write_items(frame, answer_items, size)
	for paragraph in frame.paragraphs:
		for run in paragraph.runs:
			run.font.color.rgb = WHITE
			run.font.bold = True
	slide_lib.pptx_animation.register_text_reveal(slide, frame, answer.blocks[0])
#============================================
def build_gallery(slide: object, source: slide_lib.native_model.Slide, deck: slide_lib.native_model.Deck, spec: LayoutSpec) -> None:
	"""Render a row of independently contained component images."""
	headings, _, _, _ = body_parts(source.blocks)
	gallery = next(cell for cell in source.cells if cell.name == "gallery")
	_, _, images, _ = body_parts(gallery.blocks)
	if headings:
		_, top, _ = title_and_content_top(slide, source, headings[0])
	else:
		top = 82
	width = (RIGHT - LEFT - 18 * (len(images) - 1)) / len(images)
	for index, image in enumerate(images):
		picture = add_picture(slide, resolve_image_path(deck, image), image, LEFT + index * (width + 18),
			top, width, CONTENT_BOTTOM - top)
		slide_lib.pptx_animation.register_reveal(slide, picture, image.reveal)
#============================================
def preflight_layout_capacity(source: slide_lib.native_model.Slide, spec: LayoutSpec,
		deck: slide_lib.native_model.Deck) -> None:
	"""Prove title/body capacity before the slide receives any native shapes."""
	if spec.name == "multiple-choice":
		question = next(cell for cell in source.cells if cell.name == "question")
		answer = next(cell for cell in source.cells if cell.name == "answer")
		flow = plan_cell_flow(deck, question, MULTIPLE_CHOICE_QUESTION_RECTANGLE, 22,
			"multiple-choice question")
		if flow is None:
			_, items, _, _ = body_parts(question.blocks)
			if items:
				fit_body_size([items], MULTIPLE_CHOICE_QUESTION_RECTANGLE[2],
					MULTIPLE_CHOICE_QUESTION_RECTANGLE[3], 22, question.blocks[0].location,
					"multiple-choice question")
		answer_items = [(block.inlines, 0, False, True, 1) for block in answer.blocks]
		fit_body_size([answer_items], MULTIPLE_CHOICE_ANSWER_RECTANGLE[2] - 36,
			MULTIPLE_CHOICE_ANSWER_RECTANGLE[3] - 20, 26, answer.blocks[0].location,
			"multiple-choice answer")
		return
	if spec.slot_names and spec.name not in ("gallery", "multiple-choice"):
		plan = plan_content(source, spec)
		for slot_name, rectangle in zip(spec.slot_names, content_cell_rectangles(source, spec, plan.content_rectangle)):
			cell = next(cell for cell in source.cells if cell.name == slot_name)
			_, _, _, tables = body_parts(cell.blocks)
			body_rectangle = plan_cell_body(cell, rectangle).body_rectangle
			plan_cell_flow(deck, cell, body_rectangle,
				26 if slot_name == "body" else 22, f"{spec.name} {slot_name}")
			if tables:
				_, _, width, height = body_rectangle
				fit_table_size(tables[0], width, height, f"{spec.name} {slot_name}")
LAYOUTS: dict[str, LayoutSpec] = {
	"blank": LayoutSpec("blank", 0, False, False, frozenset(), build_blank),
	"title-only": LayoutSpec("title-only", 0, False, False, frozenset(), build_title_only,
		allows_title=True),
	"title-slide": LayoutSpec("title-slide", 0, False, False, frozenset(), build_title_slide,
		allows_title=True, allows_subtitle=True),
	"one-panel": LayoutSpec("one-panel", 1, True, False, frozenset(), build_title_content,
		slot_names=("body",), allows_title=True, topology_matchable=True),
	"centered-text": LayoutSpec("centered-text", 0, False, False, frozenset(), build_centered_text,
		allows_title=True, allows_subtitle=True),
	"two-panels": LayoutSpec("two-panels", 2, False, False, frozenset(), build_title_two_content,
		slot_names=("left", "right"), allows_title=True, topology_matchable=True),
	"one-plus-two-panels": LayoutSpec("one-plus-two-panels", 3, False, False, frozenset(), build_title_content_and_two_content,
		slot_names=("left", "top-right", "bottom-right"), allows_title=True, topology_matchable=True),
	"two-plus-one-panels": LayoutSpec("two-plus-one-panels", 3, False, False, frozenset(), build_title_two_content_and_content,
		slot_names=("top-left", "bottom-left", "right"), allows_title=True, topology_matchable=True),
	"stacked-panels": LayoutSpec("stacked-panels", 2, False, False, frozenset(), build_title_content_over_content,
		slot_names=("top", "bottom"), allows_title=True, topology_matchable=True),
	"two-over-one-panels": LayoutSpec("two-over-one-panels", 3, False, False, frozenset(), build_title_two_content_over_content,
		slot_names=("top-left", "top-right", "bottom"), allows_title=True, topology_matchable=True),
	"four-panels": LayoutSpec("four-panels", 4, False, False, frozenset(), build_title_four_content,
		slot_names=("top-left", "top-right", "bottom-left", "bottom-right"), allows_title=True, topology_matchable=True),
	"six-panels": LayoutSpec("six-panels", 6, False, False, frozenset(), build_title_six_content,
		slot_names=("top-left", "top-center", "top-right", "bottom-left", "bottom-center", "bottom-right"), allows_title=True, topology_matchable=True),
	"vertical-panel": LayoutSpec("vertical-panel", 1, True, True, frozenset({0}), build_vertical_title_vertical_text,
		slot_names=("body",), allows_title=True),
	"vertical-title-two-panels": LayoutSpec("vertical-title-two-panels", 2, False, True, frozenset(), build_vertical_title_text_chart,
		slot_names=("text", "chart"), allows_title=True),
	"vertical-text-panel": LayoutSpec("vertical-text-panel", 1, True, False, frozenset({0}), build_title_vertical_text,
		slot_names=("body",), allows_title=True),
	"two-panels-vertical-clipart": LayoutSpec("two-panels-vertical-clipart", 3, False, False, frozenset({2}), build_title_two_vertical_text_clipart,
		slot_names=("top-left", "bottom-left", "right-clipart"), allows_title=True),
	"multiple-choice": LayoutSpec("multiple-choice", 2, False, False, frozenset(), build_multiple_choice,
		slot_names=("question", "answer")),
	"gallery": LayoutSpec("gallery", 1, False, False, frozenset(), build_gallery,
		slot_names=("gallery",), allows_title=True),
}
#============================================
def render_layout(slide: object, source: slide_lib.native_model.Slide, deck: slide_lib.native_model.Deck,
		writer: slide_lib.pptx_animation.PptxAnimationWriter | None = None) -> None:
	"""Validate and render exactly one native layout on a blank slide."""
	spec = validate_layout_source(source)
	preflight_layout_capacity(source, spec, deck)
	if writer is not None:
		setattr(slide, "_slide_animation_writer", writer)
	add_background(slide)
	spec.builder(slide, source, deck, spec)
