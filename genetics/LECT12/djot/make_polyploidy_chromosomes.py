#!/usr/bin/env python3
"""Regenerate LECT12B schematic chromosomes with the shared v2 renderer.

Run from the repository root: PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B genetics/LECT12/djot/make_polyploidy_chromosomes.py
Source cell outlines, connectors and labels are fixed local composition data.
Counts and reveal states follow the source, including illustrative body counts
that differ from adjacent native ploidy notation; no extra bodies are inferred.
"""

from pathlib import Path
import defusedxml.ElementTree as ET

from svg_tools.chromosomes import Centromere, Chromosome, Segment, chromosome_part, chromosome_path_part

NS = "{http://www.w3.org/2000/svg}"
ET.register_namespace("", NS[1:-1])
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
BASE = Path(__file__).resolve().parent


def chromosome(spec: dict) -> str:
	name, color = spec['name'] + '-v2', spec['color']
	if 'curve' in spec:
		part = chromosome_path_part(name, Chromosome((Segment('', color),)),
			spec['curve'], thickness=spec['thickness'], labels=False)
	else:
		fraction = spec.get('fraction', .5)
		model = Chromosome((Segment('', color, fraction), Segment('', color, 1-fraction)),
			centromeres=(Centromere(1),))
		thickness = spec['thickness'] / (2.2 if spec.get('sisters', False) else 1)
		part = chromosome_part(name, model, length=spec['length'], thickness=thickness,
			orientation=spec.get('orientation', 'vertical'), texture=False,
			sisters=spec.get('sisters', False), labels=False)
	return '<g data-chromosome="' + name + '" data-sisters="' + str(spec.get('sisters', False)).lower() + '" transform="' + spec.get('transform', '') + '">' + part.fragment + '</g>'


