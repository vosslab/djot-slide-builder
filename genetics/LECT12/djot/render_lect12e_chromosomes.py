#!/usr/bin/env python3
"""Rebuild LECT12E chromosome schematics with the shared v2 chromosome family.

Run from the repository root with PYTHONPATH="$PWD" python3 this_file.py.
Crossover source centerlines, all repeat blocks, labels, overlap order and
reciprocal ancestry tails are retained from the original instructor schematic.
Unmeasured chromosome lengths; molecular gene tracks and empirical assets stay separate.
"""

import pathlib
import string

import svgpathtools
import svg_tools.chromosomes
import svg_tools.drawing

ASSETS = pathlib.Path(__file__).parent / 'assets/lect12e-chromo_alter_2-duplications'

CROSSOVER_PATHS = [('M32 130 C85 130 84 165 108 165 S150 130 185 130 L295 130', '#287caf', 108),
	('M32 200 C85 200 84 165 108 165 S150 200 185 200 L295 200', '#287caf', 108),
	('M32 285 C85 285 84 320 108 320 S150 285 185 285 L295 285', '#6076b2', 108),
	('M32 355 C85 355 84 320 108 320 S150 355 185 355 L295 355', '#6076b2', 108),
	('M442 130 C495 130 494 165 518 165 S560 130 595 130 L705 130', '#287caf', 518),
	('M442 200 C495 200 494 165 518 165 S560 200 595 200 L705 200', '#287caf', 518),
	('M404 285 C457 285 456 320 480 320 S522 285 557 285 L667 285', '#6076b2', 480),
	('M404 355 C457 355 456 320 480 320 S522 355 557 355 L667 355', '#6076b2', 480),
	('M817 130 C858 130 858 165 884 165 S928 130 963 130 L1100 130', '#287caf', 884),
	('M817 355 C858 355 858 320 884 320 S928 355 963 355 L1100 355', '#6076b2', 884),
	('M817 200 C858 200 858 165 884 165 C930 165 948 213 976 213 C1005 213 1010 285 1040 285 L1100 '
		'285',
		'#287caf',
		884),
	('M975 213 C1005 213 1010 285 1040 285', '#ae702c', None),
	('M817 285 C858 285 858 320 884 320 C929 320 939 282 962 282 C996 282 1005 213 1030 213 L1100 213',
		'#6076b2',
		884),
	('M942 298 C951 286 955 282 962 282 C996 282 1005 213 1030 213 L1055 213', '#ae702c', None),
	('M1058 285 L1100 285', '#6076b2', None),
	('M1068 213 L1100 213', '#287caf', None),
	('M1245 100 Q1280 97 1315 100 L1481 100', '#287caf', 1300),
	('M1245 190 Q1280 187 1315 190 L1443 190', '#287caf', 1300),
	('M1413 190 L1443 190', '#6076b2', None),
	('M1245 280 Q1280 277 1315 280 L1519 280', '#6076b2', 1300),
	('M1489 280 L1519 280', '#287caf', None),
	('M1245 370 Q1280 367 1315 370 L1481 370', '#6076b2', 1300)]

