#!/usr/bin/env python3
"""Builds the multi-page Lexonia Pro Clean site.
usage: build_site.py <outdir> <deploy|preview>
Every sentence on these pages must trace to something the owner stated or to the
commercial checklist (Operations/Checklists/Lexonia-Commercial-Cleaning-Checklist.pdf)."""
import sys, os, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import diagrams_how as DH
import blocks as BL
import price_cards as PC
import blog as BLOG
import privacy as PV   # privacy notice page; describes what the site actually collects
import service_pages as SP   # one page per service sold (owner go Oct 20 2026); text from the facts below
import ledger as LEDGER   # change ledger: every page change recorded in seo/changes.csv, 28 days apart (build fails otherwise)

out, MODE = sys.argv[1], sys.argv[2]
PREVIEW = MODE == 'preview'
here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(out, exist_ok=True)
import shutil as _sh
_sh.copytree(os.path.join(here, 'assets_src'), out, dirs_exist_ok=True)   # photos, audio, logos, icons

import json as _json
SITE = 'https://lexoniaproclean.com/'
BUILD_DATE = '2026-10-20'   # update when the content changes: used for sitemap lastmod and dateModified
CLARITY_ID = 'yybv330g41'   # Microsoft Clarity project (visitor analytics). The official snippet is written to the top of site.js (self-hosted, no inline script, CSP stays strict); its queue stub is required, the tag alone does not start
LOGO = 'lexonia-pro-clean-commercial-cleaning-logo.png'
LOGO_DARK = 'lexonia-pro-clean-commercial-cleaning-logo-dark.png'
OG_IMG = 'img/lexonia-pro-clean-commercial-cleaning-og.jpg'
SIZES = _json.load(open(os.path.join(here, 'seo_img_map.json')))['sizes']   # photo sizes, so every <img> has width/height (no layout shift)
PHONE = '(952) 697-4226'
TEL = 'tel:+19526974226'
EMAIL = 'info@lexoniaproclean.com'
from profiles import SAME_AS, TT_LINK, social_row, SOCIAL_CSS   # outside profiles: footer icons + sameAs, one list, in generator/profiles.py.
# Cities named on the site and in the schema = the service areas the owner entered on the Google listing (Oct 17 2026). Edit here only.
CITIES = ['Minneapolis', 'St. Paul', 'Eden Prairie', 'Edina', 'Bloomington', 'Minnetonka', 'Hopkins', 'Plymouth', 'Maple Grove', 'Golden Valley',
          'St. Louis Park', 'Richfield', 'Wayzata', 'Excelsior', 'Chanhassen', 'Chaska', 'Burnsville', 'Eagan', 'Mendota Heights']   # Hopkins and Chaska added Oct 20 2026 to match the listing
SUBURBS = ', '.join(CITIES[3:-1]) + ' and ' + CITIES[-1]   # the named suburbs after Minneapolis, St. Paul and Eden Prairie
HOURS_TEXT = '4 PM to 3 AM, seven days a week'   # cleaning hours, same as the Google listing
INDEXNOW_KEY = '626ea4651324daaccc90eb9ef9a7094b'   # IndexNow (Bing, Yandex, others): key file served at /<key>.txt; changed URLs are pinged after each deploy. Public by design

# Rotating hero photos: the owner's Site Assets folder (stock office photos), resized to site/img/hero/.
SLIDES = ['office-open-plan', 'office-desks-computers', 'office-empty-desks-plant', 'office-natural-light',
          'office-large-windows', 'office-robot-vacuum', 'office-minimalist-desks']

def slide_div(start):
    lst = ','.join('img/hero/%s.jpg' % n for n in SLIDES)
    n = SLIDES[start]
    from PIL import Image as _I
    w, h = _I.open(os.path.join(here, 'assets_src', 'img', 'hero', n + '.jpg')).size
    return ('<div class="hero-slides" data-slides="%s" data-start="%d" aria-hidden="true"><img class="on" src="img/hero/%s-1400.jpg" '
            'srcset="img/hero/%s-900.jpg 900w, img/hero/%s-1400.jpg 1400w, img/hero/%s.jpg 1800w" sizes="100vw" width="%d" height="%d" fetchpriority="high" alt=""></div>'
            % (lst, start, n, n, n, n, w, h))

_hero_counter = [0]

# The loop on the home page: pictures change on the beat of the music.
# Order: BEFORE, then its AFTER, for each of the owner's four before/after jobs; then his supplies and bin photos. (Office stock photos only rotate in the inner-page header bands.)
LOOP = []
for slug, what in [('break-room-island', 'break room island'), ('break-room-counter', 'break room counter'), ('sink-area', 'sink area'), ('sink-detail', 'sink detail')]:
    LOOP.append(('img/loop/lexonia-pro-clean-%s-before-cleaning.jpg' % slug, 'Before cleaning: %s, Lexonia Pro Clean commercial cleaning' % what, 'Before: %s' % what))
    LOOP.append(('img/loop/lexonia-pro-clean-%s-after-cleaning.jpg' % slug, 'After cleaning: %s, Lexonia Pro Clean commercial cleaning' % what, 'After: %s' % what))
LOOP += [('img/loop/lexonia-pro-clean-cleaning-supplies-shelf.jpg', 'Shelf of cleaning supplies used by Lexonia Pro Clean', 'Cleaning supplies'),
         ('img/loop/lexonia-pro-clean-janitorial-supply-caddy.jpg', 'Janitorial caddy stocked with supplies, Lexonia Pro Clean', 'Supply caddy'),
         ('img/loop/lexonia-pro-clean-cleaning-cart-mop-bucket-vacuum.jpg', 'Lexonia Pro Clean cleaning cart with mop bucket and vacuum', 'Cart, mop bucket and vacuum'),
         ('img/loop/lexonia-pro-clean-cleaning-cart-office-hallway.jpg', 'Lexonia Pro Clean cleaning cart in a clean office hallway', 'Cart in the hallway'),
         ('img/loop/lexonia-pro-clean-trash-station-fresh-liners.jpg', 'Office trash station with fresh liners, Lexonia Pro Clean', 'Trash station')]
PAUSE_ICON = ('<svg class="i-pause" width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="5" y="4" width="5" height="16" rx="1"/><rect x="14" y="4" width="5" height="16" rx="1"/></svg>'
              '<svg class="i-play" width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4l13 8-13 8z"/></svg>')

def loop_block():
    import json, html
    data = html.escape(json.dumps(LOOP, ensure_ascii=False), quote=True)
    f = LOOP[0]
    return ('<div class="loop" data-loop="%s">\n      <div class="loop-frame"><img class="on" src="%s" alt="%s" width="800" height="1000" fetchpriority="high"></div>\n'
            '      <div class="loop-bar"><span class="loop-cap">%s</span><button type="button" class="loop-pause" aria-pressed="false" aria-label="Pause the pictures">%s</button></div>\n    </div>' % (data, f[0], f[1], f[2], PAUSE_ICON))

FACTS = ''.join('      <div class="fact"><strong>%s</strong><span>%s</span></div>\n' % (v, l) for l, v in
                [('Response to quote requests', 'Same day'), ('Scheduling', 'Evenings &amp; nights'),
                 ('Cleaning liquids &amp; equipment', 'Included'), ('Walkthrough', 'Free')])

# ------------------------------------------------------------------ icons
def svg(inner, w=24, sw=2):
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (w, w, sw, inner))

I_OFFICE = '<rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/>'
I_BAG = '<path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/>'
I_CHECK = '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>'
I_LIST = '<polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>'
I_DOC = '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>'
I_TAG = '<path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/>'
I_CLOCK = '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>'
I_SHIELD = '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'
I_SHIELD_OK = '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>'
I_MSG = '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>'
I_USER = '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>'
I_PHONE = '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/>'
I_MAIL = '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>'
I_STAR = '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>'
I_ARROW = '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>'
I_MENU = '<line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>'

# ------------------------------------------------------------------ shared pieces
NAV = [('services.html', 'Services'), ('why-us.html', 'Why Us'), ('how-it-works.html', 'How It Works'),
       ('blog/', 'Blog'), ('contact.html', 'Contact')]

def header(active):
    links = ''
    for href, label in NAV:
        cur = ' class="active" aria-current="page"' if href == active else ''
        links += '        <li><a href="%s"%s>%s</a></li>\n' % (href, cur, label)
    return ('<header>\n  <div class="container nav">\n'
            '    <a href="index.html" class="brand" aria-label="Lexonia Pro Clean home">\n'
            '      <img class="logo-img" src="%s" alt="Lexonia Pro Clean, Commercial Cleaning" width="260" height="45">\n' % LOGO +
            '    </a>\n    <nav aria-label="Main">\n      <ul class="nav-links" id="navLinks">\n' + links + '      </ul>\n    </nav>\n'
            '    <div class="nav-cta">\n'
            '      <a class="nav-phone" href="%s">%s %s</a>\n' % (TEL, svg(I_PHONE, 17), PHONE) +
            '      <a href="contact.html" class="btn btn-primary">Free Quote</a>\n'
            '    </div>\n  </div>\n</header>\n')

def footer():
    return ('<footer class="site">\n  <div class="container">\n    <div class="footer-grid">\n      <div>\n'
            '        <div class="brand"><img class="logo-img" src="%s" alt="Lexonia Pro Clean, Commercial Cleaning" width="260" height="45" loading="lazy"></div>\n' % LOGO_DARK +
            '        <p>Commercial cleaning and janitorial services for offices and small retail stores across Minneapolis, St. Paul and the suburbs. Based in Eden Prairie. Insured and background-checked.</p>\n      </div>\n'
            '      <div>\n        <p class="f-h">Pages</p>\n        <ul>\n'
            '          <li><a href="services.html">Services</a></li>\n          <li><a href="why-us.html">Why Us</a></li>\n'
            '          <li><a href="how-it-works.html">How It Works</a></li>\n          <li><a href="blog/">Blog</a></li>\n        </ul>\n      </div>\n'
            '      <div>\n        <p class="f-h">Contact</p>\n        <address><ul>\n'
            '          <li><a href="%s">%s</a></li>\n          <li><a href="mailto:%s">%s</a></li>\n          <li><a href="contact.html">Request a Quote</a></li>\n          <li class="soc-li">%s</li>\n'
            '        </ul></address>\n      </div>\n'
            '    </div>\n    <div class="footer-bottom">\n      <span>© 2026 Lexonia Pro Clean LLC. All rights reserved. · <a href="privacy.html">Privacy</a></span>\n      <span>Eden Prairie, Minnesota</span>\n    </div>\n  </div>\n</footer>\n'
            '<div class="mbar" role="group" aria-label="Contact us">\n  <a class="mbar-call" href="%s">%s Call</a>\n  <a class="mbar-quote" href="contact.html">Free Quote</a>\n</div>\n'
            % (TEL, PHONE, EMAIL, EMAIL, social_row(), TEL, svg(I_PHONE, 18)))

