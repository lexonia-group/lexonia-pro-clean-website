"""One page per service sold (owner, Oct 20 2026: "use inputs from their sites to build a better SEO/GEO").

Why: the local firms that show up for "office cleaning Eden Prairie" each have a page whose title matches that search, and none
of them publishes prices. Every sentence here traces to the owner's stated facts (README content rules); checklists, prices,
cities and shared answers come from build_site.py (one source), never retyped here.
No city pages: a city gets its own page only when Search Console shows impressions for that city and no page of ours ranks.
"""
import html as _h

NAMES = ['office-cleaning.html', 'retail-cleaning.html', 'multi-story-building-cleaning.html', 'interior-window-cleaning.html']
TABS = [('services.html', 'All services'), ('office-cleaning.html', 'Office'), ('retail-cleaning.html', 'Retail & boutique'),
        ('multi-story-building-cleaning.html', 'Multi-story buildings'), ('interior-window-cleaning.html', 'Interior windows')]


def subtabs(active):
    """Tabs inside the Services tab: shown under the heading on the Services page and on each service page."""
    items = ''.join('<li><a href="%s"%s>%s</a></li>' % (h, ' class="on" aria-current="page"' if h == active else '', _h.escape(t)) for h, t in TABS)
    return '<nav class="subtabs" aria-label="Services">\n  <div class="container"><ul>' + items + '</ul></div>\n</nav>\n'


LINKS = [('office-cleaning.html', 'Office cleaning'), ('retail-cleaning.html', 'Retail store and boutique cleaning'),
         ('multi-story-building-cleaning.html', 'Multi-story buildings, floor by floor'), ('interior-window-cleaning.html', 'Interior windows add-on')]


def _faq(items):
    rows = ''.join('      <details class="faq-item"><summary>%s</summary><p>%s</p></details>\n' % (_h.escape(q), _h.escape(a)) for q, a in items)
    return ('<section class="faq" id="faq">\n  <div class="container">\n    <div class="center"><span class="kicker">Questions</span>\n'
            '    <h2 class="section-title">What Buyers Ask Us</h2></div>\n    <div class="faq-list">\n' + rows + '    </div>\n  </div>\n</section>\n\n')


def _related(here):
    links = ''.join('<a class="sp-rel" href="%s">%s</a>' % (h, t) for h, t in LINKS if h != here)
    return ('<section class="sp-related">\n  <div class="container center">\n    <span class="kicker">Other Services</span>\n'
            '    <div class="sp-rel-row">' + links + '<a class="sp-rel" href="blog/">Guides for office and store managers</a></div>\n  </div>\n</section>\n\n')


