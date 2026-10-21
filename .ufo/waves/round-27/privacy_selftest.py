#!/usr/bin/env python3
"""Offline privacy-boundary selftest for the round-27 source capture.

Synthetic, non-secret fixtures only: a public HTML page whose markup carries a
sentinel hidden-input value, a sentinel attribute value and a sentinel script
body next to ordinary public prose, plus a plaintext code file. The cases pin
the retention boundary of ``fetch_group.py``:

  * an HTML response is retained as its public visible text: the prose survives
    and every sentinel (hidden form value, attribute value, script body) is gone;
  * a code/plaintext response is retained byte for byte;
  * ``--sanitize-existing`` migrates an own fetched directory offline, keeps the
    original received digest and observations, drops the replaced own filename and
    is idempotent: a second run leaves the manifest and the retained bytes
    unchanged, and touches no path outside its own fetched directory.

No network access, no credentials, no real token values. Writes only under a
scratch directory; prints one JSON summary; exit 0 when every case passes.
"""
import contextlib
import gzip
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SCRATCH = pathlib.Path(os.environ.get('KAKE_R27_SCRATCH', '/fast/scratch/hyaku/kake-r27/PrivacyBoundary'))

SENTINEL_FORM = 'SENTINEL-HIDDEN-INPUT-VALUE'
SENTINEL_ATTR = 'SENTINEL-ATTRIBUTE-VALUE'
SENTINEL_SCRIPT = 'SENTINEL-SCRIPT-BODY'
SENTINEL = 'SENTINEL'
PROSE = 'Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact'

HTML = (
    '<!DOCTYPE html>\n<html lang="en"><head><title>Release notes</title>\n'
    '<script>var sessionSecret = "' + SENTINEL_SCRIPT + '";</script>\n'
    '</head><body>\n'
    '<form action="/session" method="post">'
    '<input type="hidden" name="authenticity_token" value="' + SENTINEL_FORM + '">'
    '<input type="hidden" name="csrf_token" value="' + SENTINEL + '-CSRF">'
    '<button data-session-id="' + SENTINEL_ATTR + '">Sign in</button>'
    '</form>\n'
    '<h1>Public release notes</h1>\n'
    '<p>' + PROSE + '.</p>\n'
    '</body></html>\n'
).encode('utf-8')

CODE = b"name: 'Upload Pages Artifact'\ndescription: 'Uploads a Pages artifact'\ninputs:\n  path: 'dist'\n"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scratch_dir():
    """A scratch directory outside /tmp and /dev/shm."""
    try:
        SCRATCH.mkdir(parents=True, exist_ok=True)
        return SCRATCH / ('privacy-selftest-{}'.format(os.getpid()))
    except OSError:
        return pathlib.Path(os.environ.get('TMPDIR', '/tmp')) / ('privacy-selftest-{}'.format(os.getpid()))


def build_fixture(root):
    """A synthetic own r27 fetched directory holding one unfiltered HTML capture."""
    fetched = root / '.ufo/waves/round-27/fetched'
    (fetched / 'text').mkdir(parents=True, exist_ok=True)
    body = HTML
    (fetched / 'S002-1.raw.gz').write_bytes(gzip.compress(body, mtime=0))
    entry = {
        'row': 'S002',
        'index': 1,
        'url': 'https://example.test/releases/tag/v1',
        'finalUrl': 'https://example.test/releases/tag/v1',
        'status': 200,
        'error': None,
        'fetchedAt': '2026-10-20T12:00:00+00:00',
        'bytes': len(body),
        'sha256': hashlib.sha256(body).hexdigest(),
        'file': 'S002-1.raw.gz',
        'text': 'text/S002-1.txt',
    }
    (fetched / 'manifest.json').write_text(json.dumps([entry], indent=2) + '\n', encoding='utf-8')
    return fetched


