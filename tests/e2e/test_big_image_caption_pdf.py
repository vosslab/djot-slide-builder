"""Verify long native image captions actually wrap inside the exported PDF."""

import pathlib
import subprocess
import xml.etree.ElementTree as ET

import PIL.Image

import slide_lib.djot_parser
import slide_lib.layout_engine
import slide_lib.libreoffice
import slide_lib.odp_export
import slide_lib.presentation_theme


def test_long_caption_words_and_link_remain_inside_pdf(tmp_path: pathlib.Path) -> None:
	"""Text inside a rectangle previously ran across one line and disappeared off-page."""
	PIL.Image.new("RGB", (320, 180), "blue").save(tmp_path / "forecast.png")
	caption = ("Some may see intermittent light showers or sprinkles during outdoor activities tonight. "
		"Seasonably mild temperatures and mostly cloudy skies will follow into early next week. "
		"The highest chances of rain are expected towards mid-week.")
	credit = "NWS Chicago, retrieved Nov 02, 2026: https://www.weather.gov/lot/weatherstory"
	source = tmp_path / "caption.djot"
	source.write_text("=== layout: big-image\n@image\n![Forecast](forecast.png)\n"
		f"@caption\n{caption}\n\n@citation\n{credit}\n", encoding="utf-8")
	theme = slide_lib.presentation_theme.default_theme()
	plan = slide_lib.layout_engine.compile_layout_deck(slide_lib.djot_parser.parse_deck(source), theme).plan
	odp = slide_lib.odp_export.write_odp(plan, theme, tmp_path / "caption.odp")
	pdf = slide_lib.libreoffice.convert_file(odp, tmp_path, "pdf")
	result = subprocess.run(["pdftotext", "-bbox", str(pdf), "-"], check=True, capture_output=True)
	root = ET.fromstring(result.stdout)
	namespace = "{http://www.w3.org/1999/xhtml}"
	page = root.find(f".//{namespace}page")
	words = page.findall(f".//{namespace}word")
	assert " ".join(word.text for word in words) == caption + " " + credit
	assert len({word.attrib["yMin"] for word in words}) >= 3
	assert all(0 <= float(word.attrib["xMin"]) < float(word.attrib["xMax"]) <= float(page.attrib["width"])
		and 0 <= float(word.attrib["yMin"]) < float(word.attrib["yMax"]) <= float(page.attrib["height"])
		for word in words)
