# AttackV2Scope — C1 kill rule 3 (read containment, no circular reads), round 45 wave 2

Seat: `kake-r45.AttackV2Scope` (critic, operability). Target: frozen C1 kill rule 3 —
"v2 reads no control file beyond v1's reads (no circular reads)" (`SCORECARD.md`,
Round 45 C1 kill rules). Attack: compare the file reads of `.ufo/waves/round-44/c44_audit.py`
(v1) and `.ufo/waves/round-45/c45_audit.py` (v2) by static extraction **and** by kernel-level
`strace` of both drivers over identical inputs; verify no network. Read-only over the lane;
scratch `/fast/scratch/hyaku/kake-r45/AttackV2Scope/`. No tool installs (`strace` was already
present at `/usr/bin/strace`). No subagents.

## Verdict on the named attack

**PASS as written — with a HIGH-severity evidence caveat.** Over the committed 27-control
cohort, v2 opens **no input/control file that v1 does not open**: the 27 control scripts, the
controls TSV, the counter source, and the per-control receipts are read with identical
syscall pairs (`openat`/`newfstatat`) by both drivers, and neither makes any network syscall.
The only v2-only content open is **its own source** (`sha256_file(__file__)` for the run
manifest); the only other v2-only filesystem observations are a directory `openat` (for
`os.listdir(outdir)`), 27 `newfstatat` mtime reads of receipts v1 already reads, and one
`openat(..., O_WRONLY|O_CREAT|O_EXCL)` **write** of `run-manifest.json`. None is a control
file, so the rule's literal scope is not violated. Caveat F1: the driver bytes are
worktree-modified and changed at least four times during this review, so "v2" must always be
pinned to a sha — the sha named in `SCORECARD.md` and `after.json` (`f3c3171b…`) is the HEAD
blob, not the file now in the tree (`d3076be6…`).

## Method and exact commands

Scratch cohort (synthetic, one control), then the committed cohort (27 controls), then the
three invalid fixtures, each run identically under both drivers with the same `--root`,
`--controls`, `--counter`, `--classes`, `--expect`, and `--out` path (cleaned between runs).
A stub counter (in scratch) reports its own sha256/seed so both drivers see a
valid-shaped receipt; `CLASS_MODULES = []`, `PREDICATE` set. Traces use
`strace -f -qq -s 8192 -e trace=%file,network` so child counters are included.

```
S=/fast/scratch/hyaku/kake-r45/AttackV2Scope
L=/home/vgpnk/Projects/shokunin/kake-shokunin
# declared bytes, pinned from HEAD (NOT the worktree)
git -C "$L" show HEAD:.ufo/waves/round-45/c45_audit.py > $S/snap-f3c.py
# worktree bytes at trace time, pinned so later edits cannot move them
cp "$L/.ufo/waves/round-45/c45_audit.py" $S/snap-c45_audit.py

for D in "$L/.ufo/waves/round-44/c44_audit.py" $S/snap-f3c.py $S/snap-c45_audit.py; do
  rm -rf $S/realout
  strace -f -qq -s 4096 -e trace=%file,network -o $S/trace.log \
    python3 -B "$D" --root "$L" \
      --controls "$L/.ufo/waves/round-44/controls-27.tsv" \
      --counter "$S/counter.py" --classes v4 --expect blind \
      --out "$S/realout/summary.json" --label real27
done

# fixture legs, both drivers, same fixture bytes
for fx in counter-error stale-backdate; do for d in v1 v2; do
  rm -rf $S/fx-$fx-$d-out
  strace -f -qq -s 4096 -e trace=%file -o $S/fx-$fx-$d.log \
    python3 -B "$D" --root "$L" \
      --controls "$L/.ufo/waves/round-45/fixtures/$fx/controls.tsv" \
      --counter  "$L/.ufo/waves/round-45/fixtures/$fx/fake_counter.py" \
      --classes v5 --expect blind --out "$S/fx-$fx-$d-out/summary.json"
done; done
```

Read sets were normalized (outdir → `$OUT`, driver path → `$DRIVER`, interpreter/stdlib
paths filtered) and diffed as `(event, path)` sets; multiplicity was checked separately
because set-diff dedupes.

## Read-set results

Both drivers green on the same 27 committed controls, same inputs, exit 0:

