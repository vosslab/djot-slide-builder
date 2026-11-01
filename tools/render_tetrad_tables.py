#!/usr/bin/env python3
"""Render the fixed two-gene tetrad working tables as self-contained SVG figures."""

# Standard Library
import argparse
import collections
import copy
import json
import pathlib
import re
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
CLASS_COLORS = {
	"PD": ("#935D00", "#FFE3A3"),
	"TT": ("#A719DB", "#E8CCE6"),
	"NPD": ("#007A00", "#BFE6C0"),
}


#============================================
def element(parent: ET.Element, name: str, **attributes: object) -> ET.Element:
	"""Create a namespaced SVG primitive with escaped attribute values."""
	return ET.SubElement(parent, f"{{{SVG_NS}}}{name}",
		{key.replace("_", "-"): str(value) for key, value in attributes.items()})


#============================================
def label(parent: ET.Element, x: float, y: float, value: object,
		color: str = "#1D2433", bold: bool = False, anchor: str = "middle",
		size: int = 30) -> None:
	"""Keep headings, counts, and classifications as live SVG text."""
	text = element(parent, "text", x=x, y=y, fill=color, font_family="sans-serif",
		font_size=size, font_weight="bold" if bold else "normal", text_anchor=anchor)
	text.text = str(value)


#============================================
def load_asci(path: pathlib.Path) -> tuple[ET.Element, ...]:
	"""Extract the three existing unordered-ascus drawings, without their captions."""
	data = path.read_bytes()
	# ASVS 1.5.1: accept self-contained SVG without DTDs or external entities/resources.
	if b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():
		raise ValueError(f"SVG must not contain a DTD or entity declaration: {path}")
	root = ET.fromstring(data)
	for node in root.iter():
		if node.tag.rsplit("}", 1)[-1] in ("script", "foreignObject", "style"):
			raise ValueError(f"Ascus SVG must contain only self-contained drawing content: {path}")
		for name, value in node.attrib.items():
			local = name.rsplit("}", 1)[-1]
			if local.lower().startswith("on") or local == "href" and not value.startswith("#"):
				raise ValueError(f"Ascus SVG must not contain active or external content: {path}")
	asci = tuple(root.findall(f".//{{{SVG_NS}}}svg"))
	if len(asci) != 3:
		raise ValueError(f"Expected three individual ascus SVGs: {path}")
	return asci


#============================================
def classified_rows(example: dict, asci: tuple[ET.Element, ...]) -> list[tuple[dict, str]]:
	"""Check the counts and classify drawings against the given parental combinations."""
	genes = example["genes"]
	if not isinstance(genes, str) or not re.fullmatch(r"[a-z]{2}", genes) or genes[0] == genes[1]:
		raise ValueError("The table renderer requires two distinct lowercase gene letters")
	parents = example["parents"]
	rows = example["rows"]
	if type(example["total"]) is not int or example["total"] <= 0:
		raise ValueError("Total tetrads must be a positive integer")
	if len(parents) != 2 or len(set(parents)) != 2 or len(rows) != 3 or len(asci) != 3:
		raise ValueError("The table requires two parents and three tetrad sets")
	result = []
	for row, artwork in zip(rows, asci, strict=True):
		spores = row["spores"]
		count = row["count"]
		if len(spores) != 4 or type(count) is not int or count <= 0:
			raise ValueError("Each tetrad set needs four spores and a positive integer count")
		for genotype in [*spores, *parents]:
			if not isinstance(genotype, str) or len(genotype) != 2 or any(
					a not in ("+", g) for a, g in zip(genotype, genes)):
				raise ValueError(f"Invalid two-gene genotype: {genotype!r}")
		observed = collections.Counter(spores)
		if sorted(observed.values()) not in ([2, 2], [1, 1, 1, 1]):
			raise ValueError("Expected a ditype or tetratype spore multiset")
		label_value = "TT" if len(observed) == 4 else "PD" if set(observed) == set(parents) else "NPD"
		drawn = [node.attrib["data-genotype"] for node in artwork.iter()
			if "data-genotype" in node.attrib]
		# ASVS 2.2.3: each reused drawing must match the data in its own row.
		if collections.Counter(drawn) != observed:
			raise ValueError("Ascus artwork does not match the row's four genotypes")
		if artwork.attrib["viewBox"] != "0 0 122 94":
			raise ValueError("Expected the existing 122 by 94 unordered-ascus artwork")
		result.append((row, label_value))
	if sum(row["count"] for row in rows) != example["total"]:
		raise ValueError("Total tetrads must equal the sum of the three counts")
	if {kind for _, kind in result} != set(CLASS_COLORS):
		raise ValueError("Expected one PD, one TT, and one NPD set")
	return result


