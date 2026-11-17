"""Create source-preserving hybrid replacements for the LECT06 introduction panels."""

import pathlib
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as DET
import base64

import svg_tools.chromosomes
import svg_tools.parts


SOURCE_DIR = pathlib.Path(__file__).resolve().parent / 'sources'
SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

SOURCES = {
	'before': SOURCE_DIR / 'chromosome_before_replication.svg',
	'replication': SOURCE_DIR / 'chromosome_replication.svg',
	'separation': SOURCE_DIR / 'chromatid_separation.svg',
}

#============================================
def chromosome(name: str, x: float, y: float, length: float, sisters: bool = False) -> str:
	"""Return one shared-tool chromosome positioned over its source body."""
	model = svg_tools.chromosomes.Chromosome((
		svg_tools.chromosomes.Segment('', '#8A7BC4', 20),
		svg_tools.chromosomes.Segment('', '#8A7BC4', 42),
	), centromeres=(svg_tools.chromosomes.Centromere(1),))
	part = svg_tools.chromosomes.chromosome_part(name, model, length=length,
		thickness=18, orientation='vertical', texture=False, sisters=sisters, labels=False)
	return svg_tools.parts.transform(part, x=x, y=y).fragment


#============================================
def panel_bodies(key: str) -> str:
	"""Place the source states without changing any source layout component."""
	length = 80
	body = chromosome('shared-single', 333, 63, length)
	if key != 'before':
		body += chromosome('shared-sisters', 322, 223, length, sisters=True)
	if key == 'separation':
		body += chromosome('shared-daughter-left', 277, 393, length)
		body += chromosome('shared-daughter-right', 395, 393, length)
	return body


#============================================
def replace_old_body_pixels(root: ET.Element, key: str) -> None:
	"""Use the reviewed frozen pixel layer; source preservation is checked by the package."""
	image = next(element for element in root.iter() if element.attrib.get('id') == 'artwork-1')
	data = (SOURCE_DIR / f'{key}_cleaned.png').read_bytes()
	image.set('{http://www.w3.org/1999/xlink}href',
		'data:image/png;base64,' + base64.b64encode(data).decode('ascii'))


#============================================
def write_panel(key: str, output_dir: pathlib.Path) -> None:
	"""Insert shared chromosome bodies beneath existing leaders and labels."""
	tree = DET.parse(SOURCES[key])
	root = tree.getroot()
	replace_old_body_pixels(root, key)
	canvas = next(element for element in root if element.tag == '{' + SVG + '}g')
	replacement = DET.fromstring(
		'<g xmlns="http://www.w3.org/2000/svg" id="shared-chromosome-bodies">'
		+ panel_bodies(key) + '</g>')
	# Source artwork stays exact; existing leader lines and labels remain above the new bodies.
	canvas.insert(1, replacement)
	root.find('{' + SVG + '}desc').text = (
		'Source-preserving hybrid migration. Original artwork, DNA, TEM image, arrows, '
		'and labels are retained; chromosome bodies use svg_tools.chromosomes.')
	path = output_dir / (SOURCES[key].stem + '.svg')
	tree.write(path, encoding='utf-8', xml_declaration=True)


#============================================
def build(output_dir: pathlib.Path) -> None:
	"""Write the three intro assets to their owning asset directory."""
	output_dir.mkdir(parents=True, exist_ok=True)
	for key in SOURCES:
		write_panel(key, output_dir)
