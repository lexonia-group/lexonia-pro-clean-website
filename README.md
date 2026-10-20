# Lexonia Pro Clean — website (lexoniaproclean.com)

One repository, one flow. This folder tree is the single source of truth for the site.

```
generator/   builds site/ : build_site.py, blog.py, page blocks, diagrams, price-card renderer, photos, audio, fonts
content/blog one Markdown file per blog article (front matter + text); live on its date, US Central
site/        build output only: Netlify runs the generator on every push and publishes site/ (not stored in the repository)
qa/          checks: links and anchors, SEO tags, structured data, claims, security headers, form, phone/desktop layouts
netlify.toml security headers, cache rules, publish directory (sits above site/, so it is never served)
```

## The flow

1. Edit the generator or add an article to content/blog/ (never hand-edit site/; every build overwrites it). Update `BUILD_DATE` in generator/build_site.py when page content changes.
2. Build locally to check: `python3 generator/build_site.py site deploy` (Netlify runs the same command on every push).
3. Check, from the repository root: `python3 qa/validate.py` and `python3 qa/qa_static.py`. For headers, form and layouts: `python3 qa/serve_sec.py site 8765 &` then `qa/qa_form.py`, `qa/qa_browser.py`, `qa/test12.py` (responsive), `qa/test13.py` and `qa/test14.py` (picture loop and music). Browser checks need Python Playwright and numpy.
4. Commit and push to `main`. Netlify builds and deploys on every push to main: each push is one production deploy and counts against the shared Netlify credits (three sites share one plan), so batch edits. Blog: at most one publish a week. A failed build leaves the previous version live.

`python3 generator/build_site.py <folder> preview` makes the single-file preview used inside Cowork chats.

## Content rules (owner's, firm)

- Every sentence traces to what the owner said or to the real commercial checklist. Nothing invented. "Insured" and "background-checked" are true; "licensed" is not.
- Prices: owner decision Oct 17 2026, prices may be public as text. Approved amounts: from $155 per visit (1,000-2,000 sq ft, weekly, plus tax); interior windows $40 / $70 / $110. qa/qa_static.py flags any other dollar amount.
- Blog cadence (owner, Oct 18 2026): ONE article goes live per week, dated to its Thursday, the same day its Facebook post links it. Never publish several at once.
- Blog: facts only (what the owner stated, the real checklist); general photos from Unsplash with no faces and the photographer credited; educational topics only: before-and-after job photos go to social posts, never to the blog (owner, Oct 18 2026). Wording: "offices and small retail stores across the Twin Cities and suburbs".
- No brand names of products. Do not list what the crew brings.
- Never appear on the site: floor or carpet care, disinfection services or EPA claims, post-construction, one-time or emergency cleans, HEPA or eco claims, photo-verified reports.
- Thumbtack appears once: the footer link. The Facebook Page is linked in the footer and listed as an official profile (sameAs). The word "service-area" appears nowhere. The generator asserts both.
- Mobile first. Each page answers the "so what"; every chart has a legend.
- Search wording (Oct 18 2026): lead with "commercial cleaning" and "janitorial services"; name Minneapolis, St. Paul and the suburbs. The named cities are CITIES in generator/build_site.py, the same list as the Google listing's service areas; edit them there only. Hours 4 PM to 3 AM daily, as on the Google listing.
- IndexNow: the key file is built at /<INDEXNOW_KEY>.txt; after a deploy, the changed URLs are sent to api.indexnow.org (Bing and others).
- Service pages (owner go Oct 20 2026): one page per service sold, in generator/service_pages.py, reached through the tabs inside the Services tab (the top menu stays at 5 tabs). Checklist, prices, cities and shared answers come from build_site.py, never retyped. No city pages: a city gets its own page only when Search Console shows impressions for that city and no page of ours ranks, one at a time.
- Change ledger (findability engine, Oct 20 2026): seo/changes.csv records every change to a page's title, description or main text. The build fails when a page changed without a row, or when an engine or owner change comes less than 28 days after that page's previous change (exempt: baseline, new page, factual correction; blog articles are not tracked). After an intended edit: build, then `python3 generator/ledger.py record site "<type>" "<reason>"`, then build again.
- prices.json (Oct 20 2026): the price card as data, built from PRICE_ROWS (the same list the price-card images use). The Make lead flow (scenario 6640357) reads it to send each website quote lead an instant ballpark from info@lexoniaproclean.com. Change a price only in PRICE_ROWS; the card, llms.txt and the email follow. The quote form's "How often?" list must keep its option names (Weekly, Every other week, 2–3x per week, Nightly (5x+ per week), Not sure yet): the email logic matches them.
- Article backlog: seo/TOPICS.md (buyer-decision topics).

## Not in this repository

Passwords, tokens, webhook addresses, customer data, invoices, emails. The business record and the dated decision log live in the project folder (CLAUDE.md and TT-Operation-Handoff.md), not here.

## Going live

Nothing goes live and no DNS or nameserver change is made without the owner's explicit go in chat. Order: repository, Netlify project, form test, DNS (records first, nameservers second), email, search basics.
