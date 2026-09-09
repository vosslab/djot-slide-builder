"""Native ODP package skeleton projected from the immutable physical deck."""

# Standard Library
import hashlib
import mimetypes
import pathlib
import xml.etree.ElementTree
import zipfile

# PIP3 modules
import defusedxml.ElementTree

# Local Modules
import slide_lib.layout_content
import slide_lib.layout_model
import slide_lib.layout_primitives
import slide_lib.odp_animation
import slide_lib.odp_text
import slide_lib.odf_package
import slide_lib.presentation_theme


OFFICE_NS = "urn:oasis:names:tc:opendocument:xmlns:office:1.0"
DRAW_NS = "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
MANIFEST_NS = "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
STYLE_NS = "urn:oasis:names:tc:opendocument:xmlns:style:1.0"
TEXT_NS = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
PRESENTATION_NS = "urn:oasis:names:tc:opendocument:xmlns:presentation:1.0"
SVG_NS = "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
FO_NS = "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
XLINK_NS = "http://www.w3.org/1999/xlink"
XML_NS = "http://www.w3.org/XML/1998/namespace"
OTP_MIMETYPE = "application/vnd.oasis.opendocument.presentation-template"
_XML_DECLARATION = b'<?xml version="1.0" encoding="UTF-8"?>\n'
_FOREGROUND = "172033"
_ROLE_COLORS = {
	slide_lib.layout_primitives.StyleRole.ACCENT: "24578F",
	slide_lib.layout_primitives.StyleRole.TABLE_HEADER: "24578F",
	slide_lib.layout_primitives.StyleRole.MUTED: "526176",
	slide_lib.layout_primitives.StyleRole.DECORATION: "FFFFFF",
}

for _prefix, _namespace in (("office", OFFICE_NS), ("draw", DRAW_NS),
		("manifest", MANIFEST_NS), ("style", STYLE_NS), ("text", TEXT_NS),
		("presentation", PRESENTATION_NS), ("svg", SVG_NS), ("fo", FO_NS),
		("xlink", XLINK_NS)):
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
		theme: slide_lib.presentation_theme.PresentationTheme,
		layout_names: dict[slide_lib.layout_primitives.PresentationPageLayoutKey, str],
		picture_members: dict[tuple[str, str], str],
		font_faces: tuple[slide_lib.presentation_theme.OdfFontFace, ...] | None = None) -> bytes:
	"""Project the complete physical plan into editable native ODF objects."""
	root = xml.etree.ElementTree.Element(_qname(OFFICE_NS, "document-content"), {
		_qname(OFFICE_NS, "version"): "1.3",
	})
	xml.etree.ElementTree.SubElement(root, _qname(OFFICE_NS, "scripts"))
	fonts = xml.etree.ElementTree.SubElement(root, _qname(OFFICE_NS, "font-face-decls"))
	if font_faces is None:
		font_faces = slide_lib.presentation_theme.odf_font_faces()
	for face in font_faces:
		attributes = {
			_qname(STYLE_NS, "name"): face.odf_name,
			_qname(SVG_NS, "font-family"): face.embedded_family,
			_qname(SVG_NS, "font-weight"): "bold" if face.profile.bold else "normal",
			_qname(SVG_NS, "font-style"): "italic" if face.profile.italic else "normal",
		}
		declaration = xml.etree.ElementTree.SubElement(fonts, _qname(STYLE_NS, "font-face"),
			attributes)
		source = xml.etree.ElementTree.SubElement(declaration,
			_qname(SVG_NS, "font-face-src"))
		xml.etree.ElementTree.SubElement(source, _qname(SVG_NS, "font-face-uri"), {
			_qname(XLINK_NS, "href"): face.package_member,
		})
		uri = source[-1]
		xml.etree.ElementTree.SubElement(uri, _qname(SVG_NS, "font-face-format"), {
			_qname(SVG_NS, "string"): face.format_name,
		})
	automatic = xml.etree.ElementTree.SubElement(root, _qname(OFFICE_NS, "automatic-styles"))
	_add_page_style(automatic)
	slide_lib.odp_text.add_list_styles(automatic, deck, theme)
	body = xml.etree.ElementTree.SubElement(root, _qname(OFFICE_NS, "body"))
	presentation = xml.etree.ElementTree.SubElement(body, _qname(OFFICE_NS, "presentation"))
	for slide_index, slide in enumerate(deck.slides):
		layout_key = slide.layout.topology.key_for_canvas(deck.canvas)
		page = xml.etree.ElementTree.SubElement(presentation, _qname(DRAW_NS, "page"), {
			_qname(DRAW_NS, "name"): slide.identity.slide_id,
			_qname(DRAW_NS, "style-name"): "DjotPage",
			_qname(DRAW_NS, "master-page-name"): theme.master_name,
			_qname(PRESENTATION_NS, "presentation-page-layout-name"): layout_names[layout_key],
		})
		target_ids = _target_ids(slide, slide_index)
		for object_index, item in enumerate(sorted(slide.objects,
				key=lambda value: (value.z_index, value.reading_order, value.object_id))):
			_write_object(page, automatic, item, deck, theme, slide.identity.slide_id,
				slide_index, object_index, target_ids, picture_members)
		slide_lib.odp_animation.write_reveals(page, slide, target_ids)
		_write_notes(page, slide, deck, theme)
	return _xml_bytes(root)


