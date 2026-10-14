import asyncio, numpy as np
from playwright.async_api import async_playwright
base='http://127.0.0.1:8765/'
ON=np.load('onsets.npz')
INIT = """
window.__aud=null; const A=window.Audio; window.Audio=function(...a){const x=new A(...a); window.__aud=x; return x};
window.__cap=[]; window.__op=[];
document.addEventListener('DOMContentLoaded',()=>{
  const cap=document.querySelector('.loop-cap'); if(!cap) return;
  new MutationObserver(()=>{window.__cap.push([performance.now(), cap.textContent, window.__aud&&!window.__aud.paused?window.__aud.currentTime:null])}).observe(cap,{childList:true,characterData:true,subtree:true});
  setInterval(()=>{ const imgs=[...document.querySelectorAll('.loop-frame img')]; window.__op.push([performance.now(), imgs.map(i=>{const cs=getComputedStyle(i); return [+cs.opacity, +cs.zIndex]})]); },40);
});
"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
        for name,music,secs,red in [('timer reduce',False,24,'reduce'),('music',True,24,'no-preference')]:
            ctx=await b.new_context(viewport={'width':1280,'height':800}, reduced_motion=red); await ctx.add_init_script(INIT)
            pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
            await pg.goto(base+'index.html'); await pg.wait_for_timeout(2500)
            if music: await pg.click('.music-btn')
            await pg.wait_for_timeout(secs*1000)
            cap=await pg.evaluate('window.__cap'); op=await pg.evaluate('window.__op')
            # coverage dip: at any sample, the visible stack must cover fully: the lowest-z visible image should be 1 while a higher one ramps
            worst=1.0; ramp=[]; cur=None
            for t,arr in op:
                vis=sorted([a for a in arr if a[0]>0.001], key=lambda a:a[1])
                if len(vis)>=2:
                    bottom=vis[0][0]; worst=min(worst,bottom)
                    ramp.append((t,vis[-1][0]))
            # fade duration: contiguous runs where 2 imgs visible
            runs=[]; start=None; last=None
            for t,arr in op:
                two=sum(1 for a in arr if a[0]>0.001)>=2
                if two and start is None: start=t
                if not two and start is not None: runs.append((t-start)/1000); start=None
            print('==',name,'errors',errs,'| switches',len(cap),'| lowest bottom-layer opacity during overlap %.2f'%worst,'| overlap run lengths',[round(r,2) for r in runs[:6]])
            prev=None; dts=[]
            for t,c,at in cap:
                if prev is not None: dts.append((t-prev)/1000)
                prev=t
            print('   caption dt median %.2f'%np.median(dts) if dts else '')
            if music:
                offs=[]
                for t,c,at in cap:
                    if at is None: continue
                    o=ON['kick']; d=o[np.argmin(abs(o-at))]-at
                    if abs(d)<0.3: offs.append(d*1000)
                print('   caption (fade middle) vs kick onset median %.0f ms n=%d'%(np.median(offs),len(offs)))
            await ctx.close()
        await b.close()
asyncio.run(main())
