#!/usr/bin/env python3
"""Render the recovered Lecture 04 table sequences as 200-DPI PNG assets.

The HTML tables are an authoring aid for diagrams that are too wide for the
ordinary editable table layout.  The generated PNGs are ordinary component
images, so the presentation build does not depend on a browser or WeasyPrint.
"""

from __future__ import annotations

import html
import pathlib
import shutil
import subprocess
import tempfile

from weasyprint import HTML


ROOT = pathlib.Path(__file__).resolve().parents[1]
LECTURE_ASSETS = ROOT / "genetics" / "LECT04" / "djot" / "assets"
RASTER_DPI = 200


PUNNETT_ROWS = (
	("AB", ("AABB", "AABb", "AaBB", "AaBb")),
	("Ab", ("AABb", "AAbb", "AaBb", "Aabb")),
	("aB", ("AaBB", "AaBb", "aaBB", "aaBb")),
	("ab", ("AaBb", "Aabb", "aaBb", "aabb")),
)
PUNNETT_COLUMNS = ("AB", "Ab", "aB", "ab")


def esc(value: object) -> str:
	"""Escape one table value for the generated HTML."""
	return html.escape(str(value))


def page_style(width: int, height: int) -> str:
	"""Return stable page and table styling for one image series."""
	return f"""
@page {{ size: {width}px {height}px; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: white; }}
.page {{ width: {width}px; height: {height}px; padding: 55px 80px; display: flex;
  align-items: center; justify-content: center; page-break-after: always; }}
.page:last-child {{ page-break-after: auto; }}
table {{ border-collapse: collapse; table-layout: fixed; font-family: sans-serif;
  color: #172033; background: white; }}
th, td {{ border: 3px solid #496b8f; text-align: center; vertical-align: middle;
  padding: 12px 10px; font-size: 27px; line-height: 1.05; }}
th {{ background: #e7eef6; font-weight: 700; }}
.corner {{ background: #d6e2ef; }}
.row-label {{ width: 150px; }}
.empty {{ color: #9ba9b8; }}
.callout {{ margin-top: 24px; font: 28px/1.2 sans-serif; text-align: center; color: #172033; }}
.callout strong {{ color: #8e1b3e; }}
.punnett {{ width: 1120px; }}
.punnett th, .punnett td {{ height: 112px; }}
.punnett .row-label {{ width: 190px; }}
.punnett .diag {{ background: #d9e8f7; }}
.punnett .homo {{ background: #cbdcf2; }}
.punnett .dominant-a {{ background: #f4c8cc; }}
.punnett .dominant-b {{ background: #c8daf0; }}
.punnett .both-dominant {{ background: #dfc8ec; }}
.punnett .a-dominant-b-recessive {{ background: #bfe3ca; }}
.punnett .a-recessive-b-dominant {{ background: #f6d18a; }}
.punnett .both-recessive {{ background: #f2d39a; }}
.punnett .ratio {{ border: 0; background: white; font-size: 25px; padding-top: 22px; }}
.cross {{ width: 1440px; }}
.cross th, .cross td {{ height: 66px; font-size: 23px; padding: 7px 6px; }}
.cross th:first-child, .cross td:first-child {{ width: 300px; text-align: left; padding-left: 14px; }}
.cross th:last-child, .cross td:last-child {{ width: 150px; }}
.cross .genotype {{ background: #eef1f4; }}
.cross .row-a {{ background: #dbeaf7; }}
.cross .row-b {{ background: #d9eedf; }}
.cross .row-c {{ background: #fff0c4; }}
.cross .row-d {{ background: #f8d9dc; }}
.cross .row-e {{ background: #e9dcf2; }}
.cross .blank {{ background: white; }}
.cross .total {{ font-weight: 700; background: #e7eef6; }}
"""