FIGURES = [
	('assets/visual_renewal/chrysanthemum_72_90.drawn.svg',
		'<svg xmlns="http://www.w3.org/2000/svg" width="520" height="848" viewBox="0 0 520 848" role="img" aria-labelledby="title desc"><title id="title">Chrysanthemum polyploid comparison</title><desc id="desc">Schematic chromosome types retain stable color and shape. Each row contains one complete set of nine types. Each enclosing outline represents one cell.</desc><rect width="520" height="848" fill="white" />\n<g id="cell-8-40-45" data-sets="8" data-chromosomes="72"><rect x="25" y="20" width="460" height="308" rx="35" fill="#F3F6F8" stroke="#647681" stroke-width="2" />\n<g data-recipe-slot="0" /><g data-recipe-slot="1" /><g data-recipe-slot="2" /><g data-recipe-slot="3" /><g data-recipe-slot="4" /><g data-recipe-slot="5" /><g data-recipe-slot="6" /><g data-recipe-slot="7" /><g data-recipe-slot="8" /><g data-recipe-slot="9" /><g data-recipe-slot="10" /><g data-recipe-slot="11" /><g data-recipe-slot="12" /><g data-recipe-slot="13" /><g data-recipe-slot="14" /><g data-recipe-slot="15" /><g data-recipe-slot="16" /><g data-recipe-slot="17" /><g data-recipe-slot="18" /><g data-recipe-slot="19" /><g data-recipe-slot="20" /><g data-recipe-slot="21" /><g data-recipe-slot="22" /><g data-recipe-slot="23" /><g data-recipe-slot="24" /><g data-recipe-slot="25" /><g data-recipe-slot="26" /><g data-recipe-slot="27" /><g data-recipe-slot="28" /><g data-recipe-slot="29" /><g data-recipe-slot="30" /><g data-recipe-slot="31" /><g data-recipe-slot="32" /><g data-recipe-slot="33" /><g data-recipe-slot="34" /><g data-recipe-slot="35" /><g data-recipe-slot="36" /><g data-recipe-slot="37" /><g data-recipe-slot="38" /><g data-recipe-slot="39" /><g data-recipe-slot="40" /><g data-recipe-slot="41" /><g data-recipe-slot="42" /><g data-recipe-slot="43" /><g data-recipe-slot="44" /><g data-recipe-slot="45" /><g data-recipe-slot="46" /><g data-recipe-slot="47" /><g data-recipe-slot="48" /><g data-recipe-slot="49" /><g data-recipe-slot="50" /><g data-recipe-slot="51" /><g data-recipe-slot="52" /><g data-recipe-slot="53" /><g data-recipe-slot="54" /><g data-recipe-slot="55" /><g data-recipe-slot="56" /><g data-recipe-slot="57" /><g data-recipe-slot="58" /><g data-recipe-slot="59" /><g data-recipe-slot="60" /><g data-recipe-slot="61" /><g data-recipe-slot="62" /><g data-recipe-slot="63" /><g data-recipe-slot="64" /><g data-recipe-slot="65" /><g data-recipe-slot="66" /><g data-recipe-slot="67" /><g data-recipe-slot="68" /><g data-recipe-slot="69" /><g data-recipe-slot="70" /><g data-recipe-slot="71" /></g>\n<text x="255" y="373" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="26" text-anchor="middle" fill="#222">Octoploid (72)</text>\n<g id="cell-10-40-433" data-sets="10" data-chromosomes="90"><rect x="25" y="408" width="460" height="380" rx="35" fill="#F3F6F8" stroke="#647681" stroke-width="2" />\n<g data-recipe-slot="72" /><g data-recipe-slot="73" /><g data-recipe-slot="74" /><g data-recipe-slot="75" /><g data-recipe-slot="76" /><g data-recipe-slot="77" /><g data-recipe-slot="78" /><g data-recipe-slot="79" /><g data-recipe-slot="80" /><g data-recipe-slot="81" /><g data-recipe-slot="82" /><g data-recipe-slot="83" /><g data-recipe-slot="84" /><g data-recipe-slot="85" /><g data-recipe-slot="86" /><g data-recipe-slot="87" /><g data-recipe-slot="88" /><g data-recipe-slot="89" /><g data-recipe-slot="90" /><g data-recipe-slot="91" /><g data-recipe-slot="92" /><g data-recipe-slot="93" /><g data-recipe-slot="94" /><g data-recipe-slot="95" /><g data-recipe-slot="96" /><g data-recipe-slot="97" /><g data-recipe-slot="98" /><g data-recipe-slot="99" /><g data-recipe-slot="100" /><g data-recipe-slot="101" /><g data-recipe-slot="102" /><g data-recipe-slot="103" /><g data-recipe-slot="104" /><g data-recipe-slot="105" /><g data-recipe-slot="106" /><g data-recipe-slot="107" /><g data-recipe-slot="108" /><g data-recipe-slot="109" /><g data-recipe-slot="110" /><g data-recipe-slot="111" /><g data-recipe-slot="112" /><g data-recipe-slot="113" /><g data-recipe-slot="114" /><g data-recipe-slot="115" /><g data-recipe-slot="116" /><g data-recipe-slot="117" /><g data-recipe-slot="118" /><g data-recipe-slot="119" /><g data-recipe-slot="120" /><g data-recipe-slot="121" /><g data-recipe-slot="122" /><g data-recipe-slot="123" /><g data-recipe-slot="124" /><g data-recipe-slot="125" /><g data-recipe-slot="126" /><g data-recipe-slot="127" /><g data-recipe-slot="128" /><g data-recipe-slot="129" /><g data-recipe-slot="130" /><g data-recipe-slot="131" /><g data-recipe-slot="132" /><g data-recipe-slot="133" /><g data-recipe-slot="134" /><g data-recipe-slot="135" /><g data-recipe-slot="136" /><g data-recipe-slot="137" /><g data-recipe-slot="138" /><g data-recipe-slot="139" /><g data-recipe-slot="140" /><g data-recipe-slot="141" /><g data-recipe-slot="142" /><g data-recipe-slot="143" /><g data-recipe-slot="144" /><g data-recipe-slot="145" /><g data-recipe-slot="146" /><g data-recipe-slot="147" /><g data-recipe-slot="148" /><g data-recipe-slot="149" /><g data-recipe-slot="150" /><g data-recipe-slot="151" /><g data-recipe-slot="152" /><g data-recipe-slot="153" /><g data-recipe-slot="154" /><g data-recipe-slot="155" /><g data-recipe-slot="156" /><g data-recipe-slot="157" /><g data-recipe-slot="158" /><g data-recipe-slot="159" /><g data-recipe-slot="160" /><g data-recipe-slot="161" /></g>\n<text x="255" y="833" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="26" text-anchor="middle" fill="#222">Decaploid (90)</text>\n</svg>',
		[
			{'name': 'set-8-40-45-0-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,45)'},
			{'name': 'set-8-40-45-0-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,45)'},
			{'name': 'set-8-40-45-0-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,45)'},
			{'name': 'set-8-40-45-0-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,45)'},
			{'name': 'set-8-40-45-0-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,45)'},
			{'name': 'set-8-40-45-0-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,45)'},
			{'name': 'set-8-40-45-0-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,45)'},
			{'name': 'set-8-40-45-0-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,45)'},
			{'name': 'set-8-40-45-0-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,45)'},
			{'name': 'set-8-40-45-1-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,81)'},
			{'name': 'set-8-40-45-1-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,81)'},
			{'name': 'set-8-40-45-1-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,81)'},
			{'name': 'set-8-40-45-1-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,81)'},
			{'name': 'set-8-40-45-1-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,81)'},
			{'name': 'set-8-40-45-1-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,81)'},
			{'name': 'set-8-40-45-1-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,81)'},
			{'name': 'set-8-40-45-1-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,81)'},
			{'name': 'set-8-40-45-1-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,81)'},
			{'name': 'set-8-40-45-2-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,117)'},
			{'name': 'set-8-40-45-2-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,117)'},
			{'name': 'set-8-40-45-2-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,117)'},
			{'name': 'set-8-40-45-2-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,117)'},
			{'name': 'set-8-40-45-2-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,117)'},
			{'name': 'set-8-40-45-2-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,117)'},
			{'name': 'set-8-40-45-2-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,117)'},
			{'name': 'set-8-40-45-2-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,117)'},
			{'name': 'set-8-40-45-2-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,117)'},
			{'name': 'set-8-40-45-3-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,153)'},
			{'name': 'set-8-40-45-3-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,153)'},
			{'name': 'set-8-40-45-3-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,153)'},
			{'name': 'set-8-40-45-3-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,153)'},
			{'name': 'set-8-40-45-3-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,153)'},
			{'name': 'set-8-40-45-3-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,153)'},
			{'name': 'set-8-40-45-3-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,153)'},
			{'name': 'set-8-40-45-3-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,153)'},
			{'name': 'set-8-40-45-3-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,153)'},
			{'name': 'set-8-40-45-4-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,189)'},
			{'name': 'set-8-40-45-4-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,189)'},
			{'name': 'set-8-40-45-4-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,189)'},
			{'name': 'set-8-40-45-4-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,189)'},
			{'name': 'set-8-40-45-4-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,189)'},
			{'name': 'set-8-40-45-4-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,189)'},
			{'name': 'set-8-40-45-4-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,189)'},
			{'name': 'set-8-40-45-4-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,189)'},
			{'name': 'set-8-40-45-4-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,189)'},
			{'name': 'set-8-40-45-5-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,225)'},
			{'name': 'set-8-40-45-5-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,225)'},
			{'name': 'set-8-40-45-5-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,225)'},
			{'name': 'set-8-40-45-5-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,225)'},
			{'name': 'set-8-40-45-5-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,225)'},
			{'name': 'set-8-40-45-5-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,225)'},
			{'name': 'set-8-40-45-5-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,225)'},
			{'name': 'set-8-40-45-5-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,225)'},
			{'name': 'set-8-40-45-5-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,225)'},
			{'name': 'set-8-40-45-6-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,261)'},
			{'name': 'set-8-40-45-6-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,261)'},
			{'name': 'set-8-40-45-6-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,261)'},
			{'name': 'set-8-40-45-6-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,261)'},
			{'name': 'set-8-40-45-6-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,261)'},
			{'name': 'set-8-40-45-6-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,261)'},
			{'name': 'set-8-40-45-6-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,261)'},
			{'name': 'set-8-40-45-6-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,261)'},
			{'name': 'set-8-40-45-6-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,261)'},
			{'name': 'set-8-40-45-7-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,297)'},
			{'name': 'set-8-40-45-7-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,297)'},
			{'name': 'set-8-40-45-7-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,297)'},
			{'name': 'set-8-40-45-7-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,297)'},
			{'name': 'set-8-40-45-7-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,297)'},
			{'name': 'set-8-40-45-7-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,297)'},
			{'name': 'set-8-40-45-7-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,297)'},
			{'name': 'set-8-40-45-7-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,297)'},
			{'name': 'set-8-40-45-7-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,297)'},
			{'name': 'set-10-40-433-0-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,433)'},
			{'name': 'set-10-40-433-0-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,433)'},
			{'name': 'set-10-40-433-0-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,433)'},
			{'name': 'set-10-40-433-0-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,433)'},
			{'name': 'set-10-40-433-0-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,433)'},
			{'name': 'set-10-40-433-0-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,433)'},
			{'name': 'set-10-40-433-0-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,433)'},
			{'name': 'set-10-40-433-0-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,433)'},
			{'name': 'set-10-40-433-0-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,433)'},
			{'name': 'set-10-40-433-1-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,469)'},
			{'name': 'set-10-40-433-1-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,469)'},
			{'name': 'set-10-40-433-1-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,469)'},
			{'name': 'set-10-40-433-1-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,469)'},
			{'name': 'set-10-40-433-1-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,469)'},
			{'name': 'set-10-40-433-1-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,469)'},
			{'name': 'set-10-40-433-1-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,469)'},
			{'name': 'set-10-40-433-1-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,469)'},
			{'name': 'set-10-40-433-1-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,469)'},
			{'name': 'set-10-40-433-2-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,505)'},
			{'name': 'set-10-40-433-2-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,505)'},
			{'name': 'set-10-40-433-2-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,505)'},
			{'name': 'set-10-40-433-2-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,505)'},
			{'name': 'set-10-40-433-2-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,505)'},
			{'name': 'set-10-40-433-2-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,505)'},
			{'name': 'set-10-40-433-2-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,505)'},
			{'name': 'set-10-40-433-2-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,505)'},
			{'name': 'set-10-40-433-2-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,505)'},
			{'name': 'set-10-40-433-3-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,541)'},
			{'name': 'set-10-40-433-3-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,541)'},
			{'name': 'set-10-40-433-3-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,541)'},
			{'name': 'set-10-40-433-3-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,541)'},
			{'name': 'set-10-40-433-3-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,541)'},
			{'name': 'set-10-40-433-3-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,541)'},
			{'name': 'set-10-40-433-3-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,541)'},
			{'name': 'set-10-40-433-3-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,541)'},
			{'name': 'set-10-40-433-3-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,541)'},
			{'name': 'set-10-40-433-4-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,577)'},
			{'name': 'set-10-40-433-4-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,577)'},
			{'name': 'set-10-40-433-4-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,577)'},
			{'name': 'set-10-40-433-4-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,577)'},
			{'name': 'set-10-40-433-4-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,577)'},
			{'name': 'set-10-40-433-4-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,577)'},
			{'name': 'set-10-40-433-4-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,577)'},
			{'name': 'set-10-40-433-4-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,577)'},
			{'name': 'set-10-40-433-4-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,577)'},
			{'name': 'set-10-40-433-5-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,613)'},
			{'name': 'set-10-40-433-5-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,613)'},
			{'name': 'set-10-40-433-5-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,613)'},
			{'name': 'set-10-40-433-5-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,613)'},
			{'name': 'set-10-40-433-5-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,613)'},
			{'name': 'set-10-40-433-5-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,613)'},
			{'name': 'set-10-40-433-5-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,613)'},
			{'name': 'set-10-40-433-5-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,613)'},
			{'name': 'set-10-40-433-5-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,613)'},
			{'name': 'set-10-40-433-6-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,649)'},
			{'name': 'set-10-40-433-6-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,649)'},
			{'name': 'set-10-40-433-6-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,649)'},
			{'name': 'set-10-40-433-6-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,649)'},
			{'name': 'set-10-40-433-6-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,649)'},
			{'name': 'set-10-40-433-6-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,649)'},
			{'name': 'set-10-40-433-6-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,649)'},
			{'name': 'set-10-40-433-6-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,649)'},
			{'name': 'set-10-40-433-6-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,649)'},
			{'name': 'set-10-40-433-7-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,685)'},
			{'name': 'set-10-40-433-7-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,685)'},
			{'name': 'set-10-40-433-7-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,685)'},
			{'name': 'set-10-40-433-7-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,685)'},
			{'name': 'set-10-40-433-7-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,685)'},
			{'name': 'set-10-40-433-7-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,685)'},
			{'name': 'set-10-40-433-7-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,685)'},
			{'name': 'set-10-40-433-7-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,685)'},
			{'name': 'set-10-40-433-7-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,685)'},
			{'name': 'set-10-40-433-8-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,721)'},
			{'name': 'set-10-40-433-8-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,721)'},
			{'name': 'set-10-40-433-8-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,721)'},
			{'name': 'set-10-40-433-8-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,721)'},
			{'name': 'set-10-40-433-8-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,721)'},
			{'name': 'set-10-40-433-8-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,721)'},
			{'name': 'set-10-40-433-8-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,721)'},
			{'name': 'set-10-40-433-8-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,721)'},
			{'name': 'set-10-40-433-8-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,721)'},
			{'name': 'set-10-40-433-9-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,757)'},
			{'name': 'set-10-40-433-9-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,757)'},
			{'name': 'set-10-40-433-9-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,757)'},
			{'name': 'set-10-40-433-9-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,757)'},
			{'name': 'set-10-40-433-9-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,757)'},
			{'name': 'set-10-40-433-9-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,757)'},
			{'name': 'set-10-40-433-9-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,757)'},
			{'name': 'set-10-40-433-9-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,757)'},
			{'name': 'set-10-40-433-9-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,757)'},
		]),
	('assets/visual_renewal/chrysanthemum_54_72.drawn.svg',
		'<svg xmlns="http://www.w3.org/2000/svg" width="520" height="704" viewBox="0 0 520 704" role="img" aria-labelledby="title desc"><title id="title">Chrysanthemum polyploid comparison</title><desc id="desc">Schematic chromosome types retain stable color and shape. Each row contains one complete set of nine types. Each enclosing outline represents one cell.</desc><rect width="520" height="704" fill="white" />\n<g id="cell-6-40-45" data-sets="6" data-chromosomes="54"><rect x="25" y="20" width="460" height="236" rx="35" fill="#F3F6F8" stroke="#647681" stroke-width="2" />\n<g data-recipe-slot="0" /><g data-recipe-slot="1" /><g data-recipe-slot="2" /><g data-recipe-slot="3" /><g data-recipe-slot="4" /><g data-recipe-slot="5" /><g data-recipe-slot="6" /><g data-recipe-slot="7" /><g data-recipe-slot="8" /><g data-recipe-slot="9" /><g data-recipe-slot="10" /><g data-recipe-slot="11" /><g data-recipe-slot="12" /><g data-recipe-slot="13" /><g data-recipe-slot="14" /><g data-recipe-slot="15" /><g data-recipe-slot="16" /><g data-recipe-slot="17" /><g data-recipe-slot="18" /><g data-recipe-slot="19" /><g data-recipe-slot="20" /><g data-recipe-slot="21" /><g data-recipe-slot="22" /><g data-recipe-slot="23" /><g data-recipe-slot="24" /><g data-recipe-slot="25" /><g data-recipe-slot="26" /><g data-recipe-slot="27" /><g data-recipe-slot="28" /><g data-recipe-slot="29" /><g data-recipe-slot="30" /><g data-recipe-slot="31" /><g data-recipe-slot="32" /><g data-recipe-slot="33" /><g data-recipe-slot="34" /><g data-recipe-slot="35" /><g data-recipe-slot="36" /><g data-recipe-slot="37" /><g data-recipe-slot="38" /><g data-recipe-slot="39" /><g data-recipe-slot="40" /><g data-recipe-slot="41" /><g data-recipe-slot="42" /><g data-recipe-slot="43" /><g data-recipe-slot="44" /><g data-recipe-slot="45" /><g data-recipe-slot="46" /><g data-recipe-slot="47" /><g data-recipe-slot="48" /><g data-recipe-slot="49" /><g data-recipe-slot="50" /><g data-recipe-slot="51" /><g data-recipe-slot="52" /><g data-recipe-slot="53" /></g>\n<text x="255" y="301" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="26" text-anchor="middle" fill="#222">Hexaploid (54)</text>\n<g id="cell-8-40-361" data-sets="8" data-chromosomes="72"><rect x="25" y="336" width="460" height="308" rx="35" fill="#F3F6F8" stroke="#647681" stroke-width="2" />\n<g data-recipe-slot="54" /><g data-recipe-slot="55" /><g data-recipe-slot="56" /><g data-recipe-slot="57" /><g data-recipe-slot="58" /><g data-recipe-slot="59" /><g data-recipe-slot="60" /><g data-recipe-slot="61" /><g data-recipe-slot="62" /><g data-recipe-slot="63" /><g data-recipe-slot="64" /><g data-recipe-slot="65" /><g data-recipe-slot="66" /><g data-recipe-slot="67" /><g data-recipe-slot="68" /><g data-recipe-slot="69" /><g data-recipe-slot="70" /><g data-recipe-slot="71" /><g data-recipe-slot="72" /><g data-recipe-slot="73" /><g data-recipe-slot="74" /><g data-recipe-slot="75" /><g data-recipe-slot="76" /><g data-recipe-slot="77" /><g data-recipe-slot="78" /><g data-recipe-slot="79" /><g data-recipe-slot="80" /><g data-recipe-slot="81" /><g data-recipe-slot="82" /><g data-recipe-slot="83" /><g data-recipe-slot="84" /><g data-recipe-slot="85" /><g data-recipe-slot="86" /><g data-recipe-slot="87" /><g data-recipe-slot="88" /><g data-recipe-slot="89" /><g data-recipe-slot="90" /><g data-recipe-slot="91" /><g data-recipe-slot="92" /><g data-recipe-slot="93" /><g data-recipe-slot="94" /><g data-recipe-slot="95" /><g data-recipe-slot="96" /><g data-recipe-slot="97" /><g data-recipe-slot="98" /><g data-recipe-slot="99" /><g data-recipe-slot="100" /><g data-recipe-slot="101" /><g data-recipe-slot="102" /><g data-recipe-slot="103" /><g data-recipe-slot="104" /><g data-recipe-slot="105" /><g data-recipe-slot="106" /><g data-recipe-slot="107" /><g data-recipe-slot="108" /><g data-recipe-slot="109" /><g data-recipe-slot="110" /><g data-recipe-slot="111" /><g data-recipe-slot="112" /><g data-recipe-slot="113" /><g data-recipe-slot="114" /><g data-recipe-slot="115" /><g data-recipe-slot="116" /><g data-recipe-slot="117" /><g data-recipe-slot="118" /><g data-recipe-slot="119" /><g data-recipe-slot="120" /><g data-recipe-slot="121" /><g data-recipe-slot="122" /><g data-recipe-slot="123" /><g data-recipe-slot="124" /><g data-recipe-slot="125" /></g>\n<text x="255" y="689" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="26" text-anchor="middle" fill="#222">Octoploid (72)</text>\n</svg>',
		[
			{'name': 'set-6-40-45-0-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,45)'},
			{'name': 'set-6-40-45-0-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,45)'},
			{'name': 'set-6-40-45-0-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,45)'},
			{'name': 'set-6-40-45-0-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,45)'},
			{'name': 'set-6-40-45-0-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,45)'},
			{'name': 'set-6-40-45-0-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,45)'},
			{'name': 'set-6-40-45-0-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,45)'},
			{'name': 'set-6-40-45-0-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,45)'},
			{'name': 'set-6-40-45-0-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,45)'},
			{'name': 'set-6-40-45-1-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,81)'},
			{'name': 'set-6-40-45-1-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,81)'},
			{'name': 'set-6-40-45-1-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,81)'},
			{'name': 'set-6-40-45-1-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,81)'},
			{'name': 'set-6-40-45-1-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,81)'},
			{'name': 'set-6-40-45-1-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,81)'},
			{'name': 'set-6-40-45-1-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,81)'},
			{'name': 'set-6-40-45-1-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,81)'},
			{'name': 'set-6-40-45-1-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,81)'},
			{'name': 'set-6-40-45-2-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,117)'},
			{'name': 'set-6-40-45-2-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,117)'},
			{'name': 'set-6-40-45-2-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,117)'},
			{'name': 'set-6-40-45-2-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,117)'},
			{'name': 'set-6-40-45-2-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,117)'},
			{'name': 'set-6-40-45-2-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,117)'},
			{'name': 'set-6-40-45-2-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,117)'},
			{'name': 'set-6-40-45-2-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,117)'},
			{'name': 'set-6-40-45-2-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,117)'},
			{'name': 'set-6-40-45-3-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,153)'},
			{'name': 'set-6-40-45-3-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,153)'},
			{'name': 'set-6-40-45-3-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,153)'},
			{'name': 'set-6-40-45-3-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,153)'},
			{'name': 'set-6-40-45-3-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,153)'},
			{'name': 'set-6-40-45-3-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,153)'},
			{'name': 'set-6-40-45-3-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,153)'},
			{'name': 'set-6-40-45-3-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,153)'},
			{'name': 'set-6-40-45-3-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,153)'},
			{'name': 'set-6-40-45-4-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,189)'},
			{'name': 'set-6-40-45-4-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,189)'},
			{'name': 'set-6-40-45-4-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,189)'},
			{'name': 'set-6-40-45-4-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,189)'},
			{'name': 'set-6-40-45-4-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,189)'},
			{'name': 'set-6-40-45-4-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,189)'},
			{'name': 'set-6-40-45-4-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,189)'},
			{'name': 'set-6-40-45-4-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,189)'},
			{'name': 'set-6-40-45-4-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,189)'},
			{'name': 'set-6-40-45-5-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,225)'},
			{'name': 'set-6-40-45-5-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,225)'},
			{'name': 'set-6-40-45-5-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,225)'},
			{'name': 'set-6-40-45-5-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,225)'},
			{'name': 'set-6-40-45-5-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,225)'},
			{'name': 'set-6-40-45-5-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,225)'},
			{'name': 'set-6-40-45-5-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,225)'},
			{'name': 'set-6-40-45-5-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,225)'},
			{'name': 'set-6-40-45-5-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,225)'},
			{'name': 'set-8-40-361-0-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,361)'},
			{'name': 'set-8-40-361-0-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,361)'},
			{'name': 'set-8-40-361-0-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,361)'},
			{'name': 'set-8-40-361-0-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,361)'},
			{'name': 'set-8-40-361-0-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,361)'},
			{'name': 'set-8-40-361-0-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,361)'},
			{'name': 'set-8-40-361-0-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,361)'},
			{'name': 'set-8-40-361-0-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,361)'},
			{'name': 'set-8-40-361-0-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,361)'},
			{'name': 'set-8-40-361-1-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,397)'},
			{'name': 'set-8-40-361-1-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,397)'},
			{'name': 'set-8-40-361-1-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,397)'},
			{'name': 'set-8-40-361-1-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,397)'},
			{'name': 'set-8-40-361-1-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,397)'},
			{'name': 'set-8-40-361-1-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,397)'},
			{'name': 'set-8-40-361-1-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,397)'},
			{'name': 'set-8-40-361-1-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,397)'},
			{'name': 'set-8-40-361-1-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,397)'},
			{'name': 'set-8-40-361-2-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,433)'},
			{'name': 'set-8-40-361-2-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,433)'},
			{'name': 'set-8-40-361-2-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,433)'},
			{'name': 'set-8-40-361-2-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,433)'},
			{'name': 'set-8-40-361-2-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,433)'},
			{'name': 'set-8-40-361-2-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,433)'},
			{'name': 'set-8-40-361-2-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,433)'},
			{'name': 'set-8-40-361-2-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,433)'},
			{'name': 'set-8-40-361-2-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,433)'},
			{'name': 'set-8-40-361-3-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,469)'},
			{'name': 'set-8-40-361-3-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,469)'},
			{'name': 'set-8-40-361-3-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,469)'},
			{'name': 'set-8-40-361-3-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,469)'},
			{'name': 'set-8-40-361-3-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,469)'},
			{'name': 'set-8-40-361-3-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,469)'},
			{'name': 'set-8-40-361-3-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,469)'},
			{'name': 'set-8-40-361-3-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,469)'},
			{'name': 'set-8-40-361-3-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,469)'},
			{'name': 'set-8-40-361-4-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,505)'},
			{'name': 'set-8-40-361-4-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,505)'},
			{'name': 'set-8-40-361-4-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,505)'},
			{'name': 'set-8-40-361-4-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,505)'},
			{'name': 'set-8-40-361-4-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,505)'},
			{'name': 'set-8-40-361-4-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,505)'},
			{'name': 'set-8-40-361-4-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,505)'},
			{'name': 'set-8-40-361-4-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,505)'},
			{'name': 'set-8-40-361-4-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,505)'},
			{'name': 'set-8-40-361-5-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,541)'},
			{'name': 'set-8-40-361-5-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,541)'},
			{'name': 'set-8-40-361-5-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,541)'},
			{'name': 'set-8-40-361-5-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,541)'},
			{'name': 'set-8-40-361-5-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,541)'},
			{'name': 'set-8-40-361-5-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,541)'},
			{'name': 'set-8-40-361-5-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,541)'},
			{'name': 'set-8-40-361-5-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,541)'},
			{'name': 'set-8-40-361-5-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,541)'},
			{'name': 'set-8-40-361-6-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,577)'},
			{'name': 'set-8-40-361-6-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,577)'},
			{'name': 'set-8-40-361-6-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,577)'},
			{'name': 'set-8-40-361-6-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,577)'},
			{'name': 'set-8-40-361-6-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,577)'},
			{'name': 'set-8-40-361-6-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,577)'},
			{'name': 'set-8-40-361-6-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,577)'},
			{'name': 'set-8-40-361-6-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,577)'},
			{'name': 'set-8-40-361-6-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,577)'},
			{'name': 'set-8-40-361-7-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,613)'},
			{'name': 'set-8-40-361-7-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,613)'},
			{'name': 'set-8-40-361-7-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,613)'},
			{'name': 'set-8-40-361-7-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,613)'},
			{'name': 'set-8-40-361-7-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,613)'},
			{'name': 'set-8-40-361-7-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,613)'},
			{'name': 'set-8-40-361-7-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,613)'},
			{'name': 'set-8-40-361-7-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,613)'},
			{'name': 'set-8-40-361-7-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,613)'},
		]),
	('assets/visual_renewal/chrysanthemum_monoploid.drawn.svg',
		'<svg xmlns="http://www.w3.org/2000/svg" width="260" height="620" viewBox="0 0 260 620" role="img" aria-labelledby="title desc"><title id="title">One monoploid set: nine chromosome types</title><desc id="desc">Schematic chromosome types retain stable color and shape. Each row contains one complete set of nine types. Each enclosing outline represents one cell.</desc><rect width="260" height="620" fill="white" />\n<g data-recipe-slot="0" /><g data-recipe-slot="1" /><g data-recipe-slot="2" /><g data-recipe-slot="3" /><g data-recipe-slot="4" /><g data-recipe-slot="5" /><g data-recipe-slot="6" /><g data-recipe-slot="7" /><g data-recipe-slot="8" /><text x="130" y="555" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="26" text-anchor="middle" fill="#222">Monoploid set</text>\n<text x="130" y="590" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="24" text-anchor="middle" fill="#222">9 chromosomes</text>\n</svg>',
		[
			{'name': 'type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(130,55) scale(1.5)'},
			{'name': 'type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(130,107) scale(1.5)'},
			{'name': 'type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(130,159) scale(1.5)'},
			{'name': 'type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(130,211) scale(1.5)'},
			{'name': 'type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(130,263) scale(1.5)'},
			{'name': 'type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(130,315) scale(1.5)'},
			{'name': 'type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(130,367) scale(1.5)'},
			{'name': 'type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(130,419) scale(1.5)'},
			{'name': 'type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(130,471) scale(1.5)'},
		]),
	('assets/visual_renewal/chrysanthemum_18_36.drawn.svg',
		'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="630" viewBox="0 0 1100 630" role="img" aria-labelledby="title desc"><title id="title">Chrysanthemum chromosome sets</title><desc id="desc">Schematic chromosome types retain stable color and shape. Each row contains one complete set of nine types. Each enclosing outline represents one cell.</desc><rect width="1100" height="630" fill="white" />\n<g id="cell-1-50-240" data-sets="1" data-chromosomes="9"><rect x="35" y="215" width="460" height="56" rx="35" fill="#F3F6F8" stroke="#647681" stroke-width="2" />\n<g data-recipe-slot="0" /><g data-recipe-slot="1" /><g data-recipe-slot="2" /><g data-recipe-slot="3" /><g data-recipe-slot="4" /><g data-recipe-slot="5" /><g data-recipe-slot="6" /><g data-recipe-slot="7" /><g data-recipe-slot="8" /></g>\n<text x="265" y="335" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="26" text-anchor="middle" fill="#222">Monoploid set: 9</text>\n<g id="cell-2-620-100" data-sets="2" data-chromosomes="18"><rect x="605" y="75" width="460" height="92" rx="35" fill="#F3F6F8" stroke="#647681" stroke-width="2" />\n<g data-recipe-slot="9" /><g data-recipe-slot="10" /><g data-recipe-slot="11" /><g data-recipe-slot="12" /><g data-recipe-slot="13" /><g data-recipe-slot="14" /><g data-recipe-slot="15" /><g data-recipe-slot="16" /><g data-recipe-slot="17" /><g data-recipe-slot="18" /><g data-recipe-slot="19" /><g data-recipe-slot="20" /><g data-recipe-slot="21" /><g data-recipe-slot="22" /><g data-recipe-slot="23" /><g data-recipe-slot="24" /><g data-recipe-slot="25" /><g data-recipe-slot="26" /></g>\n<text x="835" y="212" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="26" text-anchor="middle" fill="#222">Diploid (18)</text>\n<g id="cell-4-620-365" data-sets="4" data-chromosomes="36"><rect x="605" y="340" width="460" height="164" rx="35" fill="#F3F6F8" stroke="#647681" stroke-width="2" />\n<g data-recipe-slot="27" /><g data-recipe-slot="28" /><g data-recipe-slot="29" /><g data-recipe-slot="30" /><g data-recipe-slot="31" /><g data-recipe-slot="32" /><g data-recipe-slot="33" /><g data-recipe-slot="34" /><g data-recipe-slot="35" /><g data-recipe-slot="36" /><g data-recipe-slot="37" /><g data-recipe-slot="38" /><g data-recipe-slot="39" /><g data-recipe-slot="40" /><g data-recipe-slot="41" /><g data-recipe-slot="42" /><g data-recipe-slot="43" /><g data-recipe-slot="44" /><g data-recipe-slot="45" /><g data-recipe-slot="46" /><g data-recipe-slot="47" /><g data-recipe-slot="48" /><g data-recipe-slot="49" /><g data-recipe-slot="50" /><g data-recipe-slot="51" /><g data-recipe-slot="52" /><g data-recipe-slot="53" /><g data-recipe-slot="54" /><g data-recipe-slot="55" /><g data-recipe-slot="56" /><g data-recipe-slot="57" /><g data-recipe-slot="58" /><g data-recipe-slot="59" /><g data-recipe-slot="60" /><g data-recipe-slot="61" /><g data-recipe-slot="62" /></g>\n<text x="835" y="549" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="26" text-anchor="middle" fill="#222">Tetraploid (36)</text>\n</svg>',
		[
			{'name': 'set-1-50-240-0-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(65,240)'},
			{'name': 'set-1-50-240-0-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(115,240)'},
			{'name': 'set-1-50-240-0-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(165,240)'},
			{'name': 'set-1-50-240-0-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(215,240)'},
			{'name': 'set-1-50-240-0-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(265,240)'},
			{'name': 'set-1-50-240-0-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(315,240)'},
			{'name': 'set-1-50-240-0-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(365,240)'},
			{'name': 'set-1-50-240-0-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(415,240)'},
			{'name': 'set-1-50-240-0-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(465,240)'},
			{'name': 'set-2-620-100-0-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(635,100)'},
			{'name': 'set-2-620-100-0-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(685,100)'},
			{'name': 'set-2-620-100-0-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(735,100)'},
			{'name': 'set-2-620-100-0-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(785,100)'},
			{'name': 'set-2-620-100-0-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(835,100)'},
			{'name': 'set-2-620-100-0-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(885,100)'},
			{'name': 'set-2-620-100-0-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(935,100)'},
			{'name': 'set-2-620-100-0-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(985,100)'},
			{'name': 'set-2-620-100-0-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(1035,100)'},
			{'name': 'set-2-620-100-1-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(635,136)'},
			{'name': 'set-2-620-100-1-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(685,136)'},
			{'name': 'set-2-620-100-1-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(735,136)'},
			{'name': 'set-2-620-100-1-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(785,136)'},
			{'name': 'set-2-620-100-1-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(835,136)'},
			{'name': 'set-2-620-100-1-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(885,136)'},
			{'name': 'set-2-620-100-1-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(935,136)'},
			{'name': 'set-2-620-100-1-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(985,136)'},
			{'name': 'set-2-620-100-1-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(1035,136)'},
			{'name': 'set-4-620-365-0-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(635,365)'},
			{'name': 'set-4-620-365-0-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(685,365)'},
			{'name': 'set-4-620-365-0-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(735,365)'},
			{'name': 'set-4-620-365-0-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(785,365)'},
			{'name': 'set-4-620-365-0-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(835,365)'},
			{'name': 'set-4-620-365-0-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(885,365)'},
			{'name': 'set-4-620-365-0-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(935,365)'},
			{'name': 'set-4-620-365-0-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(985,365)'},
			{'name': 'set-4-620-365-0-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(1035,365)'},
			{'name': 'set-4-620-365-1-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(635,401)'},
			{'name': 'set-4-620-365-1-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(685,401)'},
			{'name': 'set-4-620-365-1-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(735,401)'},
			{'name': 'set-4-620-365-1-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(785,401)'},
			{'name': 'set-4-620-365-1-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(835,401)'},
			{'name': 'set-4-620-365-1-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(885,401)'},
			{'name': 'set-4-620-365-1-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(935,401)'},
			{'name': 'set-4-620-365-1-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(985,401)'},
			{'name': 'set-4-620-365-1-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(1035,401)'},
			{'name': 'set-4-620-365-2-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(635,437)'},
			{'name': 'set-4-620-365-2-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(685,437)'},
			{'name': 'set-4-620-365-2-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(735,437)'},
			{'name': 'set-4-620-365-2-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(785,437)'},
			{'name': 'set-4-620-365-2-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(835,437)'},
			{'name': 'set-4-620-365-2-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(885,437)'},
			{'name': 'set-4-620-365-2-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(935,437)'},
			{'name': 'set-4-620-365-2-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(985,437)'},
			{'name': 'set-4-620-365-2-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(1035,437)'},
			{'name': 'set-4-620-365-3-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(635,473)'},
			{'name': 'set-4-620-365-3-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(685,473)'},
			{'name': 'set-4-620-365-3-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(735,473)'},
			{'name': 'set-4-620-365-3-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(785,473)'},
			{'name': 'set-4-620-365-3-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(835,473)'},
			{'name': 'set-4-620-365-3-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(885,473)'},
			{'name': 'set-4-620-365-3-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(935,473)'},
			{'name': 'set-4-620-365-3-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(985,473)'},
			{'name': 'set-4-620-365-3-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(1035,473)'},
		]),
	('assets/visual_renewal/chrysanthemum_18.drawn.svg',
		'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="630" viewBox="0 0 1100 630" role="img" aria-labelledby="title desc"><title id="title">Chrysanthemum chromosome sets</title><desc id="desc">Schematic chromosome types retain stable color and shape. Each row contains one complete set of nine types. Each enclosing outline represents one cell.</desc><rect width="1100" height="630" fill="white" />\n<g id="cell-1-50-240" data-sets="1" data-chromosomes="9"><rect x="35" y="215" width="460" height="56" rx="35" fill="#F3F6F8" stroke="#647681" stroke-width="2" />\n<g data-recipe-slot="0" /><g data-recipe-slot="1" /><g data-recipe-slot="2" /><g data-recipe-slot="3" /><g data-recipe-slot="4" /><g data-recipe-slot="5" /><g data-recipe-slot="6" /><g data-recipe-slot="7" /><g data-recipe-slot="8" /></g>\n<text x="265" y="335" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="26" text-anchor="middle" fill="#222">Monoploid set: 9</text>\n<g id="cell-2-620-100" data-sets="2" data-chromosomes="18"><rect x="605" y="75" width="460" height="92" rx="35" fill="#F3F6F8" stroke="#647681" stroke-width="2" />\n<g data-recipe-slot="9" /><g data-recipe-slot="10" /><g data-recipe-slot="11" /><g data-recipe-slot="12" /><g data-recipe-slot="13" /><g data-recipe-slot="14" /><g data-recipe-slot="15" /><g data-recipe-slot="16" /><g data-recipe-slot="17" /><g data-recipe-slot="18" /><g data-recipe-slot="19" /><g data-recipe-slot="20" /><g data-recipe-slot="21" /><g data-recipe-slot="22" /><g data-recipe-slot="23" /><g data-recipe-slot="24" /><g data-recipe-slot="25" /><g data-recipe-slot="26" /></g>\n<text x="835" y="212" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="26" text-anchor="middle" fill="#222">Diploid (18)</text>\n</svg>',
		[
			{'name': 'set-1-50-240-0-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(65,240)'},
			{'name': 'set-1-50-240-0-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(115,240)'},
			{'name': 'set-1-50-240-0-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(165,240)'},
			{'name': 'set-1-50-240-0-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(215,240)'},
			{'name': 'set-1-50-240-0-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(265,240)'},
			{'name': 'set-1-50-240-0-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(315,240)'},
			{'name': 'set-1-50-240-0-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(365,240)'},
			{'name': 'set-1-50-240-0-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(415,240)'},
			{'name': 'set-1-50-240-0-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(465,240)'},
			{'name': 'set-2-620-100-0-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(635,100)'},
			{'name': 'set-2-620-100-0-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(685,100)'},
			{'name': 'set-2-620-100-0-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(735,100)'},
			{'name': 'set-2-620-100-0-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(785,100)'},
			{'name': 'set-2-620-100-0-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(835,100)'},
			{'name': 'set-2-620-100-0-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(885,100)'},
			{'name': 'set-2-620-100-0-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(935,100)'},
			{'name': 'set-2-620-100-0-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(985,100)'},
			{'name': 'set-2-620-100-0-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(1035,100)'},
			{'name': 'set-2-620-100-1-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(635,136)'},
			{'name': 'set-2-620-100-1-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(685,136)'},
			{'name': 'set-2-620-100-1-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(735,136)'},
			{'name': 'set-2-620-100-1-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(785,136)'},
			{'name': 'set-2-620-100-1-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(835,136)'},
			{'name': 'set-2-620-100-1-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(885,136)'},
			{'name': 'set-2-620-100-1-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(935,136)'},
			{'name': 'set-2-620-100-1-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(985,136)'},
			{'name': 'set-2-620-100-1-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(1035,136)'},
		]),
	('assets/visual_renewal/chrysanthemum_36_54.drawn.svg',
		'<svg xmlns="http://www.w3.org/2000/svg" width="520" height="560" viewBox="0 0 520 560" role="img" aria-labelledby="title desc"><title id="title">Chrysanthemum polyploid comparison</title><desc id="desc">Schematic chromosome types retain stable color and shape. Each row contains one complete set of nine types. Each enclosing outline represents one cell.</desc><rect width="520" height="560" fill="white" />\n<g id="cell-4-40-45" data-sets="4" data-chromosomes="36"><rect x="25" y="20" width="460" height="164" rx="35" fill="#F3F6F8" stroke="#647681" stroke-width="2" />\n<g data-recipe-slot="0" /><g data-recipe-slot="1" /><g data-recipe-slot="2" /><g data-recipe-slot="3" /><g data-recipe-slot="4" /><g data-recipe-slot="5" /><g data-recipe-slot="6" /><g data-recipe-slot="7" /><g data-recipe-slot="8" /><g data-recipe-slot="9" /><g data-recipe-slot="10" /><g data-recipe-slot="11" /><g data-recipe-slot="12" /><g data-recipe-slot="13" /><g data-recipe-slot="14" /><g data-recipe-slot="15" /><g data-recipe-slot="16" /><g data-recipe-slot="17" /><g data-recipe-slot="18" /><g data-recipe-slot="19" /><g data-recipe-slot="20" /><g data-recipe-slot="21" /><g data-recipe-slot="22" /><g data-recipe-slot="23" /><g data-recipe-slot="24" /><g data-recipe-slot="25" /><g data-recipe-slot="26" /><g data-recipe-slot="27" /><g data-recipe-slot="28" /><g data-recipe-slot="29" /><g data-recipe-slot="30" /><g data-recipe-slot="31" /><g data-recipe-slot="32" /><g data-recipe-slot="33" /><g data-recipe-slot="34" /><g data-recipe-slot="35" /></g>\n<text x="255" y="229" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="26" text-anchor="middle" fill="#222">Tetraploid (36)</text>\n<g id="cell-6-40-289" data-sets="6" data-chromosomes="54"><rect x="25" y="264" width="460" height="236" rx="35" fill="#F3F6F8" stroke="#647681" stroke-width="2" />\n<g data-recipe-slot="36" /><g data-recipe-slot="37" /><g data-recipe-slot="38" /><g data-recipe-slot="39" /><g data-recipe-slot="40" /><g data-recipe-slot="41" /><g data-recipe-slot="42" /><g data-recipe-slot="43" /><g data-recipe-slot="44" /><g data-recipe-slot="45" /><g data-recipe-slot="46" /><g data-recipe-slot="47" /><g data-recipe-slot="48" /><g data-recipe-slot="49" /><g data-recipe-slot="50" /><g data-recipe-slot="51" /><g data-recipe-slot="52" /><g data-recipe-slot="53" /><g data-recipe-slot="54" /><g data-recipe-slot="55" /><g data-recipe-slot="56" /><g data-recipe-slot="57" /><g data-recipe-slot="58" /><g data-recipe-slot="59" /><g data-recipe-slot="60" /><g data-recipe-slot="61" /><g data-recipe-slot="62" /><g data-recipe-slot="63" /><g data-recipe-slot="64" /><g data-recipe-slot="65" /><g data-recipe-slot="66" /><g data-recipe-slot="67" /><g data-recipe-slot="68" /><g data-recipe-slot="69" /><g data-recipe-slot="70" /><g data-recipe-slot="71" /><g data-recipe-slot="72" /><g data-recipe-slot="73" /><g data-recipe-slot="74" /><g data-recipe-slot="75" /><g data-recipe-slot="76" /><g data-recipe-slot="77" /><g data-recipe-slot="78" /><g data-recipe-slot="79" /><g data-recipe-slot="80" /><g data-recipe-slot="81" /><g data-recipe-slot="82" /><g data-recipe-slot="83" /><g data-recipe-slot="84" /><g data-recipe-slot="85" /><g data-recipe-slot="86" /><g data-recipe-slot="87" /><g data-recipe-slot="88" /><g data-recipe-slot="89" /></g>\n<text x="255" y="545" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="26" text-anchor="middle" fill="#222">Hexaploid (54)</text>\n</svg>',
		[
			{'name': 'set-4-40-45-0-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,45)'},
			{'name': 'set-4-40-45-0-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,45)'},
			{'name': 'set-4-40-45-0-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,45)'},
			{'name': 'set-4-40-45-0-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,45)'},
			{'name': 'set-4-40-45-0-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,45)'},
			{'name': 'set-4-40-45-0-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,45)'},
			{'name': 'set-4-40-45-0-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,45)'},
			{'name': 'set-4-40-45-0-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,45)'},
			{'name': 'set-4-40-45-0-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,45)'},
			{'name': 'set-4-40-45-1-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,81)'},
			{'name': 'set-4-40-45-1-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,81)'},
			{'name': 'set-4-40-45-1-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,81)'},
			{'name': 'set-4-40-45-1-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,81)'},
			{'name': 'set-4-40-45-1-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,81)'},
			{'name': 'set-4-40-45-1-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,81)'},
			{'name': 'set-4-40-45-1-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,81)'},
			{'name': 'set-4-40-45-1-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,81)'},
			{'name': 'set-4-40-45-1-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,81)'},
			{'name': 'set-4-40-45-2-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,117)'},
			{'name': 'set-4-40-45-2-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,117)'},
			{'name': 'set-4-40-45-2-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,117)'},
			{'name': 'set-4-40-45-2-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,117)'},
			{'name': 'set-4-40-45-2-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,117)'},
			{'name': 'set-4-40-45-2-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,117)'},
			{'name': 'set-4-40-45-2-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,117)'},
			{'name': 'set-4-40-45-2-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,117)'},
			{'name': 'set-4-40-45-2-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,117)'},
			{'name': 'set-4-40-45-3-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,153)'},
			{'name': 'set-4-40-45-3-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,153)'},
			{'name': 'set-4-40-45-3-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,153)'},
			{'name': 'set-4-40-45-3-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,153)'},
			{'name': 'set-4-40-45-3-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,153)'},
			{'name': 'set-4-40-45-3-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,153)'},
			{'name': 'set-4-40-45-3-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,153)'},
			{'name': 'set-4-40-45-3-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,153)'},
			{'name': 'set-4-40-45-3-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,153)'},
			{'name': 'set-6-40-289-0-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,289)'},
			{'name': 'set-6-40-289-0-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,289)'},
			{'name': 'set-6-40-289-0-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,289)'},
			{'name': 'set-6-40-289-0-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,289)'},
			{'name': 'set-6-40-289-0-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,289)'},
			{'name': 'set-6-40-289-0-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,289)'},
			{'name': 'set-6-40-289-0-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,289)'},
			{'name': 'set-6-40-289-0-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,289)'},
			{'name': 'set-6-40-289-0-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,289)'},
			{'name': 'set-6-40-289-1-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,325)'},
			{'name': 'set-6-40-289-1-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,325)'},
			{'name': 'set-6-40-289-1-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,325)'},
			{'name': 'set-6-40-289-1-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,325)'},
			{'name': 'set-6-40-289-1-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,325)'},
			{'name': 'set-6-40-289-1-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,325)'},
			{'name': 'set-6-40-289-1-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,325)'},
			{'name': 'set-6-40-289-1-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,325)'},
			{'name': 'set-6-40-289-1-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,325)'},
			{'name': 'set-6-40-289-2-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,361)'},
			{'name': 'set-6-40-289-2-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,361)'},
			{'name': 'set-6-40-289-2-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,361)'},
			{'name': 'set-6-40-289-2-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,361)'},
			{'name': 'set-6-40-289-2-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,361)'},
			{'name': 'set-6-40-289-2-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,361)'},
			{'name': 'set-6-40-289-2-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,361)'},
			{'name': 'set-6-40-289-2-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,361)'},
			{'name': 'set-6-40-289-2-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,361)'},
			{'name': 'set-6-40-289-3-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,397)'},
			{'name': 'set-6-40-289-3-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,397)'},
			{'name': 'set-6-40-289-3-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,397)'},
			{'name': 'set-6-40-289-3-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,397)'},
			{'name': 'set-6-40-289-3-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,397)'},
			{'name': 'set-6-40-289-3-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,397)'},
			{'name': 'set-6-40-289-3-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,397)'},
			{'name': 'set-6-40-289-3-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,397)'},
			{'name': 'set-6-40-289-3-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,397)'},
			{'name': 'set-6-40-289-4-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,433)'},
			{'name': 'set-6-40-289-4-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,433)'},
			{'name': 'set-6-40-289-4-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,433)'},
			{'name': 'set-6-40-289-4-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,433)'},
			{'name': 'set-6-40-289-4-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,433)'},
			{'name': 'set-6-40-289-4-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,433)'},
			{'name': 'set-6-40-289-4-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,433)'},
			{'name': 'set-6-40-289-4-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,433)'},
			{'name': 'set-6-40-289-4-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,433)'},
			{'name': 'set-6-40-289-5-type-1', 'curve': 'M-11 0 Q0 -7 11 0', 'color': '#B68C00', 'thickness': 8, 'transform': 'translate(55,469)'},
			{'name': 'set-6-40-289-5-type-2', 'curve': 'M-13 -4 Q8 -7 13 5', 'color': '#C06B35', 'thickness': 8, 'transform': 'translate(105,469)'},
			{'name': 'set-6-40-289-5-type-3', 'curve': 'M-14 6 Q12 -15 14 6', 'color': '#92734A', 'thickness': 8, 'transform': 'translate(155,469)'},
			{'name': 'set-6-40-289-5-type-4', 'curve': 'M-14 8 Q0 -18 14 8', 'color': '#398DB5', 'thickness': 8, 'transform': 'translate(205,469)'},
			{'name': 'set-6-40-289-5-type-5', 'curve': 'M-17 8 Q0 -23 17 8', 'color': '#A1467E', 'thickness': 8, 'transform': 'translate(255,469)'},
			{'name': 'set-6-40-289-5-type-6', 'curve': 'M-18 -5 C-10 -11 -3 -10 2 0 C7 10 13 10 18 5', 'color': '#2B896B', 'thickness': 8, 'transform': 'translate(305,469)'},
			{'name': 'set-6-40-289-5-type-7', 'curve': 'M-18 6 Q-8 -12 18 6', 'color': '#7E9C22', 'thickness': 8, 'transform': 'translate(355,469)'},
			{'name': 'set-6-40-289-5-type-8', 'curve': 'M-11 9 Q-21 -10 11 -8', 'color': '#C45462', 'thickness': 8, 'transform': 'translate(405,469)'},
			{'name': 'set-6-40-289-5-type-9', 'curve': 'M-18 0 L18 0', 'color': '#697AA6', 'thickness': 8, 'transform': 'translate(455,469)'},
		]),
	('assets/visual_renewal/ploidy_sets.drawn.svg',
		'<svg xmlns="http://www.w3.org/2000/svg" width="780" height="650" viewBox="0 0 780 650" role="img" aria-labelledby="title desc"><title id="title">N, 2N, 3N and 4N chromosome sets</title><desc id="desc">N, 2N, 3N and 4N cells contain three chromosome types in one, two, three and four copies, respectively. Colors, lengths and centromere positions preserve source identity; unscaled schematic.</desc><rect width="780" height="650" fill="white" />\n<g id="sets-1"><rect x="30" y="55" width="340" height="230" rx="35" fill="#F3F6F8" stroke="#647681" stroke-width="2" />\n<g data-recipe-slot="0" /><g data-recipe-slot="1" /><g data-recipe-slot="2" /></g>\n<text x="200" y="325" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="26" text-anchor="middle" fill="#222">N</text>\n<g id="sets-2"><rect x="410" y="55" width="340" height="230" rx="35" fill="#F3F6F8" stroke="#647681" stroke-width="2" />\n<g data-recipe-slot="3" /><g data-recipe-slot="4" /><g data-recipe-slot="5" /><g data-recipe-slot="6" /><g data-recipe-slot="7" /><g data-recipe-slot="8" /></g>\n<text x="580" y="325" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="26" text-anchor="middle" fill="#222">2N</text>\n<g id="sets-3"><rect x="30" y="360" width="340" height="230" rx="35" fill="#F3F6F8" stroke="#647681" stroke-width="2" />\n<g data-recipe-slot="9" /><g data-recipe-slot="10" /><g data-recipe-slot="11" /><g data-recipe-slot="12" /><g data-recipe-slot="13" /><g data-recipe-slot="14" /><g data-recipe-slot="15" /><g data-recipe-slot="16" /><g data-recipe-slot="17" /></g>\n<text x="200" y="630" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="26" text-anchor="middle" fill="#222">3N</text>\n<g id="sets-4"><rect x="410" y="360" width="340" height="230" rx="35" fill="#F3F6F8" stroke="#647681" stroke-width="2" />\n<g data-recipe-slot="18" /><g data-recipe-slot="19" /><g data-recipe-slot="20" /><g data-recipe-slot="21" /><g data-recipe-slot="22" /><g data-recipe-slot="23" /><g data-recipe-slot="24" /><g data-recipe-slot="25" /><g data-recipe-slot="26" /><g data-recipe-slot="27" /><g data-recipe-slot="28" /><g data-recipe-slot="29" /></g>\n<text x="580" y="630" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="26" text-anchor="middle" fill="#222">4N</text>\n</svg>',
		[
			{'name': 'ploidy-0', 'length': 115.0, 'thickness': 13, 'color': '#C45462', 'fraction': 0.30434782608695654, 'transform': 'translate(53.5 90.0)'},
			{'name': 'ploidy-1', 'length': 145.0, 'thickness': 13, 'color': '#8970AD', 'fraction': 0.2413793103448276, 'transform': 'translate(158.5 90.0)'},
			{'name': 'ploidy-2', 'length': 95.0, 'thickness': 13, 'color': '#B68C00', 'fraction': 0.3684210526315789, 'transform': 'translate(263.5 90.0)'},
			{'name': 'ploidy-3', 'length': 115.0, 'thickness': 13, 'color': '#C45462', 'fraction': 0.30434782608695654, 'transform': 'translate(433.5 90.0)'},
			{'name': 'ploidy-4', 'length': 115.0, 'thickness': 13, 'color': '#C45462', 'fraction': 0.30434782608695654, 'transform': 'translate(453.5 90.0)'},
			{'name': 'ploidy-5', 'length': 145.0, 'thickness': 13, 'color': '#8970AD', 'fraction': 0.2413793103448276, 'transform': 'translate(538.5 90.0)'},
			{'name': 'ploidy-6', 'length': 145.0, 'thickness': 13, 'color': '#8970AD', 'fraction': 0.2413793103448276, 'transform': 'translate(558.5 90.0)'},
			{'name': 'ploidy-7', 'length': 95.0, 'thickness': 13, 'color': '#B68C00', 'fraction': 0.3684210526315789, 'transform': 'translate(643.5 90.0)'},
			{'name': 'ploidy-8', 'length': 95.0, 'thickness': 13, 'color': '#B68C00', 'fraction': 0.3684210526315789, 'transform': 'translate(663.5 90.0)'},
			{'name': 'ploidy-9', 'length': 115.0, 'thickness': 13, 'color': '#C45462', 'fraction': 0.30434782608695654, 'transform': 'translate(53.5 395.0)'},
			{'name': 'ploidy-10', 'length': 115.0, 'thickness': 13, 'color': '#C45462', 'fraction': 0.30434782608695654, 'transform': 'translate(73.5 395.0)'},
			{'name': 'ploidy-11', 'length': 115.0, 'thickness': 13, 'color': '#C45462', 'fraction': 0.30434782608695654, 'transform': 'translate(93.5 395.0)'},
			{'name': 'ploidy-12', 'length': 145.0, 'thickness': 13, 'color': '#8970AD', 'fraction': 0.2413793103448276, 'transform': 'translate(158.5 395.0)'},
			{'name': 'ploidy-13', 'length': 145.0, 'thickness': 13, 'color': '#8970AD', 'fraction': 0.2413793103448276, 'transform': 'translate(178.5 395.0)'},
			{'name': 'ploidy-14', 'length': 145.0, 'thickness': 13, 'color': '#8970AD', 'fraction': 0.2413793103448276, 'transform': 'translate(198.5 395.0)'},
			{'name': 'ploidy-15', 'length': 95.0, 'thickness': 13, 'color': '#B68C00', 'fraction': 0.3684210526315789, 'transform': 'translate(263.5 395.0)'},
			{'name': 'ploidy-16', 'length': 95.0, 'thickness': 13, 'color': '#B68C00', 'fraction': 0.3684210526315789, 'transform': 'translate(283.5 395.0)'},
			{'name': 'ploidy-17', 'length': 95.0, 'thickness': 13, 'color': '#B68C00', 'fraction': 0.3684210526315789, 'transform': 'translate(303.5 395.0)'},
			{'name': 'ploidy-18', 'length': 115.0, 'thickness': 13, 'color': '#C45462', 'fraction': 0.30434782608695654, 'transform': 'translate(433.5 395.0)'},
			{'name': 'ploidy-19', 'length': 115.0, 'thickness': 13, 'color': '#C45462', 'fraction': 0.30434782608695654, 'transform': 'translate(453.5 395.0)'},
			{'name': 'ploidy-20', 'length': 115.0, 'thickness': 13, 'color': '#C45462', 'fraction': 0.30434782608695654, 'transform': 'translate(473.5 395.0)'},
			{'name': 'ploidy-21', 'length': 115.0, 'thickness': 13, 'color': '#C45462', 'fraction': 0.30434782608695654, 'transform': 'translate(493.5 395.0)'},
			{'name': 'ploidy-22', 'length': 145.0, 'thickness': 13, 'color': '#8970AD', 'fraction': 0.2413793103448276, 'transform': 'translate(538.5 395.0)'},
			{'name': 'ploidy-23', 'length': 145.0, 'thickness': 13, 'color': '#8970AD', 'fraction': 0.2413793103448276, 'transform': 'translate(558.5 395.0)'},
			{'name': 'ploidy-24', 'length': 145.0, 'thickness': 13, 'color': '#8970AD', 'fraction': 0.2413793103448276, 'transform': 'translate(578.5 395.0)'},
			{'name': 'ploidy-25', 'length': 145.0, 'thickness': 13, 'color': '#8970AD', 'fraction': 0.2413793103448276, 'transform': 'translate(598.5 395.0)'},
			{'name': 'ploidy-26', 'length': 95.0, 'thickness': 13, 'color': '#B68C00', 'fraction': 0.3684210526315789, 'transform': 'translate(643.5 395.0)'},
			{'name': 'ploidy-27', 'length': 95.0, 'thickness': 13, 'color': '#B68C00', 'fraction': 0.3684210526315789, 'transform': 'translate(663.5 395.0)'},
			{'name': 'ploidy-28', 'length': 95.0, 'thickness': 13, 'color': '#B68C00', 'fraction': 0.3684210526315789, 'transform': 'translate(683.5 395.0)'},
			{'name': 'ploidy-29', 'length': 95.0, 'thickness': 13, 'color': '#B68C00', 'fraction': 0.3684210526315789, 'transform': 'translate(703.5 395.0)'},
		]),
	('assets/lect12b-polyploidy/unreduced_gamete_tetraploidy.drawn.svg',
		'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="600" viewBox="0 0 1200 600" role="img" aria-labelledby="title desc">\n<title id="title">Unreduced gametes and tetraploid zygote</title>\n<desc id="desc">One diploid parent produces two unreduced gametes. Each contains six separate chromosome rods; the tetraploid zygote contains twelve. Each rod has an individual primary constriction.</desc>\n<defs><radialGradient id="cell-fill" cx="30%" cy="25%" r="80%"><stop offset="0" stop-color="#fff2d8" /><stop offset="1" stop-color="#efc296" /></radialGradient></defs><rect width="1200" height="600" fill="white" />\n<g id="cell-parent"><circle id="cell-body-parent" cx="155" cy="265" r="115" fill="url(#cell-fill)" stroke="#c9a895" stroke-width="2" />\n<g id="rod-parent-1-1" transform="translate(99.1748 268.3367) rotate(12)" data-recipe-slot="0" />\n<g id="rod-parent-1-2" transform="translate(114.8252 271.6633) rotate(12)" data-recipe-slot="1" />\n<g id="rod-parent-2-1" transform="translate(191.7495 233.3809) rotate(-25)" data-recipe-slot="2" />\n<g id="rod-parent-2-2" transform="translate(206.2505 226.6191) rotate(-25)" data-recipe-slot="3" />\n<g id="rod-parent-3-1" transform="translate(150.0000 337.0000) rotate(0)" data-recipe-slot="4" />\n<g id="rod-parent-3-2" transform="translate(166.0000 337.0000) rotate(0)" data-recipe-slot="5" />\n</g>\n<g id="cell-upper-gamete"><circle id="cell-body-upper-gamete" cx="600" cy="135" r="94" fill="url(#cell-fill)" stroke="#c9a895" stroke-width="2" />\n<g id="rod-upper-gamete-1-1" transform="translate(554.1215 128.6108) rotate(10)" data-recipe-slot="6" />\n<g id="rod-upper-gamete-1-2" transform="translate(569.8785 131.3892) rotate(10)" data-recipe-slot="7" />\n<g id="rod-upper-gamete-2-1" transform="translate(625.6959 96.9253) rotate(-38)" data-recipe-slot="8" />\n<g id="rod-upper-gamete-2-2" transform="translate(638.3041 87.0747) rotate(-38)" data-recipe-slot="9" />\n<g id="rod-upper-gamete-3-1" transform="translate(625.1748 168.3367) rotate(12)" data-recipe-slot="10" />\n<g id="rod-upper-gamete-3-2" transform="translate(640.8252 171.6633) rotate(12)" data-recipe-slot="11" />\n</g>\n<g id="cell-lower-gamete"><circle id="cell-body-lower-gamete" cx="600" cy="420" r="94" fill="url(#cell-fill)" stroke="#c9a895" stroke-width="2" />\n<g id="rod-lower-gamete-1-1" transform="translate(552.7495 412.6191) rotate(25)" data-recipe-slot="12" />\n<g id="rod-lower-gamete-1-2" transform="translate(567.2505 419.3809) rotate(25)" data-recipe-slot="13" />\n<g id="rod-lower-gamete-2-1" transform="translate(630.1748 400.6633) rotate(-12)" data-recipe-slot="14" />\n<g id="rod-lower-gamete-2-2" transform="translate(645.8252 397.3367) rotate(-12)" data-recipe-slot="15" />\n<g id="rod-lower-gamete-3-1" transform="translate(595.7495 474.3809) rotate(-25)" data-recipe-slot="16" />\n<g id="rod-lower-gamete-3-2" transform="translate(610.2505 467.6191) rotate(-25)" data-recipe-slot="17" />\n</g>\n<g id="cell-zygote"><circle id="cell-body-zygote" cx="1040" cy="265" r="132" fill="url(#cell-fill)" stroke="#c9a895" stroke-width="2" />\n<g id="rod-zygote-1-1" transform="translate(1012.7495 195.6191) rotate(25)" data-recipe-slot="18" />\n<g id="rod-zygote-1-2" transform="translate(1027.2505 202.3809) rotate(25)" data-recipe-slot="19" />\n<g id="rod-zygote-2-1" transform="translate(1094.5825 219.9969) rotate(-22)" data-recipe-slot="20" />\n<g id="rod-zygote-2-2" transform="translate(1109.4175 214.0031) rotate(-22)" data-recipe-slot="21" />\n<g id="rod-zygote-3-1" transform="translate(951.1215 270.6108) rotate(10)" data-recipe-slot="22" />\n<g id="rod-zygote-3-2" transform="translate(966.8785 273.3892) rotate(10)" data-recipe-slot="23" />\n<g id="rod-zygote-4-1" transform="translate(1007.5825 337.9969) rotate(-22)" data-recipe-slot="24" />\n<g id="rod-zygote-4-2" transform="translate(1022.4175 332.0031) rotate(-22)" data-recipe-slot="25" />\n<g id="rod-zygote-5-1" transform="translate(1061.9364 266.2442) rotate(28)" data-recipe-slot="26" />\n<g id="rod-zygote-5-2" transform="translate(1076.0636 273.7558) rotate(28)" data-recipe-slot="27" />\n<g id="rod-zygote-6-1" transform="translate(1106.3431 317.3431) rotate(45)" data-recipe-slot="28" />\n<g id="rod-zygote-6-2" transform="translate(1117.6569 328.6569) rotate(45)" data-recipe-slot="29" />\n</g>\n<g id="arrow-1" fill="#252525" stroke="#252525"><path d="M297 200 L471.710 147.861" fill="none" stroke-width="6" /><path d="M488 143 L469.708 141.154 L473.712 154.569 Z" stroke="none" /></g>\n<g id="arrow-2" fill="#252525" stroke="#252525"><path d="M297 328 L472.205 397.715" fill="none" stroke-width="6" /><path d="M488 404 L474.793 391.211 L469.617 404.219 Z" stroke="none" /></g>\n<g id="arrow-3" fill="#252525" stroke="#252525"><path d="M712 143 L878.794 195.864" fill="none" stroke-width="6" /><path d="M895 201 L880.909 189.191 L876.680 202.537 Z" stroke="none" /></g>\n<g id="arrow-4" fill="#252525" stroke="#252525"><path d="M712 404 L879.240 336.373" fill="none" stroke-width="6" /><path d="M895 330 L876.616 329.883 L881.864 342.862 Z" stroke="none" /></g>\n<g font-family="Atkinson Hyperlegible Next" font-size="29" fill="#15191c" text-anchor="middle">\n<text x="155" y="93" font-weight="700">Parent Species</text>\n<text x="155" y="422" font-weight="700">2n = 6</text>\n<text x="155" y="459" font-weight="700">Diploid</text>\n<text x="393" y="269" font-weight="400">Meiotic error</text>\n<text x="802" y="253" font-weight="400">Self-</text>\n<text x="802" y="287" font-weight="400">fertilisation</text>\n<text x="600" y="552" font-weight="400">Unreduced</text>\n<text x="600" y="587" font-weight="400">gametes</text>\n<text x="1040" y="93" font-weight="700">Zygote</text>\n<text x="1040" y="440" font-weight="700">4n = 12</text>\n<text x="1040" y="477" font-weight="700">Tetraploid</text>\n</g></svg>',
		[
			{'name': 'rod-parent-1-1', 'length': 61.0, 'thickness': 10, 'color': '#617de0', 'fraction': 0.5, 'transform': 'translate(-5 -30.5)'},
			{'name': 'rod-parent-1-2', 'length': 61.0, 'thickness': 10, 'color': '#617de0', 'fraction': 0.5, 'transform': 'translate(-5 -30.5)'},
			{'name': 'rod-parent-2-1', 'length': 76.0, 'thickness': 10, 'color': '#e66b58', 'fraction': 0.5, 'transform': 'translate(-5 -38.0)'},
			{'name': 'rod-parent-2-2', 'length': 76.0, 'thickness': 10, 'color': '#e66b58', 'fraction': 0.5, 'transform': 'translate(-5 -38.0)'},
			{'name': 'rod-parent-3-1', 'length': 43.0, 'thickness': 10, 'color': '#57a68c', 'fraction': 0.5, 'transform': 'translate(-5 -21.5)'},
			{'name': 'rod-parent-3-2', 'length': 43.0, 'thickness': 10, 'color': '#57a68c', 'fraction': 0.5, 'transform': 'translate(-5 -21.5)'},
			{'name': 'rod-upper-gamete-1-1', 'length': 76.0, 'thickness': 10, 'color': '#e66b58', 'fraction': 0.5, 'transform': 'translate(-5 -38.0)'},
			{'name': 'rod-upper-gamete-1-2', 'length': 76.0, 'thickness': 10, 'color': '#e66b58', 'fraction': 0.5, 'transform': 'translate(-5 -38.0)'},
			{'name': 'rod-upper-gamete-2-1', 'length': 61.0, 'thickness': 10, 'color': '#617de0', 'fraction': 0.5, 'transform': 'translate(-5 -30.5)'},
			{'name': 'rod-upper-gamete-2-2', 'length': 61.0, 'thickness': 10, 'color': '#617de0', 'fraction': 0.5, 'transform': 'translate(-5 -30.5)'},
			{'name': 'rod-upper-gamete-3-1', 'length': 43.0, 'thickness': 10, 'color': '#57a68c', 'fraction': 0.5, 'transform': 'translate(-5 -21.5)'},
			{'name': 'rod-upper-gamete-3-2', 'length': 43.0, 'thickness': 10, 'color': '#57a68c', 'fraction': 0.5, 'transform': 'translate(-5 -21.5)'},
			{'name': 'rod-lower-gamete-1-1', 'length': 61.0, 'thickness': 10, 'color': '#617de0', 'fraction': 0.5, 'transform': 'translate(-5 -30.5)'},
			{'name': 'rod-lower-gamete-1-2', 'length': 61.0, 'thickness': 10, 'color': '#617de0', 'fraction': 0.5, 'transform': 'translate(-5 -30.5)'},
			{'name': 'rod-lower-gamete-2-1', 'length': 76.0, 'thickness': 10, 'color': '#e66b58', 'fraction': 0.5, 'transform': 'translate(-5 -38.0)'},
			{'name': 'rod-lower-gamete-2-2', 'length': 76.0, 'thickness': 10, 'color': '#e66b58', 'fraction': 0.5, 'transform': 'translate(-5 -38.0)'},
			{'name': 'rod-lower-gamete-3-1', 'length': 43.0, 'thickness': 10, 'color': '#57a68c', 'fraction': 0.5, 'transform': 'translate(-5 -21.5)'},
			{'name': 'rod-lower-gamete-3-2', 'length': 43.0, 'thickness': 10, 'color': '#57a68c', 'fraction': 0.5, 'transform': 'translate(-5 -21.5)'},
			{'name': 'rod-zygote-1-1', 'length': 76.0, 'thickness': 10, 'color': '#e66b58', 'fraction': 0.5, 'transform': 'translate(-5 -38.0)'},
			{'name': 'rod-zygote-1-2', 'length': 76.0, 'thickness': 10, 'color': '#e66b58', 'fraction': 0.5, 'transform': 'translate(-5 -38.0)'},
			{'name': 'rod-zygote-2-1', 'length': 76.0, 'thickness': 10, 'color': '#e66b58', 'fraction': 0.5, 'transform': 'translate(-5 -38.0)'},
			{'name': 'rod-zygote-2-2', 'length': 76.0, 'thickness': 10, 'color': '#e66b58', 'fraction': 0.5, 'transform': 'translate(-5 -38.0)'},
			{'name': 'rod-zygote-3-1', 'length': 61.0, 'thickness': 10, 'color': '#617de0', 'fraction': 0.5, 'transform': 'translate(-5 -30.5)'},
			{'name': 'rod-zygote-3-2', 'length': 61.0, 'thickness': 10, 'color': '#617de0', 'fraction': 0.5, 'transform': 'translate(-5 -30.5)'},
			{'name': 'rod-zygote-4-1', 'length': 61.0, 'thickness': 10, 'color': '#617de0', 'fraction': 0.5, 'transform': 'translate(-5 -30.5)'},
			{'name': 'rod-zygote-4-2', 'length': 61.0, 'thickness': 10, 'color': '#617de0', 'fraction': 0.5, 'transform': 'translate(-5 -30.5)'},
			{'name': 'rod-zygote-5-1', 'length': 43.0, 'thickness': 10, 'color': '#57a68c', 'fraction': 0.5, 'transform': 'translate(-5 -21.5)'},
			{'name': 'rod-zygote-5-2', 'length': 43.0, 'thickness': 10, 'color': '#57a68c', 'fraction': 0.5, 'transform': 'translate(-5 -21.5)'},
			{'name': 'rod-zygote-6-1', 'length': 43.0, 'thickness': 10, 'color': '#57a68c', 'fraction': 0.5, 'transform': 'translate(-5 -21.5)'},
			{'name': 'rod-zygote-6-2', 'length': 43.0, 'thickness': 10, 'color': '#57a68c', 'fraction': 0.5, 'transform': 'translate(-5 -21.5)'},
		]),
	('assets/lect12b-polyploidy/auto_allopolyploid_comparison.drawn.svg',
		'<svg xmlns="http://www.w3.org/2000/svg" width="2119" height="1485" viewBox="0 0 1200 840.962718263" role="img" aria-labelledby="figure-title figure-description">\n<title id="figure-title">Autopolyploidy and allopolyploidy</title>\n<desc id="figure-description">Conceptual, unscaled comparison. Each diploid parent has four single chromosomes: two long blue rods and two short red rods. Dark colors identify species A; light colors identify species B. The autotetraploid contains two complete diploid A genomes, eight rods. The allotetraploid contains one complete diploid A genome and one complete diploid B genome, eight rods. Rods are unreplicated chromosomes; their narrowed waists represent centromeres.</desc>\n<rect width="1200" height="840.962718263" fill="#ffffff" />\n<path d="M 534,38 V 801" stroke="#e4e9eb" stroke-width="1.5" />\n<g id="labels" fill="#263b48" font-family="Atkinson Hyperlegible Next, sans-serif">\n  <text id="auto-heading" x="255" y="46" text-anchor="middle" font-size="32" font-weight="bold">Autopolyploidy</text>\n  <text id="allo-heading" x="873" y="46" text-anchor="middle" font-size="32" font-weight="bold">Allopolyploidy</text>\n  <text id="auto-parent-label" x="255" y="100" text-anchor="middle" font-size="25">Species A (diploid)</text>\n  <text id="allo-a-label" x="708" y="100" text-anchor="middle" font-size="25">Species A (diploid)</text>\n  <text id="allo-b-label" x="1040" y="100" text-anchor="middle" font-size="25">Species B (diploid)</text>\n</g>\n\n<g id="auto-a-parent" data-cell="true" transform="translate(255 218)">\n<g transform="scale(1 1)"><path d="M -139,-6 C -144,-66 -93,-101 -29,-103 C 40,-114 117,-85 137,-29 C 162,40 111,94 44,104 C -29,121 -129,84 -139,-6 Z" fill="#f4ecdc" stroke="#667a80" stroke-width="2.7" /><path d="M -128,24 C -101,82 -27,100 41,90 C 91,84 124,57 137,26 C 124,75 92,97 44,101 C -31,117 -111,84 -128,24 Z" fill="#e4d9c3" /><path d="M -114,-40 C -95,-76 -56,-88 -24,-89" fill="none" stroke="#fffaf0" stroke-width="4.5" stroke-linecap="round" /></g>\n<g id="auto-a-parent-genome-1-long-1" data-species="A" data-kind="long" transform="translate(-80 -1) rotate(-13) scale(1)" data-recipe-slot="0">\n      </g>\n<g id="auto-a-parent-genome-1-long-2" data-species="A" data-kind="long" transform="translate(-27 2) rotate(9) scale(1)" data-recipe-slot="1">\n      </g>\n<g id="auto-a-parent-genome-1-short-3" data-species="A" data-kind="short" transform="translate(40 -8) rotate(-17) scale(1)" data-recipe-slot="2">\n      </g>\n<g id="auto-a-parent-genome-1-short-4" data-species="A" data-kind="short" transform="translate(91 9) rotate(14) scale(1)" data-recipe-slot="3">\n      </g>\n</g>\n<g id="allo-a-parent" data-cell="true" transform="translate(708 218)">\n<g transform="scale(1 1)"><path d="M -139,-8 C -138,-65 -95,-98 -35,-103 C 38,-116 117,-86 139,-27 C 158,29 116,88 50,103 C -26,121 -126,84 -139,-8 Z" fill="#f4ecdc" stroke="#667a80" stroke-width="2.7" /><path d="M -124,30 C -98,78 -29,103 46,88 C 93,79 125,57 138,24 C 125,73 93,91 50,100 C -26,117 -109,83 -124,30 Z" fill="#e4d9c3" /><path d="M -113,-41 C -95,-73 -60,-88 -27,-90" fill="none" stroke="#fffaf0" stroke-width="4.5" stroke-linecap="round" /></g>\n<g id="allo-a-parent-genome-1-long-1" data-species="A" data-kind="long" transform="translate(-80 -1) rotate(-13) scale(1)" data-recipe-slot="4">\n      </g>\n<g id="allo-a-parent-genome-1-long-2" data-species="A" data-kind="long" transform="translate(-27 2) rotate(9) scale(1)" data-recipe-slot="5">\n      </g>\n<g id="allo-a-parent-genome-1-short-3" data-species="A" data-kind="short" transform="translate(40 -8) rotate(-17) scale(1)" data-recipe-slot="6">\n      </g>\n<g id="allo-a-parent-genome-1-short-4" data-species="A" data-kind="short" transform="translate(91 9) rotate(14) scale(1)" data-recipe-slot="7">\n      </g>\n</g>\n<g id="allo-b-parent" data-cell="true" transform="translate(1040 218)">\n<g transform="scale(1 1)"><path d="M -141,1 C -153,-54 -110,-98 -45,-104 C 22,-113 103,-95 132,-39 C 168,21 126,81 67,99 C -8,122 -122,92 -141,1 Z" fill="#f4ecdc" stroke="#667a80" stroke-width="2.7" /><path d="M -128,27 C -91,88 -14,103 62,85 C 106,73 130,54 141,23 C 127,70 108,85 66,96 C -11,119 -110,82 -128,27 Z" fill="#e4d9c3" /><path d="M -116,-34 C -100,-68 -67,-87 -38,-90" fill="none" stroke="#fffaf0" stroke-width="4.5" stroke-linecap="round" /></g>\n<g id="allo-b-parent-genome-1-long-1" data-species="B" data-kind="long" transform="translate(-80 -1) rotate(-13) scale(1)" data-recipe-slot="8">\n      </g>\n<g id="allo-b-parent-genome-1-long-2" data-species="B" data-kind="long" transform="translate(-27 2) rotate(9) scale(1)" data-recipe-slot="9">\n      </g>\n<g id="allo-b-parent-genome-1-short-3" data-species="B" data-kind="short" transform="translate(40 -8) rotate(-17) scale(1)" data-recipe-slot="10">\n      </g>\n<g id="allo-b-parent-genome-1-short-4" data-species="B" data-kind="short" transform="translate(91 9) rotate(14) scale(1)" data-recipe-slot="11">\n      </g>\n</g>\n<g id="process-arrows" fill="none" stroke="#263b48" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">\n  <path id="auto-process" d="M 230,340 L 230,423 M 219,406 L 230,423 L 241,406" />\n  <path id="allo-merge" d="M 708,336 V 337 Q 708,347 724,347 H 853 Q 870,347 870,365 M 1040,336 V 337 Q 1040,347 1024,347 H 887 Q 870,347 870,365 V 423 M 859,406 L 870,423 L 881,406" />\n</g>\n<g id="process-labels" fill="#263b48" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="23">\n  <text id="auto-process-label" x="264" y="371"><tspan x="264">Sexual or asexual </tspan><tspan x="264" dy="29">polyploidization</tspan></text>\n  <text id="allo-process-label" x="899" y="378"><tspan x="899">Hybridization accompanied </tspan><tspan x="899" dy="26">by sexual or asexual </tspan><tspan x="899" dy="26">polyploidization</tspan></text>\n</g>\n<g id="auto-product" data-cell="true" transform="translate(255 580)">\n<g transform="scale(1.27 1.31)"><path d="M -141,1 C -153,-54 -110,-98 -45,-104 C 22,-113 103,-95 132,-39 C 168,21 126,81 67,99 C -8,122 -122,92 -141,1 Z" fill="#f4ecdc" stroke="#667a80" stroke-width="2.7" /><path d="M -128,27 C -91,88 -14,103 62,85 C 106,73 130,54 141,23 C 127,70 108,85 66,96 C -11,119 -110,82 -128,27 Z" fill="#e4d9c3" /><path d="M -116,-34 C -100,-68 -67,-87 -38,-90" fill="none" stroke="#fffaf0" stroke-width="4.5" stroke-linecap="round" /></g>\n<g id="auto-product-genome-1-long-1" data-species="A" data-kind="long" transform="translate(-80 -62) rotate(-13) scale(0.94)" data-recipe-slot="12">\n      </g>\n<g id="auto-product-genome-1-long-2" data-species="A" data-kind="long" transform="translate(-27 -59) rotate(9) scale(0.94)" data-recipe-slot="13">\n      </g>\n<g id="auto-product-genome-1-short-3" data-species="A" data-kind="short" transform="translate(40 -69) rotate(-17) scale(0.94)" data-recipe-slot="14">\n      </g>\n<g id="auto-product-genome-1-short-4" data-species="A" data-kind="short" transform="translate(91 -52) rotate(14) scale(0.94)" data-recipe-slot="15">\n      </g>\n<g id="auto-product-genome-2-long-1" data-species="A" data-kind="long" transform="translate(-80 60) rotate(-13) scale(0.94)" data-recipe-slot="16">\n      </g>\n<g id="auto-product-genome-2-long-2" data-species="A" data-kind="long" transform="translate(-27 63) rotate(9) scale(0.94)" data-recipe-slot="17">\n      </g>\n<g id="auto-product-genome-2-short-3" data-species="A" data-kind="short" transform="translate(40 53) rotate(-17) scale(0.94)" data-recipe-slot="18">\n      </g>\n<g id="auto-product-genome-2-short-4" data-species="A" data-kind="short" transform="translate(91 70) rotate(14) scale(0.94)" data-recipe-slot="19">\n      </g>\n</g>\n<g id="allo-product" data-cell="true" transform="translate(870 580)">\n<g transform="scale(1.27 1.31)"><path d="M -139,-6 C -144,-66 -93,-101 -29,-103 C 40,-114 117,-85 137,-29 C 162,40 111,94 44,104 C -29,121 -129,84 -139,-6 Z" fill="#f4ecdc" stroke="#667a80" stroke-width="2.7" /><path d="M -128,24 C -101,82 -27,100 41,90 C 91,84 124,57 137,26 C 124,75 92,97 44,101 C -31,117 -111,84 -128,24 Z" fill="#e4d9c3" /><path d="M -114,-40 C -95,-76 -56,-88 -24,-89" fill="none" stroke="#fffaf0" stroke-width="4.5" stroke-linecap="round" /></g>\n<g id="allo-product-genome-1-long-1" data-species="A" data-kind="long" transform="translate(-80 -62) rotate(-13) scale(0.94)" data-recipe-slot="20">\n      </g>\n<g id="allo-product-genome-1-long-2" data-species="A" data-kind="long" transform="translate(-27 -59) rotate(9) scale(0.94)" data-recipe-slot="21">\n      </g>\n<g id="allo-product-genome-1-short-3" data-species="A" data-kind="short" transform="translate(40 -69) rotate(-17) scale(0.94)" data-recipe-slot="22">\n      </g>\n<g id="allo-product-genome-1-short-4" data-species="A" data-kind="short" transform="translate(91 -52) rotate(14) scale(0.94)" data-recipe-slot="23">\n      </g>\n<g id="allo-product-genome-2-long-1" data-species="B" data-kind="long" transform="translate(-80 60) rotate(-13) scale(0.94)" data-recipe-slot="24">\n      </g>\n<g id="allo-product-genome-2-long-2" data-species="B" data-kind="long" transform="translate(-27 63) rotate(9) scale(0.94)" data-recipe-slot="25">\n      </g>\n<g id="allo-product-genome-2-short-3" data-species="B" data-kind="short" transform="translate(40 53) rotate(-17) scale(0.94)" data-recipe-slot="26">\n      </g>\n<g id="allo-product-genome-2-short-4" data-species="B" data-kind="short" transform="translate(91 70) rotate(14) scale(0.94)" data-recipe-slot="27">\n      </g>\n</g>\n<g id="genome-leaders" fill="none" stroke="#667a80" stroke-width="2" stroke-linecap="round">\n  <path d="M 255,723 V 735" /><path d="M 870,723 V 735" />\n</g>\n<g id="outcome-labels" fill="#263b48" font-family="Atkinson Hyperlegible Next, sans-serif" text-anchor="middle">\n  <text id="auto-genome-label" x="255" y="765" font-size="23"><tspan x="255">Two complete diploid A genomes</tspan></text>\n  <text id="allo-genome-label" xml:space="preserve" x="870" y="765" font-size="23"><tspan x="870">Complete diploid A genome </tspan><tspan font-style="italic">plus </tspan><tspan x="870" dy="27">complete diploid B genome</tspan></text>\n  <text id="auto-product-label" x="255" y="827" font-size="25" font-weight="bold">New autotetraploid species</text>\n  <text id="allo-product-label" x="870" y="827" font-size="25" font-weight="bold">New allotetraploid species</text>\n</g>\n</svg>',
		[
			{'name': 'auto-a-parent-genome-1-long-1', 'length': 112, 'thickness': 19, 'color': '#2d719e', 'fraction': 0.5, 'transform': 'translate(-9.5 -56.0)'},
			{'name': 'auto-a-parent-genome-1-long-2', 'length': 112, 'thickness': 19, 'color': '#2d719e', 'fraction': 0.5, 'transform': 'translate(-9.5 -56.0)'},
			{'name': 'auto-a-parent-genome-1-short-3', 'length': 72, 'thickness': 19, 'color': '#b95040', 'fraction': 0.5, 'transform': 'translate(-9.5 -36.0)'},
			{'name': 'auto-a-parent-genome-1-short-4', 'length': 72, 'thickness': 19, 'color': '#b95040', 'fraction': 0.5, 'transform': 'translate(-9.5 -36.0)'},
			{'name': 'allo-a-parent-genome-1-long-1', 'length': 112, 'thickness': 19, 'color': '#2d719e', 'fraction': 0.5, 'transform': 'translate(-9.5 -56.0)'},
			{'name': 'allo-a-parent-genome-1-long-2', 'length': 112, 'thickness': 19, 'color': '#2d719e', 'fraction': 0.5, 'transform': 'translate(-9.5 -56.0)'},
			{'name': 'allo-a-parent-genome-1-short-3', 'length': 72, 'thickness': 19, 'color': '#b95040', 'fraction': 0.5, 'transform': 'translate(-9.5 -36.0)'},
			{'name': 'allo-a-parent-genome-1-short-4', 'length': 72, 'thickness': 19, 'color': '#b95040', 'fraction': 0.5, 'transform': 'translate(-9.5 -36.0)'},
			{'name': 'allo-b-parent-genome-1-long-1', 'length': 112, 'thickness': 19, 'color': '#7ba9ca', 'fraction': 0.5, 'transform': 'translate(-9.5 -56.0)'},
			{'name': 'allo-b-parent-genome-1-long-2', 'length': 112, 'thickness': 19, 'color': '#7ba9ca', 'fraction': 0.5, 'transform': 'translate(-9.5 -56.0)'},
			{'name': 'allo-b-parent-genome-1-short-3', 'length': 72, 'thickness': 19, 'color': '#de8e77', 'fraction': 0.5, 'transform': 'translate(-9.5 -36.0)'},
			{'name': 'allo-b-parent-genome-1-short-4', 'length': 72, 'thickness': 19, 'color': '#de8e77', 'fraction': 0.5, 'transform': 'translate(-9.5 -36.0)'},
			{'name': 'auto-product-genome-1-long-1', 'length': 112, 'thickness': 19, 'color': '#2d719e', 'fraction': 0.5, 'transform': 'translate(-9.5 -56.0)'},
			{'name': 'auto-product-genome-1-long-2', 'length': 112, 'thickness': 19, 'color': '#2d719e', 'fraction': 0.5, 'transform': 'translate(-9.5 -56.0)'},
			{'name': 'auto-product-genome-1-short-3', 'length': 72, 'thickness': 19, 'color': '#b95040', 'fraction': 0.5, 'transform': 'translate(-9.5 -36.0)'},
			{'name': 'auto-product-genome-1-short-4', 'length': 72, 'thickness': 19, 'color': '#b95040', 'fraction': 0.5, 'transform': 'translate(-9.5 -36.0)'},
			{'name': 'auto-product-genome-2-long-1', 'length': 112, 'thickness': 19, 'color': '#2d719e', 'fraction': 0.5, 'transform': 'translate(-9.5 -56.0)'},
			{'name': 'auto-product-genome-2-long-2', 'length': 112, 'thickness': 19, 'color': '#2d719e', 'fraction': 0.5, 'transform': 'translate(-9.5 -56.0)'},
			{'name': 'auto-product-genome-2-short-3', 'length': 72, 'thickness': 19, 'color': '#b95040', 'fraction': 0.5, 'transform': 'translate(-9.5 -36.0)'},
			{'name': 'auto-product-genome-2-short-4', 'length': 72, 'thickness': 19, 'color': '#b95040', 'fraction': 0.5, 'transform': 'translate(-9.5 -36.0)'},
			{'name': 'allo-product-genome-1-long-1', 'length': 112, 'thickness': 19, 'color': '#2d719e', 'fraction': 0.5, 'transform': 'translate(-9.5 -56.0)'},
			{'name': 'allo-product-genome-1-long-2', 'length': 112, 'thickness': 19, 'color': '#2d719e', 'fraction': 0.5, 'transform': 'translate(-9.5 -56.0)'},
			{'name': 'allo-product-genome-1-short-3', 'length': 72, 'thickness': 19, 'color': '#b95040', 'fraction': 0.5, 'transform': 'translate(-9.5 -36.0)'},
			{'name': 'allo-product-genome-1-short-4', 'length': 72, 'thickness': 19, 'color': '#b95040', 'fraction': 0.5, 'transform': 'translate(-9.5 -36.0)'},
			{'name': 'allo-product-genome-2-long-1', 'length': 112, 'thickness': 19, 'color': '#7ba9ca', 'fraction': 0.5, 'transform': 'translate(-9.5 -56.0)'},
			{'name': 'allo-product-genome-2-long-2', 'length': 112, 'thickness': 19, 'color': '#7ba9ca', 'fraction': 0.5, 'transform': 'translate(-9.5 -56.0)'},
			{'name': 'allo-product-genome-2-short-3', 'length': 72, 'thickness': 19, 'color': '#de8e77', 'fraction': 0.5, 'transform': 'translate(-9.5 -36.0)'},
			{'name': 'allo-product-genome-2-short-4', 'length': 72, 'thickness': 19, 'color': '#de8e77', 'fraction': 0.5, 'transform': 'translate(-9.5 -36.0)'},
		]),
	('assets/lect12b-polyploidy/colchicine_chromosome_doubling.drawn.svg',
		'<svg xmlns="http://www.w3.org/2000/svg" width="1208" height="834" viewBox="0 0 1208 834" role="img" aria-labelledby="figure-title figure-description">\n  <title id="figure-title">Colchicine and chromosome doubling</title>\n  <desc id="figure-description">Simplified, unscaled cell-division comparison. A monoploid metaphase cell has three replicated chromosomes: one long blue, one short red, and one intermediate green, each with two sisters joined at a shared centromere. Without colchicine, two monoploid cells each contain one single chromosome of each type. With colchicine, one diploid cell contains six separate single chromosomes, two of each type. The source\'s five identifying labels are retained.</desc>\n  <rect width="1208" height="834" fill="#ffffff" />\n  <g id="source-label" fill="#263b48" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="38" text-anchor="middle">\n    <text x="615" y="46"><tspan x="615">Metaphase in mitosis</tspan><tspan x="615" dy="46">in a monoploid cell</tspan></text>\n  </g>\n  <g id="metaphase-cell">\n    <path id="parent-cell-outline" d="M 440,249 C 435,170 500,119 602,118 C 708,111 792,160 797,239 C 807,328 725,380 627,382 C 523,391 445,340 440,249 Z" fill="#f4ecdc" stroke="#667a80" stroke-width="4" />\n    <path d="M 459,273 C 487,348 561,365 638,360 C 704,359 760,331 781,285 C 764,351 699,377 627,378 C 545,385 476,349 459,273 Z" fill="#e7ddc9" />\n    <g id="parent-blue-replicated" transform="translate(552 243) rotate(-23)" data-recipe-slot="0">\n      </g>\n    <g id="parent-red-replicated" transform="translate(696 195) rotate(65)" data-recipe-slot="1">\n      </g>\n    <g id="parent-green-replicated" transform="translate(691 300) rotate(18)" data-recipe-slot="2">\n      </g>\n  </g>\n  <g id="outcome-branches" fill="none" stroke="#263b48" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">\n    <g id="untreated-arrow">\n      <path d="M 480,354 C 445,393 394,428 325,472" />\n      <path d="M 331,447 L 325,472 L 350,469" />\n    </g>\n    <g id="colchicine-arrow">\n      <path d="M 756,354 C 801,396 853,430 923,472" />\n      <path d="M 897,469 L 923,472 L 915,447" />\n    </g>\n  </g>\n  <g id="treatment-labels" fill="#263b48" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="38" text-anchor="middle">\n    <text x="240" y="418">No colchicine</text>\n    <text x="999" y="418">Colchicine</text>\n  </g>\n  <g id="two-monoploid-cells">\n    <g id="daughter-cell-a">\n      <path id="daughter-a-outline" d="M 29,619 C 24,543 76,500 151,500 C 228,495 284,546 287,622 C 294,699 237,749 160,750 C 84,753 32,699 29,619 Z" fill="#f4ecdc" stroke="#667a80" stroke-width="4" />\n      <path d="M 45,645 C 72,714 132,733 184,726 C 224,723 262,698 276,664 C 260,720 215,747 160,746 C 100,748 54,711 45,645 Z" fill="#e7ddc9" />\n      <g id="daughter-a-blue" transform="translate(111 610) rotate(-20)" data-recipe-slot="3" />\n      <g id="daughter-a-red" transform="translate(215 578) rotate(68)" data-recipe-slot="4" />\n      <g id="daughter-a-green" transform="translate(203 657) rotate(16)" data-recipe-slot="5" />\n    </g>\n    <g id="daughter-cell-b">\n      <path id="daughter-b-outline" d="M 328,626 C 322,549 371,504 449,500 C 531,495 586,542 590,618 C 595,696 541,747 461,750 C 385,756 333,708 328,626 Z" fill="#f4ecdc" stroke="#667a80" stroke-width="4" />\n      <path d="M 343,651 C 369,720 434,736 491,725 C 532,717 566,698 578,664 C 561,720 515,747 461,746 C 404,750 354,718 343,651 Z" fill="#e7ddc9" />\n      <g id="daughter-b-blue" transform="translate(416 608) rotate(20)" data-recipe-slot="6" />\n      <g id="daughter-b-red" transform="translate(520 581) rotate(-58)" data-recipe-slot="7" />\n      <g id="daughter-b-green" transform="translate(513 654) rotate(-12)" data-recipe-slot="8" />\n    </g>\n  </g>\n  <g id="one-diploid-cell">\n    <path id="diploid-cell-outline" d="M 781,624 C 775,544 849,498 958,498 C 1068,493 1162,538 1170,615 C 1179,696 1086,748 982,751 C 867,758 787,707 781,624 Z" fill="#f4ecdc" stroke="#667a80" stroke-width="4" />\n    <path d="M 797,649 C 832,718 920,735 1001,728 C 1070,726 1139,698 1156,659 C 1137,716 1062,746 982,747 C 886,753 813,713 797,649 Z" fill="#e7ddc9" />\n    <g id="diploid-blue-a" transform="translate(851 620) rotate(-8)" data-recipe-slot="9" />\n    <g id="diploid-blue-b" transform="translate(907 619) rotate(8)" data-recipe-slot="10" />\n    <g id="diploid-red-a" transform="translate(987 553) rotate(73)" data-recipe-slot="11" />\n    <g id="diploid-red-b" transform="translate(1084 565) rotate(82)" data-recipe-slot="12" />\n    <g id="diploid-green-a" transform="translate(993 661) rotate(9)" data-recipe-slot="13" />\n    <g id="diploid-green-b" transform="translate(1080 664) rotate(-5)" data-recipe-slot="14" />\n  </g>\n  <g id="outcome-labels" fill="#263b48" font-family="Atkinson Hyperlegible Next, sans-serif" font-size="39" text-anchor="middle">\n    <text x="309" y="810">Two monoploid cells</text>\n    <text x="976" y="810">One diploid cell</text>\n  </g>\n</svg>',
		[
			{'name': 'parent-blue-replicated', 'length': 160, 'thickness': 62, 'color': '#2d719e', 'fraction': 0.5, 'sisters': True, 'transform': 'translate(-31.0 -80.0)'},
			{'name': 'parent-red-replicated', 'length': 77, 'thickness': 62, 'color': '#b95040', 'fraction': 0.5, 'sisters': True, 'transform': 'translate(-31.0 -38.5)'},
			{'name': 'parent-green-replicated', 'length': 114, 'thickness': 62, 'color': '#278065', 'fraction': 0.5, 'sisters': True, 'transform': 'translate(-31.0 -57.0)'},
			{'name': 'daughter-a-blue', 'length': 160, 'thickness': 22, 'color': '#2d719e', 'fraction': 0.5, 'sisters': False, 'transform': 'translate(-11.0 -80.0)'},
			{'name': 'daughter-a-red', 'length': 77, 'thickness': 22, 'color': '#b95040', 'fraction': 0.5, 'sisters': False, 'transform': 'translate(-11.0 -38.5)'},
			{'name': 'daughter-a-green', 'length': 114, 'thickness': 22, 'color': '#278065', 'fraction': 0.5, 'sisters': False, 'transform': 'translate(-11.0 -57.0)'},
			{'name': 'daughter-b-blue', 'length': 160, 'thickness': 22, 'color': '#2d719e', 'fraction': 0.5, 'sisters': False, 'transform': 'translate(-11.0 -80.0)'},
			{'name': 'daughter-b-red', 'length': 77, 'thickness': 22, 'color': '#b95040', 'fraction': 0.5, 'sisters': False, 'transform': 'translate(-11.0 -38.5)'},
			{'name': 'daughter-b-green', 'length': 114, 'thickness': 22, 'color': '#278065', 'fraction': 0.5, 'sisters': False, 'transform': 'translate(-11.0 -57.0)'},
			{'name': 'diploid-blue-a', 'length': 160, 'thickness': 22, 'color': '#2d719e', 'fraction': 0.5, 'sisters': False, 'transform': 'translate(-11.0 -80.0)'},
			{'name': 'diploid-blue-b', 'length': 160, 'thickness': 22, 'color': '#2d719e', 'fraction': 0.5, 'sisters': False, 'transform': 'translate(-11.0 -80.0)'},
			{'name': 'diploid-red-a', 'length': 77, 'thickness': 22, 'color': '#b95040', 'fraction': 0.5, 'sisters': False, 'transform': 'translate(-11.0 -38.5)'},
			{'name': 'diploid-red-b', 'length': 77, 'thickness': 22, 'color': '#b95040', 'fraction': 0.5, 'sisters': False, 'transform': 'translate(-11.0 -38.5)'},
			{'name': 'diploid-green-a', 'length': 114, 'thickness': 22, 'color': '#278065', 'fraction': 0.5, 'sisters': False, 'transform': 'translate(-11.0 -57.0)'},
			{'name': 'diploid-green-b', 'length': 114, 'thickness': 22, 'color': '#278065', 'fraction': 0.5, 'sisters': False, 'transform': 'translate(-11.0 -57.0)'},
		]),
]


