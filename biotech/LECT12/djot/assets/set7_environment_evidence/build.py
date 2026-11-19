#!/usr/bin/env python3
"""Draw evidence figures for the public and environmental Set 7 topics."""
import csv
import pathlib

from svg_tools import drawing

HERE = pathlib.Path(__file__).parent
INK = '#344651'
BLUE = '#275A88'
GREEN = '#247257'


def text(x: float, y: float, words: str, size: int = 28, anchor: str = 'middle', color: str = INK) -> str:
	return drawing.text(x, y, words, size=size, anchor=anchor, color=color)


def line(x1: float, y1: float, x2: float, y2: float, width: float = 3, color: str = INK) -> str:
	return drawing.line(x1, y1, x2, y2, width=width, color=color)


def write(name: str, title: str, description: str, parts: list[str]) -> None:
	drawing.write_svg(HERE / f'{name}.drawn.svg', 1000, 500, title, description, ''.join(parts))


def read_series(name: str, value_name: str) -> list[tuple[int, float]]:
	with (HERE / f'{name}.csv').open(newline='') as source:
		rows = list(csv.DictReader(source))
	return [(int(row['year']), float(row[value_name])) for row in rows]


def trend(name: str, title: str,
		series: list[tuple[int, float]], ymax: int, color: str, units: str, description: str, tick_step: int) -> None:
	left, right, top, bottom = 120, 920, 65, 390
	parts = [line(left, top, left, bottom), line(left, bottom, right, bottom)]
	for value in range(0, ymax + 1, ymax // 4):
		y = bottom - (value / ymax) * (bottom - top)
		parts += [line(left - 8, y, left, y), text(left - 18, y + 9, f'{value:,}', 24, 'end')]
	first_year, last_year = series[0][0], series[-1][0]
	points = []
	for year, value in series:
		x = left + (year - first_year) * (right - left) / (last_year - first_year)
		y = bottom - (value / ymax) * (bottom - top)
		points.append(f'{x:.1f},{y:.1f}')
		parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{color}"/>')
	label_years = list(range(first_year, last_year + 1, tick_step))
	if label_years[-1] != last_year:
		label_years.append(last_year)
	for year in label_years:
		x = left + (year - first_year) * (right - left) / (last_year - first_year)
		parts += [line(x, bottom, x, bottom + 8), text(x, 432, str(year), 22)]
	parts += [f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="7"/>',
		text(500, 478, units, 27)]
	write(name, title, description, parts)


def decision_map() -> None:
	parts = []
	for x, label in [(180, 'Question'), (500, 'Evidence'), (820, 'Decision')]:
		parts += [f'<rect x="{x-105}" y="175" width="210" height="100" rx="18" fill="#E8F2F4" stroke="{INK}" stroke-width="3"/>',
			text(x, 233, label, 34)]
	parts += [line(285, 225, 395, 225, 5, GREEN), line(605, 225, 715, 225, 5, GREEN),
		text(180, 330, 'What public-health action', 24), text(180, 360, 'could change?', 24),
		text(500, 330, 'Can existing data', 24), text(500, 360, 'answer it?', 24),
		text(820, 330, 'Benefit, risk,', 24), text(820, 360, 'and oversight', 24)]
	write('review_decision', 'A review decision has a use for the result',
		'Topics 10 and 11. A committee can compare the stated public-health use with evidence and safeguards.', parts)


if __name__ == '__main__':
	trend('overdose_deaths', 'U.S. drug overdose deaths', read_series('overdose_deaths', 'deaths'),
		120000, BLUE, 'Deaths, all drug overdoses',
		'Topic 4. CDC National Vital Statistics System counts. The 2024 count is 79,384.', 2)

	trend('ge_soybean_adoption', 'Herbicide-tolerant soybean adoption', read_series('ge_soybean_adoption', 'percent'),
		100, GREEN, 'Percent of U.S. soybean planted acres',
		'Topic 7. USDA ERS adoption data. Every point is one annual estimate in the published series.', 5)
	decision_map()
