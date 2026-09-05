from pathlib import Path
from collections import deque
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'
SRC=ROOT/'source'/'tinker-clockwork-kit-v2-source.png'
im=Image.open(SRC).convert('RGBA')

def extract(box):
    a=np.array(im.crop(box))
    # Only remove light pixels connected to the exterior, retaining metal highlights.
    bright=a[:,:,:3].min(axis=2)>170
    seen=np.zeros(bright.shape,bool)
    h,w=bright.shape
    q=deque()
    for x in range(w):
        for y in (0,h-1):
            if bright[y,x]: q.append((x,y));seen[y,x]=True
    for y in range(h):
        for x in (0,w-1):
            if bright[y,x]: q.append((x,y));seen[y,x]=True
    while q:
        x,y=q.popleft()
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            xx,yy=x+dx,y+dy
            if 0<=xx<w and 0<=yy<h and bright[yy,xx] and not seen[yy,xx]:
                seen[yy,xx]=True;q.append((xx,yy))
    a[seen]=0
    return Image.fromarray(a)

manifest={'version':1,'source':SRC.name,'assets':{}}

def clear_dark_backing(img):
    a=np.array(img)
    value=a[:,:,:3].max(axis=2).astype(float)
    factor=np.clip((value-42)/32,0,1)
    a[:,:,3]=(a[:,:,3]*factor).astype('uint8')
    return Image.fromarray(a)

def extract_control(box):
    a=np.array(im.crop(box))
    rgb=a[:,:,:3].astype(float)
    lo=rgb.min(axis=2); spread=rgb.max(axis=2)-lo
    # Seed white background everywhere, including enclosed pipe openings.
    removed=(lo>225)&(spread<25)
    candidates=(lo>160)&(spread<40)
    while True:
        adjacent=np.array(Image.fromarray(removed.astype('uint8')*255).filter(ImageFilter.MaxFilter(3)))>0
        grown=removed|(adjacent&candidates)
        if np.array_equal(grown,removed):break
        removed=grown
    # Remove the narrow neutral matte fringe next to the identified background.
    for _ in range(2):
        adjacent=np.array(Image.fromarray(removed.astype('uint8')*255).filter(ImageFilter.MaxFilter(3)))>0
        removed|=adjacent&(lo>115)&(spread<40)
    a[removed]=0
    return Image.fromarray(a)

def save_slices(name,img,slices,scale,minsize):
    t,r,b,l=slices;w,h=img.size
    img.save(OUT/(name+'.png'))
    xs=[0,l,w-r,w];ys=[0,t,h-b,h]
    labels=[['top-left','top','top-right'],['left','center','right'],['bottom-left','bottom','bottom-right']]
    folder=OUT/name;folder.mkdir(exist_ok=True)
    for yi in range(3):
        for xi in range(3):
            img.crop((xs[xi],ys[yi],xs[xi+1],ys[yi+1])).save(folder/(labels[yi][xi]+'.png'))
    manifest['assets'][name]={'file':name+'.png','size':[w,h],'sliceTRBL':slices,'displayScale':scale,'borderWidthTRBL':[v*scale for v in slices],'minimumSize':minsize}
    return img

# Panels: constant straight edge strips replace the variable central mechanisms.
# Original corners retain their exact pixels. Detached ornaments are overlaid later.
main=extract((8,0,734,879));w,h=main.size
t,r,b,l=145,156,155,155
main.paste(main.crop((225,0,226,t)).resize((w-l-r,t)),(l,0))
main.paste(main.crop((215,h-b,216,h)).resize((w-l-r,b)),(l,h-b))
main.paste(main.crop((0,400,l,401)).resize((l,h-t-b)),(0,t))
main.paste(main.crop((w-r,400,w,401)).resize((r,h-t-b)),(w-r,t))
main.paste((0,0,0,0),(l,t,w-r,h-b))
main.paste((0,0,0,0),(l,72,w-r,h-47))
main.paste((0,0,0,0),(45,t,w-43,h-b))
main=clear_dark_backing(main)
save_slices('shop-frame',main,[t,r,b,l],.5,[360,320])

anvil=extract((751,58,1205,509));w,h=anvil.size
t,r,b,l=112,110,112,110
anvil.paste(anvil.crop((180,0,181,t)).resize((w-l-r,t)),(l,0))
anvil.paste(anvil.crop((180,h-b,181,h)).resize((w-l-r,b)),(l,h-b))
anvil.paste(anvil.crop((0,140,l,141)).resize((l,h-t-b)),(0,t))
anvil.paste(anvil.crop((w-r,140,w,141)).resize((r,h-t-b)),(w-r,t))
anvil.paste((0,0,0,0),(l,t,w-r,h-b))
anvil.paste((0,0,0,0),(l,55,w-r,h-47))
anvil.paste((0,0,0,0),(49,t,w-44,h-b))
anvil=clear_dark_backing(anvil)
save_slices('improvement-frame',anvil,[t,r,b,l],.5,[260,260])

