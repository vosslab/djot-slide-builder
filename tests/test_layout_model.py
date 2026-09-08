"""Behavior tests for format-neutral presentation layout records."""

import dataclasses
import pathlib

import pytest

import slide_lib.layout_content as content
import slide_lib.layout_model as model
import slide_lib.layout_primitives as primitives
import slide_lib.native_model


def source() -> slide_lib.native_model.SourceLocation:
	return slide_lib.native_model.SourceLocation(pathlib.Path("inline.djot"), 1)


def frame_text() -> primitives.FrameTextProperties:
	return primitives.FrameTextProperties(
		primitives.Insets(0.0, 0.0, 0.0, 0.0), primitives.VerticalAlignment.TOP,
		primitives.TextWrap.WRAP, primitives.TextDirection.HORIZONTAL, primitives.OverflowPolicy.SHRINK,
	)


def typography() -> primitives.Typography:
	return primitives.Typography(primitives.StyleRole.OUTLINE, "OpenDyslexic", 28.0, 28.0, 24.0)


def text(value: str) -> content.TextContent:
	style = content.RunStyle("OpenDyslexic", "ink")
	paragraph = content.TextParagraph((content.TextRun(value, style),), typography(),
		primitives.ParagraphProperties(primitives.HorizontalAlignment.START, 0.0, 0.0, 28.0,
			0.0, 0.0, 0.0, ()))
	return content.TextContent((paragraph,))


def outline_slot(rectangle: primitives.LogicalRectangle | None = None) -> model.LayoutSlot:
	return model.LayoutSlot("body", primitives.PlaceholderKind.OUTLINE,
		primitives.PresentationRole.OUTLINE,
		primitives.LogicalRectangle(0.0, 0.0, 500.0, 300.0) if rectangle is None else rectangle,
		0, primitives.PlaceholderProperties(primitives.StyleRole.OUTLINE, frame_text()))


def identity(slots: tuple[model.LayoutSlot, ...]) -> model.LayoutIdentity:
	topology = primitives.PlaceholderTopology("one-panel", tuple(slot.topology_member() for slot in slots))
	return model.LayoutIdentity("one-panel", topology)


def outline_object(value: str, reveal_targets: tuple[model.RevealTarget, ...] = ()) -> model.LayoutObject:
	return model.LayoutObject("body", primitives.PresentationRole.OUTLINE, primitives.StyleRole.OUTLINE,
		primitives.LogicalRectangle(20.0, 80.0, 400.0, 160.0), primitives.ObjectLayer.LAYOUT,
		0, 0, text(value), frame_text(), "body", "body", primitives.PlaceholderKind.OUTLINE,
		source(), reveal_targets)


def slide(value: str) -> model.LayoutSlide:
	slot = outline_slot()
	return model.LayoutSlide(model.SlideIdentity(f"slide-{value}", 0, source()), identity((slot,)),
		(slot,), (outline_object(value),), ())


def test_same_declared_topology_produces_one_reusable_layout_key() -> None:
	canvas = primitives.LogicalCanvas()
	assert slide("first").layout.topology.key_for_canvas(canvas) == \
		slide("second").layout.topology.key_for_canvas(canvas)


def test_role_and_rectangle_change_prevent_layout_reuse() -> None:
	base = outline_slot()
	role_changed = model.LayoutSlot("body", primitives.PlaceholderKind.OBJECT,
		primitives.PresentationRole.CONTENT, base.rectangle, 0,
		primitives.PlaceholderProperties(primitives.StyleRole.BODY))
	rectangle_changed = outline_slot(primitives.LogicalRectangle(0.0, 0.0, 501.0, 300.0))
	canvas = primitives.LogicalCanvas()
	base_key = identity((base,)).topology.key_for_canvas(canvas)
	assert base_key != identity((role_changed,)).topology.key_for_canvas(canvas)
	assert base_key != identity((rectangle_changed,)).topology.key_for_canvas(canvas)


def test_distinct_declared_topology_identity_prevents_layout_reuse() -> None:
	slot = outline_slot()
	first = identity((slot,))
	second_topology = primitives.PlaceholderTopology("one-panel-alternate",
		tuple(item.topology_member() for item in (slot,)))
	second = model.LayoutIdentity("one-panel-alternate", second_topology)
	assert first.topology.key_for_canvas(primitives.LogicalCanvas()) != \
		second.topology.key_for_canvas(primitives.LogicalCanvas())


