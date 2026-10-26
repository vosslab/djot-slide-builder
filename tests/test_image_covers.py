"""Image-owned cover geometry and native click-to-remove behavior."""

import pathlib
import zipfile

import PIL.Image
import pytest

import slide_lib.djot_parser
import slide_lib.layout_content
import slide_lib.layout_engine
import slide_lib.native_model
import slide_lib.odp_export
import slide_lib.odf_package
import slide_lib.presentation_theme


def compile_source(tmp_path: pathlib.Path, source: str):
	path = tmp_path / 'cover.djot'
	path.write_text(source)
	PIL.Image.new('RGB', (400, 200), 'blue').save(tmp_path / 'diagram.png')
	theme = slide_lib.presentation_theme.default_theme()
	result = slide_lib.layout_engine.compile_layout_deck(slide_lib.djot_parser.parse_deck(path), theme)
	return result, theme


@pytest.mark.parametrize('layout', ('one-panel', 'two-panels'))
def test_cover_tracks_displayed_image_and_consumes_no_layout_space(tmp_path: pathlib.Path, layout: str) -> None:
	prefix = ('=== layout: one-panel\n\n# Diagram\n\n@body\n\n' if layout == 'one-panel' else
		'=== layout: two-panels\n\n# Diagram\n\n@left\n\nExplanation\n\n@right\n\n')
	image = '![Diagram](diagram.png)\n\n'
	result, theme = compile_source(tmp_path, prefix + image + '=> disappear\ncover: 10 20 30 40\n')
	page = result.plan.slides[0]
	picture = next(item for item in page.objects if isinstance(item.content, slide_lib.layout_content.PictureContent))
	cover = next(item for item in page.objects if item.object_id.endswith('-cover'))
	displayed = picture.content.placement.displayed_rectangle
	assert (cover.rectangle.x, cover.rectangle.y, cover.rectangle.width, cover.rectangle.height) == pytest.approx((
		displayed.x + displayed.width * .1, displayed.y + displayed.height * .2,
		displayed.width * .3, displayed.height * .4))
	assert cover.z_index > picture.z_index
	plain, _theme = compile_source(tmp_path, prefix + image)
	assert page.slots == plain.plan.slides[0].slots
	assert picture == next(item for item in plain.plan.slides[0].objects
		if isinstance(item.content, slide_lib.layout_content.PictureContent))
	output = slide_lib.odp_export.write_odp(result.plan, theme, tmp_path / 'cover.odp')
	with zipfile.ZipFile(output) as archive:
		root = slide_lib.odf_package.parse_xml(archive.read('content.xml'), 'content.xml')
	ns = {'a': 'urn:oasis:names:tc:opendocument:xmlns:animation:1.0',
		's': 'urn:oasis:names:tc:opendocument:xmlns:smil-compatible:1.0',
		'p': slide_lib.odp_export.PRESENTATION_NS, 'd': slide_lib.odp_export.DRAW_NS}
	action = root.find('.//a:set', ns)
	assert action.get('{'+ns['s']+'}attributeName') == 'visibility'
	assert action.get('{'+ns['s']+'}to') == 'hidden'
	click = next(item for item in root.findall('.//a:par', ns)
		if item.get('{'+ns['p']+'}preset-class') == 'exit')
	assert click.get('{'+ns['s']+'}begin') == 'next'
	assert click.get('{'+ns['p']+'}preset-id') == 'ooo-exit-disappear'
	target = action.get('{'+ns['s']+'}targetElement')
	assert any(node.get('{'+ns['d']+'}id') == target for node in root.iter())
	shape = next(node for node in root.iter() if node.get('{'+ns['d']+'}id') == target)
	style_name = shape.get('{'+ns['d']+'}style-name')
	style = next(node for node in root.iter() if node.get('{'+slide_lib.odp_export.STYLE_NS+'}name') == style_name)
	properties = style.find('{'+slide_lib.odp_export.STYLE_NS+'}graphic-properties')
	assert properties.get('{'+ns['d']+'}fill') == 'solid'
	assert properties.get('{'+ns['d']+'}fill-color') == '#FFFFFF'
	assert properties.get('{'+ns['d']+'}opacity') == '100%'


@pytest.mark.parametrize('content, message', (
	('=> disappear\ncover: 10 20 30 40', 'immediately follow'),
	('![Diagram](diagram.png)\n\nUnrelated text\n\n=> disappear\ncover: 10 20 30 40', 'immediately follow'),
	('![Diagram](diagram.png)\n\n=> appear\ncover: 10 20 30 40', 'requires disappear'),
	('![Diagram](diagram.png)\n\n=> disappear\n{color=red}\ncover: 10 20 30 40', 'no attributes'),
	('![Diagram](diagram.png)\n\n=> disappear\ncover: 90 20 30 40', 'inside'),
	('![Diagram](diagram.png)\n\n=> disappear\ncover: -1 20 30 40', 'four percentages'),
	('![Diagram](diagram.png)\n\n=> disappear\ncover: 10 20 30', 'four percentages'),
	('=> disappear\nOrdinary paragraph', 'requires an image cover'),
	('- A list item\n<= disappear', 'requires an image cover'),
))
def test_invalid_cover_ownership_bounds_and_actions_fail(tmp_path: pathlib.Path, content: str, message: str) -> None:
	with pytest.raises(ValueError, match=message):
		compile_source(tmp_path, '=== layout: one-panel\n\n@body\n\n' + content + '\n')


def test_cover_click_keeps_its_source_position_between_other_reveals(tmp_path: pathlib.Path) -> None:
	result, _theme = compile_source(tmp_path, '=== layout: one-panel\n\n@body\n\n'
		'=> appear\nFirst\n\n![Diagram](diagram.png)\n\n=> disappear\ncover: 10 20 30 40\n\n'
		'=> appear\nLast\n')
	targets = sorted((target for item in result.plan.slides[0].objects for target in item.reveal_targets),
		key=lambda target: target.activation_order)
	assert [target.reveal.effect for target in targets] == [
		slide_lib.native_model.RevealEffect.APPEAR, slide_lib.native_model.RevealEffect.DISAPPEAR,
		slide_lib.native_model.RevealEffect.APPEAR]
