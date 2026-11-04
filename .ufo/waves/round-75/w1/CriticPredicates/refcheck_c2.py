#!/usr/bin/env python3
"""refcheck_c2.py — critic's LITERAL reading of contract §C2, used because
scripts/instrument_receipts.py does not exist at base c9c5e48 or in the lane.
Not a deliverable; a measuring stick for the frozen predicate text."""
import argparse, hashlib, json, os, re, subprocess, sys

SEC = re.compile(r'^### Round (\d+) gate registry additions')
FILE = re.compile(r'((?:scripts|\.ufo)/[\w./-]+\.(?:py|mjs))')

def git(root, *a):
    return subprocess.run(['git','-C',root,*a], capture_output=True, text=True)

def blob(root, rev, path):
    p = git(root,'show',f'{rev}:{path}')
    return p.stdout.encode() if p.returncode == 0 else None

def population(root, rev):
    txt = git(root,'show',f'{rev}:SKILL.md').stdout
    rows, sec = [], None
    for line in txt.splitlines():
        m = SEC.match(line)
        if m: sec = int(m.group(1)); continue
        if line.startswith('### '): sec = None; continue
        if sec and line.startswith('| ') and line.count('|') >= 6:
            c = [x.strip() for x in line.strip().strip('|').split('|')]
            if c[0] == 'Name' or set(c[0]) <= set('-: '): continue
            if 'historical' in c[1]: continue
            rows.append(c)
    seen = []
    for c in rows:
        f = None
        if FILE.fullmatch(c[0]): f = c[0]
        else:
            for i in (2,4):
                m = FILE.search(c[i])
                if m: f = m.group(1); break
            if not f:
                m = FILE.search(' '.join(c))
                f = m.group(1) if m else None
        if f and f not in seen: seen.append(f)
    return seen

def entry_of(root, rev, path):
    b = blob(root, rev, path)
    if b is None: return None
    return {'path': path, 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b),
            'selftest_mode': bool(re.search(r'[\'"]--selftest[\'"]', b.decode('utf-8','replace')))}

def check(root, rev, receipt_path, derive):
    pop = population(root, rev) if derive == 'skill' else []
    raw = blob(root, rev, receipt_path)
    if raw is None:
        return {'population': len(pop), 'bound': 0, 'mismatches': len(pop),
                'met': False, 'why': 'receipt absent at rev'}
    rec = json.loads(raw.decode())
    ents = {e['path']: e for e in rec.get('files', [])}
    if derive == 'receipt':
        pop = list(ents); mism = 0; bound = 0
    else:
        mism = 0; bound = 0
    details = []
    for p in pop:
        o = entry_of(root, rev, p)
        e = ents.get(p)
        if e is None:
            mism += 1; details.append(f'MISSING {p}'); continue
        if o is None:
            mism += 1; details.append(f'UNRESOLVED {p}'); continue
        ok = (o['sha256'] == e.get('sha256') and o['bytes'] == e.get('bytes')
              and bool(o['selftest_mode']) == bool(e.get('selftest_mode')))
        if ok: bound += 1
        else: mism += 1; details.append(f'MISMATCH {p}')
    met = (bound == len(pop)) and (mism == 0)
    return {'population': len(pop), 'bound': bound, 'mismatches': mism, 'met': met,
            'receipt_revision': rec.get('revision'), 'revision_field_equals_rev': rec.get('revision') == rev,
            'details': details}

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--root'); ap.add_argument('--revision')
    ap.add_argument('--receipt', default='corpus/knowledge/instrument-receipts.json')
    ap.add_argument('--derive', default='skill', choices=['skill','receipt'])
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--date', default='2026-11-03')
    a = ap.parse_args()
    if a.write:
        pop = population(a.root, a.revision)
        files = [entry_of(a.root, a.revision, p) for p in pop]
        rec = {'schema': 'instrument-receipts/v1', 'revision': a.revision, 'date': a.date,
               'host': 'linux-x86_64', 'files': files}
        os.makedirs(os.path.dirname(os.path.join(a.root, a.receipt)), exist_ok=True)
        with open(os.path.join(a.root, a.receipt), 'w') as fh:
            json.dump(rec, fh, indent=1); fh.write('\n')
        print(f'wrote {len(files)} entries to {a.receipt}')
        sys.exit(0)
    r = check(a.root, a.revision, a.receipt, a.derive)
    print(f"C2ref revision={a.revision[:8]} derive={a.derive} population={r['population']} "
          f"bound={r['bound']} mismatches={r['mismatches']} met={str(r['met']).lower()} "
          f"receipt_revision={str(r.get('receipt_revision'))[:8]} rev_field_eq={r.get('revision_field_equals_rev')}")
    for d in r.get('details', [])[:20]: print('  ' + d)
