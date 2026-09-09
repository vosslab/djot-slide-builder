"""Behavior coverage for the format-neutral layout compiler boundary."""

import dataclasses
import pathlib

import pytest

import slide_lib.djot_parser
import slide_lib.layout_engine
import slide_lib.layout_content
import slide_lib.layout_builders
import slide_lib.layout_measurement
import slide_lib.layout_primitives
import slide_lib.native_model
import slide_lib.presentation_theme


def compile_source(tmp_path: pathlib.Path, source: str) -> slide_lib.layout_model.LayoutDeck:
	"""Parse and compile one small Djot specimen through the public API."""
	path = tmp_path / "specimen.djot"
	# A one-pixel GIF keeps gallery/image placement tests self-contained and offline.
	(tmp_path / "pixel.gif").write_bytes(
		b"GIF87a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;")
	path.write_text(source, encoding="utf-8")
	deck = slide_lib.djot_parser.parse_deck(path)
	result = slide_lib.layout_engine.compile_layout_deck(deck, slide_lib.presentation_theme.default_theme())
	return result


def source_for(name: str) -> str:
	"""Return a valid minimal source surface for each registered layout."""
	contract = slide_lib.layout_engine.layout_contract(name)
	lines = [f"=== layout: {name}"]
	if contract.allows_title:
		lines.extend(("", "# Title"))
	for slot in contract.slot_names:
		lines.extend(("", f"@{slot}", "", f"Text in {slot}."))
	if name == "gallery":
		lines[-1] = "![Pixel](pixel.gif)"
	result = "\n".join(lines)
	return result


@pytest.mark.parametrize("name", slide_lib.layout_engine.registered_layout_names())
def test_every_registered_layout_compiles_to_a_complete_immutable_plan(tmp_path: pathlib.Path,
		name: str) -> None:
	deck = compile_source(tmp_path, source_for(name))
	slide = deck.slides[0]
	assert slide.layout.layout_name == name
	assert slide.layout.topology.key_for_canvas(deck.canvas) in deck.presentation_page_layouts
	assert tuple(slot.slot_id for slot in slide.slots if slot.slot_id != "title") == \
		slide_lib.layout_engine.layout_contract(name).slot_names


def test_centered_text_uses_one_mixed_typography_libreoffice_member(
		tmp_path: pathlib.Path) -> None:
	"""Centered title and subtitle remain editable inside the one built-in text member."""
	deck = compile_source(tmp_path, "=== layout: centered-text\n\n# Title\n\n## Subtitle")
	slide = deck.slides[0]
	roles = tuple(paragraph.typography.role for paragraph in slide.objects[0].content.paragraphs)
	assert roles == (slide_lib.layout_primitives.StyleRole.TITLE,
		slide_lib.layout_primitives.StyleRole.SUBTITLE)
	assert slide.layout.topology.libreoffice_layout.autolayout is \
		slide_lib.layout_primitives.LibreOfficeAutoLayout.ONLY_TEXT


def test_vertical_title_catalog_uses_right_strip_and_stacked_content(
		tmp_path: pathlib.Path) -> None:
	"""The physical plan follows LibreOffice's vertical-title layout relationship."""
	deck = compile_source(tmp_path, source_for("vertical-title-two-panels"))
	title, text, chart = deck.slides[0].slots
	assert title.rectangle.x > text.rectangle.x and text.rectangle.y < chart.rectangle.y
	assert text.properties.frame_text.text_direction is \
		slide_lib.layout_primitives.TextDirection.VERTICAL and \
		chart.properties.frame_text.text_direction is \
		slide_lib.layout_primitives.TextDirection.HORIZONTAL


def test_two_vertical_content_members_are_side_by_side(tmp_path: pathlib.Path) -> None:
	"""The approved final layout name projects LibreOffice's two vertical-content grid."""
	deck = compile_source(tmp_path, source_for("two-panels-vertical-clipart"))
	left, right = deck.slides[0].slots[1:]
	assert left.rectangle.x < right.rectangle.x
	assert all(slot.properties.frame_text.text_direction is
		slide_lib.layout_primitives.TextDirection.VERTICAL for slot in (left, right))


