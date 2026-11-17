"""Check local part geometry and renderer adapters."""

import math
import pytest

import svg_tools.parts


#============================================
def test_part_validates_geometry() -> None:
	part = svg_tools.parts.SvgPart('<circle/>', (-1, -1, 1, 1), {'center': (0, 0)})
	assert part.anchors['center'] == (0, 0)
	with pytest.raises(ValueError):
		svg_tools.parts.SvgPart('', (0, 0, math.inf, 1), {})
	with pytest.raises(ValueError):
		svg_tools.parts.SvgPart('', (0, 0, 1, 1), {'bad': (math.nan, 0)})


#============================================
def test_text_bounds_include_measured_oversized_label() -> None:
	fragment = ("<g><text x='5' y='5' font-size='20' text-anchor='middle' "
		"font-weight='600'>WIDE</text></g>")
	bounds = svg_tools.parts.include_text_bounds(fragment, (0, 0, 10, 10))
	assert bounds[0] < 0 and bounds[2] > 10
	assert bounds[1] < 0


#============================================
def test_text_bounds_allow_for_scientific_fallback_glyphs(monkeypatch) -> None:
	label = '&alpha;′漢'
	fragment = f"<g><text x='0' y='0' font-size='20'>{label}</text></g>"
	bounds = svg_tools.parts.include_text_bounds(fragment, (0, 0, 0, 0))
	monkeypatch.setattr(svg_tools.parts, '_font_characters', lambda path: set(map(ord, label)))
	measured = svg_tools.parts.include_text_bounds(fragment, (0, 0, 0, 0))
	assert label in fragment
	assert all(math.isfinite(value) for value in bounds)
	assert bounds[0] <= measured[0] - 60 and bounds[2] >= measured[2] + 60
	assert bounds[1] <= measured[1] - 20 and bounds[3] >= measured[3] + 20


