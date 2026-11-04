import pathlib
import re
from playwright.sync_api import sync_playwright
folder=pathlib.Path('output/pdf/stvc-flyer-assets')
with sync_playwright() as p:
 browser=p.chromium.launch()
 page=browser.new_page()
 for path in folder.glob('*-wordmark.svg'):
  svg=path.read_text()
  w,h=map(float,re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"',svg).groups())
  page.set_content('<style>@page{margin:0}body{margin:0}svg{width:100%;height:100%}*{animation:none!important}</style>'+svg)
  page.pdf(path=str(path.with_suffix('.pdf')),width=f'{w}px',height=f'{h}px',print_background=True)
 browser.close()
