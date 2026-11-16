#!/usr/bin/env python3
"""Rebuild three crossover scenes; preserve the source's native ascus and labels."""
import pathlib
import xml.etree.ElementTree as ET
import svg_tools.chromosomes
import svgpathtools

BASE = pathlib.Path(__file__).resolve().parent
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
def main() -> None:
	for name, strands in paths.items():
		root = ET.parse(TEMPLATES / (name + '.svg')).getroot()
		viewport = next(e for e in root if e.tag == f'{{{NS}}}g')
		scene = ET.Element('g', {'id':'chromosome-scene'})
		viewport.insert(0, scene)
		for i, (path, left, right) in enumerate(strands):
			curve = svgpathtools.parse_path(path)
			cross_x = 455 if name == 'four_strand_dco_to_npd' and i in (0, 3) else 350
			pieces = list(curve)
			cross = next((j+1 for j, piece in enumerate(pieces) if abs(piece.end.real-cross_x) < .01), None)
			before = sum(piece.length() for piece in pieces[:cross]) if cross else curve.length()/2
			after = curve.length()-before
			model = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('proximal', left, before), svg_tools.chromosomes.Segment('distal', right, after)))
			part = svg_tools.chromosomes.chromosome_path_part(f'chromatid-{i+1}', model, path, thickness=34, labels=False)
			group = ET.SubElement(scene, 'g', {'id': f'strand-{i+1}', 'data-chromatid':'true', 'data-product': ('AB','Ab','aB','ab')[i] if name == 'sco_to_tt' else (('AB','AB','ab','ab')[i] if name == 'nco_to_pd' else ('Ab','Ab','aB','aB')[i])})
			group.append(ET.fromstring(part.fragment))
		for i, y in enumerate((100, 260), start=1):
			marker = ET.fromstring(svg_tools.chromosomes.centromere_part(f'marker-{i}', thickness=34).fragment)
			marker.set('transform', f'translate(210 {y})')
			scene.append(marker)
		if name == 'four_strand_dco_to_npd':
			title = ET.SubElement(scene, f'{{{NS}}}text', {'x':'50', 'y':'28', 'font-family':'Atkinson Hyperlegible Next', 'font-size':'25', 'fill':'#172B3A'})
			title.text = '4-strand double crossing over'
		# Alleles on the source chromosome illustration, separate from the retained ascus labels.
		def y_at_x(path: str, x: float) -> float:
			curve = svgpathtools.parse_path(path)
			low, high = 0., 1.
			for _ in range(40):
				mid = (low + high) / 2
				if curve.point(mid).real < x: low = mid
				else: high = mid
			return curve.point((low + high) / 2).imag
		for x, ys, letters in [(275,[y_at_x(p, 275) for p, _, _ in strands],['A','A','a','a']), (550,[60,150,220,310],['B','B','b','b'])]:
			for y, letter in zip(ys, letters):
				t = ET.SubElement(scene, f'{{{NS}}}text', {'x':str(x),'y':str(y+9),'text-anchor':'middle','font-family':'Atkinson Hyperlegible Next','font-size':'35','font-style':'italic','fill':'white','data-allele':'true'})
				t.text = letter
		OUTPUT.mkdir(parents=True, exist_ok=True)
		out = OUTPUT / (name + '.svg')
		ET.ElementTree(root).write(out, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
	main()