CROSSOVER_TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="460" viewBox="0 0 1600 460" role="img" aria-labelledby="title description">
<title id="title">Unequal crossing over expands or contracts a tandem duplication</title>
<desc id="description">Four chromatids pass through normal pairing, mispairing and an exchange between nonsister chromatids. Products retain two, one, three and two repeat copies in source order. Hollow purple markers identify the source centromeres. Shared v2 bodies retain the original source centerlines and repeat overlays. L and R identify the left and right copies. The two inner chromatids exchange within misaligned repeats; white interruptions distinguish overlap from fusion.</desc>
<metadata id="provenance">Original editable schematic constructed from instructor asset genetics/LECT11/djot/assets/lect11e-chromo_alter_2-duplications/image_002.png; source meaning and labels retained, geometry recomposed. Unmeasured chromosome lengths. 2026-11-09. Shared v2 chromosome-body migration 2026-11-15.</metadata>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M1 1 L9 5 L1 9" fill="none" stroke="#213547" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>
<rect width="1600" height="460" fill="white"/>
<g font-family="Atkinson Hyperlegible Next">
<text x="22" y="38" font-size="25" text-anchor="start" fill="#213547" font-weight="bold" >(A)		Normal pairing</text>
<text x="410" y="38" font-size="25" text-anchor="start" fill="#213547" font-weight="bold" >(B)		Mispairing</text>
<text x="800" y="38" font-size="25" text-anchor="start" fill="#213547" font-weight="bold" >(C)		Unequal crossing over</text>
<text x="1230" y="38" font-size="25" text-anchor="start" fill="#213547" font-weight="bold" >(D)		Result of crossover</text>
<g id="normal-pairing">
<path d="M32 130 C85 130 84 165 108 165 S150 130 185 130 L295 130" fill="none" stroke="white" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>$chromatid_0<rect x="187" y="117" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/><rect x="225" y="117" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/><path d="M32 200 C85 200 84 165 108 165 S150 200 185 200 L295 200" fill="none" stroke="white" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>$chromatid_1<rect x="187" y="187" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/><rect x="225" y="187" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/>
<path d="M32 285 C85 285 84 320 108 320 S150 285 185 285 L295 285" fill="none" stroke="white" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>$chromatid_2<rect x="187" y="272" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/><rect x="225" y="272" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/><path d="M32 355 C85 355 84 320 108 320 S150 355 185 355 L295 355" fill="none" stroke="white" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>$chromatid_3<rect x="187" y="342" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/><rect x="225" y="342" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/>
<text x="180" y="430" font-size="25" text-anchor="middle" fill="#213547" font-weight="normal" >Tandem duplication</text>
<path d="M165 402 L205 365 M165 402 L245 365" fill="none" stroke="#526879" stroke-width="2"/>
</g>
<g id="mispaired-four-chromatids">
<path d="M442 130 C495 130 494 165 518 165 S560 130 595 130 L705 130" fill="none" stroke="white" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>$chromatid_4<rect x="597" y="117" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/><text x="615.5" y="138" font-size="24" text-anchor="middle" fill="white" font-weight="normal" font-style="italic">L</text><rect x="635" y="117" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/><text x="653.5" y="138" font-size="24" text-anchor="middle" fill="white" font-weight="normal" font-style="italic">R</text><path d="M442 200 C495 200 494 165 518 165 S560 200 595 200 L705 200" fill="none" stroke="white" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>$chromatid_5<rect x="597" y="187" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/><text x="615.5" y="208" font-size="24" text-anchor="middle" fill="white" font-weight="normal" font-style="italic">L</text><rect x="635" y="187" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/><text x="653.5" y="208" font-size="24" text-anchor="middle" fill="white" font-weight="normal" font-style="italic">R</text>
<path d="M404 285 C457 285 456 320 480 320 S522 285 557 285 L667 285" fill="none" stroke="white" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>$chromatid_6<rect x="559" y="272" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/><text x="577.5" y="293" font-size="24" text-anchor="middle" fill="white" font-weight="normal" font-style="italic">L</text><rect x="597" y="272" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/><text x="615.5" y="293" font-size="24" text-anchor="middle" fill="white" font-weight="normal" font-style="italic">R</text><path d="M404 355 C457 355 456 320 480 320 S522 355 557 355 L667 355" fill="none" stroke="white" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>$chromatid_7<rect x="559" y="342" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/><text x="577.5" y="363" font-size="24" text-anchor="middle" fill="white" font-weight="normal" font-style="italic">L</text><rect x="597" y="342" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/><text x="615.5" y="363" font-size="24" text-anchor="middle" fill="white" font-weight="normal" font-style="italic">R</text>
</g>
<path d="M742 245 L790 245" fill="none" stroke="#213547" stroke-width="2.8" marker-end="url(#arrow)"/>
<g id="unequal-nonsister-exchange">
<path d="M817 130 C858 130 858 165 884 165 S928 130 963 130 L1100 130" fill="none" stroke="white" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>$chromatid_8
<path d="M817 355 C858 355 858 320 884 320 S928 355 963 355 L1100 355" fill="none" stroke="white" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>$chromatid_9
<rect x="980" y="117" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/>
<rect x="1018" y="117" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/>
<rect x="942" y="342" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/>
<rect x="980" y="342" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/>
<path d="M817 200 C858 200 858 165 884 165 C930 165 948 213 976 213 C1005 213 1010 285 1040 285 L1100 285" fill="none" stroke="white" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>$chromatid_10
$chromatid_11
<path d="M817 285 C858 285 858 320 884 320 C929 320 939 282 962 282 C996 282 1005 213 1030 213 L1100 213" fill="none" stroke="white" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>$chromatid_12
$chromatid_13
$chromatid_14
$chromatid_15
<path d="M978 266 L999 277 M1020 201 L1029 225" fill="none" stroke="#f5dcb9" stroke-width="1.5"/>


