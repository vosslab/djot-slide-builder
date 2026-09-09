"""Small invariant coverage for the one-to-one physical model."""

import pathlib

import pytest

import slide_lib.layout_model as model
import slide_lib.layout_content as content
import slide_lib.layout_primitives as primitives
import slide_lib.native_model as native


def source() -> native.SourceLocation:
	return native.SourceLocation(pathlib.Path("source.djot"), 1)


def layout_slide(reveal_order: int = 0, slot_id: str = "body") -> model.LayoutSlide:
	"""Build the smallest native-placeholder slide for adapter-boundary checks."""
	rectangle = primitives.LogicalRectangle(0.0, 0.0, 300.0, 200.0)
	frame_text = primitives.FrameTextProperties(primitives.Insets(0.0, 0.0, 0.0, 0.0),
		primitives.VerticalAlignment.TOP, primitives.TextWrap.WRAP, primitives.OverflowPolicy.SHRINK)
	slot = model.LayoutSlot(slot_id, primitives.PlaceholderKind.OUTLINE,
		primitives.PresentationRole.OUTLINE, rectangle, 0,
		primitives.PlaceholderProperties(primitives.StyleRole.OUTLINE, frame_text))
	expected_slot = model.LayoutSlot("body", primitives.PlaceholderKind.OUTLINE,
		primitives.PresentationRole.OUTLINE, rectangle, 0,
		primitives.PlaceholderProperties(primitives.StyleRole.OUTLINE, frame_text))
	topology = primitives.PlaceholderTopology("one-panel", (expected_slot.topology_member(),))
	content_item = content.ShapeContent(primitives.ShapeKind.RECTANGLE,
		content.ShapeStyle(primitives.StyleRole.ACCENT, primitives.StyleRole.ACCENT, 1.0,
			primitives.LinePattern.SOLID), primitives.ObjectAccessibility(decorative=True))
	reveal = native.Reveal(native.RevealEffect.APPEAR, native.RevealSequence.OBJECT)
	object_item = model.LayoutObject("object", primitives.PresentationRole.OUTLINE,
		primitives.StyleRole.OUTLINE, rectangle, primitives.ObjectLayer.CONTENT, 0, 0,
		content_item, None, "body", "body", primitives.PlaceholderKind.OUTLINE, source(),
		(model.RevealTarget("reveal", "object", reveal, reveal_order),))
	return model.LayoutSlide(model.SlideIdentity("slide-1", 0, source()),
		model.LayoutIdentity("one-panel", topology), (slot,), (object_item,), ())


def test_layout_slide_rejects_noncontiguous_reveal_activation() -> None:
	"""Native animation receives a contiguous click sequence rather than a corrupt gap."""
	with pytest.raises(ValueError, match="contiguous source-ordered activation"):
		layout_slide(reveal_order=1)


def test_layout_slide_rejects_slots_outside_its_native_topology() -> None:
	"""Native placeholder membership stays aligned with the declared layout identity."""
	with pytest.raises(ValueError, match="match the declared presentation layout topology"):
		layout_slide(slot_id="other")


def test_picture_placement_rejects_crop_or_an_outside_frame() -> None:
	"""ODP image frames preserve a contained source inside their allocation."""
	allocation = primitives.LogicalRectangle(0.0, 0.0, 300.0, 200.0)
	with pytest.raises(ValueError, match="cannot crop"):
		content.PicturePlacement(allocation, allocation, primitives.PictureFit.CONTAIN,
			primitives.CropInsets(0.1, 0.0, 0.0, 0.0))
	with pytest.raises(ValueError, match="inside its allocation"):
		content.PicturePlacement(allocation, primitives.LogicalRectangle(250.0, 0.0, 100.0, 100.0),
			primitives.PictureFit.CONTAIN, primitives.CropInsets(0.0, 0.0, 0.0, 0.0))
