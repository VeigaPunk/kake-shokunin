#!/usr/bin/env python3
"""Local-loopback regression checks for snapshot confinement and re-audit integrity.

snapshot_probe.py --snapshot-script PATH --validator PATH
All files are temporary; the server accepts GET only. A passing result means
normal capture/re-audit work, forbidden output leaves do not change the outside
sentinel, edited/missing snapshots fail with exit 2, and a blocked redirect is
not misreported as an observed destination. No public URLs are contacted.
"""
import argparse
import http.server
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/blocked':
            self.send_response(302)
            self.send_header('Location', 'file:///unfetched/local-sentinel')
            self.end_headers()
            return
        body = f"<head><link rel=canonical href='http://127.0.0.1:{self.server.server_port}/'></head><body></body>".encode()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--snapshot-script', required=True)
    parser.add_argument('--validator', required=True)
    args = parser.parse_args()
    script, validator = map(os.path.abspath, (args.snapshot_script, args.validator))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    rows = []
    with tempfile.TemporaryDirectory(prefix='kake-r23-snapshot-probe-') as scratch:
        root = Path(scratch)
        url = f'http://127.0.0.1:{server.server_port}/'

        def invoke(name, *, reaudit=False, location=None, surface_id='page'):
            pop = root / f'{name}.json'
            pop.write_text(json.dumps({'surfaces': [{'id': surface_id, 'url': location or url, 'expectedCanonical': url}]}))
            argv = [sys.executable, '-B', script, '--population', str(pop), '--out', str(root / name), '--validator', validator]
            if reaudit:
                argv.append('--reaudit')
            done = subprocess.run(argv, capture_output=True, text=True, timeout=30)
            return done.returncode, done.stdout

        code, output = invoke('normal')
        rows.append({'case': 'normal', 'exit': code, 'ok': code == 0})
        code, output = invoke('normal', reaudit=True)
        rows.append({'case': 'reaudit-unaltered', 'exit': code, 'ok': code == 0})
        for name, hard in [('symlink-leaf', False), ('hardlink-leaf', True)]:
            directory = root / name / 'page'
            directory.mkdir(parents=True)
            outside = root / f'{name}-outside'
            outside.write_text('UNCHANGED')
            if hard:
                os.link(outside, directory / 'fetch.json')
            else:
                (directory / 'fetch.json').symlink_to(outside)
            code, output = invoke(name)
            unchanged = outside.read_text() == 'UNCHANGED'
            rows.append({'case': name, 'exit': code, 'outsideUnchanged': unchanged, 'ok': code == 2 and unchanged})
        for name in ['edited-page', 'edited-digest', 'missing-page', 'missing-fetch', 'edited-final-url', 'array-metadata', 'content-type-metadata']:
            code, output = invoke(name)
            directory = root / name / 'page'
            if name == 'edited-page':
                (directory / 'page.html').write_text('<head></head>')
            elif name in {'edited-digest', 'edited-final-url', 'array-metadata', 'content-type-metadata'}:
                meta = json.loads((directory / 'fetch.json').read_text())
                if name == 'edited-digest':
                    meta['sha256'] = '0' * 64
                elif name == 'edited-final-url':
                    meta['finalUrl'] = url + 'different-base/'
                elif name == 'content-type-metadata':
                    meta['contentType'] = 123
                else:
                    meta = []
                (directory / 'fetch.json').write_text(json.dumps(meta))
            else:
                (directory / ('page.html' if name == 'missing-page' else 'fetch.json')).unlink()
            code, output = invoke(name, reaudit=True)
            error = json.loads(output).get('error') if code == 2 else None
            ok = code == 2 and (name != 'content-type-metadata' or error == 'snapshot contentType must be a string or null')
            rows.append({'case': name, 'exit': code, 'error': error, 'ok': ok})
        code, output = invoke('blocked', location=url + 'blocked')
        meta = json.loads((root / 'blocked/page/fetch.json').read_text())
        rows.append({'case': 'blocked-redirect-url', 'exit': code, 'finalUrl': meta['finalUrl'],
                     'ok': meta['finalUrl'] == url + 'blocked' and bool(meta.get('error'))})
    server.shutdown()
    server.server_close()
    passed = all(row['ok'] for row in rows)
    print(json.dumps({'script': script, 'passed': passed, 'met': sum(r['ok'] for r in rows), 'total': len(rows), 'cases': rows}, indent=1))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
