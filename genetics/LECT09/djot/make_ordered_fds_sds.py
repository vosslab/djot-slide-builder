#!/usr/bin/env python3
"""Rebuild the three ordered-tetrad diagrams from durable layout/geometry inputs."""
import json
import pathlib

import svgpathtools
import lxml.etree
import svg_tools._xml
import svg_tools.chromosomes
import svg_tools.drawing

BASE = pathlib.Path(__file__).resolve().parent
DATA = BASE/'assets/lect09_ordered_fds_sds_templates'
OUTPUT = BASE/'assets/lect09_tetrad_concepts'
NS = '{http://www.w3.org/2000/svg}'
THICKNESS = 14



def fragment(xml: str) -> lxml.etree._Element:
	element = svg_tools._xml.parse(xml)
	for node in element.iter():
		node.tag = NS + node.tag
	return element


def build(name: str, contract: dict) -> bytes:
	root = svg_tools._xml.read(DATA/f'{name}.svg')
	bodies = {b['id']: b for g in contract['groups'] for b in g['bodies']}
	markers = {m['id']: m for g in contract['groups'] for m in g['markers']}
	for parent in list(root.iter()):
		for slot in list(parent):
			cid, mid = slot.get('data-chromosome-slot'), slot.get('data-centromere-slot')
			if cid:
				body = bodies[cid]
				regions = []
				for piece in body['pieces']:
					length = svgpathtools.parse_path(piece['path']).length()
					if regions and regions[-1][0] == piece['color']:
						regions[-1][1] += length
					else:
						regions.append([piece['color'], length])
				# Avoid floating-point inversion at an exact cubic knot; under 1e-7 SVG units.
				if len(regions)>1:
					regions[0][1] += 1e-7
					regions[-1][1] -= 1e-7
				model = svg_tools.chromosomes.Chromosome(tuple(
					svg_tools.chromosomes.Segment('A' if color=='#347A40' else 'a', color, length)
					for color, length in regions))
				part = svg_tools.chromosomes.chromosome_path_part(cid, model, body['path'], thickness=THICKNESS, labels=False)
				element = fragment(part.fragment)
				element.set('data-role', 'chromatid')
				element.set('data-centerline', body['path'])
				element.set('data-product', 'A' if regions[-1][0]=='#347A40' else 'a')
			elif mid:
				x, y = markers[mid]['center']
				element = fragment(svg_tools.chromosomes.centromere_part(mid, thickness=THICKNESS).fragment)
				element.set('transform', f'translate({x:g} {y:g}) rotate(90)')
				element.set('data-role', 'centromere')
			else:
				continue
			parent.insert(list(parent).index(slot), element)
			parent.remove(slot)
	lxml.etree.indent(root, space='  ')
	return lxml.etree.tostring(svg_tools.drawing.svg_root(root), encoding='utf-8', xml_declaration=True)+b'\n'


def main() -> None:
	contracts = json.loads((DATA / "source_contract.json").read_text())
	OUTPUT.mkdir(parents=True, exist_ok=True)
	for name, contract in contracts.items():
		(OUTPUT / f"{name}.drawn.svg").write_bytes(build(name, contract))


if __name__ == "__main__":
	main()