#============================================
def _add_page_style(automatic: xml.etree.ElementTree.Element) -> None:
	"""Define the one visible theme-backed drawing-page style."""
	style = xml.etree.ElementTree.SubElement(automatic, _qname(STYLE_NS, "style"), {
		_qname(STYLE_NS, "name"): "DjotPage",
		_qname(STYLE_NS, "family"): "drawing-page",
	})
	xml.etree.ElementTree.SubElement(style, _qname(STYLE_NS, "drawing-page-properties"), {
		_qname(PRESENTATION_NS, "background-visible"): "true",
		_qname(PRESENTATION_NS, "background-objects-visible"): "true",
		_qname(PRESENTATION_NS, "display-page-number"): "false",
		_qname(PRESENTATION_NS, "display-footer"): "false",
		_qname(PRESENTATION_NS, "display-date-time"): "false",
	})


#============================================
def _target_ids(slide: slide_lib.layout_model.LayoutSlide, slide_index: int) -> dict[str, str]:
	"""Allocate XML IDs for every source-ordered reveal target."""
	targets = sorted((target for item in slide.objects for target in item.reveal_targets),
		key=lambda value: value.activation_order)
	identities: dict[tuple[str, tuple[int, ...]], str] = {}
	result: dict[str, str] = {}
	for target in targets:
		key = (target.object_id, target.paragraph_indexes)
		if key not in identities:
			identities[key] = f"djot-reveal-{slide_index + 1}-{len(identities) + 1}"
		result[target.target_id] = identities[key]
	return result


