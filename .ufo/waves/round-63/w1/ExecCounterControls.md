# Seat ExecCounterControls — round-63 w1

**Item:** Repeat the round-62 `ReviewerCounterControls` method against
`.ufo/waves/round-63/c63_calibration.py`: construct marker-only fixture
variants (with and without the S432 `Disagree` line, with a fabricated ledger
whose shas match nothing) and run the counter on each. Every variant must
print `met=false`.

**Verdict: ALL ASSIGNED VARIANTS PRINT `met=false` (exit 1).** The
round-62 marker-only false-green is dead in the c63 family, and the
disagreement dimension now actually moves the counter's output.

**Scope note.** Read-only against the fleet repo
`/home/vgpnk/Projects/shokunin/kake-shokunin`. Nothing in the fleet repo,
`.ufo/state`, `scripts/`, `templates/`, the corpus or `SOURCES.md` was
modified; no git/jj mutation was performed against the fleet repo or any
sibling repo; no commit, push, or deploy. All fixtures were built under
`/fast/scratch/hyaku/kake-r63/ExecCounterControls/` in throwaway repos with a
throwaway identity local to each fixture, and the whole scratch directory was
deleted at the end of the seat. This report file is the only path written
outside scratch.

**Tools installed:** none. No `pacman` transaction was run (pacman is paused
host-wide).

---

## 1. The frozen target, verified before attacking

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin && sha256sum \
    .ufo/waves/round-63/c63_calibration.py \
    .ufo/waves/round-63/c63_quote_tool.py \
    scripts/quote_class.py \
    .ufo/waves/round-63/quote-class/quote-classes.json
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  .ufo/waves/round-63/c63_calibration.py
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  .ufo/waves/round-63/c63_quote_tool.py
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  .ufo/waves/round-63/quote-class/quote-classes.json
```

All four match the contract's frozen hashes exactly. The counter was attacked
**unmodified**.

### Canonical receipts re-run at the fleet root (read-only)

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
```

These reproduce `.ufo/waves/round-63/controls/after-c1.txt` and
`base-c1.txt` byte-for-byte.

---

## 2. Method (round-62 `ReviewerCounterControls` method, repeated)

The round-62 method was: build a scratch git repo containing only the literal
markers the counter tests for, no source body, and run the counter on it. I
repeated it, and hardened the marker bundle so the attack cannot fail for a
trivial reason.

Every fixture:

1. `mkdir -p /fast/scratch/hyaku/kake-r63/ExecCounterControls/<name>`
2. `git -C "$D" init -q`
3. **assert** `git -C "$D" rev-parse --show-toplevel` == `$D` (asserted in
   the driver; every fixture raised on mismatch, none did)
4. write the fixture files, `git -C "$D" add -A`
5. commit with a **throwaway identity local to the fixture repo only**
   (`GIT_AUTHOR_NAME=kake-r63-fixture`, `GIT_AUTHOR_EMAIL=fixture@invalid.example`)
6. `REV=$(git -C "$D" rev-parse HEAD)`
7. `python3 -B .ufo/waves/round-63/c63_calibration.py --root "$D" --revision "$REV"`

The marker bundle is the **real** corpus at the measured revision
`05b0d7f4b4a23513390f7b92547e2b0f1fccb06f` (byte-exact `git show` of
`corpus/lessons/round-61-verifier-spotcheck.md`,
`corpus/knowledge/response-header-expectations.md`, `corpus/QUALITY.md`,
`corpus/lessons/round-63.md`, `corpus/SOURCES.md`) — not hand-typed
approximations. So every variant carries the genuine `[r63-correction]` block
quoting the frozen span, the genuine ledger path, the genuine criterion
terms, the genuine `## Gate` lesson block and the genuine S432 registry row.
Only the *evidence* is missing or forged, which is exactly the attack.

The frozen `FROZEN_QUOTE` constant was loaded out of the counter module
itself (`importlib` on the frozen file) rather than retyped, so no variant can
fail on a byte-level quote mismatch.

---

