#!/usr/bin/env python3
"""Rebuild unlinked PD and NPD chromatids from explicit centerline models."""

# Standard Library
import json
import pathlib
import xml.etree.ElementTree as ET

# local repo modules
import svg_tools.chromosomes

BASE = pathlib.Path(__file__).resolve().parent
DATA = BASE / 'assets/lect09_history_templates'
OUTPUT = BASE / 'assets/lect09b-tetrads_1_introduction'
NS = 'http://www.w3.org/2000/svg'


def main() -> None:
	"""Render each template slot with the shared chromosome body tool."""
	ET.register_namespace('', NS)
	root = ET.parse(DATA / 'unlinked_pd_npd.svg').getroot()
	models = json.loads((DATA / 'unlinked_pd_npd_models.json').read_text())
	for model in models:
		group = root.find(".//{%s}g[@id='%s']" % (NS, model['id']))
		chromosome = svg_tools.chromosomes.Chromosome((
			svg_tools.chromosomes.Segment(model['id'], model['color']),
		))
		part = svg_tools.chromosomes.chromosome_path_part(
			model['id'] + '-body', chromosome, model['path'], thickness=28, labels=False,
		)
		group.set('data-chromatid', 'true')
		group.append(ET.fromstring(part.fragment))
	OUTPUT.mkdir(parents=True, exist_ok=True)
	ET.ElementTree(root).write(
		OUTPUT / 'unlinked_pd_npd.drawn.svg', encoding='utf-8', xml_declaration=True,
	)


if __name__ == '__main__':
	main()