#============================================
def render_table(example: dict, asci: tuple[ET.Element, ...], reveal: bool) -> str:
	"""Compose a compact three-row table with legible four-spore figures."""
	rows = classified_rows(example, asci)
	root = ET.Element(f"{{{SVG_NS}}}svg", {
		"width": "482", "height": "504", "viewBox": "0 0 482 504",
		"role": "img", "aria-labelledby": "table-title table-description",
	})
	element(root, "title", id="table-title").text = "Two-Gene Tetrad Working Table"
	description = element(root, "desc", id="table-description")
	description.text = "Given parents: " + " / ".join(example["parents"]) + ". "
	description.text += "; ".join(f"Set {i}: {', '.join(row['spores'])}; "
		f"{row['count']} tetrads; {kind if reveal else 'classify this set'}"
		for i, (row, kind) in enumerate(rows, 1))
	description.text += f". Total: {example['total']} tetrads. Spore positions are unordered."
	element(root, "metadata").text = (
		"Source: adjacent problem_data.json and existing ascus SVGs. "
		"Allele labels enlarged; spore geometry and genotype multisets preserved. "
		"Colors identify alleles, not measured pigmentation.")
	group = element(root, "g", transform="translate(1 1)")
	element(group, "rect", width=480, height=502, fill="#F2F3F4")
	element(group, "rect", width=480, height=56, fill="#BDD0E4")
	element(group, "rect", y=452, width=480, height=50, fill="#BDD0E4")
	for x, value in ((32, "Set"), (171, "4 Spores"), (326, "n"), (427, "Type")):
		label(group, x, 38, value, "#000000", True)
	for i, ((row, kind), source) in enumerate(zip(rows, asci, strict=True), 1):
		top = 56 + (i - 1) * 132
		row_group = element(group, "g", data_set=i, data_count=row["count"])
		if reveal:
			element(row_group, "rect", x=374, y=top, width=106, height=132,
				fill=CLASS_COLORS[kind][1])
		artwork = copy.deepcopy(source)
		artwork.attrib.update({"x": "88", "y": str(top + 2), "width": "166", "height": "128"})
		for node in artwork.iter(f"{{{SVG_NS}}}text"):
			node.set("font-size", "22")
		row_group.append(artwork)
		label(row_group, 32, top + 76, i)
		label(row_group, 326, top + 76, f"{row['count']:,}")
		label(row_group, 427, top + 80, kind if reveal else "?",
			CLASS_COLORS[kind][0] if reveal else "#1D2433", reveal, size=40)
	label(group, 14, 487, "Total", bold=True, anchor="start")
	label(group, 326, 487, f"{example['total']:,}", bold=True)
	grid = element(group, "g", fill="none", stroke="#2B5B8E", stroke_width=2)
	element(grid, "rect", width=480, height=502)
	for y in (56, 188, 320, 452):
		element(grid, "line", x1=0, x2=480, y1=y, y2=y)
	for x in (64, 278, 374):
		element(grid, "line", x1=x, x2=x, y1=0, y2=452 if x == 64 else 502)
	return ET.tostring(root, encoding="unicode") + "\n"


#============================================
def main() -> None:
	"""Rebuild question and classified figures beside the supplied problem data."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("problem_data", type=pathlib.Path,
		help="fixed BPW problem_data.json with adjacent two_gene_asci.svg and unlinked_asci.svg")
	args = parser.parse_args()
	data = json.loads(args.problem_data.read_text(encoding="utf-8"))
	outputs = {}
	for example in data["examples"]:
		if len(example["genes"]) != 2:
			continue
		pair = example["genes"].upper()
		prefix = "two_gene" if "distance" in example["pairs"][pair] else "unlinked"
		artwork = load_asci(args.problem_data.parent / f"{prefix}_asci.svg")
		for reveal, state in ((False, "question"), (True, "classified")):
			path = args.problem_data.parent / f"{prefix}_table_{state}.drawn.svg"
			if path in outputs:
				raise ValueError("The input contains duplicate linked or unlinked two-gene examples")
			outputs[path] = render_table(example, artwork, reveal)
	if len(outputs) != 4:
		raise ValueError("Expected one linked and one unlinked two-gene example")
	# Validate all figures before replacing any generated output.
	for path, svg in outputs.items():
		path.write_text(svg, encoding="utf-8")
		print(path)


if __name__ == "__main__":
	main()
