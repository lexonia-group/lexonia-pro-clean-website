# Lexonia Pro Clean — website (lexoniaproclean.com)

One repository, one flow. Private. This folder tree is the single source of truth for the site.

```
site/        the published website (Netlify publishes this folder; no build step on Netlify)
generator/   builds site/ : build_site.py, page blocks, diagrams, price-card renderer, photos, audio, fonts
qa/          checks: links and anchors, SEO tags, structured data, claims, security headers, form, phone/desktop layouts
netlify.toml security headers, cache rules, publish directory (sits above site/, so it is never served)
```

## The flow

1. Edit the generator (never hand-edit site/; the next build overwrites it). Update `BUILD_DATE` in generator/build_site.py when content changes.
2. Build: `python3 generator/build_site.py site deploy`
3. Check, from the repository root: `python3 qa/validate.py` and `python3 qa/qa_static.py`. For headers, form and layouts: `python3 qa/serve_sec.py site 8765 &` then `qa/qa_form.py`, `qa/qa_browser.py`, `qa/test12.py` (responsive), `qa/test13.py` and `qa/test14.py` (picture loop and music). Browser checks need Python Playwright and numpy.
4. Commit and push to `main`. Netlify deploys on every push to main: each push is one production deploy and counts against the shared Netlify credits, so batch edits.

`python3 generator/build_site.py <folder> preview` makes the single-file preview used inside Cowork chats.

## Content rules (owner's, firm)

- Every sentence traces to what the owner said or to the real commercial checklist. Nothing invented. "Insured" and "background-checked" are true; "licensed" is not.
- Prices appear only as image cards. No dollar amounts in page text, structured data, llms.txt or image alt text.
- No brand names of products. Do not list what the crew brings.
- Never appear on the site: floor or carpet care, disinfection services or EPA claims, post-construction, one-time or emergency cleans, HEPA or eco claims, photo-verified reports.
- Thumbtack appears once: the footer link. The word "service-area" appears nowhere. The generator asserts both.
- Mobile first. Each page answers the "so what"; every chart has a legend.

## Not in this repository

Passwords, tokens, webhook addresses, customer data, invoices, emails. The business record and the dated decision log live in the project folder (CLAUDE.md and TT-Operation-Handoff.md), not here.

## Going live

Nothing goes live and no DNS or nameserver change is made without the owner's explicit go in chat. Order: repository, Netlify project, form test, DNS (records first, nameservers second), email, search basics.
