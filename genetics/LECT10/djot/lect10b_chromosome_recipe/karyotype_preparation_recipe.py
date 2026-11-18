"""Replace only the embedded schematic; retain the empirical image bytes."""
import pathlib
import subprocess
import svgpathtools
import lxml.etree
import svg_tools._xml
import svg_tools.chromosomes
import svg_tools.chromosome_surface
import svg_tools.drawing

NS = 'http://www.w3.org/2000/svg'
XLINK = 'http://www.w3.org/1999/xlink'


HERE = pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip()) / 'genetics/LECT10/djot/lect10b_chromosome_recipe'
# Approximate source band boundaries and colors read from the embedded illustration.
# The image's empirical right panel begins at x=330; the mask ends at x=190.
BANDS = [(190,219,'#d41489'), (219,235,'#f3ad59'), (235,267,'#258068'),
	(267,281,'#007096'), (281,293,'#f0ae5b'), (293,301,'#258068'),
	(301,311,'#258068'), (311,324,'#e4e77b'), (324,349,'#f3ae5c'),
	(349,357,'#26836b'), (357,374,'#a2cf68'), (374,382,'#258068'),
	(382,394,'#f3ad59'), (394,400,'#007096'), (400,427,'#d41489')]
# Each source homolog comprises two side-by-side sisters converging at y=301.
CENTERLINES = [((190,55),(301,92),(427,52)), ((190,64),(301,99),(427,61)),
	((190,169),(301,116),(427,137)), ((190,178),(301,123),(427,146))]


#============================================
def distance_at_y(path: svgpathtools.Path, y: float) -> float:
	"""Keep each source band at its recorded height on the downward-running spine."""
	if y == path.start.imag:
		return 0.0
	if y == path.end.imag:
		return path.length()
	low, high = 0.0, 1.0
	for _ in range(40):
		middle = (low + high)/2
		if path.point(middle).imag < y:
			low = middle
		else:
			high = middle
	distance = path.length(0, (low + high)/2)
	return distance


#============================================
def main(destination: pathlib.Path) -> None:
	"""Keep the source bands and photograph while drawing four smooth sisters."""
	root=svg_tools._xml.read(HERE/'templates'/'karyotype_preparation.svg')
	parent=next(p for p in root.iter() if any(c.get('id')=='image_6' for c in p))
	image=next(c for c in parent if c.get('id')=='image_6')
	overlay=lxml.etree.Element(f'{{{NS}}}g',{'id':'chromosome-schematic-replacement'})
	lxml.etree.SubElement(overlay,f'{{{NS}}}rect',{'x':'40','y':'180','width':'150','height':'255','fill':'white'})
	for i, knots in enumerate(CENTERLINES):
		points = [complex(x, y) for y, x in knots]
		path = svg_tools.chromosome_surface.smooth_centerline(svgpathtools.Path(
			*(svgpathtools.Line(a, b) for a, b in zip(points, points[1:]))))
		ys=[BANDS[0][0]]+[b[1] for b in BANDS]
		distances = [distance_at_y(path, y) for y in ys]
		lengths = [b-a for a, b in zip(distances, distances[1:])]
		model=svg_tools.chromosomes.Chromosome(tuple(svg_tools.chromosomes.Segment('',band[2],length) for band,length in zip(BANDS,lengths)),
			(svg_tools.chromosomes.Centromere(6),))
		part=svg_tools.chromosomes.chromosome_path_part('schematic-sister-'+str(i),model,path.d(),thickness=8,labels=False)
		overlay.append(svg_tools._xml.parse(part.fragment))
	parent.insert(list(parent).index(image)+1,overlay)
	svg_tools.drawing.remove_canvas_background(root)
	lxml.etree.ElementTree(svg_tools.drawing.svg_root(root)).write(destination, encoding='ascii', xml_declaration=False)
