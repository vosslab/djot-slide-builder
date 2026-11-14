#!/usr/bin/env python3
"""Compose Western and sandwich binding contacts from independent parts."""

import pathlib

import svg_tools.binding
import svg_tools.drawing
import svg_tools.parts
import svg_tools.text


#============================================
def dock(part: svg_tools.parts.SvgPart, anchor: str, point: tuple[float, float], rotation: float = 0) -> svg_tools.parts.SvgPart:
	"""Place the named point on the caller-specified contact."""
	rotated = svg_tools.parts.transform(part, rotation=rotation)
	x, y = rotated.anchors[anchor]
	return svg_tools.parts.transform(rotated, x=point[0]-x, y=point[1]-y)


#============================================
def examples() -> tuple[svg_tools.parts.SvgPart, svg_tools.parts.SvgPart]:
	"""Return individually named compositions with coincident contact anchors."""
	target = svg_tools.parts.transform(svg_tools.binding.antigen(width=100, height=62, color='#73ba68'), x=250, y=375)
	primary = dock(svg_tools.binding.antibody(width=110, height=120, color='#d34b59'),
		'Fab_left', target.anchors['top'], rotation=180)
	secondary = dock(svg_tools.binding.antibody(width=110, height=120, color='#4291c4'),
		'Fab_left', primary.anchors['Fc'], rotation=180)
	enzyme = dock(svg_tools.binding.enzyme_tag(width=46, height=46, color='#bf3158'),
		'bottom', secondary.anchors['Fc'])
	western = svg_tools.parts.group({'target': target, 'primary': primary, 'secondary': secondary, 'enzyme': enzyme})

	antigen = svg_tools.parts.transform(svg_tools.binding.antigen(width=100, height=62, color='#73ba68'), x=680, y=240)
	capture = dock(svg_tools.binding.antibody(width=110, height=120, color='#4291c4'),
		'Fab_right', antigen.anchors['bottom'])
	detection = dock(svg_tools.binding.antibody(width=110, height=120, color='#d34b59'),
		'Fab_left', antigen.anchors['top'], rotation=180)
	sandwich = svg_tools.parts.group({'antigen': antigen, 'capture': capture, 'detection': detection})
	return western, sandwich


#============================================
def main() -> None:
	western, sandwich = examples()
	labels = [svg_tools.text.label(250, 40, 'Detection in Western Blots', size=22, color='#344651', bold=True),
		svg_tools.text.label(680, 40, 'Sandwich binding', size=22, color='#344651', bold=True),
		svg_tools.text.label(385, 112, 'Enzyme', size=16, color='#344651'),
		svg_tools.text.label(385, 180, 'Secondary Antibody', size=16, color='#344651'),
		svg_tools.text.label(385, 294, 'Primary Antibody', size=16, color='#344651'),
		svg_tools.text.label(250, 432, 'Target Protein', size=16, color='#344651'),
		svg_tools.text.label(805, 152, 'Detection antibody', size=16, color='#344651'),
		svg_tools.text.label(805, 245, 'Antigen', size=16, color='#344651'),
		svg_tools.text.label(805, 340, 'Capture antibody', size=16, color='#344651')]
	output = pathlib.Path('_temp/svg_toolkit/binding/binding.svg')
	output.parent.mkdir(parents=True, exist_ok=True)
	svg_tools.drawing.write_svg(output, 940, 460, 'Binding examples',
		'Western detection and sandwich binding with explicitly authored contacts.',
		western.fragment + sandwich.fragment + ''.join(label.fragment for label in labels))


if __name__ == '__main__':
	main()
