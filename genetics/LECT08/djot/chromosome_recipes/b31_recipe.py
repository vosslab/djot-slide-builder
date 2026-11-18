#!/usr/bin/env python3
"""Rebuild b31 chromatids over source cells, connectors, micrograph and live labels."""
# Standard Library
import argparse
import json
import pathlib
# local repo modules
import lxml.etree
import svg_tools._xml
import svg_tools.chromosomes
import svg_tools.drawing



#============================================
def parse_args() -> argparse.Namespace:
	"""Parse the output destination."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-o', '--output-root', dest='output_root', type=pathlib.Path)
	args = parser.parse_args()
	return args


#============================================
def main() -> None:
	"""Regenerate the source compositions."""
	HERE=pathlib.Path(__file__).resolve().parent
	args = parse_args()
	OUTPUT = args.output_root
	DESTINATIONS = json.loads((HERE / 'destinations.json').read_text())
	source_path = HERE / 'b31_sources.json'
	source=json.loads(source_path.read_text())
	image_name = 'b31_micrograph_source.svg'
	image_source = svg_tools._xml.parse((source_path.parent / image_name).read_bytes())
	image_uri = next(node for node in image_source if node.tag.endswith('image')).attrib['href']
	root=svg_tools._xml.parse((HERE / source['artwork']).read_text().replace('local-image:' + image_name, image_uri))
	original=next(n for n in root if n.tag.endswith('image'))
	layer=lxml.etree.Element('g')
	# Source art occupies 987 by 937 pixels in the positioned SVG image.
	layer.set('transform','translate(150.49099731445312 14.948984146118164) scale(0.4990932228743324 0.499335117)')
	for patch in source['patches']:
		for path, color in patch['spans']:
			lxml.etree.SubElement(layer,'path',{'d':path,'fill':color})
	blue='#149dc8'
	red='#e93b38'
	# Centerlines follow the source's stage, homolog order and reciprocal products.
	paths=[
		('M464 43 V135',[blue],False),('M472 43 V135',[blue],False),('M482 43 V135',[red],False),('M489 43 V135',[red],False),
		('M459 240 C475 255 454 315 445 343',[blue],True),('M469 240 C485 250 484 260 472 275 C470 290 462 325 457 343',[blue],False),
		('M491 240 C475 250 476 260 488 275 C490 290 498 325 504 343',[red],True),('M500 240 C486 260 503 316 512 343',[red],False),
		('M433 456 C435 474 455 507 460 524',[blue],True),('M457 456 C455 474 437 507 434 524',[red,blue,red],False),
		('M495 456 C497 474 514 507 518 524',[blue,red,blue],True),('M518 456 C515 474 496 507 492 524',[red],False),
		('M333 632 C330 646 320 659 329 674 S338 693 333 700',[blue],True),
		('M380 632 C382 648 393 660 384 674 S375 693 380 700',[red,blue,red],True),
		('M568 632 C565 648 554 660 563 674 S572 693 567 700',[blue,red,blue],True),
		('M620 632 C623 648 634 660 625 674 S616 693 620 700',[red],True),
		('M288 807 V871',[blue],True),('M412 807 V871',[red,blue,red],True),
		('M542 807 V871',[blue,red,blue],True),('M663 807 V871',[red],True)]
	markers=[]
	for i,(d,colors,marker) in enumerate(paths):
		if len(colors)==1:
			regions=[(colors[0],.5),(colors[0],.5)] if marker else [(colors[0],1)]
			center=1 if marker else None
		elif len(colors)==2:
			regions=[(colors[0],.5),(colors[1],.5)]
			center=1 if marker else None
		else:
			regions=[(colors[0],.2),(colors[1],.3),(colors[1],.3),(colors[2],.2)]
			center=2 if marker else None
		sites = () if center is None else (svg_tools.chromosomes.Centromere(center),)
		model=svg_tools.chromosomes.Chromosome(tuple(svg_tools.chromosomes.Segment('',c,n) for c,n in regions),sites)
		part=svg_tools.chromosomes.chromosome_path_part(f'b31-chromatid-{i}',model,d,thickness=7 if i<4 else 9 if i<12 else 12,labels=False)
		fragment=svg_tools._xml.parse(part.fragment)
		for node in list(fragment):
			if node.get('id','').startswith(f'b31-chromatid-{i}-centromere-'):
				fragment.remove(node)
				markers.append(node)
		layer.append(fragment)
	for marker in markers:
		layer.append(marker)
	root.insert(list(root).index(original)+1,layer)
	out=(OUTPUT / 'b31_labeled.svg' if OUTPUT is not None else HERE.parent / 'assets' / DESTINATIONS['b31_labeled.svg'])
	out.parent.mkdir(parents=True, exist_ok=True)
	out.write_bytes(lxml.etree.tostring(svg_tools.drawing.svg_root(root),encoding='utf-8',xml_declaration=True))


if __name__ == "__main__":
	main()
