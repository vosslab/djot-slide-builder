"""Prototype-only crops that put inversion explanations in native Djot text."""

from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET


SVG = '{http://www.w3.org/2000/svg}'
ET.register_namespace('', 'http://www.w3.org/2000/svg')


def _write(root: ET.Element, path: Path) -> None:
	ET.ElementTree(root).write(path, encoding='ascii', xml_declaration=True)


def _canvas(root: ET.Element) -> ET.Element:
	return root.find(f'{SVG}g')


def _remove_text(canvas: ET.Element, values: set[str]) -> None:
	for node in list(canvas):
		if node.tag == f'{SVG}text' and ''.join(node.itertext()) in values:
			canvas.remove(node)


def _crop(root: ET.Element, width: int, height: int, y: int = 0) -> None:
	root.set('width', str(width))
	root.set('height', str(height))
	root.set('viewBox', f'0 {y} {width} {height}')


def _split_c55(path: Path) -> None:
	"""Split the overview and the loop into two compact, independent panels."""
	original = ET.parse(path).getroot()

	left = deepcopy(original)
	left_canvas = _canvas(left)
	for node in list(left_canvas)[32:]:
		left_canvas.remove(node)
	_crop(left, 1000, 390)
	_write(left, path)

	right = deepcopy(original)
	right_canvas = _canvas(right)
	# defs plus the transition arrow and the loop assembly are all this panel needs.
	for index, node in reversed(list(enumerate(list(right_canvas)))):
		if index != 0 and not 33 <= index <= 42:
			right_canvas.remove(node)
	_crop(right, 1000, 500, 380)
	right_path = path.with_name('inversion-synapsis-loop.drawn.svg')
	_write(right, right_path)


def separate_inversion_prose() -> None:
	"""Apply the fixed C55, C56, and C59 review compositions after recipes run."""
	assets = Path(__file__).resolve().parent / 'chromosome_assets/assets/lect13b-chromo_alter_3-inversion'

	_split_c55(assets / 'inversion-synapsis.drawn.svg')

	path = assets / 'paracentric-anaphase.drawn.svg'
	root = ET.parse(path).getroot()
	canvas = _canvas(root)
	_remove_text(canvas, {
		'When the centromere is not included in the inverted region, one of the crossover products',
		'is a dicentric chromosome, and the reciprocal product is an acentric chromosome.',
		'Among the two chromatids not involved in the crossover, one carries the inversion and',
		'the other the normal gene sequence.',
	})
	for node in list(canvas):
		if node.get('d') == 'M 30,590 H 1420':
			canvas.remove(node)
	_crop(root, 1460, 590)
	_write(root, path)

	path = assets / 'inversion-double-crossover-problem.drawn.svg'
	root = ET.parse(path).getroot()
	canvas = _canvas(root)
	_remove_text(canvas, {
		'First crossover: between B/b and C/c',
		'Only the inverted region is shown paired; ends are unpaired.',
	})
	_crop(root, 1000, 430)
	_write(root, path)
