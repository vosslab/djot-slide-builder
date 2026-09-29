"""Preserve embedded GDI figures as component images during ODP import."""

# Standard Library
import pathlib
import tempfile
import xml.etree.ElementTree as ET
import zipfile

# local repo modules
import slide_lib.libreoffice
import slide_lib.odf_package


METAFILE_SUFFIXES = frozenset({".svm", ".emf", ".wmf"})
RASTER_SUFFIXES = frozenset({".png", ".jpg", ".jpeg", ".gif"})
DRAW = "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
XLINK = "http://www.w3.org/1999/xlink"


#============================================
def frame_image(frame: ET.Element) -> ET.Element | None:
	"""Prefer an embedded raster alternative to a metafile in the same ODF frame."""
	images = frame.findall(f"{{{DRAW}}}image")
	if not images:
		return None
	first = images[0]
	suffix = pathlib.PurePosixPath(first.get(f"{{{XLINK}}}href", "")).suffix.lower()
	if suffix in METAFILE_SUFFIXES:
		for image in images[1:]:
			reference = image.get(f"{{{XLINK}}}href", "")
			if slide_lib.odf_package.package_reference_target("content.xml", reference) is not None \
					and pathlib.PurePosixPath(reference).suffix.lower() in RASTER_SUFFIXES:
				return image
	return first


#============================================
def validate_metafile(blob: bytes, suffix: str) -> None:
	"""Admit bounded recognizable GDI headers before the LibreOffice decoder."""
	# ASVS 5.2.1 and 5.2.2: reject oversized or mislabeled component files.
	if len(blob) > slide_lib.odf_package.MAX_MEMBER_BYTES:
		raise ValueError("ODP metafile exceeds the per-image size limit")
	valid = False
	if suffix == ".svm":
		valid = len(blob) >= 12 and blob.startswith(b"VCLMTF")
	elif suffix == ".emf":
		valid = len(blob) >= 88 and blob[:4] == b"\x01\x00\x00\x00" \
			and blob[40:44] == b" EMF"
	elif suffix == ".wmf":
		valid = len(blob) >= 18 and (blob.startswith(b"\xd7\xcd\xc6\x9a") \
			or blob[:4] in {b"\x01\x00\x09\x00", b"\x02\x00\x09\x00"})
	if not valid:
		raise ValueError(f"unsupported ODP image type or invalid metafile header: {suffix}")


#============================================
def drawing_package(blob: bytes, suffix: str, width: float, height: float,
		output_path: pathlib.Path) -> None:
	"""Wrap only the component in a full-bleed Draw page, avoiding default-page padding."""
	namespaces = {
		"office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
		"style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
		"draw": DRAW,
		"svg": "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0",
		"fo": "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0",
		"xlink": XLINK,
	}
	declarations = " ".join(f'xmlns:{prefix}="{uri}"' for prefix, uri in namespaces.items())
	# The caller's admitted geometry is numeric; package paths are generated internally.
	# ASVS 1.2.1 and 5.3.2: only trusted names and numeric extents enter generated XML.
	member = f"Pictures/figure{suffix}"
	content = f'<office:document-content {declarations} office:version="1.2">'
	content += '<office:body><office:drawing><draw:page draw:name="figure" draw:master-page-name="FigureMaster">'
	content += f'<draw:frame svg:x="0pt" svg:y="0pt" svg:width="{width}pt" svg:height="{height}pt">'
	content += f'<draw:image xlink:href="{member}" xlink:type="simple"/>'
	content += '</draw:frame></draw:page></office:drawing></office:body></office:document-content>'
	styles = f'<office:document-styles {declarations} office:version="1.2">'
	styles += '<office:styles/><office:automatic-styles><style:page-layout style:name="figure">'
	styles += f'<style:page-layout-properties fo:page-width="{width * 2.54 / 72}cm" fo:page-height="{height * 2.54 / 72}cm" fo:margin="0cm" style:print-orientation="landscape"/>'
	styles += '</style:page-layout></office:automatic-styles><office:master-styles>'
	styles += '<style:master-page style:name="FigureMaster" style:page-layout-name="figure"/>'
	styles += '</office:master-styles></office:document-styles>'
	mimetype = "application/vnd.oasis.opendocument.graphics"
	manifest = '<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">'
	for name, media_type in (("/", mimetype), ("content.xml", "text/xml"),
			("styles.xml", "text/xml"), (member, "")):
		manifest += f'<manifest:file-entry manifest:full-path="{name}" manifest:media-type="{media_type}"/>'
	manifest += '</manifest:manifest>'
	with zipfile.ZipFile(output_path, "w") as archive:
		archive.writestr("mimetype", mimetype, compress_type=zipfile.ZIP_STORED)
		archive.writestr("content.xml", content)
		archive.writestr("styles.xml", styles)
		archive.writestr("META-INF/manifest.xml", manifest)
		archive.writestr(member, blob)


#============================================
def raster_image(blob: bytes, suffix: str,
		geometry: tuple[float, float, float, float]) -> tuple[bytes, str]:
	"""Convert a preview-less metafile using the shared sequential LibreOffice workflow."""
	if suffix not in METAFILE_SUFFIXES:
		return blob, suffix
	validate_metafile(blob, suffix)
	_left, _top, width, height = geometry
	# Bound the PNG export to about 1600 pixels along its longest edge at 96 dpi.
	scale = 1200.0 / max(width, height)
	with tempfile.TemporaryDirectory(prefix="odp_metafile_") as temp_dir:
		root = pathlib.Path(temp_dir)
		input_path = root / "figure.odg"
		drawing_package(blob, suffix, width * scale, height * scale, input_path)
		output_path = slide_lib.libreoffice.convert_file(input_path, root, "png")
		if output_path.stat().st_size > slide_lib.odf_package.MAX_MEMBER_BYTES:
			raise ValueError("converted ODP metafile exceeds the per-image size limit")
		converted = output_path.read_bytes()
	# The reader decodes and applies aggregate raster budgets before staging this PNG.
	return converted, ".png"
