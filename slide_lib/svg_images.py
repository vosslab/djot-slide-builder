"""Intrinsic sizing for self-contained SVG component images."""

import math
import pathlib
import re

import slide_lib.odf_package


def dimensions(path: pathlib.Path) -> tuple[float, float]:
	"""Read an SVG viewport without rasterizing or resolving external resources."""
	return dimensions_blob(path.read_bytes(), str(path))


def dimensions_blob(blob: bytes, source: str) -> tuple[float, float]:
	"""Validate self-contained SVG bytes and return their intrinsic dimensions."""
	path = source
	root = slide_lib.odf_package.parse_xml(blob, source)
	slide_lib.odf_package.validate_xml_tree(root, source)
	if root.tag != "{http://www.w3.org/2000/svg}svg":
		raise ValueError(f"{path}: expected an SVG root")
	for element in root.iter():
		if element.tag in {"{http://www.w3.org/2000/svg}script",
				"{http://www.w3.org/2000/svg}foreignObject"}:
			raise ValueError(f"{path}: SVG components must be static")
		for name, value in element.attrib.items():
			if name.rsplit("}", 1)[-1].lower().startswith("on"):
				raise ValueError(f"{path}: SVG components must be static")
			if name.rsplit("}", 1)[-1] == "href" and not value.startswith((
					"#", "data:image/png;base64,", "data:image/jpeg;base64,")):
				raise ValueError(f"{path}: SVG resources must be embedded")
			_check_css_resources(value, path)
		if element.tag == "{http://www.w3.org/2000/svg}style":
			_check_css_resources(element.text or "", path)
	width, height = root.get("width"), root.get("height")
	if width is not None and height is not None:
		result = (_length(width, path), _length(height, path))
	else:
		viewbox = root.get("viewBox", "").replace(",", " ").split()
		if len(viewbox) != 4:
			raise ValueError(f"{path}: SVG requires dimensions or a four-number viewBox")
		values = tuple(float(value) for value in viewbox)
		if not all(math.isfinite(value) for value in values):
			raise ValueError(f"{path}: SVG viewBox must be finite")
		result = values[2:]
	if any(not math.isfinite(value) or value <= 0 for value in result):
		raise ValueError(f"{path}: SVG dimensions must be finite and positive")
	return result


def _check_css_resources(value: str, path: str) -> None:
	"""Allow same-document paint references while keeping styles self-contained."""
	if "@import" in value.lower():
		raise ValueError(f"{path}: SVG styles must be self-contained")
	for match in re.finditer(r"url\(\s*['\"]?([^)'\"]+)", value, re.IGNORECASE):
		if not match.group(1).strip().startswith("#"):
			raise ValueError(f"{path}: SVG style resources must be local fragments")


def _length(value: str, path: str) -> float:
	"""Convert an explicit absolute SVG viewport length into CSS pixels."""
	match = re.fullmatch(r"\s*([+\-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+\-]?\d+)?)\s*(px|pt|pc|mm|cm|in)?\s*", value)
	if match is None:
		raise ValueError(f"{path}: SVG viewport lengths must use absolute units")
	factors = {None: 1, "px": 1, "pt": 96 / 72, "pc": 16, "mm": 96 / 25.4,
		"cm": 96 / 2.54, "in": 96}
	result = float(match.group(1)) * factors[match.group(2)]
	return result
