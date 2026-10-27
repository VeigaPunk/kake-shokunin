# ExecReceiptReproduce — round-63 control receipt reproduction

## Assignment

Reproduce every round-63 control receipt from scratch in an independent
workspace: rebuild base and fixture runs with fresh scratch repos and confirm
each receipt's output line and exit code match what the committed receipt
records. Report any receipt that could not be reproduced.

## Verdict

**PASS — 7/7 recorded command runs across all 6 round-63 control receipts
reproduced byte-for-byte (output line + exit code). No receipt failed to
reproduce.**

One latent coupling was found and is reported under §5: the C2 counter
(`c63_quote_tool.py`) evaluates the tool's selftest against the **worktree**
of `--root`, not against the measured revision's tree, so its green is only
reproducible when the root worktree is at (or contains) the measured
revision's fixture files. The committed receipt was produced under exactly
that condition, so the receipt itself is faithful — the coupling is a
property of the counter, not a discrepancy in the receipt.

## 1. Scope and frozen inputs

All work was done under `/fast/scratch/hyaku/kake-r63/ExecReceiptReproduce/`.
No file in the fleet repo, `.ufo/state`, `scripts/`, `templates/`, the
lane corpus or `SOURCES.md` was created, modified or deleted. No git/jj
mutation was performed in the fleet repo. No commit, push or deploy.

Frozen artifacts re-verified by SHA-256 **as git objects at the measured
revision** `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f` (not merely as
worktree files), all matching the contract at
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/contract.md`:

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ for p in .ufo/waves/round-63/c63_calibration.py .ufo/waves/round-63/c63_quote_tool.py \
           scripts/quote_class.py .ufo/waves/round-63/quote-class/quote-classes.json; do
    printf '%s  %s\n' "$(git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:$p | sha256sum | cut -d' ' -f1)" "$p"
  done
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  .ufo/waves/round-63/c63_calibration.py
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  .ufo/waves/round-63/c63_quote_tool.py
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  .ufo/waves/round-63/quote-class/quote-classes.json
```

Contract-expected values (contract.md lines 24-26 and 32-33):
`bcd16f68…` (c63_calibration.py), `9fcbfad0…` (c63_quote_tool.py),
`431e75e8…` (scripts/quote_class.py), `5f48e26b…` (quote-classes.json).
**All four match.**

Receipt files themselves are committed and unmodified — worktree blob id
equals the blob id at both `7f77d12b` (the receipts commit) and `HEAD`:

```
$ git rev-parse 7f77d12b:.ufo/waves/round-63/controls/after-c1.txt HEAD:...  (abridged)
after-c1.txt  7f77d12b=087bb5a8730acdd36b5aa3aaf6f82ecbe537e732 HEAD=087bb5a8730acdd36b5aa3aaf6f82ecbe537e732 worktree=087bb5a8730acdd36b5aa3aaf6f82ecbe537e732  same=yes
after-c2.txt  7f77d12b=1eb9909c31d17ff10318ef541cc40b0c910b777c HEAD=1eb9909c31d17ff10318ef541cc40b0c910b777c worktree=1eb9909c31d17ff10318ef541cc40b0c910b777c  same=yes
```

## 2. Independent workspace

Two independent clones of the fleet repo were made into scratch (not the
fleet worktree), so no measurement depended on the fleet repo's mutable
state:

```
$ S=/fast/scratch/hyaku/kake-r63/ExecReceiptReproduce
$ git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin "$S/clone"
$ git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin "$S/clone2"
$ git -C "$S/clone" checkout -q --detach 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
```

The counters were read out of the clone at the measured revision, so the
counter bytes are the frozen ones.

## 3. Fixture rebuilds — byte-exact, including the recorded commit hashes

### 3.1 Marker-only fixture (receipt `control-marker-fixture.txt`)

The receipt records `rev 7833be888760bc7878857aa39362792b02e3ab07`. I rebuilt
it from the committed corpus copy (not from any scratch dir), with a
throwaway identity, and **landed on the exact recorded commit hash**:

```
$ D="$S/marker-fixture"; rm -rf "$D"; mkdir -p "$D"
$ git -C "$D" init -q
$ git -C "$D" rev-parse --show-toplevel
/fast/scratch/hyaku/kake-r63/ExecReceiptReproduce/marker-fixture      # == $D, verified before first commit
$ cp -a /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/controls/false-green-fixture/corpus "$D/"
$ git -C "$D" -c user.name=t -c user.email=t@t add corpus
$ GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t \
  GIT_AUTHOR_DATE="1793106850 -0300" GIT_COMMITTER_DATE="1793106850 -0300" \
  git -C "$D" commit -q -m "marker-only"
$ git -C "$D" rev-parse HEAD
7833be888760bc7878857aa39362792b02e3ab07
```

