#!/usr/bin/env python3
"""Generate retained LECT06 figures using shared chromosome bodies."""
import argparse
import json
import math
import svgpathtools
import svg_tools.parts
import pathlib
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as DET
import svg_tools.chromosomes
import subprocess
import svg_tools.drawing

NS='{http://www.w3.org/2000/svg}'
REPOSITORY_ROOT = pathlib.Path(subprocess.check_output(
	['git', 'rev-parse', '--show-toplevel'], text=True).strip())
DIRECTORY = REPOSITORY_ROOT / 'genetics/LECT06/djot'


def generate(data_directory: pathlib.Path, output_directory: pathlib.Path) -> None:
	ET.register_namespace('',NS[1:-1])
	output_directory.mkdir(parents=True, exist_ok=True)
	directory=data_directory
	for data_file in sorted(directory.glob('*.json')):
		data=json.loads(data_file.read_text()); root=DET.parse(data_file.with_suffix('.template.svg')).getroot()
		groups={e.get('id'):e for e in root.iter() if e.get('id')}
		for item in data['placements']:
			markers=[]
			for i,body in enumerate(item['parts']):
				segments=body.get('segments') or [[body['color'],1],[body['color'],1]]
				model=svg_tools.chromosomes.Chromosome(tuple(svg_tools.chromosomes.Segment('',color,length) for color,length in segments),
					centromeres=(svg_tools.chromosomes.Centromere(1),) if item['centromere'] else ())
				part=svg_tools.chromosomes.chromosome_path_part(item['group']+'-shared-'+str(i),model,body['path'],thickness=body['width'],labels=False)
				fragment=DET.fromstring(part.fragment)
				marker=next((e for e in fragment.iter() if '-centromere-' in e.get('id','')),None)
				if marker is not None:
					marker_parent=next(e for e in fragment.iter() if marker in list(e)); marker_parent.remove(marker)
					markers.append((part.anchors['centromere'], body['width'], body['path']))
				groups[item['group']].append(fragment)
			group=groups[item['group']]
			pair_size=2 if len(markers) in (2,4) else 1
			for start in range(0,len(markers),pair_size):
				pair=markers[start:start+pair_size]
				centers = [entry[0] for entry in pair]
				cx, cy = (sum(point[index] for point in centers)/len(centers) for index in (0, 1))
				if item.get('marker_centers'):
					cx,cy=item['marker_centers'][start//pair_size]
				width = max(entry[1] for entry in pair)
				if len(pair) == 2:
					dx, dy = centers[1][0]-centers[0][0], centers[1][1]-centers[0][1]
					angle = math.degrees(math.atan2(dy, dx))-90
					span = math.hypot(dx,dy)+width*1.3
				else:
					path = svgpathtools.parse_path(pair[0][2])
					tangent = path.unit_tangent(path.ilength(path.length()/2))
					angle = math.degrees(math.atan2(tangent.imag, tangent.real))
					span = width*1.3
				marker = svg_tools.chromosomes.centromere_part(item['group']+'-belt-'+str(start),
					thickness=width, across=span)
				group.append(DET.fromstring(svg_tools.parts.transform(marker,x=cx,y=cy,rotation=angle).fragment))
		svg_tools.drawing.remove_canvas_background(root)
		output=output_directory/(data_file.stem+'.drawn.svg'); output.write_text(ET.tostring(root,encoding='unicode')+'\n')

		print(output.name)


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--output-root', type=pathlib.Path,
		default=DIRECTORY / 'assets')
	args = parser.parse_args()
	generate(DIRECTORY / "chromosome_models" / "assortment", args.output_root / "lect06c-meiosis")


if __name__ == "__main__":
	main()
