#!/usr/bin/env python3
"""Rebuild the illustrative UPGMA slides and their metric trees."""

import json
import pathlib
import itertools
import fractions

import svg_tools.text
import svg_tools.drawing

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE / 'assets' / 'lect11_gene_tree_examples'


def pair_values(left: str, right: str, pairs: dict) -> list[int]:
	"""Return all original cross-cluster pair distances."""
	return [pairs[''.join(sorted((a, b)))] for a in left for b in right]


def distance(left: str, right: str, pairs: dict) -> fractions.Fraction:
	values = pair_values(left, right, pairs)
	return fractions.Fraction(sum(values), len(values))


def steps(data: dict) -> list[dict]:
	"""Compute the full history, weighting each original gene equally."""
	clusters = list(data['labels'])
	heights = {label: fractions.Fraction(0) for label in clusters}
	result = []
	while len(clusters) > 1:
		choices = [(distance(a, b, data['pairs']), a, b)
			for a, b in itertools.combinations(clusters, 2)]
		value, left, right = min(choices)
		merged = ''.join(sorted(left + right))
		remaining = [c for c in clusters if c not in (left, right)]
		height = value / 2
		result.append({'clusters': clusters, 'left': left, 'right': right,
			'merged': merged, 'distance': value, 'height': height,
			'branches': (height - heights[left], height - heights[right]),
			'remaining': remaining})
		heights[merged] = height
		clusters = [merged if c == left else c for c in clusters if c != right]
	return result


def number(value: fractions.Fraction | int) -> str:
	return str(value.numerator) if isinstance(value, fractions.Fraction) and value.denominator == 1 else str(value)


def matrix(clusters: list[str], pairs: dict, group: str, selected: tuple[str, str] | None) -> str:
	"""Build an editable native lower triangular distance table."""
	# Keep repeated matrices stable despite surrounding prompts and answer highlights.
	line = f'{{table-style=matrix-lower table-group={group} padding="3pt 2pt" font-size=22pt}}\n'
	line += '|  | ' + ' | '.join(clusters) + ' |\n'
	line += '| --- | ' + ' | '.join('---' for _ in clusters) + ' |\n'
	for i, row in enumerate(clusters):
		cells = []
		for j, col in enumerate(clusters):
			value = number(distance(row, col, pairs)) if j < i else ''
			if j < i and selected and {row, col} == set(selected):
				value = f'[{value}]{{background-color=#FFF1B8 border="0.5pt solid #222222"}}'
			cells.append(value)
		line += '| ' + row + ' | ' + ' | '.join(cells) + ' |\n'
	return line


def tree(data: dict, history: list[dict], count: int, path: pathlib.Path) -> None:
	"""Draw completed branches with x proportional to height; keep all tips visible."""
	order = data['tip_order']
	root_height = float(history[-1]['height'])
	scale = 300 / root_height
	positions = {label: (330.0, 30 + i * 55.0) for i, label in enumerate(order)}
	body = '<g id="tips">'
	for label in order:
		x, y = positions[label]
		body += svg_tools.text.label(x + 12, y + 8, label, size=30, color='#17202A', anchor='start').fragment
	body += '</g>'
	for index, step in enumerate(history[:count]):
		left, right = step['left'], step['right']
		x1, y1 = positions[left]
		x2, y2 = positions[right]
		x = 330 - float(step['height']) * scale
		y = (y1 + y2) / 2
		body += f'<g id="merge-{index + 1}" stroke="#254B68" stroke-width="3" fill="none">'
		body += f'<path d="M {x1} {y1} H {x} V {y2} H {x2}"/></g>'
		body += svg_tools.text.label(x + 7, y + 12, 'h=' + number(step['height']), size=23,
			color='#17202A', anchor='start').fragment
		positions[step['merged']] = (x, y)
	description = f'{count} completed merges; branch length is proportional to height.'
	svg_tools.drawing.write_svg(path, 375, 60 + (len(order) - 1) * 55, 'Gene tree', description, body)


def slide(title: str, left: str, image: str) -> str:
	return (f'=== layout: two-panels\n\n# {title}\n\n@left\n\n{left}\n'
		f'@right\n\n![Gene tree]({image})\n\n')


