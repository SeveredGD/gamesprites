/* Local, dependency-free live DOM text. Use setText() for later updates. */
window.SilverReliquary={
  setText(element,text){
    element.classList.add('silver-reliquary');
    const layers=['outer','accent','inner','face'].map(name=>{
      const span=document.createElement('span');
      span.className='sr-'+name;
      span.textContent=String(text);
      if(name!=='face')span.setAttribute('aria-hidden','true');
      return span;
    });
    element.replaceChildren(...layers);
  },
  enhance(root=document){root.querySelectorAll('.silver-reliquary').forEach(el=>{
    if(!el.querySelector('.sr-face'))this.setText(el,el.textContent);
  });}
};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>SilverReliquary.enhance());
else SilverReliquary.enhance();
