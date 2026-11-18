#!/usr/bin/env python3
"""Regenerate five early meiosis and homolog/sister figures from frozen sources."""
import argparse
import pathlib
import subprocess

import lxml.etree
import svg_tools._xml
import svg_tools.chromosomes
import svg_tools.drawing

REPOSITORY_ROOT = pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip())
DIRECTORY = REPOSITORY_ROOT / 'genetics/LECT06/djot'
SOURCE = DIRECTORY / 'chromosome_models' / 'early_meiosis'
OUTPUT = DIRECTORY / 'assets' / 'lect06c-meiosis'
NAMES = ('meiosis_interphase', 'prophase_leptotene_zygotene',
	'prophase_pachytene', 'prophase_diplotene_diakinesis',
	'meiosis_homolog_sister_sequence')
NS = '{http://www.w3.org/2000/svg}'
COLORS = {'#087EA4', '#BB2637', '#087faf', '#50a374', '#df8746',
	'#ab597b', '#188e75', '#1684b4'}
EXPECTED = (6, 16, 24, 32, 20)
CONDENSED = ('prophase_diplotene_diakinesis', 'meiosis_homolog_sister_sequence')


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--output-root', type=pathlib.Path, default=DIRECTORY / 'assets')
	args = parser.parse_args()
	output_dir = args.output_root / 'lect06c-meiosis'

	output_dir.mkdir(parents=True, exist_ok=True)
	for name, expected in zip(NAMES, EXPECTED):
		root = svg_tools._xml.read(SOURCE / (name + '.drawn.svg'))
		count = 0
		for parent in list(root.iter()):
			for index, node in enumerate(list(parent)):
				if node.tag != NS + 'path' or node.get('stroke') not in COLORS:
					continue
				count += 1
				# The pachytene source tags its condensed rods with data-chromatid.
				if name not in CONDENSED and node.get('data-chromatid') is None:
					continue
				color = node.get('stroke')
				width = float(node.get('stroke-width'))
				model = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('', color, 1),))
				part = svg_tools.chromosomes.chromosome_path_part(f'{name}-chromatid-{count-1}', model,
					node.get('d'), thickness=width, labels=False)
				body = svg_tools._xml.parse(part.fragment)
				if node.get('id'):
					body.set('id', node.get('id'))
				if node.get('data-chromatid'):
					body.set('data-chromatid', node.get('data-chromatid'))
				parent.remove(node)
				parent.insert(index, body)
		if count != expected:
			raise ValueError(f'{name}: expected {expected} source bodies, found {count}')
		# Retain the source's explicitly located centromeres and chiasma overlays.
		for node in root.iter():
			if node.get('data-centromere') == 'true' or node.get('id', '').endswith('-center'):
				node.set('fill', 'none')
				node.set('stroke', '#72508C')
			# Interphase circles are the only original circles inside after groups.
		for group in root.iter(NS + 'g'):
			if group.get('id') in ('after0', 'after1'):
				for circle in group.findall(NS + 'circle'):
					circle.set('fill', 'none')
					circle.set('stroke', '#72508C')
		svg_tools.drawing.remove_canvas_background(root)
		output = output_dir / (name + '.drawn.svg')
		output.write_text(lxml.etree.tostring(svg_tools.drawing.svg_root(root), encoding='unicode') + '\n')

		print(name, count)


if __name__ == '__main__':
	main()
