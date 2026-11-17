"""Regenerate the LECT10 source's labeled rod and joined-sister comparison."""
import pathlib

import svg_tools.chromosomes
import svg_tools.drawing


def main(destination: pathlib.Path) -> None:
	# Source: image_027.png, approximately equal upper and lower arms.
	model = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('', '#111111', 1), svg_tools.chromosomes.Segment('', '#111111', 1)),
		(svg_tools.chromosomes.Centromere(1),))
	rod = svg_tools.chromosomes.chromosome_path_part('haploid', model,
		'M 20 31 Q 34 48 34 78 Q 32 103 20 128', thickness=17, labels=False)
	sisters = svg_tools.chromosomes.render_chromosome_layout('diploid', model, length=112, thickness=17,
		orientation='vertical', texture=False, sisters=True, labels=False)
	body = ''
	body += rod.fragment
	body += f'<g transform="translate(92 24)">{sisters.svg}</g>'
	body += svg_tools.drawing.text(9, 157, 'haploid', size=11, color='#111111', anchor='start')
	body += svg_tools.drawing.text(9, 171, 'chromosome', size=11, color='#111111', anchor='start')
	body += svg_tools.drawing.text(103, 157, 'diploid', size=11, color='#111111', anchor='start')
	body += svg_tools.drawing.text(103, 171, 'chromosome', size=11, color='#111111', anchor='start')
	svg_tools.drawing.write_svg(destination, 182, 179, 'Chromosome forms',
		'The original labels accompany one chromatid and a joined pair of sister chromatids.', body)