#============================================
def _write_object(page: xml.etree.ElementTree.Element,
		automatic: xml.etree.ElementTree.Element, item: slide_lib.layout_model.LayoutObject,
		deck: slide_lib.layout_model.LayoutDeck,
		theme: slide_lib.presentation_theme.PresentationTheme, slide_id: str,
		slide_index: int, object_index: int, target_ids: dict[str, str],
		picture_members: dict[tuple[str, str], str]) -> None:
	"""Write one plan object without recomputing its physical placement."""
	content = item.content
	style_name = f"DjotFrame{slide_index + 1}_{object_index + 1}"
	_add_frame_style(automatic, style_name, item, deck, theme)
	object_parent = page
	if isinstance(content, (slide_lib.layout_content.PictureContent,
			slide_lib.layout_content.ShapeContent)) and content.link_url is not None:
		object_parent = xml.etree.ElementTree.SubElement(page, _qname(DRAW_NS, "a"), {
			_qname(XLINK_NS, "href"): content.link_url,
			_qname(XLINK_NS, "type"): "simple",
			_qname(XLINK_NS, "show"): "new",
			_qname(XLINK_NS, "actuate"): "onRequest",
		})
	if isinstance(content, slide_lib.layout_content.ShapeContent):
		_write_shape(object_parent, automatic, item, content, deck, theme, style_name,
			slide_index, object_index, target_ids)
	elif isinstance(content, slide_lib.layout_content.TableContent):
		element = xml.etree.ElementTree.SubElement(page, _qname(DRAW_NS, "frame"),
			_frame_attributes(item, deck, theme, style_name, target_ids))
		_write_accessibility(element, item)
		slide_lib.odp_text.write_table(element, automatic, item.object_id, content,
			deck, theme, slide_index, object_index)
	else:
		element = xml.etree.ElementTree.SubElement(object_parent, _qname(DRAW_NS, "frame"),
			_frame_attributes(item, deck, theme, style_name, target_ids))
		_write_accessibility(element, item)
		if isinstance(content, slide_lib.layout_content.TextContent):
			text_box = xml.etree.ElementTree.SubElement(element, _qname(DRAW_NS, "text-box"))
			slide_lib.odp_text.write_text(text_box, automatic, content, slide_index,
				object_index, target_ids, item.reveal_targets)
		elif isinstance(content, slide_lib.layout_content.PictureContent):
			xml.etree.ElementTree.SubElement(element, _qname(DRAW_NS, "image"), {
				_qname(XLINK_NS, "href"): picture_members[(slide_id, item.object_id)],
				_qname(XLINK_NS, "type"): "simple",
				_qname(XLINK_NS, "show"): "embed",
				_qname(XLINK_NS, "actuate"): "onLoad",
			})
		else:
			raise ValueError(f"unsupported planned ODP content: {type(content).__name__}")

#============================================
def _frame_attributes(item: slide_lib.layout_model.LayoutObject,
		deck: slide_lib.layout_model.LayoutDeck,
		theme: slide_lib.presentation_theme.PresentationTheme, style_name: str,
		target_ids: dict[str, str]) -> dict[str, str]:
	"""Return geometry, role, style, and animation identity for one native frame."""
	if isinstance(item.content, slide_lib.layout_content.PictureContent):
		rectangle = item.content.placement.displayed_rectangle
	else:
		rectangle = item.rectangle
	attributes = {
		_qname(DRAW_NS, "name"): item.object_id,
		_qname(DRAW_NS, "layer"): item.layer.value,
		_qname(SVG_NS, "x"): _cm_x(rectangle.x, deck, theme),
		_qname(SVG_NS, "y"): _cm_y(rectangle.y, deck, theme),
		_qname(SVG_NS, "width"): _cm_x(rectangle.width, deck, theme),
		_qname(SVG_NS, "height"): _cm_y(rectangle.height, deck, theme),
	}
	text_placeholder = item.placeholder_kind in (slide_lib.layout_primitives.PlaceholderKind.TITLE,
		slide_lib.layout_primitives.PlaceholderKind.SUBTITLE,
		slide_lib.layout_primitives.PlaceholderKind.OUTLINE)
	presentation_style = text_placeholder or \
		item.role is slide_lib.layout_primitives.PresentationRole.OBJECT
	if presentation_style:
		attributes[_qname(PRESENTATION_NS, "style-name")] = style_name
	else:
		attributes[_qname(DRAW_NS, "style-name")] = style_name
	if item.placeholder_kind is not slide_lib.layout_primitives.PlaceholderKind.NONE:
		attributes[_qname(PRESENTATION_NS, "class")] = item.role.value
	object_targets = tuple(target for target in item.reveal_targets if not target.paragraph_indexes)
	if object_targets:
		xml_id = target_ids[object_targets[0].target_id]
		attributes[_qname(DRAW_NS, "id")] = xml_id
		attributes[_qname(XML_NS, "id")] = xml_id
	return attributes


