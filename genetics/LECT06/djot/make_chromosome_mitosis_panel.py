#!/usr/bin/env python3
"""Compose the frozen mitosis background and measured shared-renderer chromosomes."""

import argparse
import base64
import hashlib
import json
import pathlib
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as DET

import svgpathtools
import svg_tools.chromosomes
import svg_tools.drawing


DIRECTORY = pathlib.Path(__file__).resolve().parent
SOURCES = DIRECTORY / 'chromosome_models' / 'mitosis_panel'
OUTPUT = DIRECTORY / 'assets' / 'lect06b-intro_cells' / 'image_011.normal.svg'


#============================================
def embedded_png(path: pathlib.Path) -> str:
	"""Keep the finished SVG portable and independent of local raster paths."""
	encoded = base64.b64encode(path.read_bytes()).decode('ascii')
	result = '<image href="data:image/png;base64,' + encoded
	result += '" width="1037" height="1311"/>'
	return result


#============================================
def chromosome_overlay(ledger: dict) -> str:
	"""Retain measured source paths, sister colors, and supported centromere loci."""
	groups = []
	for chromosome in ledger['objects']:
		fragments = []
		markers = []
		for index, (sections, color_key) in enumerate(zip(chromosome['paths'], chromosome['colors'])):
			path = svgpathtools.parse_path(' '.join(sections))
			first_arm = svgpathtools.parse_path(sections[0])
			if abs(first_arm.end - complex(*chromosome['path_join'])) >= .001:
				raise ValueError('Path join differs from measured source: ' + chromosome['id'])
			color = ledger['colors'][color_key]
			if chromosome['centromere'] is None:
				model = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('', color),))
			else:
				first_length = first_arm.length()
				model = svg_tools.chromosomes.Chromosome((
					svg_tools.chromosomes.Segment('', color, first_length),
					svg_tools.chromosomes.Segment('', color, path.length() - first_length)),
					centromeres=(svg_tools.chromosomes.Centromere(1),))
			name = f"{chromosome['id']}-chromatid-{index + 1}"
			part = svg_tools.chromosomes.chromosome_path_part(name, model, path.d(),
				thickness=chromosome['thickness'], labels=False)
			if chromosome['centromere'] is not None:
				position = complex(*part.anchors['centromere'])
				if abs(position - complex(*chromosome['centromere'])) >= .001:
					raise ValueError('Shared renderer moved a source centromere: ' + name)
			fragment = DET.fromstring(part.fragment)
			marker = fragment.find(f".//*[@id='{name}-centromere-0']")
			if marker is not None:
				fragment.remove(marker)
				if index == 0:
					markers.append(ET.tostring(marker, encoding='unicode'))
			fragments.append(ET.tostring(fragment, encoding='unicode'))
		state = 'replicated' if len(chromosome['paths']) == 2 else 'single-chromatid'
		group = f'<g id="{chromosome["id"]}" data-state="{state}">'
		# The single sister-pair marker stays above both shared-renderer bodies.
		group += ''.join(fragments + markers) + '</g>'
		groups.append(group)
	result = ''.join(groups)
	return result


#============================================
def main(output_root: pathlib.Path | None = None) -> None:
	"""Generate the normal SVG from frozen data without image-processing dependencies."""
	manifest = json.loads((SOURCES / 'manifest.json').read_text())
	for name, expected in manifest.items():
		actual = hashlib.sha256((SOURCES / name).read_bytes()).hexdigest()
		if actual != expected:
			raise ValueError('Frozen input checksum changed: ' + name)
	ledger = json.loads((SOURCES / 'source-ledger.json').read_text())
	objects = ledger['objects']
	if len(objects) != 48 or sum(len(item['paths']) for item in objects) != 64:
		raise ValueError('Source inventory requires 48 chromosomes and 64 chromatids')
	overlay = chromosome_overlay(ledger)
	body = embedded_png(SOURCES / 'background.png') + overlay
	body += embedded_png(SOURCES / 'protected-leaders.png')
	output = OUTPUT if output_root is None else output_root / 'lect06b-intro_cells' / OUTPUT.name
	output.parent.mkdir(parents=True, exist_ok=True)
	svg_tools.drawing.write_svg(output, 1037, 1311,
		'Stages of mitosis',
		'Chromosomes condense in prophase and align at metaphase. '
		'Sister chromatids separate in anaphase, and two daughter nuclei form in telophase. '
		'Enlarged and miniature views show these stages.', body)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--output-root', type=pathlib.Path)
	main(parser.parse_args().output_root)
