"""Retain the original meiosis tree and replace only schematic chromosome bodies."""

import base64
import pathlib
import xml.etree.ElementTree as ET

import svg_tools.chromosomes as chromosomes

BASE = pathlib.Path(__file__).resolve().parent
SOURCE = BASE / 'sources/meiosis_overview.svg'
SVG = 'http://www.w3.org/2000/svg'
XLINK = 'http://www.w3.org/1999/xlink'
ET.register_namespace('', SVG)
ET.register_namespace('xlink', XLINK)
RED = '#C95D48'
BLUE = '#2196AD'


def model(color: str, tip: str | None = None,
	start_tip: str | None = None) -> chromosomes.Chromosome:
	"""The source's exchanged distal segment remains attached to its chromatid."""
	segments = (chromosomes.Segment('', start_tip or color, 15),
		chromosomes.Segment('', color, 33), chromosomes.Segment('', color, 37),
		chromosomes.Segment('', tip or color, 15))
	return chromosomes.Chromosome(segments, 2)


def geometry() -> tuple[list, list]:
	"""Positions are measured on the 1600-pixel source preview, not new layouts."""
	paths = []
	xs = []
	def rod(name: str, d: str, color: str, tip: str | None = None,
		thick: float = 5.2, start_tip: str | None = None) -> None:
		paths.append((name, d, color, tip, thick, start_tip))
	def pair(name: str, first: str, second: str, color: str,
		tip: str | None = None, start_tip: str | None = None) -> None:
		rod(name+'-s1', first, color)
		rod(name+'-s2', second, color, tip, start_tip=start_tip)
	# Prophase I has three paired homologs, each with two sister chromatids.
	pair('p1-blue-left', 'M 39 443 L 59 483', 'M 45 442 L 65 480', BLUE)
	pair('p1-red-left', 'M 51 444 L 72 481', 'M 57 446 L 77 477', RED)
	pair('p1-blue-diagonal', 'M 76 424 Q 90 452 128 469',
		'M 81 424 Q 94 445 130 465', BLUE)
	pair('p1-red-diagonal', 'M 61 441 Q 88 446 120 474',
		'M 60 447 Q 87 453 119 480', RED)
	pair('p1-red-bottom', 'M 78 494 Q 92 491 107 495',
		'M 78 500 Q 92 496 109 499', RED)
	pair('p1-blue-bottom', 'M 77 503 Q 94 499 108 503',
		'M 77 509 Q 94 505 108 508', BLUE)
	# Metaphase I: three bivalents aligned at the plate.
	for n, (x, length) in enumerate(((226, 42), (281, 31), (322, 48))):
		upper, lower = (BLUE, RED) if n == 2 else (RED, BLUE)
		for row, color in ((480, upper), (491, lower)):
			xs.append((f'm1-{n}-{color[1:]}', x, row, length, 9, color,
				(None, None), (None, None), 'horizontal'))
	# Anaphase I: six still-replicated homologs move toward opposite poles.
	pair('a1-r-long', 'M 443 417 Q 455 395 468 417',
		'M 448 419 Q 455 398 464 419', RED, BLUE)
	pair('a1-r-short', 'M 484 417 Q 495 407 507 417',
		'M 486 422 Q 495 411 506 422', RED, BLUE)
	pair('a1-b-long', 'M 516 407 Q 530 387 551 405',
		'M 519 413 Q 531 393 547 410', BLUE, RED, RED)
	pair('a1-b-other', 'M 441 440 Q 453 458 467 439',
		'M 445 435 Q 453 451 463 435', BLUE, RED)
	pair('a1-b-short', 'M 484 445 Q 495 455 507 444',
		'M 487 441 Q 496 449 504 441', BLUE, RED)
	pair('a1-r-other', 'M 516 445 Q 530 470 551 447',
		'M 520 440 Q 531 462 547 441', RED, BLUE, BLUE)
	# Telophase I and prophase II retain three replicated homologs per cell.
	for prefix, dx, dy, colors in (
		('t1-upper', 0, 0, (RED, RED, BLUE)),
		('t1-lower', 0, 65, (BLUE, BLUE, RED)),
		('p2-upper', 185, 8, (RED, RED, BLUE)),
		('p2-lower', 185, 165, (BLUE, BLUE, RED))):
		def moved(coords: list[tuple[float, float]]) -> str:
			return 'M '+' L '.join(f'{x+dx} {y+dy}' for x, y in coords)
		other = BLUE if colors[0] == RED else RED
		pair(prefix+'-long', moved([(671,393),(699,397),(735,395)]),
			moved([(671,399),(699,402),(735,401)]), colors[0], other)
		pair(prefix+'-short', moved([(689,406),(710,407),(735,407)]),
			moved([(689,412),(710,411),(735,413)]), colors[1], other)
		pair(prefix+'-curved', moved([(655,406),(687,422),(717,427),(743,419)]),
			moved([(655,413),(687,429),(717,433),(743,425)]), colors[2], colors[0], colors[0])
	# Metaphase II: three replicated chromosomes in each retained branch.
	for prefix, dy, colors in (('m2-upper', 0, (RED,RED,BLUE)),
		('m2-lower', 225, (BLUE,BLUE,RED))):
		for n, (y, length) in enumerate(((337, 32),(376, 29),(408, 36))):
			color = colors[n]
			other = BLUE if color == RED else RED
			first, second = ((None, other), (None, None)) if n == 0 else (
				((None, None), (None, other)) if n == 1 else
				((other, other), (None, None)) if dy == 0 else
				((None, None), (other, other)))
			xs.append((prefix+f'-{n}', 1085, y+dy, length, 14, color,
				first, second, 'vertical'))
	# Anaphase II: three single chromatids at each pole in both branches.
	for prefix, dy, colors in (('a2-upper', 0, (RED,RED,BLUE)),
		('a2-lower', 226, (BLUE,BLUE,RED))):
		for n, (y, width, color) in enumerate(zip((380,405,427),(22,16,28),colors)):
			other = BLUE if color == RED else RED
			left, right = ((None, other), (None, None)) if n == 0 else (
				((None, None), (None, other)) if n == 1 else
				((other, other), (None, None)) if dy == 0 else
				((None, None), (other, other)))
			rod(prefix+f'-left-{n}', f'M {1263+width} {y-8+dy} L 1263 {y+dy} L {1263+width} {y+8+dy}', color, left[1], 5.6, left[0])
			rod(prefix+f'-right-{n}', f'M {1327-width} {y-8+dy} L 1327 {y+dy} L {1327-width} {y+8+dy}', color, right[1], 5.6, right[0])
	# Telophase II retains the source's curved long chromosomes, not three equal rods.
	for name,d,color,tip,start_tip in (
		('top-left-long-red','M 1473 397 C 1470 410 1484 414 1482 430',RED,None,None),
		('top-left-short','M 1464 410 L 1464 424 L 1468 442',RED,BLUE,None),
		('top-left-long-blue','M 1457 401 C 1455 416 1464 421 1468 427 C 1475 443 1484 461 1473 462 C 1452 472 1448 449 1457 432',BLUE,RED,RED),
		('top-right-long-red','M 1521 398 C 1524 414 1517 414 1521 427 L 1526 440',RED,None,None),
		('top-right-short','M 1512 408 C 1506 417 1512 424 1512 439',RED,BLUE,None),
		('top-right-long-blue','M 1502 412 C 1497 430 1506 438 1502 454 C 1502 465 1513 467 1519 452 L 1518 428',BLUE,None,None),
		('bottom-left-long-blue','M 1474 608 C 1472 625 1481 629 1480 648',BLUE,None,None),
		('bottom-left-short','M 1456 620 C 1454 633 1463 638 1459 650',BLUE,RED,None),
		('bottom-left-long-red','M 1464 613 C 1463 631 1472 643 1477 660 C 1478 677 1446 669 1450 649 L 1451 634',RED,None,None),
		('bottom-right-long-blue','M 1520 608 C 1523 619 1513 623 1517 633 L 1523 648',BLUE,RED,None),
		('bottom-right-short','M 1509 619 C 1499 626 1505 637 1508 649',BLUE,RED,None),
		('bottom-right-long-red','M 1499 619 C 1490 630 1501 641 1498 650 C 1494 668 1507 671 1516 653 L 1514 633',RED,BLUE,BLUE),
	):
		rod('t2-'+name,d,color,tip,5.5,start_tip)
	return paths, xs


