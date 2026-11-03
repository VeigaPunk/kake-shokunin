#!/usr/bin/env python3
import collections
import hashlib
import json
import os
import subprocess

lane = '/home/vgpnk/Projects/shokunin/kake-shokunin'
base = 'ced2878a1e77f57afb4ee3baebf1021e5130399b'
raw = subprocess.run(['git', '-C', lane, 'show', base + ':corpus/knowledge/freshness-sidecar.json'], check=True, capture_output=True, text=True).stdout
entries = json.loads(raw)['entries']
rows = []
for index, entry in enumerate(entries):
    try:
        os.stat(os.path.expanduser(entry['token']))
        state = 'present'
    except (FileNotFoundError, NotADirectoryError):
        state = 'absent'
    except OSError as error:
        state = type(error).__name__
    rows.append(dict(index=index, file=entry['file'], line=entry['line'], token=entry['token'], kind=entry['kind'], state=state))
counts = collections.Counter((row['kind'], row['state']) for row in rows)
indices = sorted(range(len(rows)), key=lambda i: hashlib.sha256(('ReviewerC2-r74:' + str(i)).encode()).digest())[:20]
print(json.dumps(dict(entries=len(rows), counts={str(k): v for k, v in counts.items()}, remaining=[row for row in rows if row['kind'] == 'absent' and row['state'] == 'absent'], sample=[rows[i] for i in indices]), indent=2))