```
$ python3 -B <driver> --root LANE --controls .ufo/waves/round-44/controls-27.tsv \
    --counter scratch/counter.py --classes v4 --expect blind --out .../summary.json
v1  (8ee2c8bf): AUDIT real27 classes=v4 classKeys=- witnessed=0/27 ... ok=True counter=31a266abd22c
v2 declared (f3c3171b): AUDIT head   classes=v4 classKeys=- witnessed=0/27 ... ok=True counter=31a266abd22c
v2 worktree (6abab9ea): AUDIT cur    classes=v4 classKeys=- witnessed=0/27 ... ok=True counter=31a266abd22c
```
(`witnessed=0` is by construction: `--classes v4` has no class keys and the stub counter
reports `met=True`; this run measures the *read set*, not the witness gate.)

Normalized three-way diff on the committed cohort:

```
v1                    events=108  network=0
v2 declared f3c3171b  events=128  network=0
v2 worktree 6abab9ea  events=128  network=0
control-script read pairs identical v1==declared: True  v1==worktree: True  (pairs per driver: 54)
controls-27.tsv read by both: True
```

| input | v1 `c44_audit.py` | v2 `c45_audit.py` |
|---|---|---|
| `controls-27.tsv` | `openat O_RDONLY` | identical |
| 27 control scripts | 27 × (`newfstatat` exists + `openat` sha256) | identical (54 pairs, set-equal) |
| counter source | `openat` (sha256 + `exec_module`) | identical |
| 27 per-control receipts | `openat` (`json.load`) | identical, **plus** `newfstatat` (mtime window) |
| driver's own source | interpreter open only (2 `openat`) | **+1** `openat` (`sha256_file(__file__)`; 3 total) |
| output directory | none | **`openat` dir** (`os.listdir`, empty-dir precondition) |
| `run-manifest.json` | none | **write** `O_WRONLY\|O_CREAT\|O_EXCL` (not a read) |
| network | 0 syscalls | 0 syscalls |

Verbatim decisive trace lines:

```
# v2-only directory open (os.listdir), absent from v1:
2070448 openat(AT_FDCWD, "/fast/scratch/hyaku/kake-r45/AttackV2Scope/realout3", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = 3
# v1 same call: 0

# v2 self-source opens (3; v1 has 2 — the extra one is sha256_file(__file__)):
openat(AT_FDCWD, ".../snap-f3c.py", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, ".../snap-f3c.py", O_RDONLY) = 3          <-- extra self-read
openat(AT_FDCWD, ".../snap-f3c.py", O_RDONLY|O_CLOEXEC) = 3
# v1: 2 self opens, no sha256 open

# v2 receipt mtime stat (27 occurrences), v1: 0:
newfstatat(AT_FDCWD, ".../realout3/tools/buildscheme-M5.json", {st_mode=S_IFREG|0644, ...}, 0) = 0

# manifest is a write, not a read:
openat(AT_FDCWD, ".../realout3/run-manifest.json", O_WRONLY|O_CREAT|O_EXCL|O_CLOEXEC, 0666) = 3
```

Fixture legs, identical fixture bytes under both drivers — v1 accepts, v2 refuses, read sets
are **set-identical** on fixture paths:

```
AUDIT kake-r44 ... witnessed=1/1 notMet=1 ... ok=False  counter=15363b71eaa0   (counter-error, v1)
AUDIT kake-r45 ... witnessed=0/0 notMet=0 ... ok=False  counter=15363b71eaa0   (counter-error, v2)
AUDIT kake-r44 ... witnessed=1/1 notMet=1 ... ok=False  counter=77aa39c7eefa   (stale-backdate, v1)
AUDIT kake-r45 ... witnessed=0/0 notMet=0 ... ok=False  counter=77aa39c7eefa   (stale-backdate, v2)
```
Both drivers read `fixtures/<fx>/{controls.tsv,ctl1.py,fake_counter.py}` and the same
`__pycache__/fake_counter.cpython-314.pyc`; `counter-error/fake_counter.py` additionally
reads the committed `fixtures/counter-error/control-receipt.json` **under both drivers**
(same bytes), so that is a shared provenance path, not a v2-only read.

## Findings by severity

### F1 — HIGH (evidence integrity): the driver under test is worktree-modified and changed four times during this review

