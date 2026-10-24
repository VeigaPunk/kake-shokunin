# RederiveV4Receipt — C2(b) after-receipt re-derivation (falsify wave 2)

Seat: `kake-r45.RederiveV4Receipt`. Lane tip at review: `e545525` (+ untracked wave-2 reports,
and one **uncommitted modification to a committed instrument**, F2 below). Scratch:
`/fast/scratch/hyaku/kake-r45/RederiveV4Receipt/`. Tool installs: none.

Audited target: the after receipt
`.ufo/waves/round-45/verification/v6v4/counter-v4.json` (+ `counter-v4.txt`), and the before
receipt `.ufo/waves/round-44/verification/claim/v4-final/v4.json`.

## Verdict on the named attack

**PASS on all six named checks and on `before=true`** — the receipt says exactly what the ticket
asserts, its `counterSha256` is the self-hash of the committed counter, and a same-seed re-run
reproduces every deterministic field. **But the C2(b) repair it evidences is producer-partial:**
the shipped v2 audit driver still stamps the "ten class runs" predicate into v4-mode summaries
(F1), which is the artifact class the before-side evidence came from. The literal after-clause
("the counter v6 … emits a receipt whose predicate names only the eleven v4 runs") holds; the
freshness claim's own defect sentence ("a v4-mode receipt's predicate text names ten class runs")
is still reproducible with shipped instruments.

## 1. Named checks — worked, with decisive output

Command (identity):

```sh
sha256sum .ufo/waves/round-45/c45_count.py scripts/sitemap_audit.py
```
```text
e17b5dc8a6bd710cd5b4c27569c0972730cf0048d8db4842e115945982cf403b  .ufo/waves/round-45/c45_count.py
914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021  scripts/sitemap_audit.py
```

Command (shape/identity re-derivation; loads the counter module and compares its constants,
parses the receipt with a duplicate-key hook):

```sh
python3 -B - <<'PY'  # (executed in the session eval; abbreviated here to the printed facts)
...
PY
```
```text
dup_key_sets: []
predicate == module PREDICATE_V4: True
after predicate: met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's
'class runs' in after predicate: False
'eleven v4 runs' in after predicate: True
classesMode: v4 | classRuns: [] | len: 0
runs keys: ['A', 'B', 'C', 'D', 'E', 'F', 'T1', 'T2', 'T3', 'T4', 'T5']
keys == A-F+T1-T5 exactly: True | nkeys: 11
G-keys present: []
sum(values)= 11878  receipt equalValues= 11878  match: True
all equal & 5/5 reps: True | equalRuns: 11/11 | n runs: 11
median ratios re-derived: [('T1', 1.015745, 1.0157450505173422, True), ('T2', 1.197075, 1.1970754403456298, True), ('T3', 1.318827, 1.3188273641690162, True), ('T4', 1.270495, 1.2704953014723896, True), ('T5', 1.169649, 1.169648814217262, True)]
all ratios <= 2.0: True | ratioLimit: 2.0 | reps: 5
counterSha256 == sha256(c45_count.py): True
toolSha256 == sha256(sitemap_audit.py): True
met: True | note: None | seed: 46477493193740 | revision: None | toolFile: scripts/sitemap_audit.py
BEFORE predicate: met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's
BEFORE 'ten class runs': True | 'class runs': True
BEFORE classesMode: v4 | classKeys: [] | has classRuns field: False
BEFORE rows: 27 | predicate eleven v4 runs: True
```

Exit-code datum (`counter-v4.txt`, verbatim, 2 lines):

```text
{"label": "", "revision": null, "toolSha256": "914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021", "equalRuns": "11/11", "ratios": {"T1": 1.016, "T2": 1.197, "T3": 1.319, "T4": 1.27, "T5": 1.17}, "met": true, "note": null}
V4_EXIT=0
```

