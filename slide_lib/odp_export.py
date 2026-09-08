"""Native ODP package skeleton projected from the immutable physical deck."""

# Standard Library
import mimetypes
import pathlib
import xml.etree.ElementTree
import zipfile

# PIP3 modules
# Local Modules
import slide_lib.layout_model
import slide_lib.odf_package
import slide_lib.presentation_theme


OFFICE_NS = "urn:oasis:names:tc:opendocument:xmlns:office:1.0"
DRAW_NS = "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
MANIFEST_NS = "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
OTP_MIMETYPE = "application/vnd.oasis.opendocument.presentation-template"
_XML_DECLARATION = b'<?xml version="1.0" encoding="UTF-8"?>\n'

for _prefix, _namespace in (("office", OFFICE_NS), ("draw", DRAW_NS),
		("manifest", MANIFEST_NS)):
	xml.etree.ElementTree.register_namespace(_prefix, _namespace)


#============================================
def _qname(namespace: str, local_name: str) -> str:
	"""Build one ElementTree-qualified name."""
	return f"{{{namespace}}}{local_name}"


#============================================
def _xml_bytes(root: xml.etree.ElementTree.Element) -> bytes:
	"""Return deterministic UTF-8 XML with its ODF declaration."""
	return _XML_DECLARATION + xml.etree.ElementTree.tostring(root, encoding="utf-8")


#============================================
def _content_xml(deck: slide_lib.layout_model.LayoutDeck,
		theme: slide_lib.presentation_theme.PresentationTheme) -> bytes:
	"""Create ODF 1.3 page containers; frame/content projection belongs to WP-O2/O3."""
	root = xml.etree.ElementTree.Element(_qname(OFFICE_NS, "document-content"), {
		_qname(OFFICE_NS, "version"): "1.3",
	})
	xml.etree.ElementTree.SubElement(root, _qname(OFFICE_NS, "automatic-styles"))
	body = xml.etree.ElementTree.SubElement(root, _qname(OFFICE_NS, "body"))
	presentation = xml.etree.ElementTree.SubElement(body, _qname(OFFICE_NS, "presentation"))
	for slide in deck.slides:
		xml.etree.ElementTree.SubElement(presentation, _qname(DRAW_NS, "page"), {
			_qname(DRAW_NS, "name"): slide.identity.slide_id,
			_qname(DRAW_NS, "master-page-name"): theme.master_name,
		})
	return _xml_bytes(root)


#============================================
def _media_type(member_name: str) -> str:
	"""Choose a stable manifest media type for retained package members."""
	if member_name.endswith(".xml"):
		return "text/xml"
	media_type, _encoding = mimetypes.guess_type(member_name)
	return media_type or "application/octet-stream"


#============================================
def _template_payloads(template_path: pathlib.Path) -> dict[str, bytes]:
	"""Retain required package XML and resources reachable from retained XML."""
	with zipfile.ZipFile(template_path) as archive:
		all_payloads = {info.filename: archive.read(info.filename) for info in archive.infolist()
			if not info.is_dir()}
	retained = {"styles.xml", "settings.xml", "meta.xml"}
	pending = list(retained)
	while pending:
		member_name = pending.pop()
		content = all_payloads.get(member_name)
		if content is None:
			raise ValueError(f"template is missing required member: {member_name}")
		for target in slide_lib.odf_package.xml_reference_targets(member_name, content):
			if target not in all_payloads:
				raise ValueError(f"template XML reference is missing member: {target}")
			if target not in retained:
				retained.add(target)
				pending.append(target)
	return {name: all_payloads[name] for name in retained}


#============================================
def _manifest_xml(payloads: dict[str, bytes]) -> bytes:
	"""Reconcile the ODF manifest with the exact retained/generated member set."""
	root = xml.etree.ElementTree.Element(_qname(MANIFEST_NS, "manifest"), {
		_qname(MANIFEST_NS, "version"): "1.3",
	})
	xml.etree.ElementTree.SubElement(root, _qname(MANIFEST_NS, "file-entry"), {
		_qname(MANIFEST_NS, "full-path"): "/",
		_qname(MANIFEST_NS, "media-type"): slide_lib.odf_package.ODP_MIMETYPE,
		_qname(MANIFEST_NS, "version"): "1.3",
	})
	for name in sorted(set(payloads) - {"mimetype", slide_lib.odf_package.MANIFEST_NAME}):
		xml.etree.ElementTree.SubElement(root, _qname(MANIFEST_NS, "file-entry"), {
			_qname(MANIFEST_NS, "full-path"): name,
			_qname(MANIFEST_NS, "media-type"): _media_type(name),
		})
	return _xml_bytes(root)


#============================================
def write_odp(deck: slide_lib.layout_model.LayoutDeck,
		theme: slide_lib.presentation_theme.PresentationTheme,
		destination: pathlib.Path) -> pathlib.Path:
	"""Atomically write the native ODP package base for a compiled physical deck."""
	if not isinstance(deck, slide_lib.layout_model.LayoutDeck):
		raise TypeError("ODP writer requires a LayoutDeck")
	if not isinstance(theme, slide_lib.presentation_theme.PresentationTheme):
		raise TypeError("ODP writer requires a PresentationTheme")
	slide_lib.odf_package.validate_package(theme.template_path, ".otp", OTP_MIMETYPE,
		slide_lib.odf_package.REQUIRED_ODP_MEMBERS)
	payloads = _template_payloads(theme.template_path)
	payloads["mimetype"] = slide_lib.odf_package.ODP_MIMETYPE.encode("ascii")
	payloads["content.xml"] = _content_xml(deck, theme)
	payloads[slide_lib.odf_package.MANIFEST_NAME] = _manifest_xml(payloads)
	return slide_lib.odf_package.publish_odp(destination, payloads)
