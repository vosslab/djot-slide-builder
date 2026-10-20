"""Offline contracts for compiler-owned equation placement and ODP packaging."""

import pathlib
import zipfile
import xml.etree.ElementTree

import pytest

import slide_lib.djot_parser
import slide_lib.layout_engine
import slide_lib.math_render
import slide_lib.native_model
import slide_lib.odp_export
import slide_lib.presentation_theme


#============================================
def measured_equations(requests: dict[tuple[str, bool], slide_lib.native_model.SourceLocation]
		) -> dict[tuple[str, bool], slide_lib.math_render.RenderedMath]:
	"""Supply known math geometry so layout tests need neither Node nor LibreOffice."""
	svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="48px" height="48px" '
		'viewBox="0 0 48 48"><path fill="currentColor" d="M0 0h48v48H0z"/></svg>')
	return {key: slide_lib.math_render.RenderedMath(svg, 3, 2, 1) for key in requests}


#============================================
def test_equation_bullets_keep_native_prose_and_reveals(
		tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
	"""Equation bullets stack with intact native paragraphs and preserve reveals."""
	monkeypatch.setattr(slide_lib.math_render, "render_equations", measured_equations)
	path = tmp_path / "inline.djot"
	path.write_text("=== layout: one-panel\n# Example\n@body\n"
		"=> cascade appear\n- A complete native prose paragraph.\n- $x$\n"
		"=== layout: one-panel\n# Display\n@body\n$$x$$\n", encoding="utf-8")
	theme = slide_lib.presentation_theme.default_theme()
	plan = slide_lib.layout_engine.compile_layout_deck(slide_lib.djot_parser.parse_deck(path), theme).plan
	output = slide_lib.odp_export.write_odp(plan, theme, tmp_path / "inline.odp")
	with zipfile.ZipFile(output) as archive:
		root = xml.etree.ElementTree.fromstring(archive.read("content.xml"))
		images = root.findall(f".//{{{slide_lib.odp_export.DRAW_NS}}}image")
		assert len(images) == 2
		paragraphs = root.findall(f".//{{{slide_lib.odp_export.TEXT_NS}}}p")
		assert any("".join(paragraph.itertext()) == "A complete native prose paragraph."
			for paragraph in paragraphs)
		for image in images:
			member = image.attrib[f"{{{slide_lib.odp_export.XLINK_NS}}}href"]
			assert member.endswith(".svg") and archive.read(member).startswith(b"<svg")
		ids = {element.get(f"{{{slide_lib.odp_export.XML_NS}}}id") for element in root.iter()}
		targets = [value for element in root.iter() for name, value in element.attrib.items()
			if name.endswith("}targetElement")]
		assert targets and all(target in ids for target in targets)


#============================================
@pytest.mark.parametrize("body", [
	"Before $x$ after.", "- Before $x$",
])
def test_mixed_math_reports_source_location(
		tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, body: str) -> None:
	"""Reject unsupported authoring with a useful location, rather than fragile output."""
	monkeypatch.setattr(slide_lib.math_render, "render_equations", measured_equations)
	path = tmp_path / "mixed.djot"
	path.write_text("=== layout: one-panel\n# Example\n@body\n" + body + "\n")
	with pytest.raises(ValueError, match=r"mixed.djot:\d+: mixed text and math"):
		slide_lib.layout_engine.compile_layout_deck(slide_lib.djot_parser.parse_deck(path),
			slide_lib.presentation_theme.default_theme())
