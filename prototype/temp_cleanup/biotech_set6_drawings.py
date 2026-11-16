#!/usr/bin/env python3
"""Original, editable teaching schematics. Not measured biological drawings."""
import html
import pathlib

OUT = pathlib.Path('biotech/LECT11/djot/assets/set6_drawings')
FONT = 'Atkinson Hyperlegible Next'
BLUE = '#164D78'
RED = '#A92320'
GREEN = '#00775F'
GOLD = '#A66000'

def text(x: int, y: int, value: str, size: int = 27, color: str = '#202124', anchor: str = 'middle') -> str:
	return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{html.escape(value)}</text>'

def box(x: int, y: int, w: int, h: int, label: str, color: str = BLUE) -> str:
	return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#F4F7FA" stroke="{color}" stroke-width="3"/>' + text(x + w // 2, y + h // 2 + 10, label, 27, color)

def arrow(x: int, y: int, xx: int, yy: int, color: str = '#555555') -> str:
	return f'<path d="M{x} {y} L{xx} {yy}" stroke="{color}" stroke-width="4" fill="none" marker-end="url(#arrow)"/>'

def save(name: str, title: str, description: str, content: str) -> None:
	OUT.mkdir(parents=True, exist_ok=True)
	prefix = f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="570" viewBox="0 0 1100 570" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(description)} Original simplified teaching schematic; not to scale.</desc><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#555555"/></marker></defs><rect width="1100" height="570" fill="white"/>'
	(OUT / (name + '.drawn.svg')).write_text(prefix + content + '</svg>')

