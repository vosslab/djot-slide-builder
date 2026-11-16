#!/usr/bin/env python3
"""Compose the frozen meiosis background with measured shared-renderer chromatids."""
import base64
import hashlib
import json
import pathlib
import xml.etree.ElementTree as ET

import svg_tools.chromosomes

DIRECTORY = pathlib.Path(__file__).resolve().parent
SOURCES = DIRECTORY / 'chromosome_models' / 'meiosis_panel'
OUTPUT = DIRECTORY / 'assets' / 'lect06c-meiosis' / 'image_020.normal.svg'


def data_uri(path: pathlib.Path) -> str:
	"""Embed the fixed prepared pixel layer without reprocessing it."""
	return 'data:image/png;base64,' + base64.b64encode(path.read_bytes()).decode('ascii')


def render() -> str:
	"""Return one standalone SVG with 144 authored chromatid centerlines."""
	manifest = json.loads((SOURCES / 'manifest.json').read_text())
	for name, expected in manifest['sha256'].items():
		if hashlib.sha256((SOURCES / name).read_bytes()).hexdigest() != expected:
			raise ValueError(f'Frozen meiosis input changed: {name}')
	records = json.loads((SOURCES / 'chromatids.json').read_text())
	if len(records) != 144:
		raise ValueError('The meiosis source has 72 enlarged and 72 miniature chromatids')
	if sum(record['center'] is not None for record in records) != 136:
		raise ValueError('Only the 136 source-localized centromeres receive markers')
	fragments: list[str] = []
	for record in records:
		model = svg_tools.chromosomes.Chromosome(tuple(svg_tools.chromosomes.Segment('', color, length)
			for color, length in record['segments']), record['center'])
		part = svg_tools.chromosomes.chromosome_path_part(record['name'], model, record['path_d'],
			thickness=record['width'], labels=False)
		fragments.append(part.fragment)
	background = data_uri(SOURCES / 'background.png')
	protection = data_uri(SOURCES / 'foreground-protection.png')
	svg = (
		'<svg xmlns="http://www.w3.org/2000/svg" '
		'xmlns:xlink="http://www.w3.org/1999/xlink" '
		'width="2261" height="1361" viewBox="0 0 2261 1361" '
		'role="img" aria-labelledby="title desc">'
		'<title id="title">Meiosis: chromosome pairing, recombination and separation</title>'
		'<desc id="desc">Pairing and crossing over occur in prophase I. '
		'Homologous chromosomes separate in meiosis I, and sister chromatids separate in meiosis II. '
		'Both enlarged and miniature views end with four daughter cells.</desc>'
		'<defs><mask id="foreground-protection" maskUnits="userSpaceOnUse" '
		'x="0" y="0" width="2261" height="1361">'
		f'<image width="2261" height="1361" xlink:href="{protection}"/>'
		'</mask></defs>'
		f'<image id="source-background" width="2261" height="1361" xlink:href="{background}"/>'
		'<g id="chromosome-bodies" mask="url(#foreground-protection)">'
		+ ''.join(fragments) + '</g></svg>'
	)
	ET.fromstring(svg)
	return svg


def main() -> None:
	OUTPUT.parent.mkdir(parents=True, exist_ok=True)
	OUTPUT.write_text(render(), encoding='utf-8')


if __name__ == '__main__':
	main()
