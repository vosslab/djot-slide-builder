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