def main() -> None:
	s = text(550, 45, 'A contaminated lot connects production to patients', 32)
	for x, label in [(30, 'Source material'), (400, 'Production lot'), (770, 'Patients')]:
		s += box(x, 130, 300, 90, label)
	s += arrow(335, 175, 390, 175) + arrow(705, 175, 760, 175)
	for x, label in [(180, 'Identity'), (550, 'Purity + potency'), (920, 'Traceability')]:
		s += text(x, 295, label, 28, GREEN)
		s += arrow(x, 320, x, 385)
	s += box(65, 395, 970, 100, 'Inspect the process + test the product + keep the records', GREEN)
	save('lot_control', 'Biologic lot control', 'Three linked stages and their distinct quality questions.', s)
	s = text(550, 45, 'Bt protein targets susceptible insects', 32)
	s += box(35, 105, 280, 85, 'Bt expression cassette', BLUE) + arrow(325, 147, 380, 147)
	s += '<path d="M500 280 Q350 160 495 90 Q640 170 500 280Z" fill="#D7EEE1" stroke="#00775F" stroke-width="4"/><path d="M495 95 L500 290" stroke="#00775F" stroke-width="4"/>'
	s += text(500, 335, 'Protein made in plant', 27, GREEN)
	s += arrow(620, 170, 715, 170)
	for i in range(6):
		s += f'<circle cx="{765 + i * 36}" cy="170" r="29" fill="#F5D591" stroke="#A66000" stroke-width="3"/>'
	s += '<path d="M947 146 L970 120 M947 150 L990 142" stroke="#A66000" stroke-width="3"/>'
	s += text(870, 250, 'Susceptible insect feeds', 25, GOLD)
	s += arrow(880, 280, 880, 365) + box(700, 380, 360, 80, 'Midgut effect + pest control', GOLD)
	s += text(365, 440, 'Different question:', 28, RED) + text(365, 480, 'non-target exposure and resistance', 26)
	save('bt_crop', 'Bt plant-incorporated protectant', 'The expression cassette leads to plant-made protein, ingestion by a susceptible insect, and a midgut effect. Specificity and resistance require evidence.', s)
	s = text(550, 45, 'Containment is a set of nested controls', 32)
	for x,y,w,h,col in [(70,85,960,430,BLUE),(170,145,760,310,GREEN),(290,215,520,180,GOLD)]:
		s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="24" fill="none" stroke="{col}" stroke-width="5"/>'
	s += text(550, 125, 'Facility: access, airflow, screens, waste route', 28, BLUE)
	s += text(550, 190, 'Procedure: training, aerosols, cleaning, incident response', 25, GREEN)
	s += text(550, 265, 'Organism + vector + inserted material', 28, GOLD)
	s += '<ellipse cx="550" cy="330" rx="115" ry="35" fill="#EBD9A2" stroke="#A66000" stroke-width="3"/>'
	s += text(550, 340, 'Biological limits', 24)
	save('containment', 'Containment layers', 'Nested facility, procedural, and biological controls. No single layer establishes safety.', s)
	s = text(550, 45, 'Bt corn raises different questions for different authorities', 30)
	for x, label, sub, col in [(25,'NIH / IBC','Covered research',BLUE),(300,'USDA-APHIS','Plant-pest risks',GREEN),(575,'EPA','Pesticidal trait',GOLD),(850,'FDA','Food and feed',RED)]:
		s += box(x,100,225,95,label,col) + text(x+112,240,sub,24,col)
		s += arrow(x+112,265,x+112,350)
	s += box(55,370,990,100,'One product; several responsibilities and evidence questions', BLUE)
	save('agency_map', 'Biotechnology responsibilities', 'Separate covered research oversight, plant-pest responsibilities, pesticides, and food/feed safety. The map is specific to the teaching example, not a universal approval checklist.', s)
	s = text(550,45,'Different questions before and after approval',32)
	stages=[('Nonclinical','Mechanism + hazards'),('I','Safety + dose'),('II','Activity + dose'),('III','Benefit + risk'),('IV','After approval')]
	for i,(label,sub) in enumerate(stages):
		x=20+i*218
		s += box(x,150,190,100,label,GREEN if i==4 else BLUE) + text(x+95,295,sub,21)
		if i<4: s+=arrow(x+195,200,x+212,200)
	s += '<path d="M880 95 L880 385" stroke="#A92320" stroke-width="4" stroke-dasharray="10 7"/>'
	s += text(550,420,'Optional exploratory studies and combined phases can occur',27)
	s += text(550,470,'The sequence organizes evidence; it does not guarantee success',27,RED)
	save('trial_path', 'Clinical development questions', 'A simplified sequence of study purposes. The dashed boundary marks the transition to post-approval studies; individual programs can differ.',s)
	s = text(550,45,'Illustrative bioequivalence confidence intervals',32)
	xmap=lambda value: 120+(value-0.7)/0.7*850
	for v in [0.8,1.0,1.25]:
		x=xmap(v); s+=f'<path d="M{x} 110 L{x} 440" stroke="{GREEN if v!=1 else BLUE}" stroke-width="3" stroke-dasharray="8 6"/>'
		s+=text(int(x),485,f'{v:.2f}',27)
	for y,lo,mid,hi,col,label in [(200,.96,1.01,1.06,BLUE,'Within bounds'),(350,.74,.86,1.00,RED,'Outside bounds')]:
		s+=f'<path d="M{xmap(lo)} {y} L{xmap(hi)} {y} M{xmap(lo)} {y-14} L{xmap(lo)} {y+14} M{xmap(hi)} {y-14} L{xmap(hi)} {y+14}" stroke="{col}" stroke-width="7"/><circle cx="{xmap(mid)}" cy="{y}" r="10" fill="{col}"/>'
		s+=text(805,y+10,label,25,col)
	s+=text(550,535,'Test / reference exposure ratio; line = simulated 90% interval',25)
	save('bioequivalence', 'Bioequivalence example', 'Invented intervals compare exposure ratios with typical 0.80 and 1.25 boundaries. These are not ingredient amounts or measurements from a real drug.',s)
	s=text(550,45,'Cleaning water is not the same as destroying PFAS',32)
	for x,y,w,h,l,col in [(35,110,320,95,'Contaminated water',BLUE),(410,110,270,95,'Capture / separation',BLUE),(745,110,320,95,'Treated water',GREEN),(410,350,270,95,'Concentrated PFAS',RED)]: s+=box(x,y,w,h,l,col)
	s+=arrow(360,157,400,157)+arrow(685,157,735,157)+arrow(545,215,545,335)
	s+=text(545,495,'Further treatment / disposal; verify products and fluorine balance',27,RED)
	save('pfas_fate','PFAS separation versus destruction','Capture moves PFAS into another stream or medium. Destruction requires separate evidence about transformation and fluorine fate.',s)
	s=text(550,45,'Genomic DNA, mature RNA, and cDNA',32)
	for y,name in [(130,'Genomic DNA'),(290,'Mature RNA'),(450,'cDNA')]:
		s+=text(210,y+23,name,28,BLUE)
		if y==130:
			s+='<path d="M410 150 L1010 150" stroke="#777" stroke-width="6"/>'
			for x in [430,660,890]: s+=f'<rect x="{x}" y="125" width="100" height="50" fill="#164D78"/>'
			s+=text(600,110,'intron',22)+text(830,110,'intron',22)
		else:
			for x in [570,670,770]: s+=f'<rect x="{x}" y="{y-5}" width="100" height="50" fill="{GREEN if y==290 else GOLD}" stroke="white" stroke-width="2"/>'
	s+=arrow(720,185,720,265)+text(925,240,'Transcription + splicing',22)
	s+=arrow(720,345,720,425)+text(920,395,'Reverse transcription',22)
	save('dna_cdna','DNA and cDNA comparison','Colored blocks denote the same exon sequences through a simplified transcription, splicing, and reverse-transcription sequence. Short natural sequences can lack introns; synthesis alone does not establish patentability.',s)
	s=text(550,45,'Separate the biological result from the patent question',31)
	s+='<circle cx="260" cy="270" r="150" fill="#EDF5FC" stroke="#164D78" stroke-width="5"/><circle cx="560" cy="270" r="150" fill="#FFF2DB" stroke="#A66000" stroke-width="5"/><circle cx="860" cy="270" r="150" fill="#E2F3ED" stroke="#00775F" stroke-width="5"/>'
	for x,lines,col in [(260,['Patent eligibility','and valid claims'],BLUE),(560,['Freedom','to operate'],GOLD),(860,['Regulatory','authorization'],GREEN)]:
		for j,line in enumerate(lines):s+=text(x,255+40*j,line,28,col)
	s+=text(550,490,'Each circle needs its own evidence and decision',29,RED)
	save('three_permissions','Three distinct product questions','Patent rights, freedom to operate, and regulatory authorization are separate questions; success in one does not establish the others.',s)
	s=text(550,45,'Two causes of seed-saving difficulties',32)
	s+=box(40,120,300,100,'F1 hybrid',BLUE)+arrow(350,170,450,170)+box(470,120,570,100,'F2 offspring: alleles segregate',BLUE)
	for i,col in enumerate([BLUE,GREEN,GOLD,RED,BLUE,GOLD]):s+=f'<ellipse cx="{545+i*78}" cy="270" rx="20" ry="29" fill="{col}"/>'
	s+=box(40,370,300,100,'Legal restriction',RED)+arrow(350,420,450,420)+box(470,370,570,100,'Patent / variety right / contract',RED)
	s+=text(550,540,'Variable offspring, sterility, and legal restrictions are different',27)
	save('seed_saving','Seed inheritance and legal rights','F2 variation from segregation is contrasted with legal restrictions. The diagram does not claim that all hybrid seeds are sterile or that all seed saving is forbidden.',s)
	print('Created 10 original vector teaching diagrams.')

if __name__ == '__main__':
	main()
