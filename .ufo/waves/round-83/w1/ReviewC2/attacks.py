#!/usr/bin/env python3
"""ReviewC2 round-83 attack harness (scratch only; reads the lane read-only)."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/kake-r83/ReviewC2')
LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
COUNTER = LANE / '.ufo/waves/round-83/c83_drift_class.py'
TOOL = LANE / 'scripts/header_change_class.py'
PY = sys.executable
STAMP = 'Tue, 04 Nov 2026 10:00:00 GMT'


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def rec(d: Path, body: bytes, headers: dict, status: int = 200,
        url: str = 'https://example.test/') -> None:
    d.mkdir(parents=True, exist_ok=True)
    (d / 'body.bin').write_bytes(body)
    doc = {"bodyFile": "body.bin", "bytes": len(body),
           "fetchedAt": "2026-11-04T00:00:00Z", "finalUrl": url,
           "headers": [{"name": k, "value": v} for k, v in headers.items()],
           "method": "GET", "sha256": sha(body), "status": status,
           "truncated": False, "url": url}
    (d / 'response.json').write_text(json.dumps(doc, indent=1), encoding='utf-8')


def run(cmd, cwd=None):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def fresh(p: Path) -> Path:
    if p.exists():
        shutil.rmtree(p)
    p.mkdir(parents=True)
    return p


DECL = json.loads((LANE / '.ufo/waves/round-81/capture-expectations.json').read_text())
SURFACES = [s['id'] for s in DECL['surfaces']]

# ---------------------------------------------------------------- Q2 fabricated
print('=' * 20, 'Q2 fabrication: synthetic receipts, no socket')
Q2 = fresh(S / 'q2-fabricated')
(Q2 / 'scripts').mkdir()
(Q2 / 'scripts/header_change_class.py').write_text(TOOL.read_text(encoding='utf-8'), encoding='utf-8')
(Q2 / '.ufo/waves/round-81').mkdir(parents=True)
(Q2 / '.ufo/waves/round-81/capture-expectations.json').write_text(
    json.dumps(DECL, indent=1), encoding='utf-8')
A_H = {"Date": STAMP, "ETag": '"ghost-a"', "Content-Length": "18",
       "Content-Type": "text/plain", "Cache-Control": "max-age=600", "X-Cache": "HIT"}
B_H = dict(A_H, Date='Tue, 04 Nov 2026 11:00:00 GMT', **{"X-Cache": "MISS"})
GHOST = {sid: ('ghost-body-for-' + sid).encode() for sid in SURFACES}
for sid in SURFACES:
    body = GHOST[sid]
    a_h = dict(A_H, **{"Content-Length": str(len(body))})
    b_h = dict(B_H, **{"Content-Length": str(len(body))})
    # receipts point at example.test even though the declaration names ds4cc.com
    rec(Q2 / '.ufo/waves/round-81/capture' / sid, body, a_h, url='https://example.test/')
    rec(Q2 / '.ufo/waves/round-82/capture' / sid, body, b_h, url='https://example.test/')
# control pair: copy the committed one (it is evidence, only the captures are fabricated)
shutil.copytree(LANE / '.ufo/waves/round-83/capture-control',
                Q2 / '.ufo/waves/round-83/capture-control')
# generate the record exactly as build_green does: from the tool's own stdout
rc, out, err = run([PY, '-B', str(COUNTER.parent / 'c83_drift_class.py'), '--help'])
rc, out, err = run([PY, '-B', str(Q2 / 'scripts/header_change_class.py'),
                    '--a', str(Q2 / '.ufo/waves/round-81/capture'),
                    '--b', str(Q2 / '.ufo/waves/round-82/capture'),
                    '--declared', str(Q2 / '.ufo/waves/round-81/capture-expectations.json')])
print(f'tool_on_fabricated rc={rc}\n{out}')
(Q2 / '.ufo/waves/round-83/controls').mkdir(parents=True)
(Q2 / '.ufo/waves/round-83/controls/after-c2-classes.txt').write_bytes(out.encode())
rc, out2, err2 = run([PY, '-B', str(COUNTER), '--root', str(Q2), '--work', str(S / 'q2-work')])
print(f'counter_on_fabricated rc={rc}\n{out2}{err2}')

# empty-body variant: bytes=0, sha256(e3b0...) verifies
Q2E = S / 'q2-empty'
if Q2E.exists():
    shutil.rmtree(Q2E)
shutil.copytree(Q2, Q2E)
for sid in SURFACES:
    for tree in ('.ufo/waves/round-81/capture', '.ufo/waves/round-82/capture'):
        d = Q2E / tree / sid
        (d / 'body.bin').write_bytes(b'')
        doc = json.loads((d / 'response.json').read_text())
        doc['bytes'] = 0
        doc['sha256'] = sha(b'')
        doc['headers'] = [h for h in doc['headers'] if h['name'].lower() != 'content-length']
        (d / 'response.json').write_text(json.dumps(doc, indent=1))
rc, outE, errE = run([PY, '-B', str(COUNTER), '--root', str(Q2E), '--work', str(S / 'q2e-work')])
print(f'counter_on_empty_bodies rc={rc}\n{outE}{errE}')

# ---------------------------------------------------------------- Q3 classification
print('=' * 20, 'Q3 classification attack')
BASE = {"Date": STAMP, "Content-Type": "text/plain", "Content-Length": "5",
        "Cache-Control": "max-age=600"}


def case(name, a_extra, b_extra, a_body=b'hello', b_body=b'hello'):
    root = fresh(S / 'q3' / name)
    (root / 'd.json').write_text(json.dumps(
        {"surfaces": [{"id": "s1", "url": "https://ds4cc.com/"}]}), encoding='utf-8')
    rec(root / 'a/s1', a_body, dict(BASE, **a_extra))
    rec(root / 'b/s1', b_body, dict(BASE, **b_extra))
    rc, out, err = run([PY, '-B', str(TOOL), '--a', str(root / 'a'),
                        '--b', str(root / 'b'), '--declared', str(root / 'd.json')])
    line = [ln for ln in out.splitlines() if ln.startswith('surface=')]
    print(f'[{name}] rc={rc} {line[0] if line else out}{err}')
    return rc, line[0] if line else ''


case('robots-tag', {'X-Robots-Tag': 'noindex, nofollow'}, {'X-Robots-Tag': 'index, follow'})
case('link-canonical',
     {'Link': '<https://ds4cc.com/>; rel="canonical"'},
     {'Link': '<https://other.example/>; rel="canonical"'})
case('accept-ranges', {'Accept-Ranges': 'bytes'}, {})
case('digest', {'Digest': 'sha-256=AAAA'}, {'Digest': 'sha-256=BBBB'})
case('last-modified', {'Last-Modified': 'Tue, 04 Nov 2026 08:00:00 GMT'},
     {'Last-Modified': 'Tue, 04 Nov 2026 09:00:00 GMT'})
case('vary', {}, {'Vary': 'Accept-Encoding'})
# contract wildcard vs code enumeration
case('acac', {}, {'Access-Control-Allow-Credentials': 'true'})
case('content-type', {'Content-Type': 'text/plain'}, {'Content-Type': 'text/html'})

# ---------------------------------------------------------------- Q4 control pair
print('=' * 20, 'Q4 control-pair attack')
Q4B = S / 'q4-base'
if Q4B.exists():
    shutil.rmtree(Q4B)
(Q4B / 'scripts').mkdir(parents=True)
(Q4B / 'scripts/header_change_class.py').write_text(TOOL.read_text(encoding='utf-8'), encoding='utf-8')
for rel in ('.ufo/waves/round-81/capture-expectations.json',):
    (Q4B / rel).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(LANE / rel, Q4B / rel)
for rel in ('.ufo/waves/round-81/capture', '.ufo/waves/round-82/capture',
            '.ufo/waves/round-83/capture-control'):
    shutil.copytree(LANE / rel, Q4B / rel)
(Q4B / '.ufo/waves/round-83/controls').mkdir(parents=True)
shutil.copy2(LANE / '.ufo/waves/round-83/controls/after-c2-classes.txt',
             Q4B / '.ufo/waves/round-83/controls/after-c2-classes.txt')


def clone(name: Path) -> Path:
    if name.exists():
        shutil.rmtree(name)
    shutil.copytree(Q4B, name)
    return name


def normalize(root: Path, mutate):
    """Make control B bodies byte-identical to A, then apply one header delta."""
    for sid in SURFACES:
        a_dir = root / '.ufo/waves/round-83/capture-control/a' / sid
        b_dir = root / '.ufo/waves/round-83/capture-control/b' / sid
        body = (a_dir / 'body.bin').read_bytes()
        (b_dir / 'body.bin').write_bytes(body)
        a = json.loads((a_dir / 'response.json').read_text())
        b = json.loads((b_dir / 'response.json').read_text())
        ha = {h['name'].lower(): h['value'] for h in a['headers']}
        hb = dict(ha)
        mutate(ha, hb, body)
        a['bytes'] = len(body)
        a['sha256'] = sha(body)
        b['bytes'] = len(body)
        b['sha256'] = sha(body)
        a['headers'] = [{"name": k, "value": v} for k, v in ha.items()]
        b['headers'] = [{"name": k, "value": v} for k, v in hb.items()]
        (a_dir / 'response.json').write_text(json.dumps(a, indent=1))
        (b_dir / 'response.json').write_text(json.dumps(b, indent=1))


def counter(root: Path, tag: str):
    rc, out, err = run([PY, '-B', str(COUNTER), '--root', str(root),
                        '--work', str(S / ('work-' + tag))])
    print(f'[{tag}] rc={rc}\n{out}{err}')
    return rc, out


counter(Q4B, 'q4-base')

CL = clone(S / 'q4-content-length')


def cl_mut(ha, hb, body):
    hb['content-length'] = str(len(body) + 1)


normalize(CL, cl_mut)
counter(CL, 'q4-content-length')

LM = clone(S / 'q4-last-modified')


def lm_mut(ha, hb, body):
    ha['last-modified'] = 'Tue, 04 Nov 2026 08:00:00 GMT'
    hb['last-modified'] = 'Tue, 04 Nov 2026 09:00:00 GMT'


normalize(LM, lm_mut)
counter(LM, 'q4-last-modified')

# ---------------------------------------------------------------- mutant classifier
print('=' * 20, 'mutant classifier: representation headers folded into policy')
MUT = clone(S / 'q4-mutant')
src = TOOL.read_text(encoding='utf-8')
rep_block = re.search(r'REPRESENTATION = \{.*?\n\}', src, re.S)
names = re.findall(r'"([^"]+)"', rep_block.group(0))
print('moved names:', names)
mut_src = src[:rep_block.start()] + 'REPRESENTATION = set()' + src[rep_block.end():]
policy = re.search(r'POLICY = \{.*?\n\}', mut_src, re.S)
tail = policy.group(0).rsplit('}', 1)[0].rstrip()
mut_src = mut_src[:policy.start()] + tail + '\n    ' + ', '.join(f'"{n}"' for n in names) + ',\n}' + mut_src[policy.end():]
(MUT / 'scripts/header_change_class.py').write_text(mut_src, encoding='utf-8')
rc, out, err = run([PY, '-B', str(MUT / 'scripts/header_change_class.py'), '--selftest',
                    '--work', str(S / 'mut-selftest')])
print(f'mutant_selftest rc={rc}\n{out}{err}')
counter(MUT, 'q4-mutant')
# what the mutant says about a real representation change
cc = S / 'q3/content-type'
rc, out, err = run([PY, '-B', str(MUT / 'scripts/header_change_class.py'),
                    '--a', str(cc / 'a'), '--b', str(cc / 'b'),
                    '--declared', str(cc / 'd.json')])
print(f'mutant_on_content_type_change rc={rc}\n{out}')

# ---------------------------------------------------------------- Q1 offline probes
print('=' * 20, 'Q1 tool_offline evasion probes')
probe = S / 'c83_probe.py'
probe.write_text(COUNTER.read_text(encoding='utf-8'), encoding='utf-8')
import importlib.util
spec = importlib.util.spec_from_file_location('c83probe', str(probe))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
print('tool_offline(real tool) =', mod.tool_offline(LANE))
base_src = TOOL.read_text(encoding='utf-8')


def probe_mut(name, text):
    d = fresh(S / 'q1' / name)
    (d / 'scripts').mkdir()
    (d / 'scripts/header_change_class.py').write_text(text, encoding='utf-8')
    verdict = mod.tool_offline(d)
    compile(text, str(d / 'scripts/header_change_class.py'), 'exec')  # must stay valid Python
    print(f'{name}: tool_offline={verdict}')
    return verdict


probe_mut('nested-import', base_src + '\n\ndef helper():\n    import socket\n')
probe_mut('importlib-concat',
          base_src + '\nimport importlib\n_m = importlib.import_module("sock" + "et")\n')
probe_mut('http-from-import', base_src + '\nfrom http import client\n')
probe_mut('subprocess-curl',
          base_src + '\nimport subprocess\nsubprocess.run(["curl", "-sS", "https://ds4cc.com/"])\n')
probe_mut('os-wget', base_src + '\nimport os\nos.system("wget -qO- https://ds4cc.com/")\n')
probe_mut('socket-honest', base_src + '\nimport socket\n')
# docstring-substring hole: docstring value used as a text replacement key
import ast as _ast
_tree = _ast.parse(base_src)
_doc = _tree.body[0].value.value
hole = base_src.replace(_doc, 'sock', 1) + '\nimport socket\n'
probe_mut('docstring-substring-sock', hole)
print('DONE')
