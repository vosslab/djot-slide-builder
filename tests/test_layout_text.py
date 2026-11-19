"""Text layout contracts for readable links, citations, and content-preserving wrapping."""

import pathlib

import pytest

import slide_lib.djot_audit
import slide_lib.layout_content
import slide_lib.layout_measurement
import slide_lib.layout_object_builders
import slide_lib.layout_primitives
import slide_lib.native_model
import slide_lib.presentation_theme
import layout_test_helpers


#============================================
def test_citation_preserves_layout_and_keeps_condensed_clickable_text(tmp_path: pathlib.Path) -> None:
	"""Citation text uses the bottom margin without consuming the existing panel space."""
	base = "=== layout: two-panels\n\n# Tutorial\n\n@left\n\nStory cue.\n\n@right\n\nComparison.\n"
	url = "https://example.test/tutorial"
	plain = layout_test_helpers.compile_source(tmp_path, base).plan.slides[0]
	cited_source = base + "\n@citation\n\nSmith. _Study title._ 2026. " + url
	cited = layout_test_helpers.compile_source(tmp_path, cited_source).plan.slides[0]
	assert cited.slots == plain.slots
	assert cited.objects[:-1] == plain.objects
	citation = cited.objects[-1]
	assert citation.rectangle.y >= max(slot.rectangle.y + slot.rectangle.height for slot in plain.slots)
	runs = [run for paragraph in citation.content.paragraphs for run in paragraph.inlines
		if isinstance(run, slide_lib.layout_content.TextRun)]
	assert all(run.style.font_family == "IBM Plex Sans Condensed" for run in runs)
	assert any(run.style.italic for run in runs)
	assert any(run.style.link_url == url for run in runs)


#============================================


#============================================
@pytest.mark.parametrize("content", ("- A list", "![Image](missing.png)", "$x$"))
def test_citation_rejects_nonprose_before_export(tmp_path: pathlib.Path, content: str) -> None:
	with pytest.raises(ValueError, match="@citation"):
		layout_test_helpers.compile_source(tmp_path, "=== layout: one-panel\n\n@body\n\nContent.\n\n@citation\n\n" + content)


#============================================


#============================================