def test_text_uses_point_sizes_and_native_shrink_policy(tmp_path: pathlib.Path) -> None:
	deck = compile_source(tmp_path, "=== layout: one-panel\n\n# Title\n\n@body\n\nOrdinary text.")
	title, body = deck.slides[0].objects
	assert title.content.paragraphs[0].typography.selected_size_pt == 36.0
	assert body.content.paragraphs[0].typography.selected_size_pt == 28.0
	assert title.frame_text.overflow_policy.value == "shrink"


def test_overflow_and_unsupported_source_fail_at_the_source_location(tmp_path: pathlib.Path) -> None:
	long_line = " ".join("word" for _ in range(5000))
	with pytest.raises(ValueError, match=r"specimen\.djot:5:.*24 pt"):
		compile_source(tmp_path, f"=== layout: one-panel\n\n@body\n\n{long_line}")
	with pytest.raises(ValueError, match=r"specimen\.djot:5: CodeBlock has no physical projection"):
		compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\n```\ncode\n```")


def test_reveals_have_stable_contiguous_activation_order(tmp_path: pathlib.Path) -> None:
	deck = compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\n=> appear\nVisible later.")
	targets = tuple(target for item in deck.slides[0].objects for target in item.reveal_targets)
	assert tuple(target.activation_order for target in targets) == tuple(range(len(targets)))
	assert targets[0].target_id.startswith("body")


def test_one_panel_continuation_is_greedy_and_repeats_title_notes_and_number(tmp_path: pathlib.Path) -> None:
	"""A long source becomes same-topology physical pages at whole paragraph boundaries."""
	paragraphs = "\n\n".join(f"Paragraph {number}: " + "word " * 30 for number in range(36))
	deck = compile_source(tmp_path, f"=== layout: one-panel\n\n# Stable title\n\n@body\n\n{paragraphs}")
	assert len(deck.slides) > 1
	assert tuple(page.identity.slide_id for page in deck.slides) == tuple(
		f"slide-1-p{number}" for number in range(len(deck.slides)))
	assert tuple(page.identity.index for page in deck.slides) == tuple(range(len(deck.slides)))
	assert all(page.layout == deck.slides[0].layout for page in deck.slides)
	assert all(note.note_id.startswith(page.identity.slide_id) for page in deck.slides for note in page.notes)
	assert all(page.objects[-1].object_id == "page-number" for page in deck.slides)
	body_counts = [len(page.objects[1].content.paragraphs) for page in deck.slides]
	assert sum(body_counts) == 36


def test_continuation_preserves_root_list_subtrees_and_does_not_repeat_context_reveals(
		tmp_path: pathlib.Path) -> None:
	"""A nested list is indivisible while the local H2 remains readable on later pages."""
	items = "\n".join(f"- Item {number}\n  - child " + "word " * 18 for number in range(20))
	deck = compile_source(tmp_path, "=== layout: one-panel\n\n# Title\n\n@body\n\n## Context\n\n" + items)
	assert len(deck.slides) > 1
	for page in deck.slides:
		text_objects = tuple(item for item in page.objects if hasattr(item.content, "paragraphs"))
		assert any("Context" in "".join(run.text for run in item.content.paragraphs[0].inlines
			if hasattr(run, "text")) for item in text_objects)
		assert any(len(item.content.paragraphs) > 1 for item in text_objects)


def test_pagination_does_not_rescue_forbidden_layout_or_atomic_content(tmp_path: pathlib.Path) -> None:
	"""Only one-panel gets the continuation policy, and an oversized paragraph still fails."""
	long_text = "word " * 5000
	with pytest.raises(ValueError, match=r"specimen\.djot:5:.*24 pt"):
		compile_source(tmp_path, f"=== layout: two-panels\n\n@left\n\n{long_text}\n\n@right\n\nShort.")
	with pytest.raises(ValueError, match=r"specimen\.djot:5: one atomic continuation unit.*24 pt"):
		compile_source(tmp_path, f"=== layout: one-panel\n\n@body\n\n{long_text}")


