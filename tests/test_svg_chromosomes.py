"""Stable ordering, geometry and composition contracts for chromosome fragments."""

import math
import xml.etree.ElementTree

import pytest

import svg_tools.chromosomes


#============================================
def test_explicit_allele_typography() -> None:
	"""Allele mode keeps empty arms and live italic genes with raised readable signs."""
	genes = [("", "#C1E7EE"), ("a+", "#D9C9EF"), ("b-", "#C1E7EE")]
	fragment, width, boundaries = svg_tools.chromosomes.chromosome_svg(
		"alleles", genes, centromere_after=1, allele_labels=True)
	labels = xml.etree.ElementTree.fromstring(fragment).findall(".//text")
	assert ["".join(node.itertext()) for node in labels] == ["", "a+", "b\u2212"]
	for label in labels[1:]:
		assert label[0].attrib["font-style"] == "italic"
		assert float(label[1].attrib["dy"]) < 0
	assert fragment.isascii()
	plain, plain_width, plain_boundaries = svg_tools.chromosomes.chromosome_svg(
		"alleles", genes, centromere_after=1)
	assert (width, boundaries) == (plain_width, plain_boundaries)
	assert xml.etree.ElementTree.fromstring(plain).findall(".//text")[2].text == "b-"
	for invalid in ("A+", "abc-", "a", "a++"):
		with pytest.raises(ValueError, match="Allele labels"):
			svg_tools.chromosomes.chromosome_svg("bad", [(invalid, "#FFFFFF")], allele_labels=True)


#============================================
def test_order_locus_and_composition() -> None:
	"""Deletion changes length; collars, joins and unique local refs stay distinct."""
	parts = []
	widths = []
	for name, sequence, centromere, joins in (
		("before", "ABCDEFGH", 5, ()), ("after", "ABCEFGH", 4, (3,)),
	):
		fragment, width, boundaries = svg_tools.chromosomes.chromosome_svg(
			name, [(letter, "#B48CDE" if letter == "D" else "#D9C9EF")
				for letter in sequence],
			centromere_after=centromere, junctions=joins)
		root = xml.etree.ElementTree.fromstring(fragment)
		assert "".join(node.text for node in root.iter("text")) == sequence
		assert all(a < b for a, b in zip(boundaries, boundaries[1:]))
		assert len(boundaries) == len(sequence) + 1
		assert root.find(f".//*[@id='{name}-centromere']") is not None
		labels = root.findall(".//text")
		assert float(labels[centromere-1].attrib["x"]) < boundaries[centromere]
		assert float(labels[centromere].attrib["x"]) > boundaries[centromere]
		parts.append(fragment)
		widths.append(width)
	assert widths[0] > widths[1]
	root = xml.etree.ElementTree.fromstring("<svg>" + "".join(parts) + "</svg>")
	ids = [node.attrib["id"] for node in root.iter() if "id" in node.attrib]
	assert len(ids) == len(set(ids))
	for node in root.iter():
		if "clip-path" in node.attrib:
			assert node.attrib["clip-path"][5:-1] in ids
	assert root.find(".//*[@id='after-join-3']") is not None
	assert root.find(".//*[@id='before-join-5']") is None
	assert root.find(".//*[@id='before-region-3']/rect").attrib["fill"] == "#B48CDE"


#============================================
def test_explicit_absence_and_escaped_labels() -> None:
	"""Unlabeled and special-character labels compose as ordinary live XML text."""
	fragment, _, _ = svg_tools.chromosomes.chromosome_svg(
		"plain", [("", "#FFFFFF"), ("A&B<\u03b1", "#FFFFFF")])
	root = xml.etree.ElementTree.fromstring(fragment)
	assert root.findall(".//text")[1].text == "A&B<\u03b1"
	assert root.find(".//*[@id='plain-centromere']") is None
	assert fragment.isascii()


#============================================
def test_invalid_geometry_and_boundaries() -> None:
	"""Reject nonfinite geometry and ambiguous topology rather than drawing it."""
	genes = [("A", "#FFFFFF"), ("B", "#FFFFFF")]
	for kwargs in ({"pitch": 0}, {"height": -1}, {"pitch": math.inf},
		{"height": math.nan}, {"centromere_after": 0}, {"junctions": (2,)},
		{"centromere_after": 1, "junctions": (1,)}, {"junctions": (1, 1)}):
		with pytest.raises(ValueError):
			svg_tools.chromosomes.chromosome_svg("bad", genes, **kwargs)
	with pytest.raises(ValueError):
		svg_tools.chromosomes.chromosome_svg("bad id", genes)
	with pytest.raises(ValueError):
		svg_tools.chromosomes.chromosome_svg("empty", [])
	with pytest.raises(ValueError):
		svg_tools.chromosomes.chromosome_svg("bad-fill", [("A", "url(external)")])
