#!/usr/bin/env python3
"""Characterise ExecReader-mutant survivors: population coverage + concrete witnesses."""
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

CAND = HERE / 'exe_vary_match.py'


def kind_hit(case, kind):
    vary, stored, presented = case['vary'], case['stored'], case['presented']
    sides = [stored, presented]
    if kind == 'double_ws':
        return any(isinstance(s, str) and ('  ' in s or '\t' in s)
                   for side in sides for v in side.values()
                   for s in (v if isinstance(v, list) else [v]))
    if kind == 'mixed_list':
        return any(isinstance(v, list) and any(not isinstance(x, str) for x in v)
                   for side in sides for v in side.values())
    if kind == 'dup_case_key':
        return any(len([k.lower() for k in side]) != len({k.lower() for k in side}) for side in sides)
    if kind == 'absent_vs_empty':
        if not isinstance(vary, str):
            return False
        for name in [m.strip(' \t').lower() for m in vary.split(',')]:
            for a, b in ((stored, presented), (presented, stored)):
                la = {k.lower(): v for k, v in a.items()}
                lb = {k.lower(): v for k, v in b.items()}
                if name not in la and isinstance(lb.get(name), str) and lb[name] == '':
                    return True
        return False
    if kind == 'nonascii':
        return any(not all(ord(ch) < 128 for ch in str(s))
                   for side in sides for key, v in side.items()
                   for s in [key] + (v if isinstance(v, list) else [v]))
    if kind == 'star_with_invalid':
        star = isinstance(vary, str) and any(m.strip(' \t') == '*' for m in vary.split(','))
        return star and C.reference(vary, stored, presented) == 'invalid'
    if kind == 'star_at_all':
        return isinstance(vary, str) and any(m.strip(' \t') == '*' for m in vary.split(','))
    raise ValueError(kind)


KINDS = ['double_ws', 'mixed_list', 'dup_case_key', 'absent_vs_empty', 'nonascii',
         'star_with_invalid', 'star_at_all']

WITNESSES = {
    'e08_internal_ws_collapse': {'vary': 'accept-encoding',
                                 'stored': {'accept-encoding': 'gzip;  q=1'},
                                 'presented': {'accept-encoding': 'gzip; q=1'}},
    'e10_dupkey_refusal_removed': {'vary': 'accept-encoding',
                                   'stored': {'Accept-Encoding': 'gzip', 'accept-encoding': 'br'},
                                   'presented': {'accept-encoding': 'br'}},
    'e15_empty_value_absent': {'vary': 'accept-encoding', 'stored': {},
                               'presented': {'accept-encoding': ''}},
    'e16_list_elem_check_removed': {'vary': 'accept-encoding',
                                    'stored': {'accept-encoding': ['gzip', 5]},
                                    'presented': {'accept-encoding': 'gzip, 5'}},
    'e21_token_too_permissive': {'vary': 'caf\u00e9', 'stored': {'caf\u00e9': 'x'},
                                 'presented': {'caf\u00e9': 'x'}},
}


def run(tool, payload):
    p = subprocess.run([sys.executable, '-B', str(tool)], input=json.dumps(payload),
                       capture_output=True, text=True, timeout=30)
    return dict(exit=p.returncode, out=p.stdout.strip(),
                err=p.stderr.strip().splitlines()[-1] if p.stderr.strip() else '')


def main():
    sweep = json.loads((HERE / 'receipts' / 'exec_sweep.json').read_text())
    out = dict(source_sha256=sweep['source_sha256'], baselines=sweep['baselines'],
               populations={k: {'frozen': sum(kind_hit(c, k) for c in C.CASES),
                                'random': sum(kind_hit(c, k) for c in C.RANDOM_CASES)}
                            for k in KINDS},
               kills=[], witnesses={}, equivalence={})
    print('population coverage (v3 reference labels):')
    for k, v in out['populations'].items():
        print(f'  {k:18s} frozen={v["frozen"]:2d}/20  random={v["random"]:3d}/200')

    print('\nkill attribution per mutant (frozen cases that failed / random cases that failed):')
    for m in sweep['mutants']:
        s3 = m['scores']['v3-live']
        frozen_hits = [c for c in s3['failed_cases'] if not str(c).startswith('r')]
        row = dict(name=m['name'], exit=s3['exit'], frozen=s3['frozen'], random=s3['random'],
                   met=s3['met'], frozen_killers=frozen_hits, failed_cases=s3['failed_cases'],
                   caught_by_events=s3['detail_events'])
        out['kills'].append(row)
        tag = 'KILLED ' if s3['exit'] != 0 else 'SURVIVED'
        print(f'  {m["name"]:30s} {tag} frozen={s3["frozen"]}/20 random={s3["random"]}/200 '
              f'frozen_killers={frozen_hits}')

    print('\nwitness divergence (candidate vs mutant):')
    for name, payload in WITNESSES.items():
        a = run(CAND, payload)
        b = run(HERE / 'mutants_exec' / f'{name}.py', payload)
        diverges = (a['exit'], a['out'], a['err'].startswith('invalid_input:')) != \
                   (b['exit'], b['out'], b['err'].startswith('invalid_input:'))
        out['witnesses'][name] = dict(payload=payload, candidate=a, mutant=b, diverges=diverges)
        print(f'  {name}')
        print(f'    payload   {json.dumps(payload, sort_keys=True)}')
        print(f'    candidate exit={a["exit"]} out={a["out"]!r} err={a["err"]!r}')
        print(f'    mutant    exit={b["exit"]} out={b["out"]!r} err={b["err"]!r}')
        print(f'    diverges={diverges}')

    # e20 claims to be equivalent: 100k-input differential against the candidate,
    # compared in-process on the same decide() the CLI calls.
    import importlib.util as _iu
    import random as _r

    def load(path, name):
        s = _iu.spec_from_file_location(name, path)
        m = _iu.module_from_spec(s)
        s.loader.exec_module(m)
        return m

    cand_mod = load(CAND, 'cand_mod')
    e20_mod = load(HERE / 'mutants_exec' / 'e20_dedup_removed.py', 'e20_mod')
    rng = _r.Random(880_088)
    keys = ['accept-encoding', 'Accept-Encoding', 'accept-language', 'x-kake-token', 'a']
    vals = ['', ' ', 'gzip', ' gzip ', 'GZIP', 'gzip, br', 'gzip; q=1', ['gzip', 'br'],
            ['br', 'gzip'], [], 5, True, None, '\tgzip\t']
    varys = ['', '*', ' ', ',', 'a,,b', 'accept-encoding', 'Accept-Encoding',
             'accept-encoding, *', 'accept encoding', 'accept-encoding,accept-language',
             'Accept-Encoding, accept-encoding', 'accept-encoding , accept-language']
    splits = []
    n = 100_000
    for _ in range(n):
        payload = {'vary': rng.choice(varys),
                   'stored': {rng.choice(keys): rng.choice(vals) for _ in range(rng.randint(0, 3))},
                   'presented': {rng.choice(keys): rng.choice(vals) for _ in range(rng.randint(0, 3))}}
        a = cand_mod.decide(payload)
        b = e20_mod.decide(payload)
        if a != b:
            splits.append(dict(payload=payload, candidate=list(a), mutant=list(b)))
            if len(splits) >= 5:
                break
    out['equivalence']['e20_dedup_removed'] = dict(sampled=n, splits=splits, in_process=True)
    print(f'\ne20 dedup-removal differential over {n} in-process inputs: {len(splits)} splits '
          f'(0 = equivalent mutant)')

    (HERE / 'receipts' / 'exec_survivors.json').write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
