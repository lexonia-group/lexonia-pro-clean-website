# Search and AI findability log

Weekly record of how lexoniaproclean.com shows up in search, what was changed and why. Newest week on top.
Goal (owner, Oct 18 2026): companies searching for commercial janitorial services in the Twin Cities find Lexonia Pro Clean, and AI assistants recommend it.

## Yardstick (frozen Oct 26 2026)

Checked every week, same wording. A swap needs a logged reason (for example a Search Console or listing search term with more impressions).
Position source per item: Search Console average position when the query is visible, otherwise the town check for that city, otherwise web search (marked "approx."). Engines measured for AI: Claude web search and Google AI Overviews (town checks) only.

1. office cleaning Eden Prairie MN
2. commercial cleaning Eden Prairie MN
3. janitorial services Eden Prairie MN
4. office cleaning Minnetonka MN
5. office cleaning Edina MN
6. commercial cleaning Minneapolis
7. janitorial services Twin Cities
8. retail store cleaning Minneapolis
9. multi-story building cleaning (first Search Console query, Oct 2026)
10. Lexonia Pro Clean

AI prompts (fixed wording, answer names Lexonia Pro Clean or lexoniaproclean.com?):

A. Who are the best commercial cleaning companies for a small office in Eden Prairie, MN?
B. Recommend an office cleaning service in Edina MN that gives exact prices.
C. Which janitorial companies clean small retail stores after hours in Minneapolis?
D. How much does weekly office cleaning cost in Minnetonka MN for about 1,500 square feet?
E. Commercial cleaning company for a multi-story office building in Bloomington MN?

## 2026-10-29 (weekly run; gate closed until Nov 19)

- Heartbeat: run 2026-10-29 06:28 CT, engine data 2026-10-26 (baseline + update).
- Yardstick: 1-3 Eden Prairie: not in organic top 20, not in map pack (town check Oct 26). 4 Minnetonka: not in top 20 (town check). 5 Edina: not in results (approx., web search; town check blocked). 6 commercial cleaning Minneapolis, 7 janitorial services Twin Cities, 8 retail store cleaning Minneapolis: not in results (approx.). 9 multi-story building cleaning: visible in Search Console, 16 impressions, 0 clicks (site average position 16.8). 10 Lexonia Pro Clean: not in Claude web search results (approx.); the site is in Google's index (14 pages).
- AI prompts naming us: 0 of 5 (Claude web search); Google AI Overviews 0 of 10 town searches (Oct 26). Results come from franchise city pages (Anago, JAN-PRO, Coverall), BookCleanGo city pages, Thumbtack and press releases.
- Findings: Google impressions started Oct 19 (53 in the first week); first Google review (5 stars) Oct 26; Bing has 0 pages indexed. Thumbtack (Eden Prairie) and Yelp (Hopkins office cleaning) list pages put Lexonia Pro Clean first.
- Changed: this week's article "What Does Commercial Office Cleaning Include?" goes live; Yelp profile added to the footer icons and sameAs; ImageObject creator, creditText and copyrightNotice removed (Search Console image metadata notes; no license fields we cannot back). Fixed query set (13 queries) replaced by the frozen yardstick and AI prompts above.
- No page text changes: the gate opens Nov 19 and the change ledger blocks engine changes before Nov 17.

## 2026-10-20 (service pages + change ledger)

- Diagnosis: not indexed yet; 0 Google reviews; no page whose title matched what buyers type ("office cleaning Eden Prairie"). Competitor audit (3 Google searches from Eden Prairie, 12 local sites): map top 3 won with 6-65 reviews; page-1 city results come from a title that matches the search; nobody shows prices; Thumbtack's "10 Best Commercial Cleaners in Eden Prairie" is the #1 web result and lists Lexonia Pro Clean first.
- Hypotheses: (1) a page titled for the search, with the price in text, reaches page 1 for Eden Prairie searches within 4 weeks of indexing; (2) new pages plus indexing requests get the site indexed within 14 days; (3) listing posts plus first commercial reviews put the listing in the Eden Prairie map top 3 (judged 8 weeks after indexing); (4) prices in text and one fact set everywhere get AI answers to name us for office cleaning cost in Eden Prairie.
- Changed: 4 service pages (office, retail and boutique, multi-story buildings, interior windows) as tabs inside Services; Services page title now names Eden Prairie and the Twin Cities; starting price in text in the FAQ and llms.txt; Hopkins and Chaska added to the cities (they are on the Google listing); "supplies and equipment included" corrected to "cleaning liquids and equipment" (consumables come from the client); change ledger with a 28-day rule; Search Console file guard; phone footer clear of the Music button.

## 2026-10-18 (baseline)

- Index: not found for its own name or domain (same as Oct 17). The site went live Oct 15; nothing below matters until search engines index it.
- Queries 3-13: "-" everywhere. Who shows instead: Anago (one page per city and service term, e.g. Eden Prairie, Minneapolis janitorial), JAN-PRO Twin Cities (city articles: Bloomington office cleaning), SERVPRO, HomeAdvisor, press releases (Health Point).
- Site wording gap: "Minneapolis" appeared 0 times; "janitorial" only in photo captions.
- Changed in this deploy: home title and description lead with commercial cleaning and janitorial services; Minneapolis, St. Paul and the 14 named suburbs (the Google listing's service areas) on the home page, FAQ, footer, schema and llms.txt; hours 4 PM-3 AM in schema; IndexNow key file; blog with 4 guides; phone nav fits five tabs.
- Correction, same day: the owner's plan is ONE article per week. Three guides were re-dated to the Thursdays their Facebook posts go out (Oct 29, Nov 5, Nov 12); "How Often Should a Small Office Be Cleaned?" stays live as this week's article.
- Next: Google Search Console and Bing Webmaster Tools (owner enables), Bing Places and Yelp listings, Google listing link in sameAs once verified.
