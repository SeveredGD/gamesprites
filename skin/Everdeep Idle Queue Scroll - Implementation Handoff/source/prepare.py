from pathlib import Path
from PIL import Image
import numpy as np,json
p=Path(__file__).parent
im=Image.open(p/'silver-scroll-components-magenta.png').convert('RGBA');w,h=im.size
bands=[('header',0,.21),('body',.22,.57),('footer',.60,.81),('run',.83,.96)]
meta={}
for name,y0,y1 in bands:
 c=im.crop((0,int(h*y0),w,int(h*y1)));a=np.array(c);r,g,b=[a[:,:,i].astype(float) for i in range(3)]
 # Separate saturated magenta key from gray/black art; retain violet title gems.
 key=(r>110)&(b>100)&(r>g*1.6)&(b>g*1.6)&(r+b>330)
 a[key,3]=0
 # Remove magenta fringe, including partially mixed edge pixels.
 spill=(r-g>35)&(b-g>35)&(r>100)&(b>100)
 a[spill,0]=a[spill,1];a[spill,2]=a[spill,1]
 c=Image.fromarray(a);bb=c.getbbox();c=c.crop(bb);c.save(p/(name+'.png'))
 meta[name]={'size':c.size,'sourceCrop':[bb[0],bb[1]+int(h*y0),bb[2],bb[3]+int(h*y0)]}
meta['body']['slice']=[24,24,24,24];meta['run']['slice']=[18,22,18,22];meta['footer']['slice']=[45,205,45,205]
(p/'slices.json').write_text(json.dumps(meta,indent=2))
print(meta)