- `txt==json on shared keys: True` (all seven keys the counter's `finish()` prints).
- Source semantics bind the code to the datum: `finish(0 if rec["met"] else 1)`
  (`c45_count.py:1120`). `met=true` ⇒ exit 0. Reproduced live below (`RERUN_EXIT=0`).

| check | result |
|---|---|
| predicate names only eleven v4 runs, no "class runs" | **PASS** (byte-equal to module `PREDICATE_V4`) |
| `classesMode == "v4"` | **PASS** |
| `classRuns == []` | **PASS** |
| `runs` keys exactly A–F + T1–T5 (11, no dupes, no G) | **PASS** |
| exit 0 recorded in `counter-v4.txt` | **PASS** (`V4_EXIT=0`; reproduced) |
| `counterSha256 == sha256(c45_count.py)` | **PASS** (`e17b5dc8…`; also reconstructed independently, §2) |
| before receipt predicate names the ten class runs (`before=true`) | **PASS** (§1 output, `before` block) |

## 2. Independent reconstruction and same-seed reproduction

(a) The committed v6 diff applied to the frozen v5 produces the counter byte-for-byte:

```sh
cp .ufo/waves/round-44/c44_count_v5.py /fast/scratch/.../base_v5.py
patch -p0 /fast/scratch/.../patched.py < .ufo/waves/round-45/v6diff/v5-v6.diff
sha256sum patched.py .ufo/waves/round-45/c45_count.py
```
```text
e17b5dc8a6bd710cd5b4c27569c0972730cf0048d8db4842e115945982cf403b  patched.py
e17b5dc8a6bd710cd5b4c27569c0972730cf0048d8db4842e115945982cf403b  .ufo/waves/round-45/c45_count.py
PATCHED==WORKING_BYTE_IDENTICAL
```

(b) Re-run of the committed counter with the receipt's recorded seed, output to scratch:

```sh
python3 -B .ufo/waves/round-45/c45_count.py --root . --tool-file scripts/sitemap_audit.py \
  --classes v4 --seed 46477493193740 --out /fast/scratch/.../rerun-v4.json
```
```text
{"label": "", "revision": null, "toolSha256": "914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021", "equalRuns": "11/11", "ratios": {"T1": 0.986, "T2": 1.147, "T3": 1.299, "T4": 1.229, "T5": 1.128}, "met": true, "note": null}
RERUN_EXIT=0
```

Deterministic comparison against the committed receipt:

```text
top-level deterministic equal: True []
run key order equal: True
per-run deterministic mismatches: NONE (11/11 runs reproduce values+exit+out-sha256+equal)
rerun exit-relevant met: True
```

So the committed receipt is a faithful, reproducible output of the committed counter at the
recorded seed. Timing ratios move with load (all still ≤ 2.0); nothing else changes.

## 3. Findings

### F1 — HIGH: C2(b) repair is producer-partial; the falsified predicate is still emitted by the shipped audit driver

The falsified round-44 receipt (`v4-final/v4.json`) is **not** a counter receipt: its key set is
identical to the audit driver's summary (`key set == current audit-driver summary key set: True`,
`rows: 27`, `classKeys: []`, `classesMode: v4`). The producer stamps the module-level alias:

- `.ufo/waves/round-45/c45_audit.py:409` (HEAD, sha `f3c3171b…`): `"predicate": counter_mod.PREDICATE`
- `.ufo/waves/round-45/c45_count.py:84`: `PREDICATE = PREDICATE_V5  # driver compatibility: audit drivers read the module-level name`

Since v6 deliberately pins `PREDICATE` to the **v5** text, every v4-mode audit summary still
names the ten class runs. Live reproduction with shipped instruments (one frozen control, run in
scratch, `AUDIT_EXIT=0`):

```sh
python3 -B .ufo/waves/round-45/c45_audit.py --root . --controls $S/controls-1.tsv \
  --counter .ufo/waves/round-45/c45_count.py --classes v4 --expect blind --workers 1 \
  --out $S/audit-v4/summary.json
```
```text
classesMode: v4
classKeys: []
counterSha256: e17b5dc8a6bd710cd5b4c27569c0972730cf0048d8db4842e115945982cf403b
predicate: met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's
'class runs' in predicate: True
'ten class runs' in predicate: True
verdict: witnessed 0/1 notMet=0 | ok: True
inner counter receipt predicate: met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs), and its medi
inner classesMode: v4 | inner classRuns: [] | inner equalRuns: 11/11 | inner met: True
```

Consequence: the wave's before/after pair swaps producers (audit summary → counter receipt). The
"class-runs predicate: true → false" transition is demonstrated only for the counter's own
receipt, while the artifact class that supplied the before side still reproduces `true` under the
same `--classes v4` invocation. The frozen counting command cannot see this: `c45_freshness.py:40-45`
reads a single path (`verification/v6v4/counter-v4.json`) and tests only the substring
`"class runs" in predicate`. C2(b) as measured is literally true for its named subject; the
defect sentence it claims to repair is **not** closed across shipped receipt producers.

### F2 — HIGH (evidence integrity): a committed instrument is being modified in the lane during wave 2

My first `git status --porcelain` in this session showed only `?? .ufo/.ufo/`. At report time:

```text
 M .ufo/waves/round-45/c45_audit.py
```

Three distinct identities for the same path, none equal:

