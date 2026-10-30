# ReviewerC1Located — located-range attack

## Verdict

Recommendation: no C1 kill-rule reproduction in this scope. One low-severity boundary/terminology weakness exists in the helper, but the frozen raw/recipe/ledger pins prevent it from admitting a changed tree. This is a review recommendation, not an admission or saturation claim.

Axes: located-range correctness; evidence binding; fail-closed behavior; reproducibility. Only this seat's C1 located-range surface was attacked.

## Findings by severity

### Low — `LOCATED_SPAN_MAX = 15` permits 16 inclusive raw lines; the window bounds starts, not ends

Evidence: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:96-97,163-182`. The inner range includes `b = a + 15`, while the slice `raw_lines[a - 1:b]` contains `b - a + 1` lines. A concrete 16-line quote fixture returns `6150-6165`. Starting the same fixture at 6200 returns `6200-6215`, although the nominal window is 6100–6200. Likewise a quote solely on line 6201 can be found as `6200-6201` by including the preceding blank line.

This is a limitation/ambiguity of the helper's advertised bounded search, not a demonstrated false green: the frozen retained source derives five lines, `6150-6154`; any changed source fails its SHA pin before this helper runs. If “span” intentionally means endpoint distance, 15 is internally consistent; it is not a 15-line inclusive cap. No contract requirement explicitly insists both endpoints remain inside the window.

## Checks and invariant analysis

- Actual addition inspected with `git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb -- .ufo/waves/round-64/c64_calibration.py`: 449 inserted lines, new counter.
- Committed T0 counter bytes independently hash to the frozen `5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf`.
- One-based indexing is correct: `a - 1:b` includes numbered lines a through b. The actual quote begins at retained raw line 6150 and finishes at 6154 (`.../.ufo/waves/round-61/sources/S432.html:6150-6154`). An exhaustive bounded enumeration without the implementation's early break found `(inclusive_line_count, a, b) = (5, 6150, 6154)`.
- First-hit `b` per fixed `a` is sufficient for minimal span, regardless of the docstring's monotonicity assertion: no later end can be shorter for that same start. The outer comparison chooses the shortest across starts; equal-size ties retain the earliest start. A synthetic earlier 16-line occurrence and later one-line occurrence selected the latter, `6150-6150`.
- Ledger equality is required against BOTH values: lines 240–243 reject if `located != EXPECTED_LOCATED OR ledger_row.get('locatedRawLines') != located`, clearing `class_match`. The conjunction in lines 268–270 requires `class_match`. `EXPECTED_LOCATED` alone does not constrain a ledger field. Under the existing whole-ledger SHA pin, field equality is defense-in-depth/redundant for these exact bytes; it remains an explicitly enforced independent relationship.
- Changed raw bytes cannot evaluate located: `pins` at lines 206–208 covers every blob; `parse_ledger(... if pins else None)` at line 220 and the `if pins` at line 221 prevent recipe execution and located derivation. The drift fixture additionally replaced `derive_located` with a function that raises if called: evaluation still completed, exit 1, `located=unevaluable`. Canonical met logic is lines 267–278, not a separately reconstructed predicate.
- Literal caller search found the production call at line 240 and selftest call at line 413. No semantic LSP proof is claimed: `read xd://lsp` returned `No such tool`; the LSP device was unavailable, so references/definition/diagnostics could not be requested. Text search was the explicit fallback.

## Exact attack driver and observed output

Executed in the Python eval tool, with no Git mutation, fixture commits, or lane changes. All imports of reviewed modules were from `git show` bytes, not worktree modules. The concrete synthetic fixtures were in-memory raw-line arrays. `git_show` substitution in the raw-drift test is an isolated evaluator-input injection, not a committed adversarial tree.