## 3. ASSIGNED VARIANTS — every one prints `met=false`

### V1 — marker-only, S432 `Disagree` line present (the round-62 attack verbatim)

Marker bundle only; no `.ufo/` evidence tree at all.

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root /fast/scratch/hyaku/kake-r63/ExecCounterControls/v1-marker-only-disagree --revision 071089ec5c6049b564afc8704995bbdb70ebda51
revision=071089ec5c6049b564afc8704995bbdb70ebda51 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1
```

`criterion=1 lesson_gate=1 source_row=1` — the marker bundle is complete and
the counter sees it. `quote_correction=0` because there are no committed bytes
to re-derive the digests and the class from; `derived=unevaluable` is printed
explicitly, so the class is **not** assumed from the ledger or from the
knowledge prose.

### V2 — marker-only, the S432 `Disagree` line neutralised

Same bundle; the round-61 spot-check's S432 row verdict changed
`Disagree` → `Agree` (body otherwise untouched).

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root /fast/scratch/hyaku/kake-r63/ExecCounterControls/v2-marker-only-no-disagree --revision 7417924afa41ed2f4f28d4da033a87b0344f83b8
revision=7417924afa41ed2f4f28d4da033a87b0344f83b8 disagreements=0 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false
exit=1
```

`disagreements=0` — the count genuinely moved, so the disagreement dimension
is measured and not hard-wired. Still red, because the correction is unbound.

### V3 — marker-only + fabricated ledger whose shas match nothing

Marker bundle **plus** a well-formed ledger at
`.ufo/waves/round-63/quote-class/quote-classes.json` whose `rawSha256` is
`0000…0` and `textSha256` is `ffff…f` (matching nothing), and **plus**
fabricated `S432.html` / `S432.txt` blobs at the real paths — so the failure
cannot be attributed to the blobs merely being absent.

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root /fast/scratch/hyaku/kake-r63/ExecCounterControls/v3-fabricated-ledger-bad-shas --revision 09c5ea8f1c732fd4db09df7fc3c84eade71f0670
revision=09c5ea8f1c732fd4db09df7fc3c84eade71f0670 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1
```

`blobs_match=0`. The counter re-derives `sha256(raw_blob)` / `sha256(text_blob)`
itself (`c63_calibration.py:133-137`) and compares them to the ledger rows; a
ledger whose digests match nothing fails the comparison, and the class is never
taken from the ledger's asserted `matchClass`.

### V28 — marker-only + fabricated ledger matching nothing **and** claiming a different quote

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root /fast/scratch/hyaku/kake-r63/ExecCounterControls/v28-marker-only-fabricated-ledger-wrong-quote --revision e51c101c16971d33ce84152287bd4d3532105e16
revision=e51c101c16971d33ce84152287bd4d3532105e16 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1
```

### V26 — marker-only, the entire S432 row removed from the spot-check

Stronger reading of "without the S432 Disagree line": the whole
`| S432 / Fetch | … |` row is deleted.

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root /fast/scratch/hyaku/kake-r63/ExecCounterControls/v26-spotcheck-s432-row-removed --revision f08a8cb48b8efddec84b2c505743f6f39f652a0e
revision=f08a8cb48b8efddec84b2c505743f6f39f652a0e disagreements=0 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false
exit=1
```

### Assigned-variant summary

| # | Variant | `met` | exit |
|---|---|---|---|
| V1 | marker-only, `Disagree` present | **false** | 1 |
| V2 | marker-only, `Disagree` → `Agree` | **false** | 1 |
| V3 | marker-only + fabricated ledger, shas match nothing | **false** | 1 |
| V26 | marker-only, whole S432 spot-check row removed | **false** | 1 |
| V28 | marker-only + fabricated ledger, wrong quote + matching-nothing shas | **false** | 1 |

**All five print `met=false` with exit 1.**

---

## 4. Independent reproduction of the committed control receipt

The round-62 committed marker-only fixture was copied byte-exact from the
fleet repo and run under **both** counters, so the committed
`control-marker-fixture.txt` receipt is re-derived rather than trusted.

```
$ python3 -B .ufo/waves/round-62/c62_calibration.py --root <fixture> --revision 6f0dddf1082f0862368b2bbc216744031ecc3580   # old counter, family defect
revision=6f0dddf1082f0862368b2bbc216744031ecc3580 disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true
exit=0

