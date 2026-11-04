#!/usr/bin/env python3
"""Read actual round-82 retained publisher fields; no fetch or cache approval."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--root', type=Path, required=True)
a = p.parse_args()
rows = []
for surface in ('ds4cc-primary', 'ds4cc-robots', 'ds4cc-sitemap'):
    rel = Path('.ufo/waves/round-82/capture') / surface / 'response.json'
    raw = (a.root / rel).read_bytes()
    response = json.loads(raw)
    headers = response['headers']
    def fields(name):
        return [h['value'] for h in headers if h['name'].lower() == name]
    dates, expires = fields('date'), fields('expires')
    payload = {'cache_control': fields('cache-control'), 'shared': True,
               'date': dates[0] if dates else None,
               'expires': expires[0] if expires else None}
    result = subprocess.run([sys.executable, '-B', str(a.root / 'scripts/cache_control_effective.py')],
                            input=json.dumps(payload), capture_output=True, text=True, check=False)
    if result.returncode:
        raise SystemExit(f'{surface}: reader exit {result.returncode}: {result.stderr}')
    rows.append({'surface': surface, 'retained_input': str(rel),
                 'sha256': hashlib.sha256(raw).hexdigest(), 'fetchedAt': response['fetchedAt'],
                 'input': payload, 'reader_exit': result.returncode, 'output': json.loads(result.stdout)})
print(json.dumps({'trigger': 'Publisher needs a bounded interpretation of retained Cache-Control fields',
                  'action': 'Read ordered response fields from three real round-82 retained captures and invoke the reader',
                  'outcome': rows,
                  'handoff': 'Operator: these are historical metadata observations, not current freshness, storage permission, browser behavior or deployment approval',
                  'live_requests': 0}, indent=1))
