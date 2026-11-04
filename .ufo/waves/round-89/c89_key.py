#!/usr/bin/env python3
"""Round 89 C2 — conservative Vary-nominated cache-key construction.

Claim (frozen before data): freshness, a bounded capability acquisition. The
predicate is one sentence in the plan, in this counter and in the receipt:

    frozen=N/N props=M/M refuse=K/K controls=C/C met=true   (exit 0)

`frozen` scores hand cases declared in `c2-contract.md`; `props` scores a
property population generated at scoring time from the seed printed in the
receipt, so a table over the committed cases cannot reach it; `refuse` scores
the declared refusal list; `controls` requires every committed shortcut stub to
fail. At the base revision the candidate path is absent, so the same counter
prints `frozen=0/16 props=0/200 refuse=0/9 controls=0/5 met=false`, exit 1.

The reference implementation below is the contract, not an oracle: the selftest
checks it against the contract's worked examples before any candidate is
scored, and five reference mutants must each be killed by the property
population.
"""
import argparse
import json
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = '76225160d0dff8d2042fbcd037bd08b0971d5e07'
CANDIDATE = 'scripts/cache_key.py'
CASES = HERE / 'frozen' / 'c2-cases.json'
CONTROLS = HERE / 'controls'
SEED = 89089
PROPS_PER_CLASS = 20
TCHARS = "!#$%&'*+-.^_`|~0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
US, RS, GS = '\x1f', '\x1e', '\x1c'
ESCAPES = (('%', '%25'), (GS, '%1C'), ('\x1d', '%1D'), (RS, '%1E'), (US, '%1F'))


class Invalid(Exception):
    pass


def esc(s):
    for raw, enc in ESCAPES:
        s = s.replace(raw, enc)
    return s


def is_token(s):
    return bool(s) and all(c in TCHARS for c in s)


def strip_ows(s):
    return s.strip(' \t')


def parse_vary(vary):
    if not isinstance(vary, str):
        raise Invalid('vary must be a string')
    if vary == '':
        return []
    names = []
    for raw in vary.split(','):
        member = strip_ows(raw)
        if member == '*':
            raise Invalid('vary wildcard nominates no field')
        if not is_token(member):
            raise Invalid(f'vary member is not a token: {member!r}')
        names.append(member.lower())
    if len(set(names)) != len(names):
        raise Invalid('duplicate vary member')
    return sorted(names)


def key_of(obj):
    if not isinstance(obj, dict):
        raise Invalid('input must be a JSON object')
    uri = obj.get('uri')
    if not isinstance(uri, str):
        raise Invalid('uri must be a string')
    headers = obj.get('request_headers')
    if not isinstance(headers, dict):
        raise Invalid('request_headers must be an object')
    lowered = {}
    for name, value in headers.items():
        if not isinstance(name, str) or not is_token(name):
            raise Invalid(f'header name is not a token: {name!r}')
        if not isinstance(value, str):
            raise Invalid(f'header value for {name} must be a string')
        if '\r' in value or '\n' in value:
            raise Invalid(f'header value for {name} contains CR or LF')
        low = name.lower()
        if low in lowered:
            raise Invalid(f'duplicate header name differing only in case: {low}')
        lowered[low] = value
    names = parse_vary(obj.get('vary', ''))
    parts = []
    for name in names:
        if name in lowered:
            parts.append(esc(name) + RS + esc(strip_ows(lowered[name])))
        else:
            parts.append(esc(name) + RS + GS)
    return esc(uri) + ('' if not parts else US + US.join(parts))


