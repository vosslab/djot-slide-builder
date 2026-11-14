#!/usr/bin/env python3
"""Rebuild the Western detection figure with explicitly docked binding parts."""

import pathlib
import sys

import svg_tools.binding
import svg_tools.drawing
import svg_tools.parts
import svg_tools.text


#============================================
def dock(part: svg_tools.parts.SvgPart, anchor: str, point: tuple[float, float], rotation: float = 0) -> svg_tools.parts.SvgPart:
	"""Place an anchor at the requested contact point."""
	rotated = svg_tools.parts.transform(part, rotation=rotation)
	x, y = rotated.anchors[anchor]
	return svg_tools.parts.transform(rotated, x=point[0]-x, y=point[1]-y)


#============================================
def main() -> None:
	target = svg_tools.parts.transform(svg_tools.binding.antigen(width=160, height=80, color='#73ba68'), x=520, y=530)
	primary = dock(svg_tools.binding.antibody(width=170, height=170, color='#d34b59'),
		'Fab_left', target.anchors['top'], rotation=180)
	secondary = dock(svg_tools.binding.antibody(width=170, height=170, color='#4291c4'),
		'Fab_right', primary.anchors['Fc'], rotation=180)
	enzyme = dock(svg_tools.binding.enzyme_tag(width=58, height=58, color='#bf3158'),
		'bottom', secondary.anchors['Fc'])
	molecules = svg_tools.parts.group({'target': target, 'primary': primary, 'secondary': secondary, 'enzyme': enzyme})
	color = '#213547'
	labels = [
		svg_tools.text.label(600, 50, 'Detection in Western Blots', size=39, color=color, bold=True),
		svg_tools.text.label(70, 199, 'Enzyme-conjugated', size=30, color=color, anchor='start'),
		svg_tools.text.label(70, 236, 'Secondary Antibody', size=30, color=color, anchor='start'),
		svg_tools.text.label(70, 387, 'Primary Antibody', size=30, color=color, anchor='start'),
		svg_tools.text.label(800, 503, 'Target Protein', size=30, color=color, anchor='start'),
		svg_tools.text.label(865, 263, 'Enzyme Substrate', size=30, color=color, anchor='start'),
		svg_tools.text.label(863, 101, 'Detection Signal', size=30, color=color, anchor='start'),
		svg_tools.text.label(863, 133, '(colorimetric or', size=25, color=color, anchor='start'),
		svg_tools.text.label(863, 163, 'chemiluminescent)', size=25, color=color, anchor='start'),
		svg_tools.text.label(619, 665, 'Membrane Containing Transferred Protein', size=27, color=color),
		svg_tools.text.styled_label(70, 716, [svg_tools.text.TextRun('Diagram 2:', bold=True, italic=True),
			svg_tools.text.TextRun(' Illustration of detection in Western Blots.', italic=True)],
			size=24, color=color),
	]
	background = '''<defs><marker id="arrow" viewBox="0 0 12 10" markerWidth="23" markerHeight="21" refX="10" refY="5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L12 5L0 10Z" fill="#bd2942"/></marker></defs>
	<rect width="1200" height="732.743363" fill="white"/>
	<g stroke-linejoin="round"><path d="M217 535H867L1055 614H66Z" fill="#f5f4df" stroke="#92a0a5" stroke-width="2.5"/><path d="M66 614H1055V628H66Z" fill="#dce1d4" stroke="#526879" stroke-width="2.7"/><path d="M217 535H867" fill="none" stroke="#b0bab7" stroke-width="1.5"/><path d="M238 550L153 595M340 550L285 595M744 550L789 595M846 550L926 595" fill="none" stroke="#c6cec1" stroke-width="1.5"/></g>'''
	details = '''<g fill="#c4cbd0" stroke="#6b7d89" stroke-width="2"><circle cx="802" cy="238" r="10"/><circle cx="830" cy="246" r="10"/><circle cx="813" cy="269" r="10"/><circle cx="786" cy="263" r="10"/></g>
	<g fill="#ffd64e" stroke="#ad800e" stroke-width="2"><circle cx="795" cy="105" r="10"/><circle cx="822" cy="114" r="10"/><circle cx="806" cy="138" r="10"/><circle cx="779" cy="130" r="10"/></g>
	<g fill="none" stroke="#bd2942" stroke-width="5" stroke-linecap="round"><path d="M766 251Q650 250 554 155" marker-end="url(#arrow)"/><path d="M551 120Q650 80 756 115" marker-end="url(#arrow)"/></g>
	<g fill="none" stroke="#526879" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M392 212H440L493 246"/><path d="M324 378H429"/><path d="M784 494H658L600 520"/><path d="M858 254H849"/><path d="M852 123H842"/><path d="M66 643V655H332M1055 643V655H906"/></g>'''
	output = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(
		'biotech/LECT04/djot/assets/lect04c-talking_points_set_3/western_detection_detail_toolkit.drawn.svg')
	output.parent.mkdir(parents=True, exist_ok=True)
	svg_tools.drawing.write_svg(output, 1200, 732.743363, 'Detection in Western Blots',
		'A target protein rests on a membrane and binds a primary antibody. A secondary antibody binds the primary antibody and carries an enzyme; substrate enters and detection signal leaves.',
		background + molecules.fragment + details + ''.join(label.fragment for label in labels))


if __name__ == '__main__':
	main()
