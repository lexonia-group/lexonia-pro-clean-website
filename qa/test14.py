import asyncio, numpy as np
from playwright.async_api import async_playwright
base='http://127.0.0.1:8765/'
INIT = """
window.__cap=[]; window.__op=[];
document.addEventListener('DOMContentLoaded',()=>{
  const cap=document.querySelector('.loop-cap'); if(!cap) return;
  new MutationObserver(()=>{window.__cap.push(performance.now())}).observe(cap,{childList:true,characterData:true,subtree:true});
  setInterval(()=>{ const imgs=[...document.querySelectorAll('.loop-frame img')]; window.__op.push([performance.now(), imgs.map(i=>{const cs=getComputedStyle(i); return [+cs.opacity, +cs.zIndex]})]); },40);
});
"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
        for delay in [100,400,800,1200]:
            ctx=await b.new_context(viewport={'width':1280,'height':800}); await ctx.add_init_script(INIT)
            pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
            await pg.goto(base+'index.html'); await pg.wait_for_timeout(2500)
            n0=await pg.evaluate('window.__cap.length')
            while await pg.evaluate('window.__cap.length')==n0: await pg.wait_for_timeout(15)
            await pg.wait_for_timeout(delay)
            await pg.click('.music-btn'); await pg.wait_for_timeout(9000)
            op=await pg.evaluate('window.__op'); worst=1.0
            for t,arr in op:
                vis=sorted([a for a in arr if a[0]>0.001], key=lambda a:a[1])
                if len(vis)>=2: worst=min(worst,vis[0][0])
            print('music started %d ms after a switch: errors %s, lowest bottom-layer opacity %.2f'%(delay,errs,worst))
            await ctx.close()
        await b.close()
asyncio.run(main())
