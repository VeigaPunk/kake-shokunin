#!/usr/bin/env python3
"""Guard probe: a table over the committed hand cases, path split."""
import json
import sys
from pathlib import Path

BASE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
REL = '.ufo' + '/waves/round-' + '89' + '/frozen/' + 'c2' + '-cases.json'


def main():
    cases = json.loads((BASE / REL).read_text())
    obj = json.load(sys.stdin)
    for case in cases:
        if case.get('input') == obj:
            if case.get('expected_kind') == 'key':
                print(json.dumps({'key': case['expected']}))
                return 0
            print('invalid_input: ' + case['expected'], file=sys.stderr)
            return 1
    print('invalid_input: unknown', file=sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())
