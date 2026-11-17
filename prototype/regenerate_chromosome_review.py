#!/usr/bin/env python3
"""Regenerate the chromosome-review SVGs without touching lecture assets."""

import csv
import hashlib
import pathlib
import subprocess
import sys
import xml.etree.ElementTree as ET

import devel.render_genetics_lect01_chromosomes
import devel.render_genetics_lect02_chromosomes
import devel.render_genetics_lect03_chromosomes
import genetics.LECT06.djot.make_chromosome_xlinked
import genetics.LECT06.djot.chromosome_models.mixed.intro.recipe
import genetics.LECT06.djot.chromosome_models.mixed.recombination.recipe
import genetics.LECT13.djot.lect13d_p2_compositions

import build_chromosome_replacements
import generate_chromosome_review_assets


ROOT = pathlib.Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
ASSETS = ROOT / 'chromosome_assets'


def run(*arguments: str) -> None:
	"""Run one source-backed recipe with an explicit prototype destination."""
	subprocess.run((sys.executable, '-B', *arguments), cwd=REPOSITORY, check=True)


def refresh_inventory() -> None:
	"""Record the hashes produced by this prototype-only rebuild."""
	path = ROOT / 'chromosome_replacements.csv'
	with path.open(newline='') as handle:
		rows = list(csv.DictReader(handle))
	for row in rows:
		asset = REPOSITORY / row['replacement_asset']
		if not asset.is_file():
			raise ValueError(f'Missing prototype replacement: {asset}')
		row['replacement_sha256'] = hashlib.sha256(asset.read_bytes()).hexdigest()
	with path.open('w', newline='') as handle:
		writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
		writer.writeheader()
		writer.writerows(rows)


def separate_c58_prose() -> None:
	"""Keep the C58 explanation in its native Djot text block."""
	path = ASSETS / 'assets/lect13b-chromo_alter_3-inversion/pericentric-anaphase.drawn.svg'
	root = ET.parse(path).getroot()
	canvas = root.find('{http://www.w3.org/2000/svg}g')
	# The four explanation lines and their separator belong to the native text block.
	for node in list(canvas):
		if (node.tag == '{http://www.w3.org/2000/svg}text'
			and node.attrib['x'] == '36' and float(node.attrib['y']) >= 600):
			canvas.remove(node)
		elif node.get('d') == 'M 30,590 H 1420':
			canvas.remove(node)
	root.set('height', '590')
	root.set('viewBox', '0 0 1460 590')
	ET.ElementTree(root).write(path, encoding='ascii', xml_declaration=True)


def main() -> None:
	"""Rebuild the review corpus from source recipes in the prototype tree only."""
	# Recipes without command-line output roots expose a narrow build function.
	devel.render_genetics_lect01_chromosomes.main(ASSETS)
	devel.render_genetics_lect02_chromosomes.main(ASSETS)
	devel.render_genetics_lect03_chromosomes.main(ASSETS)
	genetics.LECT06.djot.chromosome_models.mixed.intro.recipe.build(ROOT / 'assets/lect06b-intro_cells')
	genetics.LECT06.djot.chromosome_models.mixed.recombination.recipe.build(ROOT / 'assets/lect06c-meiosis')
	genetics.LECT06.djot.make_chromosome_xlinked.generate(REPOSITORY / 'genetics/LECT06/djot/chromosome_models/xlinked',
		REPOSITORY, ROOT)

	# Scripts below all receive a prototype path rather than their course default.
	run('genetics/LECT06/djot/make_chromosome_mitosis_panel.py', '--output-root', str(ROOT / 'assets'))
	run('genetics/LECT06/djot/make_chromosome_mitosis.py', '--output-root', str(ROOT / 'assets'))
	run('genetics/LECT06/djot/make_chromosome_early_meiosis.py', '--output-root', str(ROOT / 'assets'))
	run('genetics/LECT06/djot/make_chromosome_meiosis_panel.py', '--output-root', str(ROOT / 'assets'))
	run('genetics/LECT06/djot/make_chromosome_assortment.py', '--output-root', str(ROOT / 'assets'))
	run('devel/render_human_chromosome_2_fusion.py',
		str(ASSETS / 'assets/lect02c-genome_sizes/chromosome_2_fusion.drawn.svg'))
	run('genetics/LECT04/djot/assets/lect04e-segregation/make_fertilization_scene.py',
		str(ASSETS / 'assets/lect04e-segregation/fertilization_scene.drawn.svg'))
	for recipe in ('cis_recipe.py', 'crossover_recipe.py', 'double_recipe.py', 'exchanges_recipe.py', 'b31_recipe.py'):
		run('genetics/LECT08/djot/chromosome_recipes/' + recipe, '-o', str(ROOT / 'assets'))
	run('genetics/LECT09/djot/make_mitotic_yeast.py', '--output-root', str(ROOT / 'assets'))
	run('genetics/LECT09/djot/make_history_scenes.py', '--output-root', str(ROOT / 'assets'))
	run('genetics/LECT09/djot/make_centromere.py', '--output-root', str(ROOT / 'assets'))
	run('genetics/LECT10/djot/regenerate_lect10b.py', '--output-root', str(ASSETS))
	run('genetics/LECT10/djot/lect10_count_recipe.py', str(ASSETS))

	generate_chromosome_review_assets.main()
	build_chromosome_replacements.main()

	# LECT13 has one output-root convention: the supplied directory owns assets/.
	run('genetics/LECT13/djot/lect13b_loop_chromosome_recipes.py', '--output-root', str(ASSETS))
	run('genetics/LECT13/djot/lect13bc_chromosome_recipes.py', '--output-root', str(ASSETS))
	run('genetics/LECT13/djot/lect13d_chromosome_recipes.py', '--output-root', str(ASSETS))
	run('genetics/LECT13/djot/lect13d_p1_composition_recipes.py', '--output',
		str(ASSETS / 'assets/lect13d-meiosis_translocation'), '--components-dir',
		str(ASSETS / 'assets/lect13d-meiosis_translocation'))

	# The remaining p2 compositions currently provide a function rather than an output option.
	genetics.LECT13.djot.lect13d_p2_compositions.render(ASSETS / 'assets/lect13d-meiosis_translocation')
	separate_c58_prose()
	refresh_inventory()


if __name__ == '__main__':
	main()
