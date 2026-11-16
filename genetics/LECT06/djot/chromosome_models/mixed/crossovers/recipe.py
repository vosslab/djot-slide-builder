"""Preserve molecular evidence and redraw four condensed chromatids at two chiasmata."""

import pathlib
import xml.etree.ElementTree as ET

import svg_tools.chromosomes as chromosomes

BASE = pathlib.Path(__file__).resolve().parent
SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('',SVG)
ET.register_namespace('xlink','http://www.w3.org/1999/xlink')


def build(output_dir: pathlib.Path) -> None:
	"""Insert four shared centerline bodies below the original molecular inset and labels."""
	output_dir.mkdir(parents=True, exist_ok=True)
	source = BASE/'sources/crossovers_chiasmata.svg'
	root = ET.parse(source).getroot()
	art = root.find('.//{'+SVG+'}g[@id="original-artwork"]')
	group = ET.Element('{'+SVG+'}g',{'id':'shared-condensed-chromatids',
		'transform':'translate(105 39) scale(0.415625)'})
	# This white area contains only the old lower chromosome bodies and white space.
	# The separately embedded Holliday model is retained above this layer verbatim.
	ET.SubElement(group,'{'+SVG+'}rect',{'x':'48','y':'615','width':'1012','height':'302',
		'fill':'#FFFFFF'})
	paths = (
		('blue-outer','#1684B4','M 112 654 C 285 710 440 730 600 727 C 760 725 873 699 988 650'),
		('red-outer','#C95642','M 107 867 C 283 851 454 831 612 852 C 784 873 896 878 1005 871'),
		('red-inner','#C95642','M 109 821 C 238 817 311 812 389 769 C 463 729 616 747 714 778 C 825 814 913 833 1007 831'),
		('blue-inner','#1684B4','M 107 699 C 237 739 310 733 389 769 C 476 811 617 814 714 778 C 813 739 919 731 1011 703'),
	)
	for name,color,path in paths:
		model = chromosomes.Chromosome((chromosomes.Segment('',color),))
		part = chromosomes.chromosome_path_part(name,model,path,thickness=32,labels=False)
		group.append(ET.fromstring(part.fragment))
	# Alternate the existing red chromatid over the first contact to retain the weave.
	defs = ET.SubElement(group,'{'+SVG+'}defs')
	clip = ET.SubElement(defs,'{'+SVG+'}clipPath',{'id':'first-contact'})
	ET.SubElement(clip,'{'+SVG+'}circle',{'cx':'389','cy':'769','r':'42'})
	bridge = ET.SubElement(group,'{'+SVG+'}g',{'clip-path':'url(#first-contact)',
		'data-repeat-of':'red-inner'})
	model = chromosomes.Chromosome((chromosomes.Segment('','#C95642'),))
	part = chromosomes.chromosome_path_part('red-inner-contact',model,paths[2][2],
		thickness=32,labels=False)
	bridge.append(ET.fromstring(part.fragment))
	art.insert(1,group)
	root.find('{'+SVG+'}desc').text += (' Lower condensed chromatids use shared chromosome paths. '
		'Four chromatids and two nonsister crossings are retained; the source supplies no '
		'explicit centromere marker in this panel. Original upper chromatin loops, '
		'synaptonemal detail and Holliday molecular structure remain unchanged.')
	result = output_dir/'crossovers_chiasmata.svg'
	ET.ElementTree(root).write(result,encoding='utf-8',xml_declaration=True)
