"""Regenerate the source SKY workflow with shared chromosome marks."""
import pathlib
import subprocess
import lxml.etree
import svg_tools._xml
import svg_tools.chromosomes
import svg_tools.drawing

NS = 'http://www.w3.org/2000/svg'

HERE = pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip()) / 'genetics/LECT10/djot/lect10b_chromosome_recipe'
# Source slide marks: center, major and minor diameters, angle and color.
MARKS = [
	('pale-1',396,563,32,10,0,'#e8e6e7'), ('red',421,551,46,12,-42,'#da2435'),
	('yellow',464,546,46,12,48,'#f0d331'), ('pale-2',488,565,34,10,24,'#e8e6e7'),
	('pale-3',552,563,26,10,0,'#e8e6e7'), ('green',577,551,46,12,-32,'#66a343'),
	('pale-4',608,566,34,10,25,'#e8e6e7'), ('pale-5',644,554,34,10,0,'#e8e6e7'),
	('orange',667,554,18,10,0,'#ed8c2b')]

def main(destination: pathlib.Path) -> None:
	root = svg_tools._xml.read(HERE / 'templates' / 'sky_probe_mixture_workflow.drawn.svg')
	slots = {node.get('id'): node for node in root.iter()}
	for name, x, y, length, width, angle, color in MARKS:
		layout = svg_tools.chromosomes.render_chromosome_layout('sky-' + name, svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('',color),)),
			length=length, thickness=width, texture=False, labels=False)
		node = slots['slide-mark-' + name]
		node.set('transform', f'translate({x} {y}) rotate({angle}) translate({-length/2} {-width/2})')
		node.append(svg_tools._xml.parse(layout.svg))
	svg_tools.drawing.remove_canvas_background(root)
	lxml.etree.ElementTree(svg_tools.drawing.svg_root(root)).write(destination, encoding='ascii', xml_declaration=False)