def test_terminal_paragraph_has_no_spacing_after_and_lect02a_line_112_paginates() -> None:
	"""Trailing frame spacing is not capacity, and the real contact list is a continuation."""
	path = pathlib.Path("genetics/djot/lect02a-2025_announcements.djot")
	source = slide_lib.djot_parser.parse_deck(path)
	slide = next(item for item in source.slides if item.location.line == 106)
	deck = dataclasses.replace(source, slides=(slide,))
	result = slide_lib.layout_engine.compile_layout_deck(deck, slide_lib.presentation_theme.default_theme())
	assert len(result.slides) >= 2
	assert all(item.layout.layout_name == "one-panel" for item in result.slides)
	for item in result.slides:
		body = next(object for object in item.objects if object.object_id == "body")
		assert body.content.paragraphs[-1].properties.space_after_pt == 0


def test_mixed_table_flow_preserves_headers_and_all_source_objects(tmp_path: pathlib.Path) -> None:
	"""Paragraph/table/paragraph bodies retain source order instead of dropping text around a table."""
	deck = compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\nBefore table.\n\n| H | I |\n| - | - |\n| A | B |\n\nAfter table.")
	objects = tuple(item for slide in deck.slides for item in slide.objects)
	assert sum(isinstance(item.content, slide_lib.layout_content.TextContent) for item in objects) >= 2
	table = next(item.content for item in objects if isinstance(item.content, slide_lib.layout_content.TableContent))
	assert len(table.header_rows) == 1
	assert len(table.body_rows) == 1


def test_continuation_repeats_qualified_notes_without_cross_page_reveals(tmp_path: pathlib.Path) -> None:
	"""Repeated context is not reanimated, while per-page authored targets restart at zero."""
	paragraphs = "\n\n".join(f"=> appear\nParagraph {number}: " + "word " * 30 for number in range(30))
	path = tmp_path / "notes.djot"
	path.write_text(f"=== layout: one-panel\n\n# Title\n\n@body\n\n{paragraphs}", encoding="utf-8")
	source = slide_lib.djot_parser.parse_deck(path)
	slide = dataclasses.replace(source.slides[0], notes=("speaker note",))
	deck = dataclasses.replace(source, slides=(slide,))
	result = slide_lib.layout_engine.compile_layout_deck(deck, slide_lib.presentation_theme.default_theme())
	assert len(result.slides) > 1
	for page in result.slides:
		assert page.notes[0].note_id == f"{page.identity.slide_id}-note-0"
		targets = tuple(target for item in page.objects for target in item.reveal_targets)
		assert tuple(target.activation_order for target in targets) == tuple(range(len(targets)))


def test_lect02a_line_356_grid_decomposes_in_slot_order() -> None:
	"""The known dense grid becomes provenance-bearing one-panel pages, never clipped cells."""
	path = pathlib.Path("genetics/djot/lect02a-2025_announcements.djot")
	source = slide_lib.djot_parser.parse_deck(path)
	slide = next(item for item in source.slides if item.location.line == 356)
	result = slide_lib.layout_engine.compile_layout_deck(dataclasses.replace(source, slides=(slide,)),
		slide_lib.presentation_theme.default_theme())
	pages = result.slides
	assert pages
	assert all(item.layout.layout_name == "one-panel" for item in pages)
	origins = tuple(next(object.decomposition_origin for object in page.objects
		if object.decomposition_origin is not None) for page in pages)
	assert {origin.original_slot for origin in origins} == {"left", "right"}
	assert tuple(origin.source_order for origin in origins) == tuple(
		sorted(origin.source_order for origin in origins))
	assert all(origin.source_slide_id == "slide-1" for origin in origins)
	assert all(origin.source.line in (362, 375) for origin in origins)
	assert all(object.decomposition_origin is not None for page in pages for object in page.objects
		if object.origin.value == "authored" and object.object_id != "title")


