"""Validate and read an imported ODP before Djot emission."""

# Standard Library
import stat
import zipfile
import pathlib
import dataclasses
import xml.etree.ElementTree

# PIP3 modules
import defusedxml.ElementTree

# local repo modules
import slide_lib.libreoffice
import slide_lib.importers.odp_visibility as odp_visibility


NS = {
	"draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
}
ODP_MIMETYPE = "application/vnd.oasis.opendocument.presentation"
MAX_INPUT_BYTES = 256 * 1024 * 1024
MAX_MEMBER_BYTES = 128 * 1024 * 1024
MAX_UNPACKED_BYTES = 512 * 1024 * 1024
MAX_ARCHIVE_MEMBERS = 2000


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
def validate_member_name(member_name: str) -> None:
	"""Reject absolute and traversal paths in an ODP archive."""
	# ASVS 5.3.3: archive member paths never control filesystem destinations.
	normalized = member_name.replace("\\", "/")
	parts = pathlib.PurePosixPath(normalized).parts
	if normalized.startswith("/") or ".." in parts:
		raise ValueError(f"unsafe archive member path: {member_name}")


#============================================
def validate_odp(input_path: pathlib.Path) -> list[zipfile.ZipInfo]:
	"""Validate a bounded OpenDocument presentation before conversion."""
	# ASVS 2.2.1, 5.2.1, 5.2.2, and 5.2.3: validate type and archive limits.
	if not input_path.is_file() or input_path.suffix.lower() != ".odp":
		raise ValueError("input must be an existing .odp file")
	if input_path.stat().st_size > MAX_INPUT_BYTES:
		raise ValueError("ODP exceeds the compressed input limit")
	with zipfile.ZipFile(input_path) as archive:
		members = archive.infolist()
		if len(members) > MAX_ARCHIVE_MEMBERS:
			raise ValueError("ODP contains too many archive members")
		total_size = 0
		member_names: set[str] = set()
		for member in members:
			validate_member_name(member.filename)
			mode = member.external_attr >> 16
			if mode and stat.S_ISLNK(mode):
				raise ValueError(f"ODP archive contains a symlink: {member.filename}")
			if member.file_size > MAX_MEMBER_BYTES:
				raise ValueError(f"ODP member exceeds size limit: {member.filename}")
			total_size += member.file_size
			if total_size > MAX_UNPACKED_BYTES:
				raise ValueError("ODP exceeds the expanded archive limit")
			member_names.add(member.filename)
		if not {"mimetype", "content.xml"}.issubset(member_names):
			raise ValueError("ODP is missing required members")
		if archive.read("mimetype").decode("ascii", errors="strict") != ODP_MIMETYPE:
			raise ValueError("ODP mimetype member is invalid")
		# ASVS 1.5.1: defusedxml disables DTD and external entity processing.
		defusedxml.ElementTree.fromstring(archive.read("content.xml"))
		if "styles.xml" in member_names:
			defusedxml.ElementTree.fromstring(archive.read("styles.xml"))
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

