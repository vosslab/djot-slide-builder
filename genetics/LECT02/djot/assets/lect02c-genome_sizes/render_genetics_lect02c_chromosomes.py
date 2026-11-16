#!/usr/bin/env python3
"""Rebuild the five source chromosome bodies and all source callouts.

The original schematic source is LECT02C image_004.jpg (1125x613). Source band
runs below record its color order and relative display intervals, not measured
cytobands. Two ancestral rods become one dicentric chromosome; an intermediate
then marks the long-arm centromere inactive before the final chromosome2.
"""
import pathlib
import xml.etree.ElementTree as ET
import svg_tools.chromosomes as chromosomes
import svg_tools.drawing as drawing

PURPLE = '#867196'
GOLD = '#E6CF91'
INK = '#344651'
RUNS = [[[114, 123, 'gold'], [123, 127, 'purple'], [127, 133, 'gold'], [133, 148, 'purple'], [148, 156, 'gold'], [156, 169, 'purple'], [169, 177, 'gold'], [177, 196, 'purple'], [196, 203, 'gold'], [203, 211, 'purple'], [211, 223, 'gold'], [223, 236, 'purple'], [236, 246, 'gold'], [246, 274, 'marker'], [274, 285, 'gold']], [[270, 282, 'gold'], [282, 309, 'marker'], [309, 320, 'gold'], [320, 337, 'purple'], [337, 342, 'gold'], [342, 353, 'purple'], [353, 355, 'gold'], [355, 367, 'purple'], [367, 371, 'gold'], [371, 377, 'purple'], [377, 382, 'gold'], [382, 404, 'purple'], [404, 408, 'gold'], [408, 421, 'purple'], [421, 424, 'gold'], [424, 435, 'purple'], [435, 449, 'gold'], [449, 465, 'purple'], [465, 469, 'gold'], [469, 480, 'purple'], [480, 483, 'gold'], [483, 497, 'purple'], [497, 503, 'gold'], [503, 516, 'purple'], [516, 519, 'gold'], [519, 523, 'purple'], [523, 533, 'gold']], [[132, 140, 'gold'], [140, 145, 'purple'], [145, 150, 'gold'], [150, 166, 'purple'], [166, 173, 'gold'], [173, 187, 'purple'], [187, 195, 'gold'], [195, 214, 'purple'], [214, 221, 'gold'], [221, 229, 'purple'], [229, 240, 'gold'], [240, 254, 'purple'], [254, 264, 'gold'], [264, 292, 'marker'], [292, 302, 'gold'], [302, 320, 'purple'], [320, 324, 'gold'], [324, 336, 'purple'], [336, 337, 'gold'], [337, 349, 'purple'], [349, 354, 'gold'], [354, 359, 'purple'], [359, 365, 'gold'], [365, 387, 'purple'], [387, 391, 'gold'], [391, 403, 'purple'], [403, 406, 'gold'], [406, 417, 'purple'], [417, 431, 'gold'], [431, 448, 'purple'], [448, 452, 'gold'], [452, 462, 'purple'], [462, 465, 'gold'], [465, 479, 'purple'], [479, 485, 'gold'], [485, 498, 'purple'], [498, 501, 'gold'], [501, 506, 'purple'], [506, 514, 'gold']]]


def rod(name: str, x: float, top: float, bottom: float, centromere: float, runs: list) -> str:
	start, end = top+13.5, bottom-13.5
	positions = sorted({start,end,centromere,*[float(a) for a,b,color in runs if start<a<end]})
	segments = []
	for a,b in zip(positions,positions[1:]):
		kind = next(color for lo,hi,color in runs if lo <= (a+b)/2 < hi)
		segments.append(chromosomes.Segment('',PURPLE if kind=='purple' else GOLD,b-a))
	model = chromosomes.Chromosome(tuple(segments),positions.index(centromere))
	part = chromosomes.chromosome_path_part(name,model,f'M {x} {start} V {end}',thickness=27,labels=False)
	group = ET.fromstring(part.fragment)
	paint = next(e for e in group if e.get('clip-path'))
	for a,b,kind in runs:
		ET.SubElement(paint,'rect',{'x':str(x-13.5),'y':str(a),'width':'27','height':str(b-a),'fill':PURPLE if kind=='purple' else GOLD})
	return ET.tostring(group,encoding='unicode')


def text(x: float, y: float, lines: list[str], size: float = 24, anchor: str = 'start') -> str:
	return ''.join(drawing.text(x,y+index*size*1.08,line,size=size,color=INK,anchor=anchor)
		for index,line in enumerate(lines))


