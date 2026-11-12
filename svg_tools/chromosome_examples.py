#!/usr/bin/env python3
"""Reproduce the chromosome language specimen and four LECT11 pilot candidates.

Run from the repository root: python3 -m svg_tools.chromosome_examples
Course assets are deliberately not written by this recipe.
"""

import pathlib

import svg_tools.drawing
import svg_tools.chromosomes

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
def main() -> None:
	"""Write the durable specimen and review-only overview candidates."""
	make_specimen(pathlib.Path("docs/slide-specs/illustration_examples/chromosome_language.drawn.svg"))
	make_overviews(pathlib.Path("_temp/chromosome_visual_language/implementation"))


if __name__ == "__main__":
	main()
