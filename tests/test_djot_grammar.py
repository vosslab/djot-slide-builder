"""Durable contracts for the small, registry-derived Djot grammar."""

# Third-Party Modules
import pytest

# Local Modules
import slide_lib.djot_grammar
import slide_lib.layouts
import slide_lib.native_model


#============================================
@pytest.mark.parametrize(("pattern", "source", "group", "value"), (
	(slide_lib.djot_grammar.LAYOUT_DIRECTIVE_PATTERN, "=== layout: one-panel", "layout", "one-panel"),
	(slide_lib.djot_grammar.SLOT_DIRECTIVE_PATTERN, "@body", "slot", "body"),
	(slide_lib.djot_grammar.PREFIX_ACTION_PATTERN, "=> cascade appear", "action", "cascade appear"),
	(slide_lib.djot_grammar.TERMINAL_ACTION_PATTERN, "<= appear", "action", "appear"),
))
def test_directive_patterns_accept_only_whole_supported_lines(pattern: object, source: str,
		group: str, value: str) -> None:
	"""Every directive recognizer exposes its authored value from a full line."""
	match = pattern.fullmatch(source)  # type: ignore[union-attr]
	assert match is not None and match.group(group) == value


#============================================
@pytest.mark.parametrize(("pattern", "source"), (
	(slide_lib.djot_grammar.LAYOUT_DIRECTIVE_PATTERN, " === layout: one-panel"),
	(slide_lib.djot_grammar.SLOT_DIRECTIVE_PATTERN, "@body prose"),
	(slide_lib.djot_grammar.PREFIX_ACTION_PATTERN, "=> appear "),
	(slide_lib.djot_grammar.TERMINAL_ACTION_PATTERN, "<= appear "),
))
def test_directive_patterns_reject_near_matches(pattern: object, source: str) -> None:
	"""Whitespace and trailing prose never become directives by accident."""
	assert pattern.fullmatch(source) is None  # type: ignore[union-attr]


#============================================
def test_grammar_derives_layout_and_slot_names_from_registry() -> None:
	"""Grammar catalog remains an API projection of the layout owner."""
	layout_name = next(name for name, spec in slide_lib.layouts.LAYOUTS.items() if spec.slot_names)
	assert (layout_name in slide_lib.djot_grammar.legal_layout_names() and
		slide_lib.djot_grammar.legal_slot_names(layout_name) == slide_lib.layouts.LAYOUTS[layout_name].slot_names)


#============================================
def test_text_projection_decodes_author_visible_entities() -> None:
	"""Author-visible Djot text is projected into the text that will be shown."""
	assert slide_lib.djot_grammar.project_text("5&prime;") == "5\u2032"
