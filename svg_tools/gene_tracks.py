"""Editable exon blocks joined by thin schematic intron spans."""

import re
import math
import collections.abc
import xml.etree.ElementTree

import svg_tools.chromosomes


#============================================
def gene_track_svg(name: str,
	exons: collections.abc.Sequence[svg_tools.chromosomes.Segment],
	intron_lengths: collections.abc.Sequence[float], *,
	width: float | None = None, height: float = 50) -> tuple[str, float, list[float]]:
	"""Return an SVG group, whole track width, and exon starts plus final exon end.

	Lengths are schematic units. Positive introns connect thick exon blocks; zero
	introns join adjacent blocks. Segment bands are ignored. Unlike chromosome
	boundaries, these coordinates mark exon starts, including the preceding gap.
	Names must be unique XML-safe prefixes in the enclosing document. Height is
	the exon block height; provide external margins for outline strokes. Short
	labels work best; width-based font fitting is approximate.
	"""
	if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.-]*", name):
		raise ValueError("Use an XML-safe unique namespace")
	if not exons or not all(isinstance(exon, svg_tools.chromosomes.Segment) for exon in exons):
		raise ValueError("Supply at least one exon Segment")
	if len(intron_lengths) != len(exons) - 1:
		raise ValueError("Supply exactly one intron length between each pair of exons")
	if any(not isinstance(value, (int, float)) or isinstance(value, bool)
		or not math.isfinite(value) or value < 0 for value in intron_lengths):
		raise ValueError("Intron lengths must be finite and nonnegative")
	natural_width = sum(exon.length for exon in exons) + sum(intron_lengths)
	if width is None:
		width = natural_width
	if any(not isinstance(value, (int, float)) or isinstance(value, bool)
		or not math.isfinite(value) or value <= 0 for value in (natural_width, width, height)):
		raise ValueError("Track dimensions must be finite and positive")
	group = xml.etree.ElementTree.Element("g", {"id": name})
	boundaries = []
	x = 0.0
	for index, exon in enumerate(exons):
		boundaries.append(x)
		exon_width = exon.length / natural_width * width
		region = xml.etree.ElementTree.SubElement(group, "g", {"id": f"{name}-exon-{index}"})
		xml.etree.ElementTree.SubElement(region, "rect", {
			"x": str(x), "y": "0", "width": str(exon_width), "height": str(height),
			"fill": exon.color, "stroke": "#344651", "stroke-width": str(height * .035),
		})
		font_size = min(height * .59, exon_width * .8 / max(1, len(exon.label)))
		xml.etree.ElementTree.SubElement(region, "text", {
			"x": str(x + exon_width / 2), "y": str(height / 2 + font_size * .34),
			"font-family": "Atkinson Hyperlegible Next", "font-size": str(font_size),
			"font-weight": "600", "text-anchor": "middle",
			"fill": svg_tools.chromosomes._label_color(exon.color),
		}).text = exon.label
		x += exon_width
		if index < len(intron_lengths) and intron_lengths[index] > 0:
			end = x + intron_lengths[index] / natural_width * width
			xml.etree.ElementTree.SubElement(group, "line", {
				"id": f"{name}-intron-{index}", "x1": str(x), "x2": str(end),
				"y1": str(height / 2), "y2": str(height / 2),
				"stroke": "#344651", "stroke-width": str(height * .06),
			})
			x = end
	boundaries.append(x)
	fragment = xml.etree.ElementTree.tostring(
		group, encoding="ascii", xml_declaration=False).decode("ascii")
	return fragment, width, boundaries
