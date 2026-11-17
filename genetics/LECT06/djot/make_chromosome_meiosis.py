#!/usr/bin/env python3
"""Regenerate four later meiosis stage figures from frozen source templates."""
import math
import pathlib
import xml.etree.ElementTree as ET

import svgpathtools

import svg_tools.chromosomes
import svg_tools.chromosome_surface


DIRECTORY = pathlib.Path(__file__).resolve().parent
TEMPLATES = DIRECTORY / 'chromosome_models' / 'meiosis'
OUTPUT = DIRECTORY / 'assets' / 'lect06c-meiosis'
NAMESPACE = '{http://www.w3.org/2000/svg}'
NAMES = (
	'meiosis_prophase_metaphase_i', 'meiosis_anaphase_telophase_i',
	'meiosis_prophase_metaphase_ii', 'meiosis_anaphase_telophase_ii',
	)


def centerline(paths: list[ET.Element]) -> svgpathtools.Path:
	"""Join the two source arms in their existing source order around the neck."""
	if len(paths) == 1:
		return svgpathtools.parse_path(paths[0].attrib['d'])
	first, second = (svgpathtools.parse_path(path.attrib['d']) for path in paths[:2])
	if abs(first[0].start-second[0].start) < .01:
		return svgpathtools.Path(*first.reversed(), *second)
	if abs(first[-1].end-second[0].start) > .01:
		return svgpathtools.Path(*first, svgpathtools.Line(first[-1].end, second[0].start), *second)
	return svgpathtools.Path(*first, *second)


def replace_group(group: ET.Element, parent: ET.Element) -> bool:
	"""Replace one explicitly marked source chromatid without changing its group."""
	paths = [node for node in group if node.tag == NAMESPACE+'path' and node.attrib.get('stroke')]
	if not paths:
		return False
	circle = next((node for node in group if node.tag == NAMESPACE+'circle'), None)
	marker = None if circle is None else complex(float(circle.attrib['cx']), float(circle.attrib['cy']))
	parsed = [(path, svgpathtools.parse_path(path.attrib['d'])) for path in paths]
	if marker is not None:
		body = [(path, curve) for path, curve in parsed if abs(curve[0].start-marker) < .01]
	else:
		body = parsed
	if marker is not None and len(body) not in (1, 2):
		raise ValueError(f'{group.attrib["id"]}: source arms do not share centromere')
	if marker is None:
		line = svgpathtools.Path(*(segment for _, curve in body for segment in curve))
		markers = [complex(float(node.attrib['cx']), float(node.attrib['cy']))
			for node in parent if node.tag == NAMESPACE+'circle']
		marker = min(markers, key=lambda point: abs(line.point(line.ilength(
			svg_tools.chromosome_surface.nearest_distance(line, point)))-point))
	else:
		line = centerline([path for path, _ in body])
	first = body[0][1]
	second = body[1][1] if len(body) == 2 else None
	center = first.length() if second is not None else line.length()/2
	if circle is None:
		center = svg_tools.chromosome_surface.nearest_distance(line, marker)
	else:
		if second is None or abs(first[0].start-marker) > .01 or abs(second[0].start-marker) > .01:
			center = svg_tools.chromosome_surface.nearest_distance(line, marker)
	base = body[0][0].attrib['stroke']
	overlays = []
	for path, overlay in parsed:
		if circle is not None and (path, overlay) in body:
			continue
		start = svg_tools.chromosome_surface.nearest_distance(line, overlay[0].start)
		end = svg_tools.chromosome_surface.nearest_distance(line, overlay[-1].end)
		overlays.append((min(start, end), max(start, end), path.attrib['stroke']))
	breaks = {0.0, center, line.length()}
	for start, end, _ in overlays:
		breaks.update((start, end))
	breaks = sorted(breaks)
	segments = []
	for start, end in zip(breaks, breaks[1:]):
		colour = next((fill for left, right, fill in overlays
			if left <= (start+end)/2 <= right), base)
		segments.append(svg_tools.chromosomes.Segment('', colour, end-start))
	center_index = breaks.index(center)
	if center_index == 0 or center_index == len(breaks)-1:
		raise ValueError(f'{group.attrib["id"]}: source centromere at chromosome end')
	model = svg_tools.chromosomes.Chromosome(tuple(segments), center_index)
	thickness = max(float(path.attrib['stroke-width']) for path in paths)
	part = svg_tools.chromosomes.chromosome_path_part(
		group.attrib['id']+'-shared', model, line.d(), thickness=thickness,
		labels=False)
	for node in list(group):
		if node.tag in (NAMESPACE+'path', NAMESPACE+'circle'):
			group.remove(node)
	group.append(ET.fromstring(part.fragment))
	return True


def main() -> None:
	ET.register_namespace('', NAMESPACE[1:-1])
	OUTPUT.mkdir(parents=True, exist_ok=True)
	for name in NAMES:
		root = ET.parse(TEMPLATES/(name+'.drawn.svg')).getroot()
		parents = {child: parent for parent in root.iter() for child in parent}
		replaced = sum(replace_group(group, parents[group]) for group in root.iter(NAMESPACE+'g')
			if 'sister-' in group.attrib.get('id', '') or
				(name == 'meiosis_homolog_sister_sequence' and
					group.attrib.get('id', '').startswith(('A-', 'B-', 'C-', 'D-', 'E-')) and
					'spindle' not in group.attrib.get('id', '')))
		root.insert(0, ET.Comment(
			f'scratch migration: {replaced} source semantic sister groups use chromosome_path_part'))
		output = OUTPUT/(name+'.drawn.svg')
		output.write_text(ET.tostring(root, encoding='unicode')+'\n')
		print(name, replaced)


if __name__ == '__main__':
	main()
