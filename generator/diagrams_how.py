# Process maps and flow-charts for the How It Works page (HTML + CSS only: text stays readable by search engines,
# and the same markup is a horizontal map on desktop and a vertical flow on phones).

def _svg(path, size=22):
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (size, size, path))

ICON = {
    'chat':   _svg('<path d="M21 15a2 2 0 0 1-2 2H8l-5 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><line x1="8" y1="9" x2="16" y2="9"/><line x1="8" y1="13" x2="13" y2="13"/>'),
    'reply':  _svg('<polyline points="9 17 4 12 9 7"/><path d="M20 18v-2a4 4 0 0 0-4-4H4"/>'),
    'walk':   _svg('<path d="M3 21h18"/><path d="M5 21V8l7-5 7 5v13"/><rect x="9" y="12" width="6" height="9"/>'),
    'doc':    _svg('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="14" y2="17"/>'),
    'yes':    _svg('<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>'),
    'moon':   _svg('<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>'),
    'cart':   _svg('<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.7 11.4a2 2 0 0 0 2 1.6h8.1a2 2 0 0 0 2-1.5L22 7H6"/>'),
    'list':   _svg('<rect x="5" y="3" width="14" height="18" rx="2"/><polyline points="9 9 10.5 10.5 13 8"/><line x1="9" y1="15" x2="15" y2="15"/>'),
    'box':    _svg('<path d="M21 8l-9-5-9 5v8l9 5 9-5z"/><polyline points="3 8 12 13 21 8"/><line x1="12" y1="13" x2="12" y2="21"/>'),
    'copy':   _svg('<rect x="8" y="8" width="13" height="13" rx="2"/><path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3"/>'),
    'drop':   _svg('<path d="M12 2.5S5 10 5 14.5a7 7 0 0 0 14 0C19 10 12 2.5 12 2.5z"/>'),
    'cal':    _svg('<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>'),
    'build':  _svg('<rect x="4" y="3" width="16" height="18" rx="1"/><line x1="9" y1="7" x2="9" y2="7.01"/><line x1="15" y1="7" x2="15" y2="7.01"/><line x1="9" y1="11" x2="9" y2="11.01"/><line x1="15" y1="11" x2="15" y2="11.01"/><rect x="10" y="15" width="4" height="6"/>'),
}

# ----------------------------------------------------------------------------- 1. process map: who does what, step by step
# (who, icon, title, text); who: you | us | both
SWIM = [
    ('you',  'chat',  'Ask for a quote', 'Use the quote form, call, or email us. Share your square footage and schedule.'),
    ('us',   'reply', 'We reply the same day', 'Every message gets a same-day response.'),
    ('both', 'walk',  'Free walkthrough', 'About 45 to 60 minutes at your space. We go over what needs to be cleaned and how often.'),
    ('us',   'doc',   'Written scope and price', 'Within 24 hours. Cleaning liquids and equipment included, no surprise fees.'),
    ('you',  'yes',   'You say yes', 'You confirm the scope and the schedule.'),
    ('us',   'moon',  'Cleaning starts', 'Evenings and nights, on your written checklist. The first visit is a reset clean.'),
]
WHO = {'you': 'You', 'us': 'Us', 'both': 'Together'}


def swimlane():
    steps = []
    for k, (who, ic, title, text) in enumerate(SWIM):
        steps.append('    <li class="pm-step pm-%s"><div class="pm-rail" aria-hidden="true"><i></i><span class="pm-n">%d</span><i></i></div>'
                     '<div class="pm-card"><div class="pm-top"><span class="sw-ic">%s</span><span class="pm-who">%s</span></div><h3>%s</h3><p>%s</p></div></li>'
                     % (who, k + 1, ICON[ic], WHO[who], title, text))
    return ('<div class="pmap-wrap reveal" role="group" aria-label="Process map: who does what, from first call to first clean">\n'
            '  <p class="pm-legend" aria-hidden="true"><span class="lg-you">You</span><span class="lg-us">Us (Lexonia Pro Clean)</span><span class="lg-both">Together</span></p>\n'
            '  <ol class="pmap">\n' + '\n'.join(steps) + '\n  </ol>\n'
            '</div>')