def main() -> None:
	for relative, template, specs in FIGURES:
		root = ET.fromstring(template)
		for element in root.iter():
			if "data-recipe-slot" in element.attrib:
				index = int(element.attrib.pop("data-recipe-slot"))
				element.append(ET.fromstring(chromosome(specs[index])))
		data = ET.tostring(root, encoding="ascii", xml_declaration=True)
		(BASE / relative).write_bytes(data)
		if relative == 'assets/visual_renewal/ploidy_sets.drawn.svg':
			root.set('height', '760')
			root.set('viewBox', '0 0 780 760')
			root.find(NS + 'rect').set('height', '760')
			for element in root:
				if element.get('id') in ('sets-3', 'sets-4'):
					element.set('transform', 'translate(0 80)')
				if element.tag == NS + 'text':
					name = {'N': 'A', '2N': 'AA', '3N': 'AAA', '4N': 'AAAA'}[element.text]
					element.text = name + ' (' + element.text + ')'
					element.set('font-size', '64')
					element.set('y', '350' if element.get('y') == '325' else '735')
			(BASE / 'assets/visual_renewal/ploidy_sets_nomenclature.drawn.svg').write_bytes(
				ET.tostring(root, encoding='ascii', xml_declaration=True))


# Source raster scenes retain the original canvas, cell positions, branch states,
# chromosome counts and replication states. Schematic body counts intentionally
# remain source-faithful where adjacent native labels count chromosome material.
BLUE = '#8970AD'
GREEN = '#55AE6E'
INK = '#344651'