def build(output_dir: pathlib.Path) -> None:
	"""Write the overview asset using only frozen source data and shared bodies."""
	output_dir.mkdir(parents=True, exist_ok=True)
	root = ET.parse(SOURCE).getroot()
	group = root.find(f'{{{SVG}}}g')
	paths, xs = geometry()
	fragments = []
	for name, d, color, tip, thick, start_tip in paths:
		part = chromosomes.chromosome_path_part(name,model(color,tip,start_tip),d,thickness=thick,labels=False)
		fragments.append(part.fragment)
	for name, x, y, length, thick, color, first, second, orientation in xs:
		# Each sister retains its own exchange material within the same shared-tool X.
		copies = [ET.fromstring(chromosomes.chromosome_part(name,model(color,end,start),
			length=length,thickness=thick,orientation=orientation,sisters=True,
			bands=False,labels=False).fragment) for start,end in (first,second)]
		selector = f'g[@clip-path="url(#{name}-sister-1-clip)"]'
		paint = copies[0].find(selector)
		position = list(copies[0]).index(paint)
		copies[0].remove(paint)
		copies[0].insert(position,copies[1].find(selector))
		fragment = ET.tostring(copies[0],encoding='unicode')
		fragments.append(f'<g transform="translate({x} {y})">{fragment}</g>')
	patch_data = (BASE/'sources/body_cleanup.png').read_bytes()
	overlay = ET.Element(f'{{{SVG}}}g', {'id':'shared-chromosome-migration',
		'transform':'translate(21 78) scale(0.474375 0.4738955823)'})
	ET.SubElement(overlay,f'{{{SVG}}}image',{'x':'0','y':'0','width':'1600','height':'747',
		f'{{{XLINK}}}href':'data:image/png;base64,'+base64.b64encode(patch_data).decode()})
	for fragment in fragments:
		overlay.append(ET.fromstring(fragment))
	group.insert(1,overlay)
	root.find(f'{{{SVG}}}desc').text += ' Original artwork, stage tree, native labels and callouts are retained. Only schematic chromosome body pixels are locally masked; replacement rods and sisters use the shared chromosome tools.'
	result = output_dir/'meiosis_overview.svg'
	ET.ElementTree(root).write(result,encoding='utf-8',xml_declaration=True)