</g>
<path d="M1150 245 L1210 245" fill="none" stroke="#213547" stroke-width="2.8" marker-end="url(#arrow)"/>
<g id="four-products">
<g id="product-1-2-copies">
<path d="M1245 100 Q1280 97 1315 100 L1481 100" fill="none" stroke="white" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>$chromatid_16

<rect x="1375" y="87" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/>
<rect x="1413" y="87" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/>
<text x="1388" y="143" font-size="25" text-anchor="middle" fill="#213547" font-weight="normal" >Duplication</text>
</g>
<g id="product-2-1-copies">
<path d="M1245 190 Q1280 187 1315 190 L1443 190" fill="none" stroke="white" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>$chromatid_17

$chromatid_18
<rect x="1375" y="177" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/>
<text x="1388" y="233" font-size="25" text-anchor="middle" fill="#213547" font-weight="normal" >Single copy</text>
</g>
<g id="product-3-3-copies">
<path d="M1245 280 Q1280 277 1315 280 L1519 280" fill="none" stroke="white" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>$chromatid_19

$chromatid_20
<rect x="1375" y="267" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/>
<rect x="1413" y="267" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/>
<rect x="1451" y="267" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/>
<text x="1388" y="323" font-size="25" text-anchor="middle" fill="#213547" font-weight="normal" >Triplication</text>
</g>
<g id="product-4-2-copies">
<path d="M1245 370 Q1280 367 1315 370 L1481 370" fill="none" stroke="white" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>$chromatid_21

