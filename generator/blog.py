"""Blog for lexoniaproclean.com: content/blog/*.md -> site/blog/.

One article = one Markdown file with a small front-matter block. The same article is the source of that
week's Facebook / Google / Instagram post (owner, Oct 17 2026: written once, reused everywhere).

Publishing is by date: an article goes live on the first build on or after its `date` (US Central).
Netlify builds on every push, and the weekly publisher pushes on the article's day, so a future-dated
article can sit in the repository until its day comes.

Front matter (every key required unless marked optional):
    title, slug, date (YYYY-MM-DD), description (<= 160 chars), category,
    photo (https URL to download, or a site path like img/x.jpg), photo_alt,
    photo_credit (optional), photo_credit_url (optional),
    service (site page the article supports, e.g. services.html), service_label
Body: Markdown subset - paragraphs, ## / ### headings, - bullets, 1. numbered lists, **bold**, [text](url).
The first paragraph is the short, direct answer (shown in a highlighted box: the part AI assistants quote).
Content rule (owner): every business fact traces to what the owner stated; nothing invented.
"""
import os, re, html, json, datetime, urllib.request
try:
    from zoneinfo import ZoneInfo
    _TZ = ZoneInfo('America/Chicago')
except Exception:   # pragma: no cover
    _TZ = None

# Educational only (owner, Oct 18 2026): before-and-after job photos are for social posts, never blog articles
CATEGORIES = ['Cost and contracts', 'Office cleaning know-how', 'Retail and boutique', 'Larger buildings', 'Minnesota seasons']
REQUIRED = ['title', 'slug', 'date', 'description', 'category', 'photo', 'photo_alt', 'service', 'service_label']


def today_central():
    now = datetime.datetime.now(_TZ) if _TZ else datetime.datetime.utcnow() - datetime.timedelta(hours=6)
    return now.date().isoformat()


def parse(path):
    raw = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', raw, re.S)
    assert m, 'front matter missing in ' + path
    meta = {}
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        k, _, v = line.partition(':')
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'':
            v = v[1:-1]
        meta[k.strip()] = v
    for k in REQUIRED:
        assert meta.get(k), '%s: missing %s' % (path, k)
    assert re.match(r'^\d{4}-\d{2}-\d{2}$', meta['date']), path + ': date must be YYYY-MM-DD'
    assert re.match(r'^[a-z0-9-]+$', meta['slug']), path + ': slug must be lowercase words joined by hyphens'
    assert meta['category'] in CATEGORIES, '%s: unknown category %r' % (path, meta['category'])
    assert len(meta['description']) <= 160, path + ': description over 160 characters'
    assert len(meta['title']) <= 70, path + ': title over 70 characters'
    meta['body'] = m.group(2).strip()
    meta['source'] = os.path.basename(path)
    return meta


def load(content_dir, upto):
    posts = []
    if not os.path.isdir(content_dir):
        return posts
    for f in sorted(os.listdir(content_dir)):
        if f.endswith('.md') and not f.startswith('_'):
            p = parse(os.path.join(content_dir, f))
            if p['date'] <= upto:
                posts.append(p)
    slugs = [p['slug'] for p in posts]
    assert len(slugs) == len(set(slugs)), 'duplicate blog slug'
    posts.sort(key=lambda p: (p['date'], p['title']), reverse=True)
    return posts


# ------------------------------------------------------------------ Markdown subset
def _inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    def link(m):
        label, url = m.group(1), m.group(2)
        ext = url.startswith('http') and 'lexoniaproclean.com' not in url
        return '<a href="%s"%s>%s</a>' % (url, ' target="_blank" rel="noopener"' if ext else '', label)
    return re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link, t)


def md_to_html(md):
    out, para, lst, kind = [], [], [], None
    def flush():
        nonlocal para, lst, kind
        if para:
            out.append('<p>%s</p>' % _inline(' '.join(para))); para = []
        if lst:
            out.append('<%s>%s</%s>' % (kind, ''.join('<li>%s</li>' % _inline(i) for i in lst), kind)); lst = []; kind = None
    for line in md.splitlines():
        s = line.strip()
        if not s:
            flush(); continue
        h = re.match(r'^(#{2,3})\s+(.*)$', s)
        b = re.match(r'^[-*]\s+(.*)$', s)
        n = re.match(r'^\d+\.\s+(.*)$', s)
        if h:
            flush(); lvl = len(h.group(1))
            out.append('<h%d>%s</h%d>' % (lvl, _inline(h.group(2)), lvl))
        elif b or n:
            if para:
                out.append('<p>%s</p>' % _inline(' '.join(para))); para = []
            k = 'ul' if b else 'ol'
            if kind and kind != k:
                flush()
            kind = k; lst.append((b or n).group(1))
        else:
            if lst:
                flush()
            para.append(s)
    flush()
    return '\n'.join(out)