def body(name: str, x: float, y: float, length: float, color: str, *,
	sisters: bool = False, angle: float = 0, horizontal: bool = False,
	fraction: float = .5) -> str:
	thickness = length*.36 if sisters else length*.14
	return chromosome(dict(name=name, color=color, length=length, thickness=thickness,
		fraction=fraction, sisters=sisters, orientation='horizontal' if horizontal else 'vertical',
		transform=f'translate({x} {y}) rotate({angle}) translate({-length/2 if horizontal else -thickness/2} {-thickness/2 if horizontal else -length/2})'))


def cell(name: str, x: float, y: float, rx: float, ry: float, contents: str) -> str:
	return f'<g id="{name}"><ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#F5D59A" stroke="{INK}" stroke-width="2.5"/><path d="M{x-rx*.88} {y+ry*.28} Q{x} {y+ry*1.12} {x+rx*.88} {y+ry*.28} Q{x+rx*.64} {y+ry*.99} {x} {y+ry*.97} Q{x-rx*.64} {y+ry*.99} {x-rx*.88} {y+ry*.28}Z" fill="#E9C58A"/>' + contents + '</g>'


def arrow(path: str) -> str:
	return f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="3" marker-end="url(#process-arrow)"/>'


def label(x: float, y: float, text: str, size: float = 36, anchor: str = 'middle',
	bold: bool = False) -> str:
	return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Atkinson Hyperlegible Next" font-size="{size}" fill="{INK}" font-weight="{700 if bold else 400}">{text}</text>'


