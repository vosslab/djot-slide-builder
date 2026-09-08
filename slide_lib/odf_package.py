"""Bounded validation shared by OpenDocument readers and theme writers."""

# Standard Library
import stat
import pathlib
import zipfile

# PIP3 modules
import defusedxml.ElementTree


MAX_INPUT_BYTES = 256 * 1024 * 1024
MAX_MEMBER_BYTES = 128 * 1024 * 1024
MAX_UNPACKED_BYTES = 512 * 1024 * 1024
MAX_ARCHIVE_MEMBERS = 2000


#============================================
def validate_member_name(member_name: str) -> None:
	"""Reject absolute and traversal paths in an OpenDocument archive."""
	# ASVS 5.3.3: archive paths are data and never filesystem destinations.
	normalized = member_name.replace("\\", "/")
	parts = pathlib.PurePosixPath(normalized).parts
	if normalized.startswith("/") or ".." in parts:
		raise ValueError(f"unsafe archive member path: {member_name}")


#============================================
def validate_package(input_path: pathlib.Path, expected_suffix: str,
		expected_mimetype: str, required_members: frozenset[str]) -> list[zipfile.ZipInfo]:
	"""Validate one bounded OpenDocument ZIP package and its XML members."""
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
