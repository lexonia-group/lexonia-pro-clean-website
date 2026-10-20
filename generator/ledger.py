"""Change ledger for the site's pages (findability engine rule, owner go Oct 20 2026).

Why: to judge whether a change helped search results, each page changes at most once every 28 days, and every change is
written down. seo/changes.csv holds one row per change: date, page, type, fingerprint, reason. The build calls check() and
FAILS when a page's title, description or main text differs from its last row, or when an engine/owner change comes less than
28 days after the page's previous change. Exempt from the 28-day spacing: baseline, new page, factual correction.

After an intended edit: build, then  python3 generator/ledger.py record site "<type>" "<reason>"  adds the rows, then build again.
Blog articles are not tracked here (one a week by their own rule); the blog index changes with them.
"""
import csv, datetime, hashlib, os, re, sys

TYPES = ('baseline', 'new page', 'factual correction', 'engine change', 'owner request')
EXEMPT = ('baseline', 'new page', 'factual correction')
SPACING_DAYS = 28
FIELDS = ['date', 'page', 'type', 'fingerprint', 'reason']


def fingerprint(html):
    title = re.search(r'<title>(.*?)</title>', html, re.S)
    desc = re.search(r'<meta name="description" content="(.*?)">', html, re.S)
    main = re.search(r'<main[^>]*>(.*)</main>', html, re.S)
    text = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', main.group(1) if main else ''))
    blob = '\n'.join([title.group(1) if title else '', desc.group(1) if desc else '', text.strip()])
    return hashlib.sha1(blob.encode('utf-8')).hexdigest()[:12]


def tracked(out_dir):
    names = []
    for f in sorted(os.listdir(out_dir)):
        if f.endswith('.html') and f not in ('404.html', 'unavailable.html') and not f.startswith('google'):
            t = open(os.path.join(out_dir, f), encoding='utf-8').read()
            if 'name="robots" content="noindex"' not in t:
                names.append(f)
    return names


def read_rows(path):
    if not os.path.exists(path):
        return []
    with open(path, newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def problems(out_dir, ledger_path):
    rows = read_rows(ledger_path)
    out = []
    for r in rows:
        if r['type'] not in TYPES:
            out.append('unknown change type %r for %s' % (r['type'], r['page']))
    by_page = {}
    for r in rows:
        by_page.setdefault(r['page'], []).append(r)
    for page, rs in by_page.items():
        for prev, cur in zip(rs, rs[1:]):
            gap = (datetime.date.fromisoformat(cur['date']) - datetime.date.fromisoformat(prev['date'])).days
            if cur['type'] not in EXEMPT and gap < SPACING_DAYS:
                out.append('%s changed %d days after its previous change (%s); the rule is %d days unless it is a factual correction' % (page, gap, prev['date'], SPACING_DAYS))
    for name in tracked(out_dir):
        fp = fingerprint(open(os.path.join(out_dir, name), encoding='utf-8').read())
        rs = by_page.get(name)
        if not rs:
            out.append('%s has no ledger row (fingerprint %s)' % (name, fp))
        elif rs[-1]['fingerprint'] != fp:
            out.append('%s changed without a ledger row (was %s, now %s)' % (name, rs[-1]['fingerprint'], fp))
    return out


def check(out_dir, ledger_path):
    p = problems(out_dir, ledger_path)
    assert not p, 'change ledger (seo/changes.csv):\n  ' + '\n  '.join(p) + '\nRecord intended changes: python3 generator/ledger.py record site "<type>" "<reason>"'


def record(out_dir, ledger_path, kind, reason, today=None):
    assert kind in TYPES, kind
    today = today or datetime.date.today().isoformat()
    rows = read_rows(ledger_path)
    last = {}
    for r in rows:
        last[r['page']] = r['fingerprint']
    new = []
    for name in tracked(out_dir):
        fp = fingerprint(open(os.path.join(out_dir, name), encoding='utf-8').read())
        if last.get(name) != fp:
            new.append(dict(date=today, page=name, type=kind if name in last or kind == 'baseline' else 'new page', fingerprint=fp, reason=reason))
    exists = os.path.exists(ledger_path)
    with open(ledger_path, 'a', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, lineterminator='\n')
        if not exists:
            w.writeheader()
        w.writerows(new)
    return new


if __name__ == '__main__':
    if len(sys.argv) >= 5 and sys.argv[1] == 'record':
        here = os.path.dirname(os.path.abspath(__file__))
        rows = record(sys.argv[2], os.path.join(here, '..', 'seo', 'changes.csv'), sys.argv[3], sys.argv[4], *(sys.argv[5:6]))
        print('\n'.join('%(date)s %(page)s %(type)s %(fingerprint)s' % r for r in rows) or 'no changes')
    else:
        print(__doc__)
