from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "Everdeep_Icon_Curator.html"


def collect_icons() -> tuple[list[dict], list[str]]:
    icons: list[dict] = []
    warnings: list[str] = []
    for manifest_path in sorted(ROOT.rglob("*.json")):
        if manifest_path.name == "everdeep-icon-exclusions.json":
            continue
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception as exc:
            warnings.append(f"Could not read {manifest_path.relative_to(ROOT)}: {exc}")
            continue
        frames = data.get("frames")
        image_name = data.get("image")
        if not isinstance(frames, list) or not image_name:
            continue
        image_path = manifest_path.parent / image_name
        if not image_path.exists():
            warnings.append(f"Missing image for {manifest_path.relative_to(ROOT)}: {image_name}")
            continue
        manifest_rel = manifest_path.relative_to(ROOT).as_posix()
        image_rel = image_path.relative_to(ROOT).as_posix()
        category = str(data.get("category") or manifest_path.parent.name)
        sheet = data.get("sheet") or {}
        image_width = int(sheet.get("imageWidth") or 0)
        image_height = int(sheet.get("imageHeight") or 0)
        for fallback_index, frame in enumerate(frames):
            index = int(frame.get("index", fallback_index))
            icon_id = f"{manifest_rel}#{index}"
            icons.append(
                {
                    "id": icon_id,
                    "name": str(frame.get("name") or f"Frame {index}"),
                    "category": category,
                    "folder": manifest_path.parent.relative_to(ROOT).as_posix(),
                    "sheet": manifest_path.stem,
                    "manifest": manifest_rel,
                    "image": image_rel,
                    "index": index,
                    "row": int(frame.get("row", 0)),
                    "col": int(frame.get("col", 0)),
                    "x": int(frame.get("x", 0)),
                    "y": int(frame.get("y", 0)),
                    "width": int(frame.get("width", data.get("frameWidth", 64))),
                    "height": int(frame.get("height", data.get("frameHeight", 64))),
                    "imageWidth": image_width,
                    "imageHeight": image_height,
                }
            )
    return icons, warnings


HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Everdeep Icon Curator</title>
<style>
:root{color-scheme:dark;--bg:#090a0d;--panel:#12151b;--line:#303642;--gold:#d5ad55;--text:#e8e2d6;--muted:#9b9da6;--red:#ef5d62;--green:#70c48d;--card-size:148px}
*{box-sizing:border-box} body{margin:0;background:radial-gradient(circle at top,#191922 0,#090a0d 56%);color:var(--text);font:14px/1.4 Inter,Segoe UI,sans-serif;min-height:100vh}
header{position:sticky;top:0;z-index:20;background:rgba(9,10,13,.96);backdrop-filter:blur(12px);border-bottom:1px solid #3b3425;box-shadow:0 10px 30px #0009}
.top{display:flex;align-items:center;gap:18px;padding:14px 18px 9px}.brand{min-width:245px}.brand h1{font:700 22px Georgia,serif;color:#f0d487;margin:0}.brand p{margin:2px 0 0;color:var(--muted);font-size:12px}
.counts{display:flex;gap:9px;flex-wrap:wrap}.pill{border:1px solid var(--line);border-radius:999px;padding:5px 10px;background:#11141a}.pill b{color:#fff}.pill.bad b{color:var(--red)}
.toolbar{display:grid;grid-template-columns:minmax(220px,1fr) 190px 210px 150px auto;gap:8px;padding:0 18px 12px}.toolbar input,.toolbar select,.toolbar button,.actions button{min-height:36px;border:1px solid var(--line);border-radius:5px;background:#151922;color:var(--text);padding:7px 10px}.toolbar button,.actions button{cursor:pointer}.toolbar button:hover,.actions button:hover{border-color:var(--gold);color:#ffe7a5}
.actions{display:flex;gap:8px;flex-wrap:wrap;padding:11px 18px;border-top:1px solid #20242c;background:#0e1116}.actions .danger{border-color:#64353a;color:#ff9ea2}.actions .good{border-color:#315841;color:#9be0b2}.actions .primary{border-color:#715f32;color:#f1d78e}
main{padding:18px}.empty{padding:70px 20px;text-align:center;color:var(--muted);font-size:16px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(var(--card-size),1fr));gap:10px;align-items:stretch}
.card{position:relative;display:flex;flex-direction:column;align-items:center;gap:7px;min-width:0;padding:11px 8px 9px;border:1px solid #292e38;border-radius:7px;background:linear-gradient(#171b22,#101319);color:var(--text);cursor:pointer;text-align:center;box-shadow:inset 0 1px #ffffff08}.card:hover{border-color:#7b683c;transform:translateY(-1px)}.card.excluded{border-color:var(--red);background:linear-gradient(#28171b,#151116);box-shadow:inset 0 0 0 1px #ef5d6240}.card.excluded:after{content:"DO NOT USE";position:absolute;top:6px;right:6px;background:#b5383e;color:white;border-radius:3px;padding:2px 5px;font-size:9px;font-weight:800;letter-spacing:.5px}
.sprite{width:68px;height:68px;background-repeat:no-repeat;image-rendering:pixelated;filter:drop-shadow(0 4px 5px #0008)}.name{font-weight:650;line-height:1.15;min-height:31px;display:flex;align-items:center;justify-content:center}.meta{font-size:10px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}.index{position:absolute;top:7px;left:7px;color:#747984;font-size:9px}
.notice{margin:0 18px 14px;padding:9px 11px;border:1px solid #6d5630;background:#211a0d;color:#e9cc88;border-radius:5px}.hidden{display:none!important}
@media(max-width:850px){.top{align-items:flex-start;flex-direction:column}.toolbar{grid-template-columns:1fr 1fr}.toolbar input{grid-column:1/-1}.actions{overflow:auto;flex-wrap:nowrap}.actions button{white-space:nowrap}}
</style>
</head>
<body>
<header>
  <div class="top"><div class="brand"><h1>Everdeep Icon Curator</h1><p>Click any icon to mark it unusable on future sheets.</p></div><div class="counts"><span class="pill"><b id="total-count">0</b> icons</span><span class="pill"><b id="visible-count">0</b> visible</span><span class="pill bad"><b id="excluded-count">0</b> excluded</span><span class="pill"><b id="sheet-count">0</b> sheets</span></div></div>
  <div class="toolbar">
    <input id="search" type="search" placeholder="Search icon, category, sheet…" autofocus>
    <select id="category"><option value="">All categories</option></select>
    <select id="sheet"><option value="">All sheets</option></select>
    <select id="status"><option value="all">All statuses</option><option value="allowed">Allowed only</option><option value="excluded">Excluded only</option></select>
    <button id="reset-filters" type="button">Reset filters</button>
  </div>
  <div class="actions">
    <button id="exclude-visible" class="danger" type="button">Exclude visible</button>
    <button id="allow-visible" class="good" type="button">Allow visible</button>
    <button id="clear-all" type="button">Clear exclusions</button>
    <button id="export-json" class="primary" type="button">Export exclusions JSON</button>
    <button id="export-text" class="primary" type="button">Export instructions TXT</button>
    <button id="import-json" type="button">Import exclusions JSON</button>
    <input id="import-file" class="hidden" type="file" accept="application/json,.json">
  </div>
  <div id="warning" class="notice hidden"></div>
</header>
<main><div id="grid" class="grid"></div><div id="empty" class="empty hidden">No icons match these filters.</div></main>
<script>
const ICONS=__ICON_DATA__;
const BUILD_WARNINGS=__WARNINGS__;
const SOURCE_ROOT='C:\\Users\\garre\\Downloads\\new items\\production sheets';
const STORAGE_KEY='everdeep-icon-curator-exclusions-v1';
const $=s=>document.querySelector(s);
const grid=$('#grid'),empty=$('#empty'),search=$('#search'),category=$('#category'),sheet=$('#sheet'),status=$('#status');
let excluded=new Set(); let visible=[];
try{excluded=new Set(JSON.parse(localStorage.getItem(STORAGE_KEY)||'[]'))}catch(_){excluded=new Set()}

function natural(a,b){return a.localeCompare(b,undefined,{numeric:true,sensitivity:'base'})}
function fillSelect(el,values){for(const value of [...new Set(values)].sort(natural)){const o=document.createElement('option');o.value=value;o.textContent=value;el.append(o)}}
fillSelect(category,ICONS.map(x=>x.category)); fillSelect(sheet,ICONS.map(x=>x.sheet));

function drawSprite(node,icon){
  const scale=Math.min(1,64/icon.width,64/icon.height);
  node.style.width=Math.round(icon.width*scale)+'px';node.style.height=Math.round(icon.height*scale)+'px';
  node.style.backgroundImage=`url("${encodeURI(icon.image)}")`;
  node.style.backgroundSize=`${Math.round(icon.imageWidth*scale)}px ${Math.round(icon.imageHeight*scale)}px`;
  node.style.backgroundPosition=`${Math.round(-icon.x*scale)}px ${Math.round(-icon.y*scale)}px`;
}
function cardFor(icon){
  const b=document.createElement('button');b.type='button';b.className='card';b.dataset.id=icon.id;b.title=`${icon.name}\n${icon.category}\n${icon.sheet} · frame ${icon.index}`;
  b.innerHTML=`<span class="index">#${icon.index}</span><span class="sprite"></span><span class="name"></span><span class="meta"></span>`;
  b.querySelector('.name').textContent=icon.name;b.querySelector('.meta').textContent=`${icon.category} · ${icon.sheet}`;drawSprite(b.querySelector('.sprite'),icon);
  b.addEventListener('click',()=>{excluded.has(icon.id)?excluded.delete(icon.id):excluded.add(icon.id);save();render()});return b;
}
function filtered(){
  const q=search.value.trim().toLowerCase(),cat=category.value,sh=sheet.value,st=status.value;
  return ICONS.filter(i=>(!q||`${i.name} ${i.category} ${i.sheet} ${i.folder}`.toLowerCase().includes(q))&&(!cat||i.category===cat)&&(!sh||i.sheet===sh)&&(st==='all'||(st==='excluded')===excluded.has(i.id)));
}
function render(){
  visible=filtered();const frag=document.createDocumentFragment();for(const icon of visible){const card=cardFor(icon);card.classList.toggle('excluded',excluded.has(icon.id));frag.append(card)}grid.replaceChildren(frag);empty.classList.toggle('hidden',visible.length>0);
  $('#total-count').textContent=ICONS.length.toLocaleString();$('#visible-count').textContent=visible.length.toLocaleString();$('#excluded-count').textContent=excluded.size.toLocaleString();$('#sheet-count').textContent=new Set(ICONS.map(i=>i.sheet)).size;
}
function save(){localStorage.setItem(STORAGE_KEY,JSON.stringify([...excluded]))}
function download(name,type,text){const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{type}));a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)}
function excludedIcons(){return ICONS.filter(i=>excluded.has(i.id))}
function exportPayload(){const items=excludedIcons();return {schema:'everdeep-icon-exclusions/v1',generatedAt:new Date().toISOString(),sourceRoot:SOURCE_ROOT,instruction:'Never place these frames on generated or assembled item/icon sheets. Do not use them as references or substitutes.',totalIconsReviewed:ICONS.length,excludedCount:items.length,excluded:items.map(({id,name,category,folder,sheet,manifest,image,index,row,col,x,y,width,height})=>({id,name,category,folder,sheet,manifest,image,index,row,col,x,y,width,height}))}}

for(const el of [search,category,sheet,status])el.addEventListener(el===search?'input':'change',render);
$('#reset-filters').onclick=()=>{search.value='';category.value='';sheet.value='';status.value='all';render()};
$('#exclude-visible').onclick=()=>{visible.forEach(i=>excluded.add(i.id));save();render()};
$('#allow-visible').onclick=()=>{visible.forEach(i=>excluded.delete(i.id));save();render()};
$('#clear-all').onclick=()=>{if(excluded.size&&confirm(`Clear all ${excluded.size} exclusions?`)){excluded.clear();save();render()}};
$('#export-json').onclick=()=>download('everdeep-icon-exclusions.json','application/json',JSON.stringify(exportPayload(),null,2));
$('#export-text').onclick=()=>{const p=exportPayload();const lines=['EVERDEEP ICON EXCLUSION INSTRUCTIONS','',p.instruction,`Generated: ${p.generatedAt}`,`Excluded: ${p.excludedCount} of ${p.totalIconsReviewed}`,''];if(!p.excluded.length)lines.push('(No icons excluded.)');else for(const i of p.excluded)lines.push(`- [${i.category}] ${i.name} | ${i.sheet} frame ${i.index} | ${i.image}`);download('everdeep-icon-exclusion-instructions.txt','text/plain',lines.join('\n'))};
$('#import-json').onclick=()=>$('#import-file').click();
$('#import-file').onchange=async e=>{const f=e.target.files[0];if(!f)return;try{const p=JSON.parse(await f.text()),ids=Array.isArray(p)?p:(p.excluded||p.excludedIds||[]);excluded=new Set(ids.map(x=>typeof x==='string'?x:x.id).filter(Boolean));save();render()}catch(err){alert('Could not import exclusions: '+err.message)}e.target.value=''};
if(BUILD_WARNINGS.length){const w=$('#warning');w.textContent=BUILD_WARNINGS.join(' · ');w.classList.remove('hidden')}
render();
</script>
</body>
</html>'''


def main() -> None:
    icons, warnings = collect_icons()
    payload = json.dumps(icons, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    warning_payload = json.dumps(warnings, ensure_ascii=False).replace("<", "\\u003c")
    html = HTML.replace("__ICON_DATA__", payload).replace("__WARNINGS__", warning_payload)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    print(f"Sheets: {len({icon['manifest'] for icon in icons})}")
    print(f"Icons: {len(icons)}")
    print(f"Warnings: {len(warnings)}")


if __name__ == "__main__":
    main()
