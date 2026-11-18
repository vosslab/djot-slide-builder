#!/usr/bin/env python3
"""Regenerate the chromosome review SVGs and replacement inventory."""

# Standard Library
import csv
import sys
import shutil
import hashlib
import pathlib
import argparse
import tempfile
import subprocess

# local repo modules
import review_api_ring
import review_api_forms
import review_api_dosage
import review_api_ploidy
import review_api_linkage
import review_api_movement
import review_api_deletion
import review_api_inversion
import review_api_mini_views
import review_api_assortment
import review_api_duplication
import review_api_translocation
import review_api_division_intro
import review_api_division_meiosis
import make_chromosome_engine_mini2
from genetics.LECT06.djot import make_chromosome_xlinked
from genetics.LECT13.djot import lect13d_chromosome_recipes


REPOSITORY = pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip())
ROOT = REPOSITORY / 'prototype'
INVENTORY = 'chromosome_replacements.csv'


#============================================
def build_retained(output_root: pathlib.Path, scratch: pathlib.Path) -> None:
	"""Rebuild the course-backed figures that already use chromosome models."""
	xlinked = REPOSITORY / 'genetics/LECT06/djot/chromosome_models/xlinked'
	make_chromosome_xlinked.generate_complements(xlinked / 'drosophila_chromosome_complements.json',
		REPOSITORY, output_root)

	# The cis/trans recipe also emits a portrait version for the lecture.
	cis = pathlib.Path('lect08b-chap8-linked_genes/cis_trans_wide.drawn.svg')
	subprocess.run((sys.executable, 'genetics/LECT08/djot/chromosome_recipes/cis_recipe.py',
		'--output-root', str(scratch)), cwd=REPOSITORY, check=True)
	(output_root / 'assets' / cis.parent).mkdir(parents=True, exist_ok=True)
	shutil.copyfile(scratch / cis, output_root / 'assets' / cis)

	subprocess.run((sys.executable, 'genetics/LECT09/djot/make_centromere.py',
		'--output-root', str(output_root / 'assets')), cwd=REPOSITORY, check=True)

	fusion_dir = output_root / 'chromosome_assets/assets/lect13d-meiosis_translocation'
	fusion_dir.mkdir(parents=True, exist_ok=True)
	lect13d_chromosome_recipes.fusion(fusion_dir)


#============================================
def build_assets(output_root: pathlib.Path, scratch: pathlib.Path) -> None:
	"""Build each family and the figures shared with the smaller review deck."""
	api = output_root / 'assets/chromosome_review_api'
	for family in (
		review_api_forms, review_api_division_intro, review_api_division_meiosis,
		review_api_assortment, review_api_linkage, review_api_movement,
		review_api_ploidy, review_api_dosage, review_api_deletion, review_api_ring,
		review_api_duplication, review_api_inversion, review_api_translocation, review_api_mini_views,
	):
		family.build(api)

	mini = output_root / 'assets/chromosome_engine_mini2'
	mini.mkdir(parents=True, exist_ok=True)
	for filename, build in (
		('c01.drawn.svg', make_chromosome_engine_mini2.build_c01),
		('c16.drawn.svg', make_chromosome_engine_mini2.build_c16),
		('c22.drawn.svg', make_chromosome_engine_mini2.build_c22),
		('c23.drawn.svg', make_chromosome_engine_mini2.build_c23),
		('c25.drawn.svg', make_chromosome_engine_mini2.build_c25),
		('c28.drawn.svg', make_chromosome_engine_mini2.build_c28),
		('c31.image.svg', make_chromosome_engine_mini2.build_c31),
		('c61.drawn.svg', make_chromosome_engine_mini2.build_c61),
		('c63.drawn.svg', make_chromosome_engine_mini2.build_c63),
	):
		build(mini / filename)

	build_retained(output_root, scratch)


#============================================
def publish(staged: pathlib.Path, output_root: pathlib.Path) -> None:
	"""Publish the inventoried assets and hash the exact bytes being delivered."""
	with (ROOT / INVENTORY).open(encoding='utf-8', newline='') as handle:
		reader = csv.DictReader(handle)
		fieldnames = reader.fieldnames
		rows = list(reader)

	# ASVS 5.3.2: Only publish paths emitted by the repository recipes.
	paths = [pathlib.Path(row['replacement_asset']).relative_to('prototype') for row in rows]
	built = {path.relative_to(staged) for path in staged.rglob('*.svg')}
	expected = set(paths)
	if built != expected:
		raise ValueError(f'Review SVGs differ from inventory. Missing: {sorted(expected - built)}. '
			f'Unexpected: {sorted(built - expected)}.')

	hashes = {}
	for path in sorted(expected):
		asset = (staged / path).read_bytes()
		target = output_root / path
		target.parent.mkdir(parents=True, exist_ok=True)
		target.write_bytes(asset)
		hashes[path] = hashlib.sha256(asset).hexdigest()

	for row, path in zip(rows, paths, strict=True):
		row['replacement_sha256'] = hashes[path]
	with (output_root / INVENTORY).open('w', encoding='utf-8', newline='') as handle:
		writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator='\n')
		writer.writeheader()
		writer.writerows(rows)


#============================================
def generate(prototype_root: pathlib.Path) -> None:
	"""Regenerate the review under the selected prototype root."""
	scratch_root = REPOSITORY / '_temp'
	scratch_root.mkdir(exist_ok=True)
	with tempfile.TemporaryDirectory(prefix='chromosome-review-', dir=scratch_root) as scratch_dir:
		scratch = pathlib.Path(scratch_dir)
		staged = scratch / 'prototype'
		build_assets(staged, scratch / 'cis')
		publish(staged, prototype_root)


#============================================
def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--output-root', type=pathlib.Path, default=ROOT,
		help='Destination for the prototype assets and inventory')
	args = parser.parse_args()
	generate(args.output_root)


if __name__ == '__main__':
	main()
