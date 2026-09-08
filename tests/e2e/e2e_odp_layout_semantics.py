#!/usr/bin/env python3
"""Validate native ODP role layouts and LibreOffice preservation."""

# Standard Library
import copy
import dataclasses
import pathlib
import subprocess
import sys
import tempfile
import zipfile

# PIP3 modules
import defusedxml.ElementTree


NAMESPACES = {
	"draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
	"office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
	"presentation": "urn:oasis:names:tc:opendocument:xmlns:presentation:1.0",
	"style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
}
SOFFICE = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
ONE_BOX = ("title", "outline")
COMPATIBLE_ALTERNATE = ("title", "outline", "outline")
NATIVE_SENTINELS = {"title": "Native fixture title", "outline": "Native fixture body"}
GENERIC_SENTINELS = ("Generic fixture title", "Generic fixture body")


#============================================
def qname(namespace: str, name: str) -> str:
	"""Return one expanded QName from the fixed ODF namespace table."""
	return f"{{{NAMESPACES[namespace]}}}{name}"


#============================================
def require(condition: bool, message: str) -> None:
	"""Raise an actionable E2E failure for one required layout invariant."""
	if not condition:
		raise RuntimeError(message)


#============================================
def fixture_path(name: str) -> pathlib.Path:
	"""Return one committed role fixture by its stable basename."""
	root = pathlib.Path(__file__).resolve().parents[2]
	return root / "tests" / "fixtures" / "odp_native_layouts" / name


#============================================
def native_reference_path() -> pathlib.Path:
	"""Return the captured native deck used for real LibreOffice preservation."""
	root = pathlib.Path(__file__).resolve().parents[2]
	return root / "genetics" / "lect02a-2025_announcements.odp"


#============================================
def package_trees(path: pathlib.Path) -> tuple[object, object]:
	"""Read content and style trees from one ODP package."""
	with zipfile.ZipFile(path) as archive:
		content = defusedxml.ElementTree.fromstring(archive.read("content.xml"))
		styles = defusedxml.ElementTree.fromstring(archive.read("styles.xml"))
	return content, styles


#============================================
def only_page(content: object, name: str) -> object:
	"""Return the single page from an ODP content tree."""
	pages = content.findall("./office:body/office:presentation/draw:page", NAMESPACES)
	require(len(pages) == 1, f"{name} must contain exactly one comparator page")
	return pages[0]


#============================================
def normalized_text(element: object) -> str:
	"""Return descendant text normalized solely for XML whitespace."""
	return " ".join("".join(element.itertext()).split())


#============================================
def direct_content_members(page: object) -> list[object]:
	"""Return direct visual content while excluding notes and page thumbnails."""
	accepted = {qname("draw", "frame"), qname("draw", "custom-shape"),
		qname("draw", "g"), qname("draw", "connector")}
	return [child for child in list(page) if child.tag in accepted]


#============================================
def is_ooxml_rect(member: object) -> bool:
	"""Return whether one direct custom shape is a text-bearing OOXML rectangle."""
	geometry = member.find("draw:enhanced-geometry", NAMESPACES)
	shape_type = "" if geometry is None else geometry.attrib.get(qname("draw", "type"), "")
	return member.tag == qname("draw", "custom-shape") and shape_type == "ooxml-rect" and \
		normalized_text(member) != ""


#============================================
def native_role(member: object) -> str:
	"""Return the only native role allowed in this one-box comparator."""
	require(member.tag == qname("draw", "frame"), "native role content must use draw:frame")
	role = member.attrib.get(qname("presentation", "class"), "")
	require(role in ONE_BOX, f"native frame has unsupported presentation role {role!r}")
	return role


#============================================
def style_index(content: object, styles: object) -> dict[str, object]:
	"""Index every named presentation style from package content and styles."""
	result: dict[str, object] = {}
	for root in (content, styles):
		for style in root.findall(".//style:style", NAMESPACES):
			name = style.attrib.get(qname("style", "name"), "")
			if name:
				result[name] = style
	return result


