#!/usr/bin/env python3
"""Draw the shared human chromosome 2 fusion sequence for LECT02C and LECT10B.

The original schematic source is LECT02C image_004.jpg (1125x613). Source band
runs below record its color order and relative display intervals, not measured
cytobands. Two ancestral rods become one dicentric chromosome; an intermediate
then marks the long-arm centromere inactive before the final chromosome 2.
"""
import pathlib
import dataclasses
import svg_tools.chromosomes as chromosomes
import svg_tools.drawing as drawing

PURPLE = '#867196'
GOLD = '#E6CF91'
INK = '#344651'
RUNS = [[[114, 123, 'gold'], [123, 127, 'purple'], [127, 133, 'gold'], [133, 148, 'purple'],
  [148, 156, 'gold'], [156, 169, 'purple'], [169, 177, 'gold'], [177, 196, 'purple'],
  [196, 203, 'gold'], [203, 211, 'purple'], [211, 223, 'gold'], [223, 236, 'purple'],
  [236, 246, 'gold'], [246, 274, 'marker'], [274, 285, 'gold']],
 [[270, 282, 'gold'], [282, 309, 'marker'], [309, 320, 'gold'], [320, 337, 'purple'],
  [337, 342, 'gold'], [342, 353, 'purple'], [353, 355, 'gold'], [355, 367, 'purple'],
  [367, 371, 'gold'], [371, 377, 'purple'], [377, 382, 'gold'], [382, 404, 'purple'],
  [404, 408, 'gold'], [408, 421, 'purple'], [421, 424, 'gold'], [424, 435, 'purple'],
  [435, 449, 'gold'], [449, 465, 'purple'], [465, 469, 'gold'], [469, 480, 'purple'],
  [480, 483, 'gold'], [483, 497, 'purple'], [497, 503, 'gold'], [503, 516, 'purple'],
  [516, 519, 'gold'], [519, 523, 'purple'], [523, 533, 'gold']]]


def model(runs: list, sites: tuple[float, ...]) -> chromosomes.Chromosome:
	"""Keep the supplied band intervals and centromere positions as material."""
	positions = sorted({runs[-1][1], *sites, *[a for a, b, color in runs]})
	segments = []
	for a,b in zip(positions,positions[1:]):
		kind = next(color for lo,hi,color in runs if lo <= (a+b)/2 < hi)
		segments.append(chromosomes.Segment('',PURPLE if kind=='purple' else GOLD,b-a))
	return chromosomes.Chromosome(tuple(segments),
		tuple(chromosomes.Centromere(positions.index(site)) for site in sites))


def rod(name: str, x: float, top: float, material: chromosomes.Chromosome) -> str:
	"""Place a chromosome without rescaling its material length."""
	bottom = top + sum(segment.length for segment in material.segments)
	part = chromosomes.chromosome_path_part(name,material,f'M {x} {top} V {bottom}',
		thickness=27,labels=False,bands=False)
	return part.fragment



def text(x: float, y: float, lines: list[str], size: float = 24, anchor: str = 'start') -> str:
	return ''.join(drawing.text(x,y+index*size*1.08,line,size=size,color=INK,anchor=anchor)
		for index,line in enumerate(lines))


def box(x: float, y: float, w: float, h: float, lines: list[str], size: float = 24) -> str:
	return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#DFE7F3" stroke="#638DB6"/>'+text(x+12,y+size+9,lines,size)


def main(path: pathlib.Path) -> None:
	body='<rect width="1125" height="613" fill="white"/>'
	body+='<defs><marker id="process-head" markerUnits="userSpaceOnUse" markerWidth="17" markerHeight="13" refX="16" refY="6.5" orient="auto"><path d="M1 1L16 6.5L1 12" fill="none" stroke="#344651" stroke-width="2"/></marker></defs>'
	body+=rod('ancestor-top',242,114,model(RUNS[0],(260,)))
	body+=rod('ancestor-bottom',291,270,model(RUNS[1],(295,)))
	# Concatenate the ancestral material; internal telomeres become part of one body.
	fused_runs = [(a-15,b-15,color) for a,b,color in RUNS[0]] + RUNS[1]
	fused = model(fused_runs,(245,295))
	body+='<g id="dicentric" data-chromosomes="1" data-centromeres="2">'
	body+=rod('dicentric-body',574,99,fused)+'</g>'
	# Inactivation changes function, not the original long-arm chromatid material.
	body+='<g id="inactivation-intermediate" data-chromosomes="1" data-centromeres="1" data-inactive-centromeres="1">'
	inactive = dataclasses.replace(fused,centromeres=(fused.centromeres[0],
		dataclasses.replace(fused.centromeres[1],active=False)))
	body+=rod('inactivation-body',844,99,inactive)
	body+='</g>'
	human = dataclasses.replace(fused,centromeres=fused.centromeres[:1])
	body+=rod('human-chromosome-2',978,99,human)
	for a,b in ((323,548),(614,809),(861,949)):
		body+=f'<path d="M {a} 278 H {b}" fill="none" stroke="{INK}" stroke-width="3" marker-end="url(#process-head)"/>'
	body+='<path d="M 224 250 L173 330 L268 324" fill="none" stroke="#344651" stroke-width="2.5"/>'
	body+=text(15,330,['Acrocentric','chromosomes','in an ancestor of','the human species'],24)
	body+=text(337,321,['Fusion of','telomeres','of short arms'],24)
	body+=text(627,309,['Centromere','inactivation'],24)
	body+=text(574,559,['Dicentric','chromosome'],25,'middle')
	body+=text(978,559,['Human','chromosome 2'],25,'middle')
	body+=box(285,24,211,195,['A chromosome','with two','functional','centromeres','cannot persist','for very long.'],24)
	body+='<path d="M 496 136 L552 245" fill="none" stroke="#287A9F" stroke-width="2.5"/><circle cx="552" cy="245" r="4" fill="#287A9F"/>'
	body+=box(615,357,195,159,['The','centromere in','the long arm','became','inactivated.'],24)
	body+='<path d="M 800 357 L822 294" fill="none" stroke="#287A9F" stroke-width="2.5"/><circle cx="822" cy="294" r="4" fill="#287A9F"/>'
	body+=box(678,23,418,74,['No obvious indication of the','inactivated centromere remains.'],24)
	body+='<path d="M 881 97 L960 295" fill="none" stroke="#287A9F" stroke-width="2.5"/><circle cx="960" cy="295" r="4" fill="#287A9F"/>'
	body+='<path d="M 1000 100 Q1010 102 1010 115 V154 Q1010 166 1018 172 Q1010 178 1010 190 V215 Q1010 229 1000 230 M1000 260 Q1010 263 1010 277 V376 Q1010 391 1018 394 Q1010 397 1010 413 V513 Q1010 530 1000 533" fill="none" stroke="#344651" stroke-width="2"/>'
	body+=text(1032,166,['Short','arm'],25)+text(1032,386,['Long','arm'],25)
	drawing.write_svg(path,1125,613,'Chromosome 2 fusion schematic',
		'Two ancestral acrocentric chromosomes fuse at their short-arm telomeres. Their banded material is concatenated into one continuous dicentric body with only two outer telomere caps. All three fused stages retain the same material, length and band positions. The lower centromere becomes inactive, shown by a dashed rectangular collar; the final stage replaces that collar with continuing chromosome material. Solid rectangular collars mark active centromeres. Band lengths are illustration coordinates, not a measured cytogenetic map.',body)


if __name__=='__main__':
	import sys
	main(pathlib.Path(sys.argv[1]))
