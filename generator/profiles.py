"""The business's outside profiles: footer icons, sameAs (structured data), llms.txt, QA allow-list.

Single source. A profile shows in the footer only when its url is set; to add Instagram or the
Google Business Profile, paste the profile's public link into url and rebuild. Nothing else changes.
Icons: Simple Icons (CC0), drawn in one color as the brands' guidelines allow for small marks.
Owner rules: Thumbtack appears once, as the footer icon, and stays out of sameAs (Oct 14 2026);
the Facebook Page is linked and listed as an official profile (Oct 17 2026); icons, not text (Oct 18 2026).
"""

TT_URL = 'https://www.thumbtack.com/mn/eden-prairie/commercial-cleaning/lexonia-pro-clean/service/586412868292583430'
FB_URL = 'https://www.facebook.com/profile.php?id=61595444793911'
IG_URL = None    # Instagram: set when the account is ready
GBP_URL = 'https://www.google.com/maps?cid=7406041639399653483'   # Google Business Profile, verified Oct 2026 (Maps link by the listing's permanent ID)

_P_TT = 'M6.18 6.38h11.69v2.68H6.17zm7.27 3.8v3.14c0 3.23-.02 3.74-.14 4.36a7.95 7.95 0 0 1-1.3 2.87c-.03 0-.78-1.35-.9-1.62-.17-.4-.3-.8-.4-1.25l-.09-.41-.02-5.78.16-.2a3.3 3.3 0 0 1 2.44-1.1zM12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0Z'
_P_FB = 'M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z'
_P_IG = 'M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077'
_P_G = 'M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z'

# (label read aloud by screen readers, url, listed in sameAs, icon path), in footer order
PROFILES = [
    ('Follow us on Facebook', FB_URL, True, _P_FB),
    ('Follow us on Instagram', IG_URL, True, _P_IG),
    ('Find us on Google', GBP_URL, True, _P_G),
    ('Find us on Thumbtack', TT_URL, False, _P_TT),
]

SAME_AS = [u for _l, u, s, _p in PROFILES if u and s]
LINKED = [u for _l, u, _s, _p in PROFILES if u]

def icon_link(label, url, path):
    return ('<a class="soc-a" href="%s" target="_blank" rel="noopener" aria-label="%s">'
            '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false"><path d="%s"/></svg></a>'
            % (url, label, path))

TT_LINK = icon_link('Find us on Thumbtack', TT_URL, _P_TT)   # the one allowed Thumbtack mention (build guard strips exactly this)

def social_row():
    return '<div class="soc">' + ''.join(icon_link(l, u, p) for l, u, _s, p in PROFILES if u) + '</div>'

SOCIAL_CSS = '''
/* Footer profile icons: 44px tap targets, one color, brighter on hover or keyboard focus */
.soc{display:flex;flex-wrap:wrap;gap:10px;margin-top:4px}
footer.site ul a.soc-a{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:50%;border:1px solid rgba(255,255,255,.2);color:#c9d6e2;transition:color .2s,border-color .2s,background .2s}
footer.site ul a.soc-a:hover,footer.site ul a.soc-a:focus-visible{color:#fff;border-color:var(--cyan);background:rgba(255,255,255,.06)}
.soc-a svg{fill:currentColor;display:block}
'''
