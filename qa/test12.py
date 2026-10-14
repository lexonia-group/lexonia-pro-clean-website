import asyncio
from playwright.async_api import async_playwright
base='http://127.0.0.1:8765/'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w,h in [(360,740),(390,844),(414,896),(768,1024),(900,800),(1024,768),(1280,800)]:
            ctx=await b.new_context(viewport={'width':w,'height':h}, has_touch=(w<800), is_mobile=(w<800)); pg=await ctx.new_page(); errs=[]
            pg.on('pageerror',lambda e: errs.append(str(e)))
            pg.on('console',lambda m: errs.append('console:'+m.text) if m.type=='error' else None)
            res={}
            for name in ['index','services','why-us','how-it-works','contact']:
                await pg.goto(base+name+'.html'); await pg.wait_for_timeout(500)
                r=await pg.evaluate("""()=>{const tabs=[...document.querySelectorAll('.nav-links a')].map(a=>{const r=a.getBoundingClientRect();return [Math.round(r.width),Math.round(r.height),getComputedStyle(a).display!=='none'&&r.width>0]});
                  const mbar=document.querySelector('.mbar'); const mb=mbar&&getComputedStyle(mbar).display!=='none';
                  const small=[...document.querySelectorAll('a.btn,button,.nav-links a,.mbar a,summary')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.height<40)}).map(e=>e.textContent.trim().slice(0,20)+':'+Math.round(e.getBoundingClientRect().height));
                  return {overflow:document.documentElement.scrollWidth>document.documentElement.clientWidth, tabsVisible:tabs.every(t=>t[2]), mbar:mb, small:small.slice(0,5), h:document.documentElement.scrollHeight}}""")
                res[name]=r
            # home loop position
            await pg.goto(base+'index.html'); await pg.wait_for_timeout(1200)
            lp=await pg.evaluate("(()=>{const r=document.querySelector('.loop').getBoundingClientRect();return [Math.round(r.top),Math.round(r.bottom),Math.round(r.width)]})()")
            bad={k:v for k,v in res.items() if v['overflow'] or not v['tabsVisible']}
            print(w,'x',h,'loop top/bottom/width',lp,'| mbar',res['index']['mbar'],'| problems',bad,'| small targets',{k:v['small'] for k,v in res.items() if v['small']},'| errs',errs)
            if w in (390,900,1280): await pg.screenshot(path='shots/b12-%d.png'%w)
            await ctx.close()
        await b.close()
asyncio.run(main())
