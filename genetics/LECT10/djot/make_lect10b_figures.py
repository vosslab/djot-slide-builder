#!/usr/bin/env python3
"""Regenerate the LECT10B chromosome figures from adjacent models and templates."""
import argparse
import pathlib
import subprocess
import sys

import lect10b_chromosome_recipe.centromere_positions_recipe
import lect10b_chromosome_recipe.chromosome_forms_recipe
import lect10b_chromosome_recipe.karyotype_preparation_recipe
import lect10b_chromosome_recipe.mitosis_stages_recipe
import lect10b_chromosome_recipe.chromosome_movement_recipe
import lect10b_chromosome_recipe.sky_probe_mixture_recipe


REPOSITORY = pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip())


def main(deck: pathlib.Path) -> None:
	"""Regenerate LECT10B figures under the requested deck directory."""
	folder = deck / 'assets' / 'lect10b-karyotypes'
	jobs = [
		(lect10b_chromosome_recipe.chromosome_forms_recipe.main, folder / 'image_027.normal.svg'),
		(lect10b_chromosome_recipe.sky_probe_mixture_recipe.main, folder / 'sky_probe_mixture_workflow.drawn.svg'),
		(lect10b_chromosome_recipe.centromere_positions_recipe.main, folder / 'centromere_positions.drawn.svg'),
		(lect10b_chromosome_recipe.mitosis_stages_recipe.main, folder / 'mitosis_karyotype_stages.drawn.svg'),
		(lect10b_chromosome_recipe.karyotype_preparation_recipe.main, deck / 'assets' / 'lect10_repaired_figures' / 'karyotype_preparation.svg'),
	]
	for make, destination in jobs:
		destination.parent.mkdir(parents=True, exist_ok=True)
		make(destination)
	for kind in ('metacentric', 'submetacentric', 'acrocentric'):
		lect10b_chromosome_recipe.chromosome_movement_recipe.main(kind, folder / (kind + '_movement.drawn.svg'))
	path = deck / 'assets' / 'visual_renewal' / 'human_chromosome_2_fusion.drawn.svg'
	path.parent.mkdir(parents=True, exist_ok=True)
	subprocess.run((sys.executable,
		str(REPOSITORY / 'genetics/LECT10/djot/human_chromosome_2_fusion_recipe.py'),
		str(path)), cwd=REPOSITORY, check=True)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--output-root', type=pathlib.Path,
		default=REPOSITORY / 'genetics/LECT10/djot',
		help='Deck directory for generated assets (default: LECT10/djot).')
	main(parser.parse_args().output_root)
