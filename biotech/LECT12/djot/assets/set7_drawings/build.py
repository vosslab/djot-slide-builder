#!/usr/bin/env python3
"""Draw LECT12C evidence diagrams with the repository SVG toolkit.

Slide footers identify the study behind each figure. Counts in selection,
screening, and mobility examples are invented for class. Geometry in the
cell, sequence, fluorescence, and wiring diagrams is schematic.
"""
import math
import pathlib

from svg_tools import annotations, cells, drawing

HERE = pathlib.Path(__file__).parent
INK = '#344651'
BLUE = '#275A88'
PALE = '#C3E0F1'
GOLD = '#FFD47C'
PURPLE = '#694079'
GREEN = '#247257'


def label(x, y, words, size=32, anchor='middle', color=INK):
	return drawing.text(x, y, words, size=size, anchor=anchor, color=color)


def line(x1, y1, x2, y2, width=4, color=INK, dash=''):
	return drawing.line(x1, y1, x2, y2, color=color, width=width, dash=dash)


def arrow(x1, y1, x2, y2):
	return annotations.connector([(x1, y1), (x2, y2)], stroke_width=4, head_size=15).fragment


def dot(x, y, radius, fill, stroke=INK):
	return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'


def bar(x, y, w, h, fill):
	return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'


def write(name, h, title, desc, parts):
	drawing.write_svg(HERE / f'{name}.drawn.svg', 1000, h, title, desc, ''.join(parts))


def hazard():
	# A linear ratio axis includes the no-difference reference and both confidence limits.
	x = lambda ratio: 100 + (ratio - 0.8) * 3200
	items = [line(100, 230, 900, 230), line(x(1), 62, x(1), 225, 3, GREEN, '9 7'),
		label(x(1), 42, 'Equal rates', 29, color=GREEN)]
	for n in range(6):
		pos = 100 + n * 160
		items += [line(pos, 230, pos, 239), label(pos, 277, f'{0.8 + n * 0.05:.2f}', 29)]
	for ratio in [0.85, 1.02]:
		items.append(line(x(ratio), 120, x(ratio), 152, 6, BLUE))
	items += [line(x(.85), 136, x(1.02), 136, 7, BLUE), dot(x(.93), 136, 12, BLUE),
		label(x(.93), 102, '0.93', 34), label(500, 328, 'Adjusted hazard ratio for autism after MMR vaccination')]
	write('mmr_interval', 350, 'MMR cohort estimate', 'Topic 5. The interval 0.85 to 1.02 crosses 1.', items)


