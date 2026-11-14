#!/usr/bin/env python3
"""Place and group repeated chromosome parts; run from the repository root."""

import pathlib

import svg_tools.chromosomes
import svg_tools.drawing
import svg_tools.parts


#============================================
def main() -> None:
	segment = svg_tools.chromosomes.Segment('A', '#A8DADC', 40)
	model = svg_tools.chromosomes.Chromosome((segment, segment), 1)
	part = svg_tools.chromosomes.chromosome_part('chrom', model, orientation='vertical', labels=False)
	parts = [svg_tools.parts.transform(part, x=30, y=30),
		svg_tools.parts.transform(part, x=30, y=30, rotation=15)]
	parts = svg_tools.parts.align(parts, 'top', 30)
	parts = svg_tools.parts.distribute(parts, 'x', 30)
	combined = svg_tools.parts.group({'first': parts[0], 'second': parts[1]})
	output = pathlib.Path('_temp/placement.svg')
	output.parent.mkdir(exist_ok=True)
	svg_tools.drawing.write_svg(output, 250, 180, 'Chromosome placement',
		'Two aligned chromosome parts with equal spacing.', combined.fragment)
	print(output)


if __name__ == '__main__':
	main()
