#!/usr/bin/env python3
"""Self-contained span checker for the round-61 C2 entry draft (ScribeC2Entry).

    python3 -B .ufo/waves/round-61/w1/ScribeC2Entry.files/quote_check.py [--json]

Reads the retained bodies `.ufo/waves/round-61/sources/S430.html` .. `S433.html` and the draft
`.ufo/waves/round-61/w1/ScribeC2Entry.files/entry.md`, extracts every double-quoted span of the
draft, and requires, for each span: (a) exactly one of the four bodies contains it, (b) it is a
substring of one whitespace-collapsed text node under BOTH a HTMLParser reader (character
references decoded, script/style skipped) and a `>[^<>]+<` regex reader (raw text, no entity
decoding), (c) it occurs exactly once in that body's whitespace-collapsed bytes, (d) 6..25
whitespace units and <= 160 characters, (e) no curly double quote. Exit 0 all spans pass, 1 a
span fails, 2 an input file is missing.
"""
import json
import os
import re
import sys
from html.parser import HTMLParser

LANE = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..'))
SRC = os.path.join(LANE, '.ufo', 'waves', 'round-61', 'sources')
ENTRY = os.path.join(LANE, '.ufo', 'waves', 'round-61', 'w1', 'ScribeC2Entry.files', 'entry.md')
IDS = ('S430', 'S431', 'S432', 'S433')


def nodes_parser(path):
    class P(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.out, self.skip = [], 0

        def handle_starttag(self, tag, attrs):
            if tag in ('script', 'style'):
                self.skip += 1

        def handle_endtag(self, tag):
            if tag in ('script', 'style') and self.skip:
                self.skip -= 1

        def handle_data(self, data):
            if not self.skip:
                c = ' '.join(data.split())
                if c:
                    self.out.append(c)

    p = P()
    with open(path, encoding='utf-8', errors='replace') as fh:
        p.feed(fh.read())
    return p.out


def nodes_regex(path):
    with open(path, encoding='utf-8', errors='replace') as fh:
        raw = fh.read()
    raw = re.sub(r'(?is)<(style|script)\b.*?</\1>', '<>', raw)
    out = []
    for seg in re.findall(r'>([^<>]+)(?=<)', raw):
        c = ' '.join(seg.split())
        if c:
            out.append(c)
    return out


def main():
    as_json = '--json' in sys.argv
    try:
        bodies = {i: open(os.path.join(SRC, f'{i}.html'), encoding='utf-8', errors='replace').read() for i in IDS}
        entry = open(ENTRY, encoding='utf-8').read()
    except OSError as exc:
        print(f'could not read input: {exc}', file=sys.stderr)
        return 2
    parsed = {i: nodes_parser(os.path.join(SRC, f'{i}.html')) for i in IDS}
    regexed = {i: nodes_regex(os.path.join(SRC, f'{i}.html')) for i in IDS}
    collapsed = {i: ' '.join(bodies[i].split()) for i in IDS}

    rows = []
    ok = True
    for span in re.findall(r'"([^"\n]+)"', entry):
        q = ' '.join(span.split())
        hits = []
        for i in IDS:
            if any(q in n for n in parsed[i]) or any(q in n for n in regexed[i]) or collapsed[i].count(q):
                hits.append({
                    'row': i,
                    'in_parser_node': any(q in n for n in parsed[i]),
                    'in_regex_node': any(q in n for n in regexed[i]),
                    'occurrences': collapsed[i].count(q),
                })
        row = {
            'quote': q,
            'units': len(q.split()),
            'chars': len(q),
            'rows': hits,
            'curly': bool(re.search('[\u201c\u201d\u201e\u201f]', q)),
        }
        row['accepted'] = bool(
            len(hits) == 1 and hits[0]['in_parser_node'] and hits[0]['in_regex_node']
            and hits[0]['occurrences'] == 1 and 6 <= row['units'] <= 25
            and row['chars'] <= 160 and not row['curly']
        )
        ok = ok and row['accepted']
        rows.append(row)

    doc = {'entry': ENTRY, 'span_count': len(rows), 'all_ok': ok, 'spans': rows}
    if as_json:
        print(json.dumps(doc, indent=1, ensure_ascii=False))
    else:
        for r in rows:
            print(f"{r['rows'][0]['row'] if len(r['rows']) == 1 else '??'} "
                  f"{r['units']:2d}u {r['chars']:3d}c "
                  f"node={r['rows'][0]['in_parser_node'] and r['rows'][0]['in_regex_node'] if len(r['rows']) == 1 else False} "
                  f"unique={r['rows'][0]['occurrences'] == 1 if len(r['rows']) == 1 else False} "
                  f"accept={r['accepted']} :: {r['quote'][:80]}")
        print(f'spans={len(rows)} all_ok={ok}')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
