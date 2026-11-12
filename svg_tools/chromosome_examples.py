#!/usr/bin/env python3
"""Build the source-backed v2 chromosome specimen.

Historical recipes remain callable with today's renderer; they do not reproduce
the saved historical silhouettes. Ordinary module execution writes only v2.

Run from the repository root: python3 -m svg_tools.chromosome_examples
Course assets are deliberately not written by this recipe.
"""

import pathlib

import svg_tools.drawing
import svg_tools.chromosomes
import svg_tools.gene_tracks

PURPLE = "#D9C9EF"
PURPLE_TARGET = "#B48CDE"
BLUE = "#C1E7EE"
BLUE_TARGET = "#77CBDC"
FONT = "Atkinson Hyperlegible Next"


#============================================
def rod(name: str, sequence: str, target: str, base: str, emphasis: str,
	x: float, y: float, *, cuts: tuple[int, ...] = (),
	joins: tuple[int, ...] = ()) -> str:
	"""Place a source-defined rod, with cut arrows at its actual region boundaries."""
	letters = sequence.replace("|", "")
	centromere = sequence.index("|") if "|" in sequence else None
	genes = [(letter, emphasis if letter in target else base) for letter in letters]
	fragment, _, boundaries = svg_tools.chromosomes.chromosome_svg(
		name, genes, centromere_after=centromere, junctions=joins)
	body = f'<g transform="translate({x} {y})">{fragment}'
	for index in cuts:
		position = boundaries[index]
		body += f'<path d="M {position} -32 V -12" stroke="#BD2929" stroke-width="4"/>'
		body += f'<path d="M {position-7} -15 L {position} -3 L {position+7} -15 Z" fill="#BD2929"/>'
	body += '</g>'
	return body


#============================================
def stage_label(value: str, y: float) -> str:
	"""Keep row names readable at the half-width consumer size."""
	label = svg_tools.drawing.text(48, y, value, size=32, color="#344651",
		anchor="start", font=FONT)
	return label


#============================================
def make_overviews(output: pathlib.Path) -> None:
	"""Use the retained source gene orders, colors, cuts and centromere loci."""
	output.mkdir(parents=True, exist_ok=True)
	cases = [
		("deletion", "D", "ABCE|FGH", (3, 4), (3,)),
		("duplication", "BC", "ABCBCDE|FGH", (1, 3), (3, 5)),
		("inversion", "BCD", "ADCBE|FGH", (1, 4), (1, 4)),
	]
	for name, target, after, cuts, joins in cases:
		body = stage_label("Before", 103) + stage_label("After", 263)
		body += rod(f"{name}-before", "ABCDE|FGH", target, PURPLE, PURPLE_TARGET,
			218, 60, cuts=cuts)
		body += rod(f"{name}-after", after, target, PURPLE, PURPLE_TARGET,
			218, 220, joins=joins)
		description = f"Before ABCDE, centromere, FGH; after {after.replace('|', ', centromere, ')}. "
		description += f"The {target} region is emphasized; red arrows mark source cuts. "
		description += "Pale collars are centromeres; white zigzags mark joins. "
		description += "Single chromatids; equal gene spacing and subtle bands are schematic."
		svg_tools.drawing.write_svg(output / f"{name}_overview.drawn.svg", 980, 340,
			name.capitalize(), description, body)
	body = stage_label("Before", 124) + stage_label("After", 424)
	body += rod("translocation-before-1", "ABCDE|FGH", "AB", PURPLE, PURPLE_TARGET,
		218, 50, cuts=(2,))
	body += rod("translocation-before-2", "MNOPQ|R", "MNO", BLUE, BLUE_TARGET,
		218, 160, cuts=(3,))
	# Explicit colors travel with the terminal source segments, not with their new row.
	for name, sequence, colors, y, join in (
		("translocation-after-1", "MNOCDE|FGH", [BLUE_TARGET]*3 + [PURPLE]*6, 350, 3),
		("translocation-after-2", "ABPQ|R", [PURPLE_TARGET]*2 + [BLUE]*3, 460, 2),
	):
		fragment, _, _ = svg_tools.chromosomes.chromosome_svg(name,
			list(zip(sequence.replace("|", ""), colors)),
			centromere_after=sequence.index("|"), junctions=(join,))
		body += f'<g transform="translate(218 {y})">{fragment}</g>'
	svg_tools.drawing.write_svg(output / "translocation_overview.drawn.svg", 980, 580,
		"Reciprocal translocation",
		"ABCDE, centromere, FGH and MNOPQ, centromere, R exchange terminal AB and MNO. "
		"Products: MNOCDE, centromere, FGH and ABPQ, centromere, R. "
		"Color follows segment identity; red arrows mark B/C and O/P cuts; "
		"white zigzags mark joins, distinct from pale centromere collars. "
		"Single chromatids; spacing and decorative bands are schematic.", body)