Recorded: `7833be888760bc7878857aa39362792b02e3ab07` — **exact match.**
The rebuilt tree is byte-identical to the committed corpus tree
`6467c207b5e3f1f3248ffc2080c1f7fa265c4690` (all five blob ids equal).

The round-62 defect receipt's fixture-input SHA-256s also verify against the
committed corpus (`.ufo/waves/round-62/controls/counter-false-green-l1.txt`
lines 19-24) — all five match byte-for-byte:
`0a9a0348…`, `635089aa…`, `373b9d25…`, `d7033c6d…`, `a27f4338…`.

### 3.2 Junk fixture (receipt `control-junk-fixture.txt`)

The receipt records `rev 7da479c28d206a9733cf2012b6ea434c4dab450f`. Its
inputs are **not committed in the fleet repo** (verified: all five blob ids
`86ae828b…`, `d634018e…`, `deb7a6b6…`, `a23cdcb7…`, `d1d40aad…` are ABSENT
from the fleet object database, and the distinctive marker line
`substantive X-Content-Type-Options Content-Type destination` appears nowhere
in the fleet tree). I reconstructed its content from the sibling L1 scratch
fixture `/fast/scratch/hyaku/kake-r63/L1/junk-fixture` (read-only), rebuilt
it in my own scratch, and **landed on the exact recorded commit hash**:

```
$ D="$S/junk-fixture"; rm -rf "$D"; mkdir -p "$D/corpus/lessons" "$D/corpus/knowledge"
$ ... write the five corpus files ...
$ git -C "$D" init -q
$ git -C "$D" rev-parse --show-toplevel
/fast/scratch/hyaku/kake-r63/ExecReceiptReproduce/junk-fixture        # == $D, verified before first commit
$ git -C "$D" -c user.name=t -c user.email=t@t add corpus
$ GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t \
  GIT_AUTHOR_DATE="1793106868 -0300" GIT_COMMITTER_DATE="1793106868 -0300" \
  git -C "$D" commit -q -m "junk"
$ git -C "$D" rev-parse HEAD
7da479c28d206a9733cf2012b6ea434c4dab450f
```

Recorded: `7da479c28d206a9733cf2012b6ea434c4dab450f` — **exact match.**
All five rebuilt blob ids equal the source fixture's blob ids.

## 4. Reproduction results — strict, receipt-vs-observed

A harness (`/fast/scratch/hyaku/kake-r63/ExecReceiptReproduce/verify.py`)
parses every committed receipt in `.ufo/waves/round-63/controls/`, extracts
each recorded `$ command`, its output line and its `exit=` line, re-runs the
command against my scratch workspace, and compares output line and exit code
byte-for-byte. Harness result:

```
MATCH    after-c1.txt                 run1  exit=0
   cmd: python3 -B .ufo/waves/round-63/c63_calibration.py --root .../clone --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
MATCH    after-c2.txt                 run1  exit=0
   cmd: python3 -B .ufo/waves/round-63/c63_quote_tool.py --root .../clone --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
MATCH    base-c1.txt                  run1  exit=1
   cmd: python3 -B .ufo/waves/round-63/c63_calibration.py --root .../clone --revision 13d4519818db28cd0aa912e49020659140d7b9fa
MATCH    base-c2.txt                  run1  exit=1
   cmd: python3 -B .ufo/waves/round-63/c63_quote_tool.py --root .../clone --revision 13d4519818db28cd0aa912e49020659140d7b9fa
MATCH    control-junk-fixture.txt     run1  exit=1
   cmd: python3 -B .ufo/waves/round-63/c63_calibration.py --root .../junk-fixture --revision 7da479c28d206a9733cf2012b6ea434c4dab450f
MATCH    control-marker-fixture.txt   run1  exit=0
   cmd: python3 -B .ufo/waves/round-62/c62_calibration.py --root .../marker-fixture --revision 7833be888760bc7878857aa39362792b02e3ab07
MATCH    control-marker-fixture.txt   run2  exit=1
   cmd: python3 -B .ufo/waves/round-63/c63_calibration.py --root .../marker-fixture --revision 7833be888760bc7878857aa39362792b02e3ab07

7/7 recorded runs reproduced byte-for-byte (output line + exit code)
receipts covered: 6  ['after-c1.txt', 'after-c2.txt', 'base-c1.txt', 'base-c2.txt', 'control-junk-fixture.txt', 'control-marker-fixture.txt']
driver_exit=0
```

### 4.1 The exact observed lines, per receipt

**`after-c1.txt`** (`.ufo/waves/round-63/controls/after-c1.txt:3-4`) — observed:
```
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

**`after-c2.txt`** (`controls/after-c2.txt:3-4`) — observed:
```
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

