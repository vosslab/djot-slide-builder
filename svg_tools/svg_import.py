"""Import static Lucide and Matplotlib SVGs as isolated, clipped parts."""

import math
import re
import xml.etree.ElementTree as ET

import defusedxml.ElementTree
import defusedxml.common

import svg_tools.parts

SVG = 'http://www.w3.org/2000/svg'
XLINK = 'http://www.w3.org/1999/xlink'
_ELEMENTS = frozenset('svg g defs path rect circle ellipse line polyline polygon text tspan use '
	'clipPath mask pattern linearGradient radialGradient stop title desc metadata'.split())
_METADATA = frozenset(('http://www.w3.org/1999/02/22-rdf-syntax-ns#',
	'http://purl.org/dc/elements/1.1/', 'http://creativecommons.org/ns#'))
_DOCTYPE = re.compile(r'<!DOCTYPE\s+svg\s+PUBLIC\s+["\']-//W3C//DTD SVG 1\.1//EN["\']\s+'
	r'["\']http://www\.w3\.org/Graphics/SVG/1\.1/DTD/svg11\.dtd["\']\s*>', re.I)
_URL = re.compile(r'url\(\s*["\']?#([A-Za-z_][\w.:-]*)["\']?\s*\)', re.I)


#============================================
def import_svg(markup: str | bytes, *, name: str, size: float | None = None) -> svg_tools.parts.SvgPart:
	"""Import a static SVG; size optionally sets its width in local coordinates.

	The returned bounds are the clipped viewport, not a tight paint measurement.
	Use distinct names for separately placed imports, or compose with parts.group.
	"""
	if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.-]*', name):
		raise ValueError('Name must be an SVG identifier')
	if isinstance(markup, bytes):
		try:
			markup = markup.decode('utf-8')
		except UnicodeDecodeError as exc:
			raise ValueError('SVG must be UTF-8') from exc
	if not isinstance(markup, str):
		raise TypeError('SVG markup must be str or bytes')
	markup = _DOCTYPE.sub('', markup)
	try:
		parser = defusedxml.ElementTree.DefusedXMLParser(
			target=ET.TreeBuilder(insert_comments=True), forbid_dtd=True)
		parser.feed(markup)
		root = parser.close()
	except (ET.ParseError, defusedxml.common.DefusedXmlException) as exc:
		raise ValueError('Invalid or unsafe SVG XML') from exc
	if root.tag not in (f'{{{SVG}}}svg', 'svg'):
		raise ValueError('Expected an SVG root')
	# Preserve producer license comments that precede the document element.
	prologue = markup[:markup.find('<svg')] if '<svg' in markup else ''
	for comment in reversed(re.findall(r'<!--(.*?)-->', prologue, re.S)):
		root.insert(0, ET.Comment(comment))
	try:
		viewbox = [float(value) for value in re.split(r'[\s,]+', root.attrib['viewBox'].strip())]
		if len(viewbox) != 4 or not all(math.isfinite(v) for v in viewbox) or min(viewbox[2:]) <= 0:
			raise ValueError
	except (KeyError, ValueError) as exc:
		raise ValueError('SVG needs a finite positive viewBox') from exc
	width = viewbox[2] if size is None else size
	if not isinstance(width, (int, float)) or not math.isfinite(width) or width <= 0:
		raise ValueError('Size must be finite and positive')
	height = width * viewbox[3] / viewbox[2]
	if not math.isfinite(height) or height <= 0:
		raise ValueError('Viewport dimensions must be finite and positive')

	styles = []
	for parent in root.iter():
		for child in list(parent):
			if child.tag in (f'{{{SVG}}}style', 'style'):
				match = re.fullmatch(r'\s*\*\s*\{\s*(.*?)\s*\}\s*', child.text or '', re.S)
				if child.attrib.keys() - {'type'} or child.attrib.get('type', 'text/css') != 'text/css' or not match or len(child):
					raise ValueError('Unsupported SVG stylesheet')
				declarations = match.group(1)
				if not re.fullmatch(r'(?:\s*stroke-line(?:join|cap)\s*:\s*(?:round|butt|square|miter|bevel)\s*;?\s*)+', declarations):
					raise ValueError('Unsupported SVG stylesheet')
				styles.append(declarations.rstrip('; ') + ';')
				parent.remove(child)

	ids = set()
	references = []
	def validate(element: ET.Element, metadata: bool = False) -> None:
		tag = element.tag
		if tag is ET.Comment:
			return
		namespace, local = (tag[1:].split('}', 1) if tag.startswith('{') else ('', tag))
		if metadata and namespace in _METADATA:
			pass
		elif namespace not in ('', SVG) or local not in _ELEMENTS:
			raise ValueError(f'Unsupported SVG element: {local}')
		metadata = metadata or local == 'metadata'
		for key, value in element.attrib.items():
			attr = key.split('}')[-1]
			if key == '{http://www.w3.org/XML/1998/namespace}base' or attr.lower().startswith('on') or '\\' in value or '/*' in value:
				raise ValueError('Unsafe SVG attribute')
			if attr == 'id':
				if not re.fullmatch(r'[A-Za-z_][\w.:-]*', value) or value in ids:
					raise ValueError('Invalid or duplicate SVG ID')
				ids.add(value)
			if attr in ('href', 'src'):
				if not re.fullmatch(r'#[A-Za-z_][\w.:-]*', value):
					raise ValueError('Only local SVG references are supported')
				references.append(value[1:])
			if attr in ('aria-labelledby', 'aria-describedby'):
				references.extend(value.split())
			if not metadata:
				refs = _URL.findall(value)
				if re.search(r'url\s*\(', _URL.sub('', value), re.I) or re.search(r'(?:https?:|data:|javascript:|@import|expression\s*\()', value, re.I):
					raise ValueError('External or unsafe SVG resource')
				references.extend(refs)
		if styles and not metadata:
			element.set('style', ''.join(styles) + element.attrib.get('style', ''))
		for child in element:
			validate(child, metadata)
	validate(root)
	if not set(references) <= ids:
		raise ValueError('SVG contains an unresolved local reference')
	root.set('x', '0')
	root.set('y', '0')
	root.set('width', str(width))
	root.set('height', str(height))
	# Inline style wins over any original overflow attribute or stylesheet.
	root.set('style', root.attrib.get('style', '') + ';overflow:hidden')
	ET.register_namespace('xlink', XLINK)
	fragment = svg_tools.parts.namespace_ids(ET.tostring(root, encoding='unicode'), name)
	return svg_tools.parts.SvgPart(fragment, (0, 0, width, height), {})
