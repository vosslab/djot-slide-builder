"""Resolve bounded ODF style properties needed by direct import."""

# Standard Library
import dataclasses
import xml.etree.ElementTree


NS = {
	"draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
	"presentation": "urn:oasis:names:tc:opendocument:xmlns:presentation:1.0",
	"style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
	"text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
}


@dataclasses.dataclass(frozen=True)
class StyleDefinition:
	"""One bounded ODF style record used for property inheritance."""

	parent_name: str
	properties: dict[str, str]


def qname(prefix: str, local_name: str) -> str:
	"""Build one namespace-qualified XML name."""
	return f"{{{NS[prefix]}}}{local_name}"


def definitions(roots: tuple[xml.etree.ElementTree.Element, ...]) \
		-> dict[str, StyleDefinition]:
	"""Collect direct style properties and parent names from admitted XML roots."""
	result: dict[str, StyleDefinition] = {}
	for root in roots:
		for style in root.findall(".//style:style", NS):
			name = style.get(qname("style", "name"), "")
			if not name:
				continue
			properties: dict[str, str] = {}
			for child in style:
				if child.tag.endswith("-properties"):
					properties.update(child.attrib)
			result[name] = StyleDefinition(
				style.get(qname("style", "parent-style-name"), ""), properties)
	return result


def attribute(element: xml.etree.ElementTree.Element,
		style_definitions: dict[str, StyleDefinition], name: str) -> str | None:
	"""Resolve one direct or inherited style attribute with cycle detection."""
	if name in element.attrib:
		return element.attrib[name]
	style_name = element.get(qname("text", "style-name"), "") or \
		element.get(qname("draw", "style-name"), "") or \
		element.get(qname("presentation", "style-name"), "")
	ancestry: set[str] = set()
	while style_name:
		if style_name in ancestry:
			raise ValueError("ODF style inheritance contains a cycle")
		ancestry.add(style_name)
		definition = style_definitions.get(style_name)
		if definition is None:
			return None
		if name in definition.properties:
			return definition.properties[name]
		style_name = definition.parent_name
	return None
