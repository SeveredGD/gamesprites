from pathlib import Path
from collections import deque
import json
import numpy as np
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1]
atlas=Image.open(root/'source/cursor-atlas.png').convert('RGBA')
names=['default','pointer','attack','inspect','blocked','wait']
fallbacks=['default','pointer','crosshair','zoom-in','not-allowed','wait']
manifest={}
sheet=Image.new('RGB',(720,280),'#23262b');draw=ImageDraw.Draw(sheet)
for i,name in enumerate(names):
    correction=root/'source'/f'{name}-v2.png'
    if correction.exists():
        source=Image.open(correction).convert('RGBA')
        a=np.array(source)
    else:
        x=(i%3)*512;y=(i//3)*512
        a=np.array(atlas.crop((x,y,x+512,y+512)))
    sh,sw=a.shape[:2]
    bright=a[:,:,:3].min(axis=2)>185
    mask=np.zeros((sh,sw),bool);q=deque()
    for k in range(max(sw,sh)):
        points=[]
        if k<sw: points.extend([(k,0),(k,sh-1)])
        if k<sh: points.extend([(0,k),(sw-1,k)])
        for xx,yy in points:
            if bright[yy,xx] and not mask[yy,xx]:mask[yy,xx]=True;q.append((xx,yy))
    if name=='wait':
        # White atlas backing trapped between the glass and hourglass posts.
        for xx in (175,300):
            for yy in range(100,390):
                if bright[yy,xx] and not mask[yy,xx]:mask[yy,xx]=True;q.append((xx,yy))
    while q:
        xx,yy=q.popleft()
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx,ny=xx+dx,yy+dy
            if 0<=nx<sw and 0<=ny<sh and bright[ny,nx] and not mask[ny,nx]:mask[ny,nx]=True;q.append((nx,ny))
    # Respect genuine generated alpha; background flood-removal is for the original atlas.
    a[mask]=0
    img=Image.fromarray(a);bounds=img.getbbox();img=img.crop(bounds)
    # First opaque top-row pixel is the arrow/blade/fingertip interaction point.
    al=np.array(img)[:,:,3];top=int(np.where(al.max(axis=1)>128)[0][0]);tipx=int(np.where(al[top]>128)[0].mean())
    if name=='inspect':tipx=int(img.width*.35);top=int(img.height*.34)
    if name=='wait':tipx=img.width//2;top=img.height//2
    manifest[name]={}
    for size in [32,48,64]:
        scale=(size-4)/max(img.size);w=round(img.width*scale);h=round(img.height*scale)
        out=Image.new('RGBA',(size,size));out.alpha_composite(img.resize((w,h),Image.Resampling.LANCZOS),(2,2))
        out.save(root/'assets'/f'{name}-{size}.png')
        hot=[min(size-1,round(tipx*scale)+2),min(size-1,round(top*scale)+2)]
        manifest[name][str(size)]={'file':f'assets/{name}-{size}.png','hotspot':hot,'fallback':fallbacks[i]}
        px=i*120+(0 if size==32 else 36 if size==48 else 0);py=35 if size!=64 else 125
        sheet.paste(out,(px,py),out)
    draw.text((i*120+4,10),name,fill='#ded4b8')
draw.text((10,220),'Top: actual 32px and 48px. Bottom: 64px accessibility size.',fill='white')
sheet.save(root/'cursor-size-check.png')
(root/'hotspots.json').write_text(json.dumps(manifest,indent=2))
css=['/* Opt in on the game root. Text fields retain native text cursors. */']
for size in [32,48,64]:
    for name in names:
        d=manifest[name][str(size)];x,y=d['hotspot']
        selector=f'.ed-cursors-{size}' if name=='default' else f'.ed-cursors-{size} [data-cursor="{name}"]'
        if name=='pointer':selector+=f', .ed-cursors-{size} button:not(:disabled), .ed-cursors-{size} a[href], .ed-cursors-{size} select, .ed-cursors-{size} summary, .ed-cursors-{size} label[for], .ed-cursors-{size} input[type="checkbox"], .ed-cursors-{size} input[type="radio"], .ed-cursors-{size} input[type="range"], .ed-cursors-{size} [onclick], .ed-cursors-{size} [style*="cursor:pointer"], .ed-cursors-{size} [style*="cursor: pointer"]'
        if name=='blocked':selector+=f', .ed-cursors-{size} button:disabled'
        important=' !important' if name!='default' else ''
        css.append(selector+' { cursor: url("'+d['file']+'?v=2") '+str(x)+' '+str(y)+', '+d['fallback']+important+'; }')
css.append('[class*="ed-cursors-"] input, [class*="ed-cursors-"] textarea { cursor: text; }')
css.append('[class*="ed-cursors-"] [style*="cursor:grab"], [class*="ed-cursors-"] [style*="cursor: grab"] { cursor: grab !important; }')
css.append('[class*="ed-cursors-"] [style*="cursor:grabbing"], [class*="ed-cursors-"] [style*="cursor: grabbing"] { cursor: grabbing !important; }')
css.append('[class*="ed-cursors-"] [style*="cursor:col-resize"], [class*="ed-cursors-"] [style*="cursor: col-resize"] { cursor: col-resize !important; }')
css.append('[class*="ed-cursors-"] [style*="cursor:ns-resize"], [class*="ed-cursors-"] [style*="cursor: ns-resize"] { cursor: ns-resize !important; }')
(root/'cursors.css').write_text('\n'.join(css))
print('18 transparent cursors, CSS, hotspot manifest and size QA saved.')
