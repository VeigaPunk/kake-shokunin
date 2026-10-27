# Seat ExecCounterRerun — round-63 C1/C2 counting-command re-run

**Lane role:** leaf executor, no subagent dispatch, no commits, no push, no mutating
git/jj anywhere. Fleet root: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Measured commit `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`; base (round-62 tip)
`13d4519818db28cd0aa912e49020659140d7b9fa`.

**Item:** re-run both counting commands at base and at the measured commit, paste
full output, and confirm the outputs equal the committed receipts
`controls/base-c1.txt`, `controls/base-c2.txt`, `controls/after-c1.txt`,
`controls/after-c2.txt` byte-for-byte on the result lines.

**Headline:** all four re-runs reproduce the committed receipts **byte-for-byte** on
the result lines and match the recorded exit codes. Determinism confirmed over 3
repeats. Two counter-design observations are reported in §5 — neither falsifies a
receipt, but both are in scope for the L1's kill-rule reading.

---

## 1. Frozen artifacts — sha256 verified before any run

Command (cwd = fleet root):

```
$ sha256sum .ufo/waves/round-63/c63_calibration.py .ufo/waves/round-63/c63_quote_tool.py \
    .ufo/waves/round-63/quote-class/quote-classes.json scripts/quote_class.py
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  .ufo/waves/round-63/c63_calibration.py
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  .ufo/waves/round-63/c63_quote_tool.py
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  .ufo/waves/round-63/quote-class/quote-classes.json
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
```

All four equal the contract's frozen values
(`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/contract.md`
lines 22–23, 26–27, 55–56, 64–65). Re-verified **after** all runs below —
unchanged.

Both revisions resolve in the fleet repo:

```
$ git rev-parse --verify 13d4519818db28cd0aa912e49020659140d7b9fa
13d4519818db28cd0aa912e49020659140d7b9fa
$ git rev-parse --verify 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
```

Working-tree blobs are byte-identical to the measured-commit blobs for every
input the counters read, so the run sees the measured tree:

```
scripts/quote_class.py                       SAME 431e75e8…1f14
.ufo/waves/round-61/sources/S432.html        SAME 63b0a018…911b
.ufo/waves/round-63/quote-class/S432.txt     SAME 8b90d096…2a69
scripts/fixtures/quote-class/inline.raw.html SAME 1ac3d248…2a06
scripts/fixtures/quote-class/inline.txt      SAME b47cc0f1…c4380
scripts/fixtures/quote-class/markup.raw.html SAME 5af86cbb…7f26
scripts/fixtures/quote-class/markup.txt      SAME 415364a0…1fd9
```

---

## 2. The four counting commands — full output

Exactly the commands from my item (absolute `--root`):

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 -B .ufo/waves/round-63/c63_calibration.py \
    --root /home/vgpnk/Projects/shokunin/kake-shokunin \
    --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1

$ python3 -B .ufo/waves/round-63/c63_calibration.py \
    --root /home/vgpnk/Projects/shokunin/kake-shokunin \
    --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0

$ python3 -B .ufo/waves/round-63/c63_quote_tool.py \
    --root /home/vgpnk/Projects/shokunin/kake-shokunin \
    --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa present=0 selftest=unevaluable met=false
exit=1

$ python3 -B .ufo/waves/round-63/c63_quote_tool.py \
    --root /home/vgpnk/Projects/shokunin/kake-shokunin \
    --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

stderr was empty on all four runs (0 bytes each).

The receipts used the relative form `--root .`; re-running that form gives
**identical** output and identical exit codes for all four (verified). The
absolute form above is the one named in my item; both agree.

---

## 3. Byte-for-byte comparison against the committed receipts

Method: for each receipt, extract the `^revision=` result line from the receipt,
extract the observed stdout, compare with `=` (shell string equality) and
independently with sha256 of each.

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/controls
$ for pair in "base-c1.txt:$c1_base.out:1" "after-c1.txt:$c1_after.out:0" \
              "base-c2.txt:$c2_base.out:1" "after-c2.txt:$c2_after.out:0"; do … done