$ python3 -B .ufo/waves/round-63/c63_calibration.py --root <fixture> --revision 6f0dddf1082f0862368b2bbc216744031ecc3580   # repaired counter
revision=6f0dddf1082f0862368b2bbc216744031ecc3580 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
```

Byte-exactness of the copy (sha256 of each corpus file, `identical_to_committed=True`
for all five):

```
corpus/QUALITY.md                                     373b9d254dff8668f9ae273e3f24ec87ff9b52f2c862ebabd158d76ad64d0457
corpus/SOURCES.md                                     a27f4338e565e5231b48adb49c24f759612f8827927cd80cf838462ff4dd8d2b
corpus/lessons/round-61-verifier-spotcheck.md         0a9a034861b19ba9f0c2b49adb9e9c394b406816a63dc458b1b8ee62668405c3
corpus/lessons/round-62.md                            d7033c6dc40448844e9c652900fb54298de8af539c8e45819e29d377bb1a8923
corpus/knowledge/response-header-expectations.md      635089aadf398ea2b17799494c5a0e209af3f87a4459234e71892d29351ba6b6
```

The old counter greens it; the new counter is red. **The routed round-62
defect does not reproduce on c63.**

---

## 5. Supplementary probes — what the c63 gates actually bind

These are outside the assigned item; they map the counter's real defence
surface so the L1 knows which gates are load-bearing.

| # | Fixture | Result | exit |
|---|---|---|---|
| V6 | real measured blobs + real ledger + real corpus (after-state repro in scratch) | `met=true` | 0 |
| V5 | real blobs + real ledger, `Disagree` line neutralised | `met=true` (`disagreements=0`) | 0 |
| V7 / V19 | real blobs, ledger `matchClass` forged to `raw-substring` | `blobs_match=1 derived=collapsed-only class_match=0 met=false` | 1 |
| V8 | real blobs, ledger `quote` altered | `blobs_match=0 met=false` | 1 |
| V9 | real blobs, ledger absent | `blobs_match=0 met=false` | 1 |
| V10 | real blobs, ledger row under id `S433` | `blobs_match=0 met=false` | 1 |
| V13 | self-consistent fabrication whose fabricated **raw** blob contains the quote | `derived=raw-substring class_match=0 met=false` | 1 |
| V14 | real blobs, knowledge entry without the ledger path | `quote_correction=0 met=false` | 1 |
| V16 | ledger with the **real** shas, blobs absent | `blobs_match=0 met=false` | 1 |
| V21 | ledger with the correct S432 row **first** and a forged one second | `blobs_match=0 met=false` | 1 |
| V22 | ledger with a forged S432 row first and the correct one second | `met=true` (last row wins) | 0 |
| V27 | spot-check file absent entirely | `could-not-evaluate: verifier spot-check absent` | 2 |

Load-bearing findings:

- **The class is genuinely re-derived, not trusted.** V7/V19 (forged
  `matchClass`) and V13 (a fabricated raw blob that *contains* the quote, so
  the derived class becomes `raw-substring`) both go red. A ledger that lies
  about the class cannot manufacture a green.
- **The digests are re-derived from the blobs**, so V3/V8/V9/V10/V16/V21 all
  go red.
- **The disagreement dimension is real** (V2/V26 move `disagreements` to 0;
  V5 shows `disagreements=0` with a green because the *evidence* is genuine —
  the counter green on V5 is correct: the correction genuinely resolves the
  disagreement there).
- **Ledger row order is not checked** (V21/V22): `c63_calibration.py:132`
  builds `{row["id"]: row for row in classes}`, so the **last** `S432` row
  wins. A ledger with a correct row followed by a forged row goes red; the
  same ledger with the order reversed goes green. Not exploitable on its own
  (a green still needs the blobs to hash to the recorded digests), but the
  ledger is read order-sensitively.
- **Exit 2 is not a green.** V27 (spot-check absent) exits 2, not 0.

---

## 6. Residual gap found (NOT a marker-only green; does not trip the C1 kill rule)

My assigned variants are all red, and the round-62 defect species is dead.
However, probing the *evidence* gates rather than the marker gates exposed a
green that the frozen predicate does not exclude.

**V18 — genuine round-61 raw body untouched, fabricated flat-text blob,
self-consistent ledger → `met=true`.**

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root /fast/scratch/hyaku/kake-r63/ExecCounterControls/v18-real-raw-fabricated-text --revision cc87b66a9425fd2d4b4128bcde8f23153ebbc399
revision=cc87b66a9425fd2d4b4128bcde8f23153ebbc399 disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

The fixture keeps the **genuine** `.ufo/waves/round-61/sources/S432.html`
(sha256 `63b0a018…911b`, 1,854,393 bytes — byte-identical to the retained
body) and replaces only the round-63 flat-text blob with 192 hand-written
bytes that merely *contain* the frozen span, plus a ledger whose digests hash
those fabricated bytes.

**Root cause.** The counter never checks that the committed flat-text blob is
a rendering *of* the committed raw blob. `classify()`
(`c63_calibration.py:59-67`) is two substring tests over whatever two files
the tree commits; the raw→text derivation is never re-run, and the recipe
named in the ledger (`extract_text.py`) is never executed. The counter also
never consults the round-61 fetch receipt, which pins the raw body
independently:

```
$ python3 -c "...receipts.json S432 sha256 = 63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b"
receipts.json S432 sha256 = 63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b
measured raw blob sha256   = 63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b
equal = True
```

`grep -c 'receipts.json' .ufo/waves/round-63/c63_calibration.py` → **0**; the
same for `extract_text` → **0**.

**How far the text blob may drift** (real raw body untouched, ledger digest
recomputed over the drifted blob — V31):

| Committed flat-text blob | bytes | counter verdict |
|---|---|---|
| the frozen span alone, one line | 155 | `met=true` exit 0 |
| the span wrapped in unrelated prose | 192 | `met=true` exit 0 |
| the real rendering minus its first 100 000 chars | 190 480 | `met=true` exit 0 |
| the real rendering with **one byte** changed | 290 480 | `met=true` exit 0 |
| (the real rendering, for reference) | 290 480 | — |

So the committed `S432.txt` could be replaced by a 155-byte file containing
the span, and the counter would still report `derived=collapsed-only
class_match=1 met=true`.

**Scope and severity — read this before acting on it.**

- This is **not** a marker-only green. The kill rule reads "any wave attack
  reproduces a **marker-only** green" (contract §C1). The V18 tree commits
  genuine span bytes and genuine retained evidence for the *raw* blob; the
  kill rule does not name this species. So **C1 is not `unprovable` by this
  seat's evidence**, and I make no such claim.
- The real measured tree is **not** affected. I re-ran the committed recipe
  against the committed raw body and it reproduces the committed flat-text
  blob byte-for-byte:

  ```
  $ python3 -B extract_text.py --raw S432.html --out rendered.txt
  extracted 1854393 bytes -> 286933 chars
  $ sha256sum rendered.txt committed.txt
  8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  rendered.txt
  8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  committed.txt
  $ cmp rendered.txt committed.txt && echo "RECIPE REPRODUCES COMMITTED TEXT BLOB EXACTLY"
  RECIPE REPRODUCES COMMITTED TEXT BLOB EXACTLY
  ```

  The measured tree's `S432.txt` is genuinely the recipe's output of the
  genuine raw body, and the raw body is the byte-identical live
  `fetch.spec.whatwg.org` body per the round-61 receipt. `after-c1.txt` is
  therefore truthful about the tree it measures.
- What the counter would *not* catch, if a later round rewrote the flat-text
  blob or the raw body: the counter certifies the tree's **internal**
  consistency, not the blobs' **provenance**.

**Constructive fix, verified (V33).** Two additional gates close the hole and
keep the real tree green:

- **Rule A** — `sha256(raw_blob)` must equal the round-61 fetch receipt's
  S432 sha256 (`63b0a018…911b`), read from
  `.ufo/waves/round-61/sources/receipts.json` at the measured revision.
- **Rule B** — `sha256(extract_text.py(raw_blob))` must equal
  `sha256(committed text blob)`, i.e. re-run the committed recipe (read via
  `git show` into a temp dir) and compare bytes before honouring
  `textSha256` / `blobs_match`.

| Tree | Rule A | Rule B | strengthened verdict |
|---|---|---|---|
| REAL measured tree | True | True | **PASS** (stays green) |
| fabricated raw + fabricated text (V12) | False | False | **FAIL** |
| REAL raw + fabricated text (V18) | True | False | **FAIL** |
| REAL raw + real text, one byte changed (V31) | True | False | **FAIL** |

Rule B keeps C1 independent of `scripts/quote_class.py`, so the contract's
Separability clause is preserved. Rule A additionally makes the counter bind
the retained body to an independently committed fetch receipt rather than to
the tree's own ledger.

**Related, smaller gap (V32).** The counter never cross-checks the
*knowledge entry's own* stated blob digests against the ledger's. Replacing
the two digests in `corpus/knowledge/response-header-expectations.md`
(`8b90d096…` → `0000…`, `63b0a018…` → `1111…`) while leaving the ledger
correct leaves the verdict unchanged:

```
revision=686d587bc980076621694c40e06c722c3df4b81e disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

