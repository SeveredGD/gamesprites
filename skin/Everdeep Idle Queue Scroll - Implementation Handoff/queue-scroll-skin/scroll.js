const baseScrollRender=renderIdleQueue;
renderIdleQueue=function(){
 const old=document.querySelector('.q-list')?.scrollTop||0;
 const rewardsOpen=document.querySelector('.reward-drawer')?.open||false;
 baseScrollRender();
 document.querySelector('.q-header>span').textContent='IDLE QUEUE';
 document.querySelectorAll('.q-row').forEach((row,i)=>{
  const e=idleQueue[i],icon=document.createElement('span');icon.className='atlas-icon';icon.setAttribute('aria-hidden','true');
  if(e.type==='farm'||e.type==='act'){icon.classList.add('atlas-act');const pos=[[100,0],[0,0],[50,0],[50,100],[0,50]][e.actIdx||0];icon.style.backgroundPosition=pos[0]+'% '+pos[1]+'%'}
  else if(e.type==='bountyhunt'){icon.classList.add('atlas-bounty')}
  else{icon.classList.add('atlas-run');const pos={boss:[50,100],delve:[0,100],bloodpit:[100,0],everdeep:[50,0]}[e.type]||[50,0];icon.style.backgroundPosition=pos[0]+'% '+pos[1]+'%'}
  const name=row.querySelector('.q-name');name.textContent=name.textContent.replace(/^[^A-Za-z]+/,'')+(e.supplies?' · Supplied':'');row.insertBefore(icon,name);
  const controls=document.createElement('div');controls.className='run-controls';
  Array.from(row.children).forEach(el=>{if(el!==icon&&el!==name&&el!==row.firstElementChild&&!el.classList.contains('q-number'))controls.append(el)});
  row.append(controls);
 });
 const list=document.querySelector('.q-list');if(list){list.scrollTop=old;list.tabIndex=0;list.setAttribute('aria-label','Scrollable run queue')}
 const rewards=document.querySelector('.q-rewards');
 if(rewards){
  const drawer=document.createElement('details');drawer.className='reward-drawer';drawer.open=rewardsOpen;
  const summary=document.createElement('summary');summary.innerHTML='<img src="queue-skin-assets/chest.png" alt=""> <span>Pending Rewards <b>'+pendingRewards.length+'</b></span><small>Open / close</small>';drawer.append(summary);
  const content=document.createElement('div');content.className='reward-drawer-content';
  const heading=rewards.firstElementChild;const reviewAll=heading?.querySelector('button');if(reviewAll){const actions=document.createElement('div');actions.className='reward-actions';actions.append(reviewAll);content.append(actions)}
  heading?.remove();while(rewards.firstChild)content.append(rewards.firstChild);
  drawer.append(content);rewards.append(drawer);
 }
};
document.body.className='scrollskin';
document.querySelector('header h1').textContent='Idle Queue · Silver scroll';
document.querySelector('header p').textContent='Existing queue controls and expedition icons. Only the run list scrolls.';
document.querySelector('.eyebrow').textContent='EVERDEEP · SILVER SCROLL SKIN';
document.querySelector('.tools button[onclick="exportNotes()"]').remove();
const longOption=document.createElement('option');longOption.value='long';longOption.textContent='Long queue (scroll test)';document.getElementById('previewState').append(longOption);
const oldSample=sample;sample=function(state){oldSample(state==='long'?'ready':state);if(state==='long'){idleQueue=Array.from({length:4},()=>JSON.parse(JSON.stringify(idleQueue))).flat();renderIdleQueue()}document.querySelector('.q-list').scrollTop=0};
sample('long');document.getElementById('previewState').value='long';