def box(x: float, y: float, w: float, h: float, lines: list[str], size: float = 24) -> str:
	return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#DFE7F3" stroke="#638DB6"/>'+text(x+12,y+size+9,lines,size)


def main(path: pathlib.Path) -> None:
	body='<rect width="1125" height="613" fill="white"/>'
	body+='<defs><marker id="process-head" markerUnits="userSpaceOnUse" markerWidth="17" markerHeight="13" refX="16" refY="6.5" orient="auto"><path d="M1 1L16 6.5L1 12" fill="none" stroke="#344651" stroke-width="2"/></marker></defs>'
	body+=rod('ancestor-top',242,114,285,260,RUNS[0])
	body+=rod('ancestor-bottom',291,270,533,295,RUNS[1])
	body+='<g id="dicentric" data-chromosomes="1" data-centromeres="2">'
	body+=rod('dicentric-upper-source',574,114,285,260,RUNS[0])
	body+=rod('dicentric-lower-source',574,270,533,295,RUNS[1])+'</g>'
	# Inactivation changes function, not the original long-arm chromatid material.
	body+='<g id="inactivation-intermediate" data-chromosomes="1" data-centromeres="1" data-inactive-centromeres="1">'
	fused=[]
	for runs in RUNS[:2]:
		for a,b,color in runs:
			if color=='marker':color='gold'
			fused.append((a,b,color))
	# Upper source takes precedence in its short overlap, both regions are gold there.
	fused=sorted(fused)
	body+=rod('inactivation-body',844,114,533,260,fused)
	body+='<ellipse cx="844" cy="295" rx="13.5" ry="13.5" fill="white" stroke="#72508C" stroke-width="1.2" stroke-dasharray="3 2"/>'
	body+='</g>'
	body+=rod('human-chromosome-2',978,132,514,278,RUNS[2])
	for a,b in ((323,548),(614,809),(861,949)):
		body+=f'<path d="M {a} 278 H {b}" fill="none" stroke="{INK}" stroke-width="3" marker-end="url(#process-head)"/>'
	body+='<path d="M 224 250 L173 330 L268 324" fill="none" stroke="#344651" stroke-width="2.5"/>'
	body+=text(15,330,['Acrocentric','chromosomes','in an ancestor of','the human species'],24)
	body+=text(337,321,['Fusion of','telomeres','of short arms'],24)
	body+=text(627,309,['Centromere','inactivation'],24)
	body+=text(574,559,['Dicentric','chromosome'],25,'middle')
	body+=text(978,559,['Human','chromosome 2'],25,'middle')
	body+=box(285,24,211,195,['A chromosome','with two','functional','centromeres','cannot persist','for very long.'],24)
	body+='<path d="M 496 136 L552 272" fill="none" stroke="#287A9F" stroke-width="2.5"/><circle cx="552" cy="272" r="4" fill="#287A9F"/>'
	body+=box(615,357,195,159,['The','centromere in','the long arm','became','inactivated.'],24)
	body+='<path d="M 800 357 L822 294" fill="none" stroke="#287A9F" stroke-width="2.5"/><circle cx="822" cy="294" r="4" fill="#287A9F"/>'
	body+=box(678,23,418,74,['No obvious indication of the','inactivated centromere remains.'],24)
	body+='<path d="M 881 97 L955 269" fill="none" stroke="#287A9F" stroke-width="2.5"/><circle cx="955" cy="269" r="4" fill="#287A9F"/>'
	body+='<path d="M 1000 134 Q1010 136 1010 149 V181 Q1010 193 1018 199 Q1010 205 1010 217 V248 Q1010 262 1000 263 M1000 294 Q1010 297 1010 311 V384 Q1010 399 1018 402 Q1010 405 1010 421 V493 Q1010 510 1000 513" fill="none" stroke="#344651" stroke-width="2"/>'
	body+=text(1032,193,['Short','arm'],25)+text(1032,394,['Long','arm'],25)
	drawing.write_svg(path,1125,613,'Chromosome 2 fusion schematic',
		'Two acrocentric source chromosomes fuse at their short-arm telomeres. The dicentric and centromere-inactivation intermediates each retain one continuous chromosome body; the lower centromere becomes inactive. The final human chromosome 2 retains its functional centromere, short arm and long arm. Source schematic band order, source centromere positions, five source chromosome objects, and all original callout wording retained. Band lengths are illustration coordinates, not a measured cytogenetic map. Hollow purple active markers and a dashed inactive-site ring are diagram conventions.',body)


if __name__=='__main__':
	import sys
	main(pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).with_name('chromosome_2_fusion.drawn.svg'))
