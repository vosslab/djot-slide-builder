#!/usr/bin/env python3
"""Rebuild the centromere teaching figure from its layout and chromosome model."""
import argparse
import json
import pathlib
import subprocess

import svg_tools.annotations
import svg_tools.chromosome_topology as topology
import svg_tools.chromosomes
import svg_tools.drawing
import svg_tools.palette
import svg_tools.parts


BASE = pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip()) / 'genetics/LECT09/djot'
ASSETS = BASE / 'assets/lect09_ordered_templates'
OUTPUT = BASE / 'assets/lect09_tetrad_concepts'
WIDTH = 27


#============================================
def chromosome_body() -> svg_tools.parts.SvgPart:
	"""Render replicated sisters with a shared centromere and a schematic A locus."""
	source_id = 'centromere-drawn'
	length = 70 + 115
	centromere = 70 / length
	model = topology.chromosome(source_id, length=length, centromere=centromere,
		regions=((0, 'p'), (centromere, 'q')), genes={'A': 0.75})
	pair = topology.replicate(model)
	part = svg_tools.chromosomes.render(source_id, pair,
		points=((51.7, 25), (51.7, 215)), width=WIDTH, scale=190 / length,
		palette={(source_id, 'p'): svg_tools.palette.shade('sky_blue', 'dark'),
			(source_id, 'q'): svg_tools.palette.shade('dark_orange', 'dark')})
	return part


#============================================
def compose_callouts(layout: dict, part: svg_tools.parts.SvgPart) -> str:
	"""Label both arms of the right sister and the right edge of the belt."""
	anchors = part.anchors
	# The default straight downward pose places the first sister on the right.
	right_x, centromere_y = anchors['first.centromere']
	arm_edge = right_x + WIDTH / 2
	p_y = (anchors['first.start'][1] + centromere_y) / 2
	q_y = (anchors['first.gene_A'][1] + anchors['first.end'][1]) / 2
	belt_edge = part.bounds[2] - 2
	targets = {
		'p_arm': (arm_edge, round(p_y, 2)),
		'centromere_belt': (belt_edge, round(centromere_y, 2)),
		'q_arm': (arm_edge, round(q_y, 2)),
	}
	label_dx, label_dy = layout['label_offset']
	leaders = []
	labels = []
	for callout in layout['callouts']:
		end = targets[callout['target']]
		start_x = callout['leader_x']
		start_y = callout.get('leader_y', end[1])
		points = [(start_x, start_y), *callout.get('leader_elbows', []), end]
		leader = svg_tools.annotations.connector(points, kind='callout', stroke_width=1.5)
		leaders.append(leader.fragment)
		label = svg_tools.drawing.text(start_x + label_dx, start_y + label_dy,
			callout['label'], size=callout['label_size'], color='#172B3A', anchor='start')
		labels.append(label)
	return (f'<g id="leaders">{"".join(leaders)}</g>'
		f'<g id="labels" font-weight="600">{"".join(labels)}</g>')


#============================================
def main() -> None:
	"""Render the chromosome and its annotations as a complete SVG."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--output-root', type=pathlib.Path, default=OUTPUT.parent)
	args = parser.parse_args()
	layout = json.loads((ASSETS / 'centromere.json').read_text(encoding='utf-8'))
	part = chromosome_body()
	body = f'<g id="chromosome">{part.fragment}</g>' + compose_callouts(layout, part)
	output_dir = args.output_root / 'lect09_tetrad_concepts'
	output_dir.mkdir(parents=True, exist_ok=True)
	svg_tools.drawing.write_svg(output_dir / 'centromere.drawn.svg', *layout['canvas'],
		layout['title'], layout['description'], body)


if __name__ == '__main__':
	main()
