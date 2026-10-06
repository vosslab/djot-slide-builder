"""Read the bounded object-appearance evidence used by ODP import."""

# Standard Library
import dataclasses
import xml.etree.ElementTree

# Local modules
import slide_lib.importers.source_model as source_model
import slide_lib.importers.slide_plan as slide_plan


ANIMATION_NS = "urn:oasis:names:tc:opendocument:xmlns:animation:1.0"
DRAW_NS = "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
SMIL_NS = "urn:oasis:names:tc:opendocument:xmlns:smil-compatible:1.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"


def qname(namespace: str, local_name: str) -> str:
	"""Build one namespace-qualified XML name."""
	return f"{{{namespace}}}{local_name}"


def appear_target_ids(page: xml.etree.ElementTree.Element) -> frozenset[str]:
	"""Return object IDs targeted by a native visibility-appear action."""
	targets = {
		(element.get(qname(SMIL_NS, "targetElement")) or "").removeprefix("#")
		for element in page.findall(f".//{{{ANIMATION_NS}}}set")
		if element.get(qname(SMIL_NS, "attributeName")) == "visibility"
		and element.get(qname(SMIL_NS, "to")) == "visible"
	}
	return frozenset(target for target in targets if target)


def element_appears(element: xml.etree.ElementTree.Element,
		targets: frozenset[str]) -> bool:
	"""Return whether one ODF object carries an imported appear target ID."""
	identities = {
		element.get(qname(DRAW_NS, "id"), ""),
		element.get(qname(XML_NS, "id"), ""),
	}
	return bool(identities & targets)


def read_text_reveals(page: xml.etree.ElementTree.Element,
		texts: list[source_model.PositionedText],
		overlays: list[source_model.PositionedOverlay]) -> tuple[list[source_model.PositionedText], list[str]]:
	"""Retain text appearances and report animation actions we cannot reproduce."""
	paths = {}
	stack = [(page, ())]
	while stack:
		element, path = stack.pop()
		for namespace in (DRAW_NS, XML_NS):
			identity = element.get(qname(namespace, "id"))
			if identity:
				paths[identity] = path
		stack.extend((child, (*path, index)) for index, child in enumerate(element))
	parents = {child: parent for parent in page.iter() for child in parent}
	revealed = set()
	reasons = []
	supported_paths = {text.z_order for text in texts if text.source_kind != "table"}
	supported_paths.update(overlay.z_order for overlay in overlays if overlay.reveal)
	for action in page.iter():
		if not action.tag.startswith(f"{{{ANIMATION_NS}}}"):
			continue
		if action.tag.rsplit("}", 1)[-1] in {"par", "seq"}:
			continue
		target = action.get(qname(SMIL_NS, "targetElement"), "").removeprefix("#")
		path = paths.get(target)
		ancestor = action
		on_click = False
		unsupported_timing = False
		while ancestor in parents:
			on_click |= ancestor.get(qname(SMIL_NS, "begin")) == "next"
			unsupported_timing |= ancestor.get(qname(SMIL_NS, "begin"), "0s") not in {
				"0s", "0", "next"}
			unsupported_timing |= any(ancestor.get(qname(SMIL_NS, name)) is not None
				for name in ("repeatCount", "repeatDur", "end"))
			ancestor = parents[ancestor]
		supported = (action.tag == qname(ANIMATION_NS, "set")
			and action.get(qname(SMIL_NS, "attributeName")) == "visibility"
			and action.get(qname(SMIL_NS, "to")) == "visible"
			and on_click and not unsupported_timing
			and path in supported_paths and path not in revealed)
		if supported:
			revealed.add(path)
		else:
			reasons.append(f"source animation for {target or 'unknown target'} requires review")
	result = [dataclasses.replace(text, reveal=text.z_order in revealed) for text in texts]
	return result, reasons


def plan_text_reveals(plan: slide_plan.SlidePlan,
		texts: tuple[source_model.PositionedText, ...],
		regions: tuple[slide_plan.SourceTextRegion, ...],
		visuals: tuple[slide_plan.SourceImageRegion, ...]) -> tuple[slide_plan.SlidePlan, list[str]]:
	"""Map a single revealed answer onto the existing question/answer layout."""
	revealed = {text.source_ordinal for text in texts if text.reveal}
	if not revealed:
		return plan, []
	if len(revealed) == 1 and len(regions) == 2 and not visuals:
		answer = next(region for region in regions if region.source_ordinal in revealed)
		question = next(region for region in regions if region is not answer)
		question_text = " ".join(run.text for _, runs in question.paragraphs for run in runs)
		answer_text = " ".join(run.text for _, runs in answer.paragraphs for run in runs)
		if ("?" in question_text and answer_text.strip().lower().startswith("answer")
				and 1 <= len(answer.paragraphs) <= 2):
			choice = slide_plan.MultipleChoicePlan(question, answer, None,
				"question with source on-click answer reveal")
			plan = slide_plan.SlidePlan(slide_plan.TitleDecision(None, "answer reveal"), (),
				multiple_choice=choice)
	if (plan.multiple_choice is not None
			and revealed == {plan.multiple_choice.answer.source_ordinal}):
		return plan, []
	return plan, ["source text animation is not preserved by the selected layout"]
