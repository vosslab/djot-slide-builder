"""Protect the observed LibreOffice SVG text-direction compatibility fix."""

import pathlib

import pytest

import slide_lib.importers.odp_metafile as metafile
import slide_lib.odf_package


@pytest.mark.parametrize("label,direction", [("a+", "ltr"), ("\u05d0", "rtl")])
def test_svg_export_keeps_text_and_repairs_only_ltr_figures(tmp_path: pathlib.Path,
		monkeypatch: pytest.MonkeyPatch, label: str, direction: str) -> None:
	"""Exporter RTL flags must not shift Latin alleles or corrupt genuine RTL text."""
	def convert(input_path: pathlib.Path, output_dir: pathlib.Path,
			output_format: str) -> pathlib.Path:
		assert output_format == "svg"
		output = output_dir / "figure.svg"
		output.write_text('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" '
			'"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
			'<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100">'
			f'<text direction="rtl" x="40" y="60">{label}</text></svg>')
		return output
	monkeypatch.setattr(metafile.slide_lib.libreoffice, "convert_file", convert)
	blob, suffix = metafile.component_image(b"VCLMTF\x01\x00source-data", ".svm", (0, 0, 200, 100))
	assert suffix == ".svg"
	root = slide_lib.odf_package.parse_xml(blob, "result")
	text = root.find("{http://www.w3.org/2000/svg}text")
	assert text.text == label
	assert text.get("direction") == direction
	assert (text.get("x"), text.get("y")) == ("40", "60")
