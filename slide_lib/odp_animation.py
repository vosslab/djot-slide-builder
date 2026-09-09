"""Project format-neutral reveal targets into native ODF/SMIL timing trees."""

import xml.etree.ElementTree

import slide_lib.layout_model


ANIMATION_NS = "urn:oasis:names:tc:opendocument:xmlns:animation:1.0"
PRESENTATION_NS = "urn:oasis:names:tc:opendocument:xmlns:presentation:1.0"
SMIL_NS = "urn:oasis:names:tc:opendocument:xmlns:smil-compatible:1.0"

for _prefix, _namespace in (("anim", ANIMATION_NS),
		("presentation", PRESENTATION_NS), ("smil", SMIL_NS)):
	xml.etree.ElementTree.register_namespace(_prefix, _namespace)


#============================================
def _qname(namespace: str, local_name: str) -> str:
	"""Build one ElementTree-qualified name."""
	return f"{{{namespace}}}{local_name}"


#============================================
def write_reveals(page: xml.etree.ElementTree.Element,
		slide: slide_lib.layout_model.LayoutSlide, target_ids: dict[str, str]) -> None:
	"""Project ordered on-click appear and fade effects into native ODF/SMIL.

	Args:
		page: ODF page that receives the timing tree.
		slide: Physical layout slide containing source-ordered reveal targets.
		target_ids: Mapping from plan target identifiers to ODF XML identifiers.

	Raises:
		KeyError: A reveal target has no serialized ODF identifier.
		ValueError: The plan contains an unsupported reveal effect.
	"""
	targets = sorted((target for item in slide.objects for target in item.reveal_targets),
		key=lambda value: value.activation_order)
	if not targets:
		return
	root = xml.etree.ElementTree.SubElement(page, _qname(ANIMATION_NS, "par"), {
		_qname(PRESENTATION_NS, "node-type"): "timing-root",
	})
	sequence = xml.etree.ElementTree.SubElement(root, _qname(ANIMATION_NS, "seq"), {
		_qname(PRESENTATION_NS, "node-type"): "main-sequence",
		_qname(SMIL_NS, "dur"): "indefinite",
	})
	for target in targets:
		click = xml.etree.ElementTree.SubElement(sequence, _qname(ANIMATION_NS, "par"), {
			_qname(PRESENTATION_NS, "node-type"): "on-click",
			_qname(SMIL_NS, "begin"): "next",
			_qname(SMIL_NS, "fill"): "hold",
		})
		attributes = {
			_qname(SMIL_NS, "targetElement"): target_ids[target.target_id],
			_qname(SMIL_NS, "dur"): "0.001s" if target.reveal.effect.value == "appear" else "1s",
			_qname(SMIL_NS, "fill"): "hold",
		}
		if target.reveal.effect.value == "appear":
			attributes.update({_qname(SMIL_NS, "attributeName"): "visibility",
				_qname(SMIL_NS, "to"): "visible"})
			xml.etree.ElementTree.SubElement(click, _qname(ANIMATION_NS, "set"), attributes)
		elif target.reveal.effect.value == "fade":
			attributes.update({_qname(SMIL_NS, "type"): "fade",
				_qname(SMIL_NS, "subtype"): "crossfade"})
			xml.etree.ElementTree.SubElement(click,
				_qname(ANIMATION_NS, "transitionFilter"), attributes)
		else:
			raise ValueError(f"unsupported ODP reveal effect: {target.reveal.effect.value}")
