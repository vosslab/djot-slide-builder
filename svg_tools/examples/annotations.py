#!/usr/bin/env python3
"""Render a branching workflow from editable annotation parts."""

import pathlib

import svg_tools.annotations as annotations
import svg_tools.drawing
import svg_tools.parts as parts
import svg_tools.text as text


#============================================
def main() -> None:
	items = {
		'input': parts.transform(annotations.box('Receive signal', 155, 58, '#dceef4'), x=115, y=80),
		'decision': parts.transform(annotations.box('Signal strong?', 170, 116, '#fff0c2',
			shape='decision', font_size=15), x=330, y=80),
		'output': parts.transform(annotations.box('Activate response', 160, 58, '#dcefdc'), x=555, y=80),
		'pause': parts.transform(annotations.box('Pause response', 160, 58, '#f6dfdd'), x=330, y=230),
		'input_link': annotations.connector([(192.5, 80), (245, 80)]),
		'yes_link': annotations.connector([(415, 80), (475, 80)]),
		'no_link': annotations.connector([(330, 138), (330, 195)], kind='inhibition'),
		'yes': text.label(445, 63, 'yes', size=15, color='#344651'),
		'no': text.label(351, 177, 'no', size=15, color='#344651', anchor='start'),
		'callout': annotations.connector([(410, 230), (450, 230), (470, 205)], kind='callout'),
		'note': text.label(475, 200, 'Response held', size=15, color='#344651', anchor='start'),
	}
	combined = parts.group(items)
	output = pathlib.Path('_temp/annotations.svg')
	output.parent.mkdir(exist_ok=True)
	svg_tools.drawing.write_svg(output, 660, 300, 'Branching workflow',
		'A signal branches to activation or inhibition, with an explanatory callout.', combined.fragment)
	print(output)


if __name__ == '__main__':
	main()
