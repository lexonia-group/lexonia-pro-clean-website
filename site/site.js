// Microsoft Clarity (visitor analytics): official snippet, served from this file so the page needs no inline script
(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window, document, "clarity", "script", "yybv330g41");
// Mobile menu
(function(){
  var b=document.getElementById('menuBtn'), n=document.getElementById('navLinks');
  if(b&&n){ b.addEventListener('click',function(){n.classList.toggle('open')});
    n.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){n.classList.remove('open')})}); }
  // Scroll reveal
  var els=document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target)}})},{threshold:.12});
    els.forEach(function(el){io.observe(el)});
  } else { els.forEach(function(el){el.classList.add('visible')}); }
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Music: off until the visitor taps the button; remembered while they browse the site
  var KEY='lpcMusic', KT='lpcMusicT';
  function st(k,v){try{sessionStorage.setItem(k,v)}catch(e){}}
  function rd(k){try{return sessionStorage.getItem(k)}catch(e){return null}}
  var audio=new Audio('audio/summerhill.mp3'); audio.loop=true; audio.preload='none'; audio.volume=0.35;
  // Beat clock. The track runs at a steady 113 beats a minute: one beat every 0.531 s, first beat at 0.805 s (measured on the drum hits).
  // With music on, pictures follow the music's own clock. With music off, the same pace runs on a timer.
  var BEAT=0.53098, BEAT0=0.805, LAT=0.03, FADE=1.0, subs=[], onAudio=false, lastN=null, vT0=performance.now();
  function nowBeat(){
    if(!audio.paused) return Math.floor((audio.currentTime-LAT+FADE/2-BEAT0)/BEAT);   // fade starts half a fade early, so the middle of the fade lands on the beat
    return Math.floor((performance.now()-vT0)/1000/BEAT);
  }
  function frame(){
    var a=!audio.paused, n=nowBeat();
    if(a!==onAudio){ onAudio=a; lastN=n; if(a) subs.forEach(function(s){if(s.reset) s.reset();}); }
    else if(n!==lastN){ lastN=n; subs.forEach(function(s){ if((((n%s.every)+s.every)%s.every)===s.phase) s.tick(); }); }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
  function onceLoaded(imgs,cb){
    var left=imgs.length, fired=false;
    function fin(){ if(!fired){fired=true;cb();} }
    function one(){ left--; if(left<=0) fin(); }
    imgs.forEach(function(im){ if(im.complete) one(); else {im.addEventListener('load',one,{once:true}); im.addEventListener('error',one,{once:true});} });
    if(left<=0) fin(); else setTimeout(fin,4000);
  }
  // Rotating hero photos on the inner pages (first photo is in the page; the rest load after the page is ready)
  document.querySelectorAll('.hero-slides').forEach(function(box){
    var list=(box.getAttribute('data-slides')||'').split(','), idx=parseInt(box.getAttribute('data-start')||'0',10)||0;
    if(list.length<2) return;
    var need=Math.min(window.innerWidth||1280,screen.width||1280)*(window.devicePixelRatio||1), sfx=need<=900?'-900':(need<=1400?'-1400':'');
    if(sfx) list=list.map(function(u){return u.replace('.jpg',sfx+'.jpg');});
    var imgs=[box.querySelector('img')], cur=0, ready=false;
    function build(){
      for(var k=1;k<list.length;k++){var im=new Image();im.alt='';im.decoding='async';im.src=list[(idx+k)%list.length];box.appendChild(im);imgs.push(im);}
      onceLoaded(imgs,function(){ready=true;});
    }
    subs.push({every:reduce?16:8, phase:1, tick:function(){
      if(!ready) return; var n=(cur+1)%imgs.length; imgs[n].classList.add('on'); imgs[cur].classList.remove('on'); cur=n;
    }});
    if(document.readyState==='complete') setTimeout(build,800); else window.addEventListener('load',function(){setTimeout(build,800)});
  });
  // The loop on the home page: BEFORE, then its AFTER, for each job; then supplies and bin photos. Changes on the beat.
  document.querySelectorAll('[data-loop]').forEach(function(box){
    var data; try{data=JSON.parse(box.getAttribute('data-loop'));}catch(e){return;}
    var frameEl=box.querySelector('.loop-frame'), cap=box.querySelector('.loop-cap');
    frameEl.style.setProperty('--fade',FADE+'s');   // picture fades out as the next fades in (also with reduce-animations: a fade is not movement)
    var imgs=[frameEl.querySelector('img')], cur=0, target=0, ready=false;
    function ensure(i){ i=i%data.length; if(!imgs[i]){ var im=new Image(); im.alt=data[i][1]; im.width=800; im.height=1000; im.decoding='async'; im.src=data[i][0]; frameEl.appendChild(im); imgs[i]=im; } return imgs[i]; }
    var lastSwitch=-9999;
    function show(i){ if(i===cur) return; lastSwitch=performance.now(); imgs[cur].classList.remove('on'); imgs[i].classList.add('on'); cur=i; setTimeout(function(){ if(cur===i) cap.textContent=data[i][2]; },FADE*500); }   // caption changes in the middle of the overlap
    function go(i){
      target=i; var im=ensure(i); ensure(i+1); ensure(i+2);   // load just the next two pictures ahead, not all of them
      if(im.complete&&im.naturalWidth) show(i); else im.addEventListener('load',function(){ if(target===i) show(i); },{once:true});
    }
    var heldAt=performance.now(), userPaused=false;   // each picture stays up at least 1.5 s, even right after the music starts
    var pbtn=box.querySelector('.loop-pause');
    if(pbtn) pbtn.addEventListener('click',function(){
      userPaused=!userPaused; pbtn.setAttribute('aria-pressed',userPaused?'true':'false');
      pbtn.setAttribute('aria-label',userPaused?'Play the pictures':'Pause the pictures');
    });
    // Same pace for everyone: one picture every fourth beat (about 2.1 s), fading out/in on the beat.
    subs.push({every:4, phase:1,
      tick:function(){ if(ready&&!userPaused&&performance.now()-heldAt>1500){ heldAt=performance.now(); go((target+1)%data.length); } },
      reset:function(){ if(ready){ heldAt=performance.now(); var wait=Math.max(0,FADE*1000+40-(performance.now()-lastSwitch)); if(wait>0) setTimeout(function(){ go(0); },wait); else go(0); } }});   // never restart in the middle of a fade
    function start(){
      ensure(1); ensure(2);
      onceLoaded([imgs[1],imgs[2]],function(){ready=true;heldAt=performance.now();});
    }
    if(document.readyState==='complete') setTimeout(start,300); else window.addEventListener('load',function(){setTimeout(start,300)});
  });
  // Music button
  var btn=document.createElement('button'); btn.type='button'; btn.className='music-btn'; btn.setAttribute('aria-pressed','false'); btn.setAttribute('aria-label','Play background music');
  btn.innerHTML='<svg class="note" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg><span class="eq" aria-hidden="true"><i></i><i></i><i></i></span><span class="lbl">Music</span>';
  document.body.appendChild(btn);
  function setUI(on){btn.setAttribute('aria-pressed',on?'true':'false');btn.setAttribute('aria-label',on?'Pause background music':'Play background music');btn.querySelector('.lbl').textContent=on?'Music on':'Music';}
  var calibrated=false;
  function calibrate(){   // headphones and Bluetooth speakers delay the sound; shift the pictures to match when the browser reports it
    if(calibrated) return; calibrated=true;
    try{ var AC=window.AudioContext||window.webkitAudioContext; if(!AC) return; var c=new AC(); var l=(c.baseLatency||0)+(c.outputLatency||0);
      if(l>0) LAT=Math.min(0.3,Math.max(0.03,l)); if(c.close) c.close(); }catch(e){}
  }
  function play(){calibrate(); var p=audio.play(); if(p&&p.then){p.then(function(){setUI(true);st(KEY,'1')}).catch(function(){setUI(false)});} else {setUI(true);st(KEY,'1');}}
  function pause(){audio.pause();setUI(false);st(KEY,'0');}
  btn.addEventListener('click',function(){audio.paused?play():pause();});
  window.addEventListener('pagehide',function(){if(!audio.paused) st(KT,String(audio.currentTime));});
  if(rd(KEY)==='1'){
    var t=parseFloat(rd(KT)||'0');
    audio.addEventListener('loadedmetadata',function(){if(t>0&&t<audio.duration) audio.currentTime=t;},{once:true});
    audio.preload='auto';
    var rp=audio.play();
    if(rp&&rp.then){rp.then(function(){setUI(true)}).catch(function(){
      var once=function(e){document.removeEventListener('pointerdown',once,true); if(btn.contains(e.target)) return; play();};
      document.addEventListener('pointerdown',once,true);
    });}
  }
  // Preview only: the real form is handled by Netlify once the site is live.
  if(window.LPC_PREVIEW){
    var f=document.querySelector('.quote-form');
    if(f) f.addEventListener('submit',function(e){
      e.preventDefault();
      var n2=document.getElementById('previewNote');
      if(!n2){n2=document.createElement('p');n2.id='previewNote';n2.style.cssText='margin-top:14px;font-weight:600;color:#0b2545';f.appendChild(n2);}
      n2.textContent='Preview only. The form starts sending quote requests to info@lexoniaproclean.com once the site is live.';
    });
  }
})();