def generate(name: str, data: dict, stem: str) -> None:
	history = steps(data)
	result = ''
	for index, step in enumerate(history):
		image = f'assets/lect11_gene_tree_examples/{stem}_{index}.svg'
		tree(data, history, index, HERE / image)
		next_image = f'assets/lect11_gene_tree_examples/{stem}_{index + 1}.svg'
		tree(data, history, index + 1, HERE / next_image)
		group = f'gene-tree-{stem}-{len(step["clusters"])}'
		plain = matrix(step['clusters'], data['pairs'], group, None)
		choice = (step['left'], step['right'])
		answer = matrix(step['clusters'], data['pairs'], group, choice)
		result += slide('Find the Smallest Distance', plain + '\nWhich clusters join? '
			'What are the new height and branch lengths?\n', image)
		result += slide('Join the Closest Clusters', answer + '\n'
			+ f'{step["left"]} + {step["right"]}: distance {number(step["distance"])}; '
			f'height {number(step["height"])}. Branches: {step["left"]} '
			f'{number(step["branches"][0])}; {step["right"]} {number(step["branches"][1])}.\n', next_image)
		lines = []
		for other in step['remaining']:
			values = pair_values(step['merged'], other, data['pairs'])
			terms = ' + '.join(str(value) for value in values)
			lines.append(f'- {step["merged"]} to {other}: ({terms}) / {len(values)} = '
				+ number(distance(step['merged'], other, data['pairs'])))
		if lines:
			question = f'Join {step["left"]} and {step["right"]}. '
			question += f'What are the distances from {step["merged"]} to '
			question += ', '.join(step['remaining']) + '? Count each gene equally.\n\n'
			result += '=== layout: two-panels\n\n# Find the New Distances\n\n@left\n\n'
			result += plain + '\n@right\n\n' + question
			if stem == 'five' and step['merged'] == 'ace':
				result += '=== layout: two-panels\n\n# Count Every Gene Pair\n\n@left\n\n'
				result += plain + '\n@right\n\n'
				result += 'Cluster ac contains 2 genes; e contains 1. Their distances to b are 19 and 22.\n\n'
				result += 'Is the distance from ace to b 20 or 20.5? Why?\n\n'
			result += '=== layout: one-panel\n\n# Update the Distances\n\n@body\n\n'
			result += 'Average the original distances between genes in the two clusters.\n\n'
			result += '\n'.join(lines) + '\n\n'
			if stem == 'five' and step['merged'] == 'ace':
				result += 'Weight each gene equally: (2 x 19 + 1 x 22) / 3 = 20. '
				result += 'The unweighted cluster average gives 20.5.\n\n'
	last_image = f'assets/lect11_gene_tree_examples/{stem}_{len(history)}.svg'
	tree(data, history, len(history), HERE / last_image)
	question = f'Find the path length from the root to a and from the root to {data["tip_order"][-1]}. How do the lengths compare?\n'
	result += slide('Compare the Two Paths', question, last_image)
	result += '=== layout: big-image\n\n@image\n\n![Completed metric gene tree]('
	result += last_image + ')\n\n@caption\n\nReview the Completed Tree\n\n'
	result += '=== layout: one-panel\n\n# Review the Branch Lengths\n\n@body\n\n'
	result += '| Node | Height | Branches to Children |\n| --- | --- | --- |\n'
	for step in history:
		left, right = step['left'], step['right']
		result += f'| {step["merged"]} | {number(step["height"])} | '
		result += f'{left}: {number(step["branches"][0])}; '
		result += f'{right}: {number(step["branches"][1])} |\n'
	result += '\n=== layout: one-panel\n\n# Check the Tree Paths\n\n@body\n\n'
	if data['input_is_ultrametric']:
		result += 'The tree reproduces all input distances.\n\n'
	else:
		result += 'The tree uses cluster averages. Some distances along the tree differ from the original matrix.\n\n'
	result += 'These are example distances, not measurements or years.\n'
	result += '\n'
	result += f'Every root-to-tip path equals {number(history[-1]["height"])} distance units.\n\n'
	result += 'Equal path lengths follow the constant-rate model used to build the tree.\n\n'
	if stem == 'five':
		result += 'The original a-to-e distance is 6; the tree distance is 8.\n'
	(HERE / f'gene_tree_{stem}_steps.djot').write_text(result)


def main() -> None:
	data = json.loads((HERE / 'gene_tree_example_data.json').read_text())
	ASSETS.mkdir(parents=True, exist_ok=True)
	for name, stem in [('four_gene_intro', 'four'), ('five_gene_weighted', 'five'),
		('six_gene_worksheet', 'six')]:
		generate(name, data[name], stem)


if __name__ == '__main__':
	main()
