#!/usr/bin/env python3
"""Show insertional and reciprocal translocations with shared BPQ chromosomes.

Gene blocks are schematic; their widths and identities stay constant during transfer.
"""

import pathlib

import svg_tools.chromosomes as chromosomes
import svg_tools.drawing as drawing
import svg_tools.parts as parts


ASSET = pathlib.Path('genetics/LECT01/djot/assets/lect01b-genetic_disorders/chromosome_transfer_comparison.drawn.svg')
INK = '#243746'
PARENTS = (
	chromosomes.Chromosome(tuple(chromosomes.Segment(letter, '#22BFD0', 52)
		for letter in 'ABCDEFGH'), (chromosomes.Centromere(2),)),
	chromosomes.Chromosome(tuple(chromosomes.Segment(letter, '#35B94B', 52)
		for letter in 'JKLMNO'), (chromosomes.Centromere(2),)),
)


#============================================
def panel(name: str, title: str, explanation: str, products: tuple) -> str:
	"""Compare the same two parental chromosomes with their transfer products."""
	body = '<rect x="8" y="8" width="1224" height="328" rx="16" fill="#F7FBFD" stroke="#D8E5EA" stroke-width="2"/>'
	body += drawing.text(32, 45, title, size=30, color=INK, anchor='start')
	body += drawing.text(318, 86, 'Before', size=25, color=INK)
	body += drawing.text(998, 86, 'After', size=25, color=INK)
	for state, models, x in (('before', PARENTS, 110), ('after', products, 790)):
		for index, model in enumerate(models):
			y = 112 + index*100
			body += drawing.text(x-20, y+27, f'Chr {index+1}', size=21,
				color=INK, anchor='end')
			part = chromosomes.chromosome_part(f'{name}-{state}-{index}', model,
				thickness=40, labels=True)
			body += parts.transform(part, x=x, y=y).fragment
	body += '<path d="M 572 182 H 696" fill="none" stroke="#243746" stroke-width="5" marker-end="url(#process-head)"/>'
	body += drawing.text(32, 308, explanation, size=25, color=INK, anchor='start')
	return body


#============================================
def main(output_root: pathlib.Path) -> None:
	"""Render the two source mechanisms with visible gene order and chromosome origin."""
	donor, recipient = PARENTS
	insertion = (
		chromosomes.delete_segments(donor, 4, 6),
		chromosomes.Chromosome(recipient.segments[:3] + donor.segments[4:6]
			+ recipient.segments[3:], recipient.centromeres),
	)
	reciprocal = chromosomes.reciprocal_translocation(donor, 6, recipient, 4)
	body = ('<defs><marker id="process-head" markerUnits="userSpaceOnUse" '
		'markerWidth="16" markerHeight="16" refX="14" refY="8" orient="auto">'
		'<path d="M 0 0 L 16 8 L 0 16 Z" fill="#243746"/></marker></defs>'
		'<rect width="1240" height="690" fill="#FFFFFF"/>')
	body += '<g id="insertion">' + panel('insertion', 'Insertional translocation',
		'An internal segment (E-F) moves to another chromosome.', insertion) + '</g>'
	body += '<g id="reciprocal" transform="translate(0 346)">' + panel('reciprocal',
		'Reciprocal translocation', 'Chromosome ends (G-H and N-O) exchange places.', reciprocal) + '</g>'
	path = output_root / ASSET
	path.parent.mkdir(parents=True, exist_ok=True)
	drawing.write_svg(path, 1240, 690, 'Two chromosome translocation mechanisms',
		'Before and after an insertional translocation: ABCDEFGH and JKLMNO become '
		'ABCDGH and JKLEFMNO. Before and after a reciprocal translocation: the same '
		'parents become ABCDEFNO and JKLMGH. Blue and green identify the two chromosome '
		'origins. Each gene block keeps its length; both examples retain every block '
		'and one centromere on each chromosome. Schematic, not genomic scale.', body)


if __name__ == '__main__':
	import sys
	main(pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('.'))