def page_hero(kicker, h1, lead):
    _hero_counter[0] += 1
    return ('<section class="page-hero has-slides">\n  %s\n  <div class="container">\n    <span class="kicker">%s</span>\n    <h1>%s</h1>\n    <p class="lead">%s</p>\n  </div>\n</section>\n'
            % (slide_div(_hero_counter[0] % len(SLIDES)), kicker, h1, lead))

def cta_band(title='Ready for a cleaner space?', text='Tell us about your space and we will set up a free walkthrough.'):
    return ('<section class="cta-section">\n  <div class="container">\n    <div class="cta-band reveal">\n      <div><h3>%s</h3><p>%s</p></div>\n'
            '      <div class="cta-actions"><a href="contact.html" class="btn btn-primary">Get a Free Quote %s</a>'
            '<a href="%s" class="btn btn-ghost">%s</a></div>\n    </div>\n  </div>\n</section>\n' % (title, text, svg(I_ARROW, 18, 2.2), TEL, PHONE))

# ---- reviews: ONLY reviews the owner has confirmed are real customers. Add here after he confirms.
REVIEWS = [
    dict(name='Jess E.', job='Commercial cleaning', src='Customer review, Sep 2026',
         text='Oleg responded very quickly to our request for a quote and we were able to schedule a walkthrough and work out an arranged cleaning schedule very easily. He is very easy to work with and professional.'),
    dict(name='John S.', job='Office cleaning', src='Customer review, Sep 2026',
         text="We run a small office in Minnetonka — about 2,500 square feet — and most cleaning companies either won't quote something this size or treat it as an afterthought. Lexonia gave us a straight price up front and has been consistent since. Restrooms and the break room get done properly every visit, not just wiped down, and they leave a completed checklist so I can see exactly what was covered. They restock the supplies we keep on hand and flag when something's running low. I don't have to manage them."),
    dict(name='Doris F.', job='Office cleaning', src='Customer review',
         text="LEXONIA crew cleans after we close. Everyone Lexonia sends is background-checked and follows the same procedures-lights, locks, alarm, every time. Months in, not a single access issue. We come in to a clean office and no evidence anyone was here:-)"),
]

def reviews_section():
    cards = ''
    for r in REVIEWS:
        stars = ''.join(svg(I_STAR, 18, 1.5).replace('fill="none"', 'fill="currentColor"') for _ in range(5))
        cards += ('      <figure class="review-card reveal">\n        <div class="stars" role="img" aria-label="5 out of 5 stars">%s</div>\n'
                  '        <blockquote><p>%s</p></blockquote>\n        <figcaption><strong>%s</strong> &middot; %s<br><span>%s</span></figcaption>\n      </figure>\n'
                  % (stars, r['text'], r['name'], r['job'], r['src']))
    return ('<section class="reviews">\n  <div class="container center">\n    <span class="kicker">Reviews</span>\n'
            '    <h2 class="section-title">What Customers Say</h2>\n    <div class="review-list">\n' + cards + '    </div>\n'
            '  </div>\n</section>\n')

def multi_story(heading_tag='h2', link=True):
    return ('<div class="multi reveal">\n      <div>\n        <%s>Multi-Story Buildings</%s>\n'
            '        <p>For a building with more than one floor, we can clean a different floor, or two floors, each night. The whole building gets cleaned once every 1-2 weeks, depending on what it needs.</p>\n'
            + ('        <a href="contact.html" class="btn btn-primary">Ask About a Floor-by-Floor Schedule</a>\n' if link else '') +
            '      </div>\n      <ul>\n        <li>A different floor each night, or two floors</li>\n        <li>The whole building cleaned once every 1-2 weeks</li>\n        <li>How often depends on your building\'s needs</li>\n        <li>Custom pricing, at greater discounts</li>\n      </ul>\n    </div>\n') % (heading_tag, heading_tag)

def figure(img, alt, cap):
    w, h = SIZES[img]
    return ('      <figure class="reveal"><img src="img/%s" alt="%s" width="%d" height="%d" loading="lazy" decoding="async"><figcaption>%s</figcaption></figure>\n' % (img, alt, w, h, cap))

def ba_alt(what):
    return '%s before and after cleaning by Lexonia Pro Clean, commercial cleaning in the Twin Cities' % what

def pills():
    return ('    <div class="pill-row">\n'
            '      <span class="pill reveal">%s Corporate Offices</span>\n'
            '      <span class="pill reveal">%s Small Retail Stores &amp; Boutiques</span>\n    </div>\n'
            % (svg(I_OFFICE, 17), svg(I_BAG, 17)))

def card(icon, title, text, href=None, link=''):
    more = ('<a class="more-link" href="%s">%s</a>' % (href, link)) if href else ''
    return ('      <div class="card reveal">\n        <div class="icon">%s</div>\n        <h3>%s</h3>\n        <p>%s</p>%s\n      </div>\n' % (svg(icon, 26), title, text, more))

def why(icon, title, text, href=None, link=''):
    more = ('<a class="more-link" href="%s">%s</a>' % (href, link)) if href else ''
    return ('      <div class="why-item reveal">\n        <div class="icon">%s</div>\n        <div><h3>%s</h3><p>%s</p>%s</div>\n      </div>\n' % (svg(icon, 22), title, text, more))

def step(n, title, text):
    return '      <div class="step reveal"><div class="num">%s</div><h3>%s</h3><p>%s</p></div>\n' % (n, title, text)

def box(title, items):
    return ('      <div class="box reveal">\n        <h3>%s</h3>\n        <ul>\n' % title + ''.join('          <li>%s</li>\n' % i for i in items) + '        </ul>\n      </div>\n')

# ---- pricing (source: Operations\\PRICING-MASTER.md, "Commercial - per visit", checked 2026-10-14; owner: multi-story = custom pricing at greater discounts)
PRICE_ROWS = [('1,000 – 2,000', 155, 163), ('2,000 – 3,000', 220, 231), ('3,000 – 4,000', 270, 284), ('4,000 – 5,000', 340, 357),
              ('5,000 – 6,000', 410, 431), ('6,000 – 7,000', 480, 504), ('7,000 – 8,000', 540, 567), ('8,000 – 9,000', 610, 641), ('9,000 – 10,000', 670, 704)]
WIN_ROWS = [('1–5 windows', 40), ('6–10 windows', 70), ('11–15 windows', 110)]
PRICE_FROM, PRICE_TOP = PRICE_ROWS[0][1], PRICE_ROWS[-1][1]

PRICE_IMG = PC.render(PRICE_ROWS, WIN_ROWS, os.path.join(out, 'img', 'pricing'), here)   # prices live only in these images, not in page text

def _price_img(key, alt):
    src, w, h = PRICE_IMG[key]
    return '<img src="%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async" draggable="false">' % (src, w, h, alt)

def pricing_section():
    t_alt = ('Price card: recurring cleaning price per visit by size of space, weekly or every other week, for spaces from 1,000 to 10,000 square feet. '
             'For your exact price, request a free quote or call %s.' % PHONE)
    w_alt = 'Price card: interior windows add-on, priced by the number of windows (1 to 5, 6 to 10, or 11 to 15). For the price, request a free quote or call %s.' % PHONE
    return ('<section id="pricing" class="pricing">\n  <div class="container center">\n    <span class="kicker">Pricing</span>\n    <h2 class="section-title">Pricing by Size of Space</h2>\n'
        '    <p class="section-lead" style="margin:0 auto">Recurring cleaning, weekly or every other week, for spaces up to 10,000 sq ft. Cleaning liquids and equipment are included. Your exact price is confirmed in writing after a free walkthrough.</p>\n'
        '    <div class="pshow">\n'
        '      <figure class="pimg reveal">' + _price_img('by-size', t_alt) + '</figure>\n'
        '      <div class="pside">\n'
        '        <figure class="pimg reveal">' + _price_img('windows', w_alt) + '</figure>\n'
        '        <div class="pcard reveal"><h3>Daily cleaning, or over 10,000 sq ft</h3><p>A flat monthly contract, quoted after the free walkthrough, so you know your exact cost before we start.</p></div>\n'
        '        <div class="pcard pcard-hi reveal"><h3>Multi-story buildings</h3><p>Custom pricing, at greater discounts. A different floor, or two, each night.</p><p><a href="#multi-story" class="pcard-link">How floor-by-floor works</a></p></div>\n'
        '      </div>\n    </div>\n'
        '    <p class="more"><a href="contact.html" class="btn btn-primary">Get Your Free Quote ' + svg(I_ARROW, 18, 2.2) + '</a></p>\n  </div>\n</section>\n\n')

SERVICE_CARDS = (
    card(I_OFFICE, 'Office Cleaning',
         'Recurring cleaning for offices — workspaces, common areas, conference rooms, break rooms, and restrooms, with high-touch points disinfected every visit.',
         'office-cleaning.html', 'More on office cleaning')
    + card(I_BAG, 'Small Retail &amp; Boutique Cleaning',
           'Recurring cleaning for small retail stores — sales floor, front counter, fitting rooms, mirrors, restrooms, and back rooms, scheduled around your hours.',
           'retail-cleaning.html', 'More on retail cleaning'))

WHY_ITEMS = (
    why(I_LIST, 'Checklist-Driven Visits', 'Every visit follows a written checklist, and a completed copy is left on site so you can see exactly what was done.', 'services.html#checklist', 'See the checklist')
    + why(I_DOC, 'Free Walkthrough, Written Price', 'We visit your space, then send a written scope and an exact price within 24 hours.', 'how-it-works.html#process', 'See the process')
    + why(I_TAG, 'Everything Included', 'We bring the cleaning liquids and our own equipment. All of it is included in the price. No surprise fees and no travel charges.', 'services.html#not-included', 'What is not included')
    + why(I_CLOCK, 'Evenings and Nights', 'We clean when your business is closed, so we are never in your way.', 'how-it-works.html#every-visit', 'What a visit looks like')
    + why(I_SHIELD, 'Insured and Background-Checked', 'Fully insured, with background-checked crews.')
    + why(I_MSG, 'Same-Day Response', 'Every message gets a same-day response.', 'contact.html', 'Ask a question'))

AROUND = ('    <div class="guarantee reveal">\n      <div class="g-icon">%s</div>\n      <div>\n        <h3>We Clean Around Your Work</h3>\n'
          '        <p>Desks are dusted around whatever is on them. We never move, stack or read paperwork, and nothing is opened, filed, thrown out or rearranged.</p>\n'
          '      </div>\n      <a href="contact.html" class="btn btn-primary">Get Your Free Quote</a>\n    </div>\n' % svg(I_SHIELD_OK, 30))

