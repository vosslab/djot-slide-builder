"""Gallery builds preserve the caller's process state, including on failure."""

import os
import sys

import PIL.Image
import PIL.ImageFont
import pytest

import svg_tools.examples.build_gallery as gallery
import svg_tools.examples.curve_samples as curves


@pytest.mark.parametrize('fail', [False, True])
def test_gallery_restores_caller_state(tmp_path, monkeypatch, fail):
	root = tmp_path / 'root'
	(root / '_temp').mkdir(parents=True)
	output = tmp_path / 'output'
	previous_dir = os.getcwd()
	previous_file = curves.__file__
	font_path = gallery.ROOT / 'assets/fonts/atkinson_hyperlegible_next/AtkinsonHyperlegibleNext-Bold.ttf'
	truetype = PIL.ImageFont.truetype
	monkeypatch.setattr(gallery, 'ROOT', root)
	monkeypatch.setattr(gallery, 'EXAMPLES', (('curve_samples', '_temp/curve_samples.drawn.svg', 'Curves'),))
	monkeypatch.setattr(PIL.ImageFont, 'truetype', lambda *args, **kwargs: truetype(str(font_path), 18))

	def render(command, **kwargs):
		if fail:
			raise RuntimeError('renderer failed')
		PIL.Image.new('RGB', (20, 20), 'white').save(command[command.index('--output') + 1])

	monkeypatch.setattr(gallery.subprocess, 'run', render)
	if fail:
		with pytest.raises(RuntimeError, match='renderer failed'):
			gallery.build(output)
	else:
		gallery.build(output)
		assert (output / 'curve_samples.drawn.svg').is_file()
		assert (output / 'index.webp').is_file()
	assert os.getcwd() == previous_dir
	assert curves.__file__ == previous_file


def test_plot_recipe_ignores_gallery_cli_arguments(tmp_path, monkeypatch):
	root = tmp_path / 'root'
	(root / '_temp').mkdir(parents=True)
	font_path = gallery.ROOT / 'assets/fonts/atkinson_hyperlegible_next/AtkinsonHyperlegibleNext-Bold.ttf'
	truetype = PIL.ImageFont.truetype
	monkeypatch.setattr(gallery, 'ROOT', root)
	monkeypatch.setattr(gallery, 'EXAMPLES', (('plots', '_temp/plots.svg', 'Plots'),))
	monkeypatch.setattr(sys, 'argv', ['build_gallery', '--output-dir', str(tmp_path / 'output')])
	monkeypatch.setattr(PIL.ImageFont, 'truetype', lambda *args, **kwargs: truetype(str(font_path), 18))
	monkeypatch.setattr(gallery.subprocess, 'run', lambda command, **kwargs:
		PIL.Image.new('RGB', (20, 20), 'white').save(command[command.index('--output') + 1]))
	gallery.build(tmp_path / 'output')
	assert (tmp_path / 'output/plots.plot.svg').is_file()
