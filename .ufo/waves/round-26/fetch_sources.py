#!/usr/bin/env python3
"""Re-open each external SOURCES row with one public GET per URL; retain gzip bytes.

Read-only toward the network target: plain GET of the public documentation URL
already recorded in corpus/SOURCES.md, no credentials, cookies or forms.
Writes only beneath --out. Output manifest records status, final URL, selected
headers, fetch time and SHA-256 of the exact received body bytes.
"""
import argparse
import datetime
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

EXCLUDED = {'S014', 'S019', 'S035'}  # own-work rows and the source opened last round
HEADERS = ('content-type', 'last-modified', 'etag', 'date', 'content-length')


def rows(sources):
    for line in sources.read_text(encoding='utf-8').splitlines():
        if not re.match(r'^\|\s*S\d{3,}\s*\|', line):
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if cells[0] in EXCLUDED:
            continue
        urls = re.findall(r'https?://[^\s;|]+', cells[1])
        yield cells[0], urls


def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'kake-shokunin-source-recheck/26 (+GET only)'})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read()
            return response.status, response.geturl(), {k: response.headers.get(k) for k in HEADERS}, body
    except urllib.error.HTTPError as error:
        return error.code, url, {k: error.headers.get(k) for k in HEADERS}, error.read()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    manifest = []
    for row, urls in rows(args.root / 'corpus/SOURCES.md'):
        for index, url in enumerate(urls, 1):
            started = datetime.datetime.now(datetime.timezone.utc).isoformat()
            try:
                status, final, headers, body = fetch(url)
                error = None
            except Exception as exc:  # recorded, never hidden
                status, final, headers, body, error = None, url, {}, b'', f'{type(exc).__name__}: {exc}'
            name = f'{row}-{index}.raw.gz'
            (args.out / name).write_bytes(gzip.compress(body, mtime=0))
            manifest.append({'row': row, 'index': index, 'url': url, 'finalUrl': final,
                             'status': status, 'error': error, 'fetchedAt': started,
                             'headers': headers, 'bytes': len(body),
                             'sha256': hashlib.sha256(body).hexdigest(), 'file': name})
            print(row, index, status, len(body), error or '', file=sys.stderr)
    (args.out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