FAQ = [
    ('What does Lexonia Pro Clean clean?', 'We clean offices and small retail stores and boutiques across the Twin Cities metro: workspaces, common areas, conference rooms, break rooms, restrooms, sales floors, mirrors, fitting rooms and back rooms. Every visit follows a written checklist.'),
    ('Where is Lexonia Pro Clean based, and where do you work?', 'We are based in Eden Prairie, Minnesota, and serve Minneapolis, St. Paul and the suburbs, including ' + SUBURBS + '. If you are just outside the metro, ask anyway.'),
    ('When do you clean?', 'Evenings and nights, when your business is closed, so we are never in your way.'),
    ('Do you bring your own supplies and equipment?', 'Yes. We bring the cleaning liquids and our own equipment. All of it is included in the price, with no surprise fees and no travel charges.'),
    ('Who supplies trash bags, soap and paper towels?', 'Your company or building management supplies the consumables: trash bags, soap, paper towels, tissue and restroom disposal bags. We do not supply or buy them. We restock them from your supply every visit and tell you when something is running low.'),
    ('How does pricing work?', 'We start with a free walkthrough of your space, about 45 to 60 minutes. Within 24 hours you get a written scope and an exact price. For spaces up to 10,000 sq ft, weekly or every other week, the price is per visit by size of space, before sales tax: from $%d per visit for 1,000 to 2,000 sq ft, weekly (the full price card is on the Services page).' % PRICE_FROM + ' Daily cleaning, or a space over 10,000 sq ft, is a flat monthly contract quoted after the walkthrough, so you know your exact cost before we start. Multi-story buildings get custom pricing, at greater discounts.'),
    ('How fast do you respond to a quote request?', 'Every message gets a same-day response.'),
    ('What happens after the first visit?', 'The first visit is a reset clean that brings everything up to standard. Recurring visits then maintain it from there. We check in after two weeks and adjust the scope until it fits.'),
    ('How will I know what was cleaned?', 'Every visit follows a written checklist, and a completed copy is left on site so you can see exactly what was done.'),
    ('Are you insured, and are your crews background-checked?', 'Yes. Lexonia Pro Clean is fully insured, and our crews are background-checked.'),
    ('Can you clean a multi-story building?', 'Yes. We can clean a different floor, or two floors, each night, so the whole building is cleaned once every 1-2 weeks, depending on what it needs. Multi-story buildings get custom pricing, at greater discounts.'),
    ('Do you clean windows?', 'Interior windows can be added to a visit, priced by the number of windows (1-5, 6-10 or 11-15), before sales tax. They are not part of the standard checklist.'),
    ('Will you move or read the papers on my desk?', 'No. Desks are dusted around whatever is on them. We never move, stack or read paperwork, and nothing is opened, filed, thrown out or rearranged.'),
    ('What is not included?', 'Operating or maintaining your machines, moving furniture, equipment or paperwork, and biohazard, hoarding or post-construction cleanup.'),
]

def faq_section():
    import html as _h
    items = ''
    for q, a in FAQ:
        ans = _h.escape(a)
        items += '      <details class="faq-item"><summary>%s</summary><p>%s</p></details>\n' % (_h.escape(q), ans)
    return ('<section class="faq" id="faq">\n  <div class="container">\n    <div class="center"><span class="kicker">FAQ</span>\n    <h2 class="section-title">Common Questions</h2></div>\n'
            '    <div class="faq-list">\n' + items + '    </div>\n  </div>\n</section>\n\n')

FORM = ('      <form class="quote-form" name="quote-request" method="POST" action="/thanks.html" data-netlify="true" netlify-honeypot="bot-field">\n'
        '        <input type="hidden" name="form-name" value="quote-request">\n'
        '        <p class="hidden" aria-hidden="true"><label>Don\'t fill this out: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>\n'
        '        <div class="form-row">\n'
        '          <div class="field"><label for="f-name">Name *</label><input id="f-name" name="name" type="text" required maxlength="100" autocomplete="name" placeholder="Your name"></div>\n'
        '          <div class="field"><label for="f-company">Company</label><input id="f-company" name="company" type="text" maxlength="120" autocomplete="organization" placeholder="Business name"></div>\n        </div>\n'
        '        <div class="form-row">\n'
        '          <div class="field"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" required maxlength="254" autocomplete="email" placeholder="you@company.com"></div>\n'
        '          <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" maxlength="30" autocomplete="tel" inputmode="tel" placeholder="Your phone number"></div>\n        </div>\n'
        '        <div class="form-row">\n          <div class="field">\n            <label for="f-service">Service Needed *</label>\n'
        '            <select id="f-service" name="service" required>\n              <option value="" disabled selected>Select a service</option>\n'
        '              <option>Office Cleaning</option>\n              <option>Small Retail Store / Boutique</option>\n              <option>Other / Not Sure</option>\n            </select>\n          </div>\n'
        '          <div class="field">\n            <label for="f-frequency">Frequency</label>\n            <select id="f-frequency" name="frequency">\n'
        '              <option value="" disabled selected>How often?</option>\n              <option>Weekly</option>\n              <option>Every other week</option>\n              <option>2–3x per week</option>\n'
        '              <option>Nightly (5x+ per week)</option>\n              <option>Not sure yet</option>\n            </select>\n          </div>\n        </div>\n'
        '        <div class="field"><label for="f-size">Approx. Square Footage</label><input id="f-size" name="square_footage" type="text" maxlength="40" inputmode="text" placeholder="e.g., 5,000 sq ft"></div>\n'
        '        <div class="field"><label for="f-message">Anything else we should know?</label><textarea id="f-message" name="message" maxlength="2000" rows="4" placeholder="Current setup, pain points, timing…"></textarea></div>\n'
        '        <button type="submit" class="btn btn-primary">Request My Free Quote</button>\n'
        '        <p class="form-note">Same-day response. No spam, no pressure.</p>\n      </form>\n')

# ------------------------------------------------------------------ pages
pages = {}

# ---- HOME
HOME_FLOW = [('chat', 'Ask for a quote', 'Use the form, call, or email us. Every message gets a same-day response.'),
             ('walk', 'Free walkthrough', 'About 45 to 60 minutes. We go over what needs to be cleaned and how often.'),
             ('doc', 'Written scope and price', 'Within 24 hours, with an exact price. No surprise fees.'),
             ('moon', 'Cleaning starts', 'Evenings and nights, on your written checklist.')]
hero_svg = ('<svg class="bubbles" width="100%" height="100%" viewBox="0 0 1200 600" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            '<circle cx="1050" cy="110" r="130" fill="rgba(53,194,207,.08)"/><circle cx="920" cy="420" r="70" fill="rgba(53,194,207,.07)"/>'
            '<circle cx="180" cy="500" r="100" fill="rgba(139,227,236,.05)"/><circle cx="80" cy="90" r="46" fill="rgba(53,194,207,.09)"/>'
            '<circle cx="620" cy="60" r="26" fill="rgba(139,227,236,.10)"/></svg>')
home = ('<main id="top">\n<section class="hero" style="padding-top:110px">\n  ' + hero_svg + '\n  <div class="container hero-grid">\n    <div>\n'
    '      <span class="kicker" style="color:var(--cyan)">Twin Cities · Commercial Cleaning &amp; Janitorial</span>\n'
    '      <h1>A Cleaner Workplace.<br>A <span class="accent">Sharper</span> First Impression.</h1>\n'
    '      <p class="lead">Lexonia Pro Clean keeps Twin Cities offices and small retail stores consistently spotless — with background-checked crews, a written checklist for every visit, and a same-day response to every message.</p>\n'
    '      <div class="hero-actions">\n        <a href="contact.html" class="btn btn-primary">Get a Free Quote ' + svg(I_ARROW, 18, 2.2) + '</a>\n        <a href="services.html" class="btn btn-light">Our Services</a>\n      </div>\n'
    '      <div class="trust-row">\n'
    '        <div class="trust-chip">' + svg(I_SHIELD, 18, 2.2) + ' Insured</div>\n'
    '        <div class="trust-chip">' + svg(I_USER, 18, 2.2) + ' Background-Checked Crews</div>\n'
    '        <div class="trust-chip">' + svg(I_CHECK, 18, 2.2) + ' Checklist Every Visit</div>\n      </div>\n    </div>\n'
    '    <div class="hero-art">\n      ' + loop_block() + '\n    </div>\n  </div>\n'
    '  <svg class="wave" viewBox="0 0 1440 90" fill="none" preserveAspectRatio="none" aria-hidden="true" style="display:block;width:100%;height:70px"><path d="M0,50 C280,110 520,0 760,30 C1000,60 1200,80 1440,40 L1440,90 L0,90 Z" fill="#f4fafb"/></svg>\n</section>\n\n'
    '<section class="facts">\n  <div class="container">\n    <div class="facts-grid">\n' + FACTS + '    </div>\n  </div>\n</section>\n\n'
    '<section class="services">\n  <div class="container center">\n    <span class="kicker">What We Do</span>\n    <h2 class="section-title">Cleaning Built Around Your Space</h2>\n'
    '    <p class="section-lead">Recurring cleaning for offices and small retail stores, on a written checklist you can read before we start.</p>\n'
    '    <div class="cards">\n' + SERVICE_CARDS + '    </div>\n    <p class="price-tease">Recurring cleaning is priced <strong>per visit</strong>, by size of space. <a href="services.html#pricing">See the price card</a></p>\n    <p class="more"><a href="services.html" class="btn btn-ghost">See everything we do</a></p>\n  </div>\n</section>\n\n'
    '<section class="industries">\n  <div class="container center">\n    <span class="kicker">How It Works</span>\n    <h2 class="section-title">From First Message to First Clean</h2>\n'
    '    <p class="section-lead" style="margin:0 auto">A free walkthrough, then a written scope and an exact price within 24 hours.</p>\n    ' + BL.flow(HOME_FLOW, 'from first message to first clean') + '\n'
    '    <p class="flow-cta"><a href="how-it-works.html" class="btn btn-ghost">See the full process map</a></p>\n  </div>\n</section>\n\n'
    '<section>\n  <div class="container">\n    ' + multi_story('h2', link=True) + '  </div>\n</section>\n\n'
    '<section>\n  <div class="container center">\n    <span class="kicker">Our Work</span>\n    <h2 class="section-title">Before and After</h2>\n'
    '    <p class="section-lead">Break room surfaces and a sink area, before and after a visit.</p>\n    <div class="gallery two">\n'
    + figure('lexonia-pro-clean-break-room-island-before-and-after.jpg', ba_alt('Break room island'), 'Break room island')
    + figure('lexonia-pro-clean-sink-area-before-and-after.jpg', ba_alt('Sink area'), 'Sink area')
    + '    </div>\n    <p class="more"><a href="services.html#our-work" class="btn btn-ghost">More photos</a></p>\n  </div>\n</section>\n\n'
    '<section class="industries">\n  <div class="container center">\n    <span class="kicker">Who We Serve</span>\n    <h2 class="section-title">Built for Offices and Boutiques</h2>\n'
    '    <p class="section-lead" style="margin:0 auto">Every space has different standards. We tailor the checklist and the schedule to yours.</p>\n' + pills() + '    <p class="price-tease" style="margin-top:30px">Based in Eden Prairie, serving Minneapolis, St. Paul and the suburbs: ' + SUBURBS + '.</p>\n  </div>\n</section>\n\n'
    + reviews_section() + '\n' + cta_band() + '</main>\n')
