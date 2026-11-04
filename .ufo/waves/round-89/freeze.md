# Round 89 — frozen claims (written before any after-state data)

Base revision `76225160d0dff8d2042fbcd037bd08b0971d5e07` (lane `master` tip at
round open). Two claims on distinct axes. The predicate below is one sentence:
it is the plan, it is the condition in each counter's `met` computation, and it
is the label in every receipt.

## C1 — calibration, the lowest owned non-retired axis (2, HOLD)

**Claim.** The six defects routed by the round-88 outside spot-check (R88-A
selftest number, R88-B gate sample counts, R88-C unbacked re-run claim,
R88-D unpinned count, R88-E freeze-after-dispatch, R88-F lesson shape) close,
re-derived from committed bytes by one counter.

**Predicate.** `C1v1 ... items=6 open=0 closed=6 met=true`, exit 0, at the
carrier; the same counter at the base prints `open=6 closed=0 met=false`,
exit 1.

**Counting command.**

```
TMPDIR=$(mktemp -d) python3 -B .ufo/waves/round-89/c89_defect_queue.py \
  --root . --revision <REV> --work "$TMPDIR/work"
```

**Kill rule.** Any of the six items with a non-empty failure list makes
`met=false` and exit 1. No item is scored from prose alone where a behaviour is
available: A runs the tool's own `--selftest`, B parses the round-88 `## Gate`
table, C resolves every named receipt path at the revision, D recounts at the
named revision, E reads two commit objects, F parses the lesson table.

**Do-nothing control.** The base receipt `controls/base-c1.txt` is the control:
committing nothing prints `open=6 closed=0 met=false`, exit 1. A round that only
writes prose that names the six defect ids without closing them keeps every item
open (the counter reads the repo, not the round's own claims).

## C2 — freshness, bounded capability acquisition (10, HOLD)

**Claim.** The lane can construct the canonical stored-response key that a
presented request maps to under a `Vary` field: names lowercased, members
sorted, values trimmed and otherwise byte-exact, separators escaped so distinct
logical inputs cannot collide, absent distinguished from present-empty,
malformed input and the `*` wildcard refused.

**Predicate.** `C2v1 ... frozen=16/16 props=200/200 refuse=9/9 controls=5/5
met=true`, exit 0, at the carrier; the same counter at the base prints
`frozen=0/16 props=0/200 refuse=0/9 controls=5/5 met=false`, exit 1.

**Counting command.**

```
TMPDIR=$(mktemp -d) python3 -B .ufo/waves/round-89/c89_key.py \
  --root . --revision <REV> --candidate scripts/cache_key.py --work "$TMPDIR/work"
```

**Kill rule.** Any shortfall in the four counts makes `met=false`, exit 1. The
property population is generated at scoring time from the seed printed in the
receipt (`seed=89089`), so a table over the committed 16 cases cannot reach it
(measured: the committed `ctl-table.py` scores 0 properties and is rejected by
the shortcut guard; a plain frozen-case table is rejected by the property
population in the counter's own selftest).

**Do-nothing control.** The base receipt `controls/base-c2.txt` prints
`frozen=0/16 props=0/200 refuse=0/9 met=false` (candidate absent), exit 1.
Committed shortcut stubs — constant key, naive join, request representation,
counter import, case table — are each rejected in that same receipt
(`controls=5/5`).

## Freeze contents

`.ufo/waves/round-89/c89_defect_queue.py` (C1 counter, selftest 12/12),
`.ufo/waves/round-89/c89_key.py` (C2 counter and reference, selftest 43/43),
`.ufo/waves/round-89/c2-contract.md` (the declared key form and worked
examples), `.ufo/waves/round-89/frozen/c2-cases.json` (the 16 hand cases),
`.ufo/waves/round-89/controls/ctl-*.py` (the five shortcut stubs) and the base
receipts.

The freeze commit is the commit that first adds `c89_key.py`; item E of C1
requires it to be an ancestor of the commit that first adds
`.ufo/waves/round-89/w1.ready` with an earlier committer time. That is the
round-88 R88-E repair, measured on this round's own commits.

## Not claimed

No storability, freshness, revalidation, reuse or serving decision; no claim
about what any server, CDN or browser does with a key. No whole-corpus no-harm
claim. The counter's shortcut guard is textual and is disclosed as such; a
candidate that imports the reference under another name is not detected.