#============================================
def inherited_graphic_properties(style_name: str, styles: dict[str, object]) -> dict[str, str]:
	"""Resolve a presentation style chain, with child values taking precedence."""
	properties: dict[str, str] = {}
	current_name = style_name
	seen: set[str] = set()
	while current_name:
		require(current_name not in seen, f"style inheritance cycle at {current_name!r}")
		seen.add(current_name)
		style = styles.get(current_name)
		require(style is not None, f"missing presentation style {current_name!r}")
		require(style.attrib.get(qname("style", "family")) == "presentation",
			f"style {current_name!r} is not a presentation style")
		graphic = style.find("style:graphic-properties", NAMESPACES)
		if graphic is not None:
			for key, value in graphic.attrib.items():
				properties.setdefault(key, value)
		current_name = style.attrib.get(qname("style", "parent-style-name"), "")
	return properties


#============================================
def assert_style_contract(member: object, role: str, styles: dict[str, object]) -> None:
	"""Require a Default-role style chain and explicit fixed shrink-only policy."""
	style_name = member.attrib.get(qname("presentation", "style-name"), "")
	require(style_name != "", f"{role} frame lacks presentation:style-name")
	chain: list[str] = []
	current_name = style_name
	while current_name:
		chain.append(current_name)
		style = styles.get(current_name)
		require(style is not None, f"{role} frame references missing style {current_name!r}")
		current_name = style.attrib.get(qname("style", "parent-style-name"), "")
	expected_parent = "Default-title" if role == "title" else "Default-outline1"
	require(expected_parent in chain,
		f"{role} frame style chain {chain} does not inherit {expected_parent}")
	properties = inherited_graphic_properties(style_name, styles)
	require(properties.get(qname("draw", "auto-grow-height")) == "false",
		f"{role} frame must disable auto-grow-height")
	require(properties.get(qname("draw", "fit-to-size")) == "false",
		f"{role} frame must disable fit-to-size")
	require(properties.get(qname("style", "shrink-to-fit")) == "true",
		f"{role} frame must enable shrink-to-fit")


#============================================
def layout_topology(styles: object, layout_name: str) -> tuple[str, ...]:
	"""Resolve an opaque page-layout identifier to its role topology."""
	layouts = styles.findall(".//style:presentation-page-layout", NAMESPACES)
	matching = [layout for layout in layouts if layout.attrib.get(qname("style", "name")) == layout_name]
	require(len(matching) == 1, f"page layout {layout_name!r} does not resolve exactly once")
	roles = []
	for placeholder in matching[0].findall("presentation:placeholder", NAMESPACES):
		object_name = placeholder.attrib.get(qname("presentation", "object"), "")
		roles.append(object_name)
	return tuple(roles)


#============================================
def layout_name_with_topology(styles: object, expected: tuple[str, ...]) -> str:
	"""Resolve one locally captured layout name from its ordered role topology."""
	matches = []
	for layout in styles.findall(".//style:presentation-page-layout", NAMESPACES):
		name = layout.attrib.get(qname("style", "name"), "")
		if name and layout_topology(styles, name) == expected:
			matches.append(name)
	require(len(matches) == 1,
		f"expected exactly one captured layout with topology {expected!r}, got {matches!r}")
	return matches[0]


#============================================
def role_slots(topology: tuple[str, ...]) -> tuple[tuple[str, int], ...]:
	"""Name repeated role slots by their ordered occurrence within one layout."""
	occurrences: dict[str, int] = {}
	result = []
	for role in topology:
		occurrences[role] = occurrences.get(role, 0) + 1
		result.append((role, occurrences[role]))
	return tuple(result)


@dataclasses.dataclass(frozen=True)
class LayoutAssignment:
	"""One deterministic assignment from a source slot to a target slot."""

	target_slot: tuple[str, int]
	source_slot: tuple[str, int] | None
	text: str


