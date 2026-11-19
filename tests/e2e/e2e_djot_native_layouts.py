#!/usr/bin/env python3
"""Verify editable slide content through LibreOffice and selectable PDF export."""

# Standard Library
import pathlib
import shutil
import subprocess
import sys
import tempfile
import zipfile

# Third-party modules
import lxml.etree
import PIL.Image

# Local modules
import slide_lib.libreoffice
import slide_lib.odf_package


CAPTION = ("Some may see intermittent light showers or sprinkles during outdoor activities tonight. "
	"Seasonably mild temperatures and mostly cloudy skies will follow into early next week. "
	"The highest chances of rain are expected towards mid-week.")
QUESTION = "Which answer describes the result?"
ANSWER = "Choice B is correct."
NS = {
	"anim": "urn:oasis:names:tc:opendocument:xmlns:animation:1.0",
	"draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
	"office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
	"smil": "urn:oasis:names:tc:opendocument:xmlns:smil-compatible:1.0",
	"text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
}


#============================================
def require(condition: bool, message: str) -> None:
	if not condition:
		raise RuntimeError(message)


#============================================
def inspect_odp(odp_path: pathlib.Path) -> None:
	"""Check editable lists, images, and the answer reveal after Impress saves the file."""
	with zipfile.ZipFile(odp_path) as archive:
		root = slide_lib.odf_package.parse_xml(archive.read("content.xml"), "content.xml")
	pages = root.findall("./office:body/office:presentation/draw:page", NS)
	require(len(pages) == 3, "Expected three editable ODP slides.")
	list_slide, question_slide, image_slide = pages
	nested = list_slide.find(".//text:list-item/text:list", NS)
	require(nested is not None and "A nested item" in "".join(nested.itertext()),
		"Impress lost the nested editable list.")
	require(image_slide.find(".//draw:image", NS) is not None, "Impress lost the editable image.")
	objects = question_slide.findall(".//draw:text-box", NS) + question_slide.findall(".//draw:custom-shape", NS)
	texts = ["".join(node.itertext()) for node in objects]
	require(any(QUESTION in text and ANSWER not in text for text in texts),
		"The question must remain separate from the answer.")
	target_attribute = f"{{{NS['smil']}}}targetElement"
	xml_id = "{http://www.w3.org/XML/1998/namespace}id"
	targets = {node.get(target_attribute) for node in question_slide.findall(".//anim:set", NS)}
	require(any(node.get(xml_id) in targets and node.get(xml_id) is not None
		and ANSWER in "".join(node.itertext()) for node in question_slide.iter()),
		"The Impress answer reveal lost its editable target.")


#============================================
def inspect_pdf(pdf_path: pathlib.Path) -> None:
	"""Catch missing or clipped captions at the rendered PDF boundary."""
	result = subprocess.run(["pdftotext", "-bbox", str(pdf_path), "-"], check=True, capture_output=True)
	root = lxml.etree.fromstring(result.stdout)
	namespace = "{http://www.w3.org/1999/xhtml}"
	pages = root.findall(f".//{namespace}page")
	require(len(pages) == 3, "Expected three rendered PDF pages.")
	page = pages[-1]
	words = page.findall(f".//{namespace}word")
	require(" ".join(word.text for word in words) == CAPTION, "The PDF lost selectable caption text.")
	width, height = float(page.get("width")), float(page.get("height"))
	require(all(0 <= float(word.get("xMin")) < float(word.get("xMax")) <= width
		and 0 <= float(word.get("yMin")) < float(word.get("yMax")) <= height for word in words),
		"The exported caption overflows its PDF page.")


#============================================
def run() -> None:
	"""Build a representative Djot deck and resave the native ODP with LibreOffice."""
	root = pathlib.Path(__file__).resolve().parents[2]
	scratch = root / "_temp"
	scratch.mkdir(exist_ok=True)
	workspace = pathlib.Path(tempfile.mkdtemp(prefix="native_layouts_", dir=scratch))
	deck = workspace / f"{workspace.name}.djot"
	odp = root / "output" / "odp" / f"{deck.stem}.odp"
	pdf = root / "output" / "pdf" / f"{deck.stem}.pdf"
	PIL.Image.new("RGB", (320, 180), "blue").save(workspace / "forecast.png")
	deck.write_text("=== layout: one-panel\n@body\n- Native parent item\n"
		"  - A nested item\n- Native sibling item\n\n"
		f"=== layout: multiple-choice\n@question\n{QUESTION}\n\n"
		f"- Choice A\n- Choice B\n\n@answer\n{ANSWER}\n\n"
		"=== layout: big-image\n@image\n![Forecast](forecast.png)\n"
		f"@caption\n{CAPTION}\n", encoding="utf-8")
	print(f"Building {deck.relative_to(root)}. Failed-run files stay in _temp/ and output/.")
	subprocess.run([sys.executable, "deck_tools.py", "build", str(deck), "--format", "all"],
		cwd=root, check=True)
	inspect_pdf(pdf)
	resaved = slide_lib.libreoffice.convert_file(odp, workspace, "odp")
	inspect_odp(resaved)
	odp.unlink()
	pdf.unlink()
	shutil.rmtree(workspace)
	print("PASS: LibreOffice preserves editable slide content and selectable PDF captions.")


if __name__ == "__main__":
	run()
