"""Keep the source recombination tree, ancestry and live annotations intact."""

import base64
import pathlib
import xml.etree.ElementTree as ET

import svg_tools.chromosomes as chromosomes

BASE = pathlib.Path(__file__).resolve().parent
SVG = 'http://www.w3.org/2000/svg'
XLINK = 'http://www.w3.org/1999/xlink'
BLUE = '#1684B4'
RED = '#C95642'
ET.register_namespace('',SVG)
ET.register_namespace('xlink',XLINK)


def model(colors: tuple[str, str, str]) -> chromosomes.Chromosome:
	"""Two distal exchange intervals and the source's central centromere."""
	return chromosomes.Chromosome((chromosomes.Segment('',colors[0],20),
		chromosomes.Segment('',colors[1],30),chromosomes.Segment('',colors[1],30),
		chromosomes.Segment('',colors[2],20)), centromeres=(chromosomes.Centromere(2),))


def source_bodies() -> tuple:
	"""Measured source viewBox coordinates; bend/contact positions remain explicit."""
	b = (BLUE,BLUE,BLUE)
	r = (RED,RED,RED)
	brb = (BLUE,RED,BLUE)
	rbr = (RED,BLUE,RED)
	return (
		# The source has red sisters behind blue sisters, under the fixed nonsister leaders.
		('prophase-red-1',r,'M 385 33 C 385.5 48 384.8 65 385 81',5.0),
		('prophase-red-2',r,'M 392.2 33 C 392.5 48 391.8 65 392 81',5.0),
		('prophase-blue-1',b,'M 382.2 35.5 C 382 49 382.3 66 382.2 83',6.0),
		('prophase-blue-2',b,'M 388 35.5 C 388.4 46 387.7 64 388 83',6.0),
		# Two nonsister contacts flank the central centromere, as in the source.
		('synapsis-blue-outer',b,'M 378 134 C 378 142 382 144 381 148 C 378 157 376 168 379 175 C 377 179 372 182 371 185',4.0),
		('synapsis-red-outer',r,'M 397 134 C 397 140 393 143 392 146 C 396 155 398 168 392 175 C 396 178 400 182 401 185',4.0),
		('synapsis-blue-inner',b,'M 382 134 C 382 140 386 144 387.7 144.2 C 386 151 380 164 383 174 C 383 178 378 182 375 186',4.0),
		('synapsis-red-inner',r,'M 392.5 134 C 392 140 389 143 387.7 144.2 C 390 151 393 164 389 171 C 388 174 384.5 175 384 176 C 389 179 394 183 397 186',4.0),
		# Sister centerlines meet at a shared neck but retain separate source ends.
		('ana1-blue-parent',b,'M 367 242 C 367 250 373 254 374 259 C 374 264 368 271 367 277',4.4),
		('ana1-blue-recombinant',rbr,'M 380 242 C 380 250 374 254 374 259 C 374 264 379 271 380 277',4.4),
		('ana1-red-recombinant',brb,'M 396 242 C 396 250 402 254 403 259 C 403 264 397 271 396 277',4.4),
		('ana1-red-parent',r,'M 409 242 C 409 250 403 254 403 259 C 403 264 408 271 409 277',4.4),
		('ana2-left-parent',b,'M 316 331 C 315 339 311 343 315 350 L 316 363',4.5),
		('ana2-left-recombinant',rbr,'M 341 331 L 344 346 L 341 363',4.5),
		('ana2-right-recombinant',brb,'M 433 331 L 430 346 L 434 363',4.5),
		('ana2-right-parent',r,'M 458 331 L 461 346 L 458 363',4.5),
		('daughter-blue',b,'M 295 415 L 295 450',4.8),
		('daughter-red-blue-red',rbr,'M 356 415 L 356 450',4.8),
		('daughter-blue-red-blue',brb,'M 421 415 L 421 450',4.8),
		('daughter-red',r,'M 481 415 L 481 450',4.8),
	)


def clean_bodies(root: ET.Element) -> None:
	"""Use the reviewed frozen pixel layer, preserving all source annotations."""
	image = root.find('.//{'+SVG+'}image[@id="artwork-1"]')
	data = (BASE/'sources/cleaned_artwork.png').read_bytes()
	image.set('{'+XLINK+'}href','data:image/png;base64,'+base64.b64encode(data).decode())


def build(output_dir: pathlib.Path) -> None:
	"""Write both source reveals with identical chromosome geometry and original labels."""
	output_dir.mkdir(parents=True, exist_ok=True)
	for name in ('recombinant_chromosomes','recombinant_chromosomes_review'):
		source = BASE/'sources'/f'{name}.svg'
		root = ET.parse(source).getroot()
		clean_bodies(root)
		canvas = root.find('{'+SVG+'}g')
		bodies = ET.Element('{'+SVG+'}g',{'id':'shared-source-chromosome-bodies'})
		for identity,colors,path,thick in source_bodies():
			part = chromosomes.chromosome_path_part(identity,model(colors),path,
				thickness=thick,labels=False)
			bodies.append(ET.fromstring(part.fragment))
		# The source places blue over the upper contact and red over the lower contact.
		defs = ET.SubElement(bodies,'{'+SVG+'}defs')
		clip = ET.SubElement(defs,'{'+SVG+'}clipPath',{'id':'upper-synapsis-contact'})
		ET.SubElement(clip,'{'+SVG+'}circle',{'cx':'387.7','cy':'144.2','r':'4.5'})
		bridge = ET.SubElement(bodies,'{'+SVG+'}g',{'clip-path':'url(#upper-synapsis-contact)',
			'data-repeat-of':'synapsis-blue-inner'})
		identity,colors,path,thick = source_bodies()[6]
		bridge.append(ET.fromstring(chromosomes.chromosome_path_part(identity+'-contact',
			model(colors),path,thickness=thick,labels=False).fragment))
		canvas.insert(1,bodies)
		root.find('{'+SVG+'}desc').text += (' Shared chromosome bodies preserve the two '
			'chiasmata, two distinct homologs, sister identity and the red-blue-red / '
			'blue-red-blue double-exchange products. Original source labels and arrows remain live.')
		result = output_dir/f'{name}.svg'
		ET.ElementTree(root).write(result,encoding='utf-8',xml_declaration=True)