#============================================
def authored_slot_text(page: object, topology: tuple[str, ...]) -> dict[tuple[str, int], str]:
	"""Read each authored native member into its unambiguous ordered role slot."""
	expected_slots = role_slots(topology)
	result: dict[tuple[str, int], str] = {}
	occurrences: dict[str, int] = {}
	members = direct_content_members(page)
	require(len(members) == len(expected_slots),
		"authored content count must exactly match its source layout topology")
	for member in members:
		role = native_role(member)
		occurrences[role] = occurrences.get(role, 0) + 1
		slot = (role, occurrences[role])
		require(slot in expected_slots, f"authored {slot!r} has no source layout slot")
		require(slot not in result, f"authored {slot!r} maps more than once")
		text = normalized_text(member)
		require(text != "", f"authored {slot!r} must contain source text")
		result[slot] = text
	require(tuple(result) == expected_slots,
		f"authored slots {tuple(result)!r} do not match source topology {expected_slots!r}")
	return result


#============================================
def apply_layout_transition(content: object, styles: object, target_layout: str) -> list[LayoutAssignment]:
	"""Interpret a compatible layout assignment without a UI or a LibreOffice process."""
	page = only_page(content, "layout transition source")
	source_layout = page.attrib.get(qname("presentation", "presentation-page-layout-name"), "")
	require(source_layout != "", "layout transition source lacks a page-layout binding")
	source_topology = layout_topology(styles, source_layout)
	target_topology = layout_topology(styles, target_layout)
	source_slots = role_slots(source_topology)
	target_slots = role_slots(target_topology)
	require(target_slots[:len(source_slots)] == source_slots,
		"target layout must retain source role slots in their original order")
	source_text = authored_slot_text(page, source_topology)
	assignments = []
	for target_slot in target_slots:
		if target_slot in source_text:
			assignments.append(LayoutAssignment(target_slot, target_slot, source_text[target_slot]))
		else:
			assignments.append(LayoutAssignment(target_slot, None, ""))
	return assignments


#============================================
def assert_transition_contract(assignments: list[LayoutAssignment],
		target_topology: tuple[str, ...]) -> None:
	"""Require one-to-one authored retention and only compatible empty additions."""
	require(tuple(assignment.target_slot for assignment in assignments) == role_slots(target_topology),
		"transition assignments must cover the resolved target topology in order")
	authored = [assignment for assignment in assignments if assignment.source_slot is not None]
	empty = [assignment for assignment in assignments if assignment.source_slot is None]
	require(len({assignment.source_slot for assignment in authored}) == len(authored),
		"transition must not duplicate an authored source slot")
	require(all(assignment.source_slot == assignment.target_slot for assignment in authored),
		"compatible transition must retain authored content in its matching role slot")
	require(all(assignment.text == "" for assignment in empty),
		"new compatible target slots must be empty placeholders only")


#============================================
def assert_native_fixture(content: object, styles_root: object, name: str) -> None:
	"""Assert the positive native role, layout, style, and text contract."""
	page = only_page(content, name)
	layout_name = page.attrib.get(qname("presentation", "presentation-page-layout-name"), "")
	require(layout_name != "", f"{name} has no presentation-page-layout binding")
	require(layout_topology(styles_root, layout_name) == ONE_BOX,
		f"{name} page layout {layout_name!r} is not exactly the title-plus-outline topology")
	members = direct_content_members(page)
	require(len(members) == 2, f"{name} must have exactly two direct content members")
	styles = style_index(content, styles_root)
	seen_roles: set[str] = set()
	for member in members:
		role = native_role(member)
		require(role not in seen_roles, f"{name} duplicates native {role} role")
		seen_roles.add(role)
		require(member.attrib.get(qname("draw", "layer")) == "layout",
			f"{name} {role} frame is not on the layout layer")
		require(normalized_text(member) == NATIVE_SENTINELS[role],
			f"{name} {role} sentinel text must match exactly")
		assert_style_contract(member, role, styles)
	require(seen_roles == set(ONE_BOX), f"{name} does not contain title and outline frames")
	require(not any(is_ooxml_rect(member) for member in members),
		f"{name} native role fixture contains a text-bearing ooxml-rect")


