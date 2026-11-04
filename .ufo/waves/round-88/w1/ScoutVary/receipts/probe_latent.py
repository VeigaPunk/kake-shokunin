#!/usr/bin/env python3
"""ScoutVary: probe the L1 candidate (committed at v3) and the counter's own
reference on the profile branches the frozen 20 and the seeded 200 never
exercise, to see whether the counter could even detect a divergence there."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
SCRATCH = Path('/fast/scratch/hyaku/kake-r88/ScoutVary')
TOOL = LANE / '.ufo/waves/round-88/w1/L1/vary_match.py'

spec = importlib.util.spec_from_file_location('ctr', LANE / '.ufo/waves/round-88/c88_vary.py')
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)

PROBES = [
    ('case-variant duplicate field name in one request (RFC 9110 5.2 combines)',
     {'vary': 'accept-encoding', 'stored': {'accept-encoding': 'gzip', 'Accept-Encoding': 'br'},
      'presented': {'accept-encoding': 'gzip, br'}}),
    ('Vary member carrying a trailing LF (RFC 9110 5.6.2 token / 5.5 CR-LF)',
     {'vary': 'gzip\n', 'stored': {'gzip': 'v'}, 'presented': {'gzip': 'v'}}),
    ('Vary with an empty list element (RFC 9110 5.6.1.2 recipients MUST ignore)',
     {'vary': 'accept-encoding,', 'stored': {'accept-encoding': 'gzip'},
      'presented': {'accept-encoding': 'gzip'}}),
    ('empty Vary value', {'vary': '', 'stored': {}, 'presented': {}}),
    ('value list combined with ", " (RFC 9110 5.3 use comma SP)',
     {'vary': 'accept-encoding', 'stored': {'accept-encoding': 'gzip, br'},
      'presented': {'accept-encoding': ['gzip', 'br']}}),
    ('value list combined with "," (no SP)',
     {'vary': 'accept-encoding', 'stored': {'accept-encoding': 'gzip,br'},
      'presented': {'accept-encoding': ['gzip', 'br']}}),
]

def run_tool(payload):
    p = subprocess.run([sys.executable, '-B', str(TOOL)], input=json.dumps(payload),
                       capture_output=True, text=True, timeout=20)
    return p.returncode, p.stdout.strip(), p.stderr.strip()[:60]

for label, payload in PROBES:
    ref = ctr.reference(payload['vary'], payload['stored'], payload['presented'])
    rc, out, err = run_tool(payload)
    cand = 'invalid' if rc == 1 else out
    agree = (ref == 'invalid' and rc == 1) or (ref == out and rc == 0)
    print(f'{"AGREE" if agree else "DIVERGE"}  reference={ref:9s} candidate={cand:9s}  {label}')
