#!/usr/bin/env python3
"""Characterise the C2 populations and confirm each surviving mutant's divergence.

For every survivor: (1) count how many frozen/random cases could have exposed it,
(2) run a concrete witness through both the pristine reference and the mutant and
print the actual exits/streams.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path('/fast/scratch/hyaku/kake-r88/MutReader')
LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
COUNTER = LANE / '.ufo/waves/round-88/c88_vary.py'

spec = importlib.util.spec_from_file_location('c88vary', COUNTER)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)


def has_kind(case, kind):
    vary, stored, presented = case['vary'], case['stored'], case['presented']
    if kind == 'double_ws':
        for side in (stored, presented):
            for v in side.values():
                for s in (v if isinstance(v, list) else [v]):
                    if isinstance(s, str) and ('  ' in s or '\t' in s):
                        return True
        return False
    if kind == 'mixed_list':
        for side in (stored, presented):
            for v in side.values():
                if isinstance(v, list) and any(not isinstance(x, str) for x in v):
                    return True
        return False
    if kind == 'dup_case_key':
        for side in (stored, presented):
            lows = [k.lower() for k in side]
            if len(lows) != len(set(lows)):
                return True
        return False
    if kind == 'absent_vs_empty':
        names = []
        if isinstance(vary, str):
            names = [m.strip(' \t').lower() for m in vary.split(',')]
        for name in names:
            for a, b in ((stored, presented), (presented, stored)):
                low_a = {k.lower(): v for k, v in a.items()}
                low_b = {k.lower(): v for k, v in b.items()}
                if name not in low_a and isinstance(low_b.get(name), str) and low_b[name] == '':
                    return True
        return False
    raise ValueError(kind)


KINDS = ['double_ws', 'mixed_list', 'dup_case_key', 'absent_vs_empty']

WITNESSES = {
    'm08_internal_ws_collapse': {'vary': 'accept-encoding',
                                 'stored': {'accept-encoding': 'gzip;  q=1'},
                                 'presented': {'accept-encoding': 'gzip; q=1'}},
    'm11_dupkey_refusal_removed': {'vary': 'accept-encoding',
                                   'stored': {'Accept-Encoding': 'gzip', 'accept-encoding': 'br'},
                                   'presented': {'accept-encoding': 'br'}},
    'm16_empty_value_absent': {'vary': 'accept-encoding',
                               'stored': {},
                               'presented': {'accept-encoding': ''}},
    'm17_list_elem_check_removed': {'vary': 'accept-encoding',
                                    'stored': {'accept-encoding': ['gzip', 5]},
                                    'presented': {'accept-encoding': 'gzip, 5'}},
}


def run(tool, payload):
    p = subprocess.run([sys.executable, '-B', str(tool)], input=json.dumps(payload),
                       capture_output=True, text=True, timeout=20)
    return dict(exit=p.returncode, out=p.stdout.strip(), err=p.stderr.strip().splitlines()[-1] if p.stderr.strip() else '')


def main():
    out = {'populations': {}, 'frozen_total': len(C.CASES), 'random_total': len(C.RANDOM_CASES)}
    for kind in KINDS:
        out['populations'][kind] = {
            'frozen': sum(has_kind(c, kind) for c in C.CASES),
            'random': sum(has_kind(c, kind) for c in C.RANDOM_CASES),
        }
    print('population coverage of the witness classes:')
    for kind, v in out['populations'].items():
        print(f'  {kind:18s} frozen={v["frozen"]:2d}/20  random={v["random"]:3d}/200')

    out['witnesses'] = {}
    print('\nwitness divergence (pristine reference vs mutant):')
    for name, payload in WITNESSES.items():
        ref = run(HERE / 'ref_vary_match.py', payload)
        mut = run(HERE / 'mutants' / f'{name}.py', payload)
        out['witnesses'][name] = dict(payload=payload, ref=ref, mutant=mut,
                                      diverges=(ref['exit'], ref['out'], ref['err'].startswith('invalid_input:')) !=
                                               (mut['exit'], mut['out'], mut['err'].startswith('invalid_input:')))
        print(f'  {name}')
        print(f'    payload  {json.dumps(payload, sort_keys=True)}')
        print(f'    ref      exit={ref["exit"]} out={ref["out"]!r} err={ref["err"]!r}')
        print(f'    mutant   exit={mut["exit"]} out={mut["out"]!r} err={mut["err"]!r}')
        print(f'    diverges={out["witnesses"][name]["diverges"]}')

    # equivalence sweep for the guard-removal mutant: any input at all that splits it from ref?
    import random as _r
    rng = _r.Random(880_088)
    keys = ['accept-encoding', 'Accept-Encoding', 'ACCEPT-ENCODING', 'accept-language',
            'x-kake-token', 'accept encoding', 'a', 'A']
    vals = ['', ' ', 'gzip', ' gzip ', 'GZIP', 'gzip, br', 'gzip,  br', 'gzip; q=1',
            'gzip;  q=1', ['gzip', 'br'], ['br', 'gzip'], ['gzip', 5], [], 5, True, None,
            '\tgzip\t']
    varys = ['', '*', ' ', ',', 'a,,b', 'accept-encoding', 'Accept-Encoding',
             'accept-encoding, *', 'accept encoding', 'accept-encoding,accept-language',
             'accept-encoding , accept-language', 5, None]
    splits = []
    n = 40_000
    for _ in range(n):
        vary = rng.choice(varys)
        def side():
            return {rng.choice(keys): rng.choice(vals) for _ in range(rng.randint(0, 3))}
        payload = {'vary': vary, 'stored': side(), 'presented': side()}
        want = C.reference(payload['vary'], payload['stored'], payload['presented'])
        got = run(HERE / 'mutants' / 'm19_empty_member_guard_removed.py', payload)
        got_v = 'invalid' if got['exit'] == 1 else got['out']
        if got_v != want:
            splits.append(dict(payload=payload, want=want, got=got))
            if len(splits) >= 5:
                break
    out['m19_equivalence'] = dict(sampled=n, splits=splits)
    print(f'\nm19 guard-removal differential over {n} random inputs: {len(splits)} splits '
          f'(0 = semantically equivalent, i.e. an equivalent mutant the counter cannot and should not kill)')
    for s in splits:
        print('  split', json.dumps(s, sort_keys=True))

    (HERE / 'receipts' / 'c2_survivors.json').write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