#============================================
def _add_frame_style(automatic: xml.etree.ElementTree.Element, style_name: str,
		item: slide_lib.layout_model.LayoutObject, deck: slide_lib.layout_model.LayoutDeck,
		theme: slide_lib.presentation_theme.PresentationTheme) -> None:
	"""Define the exact frame behavior selected by the compiler."""
	attributes = {_qname(STYLE_NS, "name"): style_name}
	text_placeholder = item.placeholder_kind in (slide_lib.layout_primitives.PlaceholderKind.TITLE,
		slide_lib.layout_primitives.PlaceholderKind.SUBTITLE,
		slide_lib.layout_primitives.PlaceholderKind.OUTLINE)
	presentation_style = text_placeholder or \
		item.role is slide_lib.layout_primitives.PresentationRole.OBJECT
	if presentation_style:
		attributes[_qname(STYLE_NS, "family")] = "presentation"
		if text_placeholder:
			attributes[_qname(STYLE_NS, "parent-style-name")] = _parent_style(item, theme)
	else:
		attributes[_qname(STYLE_NS, "family")] = "graphic"
	style = xml.etree.ElementTree.SubElement(automatic, _qname(STYLE_NS, "style"), attributes)
	properties = {
		_qname(DRAW_NS, "auto-grow-height"): "false",
		_qname(DRAW_NS, "fill"): "none",
		_qname(DRAW_NS, "stroke"): "none",
	}
	if item.frame_text is not None:
		frame = item.frame_text
		properties[_qname(DRAW_NS, "fit-to-size")] = "false"
		properties[_qname(STYLE_NS, "shrink-to-fit")] = "false"
		properties[_qname(DRAW_NS, "textarea-vertical-align")] = frame.vertical_alignment.value
		properties[_qname(FO_NS, "padding-left")] = _cm_x(frame.padding.left, deck, theme)
		properties[_qname(FO_NS, "padding-right")] = _cm_x(frame.padding.right, deck, theme)
		properties[_qname(FO_NS, "padding-top")] = _cm_y(frame.padding.top, deck, theme)
		properties[_qname(FO_NS, "padding-bottom")] = _cm_y(frame.padding.bottom, deck, theme)
	if isinstance(item.content, slide_lib.layout_content.PictureContent):
		crop = item.content.placement.crop
		if crop.left or crop.top or crop.right or crop.bottom:
			properties[_qname(FO_NS, "clip")] = _clip_value(item, crop, deck, theme)
	if isinstance(item.content, slide_lib.layout_content.ShapeContent):
		shape_style = item.content.style
		properties[_qname(DRAW_NS, "fill")] = "solid"
		properties[_qname(DRAW_NS, "fill-color")] = f"#{_color_for(shape_style.fill_role)}"
		properties[_qname(DRAW_NS, "stroke")] = shape_style.line_pattern.value
		properties[_qname(SVG_NS, "stroke-color")] = f"#{_color_for(shape_style.line_role)}"
		properties[_qname(SVG_NS, "stroke-width")] = _pt(shape_style.line_width_pt)
	xml.etree.ElementTree.SubElement(style, _qname(STYLE_NS, "graphic-properties"), properties)


#============================================
def _parent_style(item: slide_lib.layout_model.LayoutObject,
		theme: slide_lib.presentation_theme.PresentationTheme) -> str:
	"""Select the shipped native presentation style for one semantic member."""
	if item.placeholder_kind is slide_lib.layout_primitives.PlaceholderKind.TITLE:
		return theme.title_style_name
	if item.placeholder_kind is slide_lib.layout_primitives.PlaceholderKind.SUBTITLE:
		return "Default-subtitle"
	return theme.outline_style_names[0]