def test_lect02a_line_243_grid_preflight_jointly_selects_the_largest_title() -> None:
	"""Grid decomposition uses the same title/body capacity policy as ordinary slides."""
	path = pathlib.Path("genetics/djot/lect02a-2025_announcements.djot")
	source = slide_lib.djot_parser.parse_deck(path)
	slide = next(item for item in source.slides if item.location.line == 237)
	isolated = dataclasses.replace(source, slides=(slide,))
	theme = slide_lib.presentation_theme.default_theme()
	result = slide_lib.layout_engine.compile_layout_deck(isolated, theme)
	assert all(page.layout.layout_name == "one-panel" for page in result.slides)
	first = result.slides[0]
	title = next(item for item in first.objects if item.object_id == "title")
	body = next(item for item in first.objects if item.decomposition_origin is not None)
	selected = title.content.paragraphs[0].typography.selected_size_pt
	assert 30.0 <= selected <= 36.0
	assert body.content.paragraphs[0].typography.selected_size_pt == 24.0
	assert body.decomposition_origin.original_slot == "left"
	assert body.decomposition_origin.source_order == 0
	text = "\n".join("".join(run.text for paragraph in item.content.paragraphs
		for run in paragraph.inlines if hasattr(run, "text")) for page in result.slides
		for item in page.objects if item.decomposition_origin is not None and
		isinstance(item.content, slide_lib.layout_content.TextContent))
	assert text.count("This idiom can also be applied in education") == 1
	assert text.count("https://crossidiomas.com/build-the-plane-while-flying-it/") == 1


def test_grid_stream_copacks_slots_as_distinct_provenance_objects(tmp_path: pathlib.Path) -> None:
	"""A decomposed grid may share a page, but it never joins two source slots."""
	left = "\n".join("- " + "word " * 10 for _number in range(7))
	deck = compile_source(tmp_path, f"=== layout: two-panels\n\n# Grid\n\n@left\n\n{left}\n\n@right\n\nRight.")
	authored = tuple(item for page in deck.slides for item in page.objects if item.decomposition_origin is not None)
	assert any(tuple(item.decomposition_origin.original_slot for item in page.objects
		if item.decomposition_origin is not None)[-1:] == ("right",) for page in deck.slides)
	assert all(item.object_id.startswith("body-unit-") for item in authored)


def test_grid_stream_finishes_one_slot_before_copacking_the_next(tmp_path: pathlib.Path) -> None:
	"""Long list fragments retain their left origin before the right slot can resume."""
	items = "\n".join(f"- Left {number}: " + "word " * 10 for number in range(9))
	deck = compile_source(tmp_path, "=== layout: two-panels\n\n# Grid\n\n@left\n\n## Left context\n\n" +
		items + "\n\n@right\n\nRight.")
	assert len(deck.slides) >= 2
	by_page = tuple(tuple(item.decomposition_origin.original_slot for item in page.objects
		if item.decomposition_origin is not None) for page in deck.slides)
	flattened = tuple(slot for page_slots in by_page for slot in page_slots)
	assert flattened == tuple(sorted(flattened, key=lambda slot: (slot == "right",)))
	assert any(page_slots[-1:] == ("right",) and "left" in page_slots for page_slots in by_page), by_page


def test_fitting_grid_keeps_its_declared_topology_without_origins(tmp_path: pathlib.Path) -> None:
	"""Grid provenance is only for physical one-panel decomposition."""
	deck = compile_source(tmp_path, "=== layout: two-panels\n\n# Grid\n\n@left\n\nLeft.\n\n@right\n\nRight.")
	assert deck.slides[0].layout.layout_name == "two-panels"
	assert not any(item.decomposition_origin for item in deck.slides[0].objects)


def test_grid_stream_repeats_table_headers_and_local_heading(
		tmp_path: pathlib.Path) -> None:
	"""Table-row units keep their header and local context through grid pagination."""
	rows = "\n".join(f"| Row {number} | Value {number} |" for number in range(15))
	source = "=== layout: two-panels\n\n# Grid\n\n@left\n\n## Local table\n\n| Name | Value |\n| - | - |\n" + \
		rows + "\n\n@right\n\nRight."
	deck = compile_source(tmp_path, source)
	assert len(deck.slides) > 1
	tables = tuple(item.content for page in deck.slides for item in page.objects
		if isinstance(item.content, slide_lib.layout_content.TableContent))
	assert all(len(table.header_rows) == 1 for table in tables)
	assert all(any(item.decomposition_origin and item.decomposition_origin.original_slot == "left"
		for item in page.objects) for page in deck.slides[:-1])


