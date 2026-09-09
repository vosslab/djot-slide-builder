"""Declarative Djot layout vocabulary and native-editor interoperability facts."""

import slide_lib.layout_primitives


#============================================
def _contract(name: str, slots: tuple[str, ...] = (), *, root: bool = False,
		title: bool = False, subtitle: bool = False, matchable: bool = False,
		libreoffice: slide_lib.layout_primitives.LibreOfficeAutoLayout | None = None,
		placeholders: tuple[tuple[slide_lib.layout_primitives.LibreOfficePlaceholderObject,
			str], ...] = ()) -> slide_lib.layout_primitives.LayoutContract:
	"""Create one concise immutable registry entry."""
	result = slide_lib.layout_primitives.LayoutContract(
		name=name, slot_names=slots, allows_root_body=root, allows_title=title,
		allows_subtitle=subtitle, topology_matchable=matchable,
		topology_slots=_topology(name) if matchable else (),
		libreoffice_autolayout=libreoffice,
		libreoffice_placeholder_members=placeholders,
	)
	return result


#============================================
def _topology(name: str) -> tuple[tuple[float, float, float, float, float, float], ...]:
	"""Store importer-facing normalized slots as data derived from stable layout geometry."""
	# Rectangle tuples use normalized x, y, width, and height values. The returned
	# tuples append centers for stable topology matching without adapter geometry.
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
		rectangles = (
			(0, 0, .482, .48), (.518, 0, .482, .48),
			(0, .52, .482, .48), (.518, .52, .482, .48),
		)
	elif name == "six-panels":
		rectangles = (
			(0, 0, .31, .48), (.345, 0, .31, .48), (.69, 0, .31, .48),
			(0, .52, .31, .48), (.345, .52, .31, .48), (.69, .52, .31, .48),
		)
	else:
		rectangles = ()
	result = tuple((x, y, width, height, x + width / 2, y + height / 2)
		for x, y, width, height in rectangles)
	return result


LibreOfficeAutoLayout = slide_lib.layout_primitives.LibreOfficeAutoLayout
LibreOfficePlaceholder = slide_lib.layout_primitives.LibreOfficePlaceholderObject


LAYOUT_CONTRACTS = {
	"blank": _contract("blank", libreoffice=LibreOfficeAutoLayout.NONE),
	"title-only": _contract("title-only", root=True, title=True,
		libreoffice=LibreOfficeAutoLayout.TITLE_ONLY,
		placeholders=((LibreOfficePlaceholder.TITLE, "title"),)),
	"title-slide": _contract("title-slide", title=True, subtitle=True,
		libreoffice=LibreOfficeAutoLayout.TITLE,
		placeholders=((LibreOfficePlaceholder.TITLE, "title"),
			(LibreOfficePlaceholder.SUBTITLE, "subtitle"))),
	"one-panel": _contract("one-panel", ("body",), root=True, title=True, matchable=True,
		libreoffice=LibreOfficeAutoLayout.TITLE_CONTENT,
		placeholders=((LibreOfficePlaceholder.TITLE, "title"),
			(LibreOfficePlaceholder.OUTLINE, "body"))),
	"section": _contract("section", title=True, subtitle=True,
		libreoffice=LibreOfficeAutoLayout.ONLY_TEXT,
		placeholders=((LibreOfficePlaceholder.OUTLINE, "title"),)),
	"two-panels": _contract("two-panels", ("left", "right"), title=True, matchable=True,
		libreoffice=LibreOfficeAutoLayout.TITLE_2CONTENT,
		placeholders=((LibreOfficePlaceholder.TITLE, "title"),
			(LibreOfficePlaceholder.OUTLINE, "left"),
			(LibreOfficePlaceholder.OUTLINE, "right"))),
	"one-plus-two-panels": _contract("one-plus-two-panels", ("left", "top-right", "bottom-right"),
		title=True, matchable=True,
		libreoffice=LibreOfficeAutoLayout.TITLE_CONTENT_2CONTENT,
		placeholders=((LibreOfficePlaceholder.TITLE, "title"),
			(LibreOfficePlaceholder.OUTLINE, "left"),
			(LibreOfficePlaceholder.OUTLINE, "top-right"),
			(LibreOfficePlaceholder.OUTLINE, "bottom-right"))),
	"two-plus-one-panels": _contract("two-plus-one-panels", ("top-left", "bottom-left", "right"),
		title=True, matchable=True,
		libreoffice=LibreOfficeAutoLayout.TITLE_2CONTENT_CONTENT,
		placeholders=((LibreOfficePlaceholder.TITLE, "title"),
			(LibreOfficePlaceholder.OBJECT, "top-left"),
			(LibreOfficePlaceholder.OBJECT, "bottom-left"),
			(LibreOfficePlaceholder.OUTLINE, "right"))),
	"stacked-panels": _contract("stacked-panels", ("top", "bottom"), title=True,
		matchable=True,
		libreoffice=LibreOfficeAutoLayout.TITLE_CONTENT_OVER_CONTENT,
		placeholders=((LibreOfficePlaceholder.TITLE, "title"),
			(LibreOfficePlaceholder.OBJECT, "top"),
			(LibreOfficePlaceholder.OUTLINE, "bottom"))),
	"two-over-one-panels": _contract("two-over-one-panels", ("top-left", "top-right", "bottom"),
		title=True, matchable=True,
		libreoffice=LibreOfficeAutoLayout.TITLE_2CONTENT_OVER_CONTENT,
		placeholders=((LibreOfficePlaceholder.TITLE, "title"),
			(LibreOfficePlaceholder.OBJECT, "top-left"),
			(LibreOfficePlaceholder.OBJECT, "top-right"),
			(LibreOfficePlaceholder.OUTLINE, "bottom"))),
	"four-panels": _contract("four-panels", ("top-left", "top-right", "bottom-left", "bottom-right"),
		title=True, matchable=True,
		libreoffice=LibreOfficeAutoLayout.TITLE_4CONTENT,
		placeholders=((LibreOfficePlaceholder.TITLE, "title"),
			(LibreOfficePlaceholder.OBJECT, "top-left"),
			(LibreOfficePlaceholder.OUTLINE, "top-right"),
			(LibreOfficePlaceholder.OUTLINE, "bottom-left"),
			(LibreOfficePlaceholder.OUTLINE, "bottom-right"))),
	"six-panels": _contract("six-panels", ("top-left", "top-center", "top-right",
		"bottom-left", "bottom-center", "bottom-right"),
		title=True, matchable=True,
		libreoffice=LibreOfficeAutoLayout.TITLE_6CONTENT,
		placeholders=((LibreOfficePlaceholder.TITLE, "title"),
			(LibreOfficePlaceholder.OUTLINE, "top-left"),
			(LibreOfficePlaceholder.OUTLINE, "top-center"),
			(LibreOfficePlaceholder.OUTLINE, "top-right"),
			(LibreOfficePlaceholder.OUTLINE, "bottom-left"),
			(LibreOfficePlaceholder.OUTLINE, "bottom-center"),
			(LibreOfficePlaceholder.OUTLINE, "bottom-right"))),
	"multiple-choice": _contract("multiple-choice", ("question", "answer")),
	"gallery": _contract("gallery", ("gallery",), title=True),
}


#============================================
def contract_for(name: str) -> slide_lib.layout_primitives.LayoutContract:
	"""Return an exact registered contract and fail loudly for invalid source."""
	result = LAYOUT_CONTRACTS[name]
	return result


#============================================
def names() -> tuple[str, ...]:
	"""Return the stable declaration order used by grammar and tests."""
	result = tuple(LAYOUT_CONTRACTS)
	return result
