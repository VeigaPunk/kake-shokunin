import importlib.util, os, re, hashlib, sys
HERE='/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-59'
spec=importlib.util.spec_from_file_location('qt', os.path.join(HERE,'c59_quote_truth.py'))
qt=importlib.util.module_from_spec(spec); spec.loader.exec_module(qt)
root='/home/vgpnk/Projects/shokunin/kake-shokunin'
body=open(os.path.join(HERE,'sources/S426.html'),'rb').read()
text=re.sub(r'\s+',' ',body.decode('utf-8'))
other=re.sub(r'\s+',' ',open(os.path.join(HERE,'sources/S425.html'),encoding='utf-8',newline='').read())
entry=open('googlebot-verification.md',encoding='utf-8').read()
sid='S426'
fail=[]
print('sha256', hashlib.sha256(body).hexdigest(), 'bytes', len(body))
# C2
lines=entry.splitlines(); head=lines[:8]
for key in ('source','verified-at','recheck'):
    if not any(re.match(rf'^[-* ]*{key} *:\s*\S', ln) for ln in head): fail.append(f'header {key}')
src=next((ln for ln in head if re.match(r'^[-* ]*source *:', ln)),'')
if not re.search(rf'\b{sid}\b', src): fail.append('source lacks id')
if qt.ROW_URL[sid] not in src: fail.append('source lacks url')
if not any(re.search(rf'\b{sid}\b', ln) for ln in lines[8:]): fail.append('no citation below header')
v=next((ln for ln in head if re.match(r'^[-* ]*verified-at *:', ln)),'')
if qt.ROUND_DATE not in v: fail.append('verified-at date')
r=next((ln for ln in head if re.match(r'^[-* ]*recheck *:', ln)),'')
if not re.match(r'^[-* ]*recheck *:\s*(\d+d|\d{4}-\d{2}-\d{2}|on-release)\b', r): fail.append('recheck form')
# row
row = '| S426 | Google for Developers \u2014 Verify Requests from Google Crawlers and Fetchers \u2014 https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests | docs | A | Request verification for Google crawlers and fetchers: the three-category table, the four printed reverse-then-forward DNS steps, and the published IP-range lists | \u00a7 Use command line tools (Last updated 2026-03-20 UTC) | **Reverse DNS then forward DNS** \u2014 the operator\u2019s four printed steps (reverse-resolve the logged IP with `host`, require a name under googlebot.com / google.com / googleusercontent.com, forward-resolve it, require the same IP), three worked `host` examples, and the alternative of matching the IP against the published JSON range lists | mined | 2026-10-27 | 180d | corpus/knowledge/googlebot-verification.md |'
reg = '# SOURCES\n\n## Registry\n\n| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n' + row + '\n'
rows = qt.parse_registry(reg)
print('cells', len(rows[sid]))
cells=rows[sid]
if len(cells)!=11: fail.append(f'row cells {len(cells)}')
if cells[7]!='mined': fail.append('status')
if cells[8]!=qt.ROUND_DATE: fail.append('opened')
if not re.fullmatch(r'(\d{4}-\d{2}-\d{2}|\d+d|on-release)', cells[9]): fail.append('recheck cell')
if qt.row_url(cells)!=qt.ROW_URL[sid]: fail.append('row url')
if cells[2] not in qt.ROW_KINDS or cells[3] not in ('A','B','C'): fail.append('kind/tier')
if len(cells[4])<20 or len(cells[6])<20: fail.append('scope/teaches short')
if any(c.endswith('\\') for c in cells): fail.append('escaped pipe')
print('used_by', qt.used_by(cells[10]), 'want', qt.USED_BY[sid])
if sorted(qt.used_by(cells[10]))!=sorted(qt.USED_BY[sid]): fail.append('used-by')
# title
title=' \u2014 '.join(cells[1].split(' \u2014 ')[1:-1])
page_title=(re.search(r'<title>([^<]*)</title>', text) or [None,''])[1].split(' | ')[0].strip()
print('title', repr(title), 'page_title', repr(page_title), 'units', qt.units(title))
if not title or qt.units(title)<6 or title!=page_title: fail.append('title mismatch')
# anchor
am=re.match(r'^§\s*(.*?)\s*\(Last updated \d{4}-\d{2}-\d{2} UTC\)\s*$', cells[5])
anchor=am.group(1) if am else ''
print('anchor', repr(anchor), 'headings', qt.article_headings(text,sid))
if not am: fail.append('anchor form')
if not anchor or qt.units(anchor)<3 or anchor not in qt.article_headings(text,sid): fail.append('anchor heading')
pub=re.search(r'\(Last updated (\d{4}-\d{2}-\d{2}) UTC\)\s*$', cells[5])
print('date printed in text node:', any(f'Last updated {pub.group(1)} UTC' in s for s in re.findall(r'>([^<>]+)(?=<)', text)))
# C5 quotes
uniq=set(); nquote=0
for ln,line in enumerate(entry.splitlines(),1):
    if qt.CURLY.search(line): fail.append(f'curly line {ln}')
    for span in re.findall(r'"([^"]+)"', line):
        if qt.units(span)<2 and len(span)<12: continue
        nquote+=1
        ok=True
        if qt.units(span)>qt.UNIT_CEILING: fail.append(f'{ln}: {qt.units(span)} units'); ok=False
        if len(span)>qt.CHAR_CEILING: fail.append(f'{ln}: {len(span)} chars'); ok=False
        if span not in text: fail.append(f'{ln}: not raw: {span[:50]!r}'); ok=False
        if not qt.in_content(text,span,sid): fail.append(f'{ln}: outside block: {span[:50]!r}'); ok=False
        if ok and qt.units(span)>=6 and text.count(span)==1 and span not in other: uniq.add(span)
print('quoted spans checked', nquote, 'unique spans', len(uniq))
if len(uniq)<qt.MIN_UNIQUE_SPANS: fail.append('too few unique spans')
if not any('reverse DNS' in u for u in uniq): fail.append('no subject span')
print('SUBJECT span:', [u for u in uniq if 'reverse DNS' in u])
print('FAIL' if fail else 'ALL PASS')
for f in fail: print(' -', f)