def build(c):
    """c: dict of builder pieces (page_hero, cta_band, box, flow, glance, floors, price_img, CHECKLIST, NOT_INCL, FAQ, HOME_FLOW,
    PRICE_FROM, WIN_ROWS, CITIES, HOURS_TEXT, SITE, BIZ_ID, AREA_LD). Returns {file name: page dict}."""
    P, W = c['PRICE_FROM'], c['WIN_ROWS']
    ask = dict(c['FAQ'])
    box, CK = c['box'], dict(c['CHECKLIST'])
    win_text = ', '.join('$%d for %s' % (p, n.replace('–', ' to ')) for n, p in W)
    cities = ', '.join(c['CITIES'][2:-1]) + ' and ' + c['CITIES'][-1]
    where = ('<section class="sp-where">\n  <div class="container center">\n    <span class="kicker">Where We Work</span>\n'
             '    <h2 class="section-title">Based in Eden Prairie, Across the Twin Cities</h2>\n'
             '    <p class="section-lead" style="margin:0 auto">We serve Minneapolis, St. Paul and the suburbs: %s. A business just outside the metro can still ask.</p>\n'
             '  </div>\n</section>\n\n' % cities)
    per_visit = ('Recurring cleaning up to 10,000 sq ft is priced per visit by the size of the space, weekly or every other week, before sales tax. '
                 'It starts from $%d per visit for 1,000 to 2,000 sq ft, weekly. Daily cleaning, or a space over 10,000 sq ft, is a flat monthly contract '
                 'quoted after a free walkthrough. Within 24 hours of the walkthrough you get a written scope and an exact price.' % P)
    q_cost = lambda what: ('How much does %s cost?' % what, per_visit)
    q_when = ('When do you clean?', 'Evenings and nights, between %s, when your business is closed, so we are never in your way.' % c['HOURS_TEXT'].replace(' to ', ' and ').replace(', seven days a week', ', seven days a week'))
    q_local = ('Are you a franchise?', 'No. Lexonia Pro Clean LLC is a locally owned company based in Eden Prairie, Minnesota.')
    q_prep = ('What should we do before the first visit?', 'Put confidential documents away, clear loose paper from desks where possible, make sure access codes, keys or badges are current, and tell us about anything we should not touch.')
    q_windows = ('Can you clean windows too?', ask['Do you clean windows?'].replace('(1-5, 6-10 or 11-15), before sales tax', '(%s), before sales tax' % win_text))

    def pricing(note):
        return ('<section id="price">\n  <div class="container center">\n    <span class="kicker">Pricing</span>\n    <h2 class="section-title">What It Costs</h2>\n'
                '    <div class="sp-price reveal"><p class="sp-from"><strong>From $%d</strong> per visit for 1,000 to 2,000 sq ft, weekly, plus tax</p>\n'
                '      <p>%s</p>\n      <p><a href="services.html#pricing">See the full price card by size of space</a></p></div>\n  </div>\n</section>\n\n' % (P, note))

    def how():
        return ('<section class="industries" id="how">\n  <div class="container center">\n    <span class="kicker">How It Starts</span>\n'
                '    <h2 class="section-title">From First Message to First Clean</h2>\n    ' + c['flow'](c['HOME_FLOW'], 'from first message to first clean') + '\n  </div>\n</section>\n\n')

    def included(title, lead, keys, note=''):
        return ('<section id="included">\n  <div class="container center">\n    <span class="kicker">The Checklist</span>\n    <h2 class="section-title">%s</h2>\n'
                '    <p class="section-lead">%s</p>\n    <div class="incl">\n' % (title, lead) + ''.join(box(k, CK[k]) for k in keys) + '    </div>\n'
                '    <div class="notbox reveal">\n      <h3>Not included</h3>\n      <ul>\n' + ''.join('        <li>%s</li>\n' % i for i in c['NOT_INCL']) + '      </ul>\n' + note +
                '    </div>\n  </div>\n</section>\n\n')

    def glance(tiles):
        return '<section class="glance-sec">\n  <div class="container">\n    ' + c['glance'](tiles) + '\n  </div>\n</section>\n\n'

    def service_ld(name, desc, faq, path, offer=True):
        s = {'@type': 'Service', '@id': c['SITE'] + path + '#service', 'name': name, 'serviceType': name, 'description': desc,
             'provider': {'@id': c['BIZ_ID']}, 'areaServed': c['AREA_LD']}
        if offer:
            s['offers'] = {'@type': 'Offer', 'priceCurrency': 'USD', 'priceSpecification': {'@type': 'UnitPriceSpecification', 'minPrice': P, 'priceCurrency': 'USD',
                           'unitText': 'per visit, 1,000 to 2,000 sq ft, weekly, before sales tax'}}
        return [s, {'@type': 'FAQPage', '@id': c['SITE'] + path + '#faq', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}]

    supply_note = '      <p>%s</p>\n' % ask['Who supplies trash bags, soap and paper towels?']
    pages = {}

    # ---- office cleaning
    f = [q_cost('office cleaning'), q_when, ('Who supplies trash bags, soap and paper towels?', ask['Who supplies trash bags, soap and paper towels?']),
         ('How will I know what was cleaned?', ask['How will I know what was cleaned?']), ('Will you move or read the papers on my desk?', ask['Will you move or read the papers on my desk?']),
         ('Are you insured, and are your crews background-checked?', ask['Are you insured, and are your crews background-checked?']),
         ('What happens after the first visit?', ask['What happens after the first visit?']), q_prep, q_windows, q_local]
    body = ('<main id="top">\n' + c['page_hero']('Office Cleaning', 'Office Cleaning in Eden Prairie and the Twin Cities',
            'Recurring office cleaning on a written checklist, evenings and nights while you are closed. From $%d per visit for 1,000 to 2,000 sq ft, weekly, plus tax.' % P)
            + subtabs('office-cleaning.html')
            + glance([('From $%d' % P, 'per visit, 1,000 to 2,000 sq ft, weekly, plus tax', '#price', 'What it costs'),
                      ('4 PM to 3 AM', 'evenings and nights, seven days a week', '#how', 'How it starts'),
                      ('24 hours', 'written scope and exact price after the free walkthrough', '#how', 'The steps'),
                      ('Every visit', 'a completed checklist left on site', '#included', 'What we clean')])
            + included('What We Clean in Your Office, Every Visit', 'A completed copy of the checklist is left on site, so you can see exactly what was done.',
                       ['Restrooms', 'Break room / kitchenette', 'Offices and workspaces', 'Common areas', 'High-touch points, disinfected'], supply_note)
            + pricing('Interior windows can be added to a visit: %s, before sales tax.' % win_text)
            + how() + where + _faq(f) + _related('office-cleaning.html') + c['cta_band']() + '</main>\n')
    pages['office-cleaning.html'] = dict(title='Office Cleaning in Eden Prairie & Twin Cities | Lexonia', path='office-cleaning.html', active='services.html',
        desc='Office cleaning in Eden Prairie and the Twin Cities, evenings and nights on a written checklist. From $%d per visit. Free walkthrough, exact price in 24 hours.' % P,
        body=body, ld_extra=service_ld('Office cleaning', 'Recurring office cleaning on a written checklist, evenings and nights: restrooms, break rooms, workspaces, common areas and high-touch points.', f, 'office-cleaning.html'))

    # ---- retail stores and boutiques
    f = [q_cost('retail store cleaning'), ('When do you clean a store?', 'After you close, evenings and nights between 4 PM and 3 AM, so we are never in the way of your customers.'),
         ('Who supplies trash bags, soap and paper towels?', ask['Who supplies trash bags, soap and paper towels?']),
         ('How will I know what was cleaned?', 'Every visit follows a written checklist built around your store, and a completed copy is left on site so you can see exactly what was done.'),
         ('Are you insured, and are your crews background-checked?', ask['Are you insured, and are your crews background-checked?']),
         ('What happens after the first visit?', ask['What happens after the first visit?']), q_local]
    body = ('<main id="top">\n' + c['page_hero']('Retail Cleaning', 'Retail Store and Boutique Cleaning in Eden Prairie and the Twin Cities',
            'Recurring cleaning for small retail stores and boutiques, after you close: sales floor, fitting rooms, mirrors, counters and back rooms. From $%d per visit for 1,000 to 2,000 sq ft, weekly, plus tax.' % P)
            + subtabs('retail-cleaning.html')
            + glance([('From $%d' % P, 'per visit, 1,000 to 2,000 sq ft, weekly, plus tax', '#price', 'What it costs'),
                      ('After close', 'evenings and nights, seven days a week', '#how', 'How it starts'),
                      ('24 hours', 'written scope and exact price after the free walkthrough', '#how', 'The steps'),
                      ('Your store', 'a checklist built around your store', '#included', 'What we clean')])
            + included('What We Clean in Your Store', 'Retail checklists are built around your store. A completed copy is left on site after every visit.',
                       ['Small retail stores', 'Restrooms'], supply_note)
            + pricing('Daily cleaning, or a store over 10,000 sq ft, is a flat monthly contract quoted after the free walkthrough.')
            + how() + where + _faq(f) + _related('retail-cleaning.html') + c['cta_band']() + '</main>\n')
    pages['retail-cleaning.html'] = dict(title='Retail Store & Boutique Cleaning | Eden Prairie & Twin Cities', path='retail-cleaning.html', active='services.html',
        desc='Cleaning for small retail stores and boutiques in Eden Prairie and the Twin Cities, after you close. From $%d per visit. Free walkthrough first.' % P,
        body=body, ld_extra=service_ld('Retail store and boutique cleaning', 'Recurring cleaning for small retail stores and boutiques after closing: sales floor, front counter, fitting rooms, mirrors, restrooms and back rooms.', f, 'retail-cleaning.html'))

    # ---- multi-story buildings
    f = [('How does floor-by-floor cleaning work?', ask['Can you clean a multi-story building?'].split(' Multi-story buildings get')[0]),
         ('How is a multi-story building priced?', 'Multi-story buildings get custom pricing, at greater discounts, quoted after a free walkthrough. Within 24 hours of the walkthrough you get a written scope and an exact price.'),
         q_when, ('Who supplies trash bags, soap and paper towels?', ask['Who supplies trash bags, soap and paper towels?']),
         ('Are you insured, and are your crews background-checked?', ask['Are you insured, and are your crews background-checked?']), q_local]
    body = ('<main id="top">\n' + c['page_hero']('Larger Buildings', 'Multi-Story Building Cleaning, Floor by Floor',
            'For a building with more than one floor, we clean a different floor, or two floors, each night. The whole building is cleaned once every 1 to 2 weeks, depending on what it needs.')
            + subtabs('multi-story-building-cleaning.html')
            + '<section id="floors">\n  <div class="container">\n    <div class="center"><span class="kicker">How It Works</span>\n    <h2 class="section-title">A Different Floor, or Two, Each Night</h2></div>\n'
              '    <div class="multi-how reveal">\n      <div><h3>The whole building, every 1 to 2 weeks</h3>\n      <p>Each night covers one floor, or two. How often each floor comes around depends on what your building needs. Every visit follows a written checklist.</p></div>\n      '
            + c['floors']() + '\n    </div>\n  </div>\n</section>\n\n'
            + '<section id="price">\n  <div class="container center">\n    <span class="kicker">Pricing</span>\n    <h2 class="section-title">Custom Pricing, at Greater Discounts</h2>\n'
              '    <div class="sp-price reveal"><p>Multi-story buildings are priced after a free walkthrough of about 45 to 60 minutes. Within 24 hours you get a written scope and an exact price.</p></div>\n  </div>\n</section>\n\n'
            + how() + where + _faq(f) + _related('multi-story-building-cleaning.html') + c['cta_band']('Have a building with more than one floor?', 'Tell us about it and we will set up a free walkthrough.') + '</main>\n')
    pages['multi-story-building-cleaning.html'] = dict(title='Multi-Story Building Cleaning | Twin Cities | Lexonia', path='multi-story-building-cleaning.html', active='services.html',
        desc='Floor-by-floor cleaning for multi-story buildings in the Twin Cities: a different floor, or two, each night. Custom pricing after a free walkthrough.',
        body=body, ld_extra=service_ld('Floor-by-floor cleaning for multi-story buildings', 'A different floor, or two floors, cleaned each night, so the whole building is cleaned once every 1-2 weeks, depending on what it needs.', f, 'multi-story-building-cleaning.html', offer=False))

    # ---- interior windows add-on
    f = [('How much does interior window cleaning cost?', 'It is priced by the number of windows: %s, before sales tax.' % win_text),
         ('Is it part of the standard visit?', 'No. Interior windows are an add-on to a recurring cleaning visit. They are not part of the standard checklist. Interior glass on doors and partitions is on the office checklist.'),
         ('How do I add it?', 'Ask for it in your quote request, at the free walkthrough, or any time after cleaning starts.'), q_when, q_local]
    rows = ''.join('<div class="sp-win reveal"><strong>$%d</strong><span>%s</span></div>' % (p, n) for n, p in W)
    body = ('<main id="top">\n' + c['page_hero']('Add-On', 'Interior Window Cleaning, Added to Your Office Cleaning',
            'Interior windows can be added to a recurring cleaning visit, priced by the number of windows: %s, before sales tax.' % win_text)
            + subtabs('interior-window-cleaning.html')
            + '<section id="price">\n  <div class="container center">\n    <span class="kicker">Pricing</span>\n    <h2 class="section-title">Priced by the Number of Windows</h2>\n'
              '    <div class="sp-wins">' + rows + '</div>\n    <p class="section-lead" style="margin:18px auto 0">Before sales tax. Interior windows only, added to a recurring cleaning visit.</p>\n  </div>\n</section>\n\n'
            + _faq(f) + _related('interior-window-cleaning.html') + c['cta_band']() + '</main>\n')
    pages['interior-window-cleaning.html'] = dict(title='Interior Window Cleaning Add-On | Twin Cities | Lexonia', path='interior-window-cleaning.html', active='services.html',
        desc='Interior windows added to your office or store cleaning in the Twin Cities: $%d for 1-5, $%d for 6-10, $%d for 11-15, before tax.' % tuple(p for _n, p in W),
        body=body, ld_extra=service_ld('Interior window cleaning (add-on)', 'Interior windows added to a recurring cleaning visit, priced by the number of windows.', f, 'interior-window-cleaning.html', offer=False))
    assert sorted(pages) == sorted(NAMES)
    return pages


