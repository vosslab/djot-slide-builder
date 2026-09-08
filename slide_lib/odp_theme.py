"""Apply the authoritative ODP template master to generated native slides."""

# Standard Library
import os
import re
import pathlib
import zipfile
import tempfile

# PIP3 modules
import defusedxml.ElementTree

# local repo modules
import slide_lib.odf_package
import slide_lib.presentation_theme


ODP_MIMETYPE = "application/vnd.oasis.opendocument.presentation"
MASTER_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+$")
DRAW_PAGE = "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}page"
DRAW_MASTER_PAGE_NAME = "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}master-page-name"


class OdpThemeError(ValueError):
	"""Report an ODP package that cannot accept the authoritative master."""


#============================================
def themed_content(content_bytes: bytes, master_name: str) -> bytes:
	"""Retarget every generated page and notes style to one template master."""
	if MASTER_NAME_PATTERN.fullmatch(master_name) is None:
		raise OdpThemeError("template master name contains unsupported characters")
	# ASVS 1.5.1: inspect page attributes through restrictive XML parsing first.
	root = defusedxml.ElementTree.fromstring(content_bytes)
	pages = root.findall(f".//{DRAW_PAGE}")
	if not pages:
		raise OdpThemeError("generated ODP contains no presentation pages")
	old_master_names = {page.attrib[DRAW_MASTER_PAGE_NAME] for page in pages}
	if any(MASTER_NAME_PATTERN.fullmatch(name) is None for name in old_master_names):
		raise OdpThemeError("generated ODP master name contains unsupported characters")
	replacement = f'draw:master-page-name="{master_name}"'.encode("ascii")
	content_bytes, replacement_count = re.subn(
		br'draw:master-page-name="[A-Za-z0-9_.-]+"', replacement, content_bytes,
	)
	if replacement_count != len(pages):
		raise OdpThemeError("generated ODP page masters could not be retargeted exactly once")
	for old_master_name in old_master_names:
		old_notes = f'style:parent-style-name="{old_master_name}-notes"'.encode("ascii")
		new_notes = f'style:parent-style-name="{master_name}-notes"'.encode("ascii")
		content_bytes = content_bytes.replace(old_notes, new_notes)
	return content_bytes


#============================================
def apply_template_master(input_path: pathlib.Path, output_path: pathlib.Path,
		template_path: pathlib.Path | None = None) -> pathlib.Path:
	"""Publish one generated ODP with the validated template styles and master."""
	resolved_input = input_path.resolve()
	resolved_output = output_path.resolve()
	selected_template = template_path or slide_lib.presentation_theme.DEFAULT_TEMPLATE_PATH
	theme = slide_lib.presentation_theme.load_theme(selected_template)
	required = frozenset({"mimetype", "content.xml", "styles.xml"})
	members = slide_lib.odf_package.validate_package(
		resolved_input, ".odp", ODP_MIMETYPE, required,
	)
	if resolved_output.suffix.lower() != ".odp":
		raise OdpThemeError("themed output must use the .odp extension")
	resolved_output.parent.mkdir(parents=True, exist_ok=True)
	with zipfile.ZipFile(resolved_input) as source_archive:
		content_bytes = themed_content(source_archive.read("content.xml"), theme.master_name)
		with zipfile.ZipFile(theme.template_path) as template_archive:
			styles_bytes = template_archive.read("styles.xml")
		with tempfile.TemporaryDirectory(
			prefix=".odp_theme.", dir=resolved_output.parent,
		) as temporary_name:
			staging_path = pathlib.Path(temporary_name) / resolved_output.name
			with zipfile.ZipFile(staging_path, "w") as destination_archive:
				# ASVS 5.3.2: only validated member names from the generated package are written.
				for member in members:
					data = source_archive.read(member.filename)
					if member.filename == "content.xml":
						data = content_bytes
					elif member.filename == "styles.xml":
						data = styles_bytes
					destination_archive.writestr(member, data)
			# ASVS 16.5.3: publish only after the complete staged package validates.
			slide_lib.odf_package.validate_package(staging_path, ".odp", ODP_MIMETYPE, required)
			os.replace(staging_path, resolved_output)
	return resolved_output
