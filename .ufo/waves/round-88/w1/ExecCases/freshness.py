#!/usr/bin/env python3
"""Prove every ExecCases extra tuple is absent from the frozen 20-case set.

exit 0 : no extra repeats a frozen (vary, stored, presented) tuple
exit 1 : at least one collision (printed)
"""
import json
import sys
from pathlib import Path

WAVE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88')
FROZEN = json.loads((WAVE / 'vary-cases.json').read_text())
EXTRA = json.loads((WAVE / 'w1/ExecCases/extra-cases.json').read_text())['cases']


def key(c):
    return json.dumps([c['vary'], c['stored'], c['presented']],
                      sort_keys=True, ensure_ascii=False)


frozen_keys = {key(c): c['id'] for c in FROZEN}
hits = [(e['id'], frozen_keys[key(e)]) for e in EXTRA if key(e) in frozen_keys]
print(json.dumps({'extras': len(EXTRA), 'frozen': len(FROZEN),
                  'collisions': hits}, sort_keys=True))
sys.exit(1 if hits else 0)
