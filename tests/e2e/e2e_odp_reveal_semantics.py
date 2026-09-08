#!/usr/bin/env python3
"""Interpret the bounded native ODP reveal contract and its LO round trip."""

# Standard Library
import argparse
import copy
import hashlib
import pathlib
import subprocess
import tempfile
import zipfile
from collections.abc import Callable
import xml.etree.ElementTree

# PIP3 modules
import defusedxml.ElementTree


NAMESPACES = {
	"anim": "urn:oasis:names:tc:opendocument:xmlns:animation:1.0",
	"draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
	"office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
	"presentation": "urn:oasis:names:tc:opendocument:xmlns:presentation:1.0",
	"smil": "urn:oasis:names:tc:opendocument:xmlns:smil-compatible:1.0",
	"text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
	"xml": "http://www.w3.org/XML/1998/namespace",
}
SOFFICE = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
EXPECTED_SLIDES = (
	("appear", "object", ("id1",), "Object appear target"),
	("appear", "paragraph", ("id2", "id3"), "Cascade parent"),
	("appear", "object", ("id4",), "Answer: A. Question"),
	("fade", "object", ("id5",), "Object fade target"),
)


#============================================
def qname(namespace: str, name: str) -> str:
	"""Return one expanded QName from the fixed ODF namespace table."""
	result = f"{{{NAMESPACES[namespace]}}}{name}"
	return result


#============================================
def require(condition: bool, message: str) -> None:
	"""Raise one actionable E2E failure when a contract invariant is absent."""
	if not condition:
		raise RuntimeError(message)


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse the one ODP fixture argument."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("fixture", type=pathlib.Path, help="native ODP reveal fixture")
	parser.add_argument("--xml-only", action="store_true",
		help="run the deterministic XML interpreter and negative self-tests only")
	args = parser.parse_args()
	return args


#============================================
def package_pages(path: pathlib.Path) -> list[object]:
	"""Read presentation pages from one ODP package without a UNO bridge."""
	require(path.is_file(), f"fixture does not exist: {path}")
	with zipfile.ZipFile(path) as archive:
		content = archive.read("content.xml")
	root = defusedxml.ElementTree.fromstring(content)
	pages = root.findall("./office:body/office:presentation/draw:page", NAMESPACES)
	require(pages, f"{path.name} has no presentation pages")
	return pages


#============================================
def text_value(element: object) -> str:
	"""Return normalized descendant text for a target element."""
	text = "".join(element.itertext()).strip()
	return text


#============================================
def direct_child_elements(parent: object) -> list[object]:
	"""Return element children in source order."""
	children = list(parent)
	return children


#============================================
def matching_objects(page: object, target_id: str) -> list[object]:
	"""Return native frame targets whose XML and draw identities equal target_id."""
	objects = []
	for element in page.iter():
		# Revealable object targets are native frames, never imported OOXML shapes.
		if element.tag != qname("draw", "frame"):
			continue
		if element.attrib.get(qname("draw", "id")) == target_id and \
			element.attrib.get(qname("xml", "id")) == target_id:
			objects.append(element)
	return objects


#============================================
def matching_paragraphs(page: object, target_id: str) -> list[object]:
	"""Return paragraph targets whose XML and text identities both equal target_id."""
	paragraphs = []
	for element in page.iter(qname("text", "p")):
		if element.attrib.get(qname("xml", "id")) == target_id and \
			element.attrib.get(qname("text", "id")) == target_id:
			paragraphs.append(element)
	return paragraphs


#============================================
def target_kind(page: object, target_id: str) -> tuple[str, object]:
	"""Resolve one target ID through the required paired native identities."""
	objects = matching_objects(page, target_id)
	paragraphs = matching_paragraphs(page, target_id)
	require(len(objects) + len(paragraphs) == 1,
		f"target {target_id!r} must resolve through exactly one paired native identity")
	if objects:
		result = ("object", objects[0])
	else:
		result = ("paragraph", paragraphs[0])
	return result


