#!/usr/bin/env python3
"""Regenerate the LECT10B chromosome figures from adjacent models and templates."""
import argparse
import pathlib

import devel.render_human_chromosome_2_fusion
import lect10b_chromosome_recipe.lect10_centromere_positions
import lect10b_chromosome_recipe.lect10_image_027
import lect10b_chromosome_recipe.lect10_karyotype
import lect10b_chromosome_recipe.lect10_mitosis
import lect10b_chromosome_recipe.lect10_movement
import lect10b_chromosome_recipe.lect10_sky


def main(deck: pathlib.Path) -> None:
	folder = deck / 'assets' / 'lect10b-karyotypes'
	jobs = [
		(lect10b_chromosome_recipe.lect10_image_027.main, folder / 'image_027.normal.svg'),
		(lect10b_chromosome_recipe.lect10_sky.main, folder / 'sky_probe_mixture_workflow.drawn.svg'),
		(lect10b_chromosome_recipe.lect10_centromere_positions.main, folder / 'centromere_positions.drawn.svg'),
		(lect10b_chromosome_recipe.lect10_mitosis.main, folder / 'mitosis_karyotype_stages.drawn.svg'),
		(devel.render_human_chromosome_2_fusion.main, deck / 'assets' / 'visual_renewal' / 'human_chromosome_2_fusion.drawn.svg'),
		(lect10b_chromosome_recipe.lect10_karyotype.main, deck / 'assets' / 'lect10_repaired_figures' / 'karyotype_preparation.svg'),
	]
	for make, destination in jobs:
		destination.parent.mkdir(parents=True, exist_ok=True)
		make(destination)
	for kind in ('metacentric', 'submetacentric', 'acrocentric'):
		lect10b_chromosome_recipe.lect10_movement.main(kind, folder / (kind + '_movement.drawn.svg'))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--output-root', type=pathlib.Path, default=pathlib.Path(__file__).resolve().parent,
		help='Deck directory for generated assets (default: directory containing this script).')
	main(parser.parse_args().output_root)
