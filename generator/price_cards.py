"""Renders the price cards as images (so prices are not plain page text that a bot can copy).
Called by build_site.py with the price data; re-renders only when the data or the design changes."""
import os, hashlib, json

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:transparent}
body{font-family:'Inter',sans-serif;color:#1f2d3d;-webkit-font-smoothing:antialiased}
.card{position:relative;background:#fff;border:1px solid #dce8ec;border-radius:22px;overflow:hidden;width:%(w)dpx}
.card:before{content:"LEXONIA PRO CLEAN   LEXONIA PRO CLEAN   LEXONIA PRO CLEAN   LEXONIA PRO CLEAN   LEXONIA PRO CLEAN   LEXONIA PRO CLEAN";position:absolute;left:-60px;right:-60px;top:46%%;transform:rotate(-18deg);
  font:800 30px/1 'Sora',sans-serif;letter-spacing:.2em;white-space:nowrap;color:rgba(11,37,69,.035);pointer-events:none}
.hd{background:linear-gradient(135deg,#0b2545,#13406b);color:#fff;padding:22px 26px 20px}
.hd .k{font:600 12px 'Inter',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#6fd3de;margin-bottom:6px}
.hd .t{font:800 22px/1.15 'Sora',sans-serif}
.hd .s{font:500 14px 'Inter',sans-serif;color:#c9d9e6;margin-top:5px}
table{width:100%%;border-collapse:collapse;position:relative}
thead th{font:600 13px 'Sora',sans-serif;color:#0b2545;background:#eaf6f8;padding:12px 10px;text-align:center;border-bottom:2px solid #bfe6ea}
thead th:first-child{text-align:left;padding-left:26px}
thead small{display:block;font:500 10.5px 'Inter',sans-serif;letter-spacing:.07em;text-transform:uppercase;color:#5b6b7c;margin-top:3px}
tbody th{font:600 15px 'Inter',sans-serif;color:#0b2545;text-align:left;padding:0 10px 0 26px;height:46px;white-space:nowrap}
tbody td{font:700 20px 'Sora',sans-serif;text-align:center;height:46px;color:#0b7c87}
tbody td+td{color:#0b2545}
tbody tr{border-top:1px solid #e4eef1}
tbody tr:nth-child(even){background:#f6fbfc}
.ft{padding:14px 26px 8px;font:500 13px 'Inter',sans-serif;color:#5b6b7c;border-top:1px solid #dce8ec;text-align:center}
.wm{padding:0 26px 16px;font:600 11px 'Inter',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#8aa0b2;text-align:center}
ul{list-style:none;padding:4px 26px 0}
li{display:flex;justify-content:space-between;align-items:baseline;height:46px;align-items:center;border-top:1px dashed #cfe0e5;font:600 15px 'Inter',sans-serif;color:#0b2545}
li:first-child{border-top:0}
li b{font:800 22px 'Sora',sans-serif;color:#0b7c87}
"""

def _table_html(rows, minimum):
    body = ''.join('<tr><th>%s</th><td>$%d</td><td>$%d</td></tr>' % (sz, w, b) for sz, w, b in rows)
    return ('<div class="card" id="c"><div class="hd"><div class="k">Pricing</div><div class="t">Recurring cleaning</div><div class="s">Price per visit, by size of space</div></div>'
            '<table><thead><tr><th>Size of space<small>square feet</small></th><th>Weekly<small>per visit</small></th><th>Every other week<small>per visit</small></th></tr></thead><tbody>%s</tbody></table>'
            '<div class="ft">Prices are per visit and before sales tax. Minimum job: $%d.</div><div class="wm">Lexonia Pro Clean &middot; Eden Prairie, MN &middot; 2026</div></div>' % (body, minimum))

def _windows_html(wins):
    li = ''.join('<li><span>%s</span><b>$%d</b></li>' % (a, b) for a, b in wins)
    return ('<div class="card" id="c"><div class="hd"><div class="k">Add-on</div><div class="t">Interior windows</div><div class="s">Added to any visit. Interior glass only.</div></div>'
            '<ul>%s</ul><div class="ft" style="margin-top:8px">More than 15 windows is priced at the walkthrough. Before sales tax.</div><div class="wm">Lexonia Pro Clean &middot; Eden Prairie, MN &middot; 2026</div></div>' % li)

def render(rows, wins, outdir, here):
    """Returns {name: (relative path, css width, css height)}. Image files are written to outdir (img/pricing)."""
    os.makedirs(outdir, exist_ok=True)
    spec = {'by-size': (440, _table_html(rows, rows[0][1])), 'windows': (500, _windows_html(wins))}
    key = hashlib.sha1((json.dumps([rows, wins, CSS, [s[1] for s in spec.values()]])).encode()).hexdigest()[:12]
    cache = os.path.join(here, 'price_assets')
    os.makedirs(cache, exist_ok=True)
    stamp = os.path.join(cache, 'hash.txt')
    names = {k: 'lexonia-pro-clean-price-card-%s.png' % k for k in spec}
    if not (os.path.exists(stamp) and open(stamp).read().strip() == key and all(os.path.exists(os.path.join(cache, n)) for n in names.values())):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch()
            for k, (w, html) in spec.items():
                ctx = b.new_context(viewport={'width': w + 40, 'height': 900}, device_scale_factor=2)
                pg = ctx.new_page()
                pg.set_content('<!doctype html><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@500;600&display=swap" rel="stylesheet"><style>%s</style>' % (CSS % {'w': w}) + html)
                pg.evaluate('document.fonts.ready')
                pg.wait_for_timeout(700)
                pg.locator('#c').screenshot(path=os.path.join(cache, names[k]), omit_background=True)
                ctx.close()
            b.close()
        from PIL import Image
        for n in names.values():
            f = os.path.join(cache, n)
            im = Image.open(f).convert('RGBA')
            im.quantize(colors=128, method=Image.FASTOCTREE).save(f, optimize=True)
        open(stamp, 'w').write(key)
    import shutil
    from PIL import Image
    out = {}
    for k, n in names.items():
        shutil.copyfile(os.path.join(cache, n), os.path.join(outdir, n))
        w, h = Image.open(os.path.join(cache, n)).size
        out[k] = ('img/pricing/' + n, w // 2, h // 2)
    return out
