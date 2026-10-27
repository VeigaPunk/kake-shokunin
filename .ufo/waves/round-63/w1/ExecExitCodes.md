# Seat ExecExitCodes — round-63 exit-code contract verification (C1 + C2 counters)

**Lane role:** leaf executor. No subagent dispatch beyond the single labrat
permitted by the seat spec (none needed — every check below is a direct
measurement). No commits, no push, no mutating git/jj anywhere.

**Fleet root:** `/home/vgpnk/Projects/shokunin/kake-shokunin`
**Measured commit:** `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`
**Base (round-62 tip):** `13d4519818db28cd0aa912e49020659140d7b9fa`

**Item:** verify the exit-code contract — both counters with a bogus
`--revision` (expect 2), with `--help` (expect 0), `c63_calibration.py` on the
real tree at the measured commit (expect 0), and both counters run from a
non-repo cwd with `--root` pointing at the lane (expect normal behavior).

**Headline:** 3 of the 4 sub-checks pass exactly as specified. The
**bogus-`--revision` check fails for C2** (`c63_quote_tool.py`): the documented
exit 2 (`could-not-evaluate`) is only reachable for a *non-hex* bogus
revision. A bogus revision shaped like a full 40-hex SHA — the shape a real
typo takes — makes the counter print `present=0 selftest=unevaluable
met=false` and exit **1** instead of 2. Root cause: the counter's existence
probe uses `git rev-parse --verify <rev>`, which **does not check object
existence** for a full-length 40-hex. Details and the one-line fix in §3.

The four committed after/base receipts reproduce **byte-for-byte** (§6), so
this is a counter robustness/exit-code-semantics defect, **not** a falsified
receipt. C2's kill rule ("if the after receipt does not print `met=true`, or a
stub tool passes, C2 is `unprovable`") is **not** triggered: the after receipt
does print `met=true`, and the defect direction is a *false negative* (an
unreadable revision is reported as "tool absent"), never a false green.

---

## 1. Environment and frozen-artifact verification

```
$ git --version
git version 2.56.0
$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse HEAD
15eb965c1d0f23ce2a522c651e9306a0952da7d3
```

`sha256sum` over the frozen artifacts (cwd = fleet root) — all four match the
contract's frozen values at
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/contract.md`
lines 22–23, 26–27, 55–56, 64–65:

```
$ sha256sum .ufo/waves/round-63/c63_calibration.py .ufo/waves/round-63/c63_quote_tool.py \
    scripts/quote_class.py .ufo/waves/round-63/quote-class/quote-classes.json
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  .ufo/waves/round-63/c63_calibration.py
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  .ufo/waves/round-63/c63_quote_tool.py
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  .ufo/waves/round-63/quote-class/quote-classes.json
```

Re-verified after all runs below — unchanged. No tool was installed for this
seat (stock `git 2.56.0` + `python3 3.14.8` sufficed).

Lane abbreviations used throughout:
`LANE=/home/vgpnk/Projects/shokunin/kake-shokunin`,
`C1=$LANE/.ufo/waves/round-63/c63_calibration.py`,
`C2=$LANE/.ufo/waves/round-63/c63_quote_tool.py`.

---

## 2. Sub-checks that PASS

### 2.1 `--help` → exit 0, both counters ✅

```
$ python3 -B $LANE/.ufo/waves/round-63/c63_calibration.py --help
usage: c63_calibration.py [-h] [--root ROOT] [--revision REVISION]
... (docstring) ...
options:
  -h, --help           show this help message and exit
  --root ROOT
  --revision REVISION
exit=0

$ python3 -B $LANE/.ufo/waves/round-63/c63_quote_tool.py --help
usage: c63_quote_tool.py [-h] [--root ROOT] [--revision REVISION]
... (docstring) ...
options:
  -h, --help           show this help message and exit
  --root ROOT
  --revision REVISION
