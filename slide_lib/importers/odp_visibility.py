"""Resolve ODP drawing-page visibility across page and style cascades."""

# Standard Library
import zipfile
import pathlib
import dataclasses
import xml.etree.ElementTree

# PIP3 modules
import defusedxml.ElementTree

NS = {
	"draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
	"presentation": "urn:oasis:names:tc:opendocument:xmlns:presentation:1.0",
	"style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
}


@dataclasses.dataclass(frozen=True)
class DrawingPageStyle:
	"""Visibility-related properties of one drawing-page style."""

	parent_name: str
	visibility: str | None


#============================================
def qname(prefix: str, local_name: str) -> str:
	"""Build a namespace-qualified XML name."""
	qualified_name = f"{{{NS[prefix]}}}{local_name}"
	return qualified_name


#============================================
def style_visibility(style: xml.etree.ElementTree.Element) -> str | None:
	"""Read the visibility value directly specified by one style."""
	properties = style.find("./style:drawing-page-properties", NS)
	if properties is None:
		return None
	visibility = properties.get(qname("presentation", "visibility"))
	if visibility not in {None, "hidden", "visible"}:
		raise ValueError("drawing-page style has an invalid presentation visibility")
	return visibility


#============================================
def style_definitions_from_root(
	root: xml.etree.ElementTree.Element,
) -> dict[str, DrawingPageStyle]:
	"""Extract local drawing-page style definitions from one XML root."""
	definitions: dict[str, DrawingPageStyle] = {}
	for style in root.findall(".//style:style", NS):
		if style.get(qname("style", "family")) != "drawing-page":
			continue
		style_name = style.get(qname("style", "name"), "")
		if not style_name:
			raise ValueError("drawing-page style is missing its name")
		definitions[style_name] = DrawingPageStyle(
			parent_name=style.get(qname("style", "parent-style-name"), ""),
			visibility=style_visibility(style),
		)
	return definitions


#============================================
def read_style_definitions(
	input_path: pathlib.Path,
	content_root: xml.etree.ElementTree.Element,
) -> dict[str, DrawingPageStyle]:
	"""Read named and automatic drawing-page styles with local override order."""
	definitions: dict[str, DrawingPageStyle] = {}
	with zipfile.ZipFile(input_path) as archive:
		if "styles.xml" in archive.namelist():
			styles_root = defusedxml.ElementTree.fromstring(archive.read("styles.xml"))
			definitions.update(style_definitions_from_root(styles_root))
	definitions.update(style_definitions_from_root(content_root))
	return definitions


#============================================
def resolve_style_visibility(
	style_name: str,
	definitions: dict[str, DrawingPageStyle],
	ancestry: set[str],
) -> str | None:
	"""Resolve a drawing-page style through its parent chain."""
	if not style_name:
		return None
	if style_name in ancestry:
		raise ValueError("drawing-page style inheritance contains a cycle")
	style = definitions.get(style_name)
	if style is None:
		return None
	if style.visibility is not None:
		return style.visibility
	next_ancestry = ancestry | {style_name}
	resolved_visibility = resolve_style_visibility(
		style.parent_name,
		definitions,
		next_ancestry,
	)
	return resolved_visibility


#============================================
def page_is_hidden(
	page: xml.etree.ElementTree.Element,
	definitions: dict[str, DrawingPageStyle],
) -> bool:
	"""Return page visibility, giving an explicit page value highest priority."""
	page_visibility = page.get(qname("presentation", "visibility"))
	if page_visibility == "hidden":
		return True
	if page_visibility == "visible":
		return False
	if page_visibility is not None:
		raise ValueError("drawing page has an invalid presentation visibility")
	style_name = page.get(qname("draw", "style-name"), "")
	resolved_visibility = resolve_style_visibility(style_name, definitions, set())
	hidden = resolved_visibility == "hidden"
	return hidden


#============================================
def run_visibility(input_file: pathlib.Path) -> None:
	"""Print each imported slide's resolved visible or hidden state."""
	# Import at the operation boundary to avoid a module-level cycle with odp_reader.
	import slide_lib.importers.odp_reader as odp_reader

	# ASVS 2.2.1 and 5.3.2: reuse the bounded importer validation for the file path.
	slides = odp_reader.read_slides(input_file)
	for slide in slides:
		visibility = "hidden" if slide.hidden else "visible"
		print(f"{slide.source_index}\t{visibility}\t{slide.name}")
	visible_count = sum(not slide.hidden for slide in slides)
	hidden_count = len(slides) - visible_count
	print(f"Visible: {visible_count}")
	print(f"Hidden: {hidden_count}")
