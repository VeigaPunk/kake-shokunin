#!/usr/bin/env python3
"""Independent derivation of the C1 population from a SKILL.md, per contract §C1.

Written from the contract sentence, not from c75_row_truth.py, then diffed
against both the contract's frozen 16-file list and the counter's --json output.

Rule (contract §C1): each live registry row — a table row inside a section
titled `### Round <N> gate registry additions` whose Kind cell lacks the
`historical` qualifier — resolves to one instrument file:
  the Name cell when it is itself a .py/.mjs path,
  else the first .py/.mjs token of the Entry-command cell,
  else of the Self-test cell, else of any cell.
"""
import re
import sys

SEC = re.compile(r'^### Round (\d+) gate registry additions')
TOKEN = re.compile(r'(?:scripts|\.ufo)/[A-Za-z0-9_./-]+\.(?:py|mjs)')


def cells_of(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def derive(text):
    rows, sec = [], None
    for lineno, line in enumerate(text.splitlines(), 1):
        m = SEC.match(line)
        if m:
            sec = int(m.group(1))
            continue
        if line.startswith('### '):
            sec = None
            continue
        if sec and line.startswith('| ') and line.count('|') >= 6:
            cs = cells_of(line)
            if cs[0] == 'Name' or set(cs[0]) <= set('-: '):
                continue
            rows.append({'lineno': lineno, 'section': sec, 'cells': cs})

    live = [r for r in rows if 'historical' not in r['cells'][1]]

    def instrument(r):
        c = r['cells']
        if TOKEN.fullmatch(c[0]):
            return c[0]
        for idx in (2, 4):
            m = TOKEN.search(c[idx])
            if m:
                return m.group(0)
        m = TOKEN.search(' | '.join(c))
        return m.group(0) if m else None

    groups = {}
    for r in live:
        f = instrument(r)
        r['file'] = f
        if f:
            groups.setdefault(f, []).append(r)
    return rows, live, groups


def main():
    path = sys.argv[1]
    with open(path, encoding='utf-8') as fh:
        text = fh.read()
    rows, live, groups = derive(text)
    print(f'total_rows={len(rows)} live_rows={len(live)} files={len(groups)}')
    for f in sorted(groups):
        eff = groups[f][-1]
        hist = sum(1 for r in groups[f] if r is not eff)
        print(f'{f}\teffective_row_line={eff["lineno"]}\tsection=r{eff["section"]}\tsuperseded={hist}')


if __name__ == '__main__':
    main()