Two committed files state the same two digests and the counter reconciles
neither with the other.

---

## 7. Cross-check on C2 (out of my item; recorded because it surfaced)

The C2 counter reads the tool from the **revision** but runs it with
`cwd=root` — the **working tree**. The frozen `s432_real` case resolves its
two blob paths relative to `cwd`
(`scripts/quote_class.py:57-63`, `LANE_ROOT = Path.cwd()`), so it reads
working-tree bytes.

- Working tree corrupted, commit untouched → `selftest=failed met=false`
  (exit 1), while the committed text blob still hashes
  `8b90d096…2a69`.
- **Inverse (V30):** the *revision's* committed text blob has the quote
  removed, but the working tree carries the real 290 480-byte rendering →
  `present=1 selftest=4/4 frozen_cases=ok met=true` (exit 0). The counter
  green on a revision that does not contain the evidence.

At the measured revision the working tree and the revision are byte-identical
for these paths (`git diff --stat 05b0d7f4… HEAD -- .ufo/waves/round-63/quote-class
.ufo/waves/round-61/sources corpus/` → empty), so `after-c2.txt` is not
false today. But the counter's C2 predicate is stated at a revision while
its real-corpus case is evaluated at the working tree. This is C2's counter,
not mine; I record the observation for the L1 and the C2 seats.

---

## 8. What was NOT done

- No counter, contract, receipt, ledger, corpus file, `SOURCES.md`,
  `considerthese/`, `MANIFEST.json`, `.ufo/state`, `scripts/` or
  `templates/` was modified — the frozen artifacts were attacked, not edited.
  Post-run fleet hashes are unchanged (§1) and `git status --porcelain` in the
  fleet root shows only this seat's own untracked report path.
- No git/jj mutation against the fleet repo or any sibling repo; no commit,
  push, deploy, or external-state remediation.
- No independent verification of the round-61 fetch itself: the raw body was
  taken from committed bytes, not re-fetched from the network.
- The severity/claim calls in §6 and §7 are evidence, not adjudications. The
  kill-rule question ("does a self-consistent fabrication make C1
  `unprovable`?") is the L1's, and I have not made it.

## 9. Cleanup

`/fast/scratch/hyaku/kake-r63/ExecCounterControls/` removed entirely
(`scratch_cleanup=clean`). Fixture repos, drivers and transcripts deleted.
Only this report file remains outside scratch.
