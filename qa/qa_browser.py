import sys, json
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
BASE = 'http://127.0.0.1:8765/'
PAGES = ['index', 'services', 'why-us', 'how-it-works', 'contact', 'thanks', '404']
WIDTHS = [360, 390, 414, 768, 900, 1024, 1280, 1440]
bad = []


def note(m):
    bad.append(m)


JS = """()=>{
  const ov=document.documentElement.scrollWidth>document.documentElement.clientWidth+1;
  const imgs=[...document.images].filter(i=>i.complete&&i.naturalWidth===0&&i.src).map(i=>i.src.slice(-50));
  const fonts=[document.fonts.check("700 16px Sora"),document.fonts.check("400 16px Inter")];
  const links=[...document.querySelectorAll('header nav a')];
  const navclip=links.filter(a=>{const r=a.getBoundingClientRect(); return r.width>0&&(r.right>window.innerWidth+1||r.left<-1)}).map(a=>a.textContent.trim());
  const small=[...document.querySelectorAll('a,button,input,select,textarea,summary')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&(r.height<32||r.width<32)&&!e.closest('.hidden')&&e.type!=='hidden'}).map(e=>(e.textContent||e.name||e.tagName).trim().slice(0,20)+':'+Math.round(e.getBoundingClientRect().width)+'x'+Math.round(e.getBoundingClientRect().height));
  return {ov,imgs,fonts,navclip,small:small.slice(0,6)}
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for w in WIDTHS:
        mob = w < 700
        ctx = b.new_context(viewport={'width': w, 'height': 850}, is_mobile=mob, has_touch=mob, device_scale_factor=1)
        for name in PAGES:
            pg = ctx.new_page()
            errs = []; reqs = set(); failed = []
            pg.on('console', lambda m, errs=errs: errs.append((m.type, m.text[:160])) if m.type in ('error', 'warning') else None)
            pg.on('pageerror', lambda e, errs=errs: errs.append(('pageerror', str(e)[:160])))
            pg.on('request', lambda r, reqs=reqs: reqs.add(urlparse(r.url).netloc))
            pg.on('requestfailed', lambda r, failed=failed: failed.append(r.url[-60:]))
            pg.goto(BASE + name + '.html', wait_until='load')
            pg.wait_for_timeout(500)
            H = pg.evaluate('document.documentElement.scrollHeight')
            y = 0
            while y < H:
                pg.evaluate('window.scrollTo(0,%d)' % y)
                pg.wait_for_timeout(60)
                y += 600
            pg.wait_for_timeout(400)
            r = pg.evaluate(JS)
            tag = '%s@%d' % (name, w)
            if r['ov']: note(tag + ' horizontal overflow')
            if r['imgs']: note(tag + ' broken images %s' % r['imgs'])
            if not all(r['fonts']): note(tag + ' fonts not loaded %s' % r['fonts'])
            if r['navclip']: note(tag + ' nav links clipped: %s' % r['navclip'])
            if r['small'] and w in (390, 1280): note(tag + ' small tap targets %s' % r['small'])
            ext = [o for o in reqs if o and o != '127.0.0.1:8765']
            if ext: note(tag + ' external requests: %s' % ext)
            if errs: note(tag + ' console: %s' % errs[:3])
            if failed: note(tag + ' failed requests: %s' % failed[:3])
            pg.close()
        ctx.close()
    b.close()
print('BROWSER QA: %d findings' % len(bad))
for m in bad:
    print(' -', m)
