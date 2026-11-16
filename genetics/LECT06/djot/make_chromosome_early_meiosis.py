#!/usr/bin/env python3
"""Regenerate five early meiosis and homolog/sister figures from frozen sources."""
import pathlib
import xml.etree.ElementTree as ET

import svg_tools.chromosomes

DIRECTORY = pathlib.Path(__file__).resolve().parent
SOURCE = DIRECTORY / 'chromosome_models' / 'early_meiosis'
OUTPUT = DIRECTORY / 'assets' / 'lect06c-meiosis'
NAMES = ('meiosis_interphase', 'prophase_leptotene_zygotene',
	'prophase_pachytene', 'prophase_diplotene_diakinesis',
	'meiosis_homolog_sister_sequence')
NS = '{http://www.w3.org/2000/svg}'
COLORS = {'#087EA4', '#BB2637', '#087faf', '#50a374', '#df8746',
	'#ab597b', '#188e75', '#1684b4'}
EXPECTED = (6, 16, 24, 32, 20)


def main() -> None:
	ET.register_namespace('', NS[1:-1])
	OUTPUT.mkdir(parents=True, exist_ok=True)
	for name, expected in zip(NAMES, EXPECTED):
		root = ET.parse(SOURCE / (name + '.drawn.svg')).getroot()
		count = 0
		for parent in list(root.iter()):
			for index, node in enumerate(list(parent)):
				if node.tag != NS + 'path' or node.get('stroke') not in COLORS:
					continue
				color = node.get('stroke')
				width = float(node.get('stroke-width'))
				model = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('', color, 1),), None)
				part = svg_tools.chromosomes.chromosome_path_part(f'{name}-chromatid-{count}', model,
					node.get('d'), thickness=width, labels=False)
				body = ET.fromstring(part.fragment)
				if node.get('id'):
					body.set('id', node.get('id'))
				if node.get('data-chromatid'):
					body.set('data-chromatid', node.get('data-chromatid'))
				parent.remove(node)
				parent.insert(index, body)
				count += 1
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
		output = OUTPUT / (name + '.drawn.svg')
		output.write_text(ET.tostring(root, encoding='unicode') + '\n')

		print(name, count)


if __name__ == '__main__':
	main()
