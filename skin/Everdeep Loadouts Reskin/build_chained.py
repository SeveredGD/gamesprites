from pathlib import Path
import json
from PIL import Image, ImageDraw
import numpy as np
base=Path(__file__).parent
code=(base/'build_production.py').read_text(encoding='utf-8')
code=code.replace("/'production'","/'chained-armory-production'")
code=code.replace('exec-9d56ff87-3c7b-4c82-9ef3-41060630d41a.png','exec-75c531c2-bcd1-49de-87ad-046d52538bfd.png')
start=code.index('specs=');end=code.index('\nmanifest=',start)
code=code[:start]+"specs=[('modal-frame',(15,30,775,990),(155,155,180,155)),('tab-silver',(775,40,1510,218),(60,95,60,95)),('tab-gold',(775,220,1510,389),(60,95,60,95)),('button-silver',(780,396,1500,547),(35,35,35,35)),('button-gold',(780,548,1500,701),(35,35,35,35)),('crest',(825,710,1440,966),None)]"+code[end:]
# Replace the repeating edge's center medallions with neighboring straight rails.
code=code.replace('cuts[name]=out',"""if name=='modal-frame':
        w,h=out.size
        out.paste(out.crop((220,0,280,60)),(335,0))
        out.paste(out.crop((220,h-65,280,h)),(335,h-65))
    cuts[name]=out""")
code=code.replace('border-width:50px;border-image-source','border-width:62px 62px 72px;border-image-source').replace('border-image-slice:100','border-image-slice:155 155 180 155')
code=code.replace('border-width:21px;border-image-slice:42 fill','border-width:30px 47.5px;border-image-slice:60 95 fill')
code=code.replace('border-width:12.5px;border-image-slice:25 fill','border-width:17.5px;border-image-slice:35 fill')
code=code.replace('Choose build ▾',"${i===0?'Active':'Equip'}")
code=code.replace('<div class="row"><div>${n}', '<div class="row skin build-row ${i===0?\'selected\':\'\'}"><div>${n}')
code=code.replace('Loadout skin • resizing preview','Chained Armory • production skin')
exec(compile(code,str(base/'build_production.py'),'exec'))
ROOT=base/'chained-armory-production'
manifest=json.loads((ROOT/'skin.json').read_text())
original=Image.open(base/'elaborate-concepts/01-chained-armory.png').convert('RGBA')
# Original approved row borders, with all baked text and icons removed.
for name,box in [('row-gold',(89,340,1414,501)),('row-silver',(89,508,1414,669))]:
    out=original.crop(box);w,h=out.size
    ImageDraw.Draw(out).rectangle((27,18,w-28,h-19),fill=(18,22,23,255))
    out.save(ROOT/f'assets/{name}.png')
    dest=ROOT/'slices'/name;dest.mkdir(exist_ok=True)
    xs=[0,30,w-30,w];ys=[0,22,h-22,h];files={}
    for row in range(3):
        for col in range(3):
            key=['top','middle','bottom'][row]+'-'+['left','center','right'][col]
            out.crop((xs[col],ys[row],xs[col+1],ys[row+1])).save(dest/f'{key}.png')
            files[key]=f'slices/{name}/{key}.png'
    manifest['assets'][name]={'file':f'assets/{name}.png','width':w,'height':h,'insets':dict(top=22,right=30,bottom=22,left=30),'slices':files,'source':'approved mockup, content cleared','recommendedScale':.5}
# Extract a short suspension chain directly from the approved mockup.
chain=original.crop((96,0,147,105))
a=np.array(chain).astype(float);lum=a[:,:,:3].max(axis=2)
alpha=np.clip((lum-27)/30,0,1)
a[:,:,3]=alpha*255;a[alpha==0,:3]=0
chain=Image.fromarray(a.astype('uint8'),'RGBA');chain.save(ROOT/'assets/suspension-chain.png')
manifest['assets']['suspension-chain']={'file':'assets/suspension-chain.png','width':51,'height':105,'source':'approved mockup','usage':'Fixed aspect ratio decoration; top deliberately continues beyond viewport. Do not stretch.'}
(ROOT/'skin.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
css=(ROOT/'loadout-skin.css').read_text(encoding='utf-8')
css+='\n.build-row{border-width:11px 15px!important;border-image: url(assets/row-silver.png) 22 30 fill stretch;margin:10px 0;padding:12px!important}.build-row.selected{border-image-source:url(assets/row-gold.png)}.suspension{position:absolute;top:-115px;width:36px;height:auto;pointer-events:none}.suspension.left{left:-37px}.suspension.right{right:-37px}.modal-frame{background-clip:border-box;border-image-repeat:round}.tab{min-height:76px!important} @media(max-width:560px){.suspension.left{left:-12px}.suspension.right{right:-12px}.suspension{top:-88px}.tab{border-width:22px 35px;min-height:62px!important}}'
(ROOT/'loadout-skin.css').write_text(css,encoding='utf-8')
html=(ROOT/'preview.html').read_text(encoding='utf-8').replace('<h1>LOADOUTS</h1>','<img class="suspension left" src="assets/suspension-chain.png" alt=""><img class="suspension right" src="assets/suspension-chain.png" alt=""><h1>LOADOUTS</h1>')
(ROOT/'preview.html').write_text(html,encoding='utf-8')
print('Chained kit complete:',len(manifest['assets']),'assets')
