"""Source chromosome positions and labels, with shared chromosome bodies."""
import pathlib
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as DET
import svg_tools.chromosomes

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
HERE = pathlib.Path(__file__).resolve().parent
# Group transforms in the template supply x positions; these are absolute y values.
CENTERS = {'acrocentric':140, 'submetacentric':210, 'metacentric':247}

def main(destination: pathlib.Path) -> None:
	root = DET.parse(HERE / 'templates' / 'centromere_positions.drawn.svg').getroot()
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
		body = DET.fromstring(layout.fragment)
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
	slot.append(DET.fromstring(left.fragment)); slot.append(DET.fromstring(right.fragment))
	marker_group = ET.SubElement(slot, f'{{{NS}}}g', {'transform':'translate(0 96) rotate(90)'})
	marker_group.append(DET.fromstring(marker.fragment))
	ET.ElementTree(root).write(destination,encoding='unicode')
