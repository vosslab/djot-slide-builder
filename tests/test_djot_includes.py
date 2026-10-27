"""Protect ordered chapter assembly, actionable errors, and local file boundaries."""

# Standard Library
import pathlib
import unittest.mock

# Third-Party Modules
import pytest
import PIL.Image

# Local Modules
import slide_lib.djot_errors
import slide_lib.djot_lint
import slide_lib.djot_parser
import slide_lib.native_export
import slide_lib.layout_measurement


#============================================
def test_mixed_includes_hide_whole_chapter_and_preserve_locations(tmp_path: pathlib.Path) -> None:
	"""A single include flag hides a chapter without hiding surrounding main-file slides."""
	master = tmp_path / "lecture.djot"
	chapter = tmp_path / "chapter.djot"
	chapter.write_text("=== layout: blank\n=== layout: blank\nhidden: true\n")
	text = ("=== layout: blank\n=== include: chapter.djot\nhidden: true\n"
		"=== layout: blank\n@notes\nStill in the main file.\n")
	master.write_text(text)
	deck = slide_lib.djot_parser.parse_deck(master)
	assert [slide.hidden for slide in deck.slides] == [False, True, True, False]
	assert deck.slides[1].location.path == chapter
	assert deck.slides[-1].location.line == 4
	assert deck.slides[-1].notes == ("Still in the main file.",)
	assert slide_lib.native_export.discover_decks(str(tmp_path), tmp_path) == [master]
	master.write_text(text.replace("hidden: true", "hidden: false"))
	assert [slide.hidden for slide in slide_lib.djot_parser.parse_deck(master).slides] == [
		False, False, True, False]


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
@pytest.mark.parametrize("target", ("../outside.djot", "/outside.djot", "chapter.txt"))
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


#============================================
def test_repository_includes_share_guidance_and_enforce_checkout_boundary(
		tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
	"""Lectures share one evergreen copy while traversal and escaping symlinks fail."""
	root = tmp_path / "repo"
	lecture = root / "genetics" / "LECT08" / "djot"
	shared = root / "genetics" / "evergreen"
	lecture.mkdir(parents=True)
	shared.mkdir(parents=True)
	chapter = shared / "exam.djot"
	chapter.write_text("=== layout: blank\n=== layout: blank\n")
	monkeypatch.setattr("slide_lib.djot_sources.repository_root", lambda path: root)
	master = lecture / "announcements.djot"
	text = "=== include: repo:genetics/evergreen/exam.djot\nhidden: true\n"
	master.write_text(text)
	deck = slide_lib.djot_parser.parse_deck(master)
	assert all(slide.hidden for slide in deck.slides)
	assert all(slide.location.path == chapter for slide in deck.slides)
	master.write_text(text.replace("hidden: true", "hidden: false"))
	assert not any(slide.hidden for slide in slide_lib.djot_parser.parse_deck(master).slides)
	assert slide_lib.native_export.discover_decks(str(root), root) == [master]
	master.write_text("=== include: repo:../outside.djot\n")
	with pytest.raises(slide_lib.djot_errors.DjotParseError, match="without traversal"):
		slide_lib.djot_parser.parse_deck(master)
	outside = tmp_path / "outside.djot"
	outside.write_text("=== layout: blank\n")
	(shared / "escape.djot").symlink_to(outside)
	master.write_text("=== include: repo:genetics/evergreen/escape.djot\n")
	with pytest.raises(slide_lib.djot_errors.DjotParseError, match="inside the repository"):
		slide_lib.djot_parser.parse_deck(master)


#============================================
def test_repository_images_lint_measure_and_package_from_shared_assets(
		tmp_path: pathlib.Path) -> None:
	"""Shared figures must work beyond parsing and cannot escape the checkout via symlinks."""
	root = tmp_path / "repo"
	lecture = root / "genetics" / "LECT08"
	assets = root / "genetics" / "evergreen" / "assets"
	lecture.mkdir(parents=True)
	assets.mkdir(parents=True)
	(root / ".git").mkdir()
	image = assets / "figure.png"
	PIL.Image.new("RGB", (32, 18)).save(image)
	master = lecture / "announcements.djot"
	master.write_text("=== layout: one-panel\n@body\n"
		"![Figure](repo:genetics/evergreen/assets/figure.png)\n")
	problems, _summary = slide_lib.djot_lint.lint_paths([master])
	assert not problems
	deck = slide_lib.djot_parser.parse_deck(master)
	picture = deck.slides[0].cells[0].blocks[0]
	assert slide_lib.layout_measurement.image_size(deck, picture) == (32, 18)
	output = slide_lib.native_export.render_native_odp(deck, tmp_path / "shared.odp")
	assert output.is_file()
	outside = tmp_path / "outside.png"
	image.rename(outside)
	image.symlink_to(outside)
	problems, _summary = slide_lib.djot_lint.lint_paths([master])
	assert "inside the repository" in problems[0].message
