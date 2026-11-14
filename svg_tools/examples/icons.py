#!/usr/bin/env python3
"""Look up icons and write an editable SVG strip from the repository root."""

import pathlib

import svg_tools.drawing
import svg_tools.icons
import svg_tools.parts


#============================================
def main() -> None:
	print('Microscope matches:', ', '.join(svg_tools.icons.search_icons('microscope')))
	names = ('microscope', 'dna', 'test-tube', 'workflow')
	parts = {name: svg_tools.parts.transform(svg_tools.icons.icon(name, size=48, color='#195f82'), x=20 + index*100, y=15)
		for index, name in enumerate(names)}
	labels = ''.join(svg_tools.drawing.text(44 + index*100, 86, name, size=12, color='#102c40')
		for index, name in enumerate(names))
	output = pathlib.Path('_temp/icons.svg')
	output.parent.mkdir(exist_ok=True)
	svg_tools.drawing.write_svg(output, 400, 100, 'Lucide icon strip',
		'Microscope, DNA, test tube, and workflow icons.', svg_tools.parts.group(parts).fragment + labels)
	print(output)


if __name__ == '__main__':
	main()
