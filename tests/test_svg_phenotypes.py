"""Schematic phenotype parts preserve shapes, counts, and placement."""

import xml.etree.ElementTree as ET

import pytest

from svg_tools import phenotypes
from svg_tools.examples import phenotypes as example


def test_seed_shapes_are_deterministic_and_color_independent():
	round_seed = phenotypes.seed(size=100, color='#edc743', shape='round')
	wrinkled = phenotypes.seed(size=100, color='#edc743', shape='wrinkled')
	green = phenotypes.seed(size=100, color='#72a967', shape='wrinkled')
	assert wrinkled == phenotypes.seed(size=100, color='#edc743', shape='wrinkled')
	assert ET.fromstring(round_seed.fragment).find('path').get('d') != ET.fromstring(wrinkled.fragment).find('path').get('d')
	assert wrinkled.fragment.replace('#edc743', '#72a967') == green.fragment
	assert wrinkled.bounds[0] < 0 < wrinkled.bounds[2]
	assert wrinkled.bounds[1] < 0 < wrinkled.bounds[3]
	assert wrinkled.anchors['center'] == (0, 0)
	with pytest.raises(ValueError):
		phenotypes.seed(size=0, color='green')
	with pytest.raises(ValueError):
		phenotypes.seed(size=100, color='green', shape='unknown')


def test_flower_count_and_population_positions():
	flower = phenotypes.flower(size=100, color='pink', petals=7)
	assert len(ET.fromstring(flower.fragment).findall('ellipse')) == 7
	assert flower.bounds[0] < 0 < flower.bounds[2]
	assert flower.bounds[1] < 0 < flower.bounds[3]
	assert flower.anchors['top'] == (0, -50)
	with pytest.raises(ValueError):
		phenotypes.flower(size=100, color='pink', petals=2)
	population = example.population()
	centers = [point for name, point in population.anchors.items() if name.endswith('.center')]
	assert len(centers) == len(set(centers)) == 6
	assert len({y for x, y in centers}) == 2
	assert len(ET.fromstring(population.fragment).findall('.//ellipse')) == 30