# Detached crest: retain its dark backing so it masks the straight top rail.
crest=clear_dark_backing(extract((257,0,479,112)))
crest.save(OUT/'clockwork-crest.png')
key=extract((1176,230,1254,340))
key.save(OUT/'winding-key.png')
texture=im.crop((300,350,428,478))
# Mirrored quad tile guarantees matching opposite boundaries.
tile=Image.new('RGBA',(256,256))
tile.paste(texture,(0,0));tile.paste(texture.transpose(Image.Transpose.FLIP_LEFT_RIGHT),(128,0))
tile.paste(tile.crop((0,0,256,128)).transpose(Image.Transpose.FLIP_TOP_BOTTOM),(0,128))
tile.save(OUT/'interior-tile.png')

for name,box in [('button-normal',(738,588,1243,718)),('button-pressed',(738,746,1243,876)),('tab-normal',(14,893,849,1027)),('tab-active',(14,1030,849,1164))]:
    a=extract_control(box);w,h=a.size
    save_slices(name,a,[35,110,35,110],.5,[160,h/2])

# Divider gears are five fixed ornaments over a plain repeating axle, never stretched.
divider=extract((45,1170,1209,1242));divider.save(OUT/'divider-source.png')
divider.crop((130,25,180,44)).save(OUT/'divider-axle.png')
for name,box in [('left',(24,0,104,72)),('center',(535,0,615,72)),('right',(1047,0,1127,72))]:
    divider.crop(box).save(OUT/('divider-gear-'+name+'.png'))
manifest['overlays']={'clockwork-crest':{'size':list(crest.size),'displaySize':[111,56],'anchor':'top center'},'winding-key':{'size':list(key.size),'displaySize':[39,55],'anchor':'right center, overlap 14px'}}
(ROOT/'nine-slice.json').write_text(json.dumps(manifest,indent=2))

def render9(name,size):
    d=manifest['assets'][name];s=Image.open(OUT/d['file']);w,h=s.size;t,r,b,l=d['sliceTRBL'];sc=d['displayScale']
    W,H=size;L,R,T,B=[round(v*sc) for v in (l,r,t,b)]
    out=Image.new('RGBA',size)
    if 'frame' in name:
        tx=tile.resize((128,128))
        for yy in range(8,H-8,128):
            for xx in range(8,W-8,128): out.alpha_composite(tx,(xx,yy))
        # Clear the exterior; the UI uses a separately inset tiled background.
        mask=Image.new('L',size,0);ImageDraw.Draw(mask).rectangle((16,16,W-17,H-17),fill=255)
        out.putalpha(mask)
    xs=[0,l,w-r,w];ys=[0,t,h-b,h];dx=[0,L,W-R,W];dy=[0,T,H-B,H]
    for yi in range(3):
        for xi in range(3):
            if 'frame' in name and xi==yi==1:continue
            piece=s.crop((xs[xi],ys[yi],xs[xi+1],ys[yi+1]))
            piece=piece.resize((dx[xi+1]-dx[xi],dy[yi+1]-dy[yi]),Image.Resampling.LANCZOS)
            out.alpha_composite(piece,(dx[xi],dy[yi]))
    if name=='shop-frame':out.alpha_composite(crest.resize((111,56),Image.Resampling.LANCZOS),((W-111)//2,0))
    return out

checks=[('shop-frame',(360,400)),('shop-frame',(620,360)),('improvement-frame',(260,300)),('button-normal',(180,65)),('button-normal',(340,65)),('tab-active',(300,67))]
qa=Image.new('RGB',(1040,830),'#272b31');draw=ImageDraw.Draw(qa)
positions=[(15,35),(405,35),(15,485),(310,495),(530,495),(310,610)]
for (name,size),pos in zip(checks,positions):
    img=render9(name,size);qa.paste(img,pos,img);draw.text((pos[0],pos[1]-17),name+' '+str(size),fill='white')
qa.save(ROOT/'resize-check.jpg',quality=94)
control_qa=Image.new('RGB',(920,580),'#17191d')
for row,name in enumerate(['button-normal','button-pressed','tab-normal','tab-active']):
    src=Image.open(OUT/(name+'.png'))
    # Show both endcaps at 2x so matte contamination is easy to inspect.
    for col,box in enumerate([(0,0,110,src.height),(src.width-110,0,src.width,src.height)]):
        piece=src.crop(box).resize((165,round(src.height*1.5)),Image.Resampling.NEAREST)
        piece.thumbnail((150,125))
        control_qa.paste(piece,(col*170+10,row*140+12),piece)
    small=render9(name,(340,65 if name.startswith('button') else 67))
    control_qa.paste(small,(390,row*140+35),small)
    ImageDraw.Draw(control_qa).text((745,row*140+60),name,fill='white')
control_qa.save(ROOT/'control-alpha-check.png')
for name,d in manifest['assets'].items():
    a=Image.open(OUT/d['file']);assert a.mode=='RGBA';assert a.getextrema()[3][0]==0
    t,r,b,l=d['sliceTRBL'];assert t+b<a.height and l+r<a.width
print('Built 6 nine-slice textures, 54 individual slices, detached ornaments, tiled interior, divider parts and resize QA.')