# ------------------------------------------------------------- frozen cases
# Each case: (label, input, expected). `expected` is ("key", <str>) or
# ("refuse", <substring of the reason>). Hand-derived from c2-contract.md.
FROZEN = [
    ('no-vary-no-headers',
     {'uri': 'https://e.test/a', 'request_headers': {}},
     ('key', 'https://e.test/a')),
    ('empty-vary',
     {'uri': 'https://e.test/a', 'request_headers': {'x': '1'}, 'vary': ''},
     ('key', 'https://e.test/a')),
    ('single-member',
     {'uri': 'https://e.test/a', 'request_headers': {'Accept-Encoding': 'gzip'},
      'vary': 'Accept-Encoding'},
     ('key', 'https://e.test/a' + US + 'accept-encoding' + RS + 'gzip')),
    ('value-edge-ows-trimmed',
     {'uri': 'https://e.test/a', 'request_headers': {'accept-encoding': ' GZIP '},
      'vary': 'Accept-Encoding'},
     ('key', 'https://e.test/a' + US + 'accept-encoding' + RS + 'GZIP')),
    ('absent-member',
     {'uri': 'https://e.test/a', 'request_headers': {}, 'vary': 'Accept-Encoding'},
     ('key', 'https://e.test/a' + US + 'accept-encoding' + RS + GS)),
    ('present-empty-member',
     {'uri': 'https://e.test/a', 'request_headers': {'Accept-Encoding': ''},
      'vary': 'Accept-Encoding'},
     ('key', 'https://e.test/a' + US + 'accept-encoding' + RS)),
    ('two-members-sorted',
     {'uri': 'https://e.test/a',
      'request_headers': {'accept-encoding': 'gzip', 'Accept': 'text/html'},
      'vary': 'Accept-Encoding, Accept'},
     ('key', 'https://e.test/a' + US + 'accept' + RS + 'text/html'
      + US + 'accept-encoding' + RS + 'gzip')),
    ('member-ows-and-order',
     {'uri': 'https://e.test/a',
      'request_headers': {'accept-encoding': 'gzip', 'Accept': 'text/html'},
      'vary': '  Accept\t,Accept-Encoding  '},
     ('key', 'https://e.test/a' + US + 'accept' + RS + 'text/html'
      + US + 'accept-encoding' + RS + 'gzip')),
    ('percent-escaped',
     {'uri': 'https://e.test/a', 'request_headers': {'a': '50%'}, 'vary': 'a'},
     ('key', 'https://e.test/a' + US + 'a' + RS + '50%25')),
    ('separator-in-value-escaped',
     {'uri': 'https://e.test/a', 'request_headers': {'a': 'x' + US + 'b' + RS + 'y'},
      'vary': 'a'},
     ('key', 'https://e.test/a' + US + 'a' + RS + 'x%1Fb%1Ey')),
    ('separator-split-differs',
     {'uri': 'https://e.test/a', 'request_headers': {'a': 'x', 'b': 'y'},
      'vary': 'a, b'},
     ('key', 'https://e.test/a' + US + 'a' + RS + 'x' + US + 'b' + RS + 'y')),
    ('tab-trimmed',
     {'uri': 'https://e.test/a', 'request_headers': {'a': '\tv\t'}, 'vary': 'a'},
     ('key', 'https://e.test/a' + US + 'a' + RS + 'v')),
    ('wildcard-refused',
     {'uri': 'https://e.test/a', 'request_headers': {}, 'vary': '*'},
     ('refuse', 'wildcard')),
    ('trailing-comma-refused',
     {'uri': 'https://e.test/a', 'request_headers': {'a': '1'}, 'vary': 'a,'},
     ('refuse', 'token')),
    ('duplicate-header-name-refused',
     {'uri': 'https://e.test/a', 'request_headers': {'Accept': 'a', 'accept': 'b'},
      'vary': 'Accept'},
     ('refuse', 'duplicate header')),
    ('lf-value-refused',
     {'uri': 'https://e.test/a', 'request_headers': {'a': 'x\ny'}, 'vary': 'a'},
     ('refuse', 'CR or LF')),
]

