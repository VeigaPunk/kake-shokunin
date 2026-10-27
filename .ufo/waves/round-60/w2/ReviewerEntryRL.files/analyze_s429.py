#!/usr/bin/env python3
"""Independent falsification of corpus/knowledge/robots-txt-limits.md at B1
against .ufo/waves/round-60/sources/S429.html (article block)."""
import re, hashlib, html, json, subprocess, sys

LANE = '/home/vgpnk/Projects/shokunin/kake-shokunin'
B1 = '8b33fd248d126b48d838af5c38bc175850f41a09'
SRC = LANE + '/.ufo/waves/round-60/sources'

def gitshow(path):
    return subprocess.run(['git', '-C', LANE, 'show', B1 + ':' + path],
                          capture_output=True).stdout

entry_bytes = gitshow('corpus/knowledge/robots-txt-limits.md')
entry = entry_bytes.decode('utf-8', 'replace')
w1_bytes = open(LANE + '/.ufo/waves/round-60/w1/EntryRobotsLimits.files/robots-txt-limits.md', 'rb').read()
print('== B1 entry vs w1 staged file identical:', entry_bytes == w1_bytes)
print('== entry lines:', entry_bytes.count(b'\n'))

body = open(SRC + '/S429.html', 'rb').read()
print('== S429 bytes:', len(body), 'sha256:', hashlib.sha256(body).hexdigest())

raw = body.decode('utf-8', 'replace')

def collapse(s):
    return ' '.join(s.split())

def clean(seg):
    seg = re.sub(r'<!--.*?-->', ' ', seg, flags=re.S)
    seg = re.sub(r'<(script|style|template)\b.*?</\1\s*>', ' ', seg, flags=re.S | re.I)
    return seg

def nodes_of(seg):
    out = []
    for part in re.split(r'<[^>]+>', clean(seg)):
        c = collapse(html.unescape(part))
        if c:
            out.append(c)
    return out

ai = raw.find('class="devsite-article-body')
fi = raw.find('<devsite-content-footer')
print('== article marker at', ai, 'footer at', fi)
art = raw[ai:fi]
fend = raw.find('</devsite-content-footer>', fi)
footer = clean(raw[fi:fend]) if fi >= 0 and fend > fi else ''
print('== footer Last updated:', re.findall(r'Last updated[^<]*', footer))
print('== Last updated occurrences in whole page:', len(re.findall(r'Last updated', raw)))

h2s = [collapse(html.unescape(re.sub(r'<[^>]+>', ' ', m)))
       for m in re.findall(r'<h2\b[^>]*>(.*?)</h2\s*>', art, flags=re.S)]
print('== article h2 count:', len(h2s))
for i, h in enumerate(h2s):
    print('   h2[%d] = %r' % (i, h))
h3s = [collapse(html.unescape(re.sub(r'<[^>]+>', ' ', m)))
       for m in re.findall(r'<h3\b[^>]*>(.*?)</h3\s*>', art, flags=re.S)]
print('== article h3 count:', len(h3s))
for h in h3s[:12]:
    print('   h3 = %r' % h)

t = re.search(r'<title>(.*?)</title>', raw, flags=re.S)
print('== title:', collapse(html.unescape(t.group(1))) if t else None)
print('== h1 offsets:', [m.start() for m in re.finditer(r'<h1\b', raw)],
      'first inside article?', [m.start() >= ai for m in re.finditer(r'<h1\b', raw)])

bodies = {}
for sid in ('S427', 'S428', 'S429'):
    b = open(SRC + '/' + sid + '.html', 'rb').read().decode('utf-8', 'replace')
    a = b.find('class="devsite-article-body')
    f = b.find('<devsite-content-footer')
    bodies[sid] = nodes_of(b[a:f])
    print('== %s article nodes: %d' % (sid, len(bodies[sid])))

n429 = bodies['S429']

def occ(span, sid):
    c = collapse(span)
    return sum(node.count(c) for node in bodies[sid])

quotes = re.findall(r'^> "(.+)"\s*$', entry, flags=re.M)
print('== quoted spans in entry:', len(quotes))
for q in quotes:
    c = collapse(q)
    units = len(c.split())
    print('SPAN %2du %3dc s429occ=%d s427=%d s428=%d single-node=%s | %s'
          % (units, len(c), occ(q, 'S429'), occ(q, 'S427'), occ(q, 'S428'),
             any(c in node for node in n429), c[:72]))