def test_authored_text_notes_and_paint_order_do_not_change_layout_identity() -> None:
	canvas = primitives.LogicalCanvas()
	first = slide("original")
	second = model.LayoutSlide(model.SlideIdentity("replacement", 0, source()), first.layout,
		first.slots, (outline_object("replacement"),), (model.SpeakerNote("note", "private"),))
	assert first.layout.topology.key_for_canvas(canvas) == second.layout.topology.key_for_canvas(canvas)


def test_member_must_be_explicit_and_compatible_with_its_topology() -> None:
	slot = outline_slot()
	ordinary = model.LayoutObject("body", primitives.PresentationRole.CONTENT, primitives.StyleRole.BODY,
		primitives.LogicalRectangle(20.0, 80.0, 400.0, 160.0), primitives.ObjectLayer.CONTENT,
		0, 0, text("ordinary"), frame_text(), "body", "body", primitives.PlaceholderKind.OBJECT)
	with pytest.raises(ValueError, match="incompatible"):
		model.LayoutSlide(model.SlideIdentity("bad", 0, source()), identity((slot,)),
			(slot,), (ordinary,), ())


def test_allocation_slot_and_presentation_member_are_distinct_references() -> None:
	"""Ordinary placement cannot acquire layout membership from its rectangle."""
	slot = outline_slot()
	ordinary = model.LayoutObject("ordinary", primitives.PresentationRole.CONTENT,
		primitives.StyleRole.BODY, primitives.LogicalRectangle(20.0, 80.0, 400.0, 160.0),
		primitives.ObjectLayer.CONTENT, 0, 0, text("ordinary"), frame_text(), "missing")
	with pytest.raises(ValueError, match="allocation slot"):
		model.LayoutSlide(model.SlideIdentity("bad-allocation", 0, source()), identity((slot,)),
			(slot,), (ordinary,), ())


def test_deck_catalog_deduplicates_resolved_layouts() -> None:
	first = slide("first")
	second = model.LayoutSlide(model.SlideIdentity("second", 1, source()), first.layout,
		first.slots, (outline_object("second"),), ())
	deck = model.LayoutDeck(model.DeckIdentity("deck", pathlib.Path("inline.djot")),
		primitives.LogicalCanvas(), (), (first, second))
	assert len(deck.presentation_page_layouts) == 1


def test_picture_placement_is_adapter_ready_and_accessible() -> None:
	placement = content.PicturePlacement(primitives.LogicalRectangle(0.0, 0.0, 100.0, 100.0),
		primitives.LogicalRectangle(10.0, 0.0, 80.0, 100.0), primitives.PictureFit.CONTAIN,
		primitives.CropInsets(0.0, 0.0, 0.0, 0.0))
	picture = content.PictureContent("photo.png", placement,
		primitives.ObjectAccessibility("Photo", "An accessible photo"))
	assert picture.placement.displayed_rectangle != picture.placement.allocation_rectangle


def test_picture_placement_rejects_fit_and_crop_contradictions() -> None:
	allocation = primitives.LogicalRectangle(0.0, 0.0, 100.0, 100.0)
	with pytest.raises(ValueError, match="contained pictures"):
		content.PicturePlacement(allocation, allocation, primitives.PictureFit.CONTAIN,
			primitives.CropInsets(0.1, 0.0, 0.0, 0.0))


def test_picture_placement_requires_cover_to_fill_and_stretch_to_avoid_crop() -> None:
	allocation = primitives.LogicalRectangle(0.0, 0.0, 100.0, 100.0)
	with pytest.raises(ValueError, match="covered pictures"):
		content.PicturePlacement(allocation, primitives.LogicalRectangle(5.0, 0.0, 90.0, 100.0),
			primitives.PictureFit.COVER, primitives.CropInsets(0.1, 0.0, 0.0, 0.0))
	with pytest.raises(ValueError, match="stretched pictures"):
		content.PicturePlacement(allocation, allocation, primitives.PictureFit.STRETCH,
			primitives.CropInsets(0.1, 0.0, 0.0, 0.0))
	placement = content.PicturePlacement(allocation, allocation, primitives.PictureFit.COVER,
		primitives.CropInsets(0.0, 0.0, 0.0, 0.0))
	assert placement.displayed_rectangle == allocation