#============================================
def make_specimen(path: pathlib.Path) -> None:
	"""Show the supported vocabulary without implying a measured chromosome map."""
	body = svg_tools.drawing.text(40, 48, "Single-chromatid chromosome language",
		size=30, color="#213547", anchor="start", font=FONT)
	for name, label, genes, centromere, joins, y in (
		("simple", "Unlabeled rod", [("", PURPLE)]*8, None, (), 100),
		("collar", "Centromere collar", [(c, PURPLE) for c in "ABCDEFGH"], 5, (), 225),
		("join", "Transferred segment", [(c, BLUE_TARGET if i < 3 else PURPLE)
			for i, c in enumerate("MNOCDEFGH")], 6, (3,), 350),
	):
		body += svg_tools.drawing.text(40, y+39, label, size=26, color="#344651",
			anchor="start", font=FONT)
		fragment, _, _ = svg_tools.chromosomes.chromosome_svg(name, genes,
			centromere_after=centromere, junctions=joins)
		body += f'<g transform="translate(325 {y})">{fragment}</g>'
	body += svg_tools.drawing.text(40, 514, "Explicit alleles", size=26,
		color="#344651", anchor="start", font=FONT)
	fragment, _, _ = svg_tools.chromosomes.chromosome_svg("alleles",
		[("", BLUE), ("a+", PURPLE), ("b-", BLUE), ("c+", PURPLE)],
		centromere_after=1, allele_labels=True)
	body += f'<g transform="translate(325 475)">{fragment}</g>'
	body += svg_tools.drawing.text(40, 588,
		"Neutral ends; pale collar; white join. Bands and spacing are schematic.",
		size=25, color="#344651", anchor="start", font=FONT)
	svg_tools.drawing.write_svg(path, 1020, 620, "Chromosome language specimen",
		"Four unreplicated rods show an unlabeled form, an E/F centromere collar, "
		"and transferred MNO joined to CDE with the same E/F centromere. "
		"Terminal caps are illustrative end treatments, not extra genes. "
		"The allele row has an unlabeled arm, a centromere before a, and italic a+, b-, c+ labels. "
		"Decorative bands do not represent measured G-bands.", body)


