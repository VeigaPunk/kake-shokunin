#!/usr/bin/env python3
"""Disposable counter mutants; no lane source writes, no network, no VCS mutation."""
import concurrent.futures as cf
import difflib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
S = Path('/fast/scratch/hyaku/kake-r84/MutC')
OUT = ROOT / '.ufo/waves/round-84/w1/MutC'
FROZEN = ROOT / '.ufo/waves/round-84'

def digest(b):
    return hashlib.sha256(b).hexdigest()

def run(argv, work):
    work.mkdir(parents=True, exist_ok=True)
    p = subprocess.run([str(a) for a in argv], cwd=S, capture_output=True, text=True,
                       timeout=60, env={**os.environ, 'TMPDIR': str(work), 'PYTHONDONTWRITEBYTECODE': '1'})
    return dict(command=[str(a) for a in argv], exit=p.returncode, stdout=p.stdout, stderr=p.stderr)

def put(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)

def copied(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)

sources = {k: (FROZEN / name).read_bytes() for k, name in
           [('C1', 'c84_defect_queue.py'), ('C2', 'c84_policy_values.py')]}
paths = {'C1': FROZEN / 'c84_defect_queue.py', 'C2': FROZEN / 'c84_policy_values.py'}

try:
    # Freeze independent local copies before launching the concurrent probes.
    base = S / 'c1-pristine.py'
    base.write_bytes(sources['C1'])
    spec = importlib.util.spec_from_file_location('c1_pristine', base)
    c1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c1)
    good1 = S / 'c1-good'
    c1.write_fixture(good1, lesson=c1.good_lesson(), spec=c1.good_spec(),
                     results=c1.good_results(), receipt=c1.good_receipt(), rfc=c1.good_rfc())
    bad1 = {}
    for name in ('retained', 'connector', 'w04'):
        target = S / ('c1-' + name)
        shutil.copytree(good1, target)
        bad1[name] = target
    rfc = bad1['retained'] / c1.RFC
    rfc.write_text(rfc.read_text().replace(c1.HEADINGS[0], 'missing retained heading'))
    put(bad1['connector'], c1.SPEC, json.dumps({'items': [{'name': 'E', 'role': 'executor'}]}))
    put(bad1['w04'], c1.CENSUS, c1.good_receipt().replace('S002', 'S009'))

    good2 = S / 'c2-good'
    for rel in ['scripts/policy_value_class.py', 'scripts/header_change_class.py',
                '.ufo/waves/round-81/capture', '.ufo/waves/round-82/capture',
                '.ufo/waves/round-81/capture-expectations.json',
                '.ufo/waves/round-84/capture-control', '.ufo/waves/round-84/policy-expectations.json']:
        copied(ROOT / rel, good2 / rel)
    real = run([sys.executable, '-B', good2 / 'scripts/policy_value_class.py',
                '--a', good2 / '.ufo/waves/round-81/capture',
                '--b', good2 / '.ufo/waves/round-82/capture',
                '--declared', good2 / '.ufo/waves/round-81/capture-expectations.json'], S / 'record-work')
    (OUT / 'record-generation.json').write_text(json.dumps(real, indent=2))
    if real['exit'] != 0:
        raise RuntimeError('Cannot produce real-pair positive fixture: ' + real['stderr'])
    put(good2, '.ufo/waves/round-84/controls/tool-real-pair.txt', real['stdout'])
    bad2 = {}
    for name in ('truncated', 'expectation', 'record'):
        target = S / ('c2-' + name)
        shutil.copytree(good2, target)
        bad2[name] = target
    receipt_rel = '.ufo/waves/round-84/capture-control/control/a/ds4cc-primary/response.json'
    rp = bad2['truncated'] / receipt_rel
    doc = json.loads(rp.read_text()); doc['truncated'] = True
    rp.write_text(json.dumps(doc))
    ep = bad2['expectation'] / '.ufo/waves/round-84/policy-expectations.json'
    doc = json.loads(ep.read_text()); doc['control']['ds4cc-primary']['cache-control'] = 'reordered'
    ep.write_text(json.dumps(doc))
    put(bad2['record'], '.ufo/waves/round-84/controls/tool-real-pair.txt', real['stdout'] + 'stale record\n')

    mutants = [
        ('C1-retained', 'C1', 'heading not in line or heading not in rfc', 'heading not in line', bad1['retained']),
        ('C1-connector', 'C1', 'state = spec_connectors >= 1 and len(settled) >= 1', 'state = len(settled) >= 1', bad1['connector']),
        ('C1-w04', 'C1', 'state = claimed == derived', 'state = len(claimed) == len(derived)', bad1['w04']),
        ('C2-truncated', 'C2', 'return receipt.get("truncated") is False', 'return True', bad2['truncated']),
        ('C2-expectation', 'C2', 'and flags["ctl_changed"] == 3 and flags["ctl_mismatch"] == 0', 'and flags["ctl_changed"] == 3', bad2['expectation']),
        ('C2-record', 'C2', 'and flags["record_equal"] == 1 and flags["determinism"] == 1', 'and flags["determinism"] == 1', bad2['record']),
    ]

    def probe(item):
        name, family, old, new, bad = item
        folder = S / name; folder.mkdir()
        executable = folder / 'counter.py'
        original = sources[family]
        text = original.decode()
        assert text.count(old) == 1, (name, text.count(old))
        mutant = text.replace(old, new).encode()
        diff = ''.join(difflib.unified_diff(text.splitlines(True), mutant.decode().splitlines(True), fromfile='pristine', tofile=name))
        (OUT / (name + '.diff')).write_text(diff)
        readings = {}
        def detect(phase):
            work = folder / phase
            selftest = run([sys.executable, '-B', executable, '--selftest'] +
                           (['--work', work / 'selftest'] if family == 'C1' else []), work / 'temp')
            good = good1 if family == 'C1' else good2
            positive = run([sys.executable, '-B', executable, '--root', good] +
                           (['--work', work / 'positive'] if family == 'C2' else []), work / 'temp')
            negative = run([sys.executable, '-B', executable, '--root', bad] +
                           (['--work', work / 'negative'] if family == 'C2' else []), work / 'temp')
            return dict(hash=digest(executable.read_bytes()), selftest=selftest, positive=positive, negative=negative)
        try:
            executable.write_bytes(original)
            readings['pristine'] = detect('pristine')
            executable.write_bytes(mutant)
            readings['mutant'] = detect('mutant')
        finally:
            executable.write_bytes(original)
            readings['restored'] = detect('restored')
        p, m, r = (readings[k] for k in ('pristine', 'mutant', 'restored'))
        baseline_ok = p['selftest']['exit'] == p['positive']['exit'] == 0 and p['negative']['exit'] == 1
        restored_ok = r['hash'] == p['hash'] and all(r[k]['exit'] == p[k]['exit'] and r[k]['stdout'] == p[k]['stdout'] for k in ('selftest', 'positive', 'negative'))
        if not baseline_ok or not restored_ok:
            verdict = 'inconclusive'
        elif any(m[k]['exit'] != p[k]['exit'] for k in ('selftest', 'positive', 'negative')):
            verdict = 'killed'
        else:
            verdict = 'survived'
        result = dict(name=name, family=family, old=old, new=new, fixture=str(bad),
                      verdict=verdict, baseline_ok=baseline_ok, restored_ok=restored_ok, readings=readings)
        (OUT / (name + '.json')).write_text(json.dumps(result, indent=2))
        return result

    with cf.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(probe, mutants))
    final_selftests = {}
    for family in ('C1', 'C2'):
        executable = S / ('final-' + family + '.py'); executable.write_bytes(sources[family])
        final_selftests[family] = run([sys.executable, '-B', executable, '--selftest'] +
                                       (['--work', S / 'final-c1-work'] if family == 'C1' else []), S / 'final-temp')
    hashes = {family: dict(before=digest(b), after=digest(paths[family].read_bytes())) for family, b in sources.items()}
    summary = dict(axes=['guard discrimination', 'fixture fidelity', 'exact restoration'],
                   results=results, final_selftests=final_selftests, source_hashes=hashes,
                   installs=[], scratch_cleanup='performed in finally')
    (OUT / 'results.json').write_text(json.dumps(summary, indent=2))
    for result in results:
        print(result['name'], result['verdict'],
              {phase: {k: result['readings'][phase][k]['exit'] for k in ('selftest', 'positive', 'negative')}
               for phase in ('pristine', 'mutant', 'restored')})
    print('final_selftests', {k: (v['exit'], v['stdout'].splitlines()[-1]) for k, v in final_selftests.items()})
    print('source_hashes', hashes)
finally:
    shutil.rmtree(S)