def selection():
	items = []
	for stage, (x, states) in enumerate([(155, 'SSSRSSRS'), (500, 'RRS'), (845, 'RRSRRS')]):
		items += [label(x, 46, ['Before exposure', 'Survivors', 'After reproduction'][stage], 29)]
		for i, state in enumerate(states):
			px = x - 82 + 53 * (i % 4)
			py = 114 + 76 * (i // 4)
			cell = cells.cell_envelope(kind='bacterial', width=48, height=34,
				color=GOLD if state == 'R' else PALE).fragment
			items += [f'<g transform="translate({px} {py})">{cell}</g>', label(px, py+7, state, 19)]
		if stage < 2:
			items.append(arrow(x+120, 145, x+220, 145))
	items.append(label(500, 272, 'S = susceptible    /    R = resistant', 28))
	write('bacterial_selection', 295, 'Selection in a mixed population',
		'Topic 6. The resistant fraction rises from two of eight to two of three survivors. Both types then double.', items)


def backbone():
	items = []
	for y, name, base_color, links in [(100, 'DNA', PALE, BLUE), (245, 'XNA', GOLD, PURPLE)]:
		items.append(label(70, y+12, name))
		for i, letter in enumerate('ACTGA'):
			x = 250 + i*155
			if i < 4:
				items.append(line(x, y+28, x+155, y+28, 8, links))
			items += [dot(x, y+28, 14, base_color), line(x, y+10, x, y-12, 4, links),
				label(x, y-24, letter, 40)]
	write('xna_backbones', 305, 'A base sequence on two backbones',
		'Topic 13. Each row encodes ACTGA. The two colored backbones represent different chemistries.', items)


def mtdna():
	items = []
	for x, name, color in [(205, 'Body-cell donor', PALE), (795, 'Egg donor', GOLD)]:
		items += [label(x, 42, name), f'<g transform="translate({x} 155)">'
			+ cells.cell_envelope(kind='animal', width=150, height=155, color=color).fragment + '</g>']
	mitochondrion = cells.organelle(kind='mitochondrion', width=75, height=48, color=GOLD)
	items += [dot(205,155,39,BLUE), label(205,165,'N',28,color='white'),
		f'<g transform="translate(795 155)">{mitochondrion.fragment}</g>',
		arrow(266,207,405,279), arrow(734,207,595,279),
		label(270,284,'Nuclear DNA',26),label(735,284,'Mitochondrial DNA',26),
		label(500,328,'Cloned sheep',36)]
	write('clone_dna', 350, 'Two DNA sources in the cloned sheep',
		'Topic 15. Nuclear markers came from the body cell and mitochondrial markers from the egg.',items)


def decay():
	items = [line(130,260,895,260), line(130,46,130,260)]
	for i, val in enumerate([100,50,25]):
		x = 175+i*330
		height = 1.8*val
		items += [bar(x,260-height,90,height,BLUE),label(x+45,246-height,f'{val}%',31),
			label(x+45,305,['Start','521 years','1,042 years'][i],28)]
	items += [label(510,352,'Fraction of intact 242-base-pair fragments in the model',28)]
	write('fragment_decay', 379, 'Two half-lives in the moa bone model',
		'Topic 16. Applying the reported half-life twice leaves one quarter of the starting fragments.',items)


def lineages():
	items = []
	for panel, name in enumerate(['Chimera','Mosaic']):
		x = 250+500*panel
		items.append(label(x,42,name))
		roots = [(x-85,'A',PALE),(x+85,'B',GOLD)] if panel==0 else [(x,'A',PALE)]
		items.append(f'<rect x="{x-150}" y="191" width="300" height="83" rx="35" '
			'fill="#F3F5F2" stroke="#71828C" stroke-width="2"/>')
		for px,mark,color in roots:
			items += [dot(px,105,27,color), label(px,114,mark,26)]
		for k, (px,mark,color) in enumerate([(x-85,'A',PALE),(x+85,'B',GOLD)]):
			start = px if panel==0 else x
			items += [arrow(start,140,px,184),dot(px,232,32,color),label(px,242,mark,28)]
		items += [label(x,314,['Two starting embryos','One starting embryo'][panel],27)]
	items += [line(500,60,500,270,2,'#A4ACB0'),label(500,370,'Each enclosure represents one individual.',27)]
	write('cell_lineages', 393, 'Two routes to genetically different cell groups',
		'Topic 17. Schematic embryonic chimera has two origins. In the mosaic, B arises within one lineage.',items)


def fluorescence():
	items = [dot(500,134,61,'#D6EBDD'),label(500,145,'GFP',37,color=GREEN),
		label(220,45,'Excitation light'),label(775,45,'Emitted light')]
	for x1,x2,period,color in [(65,415,42,BLUE),(590,935,71,GREEN)]:
		points = ' '.join(f'{x},{134+24*math.sin((x-x1)*math.tau/period):.1f}' for x in range(x1,x2,3))
		items.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="5"/>')
		items.append(arrow(x2-20,206,x2+8,206))
	items += [label(230,258,'Shorter wavelength',27),label(770,258,'Longer wavelength',27)]
	write('fluorescence',285,'A fluorescent protein absorbs and emits light',
		'Topic 19. Wave spacing represents relative wavelengths, with no absolute scale.',items)


def positive_screen():
	items = [label(500,45,'20 positive screens'),label(264,278,'10 condition present',30),
		label(739,278,'10 condition absent',30)]
	for group in range(2):
		for i in range(10):
			x = 115+group*475+(i%5)*74
			y = 107+(i//5)*70
			items += [dot(x,y,24,BLUE if group==0 else 'white'),
				label(x,y+8,'+' if group==0 else '-',26,color='white' if group==0 else INK)]
	write('positive_screens',307,'A closer look at the positive screening results',
		'Topic 22. Each circle is a positive screen. Ten have the condition, ten do not. Hypothetical.',items)


def gestation():
	items = [label(280,74,'Pregnancy in ewe'),label(728,74,'Extra-uterine support'),
		arrow(65,145,930,145),bar(555,129,323,31,BLUE),line(555,104,555,184),
		label(555,233,'Transfer of fetal lamb',30),label(733,114,'Up to 4 weeks',26,color=BLUE),
		label(500,299,'Developmental time (schematic)',27)]
	write('lamb_support',324,'The study began partway through gestation',
		'Topic 25. A fetus developed in a ewe before transfer. Only the later period was studied outside the uterus.',items)


def healthspan():
	items = [label(35,53,'Mobility in an invented mouse cohort',30,'start')]
	for y,group,end in [(120,'Group A',26),(227,'Group B',20)]:
		items += [label(35,y+12,group,29,'start'),bar(223,y-18,22*end,36,BLUE),
			bar(223+22*end,y-18,22*(30-end),36,'#C9CBCD'),
			label(223+22*end,y+58,f'{end} mo.',26)]
	items += [label(220,314,'Birth',26),label(885,314,'30 months',26),
		bar(245,349,29,20,BLUE),label(288,367,'Mobile',25,'start'),
		bar(541,349,29,20,'#C9CBCD'),label(584,367,'Limited mobility',25,'start')]
	write('healthspan',393,'Equal lifespans with different periods of mobility',
		'Topic 32. The two groups live 30 months. Mobility persists to 26 and 20 months in this example.',items)


def wiring():
	items=[]
	for p,title in enumerate(['Wiring map','Activity at one moment']):
		base=500*p
		items.append(label(base+250,44,title,31))
		points=[(base+95,180),(base+235,104),(base+240,245),(base+385,178)]
		for i,j in [(0,1),(0,2),(1,3),(2,3)]:
			items.append(line(*points[i],*points[j],5))
		for i,(x,y) in enumerate(points):
			on = p==1 and i in (0,2)
			items += [dot(x,y,29,GOLD if on else PALE),label(x,y+9,'ABCD'[i],26)]
	items += [label(500,331,'Same connections in both views. Gold marks active neurons in this example.',26)]
	write('connectome',358,'Connectivity and activity answer different questions',
		'Topic 36. Invented four-neuron network. On the right only neurons A and C are active.',items)


def trials():
	items=[]
	for i,(name,num) in enumerate([('Journal articles',94),('FDA records',51)]):
		y=92+i*111
		items += [label(215,y+15,name,30,'end'),bar(251,y-19,6*num,48,BLUE),
			label(267+6*num,y+16,f'{num}%',30,'start')]
	items += [line(251,272,851,272,3)]
	for val in (0,50,100):
		x=251+6*val
		items += [line(x,269,x,282,2),label(x,314,f'{val}%',24)]
	items += [label(545,368,'Share of trials that appeared positive in each record',28)]
	write('publication_bias',392,'The same research program seen through two records',
		'Topic 41. Turner et al. reported 94 percent appearing positive in publication versus 51 percent according to FDA.',items)


def sample_code():
	items = ['<g id="coded-tube"><path d="M132 55 H234 V214 Q183 292 132 214 Z" '
		'fill="#E2EEF4" stroke="#344651" stroke-width="5"/>'
		'<path d="M139 150 H227 V211 Q183 278 139 211 Z" fill="#A64949"/>'
		'<rect x="124" y="35" width="118" height="33" rx="8" fill="#668196"/>'
		'<rect x="134" y="104" width="98" height="53" fill="#FFFFFF"/></g>',
		label(183,142,'A17'), label(183,322,'Research sample'),
		arrow(300,145,475,145), label(383,111,'Look up',28),
		'<rect x="520" y="47" width="410" height="210" rx="10" fill="#F0F5F7" stroke="#344651" stroke-width="3"/>',
		label(725,98,'Hospital file',33), line(550,120,900,120,2),
		label(615,183,'A17'), arrow(682,174,749,174), label(829,183,'Donor'),
		label(725,322,'Who can access the file?')]
	write('coded_sample',350,'A sample code can lead back to a person',
		'Topic 1. The researcher sees tube A17. A hospital holds the separate file linking A17 to a donor.',items)


def fertility():
	items = []
	for y,name,left,right in [(100,'IUI','Sperm placed in uterus','Fertilization in the body'),
		(258,'IVF','Fertilization in the lab','Embryo transfer to uterus')]:
		items += [label(80,y+12,name,40,color=BLUE),label(365,y+12,left,30),
			arrow(548,y,626,y),label(810,y+12,right,29)]
	items += [line(55,179,940,179,2,'#A4ACB0')]
	write('fertilization_site',327,'Where fertilization can occur in IUI and IVF',
		'Topic 21. Sperm placement precedes possible fertilization in IUI. Fertilization precedes possible transfer in IVF.',items)


def main():
	sample_code()
	fertility()
	hazard()
	selection()
	backbone()
	mtdna()
	decay()
	lineages()
	fluorescence()
	positive_screen()
	gestation()
	healthspan()
	wiring()
	trials()


if __name__ == '__main__':
	main()
