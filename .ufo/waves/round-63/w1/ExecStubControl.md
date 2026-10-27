# Seat ExecStubControl — round-63 w1

**Item:** build a stub `scripts/quote_class.py` in a scratch clone that prints a fake
selftest JSON with the four frozen case ids marked passed (constant output, no
classification), point `c63_quote_tool.py` at a scratch git repo containing it
(plus the real fixtures), and confirm the counter rejects it (`met=false`); then
explain which check caught it.

**Verdict: THE SEAT PREMISE IS FALSIFIED. THE STUB IS ACCEPTED, NOT REJECTED.**
A constant-output stub that performs no classification at all is scored
`present=1 selftest=4/4 frozen_cases=ok met=true` with **exit 0** by the frozen
C2 counter. No check caught it: the counter's guard that was supposed to catch
it — the `derived == expected` re-derivation clause — is **vacuous** when the
stub omits both fields, because `None == None` is `True`.

This is a measured counter defect, not a property of my stub. It is the same
class of defect as the round-62 routed defect (a counter whose predicate is
satisfied by an artifact that does not do the claimed work) and it lands
directly on the contract's C2 kill rule, quoted below.

**Scope note.** Read-only against the fleet repo
`/home/vgpnk/Projects/shokunin/kake-shokunin`. Nothing in the fleet repo,
`.ufo/state`, `scripts/`, `templates/`, the corpus or `SOURCES.md` was
modified; no git/jj mutation was performed against the fleet repo or any
sibling repo; no commit, push, deploy or external-state change was made. All
fixtures were built under `/fast/scratch/hyaku/kake-r63/ExecStubControl/` in
throwaway repos with a throwaway identity local to each fixture, and the
scratch directory was deleted at the end of the seat. This report file is the
only path written outside scratch.

**Tools installed:** none. No `pacman` transaction was run (pacman is paused
host-wide).

---

## 1. The contract clause my finding lands on

`.ufo/waves/round-63/contract.md:66-72` (C2 — operability):

> - Controls: `base-c2.txt` (base → `present=0 met=false`); the counter's
>   frozen-case-set check rejects a stub selftest missing the four frozen case
>   ids (`inline_raw_substring`, `markup_collapsed_only`, `absent_everywhere`,
>   `s432_real`).
> - Kill rule: if the after receipt does not print `met=true`, or a stub tool
>   passes, C2 is `unprovable`.

The contract asserts the counter *rejects a stub*. My measurement: the stub
**passes**. The contract's own words — "a stub tool passes" — are not qualified
by "missing the four frozen case ids", so this is a contract-text hit, not
only a design observation. I report it; I do not adjudicate the claim.

## 2. What is being attacked