```
$ git status --porcelain -- .ufo/waves/round-45
 M .ufo/waves/round-45/c45_audit.py
$ git log -1 --format='%H %ci %s'
e54552553eaff4d7033dc2df299300fc056f4a0d 2026-10-24 00:56:44 -0300 round-45: wave-2 registry

$ git cat-file -p HEAD:.ufo/waves/round-45/c45_audit.py | sha256sum
f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076  -        (20320 bytes)
worktree observed during this seat, in order:
2eeecacd853236a5e24a330fe8d0cb9a959261f4e582947f9885fac044a7f9fc   (21904 bytes)
b11ccad673f96066ff29b1b03a5c80bcf0082423f1848c30b619dade68da2534
6abab9ea6791fcbfa3c96d058edde18e5f6a804a3b4e0787b41da450855401e9   (22629 bytes; traced)
d3076be631a30ba3470000486ab20a0962eddda9f692cbc8b085ceef2fe972f9   (22788 bytes; final observation)

$ python3 -c "...after.json..."
after.json driver_sha256: f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076
live tree sha256       : d3076be6...  (22788 bytes)
```

`verification/matrix/after.json` still names `f3c3171b…` (the HEAD blob) while the tree holds
an uncommitted variant. Consequences: (a) the measured after-receipt no longer identifies the
file in the tree; (b) any wave-2 re-run of the frozen counting command emits a different
`driver_sha256` than the frozen receipt; (c) any read-set or verdict statement is only
meaningful pinned to a sha. The one diff captured mid-review (at `b11ccad6`, 43 insertions /
2 deletions) is a gate repair — `toolSha256` binding inside `receipt_validity`, a `bad-build`
selftest leg, and an `if not __debug__` selftest guard — and adds **no file read and no
network call** (the traced successor `6abab9ea` has a read set identical to the declared
bytes). But the edit is uncommitted, unmeasured by any receipt, and its final form
(`d3076be6`) was never traced. This seat does not judge whether the edit is authorized; it
records that the artifact moved under measurement.

### F2 — MEDIUM (operability): kill rule 3 is not enforced or measured by the counting command

`python3 -B .ufo/waves/round-45/c45_matrix.py --stage after` never observes reads: there is no
`strace`, audit hook, open allowlist, or read counter anywhere in `c45_matrix.py` or
`c45_audit.py`. The after pass condition is only
`invalid_accepted == 0 and len(named) == 3 and honest_witnessed == 27 and honest_build_met == 3`.
So the rule's truth rests entirely on out-of-band tracing (this report). The *substance* holds
for the configurations traced (synthetic cohort, committed 27-control cohort, two fixtures ×
two drivers), but the frozen command would not detect a future regression that added an
external read — exactly the class of prose-only kill rules already reported for rules 2/4/5 in
`w1/ReviewKillRules.md` (S1-1).

### F3 — MEDIUM (dead provenance): v2's added self-read and manifest are consumed by nothing

The only v2-only content open is `sha256_file(os.path.abspath(__file__))` (3 self opens vs
v1's 2). Its value is written to `run-manifest.json` together with a `secrets.token_hex(16)`
nonce. `grep -nE 'manifest|nonce|driver_sha256|driverSha' .ufo/waves/round-45/c45_matrix.py`
returns a single line, `163: "driver_sha256": sha256(driver), …` — the matrix *writes* that
field into its own receipt but never reads or validates the driver's run manifest, and
`run_honest_leg` validates only `counterSha256`, `controls==27`, `ok`, `witnessed`, `build`,
`errors`. Therefore the new read and the nonce buy **zero verdict weight**; citing the
manifest as run-provenance evidence for the honest leg is unearned. (This is a weaker sibling
of the already-falsified causal clause: neither `toolSha256` nor `driver_sha256` is checked by
the pass condition.)

### F4 — LOW (behavior divergence): v2 adds a non-empty-output-dir hard failure

`c45_audit.py` does `os.makedirs(outdir, exist_ok=True)` then
`if os.listdir(outdir): ap.error("output directory must be empty: %s" % outdir)`; v1 has no
such precondition and is idempotent into a dirty directory. The frozen command masks this
because `run_fixture_leg`/`run_honest_leg` create fresh `uuid4()[:12]` cohort directories, so
`c45_matrix.py` is re-runnable. But any direct re-run of a driver invocation into an existing
cohort path fails, and the check is a directory enumeration (names only), not a control read.
Not a rule-3 violation; recorded because it is the only *functional* divergence found in the
v2-only filesystem observations.

### F5 — INFO (rule scope): the frozen command has no same-input comparator for the stale leg

The before stage runs `stale-planted` (SIGKILL, pre-planted receipts); the after stage runs
`stale-backdate`. v1 is never run over `stale-backdate` inside the frozen command, so "v2
reads no control file beyond v1's" has no defined comparator for the after stage's stale leg.
This seat completed the comparison out-of-band: on `stale-backdate` v1 and v2 read identical
fixture paths (v1 certifies 1/1, v2 refuses 0/0 — the claimed behavior). Residual note:
`counter-error/fake_counter.py` ingests committed `control-receipt.json` bytes under both
drivers, so the invalid fixture is a replayed committed receipt (consistent with kill rule 5's
"real receipt shape" requirement, which is another seat's scope).

## Residual risk / unrun checks

- **The full counting command was not traced.** `c45_matrix.py --stage after` writes inside the
  lane (`verification/matrix/...`, `verification/honest-regression/`), which this seat's
  read-only bounds forbid; I traced the driver plus its fixture inputs individually instead.
  Unmeasured: the matrix's own reads (`shutil.copytree` of fixture `tools/`, `load_summary`,
  the `HONEST_DIR` copy), and the `--build-rev 020bc457` build leg's git-object reads (which
  both drivers delegate to the same counter, so no driver asymmetry is expected).
