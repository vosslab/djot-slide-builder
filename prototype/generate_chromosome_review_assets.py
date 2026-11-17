#!/usr/bin/env python3
"""Generate prototype-only chromosome review assets from shared geometry."""

import pathlib

import svg_tools.chromosomes as chromosomes


ROOT = pathlib.Path(__file__).resolve().parent


def staining() -> None:
	"""Keep the three source staining comparisons while using the shared bodies."""
	patterns = {
		'G-Bands': ('#F8F8F8', '#161616', '#F8F8F8', '#161616', '#F8F8F8',
			'#161616', '#F8F8F8', '#161616', '#F8F8F8'),
		'R-Bands': ('#161616', '#F8F8F8', '#161616', '#F8F8F8', '#161616',
			'#F8F8F8', '#161616', '#F8F8F8', '#161616'),
		'C-Bands': ('#F8F8F8', '#F8F8F8', '#F8F8F8', '#F8F8F8', '#161616',
			'#161616', '#F8F8F8', '#F8F8F8', '#F8F8F8'),
	}
	fragments = []
	for column, (label, colors) in enumerate(patterns.items()):
		model = chromosomes.Chromosome(tuple(chromosomes.Segment('', color, 1)
			for color in colors), (chromosomes.Centromere(5),))
		part = chromosomes.sister_chromatid_parts(f'band-{column}',
			((model, 'M 0 0 L 0 254'), (model, 'M 34 0 L 34 254')),
			thickness=24, labels=False, bands=False)
		fragments.append(f'<g transform="translate({88 + column * 165} 36)">{part.fragment}</g>')
	svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="522" height="369" viewBox="0 0 522 369" role="img" aria-labelledby="title desc">
<title id="title">Chromosome banding comparison</title>
<desc id="desc">Three chromosome pairs compare G-bands, reverse R-bands, and central C-bands.</desc>
<rect width="522" height="369" fill="#ffffff"/>
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
