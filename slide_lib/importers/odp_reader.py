"""Validate and read an imported ODP before Djot emission."""

# Standard Library
import zipfile
import pathlib
import dataclasses
import xml.etree.ElementTree

# PIP3 modules
import defusedxml.ElementTree

# local repo modules
import slide_lib.odf_package
import slide_lib.libreoffice
import slide_lib.importers.odp_visibility as odp_visibility


NS = {
	"draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
}
ODP_MIMETYPE = "application/vnd.oasis.opendocument.presentation"
@dataclasses.dataclass(frozen=True)
class ImportedSlide:
	"""Imported slide identity and visibility retained from ODP XML."""

	source_index: int
	name: str
	hidden: bool


#============================================
def qname(prefix: str, local_name: str) -> str:
	"""Build one namespace-qualified XML name."""
	return f"{{{NS[prefix]}}}{local_name}"


#============================================
def validate_odp(input_path: pathlib.Path) -> list[zipfile.ZipInfo]:
	"""Validate a bounded OpenDocument presentation before conversion."""
	required = frozenset({"mimetype", "content.xml"})
	members = slide_lib.odf_package.validate_package(
		input_path, ".odp", ODP_MIMETYPE, required,
	)
	return members


#============================================
def read_content_root(input_path: pathlib.Path) -> xml.etree.ElementTree.Element:
	"""Parse the validated ODP content XML with restrictive XML handling."""
	validate_odp(input_path)
	with zipfile.ZipFile(input_path) as archive:
		content_bytes = archive.read("content.xml")
	root = defusedxml.ElementTree.fromstring(content_bytes)
	return root


#============================================
def read_slides(input_path: pathlib.Path) -> list[ImportedSlide]:
	"""Read imported slide order and visibility from ODP XML."""
	root = read_content_root(input_path)
	definitions = odp_visibility.read_style_definitions(input_path, root)
	pages = root.findall(".//draw:page", NS)
	slides: list[ImportedSlide] = []
	for source_index, page in enumerate(pages, start=1):
		slide_name = page.get(qname("draw", "name"), f"slide_{source_index:03d}")
		slides.append(
			ImportedSlide(
				source_index=source_index,
				name=slide_name,
				hidden=odp_visibility.page_is_hidden(page, definitions),
			)
		)
	return slides


#============================================
def convert_odp_to_pptx(input_path: pathlib.Path, temporary_root: pathlib.Path) -> pathlib.Path:
	"""Normalize ODP geometry into a temporary PPTX with LibreOffice."""
	converted_dir = temporary_root / "converted"
	converted_dir.mkdir()
	pptx_path = slide_lib.libreoffice.convert_file(input_path, converted_dir, "pptx")
	return pptx_path
