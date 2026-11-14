#!/usr/bin/env python3
"""Draw an authored operon and genomic and joined exon tracks."""

import pathlib

import svg_tools.chromosomes
import svg_tools.drawing
import svg_tools.gene_tracks
import svg_tools.parts
import svg_tools.text


#============================================
def main() -> None:
	features = {
		'promoter': (svg_tools.gene_tracks.landmark_part('promoter', 'Promoter', direction='forward'), 20),
		'operator': (svg_tools.gene_tracks.landmark_part('operator', 'Operator', direction='forward'), 100),
		'gene_a': (svg_tools.gene_tracks.gene_feature_part('Gene A', 110, 'forward', color='#a9d5df'), 165),
		'gene_b': (svg_tools.gene_tracks.gene_feature_part('Gene B', 110, 'forward', color='#b8d8b3'), 290),
		'gene_c': (svg_tools.gene_tracks.gene_feature_part('Gene C', 110, 'forward', color='#f2d28d'), 415),
		'terminator': (svg_tools.gene_tracks.landmark_part('terminator', 'Terminator', direction='forward'), 550),
	}
	exons = [svg_tools.chromosomes.Segment('Exon 1', '#a9d5df', 90), svg_tools.chromosomes.Segment('Exon 2', '#b8d8b3', 120),
		svg_tools.chromosomes.Segment('Exon 3', '#f2d28d', 75)]
	items = {
		'operon': svg_tools.parts.transform(svg_tools.gene_tracks.operon_part(features, length=610), x=30, y=70),
		'reverse': svg_tools.parts.transform(svg_tools.gene_tracks.gene_feature_part('Reverse gene', 140, 'reverse', color='#dbbfdf'), x=250, y=140),
		'genomic_label': svg_tools.text.label(30, 252, 'Genomic', size=16, color='#344651', anchor='start'),
		'genomic': svg_tools.parts.transform(svg_tools.gene_tracks.gene_track_part('genomic', exons, [60, 90], height=34), x=180, y=230),
		'joined_label': svg_tools.text.label(30, 332, 'Joined transcript', size=16, color='#344651', anchor='start'),
		'joined': svg_tools.parts.transform(svg_tools.gene_tracks.gene_track_part('joined', exons, [0, 0], height=34), x=180, y=310),
	}
	output = pathlib.Path('_temp/gene_features.svg')
	output.parent.mkdir(exist_ok=True)
	svg_tools.drawing.write_svg(output, 680, 380, 'Authored gene features',
		'An operon with three forward genes, a reverse gene, and genomic and joined exon tracks.',
		svg_tools.parts.group(items).fragment)
	print(output)


if __name__ == '__main__':
	main()