```python
import os, subprocess, hashlib, types, tempfile, shutil
lane='/home/vgpnk/Projects/shokunin/kake-shokunin'
rev='4c8295fa5e3b628f1fdf3840299ae415c01849fb'
scratch='/fast/scratch/hyaku/kake-r64/ReviewerC1Located'
os.makedirs(scratch,exist_ok=True)
def blob(rel):
 return subprocess.check_output(['git','-C',lane,'show',f'{rev}:{rel}'])
c=types.ModuleType('counter'); cb=blob('.ufo/waves/round-64/c64_calibration.py'); exec(compile(cb,'c64_calibration.py','exec'),c.__dict__)
r=types.ModuleType('recipe'); exec(compile(blob(c.RECIPE_REL),'extract_text.py','exec'),r.__dict__)
print('counter_sha='+hashlib.sha256(cb).hexdigest())
try:
 tempfile.tempdir=scratch
 raw=blob(c.RAW_REL); lines=raw.decode().split('\n')
 print('pinned_raw_derived='+c.derive_located(r.extract,lines))
 hits=[]
 for a in range(6100,6201):
  for b in range(a,min(a+15,len(lines))+1):
   if c.FROZEN_QUOTE in r.extract('\n'.join(lines[a-1:b]).encode()): hits.append((b-a+1,a,b))
 print('exhaustive_best='+str(min(hits)))
 def fixture(parts,start=6150):
  out=['']*6250; out[start-1:start-1+len(parts)]=parts; return out
 words=c.FROZEN_QUOTE.split(' ')
 sixteen=words[:15]+[' '.join(words[15:])]
 print('sixteen_line_fixture='+c.derive_located(r.extract,fixture(sixteen)))
 for start in [6099,6100,6200,6201]:
  print(f'single_line_start_{start}='+c.derive_located(r.extract,fixture([c.FROZEN_QUOTE],start)))
 print('end_outside_window='+c.derive_located(r.extract,fixture(sixteen,6200)))
 competing=fixture(sixteen,6110); competing[6149]=c.FROZEN_QUOTE
 print('global_min_fixture='+c.derive_located(r.extract,competing))
 print('baseline='+str(c.evaluate(lane,rev)))
 original_show=c.git_show
 c.git_show=lambda root,revision,rel: raw+b'\n' if rel==c.RAW_REL else original_show(root,revision,rel)
 c.derive_located=lambda *args: (_ for _ in ()).throw(AssertionError('must not derive after raw pin drift'))
 print('raw_drift_fixture='+str(c.evaluate(lane,rev)))
finally:
 shutil.rmtree(scratch)
 print('scratch_removed='+str(not os.path.exists(scratch)))
```

```text
counter_sha=5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf
pinned_raw_derived=6150-6154
exhaustive_best=(5, 6150, 6154)
sixteen_line_fixture=6150-6165
single_line_start_6099=unevaluable
single_line_start_6100=6100-6100
single_line_start_6200=6200-6200
single_line_start_6201=6200-6201
end_outside_window=6200-6215
global_min_fixture=6150-6150
baseline=(0, 'revision=4c8295fa5e3b628f1fdf3840299ae415c01849fb disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true')
raw_drift_fixture=(1, 'revision=4c8295fa5e3b628f1fdf3840299ae415c01849fb disagreements=1 pins=0 pin_drift=drift:raw recipe_rederive=0 ledger_state=ledger_absent derived=unevaluable class_match=0 located=unevaluable quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false')
scratch_removed=True
```

## Residual risk and verification gaps

No full-source global minimality claim: the counter explicitly searches a bounded start window and bounded endpoint distance. No SHA-collision attack attempted. The source/recipe pin makes synthetic helper limitations unreachable by ordinary revision-byte substitution. No committed malicious fixture was created (leaf forbids Git mutation); the raw-drift test is evaluator-input instrumentation as disclosed above. C2, C3, orchestration identity, saturation, and resume continuity were not this assignment's affected behavior and were not reviewed.

No tools installed or upgraded. Scratch was removed in `finally`; the report is the only persistent write. Frozen contract, counters, sources, receipts, lesson, and worktree were not changed.

Self-evaluation: accuracy 4/5 (input-injection fixture is not a committed tree); completeness 4/5 (no LSP service available); clarity 4/5 (long executable evidence retained for reproduction); actionability 4/5 (boundary issue is low severity and requires intended terminology to resolve); conciseness 4/5 (full driver intentionally included). Overall 4.0/5. Improvements: obtain semantic caller checks if an LSP device is made available; use an orchestrator-authorized committed fixture if stronger tree-level attack evidence is required. The user should agree that these are disclosed evidence limitations, not false-green findings.
