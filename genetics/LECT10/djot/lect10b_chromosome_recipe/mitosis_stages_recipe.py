"""Regenerate source mitosis stages from source-positioned chromosome centerlines."""
import json
import pathlib
import re
import subprocess
import svgpathtools
import lxml.etree
import svg_tools._xml
import svg_tools.chromosomes
import svg_tools.chromosome_surface
import svg_tools.drawing

NS='http://www.w3.org/2000/svg'

HERE=pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip()) / 'genetics/LECT10/djot/lect10b_chromosome_recipe'

def main(destination: pathlib.Path) -> None:
	root=svg_tools._xml.read(HERE/'templates'/'mitosis_karyotype_stages.drawn.svg')
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
			thickness=7
		elif name.startswith('prophase'):
			sister=int(name[-1]); sign=-1 if sister==0 else 1
			# Undo the source's eight-unit sister offset in the local centerlines.
			path=f'M {sign*5} {ymin+3} Q {sign*3} {ymin/2} 0 0 Q {-sign*3} {ymax/2} {-sign*5} {ymax-3}'
			thickness=7
		else:
			path=f'M 1 {ymin+3} Q -1 {ymin/2} 0 0 Q 1 {ymax/2} 1 {ymax-3}'
			thickness=7
		curve = svg_tools.chromosome_surface.smooth_centerline(svgpathtools.parse_path(path))
		center = svg_tools.chromosome_surface.nearest_distance(curve, 0j)
		lengths = (center, curve.length()-center)
		model=svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('',color,lengths[0]),svg_tools.chromosomes.Segment('',color,lengths[1])),
			(svg_tools.chromosomes.Centromere(1),))
		part=svg_tools.chromosomes.chromosome_path_part(name+'-v2',model,curve.d(),thickness=thickness,labels=False)
		slot.append(svg_tools._xml.parse(part.fragment))
	svg_tools.drawing.remove_canvas_background(root)
	lxml.etree.ElementTree(svg_tools.drawing.svg_root(root)).write(destination,encoding='utf-8')