def test_grid_stream_reveals_stay_local_to_their_physical_page(tmp_path: pathlib.Path) -> None:
	"""A decomposed stream retains source reveals and renumbers each physical page."""
	left = "\n".join("- " + "word " * 10 for _number in range(7))
	deck = compile_source(tmp_path, f"=== layout: two-panels\n\n# Grid\n\n@left\n\n{left}\n\n@right\n\n=> appear\nRight reveal.")
	for page in deck.slides:
		targets = tuple(target for item in page.objects for target in item.reveal_targets)
		assert tuple(target.activation_order for target in targets) == tuple(range(len(targets)))


def test_grid_stream_reports_an_unsplittable_unit_at_its_source(tmp_path: pathlib.Path) -> None:
	"""Grid decomposition has no anonymous paragraph fallback for atomic failure."""
	with pytest.raises(ValueError, match=r"specimen\.djot:5: one atomic grid stream unit.*24 pt"):
		compile_source(tmp_path, "=== layout: two-panels\n\n@left\n\n" + "word " * 5000 +
			"\n\n@right\n\nRight.")


def test_font_profile_measurement_is_repeatable_and_respects_runs_and_list_insets() -> None:
	"""Fitting uses the bundled face advances, explicit breaks, and master list positions."""
	theme = slide_lib.presentation_theme.default_theme()
	plain = (slide_lib.native_model.Text("A URL-sized run of ordinary editable words."),)
	broken = (slide_lib.native_model.Text("A URL-sized"), slide_lib.native_model.Break(),
		slide_lib.native_model.Text("run of ordinary editable words."))
	plain_height = slide_lib.layout_measurement.paragraph_height(plain, 28.0, 1000.0, theme)
	assert plain_height == slide_lib.layout_measurement.paragraph_height(plain, 28.0, 1000.0, theme)
	assert slide_lib.layout_measurement.paragraph_height(broken, 28.0, 1000.0, theme) > plain_height
	assert slide_lib.layout_measurement.paragraph_height(plain, 28.0, 1000.0, theme, 0, True) >= plain_height
	literal = (slide_lib.native_model.Link((slide_lib.native_model.Text("https://example.edu/a-long-address"),),
		"https://example.edu/a-long-address"),)
	ordinary = (slide_lib.native_model.Text("https://example.edu/a-long-address"),)
	assert slide_lib.layout_measurement.paragraph_height(literal, 28.0, 300.0, theme) <= \
		slide_lib.layout_measurement.paragraph_height(ordinary, 28.0, 300.0, theme)
	# Quarter-point progression stays monotonic under the pinned OpenDyslexic and
	# PT Sans Narrow faces; no host font can change this preflight result.
	assert slide_lib.layout_measurement.paragraph_height(plain, 28.0, 300.0, theme) >= \
		slide_lib.layout_measurement.paragraph_height(plain, 24.0, 300.0, theme)


def test_measurement_session_reuses_exact_shaping_without_changing_plan(tmp_path: pathlib.Path) -> None:
	"""One compilation-scoped cache reuses pinned faces and immutable paragraph keys."""
	theme = slide_lib.presentation_theme.default_theme()
	session = slide_lib.layout_measurement.MeasurementSession(theme)
	inlines = (slide_lib.native_model.Text("Repeated exact paragraph shaping stays cached."),)
	first = session.paragraph_metrics(inlines, 28.0, 600.0)
	before = session.statistics()
	second = session.paragraph_metrics(inlines, 28.0, 600.0)
	after = session.statistics()
	assert first == second
	assert after.shape_calls == before.shape_calls
	assert after.paragraph_cache_hits == before.paragraph_cache_hits + 1
	assert after.profile_resolutions <= len(theme.font_metrics)
	assert after.face_loads <= 1
	source = "=== layout: one-panel\n\n# Cached title\n\n@body\n\nRepeated body."
	assert compile_source(tmp_path, source) == compile_source(tmp_path, source)


def test_measurement_cache_distinguishes_quarter_point_face_instances() -> None:
	"""Quarter-point sizes are separate shaped-face identities, even at one pixel size."""
	theme = slide_lib.presentation_theme.default_theme()
	session = slide_lib.layout_measurement.MeasurementSession(theme)
	first = session.advance("OpenDyslexic", False, False, 24.0, "precise cache key")
	second = session.advance("OpenDyslexic", False, False, 24.25, "precise cache key")
	assert isinstance(first, float)
	assert isinstance(second, float)
	assert len(session._faces) == 2
	assert len(session._advances) == 2
	assert session.statistics().shape_calls == 2


