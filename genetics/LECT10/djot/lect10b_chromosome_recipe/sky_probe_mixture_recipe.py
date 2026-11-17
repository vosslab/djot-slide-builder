"""Regenerate the source SKY workflow with shared chromosome marks."""
import pathlib
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as DET
import svg_tools.chromosomes

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
HERE = pathlib.Path(__file__).resolve().parent
# Source slide marks: center, major and minor diameters, angle and color.
MARKS = [
	('pale-1',396,563,32,10,0,'#e8e6e7'), ('red',421,551,46,12,-42,'#da2435'),
	('yellow',464,546,46,12,48,'#f0d331'), ('pale-2',488,565,34,10,24,'#e8e6e7'),
	('pale-3',552,563,26,10,0,'#e8e6e7'), ('green',577,551,46,12,-32,'#66a343'),
	('pale-4',608,566,34,10,25,'#e8e6e7'), ('pale-5',644,554,34,10,0,'#e8e6e7'),
	('orange',667,554,18,10,0,'#ed8c2b')]

def main(destination: pathlib.Path) -> None:
	root = DET.parse(HERE / 'templates' / 'sky_probe_mixture_workflow.drawn.svg').getroot()
	slots = {node.get('id'): node for node in root.iter()}
	for name, x, y, length, width, angle, color in MARKS:
		layout = svg_tools.chromosomes.render_chromosome_layout('sky-' + name, svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('',color),)),
			length=length, thickness=width, texture=False, labels=False)
		node = slots['slide-mark-' + name]
		node.set('transform', f'translate({x} {y}) rotate({angle}) translate({-length/2} {-width/2})')
		node.append(DET.fromstring(layout.svg))
	ET.ElementTree(root).write(destination, encoding='ascii', xml_declaration=False)
