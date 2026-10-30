# ReviewerC1Unresolved — unresolved-gate review

## Scope and recommendation

Attacked C1's disagreement count, resolution subtraction, negative handling, and Gate/spot binding at measured T0 `4c8295fa5e3b628f1fdf3840299ae415c01849fb` against base `1a48131577ba82c967650561be34e8dba909432a`. Axes: truthful unresolved count; evidence-bound resolution; rejection without collateral mutation. Recommendation: **do not credit semantic closure on this evidence**. Arithmetic masking is repaired, but marker/negated Gate and synthetic spot inputs still admit. This is a review recommendation, not an admission or authoritative wave judgment.

## Findings, highest severity first

### High — a Gate explicitly denying resolution still subtracts a disagreement and admits

Definition: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:252-259` computes `lesson_gate` solely from required substrings within `## Gate`. Caller `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:267-270` then spends that flag as one resolved disagreement. It never checks an affirmative resolution decision or excludes denial. The ordinary marker fixture and the same Gate followed by **“No disagreement is resolved; this Gate rejects the claimed resolution.”** both print `lesson_gate=1 unresolved=0 met=true`, exit 0, in independent canonical-counter subprocesses.

The exact replacement Gate is:

```markdown
# lesson

## Gate

S432 / Fetch is only a generic lead-in, not substantive evidence for a response-header expectation; collapsed-only; c64_calibration.py; author-side.

No disagreement is resolved; this Gate rejects the claimed resolution.
```

All other blobs remain T0 bytes, including genuine pinned evidence and existing knowledge correction. Therefore this demonstrates a **false assertion of Gate closure**, not fabricated source extraction and not proof that the entire underlying knowledge correction is false. Block-level verdict-token binding alone does not answer the assigned question “lesson_gate=1 without any real resolution”. The existing selftest itself exercises a marker Gate with the real span at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:391-402`, but only checks aggregate rejection while other components remain red; it misses the all-other-components-green case.

### High — spot verdict provenance is not actually bound to the spot blob

At `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:193-198`, the spot file need only exist and contain one physical line with `S432` and `Disagree`. It is absent from pinned blobs at lines 90-95. The required reason at lines 78-81 is checked only against the lesson at line 256, never the actual spot bytes. Replacing the complete spot-check with exactly `S432 Disagree\n` still prints all components 1 and `met=true`, exit 0. The actual historical verdict is `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-61-verifier-spotcheck.md:33`; the synthetic replacement has no verdict row, reason, or non-author identity. This contradicts an interpretation of “binds ... to the spot-check's actual verdict span” that verifies provenance rather than merely remembering a historical string. It is distinct from arbitrary wording quality: the named source can be deleted in substance while the purported binding stays green.

## Arithmetic cases and c63 comparison

- **Zero disagreements:** canonical fixture yields `disagreements=0 lesson_gate=1 unresolved=0 met=false`, exit 1. The `>=1` check is effective.
- **Two disagreement lines:** yields `disagreements=2 lesson_gate=1 unresolved=1 met=false`, exit 1. One flag cannot mask two counted lines.
- **Missing Gate:** yields `disagreements=1 lesson_gate=0 unresolved=1 met=false`, exit 1.
- **Negative handling:** the zero-count/true-Gate fixture exercises subtraction `0-1`; `max(...,0)` clamps to zero, but cannot admit because `disagreements>=1` remains false. Count is a sum of booleans over split lines, so negative input is not directly representable.
- **Two copies on one physical line:** yields `disagreements=1 ... met=true`. This is a line-count limitation, **not an independent violation of the explicitly line-based count**; two concatenated Markdown rows are not two valid table rows. Do not overclaim it as two genuine unresolved findings bypassing the numerical guard.
- Prior definition `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_calibration.py:164-166` sets `unresolved = disagreements if not resolved else 0` and `met = bool(resolved)`, ignoring disagreement cardinality once resolved. The c64 direct arithmetic and conjunct at lines 267-270 kill that unlimited numerical masking defect. They do **not** kill the semantic false-positive flag demonstrated above. The c63 comparison here is source analysis, not a claim of an executed c63 differential.

## Evidence and reproduction

LSP first attempted `read xd://lsp`; result: **No such tool: xd://lsp** (not mounted). Semantic references/definition/diagnostics could not be requested. Source reads and literal search were fallback evidence, not semantic-server proof. Only relevant counter definitions, their main caller, Gate text, spot row, and selftest paths were reviewed. No unrelated runtime/rerouting/resume claim is made.

Actual read-only diff command:

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --stat 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb -- .ufo/waves/round-63/c63_calibration.py .ufo/waves/round-64/c64_calibration.py corpus/lessons/round-61-verifier-spotcheck.md corpus/lessons/round-64.md
```

Output:

```text
 .ufo/waves/round-64/c64_calibration.py | 449 +++++++++++++++++++++++++++++++++
 corpus/lessons/round-64.md             | 110 ++++++++
 2 files changed, 559 insertions(+)