def scene(relative: str, width: float, height: float, title: str, description: str,
	content: str) -> None:
	text = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">{title}</title><desc id="desc">{description}</desc><defs><marker id="process-arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="userSpaceOnUse"><path d="M1 1 L11 6 L1 11Z" fill="{INK}"/></marker></defs><rect width="{width}" height="{height}" fill="white"/>' + content + '</svg>'
	root = ET.fromstring(text)
	(BASE/'assets/lect12b-polyploidy'/relative).write_bytes(ET.tostring(root, encoding='ascii', xml_declaration=True))


def three_types(name: str, x: float, y: float, scale: float = 1, copies: int = 1,
	sisters: bool = False) -> str:
	result = ''
	if copies == 2:
		placements = [(-32,-60,94,65),(-40,-13,94,65),(57,-20,66,-40),(47,23,66,-40),(-36,75,42,-45),(5,70,42,-45)]
		return ''.join(body(f'{name}-{kind}',x+dx*scale,y+dy*scale,length*scale,BLUE,sisters=sisters,angle=angle) for kind,(dx,dy,length,angle) in enumerate(placements))
	for copy in range(copies):
		for kind, (dx,dy,length,angle) in enumerate([(-28,-35,94,48),(48,0,66,-40),(-25,58,42,-45)]):
			result += body(f'{name}-{copy}-{kind}',x+(dx+copy*38)*scale,y+(dy+copy*13)*scale,length*scale,BLUE,sisters=sisters,angle=angle)
	return result


