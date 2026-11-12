"""Editable schematic single-chromatid rods inspired by BPQ chromosome drawings."""

import re
import math
import xml.etree.ElementTree


#============================================
def chromosome_svg(name: str, genes: list[tuple[str, str]], *,
	centromere_after: int | None = None, junctions: tuple[int, ...] = (),
	pitch: float = 64, height: float = 62,
	allele_labels: bool = False) -> tuple[str, float, list[float]]:
	"""Draw ordered labeled regions; return markup, width and intergene coordinates.

	Args:
		name: Unique XML ID namespace within the composed document.
		genes: Ordered (label, six-digit hex fill) pairs; empty labels give an unlabeled rod.
		centromere_after: Number of regions before a collar, or None for no collar.
		junctions: Explicit intergene join indices, distinct from the centromere.
		pitch: Positive width of each schematic gene region (not genomic length).
		height: Positive rod height.
		allele_labels: Render lowercase letter +/- labels as italic genes and raised signs.

	Returns:
		SVG group, rod width, and boundaries indexed by preceding region count.
		At the centromeric boundary the coordinate is the center of the collar.
	"""
	if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.-]*", name):
		raise ValueError("Use an XML-safe unique namespace")
	if not genes or not all(math.isfinite(v) and v > 0 for v in (pitch, height)):
		raise ValueError("Supply regions and finite positive geometry")
	if not all(isinstance(label, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", fill)
		for label, fill in genes):
		raise ValueError("Regions need string labels and six-digit hex fills")
	if allele_labels and any(label and not re.fullmatch(r"[a-z][+-]", label)
		for label, _ in genes):
		raise ValueError("Allele labels need one lowercase letter and +/- or an empty label")
	indices = list(junctions)
	if centromere_after is not None:
		indices.append(centromere_after)
	if any(type(index) is not int or not 0 < index < len(genes) for index in indices):
		raise ValueError("Collars and joins must lie between regions")
	if len(set(junctions)) != len(junctions) or centromere_after in junctions:
		raise ValueError("Joins must be distinct from each other and the centromere")
	cap = height * 0.24
	collar = height * 0.48 if centromere_after is not None else 0
	width = 2 * cap + len(genes) * pitch + collar
	if not math.isfinite(width):
		raise ValueError("Rod width must be finite")
	boundary = [cap + index * pitch + (
		collar if centromere_after is not None and index > centromere_after else 0
	) for index in range(len(genes) + 1)]
	if centromere_after is not None:
		boundary[centromere_after] += collar / 2
	group = xml.etree.ElementTree.Element("g", {"id": name})
	defs = xml.etree.ElementTree.SubElement(group, "defs")
	clip = xml.etree.ElementTree.SubElement(defs, "clipPath", {"id": f"{name}-clip"})
	radius = height * .32
	top = f"M {radius} 0"
	bottom = f"L {width-radius} {height}"
	if centromere_after is not None:
		x = boundary[centromere_after] - collar / 2
		top += f" H {x} Q {x+collar/2} {height*.25} {x+collar} 0"
		bottom += f" H {x+collar} Q {x+collar/2} {height*.75} {x} {height}"
	top += f" H {width-radius} Q {width} 0 {width} {radius}"
	top += f" V {height-radius} Q {width} {height} {width-radius} {height}"
	bottom += f" H {radius} Q 0 {height} 0 {height-radius} V {radius} Q 0 0 {radius} 0 Z"
	outline = {"d": top + bottom}
	xml.etree.ElementTree.SubElement(clip, "path", outline)
	paint = xml.etree.ElementTree.SubElement(group, "g", {"clip-path": f"url(#{name}-clip)"})
	xml.etree.ElementTree.SubElement(paint, "path", dict(outline, fill="#98A2AD"))
	for index, (label, fill) in enumerate(genes):
		x = cap + index * pitch
		if centromere_after is not None and index >= centromere_after:
			x += collar
		region = xml.etree.ElementTree.SubElement(paint, "g", {"id": f"{name}-region-{index}"})
		xml.etree.ElementTree.SubElement(region, "rect", {
			"x": str(x), "y": "0", "width": str(pitch), "height": str(height), "fill": fill,
		})
		# Sparse end stripes leave the live labels clear; these are not measured G-bands.
		band_positions = (((.13, .045),), ((.84, .035),), ((.10, .025), (.89, .055)),
			((.79, .045),), ((.18, .035),))
		for offset, thickness in band_positions[index % len(band_positions)]:
			xml.etree.ElementTree.SubElement(region, "path", {
				"d": f"M {x + pitch * offset} 0 l {-height * .055} {height}",
				"stroke": "#213547", "stroke-opacity": ".09",
				"stroke-width": str(pitch * thickness),
			})
		text = xml.etree.ElementTree.SubElement(region, "text", {
			"x": str(x + pitch / 2), "y": str(height * .7),
			"font-family": "Atkinson Hyperlegible Next", "font-size": str(height * .59),
			"font-weight": "600", "text-anchor": "middle", "fill": "#172B3A",
		})
		if allele_labels and label:
			xml.etree.ElementTree.SubElement(text, "tspan", {"font-style": "italic"}).text = label[0]
			xml.etree.ElementTree.SubElement(text, "tspan", {
				"dx": str(height * .07), "dy": str(-height * .22),
				"font-size": str(height * .40),
			}).text = "+" if label[1] == "+" else "\u2212"
		else:
			text.text = label
	for index in junctions:
		x = boundary[index]
		points = [(x + (height * .035 if step % 2 else -height * .035), height * step / 6)
			for step in range(7)]
		xml.etree.ElementTree.SubElement(paint, "polyline", {
			"id": f"{name}-join-{index}", "points": " ".join(f"{x},{y}" for x, y in points),
			"fill": "none", "stroke": "#FFFFFF", "stroke-width": str(height * .065),
		})
	xml.etree.ElementTree.SubElement(group, "path", dict(
		outline, fill="none", stroke="#344651", **{"stroke-width": str(height * .035)}))
	if centromere_after is not None:
		x = boundary[centromere_after] - collar / 2
		# A pale collar narrows the rod while remaining visibly connected to both arms.
		path = f"M {x} 0 Q {x + collar/2} {height*.25} {x+collar} 0"
		path += f" L {x+collar} {height} Q {x+collar/2} {height*.75} {x} {height} Z"
		xml.etree.ElementTree.SubElement(group, "path", {
			"id": f"{name}-centromere", "d": path, "fill": "#EEF1F4",
			"stroke": "#344651", "stroke-width": str(height * .035),
		})
	fragment = xml.etree.ElementTree.tostring(
		group, encoding="ascii", xml_declaration=False).decode("ascii")
	return fragment, width, boundary
