#!/usr/bin/env python3
"""Draw four seed phenotypes and an authored wildflower population."""

import pathlib

import svg_tools.drawing
import svg_tools.parts
import svg_tools.phenotypes
import svg_tools.text


#============================================
def population() -> svg_tools.parts.SvgPart:
	"""Place six flowers in two authored rows of three."""
	flowers = {}
	for row, colors in enumerate((('#cf6677', '#cf6677', '#edb9c6'),
			('#edb9c6', '#f8f4ed', '#f8f4ed'))):
		row_parts = [svg_tools.parts.transform(svg_tools.phenotypes.flower(size=60, color=color),
			x=80, y=385 + row*90) for color in colors]
		for column, part in enumerate(svg_tools.parts.distribute(row_parts, 'x', 30)):
			flowers[f'flower_{row}_{column}'] = part
	return svg_tools.parts.group(flowers)


#============================================
def main() -> None:
	"""Write the editable SVG example."""
	move = svg_tools.parts.transform
	label = svg_tools.text.label
	items = [label(360, 38, 'Seed phenotypes', size=24, color='#344651', bold=True)]
	for index, (shape, color, name) in enumerate((('round', '#edc743', 'Round, yellow'),
			('round', '#72a967', 'Round, green'), ('wrinkled', '#edc743', 'Wrinkled, yellow'),
			('wrinkled', '#72a967', 'Wrinkled, green'))):
		x = 90 + index*180
		items.append(move(svg_tools.phenotypes.seed(size=105, color=color, shape=shape), x=x, y=130))
		items.append(label(x, 215, name, size=17, color='#344651'))
	items.extend([label(360, 285, 'A population of six wildflowers', size=24, color='#344651', bold=True),
		population(), label(430, 390, '2 red, 2 pink, 2 white', size=20, color='#344651'),
		label(430, 425, 'Generic radial flowers', size=17, color='#344651')])
	output = pathlib.Path('_temp/svg_toolkit/phenotypes/phenotypes.svg')
	output.parent.mkdir(parents=True, exist_ok=True)
	svg_tools.drawing.write_svg(output, 720, 510, 'Seed and flower phenotypes',
		'Four seed color and shape combinations and six schematic wildflowers.',
		''.join(part.fragment for part in items))


if __name__ == '__main__':
	main()
