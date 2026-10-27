# ExecDoNothingControl — round-63 w1 seat report

**Item:** Prove the do-nothing control cannot reach the target: verify that at base
`13d4519818db28cd0aa912e49020659140d7b9fa` both counters print `met=false` (paste),
and argue from the counter code why no tree lacking the retained blobs + ledger +
correction can print `met=true` for C1 or `present=1` for C2.

**Verdict: the do-nothing claim as literally stated is TRUE for C1 and for
`present=1` on C2, but FALSE for the C2 *target* line.** Measured:

| Claim | Result | Evidence |
|---|---|---|
| At base, C1 prints `met=false` (exit 1) | **CONFIRMED** | §2 CMD1 |
| At base, C2 prints `met=false` (exit 1) | **CONFIRMED** | §2 CMD2 |
| No tree lacking blobs+ledger+correction prints `met=true` for C1 | **CONFIRMED** | §4 (12 ablations, all red) |
| No tree lacking blobs+ledger+correction prints `present=1` for C2 | **CONFIRMED** | §5.1 |
| …and therefore cannot reach the C2 target `present=1 selftest=4/4 frozen_cases=ok met=true` | **REFUTED** | §5.2 — a hard-coding stub tool reaches `met=true` on a tree with **no blobs, no ledger, no correction** |

The C2 counter's four-case "frozen case set" gate is the load-bearing defect, and it is
independently reproducible from committed bytes alone. I report it; I do not adjudicate
the claim.

**Scope note.** Read-only against the fleet repo
`/home/vgpnk/Projects/shokunin/kake-shokunin`. Nothing in the fleet repo, `.ufo/state`,
`scripts/`, `templates/`, the corpus or `SOURCES.md` was modified; no git/jj mutation
was performed against the fleet repo or any sibling repo; no commit, push, deploy or
external-state change. All fixtures were built under
`/fast/scratch/hyaku/kake-r63/ExecDoNothingControl/` in throwaway repos whose identity
(`f@l` / `F`) is local to each fixture; each fixture's top-level was asserted with
`git -C "$D" rev-parse --show-toplevel` **before** its first commit. The scratch
directory was deleted at the end of the seat (`scratch_cleanup=clean`). This report file
is the only path written outside scratch.

**Tools installed:** none. No `pacman` transaction was run (pacman is paused host-wide).

---

## 1. Frozen artifacts, byte-verified

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ sha256sum .ufo/waves/round-63/c63_calibration.py \
            .ufo/waves/round-63/c63_quote_tool.py \
            scripts/quote_class.py \
            .ufo/waves/round-63/quote-class/quote-classes.json
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  .ufo/waves/round-63/c63_calibration.py
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  .ufo/waves/round-63/c63_quote_tool.py
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  .ufo/waves/round-63/quote-class/quote-classes.json
```

All four match the contract (`.ufo/waves/round-63/contract.md:38-39`, `:56-57`) exactly.

Measured commit `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`; base (round-62 tip)
`13d4519818db28cd0aa912e49020659140d7b9fa`.

---

## 2. THE REQUESTED PASTE — both counters at base print `met=false`

Command and output, run in the fleet root at the exact base revision:

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1

$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa present=0 selftest=unevaluable met=false
exit=1
```

Both byte-identical to the committed receipts
`.ufo/waves/round-63/controls/base-c1.txt` and `base-c2.txt`.

Same counters at the measured commit, for contrast:

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0

$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

---

## 3. The do-nothing tree, as a repo

Base tree extracted byte-exact into a throwaway repo (top-level asserted before the
first commit):

