#!/usr/bin/env python3
"""ScribeLesson round-88 probes — read-only measurement over frozen lane bytes.

Every probe here re-derives one claim made in
`.ufo/waves/round-88/w1/ScribeLesson/round-88.md`. Nothing is written outside
the caller's --work directory; the lane repo is only read (`git show`).

Usage:
  python3 -B round88-scribe-probes.py --lane <LANE> --work <scratch>

Probes:
  P1  v2 vs v3 seeded-population label diff (freeze amendment effect)
  P2  branch coverage of the frozen 220-case population
  P3  C1 counter: float-valued six terms + stub selftest  (D2 type gap)
  P4  C1 counter: hardcoded single-payload lookup table     (D2 arithmetic gap)
  P5  C1 counter: gutted candidate selftest only            (D2 selftest gap)
  P6  C1 counter: CRLF line-ending rewrite of the entry     (D3 byte-identity gap)
  P7  C1 counter: ledger-path look-alike in the companion   (D1 path-binding gap)
  P8  C1 counter: bare-number cadence 'recheck: 5'          (D3 cadence gap)
  P9  C1 counter: pure insertion adjacent to the recheck line (D3 false red)
  P10 C2 counter: candidate delegating to the committed oracle
  P11 C2 counter: mutants that pass 220/220 while changing declared behaviour
"""
import argparse
import hashlib
import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
LANE_DEFAULT = pathlib.Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
WAVE = '.ufo/waves/round-88'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', type=pathlib.Path, default=LANE_DEFAULT)
    ap.add_argument('--work', type=pathlib.Path, required=True)
    a = ap.parse_args()
    lane = a.lane
    work = a.work
    work.mkdir(parents=True, exist_ok=True)
    out = {}

    c1 = load(lane / WAVE / 'c88_defect_queue.py', 'c88_c1')
    c2 = load(lane / WAVE / 'c88_vary.py', 'c88_c2')

    # ---- P1  v2 vs v3 seeded population -------------------------------
    v2src = subprocess.run(['git', '-C', str(lane), 'show',
                            '8063739791e21a8d7966fd968913e552e1433881:' + WAVE + '/c88_vary.py'],
                           capture_output=True).stdout
    v3src = subprocess.run(['git', '-C', str(lane), 'show',
                            '52e41d2d0ea6f5a7eaf8b5ac09ab0d78c538d644:' + WAVE + '/c88_vary.py'],
                           capture_output=True).stdout
    tmp = work / 'p1'
    tmp.mkdir(parents=True, exist_ok=True)
    (tmp / 'vary-cases.json').write_bytes((lane / WAVE / 'vary-cases.json').read_bytes())
    (tmp / 'c88_vary_v2.py').write_bytes(v2src)
    (tmp / 'c88_vary_v3.py').write_bytes(v3src)
    v2 = load(tmp / 'c88_vary_v2.py', 'v2mod')
    v3 = load(tmp / 'c88_vary_v3.py', 'v3mod')
    d2 = {c['id']: c for c in v2.RANDOM_CASES}
    d3 = {c['id']: c for c in v3.RANDOM_CASES}
    out['P1_v2_v3'] = {
        'v2_random_sha256': v2.RANDOM_SHA,
        'v3_random_sha256': v3.RANDOM_SHA,
        'same_ids': set(d2) == set(d3),
        'label_flips': sorted(i for i in d2 if d2[i] != d3[i]),
        'frozen_set_identical': v2.CASES == v3.CASES,
        'frozen_cases_sha256': v2.CASES_SHA,
    }

    # ---- P2  branch coverage of the frozen population ------------------
    hits = {}

    def bump(k):
        hits[k] = hits.get(k, 0) + 1

    def instrumented(vary, stored, presented):
        if not isinstance(vary, str):
            bump('vary_not_str')
            return 'invalid'
        members = [x.strip(c2.OWS) for x in vary.split(',')]
        if not members or any(x == '' for x in members):
            bump('empty_member')
            return 'invalid'
        names, star = [], False
        for x in members:
            if x == '*':
                star = True
                bump('star')
            elif c2.is_token(x):
                names.append(x.lower())
            else:
                bump('nontoken_member')
                return 'invalid'

        def norm(side):
            if not isinstance(side, dict):
                bump('side_not_dict')
                return None
            o = {}
            for k, v in side.items():
                if not c2.is_token(k):
                    bump('nontoken_key')
                    return None
                low = k.lower()
                if low in o:
                    bump('dup_key_in_side')
                    return None
                if isinstance(v, str):
                    o[low] = v
                elif isinstance(v, list) and v and all(isinstance(x, str) for x in v):
                    o[low] = ', '.join(v)
                    bump('list_join')
                else:
                    bump('bad_value_type')
                    return None
            return o

        A, B = norm(stored), norm(presented)
        if A is None or B is None:
            bump('side_invalid')
            return 'invalid'
        if star:
            bump('star_mismatch')
            return 'mismatch'
        for n in set(names):
            left, right = A.get(n), B.get(n)
            if left is None and right is None:
                bump('absent_both')
                continue
            if left is None or right is None:
                bump('absent_one')
                return 'mismatch'
            if left.strip(c2.OWS) != right.strip(c2.OWS):
                bump('value_diff')
                return 'mismatch'
        bump('all_match')
        return 'match'

    disagreements = 0
    for c in list(c2.CASES) + list(c2.RANDOM_CASES):
        got = instrumented(c['vary'], c['stored'], c['presented'])
        want = c['verdict'] if c['exit'] == 0 else 'invalid'
        if got != want:
            disagreements += 1
    expected_branches = ('vary_not_str', 'empty_member', 'nontoken_member', 'star',
                         'star_mismatch', 'nontoken_key', 'dup_key_in_side', 'list_join',
                         'bad_value_type', 'side_not_dict', 'side_invalid', 'absent_both',
                         'absent_one', 'value_diff', 'all_match')
    out['P2_branch_coverage'] = {
        'population': len(c2.CASES) + len(c2.RANDOM_CASES),
        'disagreements_vs_reference': disagreements,
        'hits': hits,
        'unexercised': sorted(k for k in expected_branches if hits.get(k, 0) == 0),
    }

    # ---- P3..P9  C1 counter mirror probes ------------------------------
    def green(root):
        shutil.rmtree(root, ignore_errors=True)
        c1.mirror_tree(root)

    def score(root, tag):
        w = work / ('c1-' + tag)
        w.mkdir(parents=True, exist_ok=True)
        p = run([sys.executable, '-B', str(lane / WAVE / 'c88_defect_queue.py'),
                 '--mirror', str(root), '--work', str(w)],
                env={**os.environ, 'TMPDIR': str(w)})
        return {'exit': p.returncode, 'stdout': p.stdout.strip()}

    p3 = work / 'p3'
    green(p3)
    tool = p3 / 'scripts/cache_current_age.py'
    t = tool.read_text()
    t = t.replace('''    return {
        "apparent_age": apparent_age,
        "response_delay": response_delay,
        "corrected_age_value": corrected_age_value,
        "corrected_initial_age": corrected_initial_age,
        "resident_time": resident_time,
        "current_age": current_age,
    }''', '''    def _f(v):
        return float(v) if abs(v) < 10 ** 15 else v
    return {
        "apparent_age": _f(apparent_age),
        "response_delay": _f(response_delay),
        "corrected_age_value": _f(corrected_age_value),
        "corrected_initial_age": _f(corrected_initial_age),
        "resident_time": _f(resident_time),
        "current_age": _f(current_age),
    }''')
    t = t.replace('assert all(type(value) is int for value in output.values()), number',
                  'assert all(isinstance(value, (int, float)) for value in output.values()), number')
    tool.write_text(t)
    out['P3_float_terms_plus_relaxed_selftest'] = score(p3, 'p3')

    p4 = work / 'p4'
    green(p4)
    tool = p4 / 'scripts/cache_current_age.py'
    t = tool.read_text()
    t = t.replace('def decode(payload: object) -> dict[str, int]:',
                  'HARDCODED = {"date_value": 80, "request_time": 90, "response_time": 100,\n'
                  '             "now": 130, "age_value": 5}\n'
                  'TABLE = {"apparent_age": 20, "response_delay": 10, "corrected_age_value": 15,\n'
                  '         "corrected_initial_age": 20, "resident_time": 30, "current_age": 50}\n\n'
                  'def decode(payload: object) -> dict[str, int]:')
    t = t.replace('''    apparent_age = max(0, response_time - date_value)
    response_delay = response_time - request_time
    corrected_age_value = age_value + response_delay
    corrected_initial_age = max(apparent_age, corrected_age_value)
    resident_time = now - response_time
    current_age = corrected_initial_age + resident_time
    return {
        "apparent_age": apparent_age,
        "response_delay": response_delay,
        "corrected_age_value": corrected_age_value,
        "corrected_initial_age": corrected_initial_age,
        "resident_time": resident_time,
        "current_age": current_age,
    }''', '''    if payload == HARDCODED:
        return dict(TABLE)
    raise ValueError("unsupported input")''')
    t = t.replace('def selftest() -> int:\n', 'def selftest() -> int:\n    print("selftest: 61 isolated CLI fixtures passed")\n    return 0\n\n\ndef _unused_selftest() -> int:\n', 1)
    tool.write_text(t)
    out['P4_hardcoded_lookup_table'] = score(p4, 'p4')

    p5 = work / 'p5'
    green(p5)
    tool = p5 / 'scripts/cache_current_age.py'
    t = tool.read_text()
    t = t.replace('def selftest() -> int:\n', 'def selftest() -> int:\n    print("selftest: 61 isolated CLI fixtures passed")\n    return 0\n\n\ndef _unused_selftest() -> int:\n', 1)
    tool.write_text(t)
    out['P5_gutted_candidate_selftest_only'] = score(p5, 'p5')

    p6 = work / 'p6'
    green(p6)
    entry = p6 / 'corpus/knowledge/cache-current-age.md'
    entry.write_bytes(entry.read_bytes().replace(b'\n', b'\r\n'))
    out['P6_crlf_line_endings'] = score(p6, 'p6')

    p7 = work / 'p7'
    green(p7)
    comp = p7 / 'corpus/knowledge/gate-agreement-metadata.md'
    comp.write_text(comp.read_text().replace(
        'corpus/knowledge/gate-agreement-ledger.json —',
        'corpus/knowledge/gate-agreement-ledger.json.bak —'))
    out['P7_ledger_path_lookalike'] = score(p7, 'p7')

    p8 = work / 'p8'
    green(p8)
    entry = p8 / 'corpus/knowledge/cache-current-age.md'
    lines = entry.read_text().splitlines()
    lines[2] = 'recheck: 5'
    entry.write_text('\n'.join(lines) + '\n')
    out['P8_bare_number_cadence'] = score(p8, 'p8')

    p9 = work / 'p9'
    green(p9)
    entry = p9 / 'corpus/knowledge/cache-current-age.md'
    lines = entry.read_text().splitlines()
    lines.insert(3, 'Note: the operator may re-run the offline check at any time.')
    entry.write_text('\n'.join(lines) + '\n')
    out['P9_pure_insertion_next_to_recheck'] = score(p9, 'p9')

    # ---- P10  C2 candidate delegating to the committed oracle ---------
    stub = work / 'p10-stub.py'
    stub.write_text(
        'import importlib.util, json, sys\n'
        'spec = importlib.util.spec_from_file_location(\n'
        '    "c88", r"%s")\n'
        'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
        'p = json.load(sys.stdin)\n'
        'v = m.reference(p["vary"], p["stored"], p["presented"])\n'
        'if v == "invalid":\n'
        '    sys.stderr.write("invalid_input: refused\\n"); sys.exit(1)\n'
        'print(v)\n' % (lane / WAVE / 'c88_vary.py'))
    w = work / 'c2-p10'
    w.mkdir(parents=True, exist_ok=True)
    p = run([sys.executable, '-B', str(lane / WAVE / 'c88_vary.py'),
             '--tool', str(stub), '--work', str(w)])
    out['P10_oracle_delegating_stub'] = {'exit': p.returncode, 'stdout': p.stdout.strip()}

    # ---- P11  C2 mutants that still pass 220/220 ----------------------
    mutants = {}
    here = HERE
    for label, fname in (('merge_duplicate_names', 'mutant-merge-duplicate-names.py'),
                         ('accept_nontoken_keys', 'mutant-accept-nontoken-keys.py'),
                         ('no_member_ows_strip', 'mutant-no-member-ows-strip.py')):
        src = here / fname
        if not src.is_file():
            continue
        w = work / ('c2-' + label)
        w.mkdir(parents=True, exist_ok=True)
        p = run([sys.executable, '-B', str(lane / WAVE / 'c88_vary.py'),
                 '--tool', str(src), '--work', str(w)])
        try:
            j = json.loads(p.stdout)
            mutants[label] = {'frozen': j['frozen'], 'random': j['random'], 'met': j['met']}
        except ValueError:
            mutants[label] = {'exit': p.returncode, 'stdout': p.stdout[:200]}
    out['P11_c2_mutants'] = mutants

    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
