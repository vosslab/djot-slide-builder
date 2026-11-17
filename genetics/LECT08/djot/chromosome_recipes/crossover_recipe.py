#!/usr/bin/env python3
"""Rebuild crossover chromatids with embedded allele loci and source centromere marks."""
# Standard Library
import argparse
import json
import pathlib
import defusedxml.ElementTree as ET
# local repo modules
import subprocess
import svg_tools.chromosomes


LOCUS_FILL = '#F3D788'
LOCUS_LENGTH = 40


#============================================
def allele_model(item: dict, alleles: tuple[str, str]) -> svg_tools.chromosomes.Chromosome:
	"""Split each chromatid into structural color runs and two labeled gene regions."""
	colors = item['colors']
	lengths = item['lengths']
	total = sum(lengths)
	locus_centers = (105, total-35)
	color_ends = []
	distance = 0
	for color, length in zip(colors, lengths):
		distance += length
		color_ends.append((distance, color))
	boundaries = {0, total}
	boundaries.update(end for end, _ in color_ends)
	if item['product']:
		boundaries.add(35)
	for center in locus_centers:
		boundaries.update((center-LOCUS_LENGTH/2, center+LOCUS_LENGTH/2))
	boundaries = sorted(boundaries)
	segments = []
	for left, right in zip(boundaries, boundaries[1:]):
		middle = (left+right)/2
		label = ''
		color = next(color for end, color in color_ends if middle <= end)
		for center, allele in zip(locus_centers, alleles):
			if center-LOCUS_LENGTH/2 <= middle <= center+LOCUS_LENGTH/2:
				label = allele
				color = LOCUS_FILL
		segments.append(svg_tools.chromosomes.Segment(label, color, right-left))
	centromeres = (svg_tools.chromosomes.Centromere(boundaries.index(35)),) if item['product'] else ()
	return svg_tools.chromosomes.Chromosome(tuple(segments), centromeres=centromeres)


#============================================
def remove_legacy_alleles(root: ET.Element) -> None:
	"""Delete source labels replaced by the locus regions within each chromatid."""
	for parent in root.iter():
		for child in list(parent):
			if (child.tag.endswith('text') and child.get('font-size') == '25'
				and child.get('x') in ('180', '395')):
				parent.remove(child)



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
	HERE = pathlib.Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()) / 'genetics/LECT08/djot/chromosome_recipes'
	args = parse_args()
	OUTPUT = args.output_root
	DESTINATIONS = json.loads((HERE / 'destinations.json').read_text())
	for name, source in json.loads((HERE / 'crossover_sources.json').read_text()).items():
		root = ET.fromstring(source['svg'])
		remove_legacy_alleles(root)
		allele_rows = ((('a', 'b'), ('a', 'b'), ('+', '+'), ('+', '+')) * 2
			if name == 'no_crossover.drawn.svg' else
			(('a', 'b'), ('a', '+'), ('+', 'b'), ('+', '+')) * 2)
		for parent in root.iter():
			for child in list(parent):
				if child.get('data-source-centromere') == 'true':
					x, y = float(child.get('cx')), float(child.get('cy'))
					marker_model = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('', '#777777', 10), svg_tools.chromosomes.Segment('', '#777777', 10)), centromeres=(svg_tools.chromosomes.Centromere(1),))
					marker_part = svg_tools.chromosomes.chromosome_path_part(f'marker-{parent.get("id")}-{int(y)}', marker_model, f'M{x-10} {y} H{x+10}', thickness=14, labels=False)
					marker = next(n for n in ET.fromstring(marker_part.fragment).iter()
						if '-centromere-' in n.get('id', ''))
					parent.insert(list(parent).index(child), marker)
					parent.remove(child)
					continue
				if 'data-shared-part' not in child.attrib:
					continue
				index = int(child.get('data-shared-part'))
				item = source['parts'][index]
				model = allele_model(item, allele_rows[index])
				part = svg_tools.chromosomes.chromosome_path_part(f'chromatid-{index}', model,
					item['path'], thickness=28, labels=True, texture=False)
				parent.insert(list(parent).index(child), ET.fromstring(part.fragment))
				parent.remove(child)
		for node in root.iter():
			if node.tag.startswith('{http://www.w3.org/2000/svg}'):
				node.tag = node.tag.split('}', 1)[1]
		root.set('xmlns', 'http://www.w3.org/2000/svg')
		output = (OUTPUT / DESTINATIONS[name] if OUTPUT is not None else HERE.parent / 'assets' / DESTINATIONS[name])
		output.parent.mkdir(parents=True, exist_ok=True)
		output.write_bytes(ET.tostring(root, encoding='utf-8', xml_declaration=True))


if __name__ == "__main__":
	main()
