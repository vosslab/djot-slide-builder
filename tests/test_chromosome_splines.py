"""Shared spline geometry preserves material length, tangents and ribbon width."""

import pytest
import svgpathtools

import svg_tools.chromosome_surface


#============================================
def test_two_points_define_a_straight_centerline() -> None:
	path = svg_tools.chromosome_surface.centerline([(20, 30), (23, 34)],
		length=50, width=12)
	assert isinstance(path[0], svgpathtools.Line)
	assert path.start == 20+30j
	assert path.end == pytest.approx(50+70j)
	assert path.length() == pytest.approx(50)


#============================================
@pytest.mark.parametrize('points,length,width', [
	([(10, 20), (50, 60), (110, 5), (190, 50)], 260, 8),
	([(20, 10), (90, 10), (160, 50)], 170, 18),
])
def test_bends_interpolate_shape_with_continuous_tangents(
	points: list[tuple[int, int]], length: int, width: int) -> None:
	geometry = svg_tools.chromosome_surface
	path = geometry.centerline(points, length=length, width=width)
	assert path.length() == pytest.approx(length)
	anchor = complex(*points[0])
	assert path.start == anchor
	scale = (path.end-anchor) / (complex(*points[-1])-anchor)
	assert scale.real > 0 and scale.imag == pytest.approx(0)
	for segment, point in zip(path, points[1:]):
		assert segment.end == pytest.approx(anchor + scale.real*(complex(*point)-anchor))
	for first, second in zip(path, path[1:]):
		assert first.end == second.start
		assert first.unit_tangent(1) == pytest.approx(second.unit_tangent(0))
	surface = geometry.Surface(path, width)
	for fraction in (0, .2, .5, .8, 1):
		along = surface.length * fraction
		negative = surface.point(along, -width/2)
		positive = surface.point(along, width/2)
		assert abs(positive-negative) == pytest.approx(width)


#============================================
@pytest.mark.parametrize('points,length,width,error', [
	([(0, 0)], 50, 6, 'at least two'),
	([(0, 0), (float('nan'), 1)], 50, 6, 'finite'),
	([(0, 0), (0, 0)], 50, 6, 'distinct'),
	([(0, 0), (100, 0), (100, 100), (0, 100), (0, 0)], 400, 8, 'open'),
	([(0, 0), (20, 0), (10, 0)], 50, 6, 'reversing'),
	# The close middle knots put the tightest part of the bend inside a span.
	([(0, 0), (100, 14), (101, 13), (271, -60)], 200, 1, 'fold'),
	([(0, 0), (20, 0)], 0, 6, 'length'),
	([(0, 0), (20, 0)], 50, float('inf'), 'width'),
])
def test_bad_centerlines_are_rejected(
	points: list[tuple[float, float]], length: float, width: float, error: str) -> None:
	with pytest.raises(ValueError, match=error):
		svg_tools.chromosome_surface.centerline(points, length=length, width=width)


#============================================
@pytest.mark.parametrize('terminal_ends', [(True, False), (False, True)])
def test_envelope_rounds_only_the_native_end(terminal_ends: tuple[bool, bool]) -> None:
	geometry = svg_tools.chromosome_surface
	path = geometry.centerline([(0, 0), (100, 0)], length=100, width=30)
	surface = geometry.Surface(path, 30)
	outline = svgpathtools.parse_path(surface.envelope(terminal_ends=terminal_ends))
	vertices = {segment.start for segment in outline}
	assert outline.isclosed()
	for end, rounded in zip((0, 100), terminal_ends):
		if rounded:
			assert {end-9j, end+9j} <= vertices
			assert not {end-15j, end+15j} & vertices
		else:
			assert {end-15j, end+15j} <= vertices