#============================================
def _write_shape(page: xml.etree.ElementTree.Element,
		automatic: xml.etree.ElementTree.Element, item: slide_lib.layout_model.LayoutObject,
		content: slide_lib.layout_content.ShapeContent, deck: slide_lib.layout_model.LayoutDeck,
		theme: slide_lib.presentation_theme.PresentationTheme, style_name: str,
		slide_index: int, object_index: int,
		target_ids: dict[str, str]) -> xml.etree.ElementTree.Element:
	"""Write one editable rectangle, rounded rectangle, or line."""
	attributes = _frame_attributes(item, deck, theme, style_name, target_ids)
	if content.kind is slide_lib.layout_primitives.ShapeKind.LINE:
		attributes.pop(_qname(SVG_NS, "x"))
		attributes.pop(_qname(SVG_NS, "y"))
		attributes.pop(_qname(SVG_NS, "width"))
		attributes.pop(_qname(SVG_NS, "height"))
		rectangle = item.rectangle
		attributes.update({_qname(SVG_NS, "x1"): _cm_x(rectangle.x, deck, theme),
			_qname(SVG_NS, "y1"): _cm_y(rectangle.y, deck, theme),
			_qname(SVG_NS, "x2"): _cm_x(rectangle.x + rectangle.width, deck, theme),
			_qname(SVG_NS, "y2"): _cm_y(rectangle.y + rectangle.height, deck, theme)})
		element = xml.etree.ElementTree.SubElement(page, _qname(DRAW_NS, "line"), attributes)
	elif item.presentation_member_id is not None or item.reveal_targets:
		# LibreOffice retains presentation membership and object-level reveal IDs
		# on frames; it strips those semantics from imported custom shapes.
		element = xml.etree.ElementTree.SubElement(page, _qname(DRAW_NS, "frame"), attributes)
		if content.text is not None:
			text_box = xml.etree.ElementTree.SubElement(element, _qname(DRAW_NS, "text-box"))
			slide_lib.odp_text.write_text(text_box, automatic, content.text, slide_index,
				object_index, target_ids, item.reveal_targets)
	else:
		element = xml.etree.ElementTree.SubElement(page, _qname(DRAW_NS, "custom-shape"),
			attributes)
		if content.text is not None:
			slide_lib.odp_text.write_text(element, automatic, content.text, slide_index,
				object_index, target_ids, item.reveal_targets)
		shape_type = "round-rect" if content.kind is \
			slide_lib.layout_primitives.ShapeKind.ROUNDED_RECTANGLE else "rectangle"
		xml.etree.ElementTree.SubElement(element, _qname(DRAW_NS, "enhanced-geometry"), {
			_qname(SVG_NS, "viewBox"): "0 0 21600 21600",
			_qname(DRAW_NS, "type"): shape_type,
		})
	_write_accessibility(element, item)
	return element


#============================================
def _write_accessibility(element: xml.etree.ElementTree.Element,
		item: slide_lib.layout_model.LayoutObject) -> None:
	"""Expose stable object identity and meaningful text to presentation readers."""
	xml.etree.ElementTree.SubElement(element, _qname(SVG_NS, "title")).text = item.object_id
	if isinstance(item.content, slide_lib.layout_content.PictureContent):
		description = item.content.accessibility.description
	elif isinstance(item.content, slide_lib.layout_content.ShapeContent):
		description = item.content.accessibility.description
	else:
		description = item.role.value
	if description:
		xml.etree.ElementTree.SubElement(element, _qname(SVG_NS, "desc")).text = description


#============================================
def _write_notes(page: xml.etree.ElementTree.Element,
		slide: slide_lib.layout_model.LayoutSlide, deck: slide_lib.layout_model.LayoutDeck,
		theme: slide_lib.presentation_theme.PresentationTheme) -> None:
	"""Write authored speaker notes."""
	note_values = [note.text for note in slide.notes]
	if not note_values:
		return
	notes = xml.etree.ElementTree.SubElement(page, _qname(PRESENTATION_NS, "notes"))
	frame = xml.etree.ElementTree.SubElement(notes, _qname(DRAW_NS, "frame"), {
		_qname(DRAW_NS, "layer"): "layout",
		_qname(PRESENTATION_NS, "class"): "notes",
		_qname(SVG_NS, "x"): "2cm",
		_qname(SVG_NS, "y"): _cm_y(deck.canvas.height + 20, deck, theme),
		_qname(SVG_NS, "width"): _cm_x(deck.canvas.width - 160, deck, theme),
		_qname(SVG_NS, "height"): "10cm",
	})
	text_box = xml.etree.ElementTree.SubElement(frame, _qname(DRAW_NS, "text-box"))
	for value in note_values:
		xml.etree.ElementTree.SubElement(text_box, _qname(TEXT_NS, "p")).text = value