REFUSALS = [
    ('not-an-object', [], 'object'),
    ('uri-missing', {'request_headers': {}}, 'uri'),
    ('uri-not-string', {'uri': 5, 'request_headers': {}}, 'uri'),
    ('headers-not-object', {'uri': 'u', 'request_headers': []}, 'request_headers'),
    ('header-name-not-token', {'uri': 'u', 'request_headers': {'a b': '1'}}, 'token'),
    ('header-value-not-string', {'uri': 'u', 'request_headers': {'a': 1}}, 'string'),
    ('vary-not-string', {'uri': 'u', 'request_headers': {}, 'vary': 3}, 'string'),
    ('star-member', {'uri': 'u', 'request_headers': {}, 'vary': 'a, *'}, 'wildcard'),
    ('empty-member', {'uri': 'u', 'request_headers': {'a': '1'}, 'vary': 'a,,b'}, 'token'),
]


# --------------------------------------------------------- property population
NAMES = ['accept', 'accept-encoding', 'accept-language', 'x-probe', 'user-agent']
VALS = ['gzip', 'br', 'GZIP', 'deflate', 'en', '50%', 'a' + US + 'b', ' v ', 'x' + RS + 'y', '']


def _rand_case(rng):
    names = rng.sample(NAMES, rng.randint(2, 3))
    headers = {n: rng.choice(VALS) for n in names}
    if rng.random() < 0.2:
        headers['x-other'] = rng.choice(VALS)
    uri = 'https://e.test/' + rng.choice(['a', 'b', 'c/d', 'p?q=1', 'r#f'])
    return {'uri': uri, 'request_headers': headers, 'vary': ', '.join(names)}


def _props(rng):
    """Each property returns (label, left_input, right_input, relation)."""
    c = _rand_case(rng)
    names = [n for n in c['vary'].split(', ') if n]

    def retag(inp, mapping):
        out = {'uri': inp['uri'], 'request_headers': dict(inp['request_headers']),
               'vary': inp['vary']}
        for old, new in mapping:
            for key in list(out['request_headers']):
                if key == old:
                    out['request_headers'][new] = out['request_headers'].pop(key)
        return out

    pick = rng.choice(list(c['request_headers']))
    other = {'uri': c['uri'], 'request_headers': dict(c['request_headers']), 'vary': c['vary']}
    yield ('name_case', c, retag(c, [(pick, pick.upper())]), 'same')
    yield ('member_order', c, {'uri': c['uri'], 'request_headers': dict(c['request_headers']),
                               'vary': ', '.join(reversed(names))}, 'same')
    yield ('member_ows', c, {'uri': c['uri'], 'request_headers': dict(c['request_headers']),
                             'vary': ' \t' + ' , '.join(names) + '\t '}, 'same')
    key = names[0]
    val = other['request_headers'].get(key, '')
    padded = {'uri': c['uri'], 'request_headers': dict(c['request_headers']),
              'vary': c['vary']}
    padded['request_headers'][key] = ' \t' + val + ' \t'
    yield ('value_edge_ows', c, padded, 'same')
    base_val = {'uri': c['uri'], 'request_headers': dict(c['request_headers']), 'vary': c['vary']}
    cased = {'uri': c['uri'], 'request_headers': dict(c['request_headers']), 'vary': c['vary']}
    base_val['request_headers'][key] = strip_ows(val) + 'a'
    cased['request_headers'][key] = strip_ows(val) + 'A'
    yield ('value_case', base_val, cased, 'different')
    yield ('uri_change', c, {'uri': c['uri'] + '/x',
                             'request_headers': dict(c['request_headers']),
                             'vary': c['vary']}, 'different')
    extra = {'uri': c['uri'], 'request_headers': dict(c['request_headers']), 'vary': c['vary']}
    extra['request_headers']['x-unrelated'] = rng.choice(VALS)
    yield ('unrelated_header', c, extra, 'same')
    absent = {'uri': c['uri'], 'request_headers': dict(c['request_headers']), 'vary': key}
    empty = {'uri': c['uri'], 'request_headers': dict(c['request_headers']), 'vary': key}
    absent['request_headers'].pop(key, None)
    empty['request_headers'][key] = ''
    yield ('absent_vs_empty', absent, empty, 'different')
    x, y = rng.choice(['p', 'q', 'r']), rng.choice(['s', 't', 'u'])
    joined = {'uri': c['uri'], 'request_headers': {key: x + US + 'b' + RS + y},
              'vary': key}
    split = {'uri': c['uri'], 'request_headers': {key: x, 'b': y}, 'vary': key + ', b'}
    yield ('separator_collision', joined, split, 'different')
    pct = {'uri': c['uri'], 'request_headers': dict(c['request_headers']), 'vary': key}
    pct['request_headers'][key] = '50%'
    bare = {'uri': c['uri'], 'request_headers': dict(c['request_headers']), 'vary': key}
    bare['request_headers'][key] = '50'
    yield ('percent', pct, bare, 'different')


