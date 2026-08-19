/* Seek-driven animation harness. The capture rig calls window.__seek(t) for
   each frame; nothing runs on a wall clock, so capture is deterministic.
   - CSS animations (anim.css classes) are paused and seeked via currentTime.
   - Shots that need custom JS motion define window.__render(t). */
(function(){
  if (location.search.indexOf('clean=1')>=0)
    document.addEventListener('DOMContentLoaded',function(){document.body.classList.add('clean')});
  var paused=false;
  function pauseAll(){
    if(paused) return; paused=true;
    (document.getAnimations?document.getAnimations():[]).forEach(function(a){
      try{a.pause();}catch(e){}
    });
  }
  // Auto-reveal: for shots without a bespoke __render, stagger a fade-up on the
  // meaningful direct children of .stage so the frame assembles instead of
  // snapping in. Bespoke shots opt out by defining window.__render.
  function autoReveal(){
    if(window.__render || window.__noauto) return;
    var stage=document.querySelector('.stage'); if(!stage) return;
    var skip={GRADE:1};
    var kids=[].slice.call(stage.children).filter(function(el){
      var c=el.className&&el.className.baseVal!==undefined?el.className.baseVal:(el.className||'');
      return !/grade|scanlines|timecode|disclaimer|card-rule/.test(c);
    });
    kids.forEach(function(el,i){
      el.style.animation='fadeUp .55s cubic-bezier(.2,.7,.2,1) '+(0.05+i*0.07).toFixed(2)+'s both';
    });
  }
  document.addEventListener('DOMContentLoaded',autoReveal);
  window.__seek=function(t){
    pauseAll();
    var ms=t*1000;
    (document.getAnimations?document.getAnimations():[]).forEach(function(a){
      try{ a.currentTime = ms; }catch(e){}
    });
    if(typeof window.__render==='function') window.__render(t);
  };
  // helpers for shots
  window.A={
    // integer count-up eased
    count:function(el,from,to,t,t0,dur){
      var p=Math.max(0,Math.min(1,(t-t0)/dur)); p=1-Math.pow(1-p,3);
      el.textContent=Math.round(from+(to-from)*p);
    },
    // character type-on into a target span; keeps a caret
    type:function(el,full,t,t0,dur,caret){
      var p=Math.max(0,Math.min(1,(t-t0)/dur));
      var n=Math.floor(p*full.length);
      el.textContent=full.slice(0,n);
      if(caret!==false){ var c=(t*2%1<0.5)?'':''; }
    },
    ease:function(p){ p=Math.max(0,Math.min(1,p)); return 1-Math.pow(1-p,3); }
  };
})();