exit=0
```

`--help` writes to **stdout** (not stderr) and short-circuits argparse before
any git work, so it exits 0 even with a deliberately broken `--root`/`--revision`:

```
$ python3 -B $C1 --root /nonexistent --revision bogus --help >/dev/null 2>&1; echo "c1_help_exit=$?"
c1_help_exit=0
$ python3 -B $C2 --root /nonexistent --revision bogus --help >/dev/null 2>&1; echo "c2_help_exit=$?"
c2_help_exit=0
```

### 2.2 `c63_calibration.py` on the real tree at the measured commit → exit 0 ✅

```
$ python3 -B $C1 --root $LANE --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

(C2 at the same commit, for completeness: `present=1 selftest=4/4
frozen_cases=ok met=true`, exit 0.)

### 2.3 Non-repo cwd with `--root` pointing at the lane → normal behavior ✅

Run from `/fast/scratch/hyaku/kake-r63/ExecExitCodes`, which is **not** a git
repository (`git rev-parse --show-toplevel` → `fatal: not a git repository`,
exit 128), with `--root` as an **absolute** path to the lane:

```
$ pwd
/fast/scratch/hyaku/kake-r63/ExecExitCodes
$ git rev-parse --show-toplevel
fatal: not a git repository (or any parent up to mount point /)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).
exit=128
$ python3 -B $C1 --root $LANE --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
$ python3 -B $C2 --root $LANE --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

Same result with a **`--root` relative to the non-repo cwd** (5 levels up):

```
$ python3 -B $C1 --root ../../../../../home/vgpnk/Projects/shokunin/kake-shokunin --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
$ python3 -B $C2 --root ../../../../../home/vgpnk/Projects/shokunin/kake-shokunin --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

Both counters are correctly **cwd-independent** — they address the tree only
through `git -C root` and through the `cwd=root` they pass to the tool
subprocess (`c63_quote_tool.py:66`), never through `Path.cwd()` of the
caller. C2's cwd-independence is load-bearing here because the frozen tool
`scripts/quote_class.py:24` binds `LANE_ROOT = Path.cwd()`; the counter's
`cwd=root` override is what makes the selftest resolve the lane's fixtures
rather than the caller's cwd.

### 2.4 Bogus `--revision` in **non-hex** form → exit 2, both counters ✅

```
$ python3 -B $C1 --root $LANE --revision nosuchbranch-xyz
could-not-evaluate: revision nosuchbranch-xyz unreadable
exit=2
$ python3 -B $C2 --root $LANE --revision nosuchbranch-xyz
could-not-evaluate: revision nosuchbranch-xyz unreadable
exit=2
```

Both write the diagnostic to **stderr** and leave stdout empty, so the
"could-not-evaluate" signal is machine-distinguishable from the
"evaluated, not met" signal (which goes to stdout).

---

## 3. FINDING — bogus `--revision` in full-40-hex form: C2 exits 1, not 2 ❌

### 3.1 The observation

A bogus revision shaped like a full 40-hex SHA takes a **different** path in
each counter:

```
$ python3 -B $C1 --root $LANE --revision deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
could-not-evaluate: verifier spot-check absent
exit=2

$ python3 -B $C2 --root $LANE --revision deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
revision=deadbeefdeadbeefdeadbeefdeadbeefdeadbeef present=0 selftest=unevaluable met=false
exit=1
```

C1 happens to reach exit 2, but by a **coincidental** route (it notices the
missing `corpus/lessons/round-61-verifier-spotcheck.md` blob, not the bad
revision — note the message says "verifier spot-check absent", which
misattributes the cause). C2 reaches exit **1**, contradicting its own
docstring at `c63_quote_tool.py:11-12`:

> `Exits: 0 met; 1 not met; 2 could-not-evaluate (git unreadable).`

An unreadable revision is precisely "git unreadable", so it must be exit 2.
Exit 1 means "evaluated, and the answer is no" — a materially different claim
from "could not evaluate". The two are indistinguishable to any consumer that
keys on the exit code alone.

### 3.2 Root cause

Both counters use the same existence probe:

- `c63_quote_tool.py:50` —
  `probe = subprocess.run(["git", "-C", root, "rev-parse", "--verify", rev], …)`
