#!/usr/bin/env python3
"""Regenerate LECT06 mitosis figures with source-preserving shared chromosome bodies."""
import argparse
import pathlib
import re
import subprocess
import xml.etree.ElementTree as xml
import defusedxml.ElementTree as DET

import svgpathtools

import svg_tools.chromosomes
import svg_tools.chromosome_surface
import svg_tools.drawing


ASSETS = ('m_checkpoint_stop', 'm_checkpoint_go', 'mitosis_interphase_prophase',
	'mitosis_prometaphase_metaphase', 'mitosis_anaphase_telophase')
REPOSITORY_ROOT = pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip())
DIRECTORY = REPOSITORY_ROOT / 'genetics/LECT06/djot'
OUT = DIRECTORY / 'assets' / 'lect06b-intro_cells'
TEMPLATES = DIRECTORY / 'chromosome_models' / 'mitosis'
SVG = '{http://www.w3.org/2000/svg}'


def chromosome(name: str, chromatids: int, path_d: str | None,
	length: float = 60, thickness: float = 36, centromere_fraction: float = .5) -> str:
	"""Return the shared v2 duplicated-X or single-chromatid body at local origin."""
	if chromatids == 1:
		# The source bend is an explicit centromere (or the symmetric V apex in
		# checkpoint art).  Keep it as the shared hollow marker rather than
		# replacing it with an unmarked rod.
		segments = (
			svg_tools.chromosomes.Segment('', '#56529A', centromere_fraction),
			svg_tools.chromosomes.Segment('', '#56529A', 1-centromere_fraction))
		model = svg_tools.chromosomes.Chromosome(segments, centromeres=(svg_tools.chromosomes.Centromere(1),))
	else:
		segments = (svg_tools.chromosomes.Segment('', '#56529A'),
			svg_tools.chromosomes.Segment('', '#56529A'))
		model = svg_tools.chromosomes.Chromosome(segments, centromeres=(svg_tools.chromosomes.Centromere(1),))
	if chromatids == 1 and path_d:
		return svg_tools.chromosomes.chromosome_path_part(name, model, path_d,
			thickness=thickness, labels=False).fragment
	part = svg_tools.chromosomes.chromosome_part(name, model, length=length,
		thickness=thickness/2.2, orientation='horizontal', sisters=True, texture=False, labels=False)
	return f'<g transform="translate({-length/2} {-thickness/2})">' + part.fragment + '</g>'


def body_extent(group: xml.Element) -> tuple[float, float]:
	"""Match the source painted envelope before replacing a duplicated X."""
	points = []
	stroke = 0.0
	for node in group.iter(SVG + 'path'):
		if 'd' not in node.attrib:
			continue
		path = svgpathtools.parse_path(node.attrib['d'])
		for segment in path:
			points.extend(segment.bpoints())
		stroke = max(stroke, float(node.attrib.get('stroke-width', '0')))
	if not points:
		return 60, 36
	xs = [point.real for point in points]
	ys = [point.imag for point in points]
	return max(xs)-min(xs)+stroke, max(ys)-min(ys)+stroke


def outer_stroke(group: xml.Element) -> float:
	"""Return the visible source body width, never its bounding-box height."""
	return max((float(node.attrib.get('stroke-width', '0'))
		for node in group.iter(SVG + 'path') if node.attrib.get('d')), default=10)


def source_centromere_fraction(group: xml.Element, path_d: str) -> float:
	"""Project a source centromere ellipse onto its original body centerline."""
	ellipse = next((node for node in group.iter(SVG + 'ellipse')
		if 'cx' in node.attrib and 'cy' in node.attrib), None)
	if ellipse is None:
		return .5
	marker = complex(float(ellipse.attrib['cx']), float(ellipse.attrib['cy']))
	path = svg_tools.chromosome_surface.smooth_centerline(svgpathtools.parse_path(path_d))
	return max(.001, min(.999, svg_tools.chromosome_surface.nearest_distance(path, marker)/path.length()))


def svg_fragment(fragment: str) -> xml.Element:
	"""Parse a shared body fragment as SVG so serialization keeps one namespace."""
	element = DET.fromstring(fragment)
	for node in element.iter():
		if isinstance(node.tag, str) and not node.tag.startswith('{'):
			node.tag = SVG + node.tag
	return element


def replace_groups(root: xml.Element) -> list[dict]:
	"""Keep each existing semantic chromosome group and its placement transform."""
	records = []
	for group in root.iter(SVG + 'g'):
		identifier = group.attrib.get('id', '')
		is_checkpoint_chromosome = re.fullmatch(r'(pro|meta)-chromosome-[1-6]', identifier)
		if group.attrib.get('data-chromosomes') != '1' and not is_checkpoint_chromosome:
			continue
		chromatids = int(group.attrib.get('data-chromatids', '2'))
		path = next((child.attrib.get('d') for child in group.iter(SVG + 'path')
			if child.attrib.get('d')), None)
		length, thickness = body_extent(group)
		if chromatids == 1:
			thickness = outer_stroke(group)
			centromere_fraction = source_centromere_fraction(group, path)
		else:
			centromere_fraction = .5
		for child in list(group):
			group.remove(child)
		group.append(svg_fragment(chromosome(identifier + '-shared', chromatids, path,
			length, thickness, centromere_fraction)))
		records.append({'id': identifier, 'chromatids': chromatids,
			'transform': group.attrib.get('transform', '')})
	# The anaphase checkpoint predates semantic groups. Its twelve purple V paths
	# are still source-owned chromosome silhouettes and need the same migration.
	for cell in root.iter(SVG + 'g'):
		if cell.attrib.get('id') != 'cell-ana':
			continue
		for index, child in enumerate(list(cell)):
			if child.tag != SVG + 'path' or child.attrib.get('stroke') != '#65517f':
				continue
			path = child.attrib['d']
			body = chromosome(f'checkpoint-anaphase-{index}', 1, path,
				thickness=float(child.attrib['stroke-width']), centromere_fraction=.5)
			position = list(cell).index(child)
			cell.remove(child)
			cell.insert(position, svg_fragment(body))
			records.append({'id': f'checkpoint-anaphase-{index}', 'chromatids': 1,
				'transform': 'source-centerline'})
	return records


def main(output_root: pathlib.Path | None = None) -> None:
	xml.register_namespace("", SVG[1:-1])
	output_dir = OUT if output_root is None else output_root / 'lect06b-intro_cells'
	output_dir.mkdir(parents=True, exist_ok=True)
	manifest = {}
	for stem in ASSETS:
		root = DET.parse(TEMPLATES / (stem + '.drawn.svg')).getroot()
		manifest[stem] = replace_groups(root)
		svg_tools.drawing.remove_canvas_background(root)
		output = output_dir / (stem + '.drawn.svg')
		xml.ElementTree(root).write(output, encoding='unicode')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--output-root', type=pathlib.Path)
	main(parser.parse_args().output_root)
