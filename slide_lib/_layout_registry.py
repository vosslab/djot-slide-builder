"""Declarative Djot layout vocabulary owned by the format-neutral compiler."""

import slide_lib.layout_primitives


def _contract(name: str, slots: tuple[str, ...] = (), *, root: bool = False,
		title: bool = False, subtitle: bool = False, vertical_title: bool = False,
		vertical_slots: tuple[str, ...] = (), matchable: bool = False,
		continuation: bool = False, decompose: bool = False) -> slide_lib.layout_primitives.LayoutContract:
	"""Create one concise immutable registry entry."""
	result = slide_lib.layout_primitives.LayoutContract(
		name, slots, root, title, subtitle, vertical_title, vertical_slots, matchable,
		_topology(name) if matchable else (),
		slide_lib.layout_primitives.ContinuationPolicy.ALLOW if continuation else
		(slide_lib.layout_primitives.ContinuationPolicy.DECOMPOSE_TO_ONE_PANEL if decompose else
		 slide_lib.layout_primitives.ContinuationPolicy.FORBID),
	)
	return result


def _topology(name: str) -> tuple[tuple[float, float, float, float, float, float], ...]:
	"""Store importer-facing normalized slots as data derived from stable layout geometry."""
	if name == "one-panel":
		rectangles = ((0, 0, 1, 1),)
	elif name == "two-panels":
		rectangles = ((0, 0, .482, 1), (.518, 0, .482, 1))
	elif name == "one-plus-two-panels":
		rectangles = ((0, 0, .482, 1), (.518, 0, .482, .48), (.518, .52, .482, .48))
	elif name == "two-plus-one-panels":
		rectangles = ((0, 0, .482, .48), (0, .52, .482, .48), (.518, 0, .482, 1))
	elif name == "stacked-panels":
		rectangles = ((0, 0, 1, .48), (0, .52, 1, .48))
	elif name == "two-over-one-panels":
		rectangles = ((0, 0, .482, .48), (.518, 0, .482, .48), (0, .52, 1, .48))
	elif name == "four-panels":
		rectangles = ((0, 0, .482, .48), (.518, 0, .482, .48), (0, .52, .482, .48), (.518, .52, .482, .48))
	elif name == "six-panels":
		rectangles = ((0, 0, .31, .48), (.345, 0, .31, .48), (.69, 0, .31, .48), (0, .52, .31, .48), (.345, .52, .31, .48), (.69, .52, .31, .48))
	else:
		rectangles = ()
	result = tuple((x, y, width, height, x + width / 2, y + height / 2)
		for x, y, width, height in rectangles)
	return result


LAYOUT_CONTRACTS = {
	"blank": _contract("blank"),
	"title-only": _contract("title-only", title=True),
	"title-slide": _contract("title-slide", title=True, subtitle=True),
	"one-panel": _contract("one-panel", ("body",), root=True, title=True, matchable=True, continuation=True),
	"centered-text": _contract("centered-text", title=True, subtitle=True),
	"two-panels": _contract("two-panels", ("left", "right"), title=True, matchable=True, decompose=True),
	"one-plus-two-panels": _contract("one-plus-two-panels", ("left", "top-right", "bottom-right"), title=True, matchable=True, decompose=True),
	"two-plus-one-panels": _contract("two-plus-one-panels", ("top-left", "bottom-left", "right"), title=True, matchable=True, decompose=True),
	"stacked-panels": _contract("stacked-panels", ("top", "bottom"), title=True, matchable=True, decompose=True),
	"two-over-one-panels": _contract("two-over-one-panels", ("top-left", "top-right", "bottom"), title=True, matchable=True, decompose=True),
	"four-panels": _contract("four-panels", ("top-left", "top-right", "bottom-left", "bottom-right"), title=True, matchable=True, decompose=True),
	"six-panels": _contract("six-panels", ("top-left", "top-center", "top-right", "bottom-left", "bottom-center", "bottom-right"), title=True, matchable=True, decompose=True),
	"vertical-panel": _contract("vertical-panel", ("body",), root=True, title=True, vertical_title=True, vertical_slots=("body",)),
	"vertical-title-two-panels": _contract("vertical-title-two-panels", ("text", "chart"), title=True, vertical_title=True),
	"vertical-text-panel": _contract("vertical-text-panel", ("body",), root=True, title=True, vertical_slots=("body",)),
	"two-panels-vertical-clipart": _contract("two-panels-vertical-clipart", ("top-left", "bottom-left", "right-clipart"), title=True, vertical_slots=("right-clipart",)),
	"multiple-choice": _contract("multiple-choice", ("question", "answer")),
	"gallery": _contract("gallery", ("gallery",), title=True),
}


def contract_for(name: str) -> slide_lib.layout_primitives.LayoutContract:
	"""Return an exact registered contract and fail loudly for invalid source."""
	result = LAYOUT_CONTRACTS[name]
	return result


def names() -> tuple[str, ...]:
	"""Return the stable declaration order used by grammar and tests."""
	result = tuple(LAYOUT_CONTRACTS)
	return result
