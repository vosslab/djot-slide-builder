"""Source chromosome positions and labels, with shared chromosome bodies."""
import pathlib
import xml.etree.ElementTree
import svg_tools.chromosomes

NS = 'http://www.w3.org/2000/svg'
xml.etree.ElementTree.register_namespace('', NS)
HERE = pathlib.Path(__file__).resolve().parent
# Group transforms in the template supply x positions; these are absolute y values.
CENTERS = {'acrocentric':140, 'submetacentric':210, 'metacentric':247}

def main(destination: pathlib.Path) -> None:
	root = xml.etree.ElementTree.parse(HERE / 'templates' / 'centromere_positions.drawn.svg').getroot()
	slots = {node.get('id'): node for node in root.iter()}
	for name, center in CENTERS.items():
		top, length, thickness = 84, 326, 130
		body_height = thickness*.26
		cap, collar = min(body_height*.5,length*.08), min(body_height*.48,length*.06)
		fraction = (center-top-cap-collar/2)/(length-2*cap-collar)
		model = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('','#4c9ec7',fraction), svg_tools.chromosomes.Segment('','#4c9ec7',1-fraction)),1)
		layout = svg_tools.chromosomes.render_chromosome_layout(name+'-v2',model,length=length,thickness=thickness,
			orientation='vertical',sisters=True,bands=False,labels=False)
		slot = slots[name+'-body-slot']; slot.set('transform',f'translate(-65 {top})')
		slot.append(xml.etree.ElementTree.fromstring(layout.svg))
	# Rounded caps terminate at y=96; there is no p arm above the marker.
	model = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('', '#4c9ec7'),))
	left = svg_tools.chromosomes.chromosome_path_part('telocentric-left-v2', model,
		'M -10 112 C -14 190 -42 330 -48 394', thickness=30, labels=False)
	right = svg_tools.chromosomes.chromosome_path_part('telocentric-right-v2', model,
		'M 10 112 C 14 190 42 330 48 394', thickness=30, labels=False)
	marker = svg_tools.chromosomes.centromere_part('telocentric-terminal-v2', thickness=30)
	slot = slots['telocentric-body-slot']
	slot.append(xml.etree.ElementTree.fromstring(left.fragment)); slot.append(xml.etree.ElementTree.fromstring(right.fragment))
	marker_group = xml.etree.ElementTree.SubElement(slot, f'{{{NS}}}g', {'transform':'translate(0 96) rotate(90)'})
	marker_group.append(xml.etree.ElementTree.fromstring(marker.fragment))
	xml.etree.ElementTree.ElementTree(root).write(destination,encoding='unicode')
