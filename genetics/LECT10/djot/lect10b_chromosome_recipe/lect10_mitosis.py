"""Regenerate source mitosis stages from source-positioned chromosome centerlines."""
import json
import pathlib
import re
import xml.etree.ElementTree
import svg_tools.chromosomes

NS='http://www.w3.org/2000/svg'
xml.etree.ElementTree.register_namespace('',NS)
HERE=pathlib.Path(__file__).resolve().parent

def main(destination: pathlib.Path) -> None:
	root=xml.etree.ElementTree.parse(HERE/'templates'/'mitosis_karyotype_stages.drawn.svg').getroot()
	slots={n.get('id'):n for n in root.iter()}
	records=json.loads((HERE/'mitosis_models.json').read_text())
	for record in records:
		name=record['id']; xmin,xmax,ymin,ymax=record['bounds']
		color={'url(#pink)':'#edb3e6','url(#green)':'#83b599'}[record['fill']]
		slot=slots[name]
		transform=record['transform']
		if name.startswith('prophase'):
			match=re.fullmatch(r'translate\(([-0-9.]+) ([-0-9.]+)\) rotate\(([-0-9.]+)\)',transform)
			x,y,angle=map(float,match.groups())
			x += 4 if name.endswith('sister0') else -4
			transform=f'translate({x} {y}) rotate({angle})'
		slot.set('transform',transform)
		if name.startswith('anaphase'):
			# V-shaped single chromatid, with the source centromere leading at (0,0).
			end=ymax-4
			path=f'M -8 {end} Q -5 8 0 0 Q 5 8 8 {end}'
			lengths=(1,1); thickness=7
		elif name.startswith('prophase'):
			sister=int(name[-1]); sign=-1 if sister==0 else 1
			# Undo the source's eight-unit sister offset in the local centerlines.
			path=f'M {sign*5} {ymin+3} Q {sign*3} {ymin/2} 0 0 Q {-sign*3} {ymax/2} {-sign*5} {ymax-3}'
			lengths=(-ymin,ymax); thickness=7
		else:
			path=f'M 1 {ymin+3} Q -1 {ymin/2} 0 0 Q 1 {ymax/2} 1 {ymax-3}'
			lengths=(-ymin,ymax); thickness=7
		model=svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('',color,lengths[0]),svg_tools.chromosomes.Segment('',color,lengths[1])),
			(svg_tools.chromosomes.Centromere(1),))
		part=svg_tools.chromosomes.chromosome_path_part(name+'-v2',model,path,thickness=thickness,labels=False)
		slot.append(xml.etree.ElementTree.fromstring(part.fragment))
	xml.etree.ElementTree.ElementTree(root).write(destination,encoding='unicode')
