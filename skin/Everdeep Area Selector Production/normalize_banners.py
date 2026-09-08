from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import json, shutil

root=Path(__file__).parent
folder=root/'banners'
originals=folder/'originals'
originals.mkdir(exist_ok=True)
target=(1200,200)
manifest=[]
files=sorted(folder.glob('act-*.png'))
assert len(files)==5
for path in files:
    source=originals/path.name
    if not source.exists(): shutil.copy2(path,source)
    im=Image.open(source).convert('RGB')
    result=ImageOps.fit(im,target,method=Image.Resampling.LANCZOS,centering=(1.0,.5))
    result.save(path)
    assert Image.open(path).size==target
    manifest.append({'file':path.name,'width':1200,'height':200,'original':f'originals/{path.name}','original_size':list(im.size),'method':'proportional cover crop','anchor':'right center','resampled':True})
old=folder/'manifest.json'
if old.exists() and not (originals/'manifest.json').exists():shutil.copy2(old,originals/'manifest.json')
old.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
qa=Image.new('RGB',(1200,1100),'#131515')
d=ImageDraw.Draw(qa)
for i,path in enumerate(files):
    d.text((10,i*220+4),path.name,fill='#ddc99a')
    qa.paste(Image.open(path),(0,i*220+20))
qa.save(root/'banner-size-review.jpg',quality=95)
print(json.dumps(manifest,indent=2))
