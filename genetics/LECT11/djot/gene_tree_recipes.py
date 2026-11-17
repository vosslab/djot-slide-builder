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

# Five evenly spaced entries from the documented 14-color procedure palette.
JOIN_COLORS = ('#D40000', '#6C6C00', '#00775F', '#0067CC', '#CC0066')
JOIN_FILLS = dict(zip(JOIN_COLORS, ('#FFB8B8', '#FFFFB8', '#B8FFF0', '#B8DCFF', '#FFB8DC'), strict=True))
AVERAGE_COLORS = ('#00775F', '#0067CC', '#B74300', '#A719DB')
AVERAGE_FILLS = ('#B8FFF0', '#B8DCFF', '#FFD2B8', '#F0B8FF')


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


def matrix(clusters: list[str], pairs: dict, group: str, selected: tuple[str, str] | None,
		cluster_colors: dict[str, str] | None = None,
		merging: tuple[str, ...] = (), targets: list[str] | None = None) -> str:
	"""Build an editable native lower triangular distance table."""
	# Keep repeated matrices stable despite surrounding prompts and answer highlights.
	line = f'{{table-style=matrix-lower table-group={group} padding="3pt 2pt" font-size=22pt}}\n'
	def label(cluster: str) -> str:
		style = 'text-align=center'
		if cluster_colors and cluster in cluster_colors:
			style += f' color={cluster_colors[cluster]}'
		if cluster in merging:
			style += ' background-color=#F0B8FF'
		return f'[{cluster}]{{{style}}}'
	others = targets if targets is not None else [c for c in clusters if c not in merging]
	line += '| [ ]{text-align=center} | ' + ' | '.join(label(cluster) for cluster in clusters) + ' |\n'
	line += '| --- | ' + ' | '.join('---' for _ in clusters) + ' |\n'
	for i, row in enumerate(clusters):
		cells = []
		for j, col in enumerate(clusters):
			value = number(distance(row, col, pairs)) if j < i else ''
			style = 'text-align=center'
			if row in merging or col in merging:
				style += ' background-color=#F0B8FF'
			if j < i and (row in merging) != (col in merging):
				other = col if row in merging else row
				index = next(index for index, target in enumerate(others) if other == target or other in target)
				style = f'text-align=center color={AVERAGE_COLORS[index]} background-color={AVERAGE_FILLS[index]}'
			if j < i and selected and {row, col} == set(selected):
				if cluster_colors:
					color = cluster_colors[''.join(sorted(selected[0] + selected[1]))]
					style = f'text-align=center color={color} background-color={JOIN_FILLS[color]} '
					style += f'border="0.5pt solid {color}"'
				else:
					style = 'text-align=center background-color=#FFF1B8 border="0.5pt solid #222222"'
			cells.append(f'[{value or " "}]{{{style}}}')
		line += '| ' + label(row) + ' | ' + ' | '.join(cells) + ' |\n'
	return line


def tree(data: dict, history: list[dict], count: int, path: pathlib.Path) -> None:
	"""Draw completed branches with x proportional to height; keep all tips visible."""
	order = data['tip_order']
	root_height = float(history[-1]['height'])
	scale = 300 / root_height
	positions = {label: (330.0, 30 + i * 55.0) for i, label in enumerate(order)}
	stage_colors = JOIN_COLORS if len(data['labels']) == 6 else ()
	if len(data['labels']) == 4:
		stage_colors = ('#A719DB', '#00775F', '#45405C')
	colored_steps = history if len(data['labels']) == 4 else history[:count]
	tip_colors = {child: stage_colors[index] for index, step in enumerate(colored_steps)
		for child in (step['left'], step['right']) if len(child) == 1} if stage_colors else {}
	body = '<g id="tips">'
	for label in order:
		x, y = positions[label]
		body += svg_tools.text.label(x + 12, y + 8, label, size=30, color=tip_colors.get(label, '#17202A'), anchor='start').fragment
	body += '</g>'
	for index, step in enumerate(history[:count]):
		left, right = step['left'], step['right']
		x1, y1 = positions[left]
		x2, y2 = positions[right]
		x = 330 - float(step['height']) * scale
		y = (y1 + y2) / 2
		color = stage_colors[index] if stage_colors else '#254B68'
		weight = 4 if stage_colors else 3
		body += f'<g id="merge-{index + 1}" stroke="{color}" stroke-width="{weight}" fill="none">'
		body += f'<path d="M {x1} {y1} H {x} V {y2} H {x2}"/></g>'
		body += svg_tools.text.label(x + 7, y + 12, 'h=' + number(step['height']), size=23,
			color=color if len(data['labels']) == 6 else '#17202A', anchor='start').fragment
		positions[step['merged']] = (x, y)
	description = f'{count} completed merges; branch length is proportional to height.'
	svg_tools.drawing.write_svg(path, 375, 60 + (len(order) - 1) * 55, 'Gene tree', description, body)


def slide(title: str, left: str, image: str) -> str:
	return (f'=== layout: two-panels\n\n# {title}\n\n@left\n\n{left}\n'
		f'@right\n\n![Gene tree]({image})\n\n')