#============================================
#============================================
def _clip_value(item: slide_lib.layout_model.LayoutObject,
		crop: slide_lib.layout_primitives.CropInsets, deck: slide_lib.layout_model.LayoutDeck,
		theme: slide_lib.presentation_theme.PresentationTheme) -> str:
	"""Convert normalized source crop into ODF physical clip offsets."""
	width = item.rectangle.width / (1.0 - crop.left - crop.right)
	height = item.rectangle.height / (1.0 - crop.top - crop.bottom)
	top = _cm_y(crop.top * height, deck, theme)
	right = _cm_x(crop.right * width, deck, theme)
	bottom = _cm_y(crop.bottom * height, deck, theme)
	left = _cm_x(crop.left * width, deck, theme)
	return f"rect({top} {right} {bottom} {left})"


#============================================
def _color_for(role: slide_lib.layout_primitives.StyleRole) -> str:
	"""Return the shared resolved palette color for a semantic role."""
	return _ROLE_COLORS.get(role, _FOREGROUND)


#============================================
def _pt(value: float) -> str:
	"""Format one exact point-valued layout fact for ODF."""
	return f"{value:.4f}pt"


#============================================
def _cm_x(value: float, deck: slide_lib.layout_model.LayoutDeck,
		theme: slide_lib.presentation_theme.PresentationTheme) -> str:
	"""Convert a horizontal logical measurement to native centimeters."""
	return f"{value * theme.slide_width_cm / deck.canvas.width:.6f}cm"


#============================================
def _cm_y(value: float, deck: slide_lib.layout_model.LayoutDeck,
		theme: slide_lib.presentation_theme.PresentationTheme) -> str:
	"""Convert a vertical logical measurement to native centimeters."""
	return f"{value * theme.slide_height_cm / deck.canvas.height:.6f}cm"


#============================================
def _layout_names(deck: slide_lib.layout_model.LayoutDeck) -> dict[
		slide_lib.layout_primitives.PresentationPageLayoutKey, str]:
	"""Assign deterministic document-local names to canonical topology keys."""
	result = {key: f"DjotLayout{index + 1}"
		for index, key in enumerate(deck.presentation_page_layouts)}
	return result


#============================================
def _styles_xml(content: bytes, deck: slide_lib.layout_model.LayoutDeck,
		theme: slide_lib.presentation_theme.PresentationTheme,
		layout_names: dict[slide_lib.layout_primitives.PresentationPageLayoutKey, str]) -> bytes:
	"""Append compiler-selected page-layout classifiers to the template styles."""
	# ASVS 1.5.1: parse retained template XML with external entities disabled.
	root = defusedxml.ElementTree.fromstring(content)
	styles = root.find(_qname(OFFICE_NS, "styles"))
	if styles is None:
		raise ValueError("template styles.xml is missing office:styles")
	for key in deck.presentation_page_layouts:
		layout = xml.etree.ElementTree.SubElement(styles,
			_qname(STYLE_NS, "presentation-page-layout"), {
				_qname(STYLE_NS, "name"): layout_names[key],
			})
		if key.libreoffice_layout is None:
			placeholders = tuple((member.role.value, member.rectangle) for member in key.members)
		else:
			placeholders = tuple((member.object_name.value, member.rectangle)
				for member in key.libreoffice_layout.placeholders)
		for object_name, rectangle in placeholders:
			xml.etree.ElementTree.SubElement(layout,
				_qname(PRESENTATION_NS, "placeholder"), {
					_qname(PRESENTATION_NS, "object"): object_name,
					_qname(SVG_NS, "x"): _cm_x(rectangle.x, deck, theme),
					_qname(SVG_NS, "y"): _cm_y(rectangle.y, deck, theme),
					_qname(SVG_NS, "width"): _cm_x(rectangle.width, deck, theme),
					_qname(SVG_NS, "height"): _cm_y(rectangle.height, deck, theme),
				})
	return _xml_bytes(root)


