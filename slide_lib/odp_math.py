"""Export whole equations, list markers, and intact native paragraphs."""

import dataclasses

import slide_lib.layout_content
import slide_lib.layout_model
import slide_lib.layout_primitives


#============================================
def positioned_runs(content: slide_lib.layout_content.ObjectContent
		) -> tuple[slide_lib.layout_content.PositionedRun, ...]:
	"""Find the already-positioned text on a text box, table, or answer shape."""
	if isinstance(content, (slide_lib.layout_content.TextContent, slide_lib.layout_content.TableContent)):
		return content.positioned_runs
	if isinstance(content, slide_lib.layout_content.ShapeContent) and content.text is not None:
		return content.text.positioned_runs
	return ()


#============================================
def background_object(item: slide_lib.layout_model.LayoutObject
		) -> slide_lib.layout_model.LayoutObject | None:
	"""Retain a table's cell backgrounds or an answer's shape behind equation blocks."""
	if isinstance(item.content, slide_lib.layout_content.TableContent):
		return dataclasses.replace(item, object_id=item.object_id + "-background",
			content=dataclasses.replace(item.content, positioned_runs=()), reveal_targets=())
	if isinstance(item.content, slide_lib.layout_content.ShapeContent):
		return dataclasses.replace(item, object_id=item.object_id + "-background",
			content=dataclasses.replace(item.content, text=None), frame_text=None, reveal_targets=())
	return None


#============================================
def block_object(item: slide_lib.layout_model.LayoutObject,
		placed: slide_lib.layout_content.PositionedRun, index: int) -> slide_lib.layout_model.LayoutObject:
	"""Translate a whole equation or native paragraph without recalculating layout."""
	rectangle = dataclasses.replace(placed.rectangle,
		x=item.rectangle.x + placed.rectangle.x, y=item.rectangle.y + placed.rectangle.y)
	run = placed.run
	frame = None
	if isinstance(run, slide_lib.layout_content.MathRun):
		if placed.image_path is None:
			raise ValueError("a positioned equation requires its rendered SVG")
		content = slide_lib.layout_content.PictureContent(placed.image_path,
			slide_lib.layout_content.PicturePlacement(rectangle, rectangle,
				slide_lib.layout_primitives.PictureFit.CONTAIN,
				slide_lib.layout_primitives.CropInsets(0, 0, 0, 0)),
			slide_lib.layout_primitives.ObjectAccessibility("Equation", run.text),
			run.style.link_url)
		role = slide_lib.layout_primitives.PresentationRole.COMPONENT
	else:
		content = slide_lib.layout_content.TextContent((run,))
		frame = slide_lib.layout_primitives.FrameTextProperties(
			slide_lib.layout_primitives.Insets(0, 0, 0, 0),
			slide_lib.layout_primitives.VerticalAlignment.TOP,
			slide_lib.layout_primitives.TextWrap.WRAP,
			slide_lib.layout_primitives.OverflowPolicy.CLIP)
		role = slide_lib.layout_primitives.PresentationRole.OUTLINE
	return slide_lib.layout_model.LayoutObject(f"{item.object_id}-math-{index}", role,
		item.style_role, rectangle, item.layer, item.z_index, item.reading_order,
		content, frame, source=item.source)