#============================================
def assert_generic_fixture(content: object, styles_root: object, name: str) -> None:
	"""Assert the negative generic-text comparator cannot impersonate a layout."""
	del styles_root
	page = only_page(content, name)
	require(qname("presentation", "presentation-page-layout-name") not in page.attrib,
		f"{name} generic fixture unexpectedly binds a presentation layout")
	members = direct_content_members(page)
	require(len(members) == 2 and all(is_ooxml_rect(member) for member in members),
		f"{name} must retain exactly two text-bearing ooxml-rect objects")
	require(all(qname("presentation", "class") not in member.attrib for member in members),
		f"{name} generic objects must not gain presentation classes")
	texts = tuple(normalized_text(member) for member in members)
	require(texts == GENERIC_SENTINELS, f"{name} generic sentinel text must match exactly")


#============================================
def assert_native_reference_round_trip(path: pathlib.Path) -> None:
	"""Require the captured native slide 3 to retain its semantic role topology."""
	content, styles_root = package_trees(path)
	pages = content.findall("./office:body/office:presentation/draw:page", NAMESPACES)
	require(len(pages) >= 3, f"{path.name} must retain the captured native slide 3")
	page = pages[2]
	layout_name = page.attrib.get(qname("presentation", "presentation-page-layout-name"), "")
	require(layout_name != "", f"{path.name} slide 3 has no presentation-page-layout binding")
	require(layout_topology(styles_root, layout_name) == ONE_BOX,
		f"{path.name} slide 3 layout {layout_name!r} is not title plus outline")
	styles = style_index(content, styles_root)
	roles: dict[str, object] = {}
	for member in direct_content_members(page):
		if member.attrib.get(qname("presentation", "class")) in ONE_BOX:
			role = native_role(member)
			require(role not in roles, f"{path.name} slide 3 duplicates {role} frames")
			roles[role] = member
	require(set(roles) == set(ONE_BOX), f"{path.name} slide 3 does not retain title and outline frames")
	require(normalized_text(roles["title"]) == "Breakout Room Chat",
		f"{path.name} slide 3 title sentinel changed")
	require(normalized_text(roles["outline"]) ==
		"State your name, major, and post-grad plansWe had great weather this weekend. "
		"What is your favorite outdoor activity?Dr. Voss: riding my bicycle, watching my kids play sports, go on a walk",
		f"{path.name} slide 3 outline sentinel changed")
	for role, member in roles.items():
		style_name = member.attrib.get(qname("presentation", "style-name"), "")
		expected_parent = "Default-title" if role == "title" else "Default-outline1"
		chain = []
		while style_name:
			chain.append(style_name)
			style_name = styles[style_name].attrib.get(qname("style", "parent-style-name"), "")
		require(expected_parent in chain,
			f"{path.name} slide 3 {role} lost its {expected_parent} style parent")


#============================================
def assert_package(path: pathlib.Path) -> None:
	"""Run the matching strict fixture contract for one named ODP package."""
	content, styles = package_trees(path)
	if path.name == "one_box_native_roles.odp":
		assert_native_fixture(content, styles, path.name)
	elif path.name == "one_box_generic_text.odp":
		assert_generic_fixture(content, styles, path.name)
	else:
		raise RuntimeError(f"unrecognized layout fixture {path.name!r}")


#============================================
def style_name_for_role(content: object, role: str) -> str:
	"""Return the direct frame style name for one native role fixture member."""
	for member in direct_content_members(only_page(content, "native self-test")):
		if member.attrib.get(qname("presentation", "class")) == role:
			return member.attrib[qname("presentation", "style-name")]
	raise RuntimeError(f"native self-test fixture lacks a {role} frame")


#============================================
def expect_rejection(action: object, description: str) -> None:
	"""Require one deliberately malformed XML variant to violate the contract."""
	try:
		action()
	except RuntimeError:
		return
	raise RuntimeError(f"negative self-test accepted {description}")


