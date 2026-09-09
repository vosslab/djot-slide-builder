"""Bounded validation and atomic publication for OpenDocument packages."""

# Standard Library
import dataclasses
import os
import pathlib
import posixpath
import stat
import tempfile
import urllib.parse
import xml.etree.ElementTree
import zipfile

# PIP3 modules
import defusedxml.ElementTree


ODP_MIMETYPE = "application/vnd.oasis.opendocument.presentation"
MANIFEST_NAME = "META-INF/manifest.xml"
REQUIRED_ODP_MEMBERS = frozenset({"mimetype", "content.xml", "styles.xml", MANIFEST_NAME})
MANIFEST_FILE_ENTRY = "{urn:oasis:names:tc:opendocument:xmlns:manifest:1.0}file-entry"
MANIFEST_FULL_PATH = "{urn:oasis:names:tc:opendocument:xmlns:manifest:1.0}full-path"
MAX_INPUT_BYTES = 256 * 1024 * 1024
MAX_MEMBER_BYTES = 128 * 1024 * 1024
MAX_UNPACKED_BYTES = 512 * 1024 * 1024
MAX_ARCHIVE_MEMBERS = 2000
MAX_XML_NODES = 100_000
MAX_XML_DEPTH = 128
MAX_XML_TEXT_CHARACTERS = 2_000_000


@dataclasses.dataclass(frozen=True)
class AdmittedOdfPackage:
	"""One OpenDocument package whose XML facts passed all ODF boundaries."""

	path: pathlib.Path
	members: tuple[zipfile.ZipInfo, ...]
	member_names: frozenset[str]
	manifest_targets: frozenset[str]
	content_root: xml.etree.ElementTree.Element
	styles_root: xml.etree.ElementTree.Element


#============================================
def validate_member_name(member_name: str) -> None:
	"""Reject absolute and traversal paths in an OpenDocument archive.

	Args:
		member_name: Archive-local member name to validate.

	Raises:
		ValueError: The name is empty, absolute, or contains parent traversal.
	"""
	# ASVS 5.3.3: archive paths are data and never filesystem destinations.
	normalized = member_name.replace("\\", "/")
	parts = pathlib.PurePosixPath(normalized).parts
	if not normalized or normalized.startswith("/") or ".." in parts or \
			any(ord(character) < 32 or ord(character) == 127 for character in normalized):
		raise ValueError(f"unsafe archive member path: {member_name!r}")


#============================================
def package_reference_target(member_name: str, raw_value: str) -> str | None:
	"""Return one validated package-local reference or ``None`` for external data.

	Args:
		member_name: XML package member that owns the reference.
		raw_value: Raw XML ``href`` attribute value.

	Returns:
		A normalized archive-local target, or ``None`` when the value names an
		external URI or a same-document fragment.

	Raises:
		ValueError: The local reference escapes the ODF package namespace.
	"""
	if any(ord(character) < 32 or ord(character) == 127 for character in raw_value):
		raise ValueError(f"unsafe package reference: {raw_value!r}")
	parsed = urllib.parse.urlsplit(raw_value)
	if parsed.scheme or parsed.netloc or not parsed.path:
		return None
	decoded = urllib.parse.unquote(parsed.path)
	target = posixpath.normpath(posixpath.join(posixpath.dirname(member_name), decoded))
	validate_member_name(target)
	return target


#============================================
def validate_xml_tree(root: xml.etree.ElementTree.Element, member_name: str) -> None:
	"""Apply explicit breadth, depth, and text limits to an admitted XML tree."""
	stack = [(root, 1)]
	node_count = 0
	text_characters = 0
	while stack:
		element, depth = stack.pop()
		node_count += 1
		if node_count > MAX_XML_NODES:
			raise ValueError(f"ODF XML node limit exceeded in {member_name!r}")
		if depth > MAX_XML_DEPTH:
			raise ValueError(f"ODF XML depth limit exceeded in {member_name!r}")
		text_characters += len(element.text or "") + len(element.tail or "")
		if text_characters > MAX_XML_TEXT_CHARACTERS:
			raise ValueError(f"ODF XML text limit exceeded in {member_name!r}")
		stack.extend((child, depth + 1) for child in element)


#============================================
def xml_reference_targets_from_root(member_name: str,
		root: xml.etree.ElementTree.Element) -> frozenset[str]:
	"""Return validated package-local href targets from one parsed XML root."""
	targets: set[str] = set()
	for element in root.iter():
		for attribute, raw_value in element.attrib.items():
			if attribute.rsplit("}", 1)[-1] != "href":
				continue
			target = package_reference_target(member_name, raw_value)
			if target is not None:
				targets.add(target)
	return frozenset(targets)


