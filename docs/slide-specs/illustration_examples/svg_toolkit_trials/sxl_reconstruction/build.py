import pathlib

import svg_tools.annotations as annotations
import svg_tools.drawing as drawing
import svg_tools.parts as parts
import svg_tools.text as text


OUT = pathlib.Path(__file__).with_name('sxl_reconstruction_trial.drawn.svg')
INK = '#344651'
ON = '#f5d9df'
OFF = '#d9eeec'
WHITE = '#ffffff'
items = {}


def label(key: str, x: int, y: int, lines: list[str], size: int = 23, color: str = INK) -> None:
	for index, line in enumerate(lines):
		items[f'{key}_{index}'] = text.label(x, y + index * 27, line,
			size=size, color=color, anchor='start')


def box(key: str, x: int, y: int, width: int, height: int,
		lines: str | list[text.TextRun], fill: str = WHITE, size: int = 22) -> None:
	items[key] = parts.transform(annotations.box(lines, width, height, fill,
		font_size=size, stroke=INK, stroke_width=1.5), x=x, y=y)


def arrow(key: str, points: list[tuple[int, int]]) -> None:
	items[key] = annotations.connector(points, color=INK, stroke_width=2, head_size=9)


def symbol(key: str, x: int, y: int, kind: str) -> None:
	female = '<path d="M0 17 V37 M-9 28 H9" stroke="#b53b56"/>' if kind != 'male' else ''
	male = '<path d="M12 -12 L29 -29 M17 -29 H29 V-17" stroke="#246c91"/>' if kind != 'female' else ''
	color = '#b53b56' if kind == 'female' else '#246c91'
	fragment = (f'<g transform="translate({x} {y})" fill="none" stroke-width="3" '
		f'stroke-linecap="round" stroke-linejoin="round"><circle r="17" stroke="{color}"/>'
		f'{female}{male}</g>')
	items[key] = parts.SvgPart(fragment, (x - 19, y - 31, x + 31, y + 39), {'center': (x, y)})


label('input', 20, 205, ['Amount of', 'protein from', 'X-linked signal', 'elements (XSE)'])
label('high', 205, 34, ['High', '(equivalent to two', 'X chromosomes)'], size=21)
label('intermediate', 205, 276, ['Intermediate'], size=21)
label('low', 205, 410, ['Low', '(equivalent to one', 'X chromosome)'], size=21)

# Gene symbols are italic; their ON/OFF state is upright.
on_runs = [text.TextRun('Sxl', italic=True), text.TextRun(' ON')]
off_runs = [text.TextRun('Sxl', italic=True), text.TextRun(' OFF')]
box('high_on', 470, 112, 130, 48, on_runs, ON)
box('mid_on', 470, 252, 130, 48, on_runs, ON)
box('mid_off', 470, 340, 130, 48, off_runs, OFF)
box('low_off', 470, 500, 130, 48, off_runs, OFF)
label('some', 405, 213, ['Some cells'], size=20)
label('other', 405, 395, ['Other cells'], size=20)

box('high_protein', 695, 112, 190, 80, 'SXL protein\nproduced')
box('mid_protein', 695, 296, 190, 130, 'SXL protein\nproduced in\nsome cells,\nnot in others')
box('low_protein', 695, 500, 190, 80, 'SXL protein\nnot produced')
box('high_transcript', 960, 112, 220, 80, 'Female-specific\ntranscripts')
box('mid_transcript', 960, 296, 220, 155, 'Female-specific\ntranscripts in some\ncells, male-specific\ntranscripts in other\ncells', size=20)
box('low_transcript', 960, 500, 220, 80, 'Male-specific\ntranscripts')

# The shared input fans out, and the middle branch splits and rejoins.
arrow('input_high', [(165, 320), (185, 320), (185, 112), (399, 112)])
arrow('input_mid_on', [(185, 300), (365, 300), (365, 252), (399, 252)])
arrow('input_mid_off', [(365, 300), (365, 340), (399, 340)])
arrow('input_low', [(185, 300), (185, 500), (399, 500)])
arrow('high_protein_link', [(535, 112), (590, 112)])
arrow('mid_on_link', [(535, 252), (565, 252), (565, 275), (590, 275)])
arrow('mid_off_link', [(535, 340), (565, 340), (565, 317), (590, 317)])
arrow('low_protein_link', [(535, 500), (590, 500)])
for name, y in [('high', 112), ('mid', 296), ('low', 500)]:
	arrow(name + '_transcript_link', [(790, y), (845, y)])
	arrow(name + '_symbol_link', [(1070, y), (1120, y)])
for name, y, kind in [('high', 112, 'female'), ('mid', 296, 'intersex'), ('low', 500, 'male')]:
	symbol(name + '_symbol', 1155, y, kind)
label('female_result', 1200, 106, ['Normal', 'female'], color='#b53b56')
label('intersex_result', 1200, 303, ['Intersex'])
label('male_result', 1200, 494, ['Normal', 'male'], color='#246c91')

body = parts.group(items)
assert body.bounds[0] >= 0 and body.bounds[1] >= 0
assert body.bounds[2] <= 1330 and body.bounds[3] <= 550
OUT.parent.mkdir(parents=True, exist_ok=True)
drawing.write_svg(OUT, 1330, 550, 'X-linked signal and Sxl activity',
	'High, intermediate, and low X-linked signal branches show Sxl states, protein, transcripts, and sex symbols.', body.fragment)
