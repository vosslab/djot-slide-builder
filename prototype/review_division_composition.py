"""Prototype-only crops that keep division explanations as native Djot text."""

from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as DET

import svg_tools.drawing


SVG = '{http://www.w3.org/2000/svg}'
ET.register_namespace('', 'http://www.w3.org/2000/svg')


def _write(root: ET.Element, path: Path) -> None:
	ET.ElementTree(root).write(path, encoding='ascii', xml_declaration=True)


def _remove_labels(root: ET.Element, labels: set[str]) -> None:
	"""Remove the known explanatory labels, retaining the numbered callouts."""
	for parent in root.iter():
		for node in list(parent):
			if node.tag == f'{SVG}text' and node.get('id') in labels:
				parent.remove(node)


def _crop_c13(path: Path) -> None:
	root = DET.parse(path).getroot()
	_remove_labels(root, {
		'label-14', 'label-15', 'label-16',
		'label-17', 'label-18',
		'label-19', 'label-20', 'label-21', 'label-22',
		'label-23', 'label-24', 'label-25', 'label-26',
	})
	root.find(f'{SVG}desc').text = (
		'Recombinant chromosomes through meiosis. Numbered explanatory steps are native slide text.'
	)
	_write(root, path)


def _crop_c25(path: Path) -> None:
	root = DET.parse(path).getroot()
	svg_tools.drawing.remove_canvas_background(root)
	nodes = list(root)
	for index in (8, 9, 10, 11, 12, 22, 23):
		root.remove(nodes[index])
	root.set('height', '430')
	root.set('viewBox', '0 0 826 430')
	_write(root, path)


def separate_division_prose() -> None:
	"""Move the fixed C13, C21, and C25 prose into their Djot slides."""
	root = Path(subprocess.check_output(
		['git', 'rev-parse', '--show-toplevel'], text=True).strip())
	assets = root / 'prototype/assets'
	c13 = assets / 'lect06c-meiosis/recombinant_chromosomes.svg'
	_crop_c13(c13)
	(assets / 'lect08b-chap8-linked_genes/b31_labeled.svg').write_bytes(c13.read_bytes())
	_crop_c25(assets / 'lect09b-tetrads_1_introduction/mitotic_twin_spots.drawn.svg')
