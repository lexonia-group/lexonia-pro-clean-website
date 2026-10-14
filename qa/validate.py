import json,re,os,sys,glob
from html.parser import HTMLParser
import xml.dom.minidom as md
D='site/'
pages=['index','services','why-us','how-it-works','contact','thanks','404']
problems=[]
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.imgs=[]; s.links=[]; s.ld=[]; s._ld=False; s.ids=set(); s.h1=0; s.meta={}
    def handle_starttag(s,t,a):
        a=dict(a)
        if 'id' in a: s.ids.add(a['id'])
        if t=='img': s.imgs.append(a)
        if t=='a' and a.get('href'): s.links.append(a['href'])
        if t=='script' and a.get('type')=='application/ld+json': s._ld=True; s.ld.append('')
        if t=='h1': s.h1+=1
        if t=='meta' and a.get('name'): s.meta[a['name']]=a.get('content','')
        if t=='meta' and a.get('property'): s.meta[a['property']]=a.get('content','')
        if t=='link' and a.get('rel')=='canonical': s.meta['canonical']=a['href']
    def handle_endtag(s,t):
        if t=='script': s._ld=False
    def handle_data(s,d):
        if s._ld: s.ld[-1]+=d
allids={}
parsed={}
for n in pages:
    f=D+n+'.html'
    p=P(); p.feed(open(f,encoding='utf-8').read()); parsed[n]=p; allids[n]=p.ids
for n,p in parsed.items():
    for i in p.imgs:
        if 'alt' not in i: problems.append((n,'img no alt',i.get('src')))
        if not i.get('width') and 'img/' in i.get('src',''): problems.append((n,'img no width/height',i.get('src')))
        src=i.get('src','')
        if src and not src.startswith('http') and not os.path.exists(D+src.lstrip('/')): problems.append((n,'img missing',src))
    for l in p.links:
        if l.startswith(('http','mailto:','tel:','#')): continue
        path=l.split('#')[0]
        if path in ('',): continue
        path=path.lstrip('/')
        if not os.path.exists(D+path): problems.append((n,'broken link',l))
        elif '#' in l and path.endswith('.html'):
            h=l.split('#')[1]
            if h not in allids.get(path[:-5],set()): problems.append((n,'missing anchor',l))
    for j in p.ld:
        try:
            d=json.loads(j)
        except Exception as e: problems.append((n,'bad JSON-LD',str(e))); continue
    if n!='404' and p.h1!=1: problems.append((n,'h1 count',p.h1))
    m=p.meta
    print(n,'title/desc/canon:',bool(m.get('og:title')),len(m.get('description','')),m.get('canonical'),'| ld blocks',len(p.ld),'| imgs',len(p.imgs))
# sitemap / robots / llms
md.parse(D+'sitemap.xml'); print('sitemap ok'); print(open(D+'robots.txt').read())
sm=open(D+'sitemap.xml').read()
for u in re.findall(r'<loc>([^<]+)</loc>',sm):
    path=u.replace('https://lexoniaproclean.com/','')
    if path and not os.path.exists(D+path): problems.append(('sitemap','missing',u))
# FAQ JSON-LD matches visible
ld=json.loads(parsed['how-it-works'].ld[0]) if parsed['how-it-works'].ld else None
print('PROBLEMS',problems)
