"""Protect ordered chapter assembly, actionable errors, and local file boundaries."""

# Standard Library
import pathlib
import unittest.mock

# Third-Party Modules
import pytest

# Local Modules
import slide_lib.djot_errors
import slide_lib.djot_lint
import slide_lib.djot_parser
import slide_lib.native_export


#============================================
def test_chapters_preserve_order_notes_theme_and_image_base(tmp_path: pathlib.Path) -> None:
	"""Splitting a deck must preserve native slide semantics and its shared asset directory."""
	master = tmp_path / "lecture.djot"
	master.write_text("color-theme: biotechnology\ninclude: second.djot\ninclude: first.djot\n")
	(tmp_path / "first.djot").write_text("=== layout: section\n# Last\n@notes\nKeep this note.\n")
	second = tmp_path / "second.djot"
	second.write_text("=== layout: one-panel\n# First\n@body\n![Photo](assets/photo.png)\n")
	deck = slide_lib.djot_parser.parse_deck(master)
	assert deck.title == "First" and deck.color_theme == "biotechnology"
	assert deck.asset_root == tmp_path and deck.slides[0].location.path == second
	assert deck.slides[1].notes == ("Keep this note.",)
	image = deck.slides[0].cells[0].blocks[0]
	assert image.source == "assets/photo.png" and image.location.line == 4


#============================================
def test_nested_manifest_builds_once_and_lints_every_file(tmp_path: pathlib.Path) -> None:
	"""Folder commands produce one lecture, while native validation reaches every included file."""
	master = tmp_path / "lecture.djot"
	chapter = tmp_path / "chapter.djot"
	part = tmp_path / "part.djot"
	master.write_text("color-theme: biotechnology\ninclude: chapter.djot\n")
	chapter.write_text("include: part.djot\n")
	part.write_text("=== layout: blank\n")
	assert slide_lib.native_export.discover_decks(str(tmp_path), tmp_path) == [master]
	with unittest.mock.patch.object(slide_lib.djot_lint, "native_validator", return_value=None) as run:
		problems, summary = slide_lib.djot_lint.lint_paths([tmp_path], native_executable="jotdown")
	assert problems == [] and summary.slides == 1
	assert {call.args[0] for call in run.call_args_list} == {master, chapter, part}


#============================================
def test_included_errors_point_to_chapter_lines(tmp_path: pathlib.Path) -> None:
	"""Authors must be sent to the actual broken chapter, including missing image diagnostics."""
	master = tmp_path / "lecture.djot"
	chapter = tmp_path / "chapter.djot"
	master.write_text("include: chapter.djot\n")
	chapter.write_text("=== layout: one-panel\n\n@body\n\n![Missing](missing.png)\n")
	problems, _summary = slide_lib.djot_lint.lint_paths([master])
	assert problems[0].path == chapter and problems[0].line == 5
	chapter.write_text("=== layout: one-panel\n\n@wrong\n")
	problems, _summary = slide_lib.djot_lint.lint_paths([master])
	assert problems[0].path == chapter and problems[0].line == 3


#============================================
@pytest.mark.parametrize("target", ("../outside.djot", "/tmp/outside.djot", "chapter.txt"))
def test_includes_reject_nonlocal_or_wrong_format_paths(tmp_path: pathlib.Path, target: str) -> None:
	"""A manifest cannot read arbitrary paths or reinterpret another file type as a chapter."""
	master = tmp_path / "lecture.djot"
	master.write_text(f"include: {target}\n")
	with pytest.raises(slide_lib.djot_errors.DjotParseError, match="relative .djot path"):
		slide_lib.djot_parser.parse_deck(master)


#============================================
def test_symlink_escape_and_missing_include_report_directive(tmp_path: pathlib.Path) -> None:
	"""Containment applies after symlink resolution, and missing files identify the include."""
	folder = tmp_path / "lecture"
	folder.mkdir()
	outside = tmp_path / "outside.djot"
	outside.write_text("=== layout: blank\n")
	master = folder / "master.djot"
	master.write_text("\ninclude: chapter.djot\n")
	with pytest.raises(slide_lib.djot_errors.DjotParseError, match=r"master.djot:2:.*missing"):
		slide_lib.djot_parser.parse_deck(master)
	(folder / "chapter.djot").symlink_to(outside)
	with pytest.raises(slide_lib.djot_errors.DjotParseError, match="inside the master"):
		slide_lib.djot_parser.parse_deck(master)


#============================================
def test_cycles_and_conflicting_themes_fail_clearly(tmp_path: pathlib.Path) -> None:
	"""Cycles cannot vanish during folder discovery and chapter themes cannot silently change."""
	master = tmp_path / "master.djot"
	chapter = tmp_path / "chapter.djot"
	master.write_text("color-theme: biotechnology\ninclude: chapter.djot\n")
	chapter.write_text("color-theme: biotechnology\ninclude: master.djot\n")
	with pytest.raises(slide_lib.native_export.PresentationInputError, match="circular include"):
		slide_lib.native_export.discover_decks(str(tmp_path), tmp_path)
	chapter.write_text("color-theme: genetics\n=== layout: blank\n")
	with pytest.raises(slide_lib.djot_errors.DjotParseError, match=r"chapter.djot:1:.*conflicts"):
		slide_lib.djot_parser.parse_deck(master)


#============================================
def test_include_text_in_notes_is_literal_and_manifests_do_not_mix_slides(tmp_path: pathlib.Path) -> None:
	"""Including a chapter is an explicit master-file operation, never hidden in slide text."""
	path = tmp_path / "lecture.djot"
	path.write_text("=== layout: blank\n@notes\ninclude: missing.djot\n")
	assert slide_lib.djot_parser.parse_deck(path).slides[0].notes == ("include: missing.djot",)
	(tmp_path / "chapter.djot").write_text("=== layout: blank\n")
	path.write_text("include: chapter.djot\n=== layout: blank\n")
	with pytest.raises(slide_lib.djot_errors.DjotParseError, match="manifest lines"):
		slide_lib.djot_parser.parse_deck(path)
