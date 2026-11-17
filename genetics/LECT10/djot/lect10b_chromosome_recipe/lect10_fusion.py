"""Regenerate the source fusion diagram and preserve its band and activity evidence."""
import pathlib
import xml.etree.ElementTree
import svg_tools.chromosomes

NS = 'http://www.w3.org/2000/svg'
xml.etree.ElementTree.register_namespace('', NS)
HERE = pathlib.Path(__file__).resolve().parent
BODIES = [('ancestor-a',77,100,150,[(220,'active')]),
	('ancestor-b',162,275,180,[(305,'active')]),
	('dicentric',402,100,355,[(220,'active'),(285,'active')]),
	('inactivation',702,100,355,[(220,'active'),(285,'inactive')]),
	('human-2',1002,100,355,[(220,'active')])]

def main(destination: pathlib.Path) -> None:
	root = xml.etree.ElementTree.parse(HERE / 'templates' / 'human_chromosome_2_fusion.drawn.svg').getroot()
	slots = {node.get('id'): node for node in root.iter()}
	for name, x, y, length, centromeres in BODIES:
		locations = [location-y for location, _ in centromeres]
		limits = [0, *locations, length]
		model = svg_tools.chromosomes.Chromosome(
			tuple(svg_tools.chromosomes.Segment('', '#EBD8A0', stop-start)
				for start, stop in zip(limits, limits[1:])),
			tuple(svg_tools.chromosomes.Centromere(index, active == 'active')
				for index, (_, active) in enumerate(centromeres, 1)))
		layout = svg_tools.chromosomes.chromosome_path_part(name+'-v2', model,
			'M 18 0 L 18 ' + str(length), thickness=36, labels=False)
		slot = slots[name+'-body-slot']; slot.set('transform',f'translate({x} {y})')
		slot.append(xml.etree.ElementTree.fromstring(layout.fragment))
		group = slots[name]
		for child in list(group):
			if child.tag == f'{{{NS}}}circle':
				group.remove(child)
	xml.etree.ElementTree.ElementTree(root).write(destination,encoding='unicode')
