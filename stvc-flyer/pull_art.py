import pathlib
import base64
from playwright.sync_api import sync_playwright
root=pathlib.Path('/Users/vosslab/nsh/TYPESCRIPT')
out=pathlib.Path('output/pdf/stvc-flyer-assets')
art={'taq':root/'ms-taq-man/src/art/taq_man.svg','buddy':root/'ms-taq-man/src/art/buddy.svg','surgeon':root/'plaque-attack/src/assets/surgeon.svg','isp':root/'bad-cell-day/src/assets/isp.svg','pac':root/'bad-cell-day/src/assets/pac.svg'}
with sync_playwright() as p:
 browser=p.chromium.launch()
 page=browser.new_page(viewport={'width':900,'height':900},device_scale_factor=2)
 for name,path in art.items():
  data=base64.b64encode(path.read_bytes()).decode()
  page.set_content('<style>body{margin:0;background:transparent}img{width:360px;height:360px;object-fit:contain}</style><img src="data:image/svg+xml;base64,'+data+'">')
  page.locator('img').screenshot(path=str(out/(name+'-art.png')),omit_background=True)
 page.goto('https://vosslab.github.io/steroid-quest-into-the-nucleus/',wait_until='networkidle')
 page.locator('.steroid-mark').screenshot(path=str(out/'steroid-logo.png'),omit_background=True)
 browser.close()