```

The following Python driver was executed through Python Eval. It builds deterministic real loose Git objects directly under the assigned scratch, without any mutating git command. These are genuine revision-readable Git fixtures, not monkeypatched counter evaluations. The subprocess executes the frozen source bytes without modifying counter logic. Every Git command uses `-C`; fixture toplevels are asserted before running the counter (no `git commit` is used). `TMPDIR` is passed explicitly to each subprocess; recipe files and all fixture objects stay in the assigned scratch. The preliminary in-memory overlay run produced the same eight outcomes; the stronger subprocess results below are the relied-on evidence. To reproduce, execute the driver with Python from stdin; it removes its own scratch in `finally`.

```python
import hashlib, os, pathlib, shutil, subprocess, sys, zlib
lane = '/home/vgpnk/Projects/shokunin/kake-shokunin'
work = pathlib.Path('/fast/scratch/hyaku/kake-r64/ReviewerC1Unresolved')
revision = '4c8295fa5e3b628f1fdf3840299ae415c01849fb'
rel = '.ufo/waves/round-64/c64_calibration.py'
def show(path):
    return subprocess.check_output(['git', '-C', lane, 'show', revision+':'+path])
source = show(rel)
print('counter_sha256='+hashlib.sha256(source).hexdigest())
ns = {'__name__': 'fixture_source'}
exec(compile(source, rel, 'exec'), ns)
paths = [p for p, _ in ns['PIN_SHAS'].values()]
paths += [ns[k] for k in ('SPOT_REL', 'KNOWLEDGE_REL', 'QUALITY_REL', 'LESSON_REL', 'SOURCES_REL')]
base = {p: show(p) for p in paths}
spotrel, lessonrel = ns['SPOT_REL'], ns['LESSON_REL']
spot = base[spotrel].decode()
row = next(s for s in spot.splitlines() if 'S432' in s and 'Disagree' in s)
plain = '\n'.join(s for s in spot.splitlines() if not ('S432' in s and 'Disagree' in s))+'\n'
marker = ('# lesson\n\n## Gate\n\nS432 / Fetch '+ns['SPOT_VERDICT_SPAN']+'; collapsed-only; c64_calibration.py; author-side.\n')
negated = marker+'\nNo disagreement is resolved; this Gate rejects the claimed resolution.\n'
fixtures = [('baseline', {}), ('zero-disagreements', {spotrel: plain.encode()}),
    ('two-disagreements', {spotrel: (spot+'\n'+row+'\n').encode()}),
    ('no-gate', {lessonrel: b'# no gate\n'}), ('marker-gate', {lessonrel: marker.encode()}),
    ('negated-gate', {lessonrel: negated.encode()}),
    ('two-records-one-line', {spotrel: (plain+row+' '+row+'\n').encode()}),
    ('synthetic-spot', {spotrel: b'S432 Disagree\n'})]
# Construct loose Git objects directly: no git init/add/commit/config or other mutating Git command.
def materialize(repo, files):
    gd = repo/'.git'
    (gd/'objects').mkdir(parents=True)
    (gd/'refs'/'heads').mkdir(parents=True)
    (gd/'HEAD').write_text('ref: refs/heads/main\n')
    def obj(kind, data):
        raw = kind.encode()+b' '+str(len(data)).encode()+b'\0'+data
        oid = hashlib.sha1(raw).hexdigest()
        target = gd/'objects'/oid[:2]/oid[2:]
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(zlib.compress(raw))
        return oid
    root = {}
    for path, data in files.items():
        node = root
        parts = path.split('/')
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = data
    def tree(node):
        entries = []
        for name in sorted(node, key=lambda n: n+'/' if isinstance(node[n], dict) else n):
            value = node[name]
            mode, oid = ('40000', tree(value)) if isinstance(value, dict) else ('100644', obj('blob', value))
            entries.append(mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(oid))
        return obj('tree', b''.join(entries))
    oid = obj('commit', ('tree '+tree(root)+'\nauthor fixture <fixture@example.invalid> 0 +0000\ncommitter fixture <fixture@example.invalid> 0 +0000\n\nfixture\n').encode())
    (gd/'refs'/'heads'/'main').write_text(oid+'\n')
    top = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', '--show-toplevel']).decode().strip()
    assert top == str(repo), (top, repo)
    return oid
