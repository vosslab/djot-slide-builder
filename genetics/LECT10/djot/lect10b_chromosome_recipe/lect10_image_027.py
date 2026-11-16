"""Regenerate the LECT10 source's labeled rod and joined-sister comparison."""
import pathlib

import svg_tools.chromosomes


def main(destination: pathlib.Path) -> None:
	# Source: image_027.png, approximately equal upper and lower arms.
	model = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment('', '#111111', 1), svg_tools.chromosomes.Segment('', '#111111', 1)), 1)
	rod = svg_tools.chromosomes.chromosome_path_part('haploid', model,
		'M 20 31 Q 34 48 34 78 Q 32 103 20 128', thickness=17, labels=False)
	sisters = svg_tools.chromosomes.render_chromosome_layout('diploid', model, length=112, thickness=68,
		orientation='vertical', bands=False, sisters=True, labels=False)
	svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="182" height="179" viewBox="0 0 182 179" role="img" aria-labelledby="title desc">
<title id="title">Chromosome forms</title>
<desc id="desc">The original labels accompany one chromatid and a joined pair of sister chromatids.</desc>
<rect width="182" height="179" fill="#ffffff"/>
{rod.fragment}
<g transform="translate(92 24)">{sisters.svg}</g>
<g font-family="Atkinson Hyperlegible Next" font-size="11" fill="#111111">
<text x="9" y="157">haploid</text><text x="9" y="171">chromosome</text>
<text x="103" y="157">diploid</text><text x="103" y="171">chromosome</text>
</g></svg>'''
	pathlib.Path(destination).write_text(svg, encoding='utf-8')
