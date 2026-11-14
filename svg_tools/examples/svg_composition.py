#!/usr/bin/env python3
"""Compose repeated imported patterns and live text; run from the repository root."""

import pathlib

import svg_tools.drawing
import svg_tools.parts
import svg_tools.svg_import


FIGURE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="10 20 100 65">
<defs><pattern id="stripes" width="12" height="12" patternUnits="userSpaceOnUse">
<path d="M0 0L12 12" stroke="#195f82" stroke-width="4"/></pattern></defs>
<rect x="10" y="20" width="100" height="65" fill="#e1f2f6"/>
<rect x="10" y="20" width="100" height="65" fill="url(#stripes)"/>
<rect x="26" y="42" width="68" height="21" rx="3" fill="#e1f2f6"/>
<text x="60" y="58" text-anchor="middle" font-family="Atkinson Hyperlegible Next" font-size="14"
 fill="#102c40">Live text</text></svg>'''


#============================================
def main() -> None:
	part = svg_tools.svg_import.import_svg(FIGURE, name='figure', size=160)
	combined = svg_tools.parts.group({'left': svg_tools.parts.transform(part, x=15, y=15),
		'right': svg_tools.parts.transform(part, x=195, y=15)})
	output = pathlib.Path('_temp/svg_composition.svg')
	output.parent.mkdir(exist_ok=True)
	svg_tools.drawing.write_svg(output, 370, 135, 'Imported SVG composition',
		'Two copies of a patterned figure with live text.', combined.fragment)
	print(output)


if __name__ == '__main__':
	main()