alltext = collapse(' '.join(n429))
low = alltext.lower()
print('== negative-word counts in S429 ARTICLE text:')
for w in ['baidu', 'yahoo', 'prefix', 'wildcard', 'user-agent', 'dns', 'noindex',
          'unavailable', 'server error', 'anchor text', 'cannot fetch', 'googlebot']:
    print('   %-14s -> %d' % (w, low.count(w)))
rawall = collapse(html.unescape(clean(raw))).lower()
for w in ['baidu', 'yahoo', 'noindex', 'wildcard']:
    print('   (whole raw page) %-10s -> %d' % (w, rawall.count(w)))

def dump(sub):
    hits = [n for n in n429 if sub in n]
    for n in hits:
        print('   NODE: %s' % n)

print('== full nodes around key sentences:')
for sub in ['cannot enforce', 'may not be supported by all search engines',
            'its URL can still appear', 'hide the page completely',
            'Before you create or edit', 'Different crawlers interpret']:
    print(' -- %r' % sub)
    dump(sub)

print('== node ORDER for limits-section claims:')
for sub in ['Understand the limitations', 'What is a robots.txt file used for',
            'Before you create or edit', 'may not be supported',
            'cannot enforce', "it's up to the crawler", 'While Googlebot',
            'password-protecting', 'Although respectable',
            'some might not understand', 'A page that', 'we might still find',
            'its URL can still appear', "This won't prevent"]:
    idx = [i for i, n in enumerate(n429) if sub in n]
    print('   %-40s nodes %s' % (sub, idx))

print('== tables in article:')
for m in re.finditer(r'<table\b.*?</table\s*>', art, flags=re.S):
    print('   table at art-offset %d: %s' % (m.start(), collapse(html.unescape(
        re.sub(r'<[^>]+>', ' ', m.group(0))))[:400]))
qidx = alltext.find("This won't prevent")
print('== "This won\'t prevent" alltext offset:', qidx, 'of', len(alltext))

# recheck predicate
gr = subprocess.run(['grep', '-F', '-c',
                     'Different crawlers interpret syntax differently.',
                     SRC + '/S429.html'], capture_output=True)
print('== recheck grep -F -c exit=%d stdout=%s' % (gr.returncode, gr.stdout.decode().strip()))

# SOURCES.md row S429 at B1
srcs = gitshow('corpus/SOURCES.md').decode('utf-8', 'replace')
for line in srcs.splitlines():
    if re.match(r'^\| S42[789] \|', line):
        cells = [c.strip() for c in line.split('|')[1:-1]]
        print('== row %s: %d cells' % (cells[0], len(cells)))
        for i, c in enumerate(cells):
            print('   cell[%d] = %s' % (i, c[:110]))

# inventory at B1
ls = subprocess.run(['git', '-C', LANE, 'ls-tree', '-r', '--name-only', B1,
                     '--', 'corpus/knowledge/'], capture_output=True)
names = ls.stdout.decode().splitlines()
print('== knowledge files at B1 matching robots/google-user:')
for n in names:
    if 'robots' in n or 'google-user' in n:
        print('   ', n)
print('== staged name present at B1:',
      any(n.endswith('google-robots-txt-limits.md') for n in names))

# receipts
rec = json.load(open(SRC + '/receipts.json'))
items = rec if isinstance(rec, list) else rec.get('receipts', rec.get('sources', []))
if isinstance(items, dict):
    items = list(items.values())
for it in items:
    u = it.get('url', '') if isinstance(it, dict) else ''
    if 'robots/intro' in u or it.get('id') == 'S429' if isinstance(it, dict) else False:
        print('== receipt:', json.dumps(it, sort_keys=True)[:500])

# refused-phrase greps in B1 entry
print('== refused phrases in B1 entry (all must be 0):')
for pat in [r'its own way', r'may access', r'expected one', r'real protection',
            r'behaviour', r'three directions', r'tradition', r'ran 2026-10-24',
            r"this operator's", r'google-robots-txt-limits', r'S415']:
    print('   %-24s -> %d' % (pat, len(re.findall(pat, entry))))
print('== ground: line:', [l for l in entry.splitlines() if l.startswith('ground:')])