def test_decorative_shape_cannot_carry_semantic_text_or_link() -> None:
	style = content.ShapeStyle(primitives.StyleRole.ACCENT, primitives.StyleRole.ACCENT, 1.0,
		primitives.LinePattern.SOLID)
	with pytest.raises(ValueError, match="decorative shapes"):
		content.ShapeContent(primitives.ShapeKind.RECTANGLE, style,
			primitives.ObjectAccessibility(decorative=True), text("label"))


def test_boolean_model_fields_reject_integer_substitutes() -> None:
	with pytest.raises(ValueError, match="bool"):
		content.RunStyle("OpenDyslexic", "ink", bold=1)
	with pytest.raises(ValueError, match="bool"):
		content.TextParagraph((), typography(), primitives.ParagraphProperties(
			primitives.HorizontalAlignment.START, 0.0, 0.0, 28.0, 0.0, 0.0, 0.0, ()), 1)
	with pytest.raises(ValueError, match="bool"):
		primitives.ObjectAccessibility(decorative=1)
	with pytest.raises(ValueError, match="bool"):
		content.ListMetadata(primitives.ListKind.UNORDERED, 0, 1, 1)


def test_paragraph_line_spacing_is_an_exact_point_advance() -> None:
	"""Adapters receive one resolved physical line advance, not an em heuristic."""
	properties = primitives.ParagraphProperties(
		primitives.HorizontalAlignment.START, 0.0, 0.0, 36.4, 0.0, 0.0, 0.0, (),
		primitives.LineSpacingMode.EXACT)
	assert properties.line_spacing_mode is primitives.LineSpacingMode.EXACT
	assert properties.line_spacing_pt == 36.4
	with pytest.raises(ValueError, match="LineSpacingMode"):
		primitives.ParagraphProperties(
			primitives.HorizontalAlignment.START, 0.0, 0.0, 36.4, 0.0, 0.0, 0.0, (), "exact")


def test_list_continuation_context_is_explicit_and_immutable() -> None:
	"""Repeated ancestor context remains distinguishable from authored list items."""
	metadata = content.ListMetadata(primitives.ListKind.ORDERED, 1, 3, True)
	assert metadata.continuation_context is True
	with pytest.raises(dataclasses.FrozenInstanceError):
		metadata.continuation_context = False


def continuation_entry(value: str = "Ancestor") -> model.ContinuationContextEntry:
	return model.ContinuationContextEntry((content.TextRun(value, content.RunStyle("OpenDyslexic", "ink")),),
		primitives.ListKind.UNORDERED, 0, 1, source())


def continuation_context(
		display: primitives.ContinuationContextDisplay = primitives.ContinuationContextDisplay.INLINE_STATIC,
) -> model.ContinuationContext:
	return model.ContinuationContext(display, (continuation_entry(),))


def continuation_slide(
		kind: primitives.ContinuationKind,
		context: model.ContinuationContext | None,
		reveal_targets: tuple[model.RevealTarget, ...] = (),
		origin: primitives.LayoutObjectOrigin = primitives.LayoutObjectOrigin.AUTHORED,
) -> model.LayoutSlide:
	slot = outline_slot()
	return model.LayoutSlide(model.SlideIdentity("continued", 1, source(), "source", 0), identity((slot,)),
		(slot,), (dataclasses.replace(outline_object("body", reveal_targets), origin=origin),), (), kind, context)


def test_continuation_context_preserves_resolved_ancestor_source_and_is_immutable() -> None:
	entry = continuation_entry()
	context = continuation_context()
	assert entry.inlines[0].text == "Ancestor"
	assert context.entries == (entry,)
	with pytest.raises(dataclasses.FrozenInstanceError):
		entry.start = 2
	with pytest.raises(dataclasses.FrozenInstanceError):
		context.entries = ()


@pytest.mark.parametrize("display", (
	primitives.ContinuationContextDisplay.INLINE_STATIC,
	primitives.ContinuationContextDisplay.METADATA_ONLY,
))
def test_authored_continuation_context_accepts_static_or_metadata_display(
		display: primitives.ContinuationContextDisplay,
) -> None:
	physical = continuation_slide(primitives.ContinuationKind.AUTHORED, continuation_context(display))
	assert physical.continuation_context is not None
	assert physical.continuation_context.display is display


