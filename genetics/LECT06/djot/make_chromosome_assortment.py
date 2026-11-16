#!/usr/bin/env python3
"""Generate retained LECT06 figures using shared chromosome bodies."""
import json
import re
import pathlib
import xml.etree.ElementTree as ET
import svg_tools.chromosomes

NS='{http://www.w3.org/2000/svg}'


def generate(data_directory: pathlib.Path, output_directory: pathlib.Path) -> None:
	ET.register_namespace('',NS[1:-1])
	output_directory.mkdir(parents=True, exist_ok=True)
	directory=data_directory
	for data_file in sorted(directory.glob('*.json')):
		data=json.loads(data_file.read_text()); root=ET.parse(data_file.with_suffix('.template.svg')).getroot()
		groups={e.get('id'):e for e in root.iter() if e.get('id')}
		for item in data['placements']:
			markers=[]
			for i,body in enumerate(item['parts']):
				segments=body.get('segments') or [[body['color'],1],[body['color'],1]]
				model=svg_tools.chromosomes.Chromosome(tuple(svg_tools.chromosomes.Segment('',color,length) for color,length in segments),1 if item['centromere'] else None)
				part=svg_tools.chromosomes.chromosome_path_part(item['group']+'-shared-'+str(i),model,body['path'],thickness=body['width'],labels=False)
				fragment=ET.fromstring(part.fragment)
				marker=next((e for e in fragment.iter() if e.get('id','').endswith('-centromere')),None)
				if marker is not None:
					marker_parent=next(e for e in fragment.iter() if marker in list(e)); marker_parent.remove(marker)
					markers.append(marker)
				groups[item['group']].append(fragment)
			group=groups[item['group']]
			pair_size=2 if len(markers) in (2,4) else 1
			for start in range(0,len(markers),pair_size):
				pair=markers[start:start+pair_size]; marker=pair[0]
				for axis in ('cx','cy'):
					marker.set(axis,str(sum(float(e.get(axis)) for e in pair)/len(pair)))
				if item.get('marker_centers'):
					cx,cy=item['marker_centers'][start//pair_size]
					marker.set('cx',str(cx)); marker.set('cy',str(cy))
				angle=re.match(r'rotate\(([^ ]+)',marker.get('transform')).group(1)
				marker.set('transform',f"rotate({angle} {marker.get('cx')} {marker.get('cy')})")
				group.append(marker)
		output=output_directory/(data_file.stem+'.drawn.svg'); output.write_text(ET.tostring(root,encoding='unicode')+'\n')
	
		print(output.name)


def main() -> None:
	directory = pathlib.Path(__file__).resolve().parent
	generate(directory / "chromosome_models" / "assortment", directory / "assets" / "lect06c-meiosis")


if __name__ == "__main__":
	main()
