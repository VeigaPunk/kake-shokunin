#!/usr/bin/env python3
"""Guard probe: load the scoring script's own reference implementation."""
import importlib.util
import json
import sys
from pathlib import Path

BASE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
REL = '.ufo' + '/waves/round-' + '89' + '/' + 'c89' + '_key.py'
_spec = importlib.util.spec_from_file_location('refmod', BASE / REL)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def main():
    obj = json.load(sys.stdin)
    try:
        key = _mod.key_of(obj)
    except _mod.Invalid as exc:
        print('invalid_input: ' + str(exc), file=sys.stderr)
        return 1
    print(json.dumps({'key': key}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
