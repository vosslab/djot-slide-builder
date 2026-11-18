"""Prototype detail views of C63's dense gamete-product overview."""

import copy
import json
import pathlib
import subprocess

import lxml.etree
import svg_tools._xml



SVG = '{http://www.w3.org/2000/svg}'



def make_gamete_details() -> None:
	"""Keep the overview and enlarge its first two columns and final column separately."""
	root = pathlib.Path(subprocess.check_output(
		['git', 'rev-parse', '--show-toplevel'], text=True).strip())
	data = json.loads((root / 'genetics/LECT13/djot/lect13d_p1_composition_data.json').read_text())
	placements = data['figures']['lect13d_p1_gametes']['parts']
	directory = root / 'prototype/chromosome_assets/assets/lect13d-meiosis_translocation'
	source = svg_tools._xml.read(directory / 'lect13d_p1_gametes.drawn.svg')
	for suffix, left, width in (('left_middle', 0, 1866), ('right', 1866, 934)):
		panel = copy.deepcopy(source)
		canvas = panel.find(SVG+'g')
		for node, placement in zip(list(canvas), placements):
			if not left <= placement['x'] < left+width:
				canvas.remove(node)
		panel.set('width', str(width))
		panel.set('viewBox', f'{left} 0 {width} 700')
		columns = 'first two columns' if left == 0 else 'final column'
		panel.find(SVG+'title').text = f'Gamete products: {columns}'
		panel.find(SVG+'desc').text = (
			f'Enlarged {columns} of the gamete-product overview. '
			'Chromosome identities, locus positions and allele states follow the source components.')
		path = directory / f'lect13d_p1_gametes_{suffix}.drawn.svg'
		path.write_bytes(lxml.etree.tostring(panel, encoding='ascii', xml_declaration=True))
