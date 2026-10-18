"""Reusable page blocks for the 'so what, then drill down' structure: at-a-glance tiles, in-page jump links, step flows, next-steps list.
Text stays real HTML (readable by search engines and screen readers). Flows reuse the .vflow styles from diagrams_how."""
from diagrams_how import ICON


def flow(items, label, back=None):
    """Horizontal flow on desktop, vertical on phones. items: (icon, title, text)."""
    out = ['<div class="vflow reveal" role="group" aria-label="Flow chart: %s">' % label, '  <ol class="vf-row">']
    for k, (ic, title, text) in enumerate(items):
        out.append('    <li class="vf-node"><span class="vf-num">%d</span><span class="sw-ic">%s</span><h3>%s</h3><p>%s</p></li>' % (k + 1, ICON[ic], title, text))
        if k < len(items) - 1:
            out.append('    <li class="vf-arrow" aria-hidden="true"></li>')
    out.append('  </ol>')
    if back:
        out.append('  <div class="vf-back" aria-hidden="true"><span>%s</span></div>' % back)
    out.append('</div>')
    return '\n'.join(out)


def glance(tiles, label='At a glance'):
    """tiles: (big value, label, href, link text). Each tile drills down to the section or page that has the detail."""
    t = ''.join('<a class="gl-tile" href="%s"><strong>%s</strong><span>%s</span><em>%s</em></a>' % (h, v, l, c) for v, l, h, c in tiles)
    return '<div class="glance reveal" role="group" aria-label="%s">%s</div>' % (label, t)


def jump(items):
    """In-page links. items: (anchor id, label)."""
    return ('<nav class="jump" aria-label="On this page"><span class="jump-l">On this page</span>'
            + ''.join('<a href="#%s">%s</a>' % (a, l) for a, l in items) + '</nav>')


def next_steps(items, title='What happens next'):
    return ('<div class="nx-wrap"><h2 class="nx-h">%s</h2><ol class="nx">' % title
            + ''.join('<li><strong>%s</strong>%s</li>' % (a, b) for a, b in items) + '</ol></div>')


BLOCKS_CSS = r'''
/* ---- shared blocks: at a glance, jump links, next steps, drill-down links ---- */
section[id],div[id]{scroll-margin-top:88px}
.glance{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:0 0 44px}
.gl-tile{display:flex;flex-direction:column;gap:5px;background:#fff;border:1px solid var(--line);border-top:4px solid var(--teal);border-radius:14px;padding:16px 18px 14px;box-shadow:var(--shadow-sm);text-decoration:none;text-align:left;transition:transform .15s ease,box-shadow .15s ease,border-color .15s ease}
.gl-tile:hover,.gl-tile:focus-visible{transform:translateY(-2px);box-shadow:var(--shadow);border-color:var(--teal)}
.gl-tile strong{font:800 1.5rem/1.1 'Sora',sans-serif;color:var(--teal-dark)}
.gl-tile span{font-size:.9rem;color:var(--ink);line-height:1.35}
.gl-tile em{font-style:normal;font-size:.82rem;font-weight:700;color:var(--teal);margin-top:auto;padding-top:6px}
.gl-tile em:after{content:" \2192"}
.jump{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:center}
.jump-l{font-size:.78rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-right:6px}
.jump a{display:inline-flex;align-items:center;min-height:40px;padding:0 16px;border-radius:999px;background:#fff;border:1px solid var(--line);font-size:.9rem;font-weight:600;color:var(--navy);text-decoration:none;box-shadow:var(--shadow-sm)}
.jump a:hover,.jump a:focus-visible{border-color:var(--teal);color:var(--teal-dark)}
.jump-sec{padding:26px 0 0}
.glance-sec{padding:44px 0 34px}
.glance-sec .glance{margin-bottom:22px}
.more-link{display:inline-block;margin-top:8px;font-size:.9rem;font-weight:700;color:var(--teal-dark);text-decoration:none}
.more-link:after{content:" \2192"}
.more-link:hover{text-decoration:underline}
.flow-cta{margin-top:30px;text-align:center}
/* next steps (dark quote section) */
.nx-wrap{margin:30px 0 8px}
.nx-h{font:700 1.05rem 'Sora',sans-serif;color:#fff;margin:0 0 16px}
.nx{list-style:none;margin:0;padding:0;counter-reset:nx}
.nx li{position:relative;padding:0 0 20px 54px;color:#c9d9e6;font-size:.95rem;line-height:1.45;counter-increment:nx}
.nx li:before{content:counter(nx);position:absolute;left:0;top:0;width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,var(--teal),var(--cyan));color:#fff;font:700 .92rem 'Sora',sans-serif;display:flex;align-items:center;justify-content:center}
.nx li:after{content:"";position:absolute;left:17px;top:40px;bottom:4px;width:2px;background:rgba(139,227,236,.35)}
.nx li:last-child{padding-bottom:0}
.nx li:last-child:after{display:none}
.nx strong{display:block;color:#fff;font-size:1rem;margin-bottom:2px}
@media (max-width:960px){.glance{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.glance{gap:10px}.gl-tile{padding:14px 14px 12px}.gl-tile strong{font-size:1.25rem}.jump-l{width:100%;text-align:center;margin:0 0 2px}}
/* ---- tighter vertical rhythm: less blank space between sections ---- */
section{padding:50px 0}
.faq{padding:50px 0}
.cta-section{padding:40px 0 56px}
.section-title{margin-bottom:12px}
.faq-list{max-width:none;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 20px;align-items:start}
@media (max-width:900px){.faq-list{grid-template-columns:1fr;max-width:820px}}
@media (max-width:720px){section{padding:40px 0}.faq{padding:40px 0}.cta-section{padding:28px 0 44px}}
/* ---- bigger tap targets, and the phone menu fits without cutting off "Contact" ---- */
.nav-links a{padding-top:12px;padding-bottom:12px}
.brand{padding:8px 0}
.nav-phone{padding:10px 0}
footer.site ul{gap:0}
footer.site ul a{display:inline-block;padding:9px 0}
.more-link{padding:10px 0;margin-top:0}
.price-tease a,.multi a:not(.btn),.contact-item a,.pcard-link,.pt-then a{display:inline-block;padding:8px 0}
@media (max-width:560px){
  .nav-links{justify-content:space-between;margin:0 -12px;gap:0;flex-wrap:wrap}
  .nav-links a{padding:12px 6px;font-size:.84rem}
}
@media (max-width:350px){.nav-links{justify-content:center}}
/* ---- colour contrast (WCAG AA) and footer headings ---- */
.kicker{color:#0a6d77}
.nav-links a.active{color:#0a6d77}
footer.site .f-h{color:#fff;font:700 .95rem 'Sora',sans-serif;margin:0 0 16px}
.gl-tile em,.gl-tile:hover em{color:#0a6d77}
.price-tease a,.pcard-link,.more-link{color:#0a6d77}
.pm-us .pm-who,.pt-a .pt-tag,.pt-tag{background:#0a6d77}
.pt-b .pt-tag{background:var(--navy)}
.pm-loop span,.vs-loop{color:#0a6d77}
.pm-us .pm-n{background:#0a6d77}
/* cards that follow the page header directly (Services) need no extra gap above them */
.sr-only+.cards{margin-top:0}
/* two business types, side by side and centred */
.cards{grid-template-columns:repeat(2,minmax(0,1fr));max-width:900px;margin-left:auto;margin-right:auto}
@media (max-width:680px){.cards{grid-template-columns:1fr}}
'''
