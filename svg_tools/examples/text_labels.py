#!/usr/bin/env python3
"""Write a font-backed label example to the repository scratch directory."""

import pathlib

import svg_tools.drawing
import svg_tools.text


#============================================
def main() -> None:
	labels = [
		svg_tools.text.label(30, 45, 'Ordinary label: \u03b1, \u03b2, \u0394', size=24,
			color='#17324D', anchor='start'),
		svg_tools.text.label(30, 85, 'Bold italic gene', size=24, color='#7D245B',
			anchor='start', bold=True, italic=True),
		svg_tools.text.label(30, 125, 'ACGT 012345', size=24, color='#175E48',
			anchor='start', role='sequence'),
	]
	path = pathlib.Path('_temp/text_labels.svg')
	path.parent.mkdir(exist_ok=True)
	svg_tools.drawing.write_svg(path, 500, 150, 'Text labels',
		'Ordinary and aligned sequence labels', ''.join(part.fragment for part in labels))
	print(path)


if __name__ == '__main__':
	main()
