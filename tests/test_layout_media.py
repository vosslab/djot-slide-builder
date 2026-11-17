"""Image and question layout contracts for containment, captions, and mixed content."""

import pathlib

import pytest

import layout_test_helpers


def test_prompt_requires_supporting_examples(tmp_path: pathlib.Path) -> None:
	"""An icebreaker cannot silently regress to a question with empty supporting space."""
	with pytest.raises(ValueError, match="visible examples or suggestions"):
		layout_test_helpers.compile_source(tmp_path,
			"=== layout: prompt\n@prompt\nWhat is your sorting rule?\n@examples\n")