def test_context_handoff_requires_static_trail_and_no_body_reveals() -> None:
	physical = continuation_slide(primitives.ContinuationKind.CONTEXT_HANDOFF,
		continuation_context(primitives.ContinuationContextDisplay.HANDOFF_STATIC),
		origin=primitives.LayoutObjectOrigin.REPEATED_CONTEXT)
	assert physical.continuation_kind is primitives.ContinuationKind.CONTEXT_HANDOFF
	with pytest.raises(ValueError, match="HANDOFF_STATIC"):
		continuation_slide(primitives.ContinuationKind.CONTEXT_HANDOFF, continuation_context())
	with pytest.raises(ValueError, match="reveal targets"):
		continuation_slide(primitives.ContinuationKind.CONTEXT_HANDOFF,
			continuation_context(primitives.ContinuationContextDisplay.HANDOFF_STATIC),
			(reveal_target("reveal", "body", 0),), primitives.LayoutObjectOrigin.REPEATED_CONTEXT)


def test_context_handoff_rejects_ordinary_authored_no_reveal_object() -> None:
	with pytest.raises(ValueError, match="authored objects"):
		continuation_slide(primitives.ContinuationKind.CONTEXT_HANDOFF,
			continuation_context(primitives.ContinuationContextDisplay.HANDOFF_STATIC))


def test_context_handoff_accepts_repeated_context_and_generated_page_number() -> None:
	slot = outline_slot()
	repeated_title = dataclasses.replace(outline_object("Repeated title"), object_id="context-title",
		origin=primitives.LayoutObjectOrigin.REPEATED_CONTEXT)
	page_number = model.LayoutObject("page-number", primitives.PresentationRole.COMPONENT,
		primitives.StyleRole.MUTED, primitives.LogicalRectangle(450.0, 260.0, 40.0, 20.0),
		primitives.ObjectLayer.FOREGROUND, 1, 1, text("2"), frame_text(),
		origin=primitives.LayoutObjectOrigin.GENERATED_CHROME)
	physical = model.LayoutSlide(model.SlideIdentity("handoff", 1, source(), "source", 0), identity((slot,)),
		(slot,), (repeated_title, page_number), (), primitives.ContinuationKind.CONTEXT_HANDOFF,
		continuation_context(primitives.ContinuationContextDisplay.HANDOFF_STATIC))
	assert tuple(item.origin for item in physical.objects) == (
		primitives.LayoutObjectOrigin.REPEATED_CONTEXT,
		primitives.LayoutObjectOrigin.GENERATED_CHROME,
	)


def test_root_context_handoff_precedes_an_authored_child_continuation() -> None:
	"""A semantic handoff may be the first physical page for one source slide."""
	slot = outline_slot()
	handoff = model.LayoutSlide(model.SlideIdentity("handoff", 0, source()), identity((slot,)),
		(slot,), (dataclasses.replace(outline_object("Repeated context"),
			object_id="context", origin=primitives.LayoutObjectOrigin.REPEATED_CONTEXT),), (),
		primitives.ContinuationKind.CONTEXT_HANDOFF,
		continuation_context(primitives.ContinuationContextDisplay.HANDOFF_STATIC))
	child = model.LayoutSlide(model.SlideIdentity("authored-child", 1, source(), "handoff", 0),
		identity((slot,)), (slot,), (outline_object("Authored body"),), (),
		primitives.ContinuationKind.AUTHORED,
		continuation_context(primitives.ContinuationContextDisplay.INLINE_STATIC))
	deck = model.LayoutDeck(model.DeckIdentity("deck", pathlib.Path("inline.djot")),
		primitives.LogicalCanvas(), (), (handoff, child))
	assert deck.slides[1].identity.source_parent_id == handoff.identity.slide_id


@pytest.mark.parametrize("display", (
	primitives.ContinuationContextDisplay.INLINE_STATIC,
	primitives.ContinuationContextDisplay.METADATA_ONLY,
))
def test_root_authored_context_is_semantic_not_physical_lineage(
		display: primitives.ContinuationContextDisplay,
) -> None:
	"""A first physical page may retain ancestor context without a physical parent."""
	slot = outline_slot()
	root = model.LayoutSlide(model.SlideIdentity("root-authored", 0, source()), identity((slot,)),
		(slot,), (outline_object("Authored body"),), (), primitives.ContinuationKind.AUTHORED,
		continuation_context(display))
	deck = model.LayoutDeck(model.DeckIdentity("deck", pathlib.Path("inline.djot")),
		primitives.LogicalCanvas(), (), (root,))
	assert deck.slides[0].continuation_context.display is display


