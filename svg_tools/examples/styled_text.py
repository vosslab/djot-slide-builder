#!/usr/bin/env python3
"""Write editable wrapped biology text to the scratch directory."""

import pathlib

import svg_tools.drawing
import svg_tools.text


#============================================
def main() -> None:
	runs = [svg_tools.text.TextRun('The '),
		svg_tools.text.TextRun('BRCA1', bold=True, italic=True, color='#7D245B'),
		svg_tools.text.TextRun(' gene helps repair DNA. Water is H'),
		svg_tools.text.TextRun('2', color='#076DAD', script='sub'),
		svg_tools.text.TextRun('O, and mutations can change protein function.')]
	part = svg_tools.text.wrapped_text(30, 40, runs, width=340, size=24, color='#17324D')
	path = pathlib.Path('_temp/styled_text.svg')
	path.parent.mkdir(exist_ok=True)
	svg_tools.drawing.write_svg(path, 400, 180, 'Styled biology text',
		'Wrapped editable text with a gene and a chemical formula', part.fragment)
	print(path)


if __name__ == '__main__':
	main()
