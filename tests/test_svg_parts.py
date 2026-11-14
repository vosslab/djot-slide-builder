"""Check local part geometry and renderer adapters."""

import math
import pytest

import svg_tools.parts
import svg_tools.chromosomes
import svg_tools.gene_tracks


def test_part_validates_geometry() -> None:
	part = svg_tools.parts.SvgPart('<circle/>', (-1, -1, 1, 1), {'center': (0, 0)})
	assert part.anchors['center'] == (0, 0)
	with pytest.raises(ValueError):
		svg_tools.parts.SvgPart('', (0, 0, math.inf, 1), {})
	with pytest.raises(ValueError):
		svg_tools.parts.SvgPart('', (0, 0, 1, 1), {'bad': (math.nan, 0)})


def test_renderer_parts_preserve_fragments_and_bound_paint() -> None:
	segment = svg_tools.chromosomes.Segment('long label', '#FFFFFF', 40)
	model = svg_tools.chromosomes.Chromosome((segment, segment), 1)
	layout = svg_tools.chromosomes.render_chromosome_layout('chrom', model,
		orientation='vertical', marker_label='C')
	part = svg_tools.chromosomes.chromosome_part('chrom', model,
		orientation='vertical', marker_label='C')
	assert part.fragment == layout.svg
	assert part.anchors['centromere'] == layout.centromere
	assert part.anchors['boundary_1'] == layout.boundaries[1]
	assert part.bounds[0] < 0 and part.bounds[1] < 0
	assert part.bounds[2] > layout.width and part.bounds[3] > layout.height
	track = svg_tools.gene_tracks.gene_track_part('gene', [segment, segment], [10], height=50)
	fragment, width, boundaries = svg_tools.gene_tracks.gene_track_svg(
		'gene', [segment, segment], [10], height=50)
	assert track.fragment == fragment
	assert track.anchors['boundary_1'] == (boundaries[1], 25)
	assert track.bounds[0] < 0 and track.bounds[2] > width


def test_text_bounds_include_measured_oversized_label() -> None:
	fragment = ("<g><text x='5' y='5' font-size='20' text-anchor='middle' "
		"font-weight='600'>WIDE</text></g>")
	bounds = svg_tools.parts.include_text_bounds(fragment, (0, 0, 10, 10))
	assert bounds[0] < 0 and bounds[2] > 10
	assert bounds[1] < 0


def test_text_bounds_allow_for_scientific_fallback_glyphs(monkeypatch) -> None:
	label = 'α′漢'
	fragment = f"<g><text x='0' y='0' font-size='20'>{label}</text></g>"
	bounds = svg_tools.parts.include_text_bounds(fragment, (0, 0, 0, 0))
	monkeypatch.setattr(svg_tools.parts, '_font_characters', lambda path: set(map(ord, label)))
	measured = svg_tools.parts.include_text_bounds(fragment, (0, 0, 0, 0))
	assert label in fragment
	assert all(math.isfinite(value) for value in bounds)
	assert bounds[0] <= measured[0] - 60 and bounds[2] >= measured[2] + 60
	assert bounds[1] <= measured[1] - 20 and bounds[3] >= measured[3] + 20


def test_gene_track_part_bounds_large_text() -> None:
	segment = svg_tools.chromosomes.Segment('A', '#FFFFFF', 1000)
	part = svg_tools.gene_tracks.gene_track_part('gene', [segment], [], height=1000)
	fragment, width, _ = svg_tools.gene_tracks.gene_track_svg('gene', [segment], [], height=1000)
	assert part.fragment == fragment
	assert all(math.isfinite(value) for value in part.bounds)
	assert part.bounds[0] < 0 and part.bounds[2] > width
	assert part.bounds[1] < 0 and part.bounds[3] > 1000
