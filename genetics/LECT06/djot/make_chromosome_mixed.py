#!/usr/bin/env python3
"""Regenerate seven LECT06 hybrid figures from frozen source layers and shared bodies."""

import pathlib
import runpy
import subprocess


def main() -> None:
	"""Write only owning assets; templates and cleanup layers remain immutable."""
	root = pathlib.Path(subprocess.check_output(
		['git', 'rev-parse', '--show-toplevel'], text=True).strip())
	deck = root / 'genetics/LECT06/djot'
	models = deck / 'chromosome_models/mixed'
	for recipe_path, asset_folder in (
		('intro/intro_recipes.py', 'lect06b-intro_cells'),
		('overview/overview_recipe.py', 'lect06c-meiosis'),
		('crossovers/crossovers_recipe.py', 'lect06c-meiosis'),
		('recombination/recombination_recipes.py', 'lect06c-meiosis'),
	):
		recipe = runpy.run_path(str(models / recipe_path))
		recipe['build'](deck / 'assets' / asset_folder)


if __name__ == '__main__':
	main()