def hybrid_scene(stage: int) -> None:
	content = label(120,65,'Species A',34)+label(120,105,'2<tspan font-style="italic">n</tspan> = 6',34)+label(745,65,'Species B',34)+label(745,105,'2<tspan font-style="italic">n</tspan> = 4',34)
	content += label(140,338,'Normal gamete',32)+label(140,377,'<tspan font-style="italic">n</tspan> = 3',32)+label(730,338,'Normal gamete',32)+label(730,377,'<tspan font-style="italic">n</tspan> = 2',32)
	content += cell('species-a',295,88,80,80,three_types('a',295,88,.75,sisters=True))
	b = body('b-long',550,75,78,GREEN,sisters=True,angle=25)+body('b-short',595,108,46,GREEN,sisters=True,angle=48)
	content += cell('species-b',570,88,80,80,b)
	content += arrow('M298 170 Q305 240 329 296')+arrow('M563 170 Q560 245 539 296')
	content += cell('a-gamete',346,352,51,51,three_types('a-gamete',346,352,.51))
	content += cell('b-gamete',512,352,51,51,body('bg-long',497,341,58,GREEN,angle=22)+body('bg-short',530,369,37,GREEN,angle=45))
	if stage >= 23:
		content += label(686,590,'Sterile hybrid with',32)+label(686,630,'5 chromosomes',32)
		content += arrow('M363 402 L411 522')+arrow('M498 403 L450 522')
		chrom = three_types('hybrid',430,606,.66)+body('hybrid-b-long',401,576,65,GREEN,angle=35)+body('hybrid-b-short',463,568,45,GREEN,angle=-12)
		content += cell('sterile-hybrid',430,606,80,80,chrom)
	if stage >= 24:
		content += label(690,744,'Mitotic or meiotic error',30)+label(690,780,'doubles the chromosome',30)+label(690,816,'number.',30)
		content += label(690,913,'New species:',30)+label(690,949,'viable, fertile hybrid',30)+label(690,985,'(allopolyploid)',30)+label(690,1021,'2<tspan font-style="italic">n</tspan> = 10',30)
		content += arrow('M430 689 L430 872')
		chrom = body('doubled-a-long',392,921,75,BLUE,sisters=True,angle=45)+body('doubled-a-medium',424,947,54,BLUE,sisters=True,angle=-12)+body('doubled-a-short',389,993,35,BLUE,sisters=True,angle=-35)+body('doubled-b-long',465,980,78,GREEN,sisters=True,angle=50)+body('doubled-b-short',473,917,48,GREEN,sisters=True,angle=-28)
		content += cell('fertile-hybrid',430,958,80,80,chrom)
	scene(f'hybridization_{stage}.drawn.svg',915,1056,'Hybridization between species',
		'Source reveal preserved. Species A: three replicated purple bodies; species B: two replicated green bodies. Their gametes contain three and two single bodies.' + (' The sterile hybrid contains five single bodies.' if stage>=23 else '') + (' The final source cell contains five replicated bodies; adjacent native source label is 2n = 10. This schematic preserves that preexisting discrepancy.' if stage>=24 else ''),content)


