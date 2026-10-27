"""Protect advisory typography detection without making lecture wording a test gate."""

import dataclasses
import json
from unittest import mock

import slide_lib.cli
import slide_lib.djot_audit
import slide_lib.layout_measurement
import slide_lib.native_export
import slide_lib.native_model
import slide_lib.presentation_theme


def test_typography_distinguishes_runts_from_short_single_line_paragraphs():
	"""A lone word is fine alone; a short wrapped tail needs review."""
	check = slide_lib.djot_audit.typography_issue
	assert check([("Genes", 40)]) is None
	assert check([("Many genes", 100), ("assort", 70)]) == "runt"
	assert check([("Many independently assorting genes", 300), ("in cells", 40)]) == "runt"
	assert check([("Many genes", 100), ("in cells", 80)]) is None
	assert check([("Many genes", 100), ("in cells", 80)], title=True) == "title-wrap"


def test_audit_shares_compiler_wrapping_for_styled_bullets(tmp_path):
	"""Styled text and bullet indentation must use the compiler's line calculation."""
	path = tmp_path / "deck.djot"
	path.write_text("=== layout: two-panels\n\n# Genes\n\n@left\n\n- "
		+ "Many *linked genes* assort in chromosomes. " * 4
		+ "\n\n@right\n\nOther genes.\n", encoding="utf-8")
	deck = slide_lib.native_export.parse_deck(path)
	compilation, theme = slide_lib.native_export.compile_deck(deck)
	session = slide_lib.layout_measurement.MeasurementSession(theme)
	item = next(item for item in compilation.plan.slides[0].objects if item.slot_id == "left")
	paragraph = item.content.paragraphs[0]
	lines = slide_lib.djot_audit.paragraph_lines(paragraph, item.rectangle.width, session)
	inlines = (slide_lib.native_model.Text("Many "),
		slide_lib.native_model.Strong((slide_lib.native_model.Text("linked genes"),)),
		slide_lib.native_model.Text(" assort in chromosomes. ")) * 4
	metrics = session.paragraph_metrics(inlines, paragraph.typography.selected_size_pt,
		item.rectangle.width, list_item=True)
	assert len(lines) > 1
	assert len(lines) == metrics[2]
	assert " ".join(" ".join(text for text, _width in lines).split()) == (
		" ".join(slide_lib.layout_measurement.visible_text(inlines).split()))


def test_audit_cli_reports_source_and_keeps_warnings_advisory(tmp_path, capsys):
	"""A wrapping title is reported without changing source or failing the command."""
	path = tmp_path / "deck.djot"
	source = "=== layout: one-panel\n\n# " + "Linked genes and chromosomes " * 5
	source += "\n\n@body\n\nGenes.\n\n=== layout: one-panel\nhidden: true\n\n# "
	source += "Linked genes and chromosomes " * 5 + "\n\n@body\n\nGenes.\n"
	path.write_text(source, encoding="utf-8")
	with mock.patch.object(slide_lib.native_export, "find_repo_root", return_value=tmp_path):
		assert slide_lib.cli.main(["audit", str(path)]) == 0
	report = json.loads(capsys.readouterr().out)
	assert report["skipped"]["hidden-slides"] == 1
	finding = next(item for item in report["findings"] if item["check"] == "title-wrap")
	assert (finding["slide"], finding["source_line"]) == (1, 3)
	assert finding["file"] == str(path)
	assert len(finding["lines"]) > 1
	assert path.read_text(encoding="utf-8") == source


def test_fractional_font_sizes_do_not_collapse_to_one_measured_width():
	"""Nearby selected sizes must retain distinct advances near wrap boundaries."""
	theme = slide_lib.presentation_theme.default_theme()
	session = slide_lib.layout_measurement.MeasurementSession(theme)
	family = slide_lib.presentation_theme.ORDINARY_FONT_FAMILY
	small = slide_lib.layout_measurement.logical_points(32.1, theme)
	large = slide_lib.layout_measurement.logical_points(32.4, theme)
	assert session.advance(family, False, False, small, "Chromosomes") < (
		session.advance(family, False, False, large, "Chromosomes"))


def test_wrapping_uses_existing_hyphens_but_preserves_nonbreaking_hyphens():
	"""Native break opportunities must not invent hyphens or lose source characters."""
	theme = slide_lib.presentation_theme.default_theme()
	session = slide_lib.layout_measurement.MeasurementSession(theme)
	family = slide_lib.presentation_theme.ORDINARY_FONT_FAMILY
	for separator in ("-", "\u2010", "\u2013", "\u2011"):
		text = f"genes non{separator}recombinant"
		width = session.advance(family, False, False, 28, f"genes non{separator}") + 1
		lines, _widths = session.wrap_tokens(((text, family, False, False, False),), 28, width)
		first = "".join(token[0] for token in lines[0]).rstrip()
		assert first == ("genes" if separator == "\u2011" else f"genes non{separator}")


def test_unfit_url_stops_at_floor_and_reports_without_losing_destination(tmp_path):
	"""An excessive URL remains intact at 12 pt and produces an actionable warning."""
	url = "https://example.test/" + "long-path/" * 20
	path = tmp_path / "deck.djot"
	path.write_text(f"=== layout: two-panels\n\n@left\n\n[{url}]({url})\n\n@right\n\nGenes.\n")
	with mock.patch.object(slide_lib.native_export, "find_repo_root", return_value=tmp_path):
		report = slide_lib.djot_audit.audit(str(path))
	finding = next(item for item in report["findings"] if item["check"] == "url-too-wide")
	assert finding["font_size_pt"] == 12
	assert finding["text"] == url


def test_final_runt_exemption_requires_maximum_body_size(tmp_path):
	"""Only a final paragraph at the theme ceiling is exempt, not earlier runts."""
	path = tmp_path / "deck.djot"
	text = "You can genetically modify one animal. What would you change?"
	path.write_text(f"=== layout: one-panel\n\n# Genes\n\n@body\n\n- {text}\n- {text}\n")
	deck = slide_lib.native_export.parse_deck(path)
	# Keep this detector test focused on uncorrected output.
	with mock.patch.object(slide_lib.layout_measurement.MeasurementSession, "balance_tail"):
		compilation, theme = slide_lib.native_export.compile_deck(deck)
	for ceiling, expected in ((theme.ordinary_body_size_pt, [1]),
			(theme.ordinary_body_size_pt + 1, [1, 2])):
		with mock.patch.object(slide_lib.native_export, "find_repo_root", return_value=tmp_path), \
				mock.patch.object(slide_lib.native_export, "compile_deck", return_value=(
					compilation, dataclasses.replace(theme, ordinary_body_size_pt=ceiling))):
			report = slide_lib.djot_audit.audit(str(path))
		assert [finding["paragraph"] for finding in report["findings"]
			if finding["check"] == "runt"] == expected