#============================================
def run_negative_self_tests() -> None:
	"""Prove strict checks reject malformed layout, style, policy, text, and mappings."""
	content, styles = package_trees(fixture_path("one_box_native_roles.odp"))
	broken_layout_content = copy.deepcopy(content)
	only_page(broken_layout_content, "native self-test").attrib[
		qname("presentation", "presentation-page-layout-name")] = "missing-layout"
	expect_rejection(lambda: assert_native_fixture(broken_layout_content, styles, "broken layout"),
		"an unresolved page-layout binding")
	broken_parent_content = copy.deepcopy(content)
	broken_parent_styles = copy.deepcopy(styles)
	style_index(broken_parent_content, broken_parent_styles)[
		style_name_for_role(broken_parent_content, "title")].attrib[
		qname("style", "parent-style-name")] = "Wrong-title"
	expect_rejection(lambda: assert_native_fixture(broken_parent_content, broken_parent_styles, "broken parent"),
		"a title style chain without Default-title")
	broken_policy_content = copy.deepcopy(content)
	broken_policy_styles = copy.deepcopy(styles)
	graphic = style_index(broken_policy_content, broken_policy_styles)[
		style_name_for_role(broken_policy_content, "outline")].find(
		"style:graphic-properties", NAMESPACES)
	require(graphic is not None, "native self-test fixture lacks outline graphic properties")
	graphic.attrib[qname("style", "shrink-to-fit")] = "false"
	expect_rejection(lambda: assert_native_fixture(broken_policy_content, broken_policy_styles, "broken policy"),
		"a fixed outline without shrink-to-fit")
	broken_text_content = copy.deepcopy(content)
	broken_text_styles = copy.deepcopy(styles)
	first_text = next(iter(direct_content_members(only_page(broken_text_content, "native self-test"))[0].iter()))
	first_text.text = "Changed title"
	expect_rejection(lambda: assert_native_fixture(broken_text_content, broken_text_styles, "broken text"),
		"a non-exact native sentinel")
	generic_content, generic_styles = package_trees(fixture_path("one_box_generic_text.odp"))
	broken_generic = copy.deepcopy(generic_content)
	direct_content_members(only_page(broken_generic, "generic self-test"))[0].attrib[
		qname("presentation", "class")] = "title"
	expect_rejection(lambda: assert_generic_fixture(broken_generic, generic_styles, "broken generic"),
		"a generic rectangle pretending to be a title frame")
	broken_duplicate_content = copy.deepcopy(content)
	duplicate_page = only_page(broken_duplicate_content, "duplicate mapping")
	duplicate_page.append(copy.deepcopy(direct_content_members(duplicate_page)[0]))
	expect_rejection(lambda: apply_layout_transition(broken_duplicate_content, styles,
		layout_name_with_topology(styles, COMPATIBLE_ALTERNATE)),
		"two authored title frames mapping to one title slot")
	broken_target_styles = copy.deepcopy(styles)
	alternate_name = layout_name_with_topology(broken_target_styles, COMPATIBLE_ALTERNATE)
	for layout in broken_target_styles.findall(".//style:presentation-page-layout", NAMESPACES):
		if layout.attrib.get(qname("style", "name")) == alternate_name:
			placeholders = layout.findall("presentation:placeholder", NAMESPACES)
			placeholders[1].attrib[qname("presentation", "object")] = "subtitle"
			break
	expect_rejection(lambda: apply_layout_transition(content, broken_target_styles, alternate_name),
		"a target topology that cannot retain the primary outline slot")
	broken_duplicate_styles = copy.deepcopy(styles)
	duplicated = False
	for parent in broken_duplicate_styles.iter():
		for layout in list(parent):
			if layout.tag == qname("style", "presentation-page-layout") and \
				layout.attrib.get(qname("style", "name")) == alternate_name:
				parent.append(copy.deepcopy(layout))
				duplicated = True
				break
		if duplicated:
			break
	if not duplicated:
		raise RuntimeError("native self-test fixture lacks compatible alternate layout")
	expect_rejection(lambda: layout_name_with_topology(broken_duplicate_styles, COMPATIBLE_ALTERNATE),
		"duplicate XML definitions for the compatible role topology")


