#!/usr/bin/env python3
"""Draw the two yeast mating stages as editable SVGs."""

import argparse
import pathlib

import svg_tools.cells
import svg_tools.drawing
import svg_tools.parts
import svg_tools.text


ASSETS = pathlib.Path('genetics/LECT09/djot/assets/lect09d-yeast_unordered_tetrads')


#============================================
def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--output-dir', type=pathlib.Path, default=ASSETS)
	args = parser.parse_args()
	args.output_dir.mkdir(parents=True, exist_ok=True)
	move = svg_tools.parts.transform
	label = svg_tools.text.label
	for name, stage, caption, nuclei, title, description in (
		('yeast_mating', '2', 'Mating', ((450, 'a', '#EDF3FC', '#345B91'),
			(750, '\u03b1', '#FAEEF5', '#A43F77')), 'Haploid yeast cells mate',
			'One connected cell envelope encloses two separate haploid nuclei, a and alpha, before nuclear fusion.'),
		('yeast_diploid', '3', 'New a/\u03b1 cell', ((600, 'a/\u03b1', '#F1EDF7', '#6B478C'),),
			'Mating produces a diploid cell',
			'One connected cell envelope encloses one fused diploid a/alpha nucleus.'),
	):
		items = [move(svg_tools.cells.cell_envelope(kind='fused_yeast', width=640, height=335,
			color='#F7E4B2'), x=600, y=210)]
		for x, genotype, fill, color in nuclei:
			items.append(move(svg_tools.cells.nucleus(width=130 if len(nuclei) == 1 else 110,
				height=115 if len(nuclei) == 1 else 100, color=fill), x=x, y=210))
			items.append(label(x, 224, genotype, size=46, color=color))
		items.append(label(600, 430, caption, size=34, color='#213547'))
		items.append(label(42, 48, stage, size=23, color='#FFFFFF'))
		body = '<circle cx="42" cy="40" r="19" fill="#345B91" />' + ''.join(item.fragment for item in items)
		svg_tools.drawing.write_svg(args.output_dir / f'{name}_toolkit.drawn.svg', 1200, 470,
			title, description + ' Schematic, not to scale.', body)


if __name__ == '__main__':
	main()