def punnett_table(values: tuple[tuple[str, ...], ...], highlight: str | None = None,
				  ratios: bool = False) -> str:
	"""Build one accessible four-by-four Punnett-square table."""
	highlights: dict[str, set[tuple[int, int]]] = {
		"diag": {(0, 3), (1, 2), (2, 1), (3, 0)},
		"homo": {(0, 0), (1, 1), (2, 2), (3, 3)},
		"dominant-a": {(r, c) for r in range(4) for c in range(4)
			if "A" in PUNNETT_ROWS[r][1][c]},
		"dominant-b": {(r, c) for r in range(4) for c in range(4)
			if "B" in PUNNETT_ROWS[r][1][c]},
		"both-dominant": {(r, c) for r in range(4) for c in range(4)
			if "A" in PUNNETT_ROWS[r][1][c] and "B" in PUNNETT_ROWS[r][1][c]},
		"a-dominant-b-recessive": {(r, c) for r in range(4) for c in range(4)
			if "A" in PUNNETT_ROWS[r][1][c] and "bb" in PUNNETT_ROWS[r][1][c]},
		"a-recessive-b-dominant": {(r, c) for r in range(4) for c in range(4)
			if "aa" in PUNNETT_ROWS[r][1][c] and "B" in PUNNETT_ROWS[r][1][c]},
		"both-recessive": {(r, c) for r in range(4) for c in range(4)
			if "aa" in PUNNETT_ROWS[r][1][c] and "bb" in PUNNETT_ROWS[r][1][c]},
	}
	active = highlights.get(highlight, set())
	parts = ["<table class='punnett'><tr><th class='corner'>Female \\ Male</th>"]
	parts.extend(f"<th>{esc(value)}</th>" for value in PUNNETT_COLUMNS)
	parts.append("</tr>")
	for row_index, (label, row) in enumerate(PUNNETT_ROWS):
		parts.append(f"<tr><th class='row-label'>{esc(label)}</th>")
		for column_index, _expected in enumerate(row):
			value = values[row_index][column_index]
			cell_class = highlight if (row_index, column_index) in active else ""
			if not value:
				cell_class = "empty"
			parts.append(f"<td class='{cell_class}'>{esc(value) if value else '&nbsp;'}</td>")
		parts.append("</tr>")
	if ratios:
		parts.append("<tr><td colspan='5' class='ratio'>Genotype ratio: 1:2:1:2:4:2:1:2:1 &nbsp;&nbsp; Phenotype ratio: 9:3:3:1</td></tr>")
	parts.append("</table>")
	return "".join(parts)


def crossover_table(rows: tuple[tuple[str, tuple[str, ...], str], ...]) -> str:
	"""Build one seven-gene work table with progressive row fills."""
	parts = ["<table class='cross'><tr><th>genes -&gt;</th>"]
	parts.extend(f"<th>{letter}</th>" for letter in "ABCDEFG")
	parts.append("<th>TOTAL</th></tr>")
	for label, values, class_name in rows:
		parts.append(f"<tr class='{class_name}'><td>{esc(label)}</td>")
		cells = values if len(values) == 8 else values + ("",)
		parts.extend(f"<td>{esc(value) if value else '&nbsp;'}</td>" for value in cells)
		parts.append("</tr>")
	parts.append("</table>")
	return "".join(parts)


def render_document(output_dir: pathlib.Path, filename: str, css: str,
					pages: tuple[str, ...], names: tuple[str, ...]) -> None:
	"""Write HTML provenance and rasterize each page to a lossless 200-DPI PNG."""
	document = "<!doctype html><html><head><meta charset='utf-8'><style>" + css + "</style></head><body>"
	document += "".join(f"<section class='page'>{page}</section>" for page in pages)
	document += "</body></html>\n"
	output_dir.mkdir(parents=True, exist_ok=True)
	(output_dir / filename).write_text(document, encoding="utf-8")
	prefix_name = names[0].rsplit("_", 1)[0]
	for existing in output_dir.glob(f"{prefix_name}_*.png"):
		existing.unlink()
	with tempfile.TemporaryDirectory(prefix="lect04-table-") as temporary:
		pdf_path = pathlib.Path(temporary) / "series.pdf"
		prefix = pathlib.Path(temporary) / "page"
		HTML(string=document, base_url=str(output_dir)).write_pdf(str(pdf_path))
		subprocess.run(["pdftoppm", "-png", "-r", str(RASTER_DPI), str(pdf_path), str(prefix)],
			check=True)
		rendered = sorted(pathlib.Path(temporary).glob("page-*.png"))
		if len(rendered) != len(names):
			raise RuntimeError(f"expected {len(names)} rendered pages, found {len(rendered)}")
		for index, name in enumerate(names, start=1):
			source = rendered[index - 1]
			destination = output_dir / name
			if destination.exists():
				destination.unlink()
			shutil.move(source, destination)