def test_layout_object_requires_known_origin_enum() -> None:
	with pytest.raises(ValueError, match="LayoutObjectOrigin"):
		dataclasses.replace(outline_object("body"), origin="authored")  # type: ignore[arg-type]


def test_continuation_context_rejects_inconsistent_kind_empty_trail_and_unprojectable_entries() -> None:
	with pytest.raises(ValueError, match="normal slides"):
		continuation_slide(primitives.ContinuationKind.NORMAL, continuation_context())
	with pytest.raises(ValueError, match="nonempty ordered"):
		model.ContinuationContext(primitives.ContinuationContextDisplay.METADATA_ONLY, ())
	with pytest.raises(ValueError, match="resolved InlineContent"):
		model.ContinuationContextEntry((object(),), primitives.ListKind.UNORDERED, 0, 1, source())
	with pytest.raises(ValueError, match="nonempty resolved"):
		model.ContinuationContextEntry((content.LineBreak(),), primitives.ListKind.UNORDERED, 0, 1, source())


def reveal_target(target_id: str, object_id: str, activation_order: int) -> model.RevealTarget:
	reveal = slide_lib.native_model.Reveal(slide_lib.native_model.RevealEffect.APPEAR,
		slide_lib.native_model.RevealSequence.OBJECT)
	return model.RevealTarget(target_id, object_id, reveal, activation_order)


def test_reveal_target_must_belong_to_its_layout_object() -> None:
	with pytest.raises(ValueError, match="owning object"):
		outline_object("text", (reveal_target("target", "other-object", 0),))


def paragraph_reveal() -> model.RevealTarget:
	reveal = slide_lib.native_model.Reveal(slide_lib.native_model.RevealEffect.APPEAR,
		slide_lib.native_model.RevealSequence.PARAGRAPHS)
	target = model.RevealTarget("paragraph", "target", reveal, 0, (0,))
	return target


def test_paragraph_reveal_rejects_every_non_text_projectable_content_kind() -> None:
	placement = content.PicturePlacement(primitives.LogicalRectangle(0.0, 0.0, 100.0, 100.0),
		primitives.LogicalRectangle(0.0, 0.0, 100.0, 100.0), primitives.PictureFit.STRETCH,
		primitives.CropInsets(0.0, 0.0, 0.0, 0.0))
	picture = content.PictureContent("photo.png", placement,
		primitives.ObjectAccessibility("Photo", "A photograph"))
	shape = content.ShapeContent(primitives.ShapeKind.RECTANGLE,
		content.ShapeStyle(primitives.StyleRole.ACCENT, primitives.StyleRole.ACCENT, 1.0,
			primitives.LinePattern.SOLID), primitives.ObjectAccessibility(decorative=True))
	table = content.TableContent((content.TableRow((content.TableCell((),
		primitives.Insets(0.0, 0.0, 0.0, 0.0), primitives.VerticalAlignment.TOP),)),), (),
		(100.0,), (30.0,), table_style())
	for value in (picture, shape, table):
		frame = frame_text() if content.text_capable_content(value) else None
		with pytest.raises(ValueError, match="require TextContent"):
			model.LayoutObject("target", primitives.PresentationRole.CONTENT, primitives.StyleRole.BODY,
				primitives.LogicalRectangle(0.0, 0.0, 100.0, 100.0), primitives.ObjectLayer.CONTENT,
				0, 0, value, frame, reveal_targets=(paragraph_reveal(),))


def test_paragraph_reveal_requires_top_level_text_content_in_range() -> None:
	reveal = slide_lib.native_model.Reveal(slide_lib.native_model.RevealEffect.APPEAR,
		slide_lib.native_model.RevealSequence.PARAGRAPHS)
	too_far = model.RevealTarget("too-far", "body", reveal, 0, (1,))
	with pytest.raises(ValueError, match="top-level paragraphs in range"):
		outline_object("text", (too_far,))


@pytest.mark.parametrize(("source_kind", "attributes"), (
	("CodeBlock", ()),
	("DisplayMath", ()),
	("QuoteBlock", ()),
	("InlineMath", ()),
	("Paragraph", (slide_lib.native_model.Attribute("class", "callout"),)),
))
def test_unsupported_source_facts_preserve_complete_diagnostic_identity(
		source_kind: str, attributes: tuple[slide_lib.native_model.Attribute, ...],
) -> None:
	"""Source traversal owns creating these facts; the model preserves their diagnostics."""
	fact = model.UnsupportedSourceFact(source(), source_kind, attributes)
	assert fact.location == source()
	assert fact.source_kind == source_kind
	assert fact.attributes == attributes
	with pytest.raises(ValueError, match=rf"inline\.djot:1: {source_kind} has no physical projection"):
		model.reject_unsupported_source_facts((fact,))