def autopolyploid_division() -> None:
	content = label(320,70,'Cell division error',29)+label(138,319,'2<tspan font-style="italic">n</tspan> = 6',32)+label(510,319,'Tetraploid cell',30)+label(510,356,'4<tspan font-style="italic">n</tspan>',32)
	content += label(180,435,'Meiosis',36)+label(150,668,'2<tspan font-style="italic">n</tspan>',30)+label(150,889,'2<tspan font-style="italic">n</tspan>',30)
	content += label(460,460,'Gametes produced',32)+label(460,500,'by tetraploids',32)+label(510,854,'New species',30)+label(510,890,'(4<tspan font-style="italic">n</tspan>)',30)+label(330,1015,'Autopolyploid speciation',32)
	content += cell('parent',138,168,117,117,three_types('parent',138,168,sisters=True))
	content += cell('doubled',510,168,117,117,three_types('doubled',485,168,.9,2,True))
	content += arrow('M260 168 L382 168')+arrow('M422 351 L211 503')
	content += cell('gamete-a',150,566,75,75,three_types('gamete-a',150,566,.66,sisters=True))
	content += cell('gamete-b',150,787,75,75,three_types('gamete-b',150,787,.66,sisters=True))
	content += '<path d="M223 600 L280 669 L223 751" fill="none" stroke="#344651" stroke-width="3"/>'+arrow('M280 669 L383 669')
	content += cell('zygote',510,679,117,117,three_types('zygote',485,679,.9,2,True))
	scene('autopolyploid_division.drawn.svg',659,1056,'Autopolyploid division error',
		'Source schematic has three replicated purple bodies, then six, two gametes with three replicated bodies each, and a final cell with six replicated bodies. Native labels retain the source ploidy notation; visible source body counts are preserved without inference.',content)