#============================================
def manifest_file_targets_from_root(root: xml.etree.ElementTree.Element) -> frozenset[str]:
	"""Read validated package-local file targets from a parsed manifest root."""
	targets: set[str] = set()
	for entry in root.findall(f".//{MANIFEST_FILE_ENTRY}"):
		raw_path = entry.get(MANIFEST_FULL_PATH)
		if raw_path is None:
			raise ValueError("OpenDocument manifest entry is missing its full path")
		if raw_path == "/":
			continue
		if raw_path.endswith("/"):
			validate_member_name(raw_path[:-1])
			continue
		validate_member_name(raw_path)
		targets.add(raw_path)
	return frozenset(targets)


#============================================
def admit_package(input_path: pathlib.Path, expected_suffix: str,
		expected_mimetype: str, required_members: frozenset[str]) -> AdmittedOdfPackage:
	"""Read and validate bounded facts from one caller-owned package.

	Args:
		input_path: Existing OpenDocument package to inspect.
		expected_suffix: Required lowercase file suffix, including its leading dot.
		expected_mimetype: Exact media type required in the first archive member.
		required_members: Archive member names required for this document type.

	Returns:
		Validated member metadata, manifest targets, and parsed XML roots.

	Raises:
		ValueError: The package violates a type, path, size, or structure boundary.
		zipfile.BadZipFile: The input is not a readable ZIP package.
	"""
	# ASVS 1.5.1, 2.2.1, 5.2.1, 5.2.2, 5.2.3, and 5.3.3: one bounded admission.
	if not input_path.is_file() or input_path.suffix.lower() != expected_suffix:
		raise ValueError(f"input must be an existing {expected_suffix} file")
	if input_path.stat().st_size > MAX_INPUT_BYTES:
		raise ValueError("OpenDocument package exceeds the compressed input limit")
	with zipfile.ZipFile(input_path) as archive:
		members = tuple(archive.infolist())
		if not members or members[0].filename != "mimetype" or \
				members[0].compress_type != zipfile.ZIP_STORED:
			raise ValueError("OpenDocument mimetype must be the first uncompressed member")
		if len(members) > MAX_ARCHIVE_MEMBERS:
			raise ValueError("OpenDocument package contains too many archive members")
		total_size = 0
		member_names: set[str] = set()
		for member in members:
			validate_member_name(member.filename)
			mode = member.external_attr >> 16
			if mode and stat.S_ISLNK(mode):
				raise ValueError(f"OpenDocument package contains a symlink: {member.filename}")
			if member.flag_bits & 0x1:
				raise ValueError(f"OpenDocument package contains an encrypted member: {member.filename}")
			if member.file_size > MAX_MEMBER_BYTES:
				raise ValueError(f"OpenDocument member exceeds size limit: {member.filename}")
			total_size += member.file_size
			if total_size > MAX_UNPACKED_BYTES:
				raise ValueError("OpenDocument package exceeds the expanded archive limit")
			if member.filename in member_names:
				raise ValueError(f"OpenDocument package repeats a member: {member.filename}")
			member_names.add(member.filename)
		if not required_members.issubset(member_names):
			raise ValueError("OpenDocument package is missing required members")
		if archive.read("mimetype").decode("ascii", errors="strict") != expected_mimetype:
			raise ValueError("OpenDocument package mimetype member is invalid")
		# ASVS 1.5.1: defusedxml disables DTD and external entity processing.
		content_root = defusedxml.ElementTree.fromstring(archive.read("content.xml"))
		styles_root = defusedxml.ElementTree.fromstring(archive.read("styles.xml"))
		manifest_root = defusedxml.ElementTree.fromstring(archive.read(MANIFEST_NAME))
		for xml_name, root in (
			("content.xml", content_root), ("styles.xml", styles_root),
			(MANIFEST_NAME, manifest_root),
		):
			validate_xml_tree(root, xml_name)
		manifest_targets = manifest_file_targets_from_root(manifest_root)
		missing_manifest_targets = manifest_targets - member_names
		if missing_manifest_targets:
			raise ValueError("OpenDocument manifest references missing members")
		for xml_name, root in (("content.xml", content_root), ("styles.xml", styles_root)):
			references = xml_reference_targets_from_root(xml_name, root)
			missing_references = references - member_names
			if missing_references:
				raise ValueError("OpenDocument XML reference points to a missing member")
			missing_manifest_references = references - manifest_targets
			if missing_manifest_references:
				raise ValueError("OpenDocument XML reference misses a manifest target")
	return AdmittedOdfPackage(
		input_path, members, frozenset(member_names), manifest_targets, content_root, styles_root,
	)


