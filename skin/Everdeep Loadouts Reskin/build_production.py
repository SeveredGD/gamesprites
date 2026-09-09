from pathlib import Path
import json, shutil
import numpy as np
from PIL import Image

ROOT=Path(__file__).parent/'production'
for d in ['source','assets','slices','qa']: (ROOT/d).mkdir(parents=True,exist_ok=True)
src=Path(r'C:\Users\garre\.codex\generated_images\01a06f4b-0bce-7340-8b9a-09a55cfa1962\exec-9d56ff87-3c7b-4c82-9ef3-41060630d41a.png')
shutil.copy2(src,ROOT/'source/loadout-skin-sheet.png')
im=Image.open(src).convert('RGB')
specs=[('modal-frame',(25,30,775,980),(100,100,100,100)),('tab-silver',(780,65,1505,235),(42,42,42,42)),('tab-gold',(780,245,1505,420),(42,42,42,42)),('button-silver',(780,435,1505,570),(25,25,25,25)),('button-gold',(780,580,1505,715),(25,25,25,25)),('crest',(890,715,1365,985),None)]
manifest={'version':1,'source':'source/loadout-skin-sheet.png','insetOrder':['top','right','bottom','left'],'assets':{}}
cuts={}
for name,box,insets in specs:
    a=np.array(im.crop(box)).astype(float)
    excess=np.maximum(0,np.minimum(a[:,:,0],a[:,:,2])-a[:,:,1])
    alpha=1-np.clip(excess/255,0,1)
    alpha[alpha<.12]=0
    spill=excess>15
    for c in [0,2]:
        a[:,:,c]=np.where(spill,np.clip((a[:,:,c]-255*(1-alpha))/np.maximum(alpha,.001),0,255),a[:,:,c])
    a[:,:,1]=np.where(spill,np.clip(a[:,:,1]/np.maximum(alpha,.001),0,255),a[:,:,1])
    a[alpha==0]=0
    out=Image.fromarray(np.dstack([a,alpha*255]).astype('uint8'),'RGBA')
    bbox=out.getbbox(); out=out.crop(bbox)
    cuts[name]=out
    out.save(ROOT/f'assets/{name}.png')
    w,h=out.size
    entry={'file':f'assets/{name}.png','width':w,'height':h,'sourceCrop':[box[0]+bbox[0],box[1]+bbox[1],box[0]+bbox[2],box[1]+bbox[3]]}
    if insets:
        t,r,b,l=insets; entry.update({'insets':dict(top=t,right=r,bottom=b,left=l),'recommendedScale':.5,'minimumDisplaySize':[(l+r)*.5+1,(t+b)*.5+1],'centerTransparent':name=='modal-frame'})
        xs=[0,l,w-r,w]; ys=[0,t,h-b,h]; entries={}
        dest=ROOT/'slices'/name;dest.mkdir(exist_ok=True)
        for row in range(3):
            for col in range(3):
                key=['top','middle','bottom'][row]+'-'+['left','center','right'][col]
                out.crop((xs[col],ys[row],xs[col+1],ys[row+1])).save(dest/f'{key}.png')
                entries[key]=f'slices/{name}/{key}.png'
        entry['slices']=entries
    manifest['assets'][name]=entry
