#!/usr/bin/env python3
"""Count the source registry at two explicit revisions without executing gates."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess


def registry(root, revision):
    raw = subprocess.run(['git', '--no-replace-objects', '-C', str(root), 'show',
        revision + ':corpus/SOURCES.md'], capture_output=True, check=True).stdout.decode()
    rows = {}
    for line in raw.splitlines():
        if re.match(r'^\|\s*S\d{3,}\s*\|', line):
            cells = [part.strip() for part in line.split('|')[1:-1]]
            if len(cells) != 11 or cells[0] in rows:
                raise ValueError('invalid source registry row')
            rows[cells[0]] = (cells, line)
    return rows


def stats(rows):
    return {'rows': len(rows), 'tiers': dict(Counter(r[0][3] for r in rows.values())),
            'statuses': dict(Counter(r[0][7] for r in rows.values()))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--before', required=True)
    parser.add_argument('--after', required=True)
    args = parser.parse_args()
    before, after = registry(args.root, args.before), registry(args.root, args.after)
    changed = [key for key in before if key not in after or before[key][1] != after[key][1]]
    print(json.dumps({'beforeRevision': args.before, 'afterRevision': args.after,
        'before': stats(before), 'after': stats(after), 'priorRowsChanged': changed,
        'added': sorted(set(after) - set(before))}, sort_keys=True))
    return 1 if changed else 0


if __name__ == '__main__':
    raise SystemExit(main())
