#!/usr/bin/env python3
"""Draw compact evidence visuals for the LECT12C ethics discussion."""
from pathlib import Path

from svg_tools import annotations, drawing

HERE = Path(__file__).parent
INK = '#344651'
BLUE = '#275A88'
PALE = '#C3E0F1'
GOLD = '#FFD47C'
GREEN = '#247257'
RED = '#AF3C42'


def label(x: float, y: float, words: str, size: int = 30, anchor: str = 'middle', color: str = INK) -> str:
	return drawing.text(x, y, words, size=size, anchor=anchor, color=color)


def line(x1: float, y1: float, x2: float, y2: float, width: float = 4, color: str = INK, dash: str = '') -> str:
	return drawing.line(x1, y1, x2, y2, color=color, width=width, dash=dash)


def arrow(x1: float, y1: float, x2: float, y2: float) -> str:
	return annotations.connector([(x1, y1), (x2, y2)], stroke_width=4, head_size=15).fragment


def box(x: float, y: float, width: float, height: int, fill: str, words: str, detail: str) -> list[str]:
	return [f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="20" fill="{fill}" stroke="{INK}" stroke-width="3"/>',
		label(x + width / 2, y + 53, words, 31), label(x + width / 2, y + 99, detail, 23)]


def write(name: str, height: int, title: str, desc: str, parts: list[str]) -> None:
	drawing.write_svg(HERE / f'{name}.drawn.svg', 1000, height, title, desc, ''.join(parts))


def ethics_questions() -> None:
	parts = [label(500, 48, 'A biotech decision has more than one kind of question', 35)]
	for x, fill, title, detail in [(45, PALE, 'Evidence', 'What did it measure?'),
		(365, GOLD, 'Consent', 'Did they agree?'),
		(685, '#D6EBDD', 'Justice', 'Who bears the risk?')]:
		parts.extend(box(x, 108, 270, 124, fill, title, detail))
	parts.extend([line(500, 264, 500, 312, 4, BLUE), arrow(500, 312, 500, 354),
		label(500, 400, 'A committee can review the plan. People still disagree about the answer.', 29)])
	write('ethics_questions', 430, 'Three questions in an ethics decision',
		'Topic 1. Evidence, consent, and justice are distinct questions.', parts)


def consent_path() -> None:
	parts = [label(500, 46, 'Consent has to match the next use of the sample', 35)]
	stages = [('Donor', PALE, 'agrees to first study'), ('Consent form', GOLD, 'names future use'),
		('New proposal', '#D6EBDD', 'new question or risk')]
	for i, (title, fill, detail) in enumerate(stages):
		x = 45 + i * 320
		parts.extend(box(x, 106, 270, 128, fill, title, detail))
		if i < 2:
			parts.append(arrow(x + 275, 170, x + 315, 170))
	parts.extend([line(500, 266, 500, 313, 4, BLUE), arrow(500, 313, 500, 355),
		label(500, 400, 'Does the original permission cover this proposal?', 34)])
	write('consent_path', 430, 'Consent connects a person to a specific use',
		'Topic 1. The diagram is a teaching schematic, not a legal flowchart.', parts)


def gene_editing_views() -> None:
	parts = [label(500, 45, 'U.S. adults favored some uses of gene editing more than others', 33)]
	items = [(('Treat a serious condition', 'a person has now'), 71, GREEN),
		(('Make a baby more', 'physically attractive'), 5, RED)]
	for n, (lines, value, color) in enumerate(items):
		y = 142 + n * 128
		parts.extend([label(30, y - 11, lines[0], 25, 'start'), label(30, y + 21, lines[1], 25, 'start'),
			f'<rect x="560" y="{y - 32}" width="350" height="54" fill="#E7EAEB"/>',
			f'<rect x="560" y="{y - 32}" width="{value * 3.5}" height="54" fill="{color}"/>',
			label(580 + value * 3.5, y + 18, f'{value}% favor', 29, 'start')])
	parts.extend([line(560, 358, 910, 358, 2), label(560, 396, '0%', 24, 'start'), label(910, 396, '100%', 24, 'end'),
		label(500, 429, 'Pew surveyed U.S. adults on Nov. 1-7, 2021. The report appeared in 2022.', 25)])
	write('gene_editing_views', 455, 'Public views depend on purpose',
		'Topic 2. Pew survey of U.S. adults, November 2021. Percentages are favor responses.', parts)


def correction_record() -> None:
	parts = [label(500, 45, 'A concern about a figure starts with the record', 35)]
	stages = [('Raw files', PALE, 'original images and dates'), ('Compare', GOLD, 'does the panel match?'),
		('Correct or retract', '#D6EBDD', 'tell readers what changed')]
	for i, (title, fill, detail) in enumerate(stages):
		x = 45 + i * 320
		parts.extend(box(x, 108, 270, 128, fill, title, detail))
		if i < 2:
			parts.append(arrow(x + 275, 170, x + 315, 170))
	parts.extend([label(500, 304, 'The record can show an honest mistake or support an investigation.', 29),
		label(500, 359, 'A retraction changes the literature. It does not, by itself, name misconduct.', 27)])
	write('correction_record', 390, 'Follow the evidence before assigning blame',
		'Topic 3. Teaching schematic based on COPE retraction guidance and the NSF definition.', parts)


if __name__ == '__main__':
	ethics_questions()
	consent_path()
	gene_editing_views()
	correction_record()
