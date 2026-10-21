#!/usr/bin/env python3
"""Public GET per recorded S001-S006 URL; retain credential-free representations only.

Retention boundary
  * HTML responses retain only ``source_text.text_of(body, content_type)`` -- the
    public visible text. Attributes, script bodies, form fields and their values
    are never written to disk.
  * Code/plaintext responses whose URL names a code or config file (the recorded
    ``action.yml`` rows) retain the received bytes verbatim.
  * ``sha256``/``bytes`` in the manifest describe the RETAINED representation.
    The digest and byte count of the original HTTP body survive as
    ``receivedSha256``/``receivedBytes``. Those two are observations of a body
    that is not retained: they cannot be recomputed from the retained bytes and
    the retained bytes are not claimed to be the original body.

``--sanitize-existing`` is an offline (no network) migration of an existing
round-27 fetched directory. It reads only the caller's own manifest and its own
retained files, writes the filtered representation, preserves the original
URL/status/fetchedAt/received digest, and then removes only the own filenames it
replaced. Round-26 data and every path outside the round-27 fetched directory are
out of scope.

Modes
  * default: one public GET per recorded URL; only the filtered representation is
    written, and the own superseded ``*.raw.gz`` capture of that row is dropped.
  * ``--sanitize-existing``: no network access at all; migrate the existing own
    capture offline. Idempotent: an already filtered record keeps its original
    receivedSha256/receivedBytes and observations instead of being reclassified
    as a new GET.
  * ``--selftest``: run the offline privacy boundary selftest (privacy_selftest.py).
"""
import argparse
import datetime
import gzip
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import sys

WAVE = '.ufo/waves/round-27'
FETCHED = 'fetched'
TEXTDIR = 'text'
PUBLIC_SUFFIX = '.public.txt.gz'
SOURCE_SUFFIX = '.source.gz'
CODE_SUFFIXES = {'.yml', '.yaml', '.py', '.sh', '.js', '.ts'}
KIND_PUBLIC = 'public_visible_text'
KIND_SOURCE = 'received_code_bytes'
NOTE = ('sha256/bytes describe the retained representation; receivedSha256/'
        'receivedBytes observe the original HTTP body. HTML attributes and received '
        'HTML bytes are not retained or reconstructable; code/config may retain '
        'received bytes verbatim as stated by retainedRepresentation.')


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_source_text(root):
    """Load the frozen round-26 text view helper (read-only)."""
    path = root / '.ufo/waves/round-26/source_text.py'
    if not path.is_file():
        raise SystemExit('missing helper: ' + str(path))
    return _load_module(path, 'r26_source_text')


def load_fetch_sources(root):
    """Load the frozen round-26 single-GET helper (read-only, network side effects only when called)."""
    path = root / '.ufo/waves/round-26/fetch_sources.py'
    if not path.is_file():
        raise SystemExit('missing helper: ' + str(path))
    return _load_module(path, 'r26_fetch_sources')


def _basename(name):
    """Return a plain relative basename, or None when the name is unsafe to use."""
    if not isinstance(name, str) or not name:
        return None
    if name in {'.', '..'} or '/' in name or '\\' in name or '\x00' in name:
        return None
    if name != pathlib.PurePosixPath(name).name:
        return None
    return name


def _valid_key(row, index):
    """A manifest key must be a plain row label plus a positive fetch index."""
    if not isinstance(row, str) or not re.fullmatch(r'[A-Za-z]{1,4}[0-9]{1,4}', row):
        return False
    return isinstance(index, int) and not isinstance(index, bool) and index >= 1


def _url_basename(url):
    try:
        path = str(url or '').split('?', 1)[0].split('#', 1)[0]
    except Exception:
        return ''
    return path.rstrip('/').rsplit('/', 1)[-1].lower()


def classify(url, content_type, body, source_text):
    """Return (kind, retained_bytes) for one received body.

    HTML is reduced to its public visible text; a code/config file keeps its
    received bytes; anything else is reduced to its visible text as well.
    """
    ct = (content_type or '').lower()
    decoded = body.decode('utf-8', errors='replace')
    stripped = decoded.lstrip()
    head = stripped[:4096].lower()
    strict_html = ct.startswith('text/html') or stripped[:15].lower().startswith(('<!doctype', '<html'))
    if strict_html:
        return KIND_PUBLIC, source_text.text_of(body, content_type).encode('utf-8')
    if any(tag in head for tag in ('<html', '<body', '<form', '<input', '<script', '<!doctype')):
        # Markup without a leading doctype: force the visible-text view so that
        # attribute values and script bodies cannot survive.
        return KIND_PUBLIC, source_text.text_of(body, 'text/html').encode('utf-8')
    if pathlib.PurePosixPath(_url_basename(url)).suffix in CODE_SUFFIXES:
        return KIND_SOURCE, body
    return KIND_PUBLIC, source_text.text_of(body, content_type).encode('utf-8')


def retained_name(row, index, kind):
    suffix = SOURCE_SUFFIX if kind == KIND_SOURCE else PUBLIC_SUFFIX
    return '{}-{}{}'.format(row, index, suffix)