- `c63_calibration.py:87` — the identical line.

`git rev-parse --verify` **does not verify object existence** for a
full-length 40-hex. Per `git rev-parse(1)` (measured on git 2.56.0):

> `--verify` — "Verify that exactly one parameter is provided, and that it
> **can be turned into a raw 20-byte SHA-1 that can be used to access the
> object database**." — and: "If you want to make sure that the output
> actually names an object in your object database … you can add the
> `^{type}` peeling operator."

Measured in the lane repo:

```
$ git -C $LANE rev-parse --verify deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
exit=0
$ git -C $LANE cat-file -e deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
exit=1
$ git -C $LANE rev-parse --verify nosuchbranch-xyz
fatal: Needed a single revision
exit=128
```

`rev-parse --verify` echoes any syntactically well-formed 40-hex back with
exit 0 — it only checks that the string *could* be a SHA-1, not that the
object is in the database. `cat-file -e` (exit 1) is the actual existence
check. A non-hex name like `nosuchbranch-xyz` fails name resolution outright
(rc 128), which is why the non-hex bogus form reaches exit 2 correctly.

This is **not** an artifact of the lane repo. Reproduced in a clean scratch
repo (`git -C "$D" init -q`, `rev-parse --show-toplevel` asserted equal to
`$D` before the first commit) where the *measured* commit does not exist:

```
deadbeefdeadbeefdeadbeefdeadbeefdeadbeef: verify_rc=0  cat_file_e_rc=1
05b0d7f4b4a23513390f7b92547e2b0f1fccb06f: verify_rc=0  cat_file_e_rc=1
```

The probe is also **not** inherited from the round-62 family in a way that
made it acceptable there: `c62_calibration.py` has the same weakness but its
exit-2 route is the missing-blob check, so the round-62 defect receipt
(`c62_calibration.py --root <fixture> --revision <rev>`) was never affected.

### 3.3 The realistic failure mode: a single mistyped hex digit

A typo in a real SHA almost always stays 40 hex characters, which is exactly
the shape that slips past the probe. Measured with the measured commit's own
SHA, last character changed `f` → `e`:

```
$ git rev-parse --verify 05b0d7f4b4a23513390f7b92547e2b0f1fccb06e
05b0d7f4b4a23513390f7b92547e2b0f1fccb06e
  verify_rc=0
  cat_file_e_rc=1
$ python3 -B $C1 --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06e
could-not-evaluate: verifier spot-check absent
  exit=2
$ python3 -B $C2 --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06e
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06e present=0 selftest=unevaluable met=false
  exit=1
```

A short-hash typo (`05b0d7f5`, 7 hex) *is* caught correctly (both exit 2),
because a short hex is resolved as an abbreviation and fails name resolution.

### 3.4 Direction of the error — false negative, never a false green

Checked explicitly, because the round's kill rule is directional:

- C2 on a bogus 40-hex → `present=0 selftest=unevaluable met=false`, exit 1.
  **Never `met=true`.** The tool blob is fetched with
  `git_show(root, rev, TOOL_REL)` (`c63_quote_tool.py:56`); for a nonexistent
  revision `git show` fails, `tool_blob is None`, and the counter returns 1
  at `c63_quote_tool.py:57-59`.
- C1 on a bogus 40-hex → exit 2, `met=true` never printed.

So the defect can only make a counter **fail to prove** a claim, never
**falsely prove** one. It does not reproduce a marker-only green and does not
trip either kill rule:

- C1 kill rule — "if the after receipt does not print `met=true` … or either
  control prints `met=true`, or any wave attack reproduces a marker-only
  green, C1 is `unprovable`": the after receipt prints `met=true`; the
  committed controls print `met=false`; no marker-only green is reproduced.
  **Not tripped.**
- C2 kill rule — "if the after receipt does not print `met=true`, or a stub
  tool passes, C2 is `unprovable`": the after receipt prints `met=true`.
  **Not tripped.**

