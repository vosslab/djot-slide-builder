"""Copy the two original rubric PNGs from the instructor's Group Project ODP."""

import argparse
import pathlib
import zipfile

from slide_lib import odf_package
from slide_lib.importers import odp_media
from slide_lib.importers.odp_geometry import NS, qname


def main() -> None:
	"""Validate both rubric slides before writing their image assets."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("odp", type=pathlib.Path, help="authoritative Group Project ODP")
	source = parser.parse_args().odp
	# ASVS 5.2.1-5.2.3: reuse bounded ODP admission and PNG validation.
	package = odf_package.admit_package(source, ".odp", odf_package.ODP_MIMETYPE,
		odf_package.REQUIRED_ODP_MEMBERS)
	pages = package.content_root.findall(".//draw:page", NS)
	rubric_pages = [page for page in pages if any(
		" ".join("".join(box.itertext()).split()) == "Presentation Rubric"
		for box in page.findall("draw:frame/draw:text-box", NS))]
	if len(rubric_pages) != 2:
		parser.error(f"expected two Presentation Rubric pages, found {len(rubric_pages)}")

	budget = odp_media.MediaBudget()
	images = []
	with zipfile.ZipFile(source) as archive:
		for page in rubric_pages:
			frames = page.findall("draw:frame", NS)
			pictures = page.findall("draw:frame/draw:image", NS)
			page_objects = [node for node in page if node.tag.startswith("{" + NS["draw"] + "}")]
			if len(page_objects) != 2 or len(frames) != 2 or len(pictures) != 1:
				parser.error("each rubric page must contain one picture and its caption")
			href = pictures[0].get(qname("xlink", "href"), "")
			target = odf_package.package_reference_target("content.xml", href)
			if not target or target not in package.member_names or not target.lower().endswith(".png"):
				parser.error("each rubric picture must be a PNG embedded in the ODP")
			data = archive.read(target)
			odp_media.validate_image_blob(data, ".png", budget)
			images.append(data)

	# ASVS 5.3.3: output filenames are fixed and independent of archive paths.
	assets = pathlib.Path(__file__).resolve().parent / "assets"
	for index, image in enumerate(images, start=1):
		path = assets / f"presentation_rubric_{index}.png"
		path.write_bytes(image)
		print(path)


if __name__ == "__main__":
	main()