# ----------------------------------------------------------------------------- 2. every visit + who supplies what (one section, two panels)
VISIT = [
    ('moon', 'We arrive after hours', 'Evenings and nights, when your business is closed.'),
    ('list', 'We work the checklist', 'Restrooms, break rooms, workspaces and common areas. For retail: sales floor, mirrors and fitting rooms.'),
    ('box',  'We restock', 'Consumables come from your supply. We tell you when something is running low.'),
    ('copy', 'Completed checklist left on site', 'A completed copy of the checklist stays with you after every visit.'),
]
BEFORE = ['Desks clear of loose paper where possible', 'Confidential documents put away', 'Access codes, keys or badges current', 'Anything we should not touch flagged in advance']


def visit_prep():
    steps = ''.join('<li><span class="vs-dot">%s</span><h3>%s</h3><p>%s</p></li>' % (ICON[ic], t, x) for ic, t, x in VISIT)
    checks = ''.join('<li>%s</li>' % i for i in BEFORE)
    return ('<div class="vs-grid reveal">\n'
            '  <div class="vs-panel vs-visit">\n    <h2>What Happens at Every Visit</h2>\n'
            '    <p class="vs-sub">The same routine each time, on your written checklist.</p>\n'
            '    <ol class="vs-steps">' + steps + '</ol>\n'
            '    <p class="vs-loop">Same again at the next visit, on your schedule</p>\n  </div>\n'
            '  <div class="vs-panel vs-prep">\n    <h2>Before Your First Visit</h2>\n'
            '    <p class="vs-sub">What helps the first visit go smoothly.</p>\n'
            '    <ul class="vs-checks">' + checks + '</ul>\n  </div>\n'
            '</div>')


def price_flow(link='services.html#pricing'):
    cards = [
        ('a', 'Path A', 'Weekly or every other week', 'Up to 10,000 sq ft.', 'A set price per visit', 'Based on the size of your space. <a href="%s">See the price card</a>.' % link),
        ('b', 'Path B', 'Daily, over 10,000 sq ft, or multi-story', 'Quoted after the free walkthrough.', 'A custom quote', 'Daily or over 10,000 sq ft: a flat monthly contract. Multi-story: custom pricing, at greater discounts.'),
    ]
    cs = ''.join('<div class="pt-card pt-%s"><div class="pt-when"><span class="pt-tag">%s</span><h3>%s</h3><p>%s</p></div>'
                 '<div class="pt-then"><h4>%s</h4><p>%s</p></div></div>' % c for c in cards)
    return ('<div class="pt reveal" role="group" aria-label="Flow chart: how we price">\n'
            '  <div class="pt-q"><span class="sw-ic">%s</span><div><h3>What kind of building, and how often?</h3><p>Tell us at the quote request or the walkthrough.</p></div></div>\n'
            '  <div class="pt-fork" aria-hidden="true"><i></i><i></i></div>\n'
            '  <div class="pt-cards">%s</div>\n'
            '  <div class="pt-join" aria-hidden="true"><i></i><i></i></div>\n'
            '  <div class="pt-end"><span class="sw-ic">%s</span><div><h3>Written scope and exact price</h3><p>Within 24 hours of the free walkthrough. No surprise fees.</p></div></div>\n'
            '</div>' % (ICON['cal'], cs, ICON['doc']))


# ----------------------------------------------------------------------------- 4. multi-story, floor by night
def floors_diagram(floors=5, nights=5):
    head = ''.join('<span class="fl-h">Night %d</span>' % (n + 1) for n in range(nights))
    rows = []
    for f in range(floors, 0, -1):
        cells = ''.join('<span class="fl-c%s"></span>' % (' on' if (n + 1) == f else '') for n in range(nights))
        rows.append('<span class="fl-n">Floor %d</span>%s' % (f, cells))
    return ('<div class="floors" role="img" aria-label="Illustration: a five-floor building cleaned one floor per night, a different floor each night">\n'
            '  <div class="fl-grid" style="--nights:%d"><span></span>%s%s</div>\n'
            '  <p class="fl-note">Illustration: one floor each night. Some buildings can take two floors a night.</p>\n'
            '</div>' % (nights, head, ''.join(rows)))


