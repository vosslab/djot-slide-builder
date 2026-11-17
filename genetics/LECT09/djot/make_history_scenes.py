#!/usr/bin/env python3
"""Rebuild three crossover scenes; preserve the source's native ascus and labels."""
import argparse
import pathlib
import defusedxml.ElementTree as ET
import subprocess
import svg_tools.chromosomes
import svgpathtools

BASE = pathlib.Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()) / 'genetics/LECT09/djot'
TEMPLATES = BASE / 'assets/lect09_history_scene_templates'
OUTPUT = BASE / 'assets/lect09e-tetrad_visuals'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
BROWN, OCHRE = '#774627', '#BD760E'
# The inner chromatids cross first. The outer chromatids cross later in the DCO.
paths = {
	'nco_to_pd': [('M 95 60 C 160 60 175 90 210 90 C 255 90 270 60 320 60 L 590 60', BROWN, BROWN),
	('M 95 150 C 160 150 175 110 210 110 C 255 110 270 150 320 150 L 590 150', BROWN, BROWN),
	('M 95 220 C 160 220 175 250 210 250 C 255 250 270 220 320 220 L 590 220', OCHRE, OCHRE),
	('M 95 310 C 160 310 175 270 210 270 C 255 270 270 310 320 310 L 590 310', OCHRE, OCHRE)],
	'sco_to_tt': [('M 95 60 C 160 60 175 90 210 90 C 255 90 270 60 320 60 L 590 60', BROWN, BROWN),
	('M 95 150 C 160 150 175 110 210 110 C 270 110 300 150 350 185 C 400 220 430 220 590 220', BROWN, OCHRE),
	('M 95 220 C 160 220 175 250 210 250 C 270 250 300 220 350 185 C 400 150 430 150 590 150', OCHRE, BROWN),
	('M 95 310 C 160 310 175 270 210 270 C 255 270 270 310 320 310 L 590 310', OCHRE, OCHRE)],
	'four_strand_dco_to_npd': [('M 95 60 C 160 60 175 90 210 90 C 255 90 270 60 320 60 C 410 60 410 185 455 185 C 500 185 500 310 590 310', BROWN, OCHRE),
	('M 95 150 C 160 150 175 110 210 110 C 270 110 300 150 350 185 C 400 220 430 220 590 220', BROWN, OCHRE),
	('M 95 220 C 160 220 175 250 210 250 C 270 250 300 220 350 185 C 400 150 430 150 590 150', OCHRE, BROWN),
	('M 95 310 C 160 310 175 270 210 270 C 255 270 270 310 320 310 C 410 310 410 185 455 185 C 500 185 500 60 590 60', OCHRE, BROWN)],
}


def distance_at_x(curve: svgpathtools.Path, x: float) -> float:
	"""Return the arc distance of one known locus on a left-to-right chromatid."""
	low, high = 0., 1.
	for _ in range(40):
		middle = (low + high) / 2
		if curve.point(middle).real < x:
			low = middle
		else:
			high = middle
	distance = curve.length(0, (low + high) / 2)
	return distance


def chromatid_segments(curve: svgpathtools.Path, crossover: float, proximal: str, distal: str,
	alleles: tuple[str, str]) -> tuple[svg_tools.chromosomes.Segment, ...]:
	"""Place the two established loci as contrasting, labelled chromosome regions."""
	markers = []
	for x, allele in zip((275., 550.), alleles):
		center = distance_at_x(curve, x)
		markers.append((center-18, center+18, allele))
	boundaries = sorted({0., crossover, curve.length(),
		*(value for marker in markers for value in marker[:2])})
	regions = []
	for start, end in zip(boundaries, boundaries[1:]):
		label = next((marker[2] for marker in markers
			if start == marker[0] and end == marker[1]), '')
		color = '#F3D788' if label else (proximal if (start+end)/2 < crossover else distal)
		regions.append(svg_tools.chromosomes.Segment(label, color, end-start))
	return tuple(regions)


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--output-root', type=pathlib.Path, default=OUTPUT.parent)
	args = parser.parse_args()
	output = args.output_root / 'lect09e-tetrad_visuals'
	for name, strands in paths.items():
		root = ET.parse(TEMPLATES / (name + '.svg')).getroot()
		viewport = next(e for e in root if e.tag == f'{{{NS}}}g')
		scene = ET.Element('g', {'id':'chromosome-scene'})
		viewport.insert(0, scene)
		for i, (path, left, right) in enumerate(strands):
			curve = svgpathtools.parse_path(path)
			cross_x = 455 if name == 'four_strand_dco_to_npd' and i in (0, 3) else 350
			before = distance_at_x(curve, float(cross_x))
			alleles = ('A' if left == BROWN else 'a', 'B' if right == BROWN else 'b')
			model = svg_tools.chromosomes.Chromosome(
				chromatid_segments(curve, before, left, right, alleles))
			part = svg_tools.chromosomes.chromosome_path_part(
				f'chromatid-{i+1}', model, path, thickness=34, labels=True)
			group = ET.SubElement(scene, 'g', {'id': f'strand-{i+1}', 'data-chromatid':'true', 'data-product': ('AB','Ab','aB','ab')[i] if name == 'sco_to_tt' else (('AB','AB','ab','ab')[i] if name == 'nco_to_pd' else ('Ab','Ab','aB','aB')[i])})
			group.append(ET.fromstring(part.fragment))
		for i, y in enumerate((100, 260), start=1):
			marker = ET.fromstring(svg_tools.chromosomes.centromere_part(f'marker-{i}', thickness=34, across=20+34*1.3).fragment)
			marker.set('transform', f'translate(210 {y})')
			scene.append(marker)
		if name == 'four_strand_dco_to_npd':
			title = ET.SubElement(scene, f'{{{NS}}}text', {'x':'50', 'y':'28', 'font-family':'Atkinson Hyperlegible Next', 'font-size':'25', 'fill':'#172B3A'})
			title.text = '4-strand double crossing over'
		output.mkdir(parents=True, exist_ok=True)
		out = output / (name + '.svg')
		ET.ElementTree(root).write(out, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
	main()