def sidecar_name(row, index):
    return '{}-{}.txt'.format(row, index)


def _representation(kind, row, index, received_sha256, received_bytes, replaced=None):
    info = {
        'kind': kind,
        'file': retained_name(row, index, kind),
        'textFile': sidecar_name(row, index),
        'textDir': TEXTDIR,
        'derivation': ('source_text.text_of(receivedBody, contentType)'
                       if kind == KIND_PUBLIC else 'received bytes verbatim (code/config source)'),
        'rawHttpBodyRetained': kind == KIND_SOURCE,
        'htmlAttributesRetained': False,
        'scriptBodiesRetained': False,
        'formFieldValuesRetained': False,
        'receivedSha256': received_sha256,
        'receivedBytes': received_bytes,
        'note': NOTE,
    }
    if replaced:
        info['replacedFile'] = replaced
    return info


def _write_atomic(path, data):
    tmp = path.with_name(path.name + '.tmp-{}'.format(os.getpid()))
    tmp.write_bytes(data)
    os.replace(str(tmp), str(path))


def _entry_with(row, index, url, final, status, error, at, content_type, received_sha256, received_bytes,
                kind, retained, replaced=None, base=None):
    """Build one manifest record; ``base`` preserves the original key order and fields."""
    entry = dict(base) if isinstance(base, dict) else {}
    entry['row'] = row
    entry['index'] = index
    entry['url'] = url
    entry['finalUrl'] = final
    entry['status'] = status
    entry['error'] = error
    entry['fetchedAt'] = at
    if content_type:
        entry['contentType'] = content_type
    entry['receivedSha256'] = received_sha256
    entry['receivedBytes'] = received_bytes
    entry['bytes'] = len(retained)
    entry['sha256'] = hashlib.sha256(retained).hexdigest()
    entry['file'] = retained_name(row, index, kind)
    entry['text'] = '{}/{}'.format(TEXTDIR, sidecar_name(row, index))
    entry['retainedRepresentation'] = _representation(kind, row, index, received_sha256, received_bytes, replaced)
    return entry


def fetch_all(root, source_text):
    """One public GET per recorded URL; only the filtered representation is persisted."""
    fetch_sources = load_fetch_sources(root)
    out = root / WAVE / FETCHED
    (out / TEXTDIR).mkdir(parents=True, exist_ok=True)
    manifest = []
    for row, urls in fetch_sources.rows(root / 'corpus/SOURCES.md'):
        if row not in {'S{:03d}'.format(i) for i in range(1, 7)}:
            continue
        for index, url in enumerate(urls, 1):
            at = datetime.datetime.now(datetime.timezone.utc).isoformat()
            try:
                status, final, headers, body = fetch_sources.fetch(url)
                error = None
            except Exception as exc:
                status, final, headers, body = None, url, {}, b''
                error = type(exc).__name__ + ': ' + str(exc)
            content_type = headers.get('content-type') if isinstance(headers, dict) else None
            kind, retained = classify(url, content_type, body, source_text)
            name = retained_name(row, index, kind)
            _write_atomic(out / name, gzip.compress(retained, mtime=0))
            _write_atomic(out / TEXTDIR / sidecar_name(row, index), retained)
            manifest.append(_entry_with(row, index, url, final, status, error, at, content_type,
                                        hashlib.sha256(body).hexdigest(), len(body), kind, retained))
            print(row, index, status, len(retained), kind, error or '')
    _write_atomic(out / 'manifest.json', (json.dumps(manifest, indent=2) + '\n').encode('utf-8'))
    _drop_superseded_raw(out, manifest)
    return int(any(x['status'] != 200 for x in manifest))


def _drop_superseded_raw(out, manifest):
    """Remove the own raw capture of a row that this run replaced by a filtered one."""
    removed = []
    for entry in manifest:
        if entry.get('status') != 200:
            continue
        name = '{}-{}{}'.format(entry['row'], entry['index'], '.raw.gz')
        path = _safe_child(out, name)
        if path is None or path.is_symlink() or not path.is_file():
            continue
        path.unlink()
        removed.append(name)
    if removed:
        print('removed superseded own captures: ' + ', '.join(sorted(set(removed))))


def _safe_child(directory, name):
    """Resolve a plain basename inside ``directory``; refuse anything else."""
    base = _basename(name)
    if base is None:
        return None
    path = directory / base
    try:
        if path.parent.resolve() != directory.resolve():
            return None
    except OSError:
        return None
    return path


