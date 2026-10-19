"""Privacy notice page (privacy.html), linked from every footer and from Stripe's public details.

Rule: this page describes what the site ACTUALLY does. When the quote form, analytics, hosting
or any outside service changes, change this text in the same commit. Nothing here may promise
more than the site does. Written Oct 19 2026 from the generator itself: Netlify form fields,
the Netlify-to-Make email alert, Microsoft Clarity, self-hosted fonts/images/music, Stripe invoices.
"""

UPDATED = 'October 19, 2026'

TITLE = 'Privacy Notice | Lexonia Pro Clean'
DESC = ('How Lexonia Pro Clean handles what you send through the quote form, the visitor '
        'analytics on this site, and how to ask us to delete your details.')


def body(page_hero, email, phone, tel):
    s = [
        ('What we collect through the quote form',
         '<p>When you request a quote, the form sends us your name, company, email, phone number, '
         'the service you are asking about, the size of your space, how often you want cleaning, and '
         'any message you write. We use it only to answer you, set up a walkthrough, send a price and, '
         'if you become a customer, to provide the service and keep business records.</p>'),
        ('Who handles it for us',
         '<ul class="pv-list">'
         '<li><strong>Netlify</strong> hosts this website and stores form submissions. Like any web host, '
         'it processes technical data such as IP addresses to deliver and protect the site.</li>'
         '<li><strong>Make</strong>, an automation service, passes each form submission to our email so we can reply quickly.</li>'
         '<li><strong>Stripe</strong> handles invoices and payments for customers. We do not see or store full card or bank account numbers.</li>'
         '</ul>'
         '<p>We do not sell or rent your details, and we do not add you to a mailing list.</p>'),
        ('Visitor analytics',
         '<p>We use Microsoft Clarity to understand how visitors use this site, so we can make it easier to use. '
         'Clarity records things like clicks, scrolling and the pages you visit, and uses cookies to do it. '
         'This data is processed by Microsoft; Microsoft explains its practices in its privacy statement at privacy.microsoft.com. '
         'You can block these cookies in your browser settings without losing access to anything on this site.</p>'),
        ('What stays in your browser',
         '<p>The fonts, photos and music on this site are served from our own website. If you turn the music on, '
         'your browser remembers that choice while you browse; it is not sent to us.</p>'),
        ('How long we keep it',
         '<p>We keep a quote request as long as we need it to answer you and, if you become a customer, '
         'to serve you and keep the records the law requires.</p>'),
        ('Your choices',
         '<p>You can ask us what we hold about you, ask us to correct it, or ask us to delete it. '
         'Email <a href="mailto:%s">%s</a> or call <a href="%s">%s</a>. We reply the same day.</p>' % (email, email, tel, phone)),
        ('Children',
         '<p>This site is for businesses and is not directed to children.</p>'),
        ('Changes to this notice',
         '<p>When what we collect or how we use it changes, we update this page. The date below shows the last update.</p>'),
    ]
    sections = ''.join('      <h2>%s</h2>\n      %s\n' % (h, t) for h, t in s)
    return ('<main id="top">\n' + page_hero('Privacy', 'Privacy Notice',
                                            'What we collect on this site, why, and how to reach us about it.')
            + '<section class="pv">\n  <div class="container pv-wrap">\n' + sections
            + '      <p class="pv-date">Last updated: %s. Lexonia Pro Clean LLC, Eden Prairie, Minnesota.</p>\n' % UPDATED
            + '  </div>\n</section>\n</main>\n')


CSS = '''
/* Privacy notice: readable column, phone first */
.pv-wrap{max-width:760px}
.pv h2{font-size:1.2rem;margin:30px 0 10px}
.pv h2:first-child{margin-top:0}
.pv p,.pv li{color:var(--muted);font-size:.98rem}
.pv-list{padding-left:20px;margin:0 0 12px;display:flex;flex-direction:column;gap:8px}
.pv-date{margin-top:30px;font-size:.88rem}
.footer-bottom a{color:#9fb5c8;text-decoration:underline}
.footer-bottom a:hover{color:var(--cyan)}
'''