### 3.5 Why it still matters (the receipt-integrity risk)

The practical exposure is **receipt laundering**, not a false green. A seat or
a later round that mistypes the revision SHA in a receipt command gets a
plausible-looking line on stdout:

```
revision=<typo> present=0 selftest=unevaluable met=false
```

That line is byte-for-byte the *shape* of the legitimate base receipt
`controls/base-c2.txt` (`revision=13d45198… present=0 selftest=unevaluable
met=false`, exit 1) — the only difference is the SHA. A reader comparing
"does it say `present=0 met=false`?" would see the expected red and not
notice that the revision was never evaluated at all. The exit code, which is
the cheap machine-readable discriminator, is exactly the thing that fails to
carry the distinction.

### 3.6 The fix (one line, per counter)

Use a probe that actually resolves the object. The `^{object}` peel is the
git-documented way and was verified to discriminate correctly:

```
$ for r in deadbeef…  05b0d7f4b4a23513390f7b92547e2b0f1fccb06f  05b0…b06e  nosuchbranch-xyz; do
    git rev-parse --verify --quiet "$r^{object}" >/dev/null 2>&1; echo "peeled_rc=$?"; done
peeled_rc=1     # deadbeef… (nonexistent)
peeled_rc=0     # the real measured commit
peeled_rc=1     # the 1-digit typo
peeled_rc=1     # the non-hex name
```

So `c63_quote_tool.py:50` and `c63_calibration.py:87` should pass
`f"{rev}^{{object}}"` to `git rev-parse --verify --quiet` (or keep the bare
`--verify` and add a `git cat-file -e` check), so that a nonexistent object
lands in the existing `could-not-evaluate` branch at
`c63_quote_tool.py:52-54` / `c63_calibration.py:89-91` and exits 2.

Note this also corrects C1's **misattributed** diagnostic: today C1 reports
"verifier spot-check absent" for a bad revision, which points the reader at
the corpus rather than at the revision argument.

**I did not apply this fix.** The counters are frozen by sha256 in the
contract (lines 22–23, 26–27), the contract states "A counter, control or
predicate changed after a seat has scored is not this round's rule", and this
seat is read-only against the frozen claim. The fix is reported for the L1's
round-64 decision.

---

## 4. Additional exit-code observations (no kill-rule impact)

### 4.1 `--root` at a repo subdirectory: C1 exit 0, C2 exit 1

```
$ python3 -B $C1 --root $LANE/corpus --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
$ python3 -B $C2 --root $LANE/corpus --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=failed met=false
exit=1
```