def split_answer(md):
    """First paragraph = the short answer; the rest = the article."""
    parts = md.strip().split('\n\n', 1)
    return parts[0].strip(), (parts[1].strip() if len(parts) > 1 else '')


def plain(md):
    t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', md)
    t = re.sub(r'[*#]', '', t)
    return re.sub(r'\s+', ' ', t).strip()


def nice_date(d):
    y, m, dd = map(int, d.split('-'))
    return datetime.date(y, m, dd).strftime('%B %-d, %Y')


# ------------------------------------------------------------------ photos (stored on the site: the CSP allows images from this site only)
def photo(p, out, here):
    """Returns (relative path under site/, width, height). Remote photos are downloaded once and cropped to 16:9, 1200 px."""
    src = p['photo']
    if not src.startswith('http'):
        from PIL import Image
        path = src.lstrip('/')
        w, h = Image.open(os.path.join(out, path)).size
        return path, w, h
    rel = 'img/blog/%s.jpg' % p['slug']
    dst = os.path.join(out, rel)
    cache = os.path.join(here, 'assets_src', rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(cache) and not os.path.exists(dst):
        from PIL import Image
        import io
        try:
            req = urllib.request.Request(src, headers={'User-Agent': 'lexoniaproclean.com site build'})
            data = urllib.request.urlopen(req, timeout=60).read()
        except Exception as e:   # never fail the whole site over one photo: fall back to the site's own link-card image
            print('WARNING: blog photo download failed for %s (%s); using the default image' % (p['slug'], e))
            return 'img/lexonia-pro-clean-commercial-cleaning-og.jpg', 1200, 630
        im = Image.open(io.BytesIO(data)).convert('RGB')
        W, H = im.size
        th = int(W * 9 / 16)
        if th <= H:
            top = (H - th) // 2; im = im.crop((0, top, W, top + th))
        else:
            tw = int(H * 16 / 9); left = (W - tw) // 2; im = im.crop((left, 0, left + tw, H))
        im = im.resize((1200, 675))
        im.save(dst, 'JPEG', quality=82, optimize=True, progressive=True)
    elif os.path.exists(cache) and not os.path.exists(dst):
        import shutil
        shutil.copyfile(cache, dst)
    return rel, 1200, 675


# ------------------------------------------------------------------ pages
BLOG_CSS = '''
/* ---- blog ---- */
.blog-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:8px;text-align:left}
.post-card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow-sm);display:flex;flex-direction:column}
.post-card img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;display:block}
.post-card .pc-body{padding:18px 20px 22px;display:flex;flex-direction:column;gap:8px;flex:1}
.post-card .pc-cat{font-size:.78rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--teal-dark)}
.post-card h2{font-size:1.12rem;line-height:1.3;margin:0}
.post-card h2 a{color:var(--navy);text-decoration:none}
.post-card h2 a:hover{color:var(--teal)}
.post-card p{color:var(--muted);font-size:.92rem;margin:0}
.post-card time{font-size:.82rem;color:var(--muted);margin-top:auto}
@media (max-width:960px){.blog-grid{grid-template-columns:1fr 1fr}}
@media (max-width:640px){.blog-grid{grid-template-columns:1fr}}
.article{max-width:760px;margin:0 auto;text-align:left}
.article .post-meta{color:var(--muted);font-size:.9rem;margin-bottom:18px}
.article figure{margin:0 0 26px}
.article figure img{width:100%;height:auto;border-radius:var(--radius);display:block}
.article figcaption{font-size:.8rem;color:var(--muted);margin-top:6px}
.article figcaption a{color:var(--muted)}
.short-answer{background:var(--sky-2);border:1px solid var(--line);border-left:6px solid var(--teal);border-radius:14px;padding:18px 22px;margin:0 0 28px}
.short-answer strong.sa-label{display:block;font-family:'Sora',sans-serif;color:var(--navy);font-size:.85rem;letter-spacing:.04em;text-transform:uppercase;margin-bottom:6px}
.short-answer p{margin:0;color:var(--ink);font-size:1.05rem}
.article h2{font-size:1.4rem;margin:30px 0 10px;color:var(--navy)}
.article h3{font-size:1.12rem;margin:22px 0 8px;color:var(--navy)}
.article p{margin:0 0 14px;color:var(--ink)}
.article ul,.article ol{margin:0 0 16px 22px;color:var(--ink)}
.article li{margin:4px 0}
.article .related{margin-top:30px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px 22px}
.article .related a{font-weight:700}
.blog-empty{color:var(--muted)}
'''


def card(p, img):
    rel, w, h = img
    return ('<article class="post-card">\n  <a href="blog/%s/" tabindex="-1" aria-hidden="true"><img src="%s" alt="%s" width="%d" height="%d" loading="lazy"></a>\n'
            '  <div class="pc-body"><span class="pc-cat">%s</span><h2><a href="blog/%s/">%s</a></h2><p>%s</p><time datetime="%s">%s</time></div>\n</article>\n'
            % (p['slug'], rel, html.escape(p['photo_alt'], quote=True), w, h, html.escape(p['category']), p['slug'],
               html.escape(p['title']), html.escape(p['description']), p['date'], nice_date(p['date'])))


def build(out, here, ctx):
    """ctx: dict with header, footer, page_hero, cta_band, render_head, SITE, BIZ_ID, business_ld, LOGO, OG_IMG, root_links"""
    SITE = ctx['SITE']
    content_dir = os.path.join(os.path.dirname(here), 'content', 'blog')
    upto = today_central()
    posts = load(content_dir, upto)
    imgs = {p['slug']: photo(p, out, here) for p in posts}
    os.makedirs(os.path.join(out, 'blog'), exist_ok=True)

    # ---- index
    if posts:
        grid = '<div class="blog-grid">\n' + ''.join(card(p, imgs[p['slug']]) for p in posts) + '</div>\n'
    else:
        grid = '<p class="blog-empty">The first articles are on the way.</p>\n'
    body = ('<main id="top">\n' + ctx['page_hero']('Blog', 'Commercial Cleaning Guides',
            'Straight answers for office and store managers across the Twin Cities and suburbs: what cleaning includes, how often, how it is priced, and what to ask before you hire.')
            + '<section>\n  <div class="container">\n' + grid + '  </div>\n</section>\n'
            + ctx['cta_band']() + '</main>\n')
    idx_url = SITE + 'blog/'
    graph = [ctx['business_ld'](False),
             {'@type': 'CollectionPage', '@id': idx_url + '#webpage', 'url': idx_url, 'name': 'Commercial Cleaning Guides | Lexonia Pro Clean',
              'description': 'Guides for office and small retail managers in the Twin Cities: cleaning scope, frequency, pricing and how recurring cleaning works.',
              'isPartOf': {'@id': SITE + '#website'}, 'about': {'@id': ctx['BIZ_ID']}, 'inLanguage': 'en-US',
              'mainEntity': {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': SITE + 'blog/%s/' % p['slug'], 'name': p['title']} for i, p in enumerate(posts)]}},
             {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE},
                                                              {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': idx_url}]}]
    page = dict(title='Commercial Cleaning Guides | Lexonia Pro Clean', path='blog/', active='blog/',
                desc='Guides for office and small retail managers in the Twin Cities: what cleaning includes, how often it is needed, how it is priced, and how it works.',
                body=body, ld=graph, og_img=None, og_type='website')
    write(out, 'blog/index.html', ctx, page)

    # ---- articles
    for i, p in enumerate(posts):
        rel, w, h = imgs[p['slug']]
        answer, rest = split_answer(p['body'])
        credit = ''
        if p.get('photo_credit'):
            who = html.escape(p['photo_credit'])
            if p.get('photo_credit_url'):
                who = '<a href="%s" target="_blank" rel="noopener">%s</a>' % (p['photo_credit_url'], who)
            credit = '<figcaption>Photo: %s on <a href="https://unsplash.com/" target="_blank" rel="noopener">Unsplash</a></figcaption>' % who
        others = [q for q in posts if q['slug'] != p['slug']][:3]
        more = ''
        if others:
            more = ('<section class="reviews">\n  <div class="container">\n    <h2 class="section-title center">More guides</h2>\n'
                    '    <div class="blog-grid">\n' + ''.join(card(q, imgs[q['slug']]) for q in others) + '    </div>\n  </div>\n</section>\n')
        art = ('<main id="top">\n' + ctx['page_hero'](html.escape(p['category']), html.escape(p['title']), html.escape(p['description']))
               + '<section>\n  <div class="container">\n    <article class="article">\n'
               + '      <p class="post-meta">Published <time datetime="%s">%s</time> by Lexonia Pro Clean, Eden Prairie, MN</p>\n' % (p['date'], nice_date(p['date']))
               + '      <figure><img src="%s" alt="%s" width="%d" height="%d" fetchpriority="high">%s</figure>\n' % (rel, html.escape(p['photo_alt'], quote=True), w, h, credit)
               + '      <div class="short-answer"><strong class="sa-label">Short answer</strong><p>%s</p></div>\n' % _inline(answer)
               + md_to_html(rest) + '\n'
               + '      <p class="related">Related: <a href="%s">%s</a> · <a href="contact.html">Book a free walkthrough</a></p>\n' % (p['service'], html.escape(p['service_label']))
               + '    </article>\n  </div>\n</section>\n' + more + ctx['cta_band']() + '</main>\n')
        url = SITE + 'blog/%s/' % p['slug']
        posting = {'@type': 'BlogPosting', '@id': url + '#article', 'headline': p['title'], 'description': p['description'],
                   'image': {'@type': 'ImageObject', 'url': SITE + rel, 'width': w, 'height': h},
                   'datePublished': p['date'], 'dateModified': p.get('updated', p['date']), 'inLanguage': 'en-US',
                   'author': {'@id': ctx['BIZ_ID']}, 'publisher': {'@id': ctx['BIZ_ID']}, 'mainEntityOfPage': {'@id': url + '#webpage'},
                   'articleSection': p['category'], 'about': {'@id': ctx['BIZ_ID']},
                   'wordCount': len(plain(p['body']).split())}
        graph = [ctx['business_ld'](False),
                 {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': p['title'], 'description': p['description'],
                  'isPartOf': {'@id': SITE + '#website'}, 'inLanguage': 'en-US', 'primaryImageOfPage': {'@type': 'ImageObject', 'url': SITE + rel}},
                 posting,
                 {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE},
                                                                  {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': idx_url},
                                                                  {'@type': 'ListItem', 'position': 3, 'name': p['title'], 'item': url}]}]
        full = '%s | Lexonia Pro Clean' % p['title']
        page = dict(title=full if len(full) <= 62 else p['title'], path='blog/%s/' % p['slug'], active='blog/', desc=p['description'],
                    body=art, ld=graph, og_img=(SITE + rel, w, h, p['photo_alt']), og_type='article', published=p['date'])
        write(out, 'blog/%s/index.html' % p['slug'], ctx, page)

    # ---- RSS feed
    items = ''.join('  <item>\n    <title>%s</title>\n    <link>%sblog/%s/</link>\n    <guid>%sblog/%s/</guid>\n    <pubDate>%s</pubDate>\n    <description>%s</description>\n  </item>\n'
                    % (html.escape(p['title']), SITE, p['slug'], SITE, p['slug'],
                       datetime.datetime.strptime(p['date'], '%Y-%m-%d').strftime('%a, %d %b %Y 09:00:00 -0500'), html.escape(p['description']))
                    for p in posts)
    open(os.path.join(out, 'blog', 'feed.xml'), 'w', encoding='utf-8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n<channel>\n  <title>Lexonia Pro Clean — Commercial Cleaning Guides</title>\n'
        '  <link>%sblog/</link>\n  <description>Guides for office and small retail managers in the Twin Cities.</description>\n  <language>en-us</language>\n%s</channel>\n</rss>\n' % (SITE, items))
    return posts


def write(out, relpath, ctx, page):
    doc = ctx['render_page'](page)
    doc = ctx['root_links'](doc)
    dst = os.path.join(out, relpath)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'w', encoding='utf-8').write(doc)
