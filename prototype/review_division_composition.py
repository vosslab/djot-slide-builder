"""Prototype-only crops that keep division explanations as native Djot text."""

from pathlib import Path
import subprocess

import lxml.etree
import svg_tools._xml
import svg_tools.drawing


SVG = '{http://www.w3.org/2000/svg}'



def _write(root: lxml.etree._Element, path: Path) -> None:
	lxml.etree.ElementTree(svg_tools.drawing.svg_root(root)).write(path, encoding='ascii', xml_declaration=True)


def _remove_labels(root: lxml.etree._Element, labels: set[str]) -> None:
	"""Remove the known explanatory labels, retaining the numbered callouts."""
	for parent in list(root.iter()):
		for node in list(parent):
			if node.tag == f'{SVG}text' and node.get('id') in labels:
				parent.remove(node)


def _crop_c13(path: Path) -> None:
	root = svg_tools._xml.read(path)
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
	root = svg_tools._xml.read(path)
	svg_tools.drawing.remove_canvas_background(root)
	nodes = list(root)
	for index in (8, 9, 10, 11, 12, 22, 23):
		root.remove(nodes[index])
	root.set('height', '430')
	root.set('viewBox', '0 0 826 430')
	_write(root, path)


def separate_division_prose() -> None:
	"""Crop the C13/C21 and C25 artwork for the review deck's native prose."""
	root = Path(subprocess.check_output(
		['git', 'rev-parse', '--show-toplevel'], text=True).strip())
	assets = root / 'prototype/assets'
	_crop_c13(assets / 'lect06c-meiosis/recombinant_chromosomes.svg')
	_crop_c25(assets / 'lect09b-tetrads_1_introduction/mitotic_twin_spots.drawn.svg')
