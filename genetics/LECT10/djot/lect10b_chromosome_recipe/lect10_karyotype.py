"""Replace only the embedded schematic; retain the empirical image bytes."""
import math
import pathlib
import xml.etree.ElementTree
import svg_tools.chromosomes

NS = 'http://www.w3.org/2000/svg'
XLINK = 'http://www.w3.org/1999/xlink'
xml.etree.ElementTree.register_namespace('', NS)
xml.etree.ElementTree.register_namespace('xlink', XLINK)
HERE = pathlib.Path(__file__).resolve().parent
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

def main(destination: pathlib.Path) -> None:
	root=xml.etree.ElementTree.parse(HERE/'templates'/'karyotype_preparation.svg').getroot()
	parent=next(p for p in root.iter() if any(c.get('id')=='image_6' for c in p))
	image=next(c for c in parent if c.get('id')=='image_6')
	overlay=xml.etree.ElementTree.Element(f'{{{NS}}}g',{'id':'chromosome-schematic-replacement'})
	xml.etree.ElementTree.SubElement(overlay,f'{{{NS}}}rect',{'x':'40','y':'180','width':'150','height':'255','fill':'white'})
	for i, knots in enumerate(CENTERLINES):
		def x_at(y: float) -> float:
			a,b=(knots[:2] if y<=301 else knots[1:])
			return a[1]+(b[1]-a[1])*(y-a[0])/(b[0]-a[0])
		ys=[BANDS[0][0]]+[b[1] for b in BANDS]
		pts=[(x_at(y),y) for y in ys]
		lengths=[math.dist(a,b) for a,b in zip(pts,pts[1:])]
		model=svg_tools.chromosomes.Chromosome(tuple(svg_tools.chromosomes.Segment('',band[2],length) for band,length in zip(BANDS,lengths)),6)
		path='M '+' L '.join(f'{x:.4f} {y}' for x,y in pts)
		part=svg_tools.chromosomes.chromosome_path_part('schematic-sister-'+str(i),model,path,thickness=8,labels=False)
		overlay.append(xml.etree.ElementTree.fromstring(part.fragment))
	parent.insert(list(parent).index(image)+1,overlay)
	xml.etree.ElementTree.ElementTree(root).write(destination,encoding='unicode')