#============================================
def validate_package(input_path: pathlib.Path, expected_suffix: str,
		expected_mimetype: str, required_members: frozenset[str]) -> list[zipfile.ZipInfo]:
	"""Validate one bounded OpenDocument ZIP package for existing callers."""
	return list(admit_package(input_path, expected_suffix, expected_mimetype, required_members).members)


#============================================
def xml_reference_targets(member_name: str, content: bytes) -> frozenset[str]:
	"""Return package-local files referenced by one XML member.

	Args:
		member_name: Package-local name of the XML member.
		content: XML bytes to inspect.

	Returns:
		Normalized package-local targets referenced by relative href attributes.

	Raises:
		ValueError: A referenced package path is unsafe.
	"""
	# ASVS 1.5.1: inspect XML through a restrictive parser before consuming attributes.
	root = defusedxml.ElementTree.fromstring(content)
	validate_xml_tree(root, member_name)
	return xml_reference_targets_from_root(member_name, root)


#============================================
def manifest_file_targets(content: bytes) -> frozenset[str]:
	"""Read validated package-local file targets declared by an ODF manifest.

	Args:
		content: Raw ``META-INF/manifest.xml`` bytes.

	Returns:
		The manifest's non-directory, package-local member targets.

	Raises:
		ValueError: A manifest entry names an unsafe archive location.
	"""
	# ASVS 1.5.1 and 5.3.3: restrictive XML and package-local path validation.
	root = defusedxml.ElementTree.fromstring(content)
	validate_xml_tree(root, MANIFEST_NAME)
	return manifest_file_targets_from_root(root)


#============================================
def validate_odp_members(payloads: dict[str, bytes],
		generated_members: frozenset[str] = frozenset()) -> None:
	"""Validate ODP manifest and XML references before package publication.

	Args:
		payloads: Complete mapping of package member names to bytes.
		generated_members: Generated media that must be reachable from package XML.

	Raises:
		ValueError: Required, manifest, reference, or reachability state is invalid.
	"""
	# ASVS 2.2.1: validate the complete related package state at one trusted boundary.
	if not REQUIRED_ODP_MEMBERS.issubset(payloads):
		raise ValueError("OpenDocument package is missing required members")
	for member_name in payloads:
		validate_member_name(member_name)
	manifest_files = manifest_file_targets(payloads[MANIFEST_NAME])
	payload_files = set(payloads) - {"mimetype", MANIFEST_NAME}
	missing_payloads = manifest_files - set(payloads)
	if missing_payloads:
		raise ValueError("OpenDocument manifest references missing members")
	missing_entries = payload_files - manifest_files
	if missing_entries:
		raise ValueError("OpenDocument member is missing a manifest entry")
	references: set[str] = set()
	for member_name, content in payloads.items():
		if member_name.endswith(".xml") and member_name != MANIFEST_NAME:
			references.update(xml_reference_targets(member_name, content))
	missing_references = references - set(payloads)
	if missing_references:
		raise ValueError("OpenDocument XML reference points to a missing member")
	if not generated_members.issubset(references):
		raise ValueError("generated media is unreachable from package XML")


#============================================
def publish_odp(destination: pathlib.Path, payloads: dict[str, bytes],
		generated_members: frozenset[str] = frozenset()) -> pathlib.Path:
	"""Validate, stage, and atomically publish one complete ODP package.

	Args:
		destination: Caller-selected output path ending in ``.odp``.
		payloads: Complete mapping of package member names to bytes.
		generated_members: Generated media that must be reachable from package XML.

	Returns:
		The atomically published destination path.

	Raises:
		ValueError: The destination or package state is invalid.
	"""
	# ASVS 5.3.2: the destination is caller-owned; archive member names are validated data.
	destination = pathlib.Path(destination)
	if destination.suffix.lower() != ".odp":
		raise ValueError("ODP output must use the .odp extension")
	validate_odp_members(payloads, generated_members)
	destination.parent.mkdir(parents=True, exist_ok=True)
	with tempfile.NamedTemporaryFile(prefix=f".{destination.stem}.", suffix=".odp",
			dir=destination.parent, delete=False) as temporary:
		temporary_path = pathlib.Path(temporary.name)
	try:
		with zipfile.ZipFile(temporary_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
			archive.writestr("mimetype", payloads["mimetype"], compress_type=zipfile.ZIP_STORED)
			for member_name in sorted(set(payloads) - {"mimetype"}):
				archive.writestr(member_name, payloads[member_name])
		validate_package(temporary_path, ".odp", ODP_MIMETYPE, REQUIRED_ODP_MEMBERS)
		os.replace(temporary_path, destination)
	except BaseException:
		temporary_path.unlink(missing_ok=True)
		raise
	return destination
