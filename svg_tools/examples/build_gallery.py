#!/usr/bin/env python3
"""Build the toolkit's editable SVG gallery and white-background previews."""

import argparse
import importlib
import os
import pathlib
import shutil
import subprocess

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

import svg_tools.examples.allele_frequencies


ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / 'docs/slide-specs/illustration_examples/svg_toolkit'
EXAMPLES = (
	('placement', '_temp/placement.svg', 'Placement'),
	('text_labels', '_temp/text_labels.svg', 'Text Labels'),
	('styled_text', '_temp/styled_text.svg', 'Styled Text'),
	('curve_samples', '_temp/curve_samples.drawn.svg', 'Curves'),
	('svg_composition', '_temp/svg_composition.svg', 'SVG Import'),
	('icons', '_temp/icons.svg', 'Icons'),
	('annotations', '_temp/annotations.svg', 'Annotations'),
	('membranes', '_temp/svg_toolkit/membranes/membranes.svg', 'Membranes'),
	('proteins', '_temp/svg_toolkit/proteins/proteins.svg', 'Proteins'),
	('signaling', '_temp/svg_toolkit/signaling/signaling.svg', 'Signaling'),
	('plots', '_temp/plots.svg', 'Plots'),
	('cells', '_temp/svg_toolkit/cells/cells.svg', 'Cells'),
	('organelles', '_temp/svg_toolkit/organelles/organelles.svg', 'Organelles'),
	('gene_features', '_temp/gene_features.svg', 'Gene Features'),
	('binding', '_temp/svg_toolkit/binding/binding.svg', 'Binding'),
	('phenotypes', '_temp/svg_toolkit/phenotypes/phenotypes.svg', 'Phenotypes'),
	('allele_frequencies', '_temp/allele_frequencies.svg', 'Allele Frequencies'),
)


#============================================
def build(output_dir: pathlib.Path) -> None:
	"""Run each authored recipe and publish SVGs and proportional previews."""
	output_dir = output_dir.resolve()
	output_dir.mkdir(parents=True, exist_ok=True)
	os.chdir(ROOT)
	previews = []
	for name, source, title in EXAMPLES:
		source_path = ROOT / source
		if name == 'allele_frequencies':
			svg_tools.examples.allele_frequencies.generate(source_path)
		else:
			module = importlib.import_module(f'svg_tools.examples.{name}')
			if name == 'curve_samples':
				# The original recipe derives its output from its own file path.
				module.__file__ = str(ROOT / '_temp/curve_samples.py')
			module.main()
		suffix = 'plot' if name in ('plots', 'allele_frequencies') else 'drawn'
		svg = output_dir / f'{name}.{suffix}.svg'
		shutil.copyfile(source_path, svg)
		png = ROOT / '_temp/svg_toolkit_gallery_preview.png'
		env = dict(os.environ, PANGOCAIRO_BACKEND='fc')
		subprocess.run(['rsvg-convert', '--width', '1200', '--background-color', 'white',
			'--output', str(png), str(svg)], check=True, env=env)
		with PIL.Image.open(png) as image:
			preview = image.convert('RGB')
			preview.save(output_dir / f'{name}.webp', 'WEBP', quality=90)
			preview.thumbnail((260, 160), PIL.Image.Resampling.LANCZOS)
			previews.append((title, preview.copy()))
	png.unlink()
	font = PIL.ImageFont.truetype(str(ROOT / 'assets/fonts/atkinson_hyperlegible_next/AtkinsonHyperlegibleNext-Bold.ttf'), 18)
	columns = 4
	rows = (len(previews) + columns - 1) // columns
	index = PIL.Image.new('RGB', (columns * 290, rows * 205), 'white')
	draw = PIL.ImageDraw.Draw(index)
	for position, (title, preview) in enumerate(previews):
		x, y = (position % columns) * 290, (position // columns) * 205
		index.paste(preview, (x + (290 - preview.width) // 2, y + (165 - preview.height) // 2))
		draw.text((x + 15, y + 170), title, font=font, fill='#102c40')
	index.save(output_dir / 'index.webp', 'WEBP', quality=90)


#============================================
def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--output-dir', type=pathlib.Path, default=DEFAULT_OUTPUT)
	args = parser.parse_args()
	build(args.output_dir)


if __name__ == '__main__':
	main()
