"""Read the bounded object-appearance evidence used by ODP import."""

# Standard Library
import xml.etree.ElementTree


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
