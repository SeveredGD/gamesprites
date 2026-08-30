(function(){
  'use strict';
  var root=document.getElementById('everdeep-loader');
  if(!root)return;
  var progress=62,autoTimer=null;
  var percentNodes=root.querySelectorAll('.ed-percent,.ed-relic-percent');
  var horizontalFill=root.querySelector('.ed-horizontal-bar .ed-fill');
  var arcFill=root.querySelector('.ed-arc-fill');
  var devRange=document.getElementById('progress');
  var devOutput=document.querySelector('.ed-devtools output');

  function clamp(value){return Math.max(0,Math.min(100,Number(value)||0))}
  function setProgress(value){
    progress=clamp(value);
    var ratio=progress/100;
    var left=7.03,right=6.77+(1-ratio)*86.20;
    horizontalFill.style.clipPath='inset(0 '+right.toFixed(3)+'% 0 '+left+'%)';
    arcFill.style.strokeDasharray=progress.toFixed(2)+' 100';
    percentNodes.forEach(function(node){node.textContent=Math.round(progress)+'%'});
    if(devRange)devRange.value=progress;
    if(devOutput)devOutput.value=Math.round(progress)+'%';
  }
  function show(screen,options){
    options=options||{};
    root.dataset.screen=screen==='reliquary'?'reliquary':'gate';
    document.querySelectorAll('[data-mode]').forEach(function(button){button.classList.toggle('active',button.dataset.mode===root.dataset.screen)});
    if(options.character)root.querySelector('.ed-character').textContent='Awakening · '+options.character;
    if(options.phase){root.querySelector('.ed-phase').textContent=options.phase;root.querySelector('.ed-gate-subtitle').textContent=options.phase+' Into the Deep'}
    if(options.lore)root.querySelector('.ed-lore').textContent=options.lore;
    if(options.progress!=null)setProgress(options.progress);
    root.hidden=false;
    requestAnimationFrame(function(){root.style.opacity='1'});
  }
  function hide(){root.style.opacity='0';setTimeout(function(){root.hidden=true},460)}
  function setCharacter(name){root.querySelector('.ed-character').textContent='Awakening · '+name}
  function setPhase(text){root.querySelector('.ed-phase').textContent=text}

  for(var i=0;i<15;i++){
    var mote=document.createElement('i'),duration=4+Math.random()*5;
    mote.style.left=(Math.random()*100)+'%';mote.style.animationDuration=duration+'s';mote.style.animationDelay=(-Math.random()*duration)+'s';
    root.querySelector('.ed-motes').appendChild(mote);
  }
  document.querySelectorAll('[data-mode]').forEach(function(button){button.addEventListener('click',function(){show(button.dataset.mode)})});
  devRange.addEventListener('input',function(){setProgress(devRange.value)});
  document.getElementById('autoplay').addEventListener('change',function(event){
    clearInterval(autoTimer);autoTimer=null;
    if(event.target.checked){setProgress(0);autoTimer=setInterval(function(){setProgress(progress+1);if(progress>=100){clearInterval(autoTimer);autoTimer=null;event.target.checked=false}},55)}
  });
  if(new URLSearchParams(location.search).get('clean')==='1')document.documentElement.classList.add('clean');
  setProgress(progress);
  window.EverdeepLoadingScreens={show:show,hide:hide,setProgress:setProgress,setCharacter:setCharacter,setPhase:setPhase};
})();
