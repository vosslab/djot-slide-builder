#!/usr/bin/env python3
"""Build the LECT12 chromosome-review replacements without changing course assets."""

import pathlib
import shutil
import subprocess

from genetics.LECT12.djot import lect12c_chromosome_recipes
from genetics.LECT12.djot import make_polyploidy_chromosomes
from genetics.LECT12.djot import lect12d_chromosome_recipes
from genetics.LECT12.djot import lect12e_chromosome_recipes


ROOT = pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip()) / 'prototype'
LECT12 = ROOT.parent / 'genetics' / 'LECT12' / 'djot'
ASSETS = ROOT / 'chromosome_assets' / 'assets'


def copy_sex_dosage_sources() -> None:
	"""Use duplicate source shells because their labels are part of the reviewed figure."""
	for name in ('x_inactivation_lineages.drawn.svg', 'calico_x_lineages.drawn.svg',
			'pseudoautosomal_crossover.drawn.svg'):
		target = ASSETS / 'visual_renewal' / name
		target.parent.mkdir(parents=True, exist_ok=True)
		shutil.copy2(LECT12 / 'assets' / 'visual_renewal' / name, target)


def main() -> None:
	for relative in ('visual_renewal', 'lect12b-polyploidy'):
		(ASSETS / relative).mkdir(parents=True, exist_ok=True)
	make_polyploidy_chromosomes.BASE = ROOT / 'chromosome_assets'
	make_polyploidy_chromosomes.main(exclude=(
		'assets/visual_renewal/chrysanthemum_18.drawn.svg',
		'assets/visual_renewal/chrysanthemum_36_54.drawn.svg',
		'assets/visual_renewal/chrysanthemum_54_72.drawn.svg',
		'assets/visual_renewal/chrysanthemum_72_90.drawn.svg',
		'assets/visual_renewal/chrysanthemum_monoploid.drawn.svg',
	))
	make_polyploidy_chromosomes.make_raster_replacements()

	copy_sex_dosage_sources()
	lect12c_chromosome_recipes.ROOT = ASSETS
	for name in ('x_inactivation_lineages', 'calico_x_lineages', 'pseudoautosomal_crossover'):
		lect12c_chromosome_recipes.refresh(ASSETS / 'visual_renewal' / f'{name}.drawn.svg')

	lect12d_chromosome_recipes.ASSETS = ASSETS / 'lect12d-chromo_alter_1-deletions'
	lect12d_chromosome_recipes.ASSETS.mkdir(parents=True, exist_ok=True)
	for name in ('image_006.png', 'image_015.png'):
		shutil.copy2(LECT12 / 'assets' / 'lect12d-chromo_alter_1-deletions' / name,
			lect12d_chromosome_recipes.ASSETS / name)
	lect12d_chromosome_recipes.main()

	lect12e_chromosome_recipes.ASSETS = ASSETS / 'lect12e-chromo_alter_2-duplications'
	lect12e_chromosome_recipes.ASSETS.mkdir(parents=True, exist_ok=True)
	lect12e_chromosome_recipes.main()


if __name__ == '__main__':
	main()