def generate(name: str, data: dict, stem: str) -> None:
	history = steps(data)
	cluster_colors = {step['merged']: JOIN_COLORS[index] for index, step in enumerate(history)} \
		if len(data['labels']) == 6 else None
	result = ''
	dividers = {
		'four': {0: 'First Join', 1: 'Update and Repeat'},
		'five': {1: 'Weight Clusters by Their Size', 2: 'Complete the Remaining Joins'},
		'six': {1: 'Update the Matrix and Repeat', 3: 'Join the Remaining Clusters'},
		'six_extension': {1: 'Update the Matrix and Repeat', 3: 'Join the Remaining Clusters'},
	}[stem]
	for index, step in enumerate(history):
		if index in dividers:
			result += f'=== layout: subsection\n\n# {dividers[index]}\n\n'
		image = f'assets/lect11_gene_tree_examples/{stem}_{index}.svg'
		tree(data, history, index, HERE / image)
		next_image = f'assets/lect11_gene_tree_examples/{stem}_{index + 1}.svg'
		tree(data, history, index + 1, HERE / next_image)
		group = f'gene-tree-{stem}-{len(step["clusters"])}'
		plain = matrix(step['clusters'], data['pairs'], group, None, cluster_colors)
		choice = (step['left'], step['right'])
		merging = choice if stem in ('four', 'five') else ()
		answer = matrix(step['clusters'], data['pairs'], group, choice, cluster_colors, merging)
		stage = f'[Join {index + 1}]{{color={JOIN_COLORS[index]}}}: ' if cluster_colors else ''
		result += slide(stage + 'Find the Smallest Distance', plain + '\nWhich clusters join? '
			'What are the new height and branch lengths?\n', image)
		result += slide(stage + 'Join the Closest Clusters', answer + '\n'
			+ f'{step["left"]} + {step["right"]}: distance {number(step["distance"])}; '
			f'height {number(step["height"])}. Branches: {step["left"]} '
			f'{number(step["branches"][0])}; {step["right"]} {number(step["branches"][1])}.\n', next_image)
		lines = []
		for target_index, other in enumerate(step['remaining']):
			values = pair_values(step['merged'], other, data['pairs'])
			terms = ' + '.join(str(value) for value in values)
			calculation = f'{step["merged"]} to {other}: ({terms}) / {len(values)} = '
			calculation += number(distance(step['merged'], other, data['pairs']))
			if merging:
				calculation = f'[{calculation}]{{color={AVERAGE_COLORS[target_index]}}}'
			lines.append('- ' + calculation)
		if lines:
			question = f'Join {step["left"]} and {step["right"]}. '
			question += f'What are the distances from {step["merged"]} to '
			question += ', '.join(step['remaining']) + '? Count each gene equally.\n\n'
			result += f'=== layout: two-panels\n\n# {stage}Find the New Distances\n\n@left\n\n'
			working = matrix(step['clusters'], data['pairs'], group, None, cluster_colors, merging)
			result += working + '\n@right\n\n' + question
			if stem == 'five' and step['merged'] == 'ace':
				result += '=== layout: two-panels\n\n# Count Every Gene Pair\n\n@left\n\n'
				result += plain + '\n@right\n\n'
				result += 'Cluster ac contains 2 genes; e contains 1. Their distances to b are 19 and 22.\n\n'
				result += 'Is the distance from ace to b 20 or 20.5? Why?\n\n'
			if merging:
				original = matrix(data['labels'], data['pairs'], f'gene-tree-{stem}-{len(data["labels"])}',
					None, merging=tuple(step['merged']), targets=step['remaining'])
				result += f'=== layout: two-panels\n\n# {stage}Update the Distances\n\n@left\n\n'
				result += original + '\n@right\n\n'
				result += 'Purple bands mark the genes being merged. Same-colored cells feed one average.\n\n'
			else:
				result += f'=== layout: one-panel\n\n# {stage}Update the Distances\n\n@body\n\n'
			result += 'Average the original distances between genes in the two clusters.\n\n'
			result += '\n'.join(lines) + '\n\n'
			if stem == 'five' and step['merged'] == 'ace':
				result += 'Weight each gene equally: (2 x 19 + 1 x 22) / 3 = 20. '
				result += 'The unweighted cluster average gives 20.5.\n\n'
	last_image = f'assets/lect11_gene_tree_examples/{stem}_{len(history)}.svg'
	tree(data, history, len(history), HERE / last_image)
	question = f'Find the path length from the root to a and from the root to {data["tip_order"][-1]}. How do the lengths compare?\n'
	result += '=== layout: subsection\n\n# Check the Finished Tree\n\n'
	result += slide('Compare the Two Paths', question, last_image)
	result += '=== layout: big-image\n\n@image\n\n![Completed metric gene tree]('
	result += last_image + ')\n\n@caption\n\nReview the Completed Tree\n\n'
	result += '=== layout: one-panel\n\n# Review the Branch Lengths\n\n@body\n\n'
	result += '| Node | Height | Branches to Children |\n| --- | --- | --- |\n'
	for step in history:
		left, right = step['left'], step['right']
		node = f'[{step["merged"]}]{{color={cluster_colors[step["merged"]]}}}' \
			if cluster_colors else step['merged']
		result += f'| {node} | [{number(step["height"])}]{{text-align=center}} | '
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
		('six_gene_worksheet', 'six'), ('six_gene_extension', 'six_extension')]:
		generate(name, data[name], stem)


if __name__ == '__main__':
	main()
