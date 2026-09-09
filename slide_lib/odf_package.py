"""Bounded validation and atomic publication for OpenDocument packages."""

# Standard Library
import os
import stat
import pathlib
import zipfile
import tempfile
import posixpath
import urllib.parse

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
	if not normalized or normalized.startswith("/") or ".." in parts:
		raise ValueError(f"unsafe archive member path: {member_name}")


#============================================
def validate_package(input_path: pathlib.Path, expected_suffix: str,
		expected_mimetype: str, required_members: frozenset[str]) -> list[zipfile.ZipInfo]:
	"""Validate one bounded OpenDocument ZIP package and its XML members.

	Args:
		input_path: Existing OpenDocument package to inspect.
		expected_suffix: Required lowercase file suffix, including its leading dot.
		expected_mimetype: Exact media type required in the first archive member.
		required_members: Archive member names required for this document type.

	Returns:
		The validated archive member metadata.

	Raises:
		ValueError: The package violates a type, path, size, or structure boundary.
		zipfile.BadZipFile: The input is not a readable ZIP package.
	"""
	# ASVS 2.2.1, 5.2.1, 5.2.2, and 5.2.3: allow-list type and archive limits.
	if not input_path.is_file() or input_path.suffix.lower() != expected_suffix:
		raise ValueError(f"input must be an existing {expected_suffix} file")
	if input_path.stat().st_size > MAX_INPUT_BYTES:
		raise ValueError("OpenDocument package exceeds the compressed input limit")
	with zipfile.ZipFile(input_path) as archive:
		members = archive.infolist()
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
		for xml_name in ("content.xml", "styles.xml"):
			if xml_name in member_names:
				defusedxml.ElementTree.fromstring(archive.read(xml_name))
	return members


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
	targets: set[str] = set()
	for element in root.iter():
		for attribute, raw_value in element.attrib.items():
			if attribute.rsplit("}", 1)[-1] != "href":
				continue
			parsed = urllib.parse.urlsplit(raw_value)
			if parsed.scheme or parsed.netloc or not parsed.path:
				continue
			decoded = urllib.parse.unquote(parsed.path)
			target = posixpath.normpath(posixpath.join(posixpath.dirname(member_name), decoded))
			validate_member_name(target)
			targets.add(target)
	return frozenset(targets)


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
	manifest_root = defusedxml.ElementTree.fromstring(payloads[MANIFEST_NAME])
	manifest_entries = {entry.attrib[MANIFEST_FULL_PATH]
		for entry in manifest_root.findall(f".//{MANIFEST_FILE_ENTRY}")
		if MANIFEST_FULL_PATH in entry.attrib}
	manifest_files = {name for name in manifest_entries if name != "/" and not name.endswith("/")}
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