PROP_CLASSES = ('name_case', 'member_order', 'member_ows', 'value_edge_ows', 'value_case',
                'uri_change', 'unrelated_header', 'absent_vs_empty',
                'separator_collision', 'percent')


# ------------------------------------------------------------- candidate run
FORBIDDEN = ('c89_key', 'c89_defect_queue', 'c2-cases')


def guard(source):
    """Textual shortcut guard (disclosed limit: not a sandbox).

    It refuses the two committed shortcuts that would otherwise pass — importing
    this counter's reference, and reading the frozen case file — plus any `open(`
    of the wave tree. It does not refuse a hardcoded table or a re-implemented
    reference; the property population is what stops a table.
    """
    text = source.decode('utf-8', 'replace')
    for token in FORBIDDEN:
        if token in text:
            return f'shortcut guard: source names {token!r}'
    for line in text.splitlines():
        if 'open(' in line and '.ufo' in line:
            return 'shortcut guard: source opens the wave tree'
    return None


def run_candidate(path, payload, work, timeout=30):
    p = subprocess.run([sys.executable, '-B', str(path)], input=json.dumps(payload),
                       capture_output=True, text=True, timeout=timeout, cwd=str(work))
    return p


def score_candidate(source, work, seed):
    fails = []
    note = guard(source)
    if note:
        return 0, 0, 0, note
    work.mkdir(parents=True, exist_ok=True)
    path = work / 'candidate.py'
    path.write_bytes(source)
    frozen_ok = 0
    for label, payload, expected in FROZEN:
        try:
            p = run_candidate(path, payload, work)
        except subprocess.TimeoutExpired:
            fails.append(f'frozen {label}: timeout')
            continue
        kind, want = expected
        if kind == 'key':
            if p.returncode != 0:
                fails.append(f'frozen {label}: exit {p.returncode}')
                continue
            try:
                got = json.loads(p.stdout)['key']
            except (ValueError, KeyError, TypeError):
                fails.append(f'frozen {label}: stdout is not {{"key": ...}}')
                continue
            if got != want:
                fails.append(f'frozen {label}: key differs')
                continue
            frozen_ok += 1
        else:
            if p.returncode != 1 or not p.stderr.startswith('invalid_input:'):
                fails.append(f'frozen {label}: expected invalid_input exit 1')
                continue
            if want not in p.stderr:
                fails.append(f'frozen {label}: refusal does not name {want!r}')
                continue
            frozen_ok += 1
    refuse_ok = 0
    for label, payload, want in REFUSALS:
        try:
            p = run_candidate(path, payload, work)
        except subprocess.TimeoutExpired:
            fails.append(f'refuse {label}: timeout')
            continue
        if p.returncode == 1 and p.stderr.startswith('invalid_input:') and want in p.stderr:
            refuse_ok += 1
        else:
            fails.append(f'refuse {label}: not refused with {want!r}')
    rng = random.Random(seed)
    props_ok = 0
    props_total = 0
    for cls in PROP_CLASSES:
        for _ in range(PROPS_PER_CLASS):
            for label, left, right, relation in _props(rng):
                if label != cls:
                    continue
                props_total += 1
                try:
                    pl = run_candidate(path, left, work)
                    pr = run_candidate(path, right, work)
                except subprocess.TimeoutExpired:
                    fails.append(f'prop {cls}: timeout')
                    break
                if pl.returncode != 0 or pr.returncode != 0:
                    fails.append(f'prop {cls}: exit {pl.returncode}/{pr.returncode}')
                    break
                try:
                    kl = json.loads(pl.stdout)['key']
                    kr = json.loads(pr.stdout)['key']
                except (ValueError, KeyError, TypeError):
                    fails.append(f'prop {cls}: stdout is not {{"key": ...}}')
                    break
                if (kl == kr) == (relation == 'same'):
                    props_ok += 1
                else:
                    fails.append(f'prop {cls}: expected {relation} keys')
                    break
                break
    return frozen_ok, props_ok, refuse_ok, fails


