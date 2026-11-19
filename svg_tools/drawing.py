"""Small SVG fragments and document writing for local drawing recipes."""

import math
import pathlib

import lxml.etree

import svg_tools._xml
import svg_tools.normalize_svg


#============================================
def project(x: float, y: float, z: float) -> tuple[float, float]:
	"""Project drawing units: x right, y back/up-right, z up (parallel oblique)."""
	if not all(math.isfinite(value) for value in (x, y, z)):
		raise ValueError("Projected coordinates must be finite")
	point = (x + 0.46 * y, -0.36 * y - z)
	return point


#============================================
def _polygon(points: list[tuple[float, float]], fill: str, stroke: str,
	stroke_width: float) -> lxml.etree._Element:
	"""Keep shared corners identical and escape authored face attributes."""
	coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
	element = lxml.etree.Element("polygon", {
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
	group = lxml.etree.Element("g", {"id": name})
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
	fragment = lxml.etree.tostring(
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
	group = lxml.etree.Element("g", {"id": name})
	group.append(_polygon(upper + lower[::-1], front, stroke, stroke_width))
	group.append(_polygon(upper[16:] + lower[16:][::-1], right, "none", 0))
	cx, cy = project(x, y, z + height)
	lxml.etree.SubElement(group, "circle", {
		"r": str(top_radius), "transform": f"matrix(1 0 .46 -.36 {cx} {cy})",
		"fill": top, "stroke": stroke, "stroke-width": str(stroke_width),
	})
	fragment = lxml.etree.tostring(
		group, encoding="ascii", xml_declaration=False).decode("ascii")
	return fragment


#============================================
def text(x: float, y: float, value: str, *, size: float, color: str,
	anchor: str = "middle", font: str = "Atkinson Hyperlegible Next") -> str:
	"""Make an editable label, escaping its value and attributes as XML."""
	element = lxml.etree.Element("text", {
		"x": str(x), "y": str(y), "font-size": str(size), "fill": color,
		"text-anchor": anchor, "font-family": font,
	})
	element.text = value
	fragment = lxml.etree.tostring(
		element, encoding="ascii", xml_declaration=False).decode("ascii")
	return fragment


#============================================
def line(x1: float, y1: float, x2: float, y2: float, *, color: str,
	width: float = 3, dash: str = "") -> str:
	"""Make a round-ended line, optionally with an SVG dash pattern."""
	element = lxml.etree.Element("line", {
		"x1": str(x1), "y1": str(y1), "x2": str(x2), "y2": str(y2),
		"stroke": color, "stroke-width": str(width), "stroke-linecap": "round",
	})
	if dash:
		element.set("stroke-dasharray", dash)
	fragment = lxml.etree.tostring(
		element, encoding="ascii", xml_declaration=False).decode("ascii")
	return fragment


#============================================
def remove_canvas_background(root: lxml.etree._Element) -> None:
	"""Remove unstyled white rectangles that only cover an SVG viewport."""
	def local_name(name: str) -> str:
		return name.rsplit("}", 1)[-1]

	def number(value: str | None, default: float | None = None) -> float | None:
		if value is None:
			return default
		try:
			parsed = float(value)
		except ValueError:
			return None
		return parsed if math.isfinite(parsed) else None

	def view_box(element: lxml.etree._Element) -> tuple[float, float, float, float] | None:
		values = element.get("viewBox", "").replace(",", " ").split()
		if len(values) != 4:
			return None
		parsed = tuple(number(value) for value in values)
		if any(value is None for value in parsed):
			return None
		left, top, width, height = parsed
		if width <= 0 or height <= 0:
			return None
		return left, top, width, height

	def matches_span(value: str | None, size: float) -> bool:
		return value == "100%" or number(value) == size

	containers = [root]
	for svg in containers:
		# Only rendered containers carry canvas backgrounds; definitions retain their paint.
		containers.extend(child for child in svg if isinstance(child.tag, str)
			and local_name(child.tag) in {"svg", "g", "a", "switch"})
		if not isinstance(svg.tag, str) or local_name(svg.tag) != "svg":
			continue
		viewport = view_box(svg)
		if viewport is None:
			continue
		left, top, width, height = viewport
		for child in list(svg):
			if not isinstance(child.tag, str) or local_name(child.tag) != "rect":
				continue
			if child.get("fill", "").lower() not in {"white", "#fff", "#ffffff"}:
				continue
			if child.get("stroke", "none") not in {"", "none"}:
				continue
			if set(child.attrib) - {"x", "y", "width", "height", "fill", "stroke"}:
				continue
			if (number(child.get("x"), 0) == left and number(child.get("y"), 0) == top
					and matches_span(child.get("width"), width)
					and matches_span(child.get("height"), height)):
				svg.remove(child)


#============================================
def write_svg(path: str | pathlib.Path, width: float, height: float, title: str,
	description: str, body: str, *, crop: bool = False) -> None:
	"""Write a complete SVG after validating XML; the parent folder must exist."""
	if not all(math.isfinite(value) and value > 0 for value in (width, height)):
		raise ValueError("SVG width and height must be finite and positive")
	xlink = svg_tools._xml.XLINK
	root = svg_tools._xml.parse(f'<svg xmlns:xlink="{xlink}">{body}</svg>')
	root.attrib.update({
		"width": str(width), "height": str(height),
		"viewBox": f"0 0 {width} {height}", "role": "img", "aria-labelledby": "title desc",
	})
	remove_canvas_background(root)
	label = lxml.etree.Element("title", {"id": "title"})
	label.text = title
	root.insert(0, label)
	detail = lxml.etree.Element("desc", {"id": "desc"})
	detail.text = description
	root.insert(1, detail)
	# LibreOffice may render SVGs with an ASCII declaration blank.
	payload = lxml.etree.tostring(svg_root(root), encoding="ascii", xml_declaration=False)
	if crop:
		payload, _report = svg_tools.normalize_svg.normalize(payload, str(path))
	pathlib.Path(path).write_bytes(payload)


#============================================
def svg_root(source: lxml.etree._Element) -> lxml.etree._Element:
	"""Normalize a complete SVG for LibreOffice with document-local namespaces."""
	# LibreOffice needs unprefixed SVG elements and the literal xlink prefix.
	svg = svg_tools._xml.SVG
	if source.tag not in ("svg", f"{{{svg}}}svg"):
		raise ValueError("Expected an SVG root")
	attributes = {name: value for name, value in source.attrib.items() if name != "xmlns"}
	root = lxml.etree.Element(f"{{{svg}}}svg", attributes,
		nsmap={None: svg, "xlink": svg_tools._xml.XLINK})
	root.text = source.text
	_copy_contents(source, root, svg)
	lxml.etree.cleanup_namespaces(root)
	return root


#============================================
def _copy_contents(source: lxml.etree._Element, target: lxml.etree._Element, svg: str) -> None:
	"""Copy expanded names so source prefixes cannot shadow the writer's prefixes."""
	for child in source:
		if isinstance(child, lxml.etree._Comment):
			copy = lxml.etree.Comment(child.text)
			target.append(copy)
		else:
			tag = child.tag if child.tag.startswith("{") else f"{{{svg}}}{child.tag}"
			copy = lxml.etree.SubElement(target, tag, dict(child.attrib))
			copy.text = child.text
			_copy_contents(child, copy, svg)
		copy.tail = child.tail