#============================================
def round_trip_through_libreoffice(source: pathlib.Path, workspace: pathlib.Path) -> pathlib.Path:
	"""Perform a real ODP-to-FODP-to-ODP LibreOffice preservation transition."""
	fodp_output = workspace / "fodp"
	odp_output = workspace / "odp"
	fodp_output.mkdir(parents=True)
	odp_output.mkdir(parents=True)
	profile_one = workspace / "profile_one"
	command_one = [SOFFICE, "--headless", f"-env:UserInstallation={profile_one.as_uri()}",
		"--convert-to", "fodp", "--outdir", str(fodp_output), str(source)]
	first_result = subprocess.run(command_one, check=False, capture_output=True, text=True)
	require(first_result.returncode == 0,
		f"LibreOffice ODP-to-FODP failed: {first_result.stdout}{first_result.stderr}")
	fodp = fodp_output / f"{source.stem}.fodp"
	require(fodp.exists(),
		f"LibreOffice did not create {fodp.name}; output contains {[path.name for path in fodp_output.iterdir()]}")
	profile_two = workspace / "profile_two"
	command_two = [SOFFICE, "--headless", f"-env:UserInstallation={profile_two.as_uri()}",
		"--convert-to", "odp", "--outdir", str(odp_output), str(fodp)]
	second_result = subprocess.run(command_two, check=False, capture_output=True, text=True)
	require(second_result.returncode == 0,
		f"LibreOffice FODP-to-ODP failed: {second_result.stdout}{second_result.stderr}")
	result = odp_output / source.name
	require(result.exists(),
		f"LibreOffice did not recreate {source.name}; output contains {[path.name for path in odp_output.iterdir()]}")
	return result


#============================================
def assert_transition_evidence() -> None:
	"""Check same and compatible topology assignments against the native One Box fixture."""
	content, styles = package_trees(fixture_path("one_box_native_roles.odp"))
	page = only_page(content, "transition source")
	source_name = page.attrib[qname("presentation", "presentation-page-layout-name")]
	source_topology = layout_topology(styles, source_name)
	require(source_topology == ONE_BOX, "transition source must resolve to One Box topology")
	same_layout = apply_layout_transition(content, styles, source_name)
	assert_transition_contract(same_layout, source_topology)
	require([(item.target_slot, item.source_slot, item.text) for item in same_layout] == [
		(("title", 1), ("title", 1), NATIVE_SENTINELS["title"]),
		(("outline", 1), ("outline", 1), NATIVE_SENTINELS["outline"]),
	], "same-layout transition must retain title/body exactly once")
	compatible_name = layout_name_with_topology(styles, COMPATIBLE_ALTERNATE)
	compatible_layout = apply_layout_transition(content, styles, compatible_name)
	assert_transition_contract(compatible_layout, COMPATIBLE_ALTERNATE)
	require([(item.target_slot, item.source_slot, item.text) for item in compatible_layout] == [
		(("title", 1), ("title", 1), NATIVE_SENTINELS["title"]),
		(("outline", 1), ("outline", 1), NATIVE_SENTINELS["outline"]),
		(("outline", 2), None, ""),
	], "compatible transition must retain title/body once and add only empty secondary outline")


#============================================
def main(xml_only: bool = False) -> None:
	"""Run XML contracts and, unless requested otherwise, serialized LO preservation."""
	native = fixture_path("one_box_native_roles.odp")
	generic = fixture_path("one_box_generic_text.odp")
	assert_package(native)
	assert_package(generic)
	run_negative_self_tests()
	assert_transition_evidence()
	if xml_only:
		print("PASS: native ODP role and compatible-layout XML semantics are stable")
		return
	with tempfile.TemporaryDirectory(prefix="odp_layout_semantics_") as workspace_text:
		saved = round_trip_through_libreoffice(native_reference_path(), pathlib.Path(workspace_text))
		assert_native_reference_round_trip(saved)
	print("PASS: native ODP role semantics and LibreOffice preservation are stable")


if __name__ == "__main__":
	require(tuple(sys.argv[1:]) in ((), ("--xml-only",)),
		"usage: e2e_odp_layout_semantics.py [--xml-only]")
	main(xml_only=sys.argv[1:] == ["--xml-only"])