def sanitize_existing(root, source_text):
    """Offline, no-network migration of the caller's own round-27 fetched directory."""
    fetched = root / WAVE / FETCHED
    manifest_path = fetched / 'manifest.json'
    if not manifest_path.is_file():
        raise SystemExit('no manifest to sanitize: ' + str(manifest_path))
    entries = json.loads(manifest_path.read_text(encoding='utf-8'))
    if not isinstance(entries, list):
        raise SystemExit('manifest is not a list: ' + str(manifest_path))
    (fetched / TEXTDIR).mkdir(parents=True, exist_ok=True)
    plans = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise SystemExit('manifest entry is not an object')
        row, index = entry.get('row'), entry.get('index')
        if not _valid_key(row, index):
            raise SystemExit('unsafe manifest key: {} {}'.format(row, index))
        old_name = _basename(entry.get('file'))
        if old_name is None:
            raise SystemExit('unsafe manifest file name for {} {}'.format(row, index))
        old_path = _safe_child(fetched, old_name)
        if old_path is None or old_path.is_symlink() or not old_path.is_file():
            raise SystemExit('manifest file is not a regular file: ' + old_name)
        payload = gzip.decompress(old_path.read_bytes())
        actual = hashlib.sha256(payload).hexdigest()
        received_digest = entry.get('receivedSha256') or entry.get('sha256')
        received_bytes = entry.get('receivedBytes', entry.get('bytes'))
        info = entry.get('retainedRepresentation')
        if isinstance(info, dict) and actual == entry.get('sha256'):
            # Already filtered: keep the original received observation and the retained bytes.
            if not entry.get('receivedSha256') or entry.get('receivedBytes') is None:
                raise SystemExit('filtered record without a received observation: {} {}'.format(row, index))
            kind = info.get('kind', KIND_PUBLIC)
            retained = payload
            replaced = info.get('replacedFile')
            received_sha256 = entry['receivedSha256']
            received_bytes = entry.get('receivedBytes')
        elif actual == received_digest:
            kind, retained = classify(entry.get('url', ''), entry.get('contentType'), payload, source_text)
            replaced = old_name
            received_sha256 = actual
            received_bytes = len(payload)
        else:
            raise SystemExit('manifest digest mismatch for {} {}'.format(row, index))
        plans.append({'entry': entry, 'row': row, 'index': index, 'kind': kind, 'retained': retained,
                      'received_sha256': received_sha256, 'received_bytes': received_bytes,
                      'replaced': replaced, 'old_name': old_name})
    # 1. write the safe retained files and their quote text sidecars
    for plan in plans:
        name = retained_name(plan['row'], plan['index'], plan['kind'])
        path = fetched / name
        _write_atomic(path, gzip.compress(plan['retained'], mtime=0))
        if gzip.decompress(path.read_bytes()) != plan['retained']:
            raise SystemExit('retained file did not verify: ' + name)
        _write_atomic(fetched / TEXTDIR / sidecar_name(plan['row'], plan['index']), plan['retained'])
    # 2. write the new manifest, preserving the original URL/status/fetchedAt/received digest
    new_entries = []
    for plan in plans:
        entry = plan['entry']
        new_entries.append(_entry_with(plan['row'], plan['index'], entry.get('url'), entry.get('finalUrl'),
                                       entry.get('status'), entry.get('error'), entry.get('fetchedAt'),
                                       entry.get('contentType'), plan['received_sha256'], plan['received_bytes'],
                                       plan['kind'], plan['retained'], replaced=plan['replaced'], base=entry))
    _write_atomic(manifest_path, (json.dumps(new_entries, indent=2) + '\n').encode('utf-8'))
    # 3. remove only the own filenames that were safely replaced
    keep = {retained_name(p['row'], p['index'], p['kind']) for p in plans}
    removed = []
    for plan in plans:
        candidates = [plan['replaced'], plan['old_name']]
        for candidate in candidates:
            name = _basename(candidate)
            if not name or name in keep:
                continue
            path = _safe_child(fetched, name)
            if path is None or path.is_symlink() or not path.is_file():
                continue
            path.unlink()
            removed.append(name)
    preserved = all(
        new.get('fetchedAt') == old.get('fetchedAt') and new.get('url') == old.get('url')
        and new.get('status') == old.get('status') and new.get('receivedSha256') == old.get('receivedSha256', new.get('receivedSha256'))
        for new, old in zip(new_entries, entries))
    report = {'mode': 'sanitize-existing', 'records': len(new_entries), 'removed': sorted(set(removed)),
              'observationsPreserved': preserved, 'networkAccess': 'none (no fetch helper is loaded)'}
    print(json.dumps(report, indent=2))
    return 0


def _run_selftest():
    path = pathlib.Path(__file__).resolve().parent / 'privacy_selftest.py'
    if not path.is_file():
        raise SystemExit('missing selftest: ' + str(path))
    module = _load_module(path, 'r27_privacy_selftest')
    return module.main()


def main(argv=None):
    parser = argparse.ArgumentParser(description='Round-27 public source capture with a credential-free retention boundary.')
    parser.add_argument('--root', type=pathlib.Path, help='repository root that holds .ufo/waves/round-27')
    parser.add_argument('--sanitize-existing', action='store_true',
                        help='offline migration of an existing r27 fetched directory; performs no network access')
    parser.add_argument('--selftest', action='store_true', help='run the privacy boundary selftest and exit')
    args = parser.parse_args(argv)
    if args.selftest:
        return _run_selftest()
    if args.root is None:
        parser.error('--root is required unless --selftest is given')
    source_text = load_source_text(args.root)
    if args.sanitize_existing:
        return sanitize_existing(args.root, source_text)
    return fetch_all(args.root, source_text)


if __name__ == '__main__':
    sys.exit(main())