#============================================
def source_target_ids(page: object) -> list[str]:
	"""Return all paired target IDs in visual source order, rejecting partial IDs."""
	result = []
	for element in page.iter():
		if element.tag in (qname("draw", "frame"), qname("draw", "custom-shape")):
			xml_id = element.attrib.get(qname("xml", "id"))
			draw_id = element.attrib.get(qname("draw", "id"))
			require((xml_id is None) == (draw_id is None),
				"object targets must carry both xml:id and draw:id")
			if xml_id is not None:
				require(xml_id == draw_id, "object xml:id and draw:id must match")
				result.append(xml_id)
		if element.tag == qname("text", "p"):
			xml_id = element.attrib.get(qname("xml", "id"))
			text_id = element.attrib.get(qname("text", "id"))
			require((xml_id is None) == (text_id is None),
				"paragraph targets must carry both xml:id and text:id")
			if xml_id is not None:
				require(xml_id == text_id, "paragraph xml:id and text:id must match")
				result.append(xml_id)
	require(len(result) == len(set(result)), "target IDs must be unique within one slide")
	return result


#============================================
def timing_sequence(page: object, slide_number: int) -> list[object]:
	"""Return direct on-click nodes from the only valid timing-root tree."""
	timing_children = [child for child in direct_child_elements(page)
		if child.tag.startswith(f"{{{NAMESPACES['anim']}}}")]
	roots = [child for child in direct_child_elements(page)
		if child.tag == qname("anim", "par") and
		child.attrib.get(qname("presentation", "node-type")) == "timing-root"]
	require(len(roots) == 1, f"slide {slide_number} must have exactly one timing-root")
	require(timing_children == roots,
		f"slide {slide_number} contains timing nodes outside its timing-root")
	root = roots[0]
	# A timing node nested in content or an effect is still executable ODF/SMIL.
	# Limit the full animation namespace to this one direct timing-root subtree.
	root_subtree = set(root.iter())
	animation_nodes = [node for node in page.iter()
		if node.tag.startswith(f"{{{NAMESPACES['anim']}}}")]
	require(all(node in root_subtree for node in animation_nodes),
		f"slide {slide_number} contains animation nodes outside its timing-root subtree")
	require(set(root.attrib) == {qname("presentation", "node-type")},
		f"slide {slide_number} timing-root has unsupported attributes")
	root_children = direct_child_elements(root)
	require(len(root_children) == 1 and root_children[0].tag == qname("anim", "seq"),
		f"slide {slide_number} timing-root must contain exactly one main sequence")
	sequence = root_children[0]
	require(sequence.attrib.get(qname("presentation", "node-type")) == "main-sequence",
		f"slide {slide_number} timing sequence has the wrong node type")
	require(sequence.attrib.get(qname("smil", "dur")) == "indefinite",
		f"slide {slide_number} main sequence must have indefinite duration")
	require(set(sequence.attrib) == {qname("presentation", "node-type"), qname("smil", "dur")},
		f"slide {slide_number} main sequence has unsupported attributes")
	on_clicks = direct_child_elements(sequence)
	require(on_clicks, f"slide {slide_number} main sequence has no on-click effects")
	for on_click in on_clicks:
		require(on_click.tag == qname("anim", "par"),
			f"slide {slide_number} main sequence contains a non-par node")
		require(on_click.attrib.get(qname("presentation", "node-type")) == "on-click",
			f"slide {slide_number} effect does not use on-click activation")
		require(on_click.attrib.get(qname("smil", "begin")) == "next",
			f"slide {slide_number} on-click must begin next")
		require(on_click.attrib.get(qname("smil", "fill")) == "hold",
			f"slide {slide_number} on-click must hold its revealed state")
		require(set(on_click.attrib) == {qname("presentation", "node-type"),
			qname("smil", "begin"), qname("smil", "fill")},
			f"slide {slide_number} on-click has unsupported attributes")
	return on_clicks


