"""Enforce the universal cover contract on standalone tracked Djot decks."""

import pathlib
import re

import pytest

import file_utils
import slide_lib.djot_parser
import slide_lib.djot_sources
import slide_lib.native_model


REPORT_NAME = file_utils.report_name(__file__)
FILES = [str(path) for path in slide_lib.djot_sources.root_sources([
	pathlib.Path(path) for path in file_utils.discover_files(
		extensions=(".djot",), test_key="slide_one")])]
VIOLATIONS_BY_FILE: dict[str, list[str]] = {}
CHAPTER = r"Chapters? [1-9][0-9]*(?:\s*(?:-|,|and)\s*[1-9][0-9]*)*"


def cover_violations(slide: slide_lib.native_model.Slide, announcements: bool) -> list[str]:
	"""Check semantic headings, allowing an omitted or combined chapter line."""
	problems = []
	headings = [block for block in slide.blocks
		if isinstance(block, slide_lib.native_model.Heading)]
	lines = [slide_lib.djot_parser.visible_text(block.inlines).strip() for block in headings]
	if slide.layout_class != "title-slide" or slide.hidden:
		problems.append("Slide 1 must be a visible title-slide.")
	if slide.cells or len(headings) != len(slide.blocks):
		problems.append("Cover content must be headings; move teaching content to slide 2.")
	if not lines or not re.fullmatch(r"Lecture \d+[A-Za-z]\d*", lines[0]):
		problems.append("Put the lecture number and letter in the leading heading.")
	if any("|" in line or "\n" in line for line in lines):
		problems.append("Use separate metadata headings; vertical bars are never acceptable.")
	metadata = lines[1:]
	if len(metadata) not in (3, 4) or any(not line for line in metadata):
		problems.append("Use topic, optional chapter, Dr. Neil Voss, and lecture date; no taglines.")
		return problems
	if metadata[-2] != "Dr. Neil Voss":
		problems.append("The penultimate metadata line must be Dr. Neil Voss.")
	# Check a date-shaped line without coupling historical decks to today's date.
	date_pattern = (r"(?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
		r"Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
		r"\.? \d{1,2}, \d{4}|\d{4}-\d{2}-\d{2})")
	if not re.fullmatch(date_pattern, metadata[-1]):
		problems.append("End the cover with a lecture date including the year.")
	if announcements:
		if len(metadata) != 3 or metadata[0] != "Announcements":
			problems.append("Announcements require topic exactly 'Announcements' and no chapter.")
	elif len(metadata) == 4:
		if not re.fullmatch(CHAPTER, metadata[1]) or metadata[0].startswith("Chapter"):
			problems.append("Use topic then Chapter N (or a chapter range) on separate lines.")
	elif metadata[0].startswith("Chapter") and not re.fullmatch(CHAPTER + r": \S.*", metadata[0]):
		problems.append("A combined chapter/topic line must read Chapter N: Slide Deck Topic.")
	return problems


def check_file(relative_path: str) -> list[str]:
	"""Resolve includes before checking the first slide of an authored deck."""
	path = pathlib.Path(file_utils.get_repo_root()) / relative_path
	deck = slide_lib.djot_parser.parse_deck(path)
	if not deck.slides:
		return ["Deck has no slide 1."]
	first = deck.slides[0]
	is_announcement = "announcements" in path.stem.lower() or any(
		isinstance(block, slide_lib.native_model.Heading)
		and "announcements" in slide_lib.djot_parser.visible_text(block.inlines).lower()
		for block in first.blocks)
	problems = cover_violations(first, is_announcement)
	return [f"{first.location.path}:{first.location.line}: {problem}" for problem in problems]


@pytest.fixture(scope="module", autouse=True)
def collect_report() -> None:
	"""Write one complete repair list before individual deck assertions run."""
	file_utils.clear_stale_reports()
	VIOLATIONS_BY_FILE.clear()
	VIOLATIONS_BY_FILE.update(file_utils.collect_file_violations(FILES, check_file))
	lines = file_utils.format_violation_report("Slide 1 violations:", VIOLATIONS_BY_FILE)
	if lines:
		file_utils.write_report_lines(REPORT_NAME, lines)


@pytest.mark.parametrize("path", FILES, ids=file_utils.rel_id)
def test_slide_one(path: str) -> None:
	"""Every standalone deck follows HG; included teaching chapters are not covers."""
	relative_path = file_utils.rel_to_root(path)
	message = file_utils.format_violation_assert_message(
		relative_path, VIOLATIONS_BY_FILE.get(relative_path, []), REPORT_NAME)
	assert relative_path not in VIOLATIONS_BY_FILE, message


@pytest.mark.parametrize("metadata, announcements, valid", (
	(("Topic", "Dr. Neil Voss", "Oct 20, 2026"), False, True),
	(("Chapter 7: Topic", "Dr. Neil Voss", "Oct 20, 2026"), False, True),
	(("Topic", "Chapter 7", "Dr. Neil Voss", "Oct 20, 2026"), False, True),
	(("Announcements", "Dr. Neil Voss", "Oct 20, 2026"), True, True),
	(("Topic", "Chapter 7 | Dr. Neil Voss", "Oct 20, 2026"), False, False),
	(("Announcements", "Chapter 7", "Dr. Neil Voss", "Oct 20, 2026"), True, False),
	(("Genetics: Announcements", "Dr. Neil Voss", "Oct 20, 2026"), True, False),
	(("Topic", "A tagline", "Dr. Neil Voss", "Oct 20, 2026"), False, False),
))
def test_cover_contract(tmp_path: pathlib.Path, metadata: tuple[str, ...],
		announcements: bool, valid: bool) -> None:
	"""Keep accepted alternatives and the actual formatting regressions explicit."""
	path = tmp_path / "cover.djot"
	path.write_text("=== layout: title-slide\n# Lecture 07A2\n\n" +
		"\n\n".join(f"## {line}" for line in metadata) + "\n", encoding="utf-8")
	slide = slide_lib.djot_parser.parse_deck(path).slides[0]
	assert (not cover_violations(slide, announcements)) == valid