```
$ D=/fast/scratch/hyaku/kake-r63/ExecDoNothingControl/donothing
$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin archive 13d4519818db28cd0aa912e49020659140d7b9fa | tar -x -C "$D"
$ git -C "$D" init -q
$ echo "toplevel=$(git -C "$D" rev-parse --show-toplevel)"
toplevel=/fast/scratch/hyaku/kake-r63/ExecDoNothingControl/donothing
$ test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"   # asserted, ok
$ git -C "$D" config user.email fixture@localhost; git -C "$D" config user.name Fixture
$ git -C "$D" add -A; git -C "$D" commit -q -m "do-nothing: byte-exact base tree"
REV=286cbeb29e214958796702bb1669f32e85080469
```

Counters pointed at it:

```
revision=286cbeb29e214958796702bb1669f32e85080469 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
revision=286cbeb29e214958796702bb1669f32e85080469 present=0 selftest=unevaluable met=false
exit=1
```

An **empty** repo (nothing landed at all) is not even evaluable by C1 and is red by C2:

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root "$EMPTY" --revision 0305398de509bb8ef06d9e54c051c7d6f6091777
could-not-evaluate: verifier spot-check absent          (stderr)
exit=2
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root "$EMPTY" --revision 0305398de509bb8ef06d9e54c051c7d6f6091777
revision=0305398de509bb8ef06d9e54c051c7d6f6091777 present=0 selftest=unevaluable met=false
exit=1
```

Exit 2 is *not* `met=true`; the C1 kill rule requires the after receipt to print
`met=true` (exit 0), so a tree that cannot even be evaluated cannot score.

---

## 4. C1 — the code argument, then the ablation matrix

### 4.1 Why a tree lacking blobs + ledger + correction cannot print `met=true`

`.ufo/waves/round-63/c63_calibration.py`, decision path:

* `:107-109` — `raw_blob = git_show(root, rev, QUOTE_REL)`,
  `text_blob = git_show(root, rev, TEXT_REL)`, `ledger_blob = git_show(root, rev, LEDGER_REL)`.
  All three are read **from the revision**, never from the working tree.
* `:112-119` — ledger absent ⇒ `ledger_err = "ledger_absent"`; ledger unparseable ⇒
  `ledger_err = "ledger_unreadable:<Exc>"`. In both cases `ledger` stays `{}`.
* `:121-125` — `correction` requires **all three** of: the string `[r63-correction` in
  `corpus/knowledge/response-header-expectations.md`, the exact `FROZEN_QUOTE` (152
  chars, U+2019 apostrophe) in that same file, and the ledger path string in that file.
* `:130-137` — `blobs_match` is computed **only** inside
  `if raw_blob is not None and text_blob is not None and ledger_err is None:` and
  requires `ledger.get("S432")` to exist with
  `rawSha256 == sha256(raw_blob)`, `textSha256 == sha256(text_blob)` and
  `quote == FROZEN_QUOTE`.
* `:138-143` — `class_match` requires the **inline** round-50 re-derivation
  (`classify()`, `:60-68`, inlined so C1 never gates on `scripts/quote_class.py`) to
  yield `collapsed-only` **and** the ledger's recorded `matchClass` to be
  `collapsed-only`.
* `:145` — `quote_correction = int(correction and blobs_match and class_match)`.
* `:164-166` — `resolved = (quote_correction and criterion and lesson_gate and
  source_row)`; `met = bool(resolved)`.

**Therefore:** `met=true` ⇒ `quote_correction=1` ⇒ `correction=1` ∧ `blobs_match=1` ∧
`class_match=1`. `blobs_match=1` is arithmetically impossible unless **both** retained
blobs *and* a well-formed ledger row exist **at the measured revision**; `class_match=1`
is impossible unless the class re-derives from those same committed bytes. Drop any one
of the retained blobs, the ledger, or the correction block and `quote_correction` is
pinned to 0, `resolved` to 0, `met` to `false`. That is the "marker-only green is dead
by construction" claim, and it is structural — no marker string can substitute for the
bytes.

### 4.2 The ablation matrix (12 trees, all red)

Each fixture is a fresh throwaway repo at `/fast/scratch/hyaku/kake-r63/ExecDoNothingControl/fix/`;
top-level asserted before first commit in every case. Command shape for each row:

```
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_calibration.py \
      --root <fixture> --revision <fixture rev>
```

| # | Mutation | Output | exit |
|---|---|---|---|
| A0 | do-nothing (byte-exact base tree) | `quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 … met=false` | 1 |
| A1 | drop retained **text** blob `.ufo/waves/round-63/quote-class/S432.txt` | `quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 … met=false` | 1 |
| A2 | drop retained **raw** blob `.ufo/waves/round-61/sources/S432.html` | `quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 … met=false` | 1 |
| A3 | drop the class ledger `.ufo/waves/round-63/quote-class/quote-classes.json` | `quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 … met=false` | 1 |
| A4 | ledger `textSha256` corrupted to `0…0` | `quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 … met=false` | 1 |
| A5 | ledger `matchClass` changed to `raw-substring` | `blobs_match=1 derived=collapsed-only class_match=0 … met=false` | 1 |
| A5b | ledger `quote` changed to a different sentence | `quote_correction=0 blobs_match=0 … met=false` | 1 |
| A6 | knowledge: `[r63-correction` → `[r62-correction` | `quote_correction=0 blobs_match=1 derived=collapsed-only class_match=1 … met=false` | 1 |
| A7 | knowledge: frozen quote removed | `quote_correction=0 blobs_match=1 … met=false` | 1 |
| A8 | knowledge: ledger path string removed | `quote_correction=0 blobs_match=1 … met=false` | 1 |
| A9 | drop `corpus/lessons/round-63.md` | `lesson_gate=0 … met=false` | 1 |
| A10 | QUALITY: `X-Content-Type-Options` / `Content-Type` / `destination` redacted | `criterion=0 … met=false` | 1 |
| A11 | SOURCES: `\| S432 \|` row deleted | `source_row=0 … met=false` | 1 |
| A13 | ledger **and** text blob dropped, all markers left intact | `quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false` | 1 |
| F1 | **maximal marker planting**: every string the counter greps for placed in exactly the file it greps (`[r63-correction]` + frozen quote + ledger path in the knowledge file; `substantive` + `round-61-verifier-spotcheck` + all three purpose terms in QUALITY; `## Gate` + `Disagree` + `collapsed-only` + `author-side` in the lesson; the `\| S432 \|` row in SOURCES) — **with both retained blobs and the ledger deleted** | `disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false` | 1 |
| F2 | F1 **plus** a fabricated ledger row (correct `quote`, `matchClass=collapsed-only`, zeroed shas) — still no retained bytes | `quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 … met=false` | 1 |

F1 is the sharpest form of the round-62 routed defect: every marker the counter
greps for is present and correctly placed, the S432 `Disagree` line still stands, and
the counter is still red — `quote_correction=0`, `derived=unevaluable`.

### 4.3 Independent reproduction of the committed marker-only fixture

The committed round-62 fixture was copied byte-exact into a throwaway repo and run
through **both** counter generations:

```
$ cp -a /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/controls/false-green-fixture/corpus "$D/"
$ git -C "$D" init -q   # toplevel asserted == $D before first commit
$ git -C "$D" add corpus; git -C "$D" commit -q -m "committed round-62 marker-only fixture, byte-exact"
REV=841138a90d48c4ba43f55f3355d8f891b4f7de8f

$ python3 -B .ufo/waves/round-63/c62_calibration.py --root "$D" --revision "$REV"   # OLD counter
revision=841138a90d48c4ba43f55f3355d8f891b4f7de8f disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true
exit=0                                     # <-- the round-62 routed defect, reproduced

$ python3 -B .ufo/waves/round-63/c63_calibration.py --root "$D" --revision "$REV"   # NEW counter
revision=841138a90d48c4ba43f55f3355d8f891b4f7de8f disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1                                     # <-- repaired counter, red
```

The old family defect reproduces exactly as documented in
`.ufo/waves/round-62/controls/counter-false-green-l1.txt`; the repaired counter is red
on the same bytes. **The marker-only false-green is dead.**

---

## 5. C2 — `present=1` is unreachable without the tool; but the *target* line is reachable without the blobs

### 5.1 `present=1` genuinely requires the tool at the revision

`c63_quote_tool.py:56-59`: `tool_blob = git_show(root, rev, TOOL_REL)`; if it is
`None` the counter prints `present=0 selftest=unevaluable met=false` and exits 1.
At base, `scripts/quote_class.py` does not exist at the revision (verified:
`git cat-file -e 13d4519…:scripts/quote_class.py` → absent; the base tree's `scripts/`
listing contains no `quote_class.py`), hence `present=0` — §2 CMD2 and §3.

`present=1` is therefore emitted only when the tool blob exists at the revision
(`:86-87`, the only other `present=1` sites are `:69` `selftest=failed` and `:74`
`selftest=unparseable`, both of which are `met=false`).

### 5.2 REFUTATION: the C2 target line is reachable on a tree with no blobs, no ledger, no correction

`.ufo/waves/round-63/c63_quote_tool.py:76-85` is the entire "stub defence":

```python
cases = {c.get("id"): c for c in result.get("cases", [])}
frozen_ok = all(
    cases.get(cid, {}).get("passed") is True
    and cases.get(cid, {}).get("derived") == cases.get(cid, {}).get("expected")
    for cid in FROZEN_CASE_IDS
)
total = result.get("total")
passed = result.get("passed")
met = bool(result.get("ok") and frozen_ok and total == passed
           and total == len(FROZEN_CASE_IDS))
```

The counter runs the tool blob as a subprocess and trusts the tool's **own** JSON
(`:61-67`). A tool that simply *prints* the four frozen case ids with
`derived == expected` and `passed == true` satisfies `frozen_ok` and `met` — without
doing any classification, without touching the retained blobs.

Measured, three independent trees:

| # | Tree | C2 output | exit |
|---|---|---|---|
| B4 / D4 | measured tree with `scripts/quote_class.py` replaced by a constant-output stub that hard-codes the four frozen ids (`derived=collapsed-only`, `expected=collapsed-only`, `passed=true` for each, `total=4`, `passed=4`, `ok=true`) | `present=1 selftest=4/4 frozen_cases=ok met=true` | **0** |
| C-stub | **base tree** (no `.ufo/waves/round-63/` at all: no text blob, no ledger, no correction, no lesson) **+ the same stub tool** | `present=1 selftest=4/4 frozen_cases=ok met=true` | **0** |
| C-stub2 | measured tree with **both retained blobs and the ledger deleted** + the stub tool | `present=1 selftest=4/4 frozen_cases=ok met=true` | **0** |

C-stub is the decisive row: the tree is *the base tree* — it lacks the retained blobs,
the class ledger, the correction block, the round-63 lesson, the criterion and every
other artifact C1 demands — and C2 still prints the full target line
`present=1 selftest=4/4 frozen_cases=ok met=true` with exit 0.

The counter never pins the tool's sha256. `grep -n "sha256" .ufo/waves/round-63/c63_quote_tool.py`
returns nothing; the only reference to the tool is `TOOL_REL = "scripts/quote_class.py"`
(`:24`) and `git_show` (`:56`). The contract freezes the tool hash
(`431e75e8…41f14`, `contract.md:56-57`), but the **counter** does not check it — the
hash is checked by humans and receipts, not by the instrument. So the C2 counter
measures *"some file at `scripts/quote_class.py` printed four JSON objects"*, not
*"the frozen tool ran"*.

The contract's C2 kill rule (`contract.md:70-72`) reads:

> Kill rule: if the after receipt does not print `met=true`, **or a stub tool passes**,
> C2 is `unprovable`.

and the contract's own control clause (`contract.md:66-69`) asserts:

> the counter's frozen-case-set check rejects a stub selftest missing the four frozen
> case ids (`inline_raw_substring`, `markup_collapsed_only`, `absent_everywhere`,
> `s432_real`).

Both clauses are contradicted by the measurement above: a stub tool that *includes* the
four frozen ids passes the counter with `met=true`. The narrow wording "missing the four
frozen case ids" is technically satisfied by B3 (a stub missing `s432_real` and
substituting `extra_case_not_frozen` → `frozen_cases=missing met=false`, exit 1) — but
that is a check the stub can trivially defeat by *including* the ids, which is what
B4/D4/C-stub do. I report this; the adjudication is not mine.

### 5.3 The C2 counter is also not revision-pure for the blobs it consumes

The tool's `s432_real` selftest case resolves its two blob paths **relative to the
invoking cwd** (the contract's freeze note, `contract.md:59-64`), and the counter runs
the tool with `cwd=root` (`:66`). `root` is the *working tree* of `--root`, not the
measured revision. Measured:

| # | Situation | C1 | C2 |
|---|---|---|---|
| E1 | revision **lacks** the text blob, working tree **has** it | `met=false` | `present=1 selftest=4/4 frozen_cases=ok met=true` (exit 0) |
| E2 | revision lacks the text blob, working tree lacks it too | `met=false` | `present=1 selftest=failed met=false` (exit 1) |
| E3 / B7 | revision is green, working-tree text blob corrupted | `met=true` | `present=1 selftest=failed met=false` (exit 1) |
| D5 | real frozen tool, blobs absent from revision **and** working tree | `met=false` | `present=1 selftest=failed met=false` (exit 1) |

C1 is revision-pure (it reads every input via `git_show(root, rev, …)`), so it is
unaffected by working-tree corruption (E3). C2 is **not**: its verdict depends on the
working tree's bytes at the moment of the run. Consequence for the counting command
`python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision <commit>`: run
against a checkout whose working tree differs from the measured revision, the counter
scores the *working tree*, not the revision. The committed after receipt
`.ufo/waves/round-63/controls/after-c2.txt` is consistent with this repo's working tree
(`git diff --stat 05b0d7f4… HEAD -- scripts/quote_class.py scripts/fixtures/quote-class
.ufo/waves/round-61/sources/S432.html .ufo/waves/round-63/quote-class` → empty), so
the receipt is honest *here*; but the instrument is not revision-bound for its blob
inputs.

---

## 6. Two further C1 observations (not part of my item, reported for the record)

**6.1 The ledger's own hashes are the only provenance anchor, and they are
self-certifying.** C1 re-derives `rawSha256`/`textSha256` from the blobs *at the
revision* and compares them to the ledger, but it never checks that the raw blob is
the authentic upstream Fetch document, and it never re-runs the committed recipe
`.ufo/waves/round-63/quote-class/extract_text.py` to confirm the flat-text blob is
*that raw blob's* rendering. Consequences I measured on green-tree mutations:

| # | Mutation of the green tree | C1 result | exit |
|---|---|---|---|
| A12f | append the frozen quote to the **raw** blob and re-hash the ledger's `rawSha256` | `blobs_match=1 derived=raw-substring class_match=0 … met=false` | 1 |
| A14 / D1 | **replace** the flat-text blob with a fabricated file that contains the quote, re-hash the ledger's `textSha256` | `blobs_match=1 derived=collapsed-only class_match=1 … met=true` | **0** |
| D3 | **replace** the raw blob with unrelated HTML, re-hash the ledger's `rawSha256` (flat-text blob untouched) | `blobs_match=1 derived=collapsed-only class_match=1 … met=true` | **0** |

So the C1 counter is sound against *marker-only* attacks (its stated repair target) and
against *class mislabelling* (A5, A12f), but a tree that rewrites the retained blobs
**and** the ledger's hashes together reaches `met=true` with a self-consistent but
non-authentic pair. For the committed pair this is a non-issue — I verified the
committed flat-text blob is exactly the committed recipe's output on the committed raw
blob:

```
$ git show 05b0d7f4…:.ufo/waves/round-61/sources/S432.html | sha256sum
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  -
$ git show 05b0d7f4…:.ufo/waves/round-63/quote-class/S432.txt | sha256sum
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  -
$ python3 -B .ufo/waves/round-63/quote-class/extract_text.py --raw raw.html --out out.txt
extracted 1854393 bytes -> 286933 chars
$ sha256sum out.txt
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  out.txt
$ python3 -B .ufo/waves/round-63/quote-class/extract_text.py --selftest
selftest 1/1
```

Both hashes equal the committed ledger's `rawSha256`/`textSha256`
(`quote-classes.json`), and the recipe reproduces the committed flat-text blob
byte-for-byte. So the committed evidence chain is sound; the *counter* simply does not
enforce it (it could, by pinning the raw blob's hash and/or re-running the recipe).

**6.2 The C1 `unresolved` field is advisory only.** `:164-166`: `unresolved =
disagreements if not resolved else 0`. At the measured commit the counter prints
`disagreements=1 … unresolved=0 met=true` — the S432 `Disagree` line is still present
in `corpus/lessons/round-61-verifier-spotcheck.md` at
`05b0d7f4…` (the counter reads it at `:95-98`), and it is *the correction that
discharges it*. That is the intended round-63 resolution (admit the span as
`collapsed-only`), so it is not a defect; I note it only so that the `unresolved=0`
in the after receipt is not mistaken for "the disagreement was deleted".

---

## 7. Answers to the two questions I was asked, stated plainly

**Q: At base, do both counters print `met=false`?**
Yes. Pasted in §2, byte-identical to the committed receipts `base-c1.txt` / `base-c2.txt`.
Exit 1 in both cases. A do-nothing tree extracted byte-exact from base (§3) reproduces
the same red output, and an empty repo is red or unevaluable (exit 2), never `met=true`.

**Q: Why can no tree lacking the retained blobs + ledger + correction print `met=true`
for C1, or `present=1` for C2?**
* **C1 — confirmed, structurally and empirically.** `met=true` requires
  `quote_correction=1` (`:145`), which requires `correction=1` (`:121-125`: the
  `[r63-correction` tag, the exact 152-char frozen quote, and the ledger path, all in
  the knowledge file) **and** `blobs_match=1` (`:130-137`: both retained blobs present
  at the revision, a well-formed ledger row, and the ledger's hashes matching those
  blobs) **and** `class_match=1` (`:138-143`: the class re-derived *inline from those
  bytes* equals `collapsed-only` equals the ledger's recorded class). Missing any one
  ⇒ `quote_correction=0` ⇒ `resolved=0` ⇒ `met=false`. Fifteen independent ablations
  (§4.2), including maximal marker planting with every grep-able string in place and
  no bytes at all (F1, F2), are all red.
* **C2 — `present=1` is confirmed, the target line is not.** `present=1` requires the
  tool blob at the revision (`:56-59`); without it the counter prints `present=0` and
  exits 1. But the *counter's* notion of "the tool ran" is satisfied by a stub that
  prints the four frozen case ids (§5.2). A stub on a tree with **no blobs, no ledger,
  no correction** reaches the full target line `present=1 selftest=4/4 frozen_cases=ok
  met=true`, exit 0 (C-stub). The counter does not pin the tool's sha256 and does not
  re-derive the selftest's own classifications. The C2 kill rule's phrase "a stub tool
  passes" is met by measurement.

---

## 8. Artifacts left behind

None outside this report. Scratch root
`/fast/scratch/hyaku/kake-r63/ExecDoNothingControl/` (fixtures `donothing/`, `empty/`,
`markerfixture/`, `fix/`, `fix2/`, `fix3/`, `fix4/`, `fix5/`, `fix6/` and the
`mkfix*.py` drivers) was deleted at the end of the seat. `scratch_cleanup=clean`.