#============================================
def make_tool_specimen(path: pathlib.Path) -> None:
	"""Draw all tool modes without rewriting the historical language specimen.

	From the repository root, call just this recipe:
	python3 -c 'import pathlib; import svg_tools.chromosome_examples as examples; examples.make_tool_specimen(pathlib.Path("docs/slide-specs/illustration_examples/chromosome_tool.drawn.svg"))'
	"""
	body = '<rect width="1440" height="1510" fill="#F8F7F3"/>'

	def label(x: float, y: float, value: str, size: float = 26) -> str:
		return svg_tools.drawing.text(x, y, value, size=size, color="#213547",
			anchor="start", font=FONT)

	def place(fragment: str, x: float, y: float) -> str:
		return f'<g transform="translate({x} {y})">{fragment}</g>'

	body += label(56, 65, "Chromosomes, rearrangements & gene structure", 40)
	body += label(56, 105, "A reusable drawing vocabulary | schematic lengths and bands", 25)
	for y, height in ((140, 390), (550, 490), (1060, 370)):
		body += f'<rect x="32" y="{y}" width="1376" height="{height}" rx="22" fill="#FFFFFF"/>'
	body += label(64, 185, "01  Shape and replication", 30)
	plain = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment("", "#72B9A5"),))
	fragment, _, _ = svg_tools.chromosomes.render_chromosome("tool-plain", plain,
		width=520, height=52, bands=False)
	body += label(80, 232, "Plain color | requested width and height")
	body += place(fragment, 80, 252)
	segments = tuple(svg_tools.chromosomes.Segment(letter, PURPLE, length, band)
		for letter, length, band in zip("ABCDE", (72, 94, 60, 86, 108), (0, 2, 4, 1, 3)))
	unreplicated = svg_tools.chromosomes.Chromosome(segments)
	fragment, _, _ = svg_tools.chromosomes.render_chromosome("tool-banded", unreplicated,
		width=520, height=52)
	body += label(780, 232, "Stable bands | unequal segment lengths")
	body += place(fragment, 780, 252)
	model = svg_tools.chromosomes.Chromosome(segments, centromere_after=2)
	fragment, _, _ = svg_tools.chromosomes.render_chromosome("tool-centromere", model,
		width=520, height=62)
	body += label(80, 362, "One chromatid | centromere after B")
	body += place(fragment, 80, 388)
	fragment, _, _ = svg_tools.chromosomes.render_chromosome("tool-sisters", model,
		width=520, height=100, sisters=True)
	body += label(780, 362, "Sisters | one shared centromere")
	body += place(fragment, 780, 380)
	body += label(80, 503, "Pale constriction = centromere. Matching sisters carry the same segment pattern.", 24)

	body += label(64, 597, "02  Rearrangements preserve segment identity", 30)
	body += label(80, 641, "Deletion | remove C", 28)
	left = svg_tools.chromosomes.Chromosome(tuple(
		svg_tools.chromosomes.Segment(letter, PURPLE, length, band)
		for letter, length, band in zip("ABCDEF", (62, 76, 64, 86, 56, 68), (0, 2, 4, 1, 3, 2))), 4)
	deleted = svg_tools.chromosomes.delete_segments(left, 2, 3)
	for name, chromosome, y, joins, caption in (
		("tool-delete-before", left, 700, (), "Before"),
		("tool-delete-after", deleted, 848, (2,), "After: shorter at the same scale"),
	):
		body += label(80, y-18, caption, 24)
		fragment, _, _ = svg_tools.chromosomes.render_chromosome(name, chromosome,
			height=56, junctions=joins)
		body += place(fragment, 80, y)
	body += label(80, 956, "White zigzag = new junction", 24)
	body += label(80, 994, "Surviving lengths and bands stay fixed.", 24)

	body += label(780, 641, "Reciprocal exchange | distal tails", 28)
	parent_a = svg_tools.chromosomes.Chromosome(tuple(
		svg_tools.chromosomes.Segment(letter, PURPLE, length, band)
		for letter, length, band in zip("ABCDE", (68, 78, 60, 84, 70), (0, 2, 4, 1, 3))), 2)
	parent_b = svg_tools.chromosomes.Chromosome(tuple(
		svg_tools.chromosomes.Segment(letter, BLUE, length, band)
		for letter, length, band in zip("MNOPQ", (76, 64, 86, 58, 74), (3, 1, 2, 4, 0))), 2)
	product_a, product_b = svg_tools.chromosomes.reciprocal_translocation(parent_a, 3, parent_b, 3)
	for name, chromosome, y, joins, caption in (
		("tool-parent-a", parent_a, 686, (), "1"),
		("tool-parent-b", parent_b, 765, (), "2"),
		("tool-product-a", product_a, 874, (3,), "1'"),
		("tool-product-b", product_b, 953, (3,), "2'"),
	):
		body += label(778, y+35, caption, 24)
		fragment, _, boundaries = svg_tools.chromosomes.render_chromosome(name, chromosome,
			height=50, junctions=joins)
		body += place(fragment, 830, y)
		if not joins:
			x = 830 + boundaries[3]
			body += svg_tools.drawing.line(x, y-8, x, y+58, color="#A3293D", width=3, dash="5 4")
	body += label(830, 852, "Exchange DE and PQ; colors follow ancestry", 23)

	body += label(64, 1107, "03  Exons and introns", 30)
	for name, color, introns, y, caption in (
		("tool-dna", "#A4D6EB", (140, 190), 1150, "Genomic DNA"),
		("tool-rna", "#B7DFC7", (0, 0), 1240, "Mature RNA"),
		("tool-cdna", "#EDD18F", (0, 0), 1330, "cDNA"),
	):
		exons = tuple(svg_tools.chromosomes.Segment(str(i+1), color, length)
			for i, length in enumerate((150, 200, 170)))
		fragment, _, _ = svg_tools.gene_tracks.gene_track_svg(name, exons, introns, height=48)
		body += label(80, y+33, caption, 26)
		body += place(fragment, 340, y)
	for x, value in ((415, "Exon 1"), (560, "intron"), (730, "Exon 2"), (925, "intron"), (1105, "Exon 3")):
		body += svg_tools.drawing.text(x, 1220, value, size=21, color="#213547", font=FONT)
	body += label(80, 1475, "Schematic, not a cytogenetic map. DNA tracks show exon blocks and thin intron spans.", 24)
	svg_tools.drawing.write_svg(path, 1440, 1510, "Chromosome tool capability specimen",
		"Original schematic examples: plain rod, reproducible bands, optional centromere, and joined sisters. "
		"Deletion removes C from ABCD, centromere, EF to give ABD, centromere, EF at the same length scale. "
		"Reciprocal translocation exchanges distal DE and PQ between AB, centromere, CDE and MN, centromere, OPQ. "
		"Both products retain their centromeres: AB, centromere, CPQ and MN, centromere, ODE. "
		"Three numbered exon blocks are separated by two thin introns in genomic DNA and adjacent in mature RNA and cDNA. "
		"Decorative bands and lengths do not represent measured cytogenetic or genomic maps. "
		"Original artwork; copyright 2026 Neil R. Voss.", body)


