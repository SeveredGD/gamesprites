from pathlib import Path
root=Path(__file__).resolve().parents[1]
source=(root/'source'/'original-layout.html').read_text(encoding='utf-8')
# Keep the approved Brass & Iron structure and local demonstration interactions.
# Place the production skin overrides after the original style block.
source=source.replace('</style>','</style><link rel="stylesheet" href="brass-iron-clockwork.css?v=4"><link rel="stylesheet" href="pets-layout.css?v=4">',1)
source=source.replace("}else{const items=state.source", "}else if(state.page==='pets'){body=tinkerPetsHtml(state);}else{const items=state.source")
source=source.replace('</button></nav>', '</button><button type="button" data-page="pets" aria-pressed="\'+(state.page===\'pets\')+\'">Pets</button></nav>')
source=source.replace("else if(b.dataset.action==='buy'", "else if(b.dataset.action&&b.dataset.action.startsWith('pet-')){tinkerPetBuy(state,b.dataset.action.slice(4));}else if(b.dataset.action==='buy'")
start=source.index('if(globalThis.Tweak){')
end=source.index('\n})();',start)
source=source[:start]+source[end:]
html='<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Traveling Tinker — Brass & Iron Clockwork</title><script src="pets-preview.js?v=4"></script></head><body>'+source+'</body></html>'
(root/'brass-iron-preview.html').write_text(html,encoding='utf-8')
print('Built Brass & Iron layout with production clockwork skin.')