pages['index.html'] = dict(title='Lexonia Pro Clean | Commercial Cleaning for Offices and Small Retail — Twin Cities, MN',
    desc='Commercial cleaning for offices and small retail stores across the Twin Cities metro. Insured, background-checked crews. Free walkthrough, then a written scope and exact price within 24 hours.',
    active='', body=home)

# ---- SERVICES page
CHECKLIST = [
    ('Restrooms', ['Toilets and urinals disinfected', 'Sinks, counters and fixtures', 'Mirrors', 'Partitions, stall doors and handles', 'Floors swept and mopped with disinfectant', 'Trash emptied and bins re-lined', 'Soap, towels, tissue and liners restocked from your supply']),
    ('Break room / kitchenette', ['Counters and backsplash wiped down', 'Sink scrubbed and rinsed', 'Appliance exteriors — fridge, microwave, dishwasher', 'Tables and chairs', 'Cabinet fronts spot-cleaned', 'Trash emptied and bins re-lined', 'Floor vacuumed and mopped']),
    ('Offices and workspaces', ['Desks and accessible surfaces dusted', 'Shelves, sills and ledges', 'Trash emptied at every station and re-lined', 'Carpets vacuumed', 'Hard floors mopped']),
    ('Common areas', ['Reception, lobby and waiting areas', 'Conference rooms — tables wiped, chairs squared', 'Interior glass on doors and partitions', 'Corridors vacuumed and mopped', 'Stair and elevator landings within the suite', 'Entry mats vacuumed or shaken out']),
    ('High-touch points, disinfected', ['Door handles and push plates', 'Light switches', 'Elevator and keypad buttons', 'Handrails', 'Shared appliance handles and controls', 'Reception counter edge']),
    ('Small retail stores', ['Sales floor swept and mopped', 'Rugs vacuumed', 'Mirrors cleaned', 'Display pieces wiped down', 'Front counter wiped, counter edge disinfected', 'Fitting rooms wiped down', 'Restroom, break room, back rooms and trash']),
]   # the written checklist: services page and service pages read it from here
included = ''.join(box(t, items) for t, items in CHECKLIST)
not_incl = ['Windows (interior windows can be added)', 'Operating or maintaining your machines', 'Consumables such as trash bags, soap, paper towels and tissue — your company or building management supplies them',
            'Moving furniture, equipment or paperwork', 'Biohazard, hoarding or post-construction cleanup']
services = ('<main id="top">\n' + page_hero('Services', 'Commercial Cleaning for Offices and Small Retail Stores',
    'Recurring cleaning on a written checklist. We bring the cleaning liquids and our equipment, all included in the price.')
    + SP.subtabs('services.html')
    + '<section class="services">\n  <div class="container center">\n    <h2 class="sr-only">What we clean</h2>\n    <div class="cards">\n' + SERVICE_CARDS + '    </div>\n'
    + '  </div>\n</section>\n\n'
    + pricing_section() +
    '<section id="checklist">\n  <div class="container center">\n    <span class="kicker">The Checklist</span>\n    <h2 class="section-title">What We Do Every Visit</h2>\n'
    '    <p class="section-lead">Office visits follow this written scope, and a completed copy is left on site. Retail checklists are built around your store.</p>\n'
    '    <div class="incl">\n' + included + '    </div>\n'
    '    <div class="notbox reveal" id="not-included">\n      <h3>Not included, so there are no surprises</h3>\n      <ul>\n' + ''.join('        <li>%s</li>\n' % i for i in not_incl) + '      </ul>\n'
    '      <p>Your company or building management supplies the consumables: trash bags, soap, paper towels, tissue and restroom disposal bags. We do not supply or buy them. We bring the cleaning liquids and we restock the consumables from your supply every visit and tell you when something is running low.</p>\n    </div>\n  </div>\n</section>\n\n'
    '<section id="multi-story">\n  <div class="container">\n    <span class="kicker" style="display:block;text-align:center">Larger Buildings</span>\n    ' + multi_story('h3', link=False) + '  </div>\n</section>\n\n'
    '<section class="services" id="our-work">\n  <div class="container center">\n    <span class="kicker">Our Work</span>\n    <h2 class="section-title">Photos</h2>\n'
    '    <div class="gallery two">\n'
    + figure('lexonia-pro-clean-break-room-island-before-and-after.jpg', ba_alt('Break room island'), 'Break room island, before and after')
    + figure('lexonia-pro-clean-break-room-counter-before-and-after.jpg', ba_alt('Break room counter'), 'Counter, before and after')
    + figure('lexonia-pro-clean-sink-area-before-and-after.jpg', ba_alt('Sink area'), 'Sink area, before and after')
    + figure('lexonia-pro-clean-sink-detail-before-and-after.jpg', ba_alt('Sink detail'), 'Sink detail, before and after')
    + '    </div>\n    <div class="gallery three">\n'
    + figure('lexonia-pro-clean-restroom-vanity-cleaning.jpg', 'Clean restroom vanity after a Lexonia Pro Clean commercial cleaning visit in the Twin Cities', 'Restroom vanity')
    + figure('lexonia-pro-clean-kitchenette-sink-cleaning.jpg', 'Clean kitchenette sink after a Lexonia Pro Clean commercial cleaning visit in the Twin Cities', 'Kitchenette sink')
    + figure('lexonia-pro-clean-trash-station-cleaning.jpg', 'Office trash station with fresh liners, Lexonia Pro Clean commercial cleaning', 'Trash station')
    + '    </div>\n    <h3 class="gallery-sub">Our equipment</h3>\n    <div class="gallery three">\n'
    + figure('lexonia-pro-clean-janitorial-caddy-supplies.jpg', 'Janitorial caddy stocked with cleaning supplies, Lexonia Pro Clean', 'Supply caddy')
    + figure('lexonia-pro-clean-cleaning-cart-and-vacuum.jpg', 'Lexonia Pro Clean cleaning cart with mop bucket and vacuum', 'Cart, mop bucket and vacuum')
    + figure('lexonia-pro-clean-upright-vacuum.jpg', 'Upright vacuum used by Lexonia Pro Clean commercial cleaning crews', 'Vacuum')
    + '    </div>\n  </div>\n</section>\n\n' + cta_band() + '</main>\n')
pages['services.html'] = dict(title='Services | Lexonia Pro Clean',
    desc='Recurring commercial cleaning for offices and small retail stores in the Twin Cities metro, on a written checklist.', active='services.html', body=services)

# ---- WHY US
WHY_FLOW = [('walk', 'Free walkthrough', 'About 45 to 60 minutes, so we can see the space and talk through what needs to be cleaned.'),
            ('doc', 'Written scope and price', 'Within 24 hours: an exact price, with cleaning liquids and equipment included.'),
            ('moon', 'First visit: a reset clean', 'Evenings and nights, on your written checklist. A completed copy is left on site.'),
            ('chat', 'Two-week check-in', 'We check in and adjust the scope until it fits.'),
            ('list', 'Maintenance visits', 'After that, each visit maintains it, on your schedule.')]
why_page = ('<main id="top">\n' + page_hero('Why Us', 'How We Work', 'A written checklist for every visit, and an exact price in writing before we start.')
    + '<section>\n  <div class="container">\n    <h2 class="sr-only">Why choose Lexonia Pro Clean</h2>\n    <div class="why-grid">\n' + WHY_ITEMS + '    </div>\n' + AROUND + '  </div>\n</section>\n\n'
    + reviews_section() + '\n' + cta_band() + '</main>\n')
pages['why-us.html'] = dict(title='Why Us | Lexonia Pro Clean',
    desc='Written checklist every visit, free walkthrough, exact price in writing, evenings and nights, insured and background-checked.', active='why-us.html', body=why_page)

# ---- HOW IT WORKS
how = ('<main id="top">\n' + page_hero('How It Works', 'From First Call to First Clean', 'A free walkthrough, a written scope, and an exact price before anything starts.')
    + '<section class="jump-sec">\n  <div class="container">' + BL.jump([('process', 'Process map'), ('first-weeks', 'First weeks'), ('every-visit', 'Every visit'), ('how-we-price', 'Pricing'), ('larger-buildings', 'Larger buildings'), ('faq', 'FAQ')]) + '</div>\n</section>\n\n'
    + '<section id="process">\n  <div class="container center">\n    <span class="kicker">The Process Map</span>\n    <h2 class="section-title">Who Does What, Step by Step</h2>\n'
    '    <p class="section-lead" style="margin:0 auto">From your first message to your first clean. Every step, and who takes it.</p>\n    ' + DH.swimlane() + '\n  </div>\n</section>\n\n'
    '<section class="industries" id="first-weeks">\n  <div class="container center">\n    <span class="kicker">What To Expect</span>\n    <h2 class="section-title">Your First Few Weeks</h2>\n'
    '    <p class="section-lead" style="margin:0 auto">From the walkthrough to a routine that fits your space.</p>\n    ' + BL.flow(WHY_FLOW, 'what to expect in your first few weeks', 'Then the same visit, on your schedule') + '\n  </div>\n</section>\n\n'
    '<section class="industries" id="every-visit">\n  <div class="container">\n    ' + DH.visit_prep() + '\n  </div>\n</section>\n\n'
    '<section id="how-we-price">\n  <div class="container center">\n    <span class="kicker">Pricing</span>\n    <h2 class="section-title">How We Price</h2>\n'
    '    <p class="section-lead" style="margin:0 auto">Every job ends in a written scope and an exact price. This is how we get there.</p>\n    ' + DH.price_flow() + '\n  </div>\n</section>\n\n'
    '<section class="industries" id="larger-buildings">\n  <div class="container">\n    <div class="center"><span class="kicker">Larger Buildings</span>\n    <h2 class="section-title">Multi-Story Buildings, Floor by Floor</h2></div>\n'
    '    <div class="multi-how reveal">\n      <div><h3>A different floor, or two, each night</h3>\n      <p>The whole building is cleaned once every 1 to 2 weeks, depending on what it needs. Multi-story buildings get custom pricing, at greater discounts.</p>\n'
    '      <p><a href="services.html#multi-story" class="btn btn-ghost">More on multi-story buildings</a></p></div>\n      ' + DH.floors_diagram() + '\n    </div>\n  </div>\n</section>\n\n'
    + faq_section() + cta_band() + '</main>\n')
