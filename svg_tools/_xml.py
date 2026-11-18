"""Scoped XML parsing for SVG fragments and static source files."""

# Standard Library
import re
import pathlib

# PIP3 modules
import lxml.etree


SVG = 'http://www.w3.org/2000/svg'
XLINK = 'http://www.w3.org/1999/xlink'
_SVG11_DOCTYPE = re.compile(rb'<!DOCTYPE\s+svg\s+PUBLIC\s+["\']-//W3C//DTD SVG 1\.1//EN["\']\s+'
	rb'["\']http://www\.w3\.org/Graphics/SVG/1\.1/DTD/svg11\.dtd["\']\s*>', re.I)


#============================================
def parse(markup: str | bytes) -> lxml.etree._Element:
	"""Parse XML with entity expansion and external resource loading disabled."""
	# ASVS 1.5.1: parse each input with a restrictive, local parser.
	encoding = 'UTF-8' if isinstance(markup, str) else None
	parser = lxml.etree.XMLParser(encoding=encoding, resolve_entities=False, load_dtd=False,
		no_network=True, remove_pis=True)
	payload = markup.encode('utf-8') if isinstance(markup, str) else markup
	root = lxml.etree.fromstring(payload, parser)
	if root.getroottree().docinfo.doctype:
		raise ValueError('SVG XML document types are forbidden')
	return root


#============================================
def parse_document(markup: str | bytes) -> lxml.etree._Element:
	"""Accept the stock SVG 1.1 declaration used by Matplotlib without loading it."""
	if isinstance(markup, str):
		markup = _SVG11_DOCTYPE.sub(b'', markup.encode('utf-8')).decode('utf-8')
	else:
		markup = _SVG11_DOCTYPE.sub(b'', markup)
	return parse(markup)


#============================================
def read(path: pathlib.Path | str) -> lxml.etree._Element:
	"""Read a local SVG source using the shared parser policy."""
	return parse_document(pathlib.Path(path).read_bytes())