#============================================
def _source_runs(layout: "svg_tools.chromosomes.ChromosomeLayout",
	selected: tuple[svg_tools.chromosomes.Segment, ...]
	) -> tuple[tuple[float, float, float, float], ...]:
	"""Union consecutive selected source anchors per sister without bridging gaps."""
	identities = {id(segment) for segment in selected}
	runs = []
	for sister in sorted({anchor.sister for anchor in layout.segments}):
		bounds = None
		for anchor in (item for item in layout.segments if item.sister == sister):
			if id(anchor.segment) in identities:
				x0, y0, x1, y1 = anchor.bounds
				if bounds is None:
					bounds = (x0, y0, x1, y1)
				else:
					bounds = (min(bounds[0], x0), min(bounds[1], y0),
						max(bounds[2], x1), max(bounds[3], y1))
			elif bounds is not None:
				runs.append(bounds)
				bounds = None
		if bounds is not None:
			runs.append(bounds)
	return tuple(runs)


#============================================
def make_tool_v2_specimen(path: pathlib.Path) -> None:
	"""Show one source map as matched whole chromatids and a literal q31 crop."""
	ink, plum, accent = "#344651", "#72508C", "#963B12"

	def label(x: float, y: float, value: str, size: float = 27,
		color: str = ink) -> str:
		return svg_tools.drawing.text(x, y, value, size=size, color=color,
			anchor="start", font=FONT)

	def bracket(x: float, y0: float, y1: float, color: str) -> str:
		return (f'<path d="M {x-18} {y0} H {x} V {y1} H {x-18}" '
			f'fill="none" stroke="{color}" stroke-width="2.5"/>')

	model, _records = svg_tools.chromosomes.read_cytobands(
		pathlib.Path(__file__).parent / "data/chr7_hg38_cytobands.tsv")
	rod_width = 64
	whole = svg_tools.chromosomes.render_chromosome_layout("v2-chr7", model,
		length=520, thickness=rod_width/.61, orientation="vertical", bands=False,
		labels=False, marker_size=(38, 100))
	sisters = svg_tools.chromosomes.render_chromosome_layout("v2-sisters", model,
		length=520, thickness=rod_width/.26, orientation="vertical", sisters=True,
		bands=False, labels=False, marker_size=(38, 100))
	if whole.centromere is None:
		raise ValueError("Chromosome 7 requires a centromere")

	body = '<rect width="1600" height="860" fill="#FFFFFF"/>'
	body += label(64, 66, "One chromosome, one visual language", 40)
	body += label(64, 108, "Chromosome 7: the same source bands in each view")
	body += label(92, 172, "One chromatid", 29)
	body += label(450, 172, "Two sister chromatids", 29)
	body += label(1010, 172, "q31 enlarged 5x", 29)
	body += label(1010, 208, "A crop of the same chromosome", 24)
	body += f'<defs>{whole.svg}</defs><use href="#v2-chr7" x="115" y="212"/>'
	body += f'<g transform="translate(445 212)">{sisters.svg}</g>'
	cen_y = 212 + whole.centromere[1]
	body += svg_tools.drawing.line(218, cen_y, 279, cen_y, color=plum, width=2)
	body += label(248, cen_y-40, "Centromere", 24, plum)
	body += (f'<path d="M 279 {cen_y-31} V {cen_y} H 518" '
		f'fill="none" stroke="{plum}" stroke-width="2"/>')
	body += label(87, 315, "p", 30)
	q_arm = [a for a in whole.segments if a.segment.label.startswith("q")]
	body += bracket(100, 212+q_arm[0].start[1], 212+q_arm[-1].end[1], ink)
	body += label(65, 625, "q", 30)
	q3 = [a for a in whole.segments if a.segment.label.startswith("q3")]
	body += bracket(240, 212+q3[0].start[1], 212+q3[-1].end[1], ink)
	body += label(252, 212+(q3[0].start[1]+q3[-1].end[1])/2+8, "q3", 25)
	q31 = [a for a in whole.segments if a.segment.label.startswith("q31")]
	y0, y1 = q31[0].start[1], q31[-1].end[1]
	body += bracket(718, 212+y0, 212+y1, accent)
	body += label(730, 212+(y0+y1)/2+8, "q31", 25, accent)

	# Reuse the whole map isotropically; the viewport gives internal bands flat cut ends.
	left = (whole.width-rod_width)/2
	zoom_x, zoom_y, scale = 1000, 365, 5
	zoom_width, zoom_height = rod_width*scale, (y1-y0)*scale
	body += (f'<path d="M 790 {212+(y0+y1)/2} H 890 L 970 {zoom_y+zoom_height/2}" '
		f'fill="none" stroke="{accent}" stroke-width="2"/>')
	body += (f'<svg id="v2-q31-crop" x="{zoom_x}" y="{zoom_y}" '
		f'width="{zoom_width}" height="{zoom_height}" '
		f'viewBox="{left} {y0} {rod_width} {y1-y0}" overflow="hidden">'
		'<use href="#v2-chr7"/></svg>')
	for y in (zoom_y, zoom_y+zoom_height):
		body += (f'<path d="M {zoom_x-8} {y+5} l 16 -10 '
			f'M {zoom_x+zoom_width-8} {y+5} l 16 -10" '
			f'stroke="{ink}" stroke-width="2.24" fill="none"/>')
	for anchor in q31:
		ya = zoom_y+(anchor.start[1]-y0)*scale
		yb = zoom_y+(anchor.end[1]-y0)*scale
		mid = (ya+yb)/2
		color = accent if anchor.segment.label == "q31.2" else ink
		body += svg_tools.drawing.line(zoom_x+zoom_width+10, mid, 1350, mid,
			color=color, width=2)
		body += label(1365, mid+8, anchor.segment.label, 25, color)
		if anchor.segment.label == "q31.2":
			body += (f'<rect x="{zoom_x-5}" y="{ya}" width="{zoom_width+10}" '
				f'height="{yb-ya}" fill="none" stroke="{accent}" stroke-width="3"/>')
	body += label(1010, 310, "CFTR lies in 7q31.2", 28, accent)
	body += label(92, 779, "44 UCSC hg38 cytobands; approximate intervals. CFTR highlight marks a band, not its precise gene interval.", 24)
	body += label(92, 817, "Rounded ends mark whole chromatids; cut ends mark a crop. Caps, necks and markers are schematic.", 24)
	svg_tools.drawing.write_svg(path, 1600, 860, "Chromosome 7 in three matching views",
		"Original editable vector artwork. One chromatid and two sister chromatids use the same "
		"44 UCSC hg38 source intervals, stain values, per-chromatid widths and rounded outlines. "
		"Hollow purple centromere markers leave both lavender acen rows visible. "
		"Brackets show the q arm, q3 region and q31 band; the isotropic five-fold q31 crop "
		"has flat cut ends and shows white subband q31.2. CFTR cytoband location is approximate, "
		"not a precise molecular gene interval. Caps, necks and markers are schematic, not genomic spans. "
		"Source: https://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/cytoBand.txt.gz.", body)

#============================================
def main() -> None:
	"""Write only v2; preserve every saved historical specimen."""
	make_tool_v2_specimen(pathlib.Path(
		"docs/slide-specs/illustration_examples/chromosome_tool_v2.drawn.svg"))


if __name__ == "__main__":
	main()