def test_unsupported_source_fact_diagnostic_names_unsupported_attributes() -> None:
	fact = model.UnsupportedSourceFact(source(), "Paragraph",
		(slide_lib.native_model.Attribute("class", "callout"),
			slide_lib.native_model.Attribute("reveal", "fade")))
	assert fact.diagnostic() == (
		"inline.djot:1: Paragraph has no physical projection; unsupported attributes: class, reveal"
	)


def test_layout_objects_accept_only_adapter_projectable_content() -> None:
	placement = content.PicturePlacement(primitives.LogicalRectangle(0.0, 0.0, 100.0, 100.0),
		primitives.LogicalRectangle(0.0, 0.0, 100.0, 100.0), primitives.PictureFit.STRETCH,
		primitives.CropInsets(0.0, 0.0, 0.0, 0.0))
	picture = content.PictureContent("photo.png", placement,
		primitives.ObjectAccessibility("Photo", "A photograph"))
	shape = content.ShapeContent(primitives.ShapeKind.RECTANGLE,
		content.ShapeStyle(primitives.StyleRole.ACCENT, primitives.StyleRole.ACCENT, 1.0,
			primitives.LinePattern.SOLID), primitives.ObjectAccessibility(decorative=True))
	table = content.TableContent((content.TableRow((content.TableCell((),
		primitives.Insets(0.0, 0.0, 0.0, 0.0), primitives.VerticalAlignment.TOP),)),), (),
		(100.0,), (30.0,), table_style())
	for value in (text("body"), picture, shape, table):
		frame = frame_text() if content.text_capable_content(value) else None
		assert model.LayoutObject("projectable", primitives.PresentationRole.CONTENT,
			primitives.StyleRole.BODY, primitives.LogicalRectangle(0.0, 0.0, 100.0, 100.0),
			primitives.ObjectLayer.CONTENT, 0, 0, value, frame).content is value
	with pytest.raises(ValueError, match="adapter-projectable"):
		model.LayoutObject("unprojectable", primitives.PresentationRole.CONTENT,
			primitives.StyleRole.BODY, primitives.LogicalRectangle(0.0, 0.0, 100.0, 100.0),
			primitives.ObjectLayer.CONTENT, 0, 0, object())  # type: ignore[arg-type]


def test_numeric_primitives_reject_boolean_values() -> None:
	with pytest.raises(ValueError, match="real finite number"):
		primitives.LogicalRectangle(True, 0.0, 100.0, 100.0)
	with pytest.raises(ValueError, match="real finite number"):
		primitives.Insets(0.0, False, 0.0, 0.0)
	with pytest.raises(ValueError, match="real finite number"):
		content.ShapeStyle(primitives.StyleRole.ACCENT, primitives.StyleRole.ACCENT, 1.0,
			primitives.LinePattern.SOLID, False)


def test_slide_reveals_are_unique_contiguous_and_source_ordered() -> None:
	slot = outline_slot()
	first = outline_object("first", (reveal_target("first-target", "body", 1),))
	with pytest.raises(ValueError, match="contiguous source-ordered"):
		model.LayoutSlide(model.SlideIdentity("reveal-order", 0, source()), identity((slot,)),
			(slot,), (first,), ())


def test_slide_reveal_target_ids_are_unique() -> None:
	slot = outline_slot()
	targets = (reveal_target("duplicate", "body", 0), reveal_target("duplicate", "body", 1))
	with pytest.raises(ValueError, match="reveal target identities"):
		model.LayoutSlide(model.SlideIdentity("duplicate-reveal", 0, source()), identity((slot,)),
			(slot,), (outline_object("text", targets),), ())


def table_style() -> content.TableStyle:
	return content.TableStyle(primitives.StyleRole.TABLE_HEADER, primitives.StyleRole.TABLE_BODY,
		primitives.StyleRole.MUTED, 1.0, primitives.LinePattern.SOLID)


def test_table_grid_accepts_row_fully_covered_by_prior_row_span() -> None:
	cell = content.TableCell((), primitives.Insets(0.0, 0.0, 0.0, 0.0),
		primitives.VerticalAlignment.TOP, 2, 2)
	table = content.TableContent((content.TableRow((cell,)),), (content.TableRow(()),),
		(100.0, 100.0), (30.0, 30.0), table_style())
	assert table.body_rows[0].cells == ()