The frozen C2 counter, byte-verified against the contract:

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ sha256sum .ufo/waves/round-63/c63_quote_tool.py
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  .ufo/waves/round-63/c63_quote_tool.py
$ git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:.ufo/waves/round-63/c63_quote_tool.py | sha256sum
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  -
```

Both match the contract's frozen counter sha256 `9fcbfad0…f01e` exactly.

Its decision path (`c63_quote_tool.py`):

| Line | Check |
|------|-------|
| `:56-58` | `git show <rev>:scripts/quote_class.py` → `None` ⇒ `present=0 met=false` |
| `:63-66` | blob written to temp dir, run as `python3 -B <tmp>/quote_class.py --selftest --json` with `cwd=root` |
| `:68-70` | `proc.returncode != 0` ⇒ `selftest=failed met=false` |
| `:72-74` | `json.loads(proc.stdout)` raises ⇒ `selftest=unparseable met=false` |
| `:76-81` | `frozen_ok`: every id in `FROZEN_CASE_IDS` has `passed is True` **and** `derived == expected` |
| `:84-85` | `met = bool(result.get("ok") and frozen_ok and total == passed and total == len(FROZEN_CASE_IDS))` |

Two properties matter for my attack:

1. The counter **never hashes the tool blob**. `grep -n "hashlib\|sha256" .ufo/waves/round-63/c63_quote_tool.py` → **no matches**. The contract's frozen tool sha256 `431e75e8…1f14` is never checked by the counter, so tool *provenance* is unverified.
2. The counter **never checks that the tool read anything**. It cannot: the tool is run from a temp dir, and the tool's own stdout is the only evidence.

## 3. Method

One throwaway git repo under `/fast/scratch/hyaku/kake-r63/ExecStubControl/`
holding the real retained fixtures (`scripts/fixtures/quote-class/*`,
`.ufo/waves/round-61/sources/S432.html`, `.ufo/waves/round-63/quote-class/S432.txt`)
plus the frozen counter; the `scripts/quote_class.py` blob is then replaced
per variant and committed. The top-level assertion is enforced before the
first commit:

```
$ git -C /fast/scratch/hyaku/kake-r63/ExecStubControl/repo rev-parse --show-toplevel
/fast/scratch/hyaku/kake-r63/ExecStubControl/repo     # == $D, asserted
```

Every result below was produced with the **fleet's** frozen counter
(`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_quote_tool.py`,
sha256 `9fcbfad0…f01e`) invoked against the scratch repo — not against a
scratch copy of the counter — so the counter under test is the committed one.

**Control V0 (real tool, real fixtures, scratch repo) — green, as it must be:**

```
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_quote_tool.py \
      --root . --revision 6248efa72876e0a5562c048d7fa2924f1a827ecb
revision=6248efa72876e0a5562c048d7fa2924f1a827ecb present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

## 4. THE ATTACK — stub accepted, `met=true`

The stub, exactly as the item specifies: constant output, no classification, no
file reads, the four frozen case ids marked passed.

```python
#!/usr/bin/env python3
"""Stub quote-class tool: constant output, no classification."""
import json, os, sys
FROZEN = ["inline_raw_substring", "markup_collapsed_only",
          "absent_everywhere", "s432_real"]
CASES = [{"id": cid, "passed": True} for cid in FROZEN]
RESULT = {"cases": CASES, "total": len(CASES),
          "passed": len(CASES), "ok": True,
          "_sentinel": "STUB_EXECUTED_no_corpus_read"}
with open(os.path.join(os.getcwd(), "STUB_RAN.txt"), "w") as fh:
    fh.write("stub executed; cwd=%s; argv=%r\n" % (os.getcwd(), sys.argv))
print(json.dumps(RESULT, sort_keys=True))
sys.exit(0)
```

Result, run with the fleet's frozen counter:

```
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_quote_tool.py \
      --root . --revision 67c0b67185da50e919e502b992bbe7509fca6805
revision=67c0b67185da50e919e502b992bbe7509fca6805 present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

**The stub is accepted. `met=true`, exit 0.** The item's expected `met=false`
did not occur.

### 4.1 Proof the stub bytes are what actually ran

Three independent proofs, so this cannot be dismissed as a harness artifact:

```
$ git show 67c0b67185da50e919e502b992bbe7509fca6805:scripts/quote_class.py | sha256sum
25adda1a9c9100bc2aca0ac5422b6b44f1d5d8e29bdb92144a1458bd4d2e7640  -
$ git show 67c0b67185da50e919e502b992bbe7509fca6805:scripts/quote_class.py | head -8
#!/usr/bin/env python3
"""Stub quote-class tool: constant output, no classification, sentinel proof."""
import json, os, sys
FROZEN = ["inline_raw_substring", "markup_collapsed_only",
          "absent_everywhere", "s432_real"]
CASES = [{"id": cid, "passed": True} for cid in FROZEN]
RESULT = {"cases": CASES, "total": len(CASES),
          "passed": len(CASES), "ok": True,
```

The stub's own side-effect file appeared in the scratch root:

```
$ ls -la STUB_RAN.txt && cat STUB_RAN.txt
-rw-r--r-- 1 vgpnk vgpnk 135 Oct 27 10:31 STUB_RAN.txt
stub executed; cwd=/fast/scratch/hyaku/kake-r63/ExecStubControl/repo; argv=['/tmp/tmpe1qwqz9h/quote_class.py', '--selftest', '--json']
```

The `argv` path is a temp dir — i.e. the counter wrote the blob there
(`c63_quote_tool.py:62-63`) and ran it — and `cwd` is the counter's `--root`,
exactly as `c63_quote_tool.py:64-66` specifies.

### 4.2 The same stub greens with NO corpus in the tree at all

To show the counter is not reading evidence even in the present case, the stub
was committed into a tree containing only the stub and the counter — no
fixtures, no S432.html, no S432.txt:

```
$ find . -path ./.git -prune -o -type f -print | sort
./scripts/quote_class.py
./STUB_RAN.txt
./.ufo/waves/round-63/c63_quote_tool.py

$ python3 -B .../c63_quote_tool.py --root . --revision 1834ae3d1c467af2455d7358652d7c21f2f9a6d9
revision=1834ae3d1c467af2455d7358652d7c21f2f9a6d9 present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

Contrast: the **real** frozen tool in the same corpus-less tree fails
correctly, because it actually tries to open the blobs:

```
$ python3 -B .../c63_quote_tool.py --root . --revision 9ea7ed639eaa261e648dcf4ffe5a26e97ba19cdd
revision=9ea7ed639eaa261e648dcf4ffe5a26e97ba19cdd present=1 selftest=failed met=false
exit=1

$ python3 -B scripts/quote_class.py --selftest --json
{"cases": [{"derived": "unevaluable", "error": "FileNotFoundError: [Errno 2] No such file or directory: '.../scripts/fixtures/quote-class/inline.raw.html'", "expected": "raw-substring", "id": "inline_raw_substring", "passed": false}, ...]
```

So the counter *does* reject the honest tool when the corpus is missing — it
rejects for the wrong reason and lets the dishonest tool through.

## 5. WHICH CHECK CAUGHT IT — the answer is *none*, and here is why

The item asks which check caught the stub. **None did.** The check that was
supposed to catch it, `frozen_ok`'s second conjunct, is vacuous against this
stub. `c63_quote_tool.py:77-81`:

```python
frozen_ok = all(
    cases.get(cid, {}).get("passed") is True
    and cases.get(cid, {}).get("derived") == cases.get(cid, {}).get("expected")
    for cid in FROZEN_CASE_IDS
)
```

The stub's case dicts are `{"id": cid, "passed": True}` — **no `derived` key, no
`expected` key**. So `cases.get(cid, {}).get("derived")` is `None` and
`cases.get(cid, {}).get("expected")` is `None`, and the clause evaluates
**`None == None` → `True`**.

Isolated proof of the mechanism, running the counter's own expression over
each stub's case list:

```
v1 both fields OMITTED       derived=None               expected=None               frozen_ok=True
v11 both fields NULL         derived=None               expected=None               frozen_ok=True
v2 consistent strings        derived='collapsed-only'   expected='collapsed-only'   frozen_ok=True
v3 derived!=expected         derived='raw-substring'    expected='collapsed-only'   frozen_ok=False
v9 only expected             derived=None               expected='collapsed-only'   frozen_ok=False
```

`None == None` is `True` in Python, so a stub that omits the fields entirely —
or sets both to null — satisfies the "independent re-derivation" clause
without deriving anything. The clause is only ever violated when the stub
supplies two **different** non-null values, or exactly one of them.

The remaining conjuncts also all pass for free: `result.get("ok")` is `True`
(stub-supplied), `total == passed` (both `4`), `total == len(FROZEN_CASE_IDS)`
(`4 == 4`), `proc.returncode == 0` (stub exits 0), stdout is valid JSON.

**Conclusion.** `frozen_ok` does not re-derive the class from the blobs — it
compares two strings the tool itself supplied, and it is satisfied by their
joint absence. The counter therefore validates the tool's *self-report*, not
the tool's *behaviour*, and it never validates the tool's *identity* (no sha256
check against the contract's `431e75e8…1f14`).

## 6. Full measured matrix — 11 stub variants

Every row produced with the fleet's frozen counter against the scratch repo.

| # | Variant | Counter line | met | exit | Result |
|---|---------|--------------|-----|------|--------|
| v1 | **stub, four frozen ids, both fields omitted** | `present=1 selftest=4/4 frozen_cases=ok met=true` | **true** | **0** | **ACCEPTED (the assigned attack)** |
| v2 | stub, four ids, self-consistent derived==expected | `present=1 selftest=4/4 frozen_cases=ok met=true` | **true** | **0** | **ACCEPTED** |
| v11 | stub, four ids, derived=null expected=null | `present=1 selftest=4/4 frozen_cases=ok met=true` | **true** | **0** | **ACCEPTED** |
| v12 | stub, `ok` = string `"false"` | `present=1 selftest=4/4 frozen_cases=ok met=true` | **true** | **0** | **ACCEPTED** |
| v3 | stub, `derived != expected` on every case | `present=1 selftest=4/4 frozen_cases=missing met=false` | false | 1 | rejected |
| v9 | stub, only `expected` present | `present=1 selftest=4/4 frozen_cases=missing met=false` | false | 1 | rejected |
| v10 | stub, only `derived` present | `present=1 selftest=4/4 frozen_cases=missing met=false` | false | 1 | rejected |
| v4 | stub, only 2 of the 4 frozen ids | `present=1 selftest=2/2 frozen_cases=missing met=false` | false | 1 | rejected |
| v5 | stub, 5 cases (4 frozen + 1 extra) | `present=1 selftest=5/5 frozen_cases=ok met=false` | false | 1 | rejected |
| v6 | stub, `ok=false` (bool) | `present=1 selftest=4/4 frozen_cases=ok met=false` | false | 1 | rejected |
| v7 | stub, one case `passed=false` | `present=1 selftest=3/4 frozen_cases=missing met=false` | false | 1 | rejected |

Four of eleven stub shapes are accepted. Note the **inversion**: v3/v9/v10 — the
shapes that *do* carry derived/expected fields but disagree — are rejected,
while v1/v11, which carry **no classification information whatsoever**, are
accepted. The counter's strictness is inversely correlated with the stub's
honesty: a stub that reports *something* is checked, a stub that reports
*nothing* is waved through. That is the vacuous-`None == None` defect showing
itself across the matrix.

v5 also shows `total == len(FROZEN_CASE_IDS)` (`:85`) is a live guard against
padding the case list, and v6 shows `result.get("ok")` (`:84`) is a live guard
against a bool `ok=false`.

### 6.1 A second, independent hole: `ok` truthiness

v12 sets `"ok": "false"` — the **string**. `result.get("ok")` at `:84` is a
truthiness test, and `"false"` is a truthy string in Python, so the counter
greens a tool that means "not ok". `"ok": 0` and `"ok": []` correctly yield
`met=false` (falsy); only truthy non-bool values slip through. An
`is True` check would close it.

## 7. Does this reach the committed receipts?

**No — the committed receipts are truthful.** The after-state receipt was
produced against the measured commit, whose tool blob is the real frozen tool,
sha256-verified:

```
$ git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:scripts/quote_class.py | sha256sum
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  -
```

matches the contract's frozen tool sha256 exactly. Re-measured read-only in the
fleet repo, both receipts reproduce byte-for-byte:

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
exit=0

$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa present=0 selftest=unevaluable met=false
exit=1
```

So this is a **counter-design defect that the receipts do not exercise** — the
same shape as the round-62 routed defect, where the counter's predicate was
satisfied by an artifact that did not do the claimed work. Unlike round-62,
there is **no committed C2 stub control receipt** to catch it: the round-63
controls directory holds `after-c1.txt`, `after-c2.txt`, `base-c1.txt`,
`base-c2.txt`, `control-junk-fixture.txt`, `control-marker-fixture.txt` — the
two C2 control receipts (`base-c2.txt`, `after-c2.txt`) exercise *tool absence*
and the *real tool*, never a stub. `git ls-tree 05b0d7f4…:.ufo/waves/round-63/controls/`
confirms only four files were committed at the measured commit
(`base-c1.txt`, `base-c2.txt`, `control-junk-fixture.txt`,
`control-marker-fixture.txt`); the two after-state receipts were added
afterwards in `7f77d12b`. **No receipt in this round ever puts a stub tool in
front of `c63_quote_tool.py`.** That is the gap this seat fills with a
measurement.

## 8. Separability — C1 is unaffected (contract §Separability, confirmed)

The contract separates the claims: "C1 re-derives the match class inline from
the retained blobs (round-50 semantics) and never gates on
`scripts/quote_class.py`". Confirmed in the code and at runtime:

- `c63_calibration.py` inlines its own `classify()` (`:59-68`) and never
  references `scripts/quote_class.py` as a path — the only two mentions are
  prose in the docstring (`:15`) and an inline comment (`:61`).
- Running the C1 counter against my stub-tool scratch repo does not read the
  stub at all; it reports its own independent state
  (`could-not-evaluate: verifier spot-check absent`, exit 2 — because that
  scratch tree has no `corpus/` lesson/quality tree, not because of the stub).

So the stub defect is confined to **C2**; C1's calibration evidence is
unaffected by it, exactly as the contract's Separability clause requires.

## 9. Reproduction (exact)

```bash
# 0. scratch repo with real fixtures + frozen counter, stub as scripts/quote_class.py
D=/fast/scratch/hyaku/kake-r63/ExecStubControl/repo
mkdir -p "$D/scripts/fixtures/quote-class" "$D/.ufo/waves/round-61/sources" \
         "$D/.ufo/waves/round-63/quote-class" "$D/.ufo/waves/round-63"
cd "$D" && git init -q && git config user.email l@localhost && git config user.name L
test "$(git rev-parse --show-toplevel)" = "$D"        # assertion before first commit
cp -a /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/fixtures/quote-class/. scripts/fixtures/quote-class/
cp /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/sources/S432.html .ufo/waves/round-61/sources/
cp /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/quote-class/S432.txt .ufo/waves/round-63/quote-class/
cp /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_quote_tool.py .ufo/waves/round-63/

# 1. install the constant-output stub as scripts/quote_class.py, commit
#    (stub source in §4 of this report)
git add -A && git commit -qm "scratch: stub tool"
REV=$(git rev-parse HEAD)

# 2. run the FLEET's frozen counter against the scratch repo
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_quote_tool.py \
    --root "$D" --revision "$REV"; echo "exit=$?"
# -> revision=<REV> present=1 selftest=4/4 frozen_cases=ok met=true
# -> exit=0      <-- STUB ACCEPTED
```

## 10. Risk assessment and suggested repair (reported, not applied)

**Risk.** The C2 counter cannot distinguish the frozen tool from a stub that
prints a constant 4/4 green. Three independent gaps combine:

1. **No tool-identity check.** `c63_quote_tool.py` never hashes the tool blob
   against the contract's frozen `431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14`.
   A one-line `hashlib.sha256(tool_blob).hexdigest() == FROZEN_TOOL_SHA` closes
   the whole class, because it rejects *every* stub regardless of its JSON.
2. **Vacuous `derived == expected`.** `c63_quote_tool.py:79` accepts
   `None == None`. Requiring the keys to be present and non-null (e.g.
   `isinstance(derived, str) and derived == expected`) closes the omission
   route.
3. **`ok` truthiness.** `c63_quote_tool.py:84` accepts the string `"false"`.
   `result.get("ok") is True` closes it.

Gap 1 alone is sufficient and cheapest, and it is the check the contract
already specifies in prose (the tool's frozen sha256 is in the contract at
`contract.md:56` but is never used by the counter). Gaps 2 and 3 remain
worthwhile defence-in-depth for a counter that is meant to be robust against
hostile tools.

**Do not treat this as a C1 finding.** C1 is independent and unaffected (§8).

**Calibration note for the L1.** My seat's item asserted the expected outcome
(`met=false`); the measurement says otherwise. Under the contract's C2 kill
rule as written ("or a stub tool passes, C2 is `unprovable`"), a stub tool
passing the frozen C2 counter is a literal hit on the kill rule. Whether that
reading applies depends on whether the kill rule's "stub tool" means "a stub
in front of the counter" (my measurement: yes) or "a stub at the measured
revision" (no — the measured commit's tool is the real frozen tool,
sha256-verified, and the after receipt is truthful). I report both facts and
do not adjudicate: the counter has a demonstrable defect, and the committed
receipts are accurate for the commit they measure. Other seats in this wave
independently report the same class of finding (`ExecC2CounterAttack` §8.1/§8.2,
`SentinelFetchSecurity` F3), which suggests the L1 should treat it as a
consolidated counter-repair item rather than a single-seat artefact.

## 11. Cleanup and fleet integrity

- Scratch dir `/fast/scratch/hyaku/kake-r63/ExecStubControl/` (fixture repo,
  the no-corpus repo, the real-tool-no-corpus repo, and all stub sources)
  deleted at the end of the seat; `scratch_cleanup=clean`.
- Fleet repo `git status --porcelain` shows only the wave-harness paths the
  orchestrator itself created (`.ufo/waves/round-63/w1.ready`,
  `.ufo/waves/round-63/w1.ready.dispatched`, `.ufo/waves/round-63/w1/`); no
  tracked file was modified and no fleet-root tracked file (`LOG.md`,
  `SCORECARD.md`, `MANIFEST.json`, …) was written by this seat.
  `MANIFEST.json` and `considerthese/` were not touched; no commit, push,
  deploy or external-state change was made against the fleet repo or any
  sibling repo.
- No packages were installed (nothing to record); no `pacman` was invoked.
