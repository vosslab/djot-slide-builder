#!/usr/bin/env python3
"""Build the LECT12 chromosome-review replacements without changing course assets."""

import pathlib
import shutil

from genetics.LECT12.djot import lect12c_chromosome_recipes
from genetics.LECT12.djot import make_polyploidy_chromosomes
from genetics.LECT12.djot import render_lect12d_chromosomes
from genetics.LECT12.djot import render_lect12e_chromosomes


ROOT = pathlib.Path(__file__).resolve().parent
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
	make_polyploidy_chromosomes.main()
	make_polyploidy_chromosomes.make_raster_replacements()

	copy_sex_dosage_sources()
	lect12c_chromosome_recipes.ROOT = ASSETS
	for name in ('x_inactivation_lineages', 'calico_x_lineages', 'pseudoautosomal_crossover'):
		lect12c_chromosome_recipes.refresh(ASSETS / 'visual_renewal' / f'{name}.drawn.svg')

	render_lect12d_chromosomes.ASSETS = ASSETS / 'lect12d-chromo_alter_1-deletions'
	render_lect12d_chromosomes.ASSETS.mkdir(parents=True, exist_ok=True)
	for name in ('image_006.png', 'image_015.png'):
		shutil.copy2(LECT12 / 'assets' / 'lect12d-chromo_alter_1-deletions' / name,
			render_lect12d_chromosomes.ASSETS / name)
	render_lect12d_chromosomes.main()
	shutil.copy2(LECT12 / 'assets' / 'lect12d-chromo_alter_1-deletions' /
		'cytological_deletion_intervals.drawn.svg',
		render_lect12d_chromosomes.ASSETS / 'cytological_deletion_intervals.drawn.svg')

	render_lect12e_chromosomes.ASSETS = ASSETS / 'lect12e-chromo_alter_2-duplications'
	render_lect12e_chromosomes.ASSETS.mkdir(parents=True, exist_ok=True)
	render_lect12e_chromosomes.main()


if __name__ == '__main__':
	main()
