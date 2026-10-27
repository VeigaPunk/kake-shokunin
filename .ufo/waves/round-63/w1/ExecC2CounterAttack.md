# Seat ExecC2CounterAttack — round-63 w1

**Item:** attack `.ufo/waves/round-63/c63_quote_tool.py` (the C2 operability
counter) with four hostile tool shapes — (a) a tool that exits 0 but prints
`ok=false`; (b) a tool with 5 cases where a frozen id is missing; (c) a tool
whose `s432_real` case has `derived != expected` but `passed=true`; (d) a tool
printing valid JSON to stderr and nothing to stdout. Each must land
`met=false`.

**Verdict: ALL FOUR ASSIGNED ATTACKS LAND `met=false` (exit 1).** The
counter's four defences each hold under the specific attack aimed at it.

**Scope note.** Read-only against the fleet repo
`/home/vgpnk/Projects/shokunin/kake-shokunin`. Nothing in the fleet repo, the
`.ufo/state`, `scripts/`, `templates/`, the corpus or `SOURCES.md` was
modified; no git/jj mutation was performed against the fleet repo or any
sibling repo. All fixtures were built under
`/fast/scratch/hyaku/kake-r63/ExecC2CounterAttack/` in throwaway repos with a
throwaway identity local to each fixture, and were deleted at the end of the
seat. This report file is the only path written outside scratch.

**Tools installed:** none. No `pacman` transaction was run (pacman is paused
host-wide).

---

## 1. What is being attacked