def main():
    fetch_group = load('r27_fetch_group', HERE / 'fetch_group.py')
    source_text = fetch_group.load_source_text(ROOT)
    cases = []

    def record(name, passed, detail):
        cases.append({'case': name, 'passed': bool(passed), 'detail': detail})

    # 1. an HTML body keeps its public prose and loses every form/attribute/script value
    kind, retained = fetch_group.classify('https://example.test/releases/tag/v1', 'text/html; charset=utf-8',
                                          HTML, source_text)
    text = retained.decode('utf-8')
    record('html_retained_as_visible_text',
           kind == fetch_group.KIND_PUBLIC and PROSE in text and SENTINEL not in text,
           {'kind': kind, 'proseKept': PROSE in text, 'sentinelRemoved': SENTINEL not in text,
            'scriptTagRemoved': '<script' not in text, 'formInputRemoved': 'authenticity_token' not in text,
            'retainedBytes': len(retained)})
    record('html_fixture_carried_the_sentinel_before_filtering',
           SENTINEL in HTML.decode('utf-8'), {'fixtureIsMeaningful': SENTINEL in HTML.decode('utf-8')})

    # 2. an HTML body without a content type is still filtered (sniffed like the round-26 helper)
    kind2, retained2 = fetch_group.classify('https://example.test/releases/tag/v1', None, HTML, source_text)
    record('html_without_content_type_is_filtered',
           kind2 == fetch_group.KIND_PUBLIC and SENTINEL not in retained2.decode('utf-8')
           and PROSE in retained2.decode('utf-8'),
           {'kind': kind2, 'sentinelRemoved': SENTINEL not in retained2.decode('utf-8')})

    # 3. a code/plaintext response is retained byte for byte
    kind3, retained3 = fetch_group.classify(
        'https://raw.githubusercontent.com/example/example/0123/action.yml', 'text/plain; charset=utf-8',
        CODE, source_text)
    record('code_bytes_retained_unchanged',
           kind3 == fetch_group.KIND_SOURCE and retained3 == CODE,
           {'kind': kind3, 'identical': retained3 == CODE, 'retainedBytes': len(retained3)})

    work = scratch_dir()
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    try:
        root = work / 'repo'
        fetched = build_fixture(root)
        # an unrelated neighbouring wave must not be touched
        neighbour = root / '.ufo/waves/round-26/fetched/S002-1.raw.gz'
        neighbour.parent.mkdir(parents=True, exist_ok=True)
        neighbour.write_bytes(gzip.compress(b'round-26 payload\n', mtime=0))
        neighbour_before = neighbour.read_bytes()

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            fetch_group.sanitize_existing(root, source_text)
        printed = stdout.getvalue()
        manifest_text = (fetched / 'manifest.json').read_text(encoding='utf-8')
        manifest = json.loads(manifest_text)
        entry = manifest[0]
        retained_file = fetched / entry['file']
        retained_bytes = gzip.decompress(retained_file.read_bytes())
        sidecar = fetched / 'text/S002-1.txt'

        record('sanitize_filters_html_and_replaces_own_file',
               SENTINEL not in retained_bytes.decode('utf-8') and PROSE in retained_bytes.decode('utf-8')
               and not (fetched / 'S002-1.raw.gz').exists() and retained_file.is_file()
               and sidecar.is_file() and sidecar.read_bytes() == retained_bytes,
               {'retainedFile': entry['file'], 'oldFileRemoved': not (fetched / 'S002-1.raw.gz').exists(),
                'sidecarMatchesRetained': sidecar.read_bytes() == retained_bytes,
                'sentinelRemoved': SENTINEL not in retained_bytes.decode('utf-8')})
        record('sanitize_keeps_received_digest_and_observations',
               entry['receivedSha256'] == hashlib.sha256(HTML).hexdigest()
               and entry['receivedBytes'] == len(HTML)
               and entry['sha256'] == hashlib.sha256(retained_bytes).hexdigest()
               and entry['bytes'] == len(retained_bytes)
               and entry['url'] == 'https://example.test/releases/tag/v1'
               and entry['status'] == 200
               and entry['fetchedAt'] == '2026-10-20T12:00:00+00:00',
               {'receivedSha256Preserved': entry['receivedSha256'] == hashlib.sha256(HTML).hexdigest(),
                'retainedSha256NamesRetainedBytes': entry['sha256'] == hashlib.sha256(retained_bytes).hexdigest(),
                'fetchedAt': entry['fetchedAt']})
        record('sanitize_never_logs_sentinel_values', SENTINEL not in printed,
               {'printedMentionsSentinel': SENTINEL in printed})
        record('sanitize_touches_no_other_path', neighbour.read_bytes() == neighbour_before,
               {'neighbourUnchanged': neighbour.read_bytes() == neighbour_before})

        # a second run is idempotent: same manifest bytes, same retained bytes, same received digest
        manifest_before = (fetched / 'manifest.json').read_bytes()
        retained_before = retained_file.read_bytes()
        stdout2 = io.StringIO()
        with contextlib.redirect_stdout(stdout2):
            fetch_group.sanitize_existing(root, source_text)
        entry2 = json.loads((fetched / 'manifest.json').read_text(encoding='utf-8'))[0]
        record('sanitize_is_idempotent',
               (fetched / 'manifest.json').read_bytes() == manifest_before
               and retained_file.read_bytes() == retained_before
               and entry2['receivedSha256'] == entry['receivedSha256']
               and entry2['fetchedAt'] == entry['fetchedAt']
               and entry2['sha256'] == entry['sha256']
               and not (fetched / 'S002-1.raw.gz').exists(),
               {'manifestBytesStable': (fetched / 'manifest.json').read_bytes() == manifest_before,
                'retainedBytesStable': retained_file.read_bytes() == retained_before,
                'receivedDigestStable': entry2['receivedSha256'] == entry['receivedSha256']})
    finally:
        shutil.rmtree(work, ignore_errors=True)

    failed = sum(1 for c in cases if not c['passed'])
    print(json.dumps({'kind': 'r27-privacy-selftest', 'cases': cases, 'failed': failed}, indent=2))
    return int(failed > 0)


if __name__ == '__main__':
    sys.exit(main())