def test_deep_sibling_handoffs_keep_full_resolved_ancestor_trails(tmp_path: pathlib.Path) -> None:
	"""Deep sibling leaves hand off every ancestor, never a one-level special case."""
	ancestor_words = "word " * 20
	leaf_words = "word " * 50
	source = "=== layout: one-panel\n\n@body\n\n" + \
		f"- outer {ancestor_words}\n  - middle {ancestor_words}\n    - leaf A {leaf_words}\n    - leaf B {leaf_words}"
	deck = compile_source(tmp_path, source)
	handoffs = tuple(page for page in deck.slides if page.continuation_kind.value == "context-handoff")
	authored = tuple(page for page in deck.slides if page.continuation_context is not None and
		page.continuation_context.display.value == "metadata-only")
	assert len(handoffs) == len(authored) == 2
	assert deck.slides[0] is handoffs[0]
	assert handoffs[0].identity.source_parent_id is None
	assert handoffs[0].continuation_context is not None
	assert handoffs[0].continuation_context.display.value == "handoff-static"
	for handoff, descendant in zip(handoffs, authored):
		static = handoff.continuation_context
		metadata = descendant.continuation_context
		assert static is not None and metadata is not None
		assert static.display.value == "handoff-static"
		assert tuple(entry.level for entry in static.entries) == (0, 1)
		assert tuple(entry.level for entry in metadata.entries) == (0, 1)
		assert tuple(entry.start for entry in static.entries) == (1, 1)
		assert tuple(entry.source for entry in static.entries) == tuple(entry.source for entry in metadata.entries)
		assert tuple("".join(run.text for run in entry.inlines if hasattr(run, "text"))
			for entry in static.entries) == tuple("".join(run.text for run in entry.inlines
				if hasattr(run, "text")) for entry in metadata.entries)
		assert descendant.identity.source_parent_id == handoff.identity.slide_id


def test_overdeep_trail_uses_metadata_without_an_invalid_static_handoff(tmp_path: pathlib.Path) -> None:
	"""When the full ancestor trail cannot fit, leaf pages retain metadata only."""
	words = "word " * 50
	source = "=== layout: one-panel\n\n@body\n\n" + \
		f"- outer {words}\n  - middle {words}\n    - leaf A {words}\n    - leaf B {words}"
	deck = compile_source(tmp_path, source)
	assert not any(page.continuation_kind.value == "context-handoff" for page in deck.slides)
	metadata = tuple(page for page in deck.slides if page.continuation_context is not None)
	assert metadata
	assert all(page.continuation_context.display.value == "metadata-only" for page in metadata)
	assert all(tuple(entry.level for entry in page.continuation_context.entries) == (0, 1)
		for page in metadata)


def test_long_literal_url_has_explicit_lossless_breaks_and_floor_safe_measurement(
		tmp_path: pathlib.Path) -> None:
	"""No unbroken URL is silently certified wider than its text frame."""
	url = "https://example.edu/" + "pathsegment" * 18
	deck = compile_source(tmp_path, f"=== layout: one-panel\n\n@body\n\n[{url}]({url})")
	paragraph = deck.slides[0].objects[0].content.paragraphs[0]
	assert any(isinstance(item, slide_lib.layout_content.LineBreak) for item in paragraph.inlines)
	assert "".join(item.text for item in paragraph.inlines if hasattr(item, "text")) == url
	assert paragraph.typography.selected_size_pt >= 24.0


@pytest.mark.parametrize("source, marker", (
	("- outer\n  - inner $x$", "InlineMath"),
	("| H |\n| - |\n| $x$ |", "InlineMath"),
	("> quoted\n>\n> ```\n> code\n> ```", "QuoteBlock"),
))
def test_recursive_unsupported_source_facts_fail_through_public_compiler(
		tmp_path: pathlib.Path, source: str, marker: str) -> None:
	with pytest.raises(ValueError, match=marker):
		compile_source(tmp_path, f"=== layout: one-panel\n\n@body\n\n{source}")


