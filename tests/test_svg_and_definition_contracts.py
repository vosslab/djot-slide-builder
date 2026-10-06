"""Editable figure and definition contracts across the native pipeline."""

import pathlib
import zipfile
import xml.etree.ElementTree

import pytest

import slide_lib.djot_parser
import slide_lib.importers.djot_text
import slide_lib.importers.odf_text
import slide_lib.importers.odf_styles
import slide_lib.importers.odp_reader
import slide_lib.layout_content
import slide_lib.layout_engine
import slide_lib.odp_export
import slide_lib.presentation_theme
import slide_lib.svg_images


def test_svg_payload_and_aspect_survive_comparison_export(tmp_path: pathlib.Path) -> None:
	"""A figure stays SVG while unequal captions share a aligned native text row."""
	svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100">'
		'<text x="10" y="50">Editable label</text></svg>')
	(tmp_path / "figure.svg").write_text(svg)
	source = tmp_path / "comparison.djot"
	source.write_text('=== layout: image-comparison\n\n# Checkpoints\n\n'
		'@top-left\n\n![Stop](figure.svg)\n\n@top-right\n\n![Go](figure.svg)\n\n'
		'@bottom-left\n\nStop.\n\n@bottom-right\n\n'
		'With full chromosome attachment, go-ahead signal is received.\n')
	theme = slide_lib.presentation_theme.default_theme()
	plan = slide_lib.layout_engine.compile_layout_deck(
		slide_lib.djot_parser.parse_deck(source), theme).plan
	page = plan.slides[0]
	figures = [item for item in page.objects
		if isinstance(item.content, slide_lib.layout_content.PictureContent)]
	assert len(figures) == 2
	for figure in figures:
		display = figure.content.placement.displayed_rectangle
		assert display.width / display.height == pytest.approx(2)
	slots = {slot.slot_id: slot for slot in page.slots}
	assert slots["bottom-left"].rectangle.y == slots["bottom-right"].rectangle.y
	assert slots["top-left"].rectangle.height > slots["bottom-left"].rectangle.height
	output = slide_lib.odp_export.write_odp(plan, theme, tmp_path / "comparison.odp")
	with zipfile.ZipFile(output) as archive:
		members = [name for name in archive.namelist() if name.endswith(".svg")]
		assert len(members) == 1
		assert archive.read(members[0]) == svg.encode()
		assert b'image/svg+xml' in archive.read('META-INF/manifest.xml')
		assert b'With full chromosome' in archive.read('content.xml')


def test_definition_emphasis_survives_import_and_export_without_leaking(
		tmp_path: pathlib.Path) -> None:
	"""An inherited bold/underlined term keeps its color and a normal definition stays normal."""
	ns = slide_lib.importers.odp_reader.NS
	declarations = ' '.join(f'xmlns:{key}="{value}"' for key, value in ns.items())
	root = xml.etree.ElementTree.fromstring(f'<root {declarations}>'
		'<style:style style:name="base"><style:text-properties fo:font-weight="bold" '
		'style:text-underline-style="solid" fo:color="#ff0000"/></style:style>'
		'<style:style style:name="term" style:parent-style-name="base"/>'
		'<style:style style:name="normal"><style:text-properties fo:font-weight="normal" '
		'style:text-underline-style="none"/></style:style>'
		'<text:p><text:span text:style-name="term">Homologous'
		'<text:span text:style-name="normal"> regular</text:span></text:span>'
		' - chromosomes with the same genes.</text:p></root>')
	styles = slide_lib.importers.odf_styles.definitions((root,))
	paragraph = root.find('text:p', ns)
	runs = slide_lib.importers.odf_text.inline_runs(paragraph, styles)
	assert runs[0].bold and runs[0].underline and runs[0].color == "red"
	assert not runs[1].bold and not runs[1].underline
	assert not runs[-1].bold and not runs[-1].underline and not runs[-1].color
	text = slide_lib.importers.djot_text.render_runs(runs)
	source = tmp_path / "definition.djot"
	source.write_text('=== layout: one-panel\n\n@body\n\n- ' + text + '\n')
	theme = slide_lib.presentation_theme.default_theme()
	plan = slide_lib.layout_engine.compile_layout_deck(
		slide_lib.djot_parser.parse_deck(source), theme).plan
	output = slide_lib.odp_export.write_odp(plan, theme, tmp_path / "definition.odp")
	with zipfile.ZipFile(output) as archive:
		written = xml.etree.ElementTree.fromstring(archive.read('content.xml'))
	written_styles = slide_lib.importers.odf_styles.definitions((written,))
	spans = written.findall('.//text:span', ns)
	term = next(span for span in spans if span.text == 'Homologous')
	plain = next(span for span in spans if span.text and 'chromosomes' in span.text)
	assert slide_lib.importers.odf_styles.emphasis(term, written_styles, False, False) == (True, True)
	assert slide_lib.importers.odf_styles.emphasis(plain, written_styles, False, False) == (False, False)


