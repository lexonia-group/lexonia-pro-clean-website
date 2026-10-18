"""Static QA of site: links, anchors, images, SEO tags, structured data, claims."""
import os, re, json, sys
from html.parser import HTMLParser
from urllib.parse import urlparse, urldefrag
D='site'
pages=sorted(os.path.relpath(os.path.join(r,f),D).replace('\\','/') for r,_,fs in os.walk(D) for f in fs if f.endswith('.html'))
SITE='https://lexoniaproclean.com/'
# Outside links the owner approved: the profiles in generator/profiles.py (footer icons), Unsplash photo credits on blog articles
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'generator'))
from profiles import LINKED as _PROFILE_URLS
ALLOWED_EXT=tuple(_PROFILE_URLS)+('https://unsplash.com/',)
# Prices the owner made public as text (Oct 17 2026): from $155 per visit; interior windows $40 / $70 / $110. Any other dollar amount is flagged.
ALLOWED_PRICES={'$155','$40','$70','$110'}
UTILITY=('404.html','thanks.html')
def as_file(path):
    return path+'index.html' if path.endswith('/') or path=='' else path
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.links=[];s.ids=set();s.imgs=[];s.title='';s._t=False;s.meta={};s.canon=None;s.h=[];s._h=None;s.ld=[];s._ld=False;s.scripts=[];s.inline_js=0;s.handlers=[];s.lang=None;s.ext=[];s.forms=[];s.styles_inline=0
    def handle_starttag(s,t,a):
        a=dict(a)
        if 'id' in a: s.ids.add(a['id'])
        for k in a:
            if k.startswith('on'): s.handlers.append((t,k))
        if 'style' in a: s.styles_inline+=1
        if t=='html': s.lang=a.get('lang')
        if t=='a' and 'href' in a:
            s.links.append((a['href'],a.get('target'),a.get('rel')))
        if t=='img': s.imgs.append(a)
        if t=='title': s._t=True
        if t=='meta':
            k=a.get('name') or a.get('property')
            if k: s.meta[k]=a.get('content')
        if t=='link':
            if a.get('rel')=='canonical': s.canon=a.get('href')
            if a.get('href','').startswith('http'): s.ext.append(('link',a['href']))
        if t in('h1','h2','h3','h4'): s._h=t; s.h.append([t,''])
        if t=='script':
            if a.get('type')=='application/ld+json': s._ld=True; s.ld.append('')
            elif a.get('src'): s.scripts.append(a['src'])
            else: s.inline_js+=1
        if t=='form': s.forms.append(a)
    def handle_endtag(s,t):
        if t=='title': s._t=False
        if t==s._h: s._h=None
        if t=='script': s._ld=False
    def handle_data(s,d):
        if s._t: s.title+=d
        if s._h: s.h[-1][1]+=d
        if s._ld: s.ld[-1]+=d
R={}; issues=[]
def bad(p,m): issues.append((p,m))
for f in pages:
    s=open(os.path.join(D,f),encoding='utf-8').read(); p=P(); p.feed(s); R[f]=(p,s)
files=set()
for r,_,fs in os.walk(D):
    for x in fs: files.add(os.path.relpath(os.path.join(r,x),D).replace('\\','/'))