def test_emitted_paragraph_properties_match_measurement_and_master_list_geometry(
		tmp_path: pathlib.Path) -> None:
	"""The physical plan retains the exact spacing and hanging indent it measured."""
	deck = compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\n- First item\n  - Nested item")
	paragraphs = deck.slides[0].objects[0].content.paragraphs
	theme = slide_lib.presentation_theme.default_theme()
	for paragraph in paragraphs:
		metadata = paragraph.list_metadata
		assert metadata is not None
		expected = slide_lib.layout_measurement.paragraph_properties(
			tuple(slide_lib.native_model.Text(run.text) for run in paragraph.inlines
				if hasattr(run, "text")), paragraph.typography.selected_size_pt, 1160.0,
			theme, metadata.level, True, paragraph.properties.space_after_pt == 0)
		assert paragraph.properties.line_spacing_pt == expected.line_spacing_pt
		assert paragraph.properties.indent_start_pt == expected.indent_start_pt
		assert paragraph.properties.first_line_indent_pt == expected.first_line_indent_pt
	assert paragraphs[0].properties.first_line_indent_pt < 0
	assert paragraphs[1].properties.indent_start_pt > paragraphs[0].properties.indent_start_pt


def test_lect02a_recursive_list_split_marks_static_context_once() -> None:
	"""A root subtree at line 293 partitions only at descendant-item boundaries."""
	path = pathlib.Path("genetics/djot/lect02a-2025_announcements.djot")
	source = slide_lib.djot_parser.parse_deck(path)
	slide = next(item for item in source.slides if item.location.line == 287)
	result = slide_lib.layout_engine.compile_layout_deck(
		dataclasses.replace(source, slides=(slide,)), slide_lib.presentation_theme.default_theme())
	assert len(result.slides) > 1
	metadata = tuple(paragraph.list_metadata for page in result.slides for object_item in page.objects
		if hasattr(object_item.content, "paragraphs") for paragraph in object_item.content.paragraphs
		if paragraph.list_metadata is not None)
	assert any(item.continuation_context for item in metadata)
	assert any(not item.continuation_context for item in metadata)
	assert any(page.continuation_context is not None and
		page.continuation_context.display.value == "inline-static" for page in result.slides)


def test_lect02a_leaf_uses_context_handoff_without_shrinking_or_leaf_split() -> None:
	"""The Student Profile leaf keeps readable type through the modelled handoff."""
	path = pathlib.Path("genetics/djot/lect02a-2025_announcements.djot")
	source = slide_lib.djot_parser.parse_deck(path)
	slide = next(item for item in source.slides if item.location.line == 462)
	result = slide_lib.layout_engine.compile_layout_deck(
		dataclasses.replace(source, slides=(slide,)), slide_lib.presentation_theme.default_theme())
	handoffs = tuple(item for item in result.slides if item.continuation_kind.value == "context-handoff")
	assert handoffs
	assert all(item.continuation_context.display.value == "handoff-static" for item in handoffs)
	authored = tuple(item for item in result.slides if item.continuation_context is not None and
		item.continuation_context.display.value == "metadata-only")
	assert authored


def test_full_lect02a_compilation_is_deterministic_and_keeps_its_physical_page_budget() -> None:
	"""The public compiler owns full-deck pagination without timing-sensitive assertions."""
	path = pathlib.Path("genetics/djot/lect02a-2025_announcements.djot")
	source = slide_lib.djot_parser.parse_deck(path)
	theme = slide_lib.presentation_theme.default_theme()
	first = slide_lib.layout_engine.compile_layout_deck(source, theme)
	second = slide_lib.layout_engine.compile_layout_deck(source, theme)
	assert first == second
	assert len(first.slides) == 99


def test_compiler_has_no_adapter_imports() -> None:
	for module_path in ("slide_lib/layout_engine.py", "slide_lib/layout_registry.py",
			"slide_lib/layout_measurement.py", "slide_lib/layout_builders.py"):
		content = pathlib.Path(module_path).read_text(encoding="utf-8")
		assert "pptx" not in content.lower()
		assert "odp_" not in content.lower()
