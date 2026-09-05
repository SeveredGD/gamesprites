// Live-game catalogue; ownership and purchases here are preview-only.
const tinkerPetCatalogue=[
 {id:'clicks',name:'Clicks',effect:'2% chance on hit to poison.',price:250000,note:'It is not waving.'},
 {id:'buckle',name:'Buckle',effect:'+5% sunder.',price:450000,note:'Built like a shield. Thinks like a spoon.'},
 {id:'scraps',name:'Scraps',effect:'One scrap in ten yields a little extra gem dust.',price:350000,gate:'Salvage 3,000 items first.'},
 {id:'kettle',name:'Kettle',effect:'Now and then digs up a clockwork gear.',price:800000,note:'Runs hot. Digs cold.'},
 {id:'clicker',name:'Clicker',effect:'Reforging is 20% less likely to destroy an item.',price:600000,gate:'Craft 100 items first.'},
 {id:'socket',name:'Socket',effect:'Fetches the special line of one 5/5 tinkered unique from your vault.',price:5000000,gate:'Find its schematic in the Everdeep.'},
 {id:'coil',name:'Coil',effect:'Occasionally miscalibrates into five critical strikes in a row.',cost:'20 of every gem shard',gate:'Find its schematic from a monster kill.'}
];
function tinkerPetsHtml(state){
 return '<div class="tk-sectionline"><span>Clockwork Menagerie</span><small>Existing game catalogue · sample progress</small></div><div class="tk-pets">'+tinkerPetCatalogue.map(p=>{
 const owned=!!(state.petOwned&&state.petOwned[p.id]);const locked=!!p.gate;const poor=p.price>state.gold;
 const label=owned?'Owned':locked?'Locked':poor?'Need '+p.price.toLocaleString()+'g':'Buy · '+p.price.toLocaleString()+'g';
 return '<article class="tk-product"><div class="tk-product-head"><span class="tk-art" aria-hidden="true"></span><div><h3>'+p.name+'</h3><span class="tk-sub">'+(p.cost||p.price.toLocaleString()+' gold')+'</span></div></div><p class="tk-pet-effect">'+p.effect+'</p><p class="tk-copy">'+(p.gate||p.note)+'</p><button type="button" class="tk-button '+(!locked&&!poor&&!owned?'primary':'')+'" data-action="pet-'+p.id+'" '+(owned||locked||poor?'disabled':'')+'>'+label+'</button></article>';
 }).join('')+'</div>';
}
function tinkerPetBuy(state,id){const p=tinkerPetCatalogue.find(p=>p.id===id);if(!p||p.gate||!p.price||state.gold<p.price||(state.petOwned&&state.petOwned[id]))return;state.gold-=p.price;state.petOwned=state.petOwned||{};state.petOwned[id]=true;state.message=p.name+' joins your menagerie. Preview only.';}