def score_controls(work, seed):
    """Every committed stub must fail; returns (passed, total, lines)."""
    lines = []
    passed = 0
    total = 0
    for stub in sorted(CONTROLS.glob('ctl-*.py')):
        total += 1
        source = stub.read_bytes()
        note = guard(source)
        if note:
            lines.append(f'ctl={stub.stem} met=false ({note})')
            passed += 1
            continue
        frozen_ok, props_ok, refuse_ok, fails = score_candidate(source, work / stub.stem, seed)
        met = (frozen_ok == len(FROZEN) and props_ok == PROPS_PER_CLASS * len(PROP_CLASSES)
               and refuse_ok == len(REFUSALS))
        if not met:
            passed += 1
        lines.append(f'ctl={stub.stem} frozen={frozen_ok}/{len(FROZEN)} '
                     f'props={props_ok}/{PROPS_PER_CLASS * len(PROP_CLASSES)} '
                     f'refuse={refuse_ok}/{len(REFUSALS)} met={str(met).lower()}')
    return passed, total, lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path)
    ap.add_argument('--revision')
    ap.add_argument('--candidate', default=CANDIDATE)
    ap.add_argument('--work', type=Path)
    ap.add_argument('--seed', type=int, default=SEED)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.work:
        ap.error('--work required')
    if not a.root or not a.revision:
        ap.error('--root and --revision required')
    rev = subprocess.check_output(['git', '-C', str(a.root), 'rev-parse',
                                   f'{a.revision}^{{commit}}'], text=True).strip()
    show = subprocess.run(['git', '-C', str(a.root), 'show', f'{rev}:{a.candidate}'],
                          capture_output=True)
    ctl_ok, ctl_total, ctl_lines = score_controls(a.work / 'ctl', a.seed)
    if show.returncode != 0:
        print(f'C2v1 revision={rev} candidate={a.candidate} seed={a.seed} '
              f'frozen=0/{len(FROZEN)} props=0/{PROPS_PER_CLASS * len(PROP_CLASSES)} '
              f'refuse=0/{len(REFUSALS)} controls={ctl_ok}/{ctl_total} met=false '
              f'(candidate absent)')
        for line in ctl_lines:
            print(line)
        return 1
    frozen_ok, props_ok, refuse_ok, fails = score_candidate(show.stdout, a.work / 'cand', a.seed)
    total_props = PROPS_PER_CLASS * len(PROP_CLASSES)
    met = (frozen_ok == len(FROZEN) and props_ok == total_props
           and refuse_ok == len(REFUSALS) and ctl_ok == ctl_total and ctl_total > 0)
    print(f'C2v1 revision={rev} candidate={a.candidate} seed={a.seed} '
          f'frozen={frozen_ok}/{len(FROZEN)} props={props_ok}/{total_props} '
          f'refuse={refuse_ok}/{len(REFUSALS)} controls={ctl_ok}/{ctl_total} '
          f'met={str(met).lower()}')
    for line in ctl_lines:
        print(line)
    for f in fails[:12]:
        print('fail: ' + f)
    return 0 if met else 1


# ---------------------------------------------------------------- selftest

