#!/usr/bin/env python3
"""Reconstruct all six source panels using four continuous product chromatids each."""
import copy
import pathlib
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as DET

import svgpathtools
import svg_tools.chromosomes

BASE = pathlib.Path(__file__).resolve().parent
ROOT = BASE
SOURCE = BASE / 'assets/lect09_history_templates/crossover_histories_labels.svg'
BROWN, GOLD = '#865124', '#B77B0A'
NS = '{http://www.w3.org/2000/svg}'
PREFIX = [
	'M0 0 C15 0 25 2 30 10 C40 3 45 -2 55 0',
	'M0 20 C15 20 25 18 30 10 C40 17 45 20 55 24',
	'M0 38 C15 38 25 40 30 48 C40 41 45 38 55 38',
	'M0 58 C15 58 25 56 30 48 C40 55 45 60 55 60',
]
STRAIGHT = [' C85 0 110 0 138 0', ' C85 20 110 20 138 20',
	' C85 38 110 38 138 38', ' C85 60 110 60 138 60']
# Color changes meet at actual exchange points; intermediate projected overlaps are not exchanges.
FIRST_DOWN = ' C60 26 64 28 70 31'
FIRST_UP = ' C60 36 64 34 70 31'
PANELS = [
	dict(id='A', title='(A)  No crossing over', xy=[92,31], title_xy=[63,14],
						ascus=[299,63], outcome=['Parental','ditype (PD)'],
						spores=['AB','AB','ab','ab'], products=['AB','AB','ab','ab'], pairs=[], trajectory_pairs=[],
						paths=[[(STRAIGHT[i], i//2)] for i in range(4)]),
	dict(id='B', title='(B)  Single crossing over', xy=[92,159], title_xy=[63,140],
						ascus=[299,184], outcome=['Tetratype (TT)'],
						spores=['AB','Ab','aB','ab'], products=['AB','Ab','aB','ab'], pairs=[[1,2]], trajectory_pairs=[[1,2]],
						paths=[[(STRAIGHT[0],0)],[(FIRST_DOWN,0),(' C88 39 112 38 138 38',1)],
													[(FIRST_UP,1),(' C88 22 112 20 138 20',0)],[(STRAIGHT[3],1)]]),
	dict(id='C', title='(C)  2-strand double crossing over', xy=[92,274], title_xy=[63,259],
						ascus=[299,299], outcome=['Parental','ditype (PD)'],
						spores=['AB','AB','ab','ab'], products=['AB','AB','ab','ab'], pairs=[[1,2],[1,2]], trajectory_pairs=[[1,2],[1,2]],
						paths=[[(STRAIGHT[0],0)],[(FIRST_DOWN,0),(' C82 47 98 47 114 31',1),(' C123 22 128 20 138 20',0)],
													[(FIRST_UP,1),(' C82 15 98 15 114 31',0),(' C123 39 128 38 138 38',1)],[(STRAIGHT[3],1)]]),
	dict(id='D', title='(D)  3-strand double crossing over', xy=[377,32], title_xy=[346,14],
						ascus=[588,63], outcome=['Tetratype (TT)'],
						spores=['Ab','AB','aB','ab'], products=['Ab','AB','aB','ab'], pairs=[[1,2],[0,2]], trajectory_pairs=[[1,2],[0,1]],
						paths=[[(' C79 -8 91 1 104 19',0),(' C115 34 122 38 138 38',1)],
													[(FIRST_DOWN,0),(' C85 49 99 46 104 19',1),(' C113 7 125 0 138 0',0)],
													[(FIRST_UP,1),(' C89 20 115 20 138 20',0)],[(STRAIGHT[3],1)]]),
	dict(id='E', title='(E)  3-strand double crossing over', xy=[377,160], title_xy=[346,141],
						ascus=[588,185], outcome=['Tetratype (TT)'],
						spores=['AB','Ab','ab','aB'], products=['AB','Ab','ab','aB'], pairs=[[1,2],[1,3]], trajectory_pairs=[[1,2],[2,3]],
						paths=[[(STRAIGHT[0],0)],[(FIRST_DOWN,0),(' C88 39 112 38 138 38',1)],
													[(FIRST_UP,1),(' C85 8 101 8 104 39',0),(' C113 51 125 60 138 60',1)],
													[(' C78 64 94 58 104 39',1),(' C116 25 124 20 138 20',0)]]),
	dict(id='F', title='(F)  4-strand double crossing over', xy=[377,275], title_xy=[346,260],
						ascus=[588,300], outcome=['Nonparental','ditype (NPD)'],
						spores=['Ab','Ab','aB','aB'], products=['Ab','Ab','aB','aB'], pairs=[[1,2],[0,3]], trajectory_pairs=[[1,2],[0,3]],
						paths=[[(' C81 -9 96 0 104 31',0),(' C108 53 120 60 138 60',1)],
													[(FIRST_DOWN,0),(' C88 39 112 38 138 38',1)],
													[(FIRST_UP,1),(' C88 22 112 20 138 20',0)],
													[(' C80 65 98 58 104 31',1),(' C108 9 122 0 138 0',0)]])
]

def node(parent: ET.Element, tag: str, **attrs: str) -> ET.Element:
	return ET.SubElement(parent, tag, {key.replace('_','-'):str(value) for key,value in attrs.items()})

def text(parent: ET.Element, x: float, y: float, label: str, size: float = 11, **attrs: str) -> ET.Element:
	element=node(parent,'text',x=x,y=y,font_size=size,**attrs)
	element.text=label
	return element

def strip_namespace(element: ET.Element) -> ET.Element:
	for child in element.iter():
		child.tag=child.tag.replace(NS,'')
	return element

def build() -> bytes:
	source=DET.parse(SOURCE).getroot()
	root=ET.Element('svg',{'xmlns':NS[1:-1], 'width':source.get('width'), 'height':source.get('height'),
		'viewBox':source.get('viewBox'), 'role':'img','aria-labelledby':'figure-title figure-description'})
	node(root,'title',id='figure-title').text='Six Crossover Histories and Their Tetrad Outcomes'
	node(root,'desc',id='figure-description').text=('Six source panels reconstructed as native vector artwork. Four continuous chromatids per panel, with zero, one, or two exchanges. Brown and gold identify parental regions; allele combinations in each ascus give PD, TT, or NPD.')
	defs=node(root,'defs'); clip=node(defs,'clipPath',id='figure-viewport')
	node(clip,'rect',width=726.23629,height=367.0866)
	scene=node(root,'g',clip_path='url(#figure-viewport)',font_family='Atkinson Hyperlegible Next, sans-serif',fill='#171717')
	node(scene,'rect',width=726.23629,height=367.0866,fill='#FFFFFF')
	expected=[]; records=[]
	for panel in PANELS:
		pid=panel['id']; group=node(scene,'g',id=f'panel-{pid}')
		text(group,*panel['title_xy'],panel['title'],10.6,font_weight='600');expected.append(panel['title'])
		x,y=panel['xy']; geometry=node(group,'g',id=f'{pid}-chromatids',transform=f'translate({x} {y})'+(' scale(1 1.23)' if pid=='A' else ''))
		rec=copy.deepcopy(panel); rec['chromatids']=[]
		rec['exchange_points']=([[70,31]] if panel['pairs'] else [])
		if len(panel['pairs'])==2:rec['exchange_points'].append({'C':[114,31],'D':[104,19],'E':[104,39],'F':[104,31]}[pid])
		for index,tail in enumerate(panel['paths']):
			chunks=[(PREFIX[index],index//2)]+tail
			whole=''; lengths=[]
			for command,color in chunks:
				before=svgpathtools.parse_path(whole).length() if whole else 0
				whole+=command
				lengths.append((svgpathtools.parse_path(whole).length()-before,color))
			# Merge adjacent parental regions while retaining exact arc-length boundaries.
			regions=[]
			for length,color in lengths:
				if regions and regions[-1][1]==color:regions[-1]=(regions[-1][0]+length,color)
				else:regions.append((length,color))
			# Keep arc inversion clear of exact cubic knots by a subpixel numerical epsilon.
			if len(regions)>1:
				regions[0]=(regions[0][0]+1e-7,regions[0][1])
				regions[-1]=(regions[-1][0]-1e-7,regions[-1][1])
			model=svg_tools.chromosomes.Chromosome(tuple(svg_tools.chromosomes.Segment('brown' if color==0 else 'gold',(BROWN,GOLD)[color],length) for length,color in regions))
			part=svg_tools.chromosomes.chromosome_path_part(f'{pid}-chromatid-{index}',model,whole,thickness=9,labels=False)
			element=DET.fromstring(part.fragment)
			element.set('data-role','chromatid');element.set('data-source-index',str(index))
			product=('A' if index<2 else 'a')+('B' if regions[-1][1]==0 else 'b')
			element.set('data-product',product);element.set('data-centerline',whole)
			geometry.append(element)
			rec['chromatids'].append(dict(index=index,centerline=whole,regions=regions,product=product))
		# The unchanged middle track passes behind the second exchange in panel D.
		if pid=='D':
			middle=geometry[2];geometry.remove(middle);geometry.insert(0,middle)
		for i,cy in enumerate((10,48)):
			marker=DET.fromstring(svg_tools.chromosomes.centromere_part(f'{pid}-centromere-{i}',thickness=7).fragment)
			marker.set('transform',f'translate(30 {cy})'); geometry.append(marker)
		labels=node(geometry,'g',id=f'{pid}-alleles',font_family='Georgia, serif',font_style='italic',fill='#FFFFFF')
		for i,ly in enumerate((0,24,38,60)):
			allele='A' if i<2 else 'a';text(labels,55,ly+3.2,allele,10.5,text_anchor='middle');expected.append(allele)
		for ly,allele in zip((0,20,38,60),('B','B','b','b')):
			text(labels,128,ly+3.2,allele,10.5,text_anchor='middle');expected.append(allele)
		ax,ay=panel['ascus'];ascus=node(group,'g',id=f'{pid}-ascus')
		node(ascus,'ellipse',cx=ax,cy=ay,rx=34,ry=28.5,fill='#B5DCD1',stroke='#8F9465',stroke_width=.6)
		for (dx,dy),genotype in zip(((0,-16),(-20,0),(20,0),(0,16)),panel['spores']):
			spore=node(ascus,'g',data_role='spore',data_genotype=genotype)
			node(spore,'ellipse',cx=ax+dx,cy=ay+dy,rx=14,ry=12.3,fill='#F6E492',stroke='#B5A55D',stroke_width=.65)
			text(spore,ax+dx,ay+dy+4,genotype,12,font_family='Georgia, serif',font_style='italic',text_anchor='middle')
			expected.append(genotype)
		for i,line in enumerate(panel['outcome']):
			text(group,ax,ay+40+i*12,line,11,text_anchor='middle');expected.append(line)
		records.append(rec)
	for element in source.iter(NS+'text'):
		scene.append(strip_namespace(copy.deepcopy(element)))
		expected.append(''.join(element.itertext()))
	data=ET.tostring(root,encoding='utf-8',xml_declaration=True)+b'\n'
	return data

def main() -> None:
	data = build()
	output = BASE / 'assets/lect09_tetrad_concepts'
	output.mkdir(exist_ok=True)
	(output / 'crossover_histories.svg').write_bytes(data)


if __name__ == '__main__':
	main()
