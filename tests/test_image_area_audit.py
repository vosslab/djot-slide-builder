"""Image-area warnings measure displayed artwork without changing authored layouts."""

import pathlib

import PIL.Image
import pytest

import slide_lib.djot_parser
import slide_lib.image_area_audit
import slide_lib.layout_engine
import slide_lib.odp_export
import slide_lib.presentation_theme


def test_audit_flags_shrinking_image_and_leaves_source_untouched(tmp_path: pathlib.Path) -> None:
	"""A text-heavy conversion warns while identical layouts retain full image area."""
	asset = tmp_path / "figure.png"
	image = PIL.Image.new("RGB", (600, 400), "white")
	image.paste("red", (30, 20, 570, 380))
	image.save(asset)
	source = tmp_path / "source.djot"
	source.write_text("=== layout: big-image\n\n@image\n\n![Figure](figure.png)\n\n"
		"@caption\n\nOriginal figure.\n")
	theme = slide_lib.presentation_theme.default_theme()
	plan = slide_lib.layout_engine.compile_layout_deck(
		slide_lib.djot_parser.parse_deck(source), theme).plan
	odp = slide_lib.odp_export.write_odp(plan, theme, tmp_path / "source.odp")
	unchanged = slide_lib.image_area_audit.audit(odp, source)[0]
	assert unchanged["relative_loss_percent"] == pytest.approx(0)
	assert not unchanged["warning"]
	assert unchanged["empty_margin_fraction"] == pytest.approx(0.19)
	converted = tmp_path / "converted.djot"
	converted.write_text("=== layout: one-panel\n\n@body\n\n![Figure](figure.png)\n\n"
		"- Wild-type flies have red eyes on the left.\n"
		"- Morgan discovered a mutant male with white eyes on the right.\n"
		"- This variation made it possible to trace eye color to a specific chromosome.\n")
	before = (asset.read_bytes(), converted.read_bytes())
	changed = slide_lib.image_area_audit.audit(odp, converted)[0]
	assert changed["warning"]
	assert changed["relative_loss_percent"] > 30
	assert changed["target_slide_percent"] < changed["source_slide_percent"]
	assert (asset.read_bytes(), converted.read_bytes()) == before
	assert not slide_lib.image_area_audit.audit(odp, converted, 100)[0]["warning"]
