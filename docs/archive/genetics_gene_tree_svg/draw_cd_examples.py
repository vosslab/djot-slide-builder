"""Replay the preserved C/D metric examples into repository _temp only.

Derived from the archived cd/draw_trials.py.txt; course files are never opened.
"""

from pathlib import Path
from html import escape
# ASVS 1.5.1: reject XML entities while checking replay files.
import defusedxml.ElementTree as ET
import re

P = Path(__file__).resolve().parents[3] / "_temp/gene_tree_archive_replay"


def tree(
	name: str,
	tips: list[str],
	merges: list[tuple],
	stage: int,
	scale: float,
	source: str,
) -> Path:
	ys = {t: 55 + i * 75 for i, t in enumerate(tips)}
	hs = {t: 0 for t in tips}
	out = [
		'<svg xmlns="http://www.w3.org/2000/svg" width="860" height="570" viewBox="0 0 860 570" role="img" aria-labelledby="title desc">',
		f'<title id="title">{escape(name)}</title>',
		f'<desc id="desc">Metric tree. Horizontal branch lengths are proportional to distance. Source: {escape(source)}. Stage {stage}.</desc>',
		'<rect width="860" height="570" fill="white"/>',
		'<g font-family="Arial" font-size="27" fill="#172B3A">',
	]
	x = lambda h: 735 - h * scale
	for i, (node, a, b, h) in enumerate(merges):
		ys[node] = (ys[a] + ys[b]) / 2
		hs[node] = h
		if i >= stage:
			continue
		out.append(
			f'<g id="join-{node}"><path d="M {x(h)} {ys[a]} V {ys[b]}" stroke="#006A69" stroke-width="4" fill="none"/>'
		)
		for t in (a, b):
			out.append(
				f'<path id="edge-{node}-{t}" d="M {x(h)} {ys[t]} H {x(hs[t])}" stroke="#006A69" stroke-width="4" fill="none"/>'
			)
			out.append(
				f'<text x="{(x(h) + x(hs[t])) / 2}" y="{ys[t] - 12}" text-anchor="middle">{h - hs[t]:g}</text>'
			)
		out.append(
			f'<circle cx="{x(h)}" cy="{ys[node]}" r="5" fill="#006A69"/><text x="{x(h) - 12}" y="{ys[node] + 9}" text-anchor="end">{escape(node)}</text></g>'
		)
	visible = set()
	for _, a, b, _ in merges[:stage]:
		visible.update((a, b))
	for t in tips:
		if t in visible:
			out.append(f'<text x="750" y="{ys[t] + 9}">{escape(t)}</text>')
	out += ["</g></svg>"]
	path = P / (name + ".drawn.svg")
	path.write_text("\n".join(out))
	ET.parse(path)
	return path


# ============================================
def main() -> None:
	"""Reproduce the fourteen historical drawings in the fixed scratch directory."""
	P.mkdir(parents=True, exist_ok=True)

	seven = [
		("a", "Hu", "Ba", 1),
		("b", "Co", "Sh", 1.5),
		("c", "Mo", "Ha", 3.5),
		("d", "a", "b", 4),
		("e", "d", "c", 4.875),
		("f", "e", "Ch", 7.25),
	]
	for n in range(1, 7):
		tree(
			f"phy_c_seven_stage_{n}",
			["Hu", "Ba", "Co", "Sh", "Mo", "Ha", "Ch"],
			seven,
			n,
			80,
			"original LECT12C PDF pages 45-52",
		)

	five = [("u", "a", "b", 8.5), ("v", "u", "e", 11), ("w", "c", "d", 14), ("r", "v", "w", 16.5)]
	p = tree(
		"phy_c_five_taxa",
		["a", "b", "e", "c", "d"],
		five,
		4,
		36,
		"original LECT12C PDF page26; repeated worked dataset and instructor manual averaging authority",
	)
	s = p.read_text()
	axis = [
		'<g id="height-axis" font-family="Arial" font-size="24" fill="#172B3A">',
		'<path d="M141 470 H735" stroke="#687985" stroke-width="2"/>',
	]
	for h in (16.5, 14, 11, 8.5, 0):
		x = 735 - 36 * h
		axis += [
			f'<path d="M{x} 460 V480" stroke="#687985" stroke-width="2"/>',
			f'<text x="{x}" y="510" text-anchor="middle">{h:g}</text>',
		]
	axis += ['<text x="735" y="550" text-anchor="end">Height</text></g>']
	p.write_text(s.replace("</svg>", "\n".join(axis) + "</svg>"))
	hartl = [("CD", "C", "D", 2.5), ("AB", "A", "B", 4), ("root", "AB", "CD", 8.5)]
	p = tree(
		"phy_c_hartl_answer",
		["A", "B", "C", "D"],
		hartl,
		3,
		65,
		"original LECT12C PDF page39, question17.27",
	)
	s = p.read_text()

	# Source labels only the four taxa, not internal nodes.
	s = re.sub(r'<text x="[^"]+" y="[^"]+" text-anchor="end">(?:AB|CD|root)</text>', "", s)
	p.write_text(s, encoding="ascii")
	# Source preceding state shows the same geometry without numerical answers.
	blank = re.sub(r'<text x="[^"]+" y="[^"]+" text-anchor="middle">[^<]+</text>', "", s)
	(P / "phy_c_hartl_question.drawn.svg").write_text(
		blank.replace("phy_c_hartl_answer", "phy_c_hartl_question")
	)
	activity = [
		("ac", "a", "c", 2),
		("be", "b", "e", 3),
		("df", "d", "f", 4),
		("acbe", "ac", "be", 5),
		("root", "acbe", "df", 7),
	]
	for n in range(1, 6):
		p = tree(
			f"phy_d_activity_stage_{n}",
			["a", "c", "b", "e", "d", "f"],
			activity,
			n,
			85,
			"original LECT12D PDF pages24-28; original reconstruction from displayed merge heights",
		)
		s = p.read_text()
		s = re.sub(
			r'<text x="[^"]+" y="[^"]+" text-anchor="end">(?:ac|be|df|acbe|root)</text>', "", s
		)
		p.write_text(s, encoding="ascii")
	for p in P.glob("*.drawn.svg"):
		ET.parse(p)


if __name__ == "__main__":
	main()
