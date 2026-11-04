#!/usr/bin/env python3
"""Differential probe: reference vs each mutant, in-process through main().

main() is the candidate's entry point (the script does sys.exit(main())), so
patching sys.stdin/stdout/stderr and calling main() reproduces the CLI contract
(return code, stdout payload, stderr class) without a process per input.

Corpus: every frozen case and refusal declared by the counter, the contract's
worked examples, plus an adversarial generator over the clauses the case set
does and does not reach (U+001C/U+001D/U+001E/U+001F and '%' in values and URIs,
internal double spaces, unicode whitespace, '*' inside a token, duplicate
members, duplicate header names, empty Vary, absent vs empty).
"""
import contextlib
import importlib.util
import io
import json
import random
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/kake-r89/MutKey')
US, RS, GS, FS = '\x1f', '\x1e', '\x1c', '\x1d'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(mod, raw):
    """raw: str fed to stdin. Returns (kind, payload, exit)."""
    out, err = io.StringIO(), io.StringIO()
    old = sys.stdin
    try:
        sys.stdin = io.StringIO(raw)
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = mod.main()
            except SystemExit as e:
                code = e.code if isinstance(e.code, int) else 1
    finally:
        sys.stdin = old
    o, e = out.getvalue(), err.getvalue()
    if code == 0:
        try:
            return ('key', json.loads(o)['key'], 0)
        except Exception:
            return ('bad-stdout', o, code)
    return ('refuse', e.strip(), code)


def corpus(counter):
    out = []
    for label, payload, expected in counter.FROZEN:
        out.append((f'frozen:{label}', json.dumps(payload)))
    for label, payload, _ in counter.REFUSALS:
        out.append((f'refuse:{label}', json.dumps(payload)))
    for i, (payload, _) in enumerate(counter.WORKED, 1):
        out.append((f'worked:{i}', json.dumps(payload)))

    def add(label, obj):
        out.append((label, json.dumps(obj)))

    base = {'uri': 'https://e.test/a', 'request_headers': {}, 'vary': 'a'}
    # each control character and '%' inside a value and inside the URI
    for ch, nm in (('%', 'pct'), (GS, 'u001C'), (FS, 'u001D'), (RS, 'u001E'), (US, 'u001F')):
        add(f'value-{nm}', {'uri': 'https://e.test/a',
                            'request_headers': {'a': f'x{ch}y'}, 'vary': 'a'})
        add(f'value-{nm}-alone', {'uri': 'https://e.test/a',
                                  'request_headers': {'a': ch}, 'vary': 'a'})
        add(f'uri-{nm}', {'uri': f'https://e.test/a{ch}b',
                          'request_headers': {'a': 'v'}, 'vary': 'a'})
        add(f'uri-{nm}-novary', {'uri': f'https://e.test/a{ch}b',
                                 'request_headers': {}})
    # absent vs present-empty vs present-GS-only
    add('absent', {'uri': 'u', 'request_headers': {}, 'vary': 'a'})
    add('present-empty', {'uri': 'u', 'request_headers': {'a': ''}, 'vary': 'a'})
    add('present-GS', {'uri': 'u', 'request_headers': {'a': GS}, 'vary': 'a'})
    add('present-ows-only', {'uri': 'u', 'request_headers': {'a': ' \t '}, 'vary': 'a'})
    # internal whitespace
    add('value-internal-2sp', {'uri': 'u', 'request_headers': {'a': 'x  y'}, 'vary': 'a'})
    add('value-internal-tab', {'uri': 'u', 'request_headers': {'a': 'x\ty'}, 'vary': 'a'})
    add('value-internal-2sp-trimmed', {'uri': 'u', 'request_headers': {'a': '  x  y  '},
                                       'vary': 'a'})
    # OWS wider than SP/HTAB
    for ch, nm in (('\n', 'LF'), ('\x0b', 'VT'), ('\x0c', 'FF'), ('\r', 'CR'),
                   ('\xa0', 'NBSP'), ('\u2003', 'EMSP')):
        add(f'value-wrap-{nm}', {'uri': 'u', 'request_headers': {'a': f'{ch}v{ch}'}, 'vary': 'a'})
        add(f'member-wrap-{nm}', {'uri': 'u', 'request_headers': {'a': 'v'},
                                  'vary': f'{ch}a{ch}'})
        add(f'vary-leading-{nm}-comma', {'uri': 'u', 'request_headers': {'a': 'v'},
                                         'vary': f'a,{ch}'})
    # member spelling / wildcard / duplicates
    for v in ('*', ' * ', 'a,*', 'a, *', '*,a', 'a*', '*a', 'x*y', '**'):
        add(f'vary-{v!r}', {'uri': 'u', 'request_headers': {'a': 'v'}, 'vary': v})
    for v in ('a,A', 'A,a', 'a,a', 'Accept,accept', 'a, b, a'):
        add(f'vary-dup-{v!r}', {'uri': 'u', 'request_headers': {'a': 'v'}, 'vary': v})
    for v in ('', ' ', '\t', ',', 'a,', ',a', 'a,,b'):
        add(f'vary-emptyish-{v!r}', {'uri': 'u', 'request_headers': {'a': 'v'}, 'vary': v})
    add('vary-absent-key', {'uri': 'u', 'request_headers': {'a': 'v'}})
    add('vary-null', {'uri': 'u', 'request_headers': {}, 'vary': None})
    # name case
    for hdr in ('A', 'ACCEPT', 'Accept-Encoding', 'aCcEpT'):
        add(f'hdr-case-{hdr}', {'uri': 'u', 'request_headers': {hdr: 'v'},
                                'vary': hdr.lower()})
    add('hdr-dup-case', {'uri': 'u', 'request_headers': {'Accept': 'a', 'accept': 'b'},
                         'vary': 'accept'})
    add('hdr-dup-case-3', {'uri': 'u',
                           'request_headers': {'a': '1', 'A': '2', 'x': '3'},
                           'vary': 'a'})
    # token boundary
    for nm in ('a b', 'a\tb', 'a,b', 'a:b', 'a/b', 'a(b)', '', 'a"b', 'a\\b'):
        add(f'hdr-name-{nm!r}', {'uri': 'u', 'request_headers': {nm: 'v'}, 'vary': 'a'})
        add(f'vary-member-{nm!r}', {'uri': 'u', 'request_headers': {}, 'vary': nm})
    # CR/LF in value, CR only
    add('value-CR', {'uri': 'u', 'request_headers': {'a': 'x\ry'}, 'vary': 'a'})
    add('value-LF', {'uri': 'u', 'request_headers': {'a': 'x\ny'}, 'vary': 'a'})
    add('value-CRLF', {'uri': 'u', 'request_headers': {'a': 'x\r\ny'}, 'vary': 'a'})
    # uri shapes
    add('uri-empty', {'uri': '', 'request_headers': {}})
    add('uri-nonascii', {'uri': 'https://e.test/é', 'request_headers': {}})
    add('uri-pct-raw', {'uri': 'https://e.test/%41', 'request_headers': {}})
    add('no-uri', {'request_headers': {}})
    add('uri-int', {'uri': 5, 'request_headers': {}})
    add('headers-list', {'uri': 'u', 'request_headers': []})
    add('headers-absent', {'uri': 'u'})
    add('header-value-int', {'uri': 'u', 'request_headers': {'a': 1}})
    add('header-value-null', {'uri': 'u', 'request_headers': {'a': None}})
    # raw stdin shapes
    for raw in ('', 'null', '[]', '5', '"x"', '{}', '{', '{"uri":"u","request_headers":{}}x'):
        out.append((f'raw:{raw!r}', raw))

    rng = random.Random(89089)
    vals = ['gzip', 'GZIP', '  gzip  ', 'x  y', '', ' ', '50%', 'a' + US + 'b',
            'a' + GS + 'b', 'a' + FS + 'b', 'a' + RS + 'b', 'v\t', '\tv', '%25',
            'x\xa0y', 'x\x0by']
    names = ['a', 'b', 'Accept', 'accept-encoding', 'x-probe', 'user-agent']
    for i in range(400):
        k = rng.randint(1, 3)
        chosen = rng.sample(names, k)
        headers = {}
        for n in chosen:
            if rng.random() < 0.15:
                continue
            headers[n] = rng.choice(vals)
        if rng.random() < 0.1:
            headers['x-other'] = rng.choice(vals)
        vary = ', '.join(rng.choice([n, n.upper(), n.lower()]) for n in chosen)
        if rng.random() < 0.08:
            vary = ' ' + vary + ' '
        uri = rng.choice(['https://e.test/a', 'https://e.test/a%20b', 'u',
                          'https://e.test/a' + US + 'b'])
        out.append((f'rand:{i}', json.dumps({'uri': uri, 'request_headers': headers,
                                             'vary': vary})))
    return out