#============================================
def effect_semantics(on_click: object, slide_number: int) -> tuple[str, str]:
	"""Return one bounded effect kind and target, rejecting unsupported children."""
	children = direct_child_elements(on_click)
	require(len(children) == 1, f"slide {slide_number} on-click must have exactly one effect child")
	effect = children[0]
	require(not direct_child_elements(effect),
		f"slide {slide_number} effect nodes must be leaves")
	target_id = effect.attrib.get(qname("smil", "targetElement"))
	require(target_id is not None, f"slide {slide_number} effect has no target")
	require(effect.attrib.get(qname("smil", "fill")) == "hold",
		f"slide {slide_number} effect must hold its final state")
	if effect.tag == qname("anim", "set"):
		require(set(effect.attrib) == {qname("smil", "targetElement"),
			qname("smil", "attributeName"), qname("smil", "to"), qname("smil", "dur"),
			qname("smil", "fill")}, f"slide {slide_number} appear effect has unsupported attributes")
		require(effect.attrib.get(qname("smil", "attributeName")) == "visibility" and
			effect.attrib.get(qname("smil", "to")) == "visible",
			f"slide {slide_number} appear effect must set visibility to visible")
		require(effect.attrib.get(qname("smil", "dur")) == "0.001s",
			f"slide {slide_number} appear effect must use 0.001s duration")
		kind = "appear"
	elif effect.tag == qname("anim", "transitionFilter"):
		require(set(effect.attrib) == {qname("smil", "targetElement"), qname("smil", "type"),
			qname("smil", "subtype"), qname("smil", "dur"), qname("smil", "fill")},
			f"slide {slide_number} fade effect has unsupported attributes")
		require(effect.attrib.get(qname("smil", "type")) == "fade" and
			effect.attrib.get(qname("smil", "subtype")) == "crossfade",
			f"slide {slide_number} fade effect must be a crossfade")
		require(effect.attrib.get(qname("smil", "dur")) == "1s",
			f"slide {slide_number} fade effect must use one second")
		kind = "fade"
	else:
		raise RuntimeError(f"slide {slide_number} uses an unsupported effect node {effect.tag!r}")
	return kind, target_id


#============================================
def require_nested_cascade(page: object, parent: object, second: object) -> None:
	"""Require a genuine child list inside the first root list item."""
	lists = list(page.iter(qname("text", "list")))
	require(len(lists) >= 2, "cascade slide must contain a root and nested list")
	root_list = lists[0]
	root_items = [child for child in direct_child_elements(root_list)
		if child.tag == qname("text", "list-item")]
	require(len(root_items) == 2, "cascade slide must have exactly two root list items")
	first_item = root_items[0]
	second_item = root_items[1]
	require(parent in direct_child_elements(first_item),
		"cascade parent must be a paragraph in the first root list item")
	require(second in direct_child_elements(second_item),
		"cascade second target must be a paragraph in the second root list item")
	nested_lists = [child for child in direct_child_elements(first_item)
		if child.tag == qname("text", "list")]
	require(len(nested_lists) == 1, "first cascade item must own exactly one nested list")
	nested_text = text_value(nested_lists[0])
	require(nested_text == "Cascade child", "nested cascade child text is missing or misplaced")


#============================================
def inspect_slide(page: object, slide_number: int, expectation: tuple) -> list[str]:
	"""Interpret one slide and return its exact source-ordered state descriptions."""
	expected_kind, expected_target_kind, expected_ids, expected_text = expectation
	on_clicks = timing_sequence(page, slide_number)
	effects = [effect_semantics(on_click, slide_number) for on_click in on_clicks]
	target_ids = [target_id for _kind, target_id in effects]
	require(len(target_ids) == len(set(target_ids)), f"slide {slide_number} animates one target twice")
	expected_message = f"slide {slide_number} activation order {target_ids} does not match " + \
		f"source contract {expected_ids}"
	require(tuple(target_ids) == expected_ids, expected_message)
	require(source_target_ids(page) == list(expected_ids),
		f"slide {slide_number} paired target source order is not {list(expected_ids)}")
	states = []
	resolved = []
	for click_number, (kind, target_id) in enumerate(effects, start=1):
		require(kind == expected_kind, f"slide {slide_number} effect kind must be {expected_kind}")
		resolved_kind, target = target_kind(page, target_id)
		kind_message = f"slide {slide_number} target {target_id} has kind {resolved_kind}, " + \
			f"expected {expected_target_kind}"
		require(resolved_kind == expected_target_kind, kind_message)
		resolved.append(target)
		text = text_value(target)
		if click_number == 1:
			require(text == expected_text,
				f"slide {slide_number} first target text {text!r} does not match {expected_text!r}")
		if kind == "fade":
			state = f"slide {slide_number}: fade {resolved_kind} {target_id} {text}: " + \
				f"hidden -> visible (click {click_number}, 1s crossfade)"
		else:
			state = f"slide {slide_number}: appear {resolved_kind} {target_id} {text}: " + \
				f"hidden -> visible (click {click_number})"
		states.append(state)
	if slide_number == 2:
		require_nested_cascade(page, resolved[0], resolved[1])
	return states