#============================================
def _picture_payloads(deck: slide_lib.layout_model.LayoutDeck) -> tuple[dict[str, bytes],
		dict[tuple[str, str], str]]:
	"""Read bounded compiler-approved images into deterministic package members."""
	payloads: dict[str, bytes] = {}
	members: dict[tuple[str, str], str] = {}
	for slide in deck.slides:
		for item in slide.objects:
			if not isinstance(item.content, slide_lib.layout_content.PictureContent):
				continue
			path = pathlib.Path(item.content.source_path)
			if not path.is_absolute():
				path = deck.identity.source_path.parent / path
			path = path.resolve()
			if not path.is_file():
				raise ValueError(f"planned picture source is missing: {item.content.source_path}")
			if path.stat().st_size > slide_lib.odf_package.MAX_MEMBER_BYTES:
				raise ValueError(f"planned picture exceeds package member limit: {item.content.source_path}")
			content = path.read_bytes()
			digest = hashlib.sha256(content).hexdigest()
			suffix = path.suffix.lower()
			if not suffix or mimetypes.guess_type(path.name)[0] is None:
				raise ValueError(f"planned picture has an unsupported file type: {item.content.source_path}")
			member_name = f"Pictures/{digest[:24]}{suffix}"
			payloads[member_name] = content
			members[(slide.identity.slide_id, item.object_id)] = member_name
	return payloads, members


#============================================
def _font_payloads(font_faces: tuple[slide_lib.presentation_theme.OdfFontFace, ...]) \
		-> tuple[dict[str, bytes], dict[str, str]]:
	"""Read the already-validated bundled faces into stable ODP package members."""
	payloads = {}
	media_types = {}
	for face in font_faces:
		payloads[face.package_member] = slide_lib.presentation_theme.embedded_font_payload(face)
		media_types[face.package_member] = face.media_type
	return payloads, media_types


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
		if not member_name.endswith(".xml"):
			continue
		for target in slide_lib.odf_package.xml_reference_targets(member_name, content):
			if target not in all_payloads:
				raise ValueError(f"template XML reference is missing member: {target}")
			if target not in retained:
				retained.add(target)
				pending.append(target)
	return {name: all_payloads[name] for name in retained}


#============================================
def _manifest_xml(payloads: dict[str, bytes], media_types: dict[str, str] | None = None) -> bytes:
	"""Reconcile the ODF manifest with the exact retained/generated member set."""
	root = xml.etree.ElementTree.Element(_qname(MANIFEST_NS, "manifest"), {
		_qname(MANIFEST_NS, "version"): "1.3",
	})
	xml.etree.ElementTree.SubElement(root, _qname(MANIFEST_NS, "file-entry"), {
		_qname(MANIFEST_NS, "full-path"): "/",
		_qname(MANIFEST_NS, "media-type"): slide_lib.odf_package.ODP_MIMETYPE,
		_qname(MANIFEST_NS, "version"): "1.3",
	})
	if media_types is None:
		media_types = {}
	for name in sorted(set(payloads) - {"mimetype", slide_lib.odf_package.MANIFEST_NAME}):
		xml.etree.ElementTree.SubElement(root, _qname(MANIFEST_NS, "file-entry"), {
			_qname(MANIFEST_NS, "full-path"): name,
			_qname(MANIFEST_NS, "media-type"): media_types.get(name, _media_type(name)),
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
	layout_names = _layout_names(deck)
	picture_payloads, picture_members = _picture_payloads(deck)
	font_faces = slide_lib.presentation_theme.odf_font_faces()
	font_payloads, font_media_types = _font_payloads(font_faces)
	license_payloads, license_media_types = slide_lib.presentation_theme.odf_font_license_payloads()
	payloads["mimetype"] = slide_lib.odf_package.ODP_MIMETYPE.encode("ascii")
	payloads["styles.xml"] = _styles_xml(payloads["styles.xml"], deck, theme, layout_names)
	payloads.update(picture_payloads)
	payloads.update(font_payloads)
	payloads.update(license_payloads)
	payloads["content.xml"] = _content_xml(deck, theme, layout_names, picture_members, font_faces)
	payloads[slide_lib.odf_package.MANIFEST_NAME] = _manifest_xml(payloads,
		font_media_types | license_media_types)
	return slide_lib.odf_package.publish_odp(destination, payloads,
		frozenset(picture_payloads) | frozenset(font_payloads))