def main():
    counter = load(S / 'counter-live/c89_key.py', 'counter_live')
    ref = load(S / 'ref/cache_key.py', 'ref_mod')
    cases = corpus(counter)
    ref_out = [run(ref, raw) for _, raw in cases]
    index = json.loads((S / 'mutants/index.json').read_text())
    report = {'corpus_size': len(cases), 'reference': {'cases': len(cases)},
              'mutants': {}}
    # reference must be deterministic and produce no bad-stdout
    report['reference']['bad_stdout'] = sum(1 for r in ref_out if r[0] == 'bad-stdout')
    outdir = S / 'receipts/diff'
    outdir.mkdir(parents=True, exist_ok=True)
    for rec in index:
        mid = rec['id']
        mod = load(S / 'mutants' / f'{mid}.py', 'm_' + mid.replace('-', '_'))
        div = []
        for (label, raw), want in zip(cases, ref_out):
            got = run(mod, raw)
            if got[0] != want[0] or (got[0] == 'key' and got[1] != want[1]) \
                    or (got[0] == 'refuse' and got[2] != want[2]):
                div.append({'case': label, 'input': raw[:400],
                            'reference': [want[0], want[1] if want[0] != 'refuse' else want[1][:80]],
                            'mutant': [got[0], got[1] if got[0] != 'refuse' else got[1][:80]]})
        report['mutants'][mid] = {'clause': rec['clause'], 'divergences': len(div),
                                  'witness': div[0] if div else None}
        with open(outdir / f'{mid}.jsonl', 'w') as f:
            for d in div:
                f.write(json.dumps(d) + '\n')
        print(f'{mid:38s} divergences={len(div):4d} '
              f'{(div[0]["case"] if div else "-")}', flush=True)
    (outdir / 'diff.json').write_text(json.dumps(report, indent=1) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
