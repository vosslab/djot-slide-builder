#!/usr/bin/env python3
"""Regenerate source-preserving shared-family chromosome figures.

Source facts are retained below; source illustrations are schematic, not measurements.
Nonchromosome labels, connectors, background and figure dimensions remain source-authored.
"""
import pathlib
import subprocess
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as DET
import svg_tools.chromosomes as chromosomes
import svg_tools.parts as parts

FIGURES = [{'path': 'genetics/LECT03/djot/assets/lect03b-blood_hla_typing/hla_region.drawn.svg', 'template': '<svg width="1200" height="720" viewBox="0 0 1200 720" role="img" aria-labelledby="title desc" xmlns="http://www.w3.org/2000/svg"><title id="title">HLA genes on chromosome 6</title><desc id="desc">Original Genetics LECT03B drawing. Source long arm left and short arm right retained; classII DP,DQ,DR then classI B,C,A. Schematic order, not genomic scale.</desc><g font-family="Atkinson Hyperlegible Next, sans-serif"><text x="600" y="45" font-size="32" fill="#243746" text-anchor="middle">Chromosome 6</text><g data-slot="chromosome-6" /><text x="400" y="205" font-size="28" fill="#243746" text-anchor="middle">Long arm</text><text x="940" y="205" font-size="28" fill="#243746" text-anchor="middle">Short arm</text><text x="870" y="250" font-size="28" fill="#243746" text-anchor="middle">HLA region</text><path d="M850 165 L90 360" stroke="#607580" stroke-width="4" fill="none" /><path d="M895 165 L1110 360" stroke="#607580" stroke-width="4" fill="none" /><path d="M90 460 L1110 460" stroke="#D5A7B5" stroke-width="20" fill="none" /><path d="M120 430 L120 490" stroke="#287A43" stroke-width="14" fill="none" /><text x="120" y="535" font-size="30" fill="#243746" text-anchor="middle">DP</text><path d="M270 430 L270 490" stroke="#287A43" stroke-width="14" fill="none" /><text x="270" y="535" font-size="30" fill="#243746" text-anchor="middle">DQ</text><path d="M420 430 L420 490" stroke="#287A43" stroke-width="14" fill="none" /><text x="420" y="535" font-size="30" fill="#243746" text-anchor="middle">DR</text><path d="M800 430 L800 490" stroke="#168DA5" stroke-width="14" fill="none" /><text x="800" y="535" font-size="30" fill="#243746" text-anchor="middle">B</text><path d="M900 430 L900 490" stroke="#168DA5" stroke-width="14" fill="none" /><text x="900" y="535" font-size="30" fill="#243746" text-anchor="middle">C</text><path d="M1090 430 L1090 490" stroke="#168DA5" stroke-width="14" fill="none" /><text x="1090" y="535" font-size="30" fill="#243746" text-anchor="middle">A</text><text x="270" y="380" font-size="32" fill="#243746" text-anchor="middle">Class II</text><text x="950" y="380" font-size="32" fill="#243746" text-anchor="middle">Class I</text></g></svg>', 'source': 'Source long arm left, centromere x752.5, short arm right. HLA interval x850-895; ClassII DP DQ DR then ClassI B C A. Preserve lower molecular track.'}]


def build(root: ET.Element, item: dict) -> None:
	# Source arm split and HLA interval positions are schematic, not genomic coordinates.
	start, end, centromere = 100.0, 1090.0, 752.5
	thickness = 75.0
	cap, collar = thickness*.61*.5, thickness*.61*.48
	boundaries = (start+cap, centromere-collar/2, centromere+collar/2, 850, 895, end-cap)
	model = chromosomes.Chromosome(tuple(chromosomes.Segment('',color,length) for color,length in (
		('#B6D8C8', boundaries[1]-boundaries[0]),
		('#B6D8C8', boundaries[3]-boundaries[2]),
		('#D95358', boundaries[4]-boundaries[3]),
		('#B6D8C8', boundaries[5]-boundaries[4]))),
		(chromosomes.Centromere(1),))
	part = chromosomes.chromosome_part('hla-chromosome-6', model, length=end-start, thickness=thickness, texture=False, labels=False)
	part = parts.transform(part, start, 85)
	next(e for e in root.iter() if e.get('data-slot')=='chromosome-6').append(DET.fromstring(part.fragment))


def main(output_root: pathlib.Path) -> None:
	for item in FIGURES:
		root = DET.fromstring(item['template'])
		build(root, item)
		for element in root.iter():
			if not element.tag.startswith('{'):
				element.tag = '{http://www.w3.org/2000/svg}' + element.tag
		ET.register_namespace('', 'http://www.w3.org/2000/svg')
		path = output_root / item['path']
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_text(ET.tostring(root, encoding='unicode'), encoding='utf-8')


if __name__ == '__main__':
	import sys
	root = pathlib.Path(subprocess.check_output(
		['git', 'rev-parse', '--show-toplevel'], text=True).strip())
	main(pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root)