(ROOT/'skin.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
css='''*{box-sizing:border-box} body{margin:0;background:#101416;color:#d9d3c3;font:16px Georgia,serif} button,select,input{font:inherit} .skin{border-style:solid;border-image-repeat:stretch} .modal-frame{border-width:50px;border-image-source:url(assets/modal-frame.png);border-image-slice:100;background:linear-gradient(#171c1e,#101416);background-clip:padding-box} .tab{border-width:21px;border-image-slice:42 fill;border-image-source:url(assets/tab-silver.png)} .tab.active{border-image-source:url(assets/tab-gold.png)} .action{border-width:12.5px;border-image-slice:25 fill;border-image-source:url(assets/button-silver.png)} .action.primary{border-image-source:url(assets/button-gold.png)} button.skin{background:transparent;color:inherit;cursor:pointer;min-height:50px;padding:0 10px} button.skin:hover{filter:brightness(1.2)} button.skin:focus-visible{outline:2px solid #d3b87c;outline-offset:3px}'''
(ROOT/'loadout-skin.css').write_text(css,encoding='utf-8')
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Everdeep — Loadout skin</title><link rel="stylesheet" href="loadout-skin.css"><style>
body{padding:28px 12px}.tools{max-width:980px;margin:0 auto 70px;font:14px system-ui;display:flex;gap:15px;flex-wrap:wrap;align-items:center}.tools a{color:#dac08b}.modal-frame{position:relative;width:900px;max-width:100%;margin:auto;min-height:610px}.crest{position:absolute;width:180px;height:auto;top:-100px;left:50%;transform:translateX(-50%);pointer-events:none}h1{text-align:center;letter-spacing:5px;color:#dec995;margin:20px 0 25px;font-size:27px}nav{display:flex;gap:8px;flex-wrap:wrap}nav button{flex:1;white-space:nowrap}.status{color:#c4b69b;text-align:center;padding:15px 0;border-bottom:1px solid #514d41}.content{max-height:340px;overflow:auto;scrollbar-color:#81705a #191c1d;padding:12px 2px}.row{display:flex;justify-content:space-between;align-items:center;gap:15px;padding:15px 0;border-bottom:1px solid #343a39}.row small{display:block;color:#a6a99e;margin-top:7px}.row button{min-width:160px}footer{display:flex;gap:12px;justify-content:flex-end;margin-top:20px}.hint{font:13px system-ui;color:#a1a79f;max-width:900px;margin:20px auto}.page{display:none}.page.active{display:block}@media(max-width:560px){.modal-frame{border-width:30px}.crest{width:140px;top:-80px}h1{font-size:22px}nav{gap:5px}nav button{flex-basis:100%;min-height:45px}.row{flex-wrap:wrap}.row button{width:100%}footer{flex-wrap:wrap}footer button{flex:1}.content{max-height:330px}}
</style><div class="tools"><b>Loadout skin • resizing preview</b><label>Width <input id="width" type="range" min="340" max="1100" value="900"></label><span id="size">900 px</span><a href="skin.json">Slice metadata</a></div><main class="skin modal-frame" id="modal"><img class="crest" src="assets/crest.png" alt=""><h1>LOADOUTS</h1><nav><button class="skin tab active" data-page="builds">Builds</button><button class="skin tab" data-page="auto">Auto-switch</button><button class="skin tab" data-page="loot">Loot priorities</button></nav><div class="status">Active now: Farming gear · Clearing tree</div><div class="content"><section class="page active" id="builds"></section><section class="page" id="auto"><div class="row"><div>Farm<small>Normal enemies</small></div><button class="skin action">Farming gear ▾</button></div><div class="row"><div>Bosses<small>Act and loop bosses</small></div><button class="skin action">Boss gear ▾</button></div><div class="row"><div>Special<small>Delve · Bloodpit · Bounties</small></div><button class="skin action">Keep current ▾</button></div></section><section class="page" id="loot"><div class="row"><div>Farming<small>Loot priority configuration</small></div><button class="skin action">Choose priority ▾</button></div><div class="row"><label><input type="checkbox"> Auto-gear other loadouts</label></div></section></div><footer><button class="skin action" id="close">Close</button><button class="skin action primary" id="switch">Switch now</button></footer></main><p class="hint" id="hint">Skin preview only. Tabs and width control work; game actions are visual samples. Frame corners stay fixed; the crest is a separate image. Scroll the builds list to check containment.</p><script>
const names=['Farming','Bosses','Gold find','Magic find','Survival','Experimental'];document.querySelector('#builds').innerHTML=names.map((n,i)=>`<div class="row"><div>${n}<small>Gear ${i+1} · Skill tree ${i+1}</small></div><button class="skin action ${i===0?'primary':''}">Choose build ▾</button></div>`).join('');document.querySelector('#width').oninput=e=>{document.querySelector('#modal').style.width=e.target.value+'px';document.querySelector('#size').textContent=e.target.value+' px'};document.querySelectorAll('[data-page]').forEach(b=>b.onclick=()=>{document.querySelectorAll('.tab,.page').forEach(p=>p.classList.remove('active'));b.classList.add('active');document.getElementById(b.dataset.page).classList.add('active')});document.querySelectorAll('.action').forEach(b=>b.onclick=()=>document.querySelector('#hint').textContent='Visual skin sample — wire this control to the existing loadout action in the game.');
</script></html>'''
(ROOT/'preview.html').write_text(html,encoding='utf-8')
# Contact sheet: inspect against light AND dark backgrounds for keying defects.
qa=Image.new('RGB',(1500,1100),'#303638')
for i,(name,out) in enumerate(cuts.items()):
    thumb=out.copy();thumb.thumbnail((690,330))
    x=(i%2)*750;y=(i//2)*365
    for xx in range(x,x+730,20):
        for yy in range(y,y+350,20):
            from PIL import ImageDraw
            ImageDraw.Draw(qa).rectangle((xx,yy,xx+19,yy+19),fill='#788181' if ((xx-x)//20+(yy-y)//20)%2 else '#303638')
    qa.paste(thumb,(x+15,y+10),thumb)
qa.save(ROOT/'qa/transparency-check.png')
print(json.dumps(manifest,indent=2))