WORKED = [
    ({'uri': 'https://e.test/a', 'request_headers': {}}, 'https://e.test/a'),
    ({'uri': 'https://e.test/a', 'request_headers': {'Accept-Encoding': 'gzip'},
      'vary': 'Accept-Encoding'},
     'https://e.test/a' + US + 'accept-encoding' + RS + 'gzip'),
    ({'uri': 'https://e.test/a',
      'request_headers': {'accept-encoding': 'gzip', 'Accept': 'text/html'},
      'vary': ' Accept ,Accept-Encoding '},
     'https://e.test/a' + US + 'accept' + RS + 'text/html' + US + 'accept-encoding'
     + RS + 'gzip'),
    ({'uri': 'https://e.test/a', 'request_headers': {'a': '50%'}, 'vary': 'a'},
     'https://e.test/a' + US + 'a' + RS + '50%25'),
    ({'uri': 'https://e.test/a', 'request_headers': {'a': 'x' + US + 'b' + RS + 'y'},
      'vary': 'a'},
     'https://e.test/a' + US + 'a' + RS + 'x%1Fb%1Ey'),
    ({'uri': 'https://e.test/a', 'request_headers': {'Accept-Encoding': ''},
      'vary': 'Accept-Encoding'},
     'https://e.test/a' + US + 'accept-encoding' + RS),
    ({'uri': 'https://e.test/a', 'request_headers': {}, 'vary': 'Accept-Encoding'},
     'https://e.test/a' + US + 'accept-encoding' + RS + GS),
]

REFERENCE = '''#!/usr/bin/env python3
import json, sys
US, RS, GS = "\\x1f", "\\x1e", "\\x1c"
T = "!#$%&'*+-.^_`|~0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
def esc(s):
    for raw, enc in (("%", "%25"), (GS, "%1C"), ("\\x1d", "%1D"), (RS, "%1E"), (US, "%1F")):
        s = s.replace(raw, enc)
    return s
def tok(s):
    return bool(s) and all(c in T for c in s)
def main():
    try:
        obj = json.load(sys.stdin)
    except Exception:
        print("invalid_input: not JSON", file=sys.stderr); return 1
    if not isinstance(obj, dict):
        print("invalid_input: input must be a JSON object", file=sys.stderr); return 1
    uri = obj.get("uri")
    if not isinstance(uri, str):
        print("invalid_input: uri must be a string", file=sys.stderr); return 1
    headers = obj.get("request_headers")
    if not isinstance(headers, dict):
        print("invalid_input: request_headers must be an object", file=sys.stderr); return 1
    low = {}
    for name, value in headers.items():
        if not isinstance(name, str) or not tok(name):
            print("invalid_input: header name is not a token", file=sys.stderr); return 1
        if not isinstance(value, str):
            print("invalid_input: header value must be a string", file=sys.stderr); return 1
        if "\\r" in value or "\\n" in value:
            print("invalid_input: header value contains CR or LF", file=sys.stderr); return 1
        k = name.lower()
        if k in low:
            print("invalid_input: duplicate header name", file=sys.stderr); return 1
        low[k] = value
    vary = obj.get("vary", "")
    if not isinstance(vary, str):
        print("invalid_input: vary must be a string", file=sys.stderr); return 1
    names = []
    if vary != "":
        for raw in vary.split(","):
            m = raw.strip(" \\t")
            if m == "*":
                print("invalid_input: vary wildcard nominates no field", file=sys.stderr); return 1
            if not tok(m):
                print("invalid_input: vary member is not a token", file=sys.stderr); return 1
            names.append(m.lower())
    if len(set(names)) != len(names):
        print("invalid_input: duplicate vary member", file=sys.stderr); return 1
    parts = []
    for name in sorted(names):
        if name in low:
            parts.append(esc(name) + RS + esc(low[name].strip(" \\t")))
        else:
            parts.append(esc(name) + RS + GS)
    key = esc(uri) + ("" if not parts else US + US.join(parts))
    print(json.dumps({"key": key}))
    return 0
raise SystemExit(main())
'''