def test_table_grid_rejects_underfill_and_overlapping_spans() -> None:
	cell = content.TableCell((), primitives.Insets(0.0, 0.0, 0.0, 0.0),
		primitives.VerticalAlignment.TOP)
	with pytest.raises(ValueError, match="unfilled"):
		content.TableContent((content.TableRow((cell,)),), (), (100.0, 100.0), (30.0,), table_style())
	spanning = content.TableCell((), primitives.Insets(0.0, 0.0, 0.0, 0.0),
		primitives.VerticalAlignment.TOP, 1, 2)
	overlapping = content.TableCell((), primitives.Insets(0.0, 0.0, 0.0, 0.0),
		primitives.VerticalAlignment.TOP, 2, 1)
	rows = (content.TableRow((cell, spanning, cell)), content.TableRow((overlapping,)))
	with pytest.raises(ValueError, match="overlap"):
		content.TableContent(rows, (), (100.0, 100.0, 100.0), (30.0, 30.0), table_style())


def test_table_grid_rejects_spans_past_declared_bounds() -> None:
	cell = content.TableCell((), primitives.Insets(0.0, 0.0, 0.0, 0.0),
		primitives.VerticalAlignment.TOP, 2, 1)
	with pytest.raises(ValueError, match="exceeds"):
		content.TableContent((content.TableRow((cell,)),), (), (100.0,), (30.0,), table_style())


def test_continuations_record_parent_and_zero_based_index() -> None:
	with pytest.raises(ValueError, match="source parent"):
		model.SlideIdentity("continuation", 1, source(), continuation_index=1)
	identity_value = model.SlideIdentity("continuation", 1, source(), "source-slide", 0)
	assert identity_value.continuation_index == 0


def test_deck_requires_contiguous_physical_order_and_valid_continuations() -> None:
	first = slide("first")
	second = model.LayoutSlide(model.SlideIdentity("second", 2, source()), first.layout,
		first.slots, (outline_object("second"),), ())
	with pytest.raises(ValueError, match="contiguous physical"):
		model.LayoutDeck(model.DeckIdentity("deck", pathlib.Path("inline.djot")),
			primitives.LogicalCanvas(), (), (first, second))


def test_deck_slide_ids_and_physical_indexes_are_unique() -> None:
	first = slide("first")
	duplicate = model.LayoutSlide(model.SlideIdentity("slide-first", 1, source()), first.layout,
		first.slots, (outline_object("duplicate"),), ())
	with pytest.raises(ValueError, match="slide identities"):
		model.LayoutDeck(model.DeckIdentity("deck", pathlib.Path("inline.djot")),
			primitives.LogicalCanvas(), (), (first, duplicate))


def test_deck_continuation_sequences_require_parent_order_and_zero_based_indexes() -> None:
	parent = slide("parent")
	child = model.LayoutSlide(model.SlideIdentity("child", 1, source(), "slide-parent", 1),
		parent.layout, parent.slots, (outline_object("child"),), ())
	with pytest.raises(ValueError, match="zero-based"):
		model.LayoutDeck(model.DeckIdentity("deck", pathlib.Path("inline.djot")),
			primitives.LogicalCanvas(), (), (parent, child))


def test_deck_continuations_require_an_earlier_existing_parent() -> None:
	child = slide("child")
	orphan = model.LayoutSlide(model.SlideIdentity("orphan", 1, source(), "missing", 0),
		child.layout, child.slots, (outline_object("orphan"),), ())
	with pytest.raises(ValueError, match="must exist"):
		model.LayoutDeck(model.DeckIdentity("deck", pathlib.Path("inline.djot")),
			primitives.LogicalCanvas(), (), (child, orphan))
	parent = model.LayoutSlide(model.SlideIdentity("parent", 1, source()), child.layout,
		child.slots, (outline_object("parent"),), ())
	early_child = model.LayoutSlide(model.SlideIdentity("early-child", 0, source(), "parent", 0),
		child.layout, child.slots, (outline_object("early-child"),), ())
	with pytest.raises(ValueError, match="precede"):
		model.LayoutDeck(model.DeckIdentity("deck", pathlib.Path("inline.djot")),
			primitives.LogicalCanvas(), (), (early_child, parent))