pages['how-it-works.html'] = dict(title='How It Works | Lexonia Pro Clean',
    desc='Free walkthrough, then a written scope and exact price within 24 hours. Every visit follows your written checklist.', active='how-it-works.html', body=how)

# ---- CONTACT
contact = ('<main id="top">\n<section class="quote">\n  <div class="container">\n    <div class="quote-grid">\n      <div>\n        <span class="kicker">Free Quote</span>\n'
    '        <h1 class="section-title">Let\'s Talk About Your Space</h1>\n'
    '        <p class="section-lead">Tell us a little about your space and we\'ll get back to you the same day — with a real answer, not a sales pitch.</p>\n'
    '        ' + BL.next_steps([('We reply the same day', 'Every message gets a same-day response.'), ('Free walkthrough', 'About 45 to 60 minutes at your space, so we can go over what needs to be cleaned and how often.'),
                               ('Written scope and exact price', 'Within 24 hours of the walkthrough. No surprise fees.')]) + '\n'
    '        <div class="contact-list">\n'
    '          <div class="contact-item"><div class="icon">' + svg(I_PHONE, 20) + '</div><div><small>Call or Text</small><a href="' + TEL + '">' + PHONE + '</a></div></div>\n'
    '          <div class="contact-item"><div class="icon">' + svg(I_MAIL, 20) + '</div><div><small>Email</small><a href="mailto:' + EMAIL + '">' + EMAIL + '</a></div></div>\n'
    '        </div>\n'
    '      </div>\n' + FORM + '    </div>\n  </div>\n</section>\n</main>\n')
pages['contact.html'] = dict(title='Contact and Free Quote | Lexonia Pro Clean',
    desc='Request a free quote for office or small retail cleaning in the Twin Cities metro. Same-day response.', active='contact.html', body=contact)

# ---- THANKS
thanks = ('<main id="top">\n' + page_hero('Thank you', 'Request Received', 'Thanks for reaching out to Lexonia Pro Clean. We\'ll get back to you the same day with next steps — usually to set up a quick, free walkthrough of your space.')
    + '<section>\n  <div class="container center"><p><a href="index.html" class="btn btn-primary">Back to the Home Page</a></p></div>\n</section>\n</main>\n')
pages['thanks.html'] = dict(title='Thank You | Lexonia Pro Clean', desc='Your request was received.', active='', body=thanks, noindex=True)

# ---- PRIVACY (text and rules live in generator/privacy.py)
pages['privacy.html'] = dict(title=PV.TITLE, desc=PV.DESC, active='', path='privacy.html', body=PV.body(page_hero, EMAIL, PHONE, TEL))

# ------------------------------------------------------------------ render
FONTS = ('<link rel="preload" href="fonts/sora-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
         '<link rel="preload" href="fonts/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>\n')
# ------------------------------------------------------------------ SEO / GEO
META = {
    'index.html': dict(title='Commercial Cleaning & Janitorial Services | Twin Cities MN', path='',
        desc='Commercial cleaning and janitorial services for offices and small retail stores in Minneapolis, St. Paul and the suburbs. Insured crews. Free walkthrough.'),
    'services.html': dict(title='Commercial Cleaning Services | Eden Prairie & Twin Cities MN', path='services.html',
        desc='Recurring office and small retail cleaning in the Twin Cities, priced per visit by size of space, on a written checklist. Liquids and equipment included.'),
    'why-us.html': dict(title='Why Choose Lexonia Pro Clean | Commercial Cleaning MN', path='why-us.html',
        desc='A written checklist every visit, a free walkthrough, an exact written price, evenings and nights, and insured, background-checked crews in the Twin Cities.'),
    'how-it-works.html': dict(title='How Commercial Cleaning Works + FAQ | Lexonia Pro Clean', path='how-it-works.html',
        desc='A free walkthrough, then a written scope and an exact price within 24 hours. Answers on supplies, scheduling, insurance and multi-story buildings.'),
    'contact.html': dict(title='Free Quote for Commercial Cleaning | Lexonia Pro Clean', path='contact.html',
        desc='Request a free quote for office or small retail cleaning in the Twin Cities. Same-day response. Call (952) 697-4226 or email us.'),
}
for _n, _m in META.items():
    pages[_n].update(_m)
    assert len(_m['title']) <= 62, (_n, len(_m['title']))
    assert len(_m['desc']) <= 160, (_n, len(_m['desc']))
pages['thanks.html']['path'] = 'thanks.html'

BIZ_ID = SITE + '#business'
SERVICES_LD = [
    ('Office cleaning', 'Recurring cleaning for offices: workspaces, common areas, conference rooms, break rooms, and restrooms, with high-touch points disinfected every visit.'),
    ('Small retail and boutique cleaning', 'Recurring cleaning for small retail stores: sales floor, front counter, fitting rooms, mirrors, restrooms, and back rooms, scheduled around your hours.'),
    ('Floor-by-floor cleaning for multi-story buildings', 'A different floor, or two floors, cleaned each night, so the whole building is cleaned once every 1-2 weeks, depending on what it needs.'),
    ('Interior window cleaning (add-on)', 'Interior windows can be added to a recurring cleaning visit.'),
]
AREA_LD = [{'@type': 'City', 'name': c, 'containedInPlace': {'@type': 'State', 'name': 'Minnesota'}} for c in CITIES] + \
          [{'@type': 'AdministrativeArea', 'name': 'Twin Cities metro, Minnesota'}]
def business_ld(full=True):
    b = {'@type': ['LocalBusiness', 'ProfessionalService'], '@id': BIZ_ID, 'name': 'Lexonia Pro Clean', 'url': SITE}
    if not full: return b
    b.update({'legalName': 'Lexonia Pro Clean LLC',
        'description': 'Commercial cleaning and janitorial services for offices and small retail stores across Minneapolis, St. Paul and the Twin Cities suburbs, based in Eden Prairie, Minnesota. Recurring service on a written checklist, evenings and nights, with insured, background-checked crews.',
        'knowsAbout': ['Commercial cleaning', 'Janitorial services', 'Office cleaning', 'Retail store cleaning'],
        'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 'opens': '16:00', 'closes': '03:00'}],
        'logo': {'@type': 'ImageObject', 'url': SITE + LOGO}, 'image': [SITE + OG_IMG],
        'telephone': '+1-952-697-4226', 'email': EMAIL, 'sameAs': SAME_AS,
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Eden Prairie', 'addressRegion': 'MN', 'addressCountry': 'US'},
        'areaServed': AREA_LD,
        'geo': {'@type': 'GeoCoordinates', 'latitude': 44.8547, 'longitude': -93.4708},   # Eden Prairie city centre, not a street address
        'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Commercial cleaning services',
            'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n, 'description': d}} for n, d in SERVICES_LD]}})
    return b
pages.update(SP.build(dict(page_hero=page_hero, cta_band=cta_band, box=box, flow=BL.flow, glance=BL.glance, floors=DH.floors_diagram,
    CHECKLIST=CHECKLIST, NOT_INCL=not_incl, FAQ=FAQ, HOME_FLOW=HOME_FLOW, PRICE_FROM=PRICE_FROM, WIN_ROWS=WIN_ROWS, CITIES=CITIES,
    HOURS_TEXT=HOURS_TEXT, SITE=SITE, BIZ_ID=BIZ_ID, AREA_LD=AREA_LD)))
for _n in SP.NAMES:
    assert len(pages[_n]['title']) <= 62, (_n, len(pages[_n]['title']))
    assert len(pages[_n]['desc']) <= 160, (_n, len(pages[_n]['desc']))

def crumbs(name, label):
    items = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE}]
    if name != 'index.html': items.append({'@type': 'ListItem', 'position': 2, 'name': label, 'item': SITE + name})
    return {'@type': 'BreadcrumbList', 'itemListElement': items}