def render_punnett_series() -> None:
	"""Render the readable progressive and highlighted dihybrid tables."""
	step_one = (("AABB", "", "", ""), ("", "", "", ""), ("", "", "", ""), ("", "", "", ""))
	step_two = (("AABB", "AABb", "", ""), ("", "", "", ""), ("", "", "", ""), ("", "", "", ""))
	step_three = (("AABB", "AABb", "AaBB", "AaBb"), ("AABb", "AAbb", "AaBb", "Aabb"),
				  ("AaBB", "AaBb", "aaBB", ""), ("", "", "", ""))
	pages = (
		punnett_table(step_one), punnett_table(step_two),
		punnett_table(step_three), punnett_table(tuple(row for _label, row in PUNNETT_ROWS), ratios=True),
		punnett_table(tuple(row for _label, row in PUNNETT_ROWS), "diag"),
		punnett_table(tuple(row for _label, row in PUNNETT_ROWS), "homo"),
		punnett_table(tuple(row for _label, row in PUNNETT_ROWS), "dominant-a"),
		punnett_table(tuple(row for _label, row in PUNNETT_ROWS), "dominant-b"),
		punnett_table(tuple(row for _label, row in PUNNETT_ROWS), "both-dominant"),
		punnett_table(tuple(row for _label, row in PUNNETT_ROWS), "a-dominant-b-recessive"),
		punnett_table(tuple(row for _label, row in PUNNETT_ROWS), "a-recessive-b-dominant"),
		punnett_table(tuple(row for _label, row in PUNNETT_ROWS), "both-recessive"),
	)
	names = tuple(f"punnett_{index:02d}.png" for index in range(1, len(pages) + 1))
	render_document(LECTURE_ASSETS / "lect04g-indep_assort", "punnett_table_series.html",
		page_style(1600, 800) + """
.page { padding: 20px 40px; }
.punnett { width: 1420px; }
.punnett th, .punnett td { height: 120px; font-size: 32px; }
.punnett .row-label { width: 220px; }
.punnett .ratio { font-size: 27px; }
""", pages, names)


