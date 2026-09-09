"""Shared extended-Djot directive grammar and layout-derived vocabulary."""

# Standard Library
import re

# Local Modules
import slide_lib.layout_registry
import slide_lib.native_model


# Each pattern accepts one complete physical source line.  Callers pass a line
# without its newline, keeping hard-wrapped prose ordinary Djot content.
LAYOUT_DIRECTIVE_PATTERN = re.compile(r"\A=== layout: (?P<layout>[a-z][a-z0-9-]*)\Z")
SLOT_DIRECTIVE_PATTERN = re.compile(r"\A@(?P<slot>[a-z][a-z0-9-]*)\Z")
PREFIX_ACTION_PATTERN = re.compile(r"\A=> (?P<action>[a-z]+(?: [a-z]+)*)\Z")
TERMINAL_ACTION_PATTERN = re.compile(r"\A<= (?P<action>[a-z]+(?: [a-z]+)*)\Z")


ACTION_REVEALS: dict[str, slide_lib.native_model.Reveal] = {
	"appear": slide_lib.native_model.Reveal(
		slide_lib.native_model.RevealEffect.APPEAR,
		slide_lib.native_model.RevealSequence.OBJECT,
	),
	"cascade appear": slide_lib.native_model.Reveal(
		slide_lib.native_model.RevealEffect.APPEAR,
		slide_lib.native_model.RevealSequence.PARAGRAPHS,
	),
}
DEFERRED_ACTIONS = frozenset({"blue overlay"})
TEXT_PROJECTIONS = {"&prime;": "\u2032"}


#============================================
def legal_layout_names() -> frozenset[str]:
	"""Return the current layout spellings from the authoritative registry."""
	layout_names = frozenset(slide_lib.layout_registry.names())
	return layout_names


#============================================
def legal_slot_names(layout_name: str) -> tuple[str, ...]:
	"""Return the slots declared by one authoritative layout specification."""
	slot_names = slide_lib.layout_registry.contract_for(layout_name).slot_names
	return slot_names


#============================================
def project_text(value: str) -> str:
	"""Project the small normal-text vocabulary after strict-Djot validation."""
	for source, projection in TEXT_PROJECTIONS.items():
		value = value.replace(source, projection)
	return value
