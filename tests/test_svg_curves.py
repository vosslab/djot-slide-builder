"""Protect distance and orientation contracts used by curved illustrations."""

import math

import pytest

import svg_tools.curves


def test_straight_spacing_and_endpoint() -> None:
	samples = svg_tools.curves.sample_curve("M 0 0 L 10 0", spacing=2)
	for sample, x in zip(samples, range(0, 11, 2), strict=True):
		assert sample == pytest.approx((x, 0, 0))
	assert len(svg_tools.curves.sample_curve("M 0 0 L 10 0", spacing=3)) == 4


def test_curve_tangents_and_distance() -> None:
	samples = svg_tools.curves.sample_curve("M 0 0 C 0 10 10 10 10 0", spacing=5)
	assert len(samples) == 5
	assert samples[0] == pytest.approx((0, 0, 90))
	assert samples[-1] == pytest.approx((10, 0, -90))
	assert samples[2] == pytest.approx((5, 7.5, 0))


@pytest.mark.parametrize("spacing", [0, -1, math.inf, math.nan])
def test_invalid_spacing(spacing: float) -> None:
	with pytest.raises(ValueError, match="Spacing"):
		svg_tools.curves.sample_curve("M 0 0 L 10 0", spacing=spacing)


def test_zero_length_path() -> None:
	with pytest.raises(ValueError, match="Path length"):
		svg_tools.curves.sample_curve("M 0 0 L 0 0", spacing=1)
