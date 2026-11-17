#!/usr/bin/env python3
"""Generate prototype-only chromosome review assets from shared geometry."""

import pathlib
import subprocess

import svg_tools.chromosomes as chromosomes


ROOT = pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip()) / 'prototype'


def staining() -> None:
	"""Keep the three source staining comparisons while using the shared bodies."""
	purple, gold = '#867196', '#E6CF91'
	# Fixed schematic intervals share C36's palette, not a measured cytoband map.
	lengths = (18, 7, 25, 12, 16, 9, 20, 8, 26, 27, 11, 21, 6, 19, 30)
	patterns = {
		'G-Bands': tuple(purple if index % 2 else gold for index in range(len(lengths))),
		'R-Bands': tuple(gold if index % 2 else purple for index in range(len(lengths))),
		'C-Bands': tuple(purple if index in (8, 9) else gold for index in range(len(lengths))),
	}
	fragments = []
	for column, (label, colors) in enumerate(patterns.items()):
		model = chromosomes.Chromosome(tuple(chromosomes.Segment('', color, length)
			for color, length in zip(colors, lengths)), (chromosomes.Centromere(9),))
		part = chromosomes.sister_chromatid_parts(f'band-{column}',
			((model, 'M 0 0 L 0 254'), (model, 'M 34 0 L 34 254')),
			thickness=24, labels=False, texture=False)
		fragments.append(f'<g transform="translate({88 + column * 165} 36)">{part.fragment}</g>')
	svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="452" height="328" viewBox="56 23 452 328" role="img" aria-labelledby="title desc">
<title id="title">Chromosome banding comparison</title>
<desc id="desc">Three replicated chromosomes compare schematic G-bands, their reverse R-bands, and pericentromeric C-bands. Sisters share irregular band widths. Purple and pale yellow indicate staining contrast; colors and widths are illustrative, not a measured chromosome map or literal stain colors.</desc>
''' + ''.join(fragments) + '''<g fill="#141414" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="25">''' + ''.join(
	f'<text x="{117 + index * 165}" y="338" text-anchor="middle">{label}</text>'
	for index, label in enumerate(patterns)) + '</g></svg>'
	destination = ROOT / 'chromosome_assets/assets/lect10b-karyotypes/chromosome_staining_comparison.drawn.svg'
	destination.parent.mkdir(parents=True, exist_ok=True)
	destination.write_text(svg, encoding='utf-8')


def main() -> None:
	staining()


if __name__ == '__main__':
	main()