work.mkdir(parents=True, exist_ok=True)
try:
    counter = work/'counter.py'
    counter.write_bytes(source)
    env = dict(os.environ, TMPDIR=str(work), PYTHONDONTWRITEBYTECODE='1')
    for name, overlay in fixtures:
        repo = work/name
        oid = materialize(repo, dict(base, **overlay))
        cmd = [sys.executable, '-B', str(counter), '--root', str(repo), '--revision', oid]
        proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
        print('COMMAND '+' '.join(cmd))
        print(name+': exit='+str(proc.returncode)+' '+proc.stdout.strip())
        if proc.stderr:
            print('stderr='+proc.stderr.strip())
finally:
    shutil.rmtree(work)
print('scratch_removed='+str(not work.exists()).lower())

```

Exact canonical subprocess commands/output:

```text
counter_sha256=5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf
COMMAND /usr/bin/python -B /fast/scratch/hyaku/kake-r64/ReviewerC1Unresolved/counter.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Unresolved/baseline --revision eabf5fd0830e86da660335f14ead932cc28947b3
baseline: exit=0 revision=eabf5fd0830e86da660335f14ead932cc28947b3 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
COMMAND /usr/bin/python -B /fast/scratch/hyaku/kake-r64/ReviewerC1Unresolved/counter.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Unresolved/zero-disagreements --revision 056b646522b53f032b519b12c5c2905b7ed264a7
zero-disagreements: exit=1 revision=056b646522b53f032b519b12c5c2905b7ed264a7 disagreements=0 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false
COMMAND /usr/bin/python -B /fast/scratch/hyaku/kake-r64/ReviewerC1Unresolved/counter.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Unresolved/two-disagreements --revision 760e4871261607ee0beb58d759e435a3b83de015
two-disagreements: exit=1 revision=760e4871261607ee0beb58d759e435a3b83de015 disagreements=2 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
COMMAND /usr/bin/python -B /fast/scratch/hyaku/kake-r64/ReviewerC1Unresolved/counter.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Unresolved/no-gate --revision 08f65af5f3fe8a79b1bf199ec2f8df21da5e9aa3
no-gate: exit=1 revision=08f65af5f3fe8a79b1bf199ec2f8df21da5e9aa3 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
COMMAND /usr/bin/python -B /fast/scratch/hyaku/kake-r64/ReviewerC1Unresolved/counter.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Unresolved/marker-gate --revision 4c67c53634ab00376d4f3ab3984a950547bb8d42
marker-gate: exit=0 revision=4c67c53634ab00376d4f3ab3984a950547bb8d42 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
COMMAND /usr/bin/python -B /fast/scratch/hyaku/kake-r64/ReviewerC1Unresolved/counter.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Unresolved/negated-gate --revision fd80c7b66c3f27e01977b386427da59566b104f8
negated-gate: exit=0 revision=fd80c7b66c3f27e01977b386427da59566b104f8 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
COMMAND /usr/bin/python -B /fast/scratch/hyaku/kake-r64/ReviewerC1Unresolved/counter.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Unresolved/two-records-one-line --revision fac3f43a6461d77f4ff9cb087d2014a7c3a634d1
two-records-one-line: exit=0 revision=fac3f43a6461d77f4ff9cb087d2014a7c3a634d1 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
COMMAND /usr/bin/python -B /fast/scratch/hyaku/kake-r64/ReviewerC1Unresolved/counter.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Unresolved/synthetic-spot --revision 07721786a137bbf0f34040f3a078536d9c631143
synthetic-spot: exit=0 revision=07721786a137bbf0f34040f3a078536d9c631143 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
scratch_removed=true

```

## Residual risk, verification gaps, and hygiene

The fixture trees contain only the counter's consumed inputs, not unrelated lane files; the baseline fixture succeeds, and every attack differs from that fixture only in the named blob. Frozen raw/text/ledger/recipe remain byte-identical and re-execute in every case. No counter, contract, receipt, lesson, or lane worktree byte was changed. No mutating Git command, commit, push, tool installation, or runtime other than the assigned Python counter was invoked. Scratch deletion completed (`scratch_removed=true`). Only this assigned report is retained.

Scope does not establish exploitability of raw extraction, ledger pinning, C2/C3, or resume/saturation contracts. The report supports a semantic-closure false admission, not a general assertion that source evidence is fake. A maintainer should decide whether the frozen claim's kill rule treats this marker Gate green as disqualifying; this reviewer does not integrate or judge the wave.

Self-evaluation: accuracy 4/5 (canonical subprocess receipts; c63 comparison source-only); completeness 4/5 (all assigned shapes covered, no broader prose-language proof); clarity 4/5 (source-binding and semantic-closure defects separated); actionability 4/5 (complete deterministic driver; no fix authorized); conciseness 4/5 (full output retained for reproducibility). Overall 4.0/5. Improvements by impact: define what affirmative resolution evidence must prove, and validate the actual spot verdict provenance rather than presence of an unbound literal. User agreement expected on arithmetic outcomes; semantic severity remains a review recommendation.
