"""Checks for normalized schematic path scaling and uniform outlines."""

import svgpathtools

import svg_tools._style


def test_scaled_path_preserves_subpaths_and_closure():
	path = 'M 0 0 C .5 0 1 .5 1 1 C .5 1 0 .5 0 0 Z M .2 .2 H .4 V .4 Z'
	result = svg_tools._style.scaled_path(path, 200, 50)
	assert result.count('Z') == 2
	scaled = svgpathtools.parse_path(result)
	assert scaled.bbox() == (0, 200, 0, 50)
	assert len(scaled.continuous_subpaths()) == 2
	assert isinstance(scaled[1], svgpathtools.CubicBezier)


def test_outline_uses_final_coordinate_space():
	wide = svg_tools._style.outline(200, 50)
	tall = svg_tools._style.outline(50, 200)
	assert wide == tall
	assert wide['stroke-width'] == '1.0'
	assert wide['stroke-linejoin'] == 'round'
	assert svg_tools._style.outline(500, 340)['stroke-width'] == '3.0'
