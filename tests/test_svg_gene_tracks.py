"""Protect distinct exon/intron anatomy and composable editable SVG output."""

import defusedxml.ElementTree

import svg_tools.chromosomes
import svg_tools.gene_tracks


#============================================
def test_exon_order_gaps_and_scaled_coordinates() -> None:
	exons = [svg_tools.chromosomes.Segment(label, color, length)
		for label, color, length in (
			("A", "#FFFFFF", 40), ("B", "#000000", 60), ("C", "#C1E7EE", 80))]
	for name, gaps, scale in (("dna", [20, 30], 2), ("processed", [0, 0], 1)):
		natural = sum(exon.length for exon in exons) + sum(gaps)
		fragment, width, boundaries = svg_tools.gene_tracks.gene_track_svg(
			name, exons, gaps, width=natural * scale)
		root = defusedxml.ElementTree.fromstring(fragment)
		blocks = root.findall(".//rect")
		assert width == natural * scale
		assert boundaries == [0, (40 + gaps[0]) * scale, (100 + sum(gaps)) * scale, width]
		assert [float(block.attrib["x"]) for block in blocks] == boundaries[:-1]
		assert [float(block.attrib["width"]) for block in blocks] == [40 * scale, 60 * scale, 80 * scale]
		assert [block.attrib["fill"] for block in blocks] == [exon.color for exon in exons]
		labels = root.findall(".//text")
		assert [node.text for node in labels] == [exon.label for exon in exons]
		lines = root.findall("line")
		assert len(lines) == sum(gap > 0 for gap in gaps)
		for index, line in enumerate(lines):
			assert float(line.attrib["x1"]) == boundaries[index] + exons[index].length * scale
			assert float(line.attrib["x2"]) == boundaries[index + 1]


#============================================
def test_single_exon_and_safe_live_text_composition() -> None:
	label = "A&B<\u03b1"
	exon = svg_tools.chromosomes.Segment(label, "#C1E7EE", 90)
	parts = []
	for name in ("first", "second"):
		fragment, width, boundaries = svg_tools.gene_tracks.gene_track_svg(name, [exon], [])
		assert width == 90 and boundaries == [0, 90]
		assert fragment.isascii()
		parts.append(fragment)
	root = defusedxml.ElementTree.fromstring("<svg>" + "".join(parts) + "</svg>")
	assert [node.text for node in root.iter("text")] == [label, label]
	ids = [node.attrib["id"] for node in root.iter() if "id" in node.attrib]
	assert len(ids) == len(set(ids))
	assert not any("url(" in value or "href" in key or key.startswith("on")
		for node in root.iter() for key, value in node.attrib.items())