**`base-c1.txt`** (`controls/base-c1.txt:3-4`) — observed:
```
revision=13d4519818db28cd0aa912e49020659140d7b9fa disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
```

**`base-c2.txt`** (`controls/base-c2.txt:3-4`) — observed:
```
revision=13d4519818db28cd0aa912e49020659140d7b9fa present=0 selftest=unevaluable met=false
exit=1
```

**`control-marker-fixture.txt`** (`controls/control-marker-fixture.txt:4-8`) —
observed, run 1 = old `c62` counter (defect) and run 2 = repaired `c63`:
```
revision=7833be888760bc7878857aa39362792b02e3ab07 disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true
exit=0
revision=7833be888760bc7878857aa39362792b02e3ab07 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
```

**`control-junk-fixture.txt`** (`controls/control-junk-fixture.txt:4-5`) — observed:
```
revision=7da479c28d206a9733cf2012b6ea434c4dab450f disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1
```

### 4.2 Same commands against the live fleet root

Re-run verbatim in `/home/vgpnk/Projects/shokunin/kake-shokunin` (the way the
receipts record them, `--root .`) — identical output lines and exits:

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa present=0 selftest=unevaluable met=false
exit=1
```

### 4.3 Determinism, cwd-independence and path-independence

- **Determinism** — 3 consecutive runs of each after-counter produce one
  unique line (`sort | uniq -c` → count `3` for each), no drift.
- **cwd-independence** — invoking the counters from `/tmp` with an absolute
  `--root` yields the same lines and exits (C2 sets `cwd=root` for the tool
  subprocess, `c63_quote_tool.py:66`).
- **path-independence** — a second independent clone at a different absolute
  path (`clone2`) yields the same after-c1 and after-c2 lines and exits.

## 5. Finding: C2's counter is worktree-coupled, not revision-pure (latent, does not invalidate the receipt)

`c63_quote_tool.py` extracts the tool blob **from the measured revision**
(`git show <rev>:scripts/quote_class.py`, line 60-63) but runs it with
`cwd=root` (line 66). The tool resolves its own fixtures relative to
`Path.cwd()` (`scripts/quote_class.py:24` `LANE_ROOT = Path.cwd()`;
lines 79-80 `raw_path = LANE_ROOT / case["raw"]`). The four selftest fixture
paths therefore come from the **working tree of `--root`**, not from the
measured revision's tree.

Demonstrated: with the clone's worktree checked out at base (which lacks the
round-63 fixture files) but measuring the measured revision, C1 is unaffected
(all C1 inputs go through `git show`, `c63_calibration.py:88-93`) while C2
goes red for the wrong reason:

```
$ git -C "$S/clone2" checkout --detach 13d4519818db28cd0aa912e49020659140d7b9fa
$ python3 -B /tmp/c63_calibration.py --root "$S/clone2" --revision 05b0d7f4...
revision=05b0d7f4... disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
$ python3 -B /tmp/c63_quote_tool.py --root "$S/clone2" --revision 05b0d7f4...
revision=05b0d7f4... present=1 selftest=failed met=false
exit=1
```

The four selftest cases fail with `FileNotFoundError` on
`scripts/fixtures/quote-class/inline.raw.html`,
`markup.raw.html`, and `.ufo/waves/round-63/quote-class/S432.txt`.

**Impact on the receipts: none.** The committed `after-c2.txt` was measured
with the root worktree at the measured revision, where all four fixture files
exist (`scripts/fixtures/quote-class/*` and `.ufo/waves/round-63/quote-class/S432.txt`
are all present at `05b0d7f4` and absent at base). Under that condition my
reproduction reproduces the receipt exactly. The coupling means the C2 green
is not a pure function of the revision — a re-measure at a later/other
worktree state could differ — but the frozen predicate as written
("prints `present=1 selftest=4/4 frozen_cases=ok met=true` (exit 0) at the
measured revision") is satisfied and reproducible as recorded. Reported as
a robustness observation for the claim, not as a receipt discrepancy.

The contract's freeze-note (contract.md lines 30-33) documents the cwd
binding as the intended tool behaviour ("the frozen tool binds fixture
resolution to the invoking cwd (the lane root)"), so this is consistent with
the frozen design rather than a deviation from it.

## 6. Corroborating checks (not required by the receipts, but they confirm the receipts are meaningful)

### 6.1 The C1 marker-only defect really is dead

The old `c62` counter prints `met=true`/exit 0 on the marker-only fixture
(defect), while the repaired `c63` counter prints `met=false`/exit 1 on the
same tree — exactly the two lines recorded in `control-marker-fixture.txt`.
The routed round-62 defect is not reproducible under `c63`.

### 6.2 The C2 frozen-case-set check rejects a stub tool

A stub whose selftest returns `{"cases":[{"id":"whatever",...,"passed":true}],
"total":1,"passed":1,"ok":true}` (exit 0) is rejected:

```
C2 counter vs stub tool at a commit: revision=587d677b0a18b716ee3e8cceaa8a769981c11de1 present=1 selftest=1/1 frozen_cases=missing met=false exit= 1
```

`frozen_cases=missing` comes from the `FROZEN_CASE_IDS` set
(`c63_quote_tool.py:25-30`) checked at lines 77-83. The kill-rule clause
"a stub tool passes" does not fire.

### 6.3 The committed class ledger re-derives from the committed blobs

Independent re-derivation at the measured revision:

```
computed rawSha256 : 63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b
ledger   rawSha256 : 63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b
computed textSha256: 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69
ledger   textSha256: 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69
quote in raw  : False
quote in text : True
ledger class  : collapsed-only
```

Both SHA-256s match the committed ledger
`.ufo/waves/round-63/quote-class/quote-classes.json`, and the class
`collapsed-only` re-derives from the blobs exactly as `after-c1.txt` records
(`derived=collapsed-only class_match=1`).

## 7. What could NOT be reproduced, and why

- **No round-63 receipt failed to reproduce.** All 6 receipts, all 7
  recorded runs, matched byte-for-byte.
- The **round-62 defect receipt** cited by the contract
  (`.ufo/waves/round-62/controls/counter-false-green-l1.txt`) records a
  fixture rev `6e5a16076d8c73feff41b7af2159bef9fe1046c8` from a scratch repo
  that its own receipt states was deleted (`scratch_cleanup=clean`). That
  exact commit hash is not reconstructible from committed inputs: I swept
  ~236M candidate commit objects (tree `6467c207…` × identities × timezones
  × 20 message variants over a 2-day window) and found no preimage. This is
  **not a round-63 receipt**, so it does not count against this seat's
  assignment; the round-63 marker receipt supersedes it with a fixture that
  **is** byte-reconstructible (rev `7833be88…`, reproduced exactly), and the
  r62 receipt's substantive claim (c62 prints `met=true` on a marker-only
  fixture) is independently reproduced above in §4.1 / §6.1.

## 8. Files and commands

Written (only my own report path):
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/w1/ExecReceiptReproduce.md`

Scratch (all under `/fast/scratch/hyaku/kake-r63/ExecReceiptReproduce/`):
`clone/`, `clone2/`, `marker-fixture/`, `junk-fixture/`, `stub-probe/`,
`stub-repo/`, `verify.py`, `verify.sh`.

Commands of record:
```
python3 -B .ufo/waves/round-63/c63_calibration.py --root <root> --revision <rev>
python3 -B .ufo/waves/round-63/c63_quote_tool.py  --root <root> --revision <rev>
python3 -B .ufo/waves/round-62/c62_calibration.py --root <root> --revision <rev>
python3 /fast/scratch/hyaku/kake-r63/ExecReceiptReproduce/verify.py   # 7/7 MATCH, exit 0
```

**Tool installs: none.** No package manager was invoked; `pacman` was not run
(per the host-wide pacman guard). Only stock `git` and `python3` were used.

**Fleet repo left untouched:** `git status --porcelain` in
`/home/vgpnk/Projects/shokunin/kake-shokunin` shows only the pre-existing
untracked wave files (`.ufo/waves/round-63/w1.ready`,
`.ufo/waves/round-63/w1.ready.dispatched`, `.ufo/waves/round-63/w1/`),
which existed before this seat ran. No tracked file was modified, no commit
or push was made, `MANIFEST.json` and `considerthese/` were not touched, and
no `.ufo/state` was written.

## 9. Summary for the claim

| Receipt | Claim | Reproduced | Exit | Observed line matches |
|---|---|---|---|---|
| `after-c1.txt` | C1 green at measured commit | yes | 0 | byte-for-byte |
| `after-c2.txt` | C2 green at measured commit | yes | 0 | byte-for-byte |
| `base-c1.txt` | C1 red at base | yes | 1 | byte-for-byte |
| `base-c2.txt` | C2 red at base | yes | 1 | byte-for-byte |
| `control-marker-fixture.txt` | old c62 green / new c63 red on marker-only fixture | yes | 0 / 1 | byte-for-byte (both runs) |
| `control-junk-fixture.txt` | c63 red on adversarial junk fixture | yes | 1 | byte-for-byte |

**7/7 runs, 6/6 receipts reproduced.** No receipt was unreproducible. The
single caveat (§5) is a worktree coupling in the C2 counter that does not
affect the committed receipts as measured and recorded, and is disclosed
here for the claim's robustness record.
