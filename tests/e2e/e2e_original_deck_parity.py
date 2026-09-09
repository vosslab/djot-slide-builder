#!/usr/bin/env python3
"""Confirm each authored Djot deck keeps its recorded visible teaching sequence."""

# Standard Library
import json
import pathlib

# Local Modules
import slide_lib.native_export


#============================================
def repository_root() -> pathlib.Path:
	"""Return the repository root containing this E2E runner."""
	result = pathlib.Path(__file__).resolve().parents[2]
	return result


#============================================
def require(condition: bool, message: str) -> None:
	"""Raise a focused E2E failure when a durable migration fact differs."""
	if not condition:
		raise RuntimeError(message)


#============================================
def original_deck_facts(root: pathlib.Path) -> dict[str, object]:
	"""Load the committed source-independent visible-page migration baseline."""
	path = root / "tests" / "original_deck_facts.json"
	with path.open(encoding="utf-8") as facts_file:
		result = json.load(facts_file)
	return result


#============================================
def compiled_page_count(deck_path: pathlib.Path) -> int:
	"""Compile one Djot deck and return its one-to-one native slide count."""
	source = slide_lib.native_export.parse_deck(deck_path)
	compilation, _theme = slide_lib.native_export.compile_deck(source)
	result = len(compilation.plan.slides)
	return result


#============================================
def run() -> None:
	"""Compare each durable original visible count with its authored Djot plan."""
	root = repository_root()
	facts = original_deck_facts(root)
	for deck in facts["decks"]:
		deck_name = deck["deck"]
		deck_path = root / "genetics" / "djot" / f"{deck_name}.djot"
		actual_count = compiled_page_count(deck_path)
		expected_count = deck["visible_page_count"]
		require(actual_count == expected_count,
			f"{deck_name}: compiled {actual_count} Djot slides, expected {expected_count} visible source pages")
	print("PASS: every Djot deck retains its committed visible original-page count")


if __name__ == "__main__":
	run()