- Set-diff dedupes multiplicity; I checked openat counts separately only for the driver's own
  source (3 vs 2) and the counter (83 vs 83).
- The `__pycache__/fake_counter.cpython-314.pyc` open appears under both drivers; whether that
  pyc is stale relative to the fixture source was not tested (out of scope).
- The final worktree bytes (`d3076be6…`) were not traced; only `f3c3171b…` (declared) and
  `6abab9ea…` (traced snapshot) were. Their read sets are identical, but this is not proof for
  later edits.

## Files written

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/w2/AttackV2Scope.md` (this report)
- Scratch only: `/fast/scratch/hyaku/kake-r45/AttackV2Scope/{counter.py,controls.tsv,root/ctl.py,run-*.out,run-*.err,real-*.out,real-*.err,fx-*.out,fx-*.log,real-trace-*.log,real-trace-v2cur.log,real-trace-v2head.log,trace-*.log,snap-f3c.py,snap-c45_audit.py,realout*/**,fx-*-out/**}`

Report: .ufo/waves/round-45/w2/AttackV2Scope.md

## Addendum (appended after first write; the lane kept moving)

Re-checked immediately after writing this report. The driver moved again and the mutation is
broader than c45_audit.py:

```
$ sha256sum .ufo/waves/round-45/c45_audit.py .ufo/waves/round-45/c45_matrix.py
64bc33248c9ba2088f5447d7c3064cb2aea3f2dce9e2ba4ec4dd514a6a07841e  c45_audit.py   (5th distinct sha observed)
2e8d9af9476736d2baaa994036c4479d87e454716621298e0ea760eef576fb6f  c45_matrix.py  (now worktree-modified)
$ git status --porcelain -- .ufo/waves/round-45 | grep '^ M'
 M .ufo/waves/round-45/c45_audit.py
 M .ufo/waves/round-45/c45_freshness.py
 M .ufo/waves/round-45/c45_matrix.py
 M .ufo/waves/round-45/fixtures/counter-error/README.md
 M .ufo/waves/round-45/fixtures/counter-error/control-receipt.json
 M .ufo/waves/round-45/mutants/m1_v2.py … m4_v2.py
 M .ufo/waves/round-45/verification/freshness/freshness.json
 M .ufo/waves/round-45/verification/matrix/run-log.txt
$ python3 -c "...after.json..."
after.json driver_sha256: f3c3171b...  ran_at_ns 1792813796057423544   (unchanged)
$ grep -nE 'manifest|nonce|driver_sha256' c45_matrix.py
164:        "driver_sha256": sha256(driver), "ran_at_ns": time.time_ns(),
```

Effect on this report: F1 widens from one file to the **round-45 measured artifact set** —
five distinct driver shas (`f3c3171b` → `2eeecacd` → `b11ccad6` → `6abab9ea` → `64bc3324`)
plus a modified matrix, freshness runner, fixtures, mutants, and two committed receipts, while
`after.json`/`freshness.json` still cite the frozen shas. The read-set verdict above remains
pinned exactly to `f3c3171b…` (declared HEAD, 20320 B) and `6abab9ea…` (worktree snapshot,
22629 B): both are set-identical to v1 on control reads with zero network. No claim is made
for `64bc3324…`, and none can be until the tree stops moving and the bytes are re-frozen.
F3 is unchanged: the matrix still only *writes* `driver_sha256` and never reads the driver
run-manifest or its nonce.