<rect x="1375" y="357" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/>
<rect x="1413" y="357" width="37" height="26" rx="3" fill="#ae702c" stroke="#344651" stroke-width="0.9"/>
<text x="1388" y="413" font-size="25" text-anchor="middle" fill="#213547" font-weight="normal" >Duplication</text>
</g>
</g>
</g></svg>'''


#============================================
def crossover() -> None:
	"""Replace chromosome bodies while preserving every source arrangement."""
	replacements = {}
	for index, (path_d, color, centromere_x) in enumerate(CROSSOVER_PATHS):
		curve = svgpathtools.parse_path(path_d)
		length = curve.length()
		regions = (svg_tools.chromosomes.Segment('', color, length),)
		centromere_after = None
		if centromere_x is not None:
			# Source centerlines run left-to-right; retain their original joint x.
			lower, upper = 0., 1.
			for unused in range(48):
				middle = (lower+upper)/2
				if curve.point(middle).real < centromere_x:
					lower = middle
				else:
					upper = middle
			first_length = curve.cropped(0, (lower+upper)/2).length()
			regions = (svg_tools.chromosomes.Segment('', color, first_length),
				svg_tools.chromosomes.Segment('', color, length-first_length))
			centromere_after = 1
		centromeres = () if centromere_after is None else (svg_tools.chromosomes.Centromere(centromere_after),)
		model = svg_tools.chromosomes.Chromosome(regions, centromeres=centromeres)
		part = svg_tools.chromosomes.chromosome_path_part(f'crossover-{index}', model,
			path_d, thickness=25, labels=False)
		replacements[f'chromatid_{index}'] = part.fragment
	result = string.Template(CROSSOVER_TEMPLATE).substitute(replacements)
	(ASSETS / 'unequal_tandem_crossover.drawn.svg').write_text(result)


#============================================
def overview() -> None:
	"""Retain ABCDE|FGH to ABCBCDE|FGH, BC emphasis, and source cut arrows."""
	body = ''
	for stage, sequence, y, joins, cuts in (
		('Before', 'ABCDE|FGH', 60, (), (1, 3)),
		('After', 'ABCBCDE|FGH', 220, (3, 5), ())):
		body += svg_tools.drawing.text(48, y+43, stage, size=32,
			color='#344651', anchor='start', font='Atkinson Hyperlegible Next')
		regions = tuple(svg_tools.chromosomes.Segment(label,
			'#B48CDE' if label in 'BC' else '#D9C9EF', 64)
			for label in sequence.replace('|', ''))
		model = svg_tools.chromosomes.Chromosome(regions,
			centromeres=(svg_tools.chromosomes.Centromere(sequence.index('|')),))
		layout = svg_tools.chromosomes.render_chromosome_layout('duplication-'+stage.lower(),
			model, thickness=62, junctions=joins)
		body += f'<g transform="translate(218 {y})">{layout.svg}'
		for cut in cuts:
			x = layout.boundaries[cut][0]
			body += f'<path d="M {x} -32 V -12" stroke="#BD2929" stroke-width="4"/>'
			body += f'<path d="M {x-7} -15 L {x} -3 L {x+7} -15 Z" fill="#BD2929"/>'
		body += '</g>'
	svg_tools.drawing.write_svg(ASSETS / 'duplication_overview.drawn.svg', 980, 340,
		'Duplication', 'Source image001: ABCDE, centromere, FGH becomes ABCBCDE, '
		'centromere, FGH. BC remains emphasized; source red cuts at A/B and C/D. '
		'Hollow purple centromere markers and white joins are distinct. '
		'Single chromatids; gene spacing and decorative bands are schematic.', body)


#============================================
def copy_number() -> None:
	"""Retain source image020 neck, interval position and length increase."""
	body = ''
	for stage, sequence, x in (('Before duplication', 'ABCDE', 160),
		('After duplication', 'ABCCDE', 610)):
		body += svg_tools.drawing.text(x-80, 40, stage, size=27,
			color='#344651', anchor='start', font='Atkinson Hyperlegible Next')
		# Source y: body 11..549, neck 150, interval 182..323; added copy 141 px.
		# Half-scale source distances; letters remain an unmeasured teaching abstraction.
		regions = [svg_tools.chromosomes.Segment('A', '#E2E2E2', 20.25),
			svg_tools.chromosomes.Segment('', '#E2E2E2', 26.75),
			svg_tools.chromosomes.Segment('', '#E2E2E2', 16)]
		regions.extend(svg_tools.chromosomes.Segment(letter,
			'#D6C9F0' if letter == 'C' else '#E2E2E2', 70.5 if letter == 'C' else 56.5)
			for letter in sequence[2:])
		regions[-1] = svg_tools.chromosomes.Segment('E', '#E2E2E2', 34)
		model = svg_tools.chromosomes.Chromosome(tuple(regions),
			centromeres=(svg_tools.chromosomes.Centromere(2),))
		length = sum(region.length for region in regions)
		part = svg_tools.chromosomes.chromosome_path_part('cnv-'+sequence, model,
			f'M45 22.5 V{22.5+length}', thickness=45)
		body += f'<g transform="translate({x} 75)">{part.fragment}</g>'
		body += svg_tools.drawing.text(x+3, 75+62, 'B', size=25,
			color='#344651', anchor='end', font='Atkinson Hyperlegible Next')
	body += '<path d="M275 215 L575 215" stroke="#007A00" stroke-width="3" fill="none"/>'
	body += svg_tools.drawing.text(300, 195, 'Copied interval', size=22,
		color='#344651', anchor='start', font='Atkinson Hyperlegible Next')
	svg_tools.drawing.write_svg(ASSETS / 'copy_number_interval.drawn.svg', 900, 460,
		'Copy number interval', 'Source image020: duplicated chromosome interval C; '
		'ABCDE becomes ABCCDE. This preserves the existing lettered teaching abstraction; '
		'letters and lengths are schematic, not measured cytological bands. '
		'The original source neck is retained above C at the same proximal distance in both '
		'chromosomes. Source body lengths 538 and 679 pixels are represented at half scale.', body)


OPSIN_TRACKS = '<g font-family="Atkinson Hyperlegible Next" fill="#242334"><g id="array-1"><text x="30" y="82" font-size="25">X chromosome: r + 1 g</text><path d="M35 135 H920" stroke="#655A85" stroke-width="9"/><rect x="100" y="110" width="140" height="50" rx="10" fill="#D40000"/><text x="170" y="145" text-anchor="middle" font-size="29" fill="white">r</text><rect x="280" y="110" width="140" height="50" rx="10" fill="#007A00"/><text x="350" y="145" text-anchor="middle" font-size="29" fill="white">g</text></g><g id="array-2"><text x="30" y="217" font-size="25">X chromosome: r + 2 g</text><path d="M35 270 H920" stroke="#655A85" stroke-width="9"/><rect x="100" y="245" width="140" height="50" rx="10" fill="#D40000"/><text x="170" y="280" text-anchor="middle" font-size="29" fill="white">r</text><rect x="280" y="245" width="140" height="50" rx="10" fill="#007A00"/><text x="350" y="280" text-anchor="middle" font-size="29" fill="white">g</text><rect x="460" y="245" width="140" height="50" rx="10" fill="#007A00"/><text x="530" y="280" text-anchor="middle" font-size="29" fill="white">g</text></g><g id="array-3"><text x="30" y="352" font-size="25">X chromosome: r + 3 g</text><path d="M35 405 H920" stroke="#655A85" stroke-width="9"/><rect x="100" y="380" width="140" height="50" rx="10" fill="#D40000"/><text x="170" y="415" text-anchor="middle" font-size="29" fill="white">r</text><rect x="280" y="380" width="140" height="50" rx="10" fill="#007A00"/><text x="350" y="415" text-anchor="middle" font-size="29" fill="white">g</text><rect x="460" y="380" width="140" height="50" rx="10" fill="#007A00"/><text x="530" y="415" text-anchor="middle" font-size="29" fill="white">g</text><rect x="640" y="380" width="140" height="50" rx="10" fill="#007A00"/><text x="710" y="415" text-anchor="middle" font-size="29" fill="white">g</text></g></g>'


#============================================
def opsin_arrays() -> None:
	"""Restore source image004 X context without changing molecular array geometry."""
	# Purple/tan boundaries traced on source y=55, x=330..809; neck center x=619.
	# These are source illustration bands, not named or measured human cytobands.
	boundaries = (330, 333, 340, 351, 381, 409, 434, 449, 466, 470, 480,
		487, 523, 527, 545, 581, 590, 619, 637, 649, 663, 675, 688,
		710, 713, 733, 757, 765, 809)
	purple_starts = (333, 351, 409, 449, 470, 487, 527, 581, 637, 663,
		688, 713, 757)
	regions = tuple(svg_tools.chromosomes.Segment('',
		'#776098' if start in purple_starts else '#EDCF90', end-start)
		for start, end in zip(boundaries, boundaries[1:]))
	model = svg_tools.chromosomes.Chromosome(regions,
		centromeres=(svg_tools.chromosomes.Centromere(boundaries.index(619)),))
	part = svg_tools.chromosomes.chromosome_part('opsin-source-x', model,
		thickness=42, texture=False, labels=False)
	body = f'<g transform="translate(280 30)">{part.fragment}</g>'
	body += svg_tools.drawing.text(250, 61, 'X', size=29,
		color='#242334', anchor='middle', font='Atkinson Hyperlegible Next')
	body += '<path d="M280 78 V95 L15 220 V280 H35 M280 95 L950 220 V280 H920" '
	body += 'fill="none" stroke="#526879" stroke-width="2"/>'
	body += f'<g transform="translate(0 180)">{OPSIN_TRACKS}</g>'
	svg_tools.drawing.write_svg(ASSETS / 'opsin_arrays.drawn.svg', 1000, 680,
		'Red and green pigment gene arrays on the X chromosome',
		'Source image004: banded whole X chromosome with source neck and left-tip locus '
		'leaders to an expanded molecular region. One r gene followed by one, two, or three '
		'g genes; original molecular gene tracks unchanged. Whole chromosome source bands '
		'are illustration identities, not measured cytoband data. Expansion is not to scale.', body)


#============================================
def main() -> None:
	"""Regenerate only whole-chromosome schematic consumers."""
	overview()
	copy_number()
	crossover()
	opsin_arrays()


if __name__ == '__main__':
	main()