C1 is unaffected because `git -C <subdir>` still resolves the repository.
C2 fails because it runs the tool with `cwd=root` (`c63_quote_tool.py:66`)
and the frozen tool resolves its fixtures relative to `Path.cwd()`
(`scripts/quote_class.py:24-25`, `FIXTURES = Path("scripts/fixtures/quote-class")`),
so from `corpus/` the fixture files are not found and the selftest fails.
This is consistent with the contract's freeze note
(contract.md lines 51–54: "the frozen tool binds fixture resolution to the
invoking cwd (the lane root)") and with the counter's own design — it is
**not** a defect, but it is a real asymmetry between the two counters worth
recording: **`--root` must be the lane root for C2, but may be any path
inside the repo for C1.** All contract-specified invocations use `--root .`
at the lane root, so no committed receipt is affected.

### 4.2 `--root` at a non-repo directory → exit 2, both ✅

```
$ python3 -B $C1 --root /fast/scratch/hyaku/kake-r63/ExecExitCodes/notarepo --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
could-not-evaluate: revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f unreadable
exit=2
$ python3 -B $C2 --root /fast/scratch/hyaku/kake-r63/ExecExitCodes/notarepo --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
could-not-evaluate: revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f unreadable
exit=2
```

Also `--root` pointing at a *file* inside the repo → exit 2, both.

### 4.3 argparse rejects unknown flags with exit 2 (coincides with "could-not-evaluate")

```
$ python3 -B $C1 --bogus
usage: c63_calibration.py [-h] [--root ROOT] [--revision REVISION]
c63_calibration.py: error: unrecognized arguments: --bogus
exit=2
$ python3 -B $C2 --bogus
usage: c63_quote_tool.py [-h] [--root ROOT] [--revision REVISION]
c63_quote_tool.py: error: unrecognized arguments: --bogus
exit=2
```

argparse's default error exit is 2, which is the same code the counters use
for "could-not-evaluate". A usage error and an unreadable repository are
therefore indistinguishable by exit code (they differ on stdout vs stderr:
argparse writes to stderr, and so does the counter's exit-2 path — so even
the stream does not separate them). This is standard argparse behaviour and
not specific to these counters; noting it because the seat item is about
exit-code discriminability. The exit-2 code is documented as
"could-not-evaluate (git unreadable)", so a usage error landing in that
bucket mildly over-promises that the tree was inspected.

### 4.4 Non-commit revisions are accepted and can report `met=true`

Both counters accept any object name git can peel to a tree, not just
commits. A tree SHA at the measured commit yields `met=true` / exit 0 for
both:

```
$ python3 -B $C1 --root . --revision 1dac343d86c337e2ce4bffae2a2bc355a08af15e   # HEAD^{tree}
revision=1dac343d86c337e2ce4bffae2a2bc355a08af15e disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
$ python3 -B $C2 --root . --revision 1dac343d86c337e2ce4bffae2a2bc355a08af15e
revision=1dac343d86c337e2ce4bffae2a2bc355a08af15e present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

A blob SHA (not a tree) correctly fails: C1 exit 2, C2 exit 1. `HEAD` and
`HEAD^` also work (exit 0). The tree case is semantically harmless here —
`git show <tree>:<path>` reads the same bytes — but it confirms the counters
do not require a commit-shaped revision, consistent with the related
no-ancestry-check observation in
`.ufo/waves/round-63/w1/ReviewerFalseGreenDead.md:43-44`.

---

## 5. Exit-code summary table

| # | Scenario | C1 (`c63_calibration.py`) | C2 (`c63_quote_tool.py`) | Expected | Verdict |
|---|---|---|---|---|---|
| 1 | `--help` | exit 0, stdout | exit 0, stdout | 0 | ✅ |
| 2 | bogus `--revision nosuchbranch-xyz` | `could-not-evaluate: revision … unreadable`, exit 2 | same, exit 2 | 2 | ✅ |
| 3 | bogus `--revision deadbeef…` (40-hex) | `could-not-evaluate: verifier spot-check absent`, exit 2 | `present=0 selftest=unevaluable met=false`, exit **1** | 2 | ❌ **finding §3** |
| 4 | bogus `--revision <1-digit typo of a real SHA>` | exit 2 | exit **1** | 2 | ❌ **finding §3.3** |
| 5 | measured commit, real tree | `met=true`, exit 0 | `met=true`, exit 0 | 0 | ✅ |
| 6 | base revision | `met=false`, exit 1 | `present=0 met=false`, exit 1 | 1 | ✅ |
| 7 | non-repo cwd, `--root` absolute at lane | `met=true`, exit 0 | `met=true`, exit 0 | normal | ✅ |
| 8 | non-repo cwd, `--root` relative at lane | `met=true`, exit 0 | `met=true`, exit 0 | normal | ✅ |
| 9 | `--root` at repo subdir | `met=true`, exit 0 | `selftest=failed`, exit 1 | — | note §4.1 |
| 10 | `--root` at non-repo dir | exit 2 | exit 2 | 2 | ✅ |
| 11 | `--root` at a file | exit 2 | exit 2 | 2 | ✅ |
| 12 | unknown flag | exit 2 (argparse) | exit 2 (argparse) | — | note §4.3 |
| 13 | `--revision HEAD` / `HEAD^` / tree SHA | exit 0 | exit 0 | — | note §4.4 |

---

## 6. The four committed receipts reproduce byte-for-byte

Each committed receipt's result line compared against a fresh run's stdout
(exit code recorded separately):

```
$ python3 -B $L/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f  → exit 0
$ python3 -B $L/c63_quote_tool.py  --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f  → exit 0
$ python3 -B $L/c63_calibration.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa  → exit 1
$ python3 -B $L/c63_quote_tool.py  --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa  → exit 1

MATCH  after_c1     (controls/after-c1.txt)
MATCH  after_c2     (controls/after-c2.txt)
MATCH  base_c1      (controls/base-c1.txt)
MATCH  base_c2      (controls/base-c2.txt)
```

The `exit=` lines in the receipts (`after-c1.txt` exit=0, `after-c2.txt`
exit=0, `base-c1.txt` exit=1, `base-c2.txt` exit=1) match the observed exit
codes exactly.

---

## 7. Lane compliance

- **Files written:** only this report,
  `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/w1/ExecExitCodes.md`,
  plus scratch under
  `/fast/scratch/hyaku/kake-r63/ExecExitCodes/` (removed at the end of the
  seat).
- **Fleet repo untouched.** `git status --porcelain --untracked-files=no` is
  empty; `git diff --stat HEAD -- .ufo/waves/round-63/controls/ .ufo/waves/round-63/contract.md`
  is empty. The only untracked entries are the wave's own `w1.ready`,
  `w1.ready.dispatched` and `w1/` scaffolding, which pre-existed this seat
  (`w1/` is the wave's report directory). No `considerthese/`, no
  `MANIFEST.json`, no `.ufo/state`, no `scripts/`, no templates touched.
- **No commits, no push, no mutating git/jj** in the fleet repo or any sibling
  repo. The only `git init` was in scratch
  (`/fast/scratch/hyaku/kake-r63/ExecExitCodes/gitcheck`), where
  `git rev-parse --show-toplevel` was asserted equal to the scratch dir
  before the first commit, and the identity was throwaway
  (`git config user.email t@e.x`, `user.name t`) set **inside that scratch
  repo only**.
- **Frozen claim untouched.** All four frozen sha256s re-verified after the
  runs — unchanged (§1).
- **No tool installed.** No pacman, no `uv tool`, no `~/.local/bin` writes.
- **No subagent dispatched.** The seat spec permits a single labrat; none was
  needed — every line of evidence above is a direct measurement.

---

## 8. Verdict for the L1

1. **C1's exit-code contract holds on all four item sub-checks.** `--help`
   → 0, measured commit → 0, non-repo cwd → normal, and a bogus revision →
   2 for both the non-hex and the 40-hex forms. The 40-hex form reaches exit
   2 only incidentally (via the missing-blob branch) and reports a
   misattributed cause ("verifier spot-check absent" instead of "revision
   unreadable") — worth noting but not falsifying.
2. **C2's exit-code contract fails one sub-check.** A bogus `--revision`
   shaped like a full 40-hex SHA yields exit **1** (`present=0
   selftest=unevaluable met=false`) where the counter's own docstring
   specifies exit 2 (`could-not-evaluate (git unreadable)`). Root cause:
   `git rev-parse --verify <40-hex>` checks SHA-1 *syntax*, not object
   *existence*; a `^{object}` peel or a `git cat-file -e` fixes it (§3.6).
3. **Neither kill rule is tripped.** The C2 defect is a false *negative*
   only: `met=true` is never printed on an unreadable revision. The after
   receipt prints `met=true` and all four committed receipts reproduce
   byte-for-byte with matching exit codes (§6). C1 and C2 remain
   **verifiable** on this wave's evidence; the defect is a robustness gap in
   C2's exit-code semantics to carry into round 64's repair.
4. **Residual risk to name explicitly:** a mistyped 40-hex revision in any
   future receipt command produces a stdout line shape-identical to a
   legitimate red receipt, with the exit code failing to flag it. Receipt
   generators should assert the revision independently (e.g. compare against
   the contract's stated SHA) rather than trusting the counter's exit code.

---

Report: `.ufo/waves/round-63/w1/ExecExitCodes.md`
