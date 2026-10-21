#!/usr/bin/env python3
"""Post-hoc committed copy of the inline S008 retry the L1 ran on 2026-10-21.

The original command was a bash heredoc (python3 -B -) run from the lane root
right after fetch_sources.py reported `S008 1 None 0 TimeoutError` at the 60 s
timeout. Its logic is reproduced here verbatim except for the argparse wrapper;
it was NOT this file that produced manifest-retry.json, and running it again
overwrites S008-1-retry.raw.gz with whatever the server returns now.
One public GET, 240 s timeout, same User-Agent and header projection.
"""
import datetime
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import urllib.request

HERE = Path(__file__).resolve().parent
URL = 'https://cgit.git.savannah.gnu.org/cgit/tar.git/plain/doc/tar.texi?id=cfdb891bbd68c920ea75210977593f3cd08f0418'


def main():
    spec = importlib.util.spec_from_file_location('f', HERE / 'fetch_sources.py')
    f = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(f)
    out = HERE / 'fetched'
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    req = urllib.request.Request(URL, headers={'User-Agent': 'kake-shokunin-source-recheck/26 (+GET only)'})
    try:
        with urllib.request.urlopen(req, timeout=240) as r:
            body = r.read(); status = r.status; final = r.geturl()
            headers = {k: r.headers.get(k) for k in f.HEADERS}; err = None
    except Exception as e:
        body = b''; status = None; final = URL; headers = {}; err = f'{type(e).__name__}: {e}'
    (out / 'S008-1-retry.raw.gz').write_bytes(gzip.compress(body, mtime=0))
    rec = {'row': 'S008', 'index': 1, 'attempt': 2, 'url': URL, 'finalUrl': final, 'status': status,
           'error': err, 'fetchedAt': started, 'headers': headers, 'bytes': len(body),
           'sha256': hashlib.sha256(body).hexdigest(), 'file': 'S008-1-retry.raw.gz',
           'reason': 'first attempt TimeoutError at 60s; single retry with 240s timeout'}
    (out / 'manifest-retry.json').write_text(json.dumps([rec], indent=2) + '\n')
    print(status, len(body), err)


if __name__ == '__main__':
    main()