# ----------------------------------------------------------------------------- css
HOW_CSS = r'''
/* ---- How It Works: process map and flow charts ---- */
:root{--cn:#7fc8d0}
.sw-ic{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:12px;background:var(--sky);color:var(--teal-dark);flex:none}
.sw-ic svg{display:block}

/* ---- 1. process map ---- */
.pmap-wrap{margin-top:26px;text-align:left}
.pm-legend{display:flex;flex-wrap:wrap;gap:6px 20px;justify-content:center;margin:0 0 16px;font-size:.84rem;font-weight:600;color:var(--navy)}
.pm-legend span{display:inline-flex;align-items:center;gap:8px}
.pm-legend span:before{content:"";width:12px;height:12px;border-radius:50%;background:var(--navy)}
.pm-legend .lg-us:before{background:var(--teal)}.pm-legend .lg-both:before{background:var(--cyan)}
.pmap{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(6,minmax(0,1fr))}
.pm-step{display:flex;flex-direction:column;min-width:0}
.pm-rail{display:flex;align-items:center;height:38px}
.pm-rail i{flex:1;height:2px;background:var(--cn);position:relative}
.pm-rail i:first-child:after{content:"";position:absolute;right:-1px;top:-5px;border-left:8px solid var(--cn);border-top:6px solid transparent;border-bottom:6px solid transparent}
.pm-step:first-child .pm-rail i:first-child,.pm-step:last-child .pm-rail i:last-child{visibility:hidden}
.pm-n{flex:none;width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;font:700 .95rem 'Sora',sans-serif;color:#fff;background:var(--navy);box-shadow:0 0 0 4px #fff}
.pm-us .pm-n{background:var(--teal)}.pm-both .pm-n{background:var(--cyan);color:var(--navy)}
.pm-card{flex:1;margin:12px 7px 0;background:#fff;border:1px solid var(--line);border-top:4px solid var(--navy);border-radius:14px;padding:14px 14px 16px;box-shadow:var(--shadow-sm);display:flex;flex-direction:column;gap:8px}
.pm-us .pm-card{border-top-color:var(--teal)}
.pm-both .pm-card{border-top-color:var(--cyan);background:linear-gradient(180deg,#fff,var(--sky-2))}
.pm-top{display:flex;align-items:center;justify-content:space-between;gap:8px}
.pm-who{font-size:.66rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:3px 9px;border-radius:999px;color:#fff;background:var(--navy);white-space:nowrap}
.pm-us .pm-who{background:var(--teal)}.pm-both .pm-who{background:var(--cyan);color:var(--navy)}
.pm-card h3{font-size:1rem;line-height:1.25;margin:0}
.pm-card p{font-size:.86rem;line-height:1.45;color:var(--muted);margin:0}
/* ---- 2. every visit + supplies ---- */
.vs-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:24px;text-align:left;align-items:stretch}
.vs-panel{background:#fff;border:1px solid var(--line);border-radius:18px;padding:26px 28px 28px;box-shadow:var(--shadow-sm)}
.vs-visit{border-top:5px solid var(--teal)}.vs-prep{border-top:5px solid var(--navy)}
.vs-panel h2{font-size:1.4rem;margin:0 0 6px}
.vs-sub{color:var(--muted);font-size:.94rem;margin:0 0 20px}
.vs-visit{display:flex;flex-direction:column}
.vs-steps{list-style:none;margin:0;padding:0;counter-reset:vs;flex:1;display:flex;flex-direction:column}
.vs-steps li{position:relative;padding:0 0 18px 62px;counter-increment:vs;min-height:44px;flex:1 1 auto}
.vs-steps li:last-child{flex:0 0 auto;padding-bottom:0}
.vs-steps li:before{content:"";position:absolute;left:21px;top:48px;bottom:4px;width:2px;background:var(--cn)}
.vs-steps li:last-child:before{display:none}
.vs-dot{position:absolute;left:0;top:0;width:44px;height:44px;border-radius:14px;background:var(--sky);color:var(--teal-dark);display:flex;align-items:center;justify-content:center}
.vs-dot:after{content:counter(vs);position:absolute;right:-7px;top:-7px;width:20px;height:20px;border-radius:50%;background:var(--teal);color:#fff;font:700 .68rem 'Sora',sans-serif;display:flex;align-items:center;justify-content:center}
.vs-steps h3{font-size:1rem;margin:0 0 2px}
.vs-steps p{font-size:.9rem;color:var(--muted);margin:0;line-height:1.45}
.vs-loop{margin:6px 0 0;padding:10px 14px;border:1px dashed var(--cn);border-radius:12px;background:var(--sky-2);font-size:.88rem;font-weight:600;color:var(--teal-dark);text-align:center}
.vs-loop:before{content:"\21BB\00a0\00a0"}
.vs-prep{display:flex;flex-direction:column}
.vs-checks{list-style:none;margin:0;padding:0;flex:1;display:flex;flex-direction:column;gap:12px}
.vs-checks li{flex:1;display:flex;align-items:center;gap:14px;background:var(--sky-2);border:1px solid var(--line);border-radius:14px;padding:12px 18px;font-size:.98rem;font-weight:500;color:var(--ink);line-height:1.4}
.vs-checks li:before{content:"";flex:0 0 26px;height:26px;border-radius:50%;background:var(--teal) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 12.5l4 4 8-9'/%3E%3C/svg%3E") center/16px no-repeat}
/* ---- 3. how we price: decision tree ---- */
.pt{margin-top:28px;text-align:left}
.pt-q,.pt-end{display:flex;align-items:center;gap:16px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px 22px;box-shadow:var(--shadow-sm);max-width:640px;margin:0 auto}
.pt-q{border-top:4px solid var(--navy)}
.pt-end{border-top:4px solid var(--cyan);background:linear-gradient(180deg,#fff,var(--sky-2))}
.pt-q h3,.pt-end h3{font-size:1.08rem;margin:0 0 2px}
.pt-q p,.pt-end p{margin:0;color:var(--muted);font-size:.92rem}
.pt-fork,.pt-join{position:relative;height:44px;max-width:880px;margin:0 auto}
.pt-fork:before{content:"";position:absolute;left:50%;top:0;height:22px;margin-left:-1px;border-left:2px solid var(--cn)}
.pt-fork:after,.pt-join:after{content:"";position:absolute;left:25%;right:25%;top:22px;border-top:2px solid var(--cn)}
.pt-fork i{position:absolute;top:22px;height:22px;margin-left:-1px;border-left:2px solid var(--cn)}
.pt-fork i:nth-child(1),.pt-join i:nth-child(1){left:25%}.pt-fork i:nth-child(2),.pt-join i:nth-child(2){left:75%}
.pt-fork i:after{content:"";position:absolute;left:-6px;bottom:-1px;border-top:8px solid var(--cn);border-left:5px solid transparent;border-right:5px solid transparent}
.pt-join i{position:absolute;top:0;height:22px;margin-left:-1px;border-left:2px solid var(--cn)}
.pt-join:before{content:"";position:absolute;left:50%;top:22px;height:22px;margin-left:-1px;border-left:2px solid var(--cn)}
.pt-end{position:relative}
.pt-end:before{content:"";position:absolute;left:50%;top:-9px;margin-left:-6px;border-top:9px solid var(--cn);border-left:6px solid transparent;border-right:6px solid transparent}
.pt-cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));grid-template-rows:auto 1fr;max-width:880px;margin:0 auto}
.pt-card{margin:0 7px;border:1px solid var(--line);border-radius:16px;overflow:hidden;background:#fff;box-shadow:var(--shadow-sm);display:grid;grid-row:span 2;grid-template-rows:subgrid}
.pt-when{padding:16px 18px 18px;border-top:5px solid var(--teal)}
.pt-b .pt-when{border-top-color:var(--navy)}
.pt-tag{display:inline-block;font-size:.68rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:#fff;background:var(--teal);border-radius:999px;padding:2px 10px;margin-bottom:8px}
.pt-b .pt-tag{background:var(--navy)}
.pt-when h3{font-size:1.02rem;line-height:1.25;margin:0 0 4px}
.pt-when p,.pt-then p{margin:0;color:var(--muted);font-size:.9rem;line-height:1.45}
.pt-then{position:relative;margin-top:auto;padding:22px 18px 18px;background:var(--sky-2);border-top:1px solid var(--line)}
.pt-then:before{content:"\2193";position:absolute;left:18px;top:-13px;width:26px;height:26px;border-radius:50%;background:#fff;border:1px solid var(--line);color:var(--teal-dark);font-weight:700;display:flex;align-items:center;justify-content:center}
.pt-then h4{font-size:1rem;line-height:1.25;margin:0 0 4px;color:var(--navy)}
/* every-visit flow */
.vflow{margin-top:36px}
.vf-row{list-style:none;display:flex;align-items:stretch;gap:0;padding:0;margin:0}
.vf-node{position:relative;flex:1 1 0;min-width:0;background:#fff;border:1px solid var(--line);border-top:4px solid var(--teal);border-radius:14px;padding:16px 14px 16px;box-shadow:var(--shadow-sm);text-align:left;display:flex;flex-direction:column;gap:8px}
.vf-node:last-child{border-top-color:var(--navy)}
.vf-node h3{font-size:.98rem;line-height:1.25;margin:0}
.vf-node p{font-size:.84rem;line-height:1.45;color:var(--muted);margin:0}
.vf-num{position:absolute;top:12px;right:12px;width:24px;height:24px;border-radius:50%;background:var(--sky);color:var(--teal-dark);font-family:'Sora',sans-serif;font-size:.75rem;font-weight:700;display:flex;align-items:center;justify-content:center}
.vf-arrow{flex:0 0 28px;position:relative;align-self:center;height:2px;background:var(--cn)}
.vf-arrow:after{content:"";position:absolute;right:-1px;top:-5px;border-left:8px solid var(--cn);border-top:6px solid transparent;border-bottom:6px solid transparent}
.vf-back{margin:10px 6% 0;height:34px;border:2px dashed var(--cn);border-top:0;border-radius:0 0 18px 18px;position:relative;display:flex;align-items:flex-end;justify-content:center}
.vf-back:before{content:"";position:absolute;left:-2px;top:-8px;border-bottom:9px solid var(--cn);border-left:5px solid transparent;border-right:5px solid transparent;transform:translateX(-4px)}
.vf-back span{position:relative;top:15px;background:#fff;padding:2px 14px;font-size:.86rem;font-weight:600;color:var(--teal-dark)}
/* multi-story floors */
/* multi-story floors */
.floors{max-width:520px;margin:0 auto}
.fl-grid{display:grid;grid-template-columns:64px repeat(var(--nights),1fr);gap:6px;align-items:center}
.fl-h{font-size:.68rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);text-align:center}
.fl-n{font-size:.8rem;font-weight:600;color:var(--navy)}
.fl-c{display:block;height:38px;border-radius:8px;background:var(--sky);border:1px solid var(--line)}
.fl-c.on{background:linear-gradient(135deg,var(--teal),var(--cyan));border-color:transparent;box-shadow:0 4px 12px rgba(14,154,167,.35);position:relative}
.fl-c.on:after{content:"";position:absolute;left:50%;top:50%;width:12px;height:7px;border-left:3px solid #fff;border-bottom:3px solid #fff;transform:translate(-50%,-65%) rotate(-45deg)}
.fl-note{margin-top:12px;font-size:.84rem;color:var(--muted);text-align:center}

.multi-how{display:grid;grid-template-columns:1fr 1.1fr;gap:28px 48px;align-items:center;text-align:left;margin-top:26px;background:#fff;border:1px solid var(--line);border-radius:18px;padding:30px 34px;box-shadow:var(--shadow-sm)}
.multi-how h3{font-size:1.4rem;margin:0 0 10px}
.multi-how p{color:var(--muted);margin:0 0 14px}
.multi-how .btn{margin-top:6px}
.floors{max-width:none;margin:0}

.incl.one{grid-template-columns:1fr;max-width:560px;margin-left:auto;margin-right:auto}
/* ---- pricing table (Services) ---- */
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.pricing{background:var(--sky-2)}
.pshow{display:grid;grid-template-columns:minmax(0,440px) minmax(0,1fr);gap:26px;max-width:980px;margin:36px auto 0;align-items:start;text-align:left}
.pside{display:grid;gap:18px}
.pimg{margin:0}
.pimg img{display:block;width:100%;height:auto;-webkit-user-select:none;user-select:none;-webkit-user-drag:none;border-radius:22px;box-shadow:var(--shadow)}
.pside .pcard{margin:0}
@media (max-width:820px){.pshow{grid-template-columns:1fr;max-width:520px}}
.ptable-wrap{max-width:760px;margin:36px auto 0;background:#fff;border:1px solid var(--line);border-radius:18px;box-shadow:var(--shadow);overflow:hidden;text-align:left}
.ptable{width:100%;border-collapse:collapse}
.ptable thead th{background:var(--navy-2);color:#fff;font-family:'Sora',sans-serif;font-size:.92rem;font-weight:600;padding:16px 18px;text-align:center}
.ptable thead th:first-child{text-align:left}
.ptable thead th small{display:block;font-family:'Inter',sans-serif;font-weight:500;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:#a9c4d6;margin-top:2px}
.ptable tbody th{font-weight:600;color:var(--navy);font-size:.98rem;padding:15px 18px;text-align:left;white-space:nowrap}
.ptable td{font-family:'Sora',sans-serif;font-weight:700;color:var(--teal-dark);font-size:1.2rem;padding:15px 18px;text-align:center}
.ptable td+td{color:var(--navy)}
.ptable tbody tr{border-top:1px solid var(--line)}
.ptable tbody tr:nth-child(even){background:var(--sky-2)}
.pnote{margin:0;padding:14px 18px 16px;border-top:1px solid var(--line);color:var(--muted);font-size:.86rem;text-align:center;background:#fff}
.pgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin:28px auto 0;max-width:1000px;text-align:left}
.pcard{background:#fff;border:1px solid var(--line);border-radius:16px;padding:22px 22px 24px;box-shadow:var(--shadow-sm)}
.pcard h3{font-size:1.05rem;margin:0 0 8px}
.pcard p{color:var(--muted);margin:0 0 10px;font-size:.93rem}
.pcard-sm{font-size:.82rem !important}
.pcard-hi{border-top:5px solid var(--cyan);background:linear-gradient(180deg,#fff,var(--sky-2))}
.pcard-link{font-weight:600}
.pwin{list-style:none;margin:6px 0 10px;padding:0;display:grid;gap:6px}
.pwin li{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px dashed var(--line);padding-bottom:6px;color:var(--ink);font-size:.93rem}
.pwin strong{font-family:'Sora',sans-serif;color:var(--teal-dark)}
.pricing .more{margin-top:30px}
.price-tease{margin:26px 0 0;color:var(--muted)}
.price-tease strong{color:var(--navy)}
@media (max-width:820px){.pgrid{grid-template-columns:1fr}.ptable tbody th{white-space:normal;padding:13px 12px;font-size:.92rem}.ptable td{padding:13px 8px;font-size:1.08rem}.ptable thead th{padding:14px 8px;font-size:.84rem}}

/* ---- tablets: the process map becomes two rows of three ---- */
@media (max-width:1099px){
  .pmap{grid-template-columns:repeat(3,minmax(0,1fr));row-gap:14px}
  .pm-step:nth-child(3n+1) .pm-rail i:first-child,.pm-step:nth-child(3n) .pm-rail i:last-child{visibility:hidden}
  .pm-card h3{font-size:1.02rem}.pm-card p{font-size:.9rem}
}
@media (max-width:900px){
  .vs-grid{grid-template-columns:1fr}
  .pt-cards{grid-template-columns:1fr;grid-template-rows:none;gap:16px}
  .pt-card{margin:0;display:flex;flex-direction:column;grid-row:auto}
  .pt-fork,.pt-join{height:30px}
  .pt-fork:before{height:30px}.pt-fork:after,.pt-join:after{display:none}
  .pt-fork i:nth-child(2){display:none}
  .pt-fork i:nth-child(1){left:50%;top:0;height:30px}
  .pt-join:before{top:0;height:30px}
  .pt-join i{display:none}
  .multi-how{grid-template-columns:1fr;padding:24px 20px}
}
/* ---- phones: the process map is a vertical timeline ---- */
@media (max-width:720px){
  .pmap{grid-template-columns:1fr;max-width:560px;margin:0 auto;row-gap:0}
  .pm-step{display:grid;grid-template-columns:38px minmax(0,1fr);gap:0 14px}
  .pm-rail{flex-direction:column;height:auto}
  .pm-rail i{flex:1;width:2px;height:auto}
  .pm-rail i:first-child{display:none}
  .pm-step:last-child .pm-rail i:last-child{display:none}
  .pm-rail i:last-child{visibility:visible}
  .pm-card{margin:0 0 14px}
  .pm-n{box-shadow:none}
  .vs-panel{padding:22px 18px 24px}
}
@media (max-width:1020px){
  .vf-row{flex-direction:column}
  .vf-arrow{flex:0 0 26px;width:2px;height:26px;margin-left:28px;align-self:flex-start}
  .vf-arrow:after{right:auto;left:-5px;top:auto;bottom:-1px;border-left:6px solid transparent;border-right:6px solid transparent;border-top:9px solid var(--cn);border-bottom:0}
  .vf-node{padding-right:48px}
  .vf-back{margin:14px 0 0;height:auto;border:0;display:block;text-align:center}
  .vf-back:before{display:none}
  .vf-back span{top:0;display:inline-block;background:var(--sky);border-radius:999px;padding:8px 18px}
  .vf-back span:before{content:"\21BB\00a0\00a0"}
}
@media (max-width:480px){
  .fl-grid{grid-template-columns:52px repeat(var(--nights),1fr);gap:5px}
  .fl-h{font-size:.58rem;letter-spacing:0}
  .fl-c{height:34px}
}
'''
