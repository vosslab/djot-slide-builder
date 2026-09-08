"""Fast behavioral coverage for the repository-owned Djot front end."""

# Standard Library
import pathlib

# Third-Party Modules
import pytest

# Local Modules
import slide_lib.djot_blocks
import slide_lib.djot_errors
import slide_lib.djot_parser
import slide_lib.native_model


#============================================
def parse_source(tmp_path: pathlib.Path, source: str) -> slide_lib.native_model.Deck:
	"""Write inline source to the temporary deck path and parse it."""
	path = tmp_path / "deck.djot"
	path.write_text(source, encoding="utf-8")
	deck = slide_lib.djot_parser.parse_deck(path)
	return deck


#============================================
def parse_error(tmp_path: pathlib.Path, source: str) -> str:
	"""Return the actionable error text for one inline invalid deck."""
	with pytest.raises(slide_lib.djot_errors.DjotParseError) as raised:
		parse_source(tmp_path, source)
	message = str(raised.value)
	return message


#============================================
def test_parse_deck_binds_global_headings_and_named_cells(tmp_path: pathlib.Path) -> None:
	"""A canonical source deck keeps title material global and slots named."""
	deck = parse_source(tmp_path, "=== layout: one-panel\n# Genetics\n@body\nVisible text\n")
	assert deck.title == "Genetics" and deck.slides[0].cells[0].name == "body"


#============================================
def test_parse_deck_retains_multiple_subtitles_in_one_global_region(tmp_path: pathlib.Path) -> None:
	"""Title-slide subtitle text survives global-region assembly."""
	deck = parse_source(tmp_path, "=== layout: title-slide\n# Genetics\n## Week one\n## Open notes\n")
	subtitle_text = "\n".join(block.inlines[0].value for block in deck.slides[0].blocks
		if isinstance(block, slide_lib.native_model.Heading) and block.level == 2)
	assert "Week one" in subtitle_text and "Open notes" in subtitle_text


#============================================
@pytest.mark.parametrize(("directive", "effect", "sequence"), (
	("=> appear", slide_lib.native_model.RevealEffect.APPEAR, slide_lib.native_model.RevealSequence.OBJECT),
	("<= appear", slide_lib.native_model.RevealEffect.APPEAR, slide_lib.native_model.RevealSequence.OBJECT),
))
def test_actions_attach_typed_reveals_to_neighboring_blocks(tmp_path: pathlib.Path, directive: str,
		effect: slide_lib.native_model.RevealEffect, sequence: slide_lib.native_model.RevealSequence) -> None:
	"""Both action positions preserve the typed effect and reveal unit."""
	if directive.startswith("=>"):
		source = f"=== layout: one-panel\n@body\n{directive}\nVisible text\n"
	else:
		source = f"=== layout: one-panel\n@body\nVisible text\n{directive}\n"
	deck = parse_source(tmp_path, source)
	reveal = deck.slides[0].cells[0].blocks[0].reveal
	assert reveal is not None and (reveal.effect, reveal.sequence) == (effect, sequence)


#============================================
def test_prefix_cascade_attaches_to_a_list_block(tmp_path: pathlib.Path) -> None:
	"""Cascade reveal intent stays on the editable list it advances through."""
	deck = parse_source(tmp_path, "=== layout: one-panel\n@body\n=> cascade appear\n- Parent\n\n  - Child\n- Second\n")
	reveal = deck.slides[0].cells[0].blocks[0].reveal
	assert reveal is not None and reveal.sequence is slide_lib.native_model.RevealSequence.PARAGRAPHS


#============================================
def test_terminal_action_targets_deepest_final_list_item(tmp_path: pathlib.Path) -> None:
	"""A list action reveals the last logical child rather than its outer list."""
	deck = parse_source(tmp_path, "=== layout: one-panel\n@body\n- Parent\n\n  - Child\n<= appear\n")
	child = deck.slides[0].cells[0].blocks[0].items[0].children[0].items[0]
	assert child.reveal is not None and child.reveal.sequence is slide_lib.native_model.RevealSequence.OBJECT


#============================================
def test_multiple_choice_adds_implicit_answer_reveal(tmp_path: pathlib.Path) -> None:
	"""One popup reveal covers one or two editable answer paragraphs."""
	deck = parse_source(tmp_path, "=== layout: multiple-choice\n@question\n- A\n- B\n@answer\nB\n\nBecause DNA stores hereditary information.\n")
	answer_blocks = deck.slides[0].cells[1].blocks
	assert (answer_blocks[0].reveal == slide_lib.native_model.Reveal(
		slide_lib.native_model.RevealEffect.APPEAR, slide_lib.native_model.RevealSequence.OBJECT) and
		answer_blocks[1].reveal is None)


#============================================
@pytest.mark.parametrize(("answer", "line", "phrase"), (
	("\n- Not a paragraph\n", 5, "accepts editable text paragraphs only"),
	("\nOne\n\nTwo\n\nThree\n", 9, "requires one or two editable text paragraphs"),
))
def test_multiple_choice_answer_rejects_outside_popup_contract(tmp_path: pathlib.Path, answer: str,
		line: int, phrase: str) -> None:
	"""The parser reports the specific invalid answer source object."""
	message = parse_error(tmp_path, "=== layout: multiple-choice\n@question\n- A\n@answer" + answer)
	assert f"deck.djot:{line}:" in message and phrase in message


