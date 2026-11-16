#!/usr/bin/env python3
"""Regenerate seven LECT06 hybrid figures from frozen source layers and shared bodies."""

import pathlib
import runpy


def main() -> None:
	"""Write only owning assets; templates and cleanup layers remain immutable."""
	deck = pathlib.Path(__file__).resolve().parent
	models = deck / 'chromosome_models/mixed'
	for family, asset_folder in (
		('intro', 'lect06b-intro_cells'),
		('overview', 'lect06c-meiosis'),
		('crossovers', 'lect06c-meiosis'),
		('recombination', 'lect06c-meiosis'),
	):
		recipe = runpy.run_path(str(models / family / 'recipe.py'))
		recipe['build'](deck / 'assets' / asset_folder)


if __name__ == '__main__':
	main()