MUTANTS = {
    'no-escape': ('        s = s.replace(raw, enc)', '        s = s'),
    'no-trim': ('low[name].strip(" \\t")', 'low[name]'),
    'casefold-values': ('esc(low[name].strip(" \\t"))', 'esc(low[name].strip(" \\t").lower())'),
    'no-sort': ('for name in sorted(names):', 'for name in names:'),
    'absent-equals-empty': ('parts.append(esc(name) + RS + GS)',
                            'parts.append(esc(name) + RS)'),
}


def _ref_source():
    return REFERENCE


def selftest():
    checks = []

    def record(label, ok):
        checks.append((label, bool(ok)))

    for i, (payload, want) in enumerate(WORKED, 1):
        try:
            got = key_of(payload)
        except Invalid:
            got = None
        record(f'reference matches contract example {i}', got == want)

    for label, payload, expected in FROZEN:
        kind, want = expected
        try:
            got = key_of(payload)
            ok = (kind == 'key' and got == want)
        except Invalid as e:
            ok = (kind == 'refuse' and want in str(e))
        record(f'reference matches frozen case {label}', ok)

    for label, payload, want in REFUSALS:
        try:
            key_of(payload)
            ok = False
        except Invalid as e:
            ok = want in str(e)
        record(f'reference refuses {label}', ok)

    with tempfile.TemporaryDirectory(prefix='kake-r89-c2-selftest-') as d:
        d = Path(d)
        source = _ref_source().encode()
        frozen_ok, props_ok, refuse_ok, fails = score_candidate(source, d / 'ref', SEED)
        total_props = PROPS_PER_CLASS * len(PROP_CLASSES)
        record('reference scores frozen/props/refuse full',
               frozen_ok == len(FROZEN) and props_ok == total_props
               and refuse_ok == len(REFUSALS))
        record('reference scores no failures', not fails)

        for name, (old, new) in MUTANTS.items():
            assert old in _ref_source(), f'mutant anchor missing: {name}'
            mutant = _ref_source().replace(old, new).encode()
            _, m_props, _, _ = score_candidate(mutant, d / name, SEED)
            record(f'mutant {name} is killed by the property population',
                   m_props < total_props)

        # A table over the committed frozen cases must not reach the target.
        table = (
            'import json, sys\n'
            'CASES = ' + repr([(p, e) for _, p, e in FROZEN]) + '\n'
            'obj = json.load(sys.stdin)\n'
            'for payload, expected in CASES:\n'
            '    if payload == obj:\n'
            '        if expected[0] == "key":\n'
            '            print(json.dumps({"key": expected[1]})); sys.exit(0)\n'
            '        print("invalid_input: " + expected[1], file=sys.stderr); sys.exit(1)\n'
            'print("invalid_input: unknown", file=sys.stderr); sys.exit(1)\n').encode()
        f_ok, p_ok, r_ok, _ = score_candidate(table, d / 'table', SEED)
        record('a frozen-case table does not reach the property population',
               p_ok < total_props)

        # The committed controls must all fail, and the guard must be what
        # rejects the oracle-import and case-table stubs.
        ctl_ok, ctl_total, ctl_lines = score_controls(d / 'ctl', SEED)
        record('every committed control is rejected', ctl_total > 0 and ctl_ok == ctl_total)
        record('the shortcut guard rejects the oracle-import stub',
               any(line.startswith('ctl=ctl-oracle-import met=false (shortcut guard')
                   for line in ctl_lines))
        record('the shortcut guard rejects the case-table stub',
               any(line.startswith('ctl=ctl-table met=false (shortcut guard')
                   for line in ctl_lines))

    passed = sum(1 for _, ok in checks if ok)
    for label, ok in checks:
        print(('PASS ' if ok else 'FAIL ') + label)
    print(f'selftest: {passed}/{len(checks)} passed')
    return 0 if passed == len(checks) else 1


if __name__ == '__main__':
    raise SystemExit(main())
