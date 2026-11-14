"""Gallery builds preserve the caller's process state, including on failure."""

import sys

import PIL.Image
import PIL.ImageFont

import svg_tools.examples.build_gallery as gallery


#============================================
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