```

Result:

| Receipt | Result line | Exit | receipt-line sha256 | observed-out sha256 | Match |
|---|---|---|---|---|---|
| `base-c1.txt` | `revision=13d45198… met=false` | 1 | `0248a0774450a4af26519a50d0c6435f5b26c35ed78b3684e358f276de8ede48` | `0248a077…ede48` | **IDENTICAL** |
| `after-c1.txt` | `revision=05b0d7f4… met=true` | 0 | `edf9f23034b775718efaf5e2946b82fd405ff823e65c21cd956c5712385c34c9` | `edf9f230…4c9` | **IDENTICAL** |
| `base-c2.txt` | `revision=13d45198… met=false` | 1 | `fe56addeaf583ac09e502e50eaf4daba86edbb8d71d38f306da8f26a0066903f` | `fe56adde…903f` | **IDENTICAL** |
| `after-c2.txt` | `revision=05b0d7f4… met=true` | 0 | `8a9caf5de1109cdd20cff028fdc523593611b9072c7124515d8d7e77ea2dbb0b` | `8a9caf5d…b0b` | **IDENTICAL** |

Per-run verification output (abridged):

```
### base-c1.txt vs /tmp/r63rerun/c1_base.out (expected exit=1)
RESULT-LINE: IDENTICAL (byte-for-byte)
receipt exit=1  observed exit=1
sha256(receipt_result_line)=0248a0774450a4af26519a50d0c6435f5b26c35ed78b3684e358f276de8ede48
sha256(observed_out)=0248a0774450a4af26519a50d0c6435f5b26c35ed78b3684e358f276de8ede48

### after-c1.txt vs /tmp/r63rerun/c1_after.out (expected exit=0)
RESULT-LINE: IDENTICAL (byte-for-byte)
receipt exit=0  observed exit=0
sha256(receipt_result_line)=edf9f23034b775718efaf5e2946b82fd405ff823e65c21cd956c5712385c34c9
sha256(observed_out)=edf9f23034b775718efaf5e2946b82fd405ff823e65c21cd956c5712385c34c9

### base-c2.txt vs /tmp/r63rerun/c2_base.out (expected exit=1)
RESULT-LINE: IDENTICAL (byte-for-byte)
receipt exit=1  observed exit=1
sha256(receipt_result_line)=fe56addeaf583ac09e502e50eaf4daba86edbb8d71d38f306da8f26a0066903f
sha256(observed_out)=fe56addeaf583ac09e502e50eaf4daba86edbb8d71d38f306da8f26a0066903f

