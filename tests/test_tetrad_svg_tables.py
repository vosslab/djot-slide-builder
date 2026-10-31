"""Protect given-parent classification and genotype fidelity in the SVG working tables."""

import copy
import xml.etree.ElementTree as ET

import pytest

import tools.render_tetrad_tables


def test_table_preserves_genotypes_counts_and_question_reveal() -> None:
	"""Classify using the supplied parents even when PD has the smallest count."""
	example = {"genes": "ab", "parents": ["++", "ab"], "total": 10, "rows": [
		{"spores": ["++", "++", "ab", "ab"], "count": 1},
		{"spores": ["++", "+b", "a+", "ab"], "count": 2},
		{"spores": ["+b", "+b", "a+", "a+"], "count": 7},
	]}
	asci = []
	ns = "{http://www.w3.org/2000/svg}"
	for row in example["rows"]:
		artwork = ET.Element(ns + "svg", {"viewBox": "0 0 122 94"})
		for genotype in row["spores"]:
			ET.SubElement(artwork, ns + "g", {"data-genotype": genotype})
		asci.append(artwork)
	for reveal, expected in ((False, ["?", "?", "?"]), (True, ["PD", "TT", "NPD"])):
		root = ET.fromstring(tools.render_tetrad_tables.render_table(example, tuple(asci), reveal))
		rows = root.findall(".//" + ns + "g[@data-set]")
		assert [row.attrib["data-count"] for row in rows] == ["1", "2", "7"]
		assert [row.findall(ns + "text")[-1].text for row in rows] == expected
		assert len(root.findall(".//" + ns + "g[@data-genotype]")) == 12
		assert any(node.text == "10" for node in root.iter(ns + "text"))
	bad = copy.deepcopy(asci)
	bad[0][0].set("data-genotype", "a+")
	with pytest.raises(ValueError, match="does not match"):
		tools.render_tetrad_tables.render_table(example, tuple(bad), False)