for f,(p,s) in R.items():
    # links
    for href,tgt,rel in p.links:
        if href.startswith(('mailto:','tel:')): continue
        if href.startswith('http'):
            if tgt=='_blank' and not (rel and 'noopener' in rel): bad(f,'external _blank without noopener: '+href)
            if 'lexoniaproclean.com' not in href and not href.startswith(ALLOWED_EXT): bad(f,'external link: '+href)
            continue
        path,frag=urldefrag(href); path=path or f
        if path.startswith('/'): path=path[1:]
        path=as_file(path)
        if path not in files: bad(f,'broken link '+href); continue
        if frag and path.endswith('.html') and path in R:
            if frag not in R[path][0].ids: bad(f,'missing anchor %s#%s'%(path,frag))
    # images
    for a in p.imgs:
        src=a.get('src','')
        if src.startswith('http'): bad(f,'external image '+src); continue
        if src.lstrip('/') not in files: bad(f,'missing image '+src)
        if 'alt' not in a: bad(f,'img without alt '+src)
        if not a.get('width') and 'hero' not in src and 'loop' not in src: bad(f,'img without width/height '+src)
    # seo
    t=p.title.strip(); d=p.meta.get('description','')
    if not (20<=len(t)<=62): bad(f,'title length %d: %s'%(len(t),t))
    if f not in UTILITY and not (70<=len(d)<=165): bad(f,'description length %d'%len(d))
    h1=[x for x in p.h if x[0]=='h1']
    if len(h1)!=1 and f not in UTILITY: bad(f,'h1 count %d'%len(h1))
    if not p.lang: bad(f,'no lang')
    if 'viewport' not in p.meta: bad(f,'no viewport')
    if f not in UTILITY:
        if not p.canon: bad(f,'no canonical')
        for k in('og:title','og:description','og:image','og:url','twitter:card'):
            if k not in p.meta: bad(f,'missing '+k)
    else:
        if 'noindex' not in (p.meta.get('robots') or ''): bad(f,'utility page should be noindex')
    for k,v in p.ext:
        if v not in (p.canon,) and not v.startswith(SITE): bad(f,'external resource: '+v)
    for j in p.ld:
        try: json.loads(j)
        except Exception as e: bad(f,'JSON-LD invalid: %s'%e)
    if p.inline_js: bad(f,'inline scripts: %d'%p.inline_js)
    if p.handlers: bad(f,'inline handlers: %s'%p.handlers[:3])
    low=s.lower()
    if s.count('Find us on Thumbtack')!=(0 if f in UTILITY and 'Find us on Thumbtack' not in s else 1): bad(f,'footer Thumbtack link missing or duplicated')
    if low.replace('find us on thumbtack','').replace('thumbtack.com/mn/eden-prairie/commercial-cleaning/lexonia-pro-clean/','').count('thumbtack'): bad(f,'Thumbtack mentioned outside the footer link')
    for term in('service-area','windex','lysol','tt-card','lorem','todo','xxx'):
        if term in low: bad(f,'leftover term: '+term)
    # dollar amounts in text: only the prices the owner made public
    txt=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S); txt=re.sub(r'<[^>]+>',' ',txt)
    m=re.findall(r'\$\s?\d[\d,]*',txt)
    m=[x.replace(' ','') for x in m if x.replace(' ','') not in ALLOWED_PRICES]
    if m: bad(f,'dollar amount not on the approved list: %s'%m[:5])
# titles / descriptions unique
ts={f:R[f][0].title.strip() for f in R}; ds={f:R[f][0].meta.get('description') for f in R}
if len(set(ts.values()))!=len(ts): bad('*','duplicate titles')
if len(set(ds.values()))!=len(ds): bad('*','duplicate descriptions')
# sitemap & robots & llms
sm=open(os.path.join(D,'sitemap.xml'),encoding='utf-8').read()
locs=re.findall(r'<loc>([^<]+)</loc>',sm)
for l in locs:
    path=as_file(l.replace(SITE,''))
    if l.endswith('.jpg') or l.endswith('.png'):
        if path not in files: bad('sitemap','image missing '+l)
    elif path not in files: bad('sitemap','url missing '+l)
for f in pages:
    if f in UTILITY: continue
    u=SITE+('' if f=='index.html' else f[:-len('index.html')] if f.endswith('/index.html') else f)
    if u not in locs: bad('sitemap','page not listed '+f)
rb=open(os.path.join(D,'robots.txt')).read()
if 'Sitemap:' not in rb: bad('robots','no sitemap line')
ll=open(os.path.join(D,'llms.txt'),encoding='utf-8').read()
for l in re.findall(r'\]\((https?://[^)]+)\)',ll):
    path=as_file(l.replace(SITE,''))
    if path not in files: bad('llms.txt','dead link '+l)
print('pages:',pages)
print('ISSUES (%d):'%len(issues))
for i in issues: print(' -',i)
# summary table
for f,(p,s) in R.items():
    print(f, '| title %d | desc %d | h1 %d | h2 %d | imgs %d | forms %d | ld %d'%(len(p.title.strip()),len(p.meta.get('description','')),sum(1 for x in p.h if x[0]=='h1'),sum(1 for x in p.h if x[0]=='h2'),len(p.imgs),len(p.forms),len(p.ld)))
