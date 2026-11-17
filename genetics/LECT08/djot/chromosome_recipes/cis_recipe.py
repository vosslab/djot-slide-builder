#!/usr/bin/env python3
"""Rebuild cis/trans panels from source composition and shared chromosome parts."""
# Standard Library
import argparse
import json
import pathlib
import defusedxml.ElementTree as ET

# local repo modules
import svg_tools.chromosomes
import svgpathtools



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
	HERE = pathlib.Path(__file__).resolve().parent
	args = parse_args()
	OUTPUT = args.output_root
	DESTINATIONS = json.loads((HERE / 'destinations.json').read_text())
	sources = json.loads((HERE / 'cis_sources.json').read_text())
	for name, source in sources.items():
		root = ET.fromstring(source['svg'])
		for parent in root.iter():
			for child in list(parent):
				if 'data-shared-part' not in child.attrib:
					continue
				index = int(child.get('data-shared-part'))
				item = source['parts'][index]
				curve = svgpathtools.parse_path(item['path'])
				loci = [node for node in parent if node.get('stroke') == '#FFFFFF']
				positions = [svgpathtools.parse_path(node.get('d')).start.real-curve.start.real for node in loci]
				boundaries = sorted({0, item['before'], curve.length(),
					*(value+offset for value in positions for offset in (-12,12))})
				segments = tuple(svg_tools.chromosomes.Segment('',
					'#F3D788' if any(abs((a+b)/2-value)<12 for value in positions) else item['color'], b-a)
					for a,b in zip(boundaries,boundaries[1:]))
				model = svg_tools.chromosomes.Chromosome(segments,
					(svg_tools.chromosomes.Centromere(boundaries.index(item['before'])),))
				for node in loci:
					parent.remove(node)
				part = svg_tools.chromosomes.chromosome_path_part(f'chromosome-{index}', model, item['path'],
											thickness=40, labels=False)
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
