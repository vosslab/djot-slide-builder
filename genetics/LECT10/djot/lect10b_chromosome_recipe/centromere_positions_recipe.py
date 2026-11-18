"""Source chromosome positions and labels, with shared chromosome bodies."""
import pathlib
import subprocess
import lxml.etree
import svg_tools._xml
import svg_tools.chromosomes
import svg_tools.drawing

NS = 'http://www.w3.org/2000/svg'

HERE = pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip()) / 'genetics/LECT10/djot/lect10b_chromosome_recipe'
# Group transforms in the template supply x positions; these are absolute y values.
CENTERS = {'acrocentric':140, 'submetacentric':210, 'metacentric':247}

def main(destination: pathlib.Path) -> None:
	root = svg_tools._xml.read(HERE / 'templates' / 'centromere_positions.drawn.svg')
	slots = {node.get('id'): node for node in root.iter()}
	for name, center in CENTERS.items():
		top, length = 84, 326
		fraction = (center-top) / length
		models = tuple(svg_tools.chromosomes.Chromosome((
			svg_tools.chromosomes.Segment('', '#4c9ec7', fraction),
			svg_tools.chromosomes.Segment('', '#4c9ec7', 1-fraction)),
			(svg_tools.chromosomes.Centromere(1),)) for _ in range(2))
		chromatids = tuple((model, f'M {46 + index * 38} 0 L {46 + index * 38} {length}')
			for index, model in enumerate(models))
		layout = svg_tools.chromosomes.sister_chromatid_parts(name, chromatids,
			thickness=28, labels=False)
		body = svg_tools._xml.parse(layout.fragment)
		slot = slots[name+'-body-slot']; slot.set('transform',f'translate(-65 {top})')
		slot.append(body)
	# Rounded caps terminate at y=96; there is no p arm above the marker.
	model = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('', '#4c9ec7'),))
	left = svg_tools.chromosomes.chromosome_path_part('telocentric-left-v2', model,
		'M -10 112 C -14 190 -42 330 -48 394', thickness=30, labels=False)
	right = svg_tools.chromosomes.chromosome_path_part('telocentric-right-v2', model,
		'M 10 112 C 14 190 42 330 48 394', thickness=30, labels=False)
	marker = svg_tools.chromosomes.centromere_part('telocentric-terminal-v2', thickness=30, across=65)
	slot = slots['telocentric-body-slot']
	slot.append(svg_tools._xml.parse(left.fragment)); slot.append(svg_tools._xml.parse(right.fragment))
	marker_group = lxml.etree.SubElement(slot, f'{{{NS}}}g', {'transform':'translate(0 96) rotate(90)'})
	marker_group.append(svg_tools._xml.parse(marker.fragment))
	svg_tools.drawing.remove_canvas_background(root)
	lxml.etree.ElementTree(svg_tools.drawing.svg_root(root)).write(destination,encoding='utf-8')
