#!/usr/bin/env python3
import re, html

SRC = '/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-60/sources'
raw = open(SRC + '/S429.html', encoding='utf-8', errors='replace').read()

def collapse(s):
    return ' '.join(s.split())

def clean(seg):
    seg = re.sub(r'<!--.*?-->', ' ', seg, flags=re.S)
    seg = re.sub(r'<(script|style|template)\b.*?</\1\s*>', ' ', seg, flags=re.S | re.I)
    return seg

ai = raw.find('class="devsite-article-body')
fi = raw.find('<devsite-content-footer')
art = raw[ai:fi]

nodes = []
for part in re.split(r'<[^>]+>', clean(art)):
    c = collapse(html.unescape(part))
    if c:
        nodes.append(c)

print('== nodes 12-38 (first section incl. table):')
for i in range(12, 39):
    print('  [%2d] %s' % (i, nodes[i]))
print('== nodes 39-58 (limits + next h2):')
for i in range(39, min(59, len(nodes))):
    print('  [%2d] %s' % (i, nodes[i]))

print('== key-node indices:')
for sub in ['it is not a mechanism', 'If you want to hide', 'noindex', 'anchor text',
            'remove the page', 'password-protect', 'A robots.txt file tells',
            'Create or update']:
    print('  %-28s -> %s' % (sub, [i for i, n in enumerate(nodes) if sub.lower() in n.lower()]))

print('== table regions (row by row):')
for ti, m in enumerate(re.finditer(r'<table\b.*?</table\s*>', art, flags=re.S)):
    print(' table %d at art-offset %d..' % (ti, m.start()))
    for ri, row in enumerate(re.findall(r'<tr\b.*?</tr\s*>', m.group(0), flags=re.S)):
        cells = [' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', c)).split())
                 for c in re.findall(r'<t[dh]\b.*?</t[dh]\s*>', row, flags=re.S)]
        for ci, c in enumerate(cells):
            print('   r%d c%d: %s' % (ri, ci, c))

print('== raw HTML around "its URL can still appear":')
k = art.find('its URL can still appear')
print(art[max(0, k - 900):k + 400].replace('\n', ' '))
print('== raw HTML around "If you want to hide":')
k2 = art.find('If you want to hide')
print(art[max(0, k2 - 200):k2 + 700].replace('\n', ' '))
print('== raw HTML around "anchor text":')
k3 = art.find('anchor text')
print(art[max(0, k3 - 700):k3 + 300].replace('\n', ' '))