#============================================
def inspect_fixture(path: pathlib.Path) -> list[str]:
	"""Interpret all four bounded reveal specimens in their required order."""
	pages = package_pages(path)
	require(len(pages) == len(EXPECTED_SLIDES),
		f"{path.name} must contain the four bounded reveal specimens")
	states = []
	for slide_number, (page, expectation) in enumerate(zip(pages, EXPECTED_SLIDES), start=1):
		states.extend(inspect_slide(page, slide_number, expectation))
	return states


#============================================
def require_rejection(action: Callable[[], object], expected_message: str) -> None:
	"""Require one deliberately malformed in-memory specimen to fail interpretation."""
	try:
		action()
	except RuntimeError as error:
		require(expected_message in str(error),
			f"negative self-test failed with the wrong error: {error}")
		return
	raise RuntimeError(f"negative self-test accepted malformed specimen: {expected_message}")


#============================================
def verify_negative_cases(pages: list[object]) -> None:
	"""Prove strict target, timing, and effect boundaries without LibreOffice."""
	# A paired ID on an OOXML-style custom shape cannot be an object reveal target.
	custom_shape_page = copy.deepcopy(pages[0])
	custom_shape_target = next(custom_shape_page.iter(qname("draw", "frame")))
	custom_shape_target.tag = qname("draw", "custom-shape")
	require_rejection(lambda: inspect_slide(custom_shape_page, 1, EXPECTED_SLIDES[0]),
		"must resolve through exactly one paired native identity")

	# A timing node hidden beneath ordinary content is outside the sole timing tree.
	stray_timing_page = copy.deepcopy(pages[0])
	stray_parent = next(stray_timing_page.iter(qname("draw", "frame")))
	xml.etree.ElementTree.SubElement(stray_parent, qname("anim", "set"))
	require_rejection(lambda: inspect_slide(stray_timing_page, 1, EXPECTED_SLIDES[0]),
		"outside its timing-root subtree")

	# Effect nodes are terminal operations, not containers for another animation node.
	effect_child_page = copy.deepcopy(pages[0])
	effect = next(effect_child_page.iter(qname("anim", "set")))
	xml.etree.ElementTree.SubElement(effect, qname("anim", "set"))
	require_rejection(lambda: inspect_slide(effect_child_page, 1, EXPECTED_SLIDES[0]),
		"effect nodes must be leaves")


#============================================
def round_trip(path: pathlib.Path, workspace: pathlib.Path) -> pathlib.Path:
	"""Convert ODP to FODP then back to ODP with isolated LibreOffice profiles."""
	fodp_dir = workspace / "fodp"
	odp_dir = workspace / "odp"
	fodp_dir.mkdir()
	odp_dir.mkdir()
	first_profile = workspace / "profile_odp_to_fodp"
	second_profile = workspace / "profile_fodp_to_odp"
	first_command = [SOFFICE, "--headless", f"-env:UserInstallation={first_profile.as_uri()}",
		"--convert-to", "fodp", "--outdir", str(fodp_dir), str(path)]
	subprocess.run(first_command, check=True, capture_output=True, text=True)
	fodp_path = fodp_dir / f"{path.stem}.fodp"
	require(fodp_path.is_file(), "LibreOffice did not create the FODP transition artifact")
	second_command = [SOFFICE, "--headless", f"-env:UserInstallation={second_profile.as_uri()}",
		"--convert-to", "odp", "--outdir", str(odp_dir), str(fodp_path)]
	subprocess.run(second_command, check=True, capture_output=True, text=True)
	odp_path = odp_dir / path.name
	require(odp_path.is_file(), "LibreOffice did not recreate the ODP fixture")
	return odp_path


#============================================
def main() -> None:
	"""Run deterministic package semantics and the autonomous LO transition check."""
	args = parse_args()
	fixture = args.fixture.resolve()
	pages = package_pages(fixture)
	verify_negative_cases(pages)
	states = inspect_fixture(fixture)
	for state in states:
		print(state)
	if args.xml_only:
		print("PASS: native reveal XML semantics and negative self-tests")
		return
	with tempfile.TemporaryDirectory(prefix="odp_reveal_semantics_") as workspace_text:
		round_tripped = round_trip(fixture, pathlib.Path(workspace_text))
		round_trip_states = inspect_fixture(round_tripped)
	require(round_trip_states == states, "ODP -> FODP -> ODP changed the semantic reveal state")
	sha256 = hashlib.sha256(fixture.read_bytes()).hexdigest()
	print(f"PASS: native reveal semantics and ODP -> FODP -> ODP preservation ({sha256})")


if __name__ == "__main__":
	main()
