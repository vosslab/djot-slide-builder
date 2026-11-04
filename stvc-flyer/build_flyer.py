"""Build the standalone US Letter office-door flyer from the repository root."""
import pathlib
import reportlab.pdfgen.canvas
import reportlab.pdfbase.pdfmetrics
import reportlab.pdfbase.ttfonts

ROOT = pathlib.Path.cwd()
URL = 'https://www.youtube.com/playlist?list=PL5LJPD9b2pRYsw2sU3LRCDhvDSiZ26E48'
OUT = ROOT / 'output/pdf/stvc-office-door-flyer.pdf'
reportlab.pdfbase.pdfmetrics.registerFont(reportlab.pdfbase.ttfonts.TTFont(
	'DIN', '/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf'))
c = reportlab.pdfgen.canvas.Canvas(str(OUT), pagesize=(612, 792))
c.setTitle('Stump the Vibe Coder - Watch the playlist')
c.setAuthor('Stump the Vibe Coder')


def text(x, y, value, font, size, color):
	"""Place one line of display text."""
	c.setFillColor(color)
	c.setFont(font, size)
	c.drawString(x, y, value)


navy = '#101C2D'
red = '#E52326'
c.setFillColor(navy)
c.rect(24, 322, 564, 446, fill=1, stroke=0)
text(42, 738, 'BIOLOGY. GAMES. AI.', 'Helvetica-Bold', 13, '#5FE2E4')
text(40, 653, 'STUMP THE', 'DIN', 94, '#FFFFFF')
text(40, 568, 'VIBE CODER', 'DIN', 94, '#FFFFFF')
text(43, 542, 'Can AI code its way through biology?', 'Helvetica', 17, '#FFFFFF')
# Preserve each complete thumbnail, including its original title.
c.drawImage('genetics/LECT03/djot/assets/stump_the_vibe_coder/h1qDheNahLs.jpg',
	36, 332, width=352, height=198)
c.drawImage('genetics/LECT04/djot/assets/stump_the_vibe_coder/gNA7VV_AGp0.jpg',
	396, 431, width=180, height=101.25)
c.drawImage('genetics/LECT07/djot/assets/stump_the_vibe_coder/0zhh6g-DJFs.jpg',
	396, 322, width=180, height=101.25)
# Familiar YouTube play mark, kept separate from the QR's quiet zone.
c.setFillColor(red)
c.roundRect(42, 277, 35, 24, 7, stroke=0, fill=1)
p = c.beginPath()
p.moveTo(56, 283)
p.lineTo(56, 295)
p.lineTo(66, 289)
p.close()
c.setFillColor('#FFFFFF')
c.drawPath(p, fill=1, stroke=0)
text(86, 281, 'Watch on YouTube', 'Helvetica-Bold', 16, navy)
text(42, 219, 'SCIENCE MEETS', 'DIN', 34, navy)
text(42, 181, 'VIBE CODING.', 'DIN', 40, navy)
text(42, 143, 'Scan to watch', 'Helvetica-Bold', 21, navy)
text(42, 118, 'the StVC playlist.', 'Helvetica', 18, navy)
c.setStrokeColor(red)
c.setLineWidth(3)
c.line(43, 91, 287, 91)
c.line(278, 98, 287, 91)
c.line(278, 84, 287, 91)
c.drawImage('_temp/stvc-flyer/playlist-qr.png', 346, 64, width=222, height=222)
c.linkURL(URL, (346, 64, 568, 286), relative=0, thickness=0)
text(42, 36, 'STUMP THE VIBE CODER', 'Helvetica-Bold', 10, navy)
text(345, 36, 'Open your camera. Pick an episode.', 'Helvetica', 10, navy)
c.showPage()
c.save()
print(OUT)
