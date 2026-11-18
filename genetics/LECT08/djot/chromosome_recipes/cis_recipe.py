#!/usr/bin/env python3
"""Rebuild cis/trans panels from source composition and shared chromosome parts."""
# Standard Library
import argparse
import json
import pathlib
import subprocess

# PIP3 modules

# local repo modules
import lxml.etree
import svg_tools._xml
import svg_tools.chromosomes
import svg_tools.drawing
import svg_tools.palette
import svg_tools.chromosome_topology as topology


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse the output destination."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-o', '--output-root', dest='output_root', type=pathlib.Path)
	args = parser.parse_args()
	return args


#============================================
def draw_wide_panel(source: dict) -> lxml.etree._Element:
	"""Compose cis and trans panels from the homologs and their layout."""
	left, top, width, height = source['view_box']
	root = lxml.etree.Element('svg', {
		'width': str(width), 'height': str(height), 'viewBox': f'{left} {top} {width} {height}',
		'role': 'img', 'aria-labelledby': 'linkage_chromosomes-title linkage_chromosomes-desc',
	})
	lxml.etree.SubElement(root, 'title', {'id': 'linkage_chromosomes-title'}).text = source['title']
	lxml.etree.SubElement(root, 'desc', {'id': 'linkage_chromosomes-desc'}).text = source['description']
	font = 'Atkinson Hyperlegible Next, sans-serif'
	panels = lxml.etree.SubElement(root, 'g', {'font-family': font})

	length = 256
	cis_blue = topology.chromosome('cis-blue-homolog', length=length,
		centromere=60/length, genes={'w': 115/length, 'm': 215/length})
	cis_orange = topology.homolog(cis_blue, 'cis-orange-homolog', alleles={'w': '+', 'm': '+'})
	trans_blue = topology.homolog(cis_blue, 'trans-blue-homolog', alleles={'m': '+'})
	trans_orange = topology.homolog(cis_blue, 'trans-orange-homolog', alleles={'w': '+'})
	for name, blue, orange in (('cis', cis_blue, cis_orange), ('trans', trans_blue, trans_orange)):
		layout = source['panels'][name]
		panel = lxml.etree.SubElement(panels, 'g', {'id': name})
		caption = svg_tools.drawing.text(*layout['caption_xy'], name, size=34, color='#253342', font=font)
		label = svg_tools._xml.parse(caption)
		label.set('font-style', 'italic')
		panel.append(label)
		x = layout['caption_xy'][0] - length/2
		for model, y, hue in ((blue, 154, 'sky_blue'), (orange, 270, 'dark_orange')):
			part = svg_tools.chromosomes.render(f'{model.id}-chromatid', model,
				points=((x, y), (x + length, y)), width=40,
				palette={(model.id, 'body'): svg_tools.palette.shade(hue, 'dark')})
			group = lxml.etree.SubElement(panel, 'g', {'id': model.id})
			group.append(svg_tools._xml.parse(part.fragment))
	return root


#============================================
def draw_portrait_panel(source: dict) -> lxml.etree._Element:
	"""Keep the narrow panel's homologs on a shared scale and label their two loci."""
	width, height = source['size']
	root = lxml.etree.Element('svg', {'width': str(width), 'height': str(height),
		'viewBox': f'0 0 {width} {height}', 'role': 'img',
		'aria-labelledby': 'linkage_portrait-title linkage_portrait-desc'})
	lxml.etree.SubElement(root, 'title', {'id': 'linkage_portrait-title'}).text = source['title']
	lxml.etree.SubElement(root, 'desc', {'id': 'linkage_portrait-desc'}).text = source['description']
	font = 'Atkinson Hyperlegible Next, sans-serif'
	panels = lxml.etree.SubElement(root, 'g', {'font-family': font})
	start, end = source['arm_extent']
	centromere = source['centromere']
	loci = source['loci_x']
	positions = [value - start for value in loci]
	boundaries = sorted({0, centromere, end - start,
		*(value + offset for value in positions for offset in (-12, 12))})
	index = 0
	for name, layout in source['panels'].items():
		panel = lxml.etree.SubElement(panels, 'g', {'id': name})
		caption = lxml.etree.SubElement(panel, 'text', {'x': str(width // 2),
			'y': str(layout['heading_y']), 'font-size': '46', 'fill': '#253342',
			'text-anchor': 'middle', 'font-style': 'italic'})
		caption.text = name
		for row in layout['homologs']:
			segments = tuple(svg_tools.chromosomes.Segment('',
				'#F3D788' if any(abs((left + right)/2 - x) < 12 for x in positions) else row['color'],
				right - left) for left, right in zip(boundaries, boundaries[1:]))
			model = svg_tools.chromosomes.Chromosome(segments,
				(svg_tools.chromosomes.Centromere(boundaries.index(centromere)),))
			group = lxml.etree.SubElement(panel, 'g', {'id': f"{name}-{row['name']}-homolog"})
			y = row['y']
			part = svg_tools.chromosomes.chromosome_path_part(f'chromosome-{index}', model,
				f'M{start} {y} H{end}', thickness=40, labels=False)
			group.append(svg_tools._xml.parse(part.fragment))
			for x, allele in zip(loci, row['alleles'], strict=True):
				label = lxml.etree.SubElement(group, 'text', {'x': str(x), 'y': str(y - 34),
					'font-size': '44', 'fill': '#253342', 'text-anchor': 'middle'})
				label.text = allele
			index += 1
	return root


#============================================
def main() -> None:
	"""Regenerate the source compositions."""
	repository = pathlib.Path(subprocess.check_output(
		['git', 'rev-parse', '--show-toplevel'], text=True).strip())
	here = repository / 'genetics/LECT08/djot/chromosome_recipes'
	args = parse_args()
	output_root = args.output_root if args.output_root is not None else here.parent / 'assets'
	destinations = json.loads((here / 'destinations.json').read_text())
	sources = json.loads((here / 'cis_sources.json').read_text())
	for name, source in sources.items():
		if name == 'cis_trans_wide.drawn.svg':
			root = draw_wide_panel(source)
		else:
			root = draw_portrait_panel(source)
		output = output_root / destinations[name]
		output.parent.mkdir(parents=True, exist_ok=True)
		output.write_bytes(lxml.etree.tostring(svg_tools.drawing.svg_root(root), encoding='utf-8', xml_declaration=True))


if __name__ == "__main__":
	main()
