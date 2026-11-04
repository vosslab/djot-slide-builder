import importlib.util
import pathlib
import qrcode.image.styledpil
import qrcode.image.styles.colormasks
import PIL.ImageColor
spec=importlib.util.spec_from_file_location('qrtool','/Users/vosslab/nsh/junk-drawer/QRCODE/qrcode2.py')
qrtool=importlib.util.module_from_spec(spec)
spec.loader.exec_module(qrtool)
out=pathlib.Path('output/pdf/stvc-flyer-assets')
for name,color,url in [
 ('ms-taq-man','#00775F','https://vosslab.github.io/ms-taq-man/'),
 ('plaque-attack','#935D00','https://vosslab.github.io/plaque-attack/'),
 ('bad-cell-day','#076DAD','https://vosslab.github.io/bad-cell-day/'),
 ('steroid-quest-into-the-nucleus','#C80085','https://vosslab.github.io/steroid-quest-into-the-nucleus/'),
 ('playlist-qr','#000000','https://www.youtube.com/playlist?list=PL5LJPD9b2pRYsw2sU3LRCDhvDSiZ26E48')]:
 qr=qrtool.build_qr(url,4,20)
 image=qr.make_image(image_factory=qrcode.image.styledpil.StyledPilImage,
  color_mask=qrcode.image.styles.colormasks.SolidFillColorMask(front_color=PIL.ImageColor.getrgb(color)))
 image.save(out/(name+'.png'))
