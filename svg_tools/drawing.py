"""Small SVG fragments and document writing for local drawing recipes."""

import math
import pathlib
import xml.etree.ElementTree

import defusedxml.ElementTree


#============================================
def project(x: float, y: float, z: float) -> tuple[float, float]:
	"""Project drawing units: x right, y back/up-right, z up (parallel oblique)."""
	if not all(math.isfinite(value) for value in (x, y, z)):
		raise ValueError("Projected coordinates must be finite")
	point = (x + 0.46 * y, -0.36 * y - z)
	return point


#============================================
def _polygon(points: list[tuple[float, float]], fill: str, stroke: str,
	stroke_width: float) -> xml.etree.ElementTree.Element:
	"""Keep shared corners identical and escape authored face attributes."""
	coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
	element = xml.etree.ElementTree.Element("polygon", {
		"points": coords, "fill": fill, "stroke": stroke,
		"stroke-width": str(stroke_width), "stroke-linejoin": "round",
	})
	return element


#============================================
def cuboid(name: str, x: float, y: float, z: float, width: float, depth: float,
	height: float, *, colors: tuple[str, str, str], stroke: str,
	stroke_width: float = 2) -> str:
	"""Build top/front/right faces from a lower-front-left corner and positive sizes."""
	if not all(math.isfinite(value) and value > 0 for value in (width, depth, height)):
		raise ValueError("Cuboid dimensions must be finite and positive")
	if not math.isfinite(stroke_width) or stroke_width < 0:
		raise ValueError("Stroke width must be finite and nonnegative")
	top, front, right = colors
	group = xml.etree.ElementTree.Element("g", {"id": name})
	faces = [
		([(x, y, z), (x + width, y, z), (x + width, y, z + height),
			(x, y, z + height)], front),
		([(x + width, y, z), (x + width, y + depth, z),
			(x + width, y + depth, z + height), (x + width, y, z + height)], right),
		([(x, y, z + height), (x + width, y, z + height),
			(x + width, y + depth, z + height), (x, y + depth, z + height)], top),
	]
	for points, fill in faces:
		group.append(_polygon([project(*point) for point in points], fill, stroke, stroke_width))
	fragment = xml.etree.ElementTree.tostring(
		group, encoding="ascii", xml_declaration=False).decode("ascii")
	return fragment


#============================================
def cylinder(name: str, x: float, y: float, z: float, radius: float, height: float,
	*, colors: tuple[str, str, str], stroke: str, stroke_width: float = 2,
	top_radius: float | None = None) -> str:
	"""Build an upright cylinder or taper from its bottom center in the shared projection."""
	if top_radius is None:
		top_radius = radius
	if not all(math.isfinite(value) and value > 0 for value in (radius, top_radius, height)):
		raise ValueError("Cylinder radii and height must be finite and positive")
	if not math.isfinite(stroke_width) or stroke_width < 0:
		raise ValueError("Stroke width must be finite and nonnegative")
	top, front, right = colors
	angle = math.atan(0.46)
	# shortcut: half-circle sides suit upright parts; refine tangencies for shallow, wide tapers.
	angles = [angle + math.pi + math.pi * index / 24 for index in range(25)]
	lower = [project(x + radius * math.cos(t), y + radius * math.sin(t), z) for t in angles]
	upper = [project(x + top_radius * math.cos(t), y + top_radius * math.sin(t), z + height)
		for t in angles]
	group = xml.etree.ElementTree.Element("g", {"id": name})
	group.append(_polygon(upper + lower[::-1], front, stroke, stroke_width))
	group.append(_polygon(upper[16:] + lower[16:][::-1], right, "none", 0))
	cx, cy = project(x, y, z + height)
	xml.etree.ElementTree.SubElement(group, "circle", {
		"r": str(top_radius), "transform": f"matrix(1 0 .46 -.36 {cx} {cy})",
		"fill": top, "stroke": stroke, "stroke-width": str(stroke_width),
	})
	fragment = xml.etree.ElementTree.tostring(
		group, encoding="ascii", xml_declaration=False).decode("ascii")
	return fragment


#============================================
def text(x: float, y: float, value: str, *, size: float, color: str,
	anchor: str = "middle", font: str = "Arial, sans-serif") -> str:
	"""Make an editable label, escaping its value and attributes as XML."""
	element = xml.etree.ElementTree.Element("text", {
		"x": str(x), "y": str(y), "font-size": str(size), "fill": color,
		"text-anchor": anchor, "font-family": font,
	})
	element.text = value
	fragment = xml.etree.ElementTree.tostring(
		element, encoding="ascii", xml_declaration=False).decode("ascii")
	return fragment


#============================================
def line(x1: float, y1: float, x2: float, y2: float, *, color: str,
	width: float = 3, dash: str = "") -> str:
	"""Make a round-ended line, optionally with an SVG dash pattern."""
	element = xml.etree.ElementTree.Element("line", {
		"x1": str(x1), "y1": str(y1), "x2": str(x2), "y2": str(y2),
		"stroke": color, "stroke-width": str(width), "stroke-linecap": "round",
	})
	if dash:
		element.set("stroke-dasharray", dash)
	fragment = xml.etree.ElementTree.tostring(
		element, encoding="ascii", xml_declaration=False).decode("ascii")
	return fragment


#============================================
def write_svg(path: str | pathlib.Path, width: float, height: float, title: str,
	description: str, body: str) -> None:
	"""Write a complete SVG after validating XML; the parent folder must exist."""
	if not all(math.isfinite(value) and value > 0 for value in (width, height)):
		raise ValueError("SVG width and height must be finite and positive")
	root = defusedxml.ElementTree.fromstring("<svg>" + body + "</svg>")
	root.attrib.update({
		"xmlns": "http://www.w3.org/2000/svg", "width": str(width), "height": str(height),
		"viewBox": f"0 0 {width} {height}", "role": "img", "aria-labelledby": "title desc",
	})
	label = xml.etree.ElementTree.Element("title", {"id": "title"})
	label.text = title
	root.insert(0, label)
	detail = xml.etree.ElementTree.Element("desc", {"id": "desc"})
	detail.text = description
	root.insert(1, detail)
	# LibreOffice may render SVGs with an ASCII declaration blank.
	payload = xml.etree.ElementTree.tostring(root, encoding="ascii", xml_declaration=False)
	# Reject invalid XML characters in metadata before opening an existing destination.
	defusedxml.ElementTree.fromstring(payload)
	pathlib.Path(path).write_bytes(payload)