CSS = '''
/* Service pages: price box, window tiles, related links (phone first) */
.sp-price{max-width:760px;margin:24px auto 0;background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:24px 26px;box-shadow:var(--shadow-sm);text-align:left}
.sp-price p{color:var(--muted);margin:0 0 10px}
.sp-price p:last-child{margin-bottom:0}
.sp-from{font-size:1.05rem;color:var(--ink)!important}
.sp-from strong{font:800 1.6rem/1.1 'Sora',sans-serif;color:var(--teal-dark);margin-right:6px}
.sp-wins{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;max-width:640px;margin:24px auto 0}
.sp-win{background:#fff;border:1px solid var(--line);border-top:4px solid var(--teal);border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:4px}
.sp-win strong{font:800 1.5rem/1.1 'Sora',sans-serif;color:var(--teal-dark)}
.sp-win span{color:var(--muted);font-size:.92rem}
.sp-rel-row{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:14px}
.sp-rel{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:10px 16px;background:#fff;font-weight:600;font-size:.92rem;text-decoration:none;color:var(--teal-dark)}
.sp-rel:hover,.sp-rel:focus-visible{border-color:var(--teal)}
.subtabs{background:#fff;border-bottom:1px solid var(--line)}
.subtabs ul{list-style:none;display:flex;flex-wrap:wrap;gap:8px;padding:14px 0;margin:0}
.subtabs a{display:inline-block;padding:9px 16px;border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--teal-dark);font-weight:600;font-size:.92rem;text-decoration:none}
.subtabs a:hover,.subtabs a:focus-visible{border-color:var(--teal)}
.subtabs a.on{background:var(--teal);border-color:var(--teal);color:#fff}
@media (max-width:640px){.subtabs ul{gap:6px;padding:12px 0}.subtabs a{padding:8px 12px;font-size:.86rem}}
@media (max-width:640px){.sp-wins{grid-template-columns:1fr}}
'''