#============================================
@pytest.mark.parametrize(("source", "line", "phrase"), (
	("=== layout: one-panel extra\n", 1, "layout directives must be exact"),
	("=== layout: one-panel\n@body prose\n", 2, "slot directives must be exact"),
	("=== layout: one-panel\n@body\n<= appear\n", 3, "require a preceding block"),
	("=== layout: one-panel\n@body\n=> appear\n=> appear\nText\n", 4, "require a block before"),
	("=== layout: one-panel\n@body\n=> vanish\nText\n", 3, "unknown Djot action"),
	("=== layout: one-panel\n@body\n=> cascade appear\nText\n", 3, "requires a following ListBlock"),
	("=== layout: one-panel\n@body\nText\n<= cascade appear\n", 4, "requires a following ListBlock"),
	("=== layout: one-panel\n@body\n- Item\n<= cascade appear\n", 4, "terminal cascade appear is not supported"),
	("=== layout: unknown\n", 1, "unknown Djot layout"),
	("=== layout: one-panel\n", 1, "missing required slot"),
	("=== layout: one-panel\n@body\nText\n<= blue overlay\n", 4, "not yet supported"),
	("=== layout: multiple-choice\n@question\n- A\n@answer\n=> appear\nA\n", 5, "implicit on-click"),
))
def test_parser_reports_source_located_directive_errors(tmp_path: pathlib.Path, source: str,
		line: int, phrase: str) -> None:
	"""Unsupported or malformed directives name the physical line and reason."""
	message = parse_error(tmp_path, source)
	assert f"deck.djot:{line}:" in message and phrase in message


#============================================
def test_parser_keeps_crlf_source_locations_physical(tmp_path: pathlib.Path) -> None:
	"""CRLF input reports the authored line number rather than normalized offset."""
	message = parse_error(tmp_path, "=== layout: one-panel\r\n@body\r\n<= blue overlay\r\n")
	assert "deck.djot:3:" in message


#============================================
def test_fence_preserves_directive_looking_code_as_code_block(tmp_path: pathlib.Path) -> None:
	"""Directives inside fences remain editable source text, not deck syntax."""
	deck = parse_source(tmp_path, "=== layout: one-panel\n@body\n```text\n=== layout: title-only\n@body\n```\n")
	assert isinstance(deck.slides[0].cells[0].blocks[0], slide_lib.native_model.CodeBlock)


#============================================
def test_ordinary_instruction_like_text_stays_visible(tmp_path: pathlib.Path) -> None:
	"""An ordinary at-sign instruction remains editable body text."""
	deck = parse_source(tmp_path, "=== layout: one-panel\n@body\n@name describes the submitted work\n")
	assert deck.slides[0].cells[0].blocks[0].inlines == (
		slide_lib.native_model.Text("@name describes the submitted work"),)


#============================================
def test_block_subset_preserves_supported_semantics(tmp_path: pathlib.Path) -> None:
	"""Attributes, image, quote, code, table, and math reach their typed nodes."""
	source = ("=== layout: one-panel\n@body\n{.lead #intro}\n![DNA](dna.png)\n\n> Quoted\n\n```py\nx = 1\n```\n\n| H | I |\n| - | - |\n| A | B |\n\n$$x^2$$\n")
	deck = parse_source(tmp_path, source)
	blocks = deck.slides[0].cells[0].blocks
	assert (isinstance(blocks[0], slide_lib.native_model.Image) and blocks[0].attributes[0].name == "class" and
		isinstance(blocks[1], slide_lib.native_model.QuoteBlock) and isinstance(blocks[2], slide_lib.native_model.CodeBlock) and
		isinstance(blocks[3], slide_lib.native_model.Table) and isinstance(blocks[4], slide_lib.native_model.DisplayMath))


#============================================
@pytest.mark.parametrize(("source", "phrase"), (
	("Plain ![DNA](dna.png) prose", "images must be standalone"),
	("| A | B |\n| :-- | --: |", "alignment is not supported"),
))
def test_unsupported_block_forms_fail_instead_of_silently_changing_meaning(tmp_path: pathlib.Path,
		source: str, phrase: str) -> None:
	"""Valid-but-unmapped block semantics stop at the parser boundary."""
	message = parse_error(tmp_path, f"=== layout: one-panel\n@body\n{source}\n")
	assert phrase in message


#============================================
def test_list_boundaries_and_dash_table_rows_remain_distinct(tmp_path: pathlib.Path) -> None:
	"""A list marker does not prevent a following dash row from separating a table header."""
	parsed = slide_lib.djot_blocks.parse_blocks(tmp_path / "blocks.djot",
		"- One\n\n| H | I |\n| - | - |\n| A | B |\n")
	assert isinstance(parsed.blocks[0], slide_lib.native_model.ListBlock)
	assert (isinstance(parsed.blocks[1], slide_lib.native_model.Table) and
		parsed.blocks[1].headers != ())
