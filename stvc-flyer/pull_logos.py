import pathlib
import base64
from playwright.sync_api import sync_playwright
out=pathlib.Path('output/pdf/stvc-flyer-assets')
with sync_playwright() as p:
 browser=p.chromium.launch()
 page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=2)
 for name,selector,bg in [('ms-taq-man','.game-logo','#08131f'),('plaque-attack','#game_title','#241f33'),('bad-cell-day','.intro h2','#edc0c0')]:
  page.goto('https://vosslab.github.io/'+name+'/',wait_until='networkidle')
  markup=page.locator(selector).evaluate('(e)=>e.outerHTML')
  page.evaluate('''([markup,bg])=>{document.body.innerHTML='<div id="capture" class="game_shell intro">'+markup+'</div>';const s=document.createElement('style');s.textContent=`body{margin:0;background:white} #capture{display:block;width:660px;min-height:0;margin:0;padding:24px;background:${bg};overflow:visible;box-sizing:border-box} #capture h1,#capture h2{transform:none;margin:0;font-size:90px;white-space:nowrap} #capture img{width:100%;max-width:none;margin:0} *{animation:none!important}`;document.head.append(s)}''',[markup,bg])
  page.locator('#capture').screenshot(path=str(out/(name+'-logo.png')))
  data=base64.b64encode((out/(name+'-logo.png')).read_bytes()).decode()
  page.set_content('<div id="badge" style="width:400px;height:400px;background:white;display:flex;align-items:center;justify-content:center"><img style="width:380px;height:auto" src="data:image/png;base64,'+data+'"></div>')
  page.locator('#badge').screenshot(path=str(out/(name+'-badge.png')))
 browser.close()