### after-c2.txt vs /tmp/r63rerun/c2_after.out (expected exit=0)
RESULT-LINE: IDENTICAL (byte-for-byte)
receipt exit=0  observed exit=0
sha256(receipt_result_line)=8a9caf5de1109cdd20cff028fdc523593611b9072c7124515d8d7e77ea2dbb0b
sha256(observed_out)=8a9caf5de1109cdd20cff028fdc523593611b9072c7124515d8d7e77ea2dbb0b
```

**All four receipts confirmed byte-for-byte, with matching exit codes.**

### Determinism

Three full repeats of all four commands; every line identical, no variation:

```
$ for i in 1 2 3; do for t in c63_calibration c63_quote_tool; do for r in <base> <measured>; do … done; done; done | sort | uniq -c
```

Each of the four distinct result lines appeared with multiplicity 3 and no other
line appeared — i.e. zero variance across 3 runs.

---

## 4. Independent re-derivation of the C1 result (not taken from the counter's own output)

I re-derived C1's `resolved` from the committed bytes directly, without using
the counter's printed values.

**Ledger blob pins and inline class derivation at the measured revision:**

```
raw sha256   = 63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b
ledger rawSha= 63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b MATCH
text sha256  = 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69
ledger textSha= 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69 MATCH
ledger quote == FROZEN_QUOTE: True
quote in raw  (raw-substring)? False
quote in text (collapsed-only)? True
independent derived class = collapsed-only
ledger matchClass = collapsed-only -> class_match = 1
```

**Semantic components, computed independently at both revisions:**

| Component | base `13d45198` | measured `05b0d7f4` |
|---|---|---|
| `disagreements` (spot-check lines with S432+Disagree) | 1 | 1 |
| `correction` (3-part: `[r63-correction` + frozen span + ledger path) | 0 | 1 |
| `criterion` (QUALITY.md names the proposition) | 1 | 1 |
| `lesson_gate` (round-63.md: Gate + verdict + author-side) | 0 (file absent) | 1 |
| `source_row` (`^\|\s*S432\s*\|` in SOURCES.md) | 1 | 1 |
| **`resolved`** | **False** | **True** |

These reproduce the counter's printed components exactly. At base,
`corpus/lessons/round-63.md` is **absent** from the tree (`lesson_gate=0`),
which is why base is red.

**Real tool, run directly** (independent of the counter):

```
$ python3 -B scripts/quote_class.py --selftest --json
{"cases": [{"derived": "raw-substring", "expected": "raw-substring", "id": "inline_raw_substring", "passed": true}, {"derived": "collapsed-only", "expected": "collapsed-only", "id": "markup_collapsed_only", "passed": true}, {"derived": "absent", "expected": "absent", "id": "absent_everywhere", "passed": true}, {"derived": "collapsed-only", "expected": "collapsed-only", "id": "s432_real", "passed": true}], "ok": true, "passed": 4, "total": 4}
exit=0

$ python3 -B scripts/quote_class.py classify --quote 'The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.' --raw .ufo/waves/round-61/sources/S432.html --text .ufo/waves/round-63/quote-class/S432.txt
derived=collapsed-only
exit=0
```

The tool's own `s432_real` case reads the two committed blobs and derives
`collapsed-only` — it is a genuine derivation, not an assertion.

---

## 5. Attack probes (scratch fixtures, since deleted)

All fixtures were built under `/fast/scratch/hyaku/kake-r63/ExecCounterRerun/`,
each with `git init -q` and `git rev-parse --show-toplevel` asserted equal to the
fixture dir before the first commit, with a throwaway local identity. The fleet
repo was never mutated (`git status --porcelain` shows only the wave harness's
own untracked files). **All scratch dirs have been deleted.**

### 5.1 Round-62 marker-only false-green is dead under the new counter

Fixture: the committed round-62 corpus copied byte-exact from
`.ufo/waves/round-62/controls/false-green-fixture/corpus/` into a scratch repo
(rev `3d9687d396f1de96fa15fa5cd0e30ea12edcddea`).

```
$ python3 -B .ufo/waves/round-62/c62_calibration.py --root <fixture> --revision <rev>
revision=3d9687d3… disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true
exit=0                      # ← the round-62 defect reproduces on the OLD counter

$ python3 -B .ufo/waves/round-63/c63_calibration.py --root <fixture> --revision <rev>
revision=3d9687d3… disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1                      # ← dead under the repaired counter
```

This reproduces `controls/control-marker-fixture.txt` field-for-field (same
values, different scratch rev — the receipt's own rev `7833be88…` is scratch-only
and is not in the fleet repo, exactly as that receipt states). The counter's
component values match the receipt's new-counter line on every field.

### 5.2 Junk-marker control reproduced

Adversarial markers with the frozen span and ledger path but **no retained
blobs and no ledger** (rev `936e3cfb4829469af6e1869a4e55cdde72b8fc22`):

```
revision=936e3cfb… disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1
```

Identical to `controls/control-junk-fixture.txt` on every field. ✔

### 5.3 Forged-ledger attacks on C1 — all fail

| Attack | Fixture | Result |
|---|---|---|
| **A** | Full marker set + ledger whose sha256s are *correct* but whose blobs are actually `raw-substring`, ledger claims `collapsed-only` | `blobs_match=1 derived=raw-substring class_match=0 … met=false`, exit 1 |
| **B** | Full marker set + fully self-consistent ledger (correct quote, correct sha256s) but the quote **absent** from both blobs | `blobs_match=1 derived=absent class_match=0 … met=false`, exit 1 |
| **C** | Full marker set + ledger row whose `quote` ≠ `FROZEN_QUOTE` | `blobs_match=0 derived=unevaluable class_match=0 … met=false`, exit 1 |

Attack A is the important one: the inline re-derivation (`classify()` over the
revision's blobs) **overrides the ledger's assertion** and refuses the
false `collapsed-only` label. The ledger cannot lie its way to green. This is
the round-62 defect class, closed.

### 5.4 Separability — both directions confirmed (contract §Separability)

The contract claims C1 is verifiable on a tree where C2's tool never landed, and
C2 on a tree without C1's correction/ledger/counters. Both verified against a
scratch clone of the fleet repo:

```
######## PROBE 1: C1 on a tree where C2's tool NEVER landed ########
rev=37908895644eb9d29bbe685a6ad0146e0456a8c6  scripts/quote_class.py present? NO
C1: revision=37908895… quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true   exit=0
C2: revision=37908895… present=0 selftest=unevaluable met=false                                                          exit=1

######## PROBE 2: C2 on a tree with NO C1 correction/ledger/counters ########
rev=7d03a45403853f97a5e3ea93f9fba4fbcdff8c65   (ledger, round-63 lesson and c63_calibration.py all removed)
C2: revision=7d03a454… present=1 selftest=4/4 frozen_cases=ok met=true                                                   exit=0
```

C1 stays green without the tool; C2 stays green without any C1 artifact. The
claims do score independently, as the contract states.

### 5.5 C2 stub-resistance — partial (design observation, not a receipt falsification)

Two stub tools against `c63_quote_tool.py`:

- **Stub missing a frozen case id** (3 of 4 ids): `present=1 selftest=3/3
  frozen_cases=missing met=false`, exit 1 → **rejected**, as the contract's
  frozen-case-set check requires.
- **Stub emitting all four frozen ids with `passed=true` and no derivation at
  all** (12 lines; never opens a corpus file): `present=1 selftest=4/4
  frozen_cases=ok met=true`, exit 0 → **accepted**.
- Substituting that stub for the frozen tool **at the measured revision** (all
  corpus files present, real blobs in tree): `revision=097b8cfe… present=1
  selftest=4/4 frozen_cases=ok met=true`, exit 0.

The counter never compares the tool blob's sha256 against the contract's frozen
`431e75e8…` (`grep -nE 'sha256|hashlib' .ufo/waves/round-63/c63_quote_tool.py`
→ no matches). Sibling seat `ExecC2CounterAttack.md` §8.1–8.2 independently
reaches the same finding (including the truthy-`"ok"` variant), so this is a
consistent property of the counter, not a one-off.

**This does not falsify the C2 receipt.** The tool at the measured revision
*is* the frozen tool (sha256 `431e75e8…1f14`, verified), and the receipts are
correct. The contract's C2 kill rule reads "if the after receipt does not print
`met=true`, **or a stub tool passes**, C2 is `unprovable`", and names the
counter's frozen-case-set check as the stub defence. On the contract text as
written, a stub that *emits* the four frozen ids defeats that check — the check
is on id presence, not on tool identity. Whether this triggers the kill rule is
the L1's adjudication, not mine; I record it because it is squarely inside my
item's attack surface.

### 5.6 C2's counter is working-tree-dependent (documented freeze note — confirmed)

The tool resolves fixtures from the invoking cwd (`LANE_ROOT = Path.cwd()`,
`scripts/quote_class.py:29`), so the C2 counter's result depends on the live
tree's corpus files, not solely on the revision. Demonstrated on a scratch clone
at the measured revision with the revision itself untouched:

```
baseline (clean tree):        present=1 selftest=4/4 frozen_cases=ok met=true   exit=0
working-tree S432.txt tampered: present=1 selftest=failed met=false              exit=1
restored:                     present=1 selftest=4/4 frozen_cases=ok met=true   exit=0
```

This is the pre-wave, pre-scoring freeze note in `contract.md:57–63` — the tool
sha changed `40655dd8…` → `431e75e8…` for exactly this reason. Not a defect, but
it means the C2 receipt is only reproducible on a tree whose working-tree corpus
matches the measured commit. In the fleet repo that holds today (§1).

### 5.7 C1 goes green if the disagreement record itself is deleted

On a scratch clone at the measured revision, deleting the single S432 `Disagree`
row from `corpus/lessons/round-61-verifier-spotcheck.md` (a **non-append-only**
edit, and therefore outside the contract's No-harm rules) yields:

```
revision=d0acc70aa55bfeaf44f321143e0ba8b440a7af81 disagreements=0 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

`disagreements` drops to 0, and because `resolved` is a conjunction of four
components that do not include `disagreements == 0`, `met` stays true. The
counter reports the disagreement count but does not gate on it.

**Scope note:** the attack requires deleting a committed row, which the
contract's No-harm section forbids ("Append-only edits to existing files"), so it
is not an available attack against this round's committed state — and it is *not*
a marker-only green (the blobs, ledger and class are all genuinely present and
re-derived). I record it as a counter-design observation for the L1, consistent
with the sibling `RevengerC62Defect.md` / `ScoutC62Defect.md` readings.

---

## 6. Receipt provenance and no-harm spot-check

- The contract was frozen at `6d8c52a6` (09:54:45) with the counting commands
  already present (`git show 6d8c52a6:.ufo/waves/round-63/contract.md` →
  lines 46–47 and 65–66 contain both `python3 -B …` counting commands).
- The measured commit `05b0d7f4` (10:19:30) changed only the tool sha and
  added the freeze note (`git diff 6d8c52a6 05b0d7f4 -- …/contract.md` — a
  single 7-line hunk, no change to the predicates, controls or counting
  commands).
- The after receipts were committed at `7f77d12b` (10:19:59), **after** the
  measured commit (`git merge-base --is-ancestor 05b0d7f4 7f77d12b` → exit 0),
  and `base-c1.txt`, `base-c2.txt`, `control-marker-fixture.txt`,
  `control-junk-fixture.txt` are byte-identical at the measured revision to the
  working tree; `after-c1.txt`/`after-c2.txt` are byte-identical at `7f77d12b`
  to the working tree.
- `scripts/quote_class.py` is genuinely **absent** at base
  (`git cat-file -e 13d45198…:scripts/quote_class.py` → "exists on disk, but not
  in '13d45198…'"), which is the mechanical reason base prints `present=0`.

---

## 7. Files changed

**None in the fleet repo.** `git status --porcelain` in
`/home/vgpnk/Projects/shokunin/kake-shokunin` shows only the wave harness's own
untracked files (`.ufo/waves/round-63/w1.ready`,
`.ufo/waves/round-63/w1.ready.dispatched`, `.ufo/waves/round-63/w1/`), none
written by me. No commits, no push, no mutating git/jj anywhere; the frozen
claim, counters, receipts, `scripts/`, `templates/`, `.ufo/state`, the corpus and
`SOURCES.md` were read but never edited.

Written: this report only —
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/w1/ExecCounterRerun.md`.

Scratch fixtures under `/fast/scratch/hyaku/kake-r63/ExecCounterRerun/` were
**deleted** after use (verified absent).

**Tooling installs:** none. Only stock `git`, `sha256sum`, `python3` already on
the host. No pacman transactions (all pacman transactions are paused host-wide).

---

## 8. Verdict

1. **All four receipts confirmed byte-for-byte** on the result lines, with
   matching exit codes (base → exit 1, measured → exit 0, both counters). Fully
   deterministic over 3 repeats.
2. **The C1 result is independently re-derivable** from committed bytes: the
   ledger's blob pins match, the class re-derives to `collapsed-only` inline, and
   all four `resolved` components reproduce at both revisions.
3. **C1 survives the round-62 attack class**: the marker-only false-green
   reproduces on the old `c62_calibration.py` and is dead on `c63_calibration.py`;
   forged-ledger attacks (A/B/C) cannot reach green.
4. **Separability holds** in both directions.
5. **Two counter-design observations for the L1** (§5.5 stub-emits-frozen-ids
   accepted by C2; §5.7 `disagreements` not gated by C1). Neither falsifies a
   receipt in this round; both are in the kill-rule's decision surface.