The frozen C2 counter, unmodified:

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_quote_tool.py`
- sha256 `9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e`
  — matches the contract's frozen hash exactly.

Its decision path (`c63_quote_tool.py:46-115`):

1. `git show <rev>:scripts/quote_class.py` → `tool_blob`; `None` ⇒
   `present=0 met=false` (exit 1).
2. The blob is written to a temp dir and run as
   `python3 -B <tmp>/quote_class.py --selftest --json` with `cwd=root`.
3. `proc.returncode != 0` ⇒ `selftest=failed met=false` (exit 1).
4. `json.loads(proc.stdout)` raises ⇒ `selftest=unparseable met=false` (exit 1).
5. `cases = {c.get("id"): c for c in result.get("cases", [])}`; `frozen_ok`
   requires every id in `FROZEN_CASE_IDS` to have `passed is True` **and**
   `derived == expected` (`:92-98`).
6. `met = bool(result.get("ok") and frozen_ok and total == passed and
   total == len(FROZEN_CASE_IDS))` (`:99-101`).

Baseline re-measurement before attacking (the counter is byte-identical to
the committed receipt `.ufo/waves/round-63/controls/after-c2.txt`):

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa present=0 selftest=unevaluable met=false
exit=1

$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

The tool blob at the measured commit is the frozen tool, hash-verified:

```
$ git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:scripts/quote_class.py | sha256sum
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  -
```
(matches the contract's frozen tool sha256 `431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14`).

---

## 2. Method

Each attack is a fresh throwaway git repo under
`/fast/scratch/hyaku/kake-r63/ExecC2CounterAttack/<attack>/` containing the
mutated `scripts/quote_class.py` plus the retained blobs the tool binds to
(`scripts/fixtures/quote-class/*`, `.ufo/waves/round-61/sources/S432.html`,
`.ufo/waves/round-63/quote-class/S432.txt`), committed once. The
`rev-parse --show-toplevel` assertion is enforced in the generator before
the first commit:

```
$ git -C "$D" rev-parse --show-toplevel
/fast/scratch/hyaku/kake-r63/ExecC2CounterAttack/a-ok-false      # == $D, asserted
```

Generator: `/fast/scratch/hyaku/kake-r63/ExecC2CounterAttack/mkfixtures.py`
(scratch only; deleted with the scratch dir at the end). Each fixture's
mutation is a minimal, surgical edit of the frozen tool — the real
`classify()`, the real fixture files and the real `s432_real` quote are kept,
so the attack is aimed at the counter's *decision logic*, not at a broken
tool.

Because the counter reads the tool **from the git revision** and runs it with
`cwd=root`, the counter is exercised end-to-end exactly as the contract's
counting command would.

---

## 3. Attack (a) — tool exits 0 but prints `ok=false`

Mutation: in `run_selftest`, `"ok": passed == total` → `"ok": False`, and the
`--selftest` return changed from `return 0 if result["ok"] else 1` to
`return 0` so the tool really does exit 0. All four cases genuinely pass;
only the top-level `ok` flag is false.

Tool output (`a-ok-false`, rev `d8f5cf6e5f87f0accdb6d59db83982d3c4b3a36d`):

```
{"cases": [{"derived": "raw-substring", "expected": "raw-substring", "id": "inline_raw_substring", "passed": true}, {"derived": "collapsed-only", "expected": "collapsed-only", "id": "markup_collapsed_only", "passed": true}, {"derived": "absent", "expected": "absent", "id": "absent_everywhere", "passed": true}, {"derived": "collapsed-only", "expected": "collapsed-only", "id": "s432_real", "passed": true}], "ok": false, "passed": 4, "total": 4}
```

Counter:

```
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root a-ok-false --revision d8f5cf6e5f87f0accdb6d59db83982d3c4b3a36d
revision=d8f5cf6e5f87f0accdb6d59db83982d3c4b3a36d present=1 selftest=4/4 frozen_cases=ok met=false
exit=1
```

**RESULT: `met=false`, exit 1. PASS.** Note the trap this closes: the printed
`selftest=4/4 frozen_cases=ok` is the tool's *self-report*, and a reader
skimming the receipt would see "4/4" and "ok". The counter does not trust
it — `result.get("ok")` is a required conjunct of `met` (`c63_quote_tool.py:99`),
so a self-reporting `ok=false` is fatal. The `present=1 selftest=4/4
frozen_cases=ok met=false` shape is exactly the round-62 failure mode (a
half-green receipt) and the counter does not produce it here.

## 4. Attack (b) — tool with 5 cases where a frozen id is missing

Mutation: `s432_real` replaced by two extra cases (`extra_fourth_case`,
`extra_fifth_case`), so the tool has 5 cases, all passing, `ok=true`, but
`FROZEN_CASE_IDS` is not fully covered — `s432_real` is absent.

Tool output (`b-missing-frozen-id`, rev `12d4254760062c2c2425ab90ed0af35b06a7ec95`):

```
{"cases": [{"derived": "raw-substring", "expected": "raw-substring", "id": "inline_raw_substring", "passed": true}, {"derived": "collapsed-only", "expected": "collapsed-only", "id": "markup_collapsed_only", "passed": true}, {"derived": "absent", "expected": "absent", "id": "absent_everywhere", "passed": true}, {"derived": "raw-substring", "expected": "raw-substring", "id": "extra_fourth_case", "passed": true}, {"derived": "collapsed-only", "expected": "collapsed-only", "id": "extra_fifth_case", "passed": true}], "ok": true, "passed": 5, "total": 5}
```

Counter:

```
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root b-missing-frozen-id --revision 12d4254760062c2c2425ab90ed0af35b06a7ec95
revision=12d4254760062c2c2425ab90ed0af35b06a7ec95 present=1 selftest=5/5 frozen_cases=missing met=false
exit=1
```

**RESULT: `met=false`, exit 1. PASS.** Two independent guards fire: the
`frozen_ok` case-set check (`c63_quote_tool.py:92-98`) reports
`frozen_cases=missing`, and `total == len(FROZEN_CASE_IDS)` (5 ≠ 4) also
fails. A tool that pads its case list to reach `5/5` does not buy a green.

## 5. Attack (c) — `s432_real` has `derived != expected` but `passed=true`

Mutation: two edits to the frozen tool. (i) `s432_real`'s `raw` blob is
repointed from `.ufo/waves/round-61/sources/S432.html` to a new fixture
`scripts/fixtures/quote-class/s432.raw.html` that *contains* the S432 quote
verbatim, so the derivation becomes `raw-substring` while `expected` stays
`collapsed-only`. (ii) the tool's own verdict is made dishonest:
`passed = error is None and derived == case["expected"]` →
`passed = error is None`. The tool now reports `passed=true` on a case it
actually got wrong — the lying-selftest shape.

Tool output (`c-derived-mismatch`, rev `64e6e9af23b8126be68ac7c7ea1c250c1128ad67`):

```
{"cases": [{"derived": "raw-substring", "expected": "raw-substring", "id": "inline_raw_substring", "passed": true}, {"derived": "collapsed-only", "expected": "collapsed-only", "id": "markup_collapsed_only", "passed": true}, {"derived": "absent", "expected": "absent", "id": "absent_everywhere", "passed": true}, {"derived": "raw-substring", "expected": "collapsed-only", "id": "s432_real", "passed": true}], "ok": true, "passed": 4, "total": 4}
```

(`s432_real`: `derived=raw-substring`, `expected=collapsed-only`,
`passed=true` — the contradiction the attack is built to smuggle past.)

Counter:

```
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root c-derived-mismatch --revision 64e6e9af23b8126be68ac7c7ea1c250c1128ad67
revision=64e6e9af23b8126be68ac7c7ea1c250c1128ad67 present=1 selftest=4/4 frozen_cases=missing met=false
exit=1
```

**RESULT: `met=false`, exit 1. PASS.** This is the most important of the
four, because it is the only one where the tool lies *successfully* about
itself: `ok=true`, `total=4`, `passed=4`, `frozen_cases` fully present, and
every `passed` flag true. The counter still rejects it because `frozen_ok`
requires `derived == expected` **independently** of the tool's own `passed`
flag (`c63_quote_tool.py:92-98`):

```python
frozen_ok = all(
    cases.get(cid, {}).get("passed") is True
    and cases.get(cid, {}).get("derived") == cases.get(cid, {}).get("expected")
    for cid in FROZEN_CASE_IDS
)
```

The counter re-derives the invariant `derived == expected` itself rather
than accepting the tool's `passed` claim. This is the correct defence and
it holds. (Note the receipt renders this as `frozen_cases=missing`, which is
slightly imprecise wording for "a frozen case is absent **or** inconsistent" —
a cosmetic point only; the met=false outcome is correct and the counter
exits 1.)

## 6. Attack (d) — valid JSON on stderr, nothing on stdout

Mutation: `print(json.dumps(result, sort_keys=True))` →
`print(json.dumps(result, sort_keys=True), file=sys.stderr)`, and the
`--selftest` exit forced to 0. The tool emits a complete, valid, fully-green
selftest document — just on the wrong stream.

Tool stdout is empty (0 bytes); the stderr payload is valid JSON:

```
$ (cd d-json-on-stderr && python3 -B scripts/quote_class.py --selftest --json 2>/tmp/d_err.txt 1>/tmp/d_out.txt)
stdout bytes=0 stderr bytes=446
$ python3 -c "import json;d=json.load(open('/tmp/d_err.txt'));print('stderr IS valid JSON, keys=',sorted(d))"
stderr IS valid JSON, keys= ['cases', 'ok', 'passed', 'total']
```

Counter (`d-json-on-stderr`, rev `ba68b25f528167baeedf314b049673259d364a2c`):

```
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root d-json-on-stderr --revision ba68b25f528167baeedf314b049673259d364a2c
revision=ba68b25f528167baeedf314b049673259d364a2c present=1 selftest=unparseable met=false
exit=1
```

**RESULT: `met=false`, exit 1. PASS.** The counter parses `proc.stdout`
only (`c63_quote_tool.py:74`), never stderr, and treats an unparseable
stdout as fatal rather than falling back to stderr. A stream-confused tool
cannot talk its way to a green.

---

## 7. Summary of the four assigned attacks

| # | Attack | Counter output | met | exit | Result |
|---|--------|----------------|-----|------|--------|
| a | exits 0, prints `ok=false` | `present=1 selftest=4/4 frozen_cases=ok met=false` | false | 1 | **PASS** |
| b | 5 cases, frozen id missing | `present=1 selftest=5/5 frozen_cases=missing met=false` | false | 1 | **PASS** |
| c | `s432_real` derived≠expected, passed=true | `present=1 selftest=4/4 frozen_cases=missing met=false` | false | 1 | **PASS** |
| d | JSON on stderr only | `present=1 selftest=unparseable met=false` | false | 1 | **PASS** |

All four required attacks land `met=false` with exit 1. The counter's
defences that were aimed at are: `result.get("ok")` as a mandatory conjunct
(a), the frozen-id case-set check plus the `total == 4` conjunct (b), the
independent `derived == expected` re-derivation (c), and stdout-only parsing
(d). Each holds.

---

## 8. Additional findings (beyond the assigned four) — reported, not adjudicated

These were measured while attacking; they are outside my assigned item and
I did not change anything in response to them. They are reported because
they bear on how much the C2 green is worth, and the wave's L1 owns the
call.

### 8.1 A hardcoded stub tool greens the counter (`met=true`)

A ~20-line stub that never opens a corpus file — it simply prints a
fabricated 4/4 green selftest with the four frozen ids — is accepted:

```
$ (cd e-hardcoded-green && python3 -B scripts/quote_class.py --selftest --json)
{"cases": [{"derived": "raw-substring", "expected": "raw-substring", "id": "inline_raw_substring", "passed": true}, ...], "ok": true, "passed": 4, "total": 4}
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root e-hardcoded-green --revision 560851ec8016a91bd13d18e980a2899ffd4bb212
revision=560851ec8016a91bd13d18e980a2899ffd4bb212 present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

Same result with **no corpus in the tree at all** (`h-stub-no-corpus`,
rev `f0eec98c3cce6043acd154c00ec747e2b15c4947`): `present=1 selftest=4/4
frozen_cases=ok met=true`, exit 0.

This is a property of the counter's design, not a defect in the measured
commit: `c63_quote_tool.py` deliberately verifies *operability* ("the tool
runs and self-reports 4/4") and not *provenance*. It never compares the tool
blob's sha256 against the contract's frozen `431e75e8…`, and it never checks
that the tool actually read the corpus (`grep -n "sha256\|hashlib"
.ufo/waves/round-63/c63_quote_tool.py` → no matches). The contract's C2
kill rule says "if … a stub tool passes, C2 is `unprovable`" and names the
counter's frozen-case-set check as the stub defence — but a stub that
*emits* the four frozen ids defeats that check, because the check is on the
ids' presence, not on the tool's identity. Note the contract's own wording
("a stub tool passes") is not qualified by "missing the frozen ids", so this
reading is available on the contract text. I am not adjudicating it: the
measured commit's tool *is* the frozen tool (sha256-verified above), the
base→after receipts are correct, and the four assigned attacks all fail as
required — so this finding is a scope-of-the-guard observation for the L1,
not a falsification of the C2 receipt.

### 8.2 The `ok` field is checked for truthiness, not for `is True`

`result.get("ok")` accepts any truthy value. A tool emitting `"ok": "false"`
(the *string*) greens:

```
ok-string-false: tool ok='false' (str) -> counter: ... present=1 selftest=4/4 frozen_cases=ok met=true exit=0
```

(`"ok": 0` and `"ok": []` correctly yield `met=false`; only truthy non-boolean
values pass. This is the mirror image of attack (a) — a *string* `"false"` is
truthy in Python, so a tool that means "not ok" but serialises it wrongly
greens.) A `result.get("ok") is True` check would close it.

### 8.3 The counter's green binds to the working tree, not to the revision

The counter resolves the *tool* from the revision (`git show <rev>:…`) but
runs it with `cwd=root`, and the frozen tool binds its fixtures to the
invoking cwd (`scripts/quote_class.py:30` `LANE_ROOT = Path.cwd()`,
`FIXTURES = Path("scripts/fixtures/quote-class")`). So the corpus that
decides the outcome is read from the **checked-out working tree**, not from
the measured revision. Probe F demonstrates this with two revisions whose
tool blob is byte-identical and whose corpus differs:

```
tool blob identical at rev1/rev2: True
rev2 contains s432 corpus: False

== working tree at rev2 (corpus absent) ==
  --revision rev1: ... present=1 selftest=failed met=false   exit=1
  --revision rev2: ... present=1 selftest=failed met=false   exit=1

== working tree checked out at rev1 (corpus present) ==
  --revision rev1: ... present=1 selftest=4/4 frozen_cases=ok met=true   exit=0
  --revision rev2: ... present=1 selftest=4/4 frozen_cases=ok met=true   exit=0
```

i.e. measuring revision `rev2` — which *lacks* the S432 corpus — can print
`met=true` if the working tree happens to be at a revision that has it. For
the actual measurement this is benign: the corpus blobs are byte-identical
across the measured commit, the worktree HEAD and the working tree files
(verified: `.ufo/waves/round-61/sources/S432.html` = `63b0a018753c330a`,
`.ufo/waves/round-63/quote-class/S432.txt` = `8b90d096d2653ce5`, and all four
`scripts/fixtures/quote-class/*` blobs likewise, at all three points), and
the measured commit `05b0d7f4…` is an ancestor of the worktree HEAD
`15eb965c`. So the after-c2 receipt is not affected. The general shape —
counter measures a revision but resolves its evidence from the working tree
— is the same class of weakness as round-62's defect, and worth the L1's
attention if C2 is to be re-measured against a dirty tree.

### 8.4 Malformed case lists crash the counter instead of yielding `met=false`

Not part of my assigned item, but observed while probing the JSON surface:

```
j-cases-strings: stdout='' exit=1 stderr_last="AttributeError: 'str' object has no attribute 'get'"
k-cases-dict:     stdout='' exit=1 stderr_last="AttributeError: 'str' object has no attribute 'get'"
l-no-cases-key:   stdout='... present=1 selftest=4/4 frozen_cases=missing met=false' exit=1
m-null-cases:     stdout='' exit=1 stderr_last="TypeError: 'NoneType' object is not iterable"
```

In every case the process still exits 1 and never prints `met=true`, so
these are **not** false greens — the kill rule is not breached. But three of
the four produce an uncaught traceback and no `met=` line at all, so the
receipt shape a wave measurement expects (`present=… selftest=… met=…`) is
lost. The `cases` comprehension at `c63_quote_tool.py:92` and the
`result.get("cases", [])` default would need a type guard to make the
counter total.

---

## 9. Reproduction commands (exact)

```
# baseline
cd /home/vgpnk/Projects/shokunin/kake-shokunin
python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:scripts/quote_class.py | sha256sum
sha256sum .ufo/waves/round-63/c63_quote_tool.py

# attacks (fixture generator + driver, scratch only)
cd /fast/scratch/hyaku/kake-r63/ExecC2CounterAttack
python3 -B mkfixtures.py
for d in a-ok-false b-missing-frozen-id c-derived-mismatch d-json-on-stderr e-hardcoded-green; do
  rev=$(git -C "$d" rev-parse HEAD)
  python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_quote_tool.py \
      --root "$d" --revision "$rev"; echo "exit=$?"
done
```

## 10. Cleanup and fleet integrity

- Scratch dir `/fast/scratch/hyaku/kake-r63/ExecC2CounterAttack/` and all
  fixture repos under it were deleted at the end of this seat.
- Fleet repo `git status --porcelain` after the seat shows only the
  wave-harness paths (`.ufo/waves/round-63/w1.ready`,
  `.ufo/waves/round-63/w1.ready.dispatched`, `.ufo/waves/round-63/w1/`) that
  the orchestrator itself created; no tracked file was modified and no
  fleet-root tracked file (LOG.md, SCORECARD.md, MANIFEST.json, …) was
  written by this seat. `MANIFEST.json` and `considerthese/` were not
  touched; no commit, push, deploy or external-state change was made.
- No packages were installed (nothing to record); no `pacman` was invoked.