| source | sha256 |
|---|---|
| HEAD (`git show HEAD:.ufo/waves/round-45/c45_audit.py`) — the identity quoted in `SCORECARD.md` and in `verification/matrix/after.json` | `f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076` |
| working tree **at the moment of my audit run** (`audit-v4/run-manifest.json` `driver_sha256`) | `5735c3709f4f3b490bb24b2a35908a224cbaa2088278b1206c19eec9cd34b8df` |
| working tree now | `b61447e64730dcdb1449fcb3002d0bc09e7ceb4d8be2c249c7f1604358416660` |

The edit at report time touches only `selftest()`/fake-counter branches (`hunks @@ -170, +171;
-262, +265; -306, +315`), so HEAD's production stamping (line 409) is unchanged and my
reproduction above is valid for the committed driver. But the tree moved **while I was running
it**, wave-2 rules say mutation tests run on scratch copies, and the matrix's driver identity
(`f3c3171b…`) no longer describes the working tree. Any receipt produced now would name bytes no
committed receipt names. I did not edit or restore this file.

### F3 — MEDIUM (freshness of evidence): wave-1 runtime evidence names a counter identity that exists nowhere

Five wave-1 reports quote `ce8bf2353d4f008a987f6fb3b6d3677d2dbed98aaae274126c68f0a3cf622556`
as the v6 counter — including verbatim `sha256sum` output (`w1/CriticV6Minimal.md:79`,
`w1/ScoutCounterV4Map.md:87,134`, `w1/ScribeDeclarations.md:302`, `w1/MutCounterV6Spec.md:223`,
`drafts/scorecard-measurement.md:144`). Evidence:

```text
# every committed/reachable blob of the path
240a816 e17b5dc8a6bd710cd5b4c27569c0972730cf0048d8db4842e115945982cf403b  -
4c53844 e17b5dc8a6bd710cd5b4c27569c0972730cf0048d8db4842e115945982cf403b  -
eb23fd3 e17b5dc8a6bd710cd5b4c27569c0972730cf0048d8db4842e115945982cf403b  -

# tree-wide scan (1079 files hashed): no file matches ce8bf235
--- any file with ce8bf235 ---
(empty)
```

The committed diff reconstructs `e17b5dc8…` exactly (§2a), so `ce8bf235…` is not derivable from
committed inputs. The wave-1 "no-extra-hunks PASS" and "the v4 receipt is clean … the fix works at
runtime" verdicts were therefore rendered on bytes that are not the shipped counter. The
**committed** after receipt is unaffected — its `counterSha256` is the self-hash of the committed
bytes and reproduces — but the review evidence behind the claim is stale/unbound.

### F4 — LOW: the frozen counting command does not bind the receipt it counts

`c45_freshness.py:40-45` returns `"class runs" in json.loads(path)["predicate"]`. It never checks
`classesMode`, `classRuns`, the run-key set, or `counterSha256`, and it reads only the counter
receipt path. A hand-edited or foreign JSON at that path satisfies `after=false`; the stronger
properties verified in §1 are not gate-enforced. This is a gate-strength gap, not a defect of the
receipt itself.

### F5 — INFO: the `V4_EXIT=0` line has no committed recorder

Repo-wide `grep -rn 'V4_EXIT'` returns only the txt itself (`verification/v6v4/counter-v4.txt:2`);
no committed script appends it. The datum is nonetheless *true*: my independent re-run reproduced
exit 0 with `met=true`, and the counter's `finish()` makes 0 ⇔ met (§1).

## 4. Residual risk / unrun

- **Unrun:** the full 27-control v4 audit (F1 is demonstrated on one frozen control; the driver's
  stamping is control-independent — `"predicate": counter_mod.PREDICATE` is outside the per-row
  loop — but a 27-row run was not executed; est. ~12 min).
- **Unrun:** `c45_freshness.py` end-to-end (its v4 leg's source is quoted at F4; the selftest legs
  are other seats' scope).
- **Not re-verified here:** v5-mode receipt shape and class-run coverage; the frozen v4+class-run
  clause is by construction uncertifiable from a v4-mode receipt (11 runs only) — a scope call for
  the operator / the scope seats, recorded here as residual risk.
- The audit driver in the lane is a moving target (F2); any further reading of
  `c45_audit.py` should pin `git show HEAD:…` or a scratch copy.

## 5. Files written

- `.ufo/waves/round-45/w2/RederiveV4Receipt.md` (this report — the only lane write)
- Scratch only: `/fast/scratch/hyaku/kake-r45/RederiveV4Receipt/{base_v5.py,patched.py,v5-v6.diff,controls-1.tsv,rerun-v4.json,audit-v4/…}`

No lane file other than this report was created, edited, or restored. No commits, no pushes.