def genome(name: str, x: float, y: float, color_long: str, color_short: str,
	rows: int) -> str:
	return ''.join(body(f'{name}-{row}-{kind}',x+dx,y+row*48,length,color,horizontal=True,fraction=fraction)
		for row in range(rows) for kind,(dx,length,color,fraction) in enumerate([(-105,215,color_long,.5),(135,150,color_short,.68)]))


def auto_single() -> None:
	content = label(314,48,'Autopolyploidy',48,bold=True)+label(314,113,'Species A (diploid)',40)
	content += cell('a-parent',314,340,262,196,genome('a-parent',314,309,'#2d719e','#b95040',2))
	content += arrow('M314 584 L314 890')+label(365,751,'Sexual or asexual',38,'start')+label(365,807,'polyploidization',38,'start')
	content += cell('a-tetraploid',314,1175,292,225,genome('a-tetraploid',314,1097,'#2d719e','#b95040',4))
	content += '<path d="M573 1201 L632 1229" stroke="#344651" stroke-width="2"/>'+label(653,1253,'Two complete',37,'start')+label(653,1307,'diploid A genomes',37,'start')
	content += label(314,1475,'New autotetraploid species',44)
	scene('autopolyploid_single.drawn.svg',1049,1485,'Autopolyploidy','Four single chromosomes in the diploid A parent and eight in the new autotetraploid. Two long blue and two short red per diploid A genome. Original text and count retained.',content)


def allo_single() -> None:
	content = label(670,48,'Allopolyploidy',48,bold=True)+label(280,113,'Species A (diploid)',40)+label(880,113,'Species B (diploid)',40)
	content += cell('a-parent',280,340,260,196,genome('a-parent',280,309,'#2d719e','#b95040',2))
	content += cell('b-parent',880,340,260,196,genome('b-parent',880,309,'#7ba9ca','#d88c7c',2))
	content += '<path d="M288 584 V632 Q288 649 310 649 H570 Q592 649 592 677 Q592 649 614 649 H870 Q893 649 893 632 V584" fill="none" stroke="#344651" stroke-width="3"/>'+arrow('M592 677 V890')
	content += label(648,750,'Hybridization accompanied by',38,'start')+label(648,806,'sexual or asexual polyploidization',38,'start')
	chrom = genome('a-result',592,1098,'#2d719e','#b95040',2)+genome('b-result',592,1194,'#7ba9ca','#d88c7c',2)
	content += cell('allotetraploid',592,1175,292,225,chrom)
	content += '<path d="M865 1204 L932 1235" stroke="#344651" stroke-width="2"/>'+label(943,1253,'Complete diploid',36,'start')+label(943,1308,'A genome plus',36,'start')+label(943,1363,'complete diploid',36,'start')+label(943,1418,'B genome',36,'start')
	content += label(592,1475,'New allotetraploid species',44)
	scene('allopolyploid_single.drawn.svg',1346,1485,'Allopolyploidy','Each parent contains two long and two short single chromosomes. Dark blue and red retain A identity; pale blue and red retain B identity. The new allotetraploid contains eight chromosomes, a complete diploid A genome plus a complete diploid B genome.',content)


def make_raster_replacements() -> None:
	autopolyploid_division()
	for stage in (22,23,24): hybrid_scene(stage)
	auto_single()
	allo_single()


if __name__ == '__main__':
	main()
	make_raster_replacements()