def test_frame_formatting_resets_and_exact_color_survive_export(tmp_path: pathlib.Path) -> None:
	"""Keep inherited emphasis, capitalization, unknown RGB, and explicit normal resets."""
	ns = slide_lib.importers.odp_reader.NS
	declarations = ' '.join(f'xmlns:{key}="{value}"' for key, value in ns.items())
	root = xml.etree.ElementTree.fromstring(f'<root {declarations}>'
		'<style:style style:name="graphic"><style:graphic-properties draw:fill="none"/></style:style>'
		'<style:style style:name="base"><style:text-properties fo:font-weight="bold" '
		'fo:font-style="italic" fo:color="#CC00CC" fo:text-transform="uppercase" '
		'style:text-underline-style="solid"/></style:style>'
		'<style:style style:name="normal"><style:text-properties fo:font-weight="normal" '
		'fo:font-style="normal" fo:color="#000000" fo:text-transform="none" '
		'style:text-underline-style="none"/></style:style>'
		'<draw:frame draw:style-name="graphic" presentation:style-name="base">'
		'<draw:text-box><text:p>Important <text:span text:style-name="normal">Aa remains Aa</text:span>'
		' again</text:p></draw:text-box></draw:frame></root>')
	styles = slide_lib.importers.odf_styles.definitions((root,))
	frame = root.find('draw:frame', ns)
	context = slide_lib.importers.odf_text.text_style(frame, styles,
		slide_lib.importers.odf_text.TextStyle())
	paragraphs = slide_lib.importers.odf_text.text_paragraphs(frame, styles, context)
	runs = paragraphs[0][1]
	assert runs[0].text == 'IMPORTANT ' and runs[0].italic and runs[0].bold
	assert runs[0].underline and runs[0].color == '#CC00CC'
	assert runs[1].text == 'Aa remains Aa' and runs[1].color == 'black'
	assert not (runs[1].italic or runs[1].bold or runs[1].underline)
	assert runs[2].italic and runs[2].text == ' AGAIN'
	source = tmp_path / 'formatting.djot'
	source.write_text('=== layout: one-panel\n\n@body\n\n- '
		+ slide_lib.importers.djot_text.render_runs(runs) + '\n')
	theme = slide_lib.presentation_theme.default_theme()
	plan = slide_lib.layout_engine.compile_layout_deck(
		slide_lib.djot_parser.parse_deck(source), theme).plan
	output = slide_lib.odp_export.write_odp(plan, theme, tmp_path / 'formatting.odp')
	with zipfile.ZipFile(output) as archive:
		written = xml.etree.ElementTree.fromstring(archive.read('content.xml'))
	written_styles = slide_lib.importers.odf_styles.definitions((written,))
	spans = written.findall('.//text:span', ns)
	important = next(span for span in spans if span.text and 'IMPORTANT' in span.text)
	assert slide_lib.importers.odf_styles.attribute(important, written_styles,
		slide_lib.importers.odf_styles.qname('fo', 'font-style')) == 'italic'
	assert slide_lib.importers.odf_styles.attribute(important, written_styles,
		slide_lib.importers.odf_styles.qname('fo', 'color')).upper() == '#CC00CC'


def test_svg_dimensions_require_local_static_positive_viewport(tmp_path: pathlib.Path) -> None:
	"""SVG components cannot depend on remote images or invalid viewport sizes."""
	path = tmp_path / 'figure.svg'
	path.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="2in" height="72pt"/>')
	assert slide_lib.svg_images.dimensions(path) == (192, 96)
	path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 0 20"/>')
	with pytest.raises(ValueError, match='positive'):
		slide_lib.svg_images.dimensions(path)
	path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">'
		'<image href="https://example.com/figure.png"/></svg>')
	with pytest.raises(ValueError, match='embedded'):
		slide_lib.svg_images.dimensions(path)