def render_crossover_series() -> None:
	"""Render the recovered seven-gene work-table sequence."""
	base = (
		("George genotype", ("Aa", "Bb", "Cc", "dd", "Ee", "ff", "Gg"), "genotype"),
		("Linda genotype", ("AA", "bb", "cc", "dd", "ee", "Ff", "Gg"), "genotype"),
	)
	progress = (
		(("(a) George gametes", ("", "", "", "", "", "", ""), "row-a"),
		 ("(b) Linda gametes", ("", "", "", "", "", "", ""), "row-b"),
		 ("(c) Punnett sq. size", ("", "", "", "", "", "", ""), "row-c"),
		 ("(d) cross genotypes", ("", "", "", "", "", "", ""), "row-d"),
		 ("(e) cross phenotypes", ("", "", "", "", "", "", ""), "row-e")),
		(("(a) George gametes", ("2", "", "", "", "", "", ""), "row-a"),
		 ("(b) Linda gametes", ("", "", "", "", "", "", ""), "row-b"),
		 ("(c) Punnett sq. size", ("", "", "", "", "", "", ""), "row-c"),
		 ("(d) cross genotypes", ("", "", "", "", "", "", ""), "row-d"),
		 ("(e) cross phenotypes", ("", "", "", "", "", "", ""), "row-e")),
		(("(a) George gametes", ("2", "", "", "", "", "", ""), "row-a"),
		 ("(b) Linda gametes", ("1", "", "", "", "", "", ""), "row-b"),
		 ("(c) Punnett sq. size", ("", "", "", "", "", "", ""), "row-c"),
		 ("(d) cross genotypes", ("", "", "", "", "", "", ""), "row-d"),
		 ("(e) cross phenotypes", ("", "", "", "", "", "", ""), "row-e")),
		(("(a) George gametes", ("2", "", "", "", "", "", ""), "row-a"),
		 ("(b) Linda gametes", ("1", "", "", "", "", "", ""), "row-b"),
		 ("(c) Punnett sq. size", ("", "", "", "", "", "", ""), "row-c"),
		 ("(d) cross genotypes", ("2", "", "", "", "", "", ""), "row-d"),
		 ("(e) cross phenotypes", ("", "", "", "", "", "", ""), "row-e")),
		(("(a) George gametes", ("2", "", "", "", "", "", ""), "row-a"),
		 ("(b) Linda gametes", ("1", "", "", "", "", "", ""), "row-b"),
		 ("(c) Punnett sq. size", ("", "", "", "", "", "", ""), "row-c"),
		 ("(d) cross genotypes", ("2", "", "", "", "", "", ""), "row-d"),
		 ("(e) cross phenotypes", ("1", "", "", "", "", "", ""), "row-e")),
		(("(a) George gametes", ("2", "2", "", "", "", "", ""), "row-a"),
		 ("(b) Linda gametes", ("1", "1", "", "", "", "", ""), "row-b"),
		 ("(c) Punnett sq. size", ("", "", "", "", "", "", ""), "row-c"),
		 ("(d) cross genotypes", ("2", "2", "", "", "", "", ""), "row-d"),
		 ("(e) cross phenotypes", ("1", "2", "", "", "", "", ""), "row-e")),
		(("(a) George gametes", ("2", "2", "2", "1", "2", "1", "2"), "row-a"),
		 ("(b) Linda gametes", ("1", "1", "1", "1", "1", "2", "2"), "row-b"),
		 ("(c) Punnett sq. size", ("", "", "", "", "", "", ""), "row-c"),
		 ("(d) cross genotypes", ("2", "2", "2", "1", "2", "2", "3"), "row-d"),
		 ("(e) cross phenotypes", ("1", "2", "2", "1", "2", "2", "2"), "row-e")),
		(("(a) George gametes", ("2", "2", "2", "1", "2", "1", "2", "32"), "row-a"),
		 ("(b) Linda gametes", ("1", "1", "1", "1", "1", "2", "2", "4"), "row-b"),
		 ("(c) Punnett sq. size", ("", "", "", "", "", "", ""), "row-c"),
		 ("(d) cross genotypes", ("2", "2", "2", "1", "2", "2", "3", "96"), "row-d"),
		 ("(e) cross phenotypes", ("1", "2", "2", "1", "2", "2", "2", "32"), "row-e")),
		(("(a) George gametes", ("2", "2", "2", "1", "2", "1", "2", "32"), "row-a"),
		 ("(b) Linda gametes", ("1", "1", "1", "1", "1", "2", "2"), "row-b"),
		 ("(c) Punnett sq. size", ("", "", "", "", "", "", ""), "row-c"),
		 ("(d) cross genotypes", ("2", "2", "2", "1", "2", "2", "3"), "row-d"),
		 ("(e) cross phenotypes", ("1", "2", "2", "1", "2", "2", "2"), "row-e")),
		(("(a) George gametes", ("2", "2", "2", "1", "2", "1", "2"), "row-a"),
		 ("(b) Linda gametes", ("1", "1", "1", "1", "1", "2", "2"), "row-b"),
		 ("(c) Punnett sq. size", ("", "", "", "", "", "", ""), "row-c"),
		 ("(d) cross genotypes", ("2", "2", "2", "1", "2", "2", "3"), "row-d"),
		 ("(e) cross phenotypes", ("1", "2", "2", "1", "2", "2", "2"), "row-e")),
		(("(a) George gametes", ("2", "2", "2", "1", "2", "1", "2"), "row-a"),
		 ("(b) Linda gametes", ("1", "1", "1", "1", "1", "2", "2"), "row-b"),
		 ("(c) Punnett sq. size", ("", "", "", "", "", "", "", "128"), "row-c"),
		 ("(d) cross genotypes", ("2", "2", "2", "1", "2", "2", "3", "96"), "row-d"),
		 ("(e) cross phenotypes", ("1", "2", "2", "1", "2", "2", "2", "32"), "row-e")),
	)
	progress = (progress[0], progress[1], progress[2], progress[3], progress[4], progress[5],
		progress[6], progress[9], progress[8], progress[7], progress[10])
	pages = []
	for index, rows in enumerate(progress):
		combined = base + rows
		pages.append(crossover_table(combined))
	# Two retained group-work tables from the original closing pages.
	pages.extend((
		crossover_table((
			("Larry genotype", ("Aa", "Bb", "Cc", "dd", "ee", "ff", "gg"), "genotype"),
			("Marge genotype", ("Aa", "BB", "Cc", "DD", "EE", "ff", "Gg"), "genotype"),
			("(a) Larry gametes", ("2", "2", "2", "1", "1", "1", "1", "8"), "row-a"),
			("(b) Marge gametes", ("2", "1", "2", "1", "1", "1", "2", "8"), "row-b"),
			("(c) Punnett sq. size", ("", "", "", "", "", "", "64"), "row-c"),
			("(d) cross genotypes", ("3", "2", "3", "1", "1", "1", "2", "36"), "row-d"),
			("(e) cross phenotypes", ("2", "1", "2", "1", "1", "1", "2", "8"), "row-e"),
		)),
		crossover_table((
			("Jerry genotype", ("Aa", "Bb", "Cc", "dd", "Ee", "FF", "Gg"), "genotype"),
			("Karla genotype", ("Aa", "bb", "Cc", "DD", "Ee", "ff", "gg"), "genotype"),
			("(a) Jerry gametes", ("2", "2", "2", "1", "2", "1", "2", "32"), "row-a"),
			("(b) Karla gametes", ("2", "1", "2", "1", "2", "1", "1", "8"), "row-b"),
			("(c) Punnett sq. size", ("", "", "", "", "", "", "256"), "row-c"),
			("(d) cross genotypes", ("3", "2", "3", "1", "3", "1", "2", "108"), "row-d"),
			("(e) cross phenotypes", ("2", "2", "2", "1", "2", "1", "2", "32"), "row-e"),
		)),
	))
	names = tuple(f"crossover_{index:02d}.png" for index in range(1, len(pages) + 1))
	render_document(LECTURE_ASSETS / "lect04i-big_crossover_problem", "crossover_table_series.html",
		page_style(1600, 800), tuple(pages), names)


def main() -> None:
	"""Render both deck-specific table series."""
	render_punnett_series()
	render_crossover_series()


if __name__ == "__main__":
	main()
