import sys
import subprocess
import cv2
exec(open('_temp/stvc-flyer/make_codes.py').read().split('for name,color,url')[0])
url='https://vosslab.github.io/steroid-quest-into-the-nucleus/'
for mask in range(8):
 qr=qrtool.build_qr(url,4,20)
 qr.mask_pattern=mask
 qr.make(fit=True)
 qr.make_image(image_factory=qrcode.image.styledpil.StyledPilImage,color_mask=qrcode.image.styles.colormasks.SolidFillColorMask(front_color=(200,0,133))).save(out/'steroid-quest-into-the-nucleus.png')
 subprocess.run([sys.executable,'output/pdf/build_stvc_flyer.py'],check=True,stdout=subprocess.DEVNULL)
 subprocess.run(['pdftoppm','-r','200','-singlefile','-png','output/pdf/stvc-office-door-flyer.pdf','_temp/stvc-flyer/preview'],check=True)
 im=cv2.imread('_temp/stvc-flyer/preview.png');s=200/72
 crop=im[int((792-39-110)*s):int((792-39)*s),int(450*s):int(560*s)]
 value=cv2.QRCodeDetector().detectAndDecode(crop)[0]
 print(mask, bool(value))
 if value==url:
  break
else:
 raise RuntimeError('No mask decoded')
