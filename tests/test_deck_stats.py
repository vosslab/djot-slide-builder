"""Exercise visible-slide and authored-visual reporting through the public CLI."""

# Standard Library
import json
import pathlib

# Third-Party Modules
import pytest

# Local Modules
import slide_lib.cli


#============================================
def write_deck(tmp_path: pathlib.Path) -> pathlib.Path:
	"""Create one included deck spanning every statistics denominator."""
	chapter = tmp_path / "hidden.djot"
	chapter.write_text("""=== layout: two-panels

@left

![Hidden image](assets/hidden.jpg)

@right

This chapter is hidden by its include.
""", encoding="utf-8")
	deck = tmp_path / "deck.djot"
	deck.write_text("""=== layout: title-slide

# Start

=== layout: section

# Main section

=== layout: subsection

# Topic

=== layout: one-panel

# Native table

@body

| Source | Count |
| --- | --- |
| A | 1 |

=== layout: one-panel

# Display equation

@body

$$x^2=4$$

=== layout: two-panels

# Image with speaker notes

@left

![Visible image](assets/visible.jpg)

@speaker-notes

Do not count speaker notes as slide content.

@right

Text beside the image.

=== layout: gallery

# Gallery

@gallery

![First gallery image](assets/first.jpg)

![Second gallery image](assets/second.jpg)

=== layout: bookend

# Questions

@body

- Discuss the result.

=== layout: blank

=== layout: theend

# THE END

=== include: hidden.djot
hidden: true
""", encoding="utf-8")
	return deck


#============================================
def test_stats_json_counts_visuals_and_denominators(tmp_path: pathlib.Path,
		capsys: pytest.CaptureFixture[str]) -> None:
	"""Images, native tables, equations, and structural layouts stay distinguishable."""
	deck = write_deck(tmp_path)
	assert slide_lib.cli.main(["stats", str(deck), "--json"]) == 0
	report = json.loads(capsys.readouterr().out)
	assert report["authored_slides"] == 11
	assert report["hidden_slides"] == 1
	assert report["image_placements"] == 3
	expected_all_visible = {
		"slides": 10, "image_slides": 2, "table_slides": 1, "display_math_slides": 1,
		"visual_slides": 4, "no_visual_slides": 6, "text_only_slides": 5,
		"image_percent": 20.0, "visual_percent": 40.0,
	}
	all_visible = report["groups"]["all_visible"]
	assert {name: all_visible[name] for name in expected_all_visible} == expected_all_visible
	assert all_visible["text_only_percent"] == 50.0
	panels = report["groups"]["panel_layouts"]
	assert panels["slides"] == panels["visual_slides"] == 3
	assert panels["image_slides"] == 1
	expected_content = {
		"slides": 5, "image_slides": 2, "table_slides": 1, "display_math_slides": 1,
		"visual_slides": 4, "no_visual_slides": 1, "text_only_slides": 1,
		"image_percent": 40.0, "visual_percent": 80.0,
	}
	content = report["groups"]["content"]
	assert {name: content[name] for name in expected_content} == expected_content
	assert report["groups"]["content_without_bookends"]["visual_percent"] == 100.0
	assert report["groups"]["dedicated_image_layouts"]["slides"] == 1
	assert report["layouts"]["gallery"]["image_slides"] == 1
	assert report["layouts"]["gallery"]["visual_slides"] == 1


#============================================
def test_stats_text_report_marks_empty_image_group_as_not_applicable(
		tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]) -> None:
	"""A deck without dedicated image layouts reports an undefined percentage plainly."""
	deck = tmp_path / "text-only.djot"
	deck.write_text("""=== layout: one-panel

# Text only

@body

One statement.
""", encoding="utf-8")
	assert slide_lib.cli.main(["stats", str(deck), "--json"]) == 0
	report = json.loads(capsys.readouterr().out)
	assert report["groups"]["panel_layouts"]["text_only_percent"] == 100.0
	dedicated = report["groups"]["dedicated_image_layouts"]
	assert dedicated["slides"] == 0
	assert dedicated["image_percent"] is None
	assert dedicated["visual_percent"] is None
	assert dedicated["text_only_percent"] is None
	assert slide_lib.cli.main(["stats", str(deck)]) == 0
	output = capsys.readouterr().out
	assert "All visible slides" in output
	assert "Dedicated image layouts" in output
	assert "n/a" in output