def page_ld(name, p):
    url = SITE + p.get('path', '')
    graph = []
    if name == 'index.html':
        graph.append(business_ld(True))
        graph.append({'@type': 'WebSite', '@id': SITE + '#website', 'url': SITE, 'name': 'Lexonia Pro Clean', 'publisher': {'@id': BIZ_ID}, 'inLanguage': 'en-US'})
    else:
        graph.append(business_ld(False))
    kind = 'ContactPage' if name == 'contact.html' else 'WebPage'
    wp = {'@type': kind, '@id': url + '#webpage', 'url': url, 'name': p['title'], 'description': p['desc'], 'isPartOf': {'@id': SITE + '#website'}, 'about': {'@id': BIZ_ID},
          'primaryImageOfPage': {'@type': 'ImageObject', 'url': SITE + OG_IMG, 'width': 1200, 'height': 630}, 'inLanguage': 'en-US', 'dateModified': BUILD_DATE}
    graph.append(wp)
    if name != 'index.html': graph.append(crumbs(name, p['title'].split(' | ')[0]))
    if name == 'services.html':
        for n, d in SERVICES_LD:
            graph.append({'@type': 'Service', 'name': n, 'serviceType': n, 'description': d, 'provider': {'@id': BIZ_ID}, 'areaServed': AREA_LD})
        for img, title in [('lexonia-pro-clean-break-room-island-before-and-after.jpg', 'Break room island, before and after cleaning'),
                           ('lexonia-pro-clean-break-room-counter-before-and-after.jpg', 'Break room counter, before and after cleaning'),
                           ('lexonia-pro-clean-sink-area-before-and-after.jpg', 'Sink area, before and after cleaning'),
                           ('lexonia-pro-clean-sink-detail-before-and-after.jpg', 'Sink detail, before and after cleaning'),
                           ('lexonia-pro-clean-janitorial-caddy-supplies.jpg', 'Janitorial caddy stocked with cleaning supplies'),
                           ('lexonia-pro-clean-cleaning-cart-and-vacuum.jpg', 'Cleaning cart with mop bucket and vacuum')]:
            w, h = SIZES[img]
            graph.append({'@type': 'ImageObject', 'contentUrl': SITE + 'img/' + img, 'name': title + ' | Lexonia Pro Clean', 'caption': title + ', Lexonia Pro Clean commercial cleaning',
                          'width': w, 'height': h, 'creator': {'@id': BIZ_ID}, 'creditText': 'Lexonia Pro Clean', 'copyrightNotice': '© 2026 Lexonia Pro Clean LLC'})
    graph.extend(p.get('ld_extra', []))
    if name == 'how-it-works.html':
        graph.append({'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]})
    return '<script type="application/ld+json">\n' + _json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1) + '\n</script>\n'

def seo_head(name, p):
    if p.get('noindex'): return '<meta name="robots" content="noindex">\n'
    url = SITE + p.get('path', '')
    t, d = p['title'], p['desc']
    import html as _h
    t, d = _h.escape(t, quote=True), _h.escape(d, quote=True)
    return ('<link rel="canonical" href="%s">\n<meta name="robots" content="index, follow, max-image-preview:large">\n'
            '<meta property="og:type" content="website">\n<meta property="og:site_name" content="Lexonia Pro Clean">\n<meta property="og:locale" content="en_US">\n'
            '<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n<meta property="og:url" content="%s">\n'
            '<meta property="og:image" content="%s">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            '<meta property="og:image:alt" content="Break room island before and after cleaning by Lexonia Pro Clean">\n'
            '<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="%s">\n<meta name="twitter:description" content="%s">\n<meta name="twitter:image" content="%s">\n'
            '<meta name="theme-color" content="#0b2545">\n<meta name="geo.region" content="US-MN">\n<meta name="geo.placename" content="Eden Prairie">\n'
            % (url, t, d, url, SITE + OG_IMG, t, d, SITE + OG_IMG))

def render(name, p):
    body = header(p['active']) + p['body'] + footer()
    ld = '' if p.get('noindex') else page_ld(name, p)
    scripts = ld + ('<script>window.LPC_PREVIEW=true;</script>\n' if PREVIEW else '') + '<script src="site.js" defer></script>\n' + p.get('scripts', '')
    meta = '<meta name="description" content="%s">\n' % p['desc'].replace('"', '&quot;')
    meta += seo_head(name, p)
    icons = ('<link rel="icon" type="image/svg+xml" href="icon.svg">\n<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">\n'
             '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n')
    if PREVIEW and name == 'index.html':
        # main page of the Artifact: wrapped in a skeleton at publish time, so no doctype/html/head/body
        return '<title>%s</title>\n%s<link rel="stylesheet" href="styles.css">\n%s%s' % (p['title'].replace('&', '&amp;'), FONTS, body, scripts)
    head = ('<!DOCTYPE html>\n<html lang="en-US">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '<title>%s</title>\n%s%s%s<link rel="stylesheet" href="styles.css">\n</head>\n<body>\n'
            % (p['title'].replace('&', '&amp;'), meta, icons, FONTS))
    return head + body + scripts + '</body>\n</html>\n'

for name, p in pages.items():
    open(os.path.join(out, name), 'w', encoding='utf-8').write(render(name, p))

import re as _re_links
def root_links(doc):
    # pages below the site root (blog/...): every site link, image and photo list must start at the root
    doc = _re_links.sub(r'(href|src)="(?!https?:|mailto:|tel:|/|#|data:)', r'\1="/', doc)
    doc = _re_links.sub(r'srcset="([^"]*)"', lambda m: 'srcset="' + ', '.join(c if c.startswith(('/', 'http')) else '/' + c for c in m.group(1).split(', ')) + '"', doc)
    doc = _re_links.sub(r'data-slides="([^"]*)"', lambda m: 'data-slides="' + ','.join(u if u.startswith('/') else '/' + u for u in m.group(1).split(',')) + '"', doc)
    return doc

def render_page(p):
    # blog pages: same header, footer, styles and scripts as the rest of the site, with their own structured data and link-card image
    import html as _h
    url = SITE + p['path']
    t, d = _h.escape(p['title'], quote=True), _h.escape(p['desc'], quote=True)
    og_url, ow, oh, oalt = p['og_img'] if p.get('og_img') else (SITE + OG_IMG, 1200, 630, 'Break room island before and after cleaning by Lexonia Pro Clean')
    meta = '<meta name="description" content="%s">\n' % d
    meta += ('<link rel="canonical" href="%s">\n<meta name="robots" content="index, follow, max-image-preview:large">\n'
             '<meta property="og:type" content="%s">\n<meta property="og:site_name" content="Lexonia Pro Clean">\n<meta property="og:locale" content="en_US">\n'
             '<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n<meta property="og:url" content="%s">\n'
             '<meta property="og:image" content="%s">\n<meta property="og:image:width" content="%d">\n<meta property="og:image:height" content="%d">\n'
             '<meta property="og:image:alt" content="%s">\n'
             '<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="%s">\n<meta name="twitter:description" content="%s">\n<meta name="twitter:image" content="%s">\n'
             '<meta name="theme-color" content="#0b2545">\n<meta name="geo.region" content="US-MN">\n<meta name="geo.placename" content="Eden Prairie">\n'
             % (url, p.get('og_type', 'website'), t, d, url, og_url, ow, oh, _h.escape(oalt, quote=True), t, d, og_url))
    if p.get('published'):
        meta += '<meta property="article:published_time" content="%s">\n' % p['published']
    meta += '<link rel="alternate" type="application/rss+xml" title="Lexonia Pro Clean guides" href="%sblog/feed.xml">\n' % SITE
    icons = ('<link rel="icon" type="image/svg+xml" href="icon.svg">\n<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">\n'
             '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n')
    ld = '<script type="application/ld+json">\n' + _json.dumps({'@context': 'https://schema.org', '@graph': p['ld']}, ensure_ascii=False, indent=1) + '\n</script>\n'
    head = ('<!DOCTYPE html>\n<html lang="en-US">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '<title>%s</title>\n%s%s%s<link rel="stylesheet" href="styles.css">\n</head>\n<body>\n' % (p['title'].replace('&', '&amp;'), meta, icons, FONTS))
    return head + header(p['active']) + p['body'] + footer() + ld + '<script src="site.js" defer></script>\n</body>\n</html>\n'


# ---- crawl files (live site only)
if not PREVIEW:
    import datetime
    today = BUILD_DATE
    notfound = dict(title='Page Not Found | Lexonia Pro Clean', desc='That page was not found.', active='', noindex=True, path='404.html',
        body=('<main id="top">\n' + page_hero('404', 'Page Not Found', 'That page does not exist. Try one of the pages below or get in touch.')
              + '<section>\n  <div class="container center"><p><a href="index.html" class="btn btn-primary">Back to the Home Page</a> '
              '<a href="contact.html" class="btn btn-ghost">Contact Us</a></p></div>\n</section>\n</main>\n'))
    import re as _re
    nf = render('404.html', notfound)
    nf = _re.sub(r'(href|src)="(?!https?:|mailto:|tel:|/|#|data:)', r'\1="/', nf)   # a 404 page is served at any missing URL, so its links must be root-relative
    open(os.path.join(out, '404.html'), 'w', encoding='utf-8').write(nf)
    open(os.path.join(out, 'robots.txt'), 'w', encoding='utf-8').write(
        'User-agent: *\nAllow: /\nDisallow: /img/pricing/\n\nSitemap: %ssitemap.xml\n' % SITE)
    open(os.path.join(out, INDEXNOW_KEY + '.txt'), 'w', encoding='utf-8').write(INDEXNOW_KEY)   # IndexNow ownership check
    imgs = {'': [(i[0], i[2]) for i in LOOP[:8]],
            'services.html': [('img/lexonia-pro-clean-break-room-island-before-and-after.jpg', 'Break room island, before and after cleaning'),
                              ('img/lexonia-pro-clean-break-room-counter-before-and-after.jpg', 'Break room counter, before and after cleaning'),
                              ('img/lexonia-pro-clean-sink-area-before-and-after.jpg', 'Sink area, before and after cleaning'),
                              ('img/lexonia-pro-clean-sink-detail-before-and-after.jpg', 'Sink detail, before and after cleaning'),
                              ('img/lexonia-pro-clean-janitorial-caddy-supplies.jpg', 'Janitorial caddy stocked with cleaning supplies'),
                              ('img/lexonia-pro-clean-cleaning-cart-and-vacuum.jpg', 'Cleaning cart with mop bucket and vacuum')]}
    POSTS = BLOG.build(out, here, dict(SITE=SITE, BIZ_ID=BIZ_ID, business_ld=business_ld, page_hero=page_hero, cta_band=cta_band,
                                       render_page=render_page, root_links=root_links))
    import html as _h2
    urls = ''
    for n in ['index.html', 'services.html'] + SP.NAMES + ['why-us.html', 'how-it-works.html', 'contact.html', 'privacy.html']:
        path = pages[n]['path']
        im = ''.join('    <image:image><image:loc>%s%s</image:loc><image:caption>%s, Lexonia Pro Clean</image:caption></image:image>\n' % (SITE, i, _h2.escape(c)) for i, c in imgs.get(path, []))
        urls += '  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n%s  </url>\n' % (SITE, path, today, im)
    if POSTS:
        urls += '  <url>\n    <loc>%sblog/</loc>\n    <lastmod>%s</lastmod>\n  </url>\n' % (SITE, max(p['date'] for p in POSTS))
        for _p in POSTS:
            urls += '  <url>\n    <loc>%sblog/%s/</loc>\n    <lastmod>%s</lastmod>\n  </url>\n' % (SITE, _p['slug'], _p.get('updated', _p['date']))
    open(os.path.join(out, 'sitemap.xml'), 'w', encoding='utf-8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + urls + '</urlset>\n')
    llms = ('# Lexonia Pro Clean\n\n'
        '> Commercial cleaning and janitorial services for offices and small retail stores across Minneapolis, St. Paul and the Twin Cities suburbs, based in Eden Prairie, Minnesota. Insured, background-checked crews, a written checklist every visit, evenings and nights.\n\n'
        'Lexonia Pro Clean LLC is based in Eden Prairie, MN and serves the Twin Cities metro. If a business is just outside the metro, it can still ask.\n\n'
        '## Key facts\n\n'
        '- Who we serve: offices and small retail stores and boutiques.\n'
        '- Where: based in Eden Prairie, serving Minneapolis, St. Paul and the suburbs: ' + ', '.join(CITIES[2:]) + '. A business just outside the metro can still ask.\n'
        '- Cleaning hours: ' + HOURS_TEXT + '.\n'
        '- What we do: recurring commercial cleaning on a written checklist, with a completed copy left on site after every visit. Restrooms, break rooms, workspaces, common areas, conference rooms, sales floors, mirrors and fitting rooms.\n'
        '- When: evenings and nights, when the business is closed.\n'
        '- Pricing: a free walkthrough, then a written scope and an exact price within 24 hours. No surprise fees and no travel charges. Recurring cleaning up to 10,000 sq ft is priced per visit by size of space, weekly or every other week, before sales tax: from $' + str(PRICE_FROM) + ' per visit for 1,000 to 2,000 sq ft, weekly; the full price card is on the Services page. Interior windows are an add-on, priced by the number of windows: ' + ', '.join('$%d for %s' % (p, n.replace('–', ' to ')) for n, p in WIN_ROWS) + ', before sales tax. Daily cleaning, or a space over 10,000 sq ft: a flat monthly contract quoted after the walkthrough. Multi-story buildings: custom pricing, at greater discounts. For an exact price, request a free quote.\n'
        '- Process: a free walkthrough of about 45 to 60 minutes, a written scope and exact price within 24 hours, then recurring cleaning. The first visit is a reset clean, recurring visits maintain it, and we check in after two weeks and adjust the scope until it fits.\n'
        '- Supplies: we bring the cleaning liquids and our own equipment, all included in the price.\n'
        '- Consumables: the client\'s company or building management supplies trash bags, soap, paper towels, tissue and restroom disposal bags. We do not supply or buy them. We restock them from the client\'s supply and say when something is running low.\n'
        '- Multi-story buildings: we can clean a different floor, or two floors, each night, so the whole building is cleaned once every 1-2 weeks, depending on what it needs. Custom pricing, at greater discounts.\n'
        '- Interior windows can be added to a visit.\n'
        '- Not included: operating or maintaining machines, moving furniture, equipment or paperwork, biohazard, hoarding or post-construction cleanup.\n'
        '- Insured and background-checked crews. Every message gets a same-day response.\n\n'
        '## Contact\n\n'
        '- Phone: %s\n- Email: %s\n- Website: %s\n\n'
        '## Pages\n\n'
        '- [Services](%sservices.html): what is cleaned every visit, multi-story buildings, photos.\n'
        + ''.join('- [%s](' % t + SITE + h + ')\n' for h, t in SP.LINKS) +
        '- [Why Us](%swhy-us.html): how Lexonia Pro Clean works, customer reviews.\n'
        '- [How It Works](%show-it-works.html): the process from first call to first clean, and frequently asked questions.\n'
        '- [Contact](%scontact.html): free quote request.\n'
        '- [Blog](%sblog/): guides for office and store managers: cleaning scope, frequency, pricing.\n') % (PHONE, EMAIL, SITE, SITE, SITE, SITE, SITE, SITE)
    llms += '\n## Official profiles\n\n' + ''.join('- %s\n' % u for u in SAME_AS)
    if POSTS:
        llms += '\n## Blog articles\n\n' + ''.join('- [%s](%sblog/%s/): %s\n' % (_p['title'], SITE, _p['slug'], _p['description']) for _p in POSTS)
    open(os.path.join(out, 'llms.txt'), 'w', encoding='utf-8').write(llms)

# ------------------------------------------------------------------ css + js
base = open(os.path.join(here, 'base.css'), encoding='utf-8').read()
extra = '''
/* ---- multi-page additions ---- */
.hero-art{max-width:100%}
.loop{background:#fff;border-radius:20px;box-shadow:0 24px 60px rgba(0,0,0,.35);overflow:hidden;border:1px solid rgba(255,255,255,.25);max-width:430px;margin-inline:auto}
.loop-frame{position:relative;aspect-ratio:4/5;background:var(--navy)}
.loop-frame img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;z-index:1;transition:opacity 0s linear var(--fade,1s)}
.loop-frame img.on{opacity:1;z-index:2;transition:opacity var(--fade,1s) ease-in-out}
/* overlap: the next picture fades in on top while the old one stays fully visible underneath, then the old one is dropped */
.loop-bar{position:relative;display:flex;align-items:center;justify-content:center;padding:12px 52px;background:#fff}
.loop-pause{position:absolute;right:6px;top:50%;transform:translateY(-50%);width:44px;height:44px;border-radius:50%;border:1px solid var(--line);background:#fff;color:var(--navy);display:flex;align-items:center;justify-content:center;cursor:pointer;padding:0}
.loop-pause:hover{border-color:var(--teal);color:var(--teal)}
.loop-pause .i-play{display:none}
.loop-pause[aria-pressed="true"] .i-play{display:block}
.loop-pause[aria-pressed="true"] .i-pause{display:none}
.loop-cap{font-size:.92rem;font-weight:700;color:var(--navy);letter-spacing:.01em}
.multi{background:#fff;border:1px solid var(--line);border-left:6px solid var(--teal);border-radius:var(--radius);box-shadow:var(--shadow-sm);padding:32px 36px;text-align:left;display:grid;grid-template-columns:1.15fr 1fr;gap:28px 40px;align-items:center}
.multi h2,.multi h3{margin:0 0 10px;font-family:'Sora',sans-serif;color:var(--navy);font-size:1.5rem;line-height:1.25}
.multi p{margin:0;color:var(--muted)}
.multi ul{margin:0;padding:0;list-style:none;display:grid;gap:12px}
.multi li{position:relative;padding-left:28px;color:var(--navy);font-weight:600}
.multi li:before{content:"";position:absolute;left:0;top:.35em;width:14px;height:14px;border-radius:50%;background:var(--teal)}
.multi .btn{margin-top:18px}
@media (max-width:820px){.multi{grid-template-columns:1fr;padding:26px 22px}}
.facts{background:var(--sky-2);padding:8px 0 0}
.facts-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.fact{background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px 20px;text-align:center;box-shadow:var(--shadow-sm)}
.fact strong{display:block;font-family:'Sora',sans-serif;font-size:1.1rem;color:var(--navy)}
.fact span{color:var(--muted);font-size:.85rem}
@media (max-width:680px){.facts-grid{grid-template-columns:1fr 1fr}}
.has-slides{position:relative;overflow:hidden}
.hero-slides{position:absolute;inset:0;z-index:0}
.hero-slides img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;z-index:1;transition:opacity 0s linear 1.6s}
.hero-slides img.on{opacity:1;z-index:2;transition:opacity 1.6s ease}
.has-slides::before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(160deg,rgba(11,37,69,.86) 0%,rgba(19,49,92,.80) 55%,rgba(20,72,107,.74) 100%)}
.has-slides .bubbles{z-index:1}
.has-slides .hero-grid,.has-slides>.container{position:relative;z-index:3}
.has-slides .wave{z-index:3}

.music-btn{position:fixed;right:18px;bottom:18px;z-index:300;display:flex;align-items:center;gap:9px;background:var(--navy);color:#fff;border:1px solid rgba(255,255,255,.18);border-radius:999px;padding:11px 18px 11px 14px;font-family:'Sora',sans-serif;font-weight:600;font-size:.85rem;cursor:pointer;box-shadow:0 8px 22px rgba(11,37,69,.28);transition:transform .18s ease,background .18s ease}
.music-btn:hover{transform:translateY(-2px);background:var(--navy-2)}
.music-btn svg{color:var(--cyan);flex:none}
.music-btn .eq{display:none;gap:2px;align-items:flex-end;height:14px}
.music-btn[aria-pressed="true"] .eq{display:flex}
.music-btn[aria-pressed="true"] .note{display:none}
.eq i{display:block;width:3px;height:12px;background:var(--cyan);border-radius:2px;transform-origin:bottom;animation:eq 1s ease-in-out infinite}
.eq i:nth-child(2){animation-delay:.2s}.eq i:nth-child(3){animation-delay:.4s}
@keyframes eq{0%,100%{transform:scaleY(.35)}50%{transform:scaleY(1)}}
@media (prefers-reduced-motion:reduce){.eq i{animation:none}}
@media (max-width:560px){.music-btn{right:12px;bottom:12px;padding:10px 14px 10px 12px}}
.nav-links a.active{color:var(--teal);font-weight:600}
.page-hero{background:linear-gradient(160deg,var(--navy) 0%,var(--navy-2) 55%,#14486b 100%);color:#fff;padding:72px 0 64px}
.page-hero .kicker{color:var(--cyan)}
.page-hero h1{color:#fff;font-size:clamp(2rem,4.2vw,3rem);margin-bottom:14px;max-width:760px}
.page-hero p.lead{color:#c9d9e6;font-size:1.1rem;max-width:640px}
.more{margin-top:40px}
.hero-stat{gap:14px}
.gallery{display:grid;gap:22px;margin-top:44px}
.gallery.two{grid-template-columns:repeat(2,1fr)}
.gallery.three{grid-template-columns:repeat(3,1fr)}
.gallery figure{margin:0;background:#fff;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow-sm);text-align:left}
.gallery img{width:100%;height:auto;display:block}
.gallery.three img{aspect-ratio:3/4;object-fit:cover;object-position:center 55%}
.gallery-sub{margin-top:48px;font-size:1.15rem}
.gallery figcaption{padding:12px 16px;font-size:.88rem;color:var(--muted)}
.incl{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:44px;text-align:left}
.incl.two{grid-template-columns:repeat(2,1fr);max-width:900px;margin-left:auto;margin-right:auto}
.incl .box{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:26px}
.incl h3{font-size:1.02rem;margin-bottom:12px}
.incl ul,.notbox ul{list-style:none;display:flex;flex-direction:column;gap:8px}
.incl li{color:var(--muted);font-size:.92rem;padding-left:26px;position:relative}
.incl li::before{content:"";position:absolute;left:2px;top:.45em;width:12px;height:7px;border-left:2px solid var(--teal);border-bottom:2px solid var(--teal);transform:rotate(-45deg)}
.notbox{margin-top:34px;background:var(--sky-2);border:1px solid var(--line);border-radius:var(--radius);padding:28px 30px;text-align:left}
.notbox h3{font-size:1.05rem;margin-bottom:12px}
.notbox li{color:var(--muted);font-size:.92rem;padding-left:20px;position:relative}
.notbox li::before{content:"—";position:absolute;left:0;color:var(--teal)}
.notbox p{margin-top:16px;color:var(--muted);font-size:.92rem}
.reviews{background:var(--sky-2)}
.review-list{display:grid;gap:24px;margin-top:40px;grid-template-columns:repeat(3,1fr);align-items:start}
@media (max-width:960px){.review-list{grid-template-columns:1fr;max-width:640px;margin-left:auto;margin-right:auto}}
.review-card{margin:0;background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:32px;text-align:left;box-shadow:var(--shadow-sm)}
.review-card .stars{color:#f6b93b;display:flex;gap:3px;margin-bottom:14px}
.review-card blockquote p{font-size:1.05rem;color:var(--ink);margin-bottom:18px}
.review-card figcaption{font-size:.9rem;color:var(--navy)}
.review-card figcaption span{color:var(--muted);font-size:.82rem}
.cta-section{padding:64px 0}
.cta-band{display:flex;align-items:center;justify-content:space-between;gap:28px;flex-wrap:wrap;background:linear-gradient(135deg,var(--sky),#e2f4f6);border:1px solid var(--line);border-radius:20px;padding:36px 40px}
.cta-band h3{font-size:1.35rem;margin-bottom:6px}
.cta-band p{color:var(--muted);max-width:520px}
/* ---- phones first: tabs always visible, card in view, big tap targets ---- */
@media (max-width:1100px){
  header{position:static}
  .nav{flex-wrap:wrap;height:auto;padding-top:8px;padding-bottom:0;row-gap:0}
  .nav nav{order:3;flex:0 0 100%;width:100%;min-width:0;max-width:100%}
  .nav-links{display:flex;position:static;overflow-x:auto;gap:4px;padding:2px 0 8px;margin:0 -6px;background:none;box-shadow:none;border:0;scrollbar-width:none;-webkit-overflow-scrolling:touch}
  .nav-links::-webkit-scrollbar{display:none}
  .nav-links li{flex:none}
  .nav-links a{display:block;padding:11px 14px;border-radius:999px;line-height:22px}
  .nav-links a.active{background:var(--sky);color:var(--teal-dark)}
  .menu-btn{display:none}
}
@media (min-width:821px) and (max-width:960px){.hero-grid{grid-template-columns:1.1fr .9fr;gap:28px}.hero-art{max-width:none}}
@media (max-width:820px){
  .hero-grid{display:flex;flex-direction:column;gap:0}
  .hero-grid>div:first-child{display:contents}
  .hero-grid .kicker{order:1;align-self:flex-start}
  .hero-grid h1{order:2}
  .hero-grid .lead{order:3}
  .hero-art{order:4;width:100%;max-width:330px;margin:6px auto 26px}
  .hero-grid .hero-actions{order:5}
  .hero-grid .trust-row{order:6}
}
@media (max-width:720px){
  .hero{padding:34px 0 56px}
  .hero h1{font-size:clamp(1.85rem,8.2vw,2.35rem);margin-bottom:12px}
  .hero p.lead{font-size:1.02rem;margin-bottom:18px}
  .hero-grid .kicker{margin-bottom:10px}
  .hero-art{margin:0 auto 22px}
}
.mbar{display:none}
@media (max-width:720px){
  .mbar{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:250;gap:10px;padding:10px 14px calc(10px + env(safe-area-inset-bottom));background:rgba(255,255,255,.97);border-top:1px solid var(--line);box-shadow:0 -6px 20px rgba(11,37,69,.10)}
  .mbar a{flex:1;display:flex;align-items:center;justify-content:center;gap:8px;min-height:48px;border-radius:12px;font-weight:700;font-family:'Sora',sans-serif;font-size:1rem;color:#fff}
  .mbar-call{background:var(--navy)}
  .mbar-quote{background:linear-gradient(135deg,var(--teal),var(--cyan))}
  body{padding-bottom:76px}
  .music-btn{bottom:84px !important}
  footer.site{padding-bottom:88px}   /* the Music button sits above the call bar; keep the copyright line clear of it */
  .btn{min-height:46px}
  .field input,.field select,.field textarea{font-size:16px}
  .nav .btn{min-height:40px}
}
.faq{padding:72px 0}
.faq-list{max-width:820px;margin:28px auto 0;display:grid;gap:12px;text-align:left}
.faq-item{background:#fff;border:1px solid var(--line);border-radius:14px;padding:0 20px}
.faq-item summary{cursor:pointer;list-style:none;padding:16px 30px 16px 0;font-weight:600;color:var(--navy);position:relative;min-height:44px}
.faq-item summary::-webkit-details-marker{display:none}
.faq-item summary:after{content:"+";position:absolute;right:0;top:50%;transform:translateY(-50%);font-size:1.5rem;color:var(--teal);line-height:1}
.faq-item[open] summary:after{content:"\2212"}
.faq-item p{margin:0 0 18px;color:var(--muted)}
footer.site address{font-style:normal}
.cta-actions{display:flex;gap:14px;flex-wrap:wrap}
.quote .section-title{font-size:clamp(1.7rem,3.4vw,2.4rem)}
@media (max-width:960px){.gallery.three,.incl{grid-template-columns:1fr 1fr}}
@media (max-width:680px){.gallery.two,.gallery.three,.incl,.incl.two{grid-template-columns:1fr}.page-hero{padding:56px 0 48px}.cta-band{padding:28px 24px}}
'''
FONT_CSS = ("@font-face{font-family:'Sora';font-style:normal;font-weight:100 800;font-display:swap;src:url(fonts/sora-latin-wght-normal.woff2) format('woff2-variations'),url(fonts/sora-latin-wght-normal.woff2) format('woff2');"
            "unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}\n"
            "@font-face{font-family:'Inter';font-style:normal;font-weight:100 900;font-display:swap;src:url(fonts/inter-latin-wght-normal.woff2) format('woff2-variations'),url(fonts/inter-latin-wght-normal.woff2) format('woff2');"
            "unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}\n")
os.makedirs(os.path.join(out, 'fonts'), exist_ok=True)
for _f in ('sora-latin-wght-normal.woff2', 'inter-latin-wght-normal.woff2'):
    shutil.copyfile(os.path.join(here, 'fonts_src', _f), os.path.join(out, 'fonts', _f))
open(os.path.join(out, 'styles.css'), 'w', encoding='utf-8').write(FONT_CSS + base + extra + DH.HOW_CSS + BL.BLOCKS_CSS + BLOG.BLOG_CSS + SOCIAL_CSS + PV.CSS + SP.CSS)
js = '''// Mobile menu
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
'''
# The owner's own browsers are not recorded in Clarity (owner decision, Oct 19 2026). Each entry is the Clarity visitor ID of one of his
# browsers (Clarity's own first-party cookie): 1kx91bs = his Chrome, 150xde1 = the Claude browser on his computer.
# A new browser, a phone or cleared cookies gets a new ID: add it here. A matching browser also gets a 400-day marker cookie,
# renewed on every visit, so the exclusion holds after Clarity's own cookie expires.
OWNER_CLARITY_IDS = ['1kx91bs', '150xde1']
clarity_js = ('' if PREVIEW else
    "// Microsoft Clarity (visitor analytics): official snippet, served from this file so the page needs no inline script\n"
    "// The owner's own browsers are skipped (their Clarity visitor IDs are listed in the site generator)\n"
    "(function(){var d=document,own=%s,m=d.cookie.match(/(?:^|; )_clck=([^;]+)/),id=m?decodeURIComponent(m[1]).split(/[|^]/)[0]:'';"
    "if(own.indexOf(id)>-1||/(?:^|; )lpc_owner=1/.test(d.cookie)){d.cookie='lpc_owner=1; max-age=34560000; path=/; secure; samesite=lax';return;}\n"
    "(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};"
    "t=l.createElement(r);t.async=1;t.src=\"https://www.clarity.ms/tag/\"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})"
    "(window, document, \"clarity\", \"script\", \"%s\");})();\n" % (_json.dumps(OWNER_CLARITY_IDS), CLARITY_ID))
if not PREVIEW: js = js.replace("new Audio('audio/summerhill.mp3')", "new Audio('/audio/summerhill.mp3')")   # blog pages sit below the root
open(os.path.join(out, 'site.js'), 'w', encoding='utf-8').write(clarity_js + js)
import re as _re_ph
PHONE_LD = '+1-' + PHONE[1:4] + '-' + PHONE[6:]   # schema.org form of PHONE, e.g. +1-952-697-4226
# Guard: Thumbtack appears ONLY as the footer Contact icon (owner decision, Oct 14 2026); nowhere else
for _root, _d, _fs in os.walk(out):
    for _f in _fs:
        if _f.lower().endswith(('.html', '.js', '.css', '.txt', '.xml', '.toml', '.json', '.svg')):
            _t = open(os.path.join(_root, _f), encoding='utf-8', errors='ignore').read()
            _t_nolink = _t.replace(TT_LINK, '')
            assert 'thumbtack' not in _t_nolink.lower(), 'Thumbtack mention found in ' + _f + ' (only the footer Contact link is allowed)'
            if _f.lower().endswith('.html') and _f not in ('404.html',) and 'footer' in _t:
                assert _t.count('Find us on Thumbtack') == 1, 'footer Thumbtack link missing or duplicated in ' + _f
            assert 'service-area' not in _t.lower(), 'Service Area reference found in ' + _f
            # Guard: PHONE is the business phone (changed Oct 20 2026). Any other number anywhere on the site fails the build,
            # so a copy that was not updated (meta description, schema telephone, a page text) cannot go live.
            for _p in set(_re_ph.findall(r'\(\d{3}\) \d{3}-\d{4}', _t)) | set(_re_ph.findall(r'\+1-?\d{3}-?\d{3}-?\d{4}', _t)):
                assert _p in (PHONE, TEL[4:], PHONE_LD), 'phone number other than PHONE found in ' + _f + ': ' + _p
if not PREVIEW:
    # prices.json: the price card as data, read by the Make quote-form auto-reply (owner go Oct 20 2026). Built from PRICE_ROWS,
    # the same list the price-card images are drawn from, so the email and the card cannot disagree. Index = ceil(sq ft / 1000), 1..10;
    # each band includes its top edge (2,000 sq ft = the 1,000-2,000 price). Under 1,000 or over 10,000 sq ft: no table price.
    _bands = [PRICE_ROWS[0]] + PRICE_ROWS
    _prices = {'updated': BUILD_DATE, 'per': 'visit, plus sales tax', 'min_sqft': 1000, 'max_sqft': 10000, 'from': PRICE_FROM,
               'band': [b[0].replace(' ', '') for b in _bands], 'weekly': [b[1] for b in _bands], 'every_other_week': [b[2] for b in _bands],
               'windows': [{'windows': n, 'price': p} for n, p in WIN_ROWS]}
    assert len(_prices['weekly']) == 10 and all(100 <= v < 2000 for v in _prices['weekly'] + _prices['every_other_week']), 'prices.json out of range'
    open(os.path.join(out, 'prices.json'), 'w', encoding='utf-8').write(_json.dumps(_prices, ensure_ascii=False, indent=1))
if not PREVIEW:
    # Guard: Google Search Console verification file must be served (removing it un-verifies the URL-prefix property)
    assert os.path.exists(os.path.join(out, 'google49b64558210859aa.html')), 'Search Console verification file missing from the build'
    # Guard: change ledger (seo/changes.csv). Every change to a page's title, description or main text is recorded, 28 days apart
    LEDGER.check(out, os.path.join(here, '..', 'seo', 'changes.csv'))
print('built', MODE, sorted(os.listdir(out)))
